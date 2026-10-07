---
name: registro-edicion-abel
description: "Running log of lessons from each video I edit for Abel — his feedback, approved choices, and my own mistakes to avoid"
metadata:
  node_type: memory
  type: feedback
  originSessionId: d5e16cfe-1dfc-4d01-ac23-7f43e2a0e419
  modified: 2026-10-05T01:02:49.465Z
---

Leer antes de cada edición; ampliar después (ver [[aprender-de-cada-edicion]]).

## REGLA GENERAL · Silencios: dos criterios (Abel, 05/10/2026: «muy importante»)
Vale para todo: vídeos largos y reels. Se limpia con la transcripción: silencios, muletillas («¿de acuerdo?», «o sea»…), equivocaciones, arranques repetidos y repeticiones.
1. **Entre frases se cortan los silencios** para dar dinamismo: toda pausa > 0,3 s queda en ~0,2 s (nunca a cero).
2. **Dentro de una frase no hay cortecitos** que rompan la fluidez: nunca planos de < 1,5 s; si sale uno, se une al vecino conservando su pausa natural (≤ 0,6 s). Un silencio real (> 0,6 s) se recorta siempre, salvo que deje un conector suelto («pero… si no cambias», «así que… aplica ya»): esa pausa es de entonación y se respeta.
Valores en `herramientas/reel_yapping.py` (PAUSA, AIRE, MIN_PLANO) y `herramientas/limpiar_largo.py` (SILENCIO, ENTONACION). Antes de entregar, revisar que las uniones suenan de un tirón.

## REGLA GENERAL · Limpiar al terminar (Abel, 06/10/2026)
Con un vídeo hecho y verificado, se borra lo usado y solo quedan: su grabación original, los entregables finales, las configuraciones pequeñas (los .json y escenas.js) y, **hasta entregar sus reels**, lo que estos necesitan (toma_limpia.mov, trabajo/tiempos.json, edicion/montaje.json, index.html). Fuera: versiones anteriores, renders intermedios (`out/`), audios y pistas de trabajo, proxies, fotogramas de revisión, ficheros auxiliares y vídeos de referencia ya analizados. Al acabar los reels, también lo que solo servía para ellos.

## Lo que Abel ha aprobado
- 05/10/2026 · Reel 3 de «Sin buena intención…» («Si la intención es ganar dinero, sé honesto»): «está genial, aprende de eso». **ES EL MODELO DE REEL DE MARCA PERSONAL.** Por qué funcionó:
  - El gancho es una frase literal suya, en 2ª persona, que suena en el segundo 0.
  - Pocos tramos y largos (4 bloques), cada uno una idea completa, con un hilo claro: gancho → por qué (ego espiritual) → qué hacer (preguntas correctas) → cierre.
  - Habla de corrido en esos bloques: casi sin trocitos sueltos ni muletillas que quitar.
  - Termina en una frase completa con pausa natural detrás («…durante muchos años.»).

## Mis errores ya corregidos (no repetir)
### Reels de marca personal (feedback 05/10/2026)
- **Tramo o reel cortado a mitad de frase** (reel 2, s. 33–34: «ni a qué vengo» sin «aquí»; el reel 1 acababa en «…mucho más acertada»). La última palabra de cada tramo va seguida de una pausa ≥ 0,3 s en la toma; si no, alarga el tramo. El reel acaba en una frase completa y rotunda con 0,4 s de cola.
- **Dejar equivocaciones**: dos arranques seguidos («puedes hacer eso y puedes empezar…»), titubeos («quiero es es que»), autocorrecciones («de corazón… razón»), dobles muletillas («realmente, y digo realmente»). Antes de montar, buscar en la alineación: palabras repetidas cerca, palabras con puntuación < 0,6 y arranques que se reformulan, y quedarse solo con la versión limpia.
- **Trocitos sueltos de < 0,5 s** («minúsculas | que | ayuden») al quitar una palabra en medio de una frase fluida: suenan entrecortados. Mejor quitar o conservar la frase entera, o cortar en una pausa natural.
- Whisper duplica a veces una palabra en el cambio de segmento («hacer hacer»). Si una de las dos sale con puntuación ≈ 0,2 en la alineación, no se dijo dos veces: no la quites, o te comes la buena.

### Animaciones (vale para cualquier animación)
- Texto de animación encima de tallas o madera con mucho detalle: no se lee. Ponerle siempre sombra oscura amplia o un fondo (pastilla) y bajar el brillo de la sala.
- Palabra partida en dos (tajo): separar las mitades a lo largo del corte, nunca en vertical; si no, parecen dos palabras superpuestas.
- Anillos y ondas finos y semitransparentes: no se ven en móvil. Grosor ≥ 4–6 px y color vivo.
- Rótulos que se superponen en el cierre (sello y título que sube): revisar los últimos 2 s fotograma a fotograma.
- Antes de alargar la cola, mirar el final de la toma original: los vídeos de Abel pueden acabar con una cartela negra quemada (CTA). Hay que taparla con el fondo y rehacerla con el estilo del vídeo.

### Vídeos largos
- **`anim.py cortar` de la skill NO sirve para limpiar a Abel** (solo corta entre frases completas): se limpia con `herramientas/limpiar_largo.py` y la toma limpia pasa a la skill sin cortes. Flujo completo en [[estilo-videos-largos-stickman]].
- Sus grabaciones pueden ser **pantalla partida**. **ERROR mío:** la convertí en una ficha centrada en su cara. Se respeta su estructura.
- «Regula tu dopamina» v1 (05/10/2026): sus fallos ya están corregidos en las herramientas y como reglas en [[estilo-videos-largos-stickman]].
- Para que nada tiemble: toda forma recalculada pasa por `forma(e, fn)`. `[a, b].forEach(escribir)` es un error (forEach pasa el índice como t).

## Preferencias de Abel (ir ampliando)
- Quiere el vídeo terminado; las preguntas de estilo, en una sola tanda al principio.
- Agradece el feedback detallado por segundo («en el segundo 33–34»): usar la línea de tiempo del reel para localizarlo.
