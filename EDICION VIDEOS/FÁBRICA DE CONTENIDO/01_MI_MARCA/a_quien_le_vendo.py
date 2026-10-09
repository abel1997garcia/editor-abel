"""Genera A-QUIEN-LE-VENDO.pdf (y .md): 200 descripciones de a quién le vende Abel, por situación.
Cada una = qué hace mal la persona (connotación negativa) + lo que le está costando. Todas apuntan a la frase central.
    python a_quien_le_vendo.py
"""
import json, subprocess, html
from pathlib import Path

AQUI = Path(__file__).resolve().parent
FRASE = 'Te enseño a sanar tus emociones para que dejen de sabotear tu propia vida.'

B = {
'1 · Saben lo que tienen que hacer y se sabotean igual': [
 'Personas que se prometen cada domingo que el lunes empiezan, y el miércoles ya han vuelto a lo mismo sin entender por qué.',
 'Personas que llevan meses intentando dejar el porno y recaen justo cuando peor se sienten, y luego se machacan como si fueran débiles.',
 'Personas que cogen el móvil «cinco minutos» antes de dormir y a la una de la mañana siguen haciendo scroll con un vacío que no saben nombrar.',
 'Personas que abren la nevera a las once de la noche sin hambre, porque comer es lo único que les calma algo que no quieren mirar.',
 'Personas que dejan un vicio y a las dos semanas lo han cambiado por otro, porque lo que había debajo sigue intacto.',
 'Personas que apuestan «solo un poco» para sentir algo, y luego esconden lo que han perdido a quien tienen al lado.',
 'Personas que salen de fiesta para desconectar y se pasan el domingo con una resaca que ya no es solo física.',
 'Personas que tienen la lista perfecta de hábitos en el móvil y no cumplen ni la mitad, y cada fallo les confirma que no pueden fiarse de sí mismas.',
 'Personas que confunden disciplina con apretar los dientes, y por eso cada racha buena termina en un atracón de lo que se estaban prohibiendo.',
 'Personas que se pasan el día con una serie de fondo para no quedarse a solas con lo que piensan.',
 'Personas que fuman «porque les relaja» y nunca se han preguntado qué es exactamente lo que necesitan relajar.',
 'Personas que juegan horas a la consola para no pensar, igual que hacían de niños cuando en casa las cosas iban mal.',
 'Personas que llevan años diciendo «yo soy así» para no tener que mirar de dónde viene lo que hacen.',
 'Personas que se esconden cuando pierden el control, y esa vergüenza les pesa más que el propio descontrol.',
 'Personas que creen que su problema es la falta de fuerza de voluntad, cuando es una emoción pidiendo salida por el único canal que le dejan abierto.',
 'Personas que empiezan con todo un proyecto, un gimnasio o una dieta, y lo abandonan en cuanto deja de dar resultados rápidos.',
 'Personas que han dejado de confiar en su propia palabra porque llevan años rompiéndola en silencio.',
 'Personas que se tumban en la cama sin poder levantarse, no por pereza, sino por algo que llevan cargando mucho tiempo.',
 'Personas que se llenan la agenda de cosas para no tener ni un minuto de silencio con ellas mismas.',
 'Personas que se juran «esta es la última vez» tantas veces que ya ni ellas mismas se lo creen.',
],
'2 · Pareja y dependencia emocional': [
 'Personas que revisan el WhatsApp cada cinco minutos para ver si la otra persona está en línea y no les ha contestado.',
 'Personas que acaban siempre con el mismo tipo de pareja, con otra cara, y se preguntan por qué les pasa siempre a ellas.',
 'Personas que se callan lo que piensan en la relación para que la otra persona no se vaya, y poco a poco dejan de saber quiénes son.',
 'Personas que no soportan estar solas un fin de semana y saltan de una relación a otra para no sentir el vacío.',
 'Personas que sienten que valen algo solo cuando alguien las elige.',
 'Personas que se ponen celosas por cualquier cosa y luego se avergüenzan de cómo han reaccionado.',
 'Personas que siguen en una relación que les apaga porque les da más miedo quedarse solas que seguir infelices.',
 'Personas que lo dan todo en pareja, ceden en todo, y luego se sienten utilizadas sin entender por qué.',
 'Personas que vuelven una y otra vez con la misma ex o el mismo ex aunque saben que les hace daño.',
 'Personas que miran el perfil de su ex a escondidas meses después y se hunden cada vez que lo hacen.',
 'Personas que necesitan que su pareja les confirme todo el tiempo que les quiere, y nunca es suficiente.',
 'Personas que confunden intensidad con amor y llaman «química» a lo que en realidad es su herida reconociendo otra herida.',
 'Personas que sienten que el rechazo de alguien habla de lo que valen, y se pasan semanas dándole vueltas.',
 'Personas que eligen parejas que no están disponibles y luego se pasan la relación intentando ganarse su amor.',
 'Personas que se anestesian con relaciones rápidas para no tener que estar con lo que sienten.',
 'Personas que no saben poner un límite a su pareja sin sentirse culpables o malas personas.',
 'Personas que han convertido a su pareja en su única fuente de seguridad, y viven con miedo constante a perderla.',
 'Personas que dicen que quieren una relación sana y siguen eligiendo desde la carencia.',
 'Personas que no han superado una ruptura de hace años y siguen comparando a todo el mundo con esa persona.',
 'Personas que sienten que si se muestran como son de verdad, nadie se quedaría.',
],
'3 · Lo consiguen y siguen vacías (dinero, éxito, estatus)': [
 'Personas que ganan buen dinero y siguen sintiendo que no es suficiente, y no saben por qué.',
 'Personas que consiguen una meta, lo celebran un fin de semana y el lunes vuelven a sentir el mismo vacío.',
 'Personas que miran sus métricas, su cuenta o sus resultados de forma compulsiva por miedo a perder lo que tienen.',
 'Personas que compran cosas para sentirse mejor y al día siguiente ya no sienten nada.',
 'Personas que usan su éxito para demostrar a su familia o a su padre que valen, y nunca llega el día en que se lo reconocen.',
 'Personas que creen que «cuando tenga X por fin estaré tranquilas», y llevan años moviendo la meta.',
 'Personas que lo tienen todo por fuera, casa, coche, pareja, trabajo, y por dentro se sienten rotas sin saber explicarlo.',
 'Personas que se han convertido en un robot de productividad y ya no saben disfrutar de nada.',
 'Personas que confunden la calma de cobrar a fin de mes con estar en paz.',
 'Personas que tienen éxito profesional y una vida personal que se les cae a trozos.',
 'Personas que han basado toda su identidad en lo que tienen, y les aterra perderlo porque sentirían que no son nadie.',
 'Personas que presumen de resultados en redes para recibir una validación que dura dos horas.',
 'Personas que trabajan sin parar para no tener tiempo de sentir lo que les pasa.',
 'Personas que creen que el dinero les dará la seguridad que no tuvieron de pequeñas.',
 'Personas que se sienten culpables cuando descansan y lo llaman disciplina.',
 'Personas que han perdido dinero, negocio o trabajo y sienten que con eso han perdido también quiénes son.',
 'Personas que llegaron arriba y descubrieron que el vacío había subido con ellas.',
 'Personas que no se permiten disfrutar de lo que tienen porque siempre falta algo más.',
 'Personas que desconfían de todo lo espiritual porque «no paga facturas», y por eso nunca han mirado lo que les vacía.',
 'Personas que eligieron entre ser ambiciosas o estar en paz, y no están consiguiendo ninguna de las dos.',
],
'4 · Comparación e insuficiencia': [
 'Personas que entran en Instagram y salen sintiéndose peor con su vida, su cuerpo y su dinero.',
 'Personas que se comparan con gente que parece «de otra raza» y esa comparación es justo lo que las mantiene lejos.',
 'Personas que llaman suerte al éxito de otros para no tener que mirar por qué ellas no se mueven.',
 'Personas que en el fondo sienten que no son suficientes, hagan lo que hagan.',
 'Personas que se adaptan tanto para caer bien que ya no saben cómo son cuando no intentan agradar.',
 'Personas que critican a quien tiene éxito porque su éxito les hace sentir menos.',
 'Personas que no se atreven a subir contenido, cantar o emprender por miedo a lo que dirán.',
 'Personas que se sienten un fraude aunque los demás las vean seguras.',
 'Personas que parecen extrovertidas y por dentro viven con miedo a que las descubran.',
 'Personas que siempre sienten que van tarde en la vida respecto a los demás.',
 'Personas que se miran al espejo y solo ven lo que les falta.',
 'Personas que necesitan que alguien les diga que lo están haciendo bien para poder creérselo.',
 'Personas que nunca celebran lo que consiguen porque siempre podría haber sido mejor.',
 'Personas que se exigen tanto que acaban dejando lo que antes amaban, como le pasó a Abel con el fútbol.',
 'Personas que se toman cualquier crítica como un ataque a su valor como persona.',
 'Personas que no piden ayuda porque creen que eso demuestra que no valen.',
 'Personas que viven pendientes de los likes y de cuánta gente las ve.',
 'Personas que creen que si no nacieron con carisma ya no hay nada que hacer.',
 'Personas que se sienten raras o incomprendidas desde pequeñas y han aprendido a esconderlo.',
 'Personas que se tragan lo que sienten para no ser una carga para nadie.',
],
'5 · Viven en piloto automático (trabajo, propósito)': [
 'Personas que odian cinco días de cada siete y lo llaman tener una vida estable.',
 'Personas que viven esperando el viernes, las vacaciones o la jubilación para empezar a vivir.',
 'Personas que se sientan en la oficina, como Abel en su primer trabajo, y sienten un vacío tan grande que no saben qué hacen allí.',
 'Personas que sienten que han venido a hacer algo grande y les aterra estar desperdiciando su vida.',
 'Personas que llevan años diciendo que algún día dejarán ese trabajo y siguen exactamente igual.',
 'Personas que no saben cuál es su propósito y en el fondo temen no tener ninguno.',
 'Personas que eligieron carrera por lo que se esperaba de ellas y no por lo que sentían.',
 'Personas que tienen miedo de dejar lo seguro aunque lo seguro las esté apagando.',
 'Personas que se levantan cansadas todos los días y lo achacan al trabajo, sin mirar qué llevan dentro.',
 'Personas que sienten que su vida es una repetición del mismo día.',
 'Personas que tienen ideas para emprender pero nunca dan el paso porque «no es el momento».',
 'Personas que han estudiado, hecho másteres y cursos, y siguen sin saber qué hacer con su vida.',
 'Personas que sienten que están sobreviviendo, no viviendo.',
 'Personas que se refugian en la rutina para no tener que preguntarse si son felices.',
 'Personas que dejan pasar oportunidades por miedo y luego se arrepienten durante meses.',
 'Personas que sueñan con irse lejos, como hizo Abel a Australia, pero el miedo las paraliza.',
 'Personas que creen que querer más de la vida es de desagradecidos.',
 'Personas que han renunciado a lo que les gustaba de niñas porque «había que ser responsable».',
 'Personas que tienen la sensación constante de estar perdiendo el tiempo.',
 'Personas que no se permiten parar porque si paran tendrían que escucharse.',
],
'6 · Más dolor, más cabeza: ansiedad y pensar sin parar': [
 'Personas cuya cabeza no para ni para dormir, y cuanto peor están, más piensan.',
 'Personas que lo analizan todo mil veces antes de decidir y aun así deciden mal.',
 'Personas que llaman «estrés normal» a su ansiedad porque llamarla ansiedad les daría más miedo.',
 'Personas que se despiertan a las tres de la mañana con un nudo en el estómago y no saben de qué es.',
 'Personas que creen que todo se soluciona pensando, y por eso llevan años en el mismo sitio.',
 'Personas que se adelantan a todo lo que puede salir mal y viven el miedo como si ya estuviera pasando.',
 'Personas que no se fían de lo que sienten y deciden siempre con la lógica, aunque algo les diga «por aquí no».',
 'Personas que se meten en la cabeza para no sentir, sin saber que eso es justo lo que las hace equivocarse.',
 'Personas que dicen que su ansiedad es genética para no tener que hacer nada con ella.',
 'Personas que consumen noticias, true crime o películas de miedo cada día y luego se preguntan por qué viven en alerta.',
 'Personas que no saben estar en silencio cinco minutos sin coger el móvil.',
 'Personas que han tenido ataques de ansiedad y viven con miedo a que vuelvan.',
 'Personas que necesitan entenderlo todo con la cabeza antes de probarlo, y hay cosas que funcionan al revés.',
 'Personas que dicen «no tengo energía» todos los días y nunca se han preguntado de qué están hablando.',
 'Personas que se agobian con todo y creen que el problema son las circunstancias, no lo que llevan dentro.',
 'Personas que controlan cada detalle de su vida porque perder el control les aterra.',
 'Personas que buscan en Google sus síntomas para calmarse y acaban más asustadas.',
 'Personas que llevan una coraza de «a mí nada me afecta» y por dentro están agotadas.',
 'Personas que se tragan la rabia todo el día y luego explotan con quien menos lo merece.',
 'Personas que creen que sentir mucho es un defecto que hay que controlar.',
],
'7 · Lo que vivieron de pequeñas sigue decidiendo por ellas': [
 'Personas que vivieron la separación de sus padres de niñas y todavía hoy sienten que el suelo puede desaparecer en cualquier momento.',
 'Personas que sufrieron bullying y siguen adaptándose a todo el mundo para que no las rechacen.',
 'Personas que de pequeñas decían «todo bien» para no preocupar a nadie y de mayores siguen sin saber pedir ayuda.',
 'Personas que se mudaron muchas veces de niñas y nunca han sentido que pertenecen a ningún sitio.',
 'Personas que perdieron a alguien importante de pequeñas y arrastran una culpa que nunca han mirado.',
 'Personas que crecieron sintiéndose una carga y siguen pidiendo perdón por existir.',
 'Personas que aprendieron que para que las quisieran tenían que portarse bien, y no saben ser ellas mismas.',
 'Personas que llevan toda la vida intentando demostrar a su padre o a su madre que valen.',
 'Personas que creen que su pasado las define para siempre, y esa creencia lo convierte en verdad.',
 'Personas que reaccionan como niñas heridas en discusiones de adultos y luego no entienden por qué.',
 'Personas que nunca vieron una pareja feliz en casa y ahora intentan construir lo que no tuvieron desde el miedo.',
 'Personas que lo que escucharon de niñas sobre el dinero lleva años dirigiendo su vida sin que se den cuenta.',
 'Personas que se refugiaron en los videojuegos, la comida o la soledad de pequeñas y siguen haciendo lo mismo con otros nombres.',
 'Personas que nunca lloraron delante de nadie y ahora no saben llorar ni solas.',
 'Personas que sienten una rabia antigua que no saben de dónde viene.',
 'Personas que tuvieron que hacerse mayores demasiado pronto y ahora no saben disfrutar.',
 'Personas que repiten con sus hijos o su pareja exactamente lo que juraron que nunca harían.',
 'Personas que creen que lo de la infancia ya está superado porque no lo piensan, aunque siga decidiendo por ellas.',
 'Personas que se sienten solas incluso rodeadas de gente, como cuando eran pequeñas.',
 'Personas que nunca se han permitido sentir lo que les pasó, y por eso les sigue pasando.',
],
'8 · Espiritualidad y desarrollo personal que no las cambian': [
 'Personas que llevan años manifestando, meditando y pensando en positivo y su vida sigue exactamente igual.',
 'Personas que ven vídeos de desarrollo personal todos los días y no aplican ni uno.',
 'Personas que han leído cincuenta libros de autoayuda y siguen cayendo en lo mismo.',
 'Personas que usan la espiritualidad para no tomar decisiones incómodas.',
 'Personas que dicen «todo pasa por algo» para no responsabilizarse de su vida.',
 'Personas que se sienten superiores por ser «espirituales» y no se dan cuenta de que es otro ego.',
 'Personas que han hecho cursos, retiros y terapias y siguen buscando el método que por fin las arregle.',
 'Personas que creen que la energía es cosa de flipados y luego hablan de «mala vibra» y corazonadas todos los días.',
 'Personas que han vivido algo que no saben explicar y lo han enterrado para que no las tomen por locas.',
 'Personas que han convertido el desarrollo personal en un hobby o una muleta, en vez de conocerse de verdad.',
 'Personas que fueron al psicólogo, no les sirvió y ahora creen que no tienen remedio.',
 'Personas que visualizan la vida que quieren cada mañana y sienten lo contrario el resto del día.',
 'Personas que quieren manifestar dinero o pareja sin haber sanado lo que les hace sentir que no lo merecen.',
 'Personas que meditan media hora y lo arruinan con dos horas de contenido tóxico por la noche.',
 'Personas que descartan todo lo espiritual por los gurús que flotan, y se han quedado sin lo que había dentro.',
 'Personas que creen que hay que elegir entre ser espiritual o ser ambicioso.',
 'Personas que tienen miedo a la muerte y por eso viven como si tuvieran todo el tiempo del mundo.',
 'Personas que buscan señales del universo para no tener que escucharse a sí mismas.',
 'Personas que entienden perfectamente lo que les pasa y aun así no consiguen cambiarlo.',
 'Personas que se preguntan si su intuición es real o se están inventando una película.',
],
'9 · Complacencia, límites y decir que sí queriendo decir que no': [
 'Personas que dicen que sí a todo para caer bien y luego no tienen tiempo para ellas.',
 'Personas que confunden ser buena persona con no molestar nunca a nadie.',
 'Personas que se tragan lo que les molesta para evitar el conflicto y lo pagan con ansiedad.',
 'Personas que no saben decir que no a sus amigos aunque saben que eso les hace daño, como le pasaba a Abel con la fiesta.',
 'Personas que se conforman con migajas en sus relaciones porque creen que no merecen más.',
 'Personas que dejan que les hablen como ellas nunca le hablarían a nadie.',
 'Personas que sienten culpa cada vez que se eligen a sí mismas.',
 'Personas que siempre están para todo el mundo y nadie está para ellas.',
 'Personas que adornan la verdad para no hacer daño y acaban sin que nadie las conozca de verdad.',
 'Personas que no se atreven a pedir lo que valen en su trabajo.',
 'Personas que cambian de opinión según con quién estén.',
 'Personas que temen que si dicen lo que piensan las dejarán de querer.',
 'Personas que cargan con los problemas de su familia como si fueran suyos.',
 'Personas que se sienten responsables de las emociones de todo el mundo.',
 'Personas que esperan que los demás adivinen lo que necesitan porque no se atreven a decirlo.',
 'Personas que llevan años en un entorno que las apaga y no se van por lealtad.',
 'Personas que se disculpan por todo, incluso por cosas que no han hecho.',
 'Personas que se pasan el día ayudando a otros para no mirar su propia vida.',
 'Personas que no saben recibir un cumplido ni un regalo sin sentirse incómodas.',
 'Personas que creen que poner límites es ser egoísta.',
],
'10 · Quieren crear su propio servicio o proyecto y se bloquean': [
 'Personas que quieren vivir de lo que les apasiona y llevan años sin lanzarse por miedo al qué dirán.',
 'Personas que empiezan un canal, una marca o un negocio con ganas y lo abandonan al primer mes sin resultados.',
 'Personas que quieren ayudar a otros con su historia y no se creen con derecho a hacerlo.',
 'Personas que emprenden para demostrar que valen y viven cada mal mes como un fracaso personal.',
 'Personas que tienen un talento claro y lo esconden porque no se sienten suficientes.',
 'Personas que copian lo que hacen otros en vez de construir desde quiénes son.',
 'Personas que tienen miedo de enseñarse en redes porque les da vergüenza que las vea su entorno.',
 'Personas que se pasan meses preparando el proyecto perfecto y nunca lo publican.',
 'Personas que miran las métricas de su contenido de forma compulsiva y su ánimo depende de ellas.',
 'Personas que han invertido miles de euros en cursos y formaciones sin aplicar casi nada.',
 'Personas que tuvieron éxito con un proyecto, lo perdieron y no se atreven a volver a empezar.',
 'Personas que quieren cobrar por lo que saben y sienten que no lo merecen.',
 'Personas que construyen su negocio desde la carencia y por eso nunca les parece suficiente.',
 'Personas que tienen claro qué quieren crear pero se sabotean justo antes de lanzarlo.',
 'Personas que creen que tienen que tener su vida resuelta antes de poder ayudar a nadie.',
 'Personas que quieren hacer algo propio pero siguen en un trabajo que odian «por si acaso».',
 'Personas que se comparan con los grandes de su sector y se paralizan.',
 'Personas que saben que tienen un mensaje pero no saben cómo convertirlo en un servicio.',
 'Personas que confunden estar ocupadas con avanzar en su proyecto.',
 'Personas que quieren libertad económica y geográfica y no se atreven a dar el primer paso.',
],
}

def main():
    total = sum(len(v) for v in B.values()); assert total == 200, total
    md = ['# A quién le vendo · Abel García', '', f'**Frase central:** {FRASE}', '',
          '**Qué vendo:** mentoría 1:1. Es la transformación de la frase y, dentro, ayudar a crear el servicio o proyecto que la persona quiere.', '',
          '**Cómo usar este documento:** cada descripción es un ángulo de contenido. El gancho nombra su situación; la colleja, lo que hace mal y lo que le cuesta; la solución, sanar la emoción que hay debajo, con el ejemplo de Abel. Sin CTA.', '']
    n = 0
    for blq, lst in B.items():
        md += [f'## {blq}', '']
        for d in lst:
            n += 1; md.append(f'{n}. {d}')
        md.append('')
    (AQUI / 'A-QUIEN-LE-VENDO.md').write_text('\n'.join(md), encoding='utf-8')
    fuente = (Path.home() / 'Desktop/EDICION VIDEOS/ABEL GARCIA/Editor vídeos/herramientas/tablero/Montserrat-Variable.ttf').as_uri()
    secs, n = [], 0
    for blq, lst in B.items():
        items = ''
        for d in lst:
            n += 1; items += f'<li value="{n}">{html.escape(d)}</li>'
        secs.append(f'<section><h2>{html.escape(blq)}</h2><ol>{items}</ol></section>')
    doc = f'''<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{{font-family:M;src:url("{fuente}")}}
body{{font-family:M,sans-serif;color:#111;margin:0;font-size:11pt;line-height:1.45}}
.port{{height:250mm;display:flex;flex-direction:column;justify-content:center;padding:0 18mm;page-break-after:always}}
.port h1{{font-size:34pt;font-weight:800;margin:0 0 6mm;letter-spacing:-.02em}}
.port .f{{font-size:16pt;font-weight:700;color:#7A3FC4;margin:0 0 10mm}}
.port p{{font-size:11.5pt;color:#444;max-width:150mm}}
section{{padding:0 16mm;page-break-before:always}}
h2{{font-size:17pt;font-weight:800;border-bottom:3px solid #111;padding-bottom:2mm;margin:4mm 0 5mm}}
li{{margin:0 0 2.6mm;padding-left:1mm}} li::marker{{color:#7A3FC4;font-weight:800}}
</style></head><body>
<div class="port"><h1>A quién le vendo</h1><div class="f">«{html.escape(FRASE)}»</div>
<p><b>Qué vendo:</b> mentoría 1:1. Es la transformación de la frase y, dentro, ayudar a crear el servicio o proyecto que la persona quiere.</p>
<p><b>200 descripciones por situación</b>, no por edad ni sexo. Cada una cuenta lo que hace mal la persona y lo que le está costando.</p>
<p><b>Cómo usarlo:</b> cada descripción es un ángulo de contenido. El gancho nombra su situación; la colleja, lo que hace mal y lo que le cuesta llevado al extremo; la solución, sanar la emoción que hay debajo, con el ejemplo de Abel. Sin CTA.</p>
<p style="margin-top:14mm;font-weight:700">Abel García · 2026</p></div>
{''.join(secs)}</body></html>'''
    (AQUI / '_a_quien.html').write_text(doc, encoding='utf-8')
    js = f'''import {{ chromium }} from 'playwright-core'; import {{ readdirSync }} from 'node:fs'; import {{ pathToFileURL }} from 'node:url';
const base = process.env.LOCALAPPDATA + '/ms-playwright', hs = readdirSync(base).find(d => d.startsWith('chromium_headless_shell-'));
const b = await chromium.launch({{ executablePath: `${{base}}/${{hs}}/chrome-headless-shell-win64/chrome-headless-shell.exe`, args: ['--allow-file-access-from-files'] }});
const p = await b.newPage(); await p.goto(pathToFileURL({json.dumps(str(AQUI / '_a_quien.html'))}).href); await p.waitForTimeout(500);
await p.pdf({{ path: {json.dumps(str(AQUI / 'A-QUIEN-LE-VENDO.pdf'))}, format: 'A4', margin: {{ top: '16mm', bottom: '16mm' }}, printBackground: true,
  displayHeaderFooter: true, headerTemplate: '<span></span>', footerTemplate: '<div style="font-size:8pt;width:100%;text-align:center;color:#999"><span class="pageNumber"></span></div>' }});
await b.close();'''
    tab = Path.home() / 'Desktop/EDICION VIDEOS/ABEL GARCIA/Editor vídeos/herramientas/tablero'
    (tab / '_pdf_tmp.mjs').write_text(js, encoding='utf-8')
    subprocess.run(['node', '_pdf_tmp.mjs'], cwd=tab, check=True)
    (tab / '_pdf_tmp.mjs').unlink(); (AQUI / '_a_quien.html').unlink()
    print('ok', total, 'descripciones ->', AQUI / 'A-QUIEN-LE-VENDO.pdf')

if __name__ == '__main__':
    main()
