# Editor de vídeos — Allan (médium)

Proyecto de edición de los vídeos de Allan (médium) para reels y vídeos.

- **DOS FORMATOS de reels de Allan** (Abel 18/10/2026): **1) mensajes/reflexiones** de vídeos normales (franjas azules)
  y **2) sesiones/canalizaciones** (Allan percibe → la persona confirma; gancho = dato concreto + confirmación). El 2
  se presenta en **vertical con franja negra** (ya preeditado por Abel) o en **horizontal sin franja** (p. ej. eventos:
  cortar entre Allan y la persona, subtítulos Montserrat; estilo visual PENDIENTE de que Abel lo defina). Mismo
  contenido y edición en ambos.
- **Reel vertical con franjas azules arriba y abajo en el original** → estilo «franjas azules»:
  lee y sigue `ESTILO_REELS_FRANJAS_AZULES.md` (título Montserrat ExtraBold 60 px MAYÚSCULAS arriba, subtítulos
  Montserrat Bold 44 px abajo, negro sin fondo, gancho primero, 50–90 s, sin silencios ni muletillas pero fluido, sin microcortes).
  **Lo primordial: audio y vídeo sincronizados** (verificar con `herramientas/medir_sync.py`).
- **Todos los reels** (cualquier estilo) se entregan con su descripción de Instagram en `reels/<nombre>.txt`:
  frase gancho CORTA (5-9 palabras), cruda, que toque la fibra y resuma el vídeo (mejor si es negativa), entre comillas + 👇, párrafo que conecta con lo que siente (🤍), «Y quizá te digas que…»,
  pregunta de tú a tú y SIEMPRE el cierre `👉 Si quieres información sobre las sesiones, comenta "INFO".`
- **Reel de canalización: Allan arriba, persona abajo, franja negra en medio** → estilo «franja negra»:
  lee y sigue `ESTILO_REELS_FRANJA_NEGRA.md` (sin título; subtítulos Montserrat Bold MAYÚSCULAS 2–3 palabras centrados
  en la franja; gancho = Allan percibe algo y la persona lo confirma; fuera presentaciones).
- Formato horizontal: aún no definido.
- **CHECKLIST obligatoria de cada reel, en orden:** `CHECKLIST_REELS_ALLAN.md` (mensaje para el avatar → voz → vídeo → entrega).
- **AUDIO PRIMERO (Abel 17/10/2026, obligatorio):** tras el guion, `reel_franjas.py <spec> --voz` monta SOLO la voz
  (`trabajo/reels/<n>/voz.wav`, segundos). Se revisa con `herramientas/espectro_cortes.py <n>` (espectrograma de cada
  empalme y de la voz entera), `oir_empalmes.py --voz <n>` (todos los empalmes) y `onda.py` sobre `voz.wav`; se corrige
  midiendo en el ORIGINAL (ini_fijo/fin_max) y SOLO con la voz limpia (sin «eh», sin palabras cortadas) se renderiza el vídeo.
- **ANTES DE ENTREGAR CUALQUIER REEL (obligatorio, sin excepción):** `herramientas/comprobar_cortes.py <reels>`,
  `herramientas/oir_empalmes.py <reel> 1..N` (escuchar TODOS los empalmes), `revisar_por_tramos.py`, `medir_sync.py` (imagen) y `medir_sync_audio.py` (audio).
  Ninguna palabra cortada («exist», «cort»), ninguna muletilla asomando, empalmes suaves.
  **Y ver la PISTA DE AUDIO como un editor** (Abel 13/10/2026: «para perfilar más perfecto»):
  `python herramientas/onda.py --hueco 0.55 --final 0.4 reels/<reel>.mp4` → `trabajo/reels/<reel>/<reel>.onda.png` con la forma de onda; marca en rojo
  los huecos de más de 0,55 s (el `MAX_PAUSA` de Allan; su ritmo es pausado, NO el de Abel) y se mira la imagen antes de entregar. Para muletillas pegadas:
  `buscar_inicio.py` / `buscar_fin.py` y ajustes `ini_fijo` / `fin_max` en `trabajo/<video>/ajustes_tiempos.json`.
- Herramientas: `herramientas/reel_franjas.py` (montaje), `herramientas/comprobar_reel.py` (verificación),
  `herramientas/oir.py` (escuchar tramos con Whisper). Transcripción y alineación: skill
  `animaciones-horizontal-combinadas` en `.claude/skills/`.
- **`reels/` es la carpeta DEFINITIVA para subir: SOLO `<reel>.mp4` y `<reel>.txt`** (Abel 18/10/2026). Nada de ondas, voces, espectrogramas ni copias; todo eso en `trabajo/reels/<reel>/`. Guiones de corte en `trabajo/specs/`.
- **Carruseles de Instagram (historia de Allan y microhistorias, ref. @jun_yuh):** lee ENTERA `RUTINA_CARRUSELES_ALLAN.md`
  (mismo sistema que los carruseles de Abel, enfocado a las sesiones y la formación de mediumnidad). Herramienta
  `herramientas/carruseles/carrusel.py`; salidas en `MEDIUM ALLAN/CARRUSELES/NN · tema (vN)/`.
