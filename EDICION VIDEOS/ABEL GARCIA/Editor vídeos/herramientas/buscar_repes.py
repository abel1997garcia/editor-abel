"""Busca palabras o frases repetidas seguidas en el audio de reels ya renderizados («y son ‖ y son»): síntoma de dos planos
solapados. Las compara con la grabación original: si en el original ya estaban repetidas, no es un fallo del corte.
    python buscar_repes.py <mp4> [<mp4> ...]
"""
import re, sys, subprocess, tempfile
from pathlib import Path
import torch  # noqa: F401
from faster_whisper import WhisperModel

sys.stdout.reconfigure(encoding='utf-8')
m = WhisperModel('large-v3', device='cuda', compute_type='float16')
n = lambda w: re.sub(r'[^a-záéíóúñü0-9]', '', w.lower())
for v in sys.argv[1:]:
    wav = Path(tempfile.mkdtemp()) / 'a.wav'
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', v, '-vn', '-ac', '1', '-ar', '16000', str(wav)])
    W = [(n(w.word), w.start) for s in m.transcribe(str(wav), language='es', word_timestamps=True)[0] for w in s.words]
    W = [w for w in W if w[0]]
    rep = []
    for k in (3, 2, 1):
        for i in range(len(W) - 2 * k + 1):
            a, b = [x[0] for x in W[i:i + k]], [x[0] for x in W[i + k:i + 2 * k]]
            if a == b and (k > 1 or len(a[0]) > 3): rep.append(f"{W[i][1]:.1f}s «{' '.join(a)} {' '.join(b)}»")
    print(Path(v).name[:60], '→', '; '.join(dict.fromkeys(rep)) or 'sin repeticiones')
