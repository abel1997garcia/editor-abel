"""v3: cortes de foto de la 1.a pasada (extraidos.json) + recorte persistente de la v2; vídeos = un clip por segmento (ext2)."""
import cv2, numpy as np, json, os, shutil
exec(open('_extraer2.py', encoding='utf-8').read().split('out = []')[0].replace("os.makedirs('_ext2', exist_ok=True)", ''))
os.makedirs('_ext3', exist_ok=True)
O = [e for e in json.load(open('extraidos.json', encoding='utf-8')) if e['tipo'] == 'foto']
V2 = [e for e in json.load(open('ext2.json', encoding='utf-8')) if e['tipo'] == 'video']
out, prev = [], None
for o in O:
    pasos = list(np.arange(o['a'] + .25, o['b'] - .1, .5)) or [(o['a'] + o['b']) / 2]
    g = [frame(t) for t in pasos]
    frac = np.mean([mascara(f) for f in g], axis=0)
    c = rect(frac, .85 if len(g) > 2 else .99)
    if c is None: c = rect(frac, .6)
    if c is None: print('sin caja', o['archivo']); continue
    x0, y0, x1, y1 = c
    med = np.median(np.stack([f[y0:y1, x0:x1] for f in g]), axis=0)
    k = int(np.argmin([np.abs(f[y0:y1, x0:x1].astype(np.int16) - med).mean() for f in g]))
    im = g[k][y0 + 2:y1 - 2, x0 + 2:x1 - 2]
    v = cv2.resize(im, (32, 32)).astype(int)
    if prev is not None and abs(v - prev).mean() < 12: continue          # misma foto partida en dos
    prev = v
    out.append({'a': o['a'], 'b': o['b'], 'tipo': 'foto', 'im': im})
for e in V2: out.append({'a': e['a'], 'b': e['b'], 'tipo': 'video', 'src': e['archivo']})
out.sort(key=lambda e: e['a']); res = []
for i, e in enumerate(out):
    nom = f"_ext3/{i:03d}_{int(e['a'] // 60):02d}m{e['a'] % 60:04.1f}s"
    if e['tipo'] == 'foto': cv2.imwrite(nom + '.png', e['im']); nom += '.png'
    else: shutil.copy(e['src'], nom + '.mp4'); nom += '.mp4'
    res.append({'archivo': nom, 'a': e['a'], 'b': e['b'], 'tipo': e['tipo']})
json.dump(res, open('ext3.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(len(res), sum(r['tipo'] == 'foto' for r in res), 'fotos')
