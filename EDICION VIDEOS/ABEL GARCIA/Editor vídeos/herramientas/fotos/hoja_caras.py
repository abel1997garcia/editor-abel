"""Hojas de miniaturas numeradas para revisar a ojo.

    python hoja_caras.py refs <salida.jpg> <foto> [<foto>...]            (fotos enteras)
    python hoja_caras.py csv <caras.csv> <filtro_ruta> <salida.jpg> [min] [max_n]
        (recorte de la cara que más se parece a Abel en cada foto cuya ruta contiene el filtro;
         escribe <salida>.txt con número → ruta)
"""
import csv, sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageOps

T = 150


def abrir(p):
    im = Image.open(p)
    im = ImageOps.exif_transpose(im).convert('RGB')
    im.thumbnail((1600, 1600))
    return im


def hoja(celdas, salida, cols=8):
    filas = (len(celdas) + cols - 1) // cols
    H = Image.new('RGB', (cols * T, filas * (T + 16)), 'white')
    d = ImageDraw.Draw(H)
    for i, (im, txt) in enumerate(celdas):
        im = ImageOps.fit(im, (T, T)) if im.width and im.height else im
        x, y = (i % cols) * T, (i // cols) * (T + 16)
        H.paste(im, (x, y))
        d.text((x + 3, y + T + 2), txt, fill='black')
    H.save(salida, quality=85)


if sys.argv[1] == 'refs':
    celdas = [(abrir(p), Path(p).stem[:22]) for p in sys.argv[3:]]
    hoja(celdas, sys.argv[2], cols=6)
else:
    _, _, csvp, filtro, salida, *resto = sys.argv
    mn = float(resto[0]) if resto else 0.30
    mx = int(resto[1]) if len(resto) > 1 else 64
    filas = [r for r in csv.DictReader(open(csvp, encoding='utf-8'))
             if filtro.lower() in r['ruta'].lower() and float(r['mejor']) >= mn and int(r['w']) > 0]
    filas.sort(key=lambda r: -float(r['mejor']))
    filas = filas[:mx]
    celdas, lista = [], []
    for i, r in enumerate(filas, 1):
        im = abrir(r['ruta'])
        x, y, w, h = (int(r[k]) for k in 'xywh')
        m = int(max(w, h) * 0.6)
        cara = im.crop((max(0, x - m), max(0, y - m), x + w + m, y + h + m))
        celdas.append((cara, f"{i} · {float(r['mejor']):.2f}"))
        lista.append(f"{i}\t{r['mejor']}\t{r['ruta']}")
    hoja(celdas, salida)
    Path(salida).with_suffix('.txt').write_text('\n'.join(lista), encoding='utf-8')
    print(len(filas), 'caras')
