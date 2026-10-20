---
name: audio-manda
description: Principio de Abel para TODA edición (reels, horizontales, reels de horizontales, Allan): primero el audio (cortes, onda, espectrograma, escucha), luego el vídeo se sincroniza a él
metadata:
  type: feedback
---

Abel 16/10/2026: «el audio es el que manda… y luego construir el vídeo a su alrededor. Eso es fundamental». Vale para los reels de tablet, para los vídeos HORIZONTALES (ver dónde se equivoca, muletillas, repeticiones, vuelve a empezar, se traba), para los reels que salen de los horizontales y para el proyecto de Allan (MEDIUM ALLAN).

**Why:** lo que se oye es lo que importa; trabajar primero el audio (islas, onda, espectrograma, escuchar cada corte, decidir qué se corta) y solo después sincronizar y cortar el vídeo va mucho más rápido y sale mejor (un solo render).

**How to apply:** mismo método que [[proceso-rapido-islas]]: decidir los cortes (también los de CONTENIDO: muletillas, repeticiones, frases a medias) sobre el audio, verificar el audio, y después el vídeo. Cambia solo el ritmo: horizontales con pausas más largas (lo ya estipulado en `limpiar_largo.py`), Allan pausado (máx. ~0,55 s). Se aplicará cuando Abel pase un horizontal; no tocar las herramientas de horizontales/Allan hasta entonces.

**Flujo acordado para los HORIZONTALES (Abel 20/10/2026):** Abel manda el vídeo EN BRUTO y lo limpio yo entero. Orden: (1) AUDIO primero — espectrograma y onda, quitar muletillas, repeticiones, frases que vuelve a empezar, silencios, y donde una frase se pueda decir igual sin repetir algo o sin un conector, dejarla más fluida ([[sin-conectores]]); (2) sincronizar el VÍDEO a ese audio (vídeo de YouTube listo); (3) sobre el vídeo limpio, apuntar en `reels_banco.md` TODOS los ganchos y las estructuras (colleja + solución por idea) bien esquematizados, y combinarlos gancho × estructura de la misma idea ([[reels-marca-personal]] 7b); (4) reels con plano cerca + zoom alterno + mejora reforzada. Etiquetar cada reel por tipo ([[mezcla-contenido]]).
- **Audio del largo = el mismo tratamiento que los reels** (Abel 20/10/2026): limpieza de voz, voz suave igualada, volumen igualado (como `_voz_suave.wav` de los reels), pero sobre el vídeo entero.
- **Motion graphics SOLO en los primeros ~30 s del vídeo de YouTube** (Abel 20/10/2026, para darle mucho dinamismo al arranque). Se generan DOS salidas de la misma línea de tiempo limpia: (a) `limpio` SIN grafismos → de aquí salen los reels (si un reel usa el gancho del principio, va sin esos grafismos); (b) `youtube` = limpio + capa de motion graphics en 0-30 s. Nunca sacar reels del (b). Estilo de los grafismos: pendiente de proponer y probar con el primer horizontal.
