"""Reels yapping de Abel con su plantilla (tipo OpusClip): título arriba, vídeo 4:3 en el centro, subtítulos abajo, música.

    python reel_yapping.py config.json            -> <salida>/<reel>.mp4 (1080x1920, 30 fps; su voz al volumen original)
    python reel_yapping.py config.json --texto    -> solo texto, duración y avisos

Se saca del vídeo horizontal YA EDITADO (con sus animaciones), recortado a 4:3: en los planos de cara, centrado en él
(con el acercamiento alterno); en los de animación, el 4:3 central sin acercamiento (ahí van las animaciones).

config.json:
{ "fuente": "vídeo horizontal editado (1920x1080)", "tiempos": "trabajo/tiempos.json (palabras en el tiempo del vídeo editado)",
  "montaje": "edicion/montaje.json del proyecto horizontal (qué tramos son animación)", "salida": "out",
  "reels": { "nombre": { "tramos": [[i0, i1], ...], "quitar": [i, ...], "titulo": "en minúsculas, con la primera en mayúscula",
                         "musica": "EMOCIONAL/tema.mp3", "desde": null,
                         "enfasis": [[i0, i1], ...] } } }   frases clave con zoom de énfasis (2–4 por reel; nunca sobre la pantalla blanca)
tramos = índices de palabra en el orden en que se oyen; o por partes: "gancho", "cuerpo", "final" (se unen en ese orden).
Variante: { "de": "reel_1", "gancho": [...], "titulo": "..." } hereda todo de reel_1 y cambia solo lo que trae.
 música = ruta dentro de MUSICA; "desde" = segundo de la
canción (null: el estribillo de MUSICA/catalogo.json, o lo busca por energía).
"""
from mejora_imagen import filtro                      # nitidez + luz compensada, igual en TODOS los reels (Abel 16/10/2026)
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
PAUSA = .45        # corte grueso por los tiempos de Whisper; los microsilencios (≥ 0,2 s) los quita microcortes() midiendo el audio
AIRE = .02         # Abel 14/10/2026, ritmo de Lavri: en cada unión quedan ~0,08 s (antes 0,05 → ~0,14 s), nunca cero
MIN_PLANO = 1.5    # un plano más corto se une al de al lado: dentro de una frase no hay cortecitos
PAUSA_MAX = .45   # pero solo si la pausa que los separa es natural; más larga, se corta (vídeo dinámico)
PAUSA_UNIR = .65  # una palabra suelta («dije», «y») nunca se queda en un plano de medio segundo: se une a su frase si la pausa es ≤ esto
COLA = .45         # el último plano respira
CERCA = 1.30       # plano base MÁS CERCA de su cara (Abel 19/10/2026: en los horizontales sale lejos y la franja queda sosa; Rebeca/Lavri/Luigi ocupan media franja con la cara)
ZOOM = 1.12        # y encima, acercamiento alterno en uno de cada dos cortes de contenido («aplicar el zoom a veces»)
ENFASIS = 1.25     # zoom de énfasis en las frases clave del reel ("enfasis" en el config; Abel 12/10/2026). Nunca sobre la pantalla blanca

# --- música: 26 dB por debajo de la voz (la voz va tal cual), empezando en el estribillo y a su velocidad normal
MUSICA_DB, MUSICA_IN, MUSICA_OUT = -11.5, .4, 1.5   # dB por debajo de la voz. Abel 14/10/2026 a −13,5: «casi ni se escucha» → −11,5 (13/10 había pedido bajarla desde −11,5; a −26 «no hay música»)
COLA_FINAL = .1   # Abel 13/10/2026: el reel acaba 0,1 s tras la última palabra (con 0,5 s «salgo yo ahí sin decir nada»)
FUNDIDO = .04     # fundido de audio en los cortes pegados: nunca un empalme seco (Abel: «se corta muy brusco»)

# --- todo el reel (vídeo, voz, subtítulos) a 1,10x (1,15 era demasiado rápido; 1,07 también le vale); la música no
VELOCIDAD = 1.0                                      # Abel 19/10/2026: velocidad NORMAL en todos los reels («la clave no está en aumentar la velocidad, sino en reducir los silencios»); antes 1,10x


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
    enf = {i for a, b in reel.get('enfasis', []) for i in range(a, b + 1)}     # frases clave: su propio plano, con zoom
    grupos = []
    for a, b in reel['tramos']:
        g = []
        for i in range(a, b + 1):
            if i in quitar:
                if g: grupos.append(g); g = []
                continue
            if g and (W[i]['s'] - W[g[-1]]['e'] > PAUSA or (i in enf) != (g[-1] in enf)): grupos.append(g); g = []
            g.append(i)
        if g: grupos.append(g)
    dur = lambda g: W[g[-1]]['e'] - W[g[0]]['s']
    # unir trocitos cortos con su vecino si son palabras seguidas y la pausa es natural (≤ PAUSA_MAX); un silencio más
    # largo se recorta siempre (Abel, 08/10/2026: «no es fluido ni dinámico»: quedaban pausas de hasta 1,4 s dentro de los planos)
    unible = lambda i, j: j == i + 1 and W[j]['s'] - W[i]['e'] <= PAUSA_UNIR and (i in enf) == (j in enf)
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


def frase(titulo):
    """Títulos de reel con la primera en mayúscula y el resto en minúscula, como en el F1, en todos los formatos (Abel 13/10/2026,
    tras probar las mayúsculas). Si llega todo en MAYÚSCULAS (configs antiguas) se pasa a minúsculas; si no, se respetan los nombres propios."""
    t = titulo.strip()
    if t == t.upper(): t = t.lower()
    return t[:1].upper() + t[1:]


cursiva = lambda l: re.sub(r'(“[^”]+”)', r'{\\i1}\1{\\i0}', l)   # la palabra clave entre comillas, en cursiva (como Lavri)


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
    for w in frase(titulo).split():
        prueba = (lineas[-1] + ' ' + w).strip()
        if lineas[-1] and f.getlength(prueba) > TITULO_ANCHO: lineas.append(w)
        else: lineas[-1] = prueba
    if len(lineas) == 2 or (len(lineas) == 1 and f.getlength(lineas[0]) > TITULO_ANCHO * .75):   # dos líneas equilibradas
        pal = ' '.join(lineas).split()
        k = min(range(1, len(pal)), key=lambda i: abs(f.getlength(' '.join(pal[:i])) - f.getlength(' '.join(pal[i:]))))
        lineas = [' '.join(pal[:k]), ' '.join(pal[k:])]
    ev = [f"Dialogue: 0,{tc(0)},{tc(subs[-1][1] + 5)},Titulo,,0,0,0,,{{\\pos(540,{TITULO_Y + (i - (len(lineas) - 1) / 2) * TITULO_PASO:.0f})}}{cursiva(l)}"
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
            if all(db(u2 + k * .01) < max(-42, pico - 24) for k in range(25)):
                # solo si después ya no vuelve la voz: si la palabra sigue tras la pausa («emocional… mente»), NO se corta
                # (12/10/2026: se perdía el final de «emocionalmente»); esa pausa ya la recorta microcortes
                if not any(db(u2 + .25 + k * .01) > max(-42, pico - 24) for k in range(int((t1n - u2 - .25) / .01))): corte_ = u2
                break
            u2 += .01
        if corte_: out.append((round(t0, 3), round(corte_ + .1, 3), g)); continue
        out.append((round(t0, 3), round(t1n, 3), g))
    # dos planos seguidos de la misma toma nunca se solapan: si el final de uno pasa del inicio del siguiente, el audio se
    # repetía («y son ‖ y son», 12/10/2026). Se cortan en el punto más silencioso entre los dos
    for k in range(1, len(out)):
        (a0, b0, g0), (a1, b1, g1) = out[k - 1], out[k]
        if a1 < b0 and a1 > a0:
            ts = [a1 + j * .01 for j in range(int((b0 - a1) / .01) + 1)]; m = round(min(ts, key=db), 3)
            out[k - 1], out[k] = (a0, m, g0), (m, b1, g1)
    return microcortes(fuente, W, out)


MICRO, MICRO_FIN, MICRO_INICIO, MICRO_PLANO = .10, .03, .04, .12   # Abel 13/10/2026, ritmo de Lavri (reel DeNRktgtcyT: pausas de 0,03–0,08 s): todo silencio ≥ 0,10 s queda en ~0,07 s (antes ~0,13)


def microcortes(fuente, W, ps, desde=None):
    """Abel 12/10/2026 («sí o sí, siempre»): todo silencio REAL de ≥ 0,2 s entre dos palabras se deja en ~0,13 s (0,05 tras la cola + 0,08 antes del arranque, medidos con umbral suave)
   , también dentro de la frase, para más dinamismo. Se mide en el audio, así nunca se corta una palabra; no se corta si
    deja un plano < 1 s ni desde la palabra `desde` (el cierre que no se toca). ps = [(t0, t1, g, *resto)]"""
    import numpy as np
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', fuente, '-vn', '-ac', '1', '-ar', '16000', '-f', 's16le', '-'], capture_output=True).stdout
    x = np.frombuffer(raw, np.int16).astype(float) / 32768; x = x[:len(x) // 160 * 160]
    E = 20 * np.log10(np.sqrt((x.reshape(-1, 160) ** 2).mean(1)) + 1e-9)                    # envolvente cada 10 ms
    out = []
    for t0, t1, g, *resto in ps:
        if desde is not None and g[-1] >= desde: out.append((t0, t1, g, *resto)); continue
        env = list(E[max(0, int(round(t0 * 100))):int(round(t1 * 100))])
        umbral = max(-42, max(env, default=-42) - 30)   # a −24 se comía arranques suaves («habrá»)
        # bordes del plano: fuera el silencio de delante y de detrás (en las uniones quedaban huecos de 0,4–0,6 s), también en el último plano
        voz = [k for k, e in enumerate(env) if e > max(-58, umbral - 8)]
        # un pico de ≤ 0,06 s pegado al borde tras ≥ 0,08 s de silencio es el arranque de la palabra siguiente (o la cola de la
        # anterior), no voz de este plano: fuera, si no dejaba ese silencio dentro (Abel 12/10/2026: pausas ≤ 0,15 s)
        if voz and voz[-1] >= len(env) - 3:                          # final: el último tramo de voz, ¿es un pico suelto?
            k = len(voz) - 1
            while k > 0 and voz[k] - voz[k - 1] <= 1: k -= 1
            if 0 < k and len(voz) - k <= 6 and voz[k] - voz[k - 1] > 8: voz = voz[:k]
        if voz and voz[0] <= 2:                                      # principio: igual con el primer tramo
            k = 0
            while k + 1 < len(voz) and voz[k + 1] - voz[k] <= 1: k += 1
            if k + 1 < len(voz) and k + 1 <= 6 and voz[k + 1] - voz[k] > 8: voz = voz[k + 1:]
        if voz:
            n0 = t0 + max(0, voz[0] * .01 - MICRO_INICIO); n1 = t0 + (voz[-1] + 1) * .01 + MICRO_FIN
            ultimo = (t0, t1, g) == tuple(ps[-1][:3])
            if n0 > t0 + .02: env = env[int(round((n0 - t0) * 100)):]; t0 = round(n0, 3)
            fin = n1 + (.05 if ultimo else 0)              # Abel 13/10/2026: el reel acaba 0,1 s tras la última palabra (antes quedaban ~0,4 s callado)
            if fin < t1 - .02: env = env[:int(round((fin - t0) * 100))]; t1 = round(fin, 3)
        partes, a, ga = [], t0, list(g)
        k = 0
        while k < len(env):
            if env[k] >= umbral: k += 1; continue
            j = k
            while j < len(env) and env[j] < umbral: j += 1
            s0, s1 = t0 + k * .01, t0 + j * .01
            antes = [i for i in ga if W[i]['s'] < (s0 + s1) / 2]; despues = [i for i in ga if W[i]['s'] >= (s0 + s1) / 2]
            dentro = False   # (12/10) sin guarda por tiempos de Whisper: estira palabras sobre los silencios; los bordes se miden en el audio con umbral suave
            # bordes finos con un umbral mucho más bajo: la cola y el arranque suaves («v» de «voy», «te») son voz, no silencio
            suave, k2, j2 = max(-58, umbral - 8), k, j
            while k2 < j and env[k2] > suave: k2 += 1
            while j2 > k2 and env[j2 - 1] > suave: j2 -= 1
            c0, c1 = t0 + k2 * .01 + MICRO_FIN, t0 + j2 * .01 - MICRO_INICIO
            if s1 - s0 >= MICRO and c1 - c0 >= .02 and not dentro and j < len(env) and antes and despues and c0 - a >= MICRO_PLANO and t1 - c1 >= MICRO_PLANO:
                partes.append((round(a, 3), round(c0, 3), antes)); a, ga = c1, despues
            k = j
        partes.append((round(a, 3), t1, ga))
        out += [(p0, p1, pg, *resto) for p0, p1, pg in partes]
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


def ganancia_musica(mus, desde, dur, l_voz):
    """dB que hay que aplicar a la música para que el trozo que suena (desde el estribillo, lo que dura el reel) quede
    exactamente MUSICA_DB por debajo de la voz. Se mide ESE trozo, no la canción entera (Abel 12/10/2026: cada canción suena
    con una intensidad distinta; el volumen tiene que ser el mismo en todos los reels). Ganancia fija: no bombea"""
    err = subprocess.run(['ffmpeg', '-hide_banner', '-nostats', '-ss', str(desde), '-t', f'{dur:.2f}', '-i', str(mus), '-vn', '-af', 'ebur128',
                          '-f', 'null', '-'], capture_output=True, text=True).stderr
    l_mus = float(re.findall(r'I:\s+(-?[\d.]+) LUFS', err)[-1])
    g = max(-30, min(-5, l_voz)) + MUSICA_DB - l_mus
    print(f'  música: el estribillo suena a {l_mus:.1f} LUFS, la voz a {l_voz:.1f} → {g:+.1f} dB (queda {-MUSICA_DB} dB por debajo)')
    return g


def solo_voz(cfg, nombre, reel, W):
    """--voz: <salida>/_<reel>/voz.wav + planos.json, para verificar_audio.py ANTES del render (flujo de reels, paso 3)"""
    ps = ajustar_finales(cfg['fuente'], W, planos(W, reel)); pads = rellenos(W, ps)
    tmp = Path(cfg.get('salida', 'out')).resolve() / f'_{nombre}'; tmp.mkdir(parents=True, exist_ok=True)
    fil = []
    for k, (t0, t1, g) in enumerate(ps):
        d = t1 - t0; fo = FUNDIDO if pads[k] > 0 else .01
        fil.append(f"[0:a]atrim={t0}:{t1},asetpts=PTS-STARTPTS,aresample=48000,afade=t=in:d=0.01,"
                   f"afade=t=out:st={d - fo:.3f}:d={fo},apad=pad_dur={pads[k]}[a{k}];")
    fil.append(''.join(f'[a{k}]' for k in range(len(ps))) + f'concat=n={len(ps)}:v=0:a=1,atempo={VELOCIDAD}[voz]')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', cfg['fuente'], '-filter_complex', ''.join(fil), '-map', '[voz]',
                    str(tmp / 'voz.wav')], check=True)
    (tmp / 'planos.json').write_text(json.dumps([None] + [[t0, t1, p] for (t0, t1, _), p in zip(ps, pads)]))
    dur = sum(b - a + p for (a, b, _), p in zip(ps, pads)) / VELOCIDAD   # listón: ≥ 3,3 palabras/s y la ONDA sin rojos (onda.py)
    print(f"  listón: {sum(len(g) for *_, g in ps) / dur:.2f} palabras/s"); import onda; onda.revisar(tmp / 'voz.wav')
    return tmp


def montar(cfg, nombre, reel, W, cara):
    ps = ajustar_finales(cfg['fuente'], W, planos(W, reel)); cx, fw, fh = cara; anim = ventanas_anim(cfg.get('montaje')); nuc = nucleos(cfg, W)
    toma = 1 if cfg.get('toma') else None
    pads = rellenos(W, ps)
    dur = (sum(b - a for a, b, _ in ps) + sum(pads)) / VELOCIDAD
    tmp = Path(tempfile.mkdtemp(prefix='reel_'))      # ruta sin acentos ni espacios: el filtro ass de ffmpeg lo agradece
    shutil.copy(FUENTE_TTF, tmp / 'm.ttf')
    ass(reel['titulo'], [(a / VELOCIDAD, b / VELOCIDAD, t) for a, b, t in subtitulos(W, ps, pads)], tmp / 's.ass')
    fil, z = [], ZOOM
    enf = {i for a, b in reel.get('enfasis', []) for i in range(a, b + 1)}
    ch0 = fh; cw0 = ch0 * 4 / 3                       # 4:3 a toda la altura del original, centrado en su cara
    for k, (t0, t1, g) in enumerate(ps):
        prev = ps[k - 1][2][-1] if k else None
        if k == 0 or g[0] != prev + 1: z = 1.0 if z != 1.0 else ZOOM
        tz = trozos(t0, t1, g, W, anim, nuc) if toma else [(t0, t1, 0, [(max(a, t0), min(b, t1)) for a, b, _ in anim if a < t1 and b > t0])]
        zz = 1.0 if any(d for *_, d in tz) else CERCA * (ENFASIS / ZOOM if set(g) <= enf else z)   # con animación o pantalla blanca, sin acercamiento
        cw, ch = cw0 / zz, ch0 / zz; xc = f'{min(max(cx - cw / 2, 0), fw - cw):.1f}'; y = (fh - ch) * .35
        for j, (a, b, src, dentro) in enumerate(tz):
            x = xc
            if dentro:                                                     # en la animación, el 4:3 central
                cond = '+'.join(f'between(t,{p - a:.3f},{q - a:.3f})' for p, q in dentro)   # entre comillas: comas sin escapar
                x = f"'if({cond},{(fw - cw) / 2:.1f},{xc})'"
            fil.append(f"[{src}:v]trim={a}:{b},setpts=PTS-STARTPTS,crop={cw:.1f}:{ch:.1f}:{x}:{y:.1f},"
                       f"scale={VID_W}:{VID_H}:flags=lanczos,setsar=1,fps=30,{filtro(cfg['fuente'], horizontal=True)}[v{k}_{j}];"
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
        fil.append(f"[{mi}:a]atrim=0:{dur:.3f},volume={ganancia_musica(mus, desde, dur, voz_lufs(cfg['fuente'])):.2f}dB,"
                   f"afade=t=in:d={MUSICA_IN},afade=t=out:st={dur - MUSICA_OUT:.3f}:d={MUSICA_OUT}[mu];"
                   f"[voz][mu]amix=inputs=2:duration=first:normalize=0,alimiter=limit=0.891:level=0,aresample=48000[a]")
    else:
        fil.append('[voz]alimiter=limit=0.891:level=0,aresample=48000[a]')
    salida = Path(cfg.get('salida', 'out')).resolve(); salida.mkdir(parents=True, exist_ok=True)
    final = salida / f'{nombre}.mp4'
    subprocess.run(['ffmpeg', '-v', 'error', '-y', *entradas, '-filter_complex', ''.join(fil), '-map', '[v]', '-map', '[a]',
                    '-c:v', 'libx264', '-preset', 'medium', '-crf', '18', '-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart',
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
    solo = '--texto' in sys.argv or '--voz' in sys.argv
    cara = None if solo else centro_cara(cfg['fuente'])
    elegidos = sys.argv[sys.argv.index('--solo') + 1].split(',') if '--solo' in sys.argv else None
    for nombre, reel in resolver(cfg['reels']).items():
        if elegidos and nombre not in elegidos: continue
        ps = planos(W, reel)
        print(f"\n== {nombre}: {sum(b - a for a, b, _ in ps) / VELOCIDAD:.1f} s a {VELOCIDAD}x · {len(ps)} planos · «{frase(reel['titulo'])}»")
        print(' | '.join(' '.join(W[i]['w'] for i in g) for _, _, g in ps))
        for a in avisos(W, PW, reel): print('  AVISO:', a)
        if '--voz' in sys.argv: print('  ->', solo_voz(cfg, nombre, reel, W))
        elif not solo: print('  ->', montar(cfg, nombre, reel, W, cara))
