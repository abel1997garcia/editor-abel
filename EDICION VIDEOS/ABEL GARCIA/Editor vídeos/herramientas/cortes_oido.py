# escucha CADA corte del reel por separado (±1,3 s) sobre voz.wav o el MP4 — la escucha del vídeo entero RELLENA lo que falta
import torch, sys, json, subprocess, numpy as np
sys.path.insert(0, r'C:\Users\Clap\Desktop\EDICION VIDEOS\ABEL GARCIA\Editor vídeos\herramientas')
from casual_prep import LITERAL
from faster_whisper import WhisperModel
m = WhisperModel('large-v3', device='cuda', compute_type='float16')
d, V = sys.argv[1], float(sys.argv[2])
for r in sys.argv[3:]:
    c = json.load(open(f'{d}/out/_{r}/onda.json')); T = 0; cs = []
    for (a, b, g), p in zip(c['ps'], c['pads']): T += (b - a) / V; cs.append((round(T, 2), b)); T += p / V
    src = f'{d}/out/{r}.mp4' if '--mp4' in sys.argv else f'{d}/out/_{r}/voz.wav'
    x0 = np.frombuffer(subprocess.run(['ffmpeg','-v','error','-i',src,'-ac','1','-ar','16000','-f','s16le','-'],capture_output=True).stdout,np.int16).astype(np.float32)/32768
    print('##', r)
    for t, b in cs[:-1]:
        x = np.concatenate([np.zeros(8000,np.float32), x0[int(max(0,t-1.3)*16000):int((t+1.3)*16000)], np.zeros(8000,np.float32)])
        s, _ = m.transcribe(x, language='es', initial_prompt=LITERAL, condition_on_previous_text=False)
        print(f'{t:6.2f}s |', ' '.join(q.text.strip() for q in s))
