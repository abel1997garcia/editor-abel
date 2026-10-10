"""Reels F3 · TABLERO de Abel (memoria reels-marca-personal; maquetas en MarcaPersonal/formato3/).

    python reel_tablero.py reels.json                  -> <salida>/<reel>.mp4 (1080x1920, 30 fps)
    python reel_tablero.py reels.json --texto          -> texto, duración, avisos y los tramos de tablero con sus palabras
    python reel_tablero.py reels.json --fotos 1,5.5    -> fotogramas sueltos para revisar (<salida>/_<reel>/f_*.png)
    python reel_tablero.py reels.json --solo c01 ...   -> solo ese reel

reels.json:
{ "fuente": "toma limpia del horizontal (su cara sin animaciones)", "tiempos": "trabajo/tiempos.json en el tiempo de esa toma",
  "salida": "carpeta",
  "reels": { "nombre": { "tramos": [["frase de inicio", "frase final", desde_s], ...],   en el orden en que se oyen
                         "quitar": [["frase", desde_s], ...],                             trocitos dentro de un tramo
                         "titulo": "EN MAYÚSCULAS (≤ 7 palabras)", "acento": "corona" (centro del tema) o "#hex",
                         "musica": "EMOCIONAL/tema.mp3", "desde": null (estribillo del catálogo),
                         "escenas": "c01.js",                                             gráficos del tablero
                         "modos": null | [[t, "tablero"|"grande"], ...],                  por defecto se alternan solos
                         "formato": "F2", "imagenes": "imagenes" } } }                  F2 · imagen abajo (motor_f2.html; las fotos en img/)
F4 · él a pantalla completa en vertical (motor_f4.html): "formato": "F4", "imagenes", "titulo" (en minúsculas normales),
     "titulo_hasta": s, "apartados": [["1. …", "frase", desde], ...]; en escenas: imagen(), collage(), cta() (Referencias/formato4/analisis.md)
F5 · CASUAL, reels de guion grabados con el móvil (motor_f5.html): "formato": "F5", "titulo" (crudo, completa el hook; todo el reel).
     Como F4 en cortes y zooms, pero sin imágenes, sin escenas y sin efectos; subtítulos en una línea de ≤ 4 palabras.
Gancho en el tablero desde el segundo 0; después tablero ↔ él en grande cada 4–6 s, cambiando entre palabras.
Su voz va tal cual (a 1,10x, como todo el reel); la música 26 dB por debajo desde el estribillo; los efectos que
declaran las escenas (suena) con la proporción del horizontal.
"""
import json, math, os, shutil, subprocess, sys
from pathlib import Path
import numpy as np
AQUI = Path(__file__).resolve().parent
sys.path[:0] = [str(AQUI), str(AQUI / 'pizarra')]
from reel_yapping import planos, VELOCIDAD, MUSICA, MUSICA_IN, MUSICA_OUT, AIRE, MUSICA_DB, COLA_FINAL, FUNDIDO, rellenos, ajustar_finales, estribillo, voz_lufs, centro_cara
from ventanas import buscar

TAB = AQUI / 'tablero'
SON = AQUI / 'sonidos'
CENTROS = {'raiz': '#C8372D', 'sacro': '#E06A1B', 'plexo': '#C99A00', 'corazon': '#1E7A46', 'garganta': '#1D7FD1', 'ojo': '#3F3FB5', 'corona': '#7A3FC4'}
FW, FH, SR = 1280, 720, 48000
TRAMO_MIN, TRAMO_OBJ, TRAMO_MAX = 2.8, 3.6, 4.8      # tablero ↔ él cada 3–4,5 s (Abel 08/10: «muy pausado»)
GANCHO_MIN = 3.5                                       # el gancho se queda en el tablero al menos esto


def indices(W, reel):
    tr = []
    for ini, fin, desde in reel['tramos']:
        a, _ = buscar(W, ini, desde); _, b = buscar(W, fin, W[a]['s']); tr.append([a, b])
    q = []
    for frase, desde in reel.get('quitar', []):
        a, b = buscar(W, frase, desde); q += list(range(a, b + 1))
    return {'tramos': tr, 'quitar': q}


def palabras(W, ps, pads):
    out, T = [], 0.0
    for (t0, t1, g), pd in zip(ps, pads):
        out += [[W[i]['w'], round((T + W[i]['s'] - t0) / VELOCIDAD, 3), round((T + W[i]['e'] - t0) / VELOCIDAD, 3)] for i in g]
        T += t1 - t0 + pd
    return out


def modos_auto(PAL, dur):
    """tablero desde 0 con el gancho (hasta el final de su primera frase); luego se alterna en los huecos entre palabras"""
    hueco = lambda i: PAL[i][1] - PAL[i - 1][2]
    def corte(desde, lo, hi):
        cand = [i for i in range(1, len(PAL)) if desde + lo <= PAL[i][1] <= desde + hi]
        if not cand: return None
        return PAL[max(cand, key=lambda i: hueco(i) - .05 * abs(PAL[i][1] - desde - TRAMO_OBJ))][1] - .05
    m, t, modo = [[0, 'tablero']], 0.0, 'tablero'
    t1 = corte(0, GANCHO_MIN, TRAMO_MAX + 1)
    while t1 and dur - t1 > 2.5:
        modo = 'grande' if modo == 'tablero' else 'tablero'; m.append([round(t1, 3), modo]); t = t1
        t1 = corte(t, TRAMO_MIN, TRAMO_MAX)
    return m


def titulo2(titulo, mayus=True):
    pal = (titulo.upper() if mayus else titulo).split()
    if len(pal) < 4: return [' '.join(pal)]
    k = min(range(1, len(pal)), key=lambda i: abs(len(' '.join(pal[:i])) - len(' '.join(pal[i:]))))
    return [' '.join(pal[:k]), ' '.join(pal[k:])]


def clip(cfg, ps, pads, tmp, vf):
    fil = []
    for k, ((t0, t1, g), pd) in enumerate(zip(ps, pads)):
        d = t1 - t0
        fo = FUNDIDO if pd > 0 else .01                       # corte pegado a la palabra siguiente: fundido algo más largo
        fil.append(f"[0:v]trim={t0}:{t1},setpts=PTS-STARTPTS,{vf},fps=30,setsar=1,tpad=stop_mode=clone:stop_duration={pd}[v{k}];"
                   f"[0:a]atrim={t0}:{t1},asetpts=PTS-STARTPTS,afade=t=in:d=0.01,afade=t=out:st={d - fo:.3f}:d={fo},apad=pad_dur={pd}[a{k}];")
    n = len(ps)
    fil.append(''.join(f'[v{k}][a{k}]' for k in range(n)) + f'concat=n={n}:v=1:a=1[vc][ac];'
               f'[vc]setpts=PTS/{VELOCIDAD},fps=30[v];[ac]atempo={VELOCIDAD},aresample={SR}[a]')
    (tmp / 'clip.txt').write_text(''.join(fil), encoding='utf-8')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', cfg['fuente'], '-/filter_complex', str(tmp / 'clip.txt'), '-map', '[v]', '-map', '[a]',
                    '-c:v', 'libx264', '-crf', '16', '-preset', 'veryfast', '-c:a', 'pcm_s16le', str(tmp / 'clip.mov')], check=True)
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(tmp / 'clip.mov'), '-vn', '-c:a', 'pcm_s16le', str(tmp / 'voz.wav')], check=True)
    fr = tmp / 'frames'; shutil.rmtree(fr, ignore_errors=True); fr.mkdir()
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(tmp / 'clip.mov'), '-q:v', '3', str(fr / '%05d.jpg')], check=True)


def colores_texto(tmp, hasta):
    """F4: color del título y de los subtítulos según el fondo real que tienen detrás (Abel: con fondo blanco, el texto blanco
    no se ve). Luminosidad media de la zona en los fotogramas: clara -> texto oscuro con halo claro; oscura -> blanco con sombra."""
    from PIL import Image
    fr = sorted((tmp / 'frames').glob('*.jpg'))
    def lum(sel, caja):
        v = []
        for f in sel:
            im = Image.open(f).convert('L').resize((270, 480)); x0, y0, x1, y1 = [c // 4 for c in caja]
            v.append(sum(im.crop((x0, y0, x1, y1)).getdata()) / ((x1 - x0) * (y1 - y0)) / 255)
        return sorted(v)[len(v) // 2] if v else 0
    tit = lum(fr[:max(1, int(hasta * 30)):10], (100, 150, 980, 380))
    sub = lum(fr[::30], (220, 1120, 860, 1260))
    oscuro = lambda l: {'color': '#141414', 'sombra': '0 2px 16px rgba(255,255,255,.75), 0 0 3px rgba(255,255,255,.6)'} if l > .6 else \
        {'color': '#ffffff', 'sombra': '0 3px 18px rgba(0,0,0,.65), 0 0 4px rgba(0,0,0,.6)'}
    print(f'  fondo: título {tit:.2f}, subtítulos {sub:.2f} (0 negro, 1 blanco)')
    return {'tit': oscuro(tit), 'sub': oscuro(sub)}


def efectos(sfx, dur, l_voz, ruta):
    import soundfile as sf
    cat = json.load(open(SON / 'sonidos.json', encoding='utf-8'))
    pista = np.zeros((int((dur + 3) * SR), 2))
    for t, nombre, vol in sfx:
        m = cat[nombre]; x, sr = sf.read(str(SON / m['archivo']), always_2d=True)
        if sr != SR: x = np.stack([np.interp(np.arange(0, len(x), sr / SR), np.arange(len(x)), x[:, c]) for c in range(x.shape[1])], 1)
        if x.shape[1] == 1: x = np.repeat(x, 2, 1)
        g = 10 ** ((m['gain_db'] + 20 * math.log10(max(1e-4, vol)) + (l_voz + 16)) / 20)   # como junto a la voz a −16 LUFS del horizontal
        i0 = max(0, int(round((t - (m['dur'] if m['ancla'] == 'fin' else m['pico'])) * SR)))
        n = min(len(x), len(pista) - i0); pista[i0:i0 + n] += g * x[:n]
    sf.write(str(ruta), pista[:int(dur * SR)], SR)


def hacer(cfg, nombre, reel, W, PW, cara, modo):
    ix = indices(W, reel); ps = planos(W, ix)
    ps = ajustar_finales(cfg['fuente'], W, ps)                       # también en --texto: los tiempos tienen que ser los del render
    pads = rellenos(W, ps)
    PAL = palabras(W, ps, pads); dur = round((sum(b - a for a, b, _ in ps) + sum(pads)) / VELOCIDAD, 3)
    f2, f5 = reel.get('formato') == 'F2', reel.get('formato') == 'F5'
    f4 = reel.get('formato') in ('F4', 'F5')                         # F2 · imagen abajo / F4 y F5 · él a pantalla completa: sin alternar
    if f5: reel = {**reel, 'titulo_hasta': dur}                       # F5: el título se queda todo el reel
    modos = [[0, 'tablero']] if f2 or f4 else reel.get('modos') or modos_auto(PAL, dur)
    print(f"\n== {nombre}: {dur:.1f} s a {VELOCIDAD}x · {len(ps)} planos · «{reel['titulo'].upper()}»")
    print(' | '.join(' '.join(W[i]['w'] for i in g) for _, _, g in ps))
    if dur < 50: print(f'  AVISO: dura {dur:.1f} s (mínimo 50–55 s)')
    sal = Path(cfg['salida']); tmp = sal / f'_{nombre}'; tmp.mkdir(parents=True, exist_ok=True)
    if modo == 'texto':
        lims = [a for a, _ in modos] + [dur]
        for (a, m), b in zip(modos, lims[1:]):
            print(f"  {m:8s} {a:6.2f}–{b:6.2f}  " + ' '.join(f"{w}@{s:.2f}" for w, s, _ in PAL if a - .05 <= s < b))
        return
    # imagen: "recorte_y" = hasta qué altura (px de la fuente) se puede ver (Abel: «que no se me vean los pantalones del pijama»);
    # "mejorar": limpieza de ruido suave, nitidez y algo de contraste/color. Con recorte se trabaja a resolución completa.
    y1 = reel.get('recorte_y', cfg.get('recorte_y'))
    fw, fh = (1920, int(y1) // 2 * 2) if y1 else (FW, FH)
    vf = (f'crop=1920:{fh}:0:0' if y1 else f'scale={FW}:{FH}')
    if f4:                                                            # F4: vertical 9:16 centrado en su cara (venga en horizontal o en vertical)
        sw, sh = cara[1], cara[2]; h = int(y1 or sh) // 2 * 2; w = min(sw, round(h * 9 / 16 / 2) * 2)
        x0 = int(min(max(cara[0] - w / 2, 0), sw - w)); vf = f'crop={w}:{h}:{x0}:0,scale=1080:1920:flags=lanczos'; fw, fh = 1080, 1920
    if reel.get('mejorar', cfg.get('mejorar')): vf += ',hqdn3d=1.5:1.5:4:4,unsharp=5:5:0.7:5:5:0.0,eq=contrast=1.05:saturation=1.08:gamma=1.02'
    firma = json.dumps([vf] + [[a, b, p] for (a, b, _), p in zip(ps, pads)])                    # el clip se rehace si cambian los tramos
    if not (tmp / 'clip.mov').exists() or modo == 'todo' or not (tmp / 'planos.json').exists() or (tmp / 'planos.json').read_text() != firma:
        clip(cfg, ps, pads, tmp, vf); (tmp / 'planos.json').write_text(firma)
    colores = colores_texto(tmp, reel.get('titulo_hasta', 6)) if f4 else {}
    acento = CENTROS.get(reel.get('acento', 'corona'), reel.get('acento', '#7A3FC4'))
    cx = 540 if f4 else cara[0] * fw / cara[1]
    cortes, T, z = [], 0.0, 1.08                                      # F4: acercamiento alterno 1,00/1,08 en cada salto de contenido
    for k, ((t0, t1, g), pd) in enumerate(zip(ps, pads)):
        if k == 0 or g[0] != ps[k - 1][2][-1] + 1 or T / VELOCIDAD - cortes[-1][0] >= 3:   # salto de contenido, o corte de silencio tras ≥ 3 s
            z = 1.0 if z != 1.0 else 1.08; cortes.append([round(T / VELOCIDAD, 3), z, 0])
        for i, j in zip(g, g[1:]):                                    # plano largo: acercamiento suave en una micropausa cada ~4,5 s
            tj = (T + W[j]['s'] - t0) / VELOCIDAD
            if W[j]['s'] - W[i]['e'] > .12 and tj - cortes[-1][0] >= 4.5 and (T + t1 - t0) / VELOCIDAD - tj > 1.5:
                z = 1.0 if z != 1.0 else 1.06; cortes.append([round(tj - .1, 3), z, 1])
        T += t1 - t0 + pd
    (tmp / 'datos.js').write_text(
        f"const PAL = {json.dumps(PAL, ensure_ascii=False)};\nconst MODOS = {json.dumps(modos)};\nconst TITULO = {json.dumps(titulo2(reel['titulo'], not f4), ensure_ascii=False)};\n"
        f"const ACENTO = '{acento}', FW = {fw}, FH = {fh}, FX = {cx:.1f}, DUR = {dur};\nconst COLORES = {json.dumps(colores)}, CORTES = {json.dumps(cortes)}, TITULO_HASTA = {reel.get('titulo_hasta', 6)}, APARTADOS = {json.dumps(reel.get('apartados', []), ensure_ascii=False)};\n", encoding='utf-8')
    shutil.copy(TAB / ('motor_f5.html' if f5 else 'motor_f4.html' if f4 else 'motor_f2.html' if f2 else 'motor.html'), tmp / 'motor.html'); shutil.copy(TAB / 'Montserrat-Variable.ttf', tmp)
    if reel.get('imagenes'):                                          # F2: las fotos (rutas relativas al reels.json)
        shutil.copytree(Path(cfg['_base']) / reel['imagenes'], tmp / 'img', dirs_exist_ok=True, ignore=shutil.ignore_patterns('*.mp4', '*.mov', '*.MOV'))
    for nom, (src, a, b) in reel.get('clips', {}).items():           # F3: vídeos de su vida -> clips/<nom>/ (JPG a 30 fps, sin sonido)
        d = tmp / 'clips' / nom
        if not d.exists():
            d.mkdir(parents=True)
            subprocess.run(['ffmpeg', '-v', 'error', '-ss', str(a), '-to', str(b), '-i', str(Path(cfg['_base']) / src), '-an', '-vf', 'fps=30,scale=720:-2',
                            '-q:v', '3', str(d / '%05d.jpg')], check=True)
        print(f'  clip {nom}: {len(list(d.glob("*.jpg")))} fotogramas')
    esc = Path(cfg['_base']) / reel['escenas'] if reel.get('escenas') else None
    (tmp / 'escenas.js').write_text(esc.read_text(encoding='utf-8') if esc and esc.exists() else 'ESC = () => {};', encoding='utf-8')
    node = ['node', str(TAB / 'grabar.mjs'), str(tmp)]
    if modo.startswith('fotos:'):
        subprocess.run(node + ['0', str(tmp), '--fotos', modo[6:]], check=True); print('  fotos ->', tmp); return
    subprocess.run(node + [str(dur), str(tmp / 'video.mp4'), '--sfx', str(tmp / 'sfx.json')], check=True)
    l_voz = voz_lufs(str(tmp / 'voz.wav'))
    efectos(json.load(open(tmp / 'sfx.json')), dur, l_voz, tmp / 'efectos.wav')
    ent = ['-i', str(tmp / 'video.mp4'), '-i', str(tmp / 'voz.wav'), '-i', str(tmp / 'efectos.wav')]
    fil = '[1:a][2:a]amix=inputs=2:duration=first:normalize=0[vf];'
    if reel.get('musica'):
        mus = MUSICA / reel['musica']; catm = json.load(open(MUSICA / 'catalogo.json', encoding='utf-8'))
        desde = reel.get('desde')
        if desde is None: desde = catm.get(reel['musica'], {}).get('estribillo') or estribillo(str(mus), dur)
        print(f"  música: {reel['musica']} desde {desde} s")
        ent += ['-ss', str(desde), '-i', str(mus)]
        fil += (f"[3:a]atrim=0:{dur:.3f},loudnorm=I={max(-30, min(-5, l_voz)):.1f}:TP=-2:LRA=11,volume={MUSICA_DB}dB,aresample={SR},"
                f"afade=t=in:d={MUSICA_IN},afade=t=out:st={dur - MUSICA_OUT:.3f}:d={MUSICA_OUT}[mu];[vf][mu]amix=inputs=2:duration=first:normalize=0[mx];")
    else:
        fil += '[vf]anull[mx];'
    fil += '[mx]alimiter=limit=0.891:level=0[a]'
    final = sal / f'{nombre}.mp4'
    subprocess.run(['ffmpeg', '-v', 'error', '-y', *ent, '-filter_complex', fil, '-map', '0:v', '-map', '[a]', '-c:v', 'libx264', '-preset', 'slow',
                    '-crf', '18', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '192k', '-ar', str(SR), '-movflags', '+faststart', '-t', str(dur), str(final)], check=True)
    print('  ->', final)


if __name__ == '__main__':
    ruta = Path(sys.argv[1]).resolve(); cfg = json.load(open(ruta, encoding='utf-8')); cfg['_base'] = str(ruta.parent)
    for k in ('fuente', 'tiempos', 'salida'): cfg[k] = str((ruta.parent / cfg[k]).resolve())
    W = json.load(open(cfg['tiempos'], encoding='utf-8')); W = W['palabras'] if isinstance(W, dict) else W
    a = sys.argv[2:]
    modo = 'texto' if '--texto' in a else ('fotos:' + a[a.index('--fotos') + 1]) if '--fotos' in a else 'todo' if '--rehacer' in a else 'render'
    solo = a[a.index('--solo') + 1:] if '--solo' in a else None
    cara = None if modo == 'texto' else centro_cara(cfg['fuente'])
    for n, r in cfg['reels'].items():
        if solo and n not in solo: continue
        hacer(cfg, n, r, W, None, cara, modo)
