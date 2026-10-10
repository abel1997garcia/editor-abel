"""Genera A-QUIEN-LE-VENDO.pdf (y .md): 200 descripciones de a quién le vende Abel (nicho del 10/10/2026), por situación.
Cada una = qué hace mal la persona (connotación negativa) + lo que le está costando. El avatar manda en 00-avatar-operativo.md.
    python a_quien_le_vendo.py
"""
import json, subprocess, html
from pathlib import Path

AQUI = Path(__file__).resolve().parent
FRASE = 'Si emprendes, te enseño a llenar tu agenda con tu marca personal. Sin perseguir clientes ni perder tu autenticidad.'

B = {
'1 · Tienen un don y la agenda medio vacía': [
 'Terapeutas que cambian la vida de cada persona que pasa por su consulta y aun así tienen huecos en la agenda toda la semana.',
 'Coaches que tienen una certificación detrás de otra y siguen sin un solo cliente que no venga de un amigo.',
 'Gente de reiki que da sesiones increíbles y vive con miedo a final de mes porque nunca sabe cuántas personas vendrán.',
 'Médiums con un don que impresiona a cualquiera, que siguen atendiendo solo a conocidos de conocidos.',
 'Profesores de yoga que llenan una clase en verano y la ven medio vacía en cuanto llega septiembre.',
 'Terapeutas que dependen del boca a boca y se quedan sin clientes en cuanto alguien deja de recomendarlas.',
 'Guías que saben que podrían ayudar a cientos de personas y se conforman con cinco porque no saben llegar a más.',
 'Coaches que compaginan su don con un trabajo que odian porque con sus sesiones no les da para vivir.',
 'Sanadores que dicen «lo que tenga que llegar, llegará» mientras pasan los meses sin que llegue nadie.',
 'Terapeutas que tienen la consulta perfecta, la camilla y la web, y nadie que entre por la puerta.',
 'Profesionales del bienestar que han invertido miles de euros en formarse y no han recuperado ni la mitad.',
 'Personas que dejaron su trabajo para dedicarse a ayudar y ahora se plantean volver porque no llegan a fin de mes.',
 'Terapeutas que hacen un trabajo mejor que la mitad de los que se anuncian y tienen la mitad de clientes.',
 'Gente con un don que lo esconde de lunes a viernes detrás de un trabajo de oficina.',
 'Terapeutas que cada mes empiezan de cero porque no tienen nada que haga que los clientes lleguen solos.',
 'Facilitadores de retiros que ponen fecha, lo preparan todo y cancelan porque se han apuntado tres personas.',
 'Coaches que miran su agenda los domingos por la noche con un nudo en el estómago.',
 'Tarotistas y médiums que cobran por debajo de lo que valen porque piensan que si suben no vendrá nadie.',
 'Personas con un talento real que empiezan a dudar de si sirven para esto solo porque no les llegan clientes.',
 'Coaches que tienen una lista de espera en la cabeza y un calendario real lleno de huecos.',
],
'2 · Les da vergüenza venderse (y lo llaman humildad)': [
 'Coaches que dicen «no me gusta venderme» y lo llaman humildad, cuando lo que hay es miedo a que les digan que no.',
 'Terapeutas que nunca dicen en sus redes que tienen hueco por miedo a parecer desesperadas.',
 'Gente de reiki que siente que hablar de precio ensucia lo que hace.',
 'Médiums que no ponen en su perfil que dan sesiones porque les da apuro que lo vea su familia.',
 'Guías que, cuando alguien les pregunta a qué se dedican, lo explican tan por encima que nadie se entera.',
 'Terapeutas que hablan de todo en sus redes menos de cómo pueden ayudarte.',
 'Coaches que borran una historia vendiendo su servicio a los diez minutos de subirla.',
 'Personas que esperan a que el cliente les pida trabajar juntos porque ellas no se atreven a ofrecerlo.',
 'Terapeutas que sienten que si venden pierden su espiritualidad.',
 'Profesionales que tienen una conversación preciosa por DM y nunca llegan a decir «¿quieres que trabajemos juntos?».',
 'Coaches que se esconden detrás de un logo porque les da vergüenza que se les vea la cara.',
 'Personas que no hablan de sus resultados porque les parece presumir.',
 'Terapeutas que confunden vender con manipular, y por eso no venden nada.',
 'Sanadores que creen que el universo les mandará clientes sin tener que decir que existen.',
 'Coaches que tienen un testimonio brutal guardado en el móvil y nunca lo enseñan.',
 'Personas que en persona convencen a cualquiera y delante de la cámara no saben ni presentarse.',
 'Terapeutas a las que les tiembla la voz cuando dicen su precio.',
 'Guías espirituales que piensan que quien vende es un interesado y no quieren parecerse a él.',
 'Coaches que hacen un directo al año y lo viven como si saltaran de un avión.',
 'Personas que dicen «ya me encontrarán» y llevan dos años sin que las encuentre nadie.',
],
'3 · No saben qué publicar ni cómo grabarse': [
 'Coaches que abren Instagram, miran la pantalla en blanco y lo cierran sin publicar nada.',
 'Terapeutas que graban un vídeo diez veces y no suben ninguno porque no se gustan.',
 'Gente de reiki que publica una vez al mes cuando le viene la inspiración y desaparece el resto.',
 'Médiums que no saben explicar lo que hacen sin sonar raros.',
 'Guías que publican frases de otros porque no saben qué decir con sus propias palabras.',
 'Coaches que se pasan la tarde viendo tutoriales de edición en vez de grabar.',
 'Terapeutas que creen que necesitan una cámara y una luz profesional para empezar.',
 'Personas que tienen cien ideas en las notas del móvil y ninguna grabada.',
 'Coaches que se bloquean delante de la cámara y hablan como si leyeran un informe.',
 'Terapeutas que hacen vídeos de diez minutos explicando teoría que nadie termina de ver.',
 'Profesores de yoga que solo suben fotos de posturas y no cuentan nada de ellos.',
 'Coaches que copian los bailes y trucos de moda y no les pega nada con lo que hacen.',
 'Terapeutas que empiezan todos sus vídeos con «hola, hoy os quiero hablar de» y pierden a la gente en el primer segundo.',
 'Personas que piensan que no tienen nada interesante que contar.',
 'Guías que publican todos los días sin saber para qué y se queman en un mes.',
 'Coaches que no saben qué decir sin dar los mismos consejos que ya ha dado todo el mundo.',
 'Terapeutas que esperan a tenerlo todo perfecto para empezar, y nunca está perfecto.',
 'Sanadores que dejan las redes porque «no es lo suyo» sin haberlo intentado de verdad.',
 'Coaches que no saben contar su historia sin sentir que dan pena.',
 'Personas que ven a otros grabarse con naturalidad y piensan que ellas nunca podrán.',
],
'4 · Publican y no les escribe nadie': [
 'Terapeutas que publican frases bonitas con un atardecer de fondo y luego se preguntan por qué nadie les escribe.',
 'Coaches que tienen mil seguidores y ni un mensaje privado en meses.',
 'Gente de reiki que recibe muchos «qué bonito» en los comentarios y ningún cliente.',
 'Médiums que hacen contenido que entretiene pero que no hace que nadie quiera trabajar con ellos.',
 'Guías que hablan de su método y no del problema que tiene la persona que les ve.',
 'Coaches obsesionados con los seguidores que no se dan cuenta de que lo que necesitan son conversaciones.',
 'Terapeutas que publican para otros terapeutas en vez de para quien las puede contratar.',
 'Personas que hacen contenido educativo impecable en el que nadie siente que le hablan a él.',
 'Coaches que tienen visualizaciones pero nadie que les pregunte cómo trabajar juntos.',
 'Terapeutas que nunca dicen en un vídeo a quién ayudan exactamente.',
 'Profesionales que hablan con palabras técnicas que su cliente no entiende.',
 'Sanadores que hablan de vibración y frecuencia a gente que solo quiere dormir bien.',
 'Coaches que publican lo mismo que otros cien coaches y no hay nada que los diferencie.',
 'Terapeutas que contestan los mensajes tarde y mal porque no saben qué decir cuando les escriben.',
 'Personas que hacen un vídeo viral y no consiguen ni un cliente porque no le hablaba a nadie en concreto.',
 'Guías que no enseñan nunca historias de personas a las que han ayudado.',
 'Coaches que publican en cinco redes a la vez y no destacan en ninguna.',
 'Terapeutas que tienen una bio que no dice ni a qué se dedican.',
 'Personas que culpan al algoritmo de lo que en realidad es un mensaje que no conecta.',
 'Coaches que creen que el problema es cuánto publican cuando el problema es lo que publican.',
],
'5 · Persiguen clientes y regalan su trabajo': [
 'Coaches que escriben a desconocidos por DM ofreciendo una sesión y sienten que mendigan.',
 'Terapeutas que regalan sesiones «para darse a conocer» y nunca convierten a nadie en cliente.',
 'Gente de reiki que persigue a antiguos clientes para que vuelvan.',
 'Médiums que hacen lecturas gratis en directos y luego nadie paga una.',
 'Guías que se pasan el día comentando en grupos de Facebook para ver si alguien les contrata.',
 'Coaches que mandan audios de cinco minutos a personas que no les han pedido nada.',
 'Terapeutas que hacen descuentos constantes porque sienten que sin descuento no vendrá nadie.',
 'Personas que dan tanto gratis que el cliente ya no necesita pagarles.',
 'Coaches que llaman «seguimiento» a perseguir a alguien que ya les dijo que no.',
 'Terapeutas que aceptan a cualquier cliente aunque no les encaje, por miedo a quedarse sin ninguno.',
 'Facilitadores que llenan sus talleres a base de pedir favores a sus amigos.',
 'Coaches que se agotan haciendo llamadas de descubrimiento que nunca terminan en venta.',
 'Terapeutas que contestan dudas gratis por WhatsApp hasta las once de la noche.',
 'Sanadores que trabajan «por la voluntad» y luego se sienten utilizados.',
 'Personas que van a eventos a repartir tarjetas y vuelven a casa con la misma agenda.',
 'Coaches que bajan el precio en mitad de la llamada en cuanto notan una duda.',
 'Terapeutas que sienten que tienen que convencer a la gente de que las necesita.',
 'Médiums que se pasan horas de más con un cliente sin cobrarlas porque les sabe mal.',
 'Guías que regalan lo mejor que tienen en un PDF y luego no saben qué vender.',
 'Personas que creen que persiguiendo más conseguirán más, cuando cada mensaje las aleja un poco más.',
],
'6 · Culpa por cobrar y precios bajos': [
 'Terapeutas que sienten que cobrar por ayudar está mal, y por eso cobran como si les diera vergüenza.',
 'Coaches que llevan tres años con el mismo precio porque les da miedo subirlo.',
 'Gente de reiki que cree que los dones no se cobran y luego no llega a fin de mes.',
 'Médiums que se sienten culpables cuando alguien paga una sesión y no sale como esperaba.',
 'Guías que piensan que si ganan dinero dejarán de ser espirituales.',
 'Coaches que dicen su precio y enseguida añaden «pero si no puedes, lo hablamos».',
 'Terapeutas que trabajan sesenta horas a la semana a precio de saldo y lo llaman vocación.',
 'Personas que crecieron oyendo que el dinero es sucio y hoy lo apartan sin darse cuenta.',
 'Coaches que cobran menos que su peluquero por cambiarle la vida a alguien.',
 'Terapeutas que se queman porque necesitan muchos clientes baratos para llegar a fin de mes.',
 'Sanadores que se sienten en deuda con cada persona que les paga.',
 'Coaches que no se atreven a vender un programa porque «quién soy yo para cobrar eso».',
 'Terapeutas que hacen excepciones de precio con todo el mundo y luego no les salen las cuentas.',
 'Personas que ayudan a todos a vivir con abundancia menos a sí mismas.',
 'Profesores de yoga que cobran lo mismo que el gimnasio de la esquina y sienten que valen más.',
 'Coaches que tienen miedo de que los juzguen por ganar dinero ayudando.',
 'Terapeutas que se ponen nerviosas cada vez que tienen que mandar una factura.',
 'Guías que se comparan con quien cobra más y piensan «ese es un vendehúmos».',
 'Médiums que creen que si cobran bien el don se les irá.',
 'Personas que dicen que el dinero no les importa y viven agobiadas por él.',
],
'7 · Se comparan, se sienten impostores y esperan a estar preparados': [
 'Coaches que ven a otros con menos formación llenar la agenda y sienten rabia y envidia a la vez.',
 'Terapeutas que hacen otro curso más porque sienten que todavía no saben lo suficiente.',
 'Gente de reiki que piensa que todavía no está preparada para tener clientes de verdad.',
 'Médiums que tienen miedo de que alguien les diga en público que lo suyo es mentira.',
 'Guías que se sienten un fraude cada vez que alguien les da las gracias.',
 'Coaches que no se atreven a hablar de un tema porque «ya lo ha dicho otro mejor».',
 'Terapeutas que se comparan con quien tiene cien mil seguidores y se paralizan.',
 'Personas con veinte certificados colgados en la pared y ninguna seguridad por dentro.',
 'Coaches que esperan a tener su propia vida resuelta para empezar a ayudar a otros.',
 'Terapeutas que piensan que el mercado está saturado y que no hay sitio para ellas.',
 'Sanadores que creen que tienen que ser perfectos para poder ayudar.',
 'Coaches que miran las estadísticas de otros todos los días y se sienten pequeños.',
 'Terapeutas que no se sienten legítimas porque no tienen un título «oficial».',
 'Guías que esconden su pasado porque creen que les quita autoridad, cuando es lo que más conecta.',
 'Personas que dicen «cuando tenga más experiencia» y llevan cinco años diciéndolo.',
 'Coaches que necesitan la aprobación de su mentor para cada paso que dan.',
 'Terapeutas que se paralizan con un comentario negativo entre cien buenos.',
 'Médiums que se callan lo que perciben por miedo a equivocarse en público.',
 'Coaches que se sienten pequeños al lado de un cliente al que le va bien en la vida.',
 'Personas que creen que el éxito es para otros con más suerte, más contactos o más carisma.',
],
'8 · Pierden su autenticidad copiando a otros': [
 'Coaches que copian el estilo de su mentor y suenan a una copia barata.',
 'Terapeutas que en redes hablan con una voz que no es la suya, más seria, más técnica y más fría.',
 'Gente de reiki que esconde su lado espiritual porque cree que asusta a la gente.',
 'Médiums que se disfrazan de algo que no son para parecer más creíbles.',
 'Guías que siguen todas las tendencias aunque les dé vergüenza ajena hacerlas.',
 'Coaches que se ponen la máscara de «todo me va genial» y con quienes nadie conecta.',
 'Terapeutas que nunca cuentan lo que vivieron ellas, que es justo lo que las hace únicas.',
 'Personas que hablan como un anuncio y luego no entienden por qué no generan confianza.',
 'Coaches que usan las mismas palabras que todo su sector y se vuelven invisibles.',
 'Terapeutas que quitan su opinión de todo para no molestar a nadie y no conectan con nadie.',
 'Sanadores que publican lo que creen que la gente quiere ver en vez de lo que piensan de verdad.',
 'Coaches que cambian de nicho cada tres meses porque alguien les dijo que ahí está el dinero.',
 'Terapeutas que se avergüenzan de su acento, de su casa o de su forma de hablar delante de la cámara.',
 'Guías que tienen opiniones fuertes y se las callan por miedo a perder seguidores.',
 'Personas que usan plantillas de guiones que no suenan a ellas, y se nota en cada vídeo.',
 'Coaches que imitan a gurús americanos cuando su público es de su barrio.',
 'Terapeutas que enseñan solo sus títulos y nunca a la persona que hay detrás.',
 'Médiums que suavizan tanto lo que hacen que nadie sabe exactamente qué ofrecen.',
 'Coaches que tienen miedo de que su familia vea en redes quiénes son de verdad.',
 'Personas que se pierden intentando gustar a todos y acaban sin gustarle a nadie.',
],
'9 · Solo miran el dinero y se olvidan de su mensaje': [
 'Coaches que solo hablan de facturación y se les ha olvidado por qué empezaron a ayudar.',
 'Terapeutas que venden desde la escasez, y el cliente lo nota en cada mensaje.',
 'Gente de reiki que mete urgencia falsa en cada publicación porque necesita vender este mes.',
 'Médiums que prometen cosas que no pueden cumplir para cerrar una venta.',
 'Guías espirituales que usan la espiritualidad para sentirse por encima de sus clientes.',
 'Coaches que aceptan clientes a los que no pueden ayudar solo porque necesitan el dinero.',
 'Terapeutas que cambian su mensaje cada mes según lo que creen que vende más.',
 'Personas que lanzan programas sin haber escuchado nunca qué necesita su cliente.',
 'Coaches que miden lo que valen por lo que facturan y se hunden cuando un mes va mal.',
 'Terapeutas que hablan de abundancia en redes y viven angustiadas por el alquiler.',
 'Sanadores que ayudan para que les vean, no para ayudar, y la gente lo siente.',
 'Coaches que copian lanzamientos agresivos que no van con ellos y se sienten sucios después.',
 'Terapeutas que quieren salvar a todo el mundo y se olvidan de que no todos quieren que les salven.',
 'Guías que venden el resultado de otros como si fuera suyo.',
 'Coaches que se apuntan a cada moda de negocio online y no construyen nada propio.',
 'Personas que confunden tener éxito con tener muchos seguidores.',
 'Terapeutas que se comparan en cifras con otros y pierden de vista a la persona que tienen delante.',
 'Coaches que, cuando no venden, culpan a la gente de «no estar preparada».',
 'Médiums que han convertido su don en un producto frío y ya no disfrutan.',
 'Personas que tienen una verdad que contar y la cambian por lo que dice el último curso de marketing.',
],
'10 · Lo de dentro que les sabotea el negocio': [
 'Terapeutas que ayudan a otros a sanar sus heridas y no han mirado la suya con el dinero.',
 'Coaches que de pequeños aprendieron que destacar era peligroso y hoy no se atreven a enseñarse.',
 'Gente de reiki que tiene tanto miedo a la crítica que prefiere no publicar.',
 'Médiums que siguen sintiendo que tienen que demostrarle algo a su familia.',
 'Guías que se sabotean justo cuando empieza a irles bien.',
 'Coaches que dicen que quieren más clientes y les entra el pánico cuando alguien les escribe.',
 'Terapeutas que crecieron oyendo «no te creas más que nadie» y hoy no saben hablar de lo que valen.',
 'Personas que dejan el contenido para mañana porque grabarse las enfrenta a cómo se ven.',
 'Coaches que viven con ansiedad cada vez que publican algo personal.',
 'Terapeutas que se sienten responsables de las emociones de cada cliente y acaban agotadas.',
 'Sanadores que no ponen límites a sus clientes y luego no tienen energía para nada más.',
 'Coaches que necesitan que cada vídeo funcione para sentir que valen algo.',
 'Terapeutas que tienen miedo de tener éxito porque creen que perderán a su gente.',
 'Guías que repiten con sus clientes la misma complacencia que tienen con su familia.',
 'Personas que se exigen tanto que nada de lo que publican les parece suficiente.',
 'Coaches que se quedan bloqueados cada vez que alguien les deja de seguir.',
 'Terapeutas que no se permiten ganar más que sus padres sin sentir que los traicionan.',
 'Médiums que escuchan lo que perciben de los demás y se callan lo que perciben de sí mismos.',
 'Coaches que esconden su ansiedad detrás de mensajes de «todo es posible».',
 'Personas que saben que el miedo les está frenando la agenda y aun así siguen pensando que les falta estrategia.',
],
}

def main():
    total = sum(len(v) for v in B.values()); assert total == 200, total
    md = ['# A quién le vendo · Abel García', '', f'**Nicho:** {FRASE}', '',
          '**Qué vendo:** mentoría 1:1 (997 € · 3 meses) para coaches, terapeutas, guías, gente de reiki y médiums: su mensaje, contenido que vende, captar sin perseguir y lo de dentro que les sabotea la agenda.', '',
          '**Cómo usar este documento:** cada descripción es un ángulo de contenido. El gancho nombra su situación; la colleja, lo que hace mal y lo que le cuesta; la solución, su mensaje y lo de dentro, con el ejemplo de Abel o de Allan. Sin CTA.', '']
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
<p><b>Qué vendo:</b> mentoría 1:1 (997 € · 3 meses) para coaches, terapeutas, guías, gente de reiki y médiums: su mensaje, contenido que vende, captar sin perseguir y lo de dentro que les sabotea la agenda.</p>
<p><b>200 descripciones por situación</b>, no por edad ni sexo. Cada una cuenta lo que hace mal la persona y lo que le está costando.</p>
<p><b>Cómo usarlo:</b> cada descripción es un ángulo de contenido. El gancho nombra su situación; la colleja, lo que hace mal y lo que le cuesta llevado al extremo; la solución, su mensaje y lo de dentro, con el ejemplo de Abel o de Allan. Sin CTA.</p>
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
