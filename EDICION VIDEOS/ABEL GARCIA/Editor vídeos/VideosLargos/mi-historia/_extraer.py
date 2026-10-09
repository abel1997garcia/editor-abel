"""Extrae cada foto/vídeo insertado en «Mi Historia» (segmentos.json) -> _extraidos/ (fotos .png, clips .mp4 sin sonido)."""
import cv2, numpy as np, json, os, subprocess
V = 'C:/Users/Clap/Downloads/Mi Historia.mp4'
cap = cv2.VideoCapture(V); fps = cap.get(5)
def frame(t): cap.set(0, t * 1000); return cap.read()[1]
# plano limpio de referencia (mediana de momentos sin insertos)
segs = json.load(open('segmentos.json'))
libres = [t for t in np.arange(20, 3400, 37) if not any(s['a'] - 1 <= t <= s['b'] + 1 for s in segs)]
ref = np.median(np.stack([frame(t) for t in libres[:40]]), axis=0).astype(np.int16)
os.makedirs('_extraidos', exist_ok=True)
def caja(f):
    d = np.abs(f.astype(np.int16) - ref).max(axis=2); m = (d > 40).astype(np.uint8) * 255
    m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, np.ones((15, 15), np.uint8)); m = cv2.morphologyEx(m, cv2.MORPH_OPEN, np.ones((9, 9), np.uint8))
    cs, _ = cv2.findContours(m, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not cs: return None
    x, y, w, h = cv2.boundingRect(max(cs, key=cv2.contourArea)); return (x, y, x + w, y + h)
def ahash(im): s = cv2.resize(cv2.cvtColor(im, cv2.COLOR_BGR2GRAY), (16, 16)); return s > s.mean()
items = []
for s in segs:
    H, W = ref.shape[:2]
    pasos = list(np.arange(s['a'] + .25, s['b'] - .1, .5))
    fs = [frame(t) for t in pasos]
    if s['pantalla_completa']: c = (0, 0, W, H)
    else:
        cs = [caja(f) for f in fs]; cs = [x for x in cs if x and (x[2] - x[0]) * (x[3] - x[1]) > 0.02 * W * H]
        if not cs: continue
        c = tuple(int(np.median([x[i] for x in cs])) for i in range(4))          # recuadro fijo del momento
    crops = [cv2.resize(f[c[1]:c[3], c[0]:c[2]], (64, 48)).astype(np.int16) for f in fs]
    # cortes de escena: cambio grande y sostenido del contenido (no la mano que pasa)
    cortes = [0]
    for k in range(1, len(crops)):
        d1 = np.abs(crops[k] - crops[k - 1]).mean()
        d2 = np.abs(crops[min(k + 1, len(crops) - 1)] - crops[k - 1]).mean()
        if d1 > 35 and d2 > 35 and pasos[k] - pasos[cortes[-1]] >= 1.5: cortes.append(k)
    cortes.append(len(pasos))
    for i0, i1 in zip(cortes, cortes[1:]):
        items.append({'t': pasos[i0], 'b': pasos[i1 - 1] + .5, 'c': c, 'mov': s['mov'], 'full': s['pantalla_completa']})
out = []
for k, it in enumerate(items):
    a, b, (x0, y0, x1, y1) = it['t'] - .25, it['b'], it['c']
    nom = f'_extraidos/{k:03d}_{int(a // 60):02d}m{a % 60:04.1f}s'
    movido = it['mov'] > 4
    if movido:
        w, h = (x1 - x0) // 2 * 2, (y1 - y0) // 2 * 2
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', f'{a:.2f}', '-to', f'{b:.2f}', '-i', V, '-an', '-vf', f'crop={w}:{h}:{x0}:{y0}',
                        '-c:v', 'libx264', '-crf', '18', nom + '.mp4'], check=True)
        out.append({'archivo': nom + '.mp4', 'a': round(a, 1), 'b': round(b, 1), 'tipo': 'video'})
    else:
        f = frame((a + b) / 2); cv2.imwrite(nom + '.png', f[y0 + 2:y1 - 2, x0 + 2:x1 - 2])
        out.append({'archivo': nom + '.png', 'a': round(a, 1), 'b': round(b, 1), 'tipo': 'foto'})
json.dump(out, open('extraidos.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(len(out), 'piezas:', sum(o['tipo'] == 'foto' for o in out), 'fotos,', sum(o['tipo'] == 'video' for o in out), 'vídeos')
