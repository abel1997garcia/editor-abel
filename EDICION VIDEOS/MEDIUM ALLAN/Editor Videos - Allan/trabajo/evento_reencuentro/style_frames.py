"""Style frames (1920x1080) del vídeo de presentación del evento «El Reencuentro»."""
import math, random
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps

W, H = 1920, 1080
BASE = Path(r'C:\Users\Clap\Desktop\EDICION VIDEOS\MEDIUM ALLAN')
F = BASE / 'FOTOS ALLAN'
OUT = Path(__file__).parent / 'style_frames'; OUT.mkdir(exist_ok=True)
VF = r'C:\Users\Clap\AppData\Local\Google\Chrome\User Data\Profile 1\Extensions\jkkfeklkdokfnlfodkdafododleokdoa\4.2.1_0\Fonts\Montserrat\Montserrat-VariableFont_wght.ttf'
AZUL = (24, 64, 140); CIELO = (120, 190, 255); BLANCO = (255, 255, 255)


def fuente(t, p):
    f = ImageFont.truetype(VF, t)
    try: f.set_variation_by_axes([p])
    except Exception: pass
    return f


def fondo():
    """Azul noche con luz suave arriba y partículas de luz (como el logo)."""
    im = Image.new('RGB', (W, H))
    px = im.load()
    for y in range(H):
        for x in range(0, W, 4):
            d = math.hypot((x - W * .5) / W, (y - H * .25) / H)
            k = max(0, 1 - d * 1.6)
            c = tuple(int(8 + (a - 8) * k * .55) for a in (40, 90, 170))
            for i in range(4):
                if x + i < W: px[x + i, y] = c
    capa = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(capa)
    random.seed(3)
    for _ in range(140):
        x, y, r = random.randint(0, W), random.randint(0, H), random.choice([1, 1, 2, 3])
        d.ellipse((x - r, y - r, x + r, y + r), fill=(200, 230, 255, random.randint(60, 180)))
    capa = capa.filter(ImageFilter.GaussianBlur(1.2))
    im = im.convert('RGBA'); im.alpha_composite(capa)
    return im


def texto(im, lineas, cy, f, color=BLANCO, sombra=True, sep=16):
    d = ImageDraw.Draw(im)
    alto = len(lineas) * (f.size + sep)
    y = cy - alto / 2
    capa = Image.new('RGBA', im.size, (0, 0, 0, 0)); dc = ImageDraw.Draw(capa)
    for l in lineas:
        x = (W - d.textlength(l, font=f)) / 2
        if sombra: dc.text((x + 3, y + 5), l, font=f, fill=(0, 0, 0, 170))
        y += f.size + sep
    im.alpha_composite(capa.filter(ImageFilter.GaussianBlur(8)))
    y = cy - alto / 2
    for l in lineas:
        x = (W - d.textlength(l, font=f)) / 2
        d.text((x, y), l, font=f, fill=color)
        y += f.size + sep


def foto_tarjeta(im, ruta, caja, rot=0, borde=14):
    x0, y0, w, h = caja
    f = ImageOps.fit(ImageOps.exif_transpose(Image.open(ruta)).convert('RGB'), (w, h))
    t = Image.new('RGBA', (w + 2 * borde, h + 2 * borde), (250, 250, 250, 255)); t.paste(f, (borde, borde))
    t = t.rotate(rot, expand=True, resample=Image.BICUBIC)
    s = Image.new('RGBA', t.size, (0, 0, 0, 0)); s.paste((0, 0, 0, 140), mask=t.split()[3])
    im.alpha_composite(s.filter(ImageFilter.GaussianBlur(18)), (x0 + 12, y0 + 22))
    im.alpha_composite(t, (x0, y0))


def foto_full(ruta, oscuro=150, cy=.4):
    f = ImageOps.fit(ImageOps.exif_transpose(Image.open(ruta)).convert('RGB'), (W, H), centering=(.5, cy)).convert('RGBA')
    v = Image.new('L', (W, H), 0); dv = ImageDraw.Draw(v)
    for y in range(H):
        dv.line([(0, y), (W, y)], fill=int(oscuro * max(0, (y - H * .35) / (H * .65))))
    f.alpha_composite(Image.merge('RGBA', [Image.new('L', (W, H), 0)] * 3 + [v]))
    return f


# 1 · Las dudas (0:24-0:37): texto cinético sobre azul noche
im = fondo()
texto(im, ['¿Y si no viene nadie por mí?'], 470, fuente(78, 700))
texto(im, ['¿Y si me emociono delante de todos?'], 610, fuente(44, 400), color=(190, 215, 245))
im.convert('RGB').save(OUT / '1_las_dudas_0m24.jpg', quality=92)

# 2 · Su pasado (1:08): foto real como tarjeta + frase
im = fondo()
foto_tarjeta(im, F / 'WhatsApp Image 2026-10-14 at 6.35.09 PM(1).jpeg', (120, 170, 720, 720), rot=-3)
f = fuente(62, 700)
d = ImageDraw.Draw(im)
for i, l in enumerate(['Tuve un trabajo estable.', 'Un buen sueldo.']):
    d.text((990, 390 + i * 86), l, font=f, fill=BLANCO)
d.text((990, 590), 'Desde fuera, todo estaba bien.', font=fuente(40, 400), fill=(190, 215, 245))
im.convert('RGB').save(OUT / '2_su_trabajo_1m08.jpg', quality=92)

# 3 · El sueño (1:28): la foto de su abuela con resplandor
im = fondo()
glow = Image.new('RGBA', (W, H), (0, 0, 0, 0)); dg = ImageDraw.Draw(glow)
dg.ellipse((W / 2 - 430, 110, W / 2 + 430, 970), fill=(150, 200, 255, 120))
im.alpha_composite(glow.filter(ImageFilter.GaussianBlur(90)))
foto_tarjeta(im, F / 'WhatsApp Image 2026-10-14 at 6.57.03 PM.jpeg', (W // 2 - 260, 120, 520, 690))
texto(im, ['«Te voy a ayudar»'], 930, fuente(64, 600))
im.convert('RGB').save(OUT / '3_el_sueno_1m28.jpg', quality=92)

# 4 · Las sesiones (2:27): contador + collage de fotos con personas
im = fondo()
for k, (n, x, y, r) in enumerate([('1.jpg', 70, 120, -6), ('3.jpg', 1460, 90, 5), ('4.jpg', 90, 610, 4), ('6.jpg', 1450, 600, -4)]):
    foto_tarjeta(im, F / n, (x, y, 360, 360), rot=r, borde=10)
texto(im, ['+1.200'], 470, fuente(200, 800))
texto(im, ['sesiones'], 640, fuente(56, 500), color=(190, 215, 245))
im.convert('RGB').save(OUT / '4_sesiones_2m27.jpg', quality=92)

# 5 · La respiración (2:49): círculo que respira
im = fondo()
for r, a in [(330, 40), (270, 70), (210, 110)]:
    c = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ImageDraw.Draw(c).ellipse((W / 2 - r, H / 2 - r, W / 2 + r, H / 2 + r), outline=(180, 220, 255, a), width=4)
    im.alpha_composite(c.filter(ImageFilter.GaussianBlur(2)))
g = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ImageDraw.Draw(g).ellipse((W / 2 - 200, H / 2 - 200, W / 2 + 200, H / 2 + 200), fill=(120, 180, 255, 90))
im.alpha_composite(g.filter(ImageFilter.GaussianBlur(40)))
texto(im, ['Coge aire'], H / 2, fuente(76, 600))
im.convert('RGB').save(OUT / '5_respiracion_2m49.jpg', quality=92)

# 6 · El cierre (3:35): frase final + logo
im = fondo()
texto(im, ['El amor no muere.', 'Solo cambia de lugar.'], 360, fuente(72, 700))
logo = Image.open(BASE / 'Logotipo azul El Reencuentro.png').convert('RGBA'); logo.thumbnail((700, 400))
lm = Image.new('L', logo.size, 0); px = logo.load(); pm = lm.load()
for y in range(logo.height):
    for x in range(logo.width):
        r, g, b, a = px[x, y]; pm[x, y] = min(a, max(r, g, b) * 2)
logo.putalpha(lm)
im.alpha_composite(logo, ((W - logo.width) // 2, 620))
im.convert('RGB').save(OUT / '6_cierre_3m35.jpg', quality=92)

# hoja con las 6
fs = sorted(OUT.glob('[1-6]_*.jpg'))
hoja = Image.new('RGB', (2 * 960 + 30, 3 * 540 + 40), 'white')
for i, p in enumerate(fs):
    hoja.paste(Image.open(p).resize((960, 540)), ((i % 2) * 970 + 5, (i // 2) * 550 + 5))
hoja.save(OUT / '00_maqueta_estilo.jpg', quality=88)
print('ok', len(fs))
