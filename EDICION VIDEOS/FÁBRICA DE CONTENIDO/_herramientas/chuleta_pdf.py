"""Convierte una chuleta .md sencilla en un PDF limpio para leer al grabar.

Uso:  python _herramientas/chuleta_pdf.py 07_PLANES_GRABACION/PG-001_chuleta.md
Sintaxis admitida: '# título', '## bloque', '### subtítulo', '- viñeta', '> frase destacada',
**negrita**, líneas normales. Genera el PDF al lado del .md.
"""
import html, io, os, re, subprocess, sys, tempfile

CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
CSS = """
@page { size: A4; margin: 16mm 16mm; }
body { font-family: 'Segoe UI', Arial, sans-serif; font-size: 13.5pt; line-height: 1.45; color: #1d1d1d; }
h1 { font-size: 21pt; margin: 0 0 4px; }
.sub { color: #666; font-size: 11pt; margin-bottom: 14px; }
h2 { font-size: 15pt; margin: 18px 0 6px; padding: 6px 10px; background: #efeefb; border-radius: 6px; color: #3c3489; page-break-after: avoid; }
h3 { font-size: 12pt; margin: 10px 0 2px; color: #555; text-transform: none; }
ul { margin: 4px 0 6px 0; padding-left: 20px; }
li { margin: 3px 0; }
blockquote { margin: 6px 0; padding: 4px 10px; border-left: 3px solid #d85a30; background: #faece7; font-style: italic; }
.block { page-break-inside: avoid; }
"""

def inline(s):
    s = html.escape(s)
    return re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", s)

def to_html(md):
    out, in_ul, in_block = [], False, False
    def close_ul():
        nonlocal in_ul
        if in_ul: out.append("</ul>"); in_ul = False
    for raw in md.splitlines():
        line = raw.rstrip()
        if line.startswith("- "):
            if not in_ul: out.append("<ul>"); in_ul = True
            out.append(f"<li>{inline(line[2:])}</li>"); continue
        close_ul()
        if line.startswith("# "): out.append(f"<h1>{inline(line[2:])}</h1>")
        elif line.startswith("## "):
            if in_block: out.append("</div>")
            out.append(f'<div class="block"><h2>{inline(line[3:])}</h2>'); in_block = True
        elif line.startswith("### "): out.append(f"<h3>{inline(line[4:])}</h3>")
        elif line.startswith("> "): out.append(f"<blockquote>{inline(line[2:])}</blockquote>")
        elif line.startswith("_") and line.endswith("_"): out.append(f'<div class="sub">{inline(line[1:-1])}</div>')
        elif line: out.append(f"<p>{inline(line)}</p>")
    close_ul()
    if in_block: out.append("</div>")
    return f"<!doctype html><html><head><meta charset='utf-8'><style>{CSS}</style></head><body>{''.join(out)}</body></html>"

def main(path):
    md = io.open(path, encoding="utf-8").read()
    pdf = os.path.abspath(os.path.splitext(path)[0] + ".pdf")
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, encoding="utf-8") as f:
        f.write(to_html(md)); tmp = f.name
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
                    f"--print-to-pdf={pdf}", "file:///" + tmp.replace("\\", "/")],
                   check=True, capture_output=True)
    os.remove(tmp)
    print(pdf)

if __name__ == "__main__":
    main(sys.argv[1])
