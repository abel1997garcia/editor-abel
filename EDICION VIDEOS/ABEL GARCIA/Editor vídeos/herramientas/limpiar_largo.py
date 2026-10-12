"""Vídeo horizontal de Abel ya editado (estándar desde el 11/10/2026: sin animaciones de pizarra).
Quita silencios, errores y repeticiones, hace zoom de énfasis y pone FRASES CLAVE: pantalla blanca con letras negras, centradas
en la zona 4:3, mientras su voz sigue (rompen el patrón). Sin "frases" sale la toma limpia para animar (solo si Abel lo pide:
skill animaciones-horizontal-combinadas + herramientas/pizarra).

    python limpiar_largo.py config.json           -> <salida> (1920x1080, 30 fps) + <salida>.tiempos.json (palabras en el tiempo
                                                     del vídeo final) + <salida>.montaje.json (las frases, para reel_yapping)
    python limpiar_largo.py config.json --texto   -> texto final, duración, planos y frases

config.json:
{ "fuente": "vídeo original", "tiempos": "edicion/tiempos.json (alineación de la toma)", "salida": "<tema> - horizontal.mp4",
  "quitar": [i, [i0, i1], ...],        muletillas, repeticiones y tropiezos (índices o rangos)
  "zooms":  [[i0, i1], ...],           frases importantes: acercamiento de énfasis hacia él
  "intacto_desde": i,                  opcional: desde esa palabra no se corta nada (su cierre, con su entonación)
  "frases": [["Tú eres\\NTU NEGOCIO.", i0, i1], ...] }   frase clave mientras dice i0–i1: ≤ 22 caracteres por línea,
                                       \\N = salto, una parte en MAYÚSCULAS; 5–8 por vídeo
"""
import json, shutil, subprocess, sys, tempfile
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from reel_yapping import PAUSA, AIRE, MIN_PLANO, COLA, centro_cara, microcortes

EMPUJE_PERIODO, EMPUJE = 40.0, .015   # acercamiento leve y continuo: 1,00 ↔ 1,03 (depende del tiempo del vídeo final)
ENFASIS = 1.18                        # zoom de énfasis hacia su cara
SILENCIO = .6                         # pausa mayor = silencio real: se recorta aunque deje un plano corto
ENTONACION = .7                       # plano más corto = conector suelto: se queda con su pausa
FUENTE = Path(__file__).resolve().parent / 'fuentes/InterCita.ttf'
ts_ass = lambda s: f'{int(s // 3600)}:{int(s % 3600 // 60):02d}:{s % 60:05.2f}'
ASS = """[Script Info]
ScriptType: v4.00+
PlayResX: 1920
PlayResY: 1080
WrapStyle: 2

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Fondo,Inter Cita,10,&H00FFFFFF,&H00FFFFFF,&H00FFFFFF,&H00000000,0,0,0,0,100,100,0,0,1,0,0,7,0,0,0,1
Style: Frase,Inter Cita,140,&H00111111,&H00111111,&H00000000,&H00000000,0,0,0,0,100,100,-2,0,1,0,0,5,0,0,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
CAJA = r'{\an7\pos(0,0)\p1}m 0 0 l 1920 0 1920 1080 0 1080{\p0}'


def indices(lista):
    out = set()
    for x in lista: out.update(range(x[0], x[1] + 1) if isinstance(x, list) else [x])
    return out


def planos(W, cfg):
    quitar, zoom = indices(cfg.get('quitar', [])), indices(cfg.get('zooms', []))
    orden = [i for i in range(len(W)) if i not in quitar]      # en su orden: su gancho grabado no se toca (Abel, 11/10/2026)
    intacto = cfg.get('intacto_desde', len(W))      # desde esta palabra hasta el final no se corta nada (lo cierra él)
    grupos, g = [], []
    for k, i in enumerate(orden):
        corte = g and (i != g[-1] + 1 or (W[i]['s'] - W[g[-1]]['e'] > PAUSA and i < intacto) or (i in zoom) != (g[-1] in zoom))
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
        cola = COLA if k == len(grupos) - 1 else AIRE
        t1 = W[i1]['e'] + cola
        if i1 + 1 < len(W): t1 = min(t1, W[i1 + 1]['s'] - .02)
        if i1 == len(W) - 1: t1 = cfg['fin']           # el final de la toma no se toca
        res.append((round(t0, 3), round(t1, 3), g, ENFASIS if i0 in zoom else 1.0))
    return res


def tiempos_final(W, ps):
    """las palabras en el tiempo del vídeo final"""
    out, T = [], 0.0
    for t0, t1, g, _ in ps:
        out += [{'i': len(out) + k, 'w': W[i]['w'], 's': round(T + W[i]['s'] - t0, 3), 'e': round(T + W[i]['e'] - t0, 3), 'orig': i}
                for k, i in enumerate(g)]
        T += t1 - t0
    return out


def tarjetas(F, cfg):
    """[(t0, t1, texto)] en el tiempo final, mientras dice sus palabras: hasta la última + 0,6 s (mín. 2 s)"""
    res = []
    for texto, i0, i1 in cfg.get('frases', []):
        p = next(w for w in F if w['orig'] == i0); q = next(w for w in F[p['i']:] if w['orig'] == i1)
        t0 = p['s'] - .1; res.append((t0, max(q['e'] + .6, t0 + 2), texto))
    return res


def montar(cfg, ps, cartas):
    cx, fw, fh = centro_cara(cfg['fuente'])
    fil, T = [], 0.0
    for k, (t0, t1, g, ez) in enumerate(ps):
        d = t1 - t0
        vsrc, asrc, tr, atr = '[0:v]', '[0:a]', f'trim={t0}:{t1}', f'atrim={t0}:{t1}'
        z = f"({ez}*(1+{EMPUJE}+{EMPUJE}*sin(2*PI*({T:.3f}+in/30)/{EMPUJE_PERIODO})))"
        # recorte con precisión de subpíxel (perspective): escalar a píxeles enteros iba a golpecitos.
        # El énfasis se ancla en su cara (x) y en el tercio superior (y)
        x0, y0, w, h = f"{cx / fw:.3f}*(W-W/{z})", f"0.35*(H-H/{z})", f"W/{z}", f"H/{z}"
        fil.append(f"{vsrc}{tr},setpts=PTS-STARTPTS,fps=30,perspective="
                   f"x0='{x0}':y0='{y0}':x1='{x0}+{w}':y1='{y0}':x2='{x0}':y2='{y0}+{h}':x3='{x0}+{w}':y3='{y0}+{h}'"
                   f":interpolation=cubic:eval=frame,setsar=1[v{k}];")
        fil.append(f"{asrc}{atr},asetpts=PTS-STARTPTS,afade=t=in:d=0.01,afade=t=out:st={d - .01:.3f}:d=0.01[a{k}];")
        T += d
    n = len(ps)
    tmp = Path(tempfile.mkdtemp())                     # libass y ffmpeg sin acentos en la ruta
    fil.append(''.join(f'[v{k}][a{k}]' for k in range(n)) + f'concat=n={n}:v=1:a=1[{"vc" if cartas else "v"}][a]')
    if cartas:                                         # pantalla blanca (capa 0) + frase negra centrada (capa 1), corte seco
        (tmp / 'f.ass').write_text(ASS + ''.join(f'Dialogue: 0,{ts_ass(a)},{ts_ass(b)},Fondo,,0,0,0,,{CAJA}\n'
                                                 f'Dialogue: 1,{ts_ass(a)},{ts_ass(b)},Frase,,0,0,0,,{{\\pos(960,540)}}{t}\n'
                                                 for a, b, t in cartas), encoding='utf-8')
        shutil.copy(FUENTE, tmp / 'InterCita.ttf')
        fil.append(';[vc]subtitles=f.ass:fontsdir=.[v]')
    filtro = tmp / 'filtro.txt'; filtro.write_text(''.join(fil), encoding='utf-8')   # Windows: orden demasiado larga
    audio = ['-c:a', 'aac', '-b:a', '256k'] if cfg['salida'].lower().endswith('.mp4') else ['-c:a', 'pcm_s16le']
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', cfg['fuente'], '-/filter_complex', str(filtro), '-map', '[v]', '-map', '[a]',
                    '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '14', '-pix_fmt', 'yuv420p', *audio, cfg['salida']], check=True, cwd=tmp)
    shutil.rmtree(tmp, ignore_errors=True)


if __name__ == '__main__':
    ruta = Path(sys.argv[1]).resolve(); base = ruta.parent
    cfg = json.load(open(ruta, encoding='utf-8'))
    for k in ('fuente', 'tiempos', 'salida'): cfg[k] = str((base / cfg[k]).resolve())
    cfg['fin'] = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', cfg['fuente']],
                                      capture_output=True, text=True).stdout) - .05
    W = json.load(open(cfg['tiempos'], encoding='utf-8'))
    ps = microcortes(cfg['fuente'], W, planos(W, cfg), cfg.get('intacto_desde'))
    # cada corte cuadrado a fotogramas (30 fps): si no, el vídeo redondea cada trozo y, con cientos de microcortes, la voz se
    # desviaba hasta 1,8 s de .tiempos.json (12/10/2026) y los reels se cortaban mal
    ps = [(round(t0 * 30) / 30, round(t1 * 30) / 30, g, z) for t0, t1, g, z in ps if round(t1 * 30) > round(t0 * 30)]
    F = tiempos_final(W, ps); cartas = tarjetas(F, cfg)
    print(f'{sum(t1 - t0 for t0, t1, _, _ in ps):.1f} s en {len(ps)} planos ({sum(1 for p in ps if p[3] > 1)} con zoom de énfasis), {len(cartas)} frases')
    for a, b, t in cartas: print(f'  frase {a:7.1f}–{b:7.1f} s  {t}')
    if '--texto' in sys.argv:
        print(' | '.join(('[Z] ' if z > 1 else '') + ' '.join(W[i]['w'] for i in g) for _, _, g, z in ps))
    else:
        montar(cfg, ps, cartas); sal = Path(cfg['salida'])
        json.dump(F, open(sal.with_suffix('.tiempos.json'), 'w', encoding='utf-8'), ensure_ascii=False)
        json.dump({'fps': 30, 'planos': [{'tipo': 'anim', 'f0': round(a * 30), 'f1': round(b * 30)} for a, b, _ in cartas]},
                  open(sal.with_suffix('.montaje.json'), 'w', encoding='utf-8'))
        json.dump([{'t0': a, 't1': b, 'palabras': [g[0], g[-1]], 'zoom': z} for a, b, g, z in ps],
                  open(sal.with_suffix('.planos.json'), 'w', encoding='utf-8'), indent=1)
        print('->', cfg['salida'])
