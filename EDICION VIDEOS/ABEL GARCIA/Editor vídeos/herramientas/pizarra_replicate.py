"""Escenas de pizarra para los reels HISTORIA: Nano Banana en Replicate (0,039 $/imagen) → PNG transparente
→ IMAGENES/pizarra/escenas/<vídeo>/ + IMAGENES/catalogo.json (familia «pizarra»). La clave se lee de
C:\\Users\\Clap\\.replicate_token (nunca se muestra).

CÓMO SE LLEGÓ AQUÍ (Abel 19/10/2026: «enhorabuena… explica cómo has llegado a esto»):
1. UN SOLO PERSONAJE para que la persona se meta en la historia: el muñeco de «17.000 € y vacío» (cabeza redonda, cuerpo BLANCO,
   contorno grueso, cara mínima). Rojo = cuando se abandona; azul = cuando se elige. Sus hojas de referencia
   (IMAGENES/pizarra/_personaje/hoja_rojo.png y hoja_azul.png) van SIEMPRE como image_input: así sale el mismo en cada escena.
2. ESCENA COMPLETA, no el muñeco solo (como las diapositivas de @tuseienergia): con quién está, dónde, qué siente y qué le pasa,
   con metáforas visuales claras (la batería que se vacía mientras le cargan tareas, la balanza en la que pesa más un corazón…).
   Los demás personajes, mismo estilo con contorno GRIS: el protagonista siempre destaca.
3. Fondo negro puro SIN marco, panel ni recuadro (el modelo a veces pinta uno blanco: se repite la escena), sin texto, cuadrada.
4. Se MIRA cada escena antes de usarla: que diga lo que tiene que decir (una balanza salió al revés y se repitió).
5. En el vídeo (rapido/capa_viral.py) todas van en la MISMA caja, centradas con su título (fino + palabra clave en grueso) en la zona derecha.

ANTES de generar, buscar si ya existe (se reutiliza):
    python pizarra_replicate.py buscar aprobacion
Generar una escena (en inglés, la situación completa):
    python pizarra_replicate.py nuevo <vídeo> <nombre> rojo|azul|ambos "qué muestra" "escena" "significado" "usar cuando" "palabras clave"
"""
import base64, json, sys, time, urllib.request
from datetime import date
from pathlib import Path
from pizarra_png import a_png

TOKEN = (Path.home() / '.replicate_token').read_text(encoding='utf-8').strip()
IMG = Path.home() / 'Desktop' / 'EDICION VIDEOS' / 'IMAGENES'
OUT = IMG / 'pizarra'
HOJAS = {'rojo': OUT / '_personaje' / 'hoja_rojo.png', 'azul': OUT / '_personaje' / 'hoja_azul.png'}
CATALOGO = IMG / 'catalogo.json'
MODELO, PRECIO = 'google/nano-banana', 0.039

ESCENA = ('Whiteboard explainer illustration, rich and full of context like a frame of an animated explainer, telling the whole situation at a glance. '
          'The MAIN character is EXACTLY the one from the reference sheet (same round head, white-filled body, thick {c} outline, minimal face) and he is clearly '
          'the protagonist, the same size in every scene. Other people, if any, are drawn in the same simple style but with a light GREY outline. '
          'Simple flat props with a few accent colours, clear visual metaphors, arrows or motion lines if they help. Pure black background everywhere '
          '(NO white panel, NO frame, NO card, NO box behind the scene), drawn DIRECTLY on the black canvas: NO white margin or border, NO inner rectangle, '
          'NO floor or stage shape, NO big coloured halos or glows behind the characters; square composition, everything inside the frame with margin. '
          'NO text, no letters, no words, no watermark. Scene: ')


ESCENA_AMBOS = ESCENA.replace('The MAIN character is EXACTLY the one from the reference sheet (same round head, white-filled body, thick {c} outline, minimal face) and he is clearly '
                               'the protagonist, the same size in every scene.',
                               'There are TWO main characters, EXACTLY the ones from the two reference sheets (same round head, white-filled body, minimal face): '
                               'one with a thick RED outline and one with a thick BLUE outline, same size, both clearly the protagonists.')


def correr(modelo, entrada):
    req = urllib.request.Request(f'https://api.replicate.com/v1/models/{modelo}/predictions',
                                 data=json.dumps({'input': entrada}).encode(), method='POST',
                                 headers={'Authorization': f'Bearer {TOKEN}', 'Content-Type': 'application/json', 'Prefer': 'wait'})
    r = json.load(urllib.request.urlopen(req, timeout=120))
    while r.get('status') not in ('succeeded', 'failed', 'canceled'):
        time.sleep(2); r = json.load(urllib.request.urlopen(urllib.request.Request(r['urls']['get'], headers={'Authorization': f'Bearer {TOKEN}'})))
    if r['status'] != 'succeeded': raise RuntimeError(r.get('error'))
    out = r['output']; return out[0] if isinstance(out, list) else out


def quitar_marco(ruta):
    """Nano Banana a veces enmarca la escena en un panel BLANCO aunque el prompt lo prohíba: si el borde es blanco,
    se recorta al rectángulo oscuro de dentro (la escena) — así no hay que pagar otra vez por repetirla."""
    import numpy as np
    from PIL import Image
    im = Image.open(ruta).convert('RGB'); g = np.asarray(im).astype(int); h, w = g.shape[:2]; b = max(4, w // 50)
    borde = np.concatenate([g[:b].reshape(-1, 3), g[-b:].reshape(-1, 3), g[:, :b].reshape(-1, 3), g[:, -b:].reshape(-1, 3)])
    if borde.min(axis=1).mean() < 200: return False                     # borde oscuro: no hay marco
    oscuro = g.max(axis=2) < 120; filas, cols = np.where(oscuro.mean(axis=1) > .3)[0], np.where(oscuro.mean(axis=0) > .3)[0]
    if not len(filas) or not len(cols): return False
    im.crop((cols[0] + 6, filas[0] + 6, cols[-1] - 5, filas[-1] - 5)).save(ruta); return True


def catalogo():
    return json.loads(CATALOGO.read_text(encoding='utf-8'))


def buscar(palabra):
    p = palabra.lower()
    campos = ('muestra', 'titulo', 'significado', 'usar_cuando', 'palabras_clave')
    return {k: v for k, v in catalogo().items() if v.get('familia') == 'pizarra' and p in (k + ' ' + ' '.join(v.get(c, '') for c in campos)).lower()}


def nuevo(video, nombre, color, muestra, escena, significado, usar_cuando, palabras_clave):
    dest = OUT / 'escenas' / video / f'{nombre}_{color}.png'
    if dest.exists(): raise SystemExit(f'ya existe: {dest}')
    hojas = [HOJAS['rojo'], HOJAS['azul']] if color == 'ambos' else [HOJAS[color]]      # «ambos»: Fulano (rojo) y Mengano (azul) en la misma escena
    hoja = ['data:image/png;base64,' + base64.b64encode(h.read_bytes()).decode() for h in hojas]
    crudo = OUT / '_personaje' / 'crudos' / f'{video}_{nombre}_{color}_negro.png'; dest.parent.mkdir(parents=True, exist_ok=True); crudo.parent.mkdir(parents=True, exist_ok=True)
    urllib.request.urlretrieve(correr(MODELO, {'prompt': (ESCENA.format(c='RED' if color == 'rojo' else 'BLUE') if color != 'ambos' else ESCENA_AMBOS) + escena, 'image_input': hoja,
                                               'aspect_ratio': '1:1', 'output_format': 'png'}), crudo)
    quitar_marco(crudo); a_png(crudo, dest)
    c = catalogo()
    c[dest.relative_to(IMG).as_posix()] = {'tema': f'pizarra/escenas/{video}', 'muestra': muestra, 'familia': 'pizarra', 'personaje': color,
                                          'significado': significado, 'usar_cuando': usar_cuando, 'palabras_clave': palabras_clave,
                                          'origen': f'{MODELO} con la hoja del personaje ({PRECIO} $)', 'prompt': escena, 'fecha': date.today().isoformat()}
    CATALOGO.write_text(json.dumps(c, ensure_ascii=False, indent=1), encoding='utf-8')
    return dest


if __name__ == '__main__':
    orden = sys.argv[1:2]
    if orden == ['buscar']:
        for k, v in buscar(sys.argv[2]).items(): print(f"{k}\n   significa: {v['significado']}\n   usar cuando: {v['usar_cuando']}")
    elif orden == ['nuevo']:
        print(nuevo(*sys.argv[2:10]), f'· {PRECIO} $')
    else:
        print(__doc__)
