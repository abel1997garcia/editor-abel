"""Diapositivas de CARRUSEL de Abel (ref. @jun_yuh). Guía única: Drive CARRUSELES/RUTINA_CARRUSELES.md.
Cada diapositiva: foto (o fotograma) recortada en 3:4 (1080x1440), encuadrada en la cara (o en `foco`), y el texto en letra
blanca Montserrat sobre un degradado negro, sin tapar la cara.

    python carrusel.py carrusel.json            -> <salida>/01.png, 02.png… + descripcion.txt

carrusel.json:
{ "salida": "…/CARRUSELES/NN · tema (vN)", "descripcion": "texto del post",
  "diapositivas": [ { "foto": "ruta", "titular": "inicia la frase", "lineas": ["la continúa", ...],
                      "posicion": "abajo|arriba", "foco": [x, y], "columna": "izq|der" } ] }
*palabra* = destacada en negrita.
"""
import json, sys
from pathlib import Path
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageOps

AQUI = Path(__file__).resolve().parent
FUENTE = AQUI.parent / 'fuentes' / 'Montserrat-Variable.ttf'
L, ALTO = 1080, 1440              # 3:4: la cuadrícula del perfil de Instagram lo enseña entero, sin recortar (Abel 13/10/2026; antes 1:1)
MARGEN, PAD_X, PAD_Y, RADIO, ESPACIO = 64, 20, 12, 12, 18
TAM_TIT, TAM_LIN = 54, 32


def fuente(tam, peso):
    f = ImageFont.truetype(str(FUENTE), tam)
    try: f.set_variation_by_name(peso)
    except Exception: pass
    return f


def cara(img):
    """centro y caja de la cara más grande (0-1), o None"""
    sys.path.insert(0, str(Path.home() / '.claude/skills/animaciones-horizontal-combinadas/scripts'))
    from cortar import modelo_cara                      # el mismo detector YuNet que usan los reels
    g = cv2.cvtColor(np.array(img.convert('RGB')), cv2.COLOR_RGB2BGR)
    esc = 1000 / max(g.shape[:2]); g = cv2.resize(g, None, fx=esc, fy=esc); H, W = g.shape[:2]
    det = cv2.FaceDetectorYN.create(str(modelo_cara()), '', (W, H), 0.7, 0.3, 5)
    _, caras = det.detect(g)
    if caras is None or not len(caras): return None
    x, y, w, h = max(caras, key=lambda c: c[2] * c[3])[:4]
    return ((x + w / 2) / W, (y + h / 2) / H, x / W, y / H, (x + w) / W, (y + h) / H)


def cuadrado(img, foco=None, alto_cara=.42):
    """recorte 3:4 lo más grande posible, centrado en la cara (o en `foco`); devuelve la imagen y la caja de la cara en el recorte"""
    img = ImageOps.exif_transpose(img).convert('RGB'); W, H = img.size
    an, al = (W, W * ALTO / L) if W / H <= L / ALTO else (H * L / ALTO, H)
    c = cara(img)
    cx, cy = foco or ((c[0], c[1]) if c else (.5, .45))     # «foco» manda: lo importante de la foto (una placa, un objeto…)
    x0 = int(min(max(cx * W - an / 2, 0), W - an)); y0 = int(min(max(cy * H - al * (alto_cara if not foco else .5), 0), H - al))
    rec = img.crop((x0, y0, int(x0 + an), int(y0 + al))).resize((L, ALTO), Image.LANCZOS)
    caja = None
    if c: caja = ((c[2] * W - x0) / an * L, (c[3] * H - y0) / al * ALTO, (c[4] * W - x0) / an * L, (c[5] * H - y0) / al * ALTO)
    return rec, caja


def trozos(texto):
    """'hola *mundo* ya' -> [('hola', False), ('mundo', True), ('ya', False)] palabra a palabra"""
    import re
    texto = re.sub(r'(\d[\d.,]*) (\S)', lambda m: m.group(1) + ' ' + m.group(2), texto)     # una cifra nunca se separa de lo que cuenta («30 kilos», «17.000 €»)
    out, partes = [], texto.split('*')
    for i, p in enumerate(partes):
        for k, w in enumerate(p.split(' ')):
            if not w: continue
            if k == 0 and out and not partes[i - 1].endswith(' '): out[-1] = (out[-1][0] + w.replace(' ', ' '), out[-1][1])   # «*vivido*.»: el punto, pegado
            else: out.append((w.replace(' ', ' '), i % 2 == 1))
    return out


def lineas_de(texto, f, ancho):
    """reparte las palabras en el mínimo de líneas que quepan, con las líneas lo más IGUALADAS posible (nada de una palabra sola abajo)"""
    ws, n = trozos(texto), 1
    largo = lambda grupo: f.getlength(' '.join(w for w, _ in grupo))
    while True:
        objetivo = largo(ws) / n + 1; ls, act = [], []
        for w in ws:
            if act and (largo(act + [w]) > ancho or (largo(act + [w]) > objetivo * 1.08 and len(ls) < n - 1)): ls.append(act); act = []
            act.append(w)
        ls.append(act)
        if all(largo(l) <= ancho for l in ls) and len(ls) <= n: return ls
        n += 1


def pinta_bloque(img, y, texto, f, alineado, x0=MARGEN, ancho_max=L - 2 * MARGEN, color=(255, 255, 255)):
    """Abel 13/10/2026: letra BLANCA, sin cajas («parece un pegote»); detrás va el difuminado (difuminar()). Devuelve la y siguiente."""
    lns = lineas_de(texto, f, ancho_max)
    asc, desc = f.getmetrics(); lh = int((asc + desc) * 1.08)
    d = ImageDraw.Draw(img)
    fb = fuente(f.size, 'ExtraBold')                                           # *palabra* = resaltada en negrita blanca (de vez en cuando)
    for k, ln in enumerate(lns):
        ancho = sum((fb if dst else f).getlength(w) for w, dst in ln) + f.getlength(' ') * (len(ln) - 1)
        x = x0 if alineado == 'izq' else x0 + ancho_max - ancho
        for w, dst in ln:
            ff, cc = (fb, (255, 255, 255)) if dst else (f, color)
            d.text((x + 1, y + k * lh + 2), w, font=ff, fill=(0, 0, 0)); d.text((x, y + k * lh), w, font=ff, fill=cc)   # sombra mínima
            x += ff.getlength(w) + f.getlength(' ')
    return y + lh * len(lns)


def difuminar(img, zona, lado):
    """Abel 13/10/2026: SOMBREADO NEGRO entero detrás del texto (nada de desenfoque: «parece un cuadrado difuminado»).
    Un degradado a negro desde el borde donde va el texto, a todo lo ancho (o a todo lo alto si va en columna)."""
    x0, y0, x1, y1 = zona; yy, xx = np.mgrid[0:ALTO, 0:L]
    if lado in ('abajo', 'arriba'):
        a, b = (y0 - 220, y1) if lado == 'abajo' else (y1 + 220, y0)
        m = np.clip((yy - a) / (b - a), 0, 1)
    else:
        a, b = (x0 - 220, x1) if lado == 'der' else (x1 + 220, x0)
        m = np.clip((xx - a) / (b - a), 0, 1) * np.clip((yy - (y0 - 200)) / 240, 0, 1)   # solo a la altura del texto: la cara queda limpia
    m = (m ** 1.2) * .82
    base = np.array(img, np.float32) * (1 - m[..., None])
    return Image.fromarray(np.clip(base, 0, 255).astype(np.uint8))


def alto_bloques(dia, ft, fl, ancho_max=L - 2 * MARGEN):
    h = 0
    for texto, f in [(dia.get('titular', ''), ft)] + [(l, fl) for l in dia.get('lineas', [])]:
        if not texto: continue
        asc, desc = f.getmetrics(); h += int((asc + desc) * 1.08) * len(lineas_de(texto, f, ancho_max)) + ESPACIO
    return h - ESPACIO


def diapositiva(dia, ruta):
    pos = dia.get('posicion', 'abajo')                  # por defecto abajo, con la cara en el tercio de arriba
    img, caja = cuadrado(Image.open(dia['foto']), dia.get('foco'), .30 if pos == 'abajo' else .62)
    ft, fl = fuente(TAM_TIT, 'Bold'), fuente(TAM_LIN, 'Medium')
    # «columna»: 'izq' o 'der' = el texto en media foto (para fotos donde a lo ancho taparía la cara o lo importante)
    col = dia.get('columna'); am = int(L * .58) if col else L - 2 * MARGEN
    x0 = MARGEN if col != 'der' else L - MARGEN - am; al = 'der' if col == 'der' else 'izq'
    h = alto_bloques(dia, ft, fl, am)
    y = MARGEN if pos == 'arriba' else ALTO - MARGEN - h
    if caja and pos == 'abajo' and y < caja[3] + 10: print(f'  AVISO {ruta.name}: el texto roza la cara (prueba "arriba" o menos texto)')
    if caja and pos == 'arriba' and y + h > caja[1] - 10: print(f'  AVISO {ruta.name}: el texto roza la cara (prueba "abajo" o menos texto)')
    img = difuminar(img, (x0, y, x0 + am, y + h), col or pos)
    if dia.get('titular'): y = pinta_bloque(img, y, dia['titular'], ft, al, x0, am) + ESPACIO
    for l in dia.get('lineas', []):                     # cada frase pequeña, su párrafo (como Jun Yuh): la historia se lee a golpes
        y = pinta_bloque(img, y, l, fl, al, x0, am, (235, 235, 235)) + ESPACIO
    img.save(ruta, quality=95)


if __name__ == '__main__':
    cfg = json.load(open(sys.argv[1], encoding='utf-8')); sal = Path(cfg['salida']); sal.mkdir(parents=True, exist_ok=True)
    for i, dia in enumerate(cfg['diapositivas'], 1):
        diapositiva(dia, sal / f'{i:02d}.png'); print(f'{i:02d}.png')
    if cfg.get('descripcion'): (sal / 'descripcion.txt').write_text(cfg['descripcion'].strip() + '\n', encoding='utf-8')
    print('->', sal)
