"""Mete trabajo/escenas.js en index.html (copia limpia en trabajo/index_plantilla.html)."""
import re, shutil
from pathlib import Path
if not Path('trabajo/index_plantilla.html').exists(): shutil.copy('index.html', 'trabajo/index_plantilla.html')
s = open('trabajo/index_plantilla.html', encoding='utf-8').read()
s = re.sub(r"const T = \{.*?\n\};", "const T = {};", s, count=1, flags=re.S)
fin = '/* =========================== FIN DE LA DEMO =========================== */'
a = s.index('/* =====================================================================\n   ELEMENTOS')
b = s.index(fin) + len(fin)
s = s[:a] + open('trabajo/escenas.js', encoding='utf-8').read().rstrip('\n') + s[b:]
# Inter cargada antes de layout() y del primer fotograma
s = s.replace("'italic 400 20px \"Instrument Serif\"'];", "'italic 400 20px \"Instrument Serif\"', '800 20px InterV', '600 20px InterV', '700 20px InterV'];")
assert "800 20px InterV" in s
open('index.html', 'w', encoding='utf-8').write(s)
print('ok')
