"""Cuánto dura cada escena (HISTORIA) o cada estado de la lista (TABLET) en un reel montado. Límite: MAX_ESCENA s
(Abel 19/10/2026: «si un dibujo dura mucho se hace pesado y cansino»). Si alguna pasa, se añade otra escena en ese tramo.
    python herramientas/rapido/duracion_escenas.py <carpeta> [reel]"""
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from render import en_reel, corrige_texto, mayusculas
from capa_viral import MAX_ESCENA
d = Path(sys.argv[1]); plan = json.loads((d / 'plan.json').read_text(encoding='utf-8'))
for r in (sys.argv[2:] or list(plan['reels'])[:1]):
    e = json.loads((d / 'out_rapido' / r / 'edl.json').read_text(encoding='utf-8'))
    pal = mayusculas(corrige_texto([list(p) for p in e['pal']], plan.get('corrige', [])))
    ds = plan['reels'][r].get('diapos', plan.get('diapos', [])); ts, t = [], 0
    for x in ds: t = en_reel(pal, x['frase'], t)[0]; ts.append(t)
    ts.append(e['dur']); malas = 0
    for x, a, b in zip(ds, ts, ts[1:]):
        mal = b - a > MAX_ESCENA; malas += mal
        print(f"  {'✗' if mal else ' '} {b - a:5.1f} s  {x['titulo']}  (desde «{x['frase']}», {a:.1f} s)")
    print(f'{d.name} {r}: ' + ('✓ ninguna escena pasa de %d s' % MAX_ESCENA if not malas else f'{malas} escenas demasiado largas'))
