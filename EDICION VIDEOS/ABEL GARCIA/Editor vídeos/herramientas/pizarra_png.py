"""Dibujo de pizarra sobre negro → PNG transparente, recortado a su contenido.
    python pizarra_png.py entrada.png salida.png
El negro pasa a transparente; las líneas y colores se conservan (se des-multiplica el color por el alfa)."""
import sys
import numpy as np
from PIL import Image


def a_png(entrada, salida, margen=12):
    g = np.asarray(Image.open(entrada).convert('RGB')).astype(np.float32)
    g = g[margen:-margen, margen:-margen]                       # bordes del modelo (a veces trae un marco fino)
    alfa = g.max(axis=2)
    alfa = np.clip((alfa - 18) / 110, 0, 1)                      # negro → transparente; trazos y colores, opacos
    color = np.where(alfa[..., None] > 0, g / np.maximum(alfa[..., None], 1e-3), 0).clip(0, 255)
    rgba = np.dstack([color, alfa * 255]).astype(np.uint8)
    ys, xs = np.nonzero(rgba[..., 3] > 25)
    rgba = rgba[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
    Image.fromarray(rgba, 'RGBA').save(salida)
    return salida


if __name__ == '__main__':
    a_png(sys.argv[1], sys.argv[2])
