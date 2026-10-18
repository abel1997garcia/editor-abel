"""Casa el guion (escenas) con la transcripción de la voz y calcula los tiempos reales.
Uso: python3 -I alinear.py escenas.json voz.json salida.json
- Cada palabra del guion recibe el instante en que Allan la dice.
- Tras la escena 'pasos' se abre un hueco para el vídeo de sesiones ('prueba')."""
import json, re, sys, unicodedata, difflib

esc, voz, out = sys.argv[1:4]
CON = (sys.argv[4] if len(sys.argv) > 4 else 'con') == 'con'
scenes = json.load(open(esc))['scenes']
tw = json.load(open(voz))['words']

def words(s): return [w for w in re.sub(r'\(.*?\)', '', s).split() if w]
def norm(w):
    w = unicodedata.normalize('NFD', w.lower())
    return re.sub(r'[^a-z0-9ñ]', '', ''.join(c for c in w if unicodedata.category(c) != 'Mn'))

# guion plano
flat = []
for si, sc in enumerate(scenes):
    if sc['layout'] in ('video',): continue
    for wi, w in enumerate(words(sc['voz'])): flat.append((si, wi, norm(w)))
a = [x[2] for x in flat]; b = [norm(w['w']) for w in tw]
sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
t0 = [None] * len(a); t1 = [None] * len(a)
for blk in sm.get_matching_blocks():
    for k in range(blk.size): t0[blk.a + k] = tw[blk.b + k]['t0']; t1[blk.a + k] = tw[blk.b + k]['t1']
# palabras casi iguales que no casaron (p. ej. "cog"/"coge"): emparejar dentro de huecos
for tag, i1, i2, j1, j2 in sm.get_opcodes():
    if tag == 'replace':
        for k in range(min(i2 - i1, j2 - j1)):
            if difflib.SequenceMatcher(None, a[i1 + k], b[j1 + k]).ratio() > .6:
                t0[i1 + k] = tw[j1 + k]['t0']; t1[i1 + k] = tw[j1 + k]['t1']
matched = sum(x is not None for x in t0)
# interpolar las que falten
idx = [i for i, x in enumerate(t0) if x is not None]
for i in range(len(a)):
    if t0[i] is None:
        p = max([j for j in idx if j < i], default=None); n = min([j for j in idx if j > i], default=None)
        if p is None: t0[i] = t0[n] - .3 * (n - i)
        elif n is None: t0[i] = t1[p] + .3 * (i - p)
        else: t0[i] = t1[p] + (t0[n] - t1[p]) * (i - p) / (n - p)
        t1[i] = t0[i] + .25

LEAD = round(1.6 - t0[0], 3)              # primera palabra a los 1,6 s del vídeo
pos = {(si, wi): k for k, (si, wi, _) in enumerate(flat)}
def first(si): return pos[(si, 0)]
def last(si): return max(k for (s, w), k in pos.items() if s == si)
ids = [sc['id'] for sc in scenes]
ip, ipr, ilogo = ids.index('pasos'), ids.index('prueba'), ids.index('logo')
cutV = t1[last(ip)] + .45                 # en tiempo del archivo de voz
pr = scenes[ipr]
durs = [4.466, 9.933, 11.333]; PAD, GAP = .8, .6
V = PAD * 2 + sum(durs) + GAP * (len(durs) - 1) if CON else 0
T = lambda v: round(v + LEAD + (V if v > cutV else 0), 3)

res = {}
order = [i for i in range(len(scenes)) if i != ipr]
for n, si in enumerate(order):
    st = T(t0[first(si)]) - .35
    res[ids[si]] = {'t0': round(st, 3), 'palabras': [T(t0[pos[(si, wi)]]) for wi in range(len(words(scenes[si]['voz'])))]}
for n, si in enumerate(order):
    nxt = order[n + 1] if n + 1 < len(order) else None
    if si == ip and CON: res[ids[si]]['t1'] = T(cutV - 1e-3) + .0
    elif si == ilogo: res[ids[si]]['t0'] = round(T(t0[first(si)]) - .4, 3); res[ids[si]]['t1'] = round(res[ids[si]]['t0'] + 6, 3)
    elif nxt is not None: res[ids[si]]['t1'] = res[ids[nxt]]['t0']
pst = round(cutV + LEAD, 3)
if CON:
    res['prueba'] = {'t0': pst, 't1': round(pst + V, 3), 'palabras': []}
    res[ids[order[order.index(ipr - 1) + 1]]]['t0'] = max(res[ids[order[order.index(ipr - 1) + 1]]]['t0'], res['prueba']['t1'])
clip_starts = []; c = pst + PAD
for d in durs: clip_starts.append(round(c, 3)); c += d + GAP
plan = {'CON_PRUEBA': CON, 'LEAD': LEAD, 'cutV': round(cutV, 3), 'V': round(V, 3), 'clip_starts': clip_starts, 'durs': durs,
        'DUR': round(res['logo']['t1'] + .6, 3)}
json.dump({'tiempos': res, 'plan': plan}, open(out, 'w'), ensure_ascii=False, indent=1)
print(f'casadas {matched}/{len(a)} palabras · duración {plan["DUR"]:.1f}s · plan {plan}')
for i in [x for x in ids if x in res]: print(f"  {res[i]['t0']:7.2f}-{res[i]['t1']:7.2f} {i}")
