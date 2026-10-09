import sys, subprocess
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, str(__import__('pathlib').Path(__file__).resolve().parent.parent / '.claude/skills/animaciones-horizontal-combinadas/scripts'))
from transcribir import preparar_cuda; preparar_cuda()
from faster_whisper import WhisperModel
m = WhisperModel('large-v3', device='cuda', compute_type='float16')
src = sys.argv[1]
for r in sys.argv[2:]:
    a, b = map(float, r.split(':'))
    subprocess.run(['ffmpeg','-v','error','-y','-ss',str(a),'-t',str(b-a),'-i',src,'-ac','1','-ar','16000','_clip.wav'],check=True)
    segs,_ = m.transcribe('_clip.wav', language='es', beam_size=5, condition_on_previous_text=False, temperature=0)
    print(f'{a}-{b}:', ' '.join(s.text.strip() for s in segs))
