"""Busca ESCUCHANDO hasta dónde llega una palabra que lleva pegada una muletilla detrás («realmente, ¿no?»).
Prueba finales cada 20 ms y devuelve el ÚLTIMO en que la última palabra oída sigue siendo la esperada (sin muletilla).
Uso: python herramientas/buscar_fin.py <tiempos.json> <indice> [...]   -> poner «fin_max» = valor devuelto"""
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
    esperado = plano(W[k]['w'])[-1]
    ultimo_ok = None
    for t in np.arange(W[k]['e'] - 0.05, W[k]['e'] + 0.7, 0.02):
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', f'{t - 1.3:.3f}', '-t', '1.3', '-i', str(audio), str(RAIZ / 'trabajo/_bf.wav')], check=True)
        segs, _ = m.transcribe(str(RAIZ / 'trabajo/_bf.wav'), language='es', beam_size=5, temperature=0, condition_on_previous_text=False)
        o = plano(' '.join(s.text for s in segs))
        if o and o[-1] == esperado:
            ultimo_ok = round(float(t), 2)
        elif ultimo_ok is not None:
            break
    print(f"[{k}] «{W[k]['w']}»: termina limpia hasta {ultimo_ok} s (alineada {W[k]['e']:.2f})")
