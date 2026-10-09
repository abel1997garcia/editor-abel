---
name: flujo-reels-paso-a-paso
description: "Optimized step-by-step to make Abel's reels (publish first, trials = same reel with only the hook changed), with the audio verifier BEFORE rendering — one render per reel, no wasted time/resources"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 3d4589e7-425f-4ade-ad39-5d4a51f78758
  modified: 2026-10-08T17:42:03.080Z
---

Abel (08/10/2026, «muy importante»): tardé muchísimo con un trial (renderizar, revisar, rehacer escenas varias veces), y eso retrasa y gasta recursos. Además, un corte mal hecho «es muy incómodo y no da sensación de profesionalidad».

## Prioridad
1. **Primero los reels de PUBLICAR**: son los buenos y donde va el esfuerzo.
2. **Trial = iteración del reel de publicar:** se mantiene la estructura y se cambia el gancho (el primer tramo y el título), que tiene que ser distinto de verdad, potente y de dolor. El formato solo cambia si él lo pide. Misma exigencia de calidad: fluido, cortes limpios, coherente a nivel visual y con sentido.

## Paso a paso (cada reel; nada de render completo hasta el paso 5)
0. **Al transcribir un horizontal:** mapear sus ganchos (frases que atacan creencias, con buena energía) y sus trozos de colleja y de solución. Los ganchos sin desarrollo detrás van a `MarcaPersonal/banco_ganchos.md` para combinarlos con otro contenido de la misma idea.
1. **Guion antes que herramienta.** Elegir los trozos del horizontal con [[criterios-contenido-util]]:
   - gancho = dolor o verdad incómoda;
   - galletita aplicable;
   - su lente;
   - EN SU ORDEN, sin reordenar.
   Leerlo seguido como texto corrido y comprobar la ESTRUCTURA OBLIGATORIA de [[reels-marca-personal]]: gancho que ataca una creencia → colleja (connotación negativa) → solución con ejemplos y beneficio; sin CTA ni pregunta final; cada frase al servicio de la idea del gancho.
2. `reel_tablero.py reels.json --texto --solo X`: duración ≈ 40–50 s y **número de tramos de tablero** (hay que escribir un bloque para CADA uno; si falta alguno, el tablero sale vacío).
3. **Audio primero:** `--fotos 1 --solo X` (genera solo la voz) → `herramientas/verificar_audio.py out/_X <tiempos.json>`.
   - Corregir hasta que salga ✓: quitar o ampliar tramos, nunca cortar entre palabras pegadas.
   - Leer en voz alta las uniones ‖.
   - Mirar que no haya planos < 1 s (escenas de medio segundo).
3b. **Música según el estilo de su voz** (Abel 09/10/2026, «muy, muy en cuenta»: la música SIEMPRE amplifica el mensaje; calmado y desde el amor + música cañera = el mensaje se pierde).
   - Correr `herramientas/estilo_voz.py out/_X/voz.wav --base <wav de 5 min de la toma>`. Mide ritmo, entonación y fuerza contra su forma normal de hablar y da el estilo: CALMADO/AMOR → intensidad 1, FIRME → 2, INTENSO → 3.
   - La música se elige dentro de esa intensidad por el «caracter» y el mensaje (`MUSICA/catalogo.json`: «intensidad» puesta a mano y «caracter»).
   - Las canciones nuevas se añaden al catálogo con las dos cosas.
4. **Escenas:** un bloque por tablero, con fotos de la época correcta ([[fotos-vida-abel]]). En los clips de vídeo, solo «el estribillo» de la escena: nunca el final donde vuelve a salir él hablando ni restos de otra escena.
   - Comprobar con `--fotos t1,t2,…` (unos pocos fotogramas, uno por tablero) que ninguno está vacío y que nada sale repetido en pantalla.
5. **Un solo render.** Después, verificador otra vez (rápido) y una hoja de fotogramas. Si todo está bien, se entrega.
6. **Trial:** copiar la entrada de publicar en `reels_trial.json`, cambiar solo el gancho (y el título) → paso 3 (audio) → render.
7. `.txt` al lado (1.ª línea = título; hashtags #abelunidad #autoconocimiento #espiritualidad) → programar ([[reels-marca-personal]]).

## No hacer
- Renderizar para «ver qué tal» antes de verificar el audio.
- Rehacer un reel entero cuando falla una sola cosa: arreglar esa cosa.
- Transcribir de nuevo lo ya transcrito.
- Abrir debates o reestructurar trials.
