"""Añade a cada foto de FOTOS MIAS/catalogo.json su edad, año, época, emoción y para qué ángulos de carrusel sirve.

Abel nació en 1997. Ángulos = los de la guía de carruseles (sección 2b):
por_edades · frase_repetida · yo_pequeno · creencia · historia_completa · fracaso_cifra · antes_ahora · lista_vida · mentalidad · venta
"""
import json
from pathlib import Path

CAT = Path(__file__).resolve().parents[2] / 'MarcaPersonal' / 'FOTOS MIAS' / 'catalogo.json'

# carpeta → (edad, año, época, emoción, ángulos)
EPOCA = {
    '01-infancia': ('niño (≈2-11)', '1999-2008', 'infancia en Boñar (León) y llegada a Castelldans; separación de sus padres con 7, juez con 10, muerte de su abuelo con 12', 'inocencia; refugio en su burbuja', ['por_edades', 'yo_pequeno', 'frase_repetida']),
    '01b-adolescencia': ('12-16', '2009-2013', 'ESO en Castelldans/Borges: rabia, Call of Duty, fútbol muy autoexigente', 'rabia, autoexigencia, no encajar', ['por_edades', 'yo_pequeno', 'frase_repetida', 'creencia']),
    '01c-canal-packard-minecraft': ('15', '2012', 'su primer canal, Packard Minecraft: su burbuja para no sentir', 'evasión', ['por_edades', 'yo_pequeno']),
    '02-antes-de-despertar': ('16-22', '2013-2020', 'fiesta, alcohol, apuestas online; relación tóxica; psicólogos que no le sirvieron; ADE y la oficina', 'tapar el vacío', ['por_edades', 'frase_repetida', 'creencia', 'historia_completa']),
    '03-canal-gael-blog': ('≈19-20', '2017', 'Gael Blog: blogs de crecimiento personal saliendo él; lo pusieron en la tele de un bar del pueblo y «no supo sostenerlo»', 'vergüenza, miedo a la crítica', ['por_edades', 'historia_completa', 'creencia']),
    '04-canal-clap': ('23', '2020-2021', 'pandemia: canal Clap de Clash Royale, un vídeo al día, 30.000 suscriptores y ≈200 €/mes', 'esfuerzo sin resultado', ['por_edades', 'historia_completa', 'fracaso_cifra']),
    '05-canal-automatizacion-ganaba-dinero': ('≈24-25', '2021-2022', 'el canal de automatización SIN salir él: 17.000 €/mes, viajes, rechazó 550.000 €; por dentro no se sentía suficiente', 'tenerlo todo fuera y nada dentro', ['creencia', 'historia_completa', 'frase_repetida', 'antes_ahora']),
    '06-noche-oscura-26-anos': ('26', '2023', 'la caída: le cierran todas las cuentas de YouTube, debe 3.500 € a Hacienda, rompe con su pareja: su noche oscura del alma', 'derrumbe, vacío', ['por_edades', 'fracaso_cifra', 'frase_repetida', 'historia_completa', 'antes_ahora']),
    '07-trabajo-monitor': ('joven (≈16-21)', '', 'trabajos de joven: monitor de la campaña de Navidad', 'trabajar para pagar la fiesta', ['por_edades', 'lista_vida']),
    '08-australia': ('26-27', '2023-2024', 'Australia (Brisbane), solo y sin inglés: hostal, trabajos duros (teles de 70 kg, obrero, camarero, Uber), moto de 50 cc; reconstruirse desde dentro', 'humildad, libertad, empezar de cero', ['por_edades', 'antes_ahora', 'lista_vida', 'mentalidad', 'historia_completa']),
    '09-sudeste-asiatico': ('27', '2024', 'mes y medio viajando solo por el sudeste asiático y Turquía', 'libertad, conocer gente', ['lista_vida', 'antes_ahora']),
    '10-segundo-fondo-y-sanacion': ('≈28', '2025', 'Lérida: segundo fondo en el piso donde se independizó, y la sanación (Allan, psilocibina)', 'tocar fondo otra vez y sanar', ['por_edades', 'frase_repetida', 'yo_pequeno', 'historia_completa']),
    '11-ahora': ('29', '2026', 'hoy en Lérida: su canal, la pizarra, el gimnasio, Club Unidad', 'en paz consigo mismo', ['antes_ahora', 'mentalidad', 'venta', 'yo_pequeno']),
    '12-familia-no-reels': ('varias', '', 'familia (en reels NO; en carruseles sí)', 'vínculo', ['por_edades', 'lista_vida', 'yo_pequeno']),
    '_por-tema': ('', '', 'copia por tema (ver el original)', '', []),
}
# fotos con edad o año conocidos
EXACTO = {
    'abel_nino_2004': ('7', '2004'), 'abel_nino_retrato_2006': ('9', '2006'),
    'abel_11_anos_descenso_del_sella_asturias': ('11', '2008'), 'abel_nino_con_medalla': ('≈10', '2007'),
    'abel_bebe_juguetes': ('bebé', '1997-1999'), 'abel_bebe_con_su_abuelo': ('bebé', '1997-1999'),
    'abel_bebe_con_su_abuelo_moto_roja': ('bebé', '1997-1999'),
    'abel_retrato_blanco_y_negro_20_anos': ('≈20-21', '2017-2018'),
    'abel_graduacion_ade_promocion_2015_2019': ('22', '2019'), 'video_graduacion_universidad_ade_brindis': ('22', '2019'),
    'oficina_primer_trabajo_tras_la_carrera': ('22-23', '2019-2020'),
    'abel_cumpleanos_26_noche_oscura_del_alma': ('26', '2023'),
    'leon_con_su_madre_antes_y_despues_18_anos': ('4-5 y 22-23', ''),
    'abel_presentacion_libro_romuald_fons': ('≈23', '2020-2021'),
}

cat = json.loads(CAT.read_text(encoding='utf-8'))
for ruta, d in cat.items():
    carpeta, nombre = ruta.split('/')[0], Path(ruta).stem
    edad, anio, epoca, emocion, angulos = EPOCA.get(carpeta, ('', '', '', '', []))
    edad, anio = EXACTO.get(nombre, (edad, anio))
    d.update(edad=edad, anio=anio, epoca=epoca, emocion=emocion, angulos=angulos)
CAT.write_text(json.dumps(cat, ensure_ascii=False, indent=1), encoding='utf-8')
print(len(cat), 'fotos con contexto')
