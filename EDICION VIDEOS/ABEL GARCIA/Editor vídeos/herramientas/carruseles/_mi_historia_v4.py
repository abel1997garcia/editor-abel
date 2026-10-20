"""Genera mi_historia.json (v6, 13/10/2026). Como Jun Yuh: cada momento DEMUESTRA lo que vende Abel, «autenticidad que vende».
Hilo: de ESCONDERSE (el «todo está bien», la burbuja, Gael Blog en la tele del bar, los 17.000 € sin salir él, los «ingresos pasivos»)
a DAR LA CARA (el vídeo llorando en Australia, dejar de copiar, decir lo que siente). Cierre: «lo más importante de un negocio es la
persona que hay detrás». Orden de los hechos según la línea de tiempo corregida por Abel (memoria fotos-vida-abel)."""
import json
from pathlib import Path

AQUI = Path(__file__).resolve().parent
F = 'C:/Users/Clap/Desktop/EDICION VIDEOS/ABEL GARCIA/Editor vídeos/MarcaPersonal/FOTOS MIAS/'
G = str(AQUI / 'fotogramas') + '/'

D = [
    (F + '06-noche-oscura-26-anos/abel_cumpleanos_26_noche_oscura_del_alma.jpg', "En esta foto parezco feliz,",
     ["pero mi madre me la hizo después de verme hora y media llorando sin parar.",
      "Tres días antes me había arruinado, después de años construyendo un negocio en el que nunca enseñé la cara. Si acabas de llegar, no conoces la historia…"], {}),
    (F + '12-familia-no-reels/leon_con_su_madre_antes_y_despues_18_anos.jpg', "Mis padres se separaron cuando yo tenía 7 años,",
     ["y mientras mi madre se mataba a trabajar para sacarme adelante, yo pasaba los días con cuidadoras en Boñar, mi pueblo de León.",
      "Me cuidaban bien… pero me sentía solo, y no sabía ni explicarlo."], {}),
    (F + '01-infancia/abel_11_anos_descenso_del_sella_asturias.jpg', "Con 10 años me sentaron delante de un juez para elegir entre mi padre y mi madre.",
     ["Me quedé con ella y nos fuimos a Castelldans, a 800 km de todo. El primer año sufrí bullying.",
      "Y a mi madre le decía que todo iba bien, para no ser otro problema."], {}),
    (F + '01-infancia/abel_bebe_con_su_abuelo.jpg', "Y en medio de todo eso, perdí a mi abuelo,",
     ["la persona con la que más conectaba: el que me subía a su moto roja, me enseñaba a pescar y asaba castañas conmigo.",
      "Murió en 2009, cuando yo tenía 12 años, y a 800 km no pude despedirme de él. Me pasé años sintiéndome culpable."], {}),
    (G + 'nino_sofa_consola_plano.png', "Así que me encerré en mi burbuja: los videojuegos.",
     ["Horas y horas, porque era el único sitio donde no tenía que sentir nada.",
      "Con 15 años hasta creé mi propio canal de Minecraft. No para ganar dinero: para tener un mundo donde esconderme del de verdad."], {'foco': [0.45, 0.5]}),
    (F + '03-canal-gael-blog/canal_gael_blog_como_dejar_de_ser_vago.jpg', "Con 18 años me atreví por primera vez a dar la cara,",
     ["en un canal de crecimiento personal, después de probar Facebook Ads, dropshipping y tiendas online siempre detrás de una pantalla.",
      "Hasta que en mi pueblo pusieron uno de mis vídeos en la tele de un bar y se enteró todo el mundo. No supe sostenerlo."], {'foco': [0.58, 0.5]}),
    (F + '02-antes-de-despertar/abel_fiesta_noche_tumbado.jpg', "Y me volví a esconder, esta vez en la fiesta.",
     ["Veranos enteros saliendo de miércoles a domingo, cubatas, tragaperras… buscando no sentir el vacío que llevaba dentro.",
      "Una noche perdí 2.100 € apostando por internet a partidos de ping-pong, a las 3 de la mañana."], {}),
    (F + '02-antes-de-despertar/abel_fiesta_mayor_capa_rosa.jpg', "Y con 20 años estuve a punto de quitarme la vida.",
     ["Nadie lo supo. Todo el mundo me preguntaba si estaba bien, y yo sonreía, decía que sí y seguía saliendo de fiesta.",
      "Igual que con 10 años. Pero algo dentro de mí me dijo que no lo hiciera."], {}),
    (F + '12-familia-no-reels/graduacion_carrera_con_su_padrastro.jpg', "Por fuera, todo en orden: acabé la carrera de ADE.",
     ["Por dentro, fui a psicólogos y a terapias. Entendía por qué me pasaba todo… pero seguía sintiéndome exactamente igual.",
      "Y de negocios, mucha teoría y ninguna experiencia."], {}),
    (F + '04-canal-clap/abel_funda_movil_canal_clap.jpg', "En la pandemia me encerré a hacer un vídeo de Clash Royale al día,",
     ["después de dos meses en una oficina con 400 personas pensando: «¿Qué cojones hago aquí?». Me compré el curso de Romuald Fons para hacerlo mejor.",
      "Llegué a 30.000 suscriptores… y a 200 € al mes. Ahí entendí que tener audiencia no es lo mismo que tener un negocio."], {}),
    (F + '05-canal-automatizacion-ganaba-dinero/abel_placa_100k_suscriptores_youtube.jpg', "Y con 25 años, lo conseguí:",
     ["un canal de 100.000 suscriptores que facturaba 17.000 € al mes. Me ofrecieron 550.000 € por él y los rechacé.",
      "Pero en ese canal no salía yo. No me sentía suficiente para enseñarme a 100.000 personas."], {'foco': [0.5, 0.56], 'columna': 'der'}),
    (F + '05-canal-automatizacion-ganaba-dinero/abel_menorca_paseo_costa.jpg', "Viajes, pareja, libertad… y lo llamaba «ingresos pasivos».",
     ["En realidad era esconderme: si no me exponía, nadie me podía criticar ni ver quién era de verdad.",
      "Por dentro seguía siendo el niño que decía que todo iba bien."], {}),
    (F + '06-noche-oscura-26-anos/abel_pompeya_italia_a_punto_de_arruinarse.jpg', "Hasta que un día YouTube me cerró todas las cuentas.",
     ["De más de cinco cifras al mes a cero, debiendo 3.500 € a Hacienda. Todo dependía de algo que no era mío… ni era yo.",
      "Al poco se acabó mi relación. Y así llegué al cumpleaños de la primera foto."], {}),
    (F + '12-familia-no-reels/con_su_madre_dia_antes_de_irse_a_australia.jpg', "Sin nada, le tuve que pedir dinero a mi madre para irme a Australia.",
     ["Solo, sin apenas inglés, a 17.000 km de casa. Sentía que si no me iba, me moría.",
      "Al tercer día ya estaba cargando palés de cajas de 30 kilos. Allí nadie sabía quién había sido yo."], {}),
    (G + 'llorando_australia.png', "Y allí, por primera vez, di la cara de verdad.",
     ["Me grabé contando en YouTube cómo estaba sobreviviendo a Australia. Sin guion, sin careta. Llorando.",
      "Después de toda una vida diciendo que todo iba bien, por fin decía la verdad."], {'foco': [0.55, 0.6]}),
    (F + '08-australia/abel_moto_roja_australia.jpg', "Un día, parado en un semáforo bajo una tromba de agua,",
     ["en una moto de 50 cc que perdía aire por la rueda de delante, me di cuenta de que estaba disfrutando como un niño.",
      "Toda la vida persiguiendo el éxito… y era feliz ahí."], {}),
    (F + '09-sudeste-asiatico/abel_mochila_viajando_solo_asia.jpg', "Antes de volver, me fui mes y medio solo por el sudeste asiático.",
     ["Tailandia, Bali, Vietnam, Camboya… conocí a muchísima gente y culturas que llevaban siglos hablando de lo que yo estaba descubriendo.",
      "Volví a casa por sorpresa, convencido de que ya lo había entendido todo."], {}),
    (F + '10-segundo-fondo-y-sanacion/abel_segundo_fondo_mal_estado_fisico.jpg', "Pero en Lérida toqué fondo otra vez,",
     ["porque me di cuenta de que me había ido a Australia huyendo, no sanando.",
      "Y me puse otra vez a montar cosas detrás de una pantalla: automatizaciones con IA, una app, hasta un bot de trading."], {}),
    (F + '10-segundo-fondo-y-sanacion/abel_llorando_sesion_sanacion.jpg', "Así que me tocó mirar dentro de verdad.",
     ["Terapia, conciencia y, este último año, con todo el respeto, psilocibina. Ahí vi que hasta en mis vídeos copiaba la forma de hablar de alguien a quien admiraba.",
      "Me llovía el hate por cosas que ni pensaba. Desde entonces solo digo lo que siento, aunque no le guste a todo el mundo."], {}),
    (F + '11-ahora/abel_pizarra_ego_emocion.jpg', "Por eso hoy ayudo a emprendedores a llenar su agenda dando la cara:",
     ["sin caretas, sin copiar a nadie, con su historia y su intención por delante. Porque lo más importante de un negocio es la persona que hay detrás.",
      "Y si hoy tú también dices que todo va bien… no estás al final. Estás *al principio*."], {}),
]

assert len({f for f, *_ in D}) == len(D) == 20, 'foto repetida o no son 20'
c = json.load(open(AQUI / 'mi_historia.json', encoding='utf-8'))
c['diapositivas'] = [dict(foto=f, titular=t, lineas=l, **o) for f, t, l, o in D]
json.dump(c, open(AQUI / 'mi_historia.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('ok', len(D))
