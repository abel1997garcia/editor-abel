---
name: imagen-reels
description: Todos los reels (de horizontales y verticales, cualquier formato) llevan la misma mejora de imagen: nitidez suave + contraste 1,03 + luz de la CARA compensada (herramientas/mejora_imagen.py)
metadata:
  type: feedback
---

Abel 16/10/2026: «para los reels que saques de los horizontales como los vídeos verticales tipo reels de cualquier formato, aplícales el mismo filtro de color, enfoque o nitidez… tanto si son oscuros o blancos, se compensarán un poco».

**Why:** se ven mejor y todos iguales; antes solo los TAB llevaban el toque de nitidez.

**How to apply:** `herramientas/mejora_imagen.py` → `filtro(fuente)` = unsharp 0,5 + eq contrast 1,03 + gamma que acerca la luz media de la CARA (no del encuadre: la pared blanca engañaba) a 112 (la de las tablet aprobadas), solo media distancia y entre 0,95 y 1,10. Ya está en `rapido/render.py`, `reel_yapping.py` (F1 de horizontales) y `reel_tablero.py` (F1/F2/F3/TAB, siempre). Nunca más fuerte: con el filtro fuerte «me veo un poco diferente» (15/10).

**Calidad perdida en la cadena (diagnóstico del 18/10/2026; Abel ve los vídeos de Rebeca mucho más nítidos):**
1. **Reels sacados de horizontales:** el recorte vertical de un 1080p deja ~608 px de ancho, estirados ×1,8, y salen blandos. Además, el horizontal de muestra (`Dejar_ir_emociones…1080p.mp4`) está a 2,7 Mbps, muy bajo. Solución: grabar los horizontales en 4K y a bitrate alto, o grabar en vertical lo que vaya a reels.
2. **Cadena YouTube → Repurpose → Instagram:** cada plataforma recomprime, y Repurpose coge la versión ya comprimida de YouTube. Solución: subir el MP4 original directo a Instagram, o que Repurpose lo coja del archivo original (Drive/Dropbox), no de YouTube. Activar en Instagram «Subir con la máxima calidad».
3. **Nuestro render no es el problema** (CRF 16-18).

**Reels de vídeos HORIZONTALES (Abel 19/10/2026):** como el plano va más cerca (imagen ampliada), llevan la capa REFORZADA: `filtro(fuente, horizontal=True)` = unsharp 0,9 + contraste 1,06 + saturación 1,08 + la misma gamma de la cara. Ya la aplica `reel_yapping.py`. Comparativa: `MarcaPersonal/virales/mejora_imagen_horizontales.png`.
