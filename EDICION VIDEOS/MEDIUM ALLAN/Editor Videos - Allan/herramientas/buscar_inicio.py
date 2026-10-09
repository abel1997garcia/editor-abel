"""Busca ESCUCHANDO el instante exacto en que empieza una palabra que lleva pegada una muletilla delante
(«pues se arregla», «o no siempre»). Prueba arranques cada 20 ms y devuelve el primero en que Whisper oye la palabra
esperada como primera palabra. Uso: python herramientas/buscar_inicio.py <tiempos.json> <indice> [<indice> ...]"""
import json, re, subprocess, sys, unicodedata
from pathlib import Path
import numpy as np
sys.stdout.reconfigure(encoding='utf-8')
RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / '.claude/skills/animaciones-horizontal-combinadas/scripts'))
from transcribir import preparar_cuda; preparar_cuda()
from faster_whisper import WhisperModel
m = WhisperModel('large-v3', device='cuda', compute_type='float16')
plano = lambda s: re.sub(r'[^a-z0-9 ]', '', unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode().lower()).split()
tiempos = Path(sys.argv[1])
W = json.load(open(tiempos, encoding='utf-8'))
audio = tiempos.parent / 'audio16k.wav'
for k in map(int, sys.argv[2:]):
    esperado = plano(W[k]['w'])[0]
    sig = plano(W[k + 1]['w'])[0] if k + 1 < len(W) else ''
    encontrado = None
    for t in np.arange(W[k - 1]['s'], W[k]['s'] + 0.4, 0.02):
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', f'{t:.3f}', '-t', '1.3', '-i', str(audio), str(RAIZ / 'trabajo/_bi.wav')], check=True)
        segs, _ = m.transcribe(str(RAIZ / 'trabajo/_bi.wav'), language='es', beam_size=5, temperature=0, condition_on_previous_text=False)
        o = plano(' '.join(s.text for s in segs))
        if o and o[0] == esperado and (len(o) < 2 or not sig or o[1] == sig or True):
            encontrado = round(float(t), 2)
            print(f"[{k}] «{W[k]['w']}»: empieza limpia en {encontrado} s (alineada {W[k]['s']:.2f}) -> oído «{' '.join(o[:4])}»")
            break
    if encontrado is None:
        print(f"[{k}] «{W[k]['w']}»: NO encontrado un arranque limpio")
