"""Manual de marca visual de Abel (BRANDING-ABEL.pdf + páginas PNG). Versión 2 (18/10/2026).
    python branding_visual.py
Fotos reales (MarcaPersonal/FOTOS MIAS), biblioteca de imágenes (EDICION VIDEOS/IMAGENES) y carruseles ya hechos.
Estilo: agencia profesional, mucho aire, nada de pegotes ni de aspecto IA.
"""
import json, subprocess
from pathlib import Path

AQUI = Path(__file__).resolve().parent
ED = Path.home() / 'Desktop/EDICION VIDEOS/ABEL GARCIA/Editor vídeos'
FOT = ED / 'MarcaPersonal/FOTOS MIAS'
CAR = ED / 'MarcaPersonal/_escaneo_fotos'
BIB = Path.home() / 'Desktop/EDICION VIDEOS/IMAGENES'
TAB = ED / 'herramientas/tablero'
AZUL, ELEC, NEGRO, GRIS = '#1D4ED8', '#2E7BFF', '#0B0B0F', '#6B7280'


def u(p):
    return Path(p).as_uri()


def f(rel):
    return u(FOT / rel)


N = [0]


def pag(titulo, cuerpo, oscura=False, etiqueta=''):
    N[0] += 1
    cls = 'osc' if oscura else ''
    return (f'<section class="{cls}"><div class="top"><span>{etiqueta}</span><span>Abel García · Manual de marca</span></div>'
            f'{"<h2>" + titulo + "</h2>" if titulo else ""}{cuerpo}<div class="pie">{N[0]:02d}</div></section>')


P = []
P.append(f'''<section class="portada"><img src="{f('11-ahora/abel_pizarra_ego_emocion.jpg')}"><div class="vel"></div>
<div class="ptxt"><div class="eti">Manual de marca · 2026</div><h1>Abel García</h1><div class="rol">Especialista en Autoestima</div>
<div class="lema">Espiritualidad que funciona</div></div></section>''')

P.append(pag('Por qué existe esta marca', f'''<div class="cita">«Quiero guiar de forma clara a quien no se siente suficiente, porque yo lo he vivido: no tener autoestima, dejarme llevar por lo que opinaban los demás, no confiar en que podía crear mi vida. Mi razón es darte esperanza: da igual lo mal que estés, siempre hay una salida si sabes lo correcto y lo ejecutas.»</div>
<div class="tres"><div><div class="k">A quién</div><p>A la persona, hombre o mujer, que no se siente suficiente.</p></div>
<div><div class="k">Qué</div><p>Club Unidad 1:1. Autoestima, energía y emociones; y, si quiere vivir de quien es, su marca personal. Crecen juntas.</p></div>
<div><div class="k">Idea central</div><p class="az">Tu autoestima es tu energía, y la energía se recupera.</p></div></div>''', etiqueta='01 · Concepto'))

P.append(pag('Cómo hablamos', f'''<div class="dos"><div><div class="k">Personalidad</div><p class="gr">El amigo un paso por delante que te dice la verdad y te guía.</p>
<p>Habla de tú a tú, con palabras de la calle. Explica desde la energía, bajado a tierra. Cuenta lo que vivió, también lo que le avergüenza.</p>
<div class="k" style="margin-top:34px">Valores</div><div class="tags"><span>Verdad</span><span>Congruencia</span><span>Libertad</span><span>Amor incondicional</span></div></div>
<div><div class="k">Contra qué estamos</div><ul class="lista"><li>Las frases de taza y las afirmaciones que no te crees</li><li>Pensar en positivo a la fuerza</li><li>Años de terapia hablando sin cambiar</li><li>El ego espiritual de aprender, aprender, aprender</li><li>«Quiérete más» sin decirte cómo</li></ul></div></div>''', etiqueta='02 · Voz'))

P.append(pag('Color', f'''<div class="pal"><div class="sw" style="background:{AZUL}"><b>Azul intenso</b><span>{AZUL}</span><em>Acento sobre blanco</em></div>
<div class="sw" style="background:{ELEC}"><b>Azul eléctrico</b><span>{ELEC}</span><em>Acento sobre negro</em></div>
<div class="sw" style="background:{NEGRO}"><b>Negro</b><span>{NEGRO}</span><em>Títulos y fondos oscuros</em></div>
<div class="sw cl" style="background:#fff"><b>Blanco</b><span>#FFFFFF</span><em>Fondo principal</em></div></div>
<div class="prueba"><div class="pb" style="background:#fff">Tu autoestima <span style="color:{AZUL}">es tu energía</span></div><div class="pb" style="background:{NEGRO};color:#fff">Tu autoestima <span style="color:{ELEC}">es tu energía</span></div></div>
<p class="nota">El azul solo marca una palabra o un detalle por pieza. Si todo es azul, nada destaca.</p>''', etiqueta='03 · Identidad visual'))

P.append(pag('Tipografía', f'''<div class="tip"><div class="t1">Montserrat</div><div class="t2">ExtraBold para títulos. <span style="font-weight:600">SemiBold para destacar.</span> <span style="font-weight:400">Regular para leer.</span></div>
<div class="esc"><div><small>Título</small><div style="font-size:64px;font-weight:800;line-height:1">Nadie te va a hacer sentir suficiente</div></div>
<div><small>Destacado</small><div style="font-size:34px;font-weight:600">porque ese no es su <span style="color:{AZUL}">trabajo</span></div></div>
<div><small>Texto</small><div style="font-size:22px;max-width:900px">Lo que sientes cambia lo que piensas de ti, y lo que piensas de ti cambia cómo te tratan.</div></div></div></div>''', etiqueta='03 · Identidad visual'))

P.append(pag('Antes y ahora', f'''<div class="ba"><div class="col"><div class="k">Antes · tapar el vacío</div><div class="g3">
<img src="{f('02-antes-de-despertar/abel_borracho_microfono_fiesta_castelldans.jpg')}"><img src="{f('02-antes-de-despertar/abel_fiesta_noche_tumbado.jpg')}"><img src="{f('02-antes-de-despertar/abel_fiesta_mayor_capa_rosa.jpg')}"></div></div>
<div class="flecha">→</div><div class="col"><div class="k az2">El fondo</div><div class="g1"><img src="{f('10-segundo-fondo-y-sanacion/abel_llorando_sesion_sanacion.jpg')}"></div></div>
<div class="flecha">→</div><div class="col"><div class="k">Ahora · en paz contigo</div><div class="g2"><img src="{f('11-ahora/abel_pizarra_ego_emocion.jpg')}"><img src="{f('11-ahora/abel_gimnasio.jpg')}"></div></div></div>
<p class="nota">El contraste es lo que más vende. Las fotos del antes, solo si encajan al 100 % con la frase.</p>''', etiqueta='04 · Fotografía', oscura=True))

P.append(pag('La prueba: lo que construí', f'''<div class="prueba4">
<figure><img src="{f('05-canal-automatizacion-ganaba-dinero/abel_presentacion_libro_romuald_fons.png')}"><figcaption>Formándome</figcaption></figure>
<figure><img src="{f('05-canal-automatizacion-ganaba-dinero/abel_placa_100k_suscriptores_youtube.jpg')}"><figcaption>100.000 suscriptores</figcaption></figure>
<figure><img src="{f('05-canal-automatizacion-ganaba-dinero/abel_la_roca_village_noche.jpg')}"><figcaption>17.000 € al mes… y vacío</figcaption></figure>
<figure><img src="{f('06-noche-oscura-26-anos/abel_cumpleanos_26_noche_oscura_del_alma.jpg')}"><figcaption>26 años: lo pierdo todo</figcaption></figure></div>
<p class="nota">YouTube, dropshipping, Facebook Ads, IA. Valida la parte de marca personal sin venderla aparte: sale dentro de la historia.</p>''', etiqueta='04 · Fotografía'))

P.append(pag('Aplicado', f'''<div class="apl"><div><small>Carrusel</small><div class="row">
<img class="c" src="{u(CAR / 'boceto_mi_historia_autoestima/01.jpg')}"><img class="c" src="{u(CAR / 'maqueta_viral_01_energia/01.jpg')}"></div></div>
<div><small>Reel · formato 2</small><div class="f2"><div class="f2a"><img src="{f('11-ahora/abel_pizarra_ego_emocion.jpg')}"><span class="sub">energía</span></div><div class="f2t">RESPONDER A TODO TE DEJA SIN ENERGÍA</div><div class="f2b"><img src="{u(BIB / 'frecuencia-vibracion/bateria_energia_vs_burnout.png')}"></div></div>
<p class="mini-n">Arriba tú, con el subtítulo blanco bajo la boca. En medio, la franja blanca con el título en mayúsculas. Abajo, una sola imagen que explica lo que dices.</p></div></div>''', etiqueta='05 · Piezas'))

P.append(pag('Tres tipos de contenido', f'''<div class="tri"><div><div class="n">20%</div><div class="k">Atraer</div><p>Reels que traen gente nueva: lo que engancha (energía, emociones, identidad), llevado a la autoestima y dicho a tu manera.</p><p class="ej">Reels con ganchos tipo Luigi.</p></div>
<div><div class="n">70%</div><div class="k">Consolidar</div><p>Que te conozcan y confíen: tu historia, tus creencias, creencia limitante → necesaria, el antes y ahora.</p><p class="ej">Carruseles, stories y YouTube (10-12 minutos contigo).</p></div>
<div><div class="n">10%</div><div class="k">Vender sin vender</div><p>Dentro del mismo tema: cómo trabajas, lo que construiste, y cuando la autoestima se nota fuera (mostrarte, cobrar, crear lo tuyo).</p><p class="ej">El CTA, solo en la descripción.</p></div></div>''', etiqueta='06 · Contenido'))

filas = [('Autoimagen tan elevada que la realidad te obedezca', '31 K', 'Cómo tener una autoestima tan alta que dejes de buscar que te elijan'),
         ('La guía definitiva para dejar ir los apegos', '43 K', 'La guía definitiva para dejar de necesitar a alguien para estar bien'),
         ('Te pido que aprendas a vibrar alto', '27 K', 'Te pido que dejes de regalar tu energía'),
         ('Elimina creencias limitantes', '26 K', 'Las 5 creencias que te tienen con la autoestima por los suelos'),
         ('El dinero es energía', '28 K', 'Tu autoestima es energía, y así la recuperas'),
         ('Reel · historia personal', '10,7 K', 'Tus confesiones: 17.000 € al mes y vacío'),
         ('Reel · ritual en serie', '2,9 K', '«Cada mañana hago esto para no empezar el día machacándome»')]
P.append(pag('Lo que funciona, a tu manera', '<table><tr><th>Nacho Sala</th><th></th><th>Tu versión</th></tr>' +
             ''.join(f'<tr><td>{a}</td><td class="v">{v}</td><td class="b">{b}</td></tr>' for a, v, b in filas) +
             '</table><p class="nota">Un tema palanca y repetirlo. Nacho mezcla demasiados temas y sus reels rinden poco para su tamaño.</p>', etiqueta='06 · Contenido'))

P.append(pag('', '''<div class="cierre"><div class="k">Cómo se une todo</div><div class="flujo"><span>Te sientes poco</span><i>→</i><span>Trabajas tu autoestima</span><i>→</i><span class="z">Se nota fuera</span></div>
<p>En tu pareja, en tu trabajo y en lo que te atreves a mostrar y a crear. La marca personal no es otro tema: es una consecuencia. Por eso no se vende aparte.</p></div>''', oscura=True, etiqueta='07 · El puente'))

css = f'''@font-face{{font-family:M;src:url("{u(TAB / 'Montserrat-Variable.ttf')}")}}
*{{box-sizing:border-box}} body{{margin:0;font-family:M;color:{NEGRO};background:#fff}}
section{{width:1600px;height:900px;padding:70px 90px;page-break-after:always;position:relative;overflow:hidden;background:#fff}}
section.osc{{background:{NEGRO};color:#fff}} .osc .k{{color:#9CA3AF}} .osc .nota{{color:#9CA3AF;border-color:#27272a}}
.top{{position:absolute;top:34px;left:90px;right:90px;display:flex;justify-content:space-between;font-size:12px;letter-spacing:.18em;text-transform:uppercase;color:{GRIS}}}
.pie{{position:absolute;bottom:34px;right:90px;font-size:12px;color:{GRIS};letter-spacing:.1em}}
h2{{font-size:52px;font-weight:800;letter-spacing:-.02em;margin:26px 0 40px}}
.k{{font-size:13px;font-weight:700;letter-spacing:.18em;text-transform:uppercase;color:{GRIS};margin-bottom:12px}} .az2{{color:{ELEC}!important}}
p{{font-size:20px;line-height:1.55;margin:0 0 10px;max-width:640px}} .nota{{position:absolute;bottom:70px;left:90px;right:90px;max-width:none;font-size:16px;color:{GRIS};border-top:1px solid #e4e4e7;padding-top:16px}}
.portada{{padding:0;background:{NEGRO}}} .portada>img{{position:absolute;right:0;top:0;height:900px;width:900px;object-fit:cover}} .vel{{position:absolute;inset:0;background:linear-gradient(90deg,{NEGRO} 45%,rgba(11,11,15,.2) 75%,rgba(11,11,15,0))}}
.ptxt{{position:absolute;left:90px;bottom:120px;color:#fff}} .eti{{font-size:13px;letter-spacing:.25em;text-transform:uppercase;color:#9CA3AF}} .portada h1{{font-size:110px;font-weight:800;letter-spacing:-.03em;margin:14px 0 6px;line-height:1}}
.rol{{font-size:30px;font-weight:600}} .lema{{font-size:22px;color:{ELEC};font-weight:700;margin-top:26px;letter-spacing:.04em}}
.cita{{font-size:31px;font-weight:600;line-height:1.4;max-width:1300px;margin-bottom:56px}}
.tres{{display:grid;grid-template-columns:1fr 1fr 1fr;gap:60px;border-top:1px solid #e4e4e7;padding-top:30px}} .az{{color:{AZUL};font-weight:700;font-size:24px}}
.dos{{display:grid;grid-template-columns:1fr 1fr;gap:90px}} .gr{{font-size:30px;font-weight:700;line-height:1.3}}
.tags span{{display:inline-block;border:1.5px solid {NEGRO};border-radius:40px;padding:8px 20px;margin:0 10px 10px 0;font-weight:600;font-size:17px}}
.lista{{list-style:none;padding:0;margin:0}} .lista li{{font-size:21px;padding:14px 0;border-bottom:1px solid #e4e4e7}}
.pal{{display:grid;grid-template-columns:repeat(4,1fr);gap:22px}} .sw{{height:300px;border-radius:6px;color:#fff;padding:24px;display:flex;flex-direction:column;justify-content:flex-end}} .sw.cl{{color:{NEGRO};border:1px solid #e4e4e7}}
.sw b{{font-size:22px}} .sw span{{font-size:15px;opacity:.85;margin-top:4px}} .sw em{{font-style:normal;font-size:14px;opacity:.7;margin-top:10px}}
.prueba{{display:grid;grid-template-columns:1fr 1fr;gap:22px;margin-top:22px}} .pb{{border:1px solid #e4e4e7;border-radius:6px;padding:34px;font-size:34px;font-weight:800}}
.t1{{font-size:150px;font-weight:800;letter-spacing:-.04em;line-height:1}} .t2{{font-size:24px;font-weight:800;margin:10px 0 40px}} .esc{{display:grid;gap:26px}} small{{display:block;font-size:12px;letter-spacing:.18em;text-transform:uppercase;color:{GRIS};margin-bottom:8px}}
.ba{{display:flex;gap:20px;align-items:flex-start}} .col{{flex:none}} .flecha{{font-size:40px;color:#52525b;margin-top:200px}}
.g3{{display:grid;grid-template-columns:repeat(3,190px);gap:10px}} .g3 img,.g2 img,.g1 img{{width:100%;height:420px;object-fit:cover;border-radius:4px;filter:grayscale(25%)}} .g1{{width:230px}} .g2{{display:grid;grid-template-columns:repeat(2,200px);gap:10px}} .g2 img{{filter:none}}
.prueba4{{display:grid;grid-template-columns:repeat(4,1fr);gap:22px}} figure{{margin:0}} figure img{{width:100%;height:440px;object-fit:cover;border-radius:4px}} figcaption{{font-size:16px;font-weight:600;margin-top:12px}}
.apl{{display:grid;grid-template-columns:auto auto auto;gap:40px;justify-content:start}} .row{{display:flex;gap:10px}} .c{{height:380px;border-radius:4px}}
.f2{{width:270px;height:480px;background:#fff;border:1px solid #e4e4e7;border-radius:6px;overflow:hidden;display:flex;flex-direction:column}} .f2a{{height:190px;position:relative}} .f2a img{{width:100%;height:100%;object-fit:cover}} .sub{{position:absolute;bottom:14px;left:0;right:0;text-align:center;color:#fff;font-weight:800;font-size:17px;text-shadow:0 1px 4px rgba(0,0,0,.6)}} .mini-n{{font-size:15px;color:#6B7280;max-width:300px;margin-top:14px}}
.f2t{{height:45px;display:flex;align-items:center;justify-content:center;text-align:center;font-weight:800;font-size:11.5px;line-height:1.15;padding:0 10px}} .f2b{{flex:1;background:#fff}} .f2b img{{width:100%;height:100%;object-fit:contain}}
.yt{{position:relative;width:380px;height:214px;background:#fff;border:1px solid #e4e4e7;border-radius:6px;overflow:hidden}} .yt img{{position:absolute;right:0;top:0;height:100%;width:52%;object-fit:cover}} .ytt{{position:absolute;left:22px;top:50%;transform:translateY(-50%);width:42%;font-size:24px;font-weight:800;line-height:1.08;letter-spacing:-.01em}}
.tri{{display:grid;grid-template-columns:1fr 1fr 1fr;gap:60px}} .tri>div{{border-top:2px solid {NEGRO};padding-top:26px}} .n{{font-size:80px;font-weight:800;color:{AZUL};letter-spacing:-.03em;line-height:1;margin-bottom:16px}} .ej{{color:{GRIS};font-size:17px}}
table{{width:100%;border-collapse:collapse}} th{{text-align:left;font-size:12px;letter-spacing:.18em;text-transform:uppercase;color:{GRIS};padding:0 0 14px}}
td{{padding:15px 0;border-top:1px solid #e4e4e7;font-size:19px}} td.v{{color:{GRIS};width:90px}} td.b{{font-weight:700}}
.cierre{{position:absolute;left:90px;right:90px;top:280px}} .flujo{{display:flex;align-items:center;gap:30px;font-size:44px;font-weight:800;margin:20px 0 40px}} .flujo i{{font-style:normal;color:#52525b}} .flujo .z{{color:{ELEC}}} .cierre p{{color:#d4d4d8;font-size:24px;max-width:1100px}}'''

html = f'<!doctype html><html><head><meta charset="utf-8"><style>{css}</style></head><body>{"".join(P)}</body></html>'
out_html = AQUI / 'BRANDING-ABEL.html'; out_html.write_text(html, encoding='utf-8')
png_dir = AQUI / 'BRANDING-ABEL_paginas'; png_dir.mkdir(exist_ok=True)
for v in png_dir.glob('*.png'):
    v.unlink()
js = f'''import {{ chromium }} from 'playwright-core'; import {{ readdirSync }} from 'node:fs';
const base = process.env.LOCALAPPDATA + '/ms-playwright', hs = readdirSync(base).filter(d => d.startsWith('chromium_headless_shell-')).sort().reverse()[0];
const b = await chromium.launch({{ executablePath: `${{base}}/${{hs}}/chrome-headless-shell-win64/chrome-headless-shell.exe`, args: ['--allow-file-access-from-files'] }});
const p = await b.newPage({{ viewport: {{ width: 1600, height: 900 }} }}); await p.goto({json.dumps(out_html.as_uri())}); await p.waitForTimeout(1500);
await p.pdf({{ path: {json.dumps(str(AQUI / 'BRANDING-ABEL.pdf'))}, width: '1600px', height: '900px', printBackground: true }});
const n = await p.$$eval('section', s => s.length);
for (let i = 0; i < n; i++) {{ const el = (await p.$$('section'))[i]; await el.screenshot({{ path: {json.dumps(str(png_dir))} + '/' + String(i + 1).padStart(2, '0') + '.png' }}); }}
await b.close();'''
(TAB / '_brand_tmp.mjs').write_text(js, encoding='utf-8')
subprocess.run(['node', '_brand_tmp.mjs'], cwd=TAB, check=True)
(TAB / '_brand_tmp.mjs').unlink()
print('ok', len(P), 'páginas')
