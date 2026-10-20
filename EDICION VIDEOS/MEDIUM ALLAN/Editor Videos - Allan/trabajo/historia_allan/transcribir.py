"""Transcribe los vídeos de la historia de Allan (faster-whisper large-v3) -> <id>.txt con marcas de tiempo."""
import os, sys
from pathlib import Path
import nvidia
for sub in ('cublas', 'cudnn'):                        # las DLL de CUDA están en los paquetes pip de nvidia, fuera del PATH de Windows
    d = os.path.join(nvidia.__path__[0], sub, 'bin'); os.add_dll_directory(d); os.environ['PATH'] = d + os.pathsep + os.environ['PATH']
from faster_whisper import WhisperModel

AQUI = Path(__file__).resolve().parent
m = WhisperModel('large-v3', device='cuda', compute_type='float16')
for vid in sys.argv[1:]:
    segs, _ = m.transcribe(str(AQUI / f'{vid}.m4a'), language='es', vad_filter=True, beam_size=5)
    with open(AQUI / f'{vid}.txt', 'w', encoding='utf-8') as f:
        for s in segs:
            t = int(s.start); f.write(f'[{t // 60}:{t % 60:02d}] {s.text.strip()}\n'); f.flush()
    print('hecho', vid, flush=True)
