"""Guiones TABLET → imagen VERTICAL con fondo NEGRO (PNG + PDF) para importar en Miro y grabar con la tablet
(va en la zona derecha del formato tablet). La FORMA sale del concepto del guion (Abel 19/10/2026): lista,
escalera, dos columnas, ranking, batería… Estilo común: SIEMPRE fondo negro puro (sin cajas grises), Montserrat, texto blanco, anillos amarillos,
rojo = lo que resta. Lo más simple posible: solo la información de los puntos (sin título, sin cabeceras extra ni frase final).
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

FUENTES = Path(__file__).parent / 'fuentes'
OUT = Path.home() / 'Desktop' / 'EDICION VIDEOS' / 'LISTAS MIRO'
FB, FX = str(FUENTES / 'Montserrat-Black.ttf'), str(FUENTES / 'Montserrat-ExtraBold.ttf')
AMARILLO, ROJO, GRIS, LINEA = (255, 212, 0), (240, 80, 80), (150, 150, 155), (90, 90, 96)
VERDE = (46, 204, 113)   # psicología del color (Abel 19/10/2026): VERDE = lo que suma / importa / funciona; ROJO = lo que resta; AMARILLO = neutro (numeración)
W, H = 1080, 1760          # proporción de la zona derecha del formato tablet (≈ 460 × 750)


def _f(size, negra=False):
    return ImageFont.truetype(FB if negra else FX, int(size))


def _texto(d, xy, t, maxw, size, color='white', anchor='lm', negra=False):
    while _f(size, negra).getlength(t) > maxw and size > 20: size -= 2
    d.text(xy, t, font=_f(size, negra), fill=color, anchor=anchor)


def _comun(textos, maxw, size, negra=False):
    """un solo tamaño para todos los puntos: el que cabe en el más largo (si no, cada uno salía de un tamaño)"""
    while size > 20 and any(_f(size, negra).getlength(t) > maxw for t in textos): size -= 2
    return size


def _anillo(d, cx, cy, r, n, color=AMARILLO, relleno='black', num='white'):
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=relleno, outline=color, width=max(5, int(r * .16)))
    d.text((cx, cy + 2), str(n), font=_f(r, True), fill=num, anchor='mm')


def transparente(im):
    """SIN FONDO en ningún diseño de TABLET (Abel 19/10/2026: nada que parezca un pegote): el negro → transparente, los colores se quedan"""
    import numpy as np
    g = np.asarray(im.convert('RGB')).astype(np.float32); a = np.clip((g.max(axis=2) - 18) / 110, 0, 1)
    c = np.where(a[..., None] > 0, g / np.maximum(a[..., None], 1e-3), 0).clip(0, 255)
    return Image.fromarray(np.dstack([c, a * 255]).astype(np.uint8), 'RGBA')


def _guardar(im, nombre):
    if nombre is None: return im                     # sin nombre → devuelve la imagen (la capa de edición la usa por estados)
    OUT.mkdir(parents=True, exist_ok=True)
    transparente(im).save(OUT / f'{nombre}.png'); im.save(OUT / f'{nombre}.pdf', 'PDF', resolution=150)
    return OUT / f'{nombre}.png'


def lista(nombre, items, ver=None):
    """Lista numerada en línea de tiempo (1 arriba)."""
    im = Image.new('RGB', (W, H), 'black'); d = ImageDraw.Draw(im)
    paso = H / len(items); r = min(70, paso * .36); cx = r + 14; xt = cx + r + 26   # letra GRANDE (Abel 19/10/2026): proporcional a la fila y sin margen vacío
    tam = _comun(items, W - xt - 12, min(84, paso * .62))
    d.line((cx, paso * .5, cx, paso * (len(items) - .5)), fill=LINEA, width=6)
    for i, t in enumerate(items):
        cy = paso * (i + .5); _anillo(d, cx, cy, r, i + 1)
        if ver is None or i in ver: _texto(d, (xt, cy), t, W - xt - 12, tam)
    return _guardar(im, nombre)


def escalera(nombre, items, ver=None):
    """Escalera en línea blanca sobre negro: el peldaño 1 abajo y el último arriba. Proporcional al lienzo (letra grande como «10 razones»)."""
    im = Image.new('RGB', (W, H), 'black'); d = ImageDraw.Draw(im)
    n = len(items); g = max(5, int(W * .014)); alto = (H - 4 * g) / n; sangria = W * .035
    r = min(alto * .3, W * .06); hueco = r * 2 + g * 3
    tam = min(_comun([t], W - 2 * g - (2 * g + i * sangria) - hueco - 3 * g, min(84, alto * .58)) for i, t in enumerate(items))
    for i, t in enumerate(items):
        y = H - 2 * g - i * alto; x = 2 * g + i * sangria          # huella del peldaño en y, contrahuella en x
        d.line((x, y, x, y - alto + g / 2), fill='white', width=g)
        d.line((x, y - alto + g / 2, W - 2 * g, y - alto + g / 2), fill='white', width=g)
        cy = y - alto / 2 + g / 2; _anillo(d, x + g * 1.5 + r, cy, r, i + 1)
        if ver is None or i in ver: _texto(d, (x + hueco, cy), t, W - 2 * g - x - hueco - 3 * g, tam)
    return _guardar(im, nombre)


def _apiladas(izq, der, items, ver, iconos):
    """IZQ arriba y DER debajo, a todo el ancho: cabecera de color con su icono a la izquierda y cada punto con su punto de color,
    todo alineado a la izquierda (cuando lado a lado la letra saldría pequeña)."""
    from PIL import Image as _I
    im = Image.new('RGB', (W, H), 'black'); d = ImageDraw.Draw(im)
    g = max(4, int(W * .01)); pad = g * 3
    grupos = [(izq.replace('\n', ' '), VERDE, iconos[0] if iconos else None, [(k, t) for k, (t, l) in enumerate(items) if l == 'izq']),
              (der.replace('\n', ' '), ROJO, iconos[1] if iconos else None, [(k, t) for k, (t, l) in enumerate(items) if l == 'der'])]
    CAB = 1.25; filas = sum(len(gr[3]) for gr in grupos) + CAB * 2 + .5; paso = (H - 2 * pad) / filas
    r = max(5, paso * .13); xt = pad + r * 2 + g * 3
    tam = _comun([t for t, _ in items], W - xt - pad, min(84, paso * .74)); y = pad
    for k_g, (cab, c, ic, lst) in enumerate(grupos):
        if k_g: y += paso * .5; d.line((pad, y - paso * .25, W - pad, y - paso * .25), fill=LINEA, width=4)
        alto = paso * CAB; xc = pad
        if ic:
            ico = _I.open(ic).convert('RGBA'); ico.thumbnail((int(alto * 1.6), int(alto * .8)), _I.LANCZOS)
            im.paste(ico, (int(pad), int(y + (alto - ico.height) / 2)), ico); xc = pad + ico.width + g * 3
        _texto(d, (xc, y + alto / 2), cab, W - xc - pad, min(tam * 1.25, alto * .62), c, 'lm', True); y += alto
        for k, t in lst:
            cy = y + paso / 2; y += paso
            if ver is None or k in ver: d.ellipse((pad, cy - r, pad + 2 * r, cy + r), fill=c); _texto(d, (xt, cy), t, W - xt - pad, tam)
    return im, tam


def columnas(nombre, izq, der, items, ver=None, iconos=None):
    """Dos grupos (p. ej. CARGA / DESCARGA, IMPORTA / NO IMPORTA): izq en VERDE, der en ROJO, sin números; items = [(texto, 'izq'|'der')]
    en el orden en que se dicen. iconos = (izq, der): dos iconos de IMAGENES/pizarra/iconos. TODO alineado a la IZQUIERDA y ordenado,
    todas las palabras del MISMO tamaño (Abel 19/10/2026). Se elige sola la colocación con la letra MÁS GRANDE: lado a lado
    (dos columnas) o uno encima del otro."""
    lado, t1 = _lado_a_lado(izq, der, items, ver, iconos); arriba, t2 = _apiladas(izq, der, items, ver, iconos)
    return _guardar(lado if t1 >= t2 else arriba, nombre)


def _lado_a_lado(izq, der, items, ver, iconos):
    from PIL import Image as _I
    im = Image.new('RGB', (W, H), 'black'); d = ImageDraw.Draw(im); mitad = W / 2
    g = max(4, int(W * .01)); pad = g * 3; top = g * 4; colores = (VERDE, ROJO)
    xs = (pad, mitad + pad); ancho = mitad - pad - g * 2                    # x de inicio de cada columna y ancho útil
    if iconos:
        alto_ic = int(H * .11)
        for x0, ruta in zip(xs, iconos):
            ic = _I.open(ruta).convert('RGBA'); ic.thumbnail((int(ancho * .8), alto_ic), _I.LANCZOS)
            im.paste(ic, (int(x0), top + (alto_ic - ic.height) // 2), ic)
        top += alto_ic + g * 4
    lineas_cab = [t.split('\n') for t in (izq, der)]                       # «NO\nIMPORTA»: la cabecera en 2 líneas sale más grande
    tam_cab = _comun([l for ls in lineas_cab for l in ls], ancho, 60, True); n_cab = max(len(ls) for ls in lineas_cab)
    for x0, ls, c in zip(xs, lineas_cab, colores):
        for k, l in enumerate(ls): _texto(d, (x0, top + tam_cab * (.6 + 1.1 * k)), l, ancho, tam_cab, c, 'lm', True)
    raya = top + tam_cab * (1.1 * n_cab + .2) + g * 3
    d.line((mitad, top, mitad, H - pad), fill=LINEA, width=4); d.line((pad, raya, W - pad, raya), fill=LINEA, width=4)
    filas = {'izq': [], 'der': []}
    for k, (t, lado) in enumerate(items): filas[lado].append((t, ver is None or k in ver))
    n = max(len(v) for v in filas.values()); paso = (H - raya - pad) / n
    r = max(4, min(paso * .09, W * .016)); xt = r * 2 + g * 2
    tam = _comun([t for t, _ in items], ancho - xt, min(66, paso * .72))
    for (lado, x0), c in zip((('izq', xs[0]), ('der', xs[1])), colores):
        for j, (t, visible) in enumerate(filas[lado]):
            cy = raya + paso * (j + .5)
            if visible: d.ellipse((x0, cy - r, x0 + 2 * r, cy + r), fill=c); _texto(d, (x0 + xt, cy), t, ancho - xt, tam)
    return im, tam


def ranking(nombre, items, ver=None):
    """Ranking (items en orden de aparición, p. ej. del 10 al 1); el último, el más importante, destacado."""
    im = Image.new('RGB', (W, H), 'black'); d = ImageDraw.Draw(im)
    paso = (H - 60) / len(items); r = min(68, paso * .36); cx = r + 14; xt = cx + r + 26
    tam = _comun([t for _, t in items], W - xt - 12, min(84, paso * .62))
    d.line((cx, 30 + paso * .5, cx, 30 + paso * (len(items) - .5)), fill=LINEA, width=6)
    for i, (num, t) in enumerate(items):
        cy = 30 + paso * (i + .5); ultimo = i == len(items) - 1
        _anillo(d, cx, cy, r, num, VERDE if ultimo else AMARILLO, relleno=VERDE if ultimo else 'black', num='black' if ultimo else 'white')
        if ver is None or i in ver: _texto(d, (xt, cy), t, W - xt - 12, tam, VERDE if ultimo else 'white', negra=ultimo)
    return _guardar(im, nombre)


def bateria(nombre, carga, descarga, ver=None):
    """Batería: arriba lo que CARGA (verde), abajo lo que DESCARGA (rojo), dentro de una pila. Todo proporcional al lienzo
    (letra grande como en «10 razones», Abel 19/10/2026)."""
    im = Image.new('RGB', (W, H), 'black'); d = ImageDraw.Draw(im)
    g = max(6, int(W * .016)); m = g * 2; tapa = int(H * .03)
    x0, x1, y0, y1 = m, W - m, m + tapa, H - m
    d.rounded_rectangle((W / 2 - W * .14, y0 - tapa, W / 2 + W * .14, y0 + 4), g * 2, fill='white')
    d.rounded_rectangle((x0, y0, x1, y1), g * 5, outline='white', width=g); mid = (y0 + y1) / 2
    d.line((x0 + g * 3, mid, x1 - g * 3, mid), fill=LINEA, width=max(3, g // 2))
    n = max(len(carga), len(descarga)); cab = (mid - y0) * .2; paso = ((mid - y0) - cab - g * 2) / n
    xp = x0 + g * 3; r = max(6, paso * .12); xt = xp + r * 2 + g * 2; maxw = x1 - g * 3 - xt
    tam = _comun(carga + descarga, maxw, min(84, paso * .5)); tcab = min(cab * .62, tam * 1.15)
    for (ya, yb), titulo, c, signo, lst in (((y0, mid), 'CARGA', VERDE, '+', carga), ((mid, y1), 'DESCARGA', ROJO, '−', descarga)):
        _texto(d, (xp, ya + g + cab / 2), f'{signo} {titulo}', x1 - xp - g * 3, tcab, c, 'lm', True)
        for j, t in enumerate(lst):
            k = j if lst is carga else len(carga) + j          # índice global: primero las cargas, luego las descargas
            cy = ya + g + cab + paso * (j + .5); d.ellipse((xp, cy - r, xp + 2 * r, cy + r), fill=c)
            if ver is None or k in ver: _texto(d, (xt, cy), t, maxw, tam)
    return _guardar(im, nombre)
