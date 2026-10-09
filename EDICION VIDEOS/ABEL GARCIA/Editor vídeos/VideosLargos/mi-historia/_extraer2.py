"""Extracción v2: recorte = zona que cambia de forma PERSISTENTE (la foto), no la mano/mesa que entra y sale.
Fotos: cortes de escena dentro del segmento. Vídeos: un clip por segmento (sin sonido). -> _ext2/ + ext2.json"""
import cv2, numpy as np, json, os, subprocess
V = 'C:/Users/Clap/Downloads/Mi Historia.mp4'
cap = cv2.VideoCapture(V)
def frame(t): cap.set(0, t * 1000); return cap.read()[1]
segs = json.load(open('segmentos.json'))
libres = [t for t in np.arange(20, 3400, 37) if not any(s['a'] - 1 <= t <= s['b'] + 1 for s in segs)]
ref = np.median(np.stack([frame(t) for t in libres[:40]]), axis=0).astype(np.int16)
H, W = ref.shape[:2]
os.makedirs('_ext2', exist_ok=True)
def mascara(f): return (np.abs(f.astype(np.int16) - ref).max(axis=2) > 35)
def rect(frac, umbral):
    m = (frac >= umbral).astype(np.uint8) * 255
    m = cv2.morphologyEx(m, cv2.MORPH_OPEN, np.ones((11, 11), np.uint8))
    cs, _ = cv2.findContours(m, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not cs: return None
    x, y, w, h = cv2.boundingRect(max(cs, key=cv2.contourArea))
    # recortar filas/columnas del borde poco llenas (restos de mano)
    sub = m[y:y + h, x:x + w] > 0
    filas = np.where(sub.mean(axis=1) > .6)[0]; cols = np.where(sub.mean(axis=0) > .6)[0]
    if len(filas) < 20 or len(cols) < 20: return None
    return (x + cols[0], y + filas[0], x + cols[-1] + 1, y + filas[-1] + 1)
out = []
for s in segs:
    pasos = list(np.arange(s['a'] + .25, s['b'] - .1, .5)); fs = [frame(t) for t in pasos]
    video = s['mov'] > 4
    if s['pantalla_completa']: grupos = [(0, len(fs))]
    else:
        grupos = [(0, len(fs))]
    # cortes de escena sobre el frame completo de la zona derecha (para fotos)
    if not video and len(fs) > 3:
        sm = [cv2.resize(f, (64, 36)).astype(np.int16) for f in fs]; cortes = [0]
        for k in range(1, len(sm)):
            if np.abs(sm[k] - sm[k - 1]).mean() > 18 and np.abs(sm[min(k + 1, len(sm) - 1)] - sm[k - 1]).mean() > 18 and k - cortes[-1] >= 3: cortes.append(k)
        cortes.append(len(fs)); grupos = list(zip(cortes, cortes[1:]))
    for i0, i1 in grupos:
        g = fs[i0:i1]
        if s['pantalla_completa']: c = (0, 0, W, H)
        else:
            frac = np.mean([mascara(f) for f in g], axis=0)
            c = rect(frac, .85 if len(g) > 2 else .99)
            if c is None or (c[2] - c[0]) * (c[3] - c[1]) < .02 * W * H: continue
        a, b = pasos[i0] - .25, pasos[i1 - 1] + .25
        x0, y0, x1, y1 = c; nom = f"_ext2/{len(out):03d}_{int(a // 60):02d}m{a % 60:04.1f}s"
        if video:
            w, h = (x1 - x0 - 4) // 2 * 2, (y1 - y0 - 4) // 2 * 2
            subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', f'{a:.2f}', '-to', f'{b:.2f}', '-i', V, '-an', '-vf', f'crop={w}:{h}:{x0 + 2}:{y0 + 2}',
                            '-c:v', 'libx264', '-crf', '18', nom + '.mp4'], check=True)
            out.append({'archivo': nom + '.mp4', 'a': round(a, 1), 'b': round(b, 1), 'tipo': 'video'})
        else:
            # el fotograma más "limpio": el que más se parece a la mediana del grupo (sin mano encima)
            med = np.median(np.stack([f[y0:y1, x0:x1] for f in g]), axis=0)
            k = int(np.argmin([np.abs(f[y0:y1, x0:x1].astype(np.int16) - med).mean() for f in g]))
            cv2.imwrite(nom + '.png', g[k][y0 + 2:y1 - 2, x0 + 2:x1 - 2])
            out.append({'archivo': nom + '.png', 'a': round(a, 1), 'b': round(b, 1), 'tipo': 'foto'})
json.dump(out, open('ext2.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(len(out), 'piezas:', sum(o['tipo'] == 'foto' for o in out), 'fotos,', sum(o['tipo'] == 'video' for o in out), 'vídeos')
