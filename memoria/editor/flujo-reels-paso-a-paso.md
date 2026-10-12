---
name: flujo-reels-paso-a-paso
description: "Optimized step-by-step to make Abel's reels (publish first, trials = same reel with only the hook changed), with the audio verifier BEFORE rendering — one render per reel, no wasted time/resources"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 3d4589e7-425f-4ade-ad39-5d4a51f78758
  modified: 2026-10-11T19:17:46.821Z
---

**DESDE 12/10/2026 el proceso y el LISTÓN de calidad de los reels F1 están en la skill del proyecto `reels-abel` (`.claude/skills/reels-abel/SKILL.md`): usarla SIEMPRE.** Abel: «no se trata de subir por subir». Lo de abajo es el historial y vale para F2–F5.


Abel (08/10/2026, «muy importante»): tardé muchísimo con un trial (renderizar, revisar, rehacer escenas varias veces), y eso retrasa y gasta recursos. Además, un corte mal hecho «es muy incómodo y no da sensación de profesionalidad».

## Prioridad
1. **Primero los reels de PUBLICAR**: son los buenos y donde va el esfuerzo.
2. **Trial:** **Cada reel tiene algo ÚNICO (Abel 12/10/2026: «aunque cambiemos el gancho, la mayoría del vídeo es el mismo; el mismo día se nota»).** Lo preferible es que el trial lleve OTRA estructura y OTRO gancho del mismo vídeo; para eso el banco tiene que ser grande (20 o más ganchos y todas las estructuras posibles). Si un reel comparte estructura o gancho con otro, vale, pero `programar_youtube.py` los separa al menos 45 días (código `e<N>-g<N>` en el nombre). Calendario: trial 3 al día como máximo (17, 19 y 21 h); publicar 6 al día (14, 16, 18, 20, 22 y 24 h).

## Paso a paso (cada reel; nada de render completo hasta el paso 5)
0. **Al transcribir un horizontal: banco de GANCHOS y banco de ESTRUCTURAS** (método 7b de [[reels-marca-personal]]). Los reels se montan combinando un gancho con una estructura de la misma idea.
0b. (Antes) mapear sus ganchos (frases que atacan creencias, con buena energía) y sus trozos de colleja y de solución. Los ganchos sin desarrollo detrás van a `MarcaPersonal/banco_ganchos.md` para combinarlos con otro contenido de la misma idea.
1. **Guion antes que herramienta.** Elegir los trozos del horizontal con [[criterios-contenido-util]]:
   - gancho = dolor o verdad incómoda, y además **utilizable como gancho por cómo lo dice** (Abel 12/10/2026: «por la entonación la frase no puede utilizarse como gancho»):
     - frase COMPLETA: empieza tras una pausa y acaba con entonación de cierre, nunca a media lista ni con «y…»;
     - se entiende sola, sin «eso», «esto» o «con eso» que remitan a algo anterior;
     - si dudo, escucho el gancho suelto (`--voz --solo X`) antes de montar; si no suena a arranque, se descarta aunque el texto sea bueno;
   - galletita aplicable;
   - su lente;
   - EN SU ORDEN, sin reordenar.
   Leerlo seguido como texto corrido y comprobar la ESTRUCTURA OBLIGATORIA de [[reels-marca-personal]]: gancho que ataca una creencia → colleja (connotación negativa) → solución con ejemplos y beneficio; sin CTA ni pregunta final; cada frase al servicio de la idea del gancho.
2. `reel_tablero.py reels.json --texto --solo X`: duración ≈ 40–50 s y **número de tramos de tablero** (hay que escribir un bloque para CADA uno; si falta alguno, el tablero sale vacío).
3. **Audio primero:** `--fotos 1 --solo X` (genera solo la voz) → `herramientas/verificar_audio.py out/_X <tiempos.json>`.
   - Corregir hasta que salga ✓: quitar o ampliar tramos, nunca cortar entre palabras pegadas. **Un ✗ no se da por bueno «porque el texto se lee bien»** (12/10/2026: lo hice en «empezar desde 0» y salieron malos cortes): o se arregla, o se cambia el tramo, o se le dice a Abel.
   - Leer en voz alta las uniones ‖.
   - Mirar que no haya planos < 1 s (escenas de medio segundo).
   - **F1 (desde el horizontal):** `reel_yapping.py reels_f1.json --voz [--solo a,b]` deja `out/_X/voz.wav` + `planos.json` para el verificador, sin render. Los índices del banco (toma_tiempos) se pasan a `anim/trabajo/tiempos.json` con difflib.
   - El horizontal ya va sin silencios: cada tramo tiene que empezar en una palabra con ≥ 0,25 s de hueco antes, si no sale «PEGADO/CORTE SOBRE LA VOZ». Se arregla empezando una palabra antes («y muchas veces», «pero tú imagínate»).
3b. **Música según el estilo de su voz** (Abel 09/10/2026, «muy, muy en cuenta»: la música SIEMPRE amplifica el mensaje; calmado y desde el amor + música cañera = el mensaje se pierde).
   - Correr `herramientas/estilo_voz.py out/_X/voz.wav --base <wav de 5 min de la toma>`. Mide ritmo, entonación y fuerza contra su forma normal de hablar y da el estilo: CALMADO/AMOR → intensidad 1, FIRME → 2, INTENSO → 3.
   - La música se elige dentro de esa intensidad por el «caracter» y el mensaje (`MUSICA/catalogo.json`: «intensidad» puesta a mano y «caracter»).
   - Las canciones nuevas se añaden al catálogo con las dos cosas.
4. **Escenas:** un bloque por tablero, con fotos de la época correcta ([[fotos-vida-abel]]). En los clips de vídeo, solo «el estribillo» de la escena: nunca el final donde vuelve a salir él hablando ni restos de otra escena.
   - Comprobar con `--fotos t1,t2,…` (unos pocos fotogramas, uno por tablero) que ninguno está vacío y que nada sale repetido en pantalla.
4b. **F1: cada imagen tiene que dar contexto** (12/10/2026: «la imagen que aparece no hace que se entienda el contexto»). Una animación del horizontal solo sale en el reel si sale ENTERA y con la frase que la explica dentro del reel. Si el tramo pilla media animación, o una cuyo contexto se ha quedado fuera, ese trozo va con su cara (`"toma"` + `"ventanas"`). En la hoja de fotogramas no puede haber tableros a medio dibujar ni palabras sueltas.
5. **Un solo render.** Después, verificador otra vez (rápido) y una hoja de fotogramas. Si todo está bien, se entrega.
6. **Trial:** copiar la entrada de publicar en `reels_trial.json`, cambiar solo el gancho (y el título) → paso 3 (audio) → render.
7. `.txt` al lado (1.ª línea = título; hashtags #abelunidad #autoconocimiento #espiritualidad) → programar ([[reels-marca-personal]]).

## No hacer
- Renderizar para «ver qué tal» antes de verificar el audio.
- Rehacer un reel entero cuando falla una sola cosa: arreglar esa cosa.
- Transcribir de nuevo lo ya transcrito.
- Abrir debates o reestructurar trials.
