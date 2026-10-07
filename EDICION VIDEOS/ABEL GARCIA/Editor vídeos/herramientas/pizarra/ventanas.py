"""Ventanas de animación ancladas a frases del texto limpio -> <proyecto>/edicion/montaje.json.
    python ventanas.py <proyecto de la skill> <ventanas.json>
ventanas.json: [[id, frase de inicio, frase final, desde ~s], ...]. Cada una empieza 0,15 s antes de la 1.ª palabra y
aguanta SOSTEN s tras la última (Abel: no volver a su cara antes de 0,5–1 s). Mide el % de animación y los cambios
del primer minuto."""
import json, re, sys, unicodedata
from pathlib import Path

SOSTEN, FPS = .7, 30
norm = lambda w: re.sub(r'[^a-z0-9ñ]', '', ''.join(c for c in unicodedata.normalize('NFD', w.lower()) if unicodedata.category(c) != 'Mn'))


def buscar(W, frase, desde):
    f = [norm(x) for x in frase.split()]
    for k in range(len(W)):
        if W[k]['s'] < desde - 1: continue
        if [norm(W[k + j]['w']) for j in range(len(f)) if k + j < len(W)] == f: return k, k + len(f) - 1
    sys.exit(f'no encuentro «{frase}» desde {desde}')


if __name__ == '__main__':
    base = Path(sys.argv[1])
    VENTANAS = json.load(open(sys.argv[2], encoding='utf-8'))
    W = json.load(open(base / 'trabajo/tiempos.json', encoding='utf-8'))
    W = W['palabras'] if isinstance(W, dict) else W
    m = json.load(open(base / 'edicion/montaje.json', encoding='utf-8'))
    dur = m['planos'][-1]['f1']
    vs = []
    for id_, ini, fin, desde in VENTANAS:
        a, _ = buscar(W, ini, desde); _, b = buscar(W, fin, W[a]['s'])
        vs.append([id_, W[a]['s'] - .15, W[b]['e'] + SOSTEN])
    for k in range(len(vs) - 1): vs[k][2] = min(vs[k][2], vs[k + 1][1])          # no se pisan
    planos, f = [], 0
    for k, (id_, a, b) in enumerate(vs):
        f0, f1 = round(a * FPS), round(b * FPS)
        if f0 > f: planos.append({'tipo': 'cara', 'f0': f, 'f1': f0, 'zooms': [1.0]})
        p = {'tipo': 'anim', 'f0': max(f0, f), 'f1': f1, 'id': id_}
        if planos and planos[-1]['tipo'] == 'anim' and planos[-1]['f1'] == p['f0']: p['asentar'] = False
        planos.append(p); f = f1
    if f < dur: planos.append({'tipo': 'cara', 'f0': f, 'f1': dur, 'zooms': [1.0]})
    m['planos'] = planos
    json.dump(m, open(base / 'edicion/montaje.json', 'w', encoding='utf-8'), indent=1)
    an = sum(p['f1'] - p['f0'] for p in planos if p['tipo'] == 'anim') / FPS
    print(f'{len(vs)} animaciones · {an:.0f} s de {dur / FPS:.0f} s ({100 * an * FPS / dur:.0f} %) · '
          f'cambios en el 1.er minuto: {sum(1 for p in planos if 0 < p["f0"] < 60 * FPS)}')
    for id_, a, b in vs: print(f'  {id_:11s} {a:7.2f} – {b:7.2f}  ({b - a:4.1f} s)')
