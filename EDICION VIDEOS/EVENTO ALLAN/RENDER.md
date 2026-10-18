# Cómo renderizar el vídeo del evento en tu ordenador

Todo está preparado: la voz de Allan ya está sincronizada palabra a palabra con los textos, las fotos, los clips y la respiración guiada. Solo falta generar el MP4.

## Opción fácil: díselo a Claude Code
Abre Claude Code en la carpeta `EDICION VIDEOS/EVENTO ALLAN` y escribe:

> Lee RENDER.md y renderiza el vídeo del evento (versión con sesiones reales).

## Opción manual (Windows)
1. Instala **Node.js LTS** desde nodejs.org, si no lo tienes.
2. Abre una terminal en `EDICION VIDEOS\EVENTO ALLAN` y ejecuta, solo la primera vez:
   ```
   npm install
   npx playwright install chromium
   ```
3. **(Opcional) Música:** copia tu pista, estilo Gladiator, como `audio\musica.mp3`. Se mezcla sola debajo de la voz: baja cuando Allan habla, entra con un fundido y sale con otro al final. Si dura menos que el vídeo, se repite.
4. Renderiza:
   ```
   npm run render                 (versión CON los 3 momentos de sesión real, ~4:15)
   npm run render:sin-prueba      (versión SIN ellos, ~3:47)
   ```
5. El vídeo sale en `salida\Allan_Garcia_evento.mp4` (1920×1080, 30 fps).

**Para revisar solo un trozo antes de hacerlo entero:**
`node render/render_local.mjs --desde=140 --hasta=190`

**Para ir más rápido:** `--workers=8` (por defecto usa todos los núcleos menos uno).

## Qué hay en la carpeta
| Archivo | Qué es |
|---|---|
| `presentacion.html` | La animación completa (motion graphics). Se puede abrir en Chrome para verla. |
| `tiempos.js` | El momento exacto en que Allan dice cada palabra. Lo genera `render/alinear.py`; no se edita a mano. |
| `audio/voz_allan.mp3` | La voz original de Allan. La limpieza y la nivelación se hacen al renderizar. |
| `audio/m1…m3.wav` | El audio de los 3 momentos de sesión real. |
| `clips/` | Los 3 momentos verticales y las 22 caras del muro (11 familias distintas). |
| `fotos/` | La abuela, el retrato, el evento, la pluma y el cielo. |
| `render/render_local.mjs` | El script que lo genera todo. |
| `render/transcribir.py`, `render/alinear.py` | Para resincronizar si Allan regraba alguna frase. |

## Si Allan regraba el audio
1. Transcribe palabra a palabra: `python render/transcribir.py <modelo_parakeet> audio/voz_allan.mp3 render/datos/transcripcion_voz.json` (modelo: sherpa-onnx-nemo-parakeet-tdt-0.6b-v3-int8, en las releases de k2-fsa/sherpa-onnx en GitHub).
2. Exporta las escenas y alinea: `python render/alinear.py escenas.json render/datos/transcripcion_voz.json tiempos_con.json con`, y lo mismo con `sin`.
3. Regenera `tiempos.js` con los dos resultados. O, más fácil, pídeselo a Claude Code.
