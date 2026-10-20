"""Red contra las TRABAZONES (Abel 14/10/2026: «hay veces que me equivoco y no están recortados, medio recortados»).
Whisper «limpia» lo que oye: «Solo… solo publicas» lo apunta como UN «Solo» y el corte deja la trabazón dentro.
Esto vuelve a escuchar la voz YA MONTADA (out/_<reel>/voz.wav, tras `reel_tablero.py --voz`), la compara palabra a palabra
con lo que debería decir y lista lo que SOBRA o FALTA, con el segundo del reel y el de la fuente para cortarlo.

    python sobras.py <reels.json> [reel ...]
Cada «SOBRA» se corta en reels.json (partir el tramo o "quitar") y se repite --voz + sobras.py hasta que no quede nada.
"""
import difflib, json, re, sys
from pathlib import Path
import torch  # noqa: F401
from faster_whisper import WhisperModel
sys.path.insert(0, str(Path(__file__).resolve().parent))
from reel_yapping import VELOCIDAD
from casual_prep import LITERAL
sys.stdout.reconfigure(encoding='utf-8')
norm = lambda w: re.sub(r'[^a-z0-9ñ]', '', w.lower().translate(str.maketrans('áéíóúü', 'aeiouu')))


def fuente(t, ps, pads):
    """segundo del reel -> segundo de la fuente"""
    T = 0.0
    for (t0, t1, _), pd in zip(ps, pads):
        L = (t1 - t0) / VELOCIDAD
        if t <= T + L: return t0 + (t - T) * VELOCIDAD
        T += L + pd / VELOCIDAD
    return ps[-1][1]


if __name__ == '__main__':
    ruta = Path(sys.argv[1]).resolve(); cfg = json.load(open(ruta, encoding='utf-8'))
    W = json.load(open(ruta.parent / cfg['tiempos'], encoding='utf-8')); W = W['palabras'] if isinstance(W, dict) else W
    m = WhisperModel('large-v3', device='cuda', compute_type='float16'); total = 0
    for nombre in sys.argv[2:] or cfg['reels']:
        tmp = ruta.parent / cfg['salida'] / f'_{nombre}'; c = json.load(open(tmp / 'onda.json'))
        ps, pads = c['ps'], c['pads']
        if (tmp / 'velocidad.txt').exists(): VELOCIDAD = float((tmp / 'velocidad.txt').read_text())
        esperado = [W[i]['w'] for _, _, g in ps for i in g]
        segs, _ = m.transcribe(str(tmp / 'voz.wav'), language='es', word_timestamps=True, initial_prompt=LITERAL, condition_on_previous_text=False)
        oido = [(w.word.strip(), w.start) for s in segs for w in s.words]
        a, b = [norm(w) for w in esperado], [norm(w) for w, _ in oido]
        print(f'== {nombre}')
        for op, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes():
            if op == 'equal': continue
            t = oido[min(j1, len(oido) - 1)][1]
            txt = ' '.join(w for w, _ in oido[j1:j2])
            if op == 'insert': print(f'   SOBRA  «{txt}»  reel {t:.2f} s · fuente {fuente(t, ps, pads):.2f} s'); total += 1
            elif op == 'delete': print(f'   FALTA  «{" ".join(esperado[i1:i2])}»  reel ~{t:.2f} s'); total += 1
            else: print(f'   DISTINTO  esperaba «{" ".join(esperado[i1:i2])}» · se oye «{txt}»  reel {t:.2f} s · fuente {fuente(t, ps, pads):.2f} s'); total += 1
    sys.exit(1 if total else 0)
