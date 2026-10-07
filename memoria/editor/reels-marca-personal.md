---
name: reels-marca-personal
description: "Abel's vertical reels — messages from each long video turned into reels (hook + structure + format F1/F2/F3) split into publicar/ and trial/, plus the rules common to all formats"
metadata:
  node_type: memory
  type: project
  originSessionId: d5e16cfe-1dfc-4d01-ac23-7f43e2a0e419
  modified: 2026-10-06T20:59:37.011Z
---

Los reels se sacan del **vídeo horizontal ya editado** ([[estilo-videos-largos-stickman]]). 
## Común a los 3 formatos
- **Gancho:** primera frase cruda, en 2ª persona, sin nada delante; temas del avatar: energía, vibración, conciencia, inconsciente, emociones ([[posicionamiento-abel]]). Modelo: reel 3 de «Sin buena intención» ([[registro-edicion-abel]]).
- **Retención seminal:** en los vídeos que hablen de ella, los reels no la mencionan; se quedan los tramos sobre la energía, cómo te hace sentir y la emoción.
- Silencios con los dos criterios de [[registro-edicion-abel]]. Acaba en una frase completa.
- **Todo a 1,10x** (vídeo, voz y subtítulos; la música a su velocidad).
- **Título:** MAYÚSCULAS, Montserrat, ≤ 7 palabras en 2 líneas equilibradas; afirmación cruda, polémica, algo clickbait, que remueva; nunca «puede ser».
- **Subtítulos** en Montserrat. **Voz tal cual** (sin procesar ni bajar de volumen). **Música** de su carpeta `C:/Users/Clap/Desktop/EDICION VIDEOS/MUSICA/` (`catalogo.json` con duración y estribillo), **26 dB por debajo de la voz**, desde el estribillo; con mucho texto, mejor instrumentales (Interstellar, Einaudi, M83, Andrea Vanzo, Tony Ann).
- **Efectos de sonido en F2 y F3** de la biblioteca `herramientas/sonidos/` (los del horizontal aprobado; qué efecto va en cada momento y a qué volumen en `usos.md`). F1 ya los trae del horizontal.
- Lo importante fuera de la interfaz de Instagram/TikTok: arriba ~220 px, abajo ~320 px (usuario y descripción) y la columna derecha de botones (x > ~930 desde y ≈ 1000).
- **Imágenes (también en el horizontal):** cada foto tiene que servir a la vez para el F2 (hueco casi cuadrado) y el F3 (tarjeta horizontal): horizontal, **reciente** (último año o dos), nítida (≥ 1080 px de ancho si se puede), encuadre algo abierto (cabeza y hombros enteros, nunca la frente cortada), información legible, sin textos ni logos dentro del recorte. Se elige otra foto antes que rellenar con bandas o desenfoques (quedan fatal). Buscar bien en Google Imágenes (filtros: último año, grande, panorámica); los fotogramas de entrevistas recientes suelen ser lo mejor. Los derechos no le preocupan (es de fondo); **cada descarga se le confirma antes** (archivo, origen, tamaño).

## Los formatos (nombres fijos)
- **F1 · YAPPING 4:3** (su plantilla 2) — hecho, `herramientas/reel_yapping.py` (config por vídeo; ejemplo `VideosLargos/emociones-v3/reel_prueba.json`). Lienzo blanco 1080×1920; el horizontal recortado a 4:3 a todo el ancho (y 547–1357; en planos de cara centrado en él con acercamiento alterno 1,0/1,10, en animaciones el 4:3 central). Título encima (Montserrat ExtraBold 51 px reales, líneas a 61 px), subtítulos negros debajo (51 px, una línea de ≤ 3 palabras).
- **F2 · IMAGEN ABAJO** — aprobado en maqueta (`MarcaPersonal/formato2/maqueta_formato2_dispenza.png`), herramienta por hacer. Arriba él (0–760 px, nunca ampliado de más: se difumina); subtítulos palabra a palabra, Montserrat ExtraBold blancos con sombra negra, justo bajo su boca y por encima del título; franja blanca de lado a lado (760–940) con el título en Montserrat Bold negro, un poco hacia arriba; abajo (940–1920) **predomina la imagen**: 3–4 imágenes reales de lo que dice, centradas y con lo importante fuera de la interfaz. Esquemas (p. ej. mapa de Hawkins) dibujados por mí. **Siempre en movimiento** (engancha): acercamiento lento de la imagen, transiciones al cambiar de imagen y motion graphics ligeros encima sin tapar lo importante (nombre en pastilla que entra, subrayados, flechas, palabra clave que salta), con sus efectos de sonido.
- **F3 · TABLERO** — aprobado en maqueta (`MarcaPersonal/formato3/maqueta_formato3_gancho.png` y `…_desarrollo.png`), herramienta por hacer. Origen: reels de Matías Molaro (youtube.com/watch?v=4XMkySfL7Kw; análisis en `Referencias/formato3/`).
  - **Gancho:** tablero desde el segundo 0: arriba la tarjeta de contexto (foto/clip de la persona o noticia citada, nombre en pastilla negra), en medio su palabra en grande y abajo él en su tarjeta redondeada, **entero dentro de la tarjeta** (sin cabeza saliendo del marco: se nota la línea del recorte y no le gusta).
  - **Ritmo:** alterna tablero y él en grande cada 4–6 s; graba a 1080p (no 4K): su tarjeta crece (≈ 4:5) sin llenar la pantalla, con afinado suave si no se nota.
  - **Gráficos** (dibujados con la librería de la pizarra): titular en pastilla negra, barras (negro frente al acento), palabra que cambia (vieja tachada en gris → nueva en acento), contador o anillo con cifra grande, órbita de iconos, tarjetas tipo pantalla, carta de la persona citada, comparativa lado a lado y cierre con llamada a comentar; stickman en historias y silueta para energía y cuerpo.
  - **Subtítulos:** 1–2 palabras palabra a palabra, ExtraBold, negro sobre el tablero y blanco sobre él; a veces la frase en pequeño y gris encima.
  - **Colores:** tablero blanco con trama de puntos, texto negro y gris, y **un acento por reel = el color del chakra del tema** (p. ej. dopamina → sacro #E06A1B); logos e imágenes reales cuando nombra algo. Emojis pocos y solo en el storytelling.

- **F4 · dibujo a mano: descartado** (07/10/2026). Probado (`MarcaPersonal/formato4/prueba_formato4.mp4`) frente al mismo trozo en motion graphics F3 (`MarcaPersonal/formato3/prueba/prueba_F3_mg.mp4`): «el de motion graphics funciona mucho mejor».

## Descripción de cada reel (Instagram, TikTok…)
Cada reel (también los de trial) lleva su propia descripción, escrita como habla él (tono de barra de bar, como sus transcripciones), en 2ª persona, adaptada al mensaje del reel y **sin sonar a IA**: nada de frase corta, punto, frase corta, punto; frases algo más largas que fluyan.
1. **Primera frase = gancho en texto (90 %): corta** (la excepción a las frases largas; muy importante), rompedora, cruda, polémica, que remueva.
2. **El porqué** con situaciones concretas del día a día del avatar.
3. **Su creencia como experiencia propia** («para mí…», «yo no creo que…»), con autoridad, sin vender certezas que no tiene ni inventarle historias.
4. **Cierre corto** que confronte o deje algo que hacer.
5. **`#abelunidad`** al final, siempre (único hashtag).
Ejemplo suyo: «Lo que te da miedo de morir no es la muerte, es darte cuenta de que igual no has vivido tu vida. / Porque en el fondo actúas como si esto fuera infinito. Aguantas un trabajo que odias, sigues con gente con la que ya no quieres estar, no haces eso que llevas años pensando porque "ya habrá tiempo"… y así se te van los años. Yo no creo que cuando mueres simplemente desaparezcas y ya está, para mí la muerte es un cambio de conciencia, no el final. Pero precisamente por eso cada vez entiendo menos vivir con miedo a hacer lo que de verdad quieres hacer aquí. No sé qué hay después ni te voy a vender que lo sé, pero sí sé que algún día este cuerpo se acaba. / Y hay decisiones que llevas demasiado tiempo dejando para luego. / #abelunidad»
Va en un `.txt` con el mismo nombre que el vídeo, al lado (`publicar|trial/semana_…/`), y en el `plan.md`.

## Mensajes, variantes y carpetas
- **Mensajes:** de cada horizontal, tantos como haya buenos, ninguno por poner. Cada uno ataca una creencia u objeción, recoge una frase de batalla o algo que él piensa, o deja algo aplicable; auténtico, con su **punto diferenciador** (lo más importante), claro y que transmita autoridad. Gancho = 90 %; estructura con sentido hasta el final; útil, que deje ganas de más; conecta con el avatar. Duración la que pida el mensaje: mínimo 40 s, lo óptimo en torno a 1 min (hasta ~1:15), medido en el reel final.
- **Cada reel = gancho (g1, g2…) + estructura (e1, e2…: qué trozos, en qué orden y cómo acaba) + formato (F1–F3).**
- **`publicar/`** (hasta 3 por mensaje): gancho, estructura y formato distintos (si solo hay un buen gancho, uno).
- **`trial/`** (Instagram los enseña solo a no seguidores): el primer publicable en los otros 2 formatos (prueba de formato) y, si sobran ganchos buenos, misma estructura y formato con el gancho alternativo (prueba de gancho).
- **Archivos:** `MarcaPersonal/publicar/` y `MarcaPersonal/trial/`, cada una **por semanas** (`semana_<lunes AAAA-MM-DD>/`), con el día delante del nombre: `<día>_<vídeo>_c<NN>_g<N>e<N>_<F1|F2|F3>.mp4` (p. ej. `mie_dopamina_c03_g2e2_F2.mp4`), para mezclar vídeos en el calendario. Y un `MarcaPersonal/<vídeo>/plan.md` con cada reel: mensaje, gancho (frase exacta), estructura, formato, título, música, duración, carpeta, semana y día (los del mismo mensaje, separados).

**How to apply:** antes de entregar, volver a transcribir el MP4 final y leerlo entero.
