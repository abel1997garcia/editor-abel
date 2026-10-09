---
name: fotos-vida-abel
description: "Abel's life timeline (from his 58-min «Mi Historia») + his real photos/videos in MarcaPersonal/FOTOS MIAS by era — read before using any photo or telling his story"
metadata:
  node_type: memory
  type: project
  originSessionId: 3d4589e7-425f-4ade-ad39-5d4a51f78758
  modified: 2026-10-08T16:12:18.837Z
---

**Dónde:** `ABEL GARCIA/Editor vídeos/MarcaPersonal/FOTOS MIAS/`. El detalle de cada archivo está en `catalogo.json`:
- `que_es` = contexto exacto.
- `reels` = si se puede usar en reels.
- `original` = de dónde salió (las de «Mi Historia.mp4 @ m:ss» son capturas de calidad baja-media).

La transcripción con tiempos está en `VideosLargos/mi-historia/historia_texto.txt`.

**Por qué (Abel):** «una cosa es que yo diga algo y puedan pensar que me lo invento, y otra que se vea que ocurrió». Cuando cuenta algo de su vida, poner la foto o el vídeo real de ESA época. Abel me paró por mezclar épocas: **nunca usar una foto de una época para otra.**

**Vídeos:**
- Siempre sin sonido.
- Solo las escenas más explicativas.
- Los de móvil, en vertical.
- Las grabaciones de sus vlogs de YouTube son horizontales: se recortan.

**Clips sacados de sus vídeos (Abel, 09/10/2026):** a veces, sobre todo al FINAL, vuelve a salir él hablando en el plano del vídeo largo, o se cuela el principio de otra escena. Al extraerlos y al usarlos:
- detectar los cambios de escena y quedarse solo con **la parte más válida, el «estribillo»** de la escena;
- que el corte quede limpio, sin fotogramas de su plano ni de la escena siguiente.

El 09/10 ya se recortaron así los 12 clips de «Mi Historia» que lo tenían.

`12-familia-no-reels` y lo marcado `reels:false` (otras personas, su madre, la primera novia, el médium) NO van en reels.

**Cómo elegir la imagen de cada frase** (Abel, 08/10/2026):
1. Primero la época de lo que dice. Nunca una foto de otra época.
2. Dentro de esa época, la que más refuerce el sentido emocional de la frase, llevada al extremo. Si dice que estaba mal o no estaba preparado, no vale una foto neutra de viaje; vale la que más lo muestre, o el contraste «aparentemente feliz» (como el cumpleaños 26).
3. Lo que no llegó a pasar (p. ej. «me lo hubiese gastado en fiesta») va solo con gráficos.
4. Vídeos dentro del F3: `clip(nom, n, t0, t1, o)` en las escenas + `"clips": {nom: [ruta, ini, fin]}` en el reels.json. Se convierten a JPG a 30 fps, sin sonido; ejemplo en `travesia/c05t.js`.

## Línea de tiempo (de «Mi Historia», 2026)
1. **Infancia en León (Boñar, pueblo de 1.500 hab.).**
   - Nació en 1997 en León. Sus padres se separaron cuando él tenía 5 años y vivía con su madre, con cuidadoras.
   - Ya de niño le obsesionaba entender la mente y la autoestima.
   - Se refugió en los videojuegos (Pokémon, FIFA): «su burbuja».
2. **Con unos 10 años, a Castelldans (Lleida).**
   - Se mudaron por el accidente de esquí de su madre, a casa de sus tíos.
   - Juicio de custodia: con 10 años tuvo que declarar ante el juez.
   - Bullying el primer año; bajaba andando a la escuela 30-40 min, con frío.
   - Sin amigos, sin la lengua, con la familia a 800 km.
   - Canal de YouTube **Packard Minecraft**: el primero que se tomó en serio y con el que ganó algo.
3. **Su abuelo paterno.** Estaban muy unidos: la moto roja, pescar, castañas, el almacén. Murió cuando Abel estaba en 5.º-6.º de primaria, y él cargó con la culpa durante años.
4. **ESO.**
   - Call of Duty y mucha rabia; a punto de repetir 2.º.
   - El examen de inglés aprobado con un 5,15 «manifestado».
   - Fútbol (Borges Blanques): muy autoexigente y tóxico con el equipo; lo dejó.
5. **Primera novia:** canalizaba mensajes de su abuelo, y eso le quitó la culpa y abrió su búsqueda de «algo más».
6. **Fiestas y adicciones (≈16-22).**
   - Segunda relación, tóxica.
   - Cambió los videojuegos por la fiesta: alcohol, apuestas (perdió 2.100 € en un día; apostaba al ping-pong a las 3 de la mañana) y tragaperras.
   - Veranos en los pueblos de León, de miércoles a domingo de fiesta. Después, las fiestas de Castelldans y Borges.
   - Camarero los fines de semana desde los 16; monitor de tiempo libre en verano. Se gastó en fiesta el dinero del carnet.
   - En la universidad tonteó con sustancias, pero paró a tiempo.
   - Con 20-21 años, psicólogos («vaya puta mierda»). Luego terapias del inconsciente (Federica), EMDR y Gestalt.
7. **ADE 2015-2019 y el máster de 8.000 € («no me sirvió»).**
   - Primer trabajo en una oficina enorme: 2 meses de vacío, hasta la **pandemia de 2020**.
   - Canal **Clap** (Clash Royale): un vídeo al día, 30.000 suscriptores y solo ≈200 €/mes. Lo dejó para otro trabajo.
8. **Primer fondo, con unos 20 años: a punto de quitarse la vida.**
   - Se gastaba todo el dinero en fiesta y estaba hecho una mierda; el ir y volver entre León y Castelldans le reabría la herida.
   - No se lo dijo a nadie. NO hay foto de esto.
9. **Época del dinero (≈2021-2022).**
   - Antes se formó: curso Crece Tube de Romuald Fons (700 €) y la presentación de su libro.
   - Canal de **automatización**: más de 5 cifras al mes (17.000 €/mes en el Mundial de Qatar 2022).
   - Se hizo autónomo y montó una empresa. Placa de los 100K.
   - Rechazó 550.000 € por el canal.
   - Relación muy importante, gimnasio, viajes.
   - Tenía **≈25 años** (confirmado por Abel; en «la travesía» dice «21», pero es un lapsus: en los reels decir «con 25» o no decir edad).
   - Viajes de esta época: La Roca, Tenerife, Menorca, Budapest, el estadio.
10. **La caída y su NOCHE OSCURA DEL ALMA (cumpleaños 26, 2023)** — para él, el punto de verdad en que tomó conciencia de que tenía que cambiar.
    - Pompeya: estando a punto de arruinarse, unos 4 meses después de dejarlo con su última pareja.
    - Le cancelaron todas las cuentas de YouTube: de más de 5 cifras al mes a cero, y a deber más de 3.500 € a Hacienda.
    - Rompió con su pareja.
    - **Cumpleaños número 26:** la foto en casa (en `06-primer-fondo`) se la hizo su madre después de hora y media llorando.
    - Empezó a leer como un loco y a entrar en la espiritualidad («todo es energía»), además de una tarotista.
11. **Australia (Brisbane, algo más de un año).**
    - Pidió dinero a su madre para irse (luego se lo devolvió). Se fue solo y sin inglés.
    - Hostal de 6 personas. Al tercer día ya trabajaba: 100 palés de cajas de 30 kg.
    - La primera semana fue a sacarse el carnet de carretilla elevadora («toro») para trabajar. Sin coche, le pilló la lluvia y se tapó con los apuntes en su funda de plástico (vídeo).
    - Trabajos:
      - teles de 70-80 kg
      - repartidor
      - jardinero
      - obrero
      - cafés y cócteles
      - Uber
    - Su **primera casa tras el hostal**: seis meses con un compañero australiano espiritual. Vídeos de la cocina, del dormitorio y de su habitación con persiana de madera; ahí hablaba a cámara para YouTube y ahí grabó, con camisa blanca y corbata, al volver de su **primer día de camarero en el Brisbane Racing Club**.
    - La moto de 50 cc que perdía aire: feliz como un niño bajo la lluvia en un semáforo.
    - Gimnasio, meditación; constelaciones, Reiki, regresiones, reflexología.
    - Los últimos 3-4 meses trabajó 70 h/semana en dos bares y hacía Uber (Uber Eats, según él) con coches alquilados. Se fue con ≈3.000 €.
12. **Sudeste asiático, mes y medio solo:** Tailandia, Bali, Vietnam, Malasia, Camboya, y Turquía al final.
13. **Vuelta a España por sorpresa.**
    - Su madre creía que se iba a Nueva Zelanda.
    - Choque: él ya no bebe ni sale, y «todo seguía igual».
    - Luego se fue a vivir a **Lérida**, donde vive y graba.
    - Canal **El Viaje de Abel**: pizarra pequeña con el móvil, reacciones a experiencias cercanas a la muerte.
    - Sesiones con el médium **Allan** para hablar con su abuelo (las patatas escondidas en el almacén). Su madre habló con sus padres.
    - Club Unidad.
    - **Segundo fondo** (foto del espejo), en Lérida, en el piso donde se independizó al volver. Después, la sesión con psilocibina en la que sintió que sanaba (foto llorando). No salen en «Mi Historia».

Edades: 20 años ≈2017 · ADE 2015-2019 · pandemia 2020 (23) · dinero 2022 (≈25) · noche oscura 2023 (26) · Australia 2023-24 · Lérida después.

## Índice «cuando hable de… → usar»
- **Niño, infancia, separación, videojuegos como burbuja** → `01-infancia/`:
  - vídeos `video_nino_jugando_consola_sofa`, `video_nino_consola_primer_plano`
  - fotos de niño, primera comunión (sin reels), equipo de fútbol de niño
- **Su abuelo** → `01-infancia/`:
  - bebé con el abuelo
  - castañas con el abuelo
  - abuelo en blanco y negro
  - **bebé en la moto roja del abuelo**
  - `taller_casa_abuela` = el almacén del abuelo
- **Adolescencia, ESO, rabia, fútbol y autoexigencia** → `01b-adolescencia/`.
- **Su primer canal de niño** → `01c-canal-packard-minecraft/` (vídeo de la página y de una partida).
- **Fiesta, alcohol, adicciones, antes de despertar** → `02-antes-de-despertar/`:
  - capa rosa, micrófono, cabina, fuego de las fiestas de pueblo, selfie rosa
  - retrato en blanco y negro con 20 años
  - **graduación de ADE 2015-2019** (foto y vídeo)
  - **la oficina** del primer trabajo
- **Gael Blog (canal borrado, ≈2017)** → `03-canal-gael-blog/`. NO es la época del dinero.
- **Canal Clap (pandemia, 30K, ≈200 €)** → `04-canal-clap/`:
  - vídeos de la página y de él grabando Clash Royale con cascos
  - captura «no generaba ni 100 €»
  - publicación de PcComponentes
  - funda de móvil de su propio merchandising de Clap (la creó él, no la ganó)
- **Formarse y ganar mucho dinero** → `05-canal-automatizacion-ganaba-dinero/`:
  - presentación del libro de Romuald Fons (ANTES de ganar)
  - placa 100K
  - La Roca Village, Tenerife, Menorca, Budapest, estadio
  - Finlandia, viaje regalado a su madre y su padrastro (sin reels)
- **Lo perdió todo / noche oscura del alma / cumpleaños 26** → `06-noche-oscura-26-anos/` (foto en casa del cumpleaños; Pompeya, a punto de arruinarse). El primer fondo (≈20 años) no tiene foto.
- **Trabajos** → `_por-tema/trabajos/` (copias). Monitor de Navidad → `07-trabajo-monitor/`: foto suya y con los compañeros en Agustí Mestre (decir solo que trabajaba allí).
- **Irse a Australia y su vida allí** → `08-australia/`:
  - aeropuerto de Barcelona al irse
  - miniatura «+17.000 km»
  - hostal de 6 personas
  - obrero, teles, almacén, cafetería, cócteles, Racing Club, barra llena
  - moto (foto, miniatura «Tu Plan Superior», vídeo de noche)
  - leyendo con la sudadera azul
  - gimnasio
  - dos bares 70 h
  - dos coches de Uber
  - llorando en su «vídeo emocional»
  - del montaje «Así vivía a 17.000 km de casa…» (original en `VideosLargos/mi-historia/australia_montaje/`): la lluvia con los apuntes (carnet de carretilla, 1.ª semana), la primera casa (cocina, dormitorio, habitación), la cafetería que llevaba solo, el coche de Uber Eats, el bar de la camiseta negra y el primer día del Racing Club
- **Viaje solo por Asia** → `09-sudeste-asiatico/`: Batu, Ha Long, mochila, ascensor, vídeo de Turquía con las mochilas.
- **Segundo fondo y sanación (Lérida, tras Australia)** → `10-segundo-fondo-y-sanacion/` (espejo, llorando en la sesión con psilocibina; miniatura del médium, sin reels).
- **Ahora, Lérida, su canal** → `11-ahora/`: gimnasio, pizarra, vídeo de su piso de Lérida, scroll de sus vídeos de pizarra.
- **Familia** → `12-familia-no-reels/`: nunca en reels. Incluye la vuelta por sorpresa y a la primera novia.
