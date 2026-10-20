"""Mide el estilo visual de miniaturas (luz, contraste, color, cara, detalle) y compara grupos.
    python medir_miniaturas.py                 → referencias (MrBeast, Ibai) + pruebas de Abel → medidas_miniaturas.csv y resumen
    python medir_miniaturas.py img1.png ...    → mide esas imágenes y las compara con el rango de las referencias
"""
import csv, sys
from pathlib import Path
import cv2, numpy as np
import mediapipe as mp
from mediapipe.tasks.python import vision, BaseOptions
from sklearn.cluster import KMeans

AQUI = Path(__file__).parent
REF = AQUI.parent.parent / 'Referencias'
TMP = Path(r'C:\Users\Clap\AppData\Local\Temp\claude\C--Users-Clap-Desktop-EDICION-VIDEOS-ABEL-GARCIA-Editor-v-deos\d7cbc795-7ce8-4682-b768-22bda44decfe\images')
PRUEBAS = {'33': 'abel_bolsas_calle', '34': 'abel_cuaderno_OK', '35': 'abel_bolsas_v2', '36': 'abel_tarta_v1', '37': 'abel_bolsas_v3', '38': 'abel_tarta_v3'}

det = vision.FaceLandmarker.create_from_options(vision.FaceLandmarkerOptions(
    base_options=BaseOptions(model_asset_buffer=(AQUI / 'modelos' / 'face_landmarker.task').read_bytes()), num_faces=6))


def leer(p):
    im = cv2.imdecode(np.fromfile(str(p), np.uint8), cv2.IMREAD_COLOR)
    if im is None:   # webp u otros: vía PIL
        from PIL import Image
        im = cv2.cvtColor(np.array(Image.open(p).convert('RGB')), cv2.COLOR_RGB2BGR)
    h, w = im.shape[:2]; nh = w * 9 // 16
    if h > nh: im = im[(h - nh) // 2:(h - nh) // 2 + nh]
    return cv2.resize(im, (1280, 720), interpolation=cv2.INTER_AREA)


def caras(im):
    r = det.detect(mp.Image(image_format=mp.ImageFormat.SRGB, data=cv2.cvtColor(im, cv2.COLOR_BGR2RGB)))
    out = []
    for lm in r.face_landmarks:
        xs = [p.x for p in lm]; ys = [p.y for p in lm]
        x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys)
        out.append((x0, y0, x1, y1))
    return sorted(out, key=lambda b: -(b[3] - b[1]))


def medir(im):
    lab = cv2.cvtColor(im, cv2.COLOR_BGR2LAB).astype(np.float32)
    L = lab[..., 0] * 100 / 255
    hsv = cv2.cvtColor(im, cv2.COLOR_BGR2HSV).astype(np.float32)
    S, V, H = hsv[..., 1] / 255, hsv[..., 2] / 255, hsv[..., 0] * 2
    b, g, r = [im[..., i].astype(np.float32) for i in range(3)]
    rg, yb = r - g, 0.5 * (r + g) - b
    colorido = np.hypot(rg.std(), yb.std()) + 0.3 * np.hypot(rg.mean(), yb.mean())
    viv = (S > 0.5) & (V > 0.35)
    # familias de color (12 tonos de 30°) que ocupan > 4 % de la imagen entre píxeles con color
    fam = sum(1 for k in range(12) if (viv & (H >= k * 30) & (H < (k + 1) * 30)).mean() > 0.04)
    # colores dominantes (k-means en Lab, cuántos grupos superan el 8 %)
    px = lab[::8, ::8].reshape(-1, 3)
    km = KMeans(6, n_init=3, random_state=0).fit(px)
    dom = int((np.bincount(km.labels_, minlength=6) / len(px) > 0.08).sum())
    gris = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    bordes = cv2.Canny(gris, 80, 160) > 0
    d = dict(luz=L.mean(), luz_p10=np.percentile(L, 10), luz_p90=np.percentile(L, 90), oscuro_pct=(L < 20).mean() * 100,
             contraste=L.std(), saturacion=S.mean(), vivo_pct=viv.mean() * 100, colorido=colorido, familias_color=fam,
             colores_dom=dom, detalle=bordes.mean() * 100)
    cs = caras(im)
    if cs:
        x0, y0, x1, y1 = cs[0]
        X0, Y0, X1, Y1 = [int(max(0, min(1, v)) * s) for v, s in ((x0, 1280), (y0, 720), (x1, 1280), (y1, 720))]
        m = np.zeros(L.shape, bool); m[Y0:Y1, X0:X1] = True
        nit = lambda msk: cv2.Laplacian(gris, cv2.CV_64F)[msk].var()
        d.update(caras=len(cs), cara_alto_pct=(y1 - y0) * 100, cara_x=(x0 + x1) / 2, cara_y=(y0 + y1) / 2,
                 cara_luz_extra=L[m].mean() - L[~m].mean(), nitidez_cara_vs_fondo=nit(m) / max(nit(~m), 1e-6),
                 detalle_fondo=bordes[~m].mean() * 100)
    else:
        d.update(caras=0)
    return d


def grupo(nombre):
    if nombre == 'mrbeast': fs = [p for p in (REF / 'mrbeast_miniaturas').glob('*.jpg') if not p.name.startswith('hoja')]
    elif nombre == 'ibai': fs = [p for p in (REF / 'ibai_miniaturas').glob('i*.jpg')]
    else: fs = [TMP / f'{k}.webp' for k in PRUEBAS]
    return fs


CLAVES = ['luz', 'luz_p10', 'luz_p90', 'oscuro_pct', 'contraste', 'saturacion', 'vivo_pct', 'colorido', 'familias_color', 'colores_dom',
          'detalle', 'caras', 'cara_alto_pct', 'cara_x', 'cara_y', 'cara_luz_extra', 'nitidez_cara_vs_fondo', 'detalle_fondo']


def main():
    filas = []
    if len(sys.argv) > 1:
        objetivo = [(Path(a).name, 'nueva', Path(a)) for a in sys.argv[1:]]
    else:
        objetivo = []
    for g in ('mrbeast', 'ibai'):
        for f in grupo(g): objetivo.append((f.name, g, f))
    if len(sys.argv) == 1:
        for k, n in PRUEBAS.items(): objetivo.append((n, 'abel', TMP / f'{k}.webp'))
    for n, g, f in objetivo:
        d = medir(leer(f)); d.update(nombre=n, grupo=g); filas.append(d)
    with open(AQUI / 'medidas_miniaturas.csv', 'w', newline='', encoding='utf-8') as fh:
        w = csv.DictWriter(fh, ['grupo', 'nombre'] + CLAVES); w.writeheader()
        for d in filas: w.writerow({k: (round(d[k], 2) if isinstance(d.get(k), float) else d.get(k, '')) for k in ['grupo', 'nombre'] + CLAVES})
    print(f"{'medida':24s}" + ''.join(f'{g:>22s}' for g in ('mrbeast p25-med-p75', 'ibai p25-med-p75')))
    for k in CLAVES:
        lin = f'{k:24s}'
        for g in ('mrbeast', 'ibai'):
            v = [d[k] for d in filas if d['grupo'] == g and k in d]
            lin += f'{np.percentile(v, 25):7.1f}{np.median(v):7.1f}{np.percentile(v, 75):7.1f}' + ' '
        print(lin)
    print()
    otros = [d for d in filas if d['grupo'] in ('abel', 'nueva')]
    print(f"{'medida':24s}" + ''.join(f'{d["nombre"][:16]:>17s}' for d in otros))
    for k in CLAVES:
        print(f'{k:24s}' + ''.join(f'{d.get(k, float("nan")):17.1f}' for d in otros))


if __name__ == '__main__':
    main()
