"""Toma limpia (sin pausas, muletillas ni tropiezos) en ficha de cámara sobre blanco, para el vídeo largo.

Corta por palabras con la alineación de la toma (edicion/tiempos.json; las líneas de edicion/guion.txt con «~» se
quitan aunque estén en mitad de un bloque) y monta cada plano desde el vídeo ORIGINAL: la mitad de la cámara
(630x560) en una ficha de 1215x1080 sobre blanco. En los cortes de contenido y en las pausas largas el encuadre
alterna 1,0 / 1,10 DENTRO de la ficha (acercamiento a la cara; la ficha no cambia de tamaño).
    python limpiar.py          -> edicion/toma_limpia.mp4 + edicion/planos_limpios.json
    python limpiar.py --texto  -> solo el texto y la duración
"""
import json, subprocess, sys

FUENTE = r'C:\Users\Clap\Downloads\Cómo Dejar Ir las Emociones .mp4'
W = json.load(open('edicion/tiempos.json', encoding='utf-8'))
W = W['words'] if isinstance(W, dict) else W
PRE, POST, PAUSA, COLA = .07, .12, .30, .45
DINAMICO = 60.0                  # segundos del principio con acercamiento en cada corte
CAM = (0, 40, 630, 560)          # zona de la cámara en el original (x, y, ancho, alto)
CARA = (359, 300)                # centro de la cara en el original (mediana de YuNet, primeros 2 min)
FICHA_X = 268                    # la ficha (1215x1080) queda con la cara centrada en pantalla

quitadas = {w['frase'] for w in W if str(w['w']).startswith('~')}
keep = [i for i, w in enumerate(W) if w['frase'] not in quitadas]


def planos():
    grupos, g = [], []
    for i in keep:
        if g and (i != g[-1] + 1 or W[i]['s'] - W[g[-1]]['e'] > PAUSA):
            grupos.append(g); g = []
        g.append(i)
    grupos.append(g)
    res = []
    for k, g in enumerate(grupos):
        i0, i1 = g[0], g[-1]
        t0 = W[i0]['s'] - PRE
        if i0 > 0: t0 = max(t0, W[i0 - 1]['e'] + .02)
        t1 = W[i1]['e'] + (COLA if k == len(grupos) - 1 else POST)
        if i1 + 1 < len(W): t1 = min(t1, W[i1 + 1]['s'] - .02)
        res.append([round(t0, 3), round(t1, 3), g])
    return res


def montar(ps):
    fil, z, T = [], 1.10, 0.0
    for k, (t0, t1, g) in enumerate(ps):
        prev = ps[k - 1][2][-1] if k else None
        # primer minuto del vídeo: el encuadre cambia en CADA corte (dinamismo para retener, feedback 05/10/2026);
        # después, solo en los cortes de contenido y en las pausas largas
        if k == 0 or T < DINAMICO or g[0] != prev + 1 or W[g[0]]['s'] - W[prev]['e'] > .7: z = 1.0 if z != 1.0 else 1.10
        T += t1 - t0
        x, y, w, h = CAM; cw, ch = w / z, h / z
        cx = min(max(CARA[0] - cw / 2, x), x + w - cw); cy = min(max(CARA[1] - ch * .45, y), y + h - ch)
        fil.append(f"[0:v]trim={t0}:{t1},setpts=PTS-STARTPTS,crop={cw:.1f}:{ch:.1f}:{cx:.1f}:{cy:.1f},"
                   f"scale=1215:1080:flags=lanczos,unsharp=5:5:0.5,setsar=1,fps=30[c{k}];"
                   f"color=white:s=1920x1080:r=30:d={t1 - t0:.3f}[b{k}];[b{k}][c{k}]overlay={FICHA_X}:0:shortest=1[v{k}];")
        d = t1 - t0
        fil.append(f"[0:a]atrim={t0}:{t1},asetpts=PTS-STARTPTS,afade=t=in:d=0.008,afade=t=out:st={d - .008:.3f}:d=0.008[a{k}];")
        ps[k].append(z)
    n = len(ps)
    fil.append(''.join(f'[v{k}][a{k}]' for k in range(n)) + f'concat=n={n}:v=1:a=1[v][a]')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', FUENTE, '-filter_complex', ''.join(fil), '-map', '[v]', '-map', '[a]',
                    '-c:v', 'libx264', '-preset', 'medium', '-crf', '16', '-pix_fmt', 'yuv420p', '-c:a', 'pcm_s16le',
                    'edicion/toma_limpia.mov'], check=True)


if __name__ == '__main__':
    ps = planos()
    print(f'{sum(b - a for a, b, _ in ps):.1f} s en {len(ps)} planos')
    print(' | '.join(' '.join(W[i]['w'] for i in g) for _, _, g in ps))
    if '--texto' not in sys.argv:
        montar(ps)
        json.dump([{'t0': a, 't1': b, 'palabras': [g[0], g[-1]], 'zoom': z} for a, b, g, z in ps],
                  open('edicion/planos_limpios.json', 'w', encoding='utf-8'), indent=1)
        print('-> edicion/toma_limpia.mov')
