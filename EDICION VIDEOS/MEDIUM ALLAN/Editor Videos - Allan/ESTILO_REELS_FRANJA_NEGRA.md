# Estilo de reel vertical «franja negra» — canalizaciones de Allan (médium)

**Cuándo se usa:** sesiones/entrevistas de canalización: Allan arriba, la otra persona abajo, y una **franja negra
horizontal en el medio** (la da el usuario). Nada que ver con el estilo «franjas azules».
Referencia: `trabajo/referencia_franja_negra.png`.

## Contenido (lo que importa)
- Siempre es una **canalización**: Allan dice mensajes o lo que percibe, y la persona de abajo **confirma**
  (dice que sí, que es verdad, o da más datos que lo corroboran).
- **Gancho = lo más importante**: Allan dice algo que percibe y la otra persona lo confirma. Primeros segundos.
- Todo el reel enfocado en «mensaje de Allan → verificación de la persona», porque da autoridad a Allan como médium
  y genera confianza.
- **Fuera:** presentaciones («¿cómo te llamas?», etc.), preámbulos, logística de la sesión.
- Igual que siempre: sin silencios inútiles, sin muletillas, sin equivocaciones; **fluido** (sin microcortes ni ráfagas
  de cortes) y **audio y vídeo sincronizados** (verificar con `herramientas/medir_sync.py`).
- Duración: **~1 minuto** (el usuario, tras la 1.ª entrega).
- **Nada de silencio al final** (ni dentro): la alineación puede estirar la última palabra de la persona sobre el
  silencio; `reel_franjas.py` lo detecta («palabra sospechosa») y recorta por energía esos trozos. Revisar el final.
- Con su descripción de Instagram en `reels/<nombre>.txt` (como todos los reels).
- Primera entrega: **2 reels** de un vídeo largo; cuando el usuario vea que va bien, se pule y se hacen más.

## Subtítulos (los de OpusClip)
- **Sin título.** Solo subtítulos.
- Montserrat **Bold**, **MAYÚSCULAS**, blanco, **60 px reales** (medido en los reels del usuario) a 1080 de ancho (= 39 en OpusClip × 1,5; confirmado por el
  usuario: «como en la captura»). OJO: en franjas azules el usuario dio px reales (44/60); aquí dio la medida de
  OpusClip. Ante la duda, medir la captura y preguntar.
- Normalmente **2 palabras, máximo 3** por subtítulo.
- **Siempre centrado** (horizontal y vertical) **dentro de la franja negra**: en el bruto la franja ocupa
  y = 858–1060; el centro de las mayúsculas va en y = 959 (en los reels del usuario, 958).
- Grupos de 1–3 palabras repartidos por frase (programación dinámica): mejor 2, nunca acabar en palabra débil,
  corte en la puntuación. **En los silencios no hay subtítulo** (como OpusClip).
- Si el audio dice algo más veces de lo que Whisper escribió («calma» ×4), se escribe lo que se oye y se reparte.

## Cómo se hace
- Igual que franjas azules (transcribir + alinear en `trabajo/<video>/`), con spec `"estilo": "franja_negra"`, `"video"` y
  `"tiempos"` (ver `reels/specs/crear_specs_shorts_prueba.py`). `reel_franjas.py` monta; `medir_sync.py` mide la cara de
  Allan (zona de arriba); `comprobar_reel.py` y `oir.py` verifican.
- Estructura que funciona (igual que los reels del usuario «Abuela muerta» y «Mensajes del más allá»): arranque en
  seco con un dato concreto de Allan + confirmación inmediata; luego 3–4 bloques «Allan percibe → la persona confirma
  con datos»; cierre con la confirmación más emotiva. El diálogo se recorta a pausas de ~0,3 s.
- La voz de la persona (videollamada) se alinea con puntuación baja aunque los tiempos son buenos: verificar oyendo.
- Elegir la verificación más concreta como gancho (números, nombres, palabras que usaba: «Me dice cinco» →
  «Éramos cinco»; «Me pide calma» → «Era una palabra que usaba mucho»).

## Vídeo en bruto
- Viene **ya en vertical, con las dos personas apiladas y la franja negra puesta**. Solo hay que seleccionar el
  mensaje (cortes) y colocar los subtítulos en la franja. Medir la franja en el vídeo real (no fiarse de la captura).
