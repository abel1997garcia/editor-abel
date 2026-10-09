---
name: referencias-virales
description: Abel ALREADY has an Apify-powered tracker for viral reference reels — Google Sheet «Tracker - ABEL.UNIDAD» (tab REFERENCIAS: he pastes the URL, Apify fills transcription). Never create new sheets/tabs for this
metadata:
  type: project
---

**NO crear hojas ni pestañas nuevas para referencias** (09/10/2026: creé «Referencias virales» y le molestó mucho: «ya tengo la otra que lo hace, no me líes»; borrada). Él pega SOLO la URL del reel; todo lo demás se rellena solo o lo hago yo.

**Lo que ya existe (Google Drive de Abel):**
- **«Tracker - ABEL.UNIDAD»** (Google Sheet, id `1zP5aknpaXob7fsVVIvaGTrrfix_rseSBwwATwLRayyY`). Funciona con **Apify** (los vídeos salen de `api.apify.com/.../key-value-stores`).
  - Pestaña **REFERENCIAS**: `url_reel`, que pega él, y `Estado` y `Transcripción`, que rellena la automatización (Estado = COMPLETADO).
  - Pestaña **Reels**: sus propios reels con url, fecha_publicacion, duracion_seg, reproducciones, likes, comentarios, caption, gancho, tema, tipo, por_que_funciona, titulo_nuevo, video_descarga, transcripcion. Sale de la plantilla «Reels_tracker_plantilla(1).xlsx».
- **«Referencias reels»** (Google Sheet, id `171W5sSMonD1FJ34tANzeGzzRMSukeAYtiwQ4bZwRa3k`, creada el 09/10 por la mañana en otra sesión de Claude): URL ← «TÚ SOLO PEGAS ESTO»; Estado, Tipo, Creador y visitas, Gancho original, Por qué funciona, Guion para grabar → enlace, Notas (Claude). **ES LA BUENA (Abel, 09/10/2026): «Referencias reels».** Ahí pega las URLs y yo relleno el resto; «Tracker» queda solo como su histórico de Apify.

**Mi parte:** a partir de la transcripción, analizar (gancho, colleja, solución, por qué funciona) y escribir el GUION ADAPTADO:
- con su estructura obligatoria y su voz;
- apuntando a la frase central y a `A-QUIEN-LE-VENDO`;
- en un Google Doc enlazado en esa misma hoja.
La referencia es esqueleto, no contenido.

Si hace falta otra vía: `python -m yt_dlp` descarga reels públicos sin iniciar sesión (sin reproducciones).

**Acceso a los reels comprobado el 09/10/2026** con un reel ajeno (@soyrebecaschimensky, DeCcXb5oYGs):
- `PYTHONIOENCODING=utf-8 python -m yt_dlp` descarga el vídeo y da fecha, likes, comentarios y creador SIN iniciar sesión;
- se transcribe con faster-whisper large-v3;
- NO da las visitas. Para las visitas: que él inicie sesión en Instagram en el navegador integrado, o usar su Apify (su token en un archivo local, nunca en el chat).
Los vídeos se guardan en `Editor vídeos/Referencias/virales/<código>.mp4`.
