"""Transcribe todos los reels de una carpeta de referencia (bajados con yt-dlp + .info.json).
    python -I transcribir_referencias.py <carpeta con videos/>  ->  <carpeta>/transcripciones.json
Guarda por reel: likes, comentarios, duración, título del post, texto entero y el gancho (primera frase).
Si ya está transcrito, lo salta (se puede relanzar).
"""
import json, re, sys
from pathlib import Path
import torch  # noqa: F401  (DLL de cuBLAS)
from faster_whisper import WhisperModel

d = Path(sys.argv[1]); out = d / 'transcripciones.json'
res = json.loads(out.read_text(encoding='utf-8')) if out.exists() else {}
m = WhisperModel('large-v3', device='cuda', compute_type='float16')
for f in sorted((d / 'videos').glob('*.mp4')):
    if f.stem in res:
        continue
    info = json.loads(f.with_suffix('.info.json').read_text(encoding='utf-8')) if f.with_suffix('.info.json').exists() else {}
    segs, _ = m.transcribe(str(f), language='es', vad_filter=True)
    texto = ' '.join(s.text.strip() for s in segs).strip()
    res[f.stem] = {'likes': info.get('like_count'), 'comentarios': info.get('comment_count'), 'dur': info.get('duration'),
                   'fecha': info.get('upload_date'), 'post': (info.get('description') or '')[:300],
                   'gancho': re.split(r'(?<=[.?!])\s', texto, 1)[0] if texto else '', 'texto': texto}
    out.write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding='utf-8')
    print(f.stem, res[f.stem]['likes'], res[f.stem]['gancho'][:90], flush=True)
print('total', len(res))
