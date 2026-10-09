---
name: proceso-reels-allan
description: "Cómo saco reels de un vídeo largo de Allan (selección de ganchos y mensajes que el usuario aprobó, flujo de herramientas, verificación)"
metadata:
  node_type: memory
  type: project
  originSessionId: 5031045c-b367-4cb9-8826-ca24be54d6d4
  modified: 2026-10-05T10:08:53.566Z
---

Flujo aprobado por el usuario (2026-10-05, «has encontrado bien los ganchos y el mensaje, enhorabuena»):
1. Transcribir (Whisper large-v3, GPU RTX 2060) y alinear palabra a palabra con la skill animaciones-horizontal-combinadas
   (instalada en .claude/skills/; su entorno ya está completo). Listado indexado con pausas para elegir.
2. Elegir 4–5 reels por vídeo de ~15 min, cada uno con UNA idea: un momento clave de la historia con conflicto emocional.
   Gancho = la frase más fuerte/intrigante del tramo, adelantada al principio (p. ej. «Una voz me dijo: este no es tu
   lugar», «Oigo voces… creo que me estoy volviendo loco», «Me rindo, hasta aquí ha llegado»), y luego la historia que
   lleva hasta ahí, terminando en una frase de cierre (decisión, revelación o lección).
3. Título = intriga / verdad incómoda / algo personal, ≤ 7 palabras, sin repetir literal el gancho
   (aprobados: «UNA VOZ ME DIJO QUE LO DEJARA TODO», «CREÍ QUE ME ESTABA VOLVIENDO LOCO», «TODO CAMBIÓ EL DÍA QUE ME
   RENDÍ», «PEDÍ UNA SEÑAL A DIOS Y ESE MISMO DÍA LLEGÓ», «LO CONSEGUÍ TODO Y SEGUÍA VACÍO»).
4. Guion de cortes = lista [palabra_ini, palabra_fin, "subtítulo"] en orden del reel (reels/specs/*.py → json);
   herramientas/reel_franjas.py monta; medir_sync.py + comprobar_reel.py + oir.py verifican.
4b. Leer cada guion de corrido como lo oirá alguien sin contexto (congruencia, sin redundancias, conectores) y
   pasar el protocolo de [[cortes-palabras-obligatorio]] (método aprobado el 2026-10-07).
5. Escribir la descripción de Instagram de cada reel (reels/<nombre>.txt, ver [[descripcion-instagram-reels]]).
6. Entregar con tabla (reel, título, gancho, duración), las descripciones y decisiones tomadas.

**Why:** este proceso dio el resultado que el usuario dio por bueno; el estilo visual es [[estilo-reel-franjas-azules]].
**How to apply:** reutilizarlo en cada vídeo nuevo de Allan; los errores a evitar están en [[fallos-edicion-reels-allan]].
Pueden llegar otros estilos de reel: cada uno con su propio documento en el proyecto.
