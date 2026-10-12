---
name: estilo-videos-largos-stickman
description: "Abel's long horizontal videos (3 channels): by default clean edit + zooms + full-screen white key-phrase cards (no animations); whiteboard animations only when he asks"
metadata:
  node_type: memory
  type: project
  originSessionId: d5e16cfe-1dfc-4d01-ac23-7f43e2a0e419
  modified: 2026-10-05T18:25:19.404Z
---

Estilo de los vídeos largos de YouTube de Abel. **Es su producto principal**: ahí trata lo personal, rompe objeciones, se da a conocer y aporta mucho valor. Inspirado en «Como Automaticé por COMPLETO mi Edición de Video» (análisis en `Editor vídeos/Referencias/stickman/`), pero con fondo blanco.

## ESTÁNDAR (Abel, 11/10/2026): edición sencilla, SIN animaciones
Graba 3 horizontales al día (canal principal, energía sexual y documentación). Las animaciones eran ~70-80 % del gasto y del tiempo, así que por defecto ninguno las lleva:
- Se quitan silencios, errores y repeticiones; acercamiento leve y continuo y **zooms de énfasis** en sus opiniones fuertes, siempre fluidos. Sus planos nunca se reencuadran.
- **Frases clave como rompepatrón, SIEMPRE (5–8 por vídeo; Abel 12/10/2026: «la única animación por regla» en los horizontales):** pantalla blanca con la frase en negro (Inter 900), centrada y dentro del 4:3. Su voz sigue debajo y el corte es seco. Van en su historia, en la «galletita» y en sus frases de batalla.
- **Sonido:** su voz tal cual, sin música ni efectos. **El final no se toca**: lo cierra él.
- **Animaciones de pizarra: solo si Abel lo pide** (p. ej. un vídeo de venta). La receta está guardada abajo; no se borra nada.

## Cómo se hace (estándar)
Carpeta `VideosLargos/<tema>/`; `S = ~/.claude/skills/animaciones-horizontal-combinadas/scripts/anim.py`.
1. **Transcribir la grabación:** `S nuevo <tema>/transcripcion --video <grabación>` → `S transcribir --toma --nombres "…"` → corregir `edicion/guion.txt` (nombres: Club Unidad…) → `S alinear --toma` → copiar `edicion/tiempos.json` a `<tema>/toma_tiempos.json`.
2. **`limpieza.json`:** listar palabras con índice, huecos > 0,6 s y puntuación < 0,6. Campos:
   - `quitar`, `zooms`, `intacto_desde` (su cierre);
   - `frases`: `[["Tú eres\NTU NEGOCIO.", i0, i1]]`, con ≤ 22 caracteres por línea y una parte en MAYÚSCULAS.
   Palabras con puntuación 0 y < 0,1 s pegadas a otra igual son duplicados de Whisper: no se quitan.
3. `herramientas/limpiar_largo.py limpieza.json --texto`: revisar los planos < 1,5 s (ninguno en mitad de frase) y los tiempos de las frases. Luego `limpiar_largo.py limpieza.json` con `"salida": "<tema> - horizontal.mp4"` (~10 min).
   Sale el vídeo final más `.tiempos.json` y `.montaje.json`, que son lo que usa el reel F1.
4. **Comprobar el final** transcribiendo los últimos 5 s, mirar 3–4 fotogramas de frases, limpiar intermedios y actualizar el TABLERO de la Fábrica. Antes de editar, leer [[registro-edicion-abel]].

## Animaciones de pizarra (SOLO si Abel lo pide)
Inspiradas en «Como Automaticé por COMPLETO mi Edición de Video» (`Referencias/stickman/`), con fondo blanco. Animaciones a pantalla completa intercaladas con sus planos (≈ 60 % él), sin PiP. Todo dentro del 4:3 (x 280–1640) para poder sacar los reels.
- **Siempre pasa algo** (≤ 2 s), y lo escrito es lo que dice, casi literal. **Nada se pisa.** Primer minuto con > 13 cambios.
- **Personajes:** stickman de una pieza con posturas; para el cuerpo o la energía, la silueta grande. **Storytelling** con bocadillos, objetos, contadores, ✓/✗ y listas. Emojis algunas veces.
- **Aspecto:**
  - fondo #FFFFFF, Inter 800–900 en #111 que entra con la voz;
  - títulos 110–130 px, mínimo 56;
  - colores de los centros: raíz #C8372D, sacro #E06A1B, plexo #C99A00, corazón #1E7A46, garganta #1D7FD1, tercer ojo #3F3FB5, corona #7A3FC4;
  - líneas de 6–8 px que se dibujan solas.
- **Efectos de sonido** como en «dopamina v2».
- **Receta (aprobada con «La intención y energía masculina» y «Así empezaría mi marca personal desde 0»):**
  - limpieza sin `frases` y con `"salida": "toma_limpia.mov"`;
  - `S nuevo <tema>/anim --video toma_limpia.mov`; guion limpio en `edicion/guion.txt` y `trabajo/guion.txt`;
  - `S alinear --toma`; `S estilo --modo cara --sonido efectos --densidad media --subtitulos no`;
  - `S cortar --pre .2 --min-pausa 5 --inicio 0 --cola 1.4 --fin <dur − .05>`; `S alinear`; `S planos` (comprobar que CONFIG.dur = duración de la toma);
  - `ventanas.json` (≈ 40 %) → `pizarra/ventanas.py` → `pizarra/recortar_zooms.py`;
  - `escenas.js` (modelo `VideosLargos/empezar-desde-0/escenas.js`) → `pizarra/injertar.py` → `node pizarra/revisar.mjs anim` hasta «todo bien» → hojas `S revisar --hoja`;
  - `S montar` → `pizarra/postpro.py anim citas.json anim/out/anim_1080p30.mp4 "<tema> - horizontal.mp4"` (citas blancas sobre su cara).

## Vídeos derivados
- De un vídeo largo (30–40 min) puede pedir N vídeos de **mínimo 8 min**. Cada uno con **un gancho distinto, ligado a lo que se habla después en ese vídeo**, un hilo con sentido y un final limpio. Puede bastar con recortar y reordenar.

## Gancho
- **El gancho del horizontal NO se toca (Abel, 11/10/2026: «es fundamental»):** él piensa y graba un gancho específico para cada vídeo. El vídeo empieza tal cual lo grabó: nunca avance en frío, nunca otra frase delante, nunca reordenar. Dentro del gancho solo se quitan silencios y tropiezos. (Los ganchos de los reels son otra cosa: [[ganchos]].)
- Al editar, marcar (zoom o frase clave) los momentos en que cuenta su historia y los momentos de «galletita» aplicable, y poner foto o vídeo real de esa época ([[fotos-vida-abel]]). Si a un vídeo le falta su historia, decírselo para la próxima grabación: él quiere meterse más en su historia y contar cosas más profundas ([[criterios-contenido-util]]).
