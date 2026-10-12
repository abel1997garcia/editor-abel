"""Analiza reels de referencia: duración, cortes de imagen, ritmo de voz, silencios entre palabras y el gancho.
    python -I analizar_reels_ref.py <carpeta con .mp4>   -> <carpeta>/analisis.json + hoja de portadas <carpeta>/portadas.png
"""
import json, re, subprocess, sys
from pathlib import Path
import torch  # noqa: F401  (DLL de cuBLAS)
from faster_whisper import WhisperModel

d = Path(sys.argv[1]); m = WhisperModel('large-v3', device='cuda', compute_type='float16'); res = {}
for f in sorted(d.glob('*.mp4')):
    dur = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', str(f)], capture_output=True, text=True).stdout)
    sc = subprocess.run(['ffmpeg', '-hide_banner', '-i', str(f), '-vf', "select='gt(scene,0.25)',showinfo", '-an', '-f', 'null', '-'], capture_output=True, text=True).stderr
    cortes = [float(x) for x in re.findall(r'pts_time:([\d.]+)', sc)]
    w = [(x.word.strip(), x.start, x.end) for s in m.transcribe(str(f), language='es', word_timestamps=True)[0] for x in s.words]
    gaps = sorted(round(w[i + 1][1] - w[i][2], 2) for i in range(len(w) - 1))
    habla = w[-1][2] - w[0][1] if w else 0
    texto = ' '.join(x[0] for x in w)
    gancho = re.split(r'(?<=[.?!])\s', texto, 1)[0]
    res[f.stem] = {'dur': round(dur, 1), 'cortes_imagen': len(cortes), 'cortes_cada_10s': round(len(cortes) / dur * 10, 1),
                   'palabras_por_s': round(len(w) / habla, 2) if habla else 0, 'primera_palabra_s': round(w[0][1], 2) if w else None,
                   'hueco_mediana': gaps[len(gaps) // 2] if gaps else None, 'hueco_p90': gaps[int(len(gaps) * .9)] if gaps else None,
                   'hueco_max': gaps[-1] if gaps else None, 'huecos_>0,3': sum(g > .3 for g in gaps),
                   'silencio_total_s': round(sum(g for g in gaps if g > .05), 1), 'gancho': gancho, 'texto': texto}
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', '1.5', '-i', str(f), '-frames:v', '1', '-vf', 'scale=270:-2', str(d / f'_p_{f.stem}.png')])
    print(f.stem, {k: v for k, v in res[f.stem].items() if k != 'texto'})
json.dump(res, open(d / 'analisis.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1, default=float)
ps = sorted(d.glob('_p_*.png'))
subprocess.run(['ffmpeg', '-v', 'error', '-y', *sum([['-i', str(p)] for p in ps], []), '-filter_complex',
                ''.join(f'[{i}]scale=270:480,setsar=1[s{i}];' for i in range(len(ps))) + ''.join(f'[s{i}]' for i in range(len(ps))) + f'xstack=inputs={len(ps)}:layout=' +
                '|'.join(f'{(i % 5) * 270}_{(i // 5) * 480}' for i in range(len(ps))), str(d / 'portadas.png')])
for p in ps: p.unlink()
