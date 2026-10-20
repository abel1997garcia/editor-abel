"""Prueba de diapositivas-esquema (estilo propio, inspirado en @tuseienergia) con Nano Banana (0,039 $/imagen).
Sale sobre negro; luego pizarra_png.py lo convierte en PNG transparente."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from pizarra_replicate import correr, bajar, OUT

ESTILO = ('Whiteboard explainer cartoon on a pure black background (#000000): clean white line strokes, lively like a frame of an explainer animation, '
          'but simple and clear, understood in one second at small size. Simple round-headed character with a minimal expressive face. '
          'Vertical composition that fills the frame from top to bottom, the whole character visible with margin, at most the character plus 3 elements. '
          'Only the black background, no ground, no scenery. NO text, no letters, no watermark. ')
DIAPOS = {
    'rojo_persigue_aprobacion': 'The character, drawn with RED (#F05050) outline, runs desperately upward chasing a red heart and a blue thumbs-up icon '
                                'that fly away from him near the top; a long dashed white arrow goes from him to the icons; sweat drops, a few motion lines behind him.',
    'azul_deja_de_perseguir': 'The same character, drawn with BLUE (#2E7BFF) outline, stands calm at the bottom with eyes closed and a small smile, '
                              'while a red heart and a blue thumbs-up icon float down toward him; a short dashed white arrow from the icons to him.',
}
total = 0
for nombre, escena in DIAPOS.items():
    url = correr('google/nano-banana', {'prompt': ESTILO + escena, 'aspect_ratio': '2:3', 'output_format': 'png'})
    bajar(url, OUT / 'prueba_diapo' / f'nb3_{nombre}.png'); total += 0.039; print(nombre, 'ok', flush=True)
print(f'coste aproximado: {total:.3f} $')
