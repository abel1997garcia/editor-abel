---
name: carpeta-definitiva-reels
description: En reels/ (carpeta definitiva para subir) guardar SOLO el mp4 final y su .txt; ondas, voces, espectrogramas y guiones van en trabajo/
metadata:
  type: feedback
---

Abel (2026-10-18): «cuando guardes el contenido en la carpeta definitiva para subirlo, solamente el reel definitivo y
el texto que va; no me guardes ni la onda, ni la voz como archivo aparte, ni nada».

- `reels/` = SOLO `<reel>.mp4` (con su audio) + `<reel>.txt` (descripción de Instagram).
- Todo lo demás en `trabajo/`: voz.wav, ondas (onda.py ya las escribe en trabajo/reels/<reel>/), espectrogramas,
  montaje.json, y los guiones de corte en `trabajo/specs/` (antes reels/specs).
- No copiar la voz a reels/ para que la escuche: darle la ruta de trabajo/reels/<reel>/voz.wav.

**Why:** es la carpeta de la que sube los reels; cualquier otro archivo estorba.
**How to apply:** el proceso de edición no cambia ([[audio-primero]], CHECKLIST_REELS_ALLAN.md); antes de entregar,
comprobar que en reels/ solo hay pares .mp4/.txt.
