"""Prepara a Abel para la miniatura como lo haría un editor (no solo recortar).

  python integrar.py <fotograma.png> <salida.png> [--fundido 0.30] [--calidez 0] [--borrar x0,y0,x1,y1 ...]

1. Recorte con rembg (birefnet-portrait) y borde afinado (sin halo blanco ni dientes de sierra).
2. Balance de blancos neutro: la pared del fondo de su plano debería ser blanca; se corrige la dominante.
3. Contraste en S, claridad (contraste local) y enfoque fino: que la cara «salte» en pequeño.
4. Fundido inferior: el cuerpo se disuelve en el blanco en vez de cortarse en seco (no parece pegatina).
Nunca se amplía con IA (deja la piel de plástico): la cara no debe pasar de ~1x su tamaño original.
"""
import sys, numpy as np, cv2
from PIL import Image
from rembg import remove, new_session


def integrar(src, dst, fundido=.30, calidez=0.0, borrar=()):
    im = Image.open(src).convert("RGB")
    if borrar:   # 0. retoque: quita manos movidas u objetos que distraen (rellena con lo de alrededor)
        bgr = cv2.cvtColor(np.asarray(im), cv2.COLOR_RGB2BGR); m = np.zeros(bgr.shape[:2], np.uint8)
        for x0, y0, x1, y1 in borrar: cv2.ellipse(m, ((x0 + x1) // 2, (y0 + y1) // 2), ((x1 - x0) // 2, (y1 - y0) // 2), 0, 0, 360, 255, -1)
        m = cv2.dilate(m, np.ones((9, 9), np.uint8))
        im = Image.fromarray(cv2.cvtColor(cv2.inpaint(bgr, m, 12, cv2.INPAINT_TELEA), cv2.COLOR_BGR2RGB))
    a = np.asarray(remove(im, session=new_session("birefnet-portrait")).split()[3]).astype(np.float32) / 255
    rgb = np.asarray(im).astype(np.float32) / 255

    # 2. balance de blancos con la zona de pared (píxeles de fondo claros y poco saturados)
    fondo = (a < .05) & (rgb.mean(2) > .6) & (rgb.max(2) - rgb.min(2) < .12)
    if fondo.sum() > 5000:
        ref = rgb[fondo].mean(0); rgb = rgb * (ref.mean() / ref)
    rgb[..., 0] *= 1 + calidez; rgb[..., 2] *= 1 - calidez

    # 3. exposición, contraste en S, claridad y enfoque (solo cuenta la persona)
    persona = a > .5
    med = np.median(rgb[persona].mean(1)); rgb = rgb * (.50 / max(med, .2)) ** .5          # que no quede apagado
    rgb = np.clip(rgb, 0, 1); rgb = rgb + .22 * (rgb - .5) * (1 - np.abs(2 * rgb - 1))       # S suave
    blur = cv2.GaussianBlur(rgb, (0, 0), 18); rgb = rgb + .35 * (rgb - blur)                  # claridad
    blur = cv2.GaussianBlur(rgb, (0, 0), 1.1); rgb = rgb + .6 * (rgb - blur)                  # enfoque fino
    hsv = cv2.cvtColor(np.clip(rgb, 0, 1).astype(np.float32), cv2.COLOR_RGB2HSV); hsv[..., 1] *= 1.08
    rgb = np.clip(cv2.cvtColor(hsv, cv2.COLOR_HSV2RGB), 0, 1)

    # 1b. borde: quita el halo del fondo (descontamina) y suaviza 1 px
    a = cv2.GaussianBlur(np.clip((a - .08) / .84, 0, 1), (0, 0), .8)
    # 4. fundido inferior en el último tramo de la persona
    filas = np.where(persona.any(1))[0]
    if len(filas) and fundido > 0:
        y1 = filas.max() + 1; y0 = int(y1 - (y1 - filas.min()) * fundido)
        g = np.ones(a.shape[0], np.float32); g[y0:y1] = np.linspace(1, 0, y1 - y0) ** 1.6; g[y1:] = 0
        a = a * g[:, None]

    out = np.dstack([rgb, a]); Image.fromarray((out * 255).astype(np.uint8), "RGBA").save(dst)
    print(dst)


if __name__ == "__main__":
    a = sys.argv[1:]
    f = float(a[a.index("--fundido") + 1]) if "--fundido" in a else .30
    c = float(a[a.index("--calidez") + 1]) if "--calidez" in a else 0
    b = [tuple(map(int, z.split(","))) for z in a[a.index("--borrar") + 1:] if "," in z] if "--borrar" in a else ()
    integrar(a[0], a[1], f, c, b)
