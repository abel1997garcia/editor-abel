"""Detecta los momentos de «Mi Historia» en que aparece una foto o un vídeo encima del plano de Abel.
Plano fijo: se compara cada fotograma (2 por segundo) con su plano «limpio» más parecido; lo que cambia mucho y de forma
rectangular es un inserto. Salida: segmentos.json [{a, b, caja, tipo: foto|video, pantalla_completa}]."""
import cv2, numpy as np, json
V = 'C:/Users/Clap/Downloads/Mi Historia.mp4'
cap = cv2.VideoCapture(V); fps = cap.get(5); n = int(cap.get(7))
paso = int(fps / 2); fr = []
for i in range(0, n, paso):
    cap.set(1, i); ok, f = cap.read()
    if not ok: break
    fr.append((i / fps, cv2.resize(f, (320, 180))))
g = np.stack([cv2.cvtColor(f, cv2.COLOR_BGR2GRAY).astype(np.int16) for _, f in fr])
# plano limpio: mediana de la mitad izquierda-centro es Abel; el fondo de la derecha (puerta) casi no cambia
ref = np.median(g[::20], axis=0).astype(np.int16)
right = (slice(15, 125), slice(205, 315))                # zona del inserto a la derecha
full = np.abs(g - ref).mean(axis=(1, 2)); rgt = np.abs(g[:, right[0], right[1]] - ref[right]).mean(axis=(1, 2))
marca = []
for k in range(len(fr)):
    pc = full[k] > 38                                     # pantalla completa (captura o clip)
    ins = (not pc) and rgt[k] > 28
    marca.append('full' if pc else 'ins' if ins else '')
segs, k = [], 0
while k < len(marca):
    if not marca[k]: k += 1; continue
    j = k
    while j + 1 < len(marca) and marca[j + 1] == marca[k]: j += 1
    a, b = fr[k][0], fr[j][0] + .5
    if b - a >= 1.0:
        # ¿foto fija o vídeo? diferencia entre fotogramas dentro del segmento, en la zona del inserto
        zona = (slice(None), slice(None)) if marca[k] == 'full' else right
        mov = np.mean([np.abs(g[x][zona] - g[x + 1][zona]).mean() for x in range(k, j)]) if j > k else 0
        segs.append({'a': round(a, 1), 'b': round(b, 1), 'pantalla_completa': marca[k] == 'full', 'mov': round(float(mov), 1)})
    k = j + 1
json.dump(segs, open('segmentos.json', 'w'), indent=1)
print(len(segs), 'segmentos')
for s in segs: print(f"{int(s['a']//60)}:{s['a']%60:04.1f}–{int(s['b']//60)}:{s['b']%60:04.1f} {'FULL' if s['pantalla_completa'] else 'ins '} mov {s['mov']}")
