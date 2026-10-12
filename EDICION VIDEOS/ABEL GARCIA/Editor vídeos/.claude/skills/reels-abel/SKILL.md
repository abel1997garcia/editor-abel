---
name: reels-abel
description: Sacar reels de Abel de un vídeo horizontal (F1 yapping) con el listón de calidad que exige. Úsala siempre que haya que hacer, rehacer o revisar reels de publicar/ o trial/.
---

# Reels de Abel desde un horizontal (F1)

Nada se entrega si no pasa el LISTÓN. «No se trata de subir por subir» (Abel, 12/10/2026). Modelo de ritmo y títulos: Lavri (`Referencias/lavri/ANALISIS.md`, apartado reels).

## 1. Ganchos y estructuras (antes de tocar ninguna herramienta)
- Hacer el banco: 20 o más ganchos (primero los que hablan directamente a la persona) y estructuras colleja → solución de una idea, en `VideosLargos/<tema>/reels_banco.md`.
- Un gancho solo vale si:
  - es una frase COMPLETA, que arranca tras una pausa y acaba con tono de cierre (nunca la mitad de una lista, nunca la cola de otra frase);
  - se entiende sola: sin «eso», «esto» o «con eso» sin referente. Si lo lleva, se coge también la frase de antes («Los que más dinero hacen es una cosa específica… Cuando te haces bueno con eso, nunca te va a faltar negocio»);
  - toca un dolor o rompe una creencia, y pasa el test de la memoria `ganchos`.
- El cuerpo no repite el gancho.
- Trial = la misma estructura con otro gancho que cumpla lo mismo.
- 40–60 s.

## 2. Título (arriba)
- Da el contexto que el gancho no dice y lleva la connotación negativa.
- 6–10 palabras en 2 líneas, a menudo acabado en dos puntos.
- Fórmulas: «Por esto…», «Si no haces esto jamás…», «Así…».
- Números solo si son reales. La palabra clave entre “comillas” (sale en cursiva). Una palabra en MAYÚSCULAS como mucho.
- Nunca repite el gancho.

## 3. Config y voz
`MarcaPersonal/<tema>/reels_f1.json`:
- con horizontal estándar: `fuente` (el horizontal), `tiempos` (`<horizontal>.tiempos.json`) y `montaje` (`<horizontal>.montaje.json`);
- con pizarra: además `toma` y `ventanas`.

Luego:
1. `python herramientas/reel_yapping.py reels_f1.json --texto` → leer el texto corrido de cada reel en voz alta.
2. `... --voz` → `out/_<reel>/voz.wav`. Los microsilencios (≥ 0,2 s) ya salen a ~0,13 s medidos sobre la voz real (`microcortes`), sin cortar palabras.

## 4. LISTÓN de audio (todo, en cada reel)
1. La línea `listón` de `--voz`: **≥ 3,3 palabras/s** y **ningún hueco > 0,35 s** salvo el final (Lavri: máx. ~0,3).
2. `python herramientas/verificar_audio.py out/_<reel> <tiempos>` para todos (`> verif.log`).
3. `python herramientas/oir_uniones.py verif.log out` vuelve a escuchar cada ✗ con 4 s de contexto:
   - si suena igual que la toma original, es un falso aviso de Whisper;
   - si falta, sobra o se repite algo, se corrige (ampliar o mover el tramo, nunca retocar a mano los tiempos de las palabras) y se vuelve al punto 1.
   - Un ✗ NUNCA se da por bueno «porque el texto se lee bien».
4. Música por estilo: `herramientas/estilo_voz.py out/_<reel>/voz.wav --base <5 min de la toma>` → intensidad → tema de `MUSICA/catalogo.json` por su «caracter».

## 5. Render y LISTÓN de imagen
- `reel_yapping.py reels_f1.json` → hoja de 8 fotogramas por reel y mirarla.
- No puede haber:
  - animaciones a medio dibujar ni sin la frase que las explica (si pasa, ese trozo va con su cara: `toma` + `ventanas`, o se mueve el tramo);
  - palabras sueltas en pantalla;
  - un título que tape algo.

## 6. Entrega
- Copiar a `MarcaPersonal/publicar|trial/semana_<lunes>/<día>_<tema>_<cNN|tNN>_g<N>e<N>_F1.mp4` con su `.txt` (título, descripción, hashtags).
- `MarcaPersonal/<tema>/plan.md`.
- Borrar `out_f1/`.
- Nada se programa sin su OK.
