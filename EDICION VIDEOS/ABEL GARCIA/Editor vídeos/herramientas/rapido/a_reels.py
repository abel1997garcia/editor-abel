"""Copia los reels terminados de una carpeta viral a MarcaPersonal/REELS con su número, alternando PUBLICAR/TRIAL
(sigue la alternancia del último número), y su .txt de descripción (descripciones.json de la carpeta).
    python herramientas/rapido/a_reels.py MarcaPersonal/virales/<carpeta>"""
import json, re, shutil, sys
from pathlib import Path
d = Path(sys.argv[1]); plan = json.loads((d / 'plan.json').read_text(encoding='utf-8'))
desc = json.loads((d / 'descripciones.json').read_text(encoding='utf-8'))
R = Path(__file__).resolve().parents[2] / 'MarcaPersonal' / 'REELS'
ult = max((f for f in R.glob('*.mp4') if f.name[:3].isdigit()), key=lambda f: int(f.name[:3]))
n, pub = int(ult.name[:3]), 'PUBLICAR' in ult.name
for k, (nombre, r) in enumerate(plan['reels'].items()):
    n += 1; pub = not pub
    tit = re.sub(r'[:*?"<>|/\\]', '', r['titulo']).strip()
    base = f"{n:03d} · {'PUBLICAR' if pub else 'TRIAL'} · {d.name} · e1-g{k + 1} · {tit}"
    shutil.copy2(d / 'out_rapido' / nombre / f'{nombre}.mp4', R / f'{base}.mp4')
    (R / f'{base}.txt').write_text(desc[nombre], encoding='utf-8'); print(base)
