---
name: entorno-skill-animaciones
description: "Setup and Windows gotchas for the animaciones-horizontal-combinadas video skill on Abel's PC"
metadata:
  node_type: memory
  type: project
  originSessionId: d5e16cfe-1dfc-4d01-ac23-7f43e2a0e419
  modified: 2026-10-04T23:30:31.701Z
---

La skill `animaciones-horizontal-combinadas` (de skill_edicion_video_v3.zip) está instalada en `~/.claude/skills/` (05/10/2026). PC: RTX 2060 6 GB, Python 3.12, Node 22.

- PyTorch: instalar con CUDA (`--index-url https://download.pytorch.org/whl/cu124`); el pip por defecto en Windows es solo CPU.
- faster-whisper 1.2.1 falla con `av` 19 (`metadata_errors`): fijar `av` 18.1.0 (`pip install --only-binary=:all: "av>=15,<19"`; no hay compilador de C++).
- La skill está escrita para «Josema». Para Abel se usa en modo «cara» para los vídeos largos ([[estilo-videos-largos-stickman]]); los reels van con `herramientas/reel_yapping.py` ([[reels-marca-personal]]).
- OpenCV 5 ya no trae los detectores Haar: para las caras se usa YuNet (`modelo_cara()` de `cortar.py` de la skill).
- Tipografías en `Editor vídeos/herramientas/fuentes/` (Montserrat ExtraBold estática, generada de la variable con fontTools, porque libass no elige bien el peso de una variable) y `Referencias/fuentes/Inter-Variable.ttf`.
- Sus tomas pueden acabar con una cartela negra quemada (CTA «Comenta para elegir el próximo destino»): mirar la cola antes de alargarla.
- `anim.py render -h` NO muestra ayuda: lanza un render completo. Para montar se usa `anim.py montar` (renderiza solo los planos de animación).
- En `geq` de ffmpeg el tiempo es `T` (no `t`). Grafos largos: `-/filter_complex archivo` (límite de longitud de órdenes en Windows).
- `revisar --hoja <nombre>` guarda en `trabajo/revision/<nombre>.png` (no acepta ruta).
- Citas de los vídeos largos: `herramientas/fuentes/InterCita.ttf` (Inter estática wght 900, familia «Inter Cita»).

- **Llevarlo a otro ordenador:** `herramientas/empaquetar.py` crea `Escritorio/PAQUETE_EDICION_ABEL.zip` (editor + Fábrica + música + skills + las dos memorias, sin vídeos); la guía es `INSTALAR.md`. Volver a ejecutarlo tras cambios importantes.
