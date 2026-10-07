# Instalar el sistema de edición de Abel en otro ordenador

Paquete: `PAQUETE_EDICION_ABEL.zip`. Lleva todo menos los vídeos (grabaciones, tomas y vídeos finales: esos se pasan aparte, por ejemplo con un disco o Google Drive).

## Qué hay dentro

| Carpeta del zip | Qué es | Dónde va en el ordenador nuevo |
|---|---|---|
| `EDICION VIDEOS/ABEL GARCIA/Editor vídeos/` | El editor: herramientas, formatos de reels, referencias, configuraciones | `Escritorio\EDICION VIDEOS\ABEL GARCIA\Editor vídeos\` |
| `EDICION VIDEOS/FÁBRICA DE CONTENIDO/` | El gestor de contenido: cerebro de marca, planes de grabación, tablero | `Escritorio\EDICION VIDEOS\FÁBRICA DE CONTENIDO\` |
| `EDICION VIDEOS/MUSICA/` | La música de los reels (emocional y épica) | `Escritorio\EDICION VIDEOS\MUSICA\` |
| `skills/` | Las skills de Claude (animaciones + Skool Scaling) | `C:\Users\<usuario>\.claude\skills\` |
| `memoria/editor/` y `memoria/fabrica/` | La memoria de Claude de cada proyecto (lo aprendido) | ver paso 3 |

**Importante:** pon las carpetas en la misma ruta (`Escritorio\EDICION VIDEOS\...`). Las herramientas y la memoria cuentan con esas rutas.

## Pasos

### 1. Programas (una vez)
- **Windows 10/11** con **tarjeta NVIDIA** y su driver al día (sin NVIDIA funciona, pero transcribir y recortar va mucho más lento).
- **Python 3.12** (python.org; marca «Add to PATH»).
- **Node.js 22** (nodejs.org).
- **ffmpeg** (versión «full» de gyan.dev) añadido al PATH.
- **Claude Code** (la app de escritorio de Claude) con tu cuenta.

### 2. Descomprimir y colocar
Descomprime el zip y mueve cada carpeta a su sitio según la tabla de arriba.

### 3. Memoria de Claude
Claude guarda la memoria de cada proyecto en `C:\Users\<usuario>\.claude\projects\<nombre>\memory\`, y `<nombre>` es la ruta de la carpeta con los símbolos cambiados por guiones:
- Editor: `C--Users-<usuario>-Desktop-EDICION-VIDEOS-ABEL-GARCIA-Editor-v-deos` ← copia aquí `memoria/editor/`
- Fábrica: `C--Users-<usuario>-Desktop-EDICION-VIDEOS-F-BRICA-DE-CONTENIDO` ← copia aquí `memoria/fabrica/`

(En este ordenador `<usuario>` es `Clap`. Si en el nuevo tu usuario se llama distinto, cambia esa parte del nombre.)

### 4. Que Claude instale el resto
Abre Claude Code en la carpeta `Editor vídeos` y dile:

> «Instala el entorno siguiendo INSTALAR.md»

Claude hará esto (te pedirá permiso para cada descarga):
- Librerías de Python:
  - `pip install torch==2.6.0 torchaudio==2.6.0 --index-url https://download.pytorch.org/whl/cu124`
  - `pip install faster-whisper==1.2.1 ctranslate2==4.8.2 "av==18.1.0" --only-binary=:all:`
  - `pip install opencv-python onnxruntime numpy pillow fonttools scipy soundfile librosa nltk requests yt-dlp`
- Lo que necesita la skill de animaciones: `python <skill>/scripts/anim.py entorno --instalar` (Playwright y el navegador para renderizar).
- La primera vez que se use, se descargan solos los modelos: Whisper large-v3 (~3 GB), el alineador (~1,2 GB), el recorte de persona (RVM) y el detector de caras (YuNet).

### 5. Comprobar
Pídele a Claude: «Comprueba que todo funciona». Debe poder ejecutar `herramientas/limpiar_largo.py --texto` con una configuración de ejemplo, renderizar una animación de prueba y pasar `herramientas/pizarra/revisar.mjs`.

## Versiones con las que funciona (07/10/2026)
Python 3.12.7 · Node 22.22.3 · ffmpeg 8.1.1 · torch 2.6.0+cu124 · faster-whisper 1.2.1 · av 18.1.0 · opencv-python 5.0 · Playwright chromium_headless_shell-1243 · NVIDIA RTX 2060.
