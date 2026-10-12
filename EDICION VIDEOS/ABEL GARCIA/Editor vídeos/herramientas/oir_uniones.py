"""Segunda escucha de las uniones que verificar_audio marca con ✗: transcribe 4 s alrededor de cada una para ver si de verdad
falta, sobra o se repite algo (en «empezar desde 0» varios ✗ eran Whisper oyendo mal un trozo de 2 s).
    python oir_uniones.py <verif.log> <carpeta out>     (verif.log = salida de verificar_audio con «##### out/_<reel>»)
"""
import re, subprocess, sys, tempfile
from pathlib import Path
import torch  # noqa: F401
from faster_whisper import WhisperModel

sys.stdout.reconfigure(encoding='utf-8')
m = WhisperModel('large-v3', device='cuda', compute_type='float16'); reel = None
for linea in open(sys.argv[1], encoding='utf-8'):
    if linea.startswith('#####'): reel = Path(linea.split()[1]).name
    x = re.match(r'\s*✗\s+([\d.]+)s', linea)
    if x and reel:
        t = float(x.group(1)); wav = Path(tempfile.mkdtemp()) / 'u.wav'
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', str(max(0, t - 2)), '-t', '4', '-i', str(Path(sys.argv[2]) / reel / 'voz.wav'), str(wav)])
        print(f'{reel} {t:6.2f}s:', ' '.join(w.word.strip() for s in m.transcribe(str(wav), language='es', word_timestamps=True)[0] for w in s.words))
