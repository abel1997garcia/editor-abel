"""PDF limpio (A4, Montserrat) para los documentos de marca de Abel. Usa el Chrome de Playwright."""
import html, json, subprocess
from pathlib import Path

TAB = Path.home() / 'Desktop/EDICION VIDEOS/ABEL GARCIA/Editor vídeos/herramientas/tablero'
AZUL = '#1D4ED8'


def a_pdf(salida, titulo, subtitulo, intro, secciones, tabla=False):
    """secciones = [(titulo, items)]; items = textos, o pares (limitante, necesaria) si tabla=True."""
    fuente = (TAB / 'Montserrat-Variable.ttf').as_uri()
    secs, n = [], 0
    for t, items in secciones:
        if tabla:
            filas = ''
            for a, b in items:
                n += 1
                filas += f'<tr><td class="n">{n}</td><td>{html.escape(a)}</td><td class="b">{html.escape(b)}</td></tr>'
            cuerpo = f'<table><tr><th></th><th>Creencia limitante</th><th>Creencia necesaria</th></tr>{filas}</table>'
        else:
            lis = ''
            for d in items:
                n += 1; lis += f'<li value="{n}">{html.escape(d)}</li>'
            cuerpo = f'<ol>{lis}</ol>'
        secs.append(f'<section><h2>{html.escape(t)}</h2>{cuerpo}</section>')
    ps = ''.join(f'<p>{html.escape(p).replace("**", "")}</p>' for p in intro)
    doc = f'''<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{{font-family:M;src:url("{fuente}")}}
body{{font-family:M,sans-serif;color:#111;margin:0;font-size:10.5pt;line-height:1.45}}
.port{{height:250mm;display:flex;flex-direction:column;justify-content:center;padding:0 18mm;page-break-after:always}}
.port h1{{font-size:34pt;font-weight:800;margin:0 0 6mm;letter-spacing:-.02em}}
.port .f{{font-size:15pt;font-weight:700;color:{AZUL};margin:0 0 10mm}}
.port p{{font-size:11pt;color:#444;max-width:155mm}}
section{{padding:0 16mm;page-break-before:always}}
h2{{font-size:16pt;font-weight:800;border-bottom:3px solid #111;padding-bottom:2mm;margin:4mm 0 5mm}}
li{{margin:0 0 2.4mm;padding-left:1mm}} li::marker{{color:{AZUL};font-weight:800}}
table{{border-collapse:collapse;width:100%}} th{{text-align:left;font-size:9pt;color:#666;padding:1.5mm}}
td{{vertical-align:top;padding:2mm 1.5mm;border-top:1px solid #e5e5e5}} td.n{{color:{AZUL};font-weight:800;width:7mm}}
td.b{{font-weight:600;color:#0b2a6f}}
</style></head><body>
<div class="port"><h1>{html.escape(titulo)}</h1><div class="f">{html.escape(subtitulo)}</div>{ps}
<p style="margin-top:14mm;font-weight:700">Abel García · 2026</p></div>
{''.join(secs)}</body></html>'''
    tmp = Path(salida).with_suffix('.html'); tmp.write_text(doc, encoding='utf-8')
    js = f'''import {{ chromium }} from 'playwright-core'; import {{ readdirSync }} from 'node:fs'; import {{ pathToFileURL }} from 'node:url';
const base = process.env.LOCALAPPDATA + '/ms-playwright', hs = readdirSync(base).filter(d => d.startsWith('chromium_headless_shell-')).sort().reverse()[0];
const b = await chromium.launch({{ executablePath: `${{base}}/${{hs}}/chrome-headless-shell-win64/chrome-headless-shell.exe`, args: ['--allow-file-access-from-files'] }});
const p = await b.newPage(); await p.goto(pathToFileURL({json.dumps(str(tmp))}).href); await p.waitForTimeout(500);
await p.pdf({{ path: {json.dumps(str(salida))}, format: 'A4', margin: {{ top: '16mm', bottom: '16mm' }}, printBackground: true,
  displayHeaderFooter: true, headerTemplate: '<span></span>', footerTemplate: '<div style="font-size:8pt;width:100%;text-align:center;color:#999"><span class="pageNumber"></span></div>' }});
await b.close();'''
    (TAB / '_pdf_tmp.mjs').write_text(js, encoding='utf-8')
    subprocess.run(['node', '_pdf_tmp.mjs'], cwd=TAB, check=True)
    (TAB / '_pdf_tmp.mjs').unlink(); tmp.unlink()
