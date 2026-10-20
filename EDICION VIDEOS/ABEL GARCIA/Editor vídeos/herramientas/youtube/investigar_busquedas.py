"""Investiga búsquedas reales del autocompletado de YouTube y comprueba título SEO y palabras clave.

Uso:
  python investigar_busquedas.py "como conseguir clientes" "miedo a cobrar" ...
  python investigar_busquedas.py --comprobar "TÍTULO SEO" "palabra 1, palabra 2, ..." [más pares]

Investigar, para cada búsqueda:
- demanda: cuántas sugerencias distintas salen al añadir
  « a», « b»… « z» (cuantas más, más se busca);
- TODAS las sugerencias de YouTube que salen así: de ahí se sacan el título SEO
  y las palabras clave.

Comprobar: cada palabra clave tiene que salir en el autocompletado de YouTube (tal cual o
como comienzo de una sugerencia),
y el TÍTULO SEO tiene que empezar por la primera palabra clave (la búsqueda del vídeo).
"""
import json
import string
import sys
import time
import unicodedata
import urllib.parse
import urllib.request


def sugerencias(q):
    url = ("https://suggestqueries.google.com/complete/search?client=firefox&ds=yt&hl=es&gl=es"
           + "&q=" + urllib.parse.quote(q))
    for intento in range(4):
        try:
            with urllib.request.urlopen(url, timeout=10) as r:
                return json.loads(r.read().decode("utf-8", "replace"))[1]
        except (urllib.error.URLError, TimeoutError):
            if intento == 3:
                raise
            time.sleep(5 * (intento + 1))


def expandidas(q):
    vistas = set(sugerencias(q))
    for letra in string.ascii_lowercase:
        vistas.update(sugerencias(f"{q} {letra}"))
    return vistas


def norma(t):
    t = unicodedata.normalize("NFD", t.lower())
    return " ".join("".join(c for c in t if c.isalnum() or c == " ").split())


def comprobar(titulo, texto):
    claves = [k.strip() for k in texto.split(",")]
    fallos = [k for k in claves
              if not any(f"{norma(s)} ".startswith(f"{norma(k)} ") for s in sugerencias(k))]
    if not norma(titulo).startswith(norma(claves[0])):
        fallos.append(f"el título no empieza por «{claves[0]}»")
    if len(texto) > 500:
        fallos.append(f"palabras clave: {len(texto)} caracteres (máx. 500)")
    elif len(texto) < 450:
        print(f"  ⚠ palabras clave: {len(texto)} caracteres; acércate a 500 SOLO con búsquedas del tema del vídeo")
    if len(titulo) > 100:
        fallos.append(f"título: {len(titulo)} caracteres (máx. 100)")
    print(f"== {titulo}: {'OK' if not fallos else 'FALLA'}")
    for f in fallos:
        print(f"  ✗ {f}")
    return not fallos


if sys.argv[1:2] == ["--comprobar"]:
    pares = sys.argv[2:]
    sys.exit(0 if all([comprobar(t, k) for t, k in zip(pares[::2], pares[1::2])]) else 1)

for q in sys.argv[1:]:
    yt = expandidas(q)
    print(f"== {q}  ·  demanda={len(yt)}")
    for s in sorted(yt):
        print(f"  {s}")
