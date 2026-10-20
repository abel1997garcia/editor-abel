"""Banco de ganchos para que Abel marque cuáles valen (PDF A4, Montserrat). python banco_ganchos.py → BANCO-GANCHOS-VALIDAR.pdf"""
import html, json, subprocess
from pathlib import Path

AQUI = Path(__file__).parent
TAB = Path.home() / 'Desktop/EDICION VIDEOS/ABEL GARCIA/Editor vídeos/herramientas/tablero'
AZUL = '#1D4ED8'

ESTRUCTURAS = {
    'E1': 'Si [conducta del día a día], prepárate para [consecuencia que duele]',
    'E2': 'Pregunta que escuece + respuesta corta (modelo Lavri)',
    'E3': 'Orden directa: «Deja de…»',
    'E4': 'Su frase entre comillas + bofetada (modelo Rebeca)',
    'E5': 'Atacar lo que desea: «Ningún / Nadie te va a…» (modelo Luigi)',
    'E6': 'Lo que nadie te cuenta',
    'E7': 'Pregunta-trampa: «X no te hace Y. ¿Sabes qué…?»',
}

# (gancho, estructura, creencia que rompe, estado: '' | 'OK' (ya aprobado por Abel))
BANCO = [
    ('Autoestima · no sentirte suficiente', [
        ('Si necesitas «me gusta» para sentirte guapo, vas a odiarte cada vez que subas una foto.', 'E1', 'Los demás me darán la seguridad', ''),
        ('Si pides perdón hasta al camarero, prepárate para que todo el mundo te pase por encima.', 'E1', 'Pedir perdón es ser educado', ''),
        ('¿Cuántas veces te has mirado hoy al espejo y te has dicho algo bonito? Cero.', 'E2', 'Yo me trato bien', ''),
        ('Deja de esconderte detrás del «soy tímido», que se te ve a kilómetros.', 'E3', 'Soy tímido y ya está', ''),
        ('«Yo es que soy así.» Llevas diez años diciéndolo y sigues igual de jodido.', 'E4', 'Mi forma de ser no cambia', ''),
        ('Ningún ascenso, ningún coche y ninguna pareja te van a quitar esa sensación de no valer.', 'E5', 'Cuando consiga X, me sentiré bien', ''),
        ('Nadie te cuenta qué le hace a tu cabeza mirar Instagram a las dos de la mañana.', 'E6', 'Mirar redes no hace daño', ''),
        ('No te hunde que te critiquen. ¿Sabes qué te hunde de verdad?', 'E7', 'Las críticas son lo que me hunde', ''),
    ]),
    ('Complacer · decir que sí a todo', [
        ('Si dices que sí a todo para caer bien, prepárate para que te pierdan el respeto.', 'E1', 'Decir que sí es ser buena persona', 'OK'),
        ('Si dejas tus planes cada vez que alguien te llama, prepárate para no tener vida.', 'E1', 'Estar para todos es lo correcto', ''),
        ('¿Cuántos favores has hecho este mes sin querer? Y nadie te ha dado ni las gracias.', 'E2', 'Me lo agradecen', ''),
        ('Deja de ser el taxi, el banco y el psicólogo de tus amigos.', 'E3', 'Así me van a querer más', ''),
        ('«Es que no sé decir que no.» Sí sabes. Lo que te cagas es de que se enfaden.', 'E4', 'No sé poner límites', ''),
        ('Nadie te va a querer más por coger el teléfono a las once de la noche.', 'E5', 'Si estoy siempre, me valorarán', ''),
        ('Nadie te cuenta qué dicen de ti cuando no estás, por mucho que digas que sí.', 'E6', 'Me ven como alguien generoso', ''),
        ('Ser bueno no es lo que te tiene reventado. ¿Sabes qué te tiene así?', 'E7', 'Estoy cansado de ser tan bueno', ''),
    ]),
    ('Pareja · dependencia emocional', [
        ('Si le pides a tu pareja que llene tu vacío, prepárate para perderla.', 'E1', 'El amor te completa', 'OK'),
        ('Si no aguantas un sábado solo en casa, vas a aguantarle cualquier mierda a quien llegue.', 'E1', 'Necesito pareja para estar bien', ''),
        ('¿Cuántas veces más vas a elegir a alguien que no te valora? Más de las que crees.', 'E2', 'Es mala suerte en el amor', 'OK'),
        ('Deja de mirar su última conexión cada diez minutos, que te estás humillando tú solo.', 'E3', 'Si me escribe, estaré tranquilo', ''),
        ('«Es que le quiero mucho.» Le quieres tanto que te dejas tratar como a una mierda.', 'E4', 'Aguantar es querer', ''),
        ('Tu ex no va a volver por mucho que mires sus stories de madrugada.', 'E5', 'Si espero, volverá', ''),
        ('Nadie te cuenta por qué vuelves con quien te ha hecho llorar mil veces.', 'E6', 'Vuelvo porque le quiero', ''),
        ('Revisarle el móvil no es amor. ¿Sabes lo que dice de ti?', 'E7', 'Los celos son amor', ''),
    ]),
    ('Soledad · rodeado de gente y solo', [
        ('Si nadie sabe que lo estás pasando mal, el problema no lo tienen ellos.', 'E1', 'Nadie me entiende', 'OK'),
        ('¿Cuánta gente te escribiría si tú dejaras de escribir primero? Muy poca. Y no es culpa suya.', 'E2', 'Los demás pasan de mí', 'OK'),
        ('¿Cuándo fue la última vez que te preguntaron cómo estás y dijiste la verdad? Exacto.', 'E2', 'Tengo con quien hablar', ''),
        ('Deja de reírte en las cenas cuando lo que quieres es irte a casa a llorar.', 'E3', 'Si sonrío, encajo', ''),
        ('Cambiar de grupo de amigos no te va a quitar esa soledad. Ni el próximo.', 'E5', 'Me falta gente', ''),
        ('Nadie te cuenta por qué te sientes más solo en una fiesta que en tu cama.', 'E6', 'La soledad es estar solo', ''),
    ]),
    ('Emociones · ansiedad, rabia, llorar', [
        ('Si cada vez que te agobias abres TikTok, prepárate para que la ansiedad te coma.', 'E1', 'Distraerme me calma', ''),
        ('¿Cuántas veces has llorado este año delante de alguien? Si es cero, estás jodido.', 'E2', 'No llorar es ser fuerte', ''),
        ('Deja de respirar hondo cuando te da ansiedad, que así solo la escondes.', 'E3', 'Hay que controlar la ansiedad', ''),
        ('Ninguna frase positiva te va a quitar ese nudo en el pecho a las cuatro de la mañana.', 'E5', 'Pensar en positivo lo arregla', ''),
        ('Nadie te cuenta qué pasa con la rabia que te tragas para no discutir con tu pareja.', 'E6', 'Tragármela mantiene la paz', ''),
        ('No te está rompiendo la ansiedad. ¿Sabes qué te está rompiendo de verdad?', 'E7', 'Mi problema es la ansiedad', ''),
    ]),
    ('Energía · vibración (bajado a tierra)', [
        ('Si te levantas reventado aunque duermas ocho horas, el problema no está en tu colchón.', 'E1', 'Estoy cansado por dormir poco', ''),
        ('¿Cuánta energía te quita el café con esa amiga que solo se queja? Más que el trabajo.', 'E2', 'Quedar con amigos no cansa', ''),
        ('Deja de intentar vibrar alto con frases de taza, que lo único que haces es fingir.', 'E3', 'Vibrar alto es pensar bonito', ''),
        ('Ningún ritual de luna llena te sube la energía si aguantas a quien te la chupa.', 'E5', 'Un ritual me subirá la energía', ''),
        ('Nadie te cuenta por qué llegas a casa vacío después de ver a ciertas personas.', 'E6', 'Es cansancio normal', ''),
        ('Tu trabajo no te quita la energía. ¿Sabes a dónde se te va de verdad?', 'E7', 'El trabajo me agota', ''),
        ('«Es que absorbo la energía de todos.» Lo que haces es no poner ni un límite.', 'E4', 'Soy demasiado sensible', ''),
    ]),
    ('Conciencia · desarrollo personal (bajado a tierra)', [
        ('Si llevas cinco libros de autoestima este año y sigues igual, no te falta leer.', 'E1', 'Me falta saber más', ''),
        ('¿Cuánto dinero llevas gastado en cursos para sentirte bien? Y sigues igual de jodido.', 'E2', 'El siguiente curso será el bueno', ''),
        ('Deja de meditar para no sentir lo que sientes, que así no sales nunca.', 'E3', 'Meditar lo arregla todo', ''),
        ('Ninguna afirmación delante del espejo te va a quitar lo que sientes cuando apagas la luz.', 'E5', 'Las afirmaciones me subirán la autoestima', ''),
        ('Nadie te cuenta qué pasa cuando lloras todo lo que llevas años tragándote.', 'E6', 'Es mejor no sentir', ''),
        ('Pensar menos no te va a curar. ¿Sabes qué te cura de verdad?', 'E7', 'Tengo que controlar mi mente', ''),
    ]),
    ('Energía sexual · retención (canal Héroe Viaje)', [
        ('¿Por qué te sientes una mierda justo después de masturbarte? Nadie te lo explica.', 'E2', 'Masturbarse no tiene efecto', ''),
        ('Deja de ver porno si quieres que una mujer te tome en serio.', 'E3', 'El porno no afecta a nada', ''),
        ('Ninguna mujer te va a mirar distinto si te vacías cada noche delante del móvil.', 'E5', 'Atraer depende del físico', ''),
        ('Nadie te cuenta lo que cambia en tu mirada a los treinta días sin eyacular.', 'E6', 'Retener no cambia nada', ''),
    ]),
]
CHECK = ['De tú a tú y sobre la persona (nunca sobre la historia de Abel).', 'Va contra una creencia popular de ese tema.',
         'Toca el dolor desde la primera palabra.', 'Curiosidad: no es una afirmación cerrada; hay que ver el vídeo.',
         'Polémico o crudo.', 'Humano: sin antítesis, punto y coma ni abstracciones.', 'Concreto y duro: una escena, una hora, un objeto, una frase que se dice; nada de «una cosa» o «una razón».',
         'Se entiende solo y tiene 15 palabras o menos.']


def main():
    fuente = (TAB / 'Montserrat-Variable.ttf').as_uri()
    n = 0; secs = ''
    for tema, items in BANCO:
        filas = ''
        for g, e, c, st in items:
            n += 1
            ok = '<span class="ok">✔ aprobado</span>' if st == 'OK' else ''
            filas += (f'<tr><td class="n">{n}</td><td class="g">{html.escape(g)}{ok}</td><td class="e">{e}</td>'
                      f'<td class="c">{html.escape(c)}</td><td class="x">☐</td><td class="x">☐</td><td class="nota"></td></tr>')
        secs += (f'<h2>{html.escape(tema)}</h2><table><tr><th>#</th><th>Gancho</th><th>Estr.</th><th>Creencia que rompe</th>'
                 f'<th>Sí</th><th>No</th><th>Por qué / ajuste</th></tr>{filas}</table>')
    est = ''.join(f'<li><b>{k}</b> · {html.escape(v)}</li>' for k, v in ESTRUCTURAS.items())
    chk = ''.join(f'<li>{html.escape(c)}</li>' for c in CHECK)
    doc = f'''<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{{font-family:M;src:url("{fuente}")}}
@page{{size:A4 landscape;margin:12mm}}
body{{font-family:M,sans-serif;color:#111;font-size:9.5pt;line-height:1.35}}
h1{{color:{AZUL};font-size:22pt;margin:0 0 2mm}} h2{{color:{AZUL};font-size:13pt;margin:7mm 0 2mm;page-break-after:avoid}}
.sub{{color:#555;margin:0 0 5mm}} .cols{{display:flex;gap:10mm}} .cols>div{{flex:1}} ul,ol{{margin:1mm 0 0 5mm;padding:0}}
table{{width:100%;border-collapse:collapse;page-break-inside:auto}} tr{{page-break-inside:avoid}}
th{{background:{AZUL};color:#fff;text-align:left;padding:2mm;font-size:8.5pt}}
td{{border-bottom:1px solid #ddd;padding:2mm;vertical-align:top}}
.n{{width:6mm;color:#888}} .g{{font-weight:700;width:46%}} .e{{width:9mm;color:{AZUL};font-weight:700}} .c{{width:22%;color:#444}}
.x{{width:8mm;font-size:13pt;text-align:center}} .nota{{width:18%}} .ok{{display:inline-block;margin-left:2mm;color:#0a7a2f;font-size:8pt}}
</style></head><body>
<h1>Banco de ganchos para validar</h1><p class="sub">Marca Sí o No y apunta por qué o cómo lo ajustarías. Con tus marcas se afinan las estructuras que funcionan. ({n} ganchos · 18/10/2026)</p>
<div class="cols"><div><b>Checklist de cada gancho</b><ol>{chk}</ol></div><div><b>Estructuras</b><ul>{est}</ul></div></div>
{secs}</body></html>'''
    h = AQUI / '_banco_ganchos.html'; h.write_text(doc, encoding='utf-8')
    out = AQUI / 'BANCO-GANCHOS-VALIDAR.pdf'
    js = f"""import {{ chromium }} from 'playwright-core'; import {{ readdirSync }} from 'node:fs'; import {{ pathToFileURL }} from 'node:url';
const base = process.env.LOCALAPPDATA + '/ms-playwright', hs = readdirSync(base).filter(d => d.startsWith('chromium_headless_shell-')).sort().reverse()[0];
const b = await chromium.launch({{ executablePath: `${{base}}/${{hs}}/chrome-headless-shell-win64/chrome-headless-shell.exe`, args: ['--allow-file-access-from-files'] }});
const p = await b.newPage(); await p.goto(pathToFileURL({json.dumps(str(h))}).href); await p.waitForTimeout(500);
await p.pdf({{ path: {json.dumps(str(out))}, format: 'A4', landscape: true, printBackground: true }});
await b.close();"""
    (TAB / '_pdf_tmp.mjs').write_text(js, encoding='utf-8')
    subprocess.run(['node', '_pdf_tmp.mjs'], cwd=TAB, check=True)
    (TAB / '_pdf_tmp.mjs').unlink()
    h.unlink(); print(out, n)


if __name__ == '__main__':
    main()
