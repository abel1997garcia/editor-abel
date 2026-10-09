# Estilo de reel vertical «franjas azules» — Allan (médium)

**Cuándo se usa:** siempre que el vídeo original vertical (1080×1920) traiga **franjas azules de cielo arriba y abajo**
con Allan hablando en el centro. Es el estilo de los reels de reflexiones. (Otros estilos de reel vertical y el
formato horizontal irán en documentos aparte cuando se definan.)

## Objetivo
- Reels de **reflexiones** de **50 s a 1:30** (los de «historia» salieron de 57–66 s).
- **El gancho es el 90 % del vídeo**: los primeros 2–4 s tienen que ser la frase más fuerte (se puede sacar de más
  adelante y ponerla al principio). Después, la historia que lleva hasta ahí.
- Sin silencios, sin muletillas («pues», «o sea», «bueno», «eh», «no sé»), sin equivocaciones ni repeticiones tontas.
  Las repeticiones con intención («ese lugar no, ese lugar no, ese lugar no», «esperaba y esperaba…») se quedan.
- **LO PRIMERO: audio y vídeo tienen que coincidir.** Cada trozo se corta del original con su imagen y su audio
  juntos y se pegan en el orden del reel (`reel_franjas.py`); comprobar con `herramientas/medir_sync.py`.
- **Fluido, nunca robótico**: nada de microcortes palabra a palabra («y | que | yo»). Solo se recortan pausas
  reales de más de 0,7 s (quedan ~0,32 s de respiración) y las muletillas/repeticiones/titubeos. Si un corte solo
  quita una palabra pequeña de una frase («que», «porque», «y»), se deja la palabra.
- Cortar donde toca **sin comerse palabras**: `reel_franjas.py` coloca cada corte en el silencio REAL del audio
  (no en la alineación), con una respiración corta que nunca toca la voz vecina. Pausas > 0,55 s se recortan.
  Donde no hay silencio entre palabras (habla continua), no se corta: se empieza/acaba la frase donde sí lo hay.
- **Congruencia:** cada reel se lee de corrido como lo oirá alguien sin contexto: sin redundancias («realmente…
  realmente»), con los conectores que dan sentido («Es muy normal…», «Entonces…», «Porque yo creo que…»).
- Verificar también con `herramientas/revisar_por_tramos.py` (escucha por tramos de 6 s) y medir silencios > 0,5 s.

## Si el original NO trae las franjas (vídeo horizontal)
- Se compone: `plantillas/fondo_franjas_azules.png` (cielo limpio reconstruido de los reels anteriores, fijo) +
  el vídeo escalado a 1080x768 en el hueco y = 588–1356, recortando los laterales. En el spec:
  `"componer": {"fondo": "plantillas/fondo_franjas_azules.png", "y": 588, "alto": 768, "x": 90}` (x = recorte
  horizontal sobre 1365 px; 90 deja la cara de Allan centrada en sus vídeos caminando). Ver
  `reels/specs/crear_specs_desaparecidos.py`.

## Título (franja de arriba, todo el reel)
- Montserrat **ExtraBold 60 px** (a 1080 de ancho), **MAYÚSCULAS siempre**, centrado,
  **negro sin fondo**, interlínea 67 px, línea base de la última línea en y = 553 (la franja acaba en y ≈ 590).
- 2 líneas equilibradas (máx. 900 px de ancho), sin dejar palabras débiles colgando («ME», «QUE», «DE»…).
- Función: generar **intriga**, decir una **verdad incómoda** relacionada con el vídeo o algo **personal**.
  Corto (≤ 6–7 palabras). Ejemplos: «UNA VOZ ME DIJO QUE LO DEJARA TODO», «CREÍ QUE ME ESTABA VOLVIENDO LOCO»,
  «TODO CAMBIÓ EL DÍA QUE ME RENDÍ», «PEDÍ UNA SEÑAL A DIOS Y ESE MISMO DÍA LLEGÓ», «LO CONSEGUÍ TODO Y SEGUÍA VACÍO».

## Subtítulos (franja de abajo)
- **Una línea cada vez**, Montserrat **Bold 44 px**, centrado, **negro sin fondo**,
  línea base en y = 1445 (la franja empieza en y ≈ 1356).
- **Minúsculas; solo mayúscula la primera letra de cada frase** (y nombres propios: Raúl, Dios…).
- Sin comas ni puntos (se quitan al pintar); se mantienen ¿? y ¡!.
- **Cortos y legibles: máximo 6 palabras y ~760 px por subtítulo.** La letra NUNCA se encoge (error ya cometido:
  una frase de 19 palabras a 38 px en desap_04). `reel_franjas.py` parte solo y se niega a renderizar si algo no cabe.
- Si no cabe en 960 px a 44 px, se parte en dos subtítulos por palabras (nunca se encoge la letra), sin dejar
  al final una palabra débil (a, de, que, y, en, me…).
- El texto es **lo que dice** (fiel al audio), con las palabras bien escritas: «firmase» (no «filmase»),
  «mediumnidad», «médium».

Tamaños fijados por el usuario en px (5-10-2026): título 60 px, subtítulos 44 px. (La primera versión, calibrada
con un factor ×1,5 sobre OpusClip, dio subtítulos de 66 px: demasiado grandes.)

## Cómo se hace (herramientas del proyecto)
1. Entorno: la skill `animaciones-horizontal-combinadas` (en `.claude/skills/`) aporta Whisper + alineación forzada:
   `python .claude/skills/animaciones-horizontal-combinadas/scripts/anim.py entorno` (todo instalado; GPU RTX 2060).
   Fuentes en `fuentes/` (Montserrat ExtraBold y Bold, OFL).
2. Transcribir y alinear el vídeo entero:
   ```
   ffmpeg -i "<video>.mp4" -vn -ac 1 -ar 16000 trabajo/audio16k.wav
   python .claude/skills/animaciones-horizontal-combinadas/scripts/transcribir.py trabajo/audio16k.wav --salida trabajo
   python .claude/skills/animaciones-horizontal-combinadas/scripts/alinear.py trabajo/audio16k.wav trabajo/guion.txt --salida trabajo/tiempos.json
   ```
3. Elegir los reels y escribir el guion de cortes de cada uno: lista de `[palabra_ini, palabra_fin, "texto del subtítulo"]`
   en el orden del reel (ver `reels/specs/crear_specs_historia.py`). Lo que no está en ninguna línea se corta.
4. Montar: `python herramientas/reel_franjas.py reels/specs/<reel>.json` (`--solo-hoja` para ver duración y guion
   sin renderizar). Sale `reels/<reel>.mp4` (1080×1920, 30 fps, H.264 CRF 18, audio −14 LUFS).
5. **Comprobar siempre**: `python herramientas/comprobar_reel.py reels/<reel>.mp4` vuelve a transcribir y lista
   palabras que faltan o sobran. Lo dudoso se escucha con `python herramientas/oir.py <mp4> ini:fin ...`.
6. Muletillas que la alineación pegó a una palabra: se corrigen en `trabajo/ajustes_tiempos.json`
   (`"s"`, `"e"` y `"hueco_antes": [ini, fin]` para extirpar la muletilla justo antes de una palabra).

## Errores ya cometidos (no repetir)
- **Audio y vídeo descuadrados (el peor error)**: se eligieron los fotogramas con `select=` sobre el original, que los
  deja en el orden del original; al adelantar el gancho, imagen y voz iban por separado (desfases de 3–86 s).
  Ahora cada trozo sale con su audio y su imagen del mismo corte. Medir siempre con `medir_sync.py` (0 fotogramas).
- **Microcortes**: recortar todas las pausas de más de 0,3 s dejaba un habla robótica. Umbral 0,7 s.
- **Ráfagas de cortes** (pendiente de pulir): varios cortes muy seguidos (3 en < 3 s) suenan a «corte, corte, corte»
  aunque cada uno esté justificado. `reel_franjas.py` avisa con «AVISO ráfaga de cortes»: en esos tramos, conservar
  alguna pausa o elegir otro tramo. Repartir los cortes.

- **Silencio colado por palabra estirada** (visto en franja negra, vale para todos): una palabra alineada > 1 s suele
  arrastrar silencio. `reel_franjas.py` avisa y recorta por energía solo esos trozos (recortar todos se come palabras flojas).

- **Desfase de 1–3 fotogramas acumulado** (desaparecidos): el corte redondeado por encima del fotograma hacía que
  ffmpeg descartase el primero. Ya corregido en `reel_franjas.py` (corte 1 ms antes + nº exacto de fotogramas +
  aviso automático «¡¡AVISO SINCRONÍA!!»). Aun así, `medir_sync.py` SIEMPRE antes de entregar.
- **Palabra fantasma** («su abuelo, abuelo» con una sola en el audio): no cortar entre las dos.

## Lo que funcionó (aprobado por el usuario)
- Ganchos y mensajes: 5 reels de un vídeo de 15 min, uno por momento clave con conflicto emocional; gancho = la frase
  más fuerte adelantada; cierre con decisión, revelación o lección. Títulos de la tabla de arriba.
- Subtítulos de 66 px: demasiado grandes. Son 44 px; el título, 60 px.
- Whisper **no escribe muletillas** («pues», «o sea») y a veces **inventa palabras** («Fue», «Segundo»): la alineación
  forzada pega esas muletillas a la palabra de al lado y se cuelan en el corte. → Verificar cada reel con
  `comprobar_reel.py` (transcripción literal con muletillas) y arreglar en `ajustes_tiempos.json`.
- Una palabra con puntuación de alineación muy baja (< 0,1) suele no existir en el audio: no la uses en subtítulos.
- Al quitar silencios el vídeo encoge ~35 %: los primeros guiones daban 35–47 s. Elige ~95–110 s de toma por reel.
- Subtítulos con más palabras en el texto que en el tramo de índices no se pueden partir solos: la herramienta avisa.
- Whisper con arranque seco confunde palabras («nación» por «un vacío»): antes de cambiar un corte, escúchalo en el
  original con algo de margen.
