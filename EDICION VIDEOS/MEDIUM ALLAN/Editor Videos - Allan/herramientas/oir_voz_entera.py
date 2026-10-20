"""Escucha la VOZ montada ENTERA (trabajo/reels/<reel>/voz.wav) en ventanas de >= 5 s que empiezan y acaban en
empalmes (no parten palabras), con prompt que hace que Whisper escriba las muletillas, y pone debajo el guion de esa
ventana para compararlo. Marca '!!' donde lo oído no coincide con el guion.

    python herramientas/oir_voz_entera.py <reel> [<reel> ...]
"""
import difflib, json, re, subprocess, sys, unicodedata
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')
RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / '.claude/skills/animaciones-horizontal-combinadas/scripts'))
from transcribir import preparar_cuda; preparar_cuda()
from faster_whisper import WhisperModel

m = WhisperModel('large-v3', device='cuda', compute_type='float16')
plano = lambda s: re.sub(r'[^a-z0-9 ]', '', unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode().lower()).split()

for nombre in sys.argv[1:]:
    carpeta = RAIZ / 'trabajo/reels' / nombre
    M = json.load(open(carpeta / 'montaje.json', encoding='utf-8'))
    outs = [s['out'] for s in M['segmentos']] + [M['duracion']]
    v = [0.0]
    for o in outs[1:]:
        if o - v[-1] >= 5.0 or o == outs[-1]:
            v.append(o)
    subs = [s for s in M['subtitulos'] if s['txt']]
    print(f'===== {nombre}')
    for a, b in zip(v, v[1:]):
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', f'{a:.3f}', '-t', f'{b - a:.3f}', '-i', str(carpeta / 'voz.wav'),
                        '-ac', '1', '-ar', '16000', str(RAIZ / 'trabajo/_ve.wav')], check=True)
        segs, _ = m.transcribe(str(RAIZ / 'trabajo/_ve.wav'), language='es', beam_size=5, temperature=0,
                               condition_on_previous_text=False, initial_prompt='Eh... mmm... pues, eh, o sea, este... eh, ¿no?')
        oido = ' '.join(s.text.strip() for s in segs)
        guion = ' '.join(s['txt'] for s in subs if a - 0.05 <= s['t0'] < b - 0.05)
        r = difflib.SequenceMatcher(None, plano(oido), plano(guion)).ratio()
        print(f'{"!!" if r < 0.9 else "  "} {a:5.2f}-{b:5.2f}  oído : {oido}\n{"":15s}guion: {guion}')
