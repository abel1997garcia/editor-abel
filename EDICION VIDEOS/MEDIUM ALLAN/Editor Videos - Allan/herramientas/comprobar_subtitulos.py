"""Comprueba que los subtítulos CUADRAN con la voz del reel: cada uno entra cuando suena su primera palabra (entre
0,25 s antes y 0,05 s después), no se va antes de que acabe su última palabra, no hay huecos ni solapes entre
subtítulos y ninguno pasa de 6 palabras. Devuelve 1 si algo falla.

    python herramientas/comprobar_subtitulos.py <reel> [<reel> ...]
"""
import json, sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')
RAIZ = Path(__file__).resolve().parent.parent
malo = False
for nombre in sys.argv[1:]:
    M = json.load(open(RAIZ / 'trabajo/reels' / nombre / 'montaje.json', encoding='utf-8'))
    spec = json.load(open(RAIZ / 'trabajo/specs' / f'{nombre}.json', encoding='utf-8'))
    T = {w['i']: w for w in json.load(open(RAIZ / spec['tiempos'], encoding='utf-8'))}
    pos = {}
    for s in M['segmentos']:
        for i in s['palabras']:
            pos[i] = (s['out'] + max(0, T[i]['s'] - s['ini']), s['out'] + min(s['fin'], T[i]['e']) - s['ini'])
    subs = [u for u in M['subtitulos'] if u['txt']]
    fallos = []
    for k, u in enumerate(subs):
        a, b = pos[u['a']][0], pos[u['b']][1]
        if not (-0.25 <= u['t0'] - a <= 0.05):
            fallos.append(f"  «{u['txt']}» entra {u['t0'] - a:+.2f} s respecto a su primera palabra")
        if u['t1'] < b - 0.05:
            fallos.append(f"  «{u['txt']}» se va {b - u['t1']:.2f} s antes de acabar su última palabra")
        if len(u['txt'].split()) > 6:
            fallos.append(f"  «{u['txt']}» tiene {len(u['txt'].split())} palabras")
        if k and abs(u['t0'] - subs[k - 1]['t1']) > 0.01:
            fallos.append(f"  hueco/solape de {u['t0'] - subs[k - 1]['t1']:+.2f} s antes de «{u['txt']}»")
    print(f"{nombre}: {len(subs)} subtítulos -> " + ('OK, cuadran con la voz' if not fallos else f'{len(fallos)} FALLOS'))
    for f in fallos:
        print(f)
    malo |= bool(fallos)
sys.exit(1 if malo else 0)
