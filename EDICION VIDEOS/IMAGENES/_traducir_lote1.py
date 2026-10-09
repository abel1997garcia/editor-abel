"""Traduce al español el texto de las imágenes de la biblioteca: tapa cada texto con el color de su fondo y escribe la
traducción en Montserrat (su tipografía de marca), ajustando el tamaño al hueco. Los esquemas que son casi solo texto se
rehacen enteros (más limpios y a más resolución)."""
import numpy as np
from PIL import Image, ImageDraw, ImageFont

FV = 'C:/Users/Clap/Desktop/EDICION VIDEOS/ABEL GARCIA/Editor vídeos/herramientas/tablero/Montserrat-Variable.ttf'
def fuente(tam, peso=700):
    f = ImageFont.truetype(FV, tam)
    try: f.set_variation_by_axes([peso])
    except Exception: pass
    return f

def fondo(im, caja):
    x0, y0, x1, y1 = caja; a = np.asarray(im.convert('RGB')).astype(int)
    borde = np.concatenate([a[max(0, y0 - 3):y0, x0:x1].reshape(-1, 3), a[y1:y1 + 3, x0:x1].reshape(-1, 3),
                            a[y0:y1, max(0, x0 - 3):x0].reshape(-1, 3), a[y0:y1, x1:x1 + 3].reshape(-1, 3)])
    return tuple(int(v) for v in np.median(borde, 0))

def poner(im, caja, lineas, color=(17, 17, 17), peso=700, max_tam=200, tapar=True, alin='c'):
    d = ImageDraw.Draw(im); x0, y0, x1, y1 = caja
    if tapar: d.rectangle(caja, fill=fondo(im, caja))
    lineas = lineas if isinstance(lineas, list) else [lineas]
    tam = max_tam
    while tam > 8:                                     # el mayor tamaño que cabe en el hueco
        f = fuente(tam, peso); alto = tam * 1.18 * len(lineas)
        if max(d.textlength(l, font=f) for l in lineas) <= (x1 - x0) * .96 and alto <= (y1 - y0) * 1.02: break
        tam -= 1
    f = fuente(tam, peso); y = (y0 + y1) / 2 - tam * 1.18 * len(lineas) / 2
    for l in lineas:
        w = d.textlength(l, font=f); x = (x0 + x1 - w) / 2 if alin == 'c' else x0
        d.text((x, y), l, font=f, fill=color); y += tam * 1.18
    return im

def editar(ruta, cambios):
    im = Image.open(ruta).convert('RGB')
    for c in cambios: poner(im, *c[:2], **(c[2] if len(c) > 2 else {}))
    im.save(ruta)

BLANCO, NEGRO = (255, 255, 255), (17, 17, 17)
editar('miedo-amor/miedo_amor_toroide.png', [((80, 175, 300, 265), 'Miedo', {'color': BLANCO}), ((800, 25, 1080, 115), 'AMOR', {'color': BLANCO})])
editar('frecuencia-vibracion/bateria_energia_vs_burnout.png', [
    ((40, 545, 640, 805), ['GESTIONAR TU ENERGÍA', 'CON INTENCIÓN', '', 'PROGRESO SOSTENIBLE'], {'peso': 800}),
    ((790, 545, 1280, 805), ['RESPONDER', 'A TODO', '', 'AGOTAMIENTO'], {'peso': 800})])
editar('tarot/el_mago.png', [((60, 1118, 668, 1195), 'EL MAGO', {'peso': 800})])
editar('elementos/cinco_elementos.png', [
    ((180, 0, 860, 48), 'LOS CINCO ELEMENTOS', {'peso': 900}),
    ((0, 85, 112, 118), ''), ((0, 245, 96, 276), ''), ((0, 405, 112, 440), ''), ((0, 588, 106, 622), ''), ((0, 758, 110, 792), ''), ((0, 908, 118, 945), ''),
    ((262, 82, 372, 116), 'ESPÍRITU', {'peso': 800}), ((262, 407, 372, 441), 'ESPÍRITU', {'peso': 800}),
    ((280, 590, 380, 620), 'AIRE', {'peso': 800}), ((270, 760, 380, 790), 'FUEGO', {'peso': 800}), ((262, 912, 375, 945), 'AGUA', {'peso': 800}),
    ((530, 878, 790, 908), 'CADUCEO DE HERMES', {'peso': 800})])
editar('manifestacion/proceso_creacion_cabeza.png', [
    ((290, 72, 760, 178), ['El proceso interno', 'de creación'], {'peso': 800}),
    ((262, 180, 775, 288), ['Génesis 1:2', '«La tierra estaba desordenada y vacía,', 'las tinieblas cubrían el abismo y el Espíritu', 'de Dios se movía sobre las aguas.»'], {'peso': 700}),
    ((800, 85, 1325, 138), 'El proceso externo de creación', {'peso': 800}),
    ((820, 142, 1300, 258), ['Génesis 1:3 «Sea la luz»', 'Juan 1:1 «En el principio era el Verbo,', 'y el Verbo era con Dios, y el Verbo era Dios.»'], {'peso': 700}),
    ((808, 325, 1125, 405), ['Fuego: voluntad, libido,', 'vitalidad, impulso del CHI'], {'peso': 600, 'color': (140, 60, 90)}),
    ((10, 500, 215, 565), 'ÉTER', {'peso': 800}),
    ((298, 598, 537, 690), ['AGUA: subconsciente,', 'emoción, memoria,', 'receptividad, intuición'], {'peso': 600, 'color': (40, 40, 90)}),
    ((562, 596, 796, 695), ['Aire: consciente,', 'pensamiento, razón,', 'imaginación'], {'peso': 600, 'color': (60, 60, 60)}),
    ((1095, 606, 1300, 805), ['Tierra: receptiva,', 'material,', 'enraizamiento,', 'organización,', 'materialización,', 'fertilidad'], {'peso': 600, 'color': (40, 110, 80)}),
    ((55, 1055, 275, 1105), '')])

# esquemas de solo texto: rehechos enteros en español (1200 px de ancho, fondo blanco)
def lienzo(w, h, color=(255, 255, 255)): im = Image.new('RGB', (w, h), color); return im, ImageDraw.Draw(im)
def centrado(d, x, y, txt, tam, peso=700, color=NEGRO):
    f = fuente(tam, peso); w = d.textlength(txt, font=f); d.text((x - w / 2, y), txt, font=f, fill=color)
def flecha_abajo(d, x, y0, y1, color):
    d.line([(x, y0), (x, y1)], fill=color, width=10); d.polygon([(x - 22, y1 - 18), (x + 22, y1 - 18), (x, y1 + 14)], fill=color)

im, d = lienzo(1200, 1030)
centrado(d, 600, 40, 'Solo hay dos tipos de pensamiento', 62, 800)
R, V = (200, 30, 50), (40, 170, 90)
for x, items, col in [(330, ['Ilusiones', 'locura, sin sentido', 'Separación', 'Ego'], R), (870, ['Verdades', 'sabiduría, iluminación', 'UNIDAD', 'Divino'], V)]:
    y = 150
    for i, t in enumerate(items):
        flecha_abajo(d, x, y, y + 70, col); y += 100
        centrado(d, x, y, t, 50 if i % 2 == 0 else 42, 800 if i % 2 == 0 else 600); y += 95
im.save('miedo-amor/dos_tipos_de_pensamiento.png')

im, d = lienzo(1200, 1030, (250, 248, 246))
centrado(d, 600, 50, 'LAS LEYES HERMÉTICAS UNIVERSALES', 34, 600, (110, 110, 110)); d.line([(80, 72), (250, 72)], fill=(150, 150, 150), width=3); d.line([(950, 72), (1120, 72)], fill=(150, 150, 150), width=3)
centrado(d, 600, 170, 'La ley del', 96, 800); centrado(d, 600, 285, 'Mentalismo', 96, 800)
centrado(d, 600, 470, 'Todo es Mente.', 58, 500); centrado(d, 600, 545, 'El Universo es mental.', 58, 500)
for i, l in enumerate(['Todo lo que vemos y vivimos en el mundo físico', 'tiene su origen en el plano invisible, mental.',
                       'Nos dice que hay una única Conciencia Universal,', 'la Mente Universal, de la que todo se manifiesta.']):
    centrado(d, 600, 720 + i * 62, l, 36, 500, (60, 60, 60))
im.save('leyes-hermeticas/ley_del_mentalismo.png')

im, d = lienzo(1400, 820, (247, 245, 238))
centrado(d, 700, 40, 'Unidad', 60, 800); centrado(d, 700, 115, 'Amor', 60, 800); centrado(d, 700, 190, 'Creación consciente', 60, 800)
centrado(d, 360, 300, 'Femenino (madre divina)', 46, 700, (60, 160, 220)); centrado(d, 1040, 300, 'Masculino (padre divino)', 46, 700, (210, 50, 60))
d.line([(470, 380), (700, 480)], fill=NEGRO, width=5); d.line([(930, 380), (700, 480)], fill=NEGRO, width=5)
d.arc([180, 480, 1220, 1520], 180, 360, fill=NEGRO, width=14); d.line([(700, 480), (700, 820)], fill=NEGRO, width=8)
for i, (a, b) in enumerate(zip(['Corazón / emociones', 'Colectivo', 'Fuerza creativa', 'Intuición', 'Fluir', 'Subconsciente', 'Interno'],
                               ['Lógica', 'Identidad / ego', 'Protección', 'Voluntad / acción', 'Orden / estructura', 'Consciente', 'Externo'])):
    centrado(d, 545, 580 + i * 34, a, 26, 700); centrado(d, 855, 580 + i * 34, b, 26, 700)
im.save('masculino-femenino/unidad_masculino_femenino.png')
print('traducidas')
