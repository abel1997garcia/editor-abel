---
name: fallos-edicion-reels-allan
description: "Fallos cometidos y correcciones al cortar reels de Allan (desincronía audio/vídeo, microcortes y ráfagas de cortes, tamaños, muletillas coladas, palabras inventadas)"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 5031045c-b367-4cb9-8826-ca24be54d6d4
  modified: 2026-10-05T10:08:45.031Z
---

El usuario pidió apuntar fallos y correcciones. Edición de historia allan medium.mp4 (2026-10-05):
1. **Audio y vídeo descuadrados (lo más grave, el usuario lo marcó como primordial).** Monté la imagen con `select=`
   sobre el original y el audio aparte: select deja los fotogramas en el orden del original, así que al adelantar el
   gancho la imagen no correspondía a la voz (desfases de 3–86 s). Corrección: cortar cada trozo con imagen y audio del
   mismo comando y concatenar en el orden del reel; medir con herramientas/medir_sync.py (media de todos los fotogramas
   de cada trozo; medir con un solo fotograma da falsos ±1–3). Nunca procesar imagen y audio por caminos separados.
2. **Microcortes = habla robótica.** Recortaba toda pausa > 0,3 s y quitaba palabritas sueltas («que», «porque», «y»).
   Ahora: solo pausas > 0,7 s (quedan ~0,32 s), márgenes 0,12 s antes / 0,20 s después, y solo muletillas/titubeos reales.
3. **Ráfagas de cortes (pendiente de mejorar, feedback de la 2.ª versión):** aunque cada corte esté justificado, varios
   cortes muy seguidos (3 en < 3 s) suenan a «corte, corte, corte». reel_franjas.py avisa con «AVISO ráfaga de cortes».
   Regla: en esos tramos conservar alguna pausa (no recortarla) o elegir otro tramo; repartir los cortes.
4. **Tamaños:** subtítulos 44 px (yo puse 66 tras escalar ×1,5 lo de OpusClip: demasiado grandes); título 60 px.
   Pero en franja negra dijo «39 px» y quería lo de OpusClip (≈59 px reales). Regla: si da un tamaño y hay captura,
   medir la captura; si no cuadra, preguntar antes de montar.
5. Whisper omite muletillas («pues», «o sea») y la alineación las pega a la palabra vecina → se colaban. Verificar con
   comprobar_reel.py y extirpar con trabajo/ajustes_tiempos.json («hueco_antes»). La pasada larga de Whisper da falsos
   positivos: escuchar lo dudoso en clips cortos con herramientas/oir.py antes de tocar nada.
6. Whisper inventa palabras («Fue», «Segundo»); puntuación de alineación < 0,1 = probablemente no existe.
7. Quitar silencios encoge el tramo: reservar ~95–110 s de toma por reel.
8. Al partir subtítulos/títulos no dejar palabras débiles colgando; subtítulos fieles al audio y bien escritos
   («firmase», «mediumnidad»).

9. **Silencio al final del reel (canal_02_calma, feedback del usuario):** tras «todo el día los dos» quedaban ~2,3 s de
   silencio. Causa: la alineación forzada estiró la última palabra («dos», 2,6 s, puntuación 0,0) sobre el silencio,
   porque las palabras siguientes de la persona (videollamada) no se alinearon; y yo cortaba según la alineación.
   Corrección en reel_franjas.py: avisa «palabra sospechosa» (> 1,2 s) y recorta por ENERGÍA real el silencio de
   inicio/fin de un trozo SOLO cuando su primera/última palabra dura > 1 s (estirada). Recortar por energía en todos los
   trozos se comió «que con el tiempo» (Allan habla muy flojito a veces): no hacerlo. Umbral adaptativo (3× ruido de
   fondo o 25 % del pico) y voz = ≥ 60 ms seguidos (un chasquido no cuenta). Revisar SIEMPRE el final del reel a oído/energía.
10. Solapamientos (Allan dice «¿vale?» mientras la persona empieza a hablar): Whisper los marca como resto, pero en el
   reel no se perciben; no forzar cortes ahí.

11. **Desfase acumulado de 1–3 fotogramas (desaparecidos, 2026-10-06; lo pillé con medir_sync antes de entregar).**
   Causa: el instante de corte se pasaba redondeado a 4 decimales; si redondeaba POR ENCIMA del fotograma
   (595.4667 > 595.46666…) ffmpeg descartaba ese fotograma y la imagen empezaba 1 fotograma tarde en ese trozo, y se
   sumaba. Corrección en reel_franjas.py: corte 1 ms antes, -frames:v exacto, setpts=PTS-STARTPTS + tpad, y
   comprobación automática de fotogramas por trozo («¡¡AVISO SINCRONÍA!!»). Además, en overlays la capa PRINCIPAL debe
   ser siempre el vídeo (si es una imagen en bucle, la imagen se reajusta a su ritmo).
12. **Palabra duplicada fantasma:** Whisper escribió «su abuelo, abuelo» y solo había uno; la alineación repartió la
   palabra entre los dos índices (el primero con puntuación 0,0) y yo corté a mitad de palabra. Si hay una palabra
   repetida y una puntúa ~0, coger el tramo completo hasta la segunda.
13. La pasada larga de comprobar_reel.py (con prompt de muletillas) se inventa «pues»/«¿no?» que no están: confirmar
   SIEMPRE en clip corto con oir.py antes de tocar nada. Para muletillas reales: «hueco_antes» o «fin_max» (nuevo:
   límite al final de una palabra, p. ej. «alemanes, ¿no?»).
14. Ráfagas: reel_franjas.py ya las reduce solo (une pausas ≤ 1,2 s); si persisten, son saltos de contenido o pausas
   largas a mitad de frase -> quitar la frase de relleno que las provoca (mejor que dejar silencios largos).

15. **Subtítulo larguísimo e ilegible (desap_04, segundo ~10, feedback del usuario: «no puede pasar»).** Si el texto no
   tenía las mismas palabras que el tramo de audio (añadí la «a» de «a ver»), la herramienta no partía la línea y
   ENCOGÍA la letra (19 palabras a 38 px). Corrección: nunca se encoge; se parte siempre (tiempo proporcional si no
   coinciden), máx. 6 palabras / ~760 px por subtítulo, y comprobación dura antes de renderizar (para con
   «¡¡ERROR SUBTÍTULO!!»). Además 95 de 376 subtítulos eran de 7–9 palabras a todo el ancho: demasiado largos.
   Al escribir guiones, partir a mano las unidades que no deben separarse («en redes / sociales»).

16. **Banners/rótulos en el original** (guías, 2026-10-07): el vídeo traía un banner «RESERVA TU CITA AHORA» + QR en
   430-440 s y 749-758 s que caería dentro del recorte. Detectarlos antes (zona clara en la parte baja) y no usar esos tramos.
17. «fin_max» ahora fuerza corte tras la palabra (antes, si la siguiente iba pegada, quedaban en el mismo trozo y el
   «¿no?» seguía sonando).
18. Buena práctica que funcionó: escribir los subtítulos YA partidos a mano en frases naturales de <= 6 palabras
   (no dejarlo al troceado automático) y repasar máx. palabras/ancho de todos antes de entregar.

19. **Cortes mal colocados y nada fluidos (guías, feedback 2026-10-07: «cortas la palabra, otras no acaba y la
   cortas, otras demasiado silencio, no está optimizado»).** Causas: (a) cortaba con margen fijo sobre la alineación,
   que da por acabadas las palabras antes de su cola y FALLA en las palabras descartadas vecinas (muletillas,
   tartamudeos); (b) la regla anti-ráfagas conservaba pausas de hasta 1,2 s; (c) la «s» suave contaba como silencio.
   Corrección en reel_franjas.py (refinar_bordes): cada corte se coloca en el hueco de silencio REAL (>= 40 ms, energía
   total Y aguda bajo umbral) más cercano a la frontera entre palabras; respiración 0,13 s al final / 0,10 s al inicio
   que NUNCA llega a la voz vecina; si no hay hueco, valle de energía. MAX_PAUSA 0,55 s y anti-ráfagas solo hasta 0,8 s.
   Si no hay silencio entre dos palabras (habla continua), NO cortar ahí: empezar/acabar la frase donde sí lo hay
   («Y en mi caso funcionó así, que lo mejor…», «Es que confiar…», «Por ejemplo, a mí…»).
   Verificación nueva: herramientas/revisar_por_tramos.py (Whisper por tramos de ~6 s, fiable) + ver_corte.py
   (contexto y energía de un corte) + medir silencios > 0,5 s en el reel final.
20. **Congruencia del mensaje (mismo feedback):** quitar redundancias («Realmente no somos humanos, realmente somos
   almas» -> «…humanos, somos almas…») y conservar los conectores que dan contexto («Es muy normal el no entender…»,
   «Entonces, se nos olvida…», «Porque yo creo que…», «Si queremos comunicarnos, lo primero…»). Leer cada guion de
   corrido como lo oirá alguien sin contexto antes de montar.

21. **Tercera queja de cortes (2026-10-07): «existente»→«exist», «corto»→«cort», empalmes bruscos.** Ver
   [[cortes-palabras-obligatorio]]: regla dura de no cortar antes del final alineado (las oclusivas hacen silencios
   internos), ajustes medidos escuchando (buscar_inicio/buscar_fin), ini_fijo para muletillas pegadas, anti-ráfagas que
   no deshace cortes manuales, fundido 25 ms, y protocolo de escucha de TODOS los empalmes antes de entregar.

**Why:** son errores que ya le costaron revisiones al usuario.
**How to apply:** antes de entregar: medir_sync.py (todo 0), comprobar_reel.py, y revisar avisos de ráfaga y la lista
de cortes. Ver [[estilo-reel-franjas-azules]] y [[proceso-reels-allan]].
