# Instalar el sistema de edición de Abel en otro ordenador

Este repositorio, o el zip `PAQUETE_EDICION_ABEL_<fecha>.zip` del USB, lleva todo lo necesario para trabajar igual que en el ordenador original:
- el editor (horizontales y reels F1/F2/F3/F4);
- las reglas aprendidas (gancho, colleja, una idea, verificador de voz, estilo de voz para la música…);
- las skills y la memoria de Claude;
- la FÁBRICA DE CONTENIDO, la música y la biblioteca de imágenes;
- los flujos de n8n y la tarea programada.

**Qué NO lleva (a propósito):**
- los vídeos en bruto y los renders: pásalos aparte (disco o Google Drive);
- las contraseñas y claves: se ponen a mano (paso 6).

El zip del USB lleva además las fotos personales (FOTOS MIAS); GitHub no.

## Qué hay dentro y dónde va

| Carpeta | Qué es | Dónde va en el ordenador nuevo |
|---|---|---|
| `EDICION VIDEOS/` | Todo el escritorio de trabajo: `ABEL GARCIA/Editor vídeos` (editor), `FÁBRICA DE CONTENIDO`, `MUSICA`, `IMAGENES`, `MEDIUM ALLAN` (solo código y textos), logos y plantillas | `C:\Users\<usuario>\Desktop\EDICION VIDEOS\` |
| `skills/` | Skills de Claude: **animaciones-horizontal-combinadas** (la principal), Skool Scaling (5), HyperFrames, general-video, media-use | `C:\Users\<usuario>\.claude\skills\` |
| `memoria/editor`, `memoria/fabrica`, `memoria/medium-allan` | Lo que Claude ha aprendido de Abel en cada proyecto | ver paso 3 |
| `tareas-programadas/` | La tarea «Informe semanal de Instagram» (lunes a las 11:00) | ver paso 5 |
| `actualizar_copia.py` | El script que mantiene esta copia al día | — |

**Importante:** respeta las rutas (`Escritorio\EDICION VIDEOS\...`). Las herramientas y la memoria cuentan con ellas.

## 1. Programas (una vez)
- Windows 10/11 con **tarjeta NVIDIA** y su driver al día. Sin NVIDIA funciona, pero transcribir va mucho más lento.
- **Python 3.12** (marca «Add to PATH»), **Node.js 22**, **ffmpeg** (versión «full» de gyan.dev, en el PATH) y **Git**.
- **Claude** (app de escritorio) con tu cuenta.

## 2. Colocar los archivos
- **Desde GitHub:** `git clone https://github.com/abel1997garcia/editor-abel.git` y copia cada carpeta a su sitio según la tabla.
- **Desde el USB:** descomprime el zip y haz lo mismo.

## 3. Memoria de Claude
Claude guarda la memoria en `C:\Users\<usuario>\.claude\projects\<nombre>\memory\`. `<nombre>` es la ruta de la carpeta con los símbolos cambiados por guiones:
- Editor: `C--Users-<usuario>-Desktop-EDICION-VIDEOS-ABEL-GARCIA-Editor-v-deos` ← `memoria/editor/`
- Fábrica: `C--Users-<usuario>-Desktop-EDICION-VIDEOS-F-BRICA-DE-CONTENIDO` ← `memoria/fabrica/`
- Allan: `C--Users-<usuario>-Desktop-EDICION-VIDEOS-MEDIUM-ALLAN-Editor-Videos---Allan` ← `memoria/medium-allan/`

En el ordenador original `<usuario>` es `Clap`. Si el nuevo se llama distinto, cambia esa parte.

## 4. Que Claude instale el resto
Abre Claude en la carpeta `Editor vídeos` y dile: **«Instala el entorno siguiendo INSTALAR.md»**. Te pedirá permiso para cada descarga.

**1. Librerías de Python:**
- `pip install torch==2.6.0 torchaudio==2.6.0 --index-url https://download.pytorch.org/whl/cu124`
- `pip install faster-whisper==1.2.1 ctranslate2==4.8.2 "av==18.1.0" --only-binary=:all:`
- `pip install opencv-python onnxruntime numpy pillow pillow-heif fonttools scipy soundfile librosa nltk requests yt-dlp`

**2. Skill de animaciones:** `python <skill>/scripts/anim.py entorno --instalar` (Playwright y su navegador).

**3. Dependencias de Node** de las herramientas: en `Editor vídeos/herramientas/tablero/` ejecuta `npm install`. Las carpetas `node_modules` no van en la copia.

**4. video-use** (no va en la copia, es público): `git clone https://github.com/browser-use/video-use C:\Users\<usuario>\.claude\skills\video-use`

**5. Real-ESRGAN** (nitidez con IA) ya va dentro, en `herramientas/realesrgan/`.

La primera vez que se usen se descargan solos:
- los modelos de Whisper large-v3 (~3 GB);
- el alineador (~1,2 GB);
- RVM;
- YuNet.

## 5. Tarea programada
Copia `tareas-programadas/informe-semanal-instagram/` a `C:\Users\<usuario>\.claude\scheduled-tasks\` y pídele a Claude:
> «Recrea la tarea programada informe-semanal-instagram con el prompt de su SKILL.md, los lunes a las 11:00.»

Después pulsa «Ejecutar ahora» una vez para aprobar sus permisos.

## 6. Claves y contraseñas (a mano, nunca en el chat ni en GitHub)
- **`Editor vídeos/herramientas/youtube/youtube_config.json`:** la URL del webhook de n8n, la cabecera y la clave. Plantilla: `webhook`, `cabecera`, `clave`, `requiere_ok`, `desde`.
- **n8n:** los flujos se quedan en tu n8n, en la nube. Si hay que reimportarlos, están en `Editor vídeos/herramientas/youtube/` e `instagram/`. Pasos en `instagram/LEEME.md`.
  - Credenciales: token de Instagram (Query Auth `access_token`), Google Sheets y YouTube.
- **Claude:** `C:\Users\<usuario>\.claude\settings.json`, si usas un proveedor o una clave propios.

## 7. Comprobar
Pídele a Claude: «Comprueba que todo funciona». Tiene que poder:
- ejecutar `herramientas/reel_tablero.py <reels.json> --texto`;
- pasar `herramientas/verificar_audio.py` y `herramientas/estilo_voz.py` sobre un reel;
- renderizar una animación de prueba.

## Mantener la copia al día
En este ordenador: `python actualizar_copia.py --subir`, que actualiza GitHub. Con `--usb`, además crea el zip para el USB en el Escritorio.

## Versiones con las que funciona (09/10/2026)
- Python 3.12.7, Node 22.22.3, ffmpeg 8.1.1
- torch 2.6.0+cu124, faster-whisper 1.2.1, av 18.1.0, opencv-python 5.0, librosa 0.11.0
- Playwright chromium_headless_shell-1243
- NVIDIA RTX 2060
