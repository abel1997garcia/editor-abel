"""Hoja de fotos ENTERAS numeradas por filtro (para elegir a ojo).

    python hoja_filtro.py <caras.csv> <salida.jpg> <filtros_ruta separados por |> [min=0.55] [n=36] [solo=0]
    solo=1 → solo fotos con una única cara (él solo).
Escribe <salida>.txt con número → ruta.
"""
import csv, sys
from collections import defaultdict
from pathlib import Path
from PIL import Image, ImageDraw, ImageOps

csvp, salida, filtros = sys.argv[1:4]
mn = float(sys.argv[4]) if len(sys.argv) > 4 else 0.55
n = int(sys.argv[5]) if len(sys.argv) > 5 else 36
solo = len(sys.argv) > 6 and sys.argv[6] == '1'
fs = [f.lower() for f in filtros.split('|') if f]
T = 230

grupos = defaultdict(list)
for r in csv.DictReader(open(csvp, encoding='utf-8')):
    if fs and not any(f in r['ruta'].lower() for f in fs):
        continue
    if float(r['mejor']) < mn or (solo and r['n_caras'] != '1'):
        continue
    grupos[str(Path(r['ruta']).parent)].append(r)
for g in grupos.values():
    g.sort(key=lambda r: -float(r['mejor']))
elegidas = []
while len(elegidas) < n and any(grupos.values()):
    for k in list(grupos):
        if grupos[k] and len(elegidas) < n:
            elegidas.append(grupos[k].pop(0))

cols = 6
H = Image.new('RGB', (cols * T, max(1, (len(elegidas) + cols - 1) // cols) * (T + 16)), 'white')
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
