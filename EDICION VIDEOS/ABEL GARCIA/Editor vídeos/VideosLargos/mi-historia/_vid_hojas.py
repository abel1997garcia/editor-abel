import cv2, numpy as np, json, os
E = [e for e in json.load(open('ext3.json', encoding='utf-8')) if e['tipo'] == 'video']
for e in E:
    cap = cv2.VideoCapture(e['archivo']); fps = cap.get(5); n = int(cap.get(7)); paso = max(1, int(fps * 1.0)); ts = []
    for i in range(0, n, paso):
        cap.set(1, i); ok, f = cap.read()
        if not ok: break
        h = 220; f = cv2.resize(f, (int(f.shape[1] * h / f.shape[0]), h))
        cv2.putText(f, f'{i / fps:.0f}s', (5, 25), cv2.FONT_HERSHEY_SIMPLEX, .8, (0, 0, 255), 2); ts.append(f)
    w = ts[0].shape[1]; por = max(1, 1800 // w)
    while len(ts) % por: ts.append(np.full_like(ts[0], 255))
    cv2.imwrite('_v_' + os.path.basename(e['archivo'])[:-4] + '.jpg', np.vstack([np.hstack(ts[i:i + por]) for i in range(0, len(ts), por)]), [cv2.IMWRITE_JPEG_QUALITY, 80])
