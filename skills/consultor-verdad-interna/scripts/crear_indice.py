"""Genera referencias/indice-sintomas.md: cada entrada del diccionario con su línea y los libros que la mencionan.
Uso: python crear_indice.py  (vuelve a ejecutarlo cuando añadas libros)"""
import os, re, unicodedata
from collections import defaultdict

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LIBROS = os.path.join(BASE, "libros")
DICC = "DICCIONARIO BIODESCODIFICACION.txt"
EXCLUIR = {"LISA BOURBEAU", "LOUISE L. HAY", "LOUISE HAY", "DICCIONARIO", "BLOQUEO FISICO", "BLOQUEO EMOCIONAL",
           "BLOQUEO MENTAL", "BLOQUEO ESPIRITUAL", "SOLUCION POSIBLE", "CONFLICTO", "RESENTIR", "INDICE GENERAL"}

def norm(s):
    s = unicodedata.normalize("NFD", s.lower())
    return "".join(c for c in s if unicodedata.category(c) != "Mn")

# 1) entradas del diccionario
lines = open(os.path.join(LIBROS, DICC), encoding="utf-8", errors="ignore", newline="").read().split("\n")  # mismas líneas que Grep/Read
head = re.compile(r"^\s{0,40}([A-ZÁÉÍÓÚÑÜ][A-ZÁÉÍÓÚÑÜ ,()/\-\.]{2,60}?)\s*$")
entradas = defaultdict(list)
for i, l in enumerate(lines, 1):
    if i < 1900:  # índice inicial con números de página
        continue
    m = head.match(l)
    if m:
        t = re.sub(r"\s+", " ", m.group(1)).strip(" ,.-")
        if len(t) >= 3 and norm(t).upper() not in {norm(x).upper() for x in EXCLUIR}:
            entradas[t].append(i)

# agrupar por término principal (antes de coma o paréntesis)
grupos = defaultdict(list)
for t, ls in entradas.items():
    clave = re.sub(r"^(LAS|LOS|LA|EL) ", "", re.split(r"[,(]", t)[0].strip())
    grupos[clave].append((t, ls))

# 2) textos del resto de libros
textos = {}
for root, _, files in os.walk(LIBROS):
    for f in files:
        if f.endswith(".txt") and f != DICC:
            p = os.path.join(root, f)
            rel = os.path.relpath(p, LIBROS).replace("\\", "/")[:-4]
            textos[rel] = norm(open(p, encoding="utf-8", errors="ignore").read())

def raiz(clave):
    w = norm(clave)
    if " " not in w and len(w) > 5:
        w = re.sub(r"(es|s)$", "", w)  # rodillas -> rodilla, migrañas -> migraña
    return w

out = ["# Índice cruzado de síntomas y temas", "",
       "Generado con `scripts/crear_indice.py`. Para cada entrada del diccionario: sus líneas en "
       "`DICCIONARIO BIODESCODIFICACION.txt` (lee desde ahí 60–150 líneas) y los demás libros que la mencionan, "
       "con el número de menciones. **Consulta todas las fuentes que salgan con 2 o más menciones.** "
       "Los libros en inglés (Neville, Hill, Lipton-web) no aparecen aquí: búscalos con el término en inglés.", ""]
for clave in sorted(grupos, key=norm):
    r = raiz(clave)
    if len(r) < 3:
        continue
    pat = re.compile(r"\b" + re.escape(r))
    hits = []
    for rel, txt in textos.items():
        n = len(pat.findall(txt))
        if n:
            hits.append((n, rel))
    hits.sort(reverse=True)
    dic = "; ".join(f"{t} l.{','.join(map(str, ls))}" for t, ls in grupos[clave])
    otros = " · ".join(f"{rel} ({n})" for n, rel in hits[:12]) or "—"
    out.append(f"- **{clave}**: Diccionario: {dic} | {otros}")

with open(os.path.join(BASE, "referencias", "indice-sintomas.md"), "w", encoding="utf-8") as f:
    f.write("\n".join(out) + "\n")
print(len(grupos), "entradas")
