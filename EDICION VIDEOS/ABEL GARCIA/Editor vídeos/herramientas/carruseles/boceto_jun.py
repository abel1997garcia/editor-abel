"""Boceto rápido de un carrusel estilo Jun Yuh: foto a sangre + letra blanca con sombra + una palabra en azul.

    python boceto_jun.py <carrusel.json> <carpeta_salida>
JSON: [{"foto": ruta, "grande": "...", "peque": "...", "azul": "palabra", "negra": false}, ...]
"""
import json, sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps

W, H = 1080, 1440
AZUL = (29, 78, 216)
VF = r'C:\Users\Clap\AppData\Local\Google\Chrome\User Data\Profile 1\Extensions\jkkfeklkdokfnlfodkdafododleokdoa\4.2.1_0\Fonts\Montserrat\Montserrat-VariableFont_wght.ttf'


def fuente(tam, peso):
    f = ImageFont.truetype(VF, tam)
    try:
        f.set_variation_by_axes([peso])
    except Exception:
        pass
    return f


def partir(d, txt, f, ancho):
    lineas, l = [], ''
    for p in txt.split():
        prueba = (l + ' ' + p).strip()
        if d.textlength(prueba, font=f) <= ancho:
            l = prueba
        else:
            lineas.append(l); l = p
    return lineas + [l] if l else lineas


def escribir(lienzo, lineas_f, y0, azul):
    capa = Image.new('RGBA', lienzo.size, (0, 0, 0, 0))
    sombra = Image.new('RGBA', lienzo.size, (0, 0, 0, 0))
    d, ds = ImageDraw.Draw(capa), ImageDraw.Draw(sombra)
    y = y0
    for txt, f, gap in lineas_f:
        for l in txt:
            x = (W - d.textlength(l, font=f)) / 2
            ds.text((x + 3, y + 4), l, font=f, fill=(0, 0, 0, 200))
            cx = x
            for i, p in enumerate(l.split(' ')):
                pal = p + (' ' if i < len(l.split(' ')) - 1 else '')
                if azul and p.strip('.,«»"…?¿').lower() == azul.strip('.,«»"…?¿').lower():
                    w = d.textlength(p, font=f)
                    d.rounded_rectangle((cx - 8, y - 2, cx + w + 8, y + f.size + 8), 10, fill=AZUL + (235,))
                d.text((cx, y), pal, font=f, fill=(255, 255, 255))
                cx += d.textlength(pal, font=f)
            y += f.size + 14
        y += gap
    lienzo.alpha_composite(sombra.filter(ImageFilter.GaussianBlur(6)))
    lienzo.alpha_composite(capa)


def encuadrar(im, TW=None, TH=None):
    """Recorta a 3:4 con SU cara entera arriba (YuNet). Devuelve (imagen, caja de la cara en el recorte o None)."""
    import cv2, numpy as np
    det = cv2.FaceDetectorYN.create(r'C:\Users\Clap\.cache\animaciones-con-voz\face_detection_yunet_2023mar.onnx', '', im.size, 0.7)
    _, f = det.detect(cv2.cvtColor(np.array(im), cv2.COLOR_RGB2BGR))
    TW, TH = TW or W, TH or H
    w, h = im.size
    cw, ch = (w, int(w * TH / TW)) if w / h < TW / TH else (int(h * TW / TH), h)
    caja = None
    if f is None:
        x0, y0 = (w - cw) // 2, (h - ch) // 2
    else:
        x, y, fw, fh = max(f, key=lambda c: c[2] * c[3])[:4]
        cx, cy = x + fw / 2, y + fh / 2
        x0 = int(min(max(cx - cw / 2, 0), w - cw))
        y0 = int(min(max(cy - ch * 0.30, 0), h - ch))
        k = TW / cw
        # cara + pelo (arriba) + barbilla (abajo)
        caja = ((x - x0) * k, (y - 0.35 * fh - y0) * k, (x + fw - x0) * k, (y + 1.15 * fh - y0) * k)
    return im.crop((x0, y0, x0 + cw, y0 + ch)).resize((TW, TH), Image.LANCZOS), caja


def degradado(base, y_ini, y_fin, abajo):
    """Sombra negra suave detrás del texto (de transparente a ~85 %)."""
    a = Image.new('L', (1, H), 0)
    for y in range(H):
        t = (y - y_ini) / max(1, y_fin - y_ini) if abajo else (y_fin - y) / max(1, y_fin - y_ini)
        a.putpixel((0, y), int(max(0, min(1, t)) ** 0.8 * 215))
    base.alpha_composite(Image.merge('RGBA', [Image.new('L', (W, H), 0)] * 3 + [a.resize((W, H))]))


def centrado(base, txt, f, cy):
    d = ImageDraw.Draw(base)
    lineas = partir(d, txt, f, W - 140)
    alto = len(lineas) * (f.size + 12)
    escribir(base, [(lineas, f, 0)], cy - alto / 2, None)


def partida(s):
    """Diapositiva partida (arriba el estado, abajo la acción), como la referencia."""
    base = Image.new('RGBA', (W, H))
    for i, k in enumerate(('arriba', 'abajo')):
        im = ImageOps.exif_transpose(Image.open(s[k])).convert('RGB')
        mitad, _ = encuadrar(im, W, H // 2)
        mitad = mitad.convert('RGBA')
        a = Image.new('L', (1, H // 2))
        for y in range(H // 2):
            a.putpixel((0, y), int(max(0, (y - H * 0.18) / (H * 0.32)) * 190))
        mitad.alpha_composite(Image.merge('RGBA', [Image.new('L', mitad.size, 0)] * 3 + [a.resize(mitad.size)]))
        base.paste(mitad, (0, i * H // 2))
    centrado(base, s['txt_arriba'], fuente(46, 500), H * 0.43)
    centrado(base, s['txt_abajo'], fuente(58, 800), H * 0.93)
    return base.convert('RGB')


def diapo(s):
    if s.get('arriba'):
        return partida(s)
    caja = None
    if s.get('negra'):
        base = Image.new('RGBA', (W, H), (12, 12, 12, 255))
    else:
        im = ImageOps.exif_transpose(Image.open(s['foto'])).convert('RGB')
        im, caja = encuadrar(im)
        base = im.convert('RGBA')
    d = ImageDraw.Draw(base)
    pq = s.get('peque') or []
    pq = [pq] if isinstance(pq, str) else pq
    for esc in (1, 0.92, 0.85, 0.78, 0.72):
        fg, fp = fuente(int(64 * esc), 800), fuente(int(38 * esc), 500)
        bloques = [(partir(d, s['grande'], fg, W - 160), fg, 28)] + [(partir(d, t, fp, W - 200), fp, 18) for t in pq]
        alto = sum(len(l) * (f.size + 14) + gap for l, f, gap in bloques)
        if s.get('negra'):
            y0, abajo = (H - alto) / 2, True; break
        if caja is None:
            y0, abajo = H - alto - 90, True; break
        abajo_libre = (H - 70) - (caja[3] + 30)
        arriba_libre = (caja[1] - 30) - 70
        if alto <= abajo_libre:
            y0, abajo = H - alto - 70, True; break
        if alto <= arriba_libre:
            y0, abajo = 70, False; break
    else:
        y0, abajo = (H - alto - 70, True) if abajo_libre >= arriba_libre else (70, False)
    if not s.get('negra'):
        if abajo:
            degradado(base, y0 - 260, y0 + alto * 0.6, True)
        else:
            degradado(base, y0 + alto * 0.4, y0 + alto + 260, False)
    escribir(base, bloques, y0, s.get('azul'))
    return base.convert('RGB')


datos = json.loads(Path(sys.argv[1]).read_text(encoding='utf-8'))
out = Path(sys.argv[2]); out.mkdir(parents=True, exist_ok=True)
mini = []
for i, s in enumerate(datos, 1):
    im = diapo(s)
    im.save(out / f'{i:02d}.jpg', quality=90)
    mini.append(im.resize((270, 360)))
cols = 5
hoja = Image.new('RGB', (cols * 280, ((len(mini) + cols - 1) // cols) * 370), 'white')
for i, m in enumerate(mini):
    hoja.paste(m, ((i % cols) * 280 + 5, (i // cols) * 370 + 5))
hoja.save(out / '00_hoja.jpg', quality=88)
print('ok', len(datos))
