---
name: usar-system-change
description: "Cambios permanentes a sistemas repetidos (flujos, skills, documentos, automatizaciones, reglas) pasan antes por la skill system-change"
metadata:
  node_type: memory
  type: feedback
  originSessionId: f9e416f0-1005-4d32-a14e-d7a6a3fb31d5
  modified: 2026-10-05T00:21:45.497Z
---

Cuando Abel pida cambiar, rediseñar o mejorar de forma permanente un sistema que se repite (un flujo de trabajo, una skill, un documento, una automatización o una regla), usar primero la skill `system-change` y aplicar el cambio después.

**Why:** Abel lo pidió el 2026-10-05 al instalar la skill. Quiere que esté instalada solo en este proyecto ("Editor vídeos"), no global.

**How to apply:** La skill está en `.claude/skills/system-change/SKILL.md` dentro de este proyecto. No usarla para ediciones puntuales de un vídeo ni para excepciones de una sola vez. Relacionado: [[aprender-de-cada-edicion]], [[registro-edicion-abel]].
