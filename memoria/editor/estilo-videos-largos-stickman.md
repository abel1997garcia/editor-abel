---
name: estilo-videos-largos-stickman
description: "Abel's style for long YouTube videos (his main product) — original frame kept intact, intercut with white-board storytelling animations (Inter, chakra colors, stickman + his big silhouette), all inside the 4:3 zone"
metadata:
  node_type: memory
  type: project
  originSessionId: d5e16cfe-1dfc-4d01-ac23-7f43e2a0e419
  modified: 2026-10-05T18:25:19.404Z
---

Estilo de los vídeos largos de YouTube de Abel. **Es su producto principal**: ahí trata lo personal, rompe objeciones, se da a conocer y aporta mucho valor. Inspirado en «Como Automaticé por COMPLETO mi Edición de Video» (análisis en `Editor vídeos/Referencias/stickman/`), pero con fondo blanco.

## Estructura
- **Sus planos a cámara mantienen su estructura** (pantalla partida incluida, a su tamaño): nunca se reencuadran. Sí van un acercamiento muy leve y continuo (1,00 → 1,03) y **zooms de énfasis** hacia él en lo importante, **siempre fluidos** (`limpiar_largo.py`, recorte subpíxel).
- **Frases destacadas** de vez en cuando, debajo de él, **centradas**, en Inter 900 blanca con sombra suave, dentro del 4:3 (`herramientas/pizarra/postpro.py` + `citas.json`).
- Animaciones a pantalla completa intercaladas con sus planos, ≈ 60 % él. Sin ventanitas con su cara (PiP): no le gustan.
- **Zona segura 4:3 (muy importante):** los reels ([[reels-marca-personal]]) se recortan del horizontal; en 1920×1080 solo se ve x 240–1680. **Todo** lo de las animaciones (textos, dibujos, personajes) va dentro y se lee bien en vertical, contando el acercamiento de la cámara y 40 px de margen: en el reel F1 (centro 4:3) lo que roza el borde se corta. **Es lo que permite sacar los reels sin rehacer nada** (Abel, 08/10/2026: si no cuadra, hay que reprogramar y se gasta mucho más tiempo); regla completa en [[registro-edicion-abel]].
- **Primer minuto muy dinámico** (más de 13 cambios). Con toda la información en pantalla, aguantar 0,5–1 s antes de volver a su cara.
- **Sonido:** su voz tal cual, nunca se baja de volumen (tampoco en los reels); solo se baja la música. Efectos de sonido como en «dopamina v2» (cada texto, emoji y marca suena; ni más ni menos); sin música de fondo en el horizontal.
- **El final no se toca** (recortarlo deja rara la entonación): lo cierra él.

## Animaciones
- **Siempre tiene que estar pasando algo**: con él hablando, algo nuevo cada ≤ 2 s ligado a lo que dice (texto que entra con la voz, contadores, flechas que se dibujan durante la frase, objetos). Nada de ratos parados.
- **Lo que se escribe es lo que dice, casi literal**, cuando puntualiza o describe; solo los títulos de apartado («Fase 2», «Pilar 1»…) pueden resumir. Si no, lía.
- **Nada se pisa**: textos, flechas y emojis nunca se superponen; las flechas salen del borde de una caja y llegan al de otra (`unir`). Todo con sentido y en orden lógico.
- **Personajes:** para dar contexto e historias, un **stickman** sencillo de una pieza con posturas (sentado en el sofá con el móvil, manos a la cabeza, caminando, hundido, brazos arriba, escribiendo…). Para centros energéticos, emociones o el cuerpo por dentro, **la silueta grande de su boceto** (cabeza ovalada + un contorno continuo). Nunca un monigote articulado por piezas.
- **Storytelling:** el personaje protagoniza historias (la vida del avatar, sus historias personales, objeciones rotas en escena) para que el espectador piense «me entiende al 100 %». Recursos: bocadillos, objetos dibujados, contadores, símbolos en el cuerpo, flechas, ✓ y ✗, listas que se marcan, ecuaciones, comparaciones, tarjeta de cita.
- **Sus opiniones fuertes se destacan** (zoom o frase destacada) y **lo aplicable se ve paso a paso** ([[posicionamiento-abel]]).
- **Todo tiene que ver con la temática**; marcas (YouTube…): logo real o dibujo. **Emojis algunas veces** en el storytelling; no en los centros energéticos.

## Aspecto
- Fondo **blanco #FFFFFF**. **Inter 800–900**, letras apretadas, también en minúsculas (como su muestra «adiós.»); secundarios a 600.
- **Texto grande para el móvil**: títulos 110–130 px, principal 80–96, etiquetas 64–72, mínimo 56. Negro #111 que entra palabra a palabra con la voz.
- Destacados con los **colores de los centros**: raíz #C8372D, sacro #E06A1B, plexo #C99A00, corazón #1E7A46, garganta #1D7FD1, tercer ojo #3F3FB5, corona #7A3FC4.
- **Líneas perfiladas y fluidas** (6–8 px) que se dibujan solas; nada tiembla. El texto dentro de las formas cabe con ≥ 40 px de aire.

## Vídeos derivados
- De un vídeo largo (30–40 min) puede pedir N vídeos de **mínimo 8 min**. Cada uno con **un gancho distinto, ligado a lo que se habla después en ese vídeo**, un hilo con sentido y un final limpio. Puede bastar con recortar y reordenar.

## Gancho
- **La primera frase engancha desde el segundo 0** (largos, derivados y reels): es el 90 %. Si el arranque es flojo, se abre con su frase más potente en 2ª persona (avance en frío).
- **El gancho del horizontal SIEMPRE habla de un DOLOR**, nunca de una promesa (Abel, 08/10/2026). Mal: «después de este vídeo ningún vídeo de retención se va a comparar». Bien: «un hombre sin propósito está desconectado de su masculinidad». Si su arranque es una promesa, se busca dentro del vídeo su frase de dolor y va en avance en frío. En reels también es lo preferible, pero allí manda [[ganchos]].
- Al editar, marcar (zoom o frase destacada) los momentos en que cuenta su historia y los momentos de «galletita» aplicable, y poner foto o vídeo real de esa época ([[fotos-vida-abel]]). Si a un vídeo le falta su historia, decírselo para la próxima grabación: él quiere meterse más en su historia y contar cosas más profundas ([[criterios-contenido-util]]).

## Cómo se hace (receta probada; aprobada de nuevo con «La intención y energía masculina», 08/10/2026)
Carpeta `VideosLargos/<tema>/`; `S = ~/.claude/skills/animaciones-horizontal-combinadas/scripts/anim.py`.
1. **Transcribir la grabación:** `S nuevo <tema>/transcripcion --video <grabación>` → `S transcribir --toma --nombres "…"` → corregir `edicion/guion.txt` (nombres: Club Unidad…) → `S alinear --toma` → copiar `edicion/tiempos.json` a `<tema>/toma_tiempos.json`.
2. **Limpiar:** listar palabras con índice, huecos > 0,6 s y puntuación < 0,6; `limpieza.json` (gancho = su frase más rotunda en avance en frío, quitar, zooms en sus opiniones fuertes, intacto_desde = su cierre). Palabras con puntuación 0 y < 0,1 s pegadas a otra igual son duplicados de Whisper: no se quitan. `limpiar_largo.py limpieza.json --texto` y revisar planos < 1,5 s (ninguno en mitad de frase) → `limpiar_largo.py limpieza.json` (~10 min).
3. **Proyecto de animación sobre la toma limpia:** `S nuevo <tema>/anim --video toma_limpia.mov`; guion = texto limpio (una línea por plano) en `edicion/guion.txt` y `trabajo/guion.txt`; `S alinear --toma`; `S estilo --modo cara --sonido efectos --densidad media --subtitulos no`; `S cortar --pre .2 --min-pausa 5 --inicio 0 --cola 1.4 --fin <duración toma − .05>`; `S alinear`; `S planos`. **Comprobar que CONFIG.dur = duración de la toma** (la alineación comprime las últimas palabras y el final se corta).
4. **Ventanas:** `ventanas.json` (≈ 40 % animación, > 13 cambios en el 1.er minuto) → `pizarra/ventanas.py anim ventanas.json` → `pizarra/recortar_zooms.py anim toma_limpia.planos.json` (que no tapen sus zooms).
5. **Escenas:** `escenas.js` (modelo: `VideosLargos/intencion-masculina/escenas.js`, termina con el bloque «motor de la escena» de dopamina) → `pizarra/injertar.py anim escenas.js` → `node pizarra/revisar.mjs anim` hasta «todo bien» → hojas con `S revisar <t…> --hoja rN` y mirarlas (que nada se salga de su marco ni se pise).
6. **Montar:** `S montar` (≈ 9 min) → `citas.json` (≤ 22 caracteres por línea; sobre su cara) → `pizarra/postpro.py anim citas.json anim/out/anim_1080p30.mp4 "<tema> - horizontal.mp4"`.
7. **Comprobar el final** transcribiendo los últimos 5 s (si falta su despedida, añadirla de la toma limpia), limpiar intermedios, actualizar el TABLERO de la Fábrica.
Antes de editar, leer [[registro-edicion-abel]].
