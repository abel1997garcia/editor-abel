"""Carrusel «Mi historia» v9 (13/10/2026). Base: la v7 aprobada (siempre habla de Abel y de su camino, conectado con lo que vende).
Corrección de Abel sobre la v8 («parece que estés forzando a vender»): NADA de frases tipo «como cuando a ti…». Contado de tú a tú,
natural, como si se abriera en canal: lo que SENTÍA, sobre sí mismo, sobre la vida, sobre lo que merecía y lo que ha venido a hacer.
Los sentimientos salen de sus palabras (vídeo «Mi Historia» y lo que ha contado). Carpeta y nombres NUEVOS."""
import json
from pathlib import Path

AQUI = Path(__file__).resolve().parent
F = 'C:/Users/Clap/Desktop/EDICION VIDEOS/ABEL GARCIA/Editor vídeos/MarcaPersonal/FOTOS MIAS/'
G = str(AQUI / 'fotogramas') + '/'
SALIDA = 'G:/Mi unidad/FÁBRICA DE CONTENIDO/CARRUSELES/01 · Mi historia (v9)'

D = [
    (F + '06-noche-oscura-26-anos/abel_cumpleanos_26_noche_oscura_del_alma.jpg', "En esta foto parezco feliz,",
     ["pero mi madre me la hizo después de verme hora y media llorando sin parar. Tres días antes había perdido un negocio de 17.000 € al mes en el que nunca enseñé la cara.",
      "Estaba roto, sin ningún tipo de sentido. Si acabas de llegar, no conoces la historia…"], {}),
    (F + '12-familia-no-reels/leon_con_su_madre_antes_y_despues_18_anos.jpg', "Todo empezó en Boñar, un pueblo de León.",
     ["Mis padres se separaron cuando yo tenía 7 años y mi madre se mataba a trabajar. Me cuidaban cuidadoras muy buenas… pero no eran mi familia, y yo me sentía solo.",
      "Ya de niño me obsesionaba entender por qué unas personas se quieren y otras no. No sabía que eso acabaría siendo mi vida."], {}),
    (F + '01-infancia/abel_11_anos_descenso_del_sella_asturias.jpg', "Con 10 años, un juez me preguntó con quién quería vivir.",
     ["El día que llamaron para decir que me quedaba con mi madre, se me paró el tiempo. Estaba roto por dentro, y aun así la miré y le dije: «Perfecto, todo está bien». Llorando.",
      "Nos fuimos a 800 km de todo y el primer año sufrí bullying. Ahí aprendí a tragarme lo que sentía."], {}),
    (G + 'nino_sofa_consola_plano.png', "Así que me escondí detrás de una pantalla.",
     ["Los videojuegos eran mi burbuja, porque el mundo de fuera no lo quería. Con 15 años creé mi canal de Minecraft, y después probé Facebook Ads, dropshipping, tiendas online…",
      "Cuando decía que quería vivir de YouTube, casi todos me decían: «Eso no va a funcionar. Qué friki». Y me sentía fatal."], {'foco': [0.45, 0.5]}),
    (F + '03-canal-gael-blog/canal_gael_blog_como_dejar_de_ser_vago.jpg', "Con 18 años me atreví por primera vez a dar la cara,",
     ["en un canal de crecimiento personal. Hasta que pusieron uno de mis vídeos en la tele de un bar de mi pueblo y se enteró todo el mundo.",
      "No supe sostenerlo. Y me volví a esconder."], {'foco': [0.58, 0.5]}),
    (F + '02-antes-de-despertar/abel_fiesta_mayor_capa_rosa.jpg', "Con 20 años era el de la fiesta, el que siempre sonreía.",
     ["Por dentro sentía un vacío que no llenaba con nada: ni con el alcohol, ni con las apuestas, ni con nadie.",
      "Estuve a punto de quitarme la vida. Y no se lo dije a nadie."], {}),
    (F + '12-familia-no-reels/graduacion_carrera_con_su_padrastro.jpg', "Por fuera, todo en orden: acabé la carrera de ADE.",
     ["Por dentro, fui a una psicóloga por primera vez… y salí pensando: «Vaya puta mierda».",
      "Me sentí un tonto. Como si lo mío no tuviera remedio."], {}),
    (F + '04-canal-clap/abel_funda_movil_canal_clap.jpg', "En la pandemia me encerré a hacer un vídeo de Clash Royale al día,",
     ["después de dos meses en una oficina con 400 personas sintiendo un vacío tan grande que no podía ni estar sentado.",
      "Llegué a 30.000 suscriptores… y a 200 € al mes. Ahí entendí que tener audiencia no es lo mismo que tener un negocio."], {}),
    (F + '05-canal-automatizacion-ganaba-dinero/abel_placa_100k_suscriptores_youtube.jpg', "Con 25 años, por fin lo conseguí:",
     ["un canal de 100.000 suscriptores que facturaba 17.000 € al mes. Rechacé 550.000 € por él.",
      "Por fin sentía que valía algo… pero solo porque ganaba dinero. Y en ese canal no salía yo: no me sentía suficiente para enseñarme."], {'foco': [0.5, 0.56], 'columna': 'der'}),
    (F + '05-canal-automatizacion-ganaba-dinero/abel_menorca_paseo_costa.jpg', "Viajes, pareja, la vida que te venden.",
     ["Lo llamaba «ingresos pasivos». En realidad era miedo: si no me exponía, nadie me podía criticar.",
      "Por dentro seguía siendo el niño que decía que todo iba bien."], {}),
    (F + '06-noche-oscura-26-anos/abel_pompeya_italia_a_punto_de_arruinarse.jpg', "Hasta que un día YouTube me cerró todas las cuentas.",
     ["De más de cinco cifras al mes a cero, debiendo 3.500 € a Hacienda. Al poco, se acabó mi relación.",
      "Fue como caer en un pozo. Todo lo que me había creído de mi vida se derrumbó de golpe."], {}),
    (F + '12-familia-no-reels/con_su_madre_dia_antes_de_irse_a_australia.jpg', "Sin nada, le pedí dinero a mi madre y me fui solo a Australia.",
     ["Sin inglés, a 17.000 km de casa.",
      "No era un viaje. Sentía que si no me iba, me moría."], {}),
    (G + 'reparando_teles_70kg.png', "Al tercer día ya descargaba palés de 30 kilos.",
     ["Luego reparé teles de 70 kilos, fui obrero, camarero, Uber… hasta 70 horas a la semana. Allí nadie sabía quién había sido yo.",
      "Y por primera vez en mi vida, me daba igual lo que pensaran de mí."], {}),
    (G + 'llorando_australia.png', "Y un día hice lo que llevaba toda la vida evitando:",
     ["me grabé contando en YouTube cómo estaba sobreviviendo a Australia. Sin guion, sin careta. Llorando.",
      "Después de 20 años diciendo que todo iba bien, por fin dejaba que me vieran de verdad."], {'foco': [0.55, 0.6]}),
    (F + '08-australia/abel_moto_roja_australia.jpg', "En una moto que perdía aire, bajo la lluvia, era más feliz que con 17.000 € al mes.",
     ["Toda la vida buscando el éxito fuera… y lo que me faltaba era estar bien conmigo.",
      "Ahí entendí que a la gente no le importa tanto lo que haces. Le importa quién eres."], {}),
    (F + '10-segundo-fondo-y-sanacion/abel_segundo_fondo_mal_estado_fisico.jpg', "Al volver, toqué fondo otra vez.",
     ["Me di cuenta de que me había ido a Australia huyendo. Y de que en mis vídeos copiaba la forma de hablar de alguien a quien admiraba.",
      "Seguía llevando una careta. Solo que ahora era la de otro."], {}),
    (F + '10-segundo-fondo-y-sanacion/abel_llorando_sesion_sanacion.jpg', "Así que me tocó mirar dentro de verdad:",
     ["terapia, conciencia y, este último año, con todo el respeto, psilocibina.",
      "Entendí el para qué de todo lo que había vivido. Y desde entonces solo digo lo que siento. A quien le guste, bien. Y a quien no, también."], {}),
    (F + '11-ahora/abel_pizarra_ego_emocion.jpg', "Hoy hago lo que me obsesionaba de niño: entender a las personas.",
     ["Ayudo a emprendedores a llenar su agenda con su marca personal siendo ellos mismos, y he acompañado a marcas a facturar más de 10.000 € al mes.",
      "Porque lo más importante de un negocio es la persona que hay detrás. Y casi todo lo que sé lo regalo en mi canal de YouTube."], {}),
    (G + 'grabando_empezar_desde_0.png', "Por qué publico:",
     ["porque durante años me escondí detrás de un canal sin mi cara, y sé lo que cuesta dar el paso.",
      "No quiero enseñarte a copiar a nadie. Quiero enseñarte a vender siendo tú. *Autenticidad que vende*."], {}),
    (F + '01-infancia/abel_nino_gorro_blanco_negro.jpg', "Un niño diciendo «todo va bien» llorando. Un vídeo en la tele de un bar. Un canal sin mi cara.",
     ["Ahí empecé.",
      "Si hoy te escondes detrás de tu negocio, no vas tarde. Estás *al principio*."], {}),
]

DESCRIPCION = """Durante años sentí que no era suficiente.

Con 10 años, el día que el juez decidió que nos íbamos a 800 km, miré a mi madre y le dije: «Perfecto, todo está bien». Llorando. Ahí aprendí a tragarme lo que sentía.

Me escondí detrás de una pantalla: videojuegos, canales, negocios por internet. Con 18 di la cara por primera vez, pusieron uno de mis vídeos en la tele de un bar de mi pueblo y no supe sostenerlo. Con 20 estuve a punto de quitarme la vida y nadie lo supo. Con 25 facturaba 17.000 € al mes con un canal en el que no salía yo. Por fin sentía que valía algo… pero solo por el dinero.

Lo perdí todo en un día.

Y en Australia, solo, cargando palés y reparando teles, me grabé llorando y dejé que me vieran de verdad por primera vez. Ahí empezó todo.

Hoy ayudo a emprendedores a llenar su agenda siendo ellos mismos. Porque sé lo que es esconderse detrás de un negocio, y sé que lo más importante de un negocio es la persona que hay detrás.

Si hoy te escondes, no vas tarde. Estás al principio ❤️

#marcapersonal #emprendedores #autenticidad"""

assert len({f for f, *_ in D}) == len(D) == 20, 'foto repetida o no son 20'
c = {'salida': SALIDA, 'descripcion': DESCRIPCION,
     'diapositivas': [dict(foto=f, titular=t, lineas=l, **o) for f, t, l, o in D]}
json.dump(c, open(AQUI / 'mi_historia_v9.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('ok', len(D))
