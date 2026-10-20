"""Relacionador: para cada frase de un guion o transcripción, propone qué imagen encaja con LO QUE SE DICE.
    python relacionar_imagenes.py <texto.txt | "frase"> [--min 2] [--solo fotos|biblioteca]
Busca en la biblioteca de imágenes (EDICION VIDEOS/IMAGENES/catalogo.json: emociones, frecuencia, ego, leyes...)
y en sus fotos (MarcaPersonal/FOTOS MIAS/catalogo.json: su historia por épocas, solo las que valen para reels).
Solo PROPONE: cada candidata se mira a ojo junto a la frase antes de usarla (regla de Abel 18/10/2026: la imagen
tiene que ir 100 % con lo que se explica; si ninguna encaja, la frase va sin imagen).
"""
import json, re, sys, unicodedata
from pathlib import Path

BIB = Path.home() / 'Desktop/EDICION VIDEOS/IMAGENES'
FOT = Path(__file__).resolve().parent.parent / 'MarcaPersonal/FOTOS MIAS'

# Palabras con las que Abel explica cada tema (cómo lo dice él, no el nombre del archivo).
TEMAS = {
    'campo-toroidal': 'campo energia magnetismo magnetico atraer atraes corazon toroide alrededor irradiar',
    'aura-cuerpo-de-luz': 'aura cuerpo luz alma esencia quien eres energia brillo',
    'frecuencia-vibracion': 'vibracion vibrar frecuencia energia alta baja cansado agotado bateria burnout fuerzas',
    'miedo-amor': 'miedo amor contraer expandir paz',
    'ego': 'ego personaje mascara identidad orgullo aparentar actuar',
    'intuicion-tercer-ojo': 'intuicion corazonada tercer ojo sentir senales presentimiento',
    'nino-interior': 'nino interior infancia pequeno padres',
    'manifestacion': 'manifestar manifestacion crear realidad abundancia dinero atraer salto cuantico recibir',
    'tarot': 'ciclo final cerrar etapa transformacion crear',
    'elementos': 'elementos equilibrio naturaleza',
    'universo-cosmos': 'universo flujo sabiduria cosmos',
    'emociones': 'emocion emociones ruptura pareja romper dolor relacion',
    'cotidiano-bocetos': 'trabajo rutina prisa esfuerzo metas contactos talento ordenador oficina agotado mil cosas',
    'personajes': 'magnetismo carisma magnetico',
    'leyes-hermeticas': 'mente pensamiento pensamientos mentalismo leyes',
    'masculino-femenino': 'masculino femenino polaridad pareja energia masculina femenina',
    'descenso-transformacion': 'fondo tocar infierno noche oscura caida descenso crisis perderlo todo hundido pozo',
    'mitologia': 'descenso inframundo transformacion',
    'sombra-inconsciente': 'sombra inconsciente mente reprogramar presente tiempo pasado subconsciente',
    'centros-energeticos': 'chakras cuerpo energia alma espiritu',
}
VACIAS = set('el la los las un una unos unas de del al a en y o que se te me mi tu su sus lo le les con por para es son fue era muy mas pero como cuando si no ni ya yo tu esto eso esta este estas estos tan todo toda todos todas hay ser estar tener hacer'.split())


def norm(t):
    t = unicodedata.normalize('NFD', t.lower())
    return ''.join(c for c in t if unicodedata.category(c) != 'Mn')


def raices(t):
    t = norm(t).replace('.', '')
    return {w[:5] for w in re.findall(r'[a-zñ]+|\d{2,}', t) if (w.isdigit() or len(w) > 2) and w not in VACIAS}


def candidatas(solo=None):
    out = []
    if solo != 'fotos':
        for k, v in json.loads((BIB / 'catalogo.json').read_text(encoding='utf-8')).items():
            out.append(('biblioteca', str(BIB / k), v['muestra'], raices(f"{v['muestra']} {TEMAS.get(v['tema'], '')}")))
    if solo != 'biblioteca':
        for k, v in json.loads((FOT / 'catalogo.json').read_text(encoding='utf-8')).items():
            if v.get('reels') is False or not k.lower().endswith(('.jpg', '.png', '.jpeg')):
                continue
            txt = f"{k.replace('-', ' ').replace('_', ' ')} {v.get('que_es', '')} {v.get('epoca', '')} {v.get('emocion', '')} {' '.join(v.get('angulos', []))}"
            out.append(('foto', str(FOT / k), v.get('que_es', ''), raices(txt)))
    return out


def main():
    args = sys.argv[1:]
    mn = int(args[args.index('--min') + 1]) if '--min' in args else 2
    solo = args[args.index('--solo') + 1] if '--solo' in args else None
    src = args[0]
    texto = Path(src).read_text(encoding='utf-8') if Path(src).exists() else src
    frases = [f.strip() for f in re.split(r'(?<=[.?!])\s+|\n+', texto) if len(f.strip()) > 8]
    cands = candidatas(solo)
    for f in frases:
        r = raices(f)
        top = sorted(((len(r & c[3]), c) for c in cands), key=lambda x: -x[0])[:3]
        top = [t for t in top if t[0] >= mn]
        print(f'\n«{f}»')
        if not top:
            print('   — sin imagen (nada encaja)')
        for s, (fam, ruta, que, _) in top:
            print(f'   [{s}] {fam}: {que[:90]}\n        {ruta}')


if __name__ == '__main__':
    main()
