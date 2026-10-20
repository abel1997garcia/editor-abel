"""PASO 3 del proceso rápido: con el AUDIO YA APROBADO (montar.py → edl.json), corta el VÍDEO por los mismos fotogramas y lo monta
TODO en UNA sola pasada de ffmpeg: cortes + velocidad + nitidez suave + título + subtítulos (tiempos exactos de cada isla) + fotos
(solo si el plan las trae: cuando habla de su historia) + música. Sin navegador, sin zoom (Abel 15/10/2026).

    python herramientas/rapido/render.py <carpeta> [reel ...]      → <carpeta>/out_rapido/<reel>/<reel>.mp4
"""
import json, re, subprocess, sys
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageOps
AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parent))
from reel_tablero import titulo2, corrige_texto, VOZ_LUFS
from mejora_imagen import filtro
import capa_viral
from reel_yapping import tam_ass, MUSICA, MUSICA_IN, MUSICA_OUT, MUSICA_DB, estribillo, ganancia_musica, voz_lufs

FUENTE = AQUI.parent / 'fuentes' / 'Montserrat-ExtraBold.ttf'          # título (800, como siempre)
FUENTE_SUB = AQUI.parent / 'fuentes' / 'Montserrat-Black.ttf'         # subtítulos (900, como en los reels anteriores)
SUB_NOMBRE = 'Montserrat Black'
# Abel 19/10/2026: TODAS las versiones (PUBLICAR y TRIAL) con los subtítulos y la imagen IDÉNTICOS al reel que se publica
# («coge los mismos subtítulos, la misma tipografía, el mismo tamaño, todo»): entre versiones solo cambian gancho, título y música
ESTILOS = [('Montserrat-ExtraBold.ttf', 'Montserrat-Black.ttf', 'Montserrat Black', '')]
W_, H_ = 1080, 1920
CX, ANCHO = 800, 400                     # zona libre a la derecha: subtítulos centrados ahí, máx. 400 px y 80 px de margen al borde (Instagram recorta)
CORTAS = set('de del a al el la lo los las que y o en un una con por para su tu mi se te me le es ni sin'.split())
PROPIOS = {'fulano', 'mengano', 'rubius', 'siroko', 'gijón', 'gijon', 'youtube', 'instagram', 'tiktok', 'clash', 'royale', 'clap', 'abel', 'españa', 'australia', 'madrid'}
nz = lambda w: re.sub(r'[^a-z0-9ñ]', '', str(w).lower().translate(str.maketrans('áéíóúü', 'aeiouu')))


def franja(fuente):
    """filas donde empieza y acaba la franja de vídeo dentro de la plantilla blanca (primer fotograma)"""
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-ss', '1', '-i', str(fuente), '-frames:v', '1', '-vf', f'scale={W_}:{H_}', '-f', 'rawvideo', '-pix_fmt', 'gray', '-'],
                         capture_output=True).stdout
    a = np.frombuffer(raw, np.uint8).reshape(H_, W_)[:, ::8].mean(1); filas = np.where(a < 235)[0]
    return (int(filas[0]), int(filas[-1]) + 1) if len(filas) else (557, 1348)


def mayusculas(pal):
    for k, p in enumerate(pal):
        w = str(p[0]); base = re.sub(r'[^\wáéíóúñü]', '', w.lower())
        if k == 0 or str(pal[k - 1][0]).rstrip().endswith(('.', '?', '!', '…')) or base in PROPIOS: p[0] = w[:1].upper() + w[1:]
        elif w[:1].isupper() and not w.isupper(): p[0] = w[:1].lower() + w[1:]
    return pal


def bloques(pal, maxp=3, maxc=18):
    """3 palabras / 18 letras como mucho (abajo, en TABLET e HISTORIA: 5 / 30, en una línea); nunca cruza un punto ni una frase nueva; nunca acaba en palabra corta; ninguna corta sola"""
    junto = []
    for w in pal:                                             # «100 %», «200 €»: el número y su signo, siempre en el mismo bloque
        if junto and str(w[0]).strip(',.') in ('%', '€'): junto[-1] = [junto[-1][0] + ' ' + w[0], junto[-1][1], w[2]]
        else: junto.append(list(w))
    pal = junto
    out, i, fin = [], 0, []
    nueva = lambda k: (str(pal[k][0])[:1].isupper() and nz(pal[k][0]) not in PROPIOS) or nz(pal[k][0]) in ('asi', 'porque', 'pero')   # un nombre propio no empieza frase
    while i < len(pal):
        j, txt = i, ''
        while j < len(pal) and j - i < maxp and len((txt + ' ' + pal[j][0]).strip()) <= maxc:
            txt = (txt + ' ' + pal[j][0]).strip(); j += 1
            if re.search(r'[.?!…,]$', pal[j - 1][0]) or (j < len(pal) and nueva(j)): break
        if j == i: txt, j = pal[i][0], i + 1
        while j - i > 1 and j < len(pal) and nz(pal[j - 1][0]) in CORTAS and not re.search(r'[.?!…,]$', pal[j - 1][0]) and not nueva(j):
            j -= 1; txt = ' '.join(txt.split()[:-1])
        out.append([txt.rstrip(',.'), pal[i][1], pal[j - 1][2]]); fin.append(bool(re.search(r'[.?!…]$', txt))); i = j
    q = 0
    while q + 1 < len(out):                                   # palabra corta sola → con la siguiente
        if q and fin[q] and ' ' not in out[q][0] and len(nz(out[q][0])) <= 3 and len(out[q - 1][0] + ' ' + out[q][0]) <= 24:   # …que acaba frase («fe.») → con la ANTERIOR
            out[q - 1] = [out[q - 1][0] + ' ' + out[q][0], out[q - 1][1], out[q][2]]; out.pop(q); fin.pop(q - 1); continue
        if ' ' not in out[q][0] and len(nz(out[q][0])) <= 3 and len(out[q][0] + ' ' + out[q + 1][0]) <= 24:
            out[q + 1] = [out[q][0] + ' ' + out[q + 1][0], out[q][1], out[q + 1][2]]; out.pop(q); fin.pop(q)
        else: q += 1
    return out


def ass_tiempo(t):
    t = max(0, t); h = int(t // 3600); m = int(t % 3600 // 60); s = t % 60
    return f'{h}:{m:02d}:{s:05.2f}'


def arranques(voz):
    """momentos (s del reel) en que ARRANCA la voz tras un silencio: ahí se cuadra cada subtítulo (Abel: «no van 100 % sincronizados»)"""
    import onda
    _, E = onda.envolvente(str(voz)); thr = np.percentile(E, 95) - 27
    return [k * .01 for k in range(3, len(E)) if E[k] > thr and all(E[k - 3:k] <= thr)], E, thr


_ENV = {}


def suave(E, k):
    """valle SUAVE entre dos palabras pegadas («callas la», «personal lo»): ≥ 4 dB por debajo de lo que suena a los dos lados"""
    return E[k] <= E[max(0, k - 4):k + 5].min() + .5 and E[max(0, k - 4):k].max() - E[k] >= 4 and E[k + 1:k + 5].max() - E[k] >= 4


def valle(t, antes=.30, despues=.08):
    """el mínimo local de la onda (frontera entre dos palabras) más cercano a t, buscando sobre todo hacia atrás"""
    E, thr = _ENV.get('E'), _ENV.get('thr')
    if E is None: return t
    k0, k1 = max(1, int((t - antes) / .01)), min(len(E) - 2, int((t + despues) / .01))
    cand = [k for k in range(k0, k1 + 1) if E[k] <= E[k - 1] and E[k] <= E[k + 1] and (E[k] < thr + 12 and E[k + 1] < E[min(len(E) - 1, k + 4)] or suave(E, k))]
    if not cand: return t
    k = min(cand, key=lambda k: abs(k * .01 - t) * (0.7 if k * .01 < t else 1.3))
    return k * .01


def subtitulos(bls, dur, y, fotos, ruta, ons=(), abajo=False):
    """abajo=True (TABLET e HISTORIA, Abel 19/10/2026): en la franja blanca, centrados, negros, UNA sola línea"""
    cx, ancho = (540, 900) if abajo else (CX, ANCHO)
    f = lambda sz: ImageFont.truetype(str(FUENTE_SUB if abajo else AQUI.parent / 'fuentes' / 'Montserrat-Medium.ttf'), sz)
    lineas, inis = [], []
    for k, (txt, t0, t1) in enumerate(bls):                                  # 1) el INICIO de cada bloque, cuadrado con la onda
        cerca = [o for o in ons if t0 - .18 <= o <= t0 + .14]                # si justo ahí arranca la voz (tras una pausa), el subtítulo va CON ella
        ini = min(cerca, key=lambda o: abs(o - t0)) - .03 if cerca else valle(t0) - .02   # a mitad de frase: el VALLE entre palabras más cercano
        if inis: ini = max(ini, inis[-1] + .15)                            # nunca antes que el anterior (+ 0,15 s para que se lea)
        E_, thr_ = _ENV.get('E'), _ENV.get('thr')
        if E_ is not None and inis:                                          # empieza EN MITAD de la voz (la 1.ª palabra de cada toma llega
            c = round((ini + .02) / .01)                                      # hasta 0,2 s antes: «Entonces», 092-tablet08) → al siguiente valle
            if E_[max(0, c - 2):c + 3].min() > thr_ + 14 and not any(suave(E_, q) for q in range(max(1, c - 2), c + 3)):
                sig = [q for q in range(c + 1, min(len(E_) - 5, c + 26)) if E_[q] <= E_[q - 1] and E_[q] <= E_[q + 1] and (E_[q] < thr_ + 12 or suave(E_, q))]
                if sig: ini = sig[0] * .01 - .02
        inis.append(max(0, ini))
    for k, (txt, t0, t1) in enumerate(bls):                                  # 2) cada bloque dura JUSTO hasta que entra el siguiente: sin huecos ni dos a la vez
        ini = inis[k]
        fin = inis[k + 1] if k + 1 < len(bls) and inis[k + 1] - (t1 + 1.2) < .01 else min(dur, t1 + 1.2) if k + 1 == len(bls) else min(inis[k + 1], t1 + 1.2)
        sz = 72 if abajo else 64
        while True:                                             # que quepa en 400 px (como mucho 3 líneas)
            pal_, ls, cur = txt.split(), [], ''
            for w in pal_:
                if f(sz).getlength((cur + ' ' + w).strip()) <= ancho: cur = (cur + ' ' + w).strip()
                else: ls.append(cur); cur = w
            ls.append(cur)
            if all(f(sz).getlength(l) <= ancho for l in ls) and (len(ls) <= (1 if abajo else 2) or sz <= (30 if abajo else 56)) or sz <= 30: break   # 2 líneas como mucho («la / información / ya» se leía mal)
            sz -= 2
        yy = y if abajo else y + (190 if any(a - .1 <= ini <= b for a, b in fotos) else 0)
        fs = round(sz * 1.24)                                   # el tamaño de ASS es la ALTURA de línea: ×1,24 = mismo tamaño que en los reels anteriores
        if abajo:                                               # TABLET / HISTORIA = los subtítulos del YAPPING de siempre (Abel 19/10/2026, opción C):
            lineas.append(f'Dialogue: 0,{ass_tiempo(ini)},{ass_tiempo(fin)},B,,0,0,0,,{{\\pos({cx},{yy})}}' + txt); continue   # Montserrat ExtraBold 51 px FIJO, negro puro, sin animación
        # NORMAL (Abel 19/10/2026): la tipografía de TABLET e HISTORIA (Montserrat fina en blanco y la palabra fuerte del bloque en Black)
        # con la entrada suave de las escenas (fundido + sube un poco). Nada más: ni colores ni animaciones que mareen.
        cands = [w for w in txt.split() if len(nz(w)) >= 5 and nz(w) not in CORTAS]
        clave = max(cands, key=lambda w: len(nz(w))) if cands else None
        marca = lambda l: ' '.join('{\\fnMontserrat Black}' + w + '{\\fnMontserrat Medium}' if w == clave else w for w in l.split())
        lineas.append(f'Dialogue: 0,{ass_tiempo(ini)},{ass_tiempo(fin)},S,,0,0,0,,{{\\move({cx},{yy + 16},{cx},{yy},0,200)\\fad(160,0)\\fs{fs}\\blur3}}' + '\\N'.join(marca(l) for l in ls))
    cab = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {W_}
PlayResY: {H_}
WrapStyle: 2

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: S,Montserrat Medium,64,&H00FFFFFF,&H00FFFFFF,&H70000000,&H80000000,0,0,0,0,100,100,0,0,1,3,2,5,0,0,0,1
Style: B,Montserrat ExtraBold,{tam_ass(51)},&H00000000,&H00000000,&H00FFFFFF,&H00FFFFFF,0,0,0,0,100,100,0,0,1,0,0,5,0,0,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    Path(ruta).write_text(cab + '\n'.join(lineas) + '\n', encoding='utf-8')


def png_titulo(titulo, b0, ruta):
    im = Image.new('RGBA', (W_, H_), (0, 0, 0, 0)); d = ImageDraw.Draw(im); f = ImageFont.truetype(str(FUENTE), 50)
    ls = titulo2(titulo); sz = 50                                     # SIEMPRE 2 líneas (Abel 16/10): si no cabe, letra más pequeña
    while sz > 30 and max(d.textlength(l, font=f) for l in ls) > W_ - 180: sz -= 1; f = ImageFont.truetype(str(FUENTE), sz)   # 90 px de margen a cada lado: Instagram a veces recorta los lados (Abel 19/10/2026)
    lh = round(sz * 1.24)
    y = b0 - 30 - lh * len(ls)
    for l in ls: d.text(((W_ - d.textlength(l, font=f)) / 2, y), l, font=f, fill=(17, 17, 17, 255)); y += lh
    im.save(ruta)


def png_foto(src, w, h, ruta):
    im = ImageOps.fit(Image.open(src).convert('RGB'), (w, h)) if (w, h) != (0, 0) else Image.open(src).convert('RGB')
    m = Image.new('L', (w, h), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, w - 1, h - 1), 22, fill=255); im = im.convert('RGBA'); im.putalpha(m)
    c = Image.new('RGBA', (w + 12, h + 12), (0, 0, 0, 0)); ImageDraw.Draw(c).rounded_rectangle((0, 0, w + 11, h + 11), 26, fill='white'); c.alpha_composite(im, (6, 6))
    c.save(ruta); return c.size


def en_reel(pal, frase, desde=0):
    f = [nz(x) for x in frase.split()]
    for k in range(len(pal)):
        if pal[k][1] >= desde - .5 and [nz(p[0]) for p in pal[k:k + len(f)]] == f: return pal[k][1], pal[k + len(f) - 1][2]
    sys.exit(f'foto: no encuentro «{frase}» en el reel')


if __name__ == '__main__':
    d = Path(sys.argv[1]); plan = json.loads((d / 'plan.json').read_text(encoding='utf-8'))
    fuente = d / 'fuente.mp4'; b0, b1 = franja(fuente); bc = (b0 + b1) // 2
    for nombre in (sys.argv[2:] or plan['reels']):
        tf, sf, SUB_NOMBRE, eq_extra = ESTILOS[list(plan['reels']).index(nombre) % len(ESTILOS)]
        FUENTE, FUENTE_SUB = AQUI.parent / 'fuentes' / tf, AQUI.parent / 'fuentes' / sf
        r = plan['reels'][nombre]; out = d / 'out_rapido' / nombre; e = json.loads((out / 'edl.json').read_text(encoding='utf-8'))
        V, dur = e['velocidad'], e['dur']
        pal = mayusculas(corrige_texto([list(p) for p in e['pal']], plan.get('corrige', [])))
        png_titulo(r['titulo'], b0, out / 'titulo.png')
        # FOTOS (solo si el plan las trae: cuando cuenta su historia)
        fotos, ent_f, ov = [], [], ''
        for k, (src, fr_in, fr_out, *op) in enumerate(plan.get('fotos', [])):
            op = op[0] if op else {}; w, h = op.get('w', 330), op.get('h', op.get('w', 330))
            t0 = en_reel(pal, fr_in)[0] - .1; t1 = en_reel(pal, fr_out, t0)[1] + op.get('mas', 0)
            fw, fh = png_foto(d / src, w, h, out / f'foto{k}.png'); fotos.append((t0, t1))
            ent_f += ['-loop', '1', '-t', f'{dur:.3f}', '-i', str(out / f'foto{k}.png')]
            ov += f"[{4 + k}:v]format=rgba,fade=t=in:st={t0:.3f}:d=0.15:alpha=1,fade=t=out:st={t1 - .15:.3f}:d=0.15:alpha=1[f{k}];[vt{k}][f{k}]overlay={CX - fw // 2}:{bc - 120 - fh // 2}:enable='between(t,{t0:.3f},{t1:.3f})'[vt{k + 1}];"
        ons, _ENV['E'], _ENV['thr'] = arranques(out / 'voz.wav')
        abajo = plan.get('estilo') in ('tablet', 'historia')
        subtitulos(bloques(pal, 5, 30) if abajo else bloques(pal), dur - e.get('cola', 0), (b1 + H_) // 2 - 220 if abajo else bc, fotos, out / 'subs.ass', ons, abajo)
        capa = capa_viral.preparar({**plan, **{k: r[k] for k in ('diapos', 'tablet') if k in r}}, pal, out, b0, b1, dur, 4 + len(fotos), en_reel)   # un reel puede llevar sus propias diapositivas   # TABLET / HISTORIA: la zona derecha (Abel 19/10/2026)
        # VÍDEO: los mismos trozos (fotogramas exactos) que el audio aprobado
        tr = e['trozos']; fil = ''
        for k, t in enumerate(tr):
            fil += f"[0:v]trim=start={t['a']:.5f}:end={t['b'] + t['pad']:.5f},setpts=PTS-STARTPTS[v{k}];"
        fil += ''.join(f'[v{k}]' for k in range(len(tr))) + f"concat=n={len(tr)}:v=1:a=0,setpts=PTS/{V},fps=30,scale={W_}:{H_},tpad=stop_mode=clone:stop_duration={e.get('cola', 0) + .1:.2f},"
        fil += f"{filtro(fuente, (b0, b1))}{eq_extra}[vb];[vb][2:v]overlay=0:0[vt0];" + ov
        subs = str(out / 'subs.ass').replace('\\', '/').replace(':', '\\:'); fdir = str(FUENTE.parent).replace('\\', '/').replace(':', '\\:')
        if capa: fil += f"[vt{len(fotos)}]null[vin];" + capa[1]
        fil += f"[{'vcapa' if capa else f'vt{len(fotos)}'}]ass='{subs}':fontsdir='{fdir}'[v];"
        # AUDIO: voz a −14 LUFS + música (cantada: 6 dB más baja) que se aparta
        l_voz = voz_lufs(str(out / 'voz.wav')); fil += f"[1:a]volume={VOZ_LUFS - l_voz:.2f}dB[vz];"
        ent_m = []
        if r.get('musica'):
            mus = MUSICA / r['musica']; cat = json.load(open(MUSICA / 'catalogo.json', encoding='utf-8')); info = cat.get(r['musica'], {})
            desde = info.get('estribillo') or estribillo(str(mus), dur)
            largo = info.get('dur') or float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', str(mus)], capture_output=True, text=True).stdout)
            desde = max(0, min(desde, largo - dur - 8))                          # que la canción NO se acabe antes que el reel (Cornfield Chase se quedaba sin música en el 58 s)
            objetivo = VOZ_LUFS + MUSICA_DB - (3 if info.get('voz') else 0) + plan.get('musica_db', 0)   # «musica_db» (plan.json): ajuste por vídeo (historia01: −3,5, Abel 19/10/2026)   # Abel 17/10: «la música está muy baja, hay canciones con volumen muy diferente»:
            ent_m = ['-ss', str(desde), '-i', str(mus)]                       # se IGUALA el trozo (loudnorm, rango 4 LU: las partes flojas de ICARUS ya no
            print(f'  música: {r["musica"][:40]} → {objetivo:.1f} LUFS, rango igualado')   # desaparecen) y las cantadas solo 3 dB más bajas (antes 6)
            fil += (f"[3:a]atrim=0:{dur:.3f},loudnorm=I={objetivo:.1f}:LRA=4:TP=-6,aresample=48000,afade=t=in:d={MUSICA_IN},afade=t=out:st={dur - MUSICA_OUT:.3f}:d={MUSICA_OUT}[mu];"
                    f"[vz][mu]amix=inputs=2:duration=first:normalize=0,alimiter=limit=0.891:level=0[a]")
        else: fil += "[vz]alimiter=limit=0.891:level=0[a]"
        (out / 'filtro.txt').write_text(fil, encoding='utf-8')
        ent = ['-i', str(fuente), '-i', str(out / 'voz.wav'), '-loop', '1', '-t', f'{dur:.3f}', '-i', str(out / 'titulo.png')]
        ent += ent_m if ent_m else ['-f', 'lavfi', '-t', '1', '-i', 'anullsrc']
        ent += ent_f + (capa[0] if capa else [])
        final = out / f'{nombre}.mp4'
        subprocess.run(['ffmpeg', '-v', 'error', '-y', *ent, '-/filter_complex', str(out / 'filtro.txt'), '-map', '[v]', '-map', '[a]',
                        '-c:v', 'libx264', '-crf', '18', '-preset', 'veryfast', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '192k',
                        '-t', f'{dur:.3f}', '-movflags', '+faststart', str(final)], check=True)
        # COMPROBACIÓN DE SUBTÍTULOS (Abel 16/10/2026: «recuerda revisar que los subtítulos se sincronicen bien»)
        E_, thr_ = _ENV['E'], _ENV['thr']; ev = []
        for l in (out / 'subs.ass').read_text(encoding='utf-8').splitlines():
            if l.startswith('Dialogue'):
                p_ = l.split(',', 9); seg = lambda x: (lambda h, m_, s_: int(h) * 3600 + int(m_) * 60 + float(s_))(*x.split(':'))
                ev.append((seg(p_[1]), seg(p_[2]), re.sub(r'\{[^}]*\}', '', p_[9]).replace(r'\N', ' ')))
        fuera_ = [(round(a_, 2), t_) for a_, b_, t_ in ev[1:] if E_[max(0, round((a_ + .02) / .01) - 2):round((a_ + .02) / .01) + 3].min() > thr_ + 14 and not any(suave(E_, k_) for k_ in range(max(1, round((a_ + .02) / .01) - 2), round((a_ + .02) / .01) + 3))]
        huecos_ = [round(b_, 2) for (a_, b_, t_), (c_, d_, u_) in zip(ev, ev[1:]) if c_ - b_ > .02]
        solap_ = [round(b_, 2) for (a_, b_, t_), (c_, d_, u_) in zip(ev, ev[1:]) if c_ < b_ - .005]
        print(f'-> {final}  · subtítulos: {len(ev)} bloques · fuera de su palabra: {fuera_ or "0 ✓"} · huecos: {huecos_ or "0 ✓"} · solapes: {solap_ or "0 ✓"}')
