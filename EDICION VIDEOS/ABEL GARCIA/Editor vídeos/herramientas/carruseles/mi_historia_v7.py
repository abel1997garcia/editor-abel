"""Carrusel «Mi historia» v7 (13/10/2026) con la ESTRUCTURA DE JUN YUH, enfocado al 100 % en lo que vende Abel:
portada → 5 de origen (la careta: «todo va bien») → su camino creando contenido detrás de una pantalla hasta dar la cara
(cada paso = un dolor de su avatar) → la lección que hoy enseña → resultados + lo que regala → por qué publico → cierre + sígueme.
Salida en carpeta NUEVA con nombres nuevos (Drive mezcla versiones si se sobrescribe)."""
import json
from pathlib import Path

AQUI = Path(__file__).resolve().parent
F = 'C:/Users/Clap/Desktop/EDICION VIDEOS/ABEL GARCIA/Editor vídeos/MarcaPersonal/FOTOS MIAS/'
G = str(AQUI / 'fotogramas') + '/'
SALIDA = 'G:/Mi unidad/FÁBRICA DE CONTENIDO/CARRUSELES/01 · Mi historia (v7)'

D = [
    (F + '06-noche-oscura-26-anos/abel_cumpleanos_26_noche_oscura_del_alma.jpg', "En esta foto parezco feliz,",
     ["pero mi madre me la hizo después de verme hora y media llorando. Tres días antes había perdido un negocio de 17.000 € al mes… en el que nunca había enseñado la cara.",
      "Si acabas de llegar, no conoces la historia…"], {}),
    (F + '12-familia-no-reels/leon_con_su_madre_antes_y_despues_18_anos.jpg', "Todo empezó en Boñar, un pueblo de León.",
     ["Mis padres se separaron cuando yo tenía 7 años, y mi madre se mataba a trabajar para sacarme adelante.",
      "Yo aprendí muy pronto a no ser un problema."], {}),
    (F + '01-infancia/abel_11_anos_descenso_del_sella_asturias.jpg', "Con 10 años, un juez me preguntó con quién quería vivir.",
     ["Nos fuimos a Castelldans, a 800 km de todo. Sufrí bullying, y a mi madre le decía que todo iba bien. Llorando.",
      "Ahí aprendí a llevar una careta. Y la llevé durante 20 años."], {}),
    (G + 'nino_sofa_consola_plano.png', "Mi forma de esconderme fue una pantalla.",
     ["Primero los videojuegos. Con 15 años, mi canal de Minecraft. Luego Facebook Ads, dropshipping, tiendas online… siempre detrás.",
      "Y cuando decía que quería vivir de YouTube, casi todos me decían lo mismo: «Eso no va a funcionar. Qué friki»."], {'foco': [0.45, 0.5]}),
    (F + '03-canal-gael-blog/canal_gael_blog_como_dejar_de_ser_vago.jpg', "Con 18 años me atreví por primera vez a dar la cara,",
     ["en un canal de crecimiento personal. Hasta que pusieron uno de mis vídeos en la tele de un bar de mi pueblo y se enteró todo el mundo.",
      "No supe sostenerlo. Y me volví a esconder."], {'foco': [0.58, 0.5]}),
    (F + '02-antes-de-despertar/abel_fiesta_mayor_capa_rosa.jpg', "Con 20 años era el de la fiesta, el que siempre sonreía.",
     ["Por dentro estuve a punto de quitarme la vida. Y no se lo dije a nadie.",
      "Así de bien se me daba decir que todo iba bien."], {}),
    (F + '04-canal-clap/abel_funda_movil_canal_clap.jpg', "En la pandemia lo volví a intentar: un vídeo de Clash Royale al día.",
     ["Me compré el curso de Romuald Fons, llegué a 30.000 suscriptores… y a 200 € al mes.",
      "Primera lección: tener audiencia no es lo mismo que tener un negocio."], {}),
    (F + '05-canal-automatizacion-ganaba-dinero/abel_placa_100k_suscriptores_youtube.jpg', "Con 25 años, por fin lo conseguí:",
     ["un canal de 100.000 suscriptores que facturaba 17.000 € al mes. Rechacé 550.000 € por él.",
      "Pero no salía yo. No me sentía suficiente para enseñarme a 100.000 personas."], {'foco': [0.5, 0.56], 'columna': 'der'}),
    (F + '05-canal-automatizacion-ganaba-dinero/abel_menorca_paseo_costa.jpg', "Lo llamaba «ingresos pasivos».",
     ["En realidad era miedo: si no me exponía, nadie me podía criticar.",
      "Es lo mismo que veo hoy en muchos emprendedores: un negocio montado para que no se les vea."], {}),
    (F + '06-noche-oscura-26-anos/abel_pompeya_italia_a_punto_de_arruinarse.jpg', "Hasta que un día YouTube me cerró todas las cuentas.",
     ["De más de cinco cifras al mes a cero, y debiendo 3.500 € a Hacienda.",
      "Un negocio en el que no estás tú te lo pueden quitar en un día. Lo que nadie te puede cerrar es quién eres."], {}),
    (F + '12-familia-no-reels/con_su_madre_dia_antes_de_irse_a_australia.jpg', "Sin nada, le pedí dinero a mi madre y me fui solo a Australia.",
     ["Palés de 30 kilos, bares, Uber, 70 horas a la semana… Allí nadie sabía quién había sido yo.",
      "Y por primera vez, me daba igual lo que pensaran."], {}),
    (G + 'llorando_australia.png', "Y allí hice lo que llevaba toda la vida evitando:",
     ["me grabé contando en YouTube cómo estaba sobreviviendo a Australia. Sin guion, sin careta. Llorando.",
      "Después de 20 años diciendo que todo iba bien, por fin decía la verdad delante de una cámara."], {'foco': [0.55, 0.6]}),
    (F + '08-australia/abel_moto_roja_australia.jpg', "En una moto que perdía aire, bajo la lluvia, era más feliz que con 17.000 € al mes.",
     ["Y entendí lo que hoy enseño: a la gente no le importa tanto tu tema. Le importa quién eres y por qué haces lo que haces.",
      "Tu historia es lo único que nadie te puede copiar."], {}),
    (F + '10-segundo-fondo-y-sanacion/abel_segundo_fondo_mal_estado_fisico.jpg', "Al volver, toqué fondo otra vez,",
     ["y vi algo que me dolió: en mis vídeos copiaba la forma de hablar de alguien a quien admiraba. Me llovía el hate por cosas que ni pensaba.",
      "Seguía llevando una careta. Solo que ahora era la de otro."], {}),
    (F + '10-segundo-fondo-y-sanacion/abel_llorando_sesion_sanacion.jpg', "Así que me tocó mirar dentro de verdad:",
     ["terapia, conciencia y, este último año, con todo el respeto, psilocibina.",
      "Desde entonces solo digo lo que siento. A quien le guste, bien. Y a quien no, también."], {}),
    (F + '11-ahora/abel_pizarra_ego_emocion.jpg', "Hoy ayudo a emprendedores a llenar su agenda dando la cara.",
     ["He acompañado a marcas a facturar más de 10.000 € al mes de forma recurrente… y a algo que me importa todavía más: entender por qué hacen lo que hacen.",
      "Y casi todo lo que sé lo regalo en mi canal de YouTube."], {}),
    (G + 'grabando_empezar_desde_0.png', "Por qué publico:",
     ["te dicen que copies guiones, ganchos virales y la forma de hablar de otros para vender.",
      "Yo prefiero enseñarte a vender siendo tú, con tu historia, tu intención y tu verdad. *Autenticidad que vende*."], {}),
    (F + '01-infancia/abel_nino_gorro_blanco_negro.jpg', "Un niño diciendo «todo va bien» llorando. Un vídeo en la tele de un bar. Un canal sin mi cara.",
     ["Ahí empecé.",
      "Si hoy te escondes detrás de tu negocio, no vas tarde: estás *al principio*. Sígueme y te enseño a vender siendo tú, una historia cada vez."], {}),
]

DESCRIPCION = """Durante años construí negocios para que nadie me viera.

Un canal de 17.000 € al mes en el que no salía yo. «Ingresos pasivos», lo llamaba. En realidad era miedo: a no ser suficiente, a la crítica, a que volvieran a decirme «qué friki».

Lo mismo que hacía con 10 años, cuando le decía a mi madre que todo iba bien, llorando.

Lo perdí todo en un día. Y lo que me sacó adelante no fue otra estrategia: fue dar la cara de verdad.

Por eso hoy te digo lo que me habría gustado escuchar entonces: lo más importante de tu negocio eres tú. Tu historia, tu intención, tu verdad. Eso es lo que nadie te puede copiar ni cerrar.

Si estás escondido detrás de tu negocio, no vas tarde. Estás al principio ❤️

#marcapersonal #emprendedores #autenticidad"""

assert len({f for f, *_ in D}) == len(D), 'foto repetida'
c = {'salida': SALIDA, 'descripcion': DESCRIPCION,
     'diapositivas': [dict(foto=f, titular=t, lineas=l, **o) for f, t, l, o in D]}
json.dump(c, open(AQUI / 'mi_historia_v7.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('ok', len(D))
