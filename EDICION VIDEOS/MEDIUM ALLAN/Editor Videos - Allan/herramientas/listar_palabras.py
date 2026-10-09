"""Lista palabras con índice y pausas (|x.x) entre dos tiempos: python herramientas/listar_palabras.py <tiempos.json> ini fin [ini fin ...]"""
import json, sys
sys.stdout.reconfigure(encoding='utf-8')
W = json.load(open(sys.argv[1], encoding='utf-8'))
r = list(map(float, sys.argv[2:]))
for a, b in zip(r[::2], r[1::2]):
    s = f'--- {a}-{b}\n'
    for k, w in enumerate(W):
        if a <= w['s'] <= b:
            g = w['s'] - W[k - 1]['e'] if k else 0
            if g > 0.35: s += f'|{g:.1f} '
            s += f"{k}:{w['w']}" + ('?' if w['score'] < 0.3 else '') + ' '
    print(s)
