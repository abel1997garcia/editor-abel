# Biblioteca de imágenes de Abel (F4 y F2)

Imágenes con la identidad de su marca, **comprobadas a ojo** (no por el nombre del archivo) contra `ABEL GARCIA/Editor vídeos/Referencias/formato4/estilo_imagenes.png`.
Dos familias:
1. **Esquemas sobre blanco** que explican lo que dice (campo toroidal miedo/amor, chakras con nombres, cinco elementos, leyes herméticas, procesos mente-emoción).
2. **Arte visionario / esotérico**: cuerpos de luz y auras (estilo Alex Grey), campo toroidal alrededor de una figura, cosmos psicodélico, tarot (el Mago…), grabados antiguos; bocetos a tinta B/N para lo cotidiano.

Una carpeta por tema; cada imagen se apunta en `catalogo.json` con: tema, qué muestra, familia, origen (URL) y fecha. Cada descarga se confirma antes con Abel.
Temas: centros-energeticos · campo-toroidal · aura-cuerpo-de-luz · frecuencia-vibracion · miedo-amor · ego · intuicion-tercer-ojo · nino-interior · manifestacion · tarot · elementos · universo-cosmos · emociones · cotidiano-bocetos · personajes · leyes-hermeticas · masculino-femenino
Hoja de todo lo que hay: `_hoja_biblioteca.png` (rehacerla al añadir).
**Cómo crece:** Abel pasa reels de referencia; de cada uno se extraen sus imágenes (bordes rectos con OpenCV; las que se funden con el fondo, a ojo con una cuadrícula de coordenadas), se recortan limpias y se catalogan. Las sacadas de vídeo tienen poca resolución (300–700 px): sirven tal cual en el reel; si hace falta más, buscar el original con Google Lens (descarga confirmada).

## Al añadir imágenes (Abel, 08/10/2026)
1. **Recorte limpio**: que no asome nada del vídeo de detrás (ni subtítulos ni ropa); comprobarlo en una hoja sobre fondo verde. Los bordes exactos se buscan en el fotograma original (el recorte limpio se guarda en `_originales/` solo mientras se procesa).
2. **Nitidez con IA** (Real-ESRGAN, `ABEL GARCIA/Editor vídeos/herramientas/realesrgan/`): fotos, pinturas y arte visionario con `realesrgan-x4plus`; grabados, bocetos y esquemas con `realesrgan-x4plus-anime`. Guardar a ×3 del recorte. Script: `_mejorar_ia.py`.
3. **Todo el texto en español**: tapar cada texto con el color de su fondo y escribir la traducción en Montserrat; los esquemas que son casi solo texto, rehacerlos enteros. Ejemplo: `_traducir_lote1.py`. Quitar marcas de agua de otras cuentas.

4. **Al terminar, borrar `_originales/` y los temporales** (Abel: no guardar copias, ocupan espacio). Si una traducción hay que rehacerla, se pinta encima de la imagen final.
