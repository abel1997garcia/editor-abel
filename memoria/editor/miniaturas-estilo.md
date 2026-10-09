---
name: miniaturas-estilo
description: "Abel's new YouTube thumbnail system (09/10/2026, in progress): pure white background always, real photo of him + his whiteboard drawing as intrigue scene, Inter 900 lowercase with period; tools in herramientas/miniaturas"
metadata:
  node_type: memory
  type: project
  originSessionId: 59aef494-6bb3-4213-a83f-87743a599084
  modified: 2026-10-09T12:13:55.933Z
---

Abel quiere dejar las miniaturas de ChatGPT y que parezcan hechas por un editor gráfico (humanizar la marca). Decidido el 09/10/2026:
- **Fondo blanco puro `#FFFFFF` SIEMPRE**, también en temas oscuros (él: coherencia al entrar al canal). Busca romper el patrón: en el modo claro de YouTube la miniatura se funde con la página.
- **Escena completa que dé intriga**, no un dibujo pegado: «necesito darle clic porque si no, no lo entiendo». Idea llevada al extremo pero creíble, que se entienda en 1 s (sus referencias: el Rubius para la estructura, Pilar Sousa para la limpieza y el estilo propio, un canal de manifestación para la coherencia de marca).
- Sistema de prueba: él real recortado (rembg `birefnet-portrait`) a la derecha + su silueta o stickman de pizarra ([[estilo-videos-largos-stickman]]) + 1–2 palabras en Inter 900 minúscula con punto, la clave en un color de chakra.
- Herramientas: `Editor vídeos/herramientas/miniaturas/` (`base.js`, `base.css`, `render.py` → PNG 1280 y 1920, y `--mock` para simular YouTube claro/oscuro/móvil). Primera prueba: `Miniaturas/intencion-masculina/v1-v3`.
- Punto débil: los fotogramas de él hablando dan expresiones flojas. Se le recomendó un banco de fotos posadas (pared blanca, ropa oscura o de color, ~20 expresiones).
- **Veredicto de v1-v3 (09/10): «no me gusta nada».** Su cara parecía «un montaje muy mal hecho»: recortar no basta, hay que ADAPTARLO (buscar un momento con emoción de verdad, integrarlo en la escena con luz, color y nitidez). Las ideas eran «muy sosas», sin ninguna necesidad de clic. **Cómo hacerlo:** buscar primero en YouTube miniaturas de su tema, ordenar por las más populares y adaptar su mensaje a su estilo; componer con la regla de los tercios.
- **Método de la 2.ª ronda (09/10):** 1) leer el guion: el gancho real de «intención masculina» era la atracción por la retención, no «propósito»; 2) YouTube ordenado por visualizaciones con el tema real (retención y atracción: tensión hombre-mujer 1,4 M, tentación 25 M, antes/después 700 K, «ellas lo saben»); 3) `caras.py` puntúa cada segundo de sus grabaciones (sorpresa, intensidad, cómplice, preocupación, risa) y descarta movidos; 4) `integrar.py`: balance de blancos con su pared, contraste, claridad, enfoque, cuerpo que se funde en el blanco y `--borrar` para quitar manos movidas; nunca ampliar con IA; 5) tercios: ojos en la línea superior y tercio derecho, texto en el tercio inferior, dibujo a la izquierda. Resultado: `a1` («ellas lo notan.»), `b1` («por esto te miran.») y `c1` («lo que pierdes.»), pendientes de su veredicto.
- **Veredicto de a1-c1 (09/10): mejor, pero «tengo un gesto raro en todas».** Los fotogramas de él hablando NO sirven para la cara de la miniatura, aunque se puntúen: a media palabra siempre sale una mueca. Y el complemento del fondo no puede ser repetir las explicaciones del vídeo con dibujos planos: tiene que ENGANCHAR como los objetos del Rubius (caja Pokémon, aguja, sonrisa gigante) o las ilustraciones detalladas de Pilar Sousa (sistema nervioso dorado, libro misterioso). El blanco predomina, pero el elemento tiene que tener riqueza visual.
- Pendiente: convertirlo en skill (pasando por [[usar-system-change]]).
