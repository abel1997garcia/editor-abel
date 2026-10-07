"""Toma limpia v3 para el vídeo largo: su grabación TAL CUAL (estructura y tamaño originales) y un gancho en frío.

Reglas de Abel (memoria estilo-videos-largos-stickman):
- La grabación se respeta: pantalla partida, él a la izquierda y lo que explica a la derecha, al tamaño original.
  Nada de recortar ni centrar su cara. Solo un acercamiento muy leve y continuo (1,00–1,03) para darle vida; como
  depende del tiempo del vídeo final y no del plano, no salta en los cortes.
- La primera frase tiene que enganchar: se abre con GANCHO (su frase más potente) y después empieza el vídeo.
Corte por palabras (edicion/tiempos.json, alineación de la toma); las líneas «~» del guion se quitan.
    python limpiar3.py          -> edicion/toma_limpia3.mov
    python limpiar3.py --texto  -> solo el texto y la duración
"""
import json, subprocess, sys

FUENTE = r'C:\Users\Clap\Downloads\Cómo Dejar Ir las Emociones .mp4'
W = json.load(open('edicion/tiempos.json', encoding='utf-8'))
PRE, POST, PAUSA, COLA = .07, .12, .30, .45
GANCHO = (314, 352)              # «Cuando tú sueltas del control, sueltas la mente… ya deja de afectarte a tu vida»
PERIODO, AMPLITUD = 40.0, .015   # acercamiento leve: 1,00 ↔ 1,03 en un ciclo de 40 s

quitadas = {w['frase'] for w in W if str(w['w']).startswith('~')}
cuerpo = [i for i, w in enumerate(W) if w['frase'] not in quitadas]
orden = list(range(GANCHO[0], GANCHO[1] + 1)) + cuerpo     # el gancho también sigue en su sitio (es un avance)


def planos():
    grupos, g = [], []
    for k, i in enumerate(orden):
        if g and (i != g[-1] + 1 or W[i]['s'] - W[g[-1]]['e'] > PAUSA or k == GANCHO[1] - GANCHO[0] + 1):
            grupos.append(g); g = []
        g.append(i)
    grupos.append(g)
    res = []
    for k, g in enumerate(grupos):
        i0, i1 = g[0], g[-1]
        t0 = W[i0]['s'] - PRE
        if i0 > 0: t0 = max(t0, W[i0 - 1]['e'] + .02)
        fin_gancho = i1 == GANCHO[1] and k < len(grupos) - 1 and grupos[k + 1][0] != GANCHO[1] + 1
        t1 = W[i1]['e'] + (COLA if k == len(grupos) - 1 or fin_gancho else POST)
        if i1 + 1 < len(W): t1 = min(t1, W[i1 + 1]['s'] - .02)
        res.append((round(t0, 3), round(t1, 3), g))
    return res


def montar(ps):
    fil, T = [], 0.0
    for k, (t0, t1, g) in enumerate(ps):
        d = t1 - t0
        z = f"(1+{AMPLITUD}+{AMPLITUD}*sin(2*PI*({T:.3f}+t)/{PERIODO}))"
        fil.append(f"[0:v]trim={t0}:{t1},setpts=PTS-STARTPTS,fps=30,"
                   f"scale=w='trunc(1920*{z}/2)*2':h='trunc(1080*{z}/2)*2':eval=frame:flags=lanczos,crop=1920:1080,setsar=1[v{k}];")
        fil.append(f"[0:a]atrim={t0}:{t1},asetpts=PTS-STARTPTS,afade=t=in:d=0.008,afade=t=out:st={d - .008:.3f}:d=0.008[a{k}];")
        T += d
    n = len(ps)
    fil.append(''.join(f'[v{k}][a{k}]' for k in range(n)) + f'concat=n={n}:v=1:a=1[v][a]')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', FUENTE, '-filter_complex', ''.join(fil), '-map', '[v]', '-map', '[a]',
                    '-c:v', 'libx264', '-preset', 'medium', '-crf', '16', '-pix_fmt', 'yuv420p', '-c:a', 'pcm_s16le',
                    'edicion/toma_limpia3.mov'], check=True)


if __name__ == '__main__':
    ps = planos()
    print(f'{sum(b - a for a, b, _ in ps):.1f} s en {len(ps)} planos')
    print(' | '.join(' '.join(W[i]['w'] for i in g) for _, _, g in ps)[:600])
    if '--texto' not in sys.argv:
        montar(ps); print('-> edicion/toma_limpia3.mov')
