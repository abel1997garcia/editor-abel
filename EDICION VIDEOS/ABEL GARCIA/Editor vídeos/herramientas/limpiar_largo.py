"""Toma limpia de un vídeo largo horizontal de Abel (antes de animar).

    python limpiar_largo.py config.json           -> <salida>  (1920x1080, 30 fps, audio PCM)
    python limpiar_largo.py config.json --texto   -> texto final, duración y planos

config.json:
{ "fuente": "vídeo original", "tiempos": "edicion/tiempos.json (alineación de la toma)", "salida": "toma_limpia.mov",
  "gancho": [i0, i1],                  avance en frío: estas palabras abren el vídeo (y siguen en su sitio)
  "quitar": [i, [i0, i1], ...],        muletillas, repeticiones y tropiezos (índices o rangos)
  "zooms":  [[i0, i1], ...],           frases importantes: acercamiento de énfasis hacia él
  "intacto_desde": i }                 opcional: desde esa palabra no se corta nada (su cierre, con su entonación)
"""
import json, subprocess, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from reel_yapping import PAUSA, AIRE, MIN_PLANO, COLA, centro_cara

EMPUJE_PERIODO, EMPUJE = 40.0, .015   # acercamiento leve y continuo: 1,00 ↔ 1,03 (depende del tiempo del vídeo final)
ENFASIS = 1.18                        # zoom de énfasis hacia su cara
SILENCIO = .6                         # pausa mayor = silencio real: se recorta aunque deje un plano corto
ENTONACION = .7                       # plano más corto = conector suelto: se queda con su pausa


def indices(lista):
    out = set()
    for x in lista: out.update(range(x[0], x[1] + 1) if isinstance(x, list) else [x])
    return out


def planos(W, cfg):
    quitar, zoom = indices(cfg.get('quitar', [])), indices(cfg.get('zooms', []))
    a, b = cfg.get('gancho', [0, -1])
    orden = [i for i in [*range(a, b + 1), *range(len(W))] if i not in quitar]
    intacto = cfg.get('intacto_desde', len(W))      # desde esta palabra hasta el final no se corta nada (lo cierra él)
    fin_gancho = b - a + 1 - len([i for i in range(a, b + 1) if i in quitar])
    grupos, g = [], []
    for k, i in enumerate(orden):
        corte = g and (i != g[-1] + 1 or (W[i]['s'] - W[g[-1]]['e'] > PAUSA and i < intacto) or k == fin_gancho or (i in zoom) != (g[-1] in zoom))
        if corte: grupos.append(g); g = []
        g.append(i)
    grupos.append(g)
    dur = lambda g: W[g[-1]]['e'] - W[g[0]]['s']
    hueco = lambda i: W[i + 1]['s'] - W[i]['e']
    # un plano corto se une al vecino si la pausa es natural; un silencio real se recorta, salvo que deje un conector
    # suelto (< ENTONACION s: «pero… si no cambias», «así que… aplica ya»): esa pausa es de entonación y se respeta
    unible = lambda i, j, g: j == i + 1 and (hueco(i) <= SILENCIO or dur(g) < ENTONACION) and (i in zoom) == (j in zoom)
    k = 0
    while k < len(grupos):
        g = grupos[k]
        if dur(g) < MIN_PLANO:
            if k + 1 < len(grupos) and unible(g[-1], grupos[k + 1][0], g):
                grupos[k:k + 2] = [g + grupos[k + 1]]; continue
            if k > 0 and unible(grupos[k - 1][-1], g[0], g):
                grupos[k - 1:k + 1] = [grupos[k - 1] + g]; k -= 1; continue
        k += 1
    res = []
    for k, g in enumerate(grupos):
        i0, i1 = g[0], g[-1]
        t0 = W[i0]['s'] - AIRE
        if i0 > 0: t0 = max(t0, W[i0 - 1]['e'] + .02)
        cola = COLA if k == len(grupos) - 1 or (i1 == b and k + 1 < len(grupos) and grupos[k + 1][0] != b + 1) else AIRE
        t1 = W[i1]['e'] + cola
        if i1 + 1 < len(W): t1 = min(t1, W[i1 + 1]['s'] - .02)
        if i1 == len(W) - 1: t1 = cfg['fin']           # el final de la toma no se toca
        res.append((round(t0, 3), round(t1, 3), g, ENFASIS if i0 in zoom else 1.0))
    return res


def montar(cfg, ps):
    cx, fw, fh = centro_cara(cfg['fuente'])
    fil, T = [], 0.0
    for k, (t0, t1, g, ez) in enumerate(ps):
        d = t1 - t0
        z = f"({ez}*(1+{EMPUJE}+{EMPUJE}*sin(2*PI*({T:.3f}+in/30)/{EMPUJE_PERIODO})))"
        # recorte con precisión de subpíxel (perspective): escalar a píxeles enteros iba a golpecitos.
        # El énfasis se ancla en su cara (x) y en el tercio superior (y)
        x0, y0, w, h = f"{cx / fw:.3f}*(W-W/{z})", f"0.35*(H-H/{z})", f"W/{z}", f"H/{z}"
        fil.append(f"[0:v]trim={t0}:{t1},setpts=PTS-STARTPTS,fps=30,perspective="
                   f"x0='{x0}':y0='{y0}':x1='{x0}+{w}':y1='{y0}':x2='{x0}':y2='{y0}+{h}':x3='{x0}+{w}':y3='{y0}+{h}'"
                   f":interpolation=cubic:eval=frame,setsar=1[v{k}];")
        fil.append(f"[0:a]atrim={t0}:{t1},asetpts=PTS-STARTPTS,afade=t=in:d=0.01,afade=t=out:st={d - .01:.3f}:d=0.01[a{k}];")
        T += d
    n = len(ps)
    fil.append(''.join(f'[v{k}][a{k}]' for k in range(n)) + f'concat=n={n}:v=1:a=1[v][a]')
    filtro = Path(cfg['salida']).with_suffix('.filtro.txt'); filtro.write_text(''.join(fil), encoding='utf-8')   # Windows: orden demasiado larga
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', cfg['fuente'], '-/filter_complex', str(filtro), '-map', '[v]', '-map', '[a]',
                    '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '14', '-pix_fmt', 'yuv420p', '-c:a', 'pcm_s16le', cfg['salida']], check=True)


if __name__ == '__main__':
    ruta = Path(sys.argv[1]).resolve(); base = ruta.parent
    cfg = json.load(open(ruta, encoding='utf-8'))
    for k in ('fuente', 'tiempos', 'salida'): cfg[k] = str((base / cfg[k]).resolve())
    cfg['fin'] = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', cfg['fuente']],
                                      capture_output=True, text=True).stdout) - .05
    W = json.load(open(cfg['tiempos'], encoding='utf-8'))
    ps = planos(W, cfg)
    print(f'{sum(t1 - t0 for t0, t1, _, _ in ps):.1f} s en {len(ps)} planos ({sum(1 for p in ps if p[3] > 1)} con zoom de énfasis)')
    if '--texto' in sys.argv:
        print(' | '.join(('[Z] ' if z > 1 else '') + ' '.join(W[i]['w'] for i in g) for _, _, g, z in ps))
    else:
        montar(cfg, ps); json.dump([{'t0': a, 't1': b, 'palabras': [g[0], g[-1]], 'zoom': z} for a, b, g, z in ps],
                                   open(Path(cfg['salida']).with_suffix('.planos.json'), 'w', encoding='utf-8'), indent=1)
        print('->', cfg['salida'])
