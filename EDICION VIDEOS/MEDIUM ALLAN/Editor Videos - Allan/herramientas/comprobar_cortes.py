"""Comprueba que NINGÚN corte se come una palabra (error repetido: «exist», «cort»).
Para cada trozo de cada reel escucha (Whisper) sobre el ORIGINAL:
  - final: [fin-1.5, fin]  -> la última palabra oída tiene que ser la última palabra del trozo, entera;
  - inicio: [ini, ini+1.5] -> la primera palabra oída tiene que ser la primera del trozo, entera.
Si no coincide, lo marca con '!!' y muestra lo que se oye cortado y con 0,4 s más de margen.
Uso: python herramientas/comprobar_cortes.py <reel> [<reel> ...]     (nombre del reel, p. ej. guias_03_desgracias)"""
import json, re, subprocess, sys, unicodedata
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')
RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / '.claude/skills/animaciones-horizontal-combinadas/scripts'))
from transcribir import preparar_cuda; preparar_cuda()
from faster_whisper import WhisperModel
m = WhisperModel('large-v3', device='cuda', compute_type='float16')
plano = lambda s: re.sub(r'[^a-z0-9 ]', '', unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode().lower()).split()
TMP = RAIZ / 'trabajo' / '_corte.wav'


def oir(audio, a, b):
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', f'{max(0, a):.3f}', '-t', f'{b - max(0, a):.3f}', '-i', str(audio),
                    '-ac', '1', '-ar', '16000', str(TMP)], check=True)
    segs, _ = m.transcribe(str(TMP), language='es', beam_size=5, temperature=0, condition_on_previous_text=False)
    return ' '.join(s.text.strip() for s in segs)


def parecida(x, y):
    return x == y or (len(x) > 3 and len(y) > 3 and (x[:-1] == y[:-1]))   # tolera tildes/plural mínimos


malos_total = 0
for nombre in sys.argv[1:]:
    M = json.load(open(RAIZ / 'trabajo/reels' / nombre / 'montaje.json', encoding='utf-8'))
    spec = json.load(open(RAIZ / 'reels/specs' / f'{nombre}.json', encoding='utf-8'))
    W = json.load(open(RAIZ / spec['tiempos'], encoding='utf-8'))
    audio = RAIZ / Path(spec['tiempos']).parent / 'audio16k.wav'
    print(f'== {nombre}')
    for i, sg in enumerate(M['segmentos']):
        a, b = sg['palabras'][0], sg['palabras'][-1]
        ult, pri = plano(W[b]['w']), plano(W[a]['w'])
        for lado in ('fin', 'ini'):
            if lado == 'fin':
                o = plano(oir(audio, sg['fin'] - 1.5, sg['fin']))
                ok = bool(o) and bool(ult) and parecida(o[-1], ult[-1])
                esperado, visto = W[b]['w'], (o[-1] if o else '')
            else:
                o = plano(oir(audio, sg['ini'], sg['ini'] + 1.5))
                ok = bool(o) and bool(pri) and parecida(o[0], pri[0])
                esperado, visto = W[a]['w'], (o[0] if o else '')
            if not ok:
                malos_total += 1
                extra = oir(audio, sg['fin'] - 1.5, sg['fin'] + 0.4) if lado == 'fin' else oir(audio, sg['ini'] - 0.4, sg['ini'] + 1.5)
                print(f"!! trozo {i} {lado} ({sg[lado]:.2f}s): esperado «{esperado}», se oye «{visto}» | con margen: «{extra}»")
    print(f'   revisados {len(M["segmentos"])} trozos')
print(f'TOTAL a revisar: {malos_total}')
