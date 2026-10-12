---
name: reels-abel
description: Sacar reels de Abel de un vídeo horizontal (F1 sin animaciones, F2 o F3) con el listón de calidad que exige. Úsala siempre que haya que hacer, rehacer o revisar reels (publicar o trial).
---

# Reels de Abel desde un horizontal

**Formatos (Abel 12/10/2026):**
- F1 sin animaciones: siempre él; si el horizontal es antiguo con pizarra, `fuente` = su `toma_limpia.mov`.
- F2 y F3: herramienta `reel_tablero.py`; formatos en la memoria `reels-marca-personal`.
- Nunca animaciones de pizarra en un reel: «no se entiende el concepto y no salgo yo».

Nada se entrega si no pasa el LISTÓN. «No se trata de subir por subir» (Abel, 12/10/2026). Modelo de ritmo y títulos: Lavri (`Referencias/lavri/ANALISIS.md`, apartado reels).

**Por norma, de cada vídeo salen unos 10 reels: 6–7 de PUBLICAR y SIEMPRE 3 TRIALS** (Abel 12/10/2026). Los trials llevan estructuras distintas de las de publicar, para poder salir ya.

## 1. Ganchos y estructuras (antes de tocar ninguna herramienta)
- Hacer el banco: 20 o más ganchos (primero los que hablan directamente a la persona) y estructuras colleja → solución de una idea, en `VideosLargos/<tema>/reels_banco.md`.
- Un gancho solo vale si:
  - es una frase COMPLETA, que arranca tras una pausa y acaba con tono de cierre (nunca la mitad de una lista, nunca la cola de otra frase);
  - se entiende sola: sin «eso», «esto» o «con eso» sin referente. Si lo lleva, se coge también la frase de antes («Los que más dinero hacen es una cosa específica… Cuando te haces bueno con eso, nunca te va a faltar negocio»);
  - no depende del vídeo del que sale: nada de «esto que te estoy explicando», «este vídeo» o «lo que te he comentado» (el gancho de «sin guiones» falló por eso, 12/10/2026);
  - habla de la persona y de lo que le duele, no de Abel; toca un dolor o rompe una creencia, y pasa el test de la memoria `ganchos`.
- **Reels personales (12/10/2026):** de cada vídeo, uno o dos pueden ir de sus miedos o su historia para que le conozcan. Llevan la misma estructura (gancho → lo que le pasaba → lo que aprendió) y el mismo listón. El título va en primera persona y con connotación negativa («Me daba pánico enseñarme… y por eso no vendía:»). Siempre acaban en algo que sirva a quien emprende (memoria `criterios-contenido-util`).
- El cuerpo no repite el gancho.
- **Cada reel tiene algo ÚNICO (Abel 12/10/2026: «aunque cambiemos el gancho, la mayoría del vídeo es el mismo; el mismo día se nota»).** Lo preferible es que el trial lleve OTRA estructura y OTRO gancho del mismo vídeo; para eso el banco tiene que ser grande (20 o más ganchos y todas las estructuras posibles). Si un reel comparte estructura o gancho con otro, vale, pero `programar_youtube.py` los separa al menos 45 días (código `e<N>-g<N>` en el nombre). Calendario: trial 3 al día como máximo (17, 19 y 21 h); publicar 7 al día (14, 16, 18, 20, 22, 23 y 24 h), con variedad (como mucho 2 del mismo vídeo al día) y sin dejar ninguno sin programar.
- 40–60 s.

## 2. Título (arriba)
- Da el contexto que el gancho no dice y SIEMPRE lleva connotación negativa: lo que la persona hace mal o lo que le está costando («Por esto sigues sin…», «Si haces esto, jamás…», «… te está dejando sin clientes»). Nunca un título neutro o descriptivo.
- 6–10 palabras en 2 líneas, a menudo acabado en dos puntos.
- **Antes de escribirlos, mirar el banco de títulos de Rebeca y Lavri** (`Referencias/lavri/ANALISIS.md`, al final; mejor los de franja negra): copiar la estructura y adaptarla al mensaje, nunca el título.
- **Estructuras VARIADAS en cada tanda** (Abel 12/10/2026: «casi todos empiezan por “Por esto”, queda demasiado IA»): como mucho UNO con «Por esto» por vídeo, y nunca dos títulos seguidos que empiecen igual. Ejemplos:
  - afirmación cruda: «Ver otro curso no te va a traer ni un cliente:»;
  - desmontar algo: «Ese bloqueo antes de publicar no es pereza, es miedo:»;
  - causa → consecuencia: «Tu negocio no avanza porque haces 80 cosas a la vez:»;
  - lista con giro: «Gimnasio, libros… y aun así tu marca no crece:»;
  - condicional: «Si persigues a tus clientes, jamás te van a comprar:»;
  - «Por esto…» (uno como mucho).
- Números solo si son reales. La palabra clave entre “comillas” (sale en cursiva). Una palabra en MAYÚSCULAS como mucho.
- Nunca repite el gancho.
- **🔴 PRUEBA OBLIGATORIA de cada título antes de renderizar** (Abel 12/10/2026: «JAMÁS puede volver a suceder»). Se lee el título SOLO, como si no hubiera reel, y se responde:
  1. ¿Dice lo que la persona hace MAL, o lo que le pasa por hacerlo mal? Si suena a consejo o a algo que hay que hacer, está MAL.
  2. ¿Defiende lo MISMO que el reel? Si el reel dice «no persigas», el título nunca puede sonar a «persigue».
  3. «Por esto + verbo» es trampa: «Por esto tienes que perseguir a tus clientes» se lee como una orden y dice lo contrario del reel. Mejor «Si haces X, jamás Y», o «Por esto + consecuencia negativa» («Por esto nadie te compra»).
  - Escribir en `plan.md`, junto a cada título, la respuesta a 1 y 2.

## 3. Config y voz
`MarcaPersonal/<tema>/reels_f1.json`:
- con horizontal estándar: `fuente` (el horizontal), `tiempos` (`<horizontal>.tiempos.json`) y `montaje` (`<horizontal>.montaje.json`);
- con pizarra (antiguo): `fuente` = `toma_limpia.mov` y los mismos `tiempos`, sin `montaje`.
- **Sin horizontal editado:** `fuente` = la grabación original y `tiempos` = su `toma_tiempos.json`. Es lo más fiable, porque los tiempos coinciden con el audio exacto.
- Los tramos se fijan con frases, no con índices a ojo: `herramientas/anclas.py` → `A(tiempos).T('primera frase', 'última frase')`. Contar índices a mano salía desplazado una o dos palabras.

**Zoom de énfasis (F1, siempre):** 2–4 frases clave por reel en `"enfasis"` (con `anclas.py`): el remate del gancho, la colleja y la solución. Nunca sobre la pantalla blanca; la herramienta ya lo evita.

Luego:
1. `python herramientas/reel_yapping.py reels_f1.json --texto` → leer el texto corrido de cada reel en voz alta.
2. `... --voz` → `out/_<reel>/voz.wav`. Los microsilencios (≥ 0,2 s) ya salen a ~0,13 s medidos sobre la voz real (`microcortes`), sin cortar palabras.

## 4. LISTÓN de audio (todo, en cada reel)
1. La línea `listón` de `--voz`: **≥ 3,3 palabras/s** y **ningún hueco > 0,35 s** salvo el final (Lavri: máx. ~0,3).
2. `python herramientas/verificar_audio.py out/_<reel> <tiempos>` para todos (`> verif.log`).
3. `python herramientas/oir_uniones.py verif.log out` vuelve a escuchar cada ✗ con 4 s de contexto:
   - si suena igual que la toma original (transcribir también la FUENTE en ese punto), es un falso aviso de Whisper. Si en la fuente está la palabra y en el reel no, el corte es MALO (c03: «tú imagínate» perdido);
   - si falta, sobra o se repite algo, se corrige (ampliar o mover el tramo, nunca retocar a mano los tiempos de las palabras) y se vuelve al punto 1.
   - Un ✗ NUNCA se da por bueno «porque el texto se lee bien».
4. Música por estilo: `herramientas/estilo_voz.py out/_<reel>/voz.wav --base <5 min de la toma>` → intensidad → tema de `MUSICA/catalogo.json` por su «caracter».

## 5. Render y LISTÓN de imagen
- `reel_yapping.py reels_f1.json` → hoja de 8 fotogramas por reel y mirarla.
- No puede haber:
  - palabras sueltas en pantalla;
  - un título que tape algo.

## 6. Entrega
- Copiar a `MarcaPersonal/REELS/«NNN · PUBLICAR|TRIAL · <vídeo> · e<N>-g<N> · <título>.mp4»` (una sola carpeta, sin semanas; NNN = el siguiente número libre = orden de subida; al programarse pasan a `REELS/programados/`), con su `.txt` del mismo nombre (título, descripción, hashtags). Un trial nunca va justo después de su reel de publicar.
- `MarcaPersonal/<tema>/plan.md`.
- Borrar `out_f1/`.
- Nada se programa sin su OK.
