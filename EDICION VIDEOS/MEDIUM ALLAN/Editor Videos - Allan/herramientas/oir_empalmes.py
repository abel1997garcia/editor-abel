"""Escucha en el REEL cada empalme indicado (±1,3 s alrededor del corte entre el trozo n-1 y n), que es lo que oye la gente.
python herramientas/oir_empalmes.py <reel> n1 n2 ...        (sobre el MP4 montado)
python herramientas/oir_empalmes.py --voz <reel> n1 n2 ...  (PASO 1: sobre trabajo/reels/<reel>/voz.wav, antes del vídeo)"""
import json, subprocess, sys
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')
RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / '.claude/skills/animaciones-horizontal-combinadas/scripts'))
from transcribir import preparar_cuda; preparar_cuda()
from faster_whisper import WhisperModel
m = WhisperModel('large-v3', device='cuda', compute_type='float16')
args = sys.argv[1:]
usar_voz = args[0] == '--voz'
if usar_voz:
    args = args[1:]
nombre = args[0]
fuente = RAIZ / 'trabajo/reels' / nombre / 'voz.wav' if usar_voz else RAIZ / 'reels' / f'{nombre}.mp4'
M = json.load(open(RAIZ / 'trabajo/reels' / nombre / 'montaje.json', encoding='utf-8'))
for n in map(int, args[1:] or range(1, len(M['segmentos']))):
    t = M['segmentos'][n]['out']
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', f'{max(0, t - 1.3):.3f}', '-t', '2.6', '-i', str(fuente),
                    '-ac', '1', '-ar', '16000', str(RAIZ / 'trabajo/_emp.wav')], check=True)
    segs, _ = m.transcribe(str(RAIZ / 'trabajo/_emp.wav'), language='es', beam_size=5, temperature=0, condition_on_previous_text=False)
    print(f'{nombre} empalme {n-1}|{n} (t={t:.2f}): «' + ' '.join(s.text.strip() for s in segs) + '»')
