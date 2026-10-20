"""Crea la skill de claude.ai con la rutina diaria (para usarla desde el móvil).

Uso: python paquete_claude_web.py
Crea FÁBRICA DE CONTENIDO/07_PLANES_GRABACION/CLAUDE_MOVIL/fichas-youtube-abel.zip
(SKILL.md = la rutina + CONTEXTO_ABEL.md = los archivos de su marca).
Vuelve a ejecutarlo y a subir el .zip en claude.ai (Ajustes → Skills) cuando cambien la rutina,
su marca o el banco de ideas.
"""
import zipfile
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[4]
FABRICA = RAIZ / "FÁBRICA DE CONTENIDO"
PLANES = FABRICA / "07_PLANES_GRABACION"
MARCA = FABRICA / "01_MI_MARCA"
ARCHIVOS = [
    MARCA / "00-avatar-operativo.md",
    MARCA / "A-QUIEN-LE-VENDO.md",
    MARCA / "CREENCIAS-LIMITANTES-A-NECESARIAS.md",
    MARCA / "VOZ-DEL-CLIENTE.md",
    MARCA / "COMO-LO-EXPLICO.md",
    PLANES / "BANCO_IDEAS_YOUTUBE.md",
    MARCA / "creencias-y-frases-de-batalla.md",
    MARCA / "afirmaciones.md",
    MARCA / "_indice-banco.md",
    MARCA / "mi-voz" / "mi-voz.md",
    MARCA / "02-catalogo-momentos-concretos.md",
    RAIZ / "ABEL GARCIA" / "Editor vídeos" / "Referencias" / "lavri" / "ANALISIS.md",
]
CABECERA = """---
name: fichas-youtube-abel
description: Rutina diaria de Abel García - 3 fichas de YouTube (canal principal, energía sexual y documentación) con su SEO, y 3 stories (personal, laboral, ayudar), registradas en la hoja «Registro Youtube · Abel». Úsala siempre que Abel pida las fichas, las ideas de YouTube o las stories del día, o algo de SEO, títulos, listas o palabras clave de sus canales.
---

> **En claude.ai:** todos los archivos que cita esta rutina están dentro de `CONTEXTO_ABEL.md`, en esta misma skill (cada uno empieza por «# ARCHIVO:»). Lo que dice «en el ordenador» no aplica aquí: usa lo que dice «en el móvil».

"""

partes = ["# Contexto de Abel para la rutina diaria (cada archivo empieza por «# ARCHIVO:»)"]
for ruta in ARCHIVOS:
    texto = ruta.read_text(encoding="utf-8")
    if ruta.name == "_indice-banco.md":  # solo el bloque que usa la rutina
        texto = "\n".join(l for l in texto.splitlines()
                          if l.startswith("| ID") or "Masculinidad, autocontrol" in l)
    partes.append(f"# ARCHIVO: {ruta.name}\n\n{texto.strip()}")

rutina = (PLANES / "RUTINA_DIARIA_YOUTUBE_Y_STORIES.md").read_text(encoding="utf-8")
salida = PLANES / "CLAUDE_MOVIL" / "fichas-youtube-abel.zip"
salida.parent.mkdir(exist_ok=True)
with zipfile.ZipFile(salida, "w", zipfile.ZIP_DEFLATED) as z:
    z.writestr("fichas-youtube-abel/SKILL.md", CABECERA + rutina)
    z.writestr("fichas-youtube-abel/CONTEXTO_ABEL.md", "\n\n---\n\n".join(partes) + "\n")
print(salida)
