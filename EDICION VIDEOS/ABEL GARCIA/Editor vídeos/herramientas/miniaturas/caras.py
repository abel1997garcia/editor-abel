"""Busca en las grabaciones de Abel los momentos con más emoción para la miniatura.

  python caras.py <vídeo> [--cada 0.5] [--top 24]

Puntúa cada fotograma (blendshapes de MediaPipe) en varias emociones, descarta los movidos
y los que no miran a cámara, y hace una hoja de contactos por emoción en <vídeo>_caras/.
Luego se saca el fotograma bueno a resolución completa con:  python caras.py <vídeo> --sacar 343.3
"""
import sys, json, subprocess, pathlib
import numpy as np, cv2
import mediapipe as mp
from mediapipe.tasks.python import vision, BaseOptions
from PIL import Image, ImageDraw, ImageFont

AQUI = pathlib.Path(__file__).resolve().parent
MODELO = str(AQUI / "modelos" / "face_landmarker.task")
FUENTE = str(AQUI.parent / "pizarra" / "assets" / "fonts" / "Inter-Variable.ttf")

EMOCIONES = {   # blendshape: peso   (positivo suma, negativo resta)
    "sorpresa":    {"jawOpen": .8, "browInnerUp": 1.2, "browOuterUpLeft": .6, "browOuterUpRight": .6, "eyeWideLeft": 1, "eyeWideRight": 1},
    "intensidad":  {"browDownLeft": 1, "browDownRight": 1, "eyeSquintLeft": .5, "eyeSquintRight": .5, "jawOpen": -1.2, "mouthSmileLeft": -.8, "mouthSmileRight": -.8},
    "complice":    {"mouthSmileLeft": 1, "mouthSmileRight": 1, "jawOpen": -1.5, "eyeSquintLeft": .3, "eyeSquintRight": .3, "mouthPressLeft": .3, "mouthPressRight": .3},
    "preocupacion": {"browInnerUp": 1.2, "mouthFrownLeft": 1, "mouthFrownRight": 1, "mouthPressLeft": .5, "mouthPressRight": .5, "jawOpen": -.6, "mouthSmileLeft": -1, "mouthSmileRight": -1},
    "risa":        {"mouthSmileLeft": 1, "mouthSmileRight": 1, "jawOpen": .7, "eyeSquintLeft": .4, "eyeSquintRight": .4},
}
MIRADA = ["eyeLookOutLeft", "eyeLookOutRight", "eyeLookInLeft", "eyeLookInRight", "eyeLookUpLeft", "eyeLookUpRight", "eyeLookDownLeft", "eyeLookDownRight"]


def probe(v):
    o = json.loads(subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height:stream_side_data=rotation:format=duration",
                                   "-of", "json", v], capture_output=True, text=True).stdout)
    return float(o["format"]["duration"])


def analizar(video, cada=.5):
    dur = probe(video)
    W = 960
    cmd = ["ffmpeg", "-v", "error", "-i", video, "-vf", f"fps={1/cada},scale={W}:-2", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"]
    # alto real tras escalar (los verticales del móvil salen con la rotación aplicada)
    p0 = subprocess.run(["ffmpeg", "-v", "error", "-ss", "1", "-i", video, "-frames:v", "1", "-vf", f"scale={W}:-2", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True)
    H = len(p0.stdout) // (W * 3)
    det = vision.FaceLandmarker.create_from_options(vision.FaceLandmarkerOptions(
        base_options=BaseOptions(model_asset_buffer=open(MODELO, "rb").read()), output_face_blendshapes=True, num_faces=1))
    pr = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    filas, i = [], 0
    while True:
        buf = pr.stdout.read(W * H * 3)
        if len(buf) < W * H * 3: break
        fr = np.frombuffer(buf, np.uint8).reshape(H, W, 3)
        r = det.detect(mp.Image(image_format=mp.ImageFormat.SRGB, data=np.ascontiguousarray(fr)))
        t = i * cada; i += 1
        if not r.face_blendshapes: continue
        bs = {c.category_name: c.score for c in r.face_blendshapes[0]}
        lm = r.face_landmarks[0]; xs = [p.x for p in lm]; ys = [p.y for p in lm]
        x0, x1, y0, y1 = int(min(xs) * W), int(max(xs) * W), int(min(ys) * H), int(max(ys) * H)
        cara = cv2.cvtColor(fr[max(y0, 0):y1, max(x0, 0):x1], cv2.COLOR_RGB2GRAY)
        if cara.size < 400: continue
        nitidez = cv2.Laplacian(cv2.resize(cara, (200, 200)), cv2.CV_64F).var()
        mirada = 1 - max(bs.get(k, 0) for k in MIRADA)            # 1 = mira a cámara
        ojos = 1 - max(bs.get("eyeBlinkLeft", 0), bs.get("eyeBlinkRight", 0))
        filas.append({"t": round(t, 2), "bs": bs, "nitidez": nitidez, "mirada": mirada, "ojos": ojos,
                      "caja": [x0 / W, y0 / H, x1 / W, y1 / H]})
    return filas, dur


def puntuar(filas):
    nits = np.array([f["nitidez"] for f in filas]); umbral = np.percentile(nits, 35)
    for f in filas:
        base = (f["nitidez"] >= umbral) * (f["ojos"] > .55) * (.5 + .5 * f["mirada"])
        f["emo"] = {e: base * sum(w * f["bs"].get(k, 0) for k, w in pesos.items()) for e, pesos in EMOCIONES.items()}


def hoja(video, filas, emocion, top, carpeta):
    # los mejores, separados al menos 4 s entre sí
    orden = sorted(filas, key=lambda f: -f["emo"][emocion]); elegidos = []
    for f in orden:
        if all(abs(f["t"] - e["t"]) > 4 for e in elegidos): elegidos.append(f)
        if len(elegidos) == top: break
    T, cols = 300, 6
    lienzo = Image.new("RGB", (cols * T, ((len(elegidos) + cols - 1) // cols) * (T + 30)), "white")
    d = ImageDraw.Draw(lienzo); fnt = ImageFont.truetype(FUENTE, 20)
    for k, f in enumerate(elegidos):
        fr = subprocess.run(["ffmpeg", "-v", "error", "-ss", str(f["t"]), "-i", video, "-frames:v", "1", "-f", "image2pipe", "-vcodec", "png", "-"], capture_output=True).stdout
        im = Image.open(__import__("io").BytesIO(fr)).convert("RGB"); w, h = im.size
        x0, y0, x1, y1 = f["caja"]; cx, cy = (x0 + x1) / 2 * w, (y0 + y1) / 2 * h; lado = (y1 - y0) * h * 2.1
        im = im.crop((int(cx - lado / 2), int(cy - lado * .42), int(cx + lado / 2), int(cy + lado * .58))).resize((T, T))
        x, y = (k % cols) * T, (k // cols) * (T + 30)
        lienzo.paste(im, (x, y)); d.text((x + 6, y + T + 3), f"{f['t']:.1f}s  {f['emo'][emocion]:.2f}", font=fnt, fill="#111")
    out = carpeta / f"{emocion}.jpg"; lienzo.save(out, quality=88); print(out)


def sacar(video, t):
    v = pathlib.Path(video); out = v.parent / f"{v.stem}_caras" / f"frame_{t}.png"; out.parent.mkdir(exist_ok=True)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(t), "-i", str(v), "-frames:v", "1", str(out)], check=True); print(out)


if __name__ == "__main__":
    a = sys.argv[1:]; video = a[0]
    if "--sacar" in a: [sacar(video, t) for t in a[a.index("--sacar") + 1:]]; sys.exit()
    cada = float(a[a.index("--cada") + 1]) if "--cada" in a else .5
    top = int(a[a.index("--top") + 1]) if "--top" in a else 24
    v = pathlib.Path(video); carpeta = v.parent / f"{v.stem}_caras"; carpeta.mkdir(exist_ok=True)
    cache = carpeta / "caras.json"
    if cache.exists(): filas = json.loads(cache.read_text())
    else: filas, _ = analizar(video, cada); cache.write_text(json.dumps(filas))
    print(len(filas), "fotogramas con cara")
    puntuar(filas)
    for e in EMOCIONES: hoja(video, filas, e, top, carpeta)
