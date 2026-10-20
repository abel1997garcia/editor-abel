---
name: audio-primero
description: "OBLIGATORIO - en cada reel de Allan montar y depurar primero SOLO la voz (--voz, espectrograma, onda, empalmes) y después renderizar el vídeo encima"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 5031045c-b367-4cb9-8826-ca24be54d6d4
  modified: 2026-10-17T20:13:57.873Z
---

Abel (2026-10-17): «primero manda el audio, una vez optimizes el audio, montas el vídeo encima… aplicando en el audio
el espectrograma… irás más rápido y sobre seguro». Motivo: en reels anteriores se colaban «eh» y no estaba limpio
porque revisaba sobre el MP4 ya renderizado (minutos por intento). Así se hacía ya en el proyecto de Abel (skill
reels-virales: modo --voz + espectrograma + escucha de cortes, y solo luego render).

Orden obligatorio:
1. Transcribir/alinear y escribir el guion (trabajo/specs).
2. `python herramientas/reel_franjas.py <spec> --voz` -> trabajo/reels/<n>/voz.wav (~5 s; mismos cortes, fundidos y
   loudnorm que el render, misma duración exacta).
3. Revisar la voz: `python herramientas/espectro_cortes.py <n>` (viñeta ±1 s por empalme con línea cian + voz entera;
   «eh»/«mmm» = franja horizontal lisa sin consonantes; ojo, una vocal final alargada se ve igual: confirmar oyendo),
   `python herramientas/oir_empalmes.py --voz <n>` (sin números = TODOS los empalmes),
   `PYTHONIOENCODING=utf-8 python herramientas/onda.py --hueco 0.55 --final 0.4 trabajo/reels/<n>/voz.wav`,
   `comprobar_cortes.py`.
4. Corregir midiendo en el ORIGINAL (ini_fijo/fin_max en ajustes_tiempos.json, buscar_inicio/fin, oir.py), nunca
   parcheando lo montado; repetir 2-3 hasta que esté limpio.
5. Solo entonces render normal (sin --voz) y comprobaciones finales: medir_sync.py, onda.py sobre el mp4,
   revisar_por_tramos.py.

Lección del primer reel hecho así (sigue_01, 17/10/2026): la voz «ya entregada» tenía 7 muletillas: «eh» 0,67 s
delante de «El despertar», dos «eh» flojos (−30 dB) delante de «no es solo» y «es un proceso», «siempre, eh, sucede»,
«mismaaa… energía», y un «yyy» y un «queee» estirados en «y te lo digo yo que…». Las cacé con
`herramientas/voz_sin_palabra.py` (voz fuera de las palabras alineadas), escuchando con prompt de muletillas y
midiendo energía; las vi en el espectrograma como franjas lisas (una la despaché como vocal larga: NO, confirmar siempre).
Checklist completa en CHECKLIST_REELS_ALLAN.md.

Abel (17/10/2026, voz de sigue_01 aprobada: «está perfecto, muchísimo mejor»): una vez la voz está bien, lo que
queda es cuadrar y sincronizar el vídeo con el audio y que los subtítulos cuadren a la perfección (tiempos y
formato). Y «siempre ir mejorando con la experiencia de los errores»: cada fallo nuevo se apunta en
[[fallos-edicion-reels-allan]] / CHECKLIST_REELS_ALLAN.md y, si se puede, se convierte en un aviso automático.
Tú a tú: solo para los reels NUEVOS (los de «sigue» se dejan como están).

**Why:** se va más rápido (iterar sobre la voz cuesta segundos) y no se escapan muletillas.
**How to apply:** en todos los estilos (franjas azules, franja negra). Complementa [[cortes-palabras-obligatorio]] y
[[proceso-reels-allan]].
