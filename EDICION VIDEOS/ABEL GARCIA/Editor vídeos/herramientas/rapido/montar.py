"""PASO 2 del proceso rápido: monta SOLO EL AUDIO de cada reel con las islas elegidas y lo VERIFICA en una sola pasada
(el reconocedor se carga una vez). Nada de vídeo aquí: tarda segundos, se repite las veces que haga falta.

    python herramientas/rapido/montar.py <carpeta> [reel ...]

<carpeta>/plan.json:
{
  "velocidad": 1.0,
  "guion": "texto del guion del Drive (para comparar)",
  "cuerpo": [12, 16, [21, null, "seguir"], 26, ...],     # id de isla, o [id, desde_palabra|null, hasta_palabra|null] para quedarse con parte
  "reels": {"r1": {"gancho": [2], "titulo": "...", "musica": "ÉPICA/...mp3"}, ...},
  "corrige": [["oído", "dicho"], ...],                   # errores del reconocedor en los subtítulos
  "fotos": [["img/x.jpg", "frase donde entra", "frase donde sale", {"w": 330}], ...]
}
Escribe <carpeta>/out_rapido/<reel>/voz.wav (ya a la velocidad del reel), edl.json (trozos de la grabación y su sitio en el reel,
palabras con sus tiempos exactos para los subtítulos) e INFORME.txt con todo lo que hay que mirar. Código 1 si algo falla.
"""
import difflib, json, math, re, subprocess, sys
from pathlib import Path
import numpy as np
AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parent))
import onda

SR = 48000
FADE = .008                        # fundido de cada trozo: los cortes caen en silencio, solo evita el «clic»
COLA = .25                         # el reel ACABA cuando Abel deja de hablar (16/10: «lo que marca el final es que yo dejé de hablar»); la música se funde por debajo de la última frase
UNION_MAX, UNION_MIN = .09, .02    # silencio permitido en cada unión del reel (s): ninguna más larga que la pausa gancho→cuerpo
nz = lambda w: re.sub(r'[^a-z0-9ñ]', '', str(w).lower().translate(str.maketrans('áéíóúü', 'aeiouu')))


def fin_isla(islas, i):
    """dónde acaba DE VERDAD la isla i: si justo detrás (< 0,15 s) va una isla muy corta (< 0,35 s), es el FINAL de su última palabra,
    que una consonante muda («t», «p», «j») separó: «perfec-t…o» (la «o» suelta se transcribía «Toc, toc, toc» y se tiraba; tablet10)"""
    b = islas[i]['b']
    if i + 1 < len(islas) and islas[i + 1]['a'] - b < .15 and islas[i + 1]['b'] - islas[i + 1]['a'] < .35: b = islas[i + 1]['b']
    return b


def pieza(islas, spec):
    """isla entera o parte de ella: [id, desde, hasta] → (a, b, palabras). El corte va a mitad del hueco entre dos palabras."""
    if isinstance(spec, dict):                                               # corte A MANO por segundos (19/10/2026): {"isla": 46, "a": 202.33, "b": 204.8}
        i = spec['isla']; isla = islas[i]; a, b = spec.get('a', isla['a']), spec.get('b', fin_isla(islas, i))   # (respiración dentro de una frase,
        M = mms(i); P = isla['pal']                                          #  cola floja que la onda ve como hueco); las palabras se reparten con la
        if len(M) == len(P): return round(a, 3), round(b, 3), [list(w) for w, m in zip(P, M) if a <= (m[1] + m[2]) / 2 < b], i   # alineación LETRA A LETRA
        return round(a, 3), round(b, 3), [list(w) for w in P if w[2] > a and w[1] < b - .05], i              # (el reconocedor se desvía hasta 0,5 s)
    if isinstance(spec, int): i, desde, hasta = spec, None, None
    else: i, desde, hasta = (list(spec) + [None, None])[:3]
    isla = islas[i]; P = isla['pal']; a, b = isla['a'], fin_isla(islas, i); k0, k1 = 0, len(P) - 1
    if desde:
        f = desde.split(); k0 = next(k for k in range(len(P) - 1, -1, -1) if [nz(x[0]) for x in P[k:k + len(f)]] == [nz(x) for x in f])   # la ÚLTIMA vez: el arranque bueno va tras el tropiezo
        a = max(a, (P[k0 - 1][2] + P[k0][1]) / 2 if k0 else a)
    if hasta:
        f = hasta.split(); k1 = next(k + len(f) - 1 for k in range(len(P) - 1, -1, -1) if [nz(x[0]) for x in P[k:k + len(f)]] == [nz(x) for x in f])
        b = min(b, (P[k1][2] + P[k1 + 1][1]) / 2 if k1 + 1 < len(P) else b)
    if (desde and k0) or (hasta and k1 + 1 < len(P)):                        # corte A MITAD de toma: se decide con la alineación LETRA A LETRA
        from alinear_mms import palabras                                     # (el reconocedor se equivoca hasta 0,2 s: «trabaj», «tiemp», la «y» de
        M = mms(i)                                                           # «y con todo eso» perdida; tablet09-11)
        if len(M) == len(P):
            if desde and k0: a = max(isla['a'], M[k0 - 1][2] + .01, min((M[k0 - 1][2] + M[k0][1]) / 2, M[k0][1] - .03))
            if hasta and k1 + 1 < len(P): b = min(fin_isla(islas, i), M[k1 + 1][1] - .01, max((M[k1][2] + M[k1 + 1][1]) / 2, M[k1][2] + .03))
    if desde and k0: _CORTE[(i, 'a')] = a                                    # cortes A MITAD DE TOMA: los únicos que se revisan letra a letra
    if hasta and k1 + 1 < len(P): _CORTE[(i, 'b')] = b
    return round(a, 3), round(b, 3), [list(p) for p in P[k0:k1 + 1]], i


def leer(f, a=None, b=None, sr=16000):
    cmd = ['ffmpeg', '-v', 'error'] + (['-ss', f'{a:.3f}', '-to', f'{b:.3f}'] if a is not None else []) + ['-i', str(f), '-ac', '1', '-ar', str(sr), '-f', 's16le', '-']
    return np.frombuffer(subprocess.run(cmd, capture_output=True).stdout, np.int16).astype(np.float32) / 32768


LEAD, TAIL, LAX = .015, .03, 30     # aire delante/detrás de la voz real; voz = pico − 33 dB (con agudos): la vocal floja y la «s» final son palabra
_E = {}


def ajustar(pz):
    """recorta el trozo a donde EMPIEZA y ACABA la voz de verdad (pico − 30 dB, con agudos): fuera la respiración, el aire de
    margen y los CHASQUIDOS sueltos (tramos de < 60 ms separados por silencio: tras «publicas» alargaban la unión a 0,2 s)"""
    a, b, P, i = pz; E, pico = _E['E'], _E['pico']; T = .01
    fr = range(int(a / T), min(len(E), int(b / T) + 1)); runs = []
    for k in fr:
        if E[k] > pico - LAX:
            if runs and k - runs[-1][1] <= 4: runs[-1][1] = k          # huecos < 40 ms dentro de la voz: misma racha
            else: runs.append([k, k])
    runs = [r_ for r_ in runs if (r_[1] - r_[0] + 1) * T >= .06]
    if not runs: return a, b, P, i
    na, nb = max(a, runs[0][0] * T - LEAD), min(b, (runs[-1][1] + 1) * T + TAIL)
    la, lb = bordes(P, i)
    if la is not None: na, nb = max(a, min(na, la)), min(b, max(nb, lb))     # nunca por dentro de la 1.ª/última palabra
    return round(na, 3), round(nb, 3), P, i


_MMS = {}
_CORTE = {}


def mms(i):
    """palabras de la isla i con la alineación LETRA A LETRA (en caché; ~0,2 s por isla)"""
    if i not in _MMS:
        from alinear_mms import palabras
        isla = _E['islas'][i]; M = palabras(_E['suave'], isla['a'], fin_isla(_E['islas'], i), isla['texto'])
        E, pico = _E['E'], _E['pico']; voz = lambda k: E[min(len(E) - 1, k)] > pico - 45
        out = []                                                             # el alineador «estira» una palabra sobre la pausa que la sigue
        for w, a, b in M:                                                    # («es | tu»): cada palabra, ceñida a donde su voz SE OYE (> pico − 45 dB)
            k0, k1 = round(a / .01), round(b / .01)
            while k0 < k1 and not voz(k0): k0 += 1
            while k1 > k0 and not voz(k1): k1 -= 1
            out.append((w, a, b) if k1 <= k0 else (w, max(a, k0 * .01 - .01), min(b, (k1 + 1) * .01)))
        _MMS[i] = out
    return _MMS[i]


def bordes(P, i):
    """(inicio de la 1.ª letra, final de la última letra) de las palabras P de la isla i. NINGÚN recorte (cola, arranque, pausa)
    puede pasar de ahí: el reconocedor se equivoca hasta 0,2 s y los finales flojos («-da» de «reflejada», «-o» de «perfecto»)
    parecían silencio (Abel 16/10/2026: «trabajo», «tiempo», «perfecto», «y», «reflejada»)."""
    if not P or 'islas' not in _E: return None, None
    IP = _E['islas'][i]['pal']; M = mms(i)
    if len(M) != len(IP): return None, None
    k0 = next((k for k, w in enumerate(IP) if abs(w[1] - P[0][1]) < 1e-3), None); k1 = next((k for k, w in enumerate(IP) if abs(w[1] - P[-1][1]) < 1e-3), None)
    if k0 is None or k1 is None or M[k1][2] - M[k0][1] <= 0: return None, None
    ini, fin = M[k0][1], M[k1][2]
    return ini - .015, fin + .025


def enteras(piezas, islas, suave):
    """PALABRAS ENTERAS (Abel 16/10/2026: «se come la última letra de trabajo… debe haber alguna forma de verificar»): el reconocedor
    RELLENA palabras cortadas, así que cada trozo se comprueba con la alineación FINA (MMS, letra a letra): el trozo tiene que empezar
    antes de la 1.ª letra de su 1.ª palabra y acabar después de la última letra de su última palabra. Si no, se amplía (sin pisar la
    palabra de al lado) y se avisa."""
    from alinear_mms import palabras
    out, avisos = [], []
    E, pico = _E['E'], _E['pico']; voz = lambda t: E[min(len(E) - 1, max(0, round(t / .01)))] > pico - 27
    for a, b, P, i in piezas:
        isla = islas[i]
        va = (i, 'a') in _CORTE and abs(a - _CORTE[(i, 'a')]) < .3           # SOLO los cortes A MITAD DE TOMA («hasta»/«desde») pueden comerse una letra:
        vb = (i, 'b') in _CORTE and abs(b - _CORTE[(i, 'b')]) < .3           # los demás caen en una pausa real (≥ 0,07 s) y la palabra ya había acabado
        if not (va or vb): out.append((a, b, P, i)); continue               # (Abel 16/10: «solo cuando haga falta, si no volvemos a tardar»)
        M = mms(i); IP = isla['pal']
        if not P or len(M) != len(IP): out.append((a, b, P, i)); continue
        k0 = next((k for k, w in enumerate(IP) if abs(w[1] - P[0][1]) < 1e-3), None); k1 = next((k for k, w in enumerate(IP) if abs(w[1] - P[-1][1]) < 1e-3), None)
        if k0 is None or k1 is None: out.append((a, b, P, i)); continue
        ini, fin = M[k0][1] - .015, M[k1][2] + .025
        tope_a = M[k0 - 1][2] + .01 if k0 else isla['a']; tope_b = M[k1 + 1][1] - .01 if k1 + 1 < len(M) else fin_isla(islas, i)
        na, nb = (max(min(a, ini), tope_a) if va and a > ini else a), (min(max(b, fin), tope_b) if vb and b < fin else b)
        if nb > b + .03: avisos.append(f'  palabra entera: «{M[k1][0]}» acababa {fin - b:.2f} s después del corte → ampliado')
        if na < a - .03: avisos.append(f'  palabra entera: «{M[k0][0]}» empezaba {a - ini:.2f} s antes del corte → ampliado')
        out.append((round(na, 3), round(nb, 3), P, i))
    return out, avisos


def topar(piezas, V, maxu=.065):
    """cada UNIÓN, medida como la onda (pico − 27 dB): si la cola de silencio de un trozo + el arranque del siguiente pasan de
    `maxu` (s del reel), se recorta primero la cola y luego el arranque; nunca por dentro de la voz (≥ 20 ms de cola, 10 ms de arranque)"""
    E, pico = _E['E'], _E['pico']; T = .01; thr = pico - 27
    voz = lambda t: E[min(len(E) - 1, max(0, int(t / T)))] > thr
    out = [list(x) for x in piezas]
    for k in range(len(out) - 1):
        a0, b0 = out[k][0], out[k][1]; a1, b1 = out[k + 1][0], out[k + 1][1]
        fin = b0
        while fin > a0 + .05 and not voz(fin - T): fin -= T
        ini = a1
        while ini < b1 - .05 and not voz(ini): ini += T
        cola, arr = b0 - fin, ini - a1; sobra = cola + arr + 1 / 60 - maxu * V
        if sobra > 0:
            lb = bordes(out[k][2], out[k][3])[1]; la = bordes(out[k + 1][2], out[k + 1][3])[0]
            q = min(sobra, max(0, cola - .02)); out[k][1] = round(max(b0 - q, lb if lb is not None else -1), 3); sobra -= b0 - out[k][1]
            if sobra > 0: out[k + 1][0] = round(min(a1 + min(sobra, max(0, arr - .01)), la if la is not None else 1e9), 3)
    return [tuple(x) for x in out]


PAUSA = .07                         # toda pausa DENTRO de un trozo (voz < pico − 27 dB) más larga que esto se parte y se deja en ~0,06 s


def partir(pz):
    """pausas dentro de una isla («personal, | cuál es», «diferenciador, | cuál ha sido»): se parten en dos trozos"""
    a, b, P, i = pz; E, pico = _E['E'], _E['pico']; T = .01; thr = pico - 27; out = []; t = a + .05; ini = a
    IP = _E['islas'][i]['pal'] if 'islas' in _E else []
    real = {round(w[1], 3): m[1] for w, m in zip(IP, mms(i))} if IP and len(mms(i)) == len(IP) else {}
    while t < b - .05:
        if E[int(t / T)] < thr:
            u = t
            while u < b and E[int(u / T)] < thr: u += T
            c0, c1 = t + .03, u - .015                                       # 30 ms de cola, 15 ms de arranque
            if 'islas' in _E and len(mms(i)) == len(_E['islas'][i]['pal']):  # la pausa no puede caer DENTRO de una palabra («reflej|ada»)
                for w in mms(i):
                    if w[1] < c0 < w[2]: c0 = w[2] + .02
                    if w[1] < c1 < w[2]: c1 = w[1] - .015
            hondo_ = min(E[int(t / T):max(int(t / T) + 1, int(u / T))])
            if u - t > PAUSA and (hondo_ < pico - 40 or u - t > .15) and c1 - c0 > .03 and u < b - .05 and t - ini > .08:   # solo pausas DE VERDAD: una bajada de voz entre
                                                                             # palabras dichas seguidas («de verdad · sin actuar») no se parte: al partirla se fabricaba un hueco   # nunca un trozo de < 0,08 s (la «y» se quedaba en uno de 0,017 s)
                ini_w = (lambda w: real.get(round(w[1], 3), w[1]))                  # cada palabra al lado que le toca según la alineación fina
                izq = [w for w in P if ini_w(w) < c0]; P = [w for w in P if ini_w(w) >= c0]
                out.append((round(ini, 3), round(c0, 3), izq, i)); ini = c1
            t = u
        else: t += T
    out.append((round(ini, 3), round(b, 3), P, i))
    k = 1
    while k < len(out):                                                      # trozo SIN palabras que cae dentro de la última palabra del anterior
        if not out[k][2] and out[k - 1][2] and out[k][0] <= out[k - 1][2][-1][2] + .12:   # = su final («hablamo|s», 095): se pega a ella
            out[k - 1] = (out[k - 1][0], out[k][1], out[k - 1][2], i); out.pop(k)
        else: k += 1
    con = [x for x in out if x[2]] or out                                    # un trozo sin ninguna palabra es ruido (chasquido, respiración)
    if len(con) < len(out): con[-1] = (con[-1][0], con[-1][1], con[-1][2], i)
    return [ajustar(x) for x in con]


if __name__ == '__main__':
    import torch  # noqa: F401
    from faster_whisper import WhisperModel
    from casual_prep import LITERAL
    from reel_tablero import voz_suave, PRESENCIA
    d = Path(sys.argv[1])
    r_ = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v', '-show_entries', 'stream=r_frame_rate', '-of', 'csv=p=0', str(d / 'fuente.mp4')], capture_output=True, text=True).stdout.strip()
    FPS = eval(r_.split()[0]) if r_ else 30.0
    plan = json.loads((d / 'plan.json').read_text(encoding='utf-8')); V = plan.get('velocidad', 1.0)   # Abel 19/10/2026: velocidad NORMAL; el ritmo lo dan los silencios recortados
    islas = json.loads((d / 'islas.json').read_text(encoding='utf-8'))
    suave = voz_suave(str(d / 'fuente.mp4'))
    _E['suave'] = suave; _E['islas'] = islas; _E['E'] = onda.envolvente(str(suave))[1]; _E['pico'] = np.percentile(_E['E'], 95)   # se decide sobre la voz que SE OYE (la suave), como la mide la onda del reel
    m = WhisperModel('large-v3', device='cuda', compute_type='int8_float16')   # int8: la mitad de memoria (con la GPU llena, float16 iba a trompicones: 6-13 min por reel, Abel 19/10/2026)
    oir = lambda x: ' '.join(w.word.strip() for s in m.transcribe(np.concatenate([np.zeros(4000, np.float32), x, np.zeros(4000, np.float32)]),
                             language='es', word_timestamps=True, initial_prompt=LITERAL, condition_on_previous_text=False)[0] for w in s.words)
    def oir_cerca(x, centro, ancho=.9):                                    # solo lo que suena cerca de la unión (en los bordes el reconocedor se inventa «Gracias por ver el vídeo»)
        ws = [(w.word.strip(), w.start - .25) for s in m.transcribe(np.concatenate([np.zeros(4000, np.float32), x, np.zeros(4000, np.float32)]),
              language='es', word_timestamps=True, initial_prompt=LITERAL, condition_on_previous_text=False)[0] for w in s.words]
        return ' '.join(w for w, t in ws if abs(t - centro) < ancho)
    malos = 0
    for nombre in (sys.argv[2:] or plan['reels']):
        r = plan['reels'][nombre]; out = d / 'out_rapido' / nombre; out.mkdir(parents=True, exist_ok=True)
        piezas = [q for s in r['gancho'] + r.get('cuerpo', plan['cuerpo']) for q in partir(ajustar(pieza(islas, s)))]
        piezas, avisos_mms = enteras(piezas, islas, suave)
        a_, b_, P_, i_ = piezas[-1]                                          # ÚLTIMO trozo del reel: detrás no hay unión, solo el final del vídeo →
        if P_ and islas[i_]['pal'] and abs(P_[-1][1] - islas[i_]['pal'][-1][1]) < 1e-3:   # hasta el borde de su isla, que la última vocal se apague
            fin_ = max(b_, fin_isla(islas, i_)); E_, k_ = _E['E'], round(fin_ / .01)   # entera («perfect-o» cortado, tablet10)
            while k_ + 1 < len(E_) and E_[k_ + 1] > _E['pico'] - 48 and E_[k_ + 1] <= E_[k_] + 3 and k_ * .01 < fin_ + .15: k_ += 1   # y su cola suave, sin el golpe de parar la grabación
            piezas[-1] = (a_, max(fin_, k_ * .01), P_, i_)
        ids = [s if isinstance(s, int) else s['isla'] if isinstance(s, dict) else s[0] for s in r['gancho'] + r.get('cuerpo', plan['cuerpo'])]
        rep = [i for i in set(ids) if ids.count(i) > 1]                          # la misma isla elegida dos veces = frase repetida
        # 1) AUDIO: cada trozo de la voz suave, con su fundido, uno detrás de otro (las islas ya traen su aire: la unión es silencio de verdad)
        piezas = topar(piezas, V)                                              # ninguna unión > 0,07 s medida como la onda
        for vuelta in range(6):                                                # se MIDE el audio final y se recorta lo que sobre (solo audio: segundos)
            trozos, edl, T, pal = [], [], 0.0, []
            piezas = [(round(a * FPS) / FPS, math.floor(b * FPS + 1e-6) / FPS, P, i) for a, b, P, i in piezas]   # cortes en FOTOGRAMAS exactos del vídeo
            for a, b, P, i in piezas:
                x = leer(suave, a, b, SR); x = np.pad(x, (0, max(0, int(round((b - a) * SR)) - len(x))))[:int(round((b - a) * SR))]; n = int(FADE * SR)
                if len(x) > 2 * n: x[:n] *= np.linspace(0, 1, n); x[-n:] *= np.linspace(1, 0, n)
                if (a, b) == piezas[-1][:2] and len(x) > int(.3 * SR): f_ = int(.06 * SR); x[-f_:] *= np.linspace(1, 0, f_) ** 2   # final del reel: se apaga, no se corta
                nf = 3 if _E['E'][min(len(_E['E']) - 1, round(b / .01) - 2)] > _E['pico'] - 27 else 1   # acaba EN VOZ (corte a mitad de toma): pausa de coma (~0,05 s)
                edl.append({'isla': i, 'a': round(a, 5), 'b': round(b, 5), 'pad': round(nf / FPS, 5), 't': round(T / V, 4)})
                fino = {}                                                      # SUBTÍTULOS con los tiempos del alineador letra a letra (ya calculado
                IP_ = islas[i]['pal']; M_ = _MMS.get(i)                        # para proteger las palabras: no cuesta nada más; Abel 17/10)
                if M_ and len(M_) == len(IP_): fino = {round(w_[1], 3): (m_[1], m_[2]) for w_, m_ in zip(IP_, M_)}
                for w, s0, s1 in P:
                    f0, f1 = fino.get(round(s0, 3), (s0, s1))
                    if not (a - .05 <= f0 < b and f1 > f0): f0, f1 = s0, s1        # por si el alineador se va de la ventana del trozo
                    pal.append([w, round((T + max(f0, a) - a) / V, 3), round((T + min(f1, b) - a) / V, 3)])
                trozos.append(x); T += len(x) / SR
                pad = np.zeros(int(round(nf * SR / FPS)), np.float32); trozos.append(pad); T += len(pad) / SR   # 1 fotograma de silencio entre trozos: nunca pegado
            crudo = out / '_crudo.wav'
            trozos.append(np.zeros(int(COLA * V * SR), np.float32)); T += COLA * V      # COLA final: la música se apaga después de la última palabra (Abel: «se corta la música»)
            np.concatenate(trozos).astype('<f4').tofile(out / '_crudo.f32')
            subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'f32le', '-ar', str(SR), '-ac', '1', '-i', str(out / '_crudo.f32'),
                            '-af', f'atempo={V},{PRESENCIA}aresample={SR}', str(out / 'voz.wav')], check=True)
            (out / '_crudo.f32').unlink()
            _, E2 = onda.envolvente(str(out / 'voz.wav')); th2 = np.percentile(E2, 95) - 27; cambio = False
            for k, p_ in enumerate(edl[1:], 1):
                t = p_['t']; sil = 0
                for q in range(max(0, int((t - .04) / .01)), min(len(E2), int((t + .04) / .01) + 1)):
                    if E2[q] >= th2: continue
                    l = r2 = q
                    while l > 0 and E2[l - 1] < th2: l -= 1
                    while r2 < len(E2) and E2[r2] < th2: r2 += 1
                    sil = max(sil, (r2 - l) * .01)
                if sil > UNION_MAX - .005:
                    a0, b0, P0, i0_ = piezas[k - 1]; a1, b1, P1, i1_ = piezas[k]; sobra = (sil - (UNION_MAX - .02)) * V
                    q0 = min(sobra * .6, max(0, (b0 - a0) - .2), .06); q1 = min(sobra - q0, .03)
                    lb = bordes(P0, i0_)[1]; la = bordes(P1, i1_)[0]
                    nb0 = max(b0 - q0, lb if lb is not None else -1); na1 = min(a1 + max(0, q1), la if la is not None else 1e9)
                    if nb0 < b0 - .004 or na1 > a1 + .004: piezas[k - 1] = (a0, nb0, P0, i0_); piezas[k] = (na1, b1, P1, i1_); cambio = True
            juntas_ = [p_['t'] for p_ in edl[1:]]                               # hueco > 0,10 s DENTRO de un trozo («y es… perfecto», tablet10):
            for h0, h1 in onda.huecos(E2)[0]:                                   # se parte el trozo ahí y la vuelta siguiente lo deja como una unión
                if h1 >= T / V - COLA - .05 or any(abs((h0 + h1) / 2 - t) < .1 for t in juntas_): continue
                k = max((n_ for n_, p_ in enumerate(edl) if p_['t'] <= h0), default=None)
                if k is None: continue
                a0, b0, P0, i0_ = piezas[k]; s0 = a0 + (h0 - edl[k]['t']) * V; s1 = a0 + (h1 - edl[k]['t']) * V
                if s0 - a0 < .1 or b0 - s1 < .1: continue
                tramo_ = _E['E'][round(s0 / .01):max(round(s0 / .01) + 1, round(s1 / .01))]
                if min(tramo_) > _E['pico'] - 40 and s1 - s0 < .15: continue    # en la grabación NO hay silencio de verdad ahí (bajada de voz entre palabras seguidas)
                lb_ = bordes([w for w in P0 if w[2] <= s1 + .05], i0_)[1]
                if lb_ is not None and lb_ > s0 + .06: continue                 # el hueco cae dentro de una palabra
                der = [w for w in P0 if w[2] > s1 + .05]; izq = [w for w in P0 if w not in der]   # (los tiempos del reconocedor bailan: cuenta dónde ACABA cada palabra)
                if not izq or not der: continue
                piezas[k:k + 1] = [(a0, s0 + .03, izq, i0_), (s1 - .04, b0, der, i0_)]; cambio = True; break   # 40 ms antes: el golpe de la «p» de «perfecto» (tablet10)
            for k in range(1, len(piezas)):                                   # dos trozos de la MISMA isla nunca se pisan (si no, se repite audio)
                if piezas[k][3] == piezas[k - 1][3] and piezas[k][0] < piezas[k - 1][1] and piezas[k][0] > piezas[k - 1][0]:
                    m_ = (piezas[k][0] + piezas[k - 1][1]) / 2; piezas[k - 1] = (piezas[k - 1][0], m_, *piezas[k - 1][2:]); piezas[k] = (m_, *piezas[k][1:]); cambio = True
            if not cambio: break
        dur = T / V
        # 2) ONDA: silencio de cada unión (como la mide Abel) y cualquier hueco > 0,10 s
        _, E = onda.envolvente(str(out / 'voz.wav')); hs, _u = onda.huecos(E); thr = np.percentile(E, 95) - 27
        hs = [h for h in hs if h[1] < dur - COLA - .05]                      # la cola final es a propósito
        hs = [h for h in hs if any(w[1] >= h[1] - .05 for w in pal)]
        pk_ = np.percentile(E, 95)                                           # un «hueco» que nunca baja de pico − 40 y dura < 0,15 s es la voz bajando
        def blando_(a_, b_):                                                 # (el fotograma de silencio digital que separa dos trozos no cuenta)
            v_ = E[round(a_ / .01):max(round(a_ / .01) + 1, round(b_ / .01))]; dig = v_ < pk_ - 80
            return b_ - a_ < .15 and dig.sum() <= 3 and (v_[~dig].min() if (~dig).any() else -999) > pk_ - 40
        hs = [h for h in hs if not blando_(*h)]   # entre palabras dichas seguidas: no es pausa         # tras el hueco no EMPIEZA ninguna palabra = es la consonante muda
                                                                             # DENTRO de la última («perfec-t-o»): se queda tal cual
        inf = [f'##### {nombre} · {dur:.1f} s · {len(piezas)} trozos', f'huecos > 0,10 s (onda): {hs or "ninguno ✓"}']
        if rep: inf.append(f'✗ ISLA REPETIDA: {rep}')
        inf += avisos_mms
        for k, p in enumerate(edl[1:], 1):
            t = p['t']; sil = 0; fondo = 0
            for i in range(max(0, int((t - .04) / .01)), min(len(E), int((t + .04) / .01) + 1)):   # el silencio que TOCA la unión
                if E[i] >= thr: continue
                l = r_ = i
                while l > 0 and E[l - 1] < thr: l -= 1
                while r_ < len(E) and E[r_] < thr: r_ += 1
                if (r_ - l) * .01 > sil: sil = (r_ - l) * .01; zona = (l * .01, r_ * .01)
            blando = sil > 0 and blando_(*zona)                               # la voz baja pero no se calla (cola de palabra + el fotograma de unión)
            if (sil > UNION_MAX and not blando) or sil < UNION_MIN: inf.append(f'✗ {t:6.2f}s unión con {sil:.2f} s de silencio (islas {edl[k-1]["isla"]}→{p["isla"]})')
        # 3) OÍDO: cada unión escuchada sola (±1,3 s) contra lo que tiene que decir; y el reel entero contra el texto de las islas
        voz = leer(out / 'voz.wav'); esperado = [w for w, _, _ in pal]
        for k, p in enumerate(edl[1:], 1):
            t = p['t']; w0 = max(0, t - 1.3); oido = oir_cerca(voz[int(w0 * 16000):int((t + 1.3) * 16000)], t - w0)
            exp = [w for w, s0, s1 in pal if s1 > t - .9 and s0 < t + .9]
            A, B = [nz(w) for w in exp], [nz(w) for w in oido.split()]
            extra = [B[j] for op, i1, i2, j1, j2 in difflib.SequenceMatcher(None, A, B, autojunk=False).get_opcodes() if op in ('insert', 'replace') for j in range(j1, j2)]
            extra = [w for w in extra[1:-1]]                             # los bordes de la ventana cortan palabras: no cuentan
            if extra: inf.append(f'✗ {t:6.2f}s se oye de más: {extra}  ·  «{oido}»')
        todo = oir(voz).split(); A, B = [nz(w) for w in esperado], [nz(w) for w in todo]
        for op, i1, i2, j1, j2 in difflib.SequenceMatcher(None, A, B, autojunk=False).get_opcodes():
            if op != 'equal': inf.append(f'· reel entero {op}: esperado «{" ".join(esperado[i1:i2])}» · se oye «{" ".join(todo[j1:j2])}»')
        E6 = [nz(w) for w in esperado]; vistos = {}                          # FRASE REPETIDA: 6 palabras seguidas (de la MISMA frase) que salen dos veces
        fin_fr = [bool(re.search(r'[.?!…]$', w)) for w in esperado]
        for k in range(len(E6) - 5):
            if any(fin_fr[k:k + 5]): continue
            g6 = tuple(E6[k:k + 6])
            if g6 in vistos and k - vistos[g6] > 6: inf.append(f'✗ el reel repite «{" ".join(esperado[k:k + 6])}»'); break
            vistos.setdefault(g6, k)
        (out / 'edl.json').write_text(json.dumps({'velocidad': V, 'dur': round(dur, 3), 'cola': COLA, 'trozos': edl, 'pal': pal}, ensure_ascii=False), encoding='utf-8')
        texto = '\n'.join(inf); (out / 'INFORME.txt').write_text(texto, encoding='utf-8'); print(texto)
        malos += sum(1 for x in inf if x.startswith('✗')) + (1 if hs else 0)
    sys.exit(1 if malos else 0)
