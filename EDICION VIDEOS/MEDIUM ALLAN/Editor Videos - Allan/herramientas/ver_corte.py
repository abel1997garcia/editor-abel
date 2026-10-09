"""Muestra el contexto de un corte: palabras alrededor y energía (10 ms) cerca del punto.
python herramientas/ver_corte.py <reel> <n_trozo> ini|fin"""
import json, subprocess, sys
import numpy as np
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')
RAIZ = Path(__file__).resolve().parent.parent
nombre, i, lado = sys.argv[1], int(sys.argv[2]), sys.argv[3]
M = json.load(open(RAIZ / 'trabajo' / 'reels' / nombre / 'montaje.json', encoding='utf-8'))
spec = json.load(open(RAIZ / 'reels' / 'specs' / f'{nombre}.json', encoding='utf-8'))
W = json.load(open(RAIZ / spec['tiempos'], encoding='utf-8'))
sg = M['segmentos'][i]
k = sg['palabras'][0] if lado == 'ini' else sg['palabras'][-1]
t = sg['ini'] if lado == 'ini' else sg['fin']
raw = subprocess.run(['ffmpeg', '-v', 'error', '-ss', f'{t - 0.4:.3f}', '-t', '0.8', '-i',
                      str(RAIZ / Path(spec['tiempos']).parent / 'audio16k.wav'), '-f', 's16le', '-'], capture_output=True).stdout
y = np.frombuffer(raw, np.int16).astype(float)
e = [int(np.sqrt((y[j:j + 160] ** 2).mean()) / 100) for j in range(0, len(y) - 160, 160)]
ctx = ' '.join(('[' if q == k else '') + W[q]['w'] + (']' if q == k else '') for q in range(k - 3, k + 4))
print(f"{nombre} trozo {i} {lado} t={t:.2f} | {ctx}")
print('   energía -0.4..+0.4 (| = corte):', ' '.join(map(str, e[:40])), '|', ' '.join(map(str, e[40:])))
print(f"   palabra [{W[k]['w']}] alineada {W[k]['s']:.2f}-{W[k]['e']:.2f}")
