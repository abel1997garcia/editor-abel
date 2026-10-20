---
name: reels-virales
description: Editar los brutos VERTICALES que graba Abel con el móvil (guiones virales, 5 ganchos por grabación = 5 variantes con su título y su música) hasta dejarlos en REELS como PUBLICAR o TRIAL, todos con el control de calidad pasado. Úsala siempre que Abel pase vídeos verticales en bruto.
---

# Reels virales (brutos verticales de Abel)

> **15/10/2026: el F4 viral queda APARCADO** (Abel: «no conecta, muy básico, mala recepción, no se entiende»). Los guiones virales los graba con la TABLET en vertical, escribiendo lo que explica, y se editan en **formato yapping F1** (plantilla blanca, título arriba, subtítulos). Del proceso de abajo sigue valiendo TODO lo de audio y cortes (guion del Drive, islas, `revisar_cortes`, escucha entera, gancho aparte con prompt LITERAL, comprobar el MP4 final, títulos de `titulos-negativos` hablándole al cliente); lo de imagen F4 (subtítulos arriba, fotos cuadradas) ya no aplica.

> **PROCESO RÁPIDO (15/10/2026, el que se usa): `herramientas/rapido/` — islas.py → elegir.py (con guion.txt del Drive) → montar.py (solo audio + verificación única) → render.py (ffmpeg, una pasada, sin zoom). Ver memoria `proceso-rapido-islas`. El montaje viejo con reel_tablero.py ya no se usa para estos vídeos.**

> **Formato TAB (15/10/2026, primer reel 076):** `"formato": "TAB"` en reels.json (`tablero/motor_tab.html`): la grabación ya trae la plantilla blanca con la franja (se detecta sola). Título negro arriba de la franja todo el reel; subtítulos blancos de ≤ 3 palabras CENTRADOS en la zona libre de la derecha; abajo en blanco; sin emojis; foto suya 1:1 a la derecha solo si cuenta su historia (`imagen()` en escenas.js); zoom suave solo dentro de la franja. **LISTAS: `"lista": true`** → subtítulos abajo en la parte blanca y la derecha VACÍA (ahí va la tablet); los guiones TABLET llevan 5 hooks, como los demás (desde el 19/10/2026).

Abel 14/10/2026: «cuando yo te pase todos los vídeos que sean verticales, ya como brutos, tú ya sabes lo que tienes que hacer». Objetivo: **una grabación con sus 5 variantes en ~20 min**. Tardar 2 h en 9 reels fue inaceptable: el tiempo va al criterio, no a la máquina.

Antes de nada: memoria `edicion-reels-obligatoria` (ritmo, velocidad normal 1,0x, onda, cortar toda trabazón) y `ganchos` / `referencias-virales` para el contenido.

## Reglas fijas
- **IMAGEN 100 % CON LO QUE SE DICE (Abel 18/10/2026):** antes de poner cualquier imagen (F2 abajo, F4, carruseles, miniaturas), `python herramientas/relacionar_imagenes.py <guion o frase>` propone candidatas de la biblioteca (`EDICION VIDEOS/IMAGENES`) y de FOTOS MIAS; cada una se MIRA junto a su frase y solo entra si da más contexto a lo que se explica (habla de su canal → foto de su canal). Si ninguna encaja, sin imagen. Las imágenes en inglés de un viral se traducen y entran en la biblioteca (`IMAGENES/LEEME.md`).
- **PUBLICAR o TRIAL (un solo saco, Abel 19/10/2026): TODOS pasan el CONTROL DE CALIDAD de la skill `reels-abel`; el reparto, el de esa skill**: `MarcaPersonal/REELS/«NNN · TRIAL|PUBLICAR · <vídeo> · e1-g<N> · <título>.mp4»` + `.txt` (1.ª línea título de Instagram distinto según `titulos-negativos`, complementario y nunca igual a la de pantalla; descripción; `#abelunidad #autoestima #crecimientopersonal`). La DESCRIPCIÓN es el guion entero (readaptado un poco para leerse) + hashtags (Abel 18/10/2026). **SIN CTA** en los virales (Abel 18/10/2026): el CTA «UNIDAD» va solo en contenido de consolidación y venta.
- **Formato único F4 viral** (`"estilo": "viral"`, `"formato": "F4"`, `"imagenes": "img"`, `"escenas": "rN_F4.js"`; Abel 14/10/2026). **Nada de F3 ni F5** con fuente vertical. Él a pantalla completa con hueco arriba:
  - **subtítulos ARRIBA** (y≈360), en la pared: negro con sombra muy suave; la palabra clave SOLO en azul eléctrico claro (#2E8BFF). Si el fondo de arriba no es claro (graba en la calle) la herramienta lo detecta (`FONDO_CLARO`) y los pone en blanco con sombra;
  - **título abajo** (y≈1430), caja negra con letra blanca, todo el reel (se aparta cuando sale una foto). Según la memoria `titulos-negativos`; tiene que verse junto a él en la vista previa de Instagram (franja 3:4, y 240–1680);
  - **fotos CUADRADAS y pequeñas (430 px, y≈1500)**: nunca le tapan la cara; él bien encuadrado y centrado (`pos`/`size` con su cara localizada; las fotos de base son las de FOTOS MIAS / carruseles SIN texto). Solo si dan contexto exacto a la frase.
- **Una variante por gancho (Abel 19/10/2026)**: 5 ganchos → 5 reels con el mismo cuerpo (se monta UNA vez); cada uno con SU título de pantalla (distinto, según `titulos-negativos`) y SU música de fondo distinta. El que gane se apunta en `ganchos`.
- **Fotos: SOLO de Abel y con el contexto EXACTO de la frase** (`MarcaPersonal/FOTOS MIAS/catalogo.json`, memoria `fotos-vida-abel`), ≥ 600 px. Si no hay foto exacta, no se fuerza: el reel va solo con subtítulos y al entregar se le dice qué fotos faltan.
- Velocidad NORMAL 1,0x (Abel 19/10/2026; `"velocidad"` en plan.json). Ritmo, música (`MUSICA_DB` = −11,5 dB bajo la voz) y onda: los de `reel_tablero.py`, igual que en todos los reels.

## Orden (una sola pasada; el render, al final y una vez)
0. **El GUION de referencia Y SU FORMATO** (Abel 19/10/2026: el archivo del escritorio NO lleva el prefijo): el vídeo se llama igual que su guion del Drive, que está en PARA GRABAR/REELS o, ya grabado, en **GRABADOS** (id 11T484Y_Ey8ltifaQZPHeFayg2YvgbeG1). El prefijo del guion decide el formato: «TABLET · », «HISTORIA · » o nada (normal). Si sale Fulano/Mengano, es HISTORIA. Buscarlo (`search_files` por título) y leerlo: hooks + guion. Es la guía para elegir tramos y el título; al final, lo que se oye en el reel tiene que seguir el guion en orden y sin repetir nada.
1. Carpeta `MarcaPersonal/virales/v<nº>/` con `fuente.mp4` → `python herramientas/casual_prep.py <carpeta>`: voz limpia (`_fuente_limpia.wav`, la que se monta en TODOS los reels) y transcripción que conserva trabazones.
2. `reels.json`: `"velocidad": 1.10` (Abel 14/10/2026: cortos = ya dinámicos; la velocidad se aplica al final del montaje, los cortes se deciden a 1x). Tramos leyendo la lista palabra a palabra: de cada repetición, la ÚLTIMA toma completa.
3. `reel_tablero.py reels.json --voz` → corta por ISLAS DE VOZ de la onda (`igualar`): islas enteras, ~0,06 s de aire, cortes en fotogramas exactos; las respiraciones (islas sin palabra) fuera; las «s» del principio y del final protegidas por sus agudos; aire 0,06 s dentro de la frase y 0,10 s al acabar una frase («publicas. Yo» sonaba cortado). La voz que SE OYE es `_voz_suave.wav` (DeepFilterNet suave, −15 dB; la fuerte sonaba «rara» y el expansor se comía las «s»; NUNCA expansor), a −14 LUFS. Los subtítulos se sincronizan solos escuchando la voz montada (`pal_oido.json`), primera palabra en mayúscula. `"mejorar": true` en reels.json (contraste y nitidez).
4. **`python herramientas/revisar_cortes.py reels.json` = LA ESCUCHA, OBLIGATORIA EN TODOS** (Abel: «tiene que depender del audio»). Escucha el audio montado corte a corte: corte sobre voz, pegado, hueco, microcorte, principio/final con silencio y «se oye distinto» (palabra comida, trozo de otra toma). Cada ✗ se corrige como un editor y se repite 3-4 hasta que salga limpio:
   - trozo de otra toma colado / arranque en falso → `"fuera": [[ini, fin], ...]` (segundos de la grabación);
   - dos tomas sin pausa → `"cuchillas": [seg]` (en el valle de la onda);
   - corte en habla seguida que suena pegado → `"aire": [seg donde acaba el trozo]`;
   - frase que no se puede cortar sin notarse → se deja entera (quitar el "quitar").
   Lo que quede (pausa natural suya, diferencia del reconocedor lejos del corte) se le dice a Abel con el segundo exacto.
   **Y se escucha el reel ENTERO** (Whisper sobre `out/_<reel>/voz.wav`) y se compara con el guion: un gancho de más, una frase repetida o una que falta no lo ve la revisión de cortes (068: se colaba dos veces el gancho 3).
5. **Primero UN reel** completo (voz, escucha, render, fotogramas) y se le enseña a Abel; con su OK, los demás con el mismo criterio (Abel 14/10/2026: «primero hagamos un vídeo bien»).
6. Fotos por frase en `rN_F4.js`: `imagen('img/x.jpg', en('frase', desde) - .1, fin, { pos })`.
7. `reel_tablero.py reels.json` → los 10 a la vez.
8. `onda.py out/*.mp4` + hoja de fotogramas; pasar el control de calidad (todos) y copiar a REELS como PUBLICAR o TRIAL, y avisar. Nada se programa sin su OK.

## ✅ CHECKLIST FORMATO TAB (tablet / plantilla yapping) — SE SIGUE ENTERA, EN ORDEN, EN CADA VÍDEO (Abel 15/10/2026: «sigue la checklist de todos los pasos y así jamás te dejarás nada en el tintero»; 076: me salté el espectrograma, di por bueno un ✗ y se coló la cola de «vendados» en el 10,8 s)
**1 · Antes de cortar**
- [ ] Guion del Drive con el MISMO título que el vídeo (`search_files`), leído entero.
- [ ] ¿Es LISTA? («TABLET · », o lista / tier list / comparación) → `"lista": true` y su imagen de `LISTAS MIRO` revelándose punto a punto; «HISTORIA · » → pizarra; sin prefijo → subtítulos a la derecha (los tres: memoria `reels-virales-criterio`, «Edición de los 3 estilos»).
- [ ] `casual_prep.py` → transcripción con trabazones; revisar las PALABRAS SOSPECHOSAMENTE LARGAS (esconden pausas o tomas).
- [ ] Comparar lo que dice con el guion frase a frase: qué se salta, qué repite, qué dice a su manera (vale), qué tomas descartar. De cada repetición, la ÚLTIMA toma completa.
- [ ] reels.json: `"formato": "TAB"`, `"mejorar": "suave"` (nitidez leve, nunca el fuerte: le cambia la cara), `"velocidad": 1.0` (Abel 19/10/2026: normal), música, título de `titulos-negativos` hablándole al cliente.
**2 · Voz (`--voz`)** — 079 (Abel 15/10/2026, muy enfadado): silencios largos en 8, 33 y 42 s, corte malo antes de «Mi audiencia» y música cantada alta. TODO eso lo marcaban las herramientas y lo descarté. **NINGÚN ✗ SE DESCARTA CON EXCUSAS** («es la palabra apagándose», «el reconocedor lo oye bien»): el reconocedor RELLENA palabras cortadas; lo que manda es la ONDA.
- [ ] `--voz` ya aprieta solo cada unión (`apretar` + `afinar_con_onda`): la ONDA del reel montado tiene que dar **«✓ sin huecos > 0,10 s»** (también principio y final). Si no, no se sigue.
- [ ] Antes de elegir tramos: escuchar TODA la grabación por ventanas con el prompt LITERAL (las tomas repetidas se esconden dentro de palabras «largas»). Arranques pegados («audien… mi»): buscar otra toma o un «Mi» suelto y empalmar; nunca empezar un trozo sobre la cola de otra palabra.
- [ ] Al quitar algo con `fuera`, comprobar con la envolvente (10 ms) dónde acaba de verdad la palabra anterior: al quitar «y ya está» me comí «información» dos veces.
- [ ] `revisar_cortes.py`: CADA ✗ se mira con ESPECTROGRAMA de la grabación (`showspectrumpic` de 3-6 s alrededor) antes de decidir. Un «CORTE SOBRE VOZ» o un «MICROCORTE» NUNCA se da por bueno sin verlo: suele ser la cola de otra toma → `fuera`.
- [ ] Espectrograma de TODOS los cortes del reel montado: ningún trozo suelto, ninguna sílaba de otra toma, ninguna «s» comida.
- [ ] Muletillas («eh», «mmm», «o sea»), trabazones y arranques en falso: fuera.
- [ ] Silencios: mediana ≤ 0,06 s, ninguno > 0,10 s; principio sin silencio.
- [ ] Escucha entera (`escuchar.py`) contra el guion: mismo orden, nada repetido, nada que falte.
- [ ] Si cambio `fuera`/`cuchillas`/`aire`, vuelvo a pasar TODO el bloque 2.
- [ ] **CUANDO HAY UN ERROR: volver a la GRABACIÓN ORIGINAL** y medir ese punto desde cero (envolvente cada 10 ms + espectrograma de AGUDOS/formantes + escuchar cada trozo SUELTO); no parchear lo ya montado (Abel 15/10/2026: «estás intentando editar un vídeo ya editado y te vuelves loco»).
- [ ] **SILENCIO MÁXIMO = la pausa entre el gancho y el cuerpo** («…haz esto | Durante meses…»), ≈0,08 s; ninguna unión más larga ni pegada (`/tmp/gaps.py` o `afinar_con_onda` lo miden en el reel montado).
- [ ] Cada trozo pequeño (< 0,4 s) que se empalma, ESCUCHADO SOLO antes: si suena a otra cosa («Te da miedo» en vez de «Mi») es un resto de otra toma → fuera.
- [ ] Antes de quitar algo junto a una palabra acabada en «s», espectrograma de agudos: el siseo es de la palabra («mes» → la «s» de 44,86–45,04 no era una sílaba suelta).
- [ ] **Si cuenta algo de SU HISTORIA → foto suya de ese momento** (FOTOS MIAS, catálogo; 1:1 a la derecha con `imagen()` en el escenas.js y los subtítulos debajo). Siempre.

- [ ] **`python herramientas/cortes_oido.py <carpeta> 1.0 <reels> [--mp4]`: escuchar CADA CORTE POR SEPARADO (±1,3 s).** La escucha del vídeo entero RELLENA lo que falta: en el 082 decía «trabajar contigo, o no, si le hablas» y «mi mejor amigo, un… y que» (restos de tomas descartadas) y lo di por bueno. Cualquier palabra que no esté en el guion en esa ventana = resto → se mide en la grabación (trozos sueltos + envolvente) y se quita. NUNCA se da por buena una palabra rara («o no», «un…») sin comprobarla.

**3 · Render**
- [ ] ESPECTROGRAMA DEL REEL ENTERO con los cortes marcados (voz continua, sin huecos negros largos) + `onda.py` sobre el MP4 final: ✓.
- [ ] Música: si la canción es CANTADA (`"voz": true` en MUSICA/catalogo.json) va 6 dB más baja (la herramienta lo hace sola); nunca que distraiga.
- [ ] Hoja de fotogramas a resolución completa en las palabras LARGAS: ningún subtítulo se sale de la zona derecha («completamente»; se encogen solos hasta 400 px). 9:16 (1080×1920), sin franjas negras, título arriba entero, el zoom de la franja no le corta la cabeza ni deja blanco.
- [ ] Voz −14 LUFS (ebur128), música bajo la voz.
- [ ] **SUBTÍTULOS (082, Abel: «algunos subtítulos no están donde tocan, no se ven»):** (1) lista de BLOQUES contra el guion: no falta NINGUNA palabra (al quitar un microtrozo se perdían «mundo», «verdad», «de ti»), ningún bloque de una palabra corta suelta («el», «de», «es»), ninguno acaba en palabra corta; (2) hoja de la zona de subtítulos cada 0,4 s del MP4: todos opacos y legibles; (3) sincronía contra la voz del MP4: aparecen ≈0,1 s antes, nunca tarde.
- [ ] Escucha del MP4 ENTREGADO: entera (con y sin prompt LITERAL) Y corte a corte (`cortes_oido.py --mp4`). Solo entonces «está bien».

## ✅ CHECKLIST (068 aprobado por Abel 14/10/2026: «todo el vídeo está perfecto»). Se recorre ENTERA en cada reel; nada se entrega con una casilla sin marcar.
**Antes de cortar**
- [ ] Guion del Drive localizado y leído (mismo nombre que el vídeo): ganchos + guion.
- [ ] `casual_prep.py` hecho (voz limpia + transcripción que conserva trabazones); `.000` → `mil` en tiempos.json.
- [ ] reels.json: `"estilo": "viral"`, `"mejorar": true`, `"velocidad": 1.10`, F4, música.
- [ ] Tramos elegidos leyendo la lista palabra a palabra contra el guion: de cada repetición la ÚLTIMA toma completa; arranques en falso y tomas pegadas → `fuera`; nada que el guion no tenga dos veces.
**Voz montada (`--voz`)**
- [ ] **El GANCHO aparte**: los primeros 6 s transcritos CON el prompt LITERAL (sin él, Whisper junta dos tomas en una y no se ve la repetición) Y sin prompt, palabra a palabra: el gancho una sola vez y desde su toma buena (075: «Si empiezas tus… Si empiezas tus vídeos» se escapó).
- [ ] Un «SE OYE DISTINTO» que aparece IGUAL junto y por separado NO es invención: está en la grabación → es una repetición/arranque en falso REAL y se quita (`fuera`). Nunca se descarta un aviso sin espectrograma o escucha de ese trozo.
- [ ] `revisar_cortes.py`: cero ✗ reales (los que queden: pausa natural suya o 0,03 s dentro de una frase, y se le dice).
- [ ] Escucha ENTERA (`python herramientas/escuchar.py reels.json`) comparada con el guion frase a frase: mismo orden, sin ganchos colados, sin frases repetidas ni que falten, sin palabras cortadas («public», «…s Vivimos») ni restos de otra toma pegados sin pausa («Señes. Puede que…», «De verdad, yo llevé…», «tú, me imagino…» → `fuera` con los segundos de la grabación). «Gracias» o «Gracias por ver el vídeo» al final es invención del reconocedor en el silencio.
- [ ] ESPECTROGRAMA de cada corte y de TODA palabra que empiece o acabe en «s» junto a un corte (también la primera de cada trozo, como «Solo»). Si la «s» no está ni en la grabación, se deja (NUNCA prestarla de otra palabra: se nota). Cortes dudosos y palabras acabadas en «s»: espectrograma (`showspectrumpic`) de la grabación y del reel → la «s» entera dentro; ninguna «s» de la toma de antes delante.
- [ ] Respiraciones fuera; silencios tipo Lavri: mediana ≤ 0,06 s medida por `revisar_cortes` (casi ninguno > 0,05 s de silencio limpio), también tras punto; principio sin silencio.
**Render**
- [ ] Música intacta (−11,5 dB bajo la voz, sin sidechain); voz −14 LUFS (comprobar con ebur128).
- [ ] Hoja de fotogramas: subtítulos arriba (negro o blanco con sombra según el fondo), 4-5 palabras, mayúscula al empezar y tras punto, UNA clave azul; título abajo en caja negra, CRUDO y negativo, visible en la vista previa 3:4; fotos cuadradas pequeñas, sin taparle la cara, solo suyas y con contexto exacto; zoom suave al final.
- [ ] **Comprobación final sobre el MP4 ENTREGADO en REELS** (no sobre voz.wav): gancho con prompt LITERAL y escucha completa. Solo entonces se dice «está arreglado» (075: lo di por bueno sin mirar el archivo final y seguía repetido).
- [ ] Copiado a REELS como PUBLICAR o TRIAL (todos con el control de calidad pasado) con su .txt (título IG ≤ 45 caracteres, descripción, hashtags). Nada se programa sin su OK.

> **🔴 SIN RELLENO, PERO FLUIDO (Abel 18/10/2026):** fuera todo lo que no añade información vital (repeticiones, «y te lo digo claro», «así que», muletillas); el texto tiene que fluir y conectar como se habla, sin trocear frases a hachazos. Memoria `sin-conectores`.
