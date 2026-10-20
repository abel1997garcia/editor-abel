---
name: reels-virales-criterio
description: Criterio COMPLETO de edición de los reels virales (brutos verticales) que Abel fue corrigiendo el 14/10/2026 en 067-075/068 — leer SIEMPRE antes de editar uno; la skill reels-virales lo aplica
metadata:
  type: feedback
---

**068 APROBADO (14/10/2026: «por fin… todo el vídeo está perfecto»)** → es el modelo. Cada reel viral se hace recorriendo la CHECKLIST del final de la skill `reels-virales`, casilla a casilla.

Abel 14/10/2026: «todas estas cosas que estamos corrigiendo guárdalo en la memoria… si tenemos que ir vídeo por vídeo revisando todo es una locura». Todo está ya en `reel_tablero.py` / `motor_f4.html` / `revisar_cortes.py` y en la skill `reels-virales`; esto es el porqué, para no volver atrás.

**Proceso**
- Siempre TRIAL. Formato único F4 viral (`"estilo": "viral"`). Nada de F3 (con vertical deforma/corta su cara) ni F5.
- El vídeo se llama igual que su GUION del Drive: leerlo antes. Al final, lo que se oye (Whisper sobre voz.wav) se compara con el guion: ni ganchos colados (068: el gancho 3 dos veces), ni frases que falten («tu vecino, tu prima»), ni repetidas.
- Primero UN reel completo y se le enseña; con su OK, los demás.
- Escucha corte a corte obligatoria (`revisar_cortes.py`) + escucha entera. Nunca entregar sin las dos.

**Cortes** (islas de voz de la onda, nunca tiempos de Whisper)
- Ninguna palabra ni letra comida: las «s» al principio y al final se protegen por sus agudos.
- Si dos tomas/ganchos van sin silencio claro: cortar JUSTO antes de que arranque la voz sostenida de la primera palabra (no en el valle más hondo: ahí se colaba la «s» de «clientes» → «…s Vivimos»).
- **Las «s» (lo que más ha fallado, 068):** una «s» es solo agudos, la onda no la distingue de otra «s». Se decide CON EL TEXTO: si la palabra acaba en s/z/x, su «s» puede llegar SEPARADA tras un huequito («publica… s») y pegada a la palabra siguiente: se busca hasta 0,3 s y se incluye; si la palabra empieza por s/z/f/ce/ci/ch/j, igual hacia atrás; si empieza por otra letra («Vivimos»), el corte va donde arranca la voz en los GRAVES (la «s» de «clientes» de la toma de antes queda fuera). Tope = donde vuelve a sonar voz en graves, no la isla siguiente.
- Para comprobar un corte dudoso: MIRAR el espectrograma (`showspectrumpic`) de la grabación y del reel; ahí se ve si la «s» está.
- Respiraciones (coger aire) fuera. Silencios como ALEX LAVRI: ~0,05–0,07 s, máx. 0,07, también tras punto (Abel 15/10). `igualar`: aire 0,04 s, márgenes 20 ms, inicio redondeado hacia antes y final al fotograma más cercano; `revisar_cortes` da la mediana y el máximo.
- NUNCA prestar una «s» de otra palabra (probado en el 067: «queda todavía peor, la gente se da cuenta»). Si en la grabación casi no suena, se deja así.
- Trozos de otra toma / arranques en falso → `fuera`; si no se puede cortar sin notarse, la frase entera.

**Voz y mezcla**
- Voz que se oye: DeepFilterNet SUAVE (−15 dB) + EQ + brillo (+3 dB a 6 kHz), a −14 LUFS. NUNCA expansor (se comía las «s», voz «rara»). La fuerte (−40) solo para medir.
- Música 11,5 dB por debajo y NO SE TOCA (Abel: «la música no es la que tienes que tocar, es la voz»; con sidechain «ni se oye»). Lo que se ajusta es la voz.
- Velocidad NORMAL 1,0x (Abel 19/10/2026).

**Imagen**
- `"mejorar": true` (contraste y nitidez). Zoom lento en los últimos 3,5 s.
- Subtítulos ARRIBA en la pared, negro con sombra muy suave (en la calle: blanco con sombra, lo detecta solo), 4-5 palabras por bloque, nunca cruzando un punto, sincronizados con la voz montada, mayúscula al empezar y tras cada punto, UNA palabra clave por bloque en azul eléctrico claro (#2E8BFF). Nada de morado.
- Título abajo en caja negra todo el reel, CRUDO y negativo (lo que le pasa por hacerlo mal, hacia la persona de `00-avatar-operativo.md`), visible con él en la vista previa de Instagram.
- La mejora de voz (voz suave + EQ) y de imagen (`mejorar`: contraste 1,09, nitidez 1,0) se comprueba en cada reel.
- Fotos: solo suyas, con contexto exacto, CUADRADAS y pequeñas (430 px), por debajo de su barbilla, él centrado. Base: FOTOS MIAS / fotos de carruseles SIN texto.

Ver [[edicion-reels-obligatoria]], [[fotos-vida-abel]], [[ganchos]].

**Programar (Abel 15/10/2026)**: de cada grabación salen 10 trials. NUNCA dos del mismo vídeo el mismo día, aunque cambie el gancho: cada día se sube la 1.ª versión de cada vídeo (si hay 3 vídeos, las 3 primeras; si hay 5, las 5…), al día siguiente las 2.ª, etc. `programar_youtube.py`: TRIAL → SEPARACION_CASUAL = 1 día entre versiones del mismo vídeo (orden por número: 067-069 = 1.ª versión de cada vídeo).

**Fallo del 075 (Abel: «si sigues el checklist no debería pasar»)**: el gancho repetido («Si empiezas tus… Si empiezas tus vídeos») lo marcó revisar_cortes y lo descarté como invención. Regla: si un aviso sale igual «junto» y «por separado», está en la grabación y es REAL; y el gancho se escucha aparte, sin prompt, palabra a palabra.

**Nunca decir «arreglado» sin comprobar el MP4 entregado** (Abel 15/10/2026: «¿por qué confirmas que está arreglado si no lo está?»). El 075 tenía TRES tomas del gancho; la comprobación sin prompt LITERAL las juntaba. Comprobar siempre el archivo final de REELS, gancho con prompt LITERAL.

**15/10/2026 — el formato F4 viral NO convence a Abel** («no conecta conmigo, edición muy básica, no llama la atención, muy mala recepción, no se entiende»): un vídeo de «10 razones» solo con subtítulos no muestra la lista; tampoco aprovecha un título-gancho. Le funcionaba antes (desarrollo personal): grabar en HORIZONTAL con plantilla blanca (título arriba en mayúsculas, subtítulo abajo) + lo que explica ESCRITO a mano (tablet: «① Ley del desapego»; o pizarra real detrás de él): la información ordenada y visible, 1.500-3.300 vistas. Pidió investigar ese tipo de formatos para marca personal. Le preocupa tener muchos formatos que mareen, pero «iremos probando y el que mejor funcione lo dejamos». Ver propuesta en la conversación del 15/10.

**15/10/2026 — NUEVO formato para los guiones virales: TABLET + yapping (F1).** Abel graba él mismo en VERTICAL con la tablet, escribiendo/dibujando lo que explica (la lista se ve: «① …»), como su formato antiguo de desarrollo personal. Yo edito con el formato yapping F1 (plantilla blanca: título arriba, subtítulos): música, cortes de silencios, trabazones y tomas (mismo método de islas + `revisar_cortes` + escucha entera + gancho aparte con prompt LITERAL + MP4 final), y el título según [[titulos-negativos]] (crudo, hablándole al cliente). El F4 viral queda APARCADO. Primeros 3 vídeos de tablet: los grabará el 15/10.

**15/10/2026 — DOS tipos de vídeo viral, MISMA plantilla** (la del yapping: blanco arriba y abajo, su vídeo en medio, él a la IZQUIERDA y hueco libre a la DERECHA; él ya graba en vertical con la plantilla montada):
1. **Listas / tier lists / comparaciones → TABLET**: escribe número + título de cada punto en la parte derecha.
2. **Mensajes / historias → SIN dibujos**: lee el guion en el ordenador. Yo: cortes (método de siempre), **título arriba** en el blanco (titulos-negativos, hablándole al cliente), **subtítulos abajo** en el blanco, música, y en el **hueco de la derecha una palabra clave o un emoji** que refuerce lo que dice (entra con un saltito y se va; ~1 cada 4-6 s, solo si aporta). Abel: «está perfecto».

**Estilo de la plantilla vertical (Abel 15/10/2026, con su ejemplo «Separar tu negocio de quién eres te está agotando:»):**
- TÍTULO justo ENCIMA de su vídeo, negro, tamaño normal (~50 px a 1080), 2 líneas, ~8-9 palabras terminado en «:» (titulos-negativos).
- SUBTÍTULOS justo DEBAJO del vídeo, TODOS NEGROS (ninguna palabra destacada en color), MÁXIMO 4 palabras.
- DERECHA: texto BLANCO con sombra suave directamente sobre el vídeo (estilo «Tú eres / TU NEGOCIO.»: línea normal + línea en MAYÚSCULAS más gruesa). NADA de cajas/etiquetas blancas («queda como un pegote, fatal») ni emoji + etiqueta a la vez («cutre»). Limpio, profesional y que se entienda.

**Plantilla yapping vertical (tablet/ordenador) — parte derecha de la franja (Abel 15/10/2026):** complemento de los subtítulos, NO otro texto que leer («va a ser un cacao»). Centrado en la zona libre de la derecha (cx≈840, centro vertical de la franja, entre x 660–1020, sin salirse), limpio: 1-3 palabras clave en blanco grueso con sombra suave, o un emoji grande. **NUNCA emoji y texto a la vez**: se alternan (más hueco, más visual). Movimiento pequeño y barato: entrada pop (escala 0,85→1 + fundido, 0,2 s) y flotar suave ±6 px; nada que alargue el render. Maqueta: MarcaPersonal/virales/tablet01/maqueta_secuencia.png.
- **Formato «pizarra digital» (19/10, en prueba)** para virales y listas (como @tuseienergia): una diapositiva por idea, sincronizada con el audio, personaje rojo (se abandona) vs azul (se elige). Análisis en `Referencias/tuseienergia/`. **Dibujos: Nano Banana en Replicate (0,039 $), estilo pizarra de explicación (trazo blanco, personaje con contorno rojo/azul, animado pero simple, el CONCEPTO general y no detalles), PNG TRANSPARENTE sobre el vídeo: NUNCA caja ni fondo detrás (Abel: «me pones un pegote»), solo una sombra suave pegada al trazo.** Biblioteca por contexto en `IMAGENES/pizarra/<contexto>/` + `catalogo.json`, separada de miniaturas: `herramientas/pizarra_replicate.py buscar` antes de generar (reutilizar) y `nuevo` para generar. Cada dibujo con contexto completo en el catálogo (significado, usar_cuando, palabras clave; las metáforas, como la del gato, solo cuando se cuenta esa metáfora): se elige por la idea que se escucha. Personajes: Fulano (rojo) y Mengano (azul). **Distribución (Abel 19/10, captura `IMAGENES/pizarra/_distribucion_video.png`):** título del reel arriba con connotación negativa y su longitud de siempre (~9 palabras, 2 líneas), dentro de la vista 3:4 de la cuadrícula (y 240-1680) y con margen lateral; título de la diapositiva dentro del vídeo, en la zona oscura, 2-4 palabras que den contexto del tema (como la referencia: «Fulano persigue», «Como un gato»); dibujo PNG debajo; subtítulos debajo del vídeo, 4-5 palabras en UNA sola línea (si no cabe, se baja el tamaño, nunca dos líneas). Capa en la herramienta: aparte y con su OK.
- **Pizarra (Abel 19/10):** títulos de las diapositivas BLANCOS, sin nada destacado en azul (no se ve), ideas de 2-4 palabras como mucho (título del reel + subtítulos + diapositiva = lío si es más). Esquemas como @tuseienergia: personaje + 2-4 iconos, diapositivas en paralelo rojo/azul, construyéndose; análisis en `Referencias/tuseienergia/ANALISIS.md`. Clave de Replicate en `C:\Users\Clap\.replicate_token` (nunca mostrarla ni copiarla a copias/GitHub).

**Edición de los 3 estilos de viral (Abel 19/10/2026, todos los guiones ya grabados):**
- **TABLET ·** la imagen de `LISTAS MIRO` NO sale entera desde el principio: se va REVELANDO punto a punto justo cuando Abel lo dice (en la lista, los números a la izquierda desde el inicio y cada texto aparece al decirlo, en el orden en que lo diga; escalera peldaño a peldaño; columnas, cada punto a su columna; batería, cada carga/descarga al nombrarla).
- **HISTORIA ·** el dibujo de pizarra 100 % con lo que dice en ese momento, entrando con un movimiento suave y elegante.
- **Sin prefijo (frases):** subtítulos a la derecha, como siempre.
- Todos grabados igual: Abel a la izquierda y la zona derecha VACÍA para poner lo que toque. En TABLET e HISTORIA los subtítulos van ABAJO en la franja blanca, una línea de 4-5 palabras (como el yapping), con los subtítulos del YAPPING de siempre: Montserrat ExtraBold 51 px FIJO, negro puro (#000000), sin animación (Abel 19/10/2026, eligió esta frente a Montserrat Black 72 px); en HISTORIA, encima del dibujo, su título de 2-4 palabras de contexto. La capa (revelar / dibujo con movimiento) va en la herramienta de REELS VIRALES: el proceso rápido, `rapido/render.py`. Hecha el 19/10/2026 (`rapido/capa_viral.py`): en `plan.json`, `"estilo": "tablet"` + `"tablet"` (forma, args, momentos) o `"estilo": "historia"` + `"diapos"` (frase, titulo, dibujo); el formato exacto, en su docstring. Sin «estilo», render.py hace lo de siempre. Probada sobre un clip; falta verla con el primer vídeo real.

**HISTORIA, correcciones de Abel (19/10/2026, 1.er vídeo):**
- **UN SOLO PERSONAJE** en todos los dibujos (para meterse en la historia): el muñeco de «17.000 € y vacío» = cabeza redonda, cuerpo BLANCO, contorno grueso ROJO (se abandona) o AZUL (se elige), cara mínima. Hojas de referencia: `IMAGENES/pizarra/_personaje/hoja_rojo.png` y `hoja_azul.png`; cada dibujo nuevo se genera con su hoja como `image_input` de Nano Banana.
- **Mismo tamaño siempre:** el dibujo se escala a una ALTURA FIJA y el conjunto título + dibujo va CENTRADO (horizontal y vertical) en la zona derecha.
- **Títulos de diapositiva como @tuseienergia:** cuentan lo que pasa en esa escena (quién, qué, cómo), 2-6 palabras, letra fina (Montserrat Medium) con la palabra clave gruesa (Black): «Te **traicionas** para agradar», «Lo tenía todo y estaba **vacío**». Nunca una etiqueta suelta («Lo das todo»). Una frase clave puede ir sola, sin dibujo.
- **ESCENA COMPLETA, no el muñeco solo** (Abel 19/10/2026, «súper guays… enhorabuena»): con quién está, dónde, qué siente y qué le pasa, metáforas visuales claras; los demás en contorno gris. Una escena por diapositiva, hecha para ESE guion (`IMAGENES/pizarra/escenas/<vídeo>/`, ~0,30 $ por vídeo). Método completo en el docstring de `herramientas/pizarra_replicate.py`. Movimiento: solo la entrada (fundido que sube y frena); más movimiento competiría con su cara (Abel: «si marea o no añade calidad, no lo hagas»).
- Aprobado: `EDICION VIDEOS/LISTAS MIRO/_maqueta_historia_v3.png` y el 1.er vídeo (historia01).

**Saber el formato de cada vídeo (Abel 19/10/2026):** el archivo grabado no lleva prefijo; se busca su guion en el Drive (PARA GRABAR/REELS o GRABADOS, id 11T484Y_Ey8ltifaQZPHeFayg2YvgbeG1) y su prefijo manda (TABLET / HISTORIA / normal). Fulano y Mengano = siempre HISTORIA. «Atraes lo que crees que mereces» lo edité como normal por no mirarlo: error.

**Formatos (Abel 19/10/2026):** cada vídeo se edita en el formato de su guion del Drive, sin convertir (probé pasar normales a TABLET y «en el contexto no se entiende»). Pendiente para más adelante: crear NUEVOS guiones HISTORIA desde otros ángulos de la autoestima (bloques de A-QUIEN-LE-VENDO), tomando de referencia los que ya funcionan.

**Psicología del color (Abel 19/10/2026):** VERDE = lo que suma / importa / funciona (columna IMPORTA, CARGA, el puesto 1 del ranking, iconos ✓); ROJO = lo que resta (NO IMPORTA, DESCARGA, ✗, el personaje cuando se abandona); AMARILLO = neutro (numeración, anillos). Usarla siempre para decidir el color.

**Psicología del color (Abel 19/10/2026):** VERDE = lo que suma / importa / funciona (columna IMPORTA, CARGA, el puesto 1 del ranking, iconos ✓); ROJO = lo que resta (NO IMPORTA, DESCARGA, ✗, el personaje cuando se abandona); AMARILLO = neutro (numeración, anillos). Usarla siempre para decidir el color.

**Tamaño de letra en TABLET (Abel 19/10/2026, aprobado «el tamaño está bien»):** la referencia es «10 razones» (tablet14, 101-105): la lista llena casi todo el ancho de la zona derecha, letra blanca ExtraBold grande y limpia, anillos amarillos proporcionados a la fila. En `lista_tablet.py` el tamaño va proporcional a la fila (`paso*.62`, máx. 84) con el texto pegado al anillo; lista y ranking ya lo hacen. Si una forma nueva sale con la letra pequeña o con hueco vacío a la derecha, se ajusta a este nivel: que se lea bien sin recargar.
**Velocidad 1,0x en TODOS los reels (Abel 19/10/2026):** 101-110 rehechos a 1,0x (los de 1,07x en PARA BORRAR). Ojo: la velocidad la fija `montar.py` (edl.json); volver a renderizar NO la cambia, hay que volver a montar.
**TABLET sin «pegotes» (Abel 19/10/2026):** NADA en la zona derecha puede parecer un bloque pegado (ni fondo negro, ni marco/contorno grande que encierre todo): siempre PNG transparente, elementos vectorizados sueltos (iconos dibujados, p. ej. `IMAGENES/pizarra/iconos/bateria_carga_verde.png` / `bateria_descarga_roja.png`). Elegir la forma que mejor se LEA: lo que carga/descarga, suma/resta, importa/no importa → dos grupos verde / rojo con su icono (`lista_tablet.columnas`), no una pila dibujada; la herramienta elige sola lado a lado o uno ENCIMA del otro según dónde salga la letra más grande. TODO ALINEADO A LA IZQUIERDA y ordenado (icono + cabecera de color, cada punto con su puntito de color), nunca centrado. Vale para TODOS los diseños de TABLET; el PNG para Miro también sale transparente. Textos de cada punto cortos (2-3 palabras) para que la letra salga grande.
**HISTORIA: ninguna escena dura más de 7 s (Abel 19/10/2026: «si un dibujo dura mucho se hace pesado y cansino»; vio 18,7 s en historia06).** Una escena por frase/idea, y si una frase larga pasa de 7 s se parte con otra escena (reutilizar de la biblioteca si encaja). Comprobar ANTES de renderizar: `python herramientas/rapido/duracion_escenas.py <carpeta> r1 r2…` (límite `MAX_ESCENA` en `capa_viral.py`). Si un reel empieza con un gancho que es una frase del cuerpo, lleva sus propias `diapos` en ese orden.
