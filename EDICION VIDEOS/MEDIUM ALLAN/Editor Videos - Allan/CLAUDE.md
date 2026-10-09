# Editor de vídeos — Allan (médium)

Proyecto de edición de los vídeos de Allan (médium) para reels y vídeos.

- **Reel vertical con franjas azules arriba y abajo en el original** → estilo «franjas azules»:
  lee y sigue `ESTILO_REELS_FRANJAS_AZULES.md` (título Montserrat ExtraBold 60 px MAYÚSCULAS arriba, subtítulos
  Montserrat Bold 44 px abajo, negro sin fondo, gancho primero, 50–90 s, sin silencios ni muletillas pero fluido, sin microcortes).
  **Lo primordial: audio y vídeo sincronizados** (verificar con `herramientas/medir_sync.py`).
- **Todos los reels** (cualquier estilo) se entregan con su descripción de Instagram en `reels/<nombre>.txt`:
  frase gancho cruda/polémica entre comillas + 👇, párrafo que conecta con lo que siente (🤍), «Y quizá te digas que…»,
  pregunta de tú a tú y SIEMPRE el cierre `👉 Si quieres información sobre las sesiones, comenta "INFO".`
- **Reel de canalización: Allan arriba, persona abajo, franja negra en medio** → estilo «franja negra»:
  lee y sigue `ESTILO_REELS_FRANJA_NEGRA.md` (sin título; subtítulos Montserrat Bold MAYÚSCULAS 2–3 palabras centrados
  en la franja; gancho = Allan percibe algo y la persona lo confirma; fuera presentaciones).
- Formato horizontal: aún no definido.
- **ANTES DE ENTREGAR CUALQUIER REEL (obligatorio, sin excepción):** `herramientas/comprobar_cortes.py <reels>`,
  `herramientas/oir_empalmes.py <reel> 1..N` (escuchar TODOS los empalmes), `revisar_por_tramos.py`, `medir_sync.py`.
  Ninguna palabra cortada («exist», «cort»), ninguna muletilla asomando, empalmes suaves. Para muletillas pegadas:
  `buscar_inicio.py` / `buscar_fin.py` y ajustes `ini_fijo` / `fin_max` en `trabajo/<video>/ajustes_tiempos.json`.
- Herramientas: `herramientas/reel_franjas.py` (montaje), `herramientas/comprobar_reel.py` (verificación),
  `herramientas/oir.py` (escuchar tramos con Whisper). Transcripción y alineación: skill
  `animaciones-horizontal-combinadas` en `.claude/skills/`.
- Salidas en `reels/`; guiones de corte en `reels/specs/`; intermedios en `trabajo/`.
