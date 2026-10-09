"""Escucha un reel por tramos de ~6 s (Whisper en clips cortos es mucho más fiable que la pasada larga) y compara
con el guion. Marca '!!' los tramos donde lo oído no coincide. python herramientas/revisar_por_tramos.py reels/x.mp4 ..."""
import difflib, json, re, subprocess, sys, unicodedata
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')
RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / '.claude/skills/animaciones-horizontal-combinadas/scripts'))
from transcribir import preparar_cuda; preparar_cuda()
from faster_whisper import WhisperModel
m = WhisperModel('large-v3', device='cuda', compute_type='float16')
plano = lambda s: re.sub(r'[^a-z0-9 ]', '', unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode().lower())
for mp4 in sys.argv[1:]:
    nombre = Path(mp4).stem
    M = json.load(open(RAIZ / 'trabajo/reels' / nombre / 'montaje.json', encoding='utf-8'))
    subs = [s for s in M['subtitulos'] if s['txt']]
    grupos, g = [], []
    for s in subs:
        g.append(s)
        if g[-1]['t1'] - g[0]['t0'] >= 5.5:
            grupos.append(g); g = []
    if g: grupos.append(g)
    print(f'== {nombre}')
    malos = 0
    for g in grupos:
        a, b = max(0, g[0]['t0'] - 0.05), g[-1]['t1'] + 0.05
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', f'{a:.3f}', '-t', f'{b - a:.3f}', '-i', mp4, '-ac', '1', '-ar', '16000',
                        str(RAIZ / 'trabajo' / '_tramo.wav')], check=True)
        segs, _ = m.transcribe(str(RAIZ / 'trabajo' / '_tramo.wav'), language='es', beam_size=5, temperature=0,
                               condition_on_previous_text=False)
        oido = ' '.join(s.text.strip() for s in segs)
        esperado = ' '.join(s['txt'] for s in g)
        r = difflib.SequenceMatcher(None, plano(esperado).split(), plano(oido).split()).ratio()
        marca = '!!' if r < 0.9 else '  '
        malos += r < 0.9
        print(f'{marca} {a:5.1f}-{b:5.1f} {r:.2f}\n     guion: {esperado}\n     oído : {oido}')
    print(f'   tramos a revisar: {malos} de {len(grupos)}')
