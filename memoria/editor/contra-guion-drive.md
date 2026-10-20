---
name: contra-guion-drive
description: Todo reel se verifica FRASE A FRASE contra el guion del Drive (contra_guion.py): ninguna frase a medias, nada del guion fuera sin motivo
metadata:
  type: feedback
---
Abel (19/10/2026, reel 117 seg. 36): «Siempre que edites los vídeos te tienes que centrar y tomar de referencia el guion del Drive, que para eso está». Salió «O tapas las fugas, pero no cargas.» (toma a medias; el guion decía «…pero no haces nada que te cargue, y vives sin dolor, pero también sin ganas») en los 5 reels del vídeo.

**Why:** la transcripción y la onda solo comprueban que no falten ni se repitan palabras; una frase cortada se oye bien pero no tiene sentido, y como el cuerpo es común, el error sale en TODAS las versiones.
**How to apply:** (1) guarda en `<carpeta>/guion.txt` el doc del Drive (Hooks + Guion, sin las notas de dibujo); (2) al elegir islas, cada frase del cuerpo tiene que ser la frase del guion COMPLETA (si la única toma está a medias, se quita entera y se arregla lo de alrededor para que se entienda, p. ej. quitar la «O» de una disyuntiva que se queda sin pareja); (3) tras montar, `python herramientas/rapido/contra_guion.py <carpeta>` y revisar A MANO cada ✗ A MEDIAS / FALTA contra el guion antes de renderizar. Ver [[errores-raiz-reels]], [[registro-virales]].

**Final cortado (Abel 20/10/2026, reel 180 / historia11):** el reel acababa con su tono de voz aún «en el aire» porque descarté el cierre real («…va a llegar, llega. Pero no tengas miedo.»), que Whisper había transcrito como «Diego». Regla: TODO lo grabado después de la última toma usada se ESCUCHA antes de dar el reel por bueno; si es el cierre, entra (`contra_guion.py` lo avisa con «⚠ DESPUÉS DEL FINAL hay voz»). El último trozo de cada reel tiene que acabar con tono de cierre, no de frase que sigue.
