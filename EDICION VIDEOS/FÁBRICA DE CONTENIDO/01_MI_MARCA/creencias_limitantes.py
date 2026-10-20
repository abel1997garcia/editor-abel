"""Genera CREENCIAS-LIMITANTES-A-NECESARIAS.md/.pdf.

CRITERIO (Abel 18/10/2026):
- Una creencia limitante es el DIÁLOGO INTERNO negativo de la persona: lo que da por verdad sobre sí misma, lo que
  merece, lo que es capaz de conseguir, cómo funciona la vida, los demás y su entorno, el amor, el dinero o Dios.
  Dicha como la diría de verdad («yo tengo mala suerte», «valgo lo que tengo»). NO es un hábito («comer me calma»)
  ni una costumbre («mi tiempo es para los demás»).
- La necesaria, dicha como ABEL a un amigo (Abel 18/10/2026): directa, sincera, algo polémica, en UNA frase.
- Mejor pocas y buenas que muchas.
- Que suene humano (VOZ-DEL-CLIENTE.md): como se dice en un bar, palabras de la calle. La necesaria, como la diría esa
  persona un día que está algo mejor. Nada de frase de taza: sin antítesis bonitas ni punto y coma.
Lente de Abel: emociones bajas → energía baja → autoestima baja.   python creencias_limitantes.py
"""
from pathlib import Path
from pdf_marca import a_pdf

# [AMBOS] = sirven también para la parte de marca personal y negocio (el 20 %, siempre mezclado con la autoestima; Abel 18/10/2026)
AMBOS = {'Valgo lo que tengo.', 'Si no hago las cosas bien, no valgo.', 'Yo no sirvo para eso.', 'Eso es para otros, no para alguien como yo.', 'Ya es tarde para mí.', 'No soy lo bastante listo.', 'Siempre empiezo las cosas y nunca las acabo.', 'Para qué lo voy a intentar, si va a salir mal.', 'Para qué voy a pedir más, si no me lo van a dar.', 'Me miran y piensan que soy un desastre.', 'Tengo que caerle bien a todo el mundo.', 'Cuando gane más, estaré bien.', 'Si no tengo éxito, no soy nadie.', 'El dinero no es para la gente como yo.', 'Gastarme dinero en mí es tirarlo.', 'Si gano más, me respetarán más.', '¿Quién soy yo para enseñar esto?', 'Si cobro más, pensarán que soy un vendehumos.', 'Lo mío no le interesa a nadie.', 'Si me muestro, me van a criticar.'}


def tag(a):
    return a + (' [AMBOS]' if a in AMBOS else '')

AQUI = Path(__file__).resolve().parent

C = {
'1 · Lo que piensan de sí mismos': [
 ('Es que soy un inútil, no hago nada bien.', 'No eres un inútil, solo te fijas en lo que te sale mal y lo bueno ni lo ves.'),
 ('Valgo lo que tengo.', 'Si mañana te quedas sin nada, sigues siendo tú; lo que tienes no es lo que vales.'),
 ('Si no hago las cosas bien, no valgo.', 'La vas a cagar mil veces y vas a seguir valiendo lo mismo; lo que te hunde no es el fallo, es cómo te machacas después.'),
 ('Tengo 35 años y he fracasado en la vida.', 'Te han salido cosas mal, como a todos; fracasar de verdad es quedarte llorándolo toda la vida.'),
 ('Algo malo tengo, porque a los demás no les pasa.', 'No tienes nada malo, tienes cosas que te dolieron y que nunca has querido mirar.'),
 ('Yo soy así y no voy a cambiar.', 'No eres así, llevas años haciéndolo igual, que no es lo mismo.'),
 ('Me miro al espejo y me doy asco.', 'Tu cuerpo te ha aguantado todo lo que le has hecho; empieza por dejar de tratarlo como a un enemigo.'),
 ('Si me conocieran de verdad, saldrían corriendo.', 'Quien salga corriendo al conocerte entero te está haciendo un favor; el que se quede, ese vale.'),
 ('Me quiero más bien poco.', 'No hace falta que te quieras mucho mañana, empieza hoy por dejar de machacarte.'),
 ('Soy un rollo, la gente se aburre conmigo.', 'No eres un rollo, estás con gente con la que no conectas.'),
],
'2 · Lo que creen que merecen': [
 ('No me merezco nada bueno.', 'Te mereces lo mismo que cualquiera; lo que pasa es que te has acostumbrado a las migajas.'),
 ('Me lo tengo merecido.', 'Nadie se merece sentirse así, y tú tampoco, por mucho que te lo hayas creído.'),
 ('Si alguien me trata bien, algo querrá.', 'Hay gente que te trata bien porque sí; si desconfías de todo el que te quiere, te vas a quedar solo.'),
 ('Con lo que tengo, ya debería estar contento.', 'Puedes estar agradecido y querer más a la vez; una cosa no quita la otra.'),
 ('Para qué voy a pedir más, si no me lo van a dar.', 'Si no lo pides, seguro que no te lo dan.'),
 ('Si me va bien, ya vendrá el palo.', 'Si te va bien, disfrútalo; esperar el palo es la forma más rápida de que llegue.'),
 ('No me he ganado descansar.', 'Descansar no es un premio, es lo que te deja seguir; si no paras tú, te para el cuerpo.'),
],
'3 · Lo que creen que pueden conseguir': [
 ('Yo no sirvo para eso.', 'No lo has hecho nunca, que no es lo mismo que no servir.'),
 ('Eso es para otros, no para alguien como yo.', 'Los que lo consiguieron no eran mejores que tú, simplemente empezaron.'),
 ('Ya es tarde para mí.', 'Mientras sigas aquí, no es tarde; tarde es lo que te dices para no empezar.'),
 ('No soy lo bastante listo.', 'No te falta cabeza, te falta creértelo.'),
 ('Siempre empiezo las cosas y nunca las acabo.', 'Lo dejas cuando te vienes abajo; cuida cómo te sientes y verás cómo acabas lo que empiezas.'),
 ('Para qué lo voy a intentar, si va a salir mal.', 'Si no lo intentas, ya ha salido mal.'),
 ('Lo mío no tiene arreglo.', 'Lo tuyo tiene arreglo, lo que pasa es que nadie te ha enseñado a arreglarlo desde dentro.'),
 ('Yo solo no puedo, y pedir ayuda me da vergüenza.', 'Solo no has podido en años; pedir ayuda no es de débiles, es de quien ya se ha cansado de dar vueltas.'),
],
'4 · Lo que creen de la vida': [
 ('Yo es que tengo mala suerte.', 'No tienes mala suerte, tienes la energía por los suelos, y desde ahí todo te parece un castigo.'),
 ('¿Por qué siempre me pasa todo a mí?', 'Si siempre te pasa lo mismo, no es la vida, es algo que llevas dentro y que se repite.'),
 ('Mi vida va cuesta abajo y sin frenos.', 'Estás en un mal momento, no en una mala vida; no confundas una etapa con lo que eres.'),
 ('Unos nacen con estrella y otros estrellados.', 'No naciste estrellado, aprendiste a vivir así, y lo que se aprende se cambia.'),
 ('La vida es aguantar.', 'Llevas años aguantando; ya va siendo hora de vivir un poco.'),
 ('Ser feliz no es para mí.', 'Ya has sido feliz alguna vez, así que sabes que puedes.'),
 ('Lo mejor de mi vida ya pasó.', 'Lo mejor no ha pasado, es que desde donde estás ahora no lo ves.'),
 ('Esto es lo que hay.', 'Esto es lo que hay hoy; mañana depende de lo que hagas con lo que sientes.'),
],
'5 · Lo que creen de los demás y del entorno': [
 ('La gente al final siempre te falla.', 'Te han fallado unos cuantos, no todo el mundo; no pagues con los nuevos lo que te hicieron los de antes.'),
 ('Todos tienen la vida resuelta menos yo.', 'Estás comparando tu por dentro con el escaparate de los demás, y así siempre pierdes.'),
 ('Me miran y piensan que soy un desastre.', 'La mayoría ni se fija en ti, bastante tienen con lo suyo.'),
 ('Si digo que no, se van a enfadar.', 'Si alguien se enfada porque dices que no, ya sabes cuánto le importas.'),
 ('Tengo que caerle bien a todo el mundo.', 'No le vas a caer bien a todo el mundo, y menos mal, porque te volverías loco intentándolo.'),
 ('Si me alejo de esta gente, me quedo solo.', 'Mejor solo un tiempo que mal acompañado toda la vida.'),
 ('En mi familia nunca me van a entender.', 'Puede que no te entiendan nunca, y aun así tú te puedes entender.'),
 ('Si cuento cómo estoy, voy a ser una decepción.', 'Quien te quiere prefiere saber cómo estás de verdad que verte fingir.'),
],
'6 · Lo que creen del amor': [
 ('Nadie me va a querer así.', 'Te van a querer así, pero primero deja de esconder cómo eres.'),
 ('A poco que me den, yo lo doy todo.', 'Darlo todo a cambio de migajas no es amor, es miedo a que te dejen.'),
 ('Todos tienen pareja menos yo.', 'Estar solo ahora no significa estar solo siempre; mejor eso que estar con cualquiera.'),
 ('Si me ha dejado, es porque no valgo.', 'Se ha acabado, nada más; eso no dice nada de lo que vales.'),
 ('Siempre me fijo en quien no me hace caso.', 'Te fijas en quien te ignora porque es lo que conoces desde pequeño; eso se cambia.'),
 ('Al final todos se cansan de mí.', 'Quien se cansa de ti no era para ti.'),
 ('Más vale esto que estar solo.', 'Estar solo da miedo, pero estar mal acompañado te consume.'),
 ('Si me enfado, me deja.', 'Si alguien se va porque te enfadas, no te quería a ti, quería que no molestaras.'),
],
'7 · Lo que creen del dinero, el trabajo y el éxito': [
 ('¿Quién soy yo para enseñar esto?', 'Eres alguien que ya ha pasado por donde otros están ahora; con eso basta.'),
 ('Si cobro más, pensarán que soy un vendehumos.', 'El que piensa eso no te iba a pagar igual; cobra lo que vale lo que haces.'),
 ('Lo mío no le interesa a nadie.', 'Lo que has vivido le puede servir a alguien que hoy está como tú estabas, pero si no lo enseñas, nunca lo sabrá.'),
 ('Si me muestro, me van a criticar.', 'Te van a criticar igual, así que mejor que sea siendo tú.'),
 ('Cuando gane más, estaré bien.', 'Yo ganaba 17.000 € al mes y me sentía vacío; el dinero no arregla lo que sientes.'),
 ('Si no tengo éxito, no soy nadie.', 'Eres alguien con éxito y sin él; si no, cuando se acabe el éxito, se acaba también tu valor.'),
 ('El dinero no es para la gente como yo.', 'Al dinero le da igual de dónde vienes; lo que te frena es lo que te dices.'),
 ('Gastarme dinero en mí es tirarlo.', 'Te gastas dinero en el móvil, en el coche y en salir; si en ti no, es porque no crees que lo valgas.'),
 ('Si gano más, me respetarán más.', 'Quien te respeta por lo que ganas no te respeta a ti.'),
],
'8 · Lo que creen de Dios, del destino y de lo espiritual': [
 ('Dios se ha olvidado de mí.', 'No estás solo; lo que pasa es que llevas tanto tiempo sin parar que no lo notas.'),
 ('¿Qué he hecho yo para merecer esto?', 'No has hecho nada para merecerlo; te ha pasado, y puedes salir.'),
 ('Estaré pagando algo, porque esto no es normal.', 'No estás pagando nada, estás en un mal momento, y se puede cambiar.'),
 ('Si fuera más espiritual, no me pasaría esto.', 'La gente espiritual también lo pasa mal; la diferencia es cómo lo vive.'),
 ('Lo espiritual es para gente rara.', 'Lo espiritual es cómo te hablas cuando nadie te escucha; de raro, nada.'),
 ('Lo de la energía es una tontería.', 'Hay gente que te deja vacío y gente que te llena; eso es energía, lo llames como lo llames.'),
 ('Los que se fueron ya no están.', 'Ya no los ves, pero lo que te dieron lo llevas encima.'),
],
'9 · Lo que creen de sus emociones': [
 ('Si me pongo a pensar, me hundo.', 'Si no lo miras, te hundes igual, solo que más despacio.'),
 ('Llorar es de débiles.', 'Débil es seguir tragándotelo hasta que revientes por cualquier tontería.'),
 ('Tengo que poder con todo.', 'No puedes con todo, y no pasa nada por decirlo.'),
 ('Lo mío no es para tanto, hay gente peor.', 'Que haya gente peor no quita que tú estés mal.'),
 ('Si cuento lo que me pasa, molesto.', 'A quien te quiere no le molesta saber cómo estás; al que le molesta, ya sabes.'),
 ('Mejor no pensarlo y tirar.', 'Tirar sin mirarlo es lo que te ha traído hasta aquí.'),
],
'10 · Lo que creen de su pasado': [
 ('Lo que viví de pequeño me ha jodido la vida.', 'Te marcó, pero no tiene por qué decidir lo que haces a partir de hoy.'),
 ('Fue culpa mía.', 'Eras un niño; no era culpa tuya.'),
 ('Mis padres tienen la culpa de cómo soy.', 'Hicieron lo que supieron; lo que hagas ahora ya es cosa tuya.'),
 ('No puedo perdonar.', 'Perdonar no es darles la razón, es dejar de cargarlo tú.'),
 ('He tirado mi vida.', 'Has perdido años, sí, pero te quedan muchos más que perder si sigues igual.'),
 ('En mi familia todos somos así.', 'Pues sé el primero de tu casa que lo hace distinto.'),
],
'11 · Lo que creen del cambio': [
 ('La gente no cambia.', 'Tú ya has cambiado otras veces; lo que no cambia es quien no quiere mirarse.'),
 ('Esto va para años.', 'Hay cosas que tardan, pero empezar a sentirte mejor depende de cuánto estés dispuesto a hacer.'),
 ('Ya lo he probado todo.', 'Has probado mil cosas por fuera; lo de dentro no lo has tocado.'),
 ('Cuando esté bien, empiezo a vivir.', 'Empieza a vivir y ya te irás poniendo bien por el camino.'),
 ('Si cambio, voy a perder a gente.', 'Si alguien se va porque estás mejor, no te quería tanto.'),
 ('Pedir ayuda es de débiles.', 'Débil es seguir igual por orgullo; pedir ayuda es de valientes.'),
 ('Pensar en mí es ser egoísta.', 'Si tú estás bien, los que tienes al lado lo notan; egoísta es obligarles a cargar contigo mal.'),
 ('Lo de la autoestima es humo.', 'Humo son las frases bonitas; sentirte distinto contigo no lo es.'),
 ('Me gustaría arreglarlo solo, pero llevo así años.', 'Si en años solo no lo has arreglado, igual toca dejar que te acompañen.'),
],
'12 · Lo que creen de mostrarse y de vivir de lo suyo': [
 ('Tengo que tenerlo todo perfecto antes de publicar.', 'Perfecto no publica nadie; sube lo de hoy y mañana lo haces mejor.'),
 ('Mi cara y mi voz en vídeo dan pena.', 'Te ves raro porque no estás acostumbrado a verte; la gente no mira tu cara, escucha lo que dices.'),
 ('Si lo ve mi familia, qué vergüenza.', 'Tu familia ya opina de todo lo que haces; que opine también de algo que te hace feliz.'),
 ('Ya hay mucha gente hablando de esto.', 'Hay mucha gente, pero nadie con tu historia, y a ti te va a escuchar quien vivió lo mismo.'),
 ('Sin seguidores no vale la pena.', 'Todos empezaron con cero; los seguidores vienen de seguir publicando, no al revés.'),
 ('Cobrar por ayudar está mal.', 'Si ayudas de verdad, cobrar es lo que te deja seguir ayudando.'),
 ('Lo dejo porque no funciona.', 'No funciona porque lo dejas; en tres semanas nadie ve nada.'),
 ('Primero tengo que estar bien yo para enseñar a otros.', 'Enseñas lo que ya has pasado, no hace falta haber llegado a todo.'),
],
'13 · Lo que creen de la confianza, la energía y sus pensamientos': [
 ('Seguro se nace.', 'Nadie nace seguro; los que lo parecen han hecho el ridículo más veces que tú.'),
 ('La confianza se tiene o no se tiene.', 'La confianza sube cada vez que haces lo que te dijiste que ibas a hacer.'),
 ('Estoy cansado porque trabajo mucho.', 'Cansa más lo que aguantas que lo que trabajas.'),
 ('Cuando tenga energía, empiezo.', 'La energía viene de empezar, no al revés.'),
 ('No puedo controlar lo que pienso.', 'No eliges lo primero que te viene a la cabeza, pero sí quedarte ahí dándole vueltas.'),
 ('Tengo que pensar en positivo.', 'No hace falta pensar en positivo, hace falta dejar de tapar lo que sientes.'),
 ('Soy negativo, siempre lo he sido.', 'No eres negativo, llevas años rodeado de lo que te baja.'),
 ('Lo de la vibración es cosa de hippies.', 'Llámalo como quieras: hay cosas que te dejan con ganas y cosas que te dejan vacío, y eso lo notas.'),
 ('Si me siento mal, es que algo va mal en mí.', 'Sentirte mal no es estar roto, es algo que te pide que lo mires.'),
 ('Cuando todo se arregle, me sentiré bien.', 'Primero te sientes mejor y luego se van arreglando las cosas.'),
],
}
AMBOS |= dict(C['12 · Lo que creen de mostrarse y de vivir de lo suyo']).keys()


def main():
    total = sum(len(v) for v in C.values())
    intro = [
        f'{total} creencias en {len(C)} familias. A la izquierda, el diálogo interno que frena a la persona; a la derecha, lo que necesita llegar a creer, dicho como se lo diría Abel a un amigo: directo y sin rodeos.',
        'Lente de Abel: emociones bajas → energía baja → autoestima baja. Lo de fuera (complacer, engancharse, buscar el valor fuera) es la consecuencia.',
        '[AMBOS] = también sirve para la parte de marca personal y negocio, siempre mezclada con la autoestima (80 % desarrollo personal, 20 % marca personal). Cómo usarlo: en reels, la limitante es el gancho con connotación negativa y la necesaria la solución; en stories (AYUDAR), una al día; en carruseles y guiones, la objeción que se rompe. Lo clínico se deriva a un profesional.',
    ]
    md = ['# Creencias limitantes → creencias necesarias · Abel García', ''] + [p + '\n' for p in intro]
    n = 0
    for blq, lst in C.items():
        md += [f'## {blq}', '', '| # | Creencia limitante | Creencia necesaria |', '|---|---|---|']
        for a, b in lst:
            n += 1; md.append(f'| {n} | {tag(a)} | {b} |')
        md.append('')
    (AQUI / 'CREENCIAS-LIMITANTES-A-NECESARIAS.md').write_text('\n'.join(md), encoding='utf-8')
    a_pdf(AQUI / 'CREENCIAS-LIMITANTES-A-NECESARIAS.pdf', 'Creencias limitantes → necesarias', 'Especialista en Autoestima · Espiritualidad que funciona', intro, [(k, [(tag(a), b) for a, b in v]) for k, v in C.items()], tabla=True)
    print('ok', total, len(C))


if __name__ == '__main__':
    main()
