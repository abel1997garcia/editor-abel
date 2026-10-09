---
name: estilo-reel-franjas-azules
description: Estilo de reel vertical de reflexiones de Allan médium cuando el original trae franjas azules arriba/abajo (título 60px + subtítulos 44px Montserrat negros)
metadata:
  node_type: memory
  type: project
  originSessionId: 5031045c-b367-4cb9-8826-ca24be54d6d4
  modified: 2026-10-05T09:39:11.053Z
---

Si el vídeo vertical original de Allan (médium) trae franjas azules de cielo arriba y abajo, el estilo es siempre este
(definido por el usuario el 2026-10-05; detalle completo en ESTILO_REELS_FRANJAS_AZULES.md del proyecto):
- LO PRIMORDIAL: audio y vídeo sincronizados (el usuario: «es lo primordial, por Dios»).
- Reels de reflexiones de 50 s a 1:30; el gancho es el 90 % del valor (frase más fuerte al principio).
- Sin silencios, muletillas, equivocaciones ni repeticiones tontas, PERO fluido: nada de microcortes palabra a palabra
  (suena robótico). Solo se recortan pausas > 0,7 s y muletillas/titubeos.
- Título todo el reel en la franja de arriba: Montserrat ExtraBold **60 px** (a 1080 de ancho), MAYÚSCULAS, centrado,
  negro sin fondo; genera intriga, verdad incómoda o algo personal.
- Subtítulos una línea en la franja de abajo: Montserrat Bold **44 px**, minúsculas salvo inicio de frase, negro sin fondo.
- Primero vertical; el horizontal y otros estilos de reel vertical vendrán después (no inventarlos).

- Si el usuario pide franjas azules para un vídeo HORIZONTAL sin franjas (p. ej. «¿Qué ocurre con los seres queridos
  desaparecidos?», 1280x720, Allan caminando por el campo): se compone el vertical con plantillas/fondo_franjas_azules.png
  (cielo reconstruido de los reels anteriores) y el vídeo escalado a 1080x768 en y=588 (spec "componer", x=90 para
  centrar su cara). Entregados 4 reels así el 2026-10-06 (desap_01..04). Feedback: frase larguísima en desap_04 (ya corregido).
  2026-10-07: 4 reels de «Cómo conectar con tus guías espirituales» (guias_01..04, horizontal, x=100), subtítulos <= 6
  palabras partidos a mano, evitando el banner de «Reserva tu cita».

**Why:** el usuario lo replica de su plantilla de OpusClip y quiere el mismo resultado siempre. Los tamaños los corrigió
él (la 1.ª versión tenía título 50 px y subtítulos 66 px: subtítulos demasiado grandes).
**How to apply:** usar herramientas/reel_franjas.py, medir_sync.py y comprobar_reel.py; ver [[fallos-edicion-reels-allan]].
