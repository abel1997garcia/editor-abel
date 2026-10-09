import cv2, json, glob, os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
cat = json.load(open('catalogo.json', encoding='utf-8'))
def F(p): return glob.glob('_nuevas2/' + p + '*')[0]
trim = {'v3_0000.7': (0, 0, .2, 0), 'v5_0000.5': (0, .09, 0, 0), 'v5_0055.3': (0, .09, 0, 0)}
M = [('v1_0000.8', 'ego', 'ego_globo_hombre', 'Hombre señalando un globo con la palabra EGO (foto antigua B/N)', 'foto'),
('v1_0003.2', 'manifestacion', 'salto_cuantico_figura_luz', 'Figura de luz saltando con efecto glitch de colores (salto cuántico, nueva realidad)', 'visionario'),
('v1_0007.8', 'descenso-transformacion', 'inframundo_pintura', 'Pintura clásica del inframundo, fuego y almas', 'pintura'),
('v1_0010.8', 'descenso-transformacion', 'barca_inframundo_grabado', 'Grabado: barquero cruzando el río del inframundo (Dante)', 'grabado'),
('v1_0012.5s_26', 'descenso-transformacion', 'infierno_rojo_pintura', 'Pintura de infierno en rojo con figuras y llamas', 'pintura'),
('v1_0012.5s_281', 'descenso-transformacion', 'ciudad_infierno_oscura', 'Ciudad oscura en llamas, tonos rojos', 'pintura'),
('v1_0012.5s_35', 'descenso-transformacion', 'descenso_figura_alada', 'Figura oscura alada que arrastra almas (descenso)', 'pintura'),
('v1_0020.0s_210', 'tarot', 'la_muerte', 'Carta XIII La Muerte (tarot Rider-Waite): fin de un ciclo', 'grabado'),
('v1_0020.0s_26', 'descenso-transformacion', 'descenso_al_abismo_pintura', 'Figuras que descienden a una cueva junto al mar (pintura)', 'pintura'),
('v1_0033.5', 'mitologia', 'persefone_rapto_pintura', 'Hades raptando a Perséfone (pintura clásica)', 'pintura'),
('v1_0039.3', 'emociones', 'pareja_desmoronandose_collage', 'Pareja que se desmorona en pedazos (relación que se rompe), collage', 'collage'),
('v1_0048.3', 'sombra-inconsciente', 'psique_jung_self', 'Mapa de la psique de Jung: persona, ego, sí mismo, sombra, ánima/ánimus', 'esquema'),
('v1_0054.0', 'mitologia', 'pluton_grabado', 'Plutón / Hades, grabado antiguo', 'grabado'),
('v1_0056.0', 'mitologia', 'hades_trono_ceramica', 'Hades en su trono (cerámica griega roja)', 'pintura'),
('v1_0079.3', 'mitologia', 'inanna_ishtar_relieve_lineas', 'Inanna/Ishtar con el león y la estrella (dibujo a línea)', 'grabado'),
('v1_0082.7', 'aura-cuerpo-de-luz', 'grial_campo_energia', 'Grial dorado en un campo de energía azul (visionario)', 'visionario'),
('v1_0087.7', 'aura-cuerpo-de-luz', 'diosa_agua_luz', 'Diosa de luz emergiendo del agua (alma, purificación)', 'visionario'),
('v1_0093.0', 'mitologia', 'ishtar_relieve_dorado', 'Relieve dorado de Ishtar con alas', 'grabado'),
('v1_0103.8', 'ego', 'sacrificio_cabeza_mujer', 'Mujer que entrega su propia cabeza (sacrificar falsas identidades), pintura surrealista', 'pintura'),
('v1_0112.7', 'mitologia', 'persefone_ceramica_roja', 'Perséfone desciende (cerámica griega negra y roja)', 'pintura'),
('v1_0117.3', 'descenso-transformacion', 'putrefactio_alquimia', 'Grabado alquímico «Putrefactio»: esqueleto sobre el sol negro (muerte del ego)', 'grabado'),
('v1_0121.8', 'sombra-inconsciente', 'integrar_la_sombra', 'Silueta blanca frente a su sombra en llamas (integrar la sombra)', 'grabado'),
('v1_0139.8', 'aura-cuerpo-de-luz', 'silueta_estrellas_nucleo', 'Silueta abierta que muestra un núcleo de luz (quién eres de verdad)', 'visionario'),
('v2_0000.0', 'campo-toroidal', 'toroide_cuerpo_meridianos', 'Cuerpo con meridianos dentro de un campo toroidal', 'esquema'),
('v3_0000.7', 'centros-energeticos', 'espiritu_cuerpo_alma', 'Triángulo espíritu–cuerpo–alma', 'esquema'),
('v3_0010.8', 'masculino-femenino', 'polaridades_masculino_femenino', 'Polaridades: femenino (emoción, creatividad, agua) vs masculino (lógica, ciencia, fuego)', 'esquema'),
('v3_0023.0', 'masculino-femenino', 'dios_prisma_subconsciente', 'Dios → prisma: mente subconsciente (femenina) y reino dual (consciente, masculina)', 'esquema'),
('v3_0030.5', 'mitologia', 'tradiciones_antiguas_collage', 'Seis tradiciones: babilonia, hindú, maya, egipcia, cristiana', 'collage'),
('v3_0035.3', 'leyes-hermeticas', 'arbol_de_la_vida_cabala', 'Árbol de la vida (Cábala) con nombres hebreos', 'esquema'),
('v3_0037.8', 'mitologia', 'isis_osiris_egipto', 'Isis y Osiris (pintura egipcia)', 'pintura'),
('v3_0040.0', 'masculino-femenino', 'dualidad_polaridad_yin_yang', 'Ley de la polaridad / género: yin-yang', 'esquema'),
('v3_0042.3', 'masculino-femenino', 'shiva_shakti', 'Shiva y Shakti (arte hindú)', 'pintura'),
('v3_0075.7', 'intuicion-tercer-ojo', 'ida_pingala_cerebro', 'Cabeza con cerebro en colores y los canales ida y pingala', 'esquema'),
('v4_0000.0', 'manifestacion', 'alquimista_cuerpo_rayos', 'Alquimista con rayos que salen del cuerpo (grabado)', 'grabado'),
('v4_0000.5', 'frecuencia-vibracion', 'cerebro_ondas_doradas', 'Cerebro/figura con ondas doradas sobre negro', 'visionario'),
('v4_0011.0', 'cotidiano-bocetos', 'reunion_mesa_boceto', 'Personas en una mesa vistas desde arriba (conexiones), boceto', 'boceto'),
('v4_0012.3', 'cotidiano-bocetos', 'networking_oficina', 'Gente en una oficina conectando (contactos, oportunidades)', 'foto'),
('v4_0015.0', 'cotidiano-bocetos', 'trabajando_ordenador', 'Hombre de espaldas trabajando en el ordenador', 'foto'),
('v4_0015.3s_52', 'cotidiano-bocetos', 'pintora_creatividad', 'Mujer pintando en su estudio (talento, habilidades)', 'foto'),
('v4_0064.8', 'manifestacion', 'manos_sosteniendo_mundo', 'Manos sosteniendo el mundo (contribución con sentido)', 'visionario'),
('v4_0086.3', 'manifestacion', 'luz_desde_el_cielo', 'Figura pequeña bajo un haz de luz cálida (recibir)', 'visionario'),
('v4_0105.7', 'sombra-inconsciente', 'cerebro_sepia', 'Cabeza con el cerebro, grabado sepia (reprogramar la mente)', 'grabado'),
('v5_0000.5', 'intuicion-tercer-ojo', 'lamina_esoterica_ondas', 'Lámina esotérica con ondas y figuras (inspiración)', 'grabado'),
('v5_0015.3', 'aura-cuerpo-de-luz', 'cuerpo_energia_azul_rosa', 'Cuerpo humano de energía azul y rosa (creación)', 'visionario'),
('v5_0045.3', 'sombra-inconsciente', 'realidad_presente_tiempo', 'Realidad = momento presente; la ilusión del tiempo (pasado/futuro)', 'esquema'),
('v5_0055.3', 'campo-toroidal', 'toroide_silueta_negra', 'Silueta negra dentro de un toroide (campo de energía)', 'esquema')]
for p, tema, nom, desc, fam in M:
    os.makedirs(tema, exist_ok=True)
    im = cv2.imread(F(p)); h, w = im.shape[:2]; l, t, r, b = trim.get(p, (0, 0, 0, 0))
    im = im[int(h * t):int(h * (1 - b)), int(w * l):int(w * (1 - r))]
    dst = f'{tema}/{nom}.png'; cv2.imwrite('_originales/' + dst.replace('/', '__'), im)
    up = cv2.resize(im, None, fx=3, fy=3, interpolation=cv2.INTER_LANCZOS4); up = cv2.fastNlMeansDenoisingColored(up, None, 4, 4, 7, 21)
    bl = cv2.GaussianBlur(up, (0, 0), 2.2); up = cv2.addWeighted(up, 1.7, bl, -.7, 0); cv2.imwrite(dst, up)
    seg = float(p[3:9])
    cat[dst] = {'tema': tema, 'muestra': desc, 'familia': fam, 'origen': f'reel de referencia F4 (vídeo {p[1]} del 08/10), segundo {seg:.1f}',
                'resolucion': f'{up.shape[1]}x{up.shape[0]} (ampliada ×3 y enfocada)', 'fecha': '2026-10-08'}
json.dump(cat, open('catalogo.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(len(cat))
