# CHECKLIST de cada reel de Allan (obligatoria, en este ORDEN)

Abel 17/10/2026: «el orden es importante… empezar por la voz para tardar menos y, una vez la voz limpia, generar el
vídeo». Se marca cada punto; si uno falla se vuelve atrás, nunca se sigue «para arreglarlo luego».

## A. Mensaje (antes de tocar nada)
- [ ] El reel habla al AVATAR de Allan: personas que quieren una **sesión con un médium** (contactar con un ser querido
      fallecido, entender señales, duelo) o **acompañamiento espiritual** (despertar, soledad, propósito, energía).
      Pregunta de control: «¿alguien así se siente identificado y le dan ganas de pedir una sesión?». Si no, otro tramo.
- [ ] **De tú a tú:** elegir tramos donde Allan habla a UNA persona («tú», «te», «coge tus heridas», «si te
      pasa…»). Evitar «os/vosotros» («os aseguro», «imaginaos») y, si el tramo va en «nosotros», que al menos el
      gancho y el cierre vayan en tú.
- [ ] **Una idea = un reel** (regla de Abel): nada de juntar dos temas (p. ej. soledad + «las personas que pasan
      por nuestra vida»). Cada frase del guion tiene que servir a ESA idea; si no, fuera.
- [ ] Una sola idea por reel, con autoridad de Allan (lo que ve en sus sesiones, su experiencia) y un cierre que
      deje la puerta abierta a las sesiones.
- [ ] Gancho = primera frase, impacta en 2–3 s (advertencia, experiencia fuerte, verdad rotunda, pregunta que se hace
      el avatar). Nada descriptivo que tarde en arrancar.
- [ ] Guion leído de corrido: congruente, con conectores, sin redundancias ni frases repetidas.
- [ ] 50–90 s (franja negra ≈ 1 min).

## B. VOZ PRIMERO (sin vídeo)
1. [ ] `python herramientas/reel_franjas.py trabajo/specs/<n>.json --voz`  → `trabajo/reels/<n>/voz.wav` (segundos).
2. [ ] **Arranque sin silencio:** la voz empieza YA con la frase (≤ 0,10 s de aire al principio). Lo mide
       `onda.py` (hueco inicial) — si hay aire, `ini_fijo` en la primera palabra.
3. [ ] `python herramientas/espectro_cortes.py <n>` → mirar `espectro_cortes.png` y `espectro_voz.png`:
       palabra pegada a la línea cian (cortada), «eh»/«mmm» (franja lisa sin consonantes), respiraciones,
       chasquidos, ruido o audio que se oye mal.
3b. [ ] `python herramientas/voz_sin_palabra.py <n>` → sonido con voz FUERA de las palabras del guion (Whisper NO
       escribe los «eh»). Escuchar en el original (prompt de muletillas) TODO tramo >= 0,2 s, aunque sea flojo
       (−30 dB): sobre todo los de «entre INICIO y …» (muletilla delante de la primera palabra del trozo) y las
       vocales estiradas («yyy», «queee», «mismaaa»). Las colas que se apagan poco a poco son respiración: se quedan.
4. [ ] `python herramientas/oir_empalmes.py --voz <n>` → TODOS los empalmes: ninguna palabra cortada
       («exist», «cort»), ninguna muletilla («eh», «pues», «¿no?», «o sea», «y» suelto), ninguna equivocación o
       repetición («siempre, siempre»).
5. [ ] `PYTHONIOENCODING=utf-8 python herramientas/onda.py --hueco 0.55 --final 0.4 trabajo/reels/<n>/voz.wav`
       → sin huecos rojos (ritmo de Allan: pausado pero dinámico; ninguna pausa > 0,55 s salvo pausa dramática justificada).
6. [ ] `python herramientas/oir_voz_entera.py <n>`: la voz ENTERA en ventanas que empiezan y acaban en empalmes,
       con prompt de muletillas, comparada con el guion. Aquí salen las repeticiones («me quedo… me quedo»),
       tartamudeos («Pa… ¿para qué?»), autocorrecciones («parezcan, sean») y frases de más que Whisper OMITIÓ en la
       transcripción larga. Cada «!!» o diferencia se confirma en el ORIGINAL (Whisper inventa al principio de un
       archivo y al final de una ventana). `voz_sin_palabra.py <n> --oir` escucha cada sospechoso solo.
7. [ ] Si algo falla: medir en el ORIGINAL con ENERGÍA cada 10 ms (y agudos > 3 kHz para no comerse una «s»);
       `buscar_inicio.py` / `buscar_fin.py` fallan cuando hay un «eh» (Whisper no lo oye y da tiempos a > 1 s); ajustar
       `trabajo/<video>/ajustes_tiempos.json` (`ini_fijo`, `fin_fijo` = final medido de palabra alargada, `fin_max`,
       `hueco_antes`; un fin_max NUNCA antes del final de la palabra: ojo al silencio de p/t/c dentro de ella;
       `ini_fijo` ≈ arranque medido − 0,07 porque el montador suma 0,03 y redondea al fotograma siguiente) o cambiar el guion, y volver a 1.

## C. Vídeo (solo con la voz limpia)
8.  [ ] Render normal (sin `--voz`).
9.  [ ] `medir_sync.py` (IMAGEN: todos los trozos a 0 fotogramas) **y** `medir_sync_audio.py reels/<n>.mp4`
        (AUDIO: todos los trozos ~+1 ms). Audio y vídeo sincronizados: LO PRIMORDIAL. El render usa como audio la
        voz aprobada (voz.wav), así que lo que se oye es exactamente lo revisado en B.
9b. [ ] `python herramientas/comprobar_subtitulos.py <n>` → subtítulos cuadrados con la voz (entran con su primera
        palabra, sin huecos ni solapes, ≤ 6 palabras).
10. [ ] `onda.py` sobre el mp4 y mirar la imagen; final sin silencio (≤ 0,4 s).
11. [ ] Subtítulos ≤ 6 palabras, sin encoger; título sin palabra débil al final de línea; sin banners del original.

## D. Entrega
12. [ ] `reels/<n>.txt` (descripción Instagram: gancho = UNA frase corta 5-9 palabras, cruda, a la fibra, entre comillas 👇, conexión 🤍, «Y quizá te digas que…»,
        pregunta, `👉 Si quieres información sobre las sesiones, comenta "INFO".`).
13. [ ] En `reels/` SOLO quedan `<n>.mp4` y `<n>.txt` (nada de ondas, voces ni copias: todo eso en `trabajo/`).
14. [ ] Tabla de entrega: reel, título, gancho, duración, y qué se corrigió.
