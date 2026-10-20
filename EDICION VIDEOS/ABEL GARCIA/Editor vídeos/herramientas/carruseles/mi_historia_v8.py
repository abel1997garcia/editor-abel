"""Carrusel «Mi historia» v8 (13/10/2026). Sobre el modelo aprobado (v7), llevado más al fondo:
cada momento de Abel va con lo que piensa A SOLAS su cliente (miedo a enseñarse, no sentirse suficiente, publicar y que no escriba nadie,
vergüenza de cobrar, copiar a otros…), como en un reel: gancho → su historia como puente a los problemas del cliente → cómo lo arregló →
cómo lo pueden arreglar → por qué se dedica a esto. Fotos de película (el hostal, el obrero, llorando). Carpeta y nombres NUEVOS."""
import json
from pathlib import Path

AQUI = Path(__file__).resolve().parent
F = 'C:/Users/Clap/Desktop/EDICION VIDEOS/ABEL GARCIA/Editor vídeos/MarcaPersonal/FOTOS MIAS/'
G = str(AQUI / 'fotogramas') + '/'
SALIDA = 'G:/Mi unidad/FÁBRICA DE CONTENIDO/CARRUSELES/01 · Mi historia (v8)'

D = [
    (F + '06-noche-oscura-26-anos/abel_cumpleanos_26_noche_oscura_del_alma.jpg', "En esta foto parezco feliz,",
     ["pero acababa de perder un negocio de 17.000 € al mes. Uno en el que nunca enseñé la cara, porque pensaba que yo no era suficiente.",
      "Si tienes un don, miedo a enseñarte y la agenda medio vacía… esta historia también es la tuya."], {}),
    (F + '12-familia-no-reels/leon_con_su_madre_antes_y_despues_18_anos.jpg', "Todo empezó en Boñar, un pueblo de León.",
     ["Mis padres se separaron cuando yo tenía 7 años, y mi madre se mataba a trabajar para sacarme adelante.",
      "Yo aprendí muy pronto a no molestar. A no ser un problema."], {}),
    (F + '01-infancia/abel_11_anos_descenso_del_sella_asturias.jpg', "Con 10 años, un juez me preguntó con quién quería vivir.",
     ["Nos fuimos a 800 km de todo. Sufrí bullying, y a mi madre le decía que todo iba bien. Llorando.",
      "Ahí me puse mi primera careta. La misma que llevas tú cuando dices «me va bien» con la agenda medio vacía."], {}),
    (G + 'nino_sofa_consola_plano.png', "Mi forma de esconderme fue una pantalla.",
     ["Videojuegos, un canal de Minecraft con 15 años, Facebook Ads, dropshipping… siempre detrás.",
      "Y cuando decía que quería vivir de YouTube: «Eso no va a funcionar. Qué friki». Como cuando a ti te dicen que lo tuyo «no da de comer»."], {'foco': [0.45, 0.5]}),
    (F + '03-canal-gael-blog/canal_gael_blog_como_dejar_de_ser_vago.jpg', "Con 18 años me atreví por primera vez a dar la cara,",
     ["hasta que pusieron uno de mis vídeos en la tele de un bar de mi pueblo y se enteró todo el mundo. No supe sostenerlo.",
      "Quizá tú también tienes vídeos grabados que nunca has subido. Por si te ven los de siempre."], {'foco': [0.58, 0.5]}),
    (F + '02-antes-de-despertar/abel_fiesta_mayor_capa_rosa.jpg', "Con 20 años era el de la fiesta, el que siempre sonreía.",
     ["Por dentro estuve a punto de quitarme la vida. Y no se lo dije a nadie.",
      "Cuando no te sientes suficiente, aprendes a disimularlo muy bien."], {}),
    (F + '04-canal-clap/abel_funda_movil_canal_clap.jpg', "En la pandemia lo volví a intentar: un vídeo de Clash Royale al día.",
     ["30.000 suscriptores… y 200 € al mes.",
      "Como cuando publicas, te dicen «qué bonito»… y no te escribe nadie para trabajar contigo."], {}),
    (F + '05-canal-automatizacion-ganaba-dinero/abel_placa_100k_suscriptores_youtube.jpg', "Con 25 años, por fin lo conseguí:",
     ["17.000 € al mes, y 550.000 € encima de la mesa que rechacé.",
      "Pero no salía yo. Pensaba: «¿Quién soy yo para enseñarme a 100.000 personas?»."], {'foco': [0.5, 0.56], 'columna': 'der'}),
    (F + '05-canal-automatizacion-ganaba-dinero/abel_menorca_paseo_costa.jpg', "Lo llamaba «ingresos pasivos».",
     ["En realidad era miedo: si no me exponía, nadie me podía criticar.",
      "Es lo que veo en tantos coaches y terapeutas: frases bonitas con un atardecer, otro curso, otro certificado… todo menos enseñarse de verdad."], {}),
    (F + '06-noche-oscura-26-anos/abel_pompeya_italia_a_punto_de_arruinarse.jpg', "Hasta que un día YouTube me cerró todas las cuentas.",
     ["De más de cinco cifras al mes a cero, debiendo 3.500 € a Hacienda. Y al poco, sin pareja.",
      "Lo que construyes escondido te lo pueden quitar en un día. Lo que nadie te puede quitar es quién eres."], {}),
    (F + '12-familia-no-reels/con_su_madre_dia_antes_de_irse_a_australia.jpg', "Sin nada, le pedí dinero a mi madre y me fui solo a Australia.",
     ["Con 26 años, una carrera y un negocio de 17.000 € a mis espaldas… sin inglés y a 17.000 km de casa.",
      "Sentía que si no me iba, me moría."], {}),
    (G + 'hostal_litera_6_personas.png', "Mi casa era una litera en un hostal con 6 desconocidos.",
     ["Al tercer día ya descargaba palés de cajas de 30 kilos. Al siguiente, fiebre y agujetas por todo el cuerpo.",
      "El chico de los 17.000 € al mes, empezando de cero."], {'foco': [0.45, 0.5]}),
    (G + 'reparando_teles_70kg.png', "Reparando teles de 70 kilos, de obrero, repartidor, camarero, Uber…",
     ["hasta 70 horas a la semana. Allí nadie sabía quién había sido yo.",
      "Y por primera vez en mi vida, me daba igual lo que pensaran de mí."], {}),
    (G + 'llorando_australia.png', "Y allí hice lo que llevaba toda la vida evitando:",
     ["me grabé contando en YouTube cómo estaba sobreviviendo a Australia. Sin guion, sin careta. Llorando.",
      "Lo que tú tienes miedo de enseñar es justo lo que hará que alguien te elija."], {'foco': [0.55, 0.6]}),
    (F + '08-australia/abel_moto_roja_australia.jpg', "En una moto que perdía aire, bajo la lluvia, era más feliz que con 17.000 € al mes.",
     ["Y entendí lo que hoy enseño: a la gente no le importa tanto tu tema. Le importa quién eres y por qué haces lo que haces."], {}),
    (F + '10-segundo-fondo-y-sanacion/abel_segundo_fondo_mal_estado_fisico.jpg', "Al volver, toqué fondo otra vez,",
     ["y vi algo que me dolió: en mis vídeos copiaba la forma de hablar de alguien a quien admiraba.",
      "Si copias guiones y frases de otros, te pasará lo mismo: atraerás a quien no es, y no te encontrará quien te necesita."], {}),
    (F + '10-segundo-fondo-y-sanacion/abel_llorando_sesion_sanacion.jpg', "Así que me tocó mirar dentro de verdad.",
     ["Terapia, conciencia y, este último año, con todo el respeto, psilocibina.",
      "Porque lo que te vacía la agenda casi nunca es la estrategia. Es el miedo que hay debajo."], {}),
    (F + '11-ahora/abel_pizarra_ego_emocion.jpg', "Hoy ayudo a emprendedores a llenar su agenda dando la cara.",
     ["Mi primera clienta me pagaba 200 € al mes, porque me daba vergüenza cobrar más. Hoy he acompañado a marcas a facturar más de 10.000 € al mes de forma recurrente.",
      "Y casi todo lo que sé lo regalo en mi canal de YouTube."], {}),
    (G + 'grabando_empezar_desde_0.png', "Por qué publico:",
     ["te dicen que copies guiones, que te hagas viral, que bajes precios para empezar.",
      "Yo prefiero enseñarte a vender siendo tú: con tu historia, tu intención y tu verdad. *Autenticidad que vende*."], {}),
    (F + '01-infancia/abel_nino_gorro_blanco_negro.jpg', "Un niño diciendo «todo va bien» llorando. Un vídeo en la tele de un bar. Un canal sin mi cara.",
     ["Ahí empecé.",
      "Si hoy te escondes detrás de tu negocio, no vas tarde: estás *al principio*. Sígueme y te enseño a vender siendo tú, una historia cada vez."], {}),
]

DESCRIPCION = """Quizá te pase esto.

Tienes un don. Sabes que ayudas a la gente. Pero cuando te pones delante de la cámara, piensas: «¿Quién soy yo para enseñar esto?».

Grabas un vídeo y no lo subes. Publicas una frase bonita y no te escribe nadie. Te da vergüenza decir tu precio. Y cuando alguien te pregunta, dices que te va bien.

Yo hice eso durante 20 años.

Con 10 años le decía a mi madre que todo iba bien mientras lloraba. Con 18 di la cara por primera vez, pusieron uno de mis vídeos en la tele de un bar de mi pueblo y me escondí. Con 25 facturaba 17.000 € al mes con un canal en el que no salía yo, porque no me sentía suficiente.

Lo perdí todo en un día.

Y lo que me sacó adelante no fue otra estrategia ni otro curso. Fue dejar de esconderme: un vídeo grabado llorando en Australia, sin guion y sin careta.

Lo que te vacía la agenda casi nunca es la estrategia. Es el miedo que hay debajo. Y tu historia, esa que te da miedo enseñar, es justo lo que hará que alguien te elija.

Por eso hoy ayudo a emprendedores a llenar su agenda con su marca personal siendo ellos mismos. Porque he estado en los dos lados: el negocio que facturaba sin mi cara y el que construyo dando la cara.

Si hoy te escondes detrás de tu negocio, no vas tarde. Estás al principio ❤️

#marcapersonal #emprendedores #autenticidad"""

assert len({f for f, *_ in D}) == len(D) == 20, 'foto repetida o no son 20'
c = {'salida': SALIDA, 'descripcion': DESCRIPCION,
     'diapositivas': [dict(foto=f, titular=t, lineas=l, **o) for f, t, l, o in D]}
json.dump(c, open(AQUI / 'mi_historia_v8.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('ok', len(D))
