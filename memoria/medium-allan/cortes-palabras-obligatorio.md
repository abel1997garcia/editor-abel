---
name: cortes-palabras-obligatorio
description: OBLIGATORIO antes de entregar cualquier reel de Allan - escuchar TODOS los empalmes; nunca cortar dentro de una palabra (error repetido 3 veces: «exist», «cort», muletillas que asoman)
metadata:
  type: feedback
---

El usuario se ha quejado TRES veces de cortes mal hechos (2026-10-07: «existente» sonaba «exist», «corto» sonaba
«cort», cortes bruscos y nada fluidos en «creer para ver»; «es la segunda vez que te lo digo y sigue igual»).
Que una palabra se corte o que asome una muletilla en un empalme es INACEPTABLE.

Causas reales encontradas (todas corregidas en herramientas/reel_franjas.py):
1. Las oclusivas (t, p, c, d, q) hacen 50-90 ms de silencio DENTRO de la palabra («cort|o», «exis|te», «por|qué»).
   Regla dura: un final de trozo nunca cae antes del final alineado de su palabra; el inicio nunca después del
   arranque alineado; solo cuentan silencios >= 60 ms DESPUÉS del final / ANTES del inicio.
2. Ajustes manuales medidos a ojo con la energía estaban mal (puse fin «existente» en 341.08: cortaba la «-te»).
   Medir ESCUCHANDO: herramientas/buscar_inicio.py y buscar_fin.py (y confirmar con energía: Whisper «inventa» palabras
   con trocitos — el «¿no?» tras «realmente» era el arranque del «que» siguiente).
3. Muletillas pegadas sin silencio a la palabra siguiente («bueno pues se arregla», «o no siempre»): «ini_fijo».
   «y es» se pronuncia junto: no se separa, se deja la «y».
4. La regla anti-ráfagas volvía a unir trozos y deshacía cortes puestos a mano: ahora no toca cortes manuales.
5. Redondeo al fotograma hacia el lado malo: ini_fijo +30 ms y redondeo hacia delante.

PROTOCOLO OBLIGATORIO antes de entregar (no saltarse nada):
- herramientas/comprobar_cortes.py <reels>   (última/primera palabra de cada trozo entera)
- herramientas/oir_empalmes.py <reel> 1..N   (TODOS los empalmes del reel, leer cada uno)
- herramientas/revisar_por_tramos.py reels/<x>.mp4, medir_sync.py, silencios > 0,5 s
- Fundido de audio 25 ms en cada empalme (suave, no brusco). Fluidez > quitar cada muletilla: si no hay silencio
  entre dos palabras, no se corta ahí; se elige otro punto o se deja la palabra.

APROBADO (2026-10-07, guias_01..04 v3): «está perfecto, ahora sí todo tiene mucho más sentido, está bien recortado,
los ajustes se han medido escuchando el vídeo». Este es el método de referencia: cortes en el silencio real con la regla
dura, ajustes medidos ESCUCHANDO, guiones congruentes (sin redundancias, con conectores), fundido 25 ms, y escucha de
todos los empalmes antes de entregar. No volver a métodos anteriores (margen fijo sobre la alineación, medir a ojo).

**Why:** el usuario lo considera fundamental y ya lo ha pedido varias veces; cada fallo le obliga a revisar a mano.
**How to apply:** en cada reel, sin excepción, ejecutar el protocolo y escuchar los empalmes ANTES de decir que está
listo. Ver [[fallos-edicion-reels-allan]] (puntos 19-21).
