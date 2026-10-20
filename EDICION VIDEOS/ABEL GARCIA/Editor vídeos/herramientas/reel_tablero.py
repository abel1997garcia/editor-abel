"""Reels F3 · TABLERO de Abel (memoria reels-marca-personal; maquetas en MarcaPersonal/formato3/).

    python reel_tablero.py reels.json                  -> <salida>/<reel>.mp4 (1080x1920, 30 fps)
    python reel_tablero.py reels.json --texto          -> texto, duración, avisos y los tramos de tablero con sus palabras
    python reel_tablero.py reels.json --fotos 1,5.5    -> fotogramas sueltos para revisar (<salida>/_<reel>/f_*.png)
    python reel_tablero.py reels.json --solo c01 ...   -> solo ese reel
    python reel_tablero.py reels.json --voz            -> monta solo la voz y dibuja su ONDA (onda.py) para revisarlo todo ANTES del render

reels.json:
{ "fuente": "toma limpia del horizontal (su cara sin animaciones)", "tiempos": "trabajo/tiempos.json en el tiempo de esa toma",
  "salida": "carpeta",
  "reels": { "nombre": { "tramos": [["frase de inicio", "frase final", desde_s], ...],   en el orden en que se oyen
                         "quitar": [["frase", desde_s], ...],                             trocitos dentro de un tramo
                         "titulo": "≤ 7 palabras (sale SIEMPRE en mayúsculas)", "acento": "corona" (centro del tema) o "#hex",
                         "musica": "EMOCIONAL/tema.mp3", "desde": null (estribillo del catálogo),
                         "escenas": "c01.js" | "auto",                                    gráficos del tablero ("auto" = F3 LIGERO; "claves": [...] opcional)
                         "modos": null | [[t, "tablero"|"grande"], ...],                  por defecto se alternan solos
                         "formato": "F2", "imagenes": "imagenes" } } }                  F2 · imagen abajo (motor_f2.html; las fotos en img/)
F4 · él a pantalla completa en vertical (motor_f4.html): "formato": "F4", "imagenes", "titulo",
     "titulo_hasta": s, "apartados": [["1. …", "frase", desde], ...]; en escenas: imagen(), collage(), cta() (Referencias/formato4/analisis.md)
F5 · CASUAL, reels de guion grabados con el móvil (motor_f5.html): "formato": "F5", "titulo" (crudo, completa el hook; todo el reel).
     Como F4 en cortes y zooms, pero sin imágenes, sin escenas y sin efectos; subtítulos en una línea de ≤ 4 palabras.
Gancho en el tablero desde el segundo 0; después tablero ↔ él en grande cada 4–6 s, cambiando entre palabras.
Su voz va tal cual (a VELOCIDAD, como todo el reel); la música MUSICA_DB por debajo desde el estribillo; los efectos que
declaran las escenas (suena) con la proporción del horizontal.
"""
from mejora_imagen import filtro
import json, math, os, re, shutil, subprocess, sys
from pathlib import Path
import numpy as np
AQUI = Path(__file__).resolve().parent
sys.path[:0] = [str(AQUI), str(AQUI / 'pizarra')]
from reel_yapping import frase, planos, VELOCIDAD, MUSICA, MUSICA_IN, MUSICA_OUT, AIRE, MUSICA_DB, COLA_FINAL, FUNDIDO, rellenos, ajustar_finales, estribillo, voz_lufs, centro_cara, ganancia_musica
from ventanas import buscar

TAB = AQUI / 'tablero'
SON = AQUI / 'sonidos'
CENTROS = {'raiz': '#C8372D', 'sacro': '#E06A1B', 'plexo': '#C99A00', 'corazon': '#1E7A46', 'garganta': '#1D7FD1', 'ojo': '#3F3FB5', 'corona': '#7A3FC4'}
FW, FH, SR = 1280, 720, 48000
VOZ_LUFS = -14
TRAMO_MIN, TRAMO_OBJ, TRAMO_MAX = 2.8, 3.6, 4.8      # tablero ↔ él cada 3–4,5 s (Abel 08/10: «muy pausado»)
GANCHO_MIN = 3.5                                       # el gancho se queda en el tablero al menos esto


def fin_desde(W, frase, a):
    """índice de la última palabra de `frase` buscándola desde la palabra `a` (nunca antes): con tomas repetidas seguidas, buscar
    por tiempo (buscar() mira 1 s hacia atrás) cogía la toma anterior y el tramo quedaba vacío (Abel 14/10/2026, «borras los vídeos»)"""
    from ventanas import norm
    f = [norm(x) for x in frase.split()]
    for k in range(a, len(W) - len(f) + 1):
        if [norm(W[k + j]['w']) for j in range(len(f))] == f: return k + len(f) - 1
    sys.exit(f'no encuentro «{frase}» después de «{W[a]["w"]}» ({W[a]["s"]:.2f} s)')


def indices(W, reel):
    tr = []
    for ini, fin, desde in reel['tramos']:
        a, _ = buscar(W, ini, desde); tr.append([a, fin_desde(W, fin, a)])
    q = []
    for frase, desde in reel.get('quitar', []):
        a, b = buscar(W, frase, desde); q += list(range(a, b + 1))
    return {'tramos': tr, 'quitar': q}


import threading
_WH = {'m': None, 'lock': threading.Lock()}
def oidas(tmp, PAL):
    """SUBTÍTULOS SINCRONIZADOS (Abel 14/10/2026): los tiempos de cada palabra salen de ESCUCHAR la voz montada (voz.wav, ya
    a la velocidad del reel), no de la transcripción de la grabación. El texto sigue siendo el de PAL; la primera, en mayúscula."""
    import difflib, re
    c = tmp / 'pal_oido.json'
    if c.exists() and json.loads(c.read_text(encoding='utf-8'))['n'] == len(PAL) and c.stat().st_mtime > (tmp / 'voz.wav').stat().st_mtime:
        PAL = json.loads(c.read_text(encoding='utf-8'))['pal']
    else:
        with _WH['lock']:
            if _WH['m'] is None:
                import torch  # noqa: F401
                from faster_whisper import WhisperModel
                _WH['m'] = WhisperModel('large-v3', device='cuda', compute_type='float16')
            from casual_prep import LITERAL
            oido = [(w.word.strip(), w.start, w.end) for sg in _WH['m'].transcribe(str(tmp / 'voz.wav'), language='es', word_timestamps=True,
                    initial_prompt=LITERAL, condition_on_previous_text=False)[0] for w in sg.words]
        nz = lambda x: re.sub(r'[^a-z0-9ñ]', '', str(x).lower().translate(str.maketrans('áéíóúü', 'aeiouu')))
        A, B = [nz(p[0]) for p in PAL], [nz(o[0]) for o in oido]
        PAL = [list(p) for p in PAL]
        for blk in difflib.SequenceMatcher(None, A, B, autojunk=False).get_matching_blocks():
            for q in range(blk.size): PAL[blk.a + q][1], PAL[blk.a + q][2] = round(oido[blk.b + q][1], 3), round(oido[blk.b + q][2], 3)
        c.write_text(json.dumps({'n': len(PAL), 'pal': PAL}, ensure_ascii=False), encoding='utf-8')
    PROPIOS = {'rubius', 'siroko', 'gijón', 'gijon', 'youtube', 'instagram', 'tiktok', 'clash', 'royale', 'clap', 'abel', 'españa', 'australia', 'madrid'}
    for k, p in enumerate(PAL):                               # MAYÚSCULA solo al empezar y tras punto; el resto en minúscula (Whisper ponía «es Así»,
        w = str(p[0]); base = re.sub(r'[^\wáéíóúñü]', '', w.lower())   # «Porque no se reconoce» a mitad de frase, 085); los nombres propios, siempre
        if k == 0 or str(PAL[k - 1][0]).rstrip().endswith(('.', '?', '!', '…')) or base in PROPIOS: p[0] = w[:1].upper() + w[1:]
        elif w[:1].isupper() and not w.isupper(): p[0] = w[:1].lower() + w[1:]
    return PAL


def corrige_texto(PAL, cambios):
    """«corrige» (reels.json): [[«lo que oyó Whisper», «lo que dijo»], ...] palabra a palabra sobre los subtítulos, conservando los tiempos
    (085: «hace nadar el Rubius a que unas zapatillas con siroco» → «hace nada el Rubius sacó unas zapatillas con Siroko»)"""
    import re
    nz = lambda x: re.sub(r'[^a-z0-9ñ]', '', str(x).lower().translate(str.maketrans('áéíóúü', 'aeiouu')))
    for mal, bien in cambios:
        m, b = mal.split(), bien.split()
        for k in range(len(PAL) - len(m) + 1):
            if [nz(PAL[k + j][0]) for j in range(len(m))] == [nz(x) for x in m]:
                for j in range(len(m)):
                    tail = re.sub(r'^[\wáéíóúñü]+', '', str(PAL[k + j][0]))          # conserva la puntuación de Whisper
                    PAL[k + j][0] = (b[j] + tail) if j < len(b) else ''              # si junta palabras («100 .000» → «100.000»), las demás desaparecen
                if len(b) > len(m): PAL[k + len(m) - 1][0] += ' ' + ' '.join(b[len(m):])
    return [p for p in PAL if str(p[0]).strip()]


def palabras(W, ps, pads):
    out, T = [], 0.0
    for (t0, t1, g), pd in zip(ps, pads):
        out += [[W[i]['w'], round((T + W[i]['s'] - t0) / VELOCIDAD, 3), round((T + W[i]['e'] - t0) / VELOCIDAD, 3)] for i in g]
        T += t1 - t0 + pd
    return out


def modos_auto(PAL, dur):
    """tablero desde 0 con el gancho (hasta el final de su primera frase); luego se alterna en los huecos entre palabras"""
    hueco = lambda i: PAL[i][1] - PAL[i - 1][2]
    def corte(desde, lo, hi):
        cand = [i for i in range(1, len(PAL)) if desde + lo <= PAL[i][1] <= desde + hi]
        if not cand: return None
        return PAL[max(cand, key=lambda i: hueco(i) - .05 * abs(PAL[i][1] - desde - TRAMO_OBJ))][1] - .05
    m, t, modo = [[0, 'tablero']], 0.0, 'tablero'
    t1 = corte(0, GANCHO_MIN, TRAMO_MAX + 1)
    while t1 and dur - t1 > 2.5:
        modo = 'grande' if modo == 'tablero' else 'tablero'; m.append([round(t1, 3), modo]); t = t1
        t1 = corte(t, TRAMO_MIN, TRAMO_MAX)
    return m


def titulo2(titulo):
    pal = frase(titulo).split()
    if len(pal) < 4: return [' '.join(pal)]
    feo = lambda i: pal[i - 1].startswith('(') or len(pal[i - 1].strip('"«(')) <= 2 or pal[i].startswith(')') or ' '.join(pal[:i]).count('"') % 2 == 1   # nunca «… (y» / «… de» al final de la 1.ª línea
    k = min(range(1, len(pal)), key=lambda i: abs(len(' '.join(pal[:i])) - len(' '.join(pal[i:]))) + (40 if feo(i) else 0))
    return [' '.join(pal[:k]), ' '.join(pal[k:])]


_SUAVE = threading.Lock()


def voz_suave(fuente):
    """la voz que SE OYE: DeepFilterNet suave (-15 dB, sin postfiltro). La fuerte (_fuente_limpia, -40 dB) sonaba «rara»
    (Abel 14/10/2026); esa se queda solo para medir la onda y decidir los cortes"""
    d = Path(fuente).parent; v = d / '_voz_suave.wav'
    with _SUAVE:                                              # los 3 reels van en hilos: que solo uno la cree (si no, se borraban la carpeta)
        if not v.exists():
            tmp = d / '_dfs'; shutil.rmtree(tmp, ignore_errors=True); tmp.mkdir()
            subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(fuente), '-vn', '-ac', '1', '-ar', '48000', str(tmp / 'voz.wav')], check=True)
            subprocess.run([str(AQUI / 'deepfilter' / 'deep-filter.exe'), '-D', '-a', '15', '-o', str(tmp / 'out'), str(tmp / 'voz.wav')], check=True, capture_output=True)
            shutil.move(str(tmp / 'out' / 'voz.wav'), v); shutil.rmtree(tmp, ignore_errors=True)
    return v


def clip(cfg, ps, pads, tmp, vf, fundidos=()):
    lim = Path(cfg['fuente']).parent / '_fuente_limpia.wav'     # con voz limpia (casual_prep) se monta la versión SUAVE
    A, ent = (1, ['-i', str(voz_suave(cfg['fuente']))]) if lim.exists() else (0, [])
    fil = []
    for k, ((t0, t1, g), pd) in enumerate(zip(ps, pads)):
        d = t1 - t0
        fo = .06 if any(abs(t1 - x) < .05 for x in fundidos) else .02   # «fundidos» (reels.json): final que no cae en silencio («información|y», 079)
        _fo_ = .02                                              # el corte ya cae en silencio (igualar): un fundido corto basta y no se come la cola de la palabra
        fil.append(f"[0:v]trim={t0}:{t1},setpts=PTS-STARTPTS,{vf},fps=30,setsar=1,tpad=stop_mode=clone:stop_duration={pd}[v{k}];"
                   f"[{A}:a]atrim={t0}:{t1},asetpts=PTS-STARTPTS,afade=t=in:d=0.01,afade=t=out:st={d - fo:.3f}:d={fo},apad=pad_dur={pd}[a{k}];")
    n = len(ps)
    fil.append(''.join(f'[v{k}][a{k}]' for k in range(n)) + f'concat=n={n}:v=1:a=1[vc][ac];'
               f'[vc]setpts=PTS/{VELOCIDAD},fps=30[v];[ac]atempo={VELOCIDAD},{PRESENCIA if A else ""}aresample={SR}[a]')
    (tmp / 'clip.txt').write_text(''.join(fil), encoding='utf-8')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', cfg['fuente'], *ent, '-/filter_complex', str(tmp / 'clip.txt'), '-map', '[v]', '-map', '[a]',
                    '-c:v', 'libx264', '-crf', '16', '-preset', 'veryfast', '-c:a', 'pcm_s16le', str(tmp / 'clip.mov')], check=True)
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(tmp / 'clip.mov'), '-vn', '-c:a', 'pcm_s16le', str(tmp / 'voz.wav')], check=True)
    fr = tmp / 'frames'; shutil.rmtree(fr, ignore_errors=True); fr.mkdir()
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(tmp / 'clip.mov'), '-q:v', '3', str(fr / '%05d.jpg')], check=True)


PRESENCIA = 'highpass=f=80,equalizer=f=250:t=q:w=1.2:g=-2,equalizer=f=3500:t=q:w=1.2:g=1.5,highshelf=f=6000:g=3,acompressor=threshold=-20dB:ratio=2:attack=10:release=150:makeup=1.5,'   # sin expansor: se comía las «s» y la voz sonaba rara (Abel 14/10/2026)


def limpiar_voz(tmp, fuerza=40):
    """Quita ruido y eco de la habitación con DeepFilterNet (herramientas/deepfilter/deep-filter.exe, IA, v0.5.6) y le da
    un toque de presencia. fuerza = dB máximos de atenuación (40: limpio pero natural; 100 suena robótico).
    Guarda la original en voz_original.wav. Abel 10/10: «suena mucho eco»."""
    ori, voz = tmp / 'voz_original.wav', tmp / 'voz.wav'
    shutil.copy(voz, ori); d = tmp / '_df'; shutil.rmtree(d, ignore_errors=True)
    subprocess.run([str(AQUI / 'deepfilter' / 'deep-filter.exe'), '-D', '--pf', '-a', str(fuerza), '-o', str(d), str(ori)], check=True, capture_output=True)
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(d / 'voz_original.wav'), '-af',
                    f'{PRESENCIA}aresample={SR}', '-c:a', 'pcm_s16le', str(voz)], check=True)
    shutil.rmtree(d, ignore_errors=True); print(f'  voz limpia (DeepFilterNet, -{fuerza} dB)')


def colores_texto(tmp, hasta):
    """F4: color del título y de los subtítulos según el fondo real que tienen detrás (Abel: con fondo blanco, el texto blanco
    no se ve). Luminosidad media de la zona en los fotogramas: clara -> texto oscuro con halo claro; oscura -> blanco con sombra."""
    from PIL import Image
    fr = sorted((tmp / 'frames').glob('*.jpg'))
    def lum(sel, caja):
        v = []
        for f in sel:
            im = Image.open(f).convert('L').resize((270, 480)); x0, y0, x1, y1 = [c // 4 for c in caja]
            v.append(sum(im.crop((x0, y0, x1, y1)).getdata()) / ((x1 - x0) * (y1 - y0)) / 255)
        return sorted(v)[len(v) // 2] if v else 0
    tit = lum(fr[:max(1, int(hasta * 30)):10], (100, 150, 980, 380))
    sub = lum(fr[::30], (220, 1120, 860, 1260))
    oscuro = lambda l: {'color': '#141414', 'sombra': '0 2px 16px rgba(255,255,255,.75), 0 0 3px rgba(255,255,255,.6)'} if l > .6 else \
        {'color': '#ffffff', 'sombra': '0 3px 18px rgba(0,0,0,.65), 0 0 4px rgba(0,0,0,.6)'}
    print(f'  fondo: título {tit:.2f}, subtítulos {sub:.2f} (0 negro, 1 blanco)')
    return {'tit': oscuro(tit), 'sub': oscuro(sub)}


def efectos(sfx, dur, l_voz, ruta):
    import soundfile as sf
    cat = json.load(open(SON / 'sonidos.json', encoding='utf-8'))
    pista = np.zeros((int((dur + 3) * SR), 2))
    for t, nombre, vol in sfx:
        m = cat[nombre]; x, sr = sf.read(str(SON / m['archivo']), always_2d=True)
        if sr != SR: x = np.stack([np.interp(np.arange(0, len(x), sr / SR), np.arange(len(x)), x[:, c]) for c in range(x.shape[1])], 1)
        if x.shape[1] == 1: x = np.repeat(x, 2, 1)
        g = 10 ** ((m['gain_db'] + 20 * math.log10(max(1e-4, vol)) + (l_voz + 16)) / 20)   # como junto a la voz a −16 LUFS del horizontal
        i0 = max(0, int(round((t - (m['dur'] if m['ancla'] == 'fin' else m['pico'])) * SR)))
        n = min(len(x), len(pista) - i0); pista[i0:i0 + n] += g * x[:n]
    sf.write(str(ruta), pista[:int(dur * SR)], SR)


_ONDAS = {}
def igualar(W, ps, fuente, deja=.04, final=COLA_FINAL, cuchillas=(), fuera=(), respira=()):
    """CORTAR COMO UN EDITOR MIRANDO LA ONDA (Abel 14/10/2026). En la voz limpia se marcan las ISLAS de voz (separadas por
    silencios reales de ≥ 60 ms). Cada plano (tramo de reels.json) se monta con sus islas ENTERAS: nunca se corta sobre
    una palabra ni se pierde un trozo. Entre islas queda `deja` s de aire en el reel (si en la toma había menos, se respeta
    su ritmo). Whisper solo decide QUÉ islas van (y los subtítulos), no dónde se corta."""
    import onda
    if fuente not in _ONDAS:
        E = onda.envolvente(fuente)[1]; sil = E < np.percentile(E, 95) - 35; isl, k, n = [], 0, len(sil)   # −35 dB: la cola de la palabra aún es voz
        while k < n:
            if sil[k]: k += 1; continue
            j = k
            while j < n and not sil[j]: j += 1
            isl.append([k * onda.PASO, j * onda.PASO]); k = j
        jun = []
        for a, b in isl:                                      # dentro de una palabra hay baches de < 60 ms: no son silencios
            if jun and a - jun[-1][1] < .06: jun[-1][1] = b
            else: jun.append([a, b])
        _ONDAS[fuente] = ([z for z in jun if z[1] - z[0] >= .04], E, onda.agudos(fuente), onda.graves(fuente))
    ISL, E, EH, EL = _ONDAS[fuente]; V, m = VELOCIDAD, .025
    umH = np.percentile(EH, 95) - 40
    def sese(a, tope):                                        # el trozo empieza antes mientras suenen agudos (una «s» floja al
        k, n = int(a / onda.PASO), 0                          # principio: «Solo» salía «holo», Abel 14/10/2026), sin pasar de `tope`
        while n < 15 and k > 0 and (k - 1) * onda.PASO > tope and EH[k - 1] > umH: k -= 1; n += 1
        return min(a, k * onda.PASO)
    vl_ = np.percentile(EL, 95)
    sonora = lambda y: max(EL[int(y[0] / onda.PASO):int(y[1] / onda.PASO) + 1], default=-200) > vl_ - 20   # tiene voz en graves (no es solo una «s»)
    nz = lambda x: re.sub(r'[^a-zñ]', '', str(x).lower().translate(str.maketrans('áéíóúü', 'aeiouu')))
    def voz_graves(t, d):
        k = int(t / onda.PASO) + d * 2
        while 0 < k < len(EL) - 1 and EL[k] <= vl_ - 20: k += d
        return k * onda.PASO
    def sese_lejos(t, tope, d):                               # busca la «s» en los 0,3 s siguientes (d=1) o anteriores (d=-1), aunque haya
        P_ = onda.PASO; k = int(t / P_); fin = None           # un hueco antes; devuelve dónde acaba (o empieza) esa «s»
        for n in range(1, 31):
            q = k + d * n
            if q <= 0 or q >= len(EH) - 1 or (q * P_ > tope if d > 0 else q * P_ < tope): break
            if EH[q] > umH and EH[q] - EL[q] > -12: fin = q                                   # agudos fuertes y no son vocal
            elif fin is not None and abs(q - fin) > 3: break
        return (fin * P_ if fin is not None else t)
    def sese_fin(b, tope):                                    # y el final, mientras suene la «s» de «publicas» (salía «publica»)
        k, n = int(b / onda.PASO), 0
        while n < 15 and k < len(EH) - 1 and (k + 1) * onda.PASO < tope and EH[k] > umH: k += 1; n += 1
        return max(b, k * onda.PASO)
    mi, mf = .02, .02                                         # margen antes y después de cada trozo: una «s» inicial suena muy floja
                                                              # y sin margen se perdía («Solo» → «olo», Abel 14/10/2026)
    for a, b in fuera:                                        # "fuera" (reels.json): [ini, fin] de la grabación que se borra a mano
        ISL = [y for z in ISL for y in (([[z[0], a]] if z[0] < a else []) + ([[b, z[1]]] if z[1] > b else []) if z[0] < b and z[1] > a else [z])
               if y[1] - y[0] > .03]
    for c in cuchillas:                                       # "cuchillas" (reels.json): dos tomas sin pausa entre ellas; se parte
        ISL = [y for z in ISL for y in ([[z[0], c - m], [c + m, z[1]]] if z[0] < c < z[1] else [z])]   # la isla en ese segundo
    def arranque(ws):                                         # «ventas → …s Vivimos»: el valle más hondo quedaba ANTES de la «s» final
        P_, v = onda.PASO, np.percentile(E, 95)               # de la toma anterior. Se busca dónde arranca la palabra (voz fuerte) y
        k = max(0, int((ws - .15) / P_))                      # desde ahí hacia atrás el primer silencio
        vl = np.percentile(EL, 95)                            # el arranque se mide en los GRAVES: la «s» de «clientes» no suena ahí
        while k < len(EL) - 6 and k * P_ < ws + .25 and not all(EL[k + i] > vl - 14 for i in range(5)): k += 1
        j = k
        while j > k - 25 and j > 0 and EL[j] > vl - 30: j -= 1
        return j * P_ + .005
    def valle(a, b):                                          # sin silencio entre dos tomas («subirlos. Borras»): se corta en
        i, j = max(0, int(a / onda.PASO)), min(len(E) - 1, int(b / onda.PASO))   # el punto más bajo de la onda
        return (i + int(np.argmin(E[i:j + 1]))) * onda.PASO if j > i else a
    D = deja * V
    junto = [[ps[0][0], ps[0][1], list(ps[0][2])]]           # planos seguidos de la misma toma = uno (Whisper los separaba)
    for t0, t1, g in ps[1:]:
        if g[0] == junto[-1][2][-1] + 1: junto[-1][1] = t1; junto[-1][2] += list(g)
        else: junto.append([t0, t1, list(g)])
    trozos, justos = [], set()
    for k, (t0, t1, g) in enumerate(junto):
        ws, we = min(W[i]['s'] for i in g), max(W[i]['e'] for i in g)
        mias = [z for z in ISL if z[1] > ws - .3 and z[0] < we + .05 and
                (min(z[1], we) - max(z[0], ws) >= .5 * (z[1] - z[0]) or ws - .25 <= (z[0] + z[1]) / 2 <= we + .05
                 or z[0] <= ws + .05 < z[1] or z[0] < we - .05 <= z[1])]   # la isla que CONTIENE el principio o el final de la frase entra
                                                                           # (y abajo se recorta): si no, se perdían frases enteras pegadas a
                                                                           # otra toma («Y eso no es verdad», «Al principio cuesta…»)   # Whisper empieza hasta 0,3 s tarde («copias»)
        if not mias: mias = [[ws, we]]
        mias = [list(z) for z in mias]
        mias = [list(z) for z in mias]                       # la isla trae habla de antes (otra toma, otro gancho sin silencio claro
        if mias[0][0] < ws - .4: mias[0][0] = arranque(ws); justos.add(round(mias[0][0], 4))   # se corta JUSTO antes de su primera palabra (sin margen)
        if mias[-1][1] > we + .6: mias[-1][1] = valle(we - .05, we + .5) - .01  # y si sigue mucho después de la última palabra, en el valle
        seg = [[mias[0][0], mias[0][1]]]
        for a, b in mias[1:]:                                 # hueco natural más corto que el aire: se queda tal cual
            if a - seg[-1][1] < D: seg[-1][1] = b
            else: seg.append([a, b])
        par = [[a, b, []] for a, b in seg]
        for i in g:                                           # cada palabra, a la isla con la que más se solapa
            ov = [min(W[i]['e'], z[1]) - max(W[i]['s'], z[0]) for z in par]
            par[max(range(len(par)), key=lambda q: (ov[q], -abs((W[i]['s'] + W[i]['e']) / 2 - (par[q][0] + par[q][1]) / 2)))][2].append(i)
        for q, z in enumerate(par):                           # una isla sin palabra (Whisper la estiró a la de al lado) se queda con la palabra más cercana
            if z[2]: continue
            for j in (q - 1, q + 1):
                if 0 <= j < len(par) and len(par[j][2]) > 1:
                    z[2].append(par[j][2].pop(0 if j > q else -1)); break
        for z in par:                                         # una isla sin palabra es una respiración (coger aire): fuera, siempre
            if not z[2]: continue
            antes, despues = voz_graves(z[0], -1) + .02, voz_graves(z[1], 1) - .02   # tope: donde vuelve a sonar VOZ (graves) antes/después;
                                                                                     # una «s» pegada a la palabra siguiente («publicas Yo») no es tope
            gz = sorted(z[2]); w0, w1 = nz(W[gz[0]]['w']), nz(W[gz[-1]]['w'])
            ini = z[0] if round(z[0], 4) in justos else z[0] - mi
            if w0[:1] in 'szfjx' or w0[:2] in ('ce', 'ci', 'ch'): ini = min(ini, sese_lejos(z[0], antes, -1) - .01)   # «Solo»: su «s» delante
            fin = z[1] + mf
            if w1[-1:] in 'szx': fin = max(fin, sese_lejos(z[1], despues, 1) + .02)   # «publicas»: la «s» llega SEPARADA, tras un huequito
            trozos.append([ini, fin, gz])
    import math                                               # cortes en fotogramas exactos (1/30 s; si no, la voz se desfasaba):
    fl = lambda x: round(math.floor(x * 30 + 1e-6) / 30, 4)  # inicio hacia ANTES (el golpe de una «t», «c», «d» no se puede recortar)
    ce = lambda x: round(round(x * 30) / 30, 4)              # final al fotograma más cercano (hacia fuera sumaba silencio de más)
                                                              # (las «s» ya van protegidas por sese_lejos con el texto)
    out, pads = [], []
    for k, (a, b, g) in enumerate(trozos):
        A, B = fl(a), ce(b)
        if k + 1 < len(trozos) and -(mi + mf) - .005 <= trozos[k + 1][0] - b <= 0: B = fl(trozos[k + 1][0])   # justo detrás en la toma: tal cual
        if out and out[-1][0] < A < out[-1][1]: A = out[-1][1]                          # nunca se solapan dos trozos
        out.append((A, max(B, round(A + 2 / 30, 4)), g))
    for k in range(len(out)):
        if k == len(out) - 1: pads.append(ce(max(0, final * V - (out[k][1] - trozos[k][1] + mf)))); continue
        if out[k][1] == out[k + 1][0]: pads.append(0); continue
        aire = (out[k][1] - (trozos[k][1] - mf)) + ((trozos[k + 1][0] + mi) - out[k + 1][0])   # silencio que ya dejan los dos bordes
        Dk = D                                                # TODAS las uniones cortas, también tras punto (Abel 15/10: «muy muy cortos, dinámico»)
        if aire > Dk:                                          # sobra aire: se quita del final de la palabra anterior (deja 20 ms), nunca del arranque
            q = math.floor(min(aire - Dk, out[k][1] - (trozos[k][1] - mf) - .02) * 30) / 30
            if q > 0: out[k] = (out[k][0], round(out[k][1] - q, 4), out[k][2])
        envoz = E[min(len(E) - 1, int(out[k][1] / onda.PASO) - 1)] > np.percentile(E, 95) - 35 or E[min(len(E) - 1, int(out[k + 1][0] / onda.PASO))] > np.percentile(E, 95) - 35
        pads.append(max(round(round(max(0, Dk - aire) * 30) / 30, 4), round(2 / 30, 4) if envoz else 0))   # corte en habla seguida: 2 fotogramas de silencio
    for t in respira:                                         # "aire" (reels.json): cortes en habla seguida que la revisión oye pegados
        for k, (a, b, g) in enumerate(out[:-1]):              # (segundo de la grabación donde acaba el trozo): 2 fotogramas de silencio
            if abs(b - t) < .06: pads[k] = max(pads[k], round(2 / 30, 4))
    return out, pads


def encerrar(ps, pads, ventanas):
    """recorta cada trozo a la VENTANA de su frase (ver hacer): fuera de ahí suena otra toma. Si un trozo desaparece,
    sus palabras pasan al de al lado (si no, faltaban subtítulos, 082)."""
    out, op = [], []
    for (a, b, g), pd in zip(ps, pads):
        v = next(((lo, hi) for ia, ib, lo, hi in ventanas if g and ia <= g[0] <= ib), None)
        if v: a, b = max(a, math.ceil(v[0] * 30 - 1e-6) / 30), min(b, math.floor(v[1] * 30 + 1e-6) / 30)
        if b - a >= 2 / 30: out.append([round(a, 4), round(b, 4), list(g)]); op.append(pd)
        elif out: out[-1][2] += list(g)
        else: out.append(None); op.append(pd); out[-1] = [a, a, list(g)]   # (se arregla abajo)
    res, rp, colgadas = [], [], []
    for x, pd in zip(out, op):
        if x[1] - x[0] < 2 / 30: colgadas += x[2]; continue
        x[2] = colgadas + x[2]; colgadas = []; res.append(tuple(x)); rp.append(pd)
    return res, rp


def apretar(ps, pads, fuente, objetivo=.06, minimo=.04, cola=.05, arranque=.03, fuera=(), W=None):
    """Aprieta cada unión. DÓNDE ACABA/EMPIEZA una palabra se mide con umbral PERMISIVO (pico − 36 dB, agudos +20): los finales
    flojos («mundo», «verdad», «información») son palabra y NUNCA se tocan (Abel 15/10/2026: «información la cortas en la voz»;
    con −24 dB se comían). CUÁNTO SILENCIO queda se mide como la onda (−27 dB). Trozos de ruido < 0,15 s sin voz: fuera."""
    import math, onda
    if fuente not in _ONDAS_ESTRICTA:
        _, E = onda.envolvente(fuente); _ONDAS_ESTRICTA[fuente] = (E, np.percentile(E, 95))
    E, pico = _ONDAS_ESTRICTA[fuente]; P = onda.PASO; V = VELOCIDAD
    lax, thr = pico - 30, pico - 27                                           # −30: conserva la voz floja, deja fuera la respiración
    e = lambda t: E[min(len(E) - 1, max(0, int(t / P)))]
    v1 = lambda t: e(t) > lax
    voz = lambda t: v1(t) and (v1(t + P) and v1(t + 2 * P) or v1(t - P) and v1(t - 2 * P))   # 30 ms seguidos: un chasquido no es voz
    fl = lambda x: math.floor(x * 30 + 1e-6) / 30; ce = lambda x: math.ceil(x * 30 - 1e-6) / 30
    ps = [list(x) for x in ps]; pads = list(pads)
    for x in ps:                                                                # ningún trozo se mete en lo quitado a mano
        for f0, f1 in fuera:
            if x[0] < f0 < x[1]: x[1] = round(max(x[0] + 2 / 30, math.floor(f0 * 30 + 1e-6) / 30), 4)
    empieza = lambda x: W is not None and any(x[0] - .08 <= W[i]['s'] <= x[1] for i in x[2])          # dentro empieza una palabra (el «Y» flojo)
    def filtra(ps, pads):                                                       # trozo corto sin palabra = respiración / cola alargada por Whisper
        keep = [k for k, x in enumerate(ps) if not (x[1] - x[0] < .25 and not empieza(x))]
        for k in range(len(ps)):                                                # sus PALABRAS no se pierden (suenan en el trozo de al lado): sin esto
            if k not in keep and keep:                                          # faltaban subtítulos («mundo», «verdad», «de ti», 082)
                v = max([q for q in keep if q < k], default=None)
                if v is None: v = min(q for q in keep if q > k); ps[v][2] = list(ps[k][2]) + list(ps[v][2])
                else: ps[v][2] = list(ps[v][2]) + list(ps[k][2])
        return [ps[k] for k in keep], [pads[k] for k in keep]
    ps, pads = filtra(ps, pads)
    for k in range(len(ps)):
        a, b = ps[k][0], ps[k][1]
        if k + 1 < len(ps) and ps[k + 1][0] == b and pads[k] == 0: continue    # sin corte: sigue tal cual
        fin_voz = b
        while fin_voz - P > a and not voz(fin_voz - P): fin_voz -= P            # dónde acaba DE VERDAD la palabra (umbral permisivo)
        if k == 0:
            ini0 = a
            while ini0 + P < b and not voz(ini0): ini0 += P
            ps[k][0] = round(max(a, fl(ini0 - arranque)), 4)
        ps[k][1] = round(min(b, max(ce(fin_voz + cola), a + 2 / 30)), 4)
        if k == len(ps) - 1: continue
        a2, b2 = ps[k + 1][0], ps[k + 1][1]; ini2 = a2
        while ini2 + P < b2 and not voz(ini2): ini2 += P
        nuevo = fl(ini2 - arranque)
        ps[k + 1][0] = round(max(a2, nuevo) if ini2 - a2 >= arranque else nuevo, 4)
        for f0, f1 in fuera:
            if f0 <= ps[k + 1][0] < f1 <= a2 + .2: ps[k + 1][0] = round(max(a2, math.ceil(f1 * 30 - 1e-6) / 30), 4)
        pads[k] = 0 if pads[k] < 1 / 30 else pads[k]                            # el silencio final lo decide afinar_con_onda midiendo el reel
    unidos, up = [], []                                                         # trozos SEGUIDOS en la grabación = uno (la pausa podía caer en el límite)
    for x, pd in zip(ps, pads):
        if unidos and abs(unidos[-1][1] - x[0]) < .002 and up[-1] == 0: unidos[-1] = [unidos[-1][0], x[1], list(unidos[-1][2]) + list(x[2])]; up[-1] = pd
        else: unidos.append([x[0], x[1], list(x[2])]); up.append(pd)
    ps, pads = unidos, up
    partidos, pp = [], []                                                       # PAUSAS DENTRO de una frase seguida (no solo en los cortes): toda pausa
    for (a, b, g), pd in zip(ps, pads):                                         # > 0,10 s medida como la onda se queda en ~0,07 (085: «personal. | ¿Cuál es»)
        t, ini = a, a
        while t < b:
            if e(t) < thr:
                u = t
                while u < b and e(u) < thr: u += P
                if u - t > .10 * V and t - ini > .1 and b - u > .1:
                    corte_a, corte_b = round(fl(t + .04), 4), round(fl(u - .03), 4)
                    if corte_b - corte_a >= 2 / 30:
                        izq = [i for i in g if W is None or W[i]['s'] < corte_a]; der = [i for i in g if i not in izq]
                        partidos.append([ini, corte_a, izq]); pp.append(0); ini, g = corte_b, der
                t = u
            else: t += P
        partidos.append([ini, b, g]); pp.append(pd)
    ps, pads = partidos, pp
    ps, pads = filtra(ps, pads)                                                # otra vez: al ajustar bordes un trozo puede quedarse corto (respiración tras «perteneces»)
    return [tuple(x) for x in ps], pads


_ONDAS_ESTRICTA = {}


def silencio_en(E, thr, t, relleno, P=.01):
    """el silencio (por debajo de thr) que TOCA la unión del reel: el tramo que contiene [t, t + relleno] o lo roza (±30 ms)"""
    a, b = int((t - .03) / P), int((t + relleno + .03) / P)
    mejor = 0
    for i in range(max(0, a), min(len(E), b + 1)):
        if E[i] >= thr: continue
        l = r = i
        while l > 0 and E[l - 1] < thr: l -= 1
        while r < len(E) and E[r] < thr: r += 1
        mejor = max(mejor, r - l)
    return mejor * P


def afinar_con_onda(ps, pads, voz, maximo=.07, minimo=.03):
    """Mide el reel YA MONTADO con onda.py (voz = pico − 27 dB, como la mide Abel) y deja CADA unión entre `minimo` y `maximo`
    de silencio: nunca más larga que la pausa gancho→cuerpo (≈0,09 s, Abel 15/10/2026: «los silencios más largos tienen que
    durar como máximo lo que hay entre el gancho y cuando empieza»), ni pegada. Si sobra: relleno y luego cola (máx. 50 ms)."""
    import math, onda
    _, E = onda.envolvente(voz); thr = np.percentile(E, 95) - 27; P = onda.PASO; V = VELOCIDAD
    ps = [list(x) for x in ps]; pads = list(pads); T = 0.0
    for k, ((a, b, _g), pd) in enumerate(zip(ps, pads)):
        T += (b - a) / V
        if k < len(ps) - 1 and not (ps[k + 1][0] == b and pd == 0):
            sil = max(silencio_en(E, thr, T, pd / V), silencio_en(E, thr - 3, T, pd / V))   # como la onda (−27) y como revisar_cortes (−30)
            sil_min = silencio_en(E, thr - 3, T, pd / V)
            if sil > maximo + .005:
                sobra = (sil - maximo) * V
                q = min(pads[k], math.ceil(sobra * 30) / 30); pads[k] = round(pads[k] - q, 4); sobra -= q
                if sobra > 0 and ps[k][1] - ps[k][0] > .2: ps[k][1] = round(ps[k][1] - math.ceil(min(sobra, .02) * 30) / 30, 4)   # como mucho 1 fotograma de cola: la palabra no se toca
            elif sil_min < minimo - .005:
                pads[k] = round(pads[k] + math.ceil((minimo + .01 - sil_min) * V * 30) / 30, 4)
        T += pd / V
    return [tuple(x) for x in ps], pads

def fondo_claro(tmp):
    """¿la franja de arriba (donde van los subtítulos de los virales) es clara, como su pared blanca? Si graba en la calle, no:
    entonces los subtítulos van en blanco con sombra (Abel 14/10/2026)"""
    from PIL import Image
    fs = sorted((tmp / 'frames').glob('*.jpg')); v = []
    for f in fs[::max(1, len(fs) // 12)]:
        im = Image.open(f).convert('L'); w, h = im.size
        v.append(sum(im.crop((int(w * .1), int(h * .12), int(w * .9), int(h * .26))).getdata()) / (w * .8 * h * .14) / 255)
    return bool(v) and sorted(v)[len(v) // 2] > .62


def franja(tmp):
    """TAB: filas (y) donde empieza y acaba la franja de vídeo dentro de la plantilla blanca"""
    from PIL import Image
    im = Image.open(sorted((tmp / 'frames').glob('*.jpg'))[0]).convert('L'); w, h = im.size; px = im.load()
    filas = [y for y in range(h) if sum(px[x, y] for x in range(0, w, 8)) / len(range(0, w, 8)) < 235]
    return [filas[0], filas[-1] + 1] if filas else [557, 1348]


def hacer(cfg, nombre, reel, W, PW, cara, modo):
    ix = indices(W, reel); ps = planos(W, ix)
    usadas = {}
    for k, (ia, ib) in enumerate(ix['tramos']):                       # NINGUNA palabra de la grabación puede sonar dos veces (079-085: un tramo
        for i in range(ia, ib + 1):                                   # duplicado repitió «Y si quieres crear marca personal…» entera)
            if i in usadas: sys.exit(f'TRAMO REPETIDO en {nombre}: «{W[i]["w"]}» ({W[i]["s"]:.2f} s) está en los tramos {usadas[i] + 1} y {k + 1}')
            usadas[i] = k
    # VENTANA de cada frase (Abel 15/10/2026, restos «o no», «tío», «O sea, que unas»): la frase solo puede sonar entre el final de la
    # palabra ANTERIOR de la grabación y el principio de la SIGUIENTE (transcripción por ventanas). Una isla pegada a otra toma ya no entra entera.
    ventanas = []
    for ia, ib in ix['tramos']:
        s0 = W[ia]['s']; pe = W[ia - 1]['e'] if ia > 0 else 0
        lo = min(s0 - .03, max(pe + .01, s0 - .25))
        hi = max(W[ib + 1]['s'] - .02, W[ib]['e'] + .08) if ib + 1 < len(W) else 1e9   # nunca antes del final de la última palabra (un «si» inventado cortaba «marca»)
        if ventanas and ia == ventanas[-1][1] + 1:                    # tramos SEGUIDOS en la grabación = una sola ventana (si no, al recortar el
            pa, pb, plo, phi = ventanas[-1]; ventanas[-1] = (pa, ib, plo, round(hi, 3))   # 1.º se perdía el 2.º: «¿Cuál es tu mensaje diferenciador?», 085)
        else: ventanas.append((ia, ib, round(lo, 3), round(hi, 3)))
    lim = Path(cfg['fuente']).parent / '_fuente_limpia.wav'           # F5: se corta midiendo la voz LIMPIA (casual_prep.py); con el ruido del móvil quedaban pausas de 0,3-0,5 s
    ps = ajustar_finales(str(lim) if reel.get('formato') == 'F5' and lim.exists() else cfg['fuente'], W, ps)   # también en --texto
    pads = rellenos(W, ps)
    PAL = palabras(W, ps, pads); dur = round((sum(b - a for a, b, _ in ps) + sum(pads)) / VELOCIDAD, 3)
    f2, f5 = reel.get('formato') == 'F2', reel.get('formato') == 'F5'
    tab = reel.get('formato') == 'TAB'                              # TAB: plantilla yapping vertical ya grabada con su franja (Abel 15/10/2026)
    f4 = reel.get('formato') in ('F4', 'F5', 'TAB')                         # F2 · imagen abajo / F4 y F5 · él a pantalla completa: sin alternar
    if f5: reel = {**reel, 'titulo_hasta': dur}                       # F5: el título se queda todo el reel
    modos = [[0, 'tablero']] if f2 or f4 else reel.get('modos') or modos_auto(PAL, dur)
    print(f"\n== {nombre}: {dur:.1f} s a {VELOCIDAD}x · {len(ps)} planos · «{frase(reel['titulo'])}»")
    print(' | '.join(' '.join(W[i]['w'] for i in g) for _, _, g in ps))
    if dur < 50: print(f'  AVISO: dura {dur:.1f} s (mínimo 50–55 s)')
    sal = Path(cfg['salida']); tmp = sal / f'_{nombre}'; tmp.mkdir(parents=True, exist_ok=True)
    if modo == 'texto':
        lims = [a for a, _ in modos] + [dur]
        for (a, m), b in zip(modos, lims[1:]):
            print(f"  {m:8s} {a:6.2f}–{b:6.2f}  " + ' '.join(f"{w}@{s:.2f}" for w, s, _ in PAL if a - .05 <= s < b))
        return
    # imagen: "recorte_y" = hasta qué altura (px de la fuente) se puede ver (Abel: «que no se me vean los pantalones del pijama»);
    # "mejorar": limpieza de ruido suave, nitidez y algo de contraste/color. Con recorte se trabaja a resolución completa.
    y1 = reel.get('recorte_y', cfg.get('recorte_y'))
    fw, fh = (1920, int(y1) // 2 * 2) if y1 else (FW, FH)
    vf = (f'crop=1920:{fh}:0:0' if y1 else f'scale={FW}:{FH}')
    if cara[2] > cara[1] and not y1: fw, fh = 720, 1280; vf = 'scale=720:1280'   # fuente VERTICAL: sin esto el F3 la estiraba a 16:9 y deformaba su cara (Abel 14/10/2026)
    if f4:                                                            # F4: vertical 9:16 centrado en su cara (venga en horizontal o en vertical)
        sw, sh = cara[1], cara[2]; h = int(y1 or sh) // 2 * 2; w = min(sw, round(h * 9 / 16 / 2) * 2)
        x0 = int(min(max(cara[0] - w / 2, 0), sw - w)); vf = f'crop={w}:{h}:{x0}:0,scale=1080:1920:flags=lanczos'; fw, fh = 1080, 1920
    if tab: vf = 'scale=1080:1920:flags=lanczos'                     # TAB: la plantilla entera, sin recortar
    vf += ',' + filtro(cfg['fuente'])                                # nitidez + luz compensada, igual en TODOS los reels (Abel 16/10/2026: «tanto si son oscuros o blancos»)
    firma = json.dumps([vf] + [[a, b, p] for (a, b, _), p in zip(ps, pads)] + [reel.get(k) for k in ('fuera', 'cuchillas', 'aire')])   # «fuera»/«cuchillas»/«aire» también rehacen el clip                    # el clip se rehace si cambian los tramos
    cache = tmp / 'onda.json'
    if (tmp / 'clip.mov').exists() and modo != 'todo' and cache.exists() and json.loads(cache.read_text())['firma'] == firma:
        c = json.loads(cache.read_text()); ps, pads = [tuple(x) for x in c['ps']], c['pads']
    else:                                                             # LA ONDA MANDA: los cortes se ajustan sobre la onda de la grabación (igualar)
        lim = Path(cfg['fuente']).parent / '_fuente_limpia.wav'
        ps, pads = igualar(W, ps, str(lim if lim.exists() else cfg['fuente']), cuchillas=reel.get('cuchillas', ()), fuera=reel.get('fuera', ()), respira=reel.get('aire', ()))
        ps, pads = encerrar(ps, pads, ventanas)
        ps, pads = apretar(ps, pads, str(lim if lim.exists() else cfg['fuente']), fuera=reel.get('fuera', ()), W=W)   # ningún silencio > 0,07 s medido COMO LA ONDA (Abel 15/10/2026)
        clip(cfg, ps, pads, tmp, vf, reel.get('fundidos', ()))
        for _ in range(4):                                            # LA ONDA MANDA: se mide el reel montado y se corrige cada unión que pase de 0,10 s
            ps2, pads2 = afinar_con_onda(ps, pads, tmp / 'voz.wav')
            if (ps2, pads2) == (ps, pads): break
            ps, pads = ps2, pads2; clip(cfg, ps, pads, tmp, vf, reel.get('fundidos', ()))
        if reel.get('limpiar_voz', f5) and not lim.exists(): limpiar_voz(tmp, reel.get('limpiar_fuerza', 40))   # F5 sin voz limpia previa
        cache.write_text(json.dumps({'firma': firma, 'ps': ps, 'pads': pads}))
        (tmp / 'planos.json').write_text(json.dumps([vf] + [[a, b, p] for (a, b, _), p in zip(ps, pads)]))   # para verificar_audio
        (tmp / 'velocidad.txt').write_text(str(VELOCIDAD))
    PAL = corrige_texto(oidas(tmp, palabras(W, ps, pads)), reel.get('corrige', [])); dur = round((sum(b - a for a, b, _ in ps) + sum(pads)) / VELOCIDAD, 3)
    T0, k0 = 0.0, 0                                                    # la 1.ª palabra de cada trozo empieza justo donde empieza el trozo en el reel
    for (a_, b_, g_), pd_ in zip(ps, pads):                           # (tras un corte Whisper la oía 0,2-0,3 s tarde: «Porque», «Cuando», 082)
        if g_ and k0 < len(PAL) and PAL[k0][1] > T0 + .08: PAL[k0][1] = round(T0 + .03, 3)
        k0 += len(g_); T0 += (b_ - a_ + pd_) / VELOCIDAD
    if f5: reel = {**reel, 'titulo_hasta': dur}
    modos = [[0, 'tablero']] if f2 or f4 else reel.get('modos') or modos_auto(PAL, dur)
    if modo == 'voz':                                                 # LA ONDA MANDA (Abel 14/10/2026): se mira la pista de la voz cortada ANTES del render
        import onda; onda.revisar(tmp / 'voz.wav'); return
    colores = colores_texto(tmp, reel.get('titulo_hasta', 6)) if f4 else {}
    acento = CENTROS.get(reel.get('acento', 'corona'), reel.get('acento', '#7A3FC4'))
    cx = 540 if f4 else cara[0] * fw / cara[1]
    cortes, T, z, nc = [], 0.0, 1.08, 0                                      # F4: acercamiento alterno 1,00/1,08 en cada salto de contenido
    for k, ((t0, t1, g), pd) in enumerate(zip(ps, pads)):
        if k == 0 or g[0] != ps[k - 1][2][-1] + 1 or T / VELOCIDAD - cortes[-1][0] >= 3:   # salto de contenido, o corte de silencio tras ≥ 3 s
            nc += 1
            if k == 0 or not f5 or nc % 2 == 1:                       # F5: zoom solo en uno de cada dos cortes (Abel 10/10: frase a frase hay muchos cortes)
                z = 1.0 if z != 1.0 else 1.08; cortes.append([round(T / VELOCIDAD, 3), z, 0])
        for i, j in zip(g, g[1:]):                                    # plano largo: acercamiento suave en una micropausa cada ~4,5 s
            tj = (T + W[j]['s'] - t0) / VELOCIDAD
            if W[j]['s'] - W[i]['e'] > .12 and tj - cortes[-1][0] >= 4.5 and (T + t1 - t0) / VELOCIDAD - tj > 1.5:
                z = 1.0 if z != 1.0 else 1.06; cortes.append([round(tj - .1, 3), z, 1])
        T += t1 - t0 + pd
    banda = franja(tmp) if tab else [0, 1920]
    fy = reel.get('cara', [200, 870])[1] - banda[0] if tab else 0
    if tab: cx = reel.get('cara', [200, 870])[0]
    (tmp / 'datos.js').write_text(
        f"const BANDA = {json.dumps(banda)}, FY = {fy}, ES_LISTA = {json.dumps(bool(reel.get('lista')))};\n"
        f"const PAL = {json.dumps(PAL, ensure_ascii=False)};\nconst MODOS = {json.dumps(modos)};\nconst TITULO = {json.dumps(titulo2(reel['titulo']), ensure_ascii=False)};\n"
        f"const ACENTO = '{acento}', FW = {fw}, FH = {fh}, FX = {cx:.1f}, DUR = {dur};\nconst VIRAL = {json.dumps(cfg.get('estilo') == 'viral')}, FONDO_CLARO = {json.dumps(fondo_claro(tmp))}, COLORES = {json.dumps(colores)}, CORTES = {json.dumps(cortes)}, TITULO_HASTA = {reel.get('titulo_hasta', 6)}, APARTADOS = {json.dumps(reel.get('apartados', []), ensure_ascii=False)};\n", encoding='utf-8')
    shutil.copy(TAB / ('motor_tab.html' if tab else 'motor_f5.html' if f5 else 'motor_f4.html' if f4 else 'motor_f2.html' if f2 else 'motor.html'), tmp / 'motor.html'); shutil.copy(TAB / 'Montserrat-Variable.ttf', tmp)
    if reel.get('imagenes'):                                          # F2: las fotos (rutas relativas al reels.json)
        shutil.copytree(Path(cfg['_base']) / reel['imagenes'], tmp / 'img', dirs_exist_ok=True, ignore=shutil.ignore_patterns('*.mp4', '*.mov', '*.MOV'))
    for nom, (src, a, b) in reel.get('clips', {}).items():           # F3: vídeos de su vida -> clips/<nom>/ (JPG a 30 fps, sin sonido)
        d = tmp / 'clips' / nom
        if not d.exists():
            d.mkdir(parents=True)
            subprocess.run(['ffmpeg', '-v', 'error', '-ss', str(a), '-to', str(b), '-i', str(Path(cfg['_base']) / src), '-an', '-vf', 'fps=30,scale=720:-2',
                            '-q:v', '3', str(d / '%05d.jpg')], check=True)
        print(f'  clip {nom}: {len(list(d.glob("*.jpg")))} fotogramas')
    if reel.get('escenas', 'auto' if reel.get('formato', 'F3') == 'F3' else None) == 'auto':   # F3 = F3 LIGERO por defecto (Abel 13/10/2026); un cNN.js = F3 completo                                 # F3 LIGERO: los gráficos salen solos de lo que dice (tablero/escenas_auto.js)
        (tmp / 'escenas.js').write_text(f"const LIGERO = true, CLAVES = {json.dumps(reel.get('claves', []), ensure_ascii=False)};" + '\n'
                                        + (TAB / 'escenas_auto.js').read_text(encoding='utf-8'), encoding='utf-8')
    else:
        esc = Path(cfg['_base']) / reel['escenas'] if reel.get('escenas') else None
        (tmp / 'escenas.js').write_text(esc.read_text(encoding='utf-8') if esc and esc.exists() else 'ESC = () => {};', encoding='utf-8')
    node = ['node', str(TAB / 'grabar.mjs'), str(tmp)]
    if modo.startswith('fotos:'):
        subprocess.run(node + ['0', str(tmp), '--fotos', modo[6:]], check=True); print('  fotos ->', tmp); return
    subprocess.run(node + [str(dur), str(tmp / 'video.mp4'), '--sfx', str(tmp / 'sfx.json')], check=True)
    l_voz = voz_lufs(str(tmp / 'voz.wav'))
    efectos(json.load(open(tmp / 'sfx.json')), dur, l_voz, tmp / 'efectos.wav')
    ent = ['-i', str(tmp / 'video.mp4'), '-i', str(tmp / 'voz.wav'), '-i', str(tmp / 'efectos.wav')]
    g_voz = VOZ_LUFS - l_voz; l_voz = VOZ_LUFS                      # su voz siempre a −14 LUFS (estaba a −16: «que se escuche bien»)
    sc = False                                                      # la música NO se toca (Abel 14/10/2026: con sidechain «ni se oye»); se trabaja la voz
    fil = f'[1:a]volume={g_voz:.2f}dB' + ('[vz0];[vz0]asplit=2[vz][vsc];' if sc else '[vz];') + '[vz][2:a]amix=inputs=2:duration=first:normalize=0[vf];'
    if reel.get('musica'):
        mus = MUSICA / reel['musica']; catm = json.load(open(MUSICA / 'catalogo.json', encoding='utf-8'))
        extra_voz = -6 if catm.get(reel['musica'], {}).get('voz') else 0   # canción CANTADA: 6 dB más baja para que no distraiga (Abel 15/10/2026)
        desde = reel.get('desde')
        if desde is None: desde = catm.get(reel['musica'], {}).get('estribillo') or estribillo(str(mus), dur)
        print(f"  música: {reel['musica']} desde {desde} s")
        ent += ['-ss', str(desde), '-i', str(mus)]
        fil += (f"[3:a]atrim=0:{dur:.3f},volume={ganancia_musica(mus, desde, dur, l_voz) + extra_voz:.2f}dB,aresample={SR},"
                f"afade=t=in:d={MUSICA_IN},afade=t=out:st={dur - MUSICA_OUT:.3f}:d={MUSICA_OUT}[mu0];"
                f"[mu0]anull[mu];[vf][mu]amix=inputs=2:duration=first:normalize=0[mx];")   # («publicas» se oía «public»)
    else:
        fil += '[vf]anull[mx];'
    for j, (destino, o0, d) in enumerate(reel.get('eses', [])):   # «eses» (reels.json): una «s» que en la grabación casi no suena («Solo» → «olo»)
        T, tr = 0.0, None                                      # se presta de otra palabra suya y se pone justo antes: [seg. fuente donde
        for (a, b, _), pdd in zip(ps, pads):                   # arranca la palabra, seg. fuente de la «s» prestada, duración]
            if a - .2 <= destino <= b: tr = (T + destino - a) / VELOCIDAD; break
            T += b - a + pdd
        if tr is None: continue
        n = len([x for x in ent if x == '-i']); ms = max(0, int((tr - d / VELOCIDAD) * 1000))
        ent += ['-ss', str(o0), '-t', str(d), '-i', str(voz_suave(cfg['fuente']))]
        fil = fil.replace('[mx]', f'[mx0]', 1) if j == 0 and '[mx]' in fil else fil
        fil += (f"[{n}:a]atempo={VELOCIDAD},{PRESENCIA}volume={g_voz:.2f}dB,afade=t=in:d=0.015,afade=t=out:st={max(0, d / VELOCIDAD - .02):.3f}:d=0.02,"
                f"aresample={SR},adelay={ms}|{ms}[e{j}];[{'mx0' if j == 0 else f'mx{j}'}][e{j}]amix=inputs=2:duration=first:normalize=0[mx{j + 1 if j + 1 < len(reel['eses']) else ''}];")
    fil += '[mx]alimiter=limit=0.891:level=0[a]'
    final = sal / f'{nombre}.mp4'
    subprocess.run(['ffmpeg', '-v', 'error', '-y', *ent, '-filter_complex', fil, '-map', '0:v', '-map', '[a]', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', '-ar', str(SR), '-movflags', '+faststart', '-t', str(dur), str(final)], check=True)
    print('  ->', final)


if __name__ == '__main__':
    ruta = Path(sys.argv[1]).resolve(); cfg = json.load(open(ruta, encoding='utf-8')); cfg['_base'] = str(ruta.parent)
    import reel_yapping; VELOCIDAD = reel_yapping.VELOCIDAD = cfg.get('velocidad', VELOCIDAD)   # reels virales: 1,10x (Abel 14/10/2026)
    for k in ('fuente', 'tiempos', 'salida'): cfg[k] = str((ruta.parent / cfg[k]).resolve())
    W = json.load(open(cfg['tiempos'], encoding='utf-8')); W = W['palabras'] if isinstance(W, dict) else W
    a = sys.argv[2:]
    modo = 'texto' if '--texto' in a else 'voz' if '--voz' in a else ('fotos:' + a[a.index('--fotos') + 1]) if '--fotos' in a else 'todo' if '--rehacer' in a else 'render'
    solo = a[a.index('--solo') + 1:] if '--solo' in a else None
    cara = None if modo == 'texto' else centro_cara(cfg['fuente'])
    from concurrent.futures import ThreadPoolExecutor                # los formatos de un vídeo se hacen a la vez (Abel 14/10/2026)
    with ThreadPoolExecutor(1 if modo == 'texto' else 3) as ex:
        for f in [ex.submit(hacer, cfg, n, r, W, None, cara, modo) for n, r in cfg['reels'].items() if not solo or n in solo]: f.result()
