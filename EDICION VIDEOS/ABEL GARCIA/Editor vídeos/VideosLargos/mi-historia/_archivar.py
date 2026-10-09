"""Archiva en FOTOS MIAS lo sacado de «Mi Historia» (fotos nuevas + escenas explicativas de vídeos, sin sonido) y actualiza catalogo.json."""
import json, os, shutil, subprocess
FM = '../../MarcaPersonal/FOTOS MIAS/'
SRC = '_ext3/'
CAT = FM + 'catalogo.json'
E3 = json.load(open('ext3.json', encoding='utf-8'))
cat = json.load(open(CAT, encoding='utf-8'))
def mm(s): return f'{int(s // 60)}:{int(s % 60):02d}'

# ---- 1) reorganizar lo que ya existía (con lo aprendido en el vídeo) ----
def mover(viejo, nuevo, **cambios):
    os.makedirs(os.path.dirname(FM + nuevo), exist_ok=True)
    if os.path.exists(FM + viejo): shutil.move(FM + viejo, FM + nuevo)
    e = cat.pop(viejo, {}); e.update(cambios); cat[nuevo] = e
if os.path.isdir(FM + '04-canal-clap-minecraft'):
    os.rename(FM + '04-canal-clap-minecraft', FM + '04-canal-clap')
for k in [k for k in cat if k.startswith('04-canal-clap-minecraft/')]:
    cat[k.replace('04-canal-clap-minecraft/', '04-canal-clap/')] = cat.pop(k)
mover('04-canal-clap/abel_funda_movil_canal_clap_minecraft.jpg', '04-canal-clap/abel_funda_movil_canal_clap.jpg')
mover('02-antes-de-despertar/abel_fiesta_disfraz_acusti_mestre.jpg', '07-trabajo-monitor/abel_monitor_navidad_con_companeros_agusti_mestre.jpg',
      que_es='Con sus compañeros de monitor de Navidad (mono rojo y elfos) en Agustí Mestre — es el trabajo de monitor, NO una fiesta',
      reels=True)
shutil.copy(FM + '07-trabajo-monitor/abel_monitor_navidad_con_companeros_agusti_mestre.jpg', FM + '_por-tema/trabajos/')
cat['_por-tema/trabajos/abel_monitor_navidad_con_companeros_agusti_mestre.jpg'] = {'copia_de': '07-trabajo-monitor/abel_monitor_navidad_con_companeros_agusti_mestre.jpg'}
cat['06-primer-fondo/abel_en_casa_primera_vez_que_toco_fondo.jpg'].update(
    que_es='Su cumpleaños número 26 (2023): parece contento, pero su madre le hizo la foto tras hora y media sin parar de llorar; 3 días antes '
           'le habían cancelado todas las cuentas de YouTube (pasó de más de 5 cifras al mes a deber 3.500 € a Hacienda) y había roto con su pareja. '
           'Es la foto con la que abre «Mi Historia». Justo después decide irse a Australia.', reels=True)
cat['01-infancia/taller_casa_abuela.jpg'].update(que_es='El almacén de su abuelo (casa de los abuelos): donde escondía bolsas de patatas y dulces para que la abuela no los viera (lo confirmó el médium)')

# ---- 2) fotos nuevas ----
FOTOS = [  # (archivo _ext3, destino, que_es, reels)
 ('002_00m51.0s', '01-infancia/abel_nino_cumpleanos_vela_bengala.png', 'De niño soplando una vela bengala en su cumpleaños (León/Boñar)', True),
 ('008_03m27.5s', '01-infancia/abel_nino_con_medalla.png', 'De niño con una medalla y un trofeo (≈10 años, época de la mudanza a Castelldans)', True),
 ('009_04m05.0s', '01-infancia/abel_primera_comunion_grupo.png', 'Su primera comunión, foto de grupo', False),
 ('010_04m13.0s', '01-infancia/abel_nino_equipo_futbol.png', 'Con su equipo de fútbol de niño', True),
 ('016_08m31.0s', '01-infancia/abel_nino_con_su_abuelo_blanco_y_negro.png', 'De niño con su abuelo paterno (blanco y negro). Su abuelo enfermó y murió cuando él estaba en 5.º-6.º de primaria', True),
 ('026_17m16.5s', '01-infancia/abel_nino_disfrazado_con_otro_nino.png', 'De niño disfrazado (carnaval) con otro niño', True),
 ('059_53m48.0s', '01-infancia/abel_bebe_con_su_abuelo_moto_roja.png', 'De bebé subido a la moto roja de su abuelo (la moto que el médium nombró)', True),
 ('017_10m03.0s', '01b-adolescencia/abel_adolescente_montana.png', 'Adolescente en la montaña (época del instituto)', True),
 ('018_10m54.0s', '01b-adolescencia/abel_adolescente_chaqueta_cuadros.png', 'Adolescente, 1.º-2.º de la ESO: la época rebelde, Call of Duty y rabia', True),
 ('019_11m06.0s', '01b-adolescencia/abel_adolescente_con_amigos.png', 'Adolescente con amigos sentados (ESO)', False),
 ('020_12m57.0s', '01b-adolescencia/abel_futbol_descanso_con_equipo.png', 'Fútbol: descanso con el equipo (Borges Blanques). Era muy autoexigente y acabó dejándolo', False),
 ('021_13m09.0s', '01b-adolescencia/abel_futbol_jugando_partido.png', 'Fútbol: jugando un partido (Borges Blanques). Autoexigencia: si no marcaba, se quemaba', True),
 ('022_13m16.5s', '01b-adolescencia/abel_futbol_campo_partido.png', 'Fútbol: el campo durante un partido', True),
 ('023_14m27.0s', '12-familia-no-reels/primera_novia_beso_blanco_y_negro.png', 'Con su primera novia (la que canalizaba mensajes de su abuelo). Otra persona: NO en reels', False),
 ('011_05m08.5s', '12-familia-no-reels/abel_nino_cumpleanos_con_mujer_probablemente_su_madre.png', 'De niño en su cumpleaños con una mujer (probablemente su madre — por confirmar)', False),
 ('025_16m46.0s', '02-antes-de-despertar/abel_fiesta_cabina_dj_camisetas_verdes.png', 'De fiesta en una cabina con camisetas verdes (época en que cambió los videojuegos por la fiesta y el alcohol)', True),
 ('027_17m59.0s', '02-antes-de-despertar/abel_retrato_blanco_y_negro_20_anos.png', 'Retrato en blanco y negro con ≈20-21 años: época de la relación tóxica y de los psicólogos que no le sirvieron', True),
 ('028_22m11.5s', '02-antes-de-despertar/fiesta_de_pueblo_fuego_verano.png', 'Fiestas de los pueblos en verano (de miércoles a domingo de fiesta, alcohol y tragaperras)', True),
 ('031_24m12.5s', '02-antes-de-despertar/abel_fiesta_selfie_camiseta_rosa.png', 'De fiesta, selfie con camiseta rosa: fiestas de Castelldans/Borges, «el alcohol ya ni me subía»', True),
 ('032_26m30.0s', '02-antes-de-despertar/abel_graduacion_ade_promocion_2015_2019.png', 'Graduación de ADE, promoción 2015-2019 (Pas d\'Equador), con amigos y copas', True),
 ('033_26m51.5s', '02-antes-de-despertar/oficina_primer_trabajo_tras_la_carrera.png', 'La oficina enorme (300-400 personas) de su primer trabajo tras la carrera: 2 meses sintiéndose vacío, hasta la pandemia (2020)', True),
 ('035_28m04.5s', '04-canal-clap/abel_post_pccomponentes.png', 'Publicación de PcComponentes con él (época del canal Clap, 2020-21)', True),
 ('036_28m09.0s', '04-canal-clap/captura_ingresos_youtube_casi_nada.png', 'Captura de sus ingresos de YouTube: «no generaba ni 100 € con más de 200.000 visitas al mes» (canal Clap: 30.000 suscriptores, ≈200 €/mes)', True),
 ('037_30m28.5s', '05-canal-automatizacion-ganaba-dinero/abel_presentacion_libro_romuald_fons.png', 'En la presentación del libro «Crece y hazte rico» de Romuald Fons (compró su curso Crece Tube de 700 €): la época en que se formaba, justo ANTES de empezar a ganar dinero', True),
 ('041_37m10.5s', '08-australia/miniatura_video_17000km_en_2_dias.png', 'Miniatura de su vlog «+17.000 km en 2 días» (el viaje de España a Australia)', True),
 ('046_41m38.5s', '08-australia/miniatura_tu_plan_superior_moto.png', 'Miniatura de su vídeo «Tu Plan Superior» con la moto de Australia (canal El Viaje de Abel)', True),
 ('048_42m31.0s', '08-australia/abel_leyendo_sudadera_azul_primera_casa.png', 'Leyendo con la sudadera azul en su primera casa de Australia (gimnasio, meditación, estudiar espiritualidad)', True),
 ('058_52m52.5s', '10-segundo-fondo-y-sanacion/miniatura_sesion_medium_allan_garcia.png', 'Miniatura «El Camino Interior #5 | Médium Allan García»: el médium con el que habló con su abuelo (ya en Lérida, tras volver)', False),
]
for src, dst, q, r in FOTOS:
    os.makedirs(os.path.dirname(FM + dst), exist_ok=True); shutil.copy(SRC + src + '.png', FM + dst)
    a = next(e['a'] for e in E3 if e['archivo'].endswith(src + '.png'))
    cat[dst] = {'que_es': q, 'reels': r, 'original': f'Mi Historia.mp4 @ {mm(a)}', 'calidad': 'captura del vídeo (baja-media)'}
shutil.copy(FM + '02-antes-de-despertar/oficina_primer_trabajo_tras_la_carrera.png', FM + '_por-tema/trabajos/')
cat['_por-tema/trabajos/oficina_primer_trabajo_tras_la_carrera.png'] = {'copia_de': '02-antes-de-despertar/oficina_primer_trabajo_tras_la_carrera.png'}

# ---- 3) escenas explicativas de los vídeos (SIN sonido) ----
YT = '1124:632:60:0'  # zona del reproductor en las grabaciones de pantalla de YouTube
VIDEOS = [  # (clip, ini, fin, crop|None, destino, que_es, reels)
 ('004_01m12.0s', 0, 12, '960:716:158:0', '01-infancia/video_nino_jugando_consola_sofa.mp4', 'De niño tumbado en el sofá jugando a la consola: su «burbuja» tras la separación de sus padres', True),
 ('005_01m43.5s', 0, 4, '960:716:158:0', '01-infancia/video_nino_consola_primer_plano.mp4', 'De niño jugando a la consola, primer plano mirando a cámara', True),
 ('013_06m56.0s', 0, 3, None, '01c-canal-packard-minecraft/video_canal_packard_minecraft_pagina.mp4', 'La página de su primer canal, «Packard Minecraft» (de niño, el que más cariño le tiene)', True),
 ('013_06m56.0s', 11, 18, None, '01c-canal-packard-minecraft/video_packard_minecraft_partida.mp4', 'Un vídeo de Minecraft de su canal Packard Minecraft', True),
 ('034_27m41.5s', 0, 13, None, '04-canal-clap/video_canal_clap_pagina_y_miniaturas.mp4', 'Su canal «Clap» (Clash Royale): página y miniaturas. Pandemia 2020: un vídeo al día, 30.000 suscriptores, ≈200 €/mes', True),
 ('034_27m41.5s', 14, 23, None, '04-canal-clap/video_canal_clap_directo_clash_royale.mp4', 'Él grabando un vídeo de Clash Royale con cascos para su canal Clap', True),
 ('054_46m56.5s', 0, 14, YT, '08-australia/video_aeropuerto_barcelona_salida_a_australia.mp4', 'En el aeropuerto de Barcelona, saliendo hacia Australia (vlog «El viaje de mi vida»)', True),
 ('042_38m02.5s', 3, 12, '1124:632:36:0', '08-australia/video_hostal_habitacion_6_personas.mp4', 'Las primeras semanas: la habitación de 6 personas del hostal Summer House Backpackers (Brisbane) y la fachada', True),
 ('044_39m34.0s', 10, 15, None, '08-australia/video_obrero_chaleco_amarillo_selfie.mp4', 'Selfie con chaleco amarillo trabajando de obrero (Brisbane). Calidad baja', True),
 ('044_39m34.0s', 31, 42, None, '08-australia/video_barra_cocteles_llena.mp4', 'Trabajando en la barra de cócteles llena de gente (Brisbane). Calidad baja', True),
 ('055_48m05.0s', 0, 2, YT, '08-australia/video_llorando_video_emocional_australia.mp4', 'Llorando en su vídeo «Cómo sobreviví a Australia (vídeo emocional)»', True),
 ('055_48m05.0s', 2, 8, YT, '08-australia/video_dos_bares_70_horas.mp4', 'Los últimos 3-4 meses: 70 h a la semana en dos bares (uno por la mañana, otro por la tarde)', True),
 ('055_48m05.0s', 11, 13, YT, '08-australia/video_gimnasio_australia.mp4', 'Entrenando en el gimnasio en Australia', True),
 ('055_48m05.0s', 13, 20, YT, '08-australia/video_uber_coche_alquilado_1.mp4', 'En el primer coche que alquiló para hacer Uber en los ratos libres', True),
 ('055_48m05.0s', 21, 29, YT, '08-australia/video_uber_coche_alquilado_2.mp4', 'El segundo coche alquilado (blanco) para Uber y conduciendo', True),
 ('053_45m30.0s', 0, 14, YT, '09-sudeste-asiatico/video_turquia_mochilas_final_del_viaje.mp4', 'Turquía, el final del viaje en solitario: sus mochilas y él por la calle', True),
 ('052_44m59.5s', 0, 16, YT, '12-familia-no-reels/video_vuelta_sorpresa_a_casa_tras_australia.mp4', 'Llega por sorpresa a casa tras Australia (su madre creía que se iba a Nueva Zelanda). Familia: NO en reels', False),
 ('056_49m53.0s', 0, 11, '1120:630:50:0', '11-ahora/video_piso_lleida_donde_vive_y_graba.mp4', 'Su piso de Lérida, donde vive y graba (vlog «ni se te ocurra rendirte»)', True),
 ('040_36m05.5s', 0, 13, None, '08-australia/video_canal_el_viaje_de_abel_videos_australia.mp4', 'Scroll de su canal El Viaje de Abel: los vídeos de Australia. Muy pequeño (232 px)', True),
 ('040_36m05.5s', 50, 57, None, '11-ahora/video_canal_el_viaje_de_abel_videos_pizarra.mp4', 'Scroll de su canal El Viaje de Abel: los vídeos con pizarra. Muy pequeño (232 px)', True),
]
for clip, a, b, crop, dst, q, r in VIDEOS:
    os.makedirs(os.path.dirname(FM + dst), exist_ok=True)
    vf = (f'crop={crop},' if crop else '') + 'scale=trunc(iw/2)*2:trunc(ih/2)*2'
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', str(a), '-to', str(b), '-i', SRC + clip + '.mp4', '-an', '-vf', vf,
                    '-c:v', 'libx264', '-crf', '17', '-pix_fmt', 'yuv420p', FM + dst], check=True)
    t0 = next(e['a'] for e in E3 if e['archivo'].endswith(clip + '.mp4')) + a
    cat[dst] = {'que_es': q, 'reels': r, 'original': f'Mi Historia.mp4 @ {mm(t0)}', 'sonido': False}
    if any(w in dst for w in ('obrero', 'barra_cocteles', 'dos_bares', 'uber')):
        shutil.copy(FM + dst, FM + '_por-tema/trabajos/'); cat['_por-tema/trabajos/' + os.path.basename(dst)] = {'copia_de': dst}
json.dump(cat, open(CAT, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(len(FOTOS), 'fotos y', len(VIDEOS), 'escenas archivadas ·', len(cat), 'entradas en el catálogo')
