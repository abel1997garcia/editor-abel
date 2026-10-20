"""Capa de los REELS VIRALES con prefijo (Abel 19/10/2026), la usa render.py. Abel graba a la izquierda y deja la zona derecha vacía:
- TABLET:   la imagen de lista_tablet.py se va REVELANDO punto a punto cuando lo dice (la estructura y los números, desde el principio).
            plan.json → "estilo": "tablet", "tablet": {"forma": "lista|escalera|columnas|ranking|bateria", "args": [...], "momentos": ["frase con la que aparece el punto 1", ...]}
- HISTORIA: cada idea, su título (fino + **clave** en grueso) + su ESCENA de pizarra (IMAGENES/pizarra/escenas/<vídeo>/, mismo personaje),
            en la misma caja, centrados en la zona derecha, entrando con un fundido que sube y frena (sin más movimiento: competiría con su cara).
            plan.json → "estilo": "historia", "diapos": [{"frase": "frase con la que entra", "titulo": "Te **traicionas** para agradar", "dibujo": "escenas/historia01/4_te_traicionas_rojo"}, ...]
En los dos, los subtítulos van ABAJO, en la franja blanca, en UNA línea (render.py).
"""
import sys
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont
AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parent))
import lista_tablet

PIZARRA = Path.home() / 'Desktop' / 'EDICION VIDEOS' / 'IMAGENES' / 'pizarra'
FB = AQUI.parent / 'fuentes' / 'Montserrat-Black.ttf'
FV = AQUI.parent / 'fuentes' / 'Montserrat-Variable.ttf'      # títulos de escena: Medium + palabra clave en Black
X0, X1 = 580, 1020                    # zona libre a la derecha de Abel; 60 px de margen al borde (Instagram recorta a veces los lados)
ENTRA, SUBE = .35, 36                 # entrada: 0,35 s de fundido + sube 36 px con frenada suave
MAX_ESCENA = 7                       # ninguna escena (HISTORIA) dura más de 7 s: si no, «se hace pesado y cansino» (Abel 19/10/2026); duracion_escenas.py lo comprueba


def _sombra(im, r=6, fuerza=1.7):
    """sombra suave pegada al trazo (sin caja ni fondo, Abel 19/10/2026) para que se lea sobre lo que hay detrás"""
    al = im.split()[3].filter(ImageFilter.MaxFilter(5)).filter(ImageFilter.GaussianBlur(r)).point(lambda v: min(255, int(v * fuerza)))
    s = Image.new('RGBA', im.size, (0, 0, 0, 0)); s.putalpha(al); return Image.alpha_composite(s, im)


def _sin_negro(im):
    """fondo negro → transparente (los colores y el texto se quedan)"""
    g = np.asarray(im.convert('RGB')).astype(np.float32); a = np.clip((g.max(axis=2) - 18) / 110, 0, 1)
    c = np.where(a[..., None] > 0, g / np.maximum(a[..., None], 1e-3), 0).clip(0, 255)
    return Image.fromarray(np.dstack([c, a * 255]).astype(np.uint8), 'RGBA')


def _encaja(im, w, h):
    im = im.copy(); im.thumbnail((w, h), Image.LANCZOS); return im


def titulo(txt, ancho, size=44):
    """título de la diapositiva como los de @tuseienergia: fino (Montserrat Medium) y la palabra clave entre ** en grueso (Black);
    centrado, la puntuación pegada a su palabra («**cambia**?»)"""
    import re
    def fuente(peso):
        f = ImageFont.truetype(str(FV), size); f.set_variation_by_name(peso); return f
    trozos = []
    for i, parte in enumerate(re.split(r'\*\*', txt)):
        for w in parte.split():
            if trozos and re.fullmatch(r'[?!.,:;»]+', w): trozos[-1] = (trozos[-1][0] + w, trozos[-1][1])
            else: trozos.append((w, i % 2 == 1))
    lineas, cur, w_ = [], [], 0
    for w, neg in trozos:
        lw = fuente('Black' if neg else 'Medium').getlength(w + ' ')
        if cur and w_ + lw > ancho: lineas.append(cur); cur, w_ = [], 0
        cur.append((w, neg)); w_ += lw
    lineas.append(cur); alto = int(size * 1.25)
    im = Image.new('RGBA', (ancho, alto * len(lineas)), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    for k, ln in enumerate(lineas):
        tot = sum(fuente('Black' if n else 'Medium').getlength(w + ' ') for w, n in ln) - fuente('Medium').getlength(' '); x = (ancho - tot) / 2
        for w, n in ln:
            f = fuente('Black' if n else 'Medium'); d.text((x, k * alto), w, font=f, fill='white'); x += f.getlength(w + ' ')
    return im


def _momento(pal, frase, desde, en_reel):
    return en_reel(pal, frase, desde)[0]


def preparar(plan, pal, out, b0, b1, dur, n_in, en_reel):
    """→ (entradas ffmpeg, cadena de filtros que va de [vin] a [vcapa]) o None si el plan no lleva capa"""
    estilo = plan.get('estilo'); zona_h = b1 - b0 - 60; zona_w = X1 - X0; cx = (X0 + X1) // 2
    capas = []                                                   # (png, t0, t1, x, y, fundido de entrada, sube)
    if estilo == 'tablet':
        tb = plan['tablet']; forma = getattr(lista_tablet, tb['forma']); args = tb['args']; ts, t = [], 0
        for f in tb['momentos']: t = _momento(pal, f, t, en_reel) - .05; ts.append(max(0, t))
        estados = [set()] + [set(range(k + 1)) for k in range(len(ts))]
        inis = [0] + ts
        for k, ver in enumerate(estados):
            ancho = 500                                                       # lienzo compacto → letra GRANDE en la zona (Abel 19/10/2026: «que se vea mejor»)
            lista_tablet.W, lista_tablet.H = ancho, int(ancho * zona_h / zona_w)   # a la medida de la zona: la letra sale grande (a 1080 de ancho quedaba diminuta)
            try: im = forma(None, *args, ver=ver, **tb.get('kwargs', {}))
            finally: lista_tablet.W, lista_tablet.H = 1080, 1760
            im = _encaja(_sombra(_sin_negro(im)), zona_w, zona_h)
            ruta = out / f'tablet{k}.png'; im.save(ruta)
            fin = inis[k + 1] + .25 if k + 1 < len(inis) else dur      # el estado anterior sigue debajo mientras entra el nuevo
            capas.append((ruta, inis[k], fin, cx - im.width // 2, (b0 + b1) // 2 - im.height // 2, .25 if k else .4, 0))
    elif estilo == 'historia':
        ds = plan['diapos']; ts, t = [], 0
        for dpo in ds: t = _momento(pal, dpo['frase'], t, en_reel) - .05; ts.append(max(0, t))
        caja = (zona_w - 10, min(470, zona_h - 150))                    # TODAS las escenas en la MISMA caja (Abel 19/10/2026)
        for k, dpo in enumerate(ds):
            tit = titulo(dpo['titulo'], zona_w - 30)
            dib = Image.open(PIZARRA / f"{dpo['dibujo']}.png").convert('RGBA'); dib.thumbnail(caja, Image.LANCZOS)
            gh = tit.height + 18 + caja[1]; g = Image.new('RGBA', (zona_w, gh), (0, 0, 0, 0))
            g.alpha_composite(tit, ((zona_w - tit.width) // 2, 0))
            g.alpha_composite(dib, ((zona_w - dib.width) // 2, tit.height + 18 + (caja[1] - dib.height) // 2))
            ruta = out / f'diapo{k}.png'; _sombra(g).save(ruta)
            fin = ts[k + 1] if k + 1 < len(ts) else dur
            capas.append((ruta, ts[k], fin, X0, b0 + (b1 - b0 - gh) // 2, ENTRA, SUBE))   # título + escena, CENTRADOS en la zona derecha
    else:
        return None
    ent, fil, prev = [], '', 'vin'
    for k, (ruta, t0, t1, x, y, d_in, sube) in enumerate(capas):
        ent += ['-loop', '1', '-t', f'{dur:.3f}', '-i', str(ruta)]; i = n_in + k
        sal = 'vcapa' if k == len(capas) - 1 else f'vc{k}'
        fade_out = f",fade=t=out:st={max(t0, t1 - .15):.3f}:d=0.15:alpha=1" if t1 < dur - .05 and sube else ''
        yexp = f"{y}+{sube}*pow(max(0\\,1-(t-{t0:.3f})/{d_in})\\,2)" if sube else str(y)
        fil += (f"[{i}:v]format=rgba,fade=t=in:st={t0:.3f}:d={d_in}:alpha=1{fade_out}[o{k}];"
                f"[{prev}][o{k}]overlay=x={x}:y='{yexp}':enable='between(t,{t0:.3f},{t1:.3f})'[{sal}];")
        prev = sal
    return ent, fil
