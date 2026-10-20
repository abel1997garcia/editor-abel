---
name: edicion-reels-obligatoria
description: "OBLIGATORIO en TODO reel de Abel (F1-F5, casual): ritmo de Lavri (pausas ~0,05–0,07 s, máx. 0,07; > 0,10 s es error), velocidad normal, ver la pista de audio con onda.py, cortar cualquier trabazón o repetición, todo a PUBLICAR"
metadata:
  node_type: memory
  type: feedback
  originSessionId: d7cbc795-7ce8-4682-b768-22bda44decfe
  modified: 2026-10-13T21:52:16.328Z
---

**Abel 13/10/2026, tras rehacer los reels 064-066:** «ahora está muchísimo mejor… a partir de ahora todos los reels que edites tienen que seguir estos mismos patrones… guárdatelo bien porque eso 100 % tiene que seguir así, en cualquier reel que hagamos».

**Las reglas (todas, en todos los reels):**
1. **Pausas cortas, ritmo de Lavri** (su reel `Referencias/virales/ritmo_DeNRktgtcyT`: pausas reales de 0,01-0,05 s, ninguna > 0,10 s).
   - Los microcortes dejan unos 0,07 s y se corta todo silencio de ≥ 0,10 s (`MICRO` en `reel_yapping.py`).
   - El listón: pausas de ~0,05–0,07 s (máx. 0,07); la onda marca en rojo > 0,10 s, que ya es error. Al final, 0,1 s de aire (como mucho 0,16 s).
2. **Velocidad NORMAL 1,0x (Abel 19/10/2026: «la clave no está en aumentar la velocidad, sino en reducir los silencios y pulir el audio»)**: no se acelera ningún reel.
3. **Ver la pista de audio, como un editor:** `python herramientas/onda.py <reels>`. Se MIRA la imagen de la forma de onda de cada reel antes de entregar. Si hay algo en rojo (hueco > 0,10 s, también al principio y al final), no se entrega.
4. **Todo lo que no sea 100 % fluido se corta:**
   - trabarse («que digo… que digo» y luego lo dice);
   - empezar una frase y rehacerla;
   - repetir algo dos veces, aunque sea a propósito («la información, la gran mayoría de la información»);
   - muletillas;
   - frases a medias.
   - Se lee el `--texto` de cada reel buscando ESO antes de generar la voz, y después se escucha (verificar_audio + oir_uniones + buscar_repes). Se queda UNA versión, entera y limpia.
5. **PUBLICAR = reels sacados de sus vídeos largos.** Los vídeos VERTICALES que graba él (guiones virales) son SIEMPRE **TRIAL** (Abel 14/10/2026: «si te paso los vídeos en vertical se llaman trials»). [[referencias-virales]]

**Fallos de la tanda 067-075 (Abel 14/10/2026, «fatal resultado… tardaría muchísimo menos en editarlo yo a mano»):**
- Uniones pegadas: casi todos los cortes dejaban < 0,03 s de silencio real y una frase chocaba con la otra; «se escucha fatal». El silencio de cada unión se MIDE en la onda y queda en ~0,07 s (`igualar` en `reel_tablero.py`).
- Trabazones sin cortar: antes de renderizar se lee el texto palabra a palabra (tiempos.json) buscando «lo que… qué», palabras a medias («pi...»), repeticiones; NO basta el texto corrido.
- F3 ligero con fuente vertical: la cara salía DEFORMADA (escalaba a 16:9). Mirar fotogramas de cada formato antes de entregar.
- F5: título demasiado bajo y subtítulos demasiado altos; música casi inaudible a −13,5 dB.
- F4 que solo son subtítulos «no añade nada de valor»: o lleva imágenes/escenas con contexto de verdad, o no se hace.
- La voz no se mejoró en F4/F3 (solo F5 pasaba por DeepFilterNet).
- Tardar ~2 h en 9 reels es inaceptable: el render ya va en paralelo (1 min por vídeo); el trabajo largo debe ser el de criterio, no el de máquina.

**✅ AUDIO Y CORTES ARREGLADOS (Abel 14/10/2026, tras 067-075: «no hay errores en el audio ni malos cortes, eso está ya arreglado, guárdalo bien»). Así se hace y NO se cambia:**
- Se corta por ISLAS DE VOZ de la onda de la voz limpia (`igualar` en `reel_tablero.py`), nunca por los tiempos de Whisper (se equivocan hasta 0,3 s): islas enteras, margen antes 45 ms / después 30 ms, ~0,06 s de aire, cortes en fotogramas exactos (si no, la voz se desfasa).
- La voz que se monta es siempre `_fuente_limpia.wav` (casual_prep) + presencia.
- **La ESCUCHA es obligatoria en todos los reels antes del render: `revisar_cortes.py`** — escucha el audio montado corte a corte (corte sobre voz, pegado, hueco, microcorte, principio/final, «se oye distinto»). Abel: «tiene que depender del audio, no de la transcripción». Cada ✗ se corrige como un editor (`fuera`, `cuchillas`, `aire` en reels.json) hasta que salga limpio; lo que quede se le dice con el segundo exacto.
- Velocidad de los reels virales: NORMAL 1,0x (antes 1,10x, aplicada al final del montaje.

**Herramientas:** `reel_yapping.py` (F1) y `reel_tablero.py` (F2-F5, que importa los mismos ajustes). Detalle en la skill `reels-abel` y en [[registro-edicion-abel]].

**Reels de Allan:** NO llevan este ritmo rápido (Abel 13/10/2026). Solo la vista de la pista con sus límites (`onda.py --hueco 0.55 --final 0.4`), según el CLAUDE.md de su proyecto.

**CHECKLIST SIEMPRE, sin saltar pasos (Abel 15/10/2026: «edita bien todos los vídeos a la primera y no tenga que decirte mil veces de rehacerlos»):** la lista está en la skill `reels-virales` (CHECKLIST FORMATO TAB). Se recorre en orden y entera en cada vídeo: guion del Drive con el mismo título → ¿es lista? → comparar lo dicho con el guion → cortes → ESPECTROGRAMA de cada ✗ y de cada corte (nunca dar por bueno un ✗ sin verlo; en el 076 se coló la cola de «vendados» en el 10,8 s) → escucha entera → hoja de fotogramas (9:16, sin franjas, zoom sin cortarle) → escucha del MP4 final. Nitidez: SIEMPRE un poco (`"mejorar": "suave"`), nunca la fuerte (le cambia la cara).

**079 (15/10/2026) — errores que NO se repiten:** (1) silencios de 0,2 s que la onda marcaba y descarté «porque era la palabra apagándose» → NINGÚN ✗ de la onda se descarta: el reel montado tiene que dar «✓ sin huecos > 0,10 s» (ahora `--voz` lo aprieta solo midiendo el reel); (2) corte malo antes de «Mi audiencia» (empezaba sobre la cola de «audien…») → nunca arrancar un trozo sobre otra palabra; (3) subtítulo «completamente» salido del plano → se encogen solos, mirar fotogramas en palabras largas; (4) música cantada alta → cantadas 6 dB más bajas (catálogo `voz`); (5) espectrograma del reel ENTERO, no solo de los ✗. Velocidad de los TAB: **1,07x**. El reconocedor de voz NO sirve para decir que una palabra está entera (rellena lo que falta).

**079, 2.ª corrección (15/10/2026):** (a) ante un error, volver a la GRABACIÓN ORIGINAL y medir desde cero, no parchear lo montado; (b) silencio máximo de cualquier unión = la pausa gancho→cuerpo del propio reel; (c) escuchar SOLO cada trozo corto que se empalma (un «Mi» era un resto que sonaba «Te da miedo»); (d) la «s» final floja es parte de la palabra: espectrograma de agudos antes de recortar; (e) SIEMPRE foto suya del momento cuando cuenta su historia (TAB: `imagen()` a la derecha).

**Herramienta (15/10/2026, tras 079-084):** `casual_prep.py` transcribe POR VENTANAS (14 s cada 12 s, dos pasadas desplazadas 6 s y combinadas): de una pasada Whisper juntaba tomas y descolocaba tiempos («mundo» 1 s tarde) y el cortador se comía palabras. `apretar` mide el FINAL de cada palabra con umbral permisivo (pico −30 dB: la voz floja es palabra) y el silencio como la onda; descarta trozos < 0,25 s donde no empieza ninguna palabra (respiraciones). Donde la toma buena va PEGADA a la descartada («y... Pero», «amigo y | Y que»), `fuera` en el valle de la onda (la «P» tiene un cierre de labios antes). Un «Y» tan flojo que la onda lo cuenta como silencio se quita.

**082 (15/10/2026, Abel: «HAY DOS FALLOS QUE DEBERÍAS VER»):** restos de tomas descartadas («o no» antes de «Si le hablas», «un…» antes de «y que simplemente»). Las herramientas lo marcaban (SE OYE DISTINTO, «O no» en la escucha) y lo di por bueno. AHORA: `herramientas/cortes_oido.py` escucha CADA corte por separado en el MP4 entregado; cualquier palabra que no está en el guion se mide en la grabación y se quita. El principio de una palabra buena se busca escuchando TROZOS SUELTOS de la grabación (el «Si» real estaba 0,8 s más tarde de lo que decía la transcripción).

**ZOOM SIN CORTARLE (Abel 18/10/2026):** cualquier zoom al editar (F1 yapping, TAB, F4…) tiene que dejarle a ÉL entero dentro del encuadre (cara, cabeza y hombros). Si en la grabación ya está pegado a un borde, no se hace zoom o se centra en su cara; nunca se le corta. El OBS ya le deja descentrado a la izquierda (prueba del 18/10).
