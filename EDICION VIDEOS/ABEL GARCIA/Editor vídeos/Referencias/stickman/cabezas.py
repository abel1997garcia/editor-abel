"""Cabezas recortadas de Abel (pegatinas para el personaje stickman) a partir de fotogramas del vídeo.

Silueta con Robust Video Matting (el modelo de anim.py recortar), recorte por encima de la barbilla a partir de la
cara que detecta YuNet, y contorno negro + borde blanco de pegatina. Salida: caras/cabeza_<t>.png (RGBA).
    python cabezas.py 30 225 400
"""
import sys
from pathlib import Path
import numpy as np, cv2, torch
from PIL import Image, ImageFilter

SK = Path.home() / '.claude/skills/animaciones-horizontal-combinadas/scripts'
sys.path.insert(0, str(SK))
from recortar import modelo
from cortar import modelo_cara

TOMA = '../../Sin buena intención jamás obtendrás la bendición.mp4'
dev = 'cuda' if torch.cuda.is_available() else 'cpu'
rvm = modelo('resnet50', dev)
det = cv2.FaceDetectorYN.create(str(modelo_cara()), '', (1280, 720), 0.7, 0.3, 5)


def fotograma(t):
    cap = cv2.VideoCapture(TOMA); cap.set(cv2.CAP_PROP_POS_MSEC, t * 1000); ok, f = cap.read()
    return f


def alfa(bgr, t):
    """silueta: RVM es de vídeo, así que se le dan 12 fotogramas previos para que la silueta se asiente"""
    rec = [None] * 4
    cap = cv2.VideoCapture(TOMA); cap.set(cv2.CAP_PROP_POS_MSEC, max(0, t - .4) * 1000)
    for _ in range(13):
        ok, f = cap.read()
        if not ok: break
        x = torch.from_numpy(cv2.cvtColor(f, cv2.COLOR_BGR2RGB)).permute(2, 0, 1)[None].float().div(255).to(dev)
        with torch.no_grad():
            fgr, pha, *rec = rvm(x, *rec, downsample_ratio=.4)
    return (pha[0, 0].cpu().numpy() * 255).astype(np.uint8)


def cabeza(t):
    bgr = fotograma(t)
    _, caras = det.detect(bgr)
    x, y, w, h = [int(v) for v in max(caras, key=lambda c: c[2] * c[3])[:4]]
    a = alfa(bgr, t)
    # caja de la cabeza: pelo por arriba, orejas a los lados, corte un poco por debajo de la barbilla
    x0, x1 = max(0, x - int(.45 * w)), min(1280, x + w + int(.45 * w))
    y0, y1 = max(0, y - int(.75 * h)), min(720, y + h + int(.12 * h))
    a = a[y0:y1, x0:x1].copy()
    # el corte inferior, redondeado como una barbilla (no una línea recta en el cuello)
    H, W = a.shape; yy, xx = np.mgrid[0:H, 0:W]
    elipse = ((xx - W / 2) / (W * .5)) ** 2 + ((yy - H * .45) / (H * .56)) ** 2 <= 1
    a = np.where(elipse, a, 0).astype(np.uint8)
    rgb = cv2.cvtColor(bgr[y0:y1, x0:x1], cv2.COLOR_BGR2RGB)
    cara = Image.fromarray(np.dstack([rgb, a]), 'RGBA')
    # pegatina: borde blanco y, por fuera, el contorno negro del trazo del dibujo
    m = Image.fromarray(a).filter(ImageFilter.GaussianBlur(1.2))
    P = 22
    lienzo = Image.new('RGBA', (W + 2 * P, H + 2 * P), (0, 0, 0, 0))
    def capa(radio, color):
        mm = Image.new('L', lienzo.size, 0); mm.paste(m, (P, P))
        mm = mm.filter(ImageFilter.MaxFilter(radio * 2 + 1)).filter(ImageFilter.GaussianBlur(1)).point(lambda v: 255 if v > 110 else 0)
        mm = mm.filter(ImageFilter.GaussianBlur(.8))
        return Image.composite(Image.new('RGBA', lienzo.size, color), Image.new('RGBA', lienzo.size, (0, 0, 0, 0)), mm)
    lienzo = Image.alpha_composite(lienzo, capa(9, (17, 17, 17, 255)))
    lienzo = Image.alpha_composite(lienzo, capa(5, (255, 255, 255, 255)))
    lienzo.alpha_composite(cara, (P, P))
    Path('caras').mkdir(exist_ok=True)
    lienzo.save(f'caras/cabeza_{t}.png')
    print('caras/cabeza_%s.png' % t, lienzo.size)


for t in sys.argv[1:]:
    cabeza(float(t) if '.' in t else int(t))
