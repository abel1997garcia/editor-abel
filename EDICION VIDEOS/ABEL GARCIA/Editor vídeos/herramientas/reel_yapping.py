"""Reels yapping de Abel con su plantilla (tipo OpusClip): título arriba, vídeo 4:3 en el centro, subtítulos abajo, música.

    python reel_yapping.py config.json            -> <salida>/<reel>.mp4 (1080x1920, 30 fps; su voz al volumen original)
    python reel_yapping.py config.json --texto    -> solo texto, duración y avisos

Se saca del vídeo horizontal YA EDITADO (con sus animaciones), recortado a 4:3: en los planos de cara, centrado en él
(con el acercamiento alterno); en los de animación, el 4:3 central sin acercamiento (ahí van las animaciones).

config.json:
{ "fuente": "vídeo horizontal editado (1920x1080)", "tiempos": "trabajo/tiempos.json (palabras en el tiempo del vídeo editado)",
  "montaje": "edicion/montaje.json del proyecto horizontal (qué tramos son animación)", "salida": "out",
  "reels": { "nombre": { "tramos": [[i0, i1], ...], "quitar": [i, ...], "titulo": "EN MAYÚSCULAS",
                         "musica": "EMOCIONAL/tema.mp3", "desde": null } } }
tramos = índices de palabra en el orden en que se oyen; o por partes: "gancho", "cuerpo", "final" (se unen en ese orden).
Variante: { "de": "reel_1", "gancho": [...], "titulo": "..." } hereda todo de reel_1 y cambia solo lo que trae.
 música = ruta dentro de MUSICA; "desde" = segundo de la
canción (null: el estribillo de MUSICA/catalogo.json, o lo busca por energía).
"""
import json, os, re, shutil, subprocess, sys, tempfile
from pathlib import Path

AQUI = Path(__file__).resolve().parent
FUENTE_TTF = AQUI / 'fuentes' / 'Montserrat-ExtraBold.ttf'
MUSICA = Path('C:/Users/Clap/Desktop/EDICION VIDEOS/MUSICA')   # EMOCIONAL/, ÉPICA/ y catalogo.json (estribillo de cada tema)

# --- plantilla (1080x1920), medida sobre la captura de referencia de Abel (OpusClip)
VID_W, VID_H, VID_Y = 1080, 810, 547          # vídeo 4:3 con él centrado (en la referencia: y 556–1349)
TITULO_PX, TITULO_Y, TITULO_PASO, TITULO_ANCHO = 51, 473, 61, 940   # MAYÚSCULAS, ≤ 7 palabras; líneas a 61 px (ref.: 425–522)
SUB_PX, SUB_Y, SUB_MAX = 51, 1411, 3          # justo bajo el vídeo, una línea, máx. 3 palabras (ref.: 1393–1428)

# --- cortes fluidos (regla de Abel): se limpian silencios largos, pero no se trocea el habla natural
PAUSA = .45        # pausa por encima de la cual se corta (Abel 08/10/2026: cortar cada pausa de 0,3 s dejaba 25 cortes en 53 s, «nada fluido»)
AIRE = .12         # al cortar un silencio largo quedan ~0,25 s (0,12 a cada lado), nunca cero: que respire
MIN_PLANO = 1.5    # un plano más corto se une al de al lado: dentro de una frase no hay cortecitos
PAUSA_MAX = .45   # pero solo si la pausa que los separa es natural; más larga, se corta (vídeo dinámico)
PAUSA_UNIR = .65  # una palabra suelta («dije», «y») nunca se queda en un plano de medio segundo: se une a su frase si la pausa es ≤ esto
COLA = .45         # el último plano respira
ZOOM = 1.10        # acercamiento alterno solo en los cortes de contenido (aprobado en los reels)

# --- música: 26 dB por debajo de la voz (la voz va tal cual), empezando en el estribillo y a su velocidad normal
MUSICA_DB, MUSICA_IN, MUSICA_OUT = -18, .4, 1.5   # Abel, 07/10/2026: a −26 dB «no hay música»
COLA_FINAL = .5   # el reel acaba con medio segundo de aire tras la última palabra
FUNDIDO = .04     # fundido de audio en los cortes pegados: nunca un empalme seco (Abel: «se corta muy brusco»)

# --- todo el reel (vídeo, voz, subtítulos) a 1,10x (1,15 era demasiado rápido; 1,07 también le vale); la música no
VELOCIDAD = 1.10


def resolver(reels):
    """variantes ("de") y partes (gancho + cuerpo + final) -> cada reel con sus tramos"""
    out = {}
    def r(n):
        if n in out: return out[n]
        x = dict(reels[n]); base = x.pop('de', None)
        if base: x = {**r(base), **x}
        if any(k in x for k in ('gancho', 'cuerpo', 'final')):
            x['tramos'] = [t for k in ('gancho', 'cuerpo', 'final') for t in x.get(k, [])]
        out[n] = x; return x
    for n in reels: r(n)
    return out


def planos(W, reel):
    quitar = set(reel.get('quitar', []))
    grupos = []
    for a, b in reel['tramos']:
        g = []
        for i in range(a, b + 1):
            if i in quitar:
                if g: grupos.append(g); g = []
                continue
            if g and W[i]['s'] - W[g[-1]]['e'] > PAUSA: grupos.append(g); g = []
            g.append(i)
        if g: grupos.append(g)
    dur = lambda g: W[g[-1]]['e'] - W[g[0]]['s']
    # unir trocitos cortos con su vecino si son palabras seguidas y la pausa es natural (≤ PAUSA_MAX); un silencio más
    # largo se recorta siempre (Abel, 08/10/2026: «no es fluido ni dinámico»: quedaban pausas de hasta 1,4 s dentro de los planos)
    unible = lambda i, j: j == i + 1 and W[j]['s'] - W[i]['e'] <= PAUSA_UNIR
    k = 0
    while k < len(grupos):
        g = grupos[k]
        if dur(g) < MIN_PLANO:
            if k + 1 < len(grupos) and unible(g[-1], grupos[k + 1][0]): grupos[k:k + 2] = [g + grupos[k + 1]]; continue
            if k > 0 and unible(grupos[k - 1][-1], g[0]): grupos[k - 1:k + 1] = [grupos[k - 1] + g]; k -= 1; continue
        k += 1
    res = []
    for k, g in enumerate(grupos):
        i0, i1 = g[0], g[-1]
        t0 = W[i0]['s'] - AIRE
        if i0 > 0: t0 = max(t0, W[i0 - 1]['e'] + .02)
        t1 = W[i1]['e'] + (COLA if k == len(grupos) - 1 else AIRE)
        if i1 + 1 < len(W): t1 = min(t1, W[i1 + 1]['s'] - .02)
        res.append((round(t0, 3), round(t1, 3), g))
    return res


def avisos(W, PW, reel):
    """tramos que acaban sin puntuación detrás (frase sin cerrar)"""
    out, norm = [], lambda x: ''.join(c for c in x.lower() if c.isalnum())
    for n, (a, b) in enumerate(reel['tramos']):
        cand = [x for x in PW if abs(x['s'] - W[b]['s']) < .8 and norm(x['w']) == norm(W[b]['w'])]
        fin = '.?!' if n == len(reel['tramos']) - 1 else '.?!,;:'
        if cand and not min(cand, key=lambda x: abs(x['s'] - W[b]['s']))['w'].rstrip('»"').endswith(tuple(fin)):
            out.append(f"tramo {a}-{b} acaba en «{W[b]['w']}» sin puntuación (sigue «{W[b + 1]['w'] if b + 1 < len(W) else ''}»)")
    return out


def centro_cara(fuente):
    import cv2
    sys.path.insert(0, str(Path.home() / '.claude/skills/animaciones-horizontal-combinadas/scripts'))
    from cortar import modelo_cara
    cap = cv2.VideoCapture(fuente); n = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    w, h = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    det = cv2.FaceDetectorYN.create(str(modelo_cara()), '', (w, h), 0.7, 0.3, 5); xs = []
    for k in range(40):
        cap.set(cv2.CAP_PROP_POS_FRAMES, int(n * (k + .5) / 40)); ok, f = cap.read()
        if not ok: continue
        _, c = det.detect(f)
        if c is not None and len(c): x, y, cw, ch = max(c, key=lambda q: q[2] * q[3])[:4]; xs.append(x + cw / 2)
    xs.sort(); return xs[len(xs) // 2], w, h


def estribillo(musica, dur):
    """segundo de inicio del tramo de más energía sostenida (≈ el estribillo), saltando la intro"""
    import numpy as np
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', musica, '-ac', '1', '-ar', '8000', '-f', 's16le', '-'], capture_output=True).stdout
    x = np.frombuffer(raw, np.int16).astype(float); v = int(8000 * .5)
    rms = np.sqrt([np.mean(x[i:i + v] ** 2) for i in range(0, len(x) - v, v)])
    win = max(1, int(dur / .5)); total = len(rms)
    if total <= win: return 0.0
    media = np.convolve(rms, np.ones(win) / win, 'valid')
    ini = int(total * .12)
    return round(float((ini + np.argmax(media[ini:])) * .5), 1)


def tam_ass(px):
    """libass mide el cuerpo con las métricas «win» de la fuente (ascendente + descendente), no en em:
    51 px reales de Montserrat -> 80 en ASS (comprobado midiendo el ancho del texto renderizado)"""
    from fontTools.ttLib import TTFont
    f = TTFont(FUENTE_TTF); o = f['OS/2']; return round(px * (o.usWinAscent + o.usWinDescent) / f['head'].unitsPerEm)


def ass(titulo, subs, ruta):
    cab = f"""[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 0

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Titulo,Montserrat ExtraBold,{tam_ass(TITULO_PX)},&H00111111,&H00111111,&H00FFFFFF,&H00FFFFFF,0,0,0,0,100,100,0,0,1,0,0,5,70,70,0,1
Style: Sub,Montserrat ExtraBold,{tam_ass(SUB_PX)},&H00111111,&H00111111,&H00FFFFFF,&H00FFFFFF,0,0,0,0,100,100,0,0,1,0,0,5,40,40,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    tc = lambda s: f"{int(s // 3600)}:{int(s % 3600 // 60):02d}:{s % 60:05.2f}"
    # el título se parte a mano y cada línea va en su sitio: así quedan tan pegadas como en la referencia
    from PIL import ImageFont
    f, lineas = ImageFont.truetype(str(FUENTE_TTF), TITULO_PX), ['']
    for w in titulo.upper().split():
        prueba = (lineas[-1] + ' ' + w).strip()
        if lineas[-1] and f.getlength(prueba) > TITULO_ANCHO: lineas.append(w)
        else: lineas[-1] = prueba
    if len(lineas) == 2 or (len(lineas) == 1 and f.getlength(lineas[0]) > TITULO_ANCHO * .75):   # dos líneas equilibradas
        pal = ' '.join(lineas).split()
        k = min(range(1, len(pal)), key=lambda i: abs(f.getlength(' '.join(pal[:i])) - f.getlength(' '.join(pal[i:]))))
        lineas = [' '.join(pal[:k]), ' '.join(pal[k:])]
    ev = [f"Dialogue: 0,{tc(0)},{tc(subs[-1][1] + 5)},Titulo,,0,0,0,,{{\\pos(540,{TITULO_Y + (i - (len(lineas) - 1) / 2) * TITULO_PASO:.0f})}}{l}"
          for i, l in enumerate(lineas)]
    ev += [f"Dialogue: 0,{tc(a)},{tc(b)},Sub,,0,0,0,,{{\\pos(540,{SUB_Y})}}{t}" for a, b, t in subs]
    Path(ruta).write_text(cab + '\n'.join(ev) + '\n', encoding='utf-8')


def ajustar_finales(fuente, W, ps):
    """el alineador da el final de cada palabra 0,05–0,1 s antes de tiempo: el corte se comía la cola («frecuencia» sonaba
    «frecuen-que»). Se mide en el audio dónde se apaga de verdad (envolvente cada 10 ms) y el corte va 30 ms después,
    sin llegar nunca a la palabra siguiente. Al empezar un tramo, el corte va al punto más silencioso antes de su primera palabra."""
    import numpy as np
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', fuente, '-vn', '-ac', '1', '-ar', '16000', '-f', 's16le', '-'], capture_output=True).stdout
    x = np.frombuffer(raw, np.int16).astype(float) / 32768; sr, v = 16000, 160
    db = lambda t: 20 * np.log10(np.sqrt(np.mean(x[int(t * sr):int(t * sr) + v] ** 2)) + 1e-9)
    out = []
    for t0, t1, g in ps:
        i1 = g[-1]; tope = W[i1 + 1]['s'] - .02 if i1 + 1 < len(W) else t1 + .6
        pico = max(db(W[i1]['s'] + k * .01) for k in range(max(1, int((W[i1]['e'] - W[i1]['s']) / .01))))
        t = W[i1]['e'] - .03
        while t < min(tope, W[i1]['e'] + .6) and (db(t) > max(-42, pico - 24) or db(t + .01) > max(-42, pico - 24)): t += .01   # hasta 0,6 s: las vocales que alarga («deee…») se acaban enteras
        i0 = g[0]                                         # inicio: nunca arrastrar la cola de la palabra anterior («y cada vez…»)
        if i0 > 0 and W[i0]['s'] - W[i0 - 1]['e'] < .6:
            ts = [W[i0 - 1]['e'] - .05 + k * .01 for k in range(int((W[i0]['s'] - W[i0 - 1]['e'] + .05) / .01) + 1)]
            t0 = max(t0, min(ts, key=db) + .005) if ts else t0
        p0 = max(db(W[i0]['s'] + k * .01) for k in range(max(1, int((W[i0]['e'] - W[i0]['s']) / .01))))   # inicio real: saltar el silencio
        u = t0
        while u < W[i0]['e'] - .05 and db(u) < max(-42, p0 - 24) and db(u + .01) < max(-42, p0 - 24): u += .01
        if u - t0 > .12: t0 = u - .06
        # el inicio NUNCA cae encima de un sonido (verificar_audio 08/10: «no eran» empezaba a mitad de un sonido sin alinear):
        # si donde empieza hay voz, se va al punto más silencioso de los 0,35 s anteriores a su primera palabra
        if db(t0) > max(-42, p0 - 24):
            lo = max(W[i0 - 1]['e'] + .02 if i0 > 0 else 0, W[i0]['s'] - .35)
            ts = [lo + k * .01 for k in range(max(1, int((W[i0]['s'] - lo) / .01)))]
            t0 = min(ts, key=db) + .005
        silencio = lambda s: db(s) < max(-42, pico - 24)
        if not silencio(t):                                # la voz no se apaga antes del tope: cortar en lo más silencioso, no encima
            ts = [W[i1]['e'] - .05 + k * .01 for k in range(int((min(tope, W[i1]['e'] + .8) - W[i1]['e'] + .05) / .01) + 1)]
            t = min(ts, key=db) - .03 if ts else t
        e = t + .03                                        # el aire de después solo mientras siga habiendo silencio
        while e < min(tope, t + .03 + (t1 - W[i1]['e'])) and silencio(e) and silencio(e + .01): e += .01
        t1n = max(min(e, tope), W[i1]['e'] + .02)
        # final real: si dentro de la última palabra hay un silencio de ≥ 0,25 s (la alineación la estiró), se corta ahí
        u2, corte_ = W[i1]['s'] + .12, None
        while u2 < t1n - .25:
            if all(db(u2 + k * .01) < max(-42, pico - 24) for k in range(25)): corte_ = u2; break
            u2 += .01
        if corte_: out.append((round(t0, 3), round(corte_ + .1, 3), g)); continue
        out.append((round(t0, 3), round(t1n, 3), g))
    return out


def rellenos(W, ps):
    """silencio que falta tras cada plano para que el corte respire (si la palabra siguiente va pegada, la cola se queda corta)"""
    return [round(max(0, (COLA_FINAL if k == len(ps) - 1 else AIRE) - max(0, t1 - W[g[-1]]['e'])), 3) for k, (t0, t1, g) in enumerate(ps)]


def subtitulos(W, ps, pads=None):
    """bloques de hasta 3 palabras en el tiempo del reel; cortan también en cada salto de plano"""
    out, T = [], 0.0
    for t0, t1, g in ps:
        for k in range(0, len(g), SUB_MAX):
            b = g[k:k + SUB_MAX]
            a = T + W[b[0]]['s'] - t0
            fin = T + (W[g[k + SUB_MAX]]['s'] - t0 if k + SUB_MAX < len(g) else t1 - t0)
            out.append((max(0, a - .05), fin, ' '.join(str(W[i]['w']).strip('~') for i in b)))
        T += t1 - t0 + (pads[ps.index((t0, t1, g))] if pads else 0)
    # nunca dos a la vez: cada bloque se apaga justo cuando entra el siguiente
    return [(a, min(b, out[i + 1][0]) if i + 1 < len(out) else b, t) for i, (a, b, t) in enumerate(out)]


def ventanas_anim(ruta):
    """[(a, b, id)] en segundos del vídeo editado: los planos de animación de su montaje.json"""
    if not ruta: return []
    m = json.load(open(ruta, encoding='utf-8'))
    return [(p['f0'] / m['fps'], p['f1'] / m['fps'], p.get('id')) for p in m['planos'] if p['tipo'] == 'anim']


def nucleos(cfg, W):
    """de qué frase habla cada animación: {id: (inicio, fin)} según ventanas.json del horizontal"""
    if not cfg.get('ventanas'): return {}
    sys.path.insert(0, str(AQUI / 'pizarra')); from ventanas import buscar
    out = {}
    for id_, ini, fin, desde in json.load(open(cfg['ventanas'], encoding='utf-8')):
        a, _ = buscar(W, ini, desde); _, b = buscar(W, fin, W[a]['s']); out[id_] = (W[a]['s'], W[b]['e'])
    return out


def trozos(t0, t1, g, W, anim, nuc):
    """el plano en trozos [(a, b, fuente, anims propias)]: una animación cuyo mensaje no se dice en este plano (solo cae su
    cola de 0,7 s, Abel 08/10/2026: «sale la energía masculina cuando hablo de tu mejor versión») se cambia por su cara (toma limpia)"""
    propias, ajenas = [], []
    for a, b, id_ in anim:
        if not (a < t1 and b > t0): continue
        n = nuc.get(id_)
        suyas = [i for i in g if a <= W[i]['s'] < b and (not n or n[0] - .2 <= W[i]['s'] <= n[1])]
        (propias if suyas or not n else ajenas).append((max(a, t0), min(b, t1)))
    cortes = sorted({t0, t1, *[x for r in ajenas for x in r]})
    out = []
    for a, b in zip(cortes, cortes[1:]):
        if b - a < .005: continue
        aj = any(x <= a and b <= y for x, y in ajenas)
        out.append((a, b, 1 if aj else 0, [] if aj else [(x, y) for x, y in propias if x < b and y > a]))
    return out


def voz_lufs(fuente):
    err = subprocess.run(['ffmpeg', '-hide_banner', '-nostats', '-i', fuente, '-vn', '-af', 'ebur128', '-f', 'null', '-'], capture_output=True, text=True).stderr
    return float(re.findall(r'I:\s+(-?[\d.]+) LUFS', err)[-1])


def montar(cfg, nombre, reel, W, cara):
    ps = ajustar_finales(cfg['fuente'], W, planos(W, reel)); cx, fw, fh = cara; anim = ventanas_anim(cfg.get('montaje')); nuc = nucleos(cfg, W)
    toma = 1 if cfg.get('toma') else None
    pads = rellenos(W, ps)
    dur = (sum(b - a for a, b, _ in ps) + sum(pads)) / VELOCIDAD
    tmp = Path(tempfile.mkdtemp(prefix='reel_'))      # ruta sin acentos ni espacios: el filtro ass de ffmpeg lo agradece
    shutil.copy(FUENTE_TTF, tmp / 'm.ttf')
    ass(reel['titulo'], [(a / VELOCIDAD, b / VELOCIDAD, t) for a, b, t in subtitulos(W, ps, pads)], tmp / 's.ass')
    fil, z = [], ZOOM
    ch0 = fh; cw0 = ch0 * 4 / 3                       # 4:3 a toda la altura del original, centrado en su cara
    for k, (t0, t1, g) in enumerate(ps):
        prev = ps[k - 1][2][-1] if k else None
        if k == 0 or g[0] != prev + 1: z = 1.0 if z != 1.0 else ZOOM
        tz = trozos(t0, t1, g, W, anim, nuc) if toma else [(t0, t1, 0, [(max(a, t0), min(b, t1)) for a, b, _ in anim if a < t1 and b > t0])]
        zz = 1.0 if any(d for *_, d in tz) else z                          # con animación, sin acercamiento
        cw, ch = cw0 / zz, ch0 / zz; xc = f'{min(max(cx - cw / 2, 0), fw - cw):.1f}'; y = (fh - ch) * .35
        for j, (a, b, src, dentro) in enumerate(tz):
            x = xc
            if dentro:                                                     # en la animación, el 4:3 central
                cond = '+'.join(f'between(t,{p - a:.3f},{q - a:.3f})' for p, q in dentro)   # entre comillas: comas sin escapar
                x = f"'if({cond},{(fw - cw) / 2:.1f},{xc})'"
            fil.append(f"[{src}:v]trim={a}:{b},setpts=PTS-STARTPTS,crop={cw:.1f}:{ch:.1f}:{x}:{y:.1f},"
                       f"scale={VID_W}:{VID_H}:flags=lanczos,setsar=1,fps=30[v{k}_{j}];"
                       f"[{src}:a]atrim={a}:{b},asetpts=PTS-STARTPTS,aresample=48000,aformat=channel_layouts=stereo[a{k}_{j}];")
        d = t1 - t0; fo = FUNDIDO if pads[k] > 0 else .01
        fil.append(''.join(f'[v{k}_{j}][a{k}_{j}]' for j in range(len(tz))) + f'concat=n={len(tz)}:v=1:a=1[vk{k}][ak{k}];'
                   f"[vk{k}]tpad=stop_mode=clone:stop_duration={pads[k]}[v{k}];"
                   f"[ak{k}]afade=t=in:d=0.01,afade=t=out:st={d - fo:.3f}:d={fo},apad=pad_dur={pads[k]}[a{k}];")
    n = len(ps)
    fil.append(''.join(f'[v{k}][a{k}]' for k in range(n)) + f'concat=n={n}:v=1:a=1[vc0][voz0];'
               f'[vc0]setpts=PTS/{VELOCIDAD},fps=30[vc];[voz0]atempo={VELOCIDAD}[voz];')
    fil.append(f"color=white:s=1080x1920:r=30:d={dur:.3f}[fondo];[fondo][vc]overlay=0:{VID_Y}:shortest=1,ass=s.ass:fontsdir=.,format=yuv420p[v];")
    entradas = ['-i', cfg['fuente']] + (['-i', cfg['toma']] if toma else []); mi = 2 if toma else 1
    if reel.get('musica'):
        mus = str(MUSICA / reel['musica'])                          # p. ej. "EMOCIONAL/Tom Odell - Another Love….mp3"
        cat = json.load(open(MUSICA / 'catalogo.json', encoding='utf-8')) if (MUSICA / 'catalogo.json').exists() else {}
        desde = reel.get('desde')
        if desde is None: desde = cat.get(reel['musica'], {}).get('estribillo') or estribillo(mus, dur)
        print(f'  música: {reel["musica"]} desde {desde} s')
        entradas += ['-ss', str(desde), '-i', mus]
        # su voz no se toca (Abel: nunca bajarla); la música se iguala a la voz y queda MUSICA_DB por debajo
        fil.append(f"[{mi}:a]atrim=0:{dur:.3f},loudnorm=I={max(-30, min(-5, voz_lufs(cfg['fuente']))):.1f}:TP=-2:LRA=11,volume={MUSICA_DB}dB,"
                   f"afade=t=in:d={MUSICA_IN},afade=t=out:st={dur - MUSICA_OUT:.3f}:d={MUSICA_OUT}[mu];"
                   f"[voz][mu]amix=inputs=2:duration=first:normalize=0,alimiter=limit=0.891:level=0,aresample=48000[a]")
    else:
        fil.append('[voz]alimiter=limit=0.891:level=0,aresample=48000[a]')
    salida = Path(cfg.get('salida', 'out')).resolve(); salida.mkdir(parents=True, exist_ok=True)
    final = salida / f'{nombre}.mp4'
    subprocess.run(['ffmpeg', '-v', 'error', '-y', *entradas, '-filter_complex', ''.join(fil), '-map', '[v]', '-map', '[a]',
                    '-c:v', 'libx264', '-preset', 'slow', '-crf', '18', '-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart',
                    str(final)], check=True, cwd=tmp)
    shutil.rmtree(tmp, ignore_errors=True)
    return final


if __name__ == '__main__':
    cfg_ruta = Path(sys.argv[1]).resolve(); os.chdir(cfg_ruta.parent)
    cfg = json.load(open(cfg_ruta, encoding='utf-8'))
    for k in ('fuente', 'tiempos', 'salida', 'montaje', 'toma', 'ventanas'):        # ffmpeg corre en una carpeta temporal: rutas absolutas
        if k in cfg: cfg[k] = str(Path(cfg[k]).resolve())
    W = json.load(open(cfg['tiempos'], encoding='utf-8'))
    tr = Path(cfg['tiempos']).with_name('transcripcion.json')
    PW = json.load(open(tr, encoding='utf-8'))['palabras'] if tr.exists() else []
    solo = '--texto' in sys.argv
    cara = None if solo else centro_cara(cfg['fuente'])
    for nombre, reel in resolver(cfg['reels']).items():
        ps = planos(W, reel)
        print(f"\n== {nombre}: {sum(b - a for a, b, _ in ps) / VELOCIDAD:.1f} s a {VELOCIDAD}x · {len(ps)} planos · «{reel['titulo'].upper()}»")
        print(' | '.join(' '.join(W[i]['w'] for i in g) for _, _, g in ps))
        for a in avisos(W, PW, reel): print('  AVISO:', a)
        if not solo: print('  ->', montar(cfg, nombre, reel, W, cara))
