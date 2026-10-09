"""Las animaciones no tapan los zooms de énfasis de la toma limpia: recorta su final al empezar un zoom.
    python recortar_zooms.py <proyecto de la skill> <toma_limpia.planos.json>      (después de ventanas.py)"""
import json, sys
from pathlib import Path
pro, pl = Path(sys.argv[1]), Path(sys.argv[2])
m = json.load(open(pro / 'edicion/montaje.json', encoding='utf-8')); fps = m['fps']
P = json.load(open(pl, encoding='utf-8')); T, Z = 0, []
for p in P:
    d = p['t1'] - p['t0']
    if p['zoom'] > 1: Z.append((T, T + d))
    T += d
for p in m['planos']:
    if p['tipo'] != 'anim': continue
    for a, b in Z:
        if p['f0'] / fps < a < p['f1'] / fps: print(f"{p['id']}: {p['f1']/fps:.2f} -> {a:.2f}"); p['f1'] = round(a * fps)
        if a <= p['f0'] / fps < b: print('¡empieza dentro de un zoom!', p['id'])
# los planos de cara rellenan los huecos
pl, f = [], 0
for p in [x for x in m['planos'] if x['tipo'] == 'anim']:
    if p['f0'] > f: pl.append({'tipo': 'cara', 'f0': f, 'f1': p['f0'], 'zooms': [1.0]})
    pl.append(p); f = p['f1']
dur = m['planos'][-1]['f1']
if f < dur: pl.append({'tipo': 'cara', 'f0': f, 'f1': dur, 'zooms': [1.0]})
m['planos'] = pl
json.dump(m, open(pro / 'edicion/montaje.json', 'w', encoding='utf-8'), indent=1)
print('zooms:', [(round(a, 1), round(b, 1)) for a, b in Z])
