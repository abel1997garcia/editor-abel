"""Busca a Abel en carpetas de fotos (solo LEE las carpetas de origen).

Compara cada cara (YuNet + SFace de OpenCV) con las fotos de referencia de FOTOS MIAS
y escribe un CSV con la mejor coincidencia, la fecha y la cara.

    python herramientas/fotos/escanear_caras.py <salida.csv> <carpeta> [<carpeta>...]
"""
import csv, hashlib, re, sys
from pathlib import Path
import cv2, numpy as np
from PIL import Image, ExifTags

DET = r'C:\Users\Clap\.cache\animaciones-con-voz\face_detection_yunet_2023mar.onnx'
REC = r'C:\Users\Clap\.cache\modelos_cara\face_recognition_sface_2021dec.onnx'
REFS = Path(__file__).resolve().parents[2] / 'MarcaPersonal' / 'FOTOS MIAS'
EXT = {'.jpg', '.jpeg', '.png', '.bmp'}
LADO = 1600

det = cv2.FaceDetectorYN.create(DET, '', (320, 320), 0.8)
rec = cv2.FaceRecognizerSF.create(REC, '')
TAG_FECHA = next(k for k, v in ExifTags.TAGS.items() if v == 'DateTimeOriginal')


def leer(p):
    with Image.open(p) as im:
        fecha = ''
        try:
            ex = im._getexif() or {}
            fecha = (ex.get(TAG_FECHA) or ex.get(306) or '')[:10].replace(':', '-')
        except Exception:
            pass
        im = im.convert('RGB')
        im.thumbnail((LADO, LADO))
        return cv2.cvtColor(np.array(im), cv2.COLOR_RGB2BGR), fecha


def caras(img):
    h, w = img.shape[:2]
    det.setInputSize((w, h))
    _, f = det.detect(img)
    if f is None:
        return []
    return [(c, rec.feature(rec.alignCrop(img, c))) for c in f]


def fecha_ruta(p):
    m = re.search(r'(20\d\d|19\d\d)[-_]?(\d\d)?', str(p))
    return m.group(1) if m else ''


refs = []
for p in sorted(REFS.rglob('abel_*')):
    if p.suffix.lower() not in EXT:
        continue
    img, _ = leer(p)
    cs = caras(img)
    if cs:
        c, f = max(cs, key=lambda x: x[0][2] * x[0][3])   # la cara más grande
        refs.append((p.stem, f))
print(len(refs), 'referencias', flush=True)

out = csv.writer(open(sys.argv[1], 'w', newline='', encoding='utf-8'))
out.writerow(['ruta', 'fecha_exif', 'fecha_ruta', 'n_caras', 'mejor', 'ref', 'x', 'y', 'w', 'h', 'md5'])
vistos = set()
n = 0
for carpeta in sys.argv[2:]:
    for p in sorted(Path(carpeta).rglob('*')):
        if p.suffix.lower() not in EXT or '.picasaoriginals' in p.parts:
            continue
        try:
            md5 = hashlib.md5(p.read_bytes()).hexdigest()
            if md5 in vistos:
                continue
            vistos.add(md5)
            img, fecha = leer(p)
            cs = caras(img)
        except Exception as e:
            print('error', p, e, flush=True)
            continue
        mejor, ref, caja = 0.0, '', (0, 0, 0, 0)
        for c, f in cs:
            for nombre, fr in refs:
                s = rec.match(f, fr, cv2.FaceRecognizerSF_FR_COSINE)
                if s > mejor:
                    mejor, ref, caja = s, nombre, tuple(int(v) for v in c[:4])
        out.writerow([str(p), fecha, fecha_ruta(p), len(cs), f'{mejor:.3f}', ref, *caja, md5])
        n += 1
        if n % 250 == 0:
            print(n, flush=True)
print('hecho', n, flush=True)
