"""Mejora de imagen COMÚN a todos los reels (Abel 16/10/2026: «aplícales el mismo filtro de color, enfoque o nitidez que a estos…
tanto si son oscuros o blancos, se compensarán un poco»): el toque de nitidez de los reels TAB (unsharp suave + contraste 1,03) y
una compensación SUAVE de luz según lo oscura o clara que sea la grabación (gamma, que no quema los blancos ni empasta los negros).

    from mejora_imagen import filtro;  filtro(fuente) -> "unsharp=…,eq=contrast=1.03:gamma=…"   (para añadir a la cadena -vf)
    python mejora_imagen.py <vídeo> ...  -> luz media y el filtro que le tocaría
"""
import sys
from functools import lru_cache
from pathlib import Path

OBJETIVO = 112          # luz media de la CARA (Y, 0-255) en las grabaciones de la tablet que Abel dio por buenas (16/10/2026: 110-111)
NITIDEZ = 'unsharp=5:5:0.5:5:5:0.0'


@lru_cache(None)
def luz(fuente, zona=None):
    """luz media de la CARA (Y, 0-255) en ~16 fotogramas repartidos por el vídeo: el fondo blanco de los horizontales o la plantilla
    de la tablet no cuentan (si no, un vídeo con pared blanca parecía «muy claro» y se oscurecía). zona se ignora (compatibilidad)."""
    import os; os.environ.setdefault("OPENCV_LOG_LEVEL", "ERROR"); import cv2
    sys.path.insert(0, str(Path.home() / '.claude/skills/animaciones-horizontal-combinadas/scripts'))
    from cortar import modelo_cara
    cap = cv2.VideoCapture(str(fuente)); n = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    w, h = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    det = cv2.FaceDetectorYN.create(str(modelo_cara()), '', (w, h), 0.7, 0.3, 5); ys = []
    for k in range(16):
        cap.set(cv2.CAP_PROP_POS_FRAMES, int(n * (k + .5) / 16)); ok, f = cap.read()
        if not ok: continue
        _, c = det.detect(f)
        if c is None or not len(c): continue
        x, y, cw, ch = [int(v) for v in max(c, key=lambda q: q[2] * q[3])[:4]]
        cara = f[max(0, y + ch // 5):y + ch * 4 // 5, max(0, x + cw // 5):x + cw * 4 // 5]   # el centro de la cara (sin pelo ni fondo)
        if cara.size: ys.append(float(cv2.cvtColor(cara, cv2.COLOR_BGR2YUV)[:, :, 0].mean()))
    ys.sort(); return ys[len(ys) // 2] if ys else OBJETIVO


def filtro(fuente, zona=None, horizontal=False):
    """horizontal=True: reels sacados de los vídeos HORIZONTALES (plano más cerca = imagen ampliada): capa reforzada de nitidez,
    contraste 1,06 y saturación 1,08 (Abel 19/10/2026: «aplicar una capa de mejora visual de nitidez, algo de contraste»)"""
    y = luz(str(fuente), tuple(zona) if zona else None)
    gamma = min(1.10, max(.95, (OBJETIVO / max(y, 1)) ** .5))            # solo la MITAD del camino hasta el objetivo: compensa, no transforma
    if horizontal: return f'unsharp=5:5:0.9:5:5:0.0,eq=contrast=1.06:saturation=1.08:gamma={gamma:.3f}'
    return f'{NITIDEZ},eq=contrast=1.03:gamma={gamma:.3f}'


if __name__ == '__main__':
    for v in sys.argv[1:]: print(f'{luz(v):6.1f}  {filtro(v)}  {v}')
