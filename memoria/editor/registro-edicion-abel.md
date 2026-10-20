---
name: registro-edicion-abel
description: "Running log of lessons from each video I edit for Abel — his feedback, approved choices, and my own mistakes to avoid"
metadata:
  node_type: memory
  type: feedback
  originSessionId: d5e16cfe-1dfc-4d01-ac23-7f43e2a0e419
  modified: 2026-10-05T01:02:49.465Z
---

Leer antes de cada edición; ampliar después (ver [[aprender-de-cada-edicion]]).

## REGLA GENERAL · Silencios y microsilencios (Abel 12/10/2026: «sí o sí, siempre», sustituye a la de 05/10)
Vale para todo: vídeos largos y reels. Se limpian con la transcripción las muletillas («¿de acuerdo?», «o sea»…), las equivocaciones, los arranques repetidos y las repeticiones. Además, **todo silencio entre dos palabras (respiraciones incluidas) queda en ~0,05–0,07 s, como Lavri; en un reel NINGUNA pausa pasa de 0,07 s y > 0,10 s ya es error (Abel 13/10/2026; antes 0,15)**, también dentro de la frase, para dar dinamismo, **pero sin cortar nunca una palabra**.
- Se mide en el AUDIO, no en los tiempos de Whisper: `microcortes()` de `reel_yapping.py`, que ya llaman `ajustar_finales` (reels F1/F3) y `limpiar_largo.py` (horizontales).
- No corta si deja un plano < 1 s, ni en el cierre (`intacto_desde`).
- El arranque de una palabra suave («habrá») lleva 0,09 s de margen. A −24 dB se comía esos arranques; ahora el umbral es pico − 30.
- Medir antes de renderizar: `silencedetect` en la voz no debe dar pausas > 0,10 s salvo el final (la línea `listón` de `--voz`).
- Si el verificador dice que falta una palabra en una unión, se comprueba transcribiendo ese trozo suelto. En «empezar desde 0» varias eran falsos avisos de Whisper («habrá», «coño»).

## REGLA GENERAL · El horizontal se hace pensando ya en los reels (Abel, 08/10/2026: «muy, muy importante»)
Todo lo que se pone en el horizontal (frases clave y, si las hay, animaciones: textos, dibujos, personajes, emojis, flechas) va **dentro del 4:3** (x 280–1640 con margen, contando la deriva de cámara: nada a x < 350), y cada animación se entiende sola con su frase. **Por qué:** así el reel F1 sale del horizontal con solo recortar y pulir (animaciones, audio y efectos ya hechos); si algo se sale, hay que volver a programar y reajustar para el vertical, que cuesta mucho más tiempo y recursos. `herramientas/pizarra/revisar.mjs` tiene que dar «todo bien» (vigila el 4:3) antes de montar, y en las hojas de revisión se mira el 4:3 central, no la pantalla entera.

## REGLA GENERAL · Limpiar al terminar (Abel, 06/10/2026)
**Abel 12/10/2026: «ve quitando el contenido ya editado que no usaremos más, para ir limpiando espacio».** Al entregar los reels de un vídeo, se borran sus `out*/`, la toma limpia, `anim/` y `transcripcion/`, y quedan solo los .json, los .js y el plan. Los vídeos de referencia se borran en cuanto están analizados (quedan el análisis y las capturas). Las grabaciones originales, los horizontales finales y `MarcaPersonal/REELS/` nunca se tocan. Si algo puede hacer falta para rehacer un reel pendiente, se le pregunta antes.
Con un vídeo hecho y verificado, se borra lo usado y solo quedan: su grabación original, los entregables finales, las configuraciones pequeñas (los .json y escenas.js) y, **hasta entregar sus reels**, lo que estos necesitan (estándar: `<horizontal>.tiempos.json` y `.montaje.json`; con animaciones: toma_limpia.mov, trabajo/tiempos.json, edicion/montaje.json, index.html). Fuera: versiones anteriores, renders intermedios (`out/`), audios y pistas de trabajo, proxies, fotogramas de revisión, ficheros auxiliares y vídeos de referencia ya analizados. Al acabar los reels, también lo que solo servía para ellos.

## Error · c03 de «empezar desde 0» (12/10/2026: «los cortes no son limpios del todo»)
El verificador decía que faltaba «tú imagínate» y se oía «realmente que cuando salgan…». Lo di por falso aviso y era un corte que dejaba un trozo de palabra. **Si falta una palabra que SÍ está en la toma original (comprobarlo transcribiendo la fuente), es un corte malo:** se mueve el tramo o se corta antes o después de esa frase, nunca se acepta.

## Error · horizontal con cientos de microcortes (12/10/2026, «energía y negocio»)
Cada trozo se redondeaba a fotogramas y la voz acabó 1,8 s desviada de `.tiempos.json`, así que los reels F1 salían con huecos de 0,6 s. Ya lo corrige `limpiar_largo.py`, que cuadra cada corte a 30 fps. **Comprobar siempre** que la suma de `.planos.json` coincide con la duración real del vídeo (± 0,1 s).

## Lo que Abel ha aprobado
- 12/10/2026 · Los 15 reels rehechos de «empezar desde 0» con la skill `reels-abel`: «la edición está mucho mejor, los títulos mucho mejor, los cortes, los silencios y la fluidez, todo mucho mejor». Es el nivel de referencia (microcortes medidos en la voz, títulos tipo Lavri). Solo falló el gancho de «sin guiones» (ver [[ganchos]]).
- 05/10/2026 · Reel 3 de «Sin buena intención…» («Si la intención es ganar dinero, sé honesto»): «está genial, aprende de eso». **ES EL MODELO DE REEL.** Por qué funcionó:
  - El gancho es una frase literal suya, en 2ª persona, que suena en el segundo 0.
  - Pocos tramos y largos (4 bloques), cada uno una idea completa, con un hilo claro: gancho → por qué (ego espiritual) → qué hacer (preguntas correctas) → cierre.
  - Habla de corrido en esos bloques: casi sin trocitos sueltos ni muletillas que quitar.
  - Termina en una frase completa con pausa natural detrás («…durante muchos años.»).

## REGLA GENERAL · ESCUCHAR antes de entregar (Abel, 08/10/2026: trial 550.000 € «muy, pero que muy mal cortado… ¿realmente lo has revisado?»)
- Mirar fotogramas y texto NO basta. Antes de dar por bueno cualquier reel (y los horizontales), pasar **`herramientas/verificar_audio.py <out/_reel> <tiempos.json>`**. Se lanza con `--fotos 1` (genera solo el audio) antes del render completo. Hace esto:
  - vuelve a transcribir y compara el texto;
  - comprueba cada corte muestra a muestra (cortes sobre la voz, sin respirar, huecos);
  - transcribe de nuevo cada corte por separado;
  - mide el ritmo.
- Tiene que salir ✓. Además, **leer en voz alta cada unión ‖**: si no suena a una sola frase natural, se cambia.
- **No reordenar su discurso.** Montar «gancho del final + contexto de antes» dejó frases sin sentido («me dieron la placa | me di cuenta de que siendo…»). Su orden, casi de corrido; el contexto se da con imágenes.
- **No repetir en pantalla lo que ya dice él y ya sale en el subtítulo.** El «550.000» salía tres veces a la vez: título + texto grande + subtítulo.
- Una palabra suelta («dije», «y») se une a su frase. (08/10: cortar por los tiempos de Whisper dejaba 25 cortes en 53 s, «nada fluido»; ahora los microcortes se miden en el audio y quedan unos 3–4 cada 10 s.)

## REGLA GENERAL · Ganchos (Abel, 08/10/2026)
Directos, sin relleno delante («Tú cuando tenías…» → «Con 20 años tenías miedo a que te criticasen… y no les importabas una puta mierda»: fuera «tú cuando», «y», «realmente»). Si la frase del avatar de esa parte no engancha («Vas sacando un montón de emoción que has reprimido» no tiene ningún sentido como gancho), se abre con el momento más fuerte de esa parte aunque sea su historia («Estuve 15-20 minutos llorando sin parar, pensando que me había vuelto loco…») y la idea va después. Aprobados como buenos: «Las adicciones como tal no existen», «Te aseguro que en la vida no existe ninguna casualidad».

## REGLA GENERAL · Cortes fluidos y finales limpios (Abel, 07/10/2026: c02 «se corta muy brusco, eso hay que vigilarlo»)
Ningún corte puede comerse el final de una palabra ni empalmar en seco: si la palabra siguiente va pegada (hueco < 0,1 s), se añade el aire que falta (silencio + último fotograma quieto) con un fundido de audio de ~40 ms. El reel acaba con ≥ 0,5 s de cola tras la última palabra, aunque en la toma él siga hablando. Ya lo hace `reel_tablero.py` (`rellenos`); antes de entregar, escuchar cada unión y el final.

- 08/10/2026 · «La intención y energía masculina»: horizontal + 3 reels F3 (tras corregir cortes, música y final): «lo has hecho muy bien». Receta en [[estilo-videos-largos-stickman]] y [[reels-marca-personal]]; ejemplo completo en `VideosLargos/intencion-masculina/` y `MarcaPersonal/intencion-masculina/`.

## Mis errores ya corregidos (no repetir)
### Reels (feedback 05/10/2026)
- **Tramo o reel cortado a mitad de frase** (reel 2, s. 33–34: «ni a qué vengo» sin «aquí»; el reel 1 acababa en «…mucho más acertada»). La última palabra de cada tramo va seguida de una pausa ≥ 0,3 s en la toma; si no, alarga el tramo. El reel acaba en una frase completa y rotunda con 0,4 s de cola.
- **Dejar equivocaciones**: dos arranques seguidos («puedes hacer eso y puedes empezar…»), titubeos («quiero es es que»), autocorrecciones («de corazón… razón»), dobles muletillas («realmente, y digo realmente»). Antes de montar, buscar en la alineación: palabras repetidas cerca, palabras con puntuación < 0,6 y arranques que se reformulan, y quedarse solo con la versión limpia.
- **Trocitos sueltos de < 0,5 s** («minúsculas | que | ayuden») al quitar una palabra en medio de una frase fluida: suenan entrecortados. Mejor quitar o conservar la frase entera, o cortar en una pausa natural.
- Whisper duplica a veces una palabra en el cambio de segmento («hacer hacer»). Si una de las dos sale con puntuación ≈ 0,2 en la alineación, no se dijo dos veces: no la quites, o te comes la buena.

### Animaciones (vale para cualquier animación)
- Texto de animación encima de tallas o madera con mucho detalle: no se lee. Ponerle siempre sombra oscura amplia o un fondo (pastilla) y bajar el brillo de la sala.
- Palabra partida en dos (tajo): separar las mitades a lo largo del corte, nunca en vertical; si no, parecen dos palabras superpuestas.
- Anillos y ondas finos y semitransparentes: no se ven en móvil. Grosor ≥ 4–6 px y color vivo.
- Rótulos que se superponen en el cierre (sello y título que sube): revisar los últimos 2 s fotograma a fotograma.
- Antes de alargar la cola, mirar el final de la toma original: los vídeos de Abel pueden acabar con una cartela negra quemada (CTA). Hay que taparla con el fondo y rehacerla con el estilo del vídeo.

### Vídeos largos
- **`anim.py cortar` de la skill NO sirve para limpiar a Abel** (solo corta entre frases completas): se limpia con `herramientas/limpiar_largo.py` y la toma limpia pasa a la skill sin cortes. Flujo completo en [[estilo-videos-largos-stickman]].
- Sus grabaciones pueden ser **pantalla partida**. **ERROR mío:** la convertí en una ficha centrada en su cara. Se respeta su estructura.
- «Regula tu dopamina» v1 (05/10/2026): sus fallos ya están corregidos en las herramientas y como reglas en [[estilo-videos-largos-stickman]].
- **«La intención y energía masculina» (07/10/2026), errores míos ya corregidos:**
  - La alineación forzada **comprime las últimas palabras de la toma** (puntuación 0): `cortar` dejó el horizontal 1,3 s corto, **sin su «Nos vemos en el próximo vídeo»**, y un reel cortaba «toda tu vida». Comprobar siempre que `CONFIG.dur` = duración de la toma limpia y transcribir los últimos 5 s del entregable.
  - Una animación tapaba sus zooms de énfasis: tras `ventanas.py`, recortar las ventanas al empezar cada zoom (`herramientas/pizarra/recortar_zooms.py`).
  - Con la deriva de cámara (+4 %), lo que va a x < 350 se sale del 4:3: listas y ✓ desde x ≥ 350.
  - c02 acababa mal en «toda tu vida»: puse a ojo el final de las palabras que la alineación había comprimido y corté la cola de «vida». Los tiempos de palabras dudosas se miden con la envolvente de energía (cada 20 ms), nunca a ojo.
  - c01: quitar un silencio entre «…que esté en la misma frecuencia | que estés tú» dejó dos «que» seguidos que suenan a tropiezo. Si al recortar una pausa quedan dos arranques iguales, se quita el apéndice.
  - Los finales e inicios de palabra del alineador fallan 0,05–0,1 s: el corte se comía la cola («frecuen-» sonaba a «que») o arrastraba la palabra anterior («Y cada vez…»). Ya lo corrige `ajustar_finales` (reel_yapping.py, lo usan F1, F2 y F3) midiendo el audio. Comprobar siempre aislando la unión: Whisper con la frase entera «inventa» palabras.
  - Al unir tramos, no repetir palabra en la unión («o sea todo | todo es energía»): acortar el tramo.
  - En F1, si el horizontal tiene una frase destacada en ese tramo, el título del reel no la repite.
  - La alineación puede estirar la última palabra de un tramo hasta 1 s dentro de un silencio (zona con palabras mal alineadas al lado): el corte y el aire se miden en el audio, no con esos tiempos (`ajustar_finales` y `rellenos` de reel_yapping.py ya lo hacen). Verificar siempre la pausa máxima del reel final (≤ 0,3 s).
  - En las descripciones no se le inventan vivencias («lo he visto en mi vida…»): solo su creencia.
- Para que nada tiemble: toda forma recalculada pasa por `forma(e, fn)`. `[a, b].forEach(escribir)` es un error (forEach pasa el índice como t).

## Preferencias de Abel (ir ampliando)
- Quiere el vídeo terminado; las preguntas de estilo, en una sola tanda al principio.
- Agradece el feedback detallado por segundo («en el segundo 33–34»): usar la línea de tiempo del reel para localizarlo.

- **Español de España en TODO lo que escribo para él** (títulos, descripciones, guiones; Abel 13/10/2026): «visitas», no «vistas»; «me gusta», no «like»; nunca «cagazo».
- **Whisper puede «tragarse» una repetición dentro de una palabra larguísima** (13/10/2026, casual «tú eres el producto»: «Australia» de 52,1 a 56,0 s escondía «…desde cero» dicho dos veces).
  - Antes de montar, revisar en `tiempos.json` las palabras de más de ~1 s.
  - Pasar SIEMPRE `verificar_audio.py`, que vuelve a escuchar y detecta la repetición.
  - Corregir los tiempos de esas palabras para que la repetición quede fuera.
  - Ojo también con lo que Whisper se inventa («tú eres tú. Es tu propio» era «tú eres tu propio»).
- **Recortes pequeños (los de las 3 versiones de un casual):** quitar frases con PAUSA delante y detrás («que si no sé qué», «porque de esos hay miles», «tus valores»). Si no, la unión queda pegada y se come palabras («Yo | enseño» sonaba «lo enseño»).

## 13/10/2026 · Reels de «cobrar barato» (tanda 2)
- **TODOS los reels de sus vídeos largos van a PUBLICAR.** TRIAL = solo los guiones virales de otras marcas personales.
- **Nada se dice dos veces, aunque lo repita a propósito** («la información, la gran mayoría de la información», «no es nada de eso, no es absolutamente nada de eso»). Se corta y se queda una versión.
- **Velocidad:** NORMAL 1,0x (19/10/2026; antes 1,10x y 1,15x): el ritmo lo dan los silencios recortados.
- **Música:** 13,5 dB por debajo de la voz (antes 11,5): «baja un poquito el volumen».
- **Queja recurrente:** «por lo general no lo haces limpio». El mensaje tiene que quedar entero, dinámico, fluido y profesional. Leer el `--texto` buscando repeticiones y frases a medias ANTES de la voz, no solo fiarse del listón.
- **Cortar como un editor humano (Abel 13/10/2026):** al final de cada reel quedaban unos 0,4 s callado (`COLA_FINAL` = 0,5). Ahora es 0,1 s, y `herramientas/onda.py` dibuja la pista de audio del reel terminado y marca cualquier hueco de más de 0,10 s (principio, medio o final). Se mira SIEMPRE antes de entregar.
- **RITMO DE LAVRI (Abel 13/10/2026: «si no hay silencios, nosotros tenemos que hacer la edición así»).** Medido en su reel `DeNRktgtcyT`:
  - 4,47 palabras/s;
  - pausas reales de 0,01–0,05 s (máx. 0,10);
  - 0,16 s tras la última palabra.
  - Nuevo estándar: los microcortes dejan ~0,07 s (antes ~0,13).
  - Tras el ajuste, los reels 064-066 quedan en p90 0,06–0,07 s.
