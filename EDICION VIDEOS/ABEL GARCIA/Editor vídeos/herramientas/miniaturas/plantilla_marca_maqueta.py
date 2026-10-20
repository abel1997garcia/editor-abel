"""Maquetas de la plantilla de marca de Abel (para elegir el formato fijo). Uso: python plantilla_marca_maqueta.py
Usa dos miniaturas de prueba de ChatGPT (pizarra y platos) solo como material; salida en Miniaturas/_plantilla_marca/."""
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont
from rembg import remove, new_session

AQUI = Path(__file__).parent
TMP = Path(r'C:\Users\Clap\AppData\Local\Temp\claude\C--Users-Clap-Desktop-EDICION-VIDEOS-ABEL-GARCIA-Editor-v-deos\d7cbc795-7ce8-4682-b768-22bda44decfe\images')
OUT = AQUI.parent.parent / 'Miniaturas' / '_plantilla_marca'; OUT.mkdir(parents=True, exist_ok=True)
FB = str(AQUI.parent / 'fuentes' / 'Montserrat-Black.ttf')
W, H = 1280, 720
AZUL = (46, 123, 255); NAVY = (5, 14, 38)


def fondo():
    y, x = np.mgrid[0:H, 0:W]
    d = np.hypot((x - 900) / 700, (y - 330) / 520)
    g = np.clip(1 - d, 0, 1) ** 1.6
    base = np.array(NAVY, float)[None, None] * (1 - g[..., None]) + np.array(AZUL, float)[None, None] * g[..., None] * 0.95
    return Image.fromarray(base.clip(0, 255).astype(np.uint8))


def abel_recortado(src, caja):
    im = Image.open(src).convert('RGB').resize((W, H))
    cut = remove(im, session=new_session('birefnet-portrait'))
    return cut.crop(caja)


def brillo_borde(fig, color=AZUL, r=18):
    a = fig.split()[3].filter(ImageFilter.GaussianBlur(r))
    glow = Image.new('RGBA', fig.size, color + (0,)); glow.putalpha(a.point(lambda v: min(255, int(v * 1.4))))
    return glow


def texto(img, l1, l2, x, y, s1=92, s2=92, caja=True):
    d = ImageDraw.Draw(img)
    f1, f2 = ImageFont.truetype(FB, s1), ImageFont.truetype(FB, s2)
    sombra = Image.new('RGBA', img.size, (0, 0, 0, 0)); ds = ImageDraw.Draw(sombra)
    ds.text((x + 4, y + 6), l1, font=f1, fill=(0, 0, 0, 200))
    img.alpha_composite(sombra.filter(ImageFilter.GaussianBlur(6)))
    d.text((x, y), l1, font=f1, fill='white')
    y2 = y + s1 + 14
    bb = d.textbbox((x, y2), l2, font=f2)
    if caja:
        d.rounded_rectangle((bb[0] - 18, bb[1] - 12, bb[2] + 18, bb[3] + 14), 14, fill=AZUL)
        d.text((x, y2), l2, font=f2, fill='white')
    else:
        d.text((x, y2), l2, font=f2, fill=AZUL)


def tarjeta(img, elem, caja, borde=AZUL):
    x0, y0, x1, y1 = caja
    e = elem.resize((x1 - x0, y1 - y0))
    m = Image.new('L', e.size, 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, *e.size), 22, fill=255)
    glow = Image.new('RGBA', img.size, (0, 0, 0, 0)); ImageDraw.Draw(glow).rounded_rectangle((x0 - 6, y0 - 6, x1 + 6, y1 + 6), 26, outline=borde + (255,), width=8)
    img.alpha_composite(glow.filter(ImageFilter.GaussianBlur(10)))
    img.paste(e, (x0, y0), m)
    ImageDraw.Draw(img).rounded_rectangle((x0, y0, x1, y1), 22, outline=borde, width=4)


pizarra = Image.open(TMP / '45.webp').convert('RGB').resize((W, H))
esquema = pizarra.crop((20, 300, 720, 660))
abel = abel_recortado(TMP / '45.webp', (640, 0, W, H))      # Abel sonriendo, señalando

# V1 · TARJETA (estructura tipo Gemma y Patri): texto arriba, el elemento en una tarjeta, Abel a la derecha
v1 = fondo().convert('RGBA')
tarjeta(v1, esquema, (40, 300, 650, 680))
fig = abel.resize((int(abel.width * 1.05), int(abel.height * 1.05)))
v1.alpha_composite(brillo_borde(fig), (W - fig.width + 20, H - fig.height)); v1.alpha_composite(fig, (W - fig.width + 20, H - fig.height))
texto(v1, 'DI NO', 'SIN CULPA', 50, 40, 100, 86)
v1.convert('RGB').save(OUT / 'V1_tarjeta.png')

# V2 · PIZARRA DE MARCA: su pizarra con el esquema ocupa la izquierda, fondo azul, texto encima con caja azul
v2 = fondo().convert('RGBA')
tarjeta(v2, pizarra.crop((0, 290, 730, 680)), (30, 250, 700, 690), borde=(255, 255, 255))
v2.alpha_composite(brillo_borde(fig, r=26), (W - fig.width + 20, H - fig.height)); v2.alpha_composite(fig, (W - fig.width + 20, H - fig.height))
texto(v2, 'DI NO', 'SIN CULPA', 50, 30, 110, 92, caja=False)
v2.convert('RGB').save(OUT / 'V2_pizarra.png')

# V3 · ESCENA COTIDIANA con la firma: la escena, el ambiente virado a azul, texto con caja azul
import cv2
e0 = np.asarray(Image.open(TMP / '46.webp').convert('RGB').resize((W, H)))
mk = np.zeros((H, W), np.uint8); mk[0:250, 800:W] = 255
esc = cv2.inpaint(e0, mk, 9, cv2.INPAINT_TELEA).astype(float)
esc[0:250, 800:W] = cv2.GaussianBlur(esc[0:250, 800:W], (0, 0), 12)
grad = np.clip((np.arange(W) - 420) / 500, 0, 1)[None, :, None] * 0.55
tinte = esc * (1 - grad) + (esc * 0.55 + np.array(AZUL) * 0.45) * grad
v3 = Image.fromarray(tinte.clip(0, 255).astype(np.uint8)).convert('RGBA')
texto(v3, 'NADIE', 'TE VE', 760, 40, 110, 110)
v3.convert('RGB').save(OUT / 'V3_escena.png')

hoja = Image.new('RGB', (W, H * 3 + 40), 'white')
for i, n in enumerate(('V1_tarjeta', 'V2_pizarra', 'V3_escena')): hoja.paste(Image.open(OUT / f'{n}.png'), (0, i * (H + 20)))
hoja.save(OUT / 'comparar.png')
print(OUT)
