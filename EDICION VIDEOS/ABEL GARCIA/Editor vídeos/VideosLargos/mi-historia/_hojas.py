"""Hojas de revisión de _extraidos/: 24 piezas por hoja, con nombre y duración (vídeos: 3 fotogramas)."""
import cv2, numpy as np, json, os
E = json.load(open('ext3.json', encoding='utf-8'))
def miniatura(e):
    p = e['archivo']
    if p.endswith('.png'): ims = [cv2.imread(p)]
    else:
        cap = cv2.VideoCapture(p); n = int(cap.get(7)); ims = []
        for k in (0.15, 0.5, 0.85):
            cap.set(1, int(n * k)); ok, f = cap.read()
            if ok: ims.append(f)
    W, H = 360, 270; t = np.full((H + 30, W, 3), 255, np.uint8); w = W // len(ims)
    for i, im in enumerate(ims):
        s = min(w / im.shape[1], H / im.shape[0]); r = cv2.resize(im, (int(im.shape[1] * s), int(im.shape[0] * s)))
        t[(H - r.shape[0]) // 2:(H - r.shape[0]) // 2 + r.shape[0], i * w + (w - r.shape[1]) // 2:i * w + (w - r.shape[1]) // 2 + r.shape[1]] = r
    lab = os.path.basename(p)[:-4] + (f"  VID {e['b'] - e['a']:.0f}s" if p.endswith('.mp4') else '')
    cv2.putText(t, lab, (4, H + 22), cv2.FONT_HERSHEY_SIMPLEX, .55, (0, 0, 200), 1)
    return t
for h in range(0, len(E), 24):
    ts = [miniatura(e) for e in E[h:h + 24]]
    while len(ts) % 6: ts.append(np.full_like(ts[0], 255))
    filas = [np.hstack(ts[i:i + 6]) for i in range(0, len(ts), 6)]
    cv2.imwrite(f'_r3_{h // 24}.jpg', np.vstack(filas), [cv2.IMWRITE_JPEG_QUALITY, 85])
print(len(E))
