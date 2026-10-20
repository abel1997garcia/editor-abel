"""Hoja de fotos ENTERAS numeradas de un año, repartidas entre sus carpetas (para elegir a ojo).

    python hoja_fotos.py <caras.csv> <año> <salida.jpg> [min=0.55] [n=30]
Escribe <salida>.txt con número → ruta.
"""
import csv, re, sys
from collections import defaultdict
from pathlib import Path
from PIL import Image, ImageDraw, ImageOps

csvp, anio, salida = sys.argv[1:4]
mn = float(sys.argv[4]) if len(sys.argv) > 4 else 0.55
n = int(sys.argv[5]) if len(sys.argv) > 5 else 30
T = 230

grupos = defaultdict(list)
for r in csv.DictReader(open(csvp, encoding='utf-8')):
    m = re.search(r'A.O (\d{4})', r['ruta'])
    y = m.group(1) if m else r['fecha_exif'][:4]
    if y == anio and float(r['mejor']) >= mn:
        grupos[str(Path(r['ruta']).parent)].append(r)
for g in grupos.values():
    g.sort(key=lambda r: -float(r['mejor']))
elegidas = []
while len(elegidas) < n and any(grupos.values()):
    for k in list(grupos):
        if grupos[k] and len(elegidas) < n:
            elegidas.append(grupos[k].pop(0))

cols = 6
H = Image.new('RGB', (cols * T, ((len(elegidas) + cols - 1) // cols) * (T + 16)), 'white')
d = ImageDraw.Draw(H)
lista = []
for i, r in enumerate(elegidas, 1):
    im = ImageOps.exif_transpose(Image.open(r['ruta'])).convert('RGB')
    im.thumbnail((T, T))
    x, y = ((i - 1) % cols) * T, ((i - 1) // cols) * (T + 16)
    H.paste(im, (x + (T - im.width) // 2, y + (T - im.height) // 2))
    d.text((x + 3, y + T + 2), f"{i} · {Path(r['ruta']).parent.name[:26]}", fill='black')
    lista.append(f"{i}\t{r['mejor']}\t{r['ruta']}")
H.save(salida, quality=85)
Path(salida).with_suffix('.txt').write_text('\n'.join(lista), encoding='utf-8')
print(len(elegidas), 'fotos de', len(grupos), 'carpetas')
