"""Escucha ENTERA de la voz montada de cada reel (para compararla con el guion del Drive).
    python escuchar.py <reels.json> [reel ...]"""
import json, sys
from pathlib import Path
import torch  # noqa: F401
from faster_whisper import WhisperModel
sys.path.insert(0, str(Path(__file__).resolve().parent)); from casual_prep import LITERAL
sys.stdout.reconfigure(encoding='utf-8')
ruta = Path(sys.argv[1]).resolve(); cfg = json.load(open(ruta, encoding='utf-8'))
m = WhisperModel('large-v3', device='cuda', compute_type='float16')
for n in sys.argv[2:] or cfg['reels']:
    v = ruta.parent / cfg['salida'] / f'_{n}' / 'voz.wav'
    print(f'== {n}:', ' '.join(s.text.strip() for s in m.transcribe(str(v), language='es', initial_prompt=LITERAL, condition_on_previous_text=False)[0]))
