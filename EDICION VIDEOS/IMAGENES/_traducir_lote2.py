"""Lote 2 (5 vídeos del 08/10): traducción al español. Reutiliza las funciones del lote 1."""
import os, math
os.chdir(os.path.dirname(os.path.abspath(__file__)))
src = open('_traducir_lote1.py', encoding='utf-8').read()
exec(src.split("BLANCO, NEGRO = (255, 255, 255), (17, 17, 17)")[0])
BLANCO, NEGRO = (255, 255, 255), (17, 17, 17)
exec(src[src.index("def lienzo"):src.index("im, d = lienzo(1200, 1030)")])
from PIL import Image, ImageDraw
BLANCO, NEGRO = (255, 255, 255), (17, 17, 17)

im0 = Image.open('_originales/mitologia__pluton_grabado.png') if False else None
from PIL import ImageDraw as _D
_p = Image.open('mitologia/pluton_grabado.png').convert('RGB'); _D.Draw(_p).rectangle((293, 1071, 679, 1144), fill=(250, 250, 250)); _p.save('mitologia/pluton_grabado.png')
editar('mitologia/pluton_grabado.png', [((293, 1071, 679, 1144), 'PLUTÓN', {'peso': 700, 'tapar': False})])
editar('masculino-femenino/dios_prisma_subconsciente.png', [
    ((31, 212, 300, 324), 'DIOS', {'peso': 900}),
    ((187, 50, 835, 212), ['Mente subconsciente', '(femenina)'], {'peso': 800}),
    ((760, 424, 1290, 660), ['Reino dual', '(mente consciente,', 'masculina)'], {'peso': 800})])
editar('mitologia/tradiciones_antiguas_collage.png', [
    ((30, 412, 310, 458), 'BABILONIA', {'peso': 800}), ((440, 412, 650, 458), 'HINDÚ', {'peso': 800, 'color': BLANCO}),
    ((800, 412, 985, 458), 'MAYA', {'peso': 800}), ((50, 962, 290, 1005), 'EGIPTO', {'peso': 800, 'color': BLANCO}),
    ((745, 962, 995, 1005), 'CRISTIANISMO', {'peso': 800, 'color': BLANCO}),
    ((368, 548, 452, 592), ['SOL', 'MASCULINO'], {'peso': 800}), ((612, 548, 710, 592), ['LUNA', 'FEMENINO'], {'peso': 800})])
editar('cotidiano-bocetos/networking_oficina.png', [((285, 36, 512, 62), 'ESTRATEGIAS DE CONTACTO', {'peso': 700, 'color': (70, 70, 70)})])

# espíritu – cuerpo – alma
im, d = lienzo(1000, 1000)
d.line([(500, 170), (130, 860), (870, 860), (500, 170)], fill=NEGRO, width=6)
centrado(d, 500, 60, 'Espíritu', 80, 500); centrado(d, 190, 880, 'Cuerpo', 80, 500); centrado(d, 830, 880, 'Alma', 80, 500)
im.save('centros-energeticos/espiritu_cuerpo_alma.png')

# polaridades femenino / masculino
im, d = lienzo(1600, 1000)
cx1, cx2, cy = 690, 910, 520
for k in range(1, 5):
    r = 55 * k
    d.ellipse([800 - r * 2.2, cy - r, 800 + r * 2.2, cy + r], outline=(150, 150, 150), width=3)
d.ellipse([cx1 - 34, cy - 34, cx1 + 34, cy + 34], fill=(40, 90, 220)); d.ellipse([cx2 - 34, cy - 34, cx2 + 34, cy + 34], fill=(220, 40, 50))
centrado(d, 800, 40, 'ESTAS SON POLARIDADES, NO OPUESTOS', 52, 800)
for i, t in enumerate(['FEMENINO', 'EMOCIÓN', 'CREATIVIDAD', 'AGUA', 'MAGNETISMO']):
    centrado(d, 210, 230 + i * 130, t, 46, 800, (40, 90, 220))
for i, t in enumerate(['MASCULINO', 'LÓGICA', 'CIENCIA', 'FUEGO', 'ELECTRICIDAD']):
    centrado(d, 1390, 230 + i * 130, t, 46, 800, (220, 40, 50))
im.save('masculino-femenino/polaridades_masculino_femenino.png')

# dualidad de la polaridad (yin-yang)
im, d = lienzo(1200, 1000)
centrado(d, 600, 40, 'La dualidad de la polaridad', 72, 700)
cx, cy, r = 600, 480, 260
d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=BLANCO, outline=NEGRO, width=6)
d.pieslice([cx - r, cy - r, cx + r, cy + r], 270, 90, fill=NEGRO)
d.ellipse([cx - r / 2, cy - r, cx + r / 2, cy], fill=NEGRO); d.ellipse([cx - r / 2, cy, cx + r / 2, cy + r], fill=BLANCO)
d.ellipse([cx - 30, cy - r / 2 - 30, cx + 30, cy - r / 2 + 30], fill=BLANCO); d.ellipse([cx - 30, cy + r / 2 - 30, cx + 30, cy + r / 2 + 30], fill=NEGRO)
centrado(d, 230, 450, 'YANG', 56, 800); centrado(d, 970, 450, 'YIN', 56, 800)
for i, l in enumerate(['«El género está en todo; todo tiene', 'sus principios masculino y femenino;', 'el género se manifiesta en todos los planos.»']):
    centrado(d, 600, 790 + i * 58, l, 40, 500)
im.save('masculino-femenino/dualidad_polaridad_yin_yang.png')

# la realidad es el presente
im, d = lienzo(1200, 1100)
centrado(d, 600, 40, 'REALIDAD', 60, 800); centrado(d, 600, 115, '(el momento presente)', 44, 500)
d.line([(120, 330), (1080, 820)], fill=(60, 60, 60), width=4); d.line([(1080, 330), (120, 820)], fill=(60, 60, 60), width=4)
d.ellipse([440, 420, 760, 730], outline=NEGRO, width=8); centrado(d, 600, 540, 'mente', 50, 700)
centrado(d, 220, 520, 'La percepción', 40, 600); centrado(d, 220, 570, 'del pasado', 40, 600)
centrado(d, 980, 520, 'Percepción', 40, 600); centrado(d, 980, 570, 'de la realidad', 40, 600)
d.line([(330, 780), (240, 680)], fill=(210, 40, 50), width=10); d.polygon([(220, 660), (275, 680), (245, 715)], fill=(210, 40, 50))
d.line([(870, 780), (960, 680)], fill=(210, 40, 50), width=10); d.polygon([(980, 660), (925, 680), (955, 715)], fill=(210, 40, 50))
centrado(d, 600, 920, 'La ilusión del tiempo', 46, 700); centrado(d, 600, 985, '(donde vive la mente consciente)', 40, 500)
im.save('sombra-inconsciente/realidad_presente_tiempo.png')

# mapa de la psique (Jung)
im, d = lienzo(1100, 1100)
centrado(d, 550, 30, 'MUNDO EXTERIOR', 46, 700); centrado(d, 550, 1030, 'MUNDO INTERIOR', 46, 700)
d.ellipse([150, 120, 950, 600], outline=NEGRO, width=5); d.ellipse([150, 500, 950, 980], outline=NEGRO, width=5)
d.rectangle([330, 470, 770, 560], fill=BLANCO)
for i, (t, tam) in enumerate([('PERSONA', 46), ('EGO', 50), ('SÍ MISMO', 74), ('SOMBRA', 50), ('ÁNIMUS · ÁNIMA', 44)]):
    centrado(d, 550, [230, 360, 510, 700, 830][i], t, tam, 800 if t == 'SÍ MISMO' else 600)
centrado(d, 110, 520, 'Personal', 36, 500); centrado(d, 990, 520, 'Inconsciente', 36, 500)
centrado(d, 260, 330, 'Consciencia', 32, 500, (90, 90, 90)); centrado(d, 840, 330, 'Consciencia', 32, 500, (90, 90, 90))
centrado(d, 260, 760, 'Colectivo', 32, 500, (90, 90, 90)); centrado(d, 840, 760, 'Inconsciente', 32, 500, (90, 90, 90))
im.save('sombra-inconsciente/psique_jung_self.png')
print('ok')
