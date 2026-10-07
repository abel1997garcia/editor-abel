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
- **Zona segura 4:3 (muy importante):** los reels ([[reels-marca-personal]]) se recortan del horizontal; en 1920×1080 solo se ve x 240–1680. **Todo** lo de las animaciones (textos, dibujos, personajes) va dentro y se lee bien en vertical, contando el acercamiento de la cámara y 40 px de margen: en el reel F1 (centro 4:3) lo que roza el borde se corta.
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

## Cómo se hace
`limpiar_largo.py` → proyecto de la skill animaciones-horizontal-combinadas en modo «cara» sobre la toma limpia (`cortar` sin cortes) → `herramientas/pizarra/ventanas.py` (ventanas ancladas a frases; mide % y cambios) → escenas con `herramientas/pizarra/libreria.js` + `injertar.py` → **`revisar.mjs` hasta «todo bien»** → `anim.py montar` → `postpro.py`. Ejemplo completo y **aprobado** («es el resultado que yo quería», 05/10/2026): `VideosLargos/dopamina/` → «regula tu dopamina - horizontal v2.mp4». Antes de editar, leer [[registro-edicion-abel]].
