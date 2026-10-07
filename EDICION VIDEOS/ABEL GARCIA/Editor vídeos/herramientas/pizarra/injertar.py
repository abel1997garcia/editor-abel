"""Mete la pizarra de Abel en un proyecto de la skill (modo cara):
    python injertar.py <proyecto> <escenas.js>
index.html = plantilla limpia (trabajo/index_plantilla.html) con su bloque de demo sustituido por
libreria.js + TW (palabras de trabajo/tiempos.json) + escenas.js. Copia Inter a assets/fonts."""
import json, re, shutil, sys
from pathlib import Path
aqui = Path(__file__).resolve().parent
pro, esc = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
plantilla = pro / 'trabajo/index_plantilla.html'
if not plantilla.exists(): shutil.copy(pro / 'index.html', plantilla)
shutil.copy(aqui / 'assets/fonts/Inter-Variable.ttf', pro / 'assets/fonts/Inter-Variable.ttf')
s = plantilla.read_text(encoding='utf-8')
s = re.sub(r"const T = \{.*?\n\};", "const T = {};", s, count=1, flags=re.S)
fin = '/* =========================== FIN DE LA DEMO =========================== */'
a = s.index('/* =====================================================================\n   ELEMENTOS'); b = s.index(fin) + len(fin)
W = json.load(open(pro / 'trabajo/tiempos.json', encoding='utf-8'))
tw = 'const TW = ' + json.dumps([[w['w'], w['s'], w['e']] for w in W], ensure_ascii=False, separators=(',', ':')) + ';\n'
bloque = (aqui / 'libreria.js').read_text(encoding='utf-8') + '\n' + tw + esc.read_text(encoding='utf-8')
s = s[:a] + bloque.rstrip('\n') + s[b:]
s = s.replace("'italic 400 20px \"Instrument Serif\"'];", "'italic 400 20px \"Instrument Serif\"', '850 20px InterV', '600 20px InterV', '800 20px InterV'];")
assert "850 20px InterV" in s
(pro / 'index.html').write_text(s, encoding='utf-8')
print('ok ->', pro / 'index.html')
