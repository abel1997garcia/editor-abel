"""Monta el vídeo «El Reencuentro»: una escena por frase, motion graphics suaves, voz + música.

    python montar.py            (todo)
    python montar.py --hasta 40 (solo los primeros 40 s, para probar)
"""
import json, math, random, re, subprocess, sys, unicodedata
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps
from escenas import ESCENAS, F

AQUI = Path(__file__).parent
BASE = Path(r'C:\Users\Clap\Desktop\EDICION VIDEOS\MEDIUM ALLAN')
VOZ = r'C:\Users\Clap\Desktop\AUDIO BASE VIDEO EVENTO ALLAN.WAV'
MUSICA = r'C:\Users\Clap\Desktop\EDICION VIDEOS\MUSICA\ÉPICA\Hans Zimmer - Time (Inception) _ EPIC EMOTIONAL VERSION.mp3'
VF = r'C:\Users\Clap\AppData\Local\Google\Chrome\User Data\Profile 1\Extensions\jkkfeklkdokfnlfodkdafododleokdoa\4.2.1_0\Fonts\Montserrat\Montserrat-VariableFont_wght.ttf'
W, H, FPS, XF = 1920, 1080, 30, 0.5
SUAVE = (190, 215, 245)
TMP = AQUI / 'tmp'; TMP.mkdir(exist_ok=True)
HASTA = float(sys.argv[sys.argv.index('--hasta') + 1]) if '--hasta' in sys.argv else None


def fuente(t, p):
    f = ImageFont.truetype(VF, t)
    try: f.set_variation_by_axes([p])
    except Exception: pass
    return f


def norm(s):
    s = unicodedata.normalize('NFD', s.lower())
    return re.sub(r'[^a-z0-9 ]', '', ''.join(c for c in s if unicodedata.category(c) != 'Mn'))


# ---------- tiempos: cada escena empieza en su palabra ancla ----------
pal = json.loads((AQUI / 'palabras.json').read_text(encoding='utf-8'))
ws = [norm(w[0]) for w in pal]
fin_audio = pal[-1][2] + 1.2
pos = 0
for e in ESCENAS:
    if e['ancla'] is None:
        e['t'] = 0.0; continue
    a = norm(e['ancla']).split()
    for i in range(pos, len(ws) - len(a) + 1):
        if ws[i:i + len(a)] == a:
            e['t'] = max(0.0, pal[i][1] - 0.25); pos = i + 1; break
    else:
        sys.exit(f'No encuentro la ancla: {e["ancla"]}')
for i, e in enumerate(ESCENAS):
    e['fin'] = ESCENAS[i + 1]['t'] if i + 1 < len(ESCENAS) else fin_audio


# ---------- capas ----------
def fondo(semilla):
    im = Image.new('RGB', (W, H)); px = im.load()
    cx = .5 + .15 * math.sin(semilla)
    for y in range(H):
        for x in range(0, W, 4):
            k = max(0, 1 - math.hypot((x - W * cx) / W, (y - H * .25) / H) * 1.6)
            c = tuple(int(8 + (a - 8) * k * .55) for a in (40, 90, 170))
            for i in range(4):
                if x + i < W: px[x + i, y] = c
    capa = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(capa)
    random.seed(semilla)
    for _ in range(140):
        x, y, r = random.randint(0, W), random.randint(0, H), random.choice([1, 1, 2, 3])
        d.ellipse((x - r, y - r, x + r, y + r), fill=(200, 230, 255, random.randint(60, 180)))
    im = im.convert('RGBA'); im.alpha_composite(capa.filter(ImageFilter.GaussianBlur(1.2)))
    return im


FONDOS = [fondo(s) for s in range(4)]


def tarjeta(im, ruta, caja, rot=0, borde=14):
    x0, y0, w, h = caja
    f = ImageOps.fit(ImageOps.exif_transpose(Image.open(ruta)).convert('RGB'), (w, h), centering=(.5, .35))
    t = Image.new('RGBA', (w + 2 * borde, h + 2 * borde), (250, 250, 250, 255)); t.paste(f, (borde, borde))
    t = t.rotate(rot, expand=True, resample=Image.BICUBIC)
    s = Image.new('RGBA', t.size, (0, 0, 0, 0)); s.paste((0, 0, 0, 140), mask=t.split()[3])
    im.alpha_composite(s.filter(ImageFilter.GaussianBlur(18)), (x0 + 12, y0 + 22))
    im.alpha_composite(t, (x0, y0))


def brillo(im, caja, a=120):
    g = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ImageDraw.Draw(g).ellipse(caja, fill=(150, 200, 255, a))
    im.alpha_composite(g.filter(ImageFilter.GaussianBlur(90)))


def partir(txt, f, ancho):
    d = ImageDraw.Draw(Image.new('RGB', (1, 1))); out, l = [], ''
    for p in txt.split():
        if d.textlength((l + ' ' + p).strip(), font=f) <= ancho: l = (l + ' ' + p).strip()
        else: out.append(l); l = p
    return out + [l] if l else out


def capa_texto(bloques, cx, cy, ancho, alinear='c'):
    """bloques = [(texto, fuente, color)]. Devuelve RGBA a pantalla completa con sombra suave."""
    lineas = []
    for txt, f, col in bloques:
        if txt:
            lineas += [(l, f, col) for l in partir(txt, f, ancho)]
            lineas.append((None, None, 18))
    alto = sum(f.size + 14 if l else g for l, f, g in lineas)
    capa = Image.new('RGBA', (W, H), (0, 0, 0, 0)); sombra = capa.copy()
    d, ds = ImageDraw.Draw(capa), ImageDraw.Draw(sombra)
    y = cy - alto / 2
    for l, f, col in lineas:
        if l is None: y += col; continue
        w = d.textlength(l, font=f)
        x = cx - w / 2 if alinear == 'c' else cx
        ds.text((x + 3, y + 5), l, font=f, fill=(0, 0, 0, 190)); d.text((x, y), l, font=f, fill=col)
        y += f.size + 14
    sombra = sombra.filter(ImageFilter.GaussianBlur(9)); sombra.alpha_composite(capa)
    return sombra


LOGO = Image.open(BASE / 'Logotipo azul El Reencuentro.png').convert('RGBA'); LOGO.thumbnail((760, 430))
_m = Image.new('L', LOGO.size); _p, _q = LOGO.load(), _m.load()
for yy in range(LOGO.height):
    for xx in range(LOGO.width):
        r, g, b, a = _p[xx, yy]; _q[xx, yy] = min(a, max(r, g, b) * 2)
LOGO.putalpha(_m)
_p = LOGO.load()
for yy in range(int(LOGO.height * .62), LOGO.height):
    for xx in range(LOGO.width):
        r, g, b, a = _p[xx, yy]
        if a > 20: _p[xx, yy] = (255, 255, 255, a)


def capas(i, e):
    bg = FONDOS[i % 4].copy()
    G, P = fuente(76 if not e.get('grande') else 210, 700 if not e.get('grande') else 800), fuente(46, 400)
    blo = [(e.get('g'), G, (255, 255, 255)), (e.get('p'), P, SUAVE)]
    t = e['tipo']
    if t == 'texto':
        txt = capa_texto(blo, W / 2, H / 2, 1500)
    elif t == 'foto':
        if e.get('glow'): brillo(bg, (W / 2 - 430, 60, W / 2 + 430, 900))
        if e.get('lado') == 'izq':
            tarjeta(bg, e['foto'], (120, 170, 720, 720), rot=-3)
            txt = capa_texto([(e.get('g'), fuente(64, 700), (255, 255, 255)), (e.get('p'), P, SUAVE)], 1000, H / 2, 820, 'i')
        else:
            tarjeta(bg, e['foto'], (W // 2 - 270, 90, 540, 640), rot=random.Random(i).choice([-2, 2]))
            txt = capa_texto(blo, W / 2, 900, 1500)
    elif t == 'full':
        f = ImageOps.fit(ImageOps.exif_transpose(Image.open(e['foto'])).convert('RGB'), (W, H), centering=(.5, .3)).convert('RGBA')
        v = Image.new('L', (W, H)); dv = ImageDraw.Draw(v)
        for y in range(H): dv.line([(0, y), (W, y)], fill=int(90 + 120 * max(0, (y - H * .3) / (H * .7))))
        f.alpha_composite(Image.merge('RGBA', [Image.new('L', (W, H), 0)] * 3 + [v])); bg = f
        txt = capa_texto(blo, W / 2, 860, 1500)
    elif t == 'collage':
        pos = [(80, 110, -6), (1460, 90, 5), (90, 600, 4), (1450, 590, -4)]
        for n, (x, y, r) in zip(e['fotos'], pos):
            tarjeta(bg, F + n, (x, y, 360, 360), rot=r, borde=10)
        txt = capa_texto(blo, W / 2, H / 2, 900)
    elif t == 'sesiones':
        marco = Image.new('RGBA', (W, H), (0, 0, 0, 0)); dm = ImageDraw.Draw(marco)
        for k, x in enumerate((140, 1430)):
            dm.rounded_rectangle((x, 140, x + 350, 140 + 622), 18, outline=(190, 215, 245, 160), width=3, fill=(20, 40, 80, 120))
            dm.text((x + 70, 430), 'vídeo sesión', font=fuente(34, 500), fill=(190, 215, 245, 200))
        bg.alpha_composite(marco)
        txt = capa_texto(blo, W / 2, H / 2, 820)
    elif t == 'respira':
        txt = capa_texto(blo, W / 2, H / 2, 1200)
    elif t == 'logo':
        brillo(bg, (W / 2 - 500, 200, W / 2 + 500, 900), 55)
        txt = Image.new('RGBA', (W, H), (0, 0, 0, 0))
        if e.get('g'):
            txt.alpha_composite(capa_texto([(e['g'], G, (255, 255, 255))], W / 2, 300, 1500))
            txt.alpha_composite(LOGO, ((W - LOGO.width) // 2, 520))
        else:
            txt.alpha_composite(LOGO, ((W - LOGO.width) // 2, (H - LOGO.height) // 2))
    bg.convert('RGB').save(TMP / f'{i:02d}_bg.png'); txt.save(TMP / f'{i:02d}_tx.png')


CIRC = Image.new('RGBA', (1000, 1000), (0, 0, 0, 0))
for r, a in [(480, 50), (420, 80), (360, 120)]:
    ImageDraw.Draw(CIRC).ellipse((500 - r, 500 - r, 500 + r, 500 + r), outline=(180, 220, 255, a), width=6)
g = Image.new('RGBA', (1000, 1000), (0, 0, 0, 0)); ImageDraw.Draw(g).ellipse((160, 160, 840, 840), fill=(120, 180, 255, 110))
CIRC.alpha_composite(g.filter(ImageFilter.GaussianBlur(60))); CIRC.save(TMP / 'circulo.png')

escenas = [e for e in ESCENAS if HASTA is None or e['t'] < HASTA]
if '--maqueta' in sys.argv:
    from PIL import ImageFont as _F
    mini = []
    for i, e in enumerate(escenas):
        capas(i, e)
        im = Image.open(TMP / f'{i:02d}_bg.png').convert('RGBA')
        if e['tipo'] == 'respira':
            c = Image.open(TMP / 'circulo.png'); c = c.resize((700, 700)); im.alpha_composite(c, ((W - 700) // 2, (H - 700) // 2))
        im.alpha_composite(Image.open(TMP / f'{i:02d}_tx.png'))
        im = im.convert('RGB').resize((480, 270)); dd = ImageDraw.Draw(im)
        m, s = divmod(e['t'], 60)
        dd.rectangle((0, 0, 120, 26), fill=(0, 0, 0)); dd.text((6, 4), f'{i + 1:02d} · {int(m)}:{s:04.1f}', font=_F.truetype('arial.ttf', 16), fill='white')
        mini.append(im)
    cols = 4
    hoja = Image.new('RGB', (cols * 486, ((len(mini) + cols - 1) // cols) * 276), 'white')
    for i, im in enumerate(mini): hoja.paste(im, ((i % cols) * 486 + 3, (i // cols) * 276 + 3))
    hoja.save(AQUI / 'MAQUETA_todas_las_diapositivas.jpg', quality=88)
    print('maqueta', len(mini)); sys.exit()
clips = []
for i, e in enumerate(escenas):
    capas(i, e)
    fin = min(e['fin'], HASTA) if HASTA else e['fin']
    d = fin - e['t'] + (XF if i + 1 < len(escenas) else 0)
    zoom = 'scale=w=2016:h=1134,scale=w=\'2016*(1+0.04*t/{d})\':h=-2:eval=frame,crop=1920:1080'.format(d=d)
    if e['tipo'] == 'respira':
        a, b = (520, 900) if e['modo'] == 'in' else (900, 520)
        fc = (f"[0:v]{zoom}[b];[2:v]scale=w='{a}+({b}-{a})*min(t/{d * .85},1)':h=-2:eval=frame,format=rgba[c];"
              f"[b][c]overlay=x='(main_w-overlay_w)/2':y='(main_h-overlay_h)/2'[bc];"
              f"[1:v]format=rgba,fade=t=in:st={XF}:d=0.6:alpha=1,fade=t=out:st={max(0.1, d - XF - 0.35):.2f}:d=0.35:alpha=1[t];[bc][t]overlay=0:'14*(1-min(t/0.9,1))',format=yuv420p")
        ins = ['-loop', '1', '-t', f'{d}', '-i', str(TMP / f'{i:02d}_bg.png'), '-loop', '1', '-t', f'{d}', '-i', str(TMP / f'{i:02d}_tx.png'), '-loop', '1', '-t', f'{d}', '-i', str(TMP / 'circulo.png')]
    else:
        fc = (f"[0:v]{zoom}[b];[1:v]format=rgba,fade=t=in:st={XF}:d=0.6:alpha=1,fade=t=out:st={max(0.1, d - XF - 0.35):.2f}:d=0.35:alpha=1[t];"
              f"[b][t]overlay=0:'16*(1-min(t/1.0,1))',format=yuv420p")
        ins = ['-loop', '1', '-t', f'{d}', '-i', str(TMP / f'{i:02d}_bg.png'), '-loop', '1', '-t', f'{d}', '-i', str(TMP / f'{i:02d}_tx.png')]
    out = TMP / f'{i:02d}.mp4'
    subprocess.run(['ffmpeg', '-v', 'error', '-y', *ins, '-filter_complex', fc, '-r', str(FPS), '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18', '-t', f'{d}', str(out)], check=True)
    clips.append((out, e['t']))
    print(f'{i:02d} {e["t"]:6.1f}s {e["tipo"]:8} {e.get("g", "")}', flush=True)

# ---------- unir con fundidos + voz + música ----------
ins, fc, prev = [], '', '0:v'
for c, _ in clips: ins += ['-i', str(c)]
for k in range(1, len(clips)):
    fc += f'[{prev}][{k}:v]xfade=transition=fade:duration={XF}:offset={clips[k][1]:.3f}[v{k}];'
    prev = f'v{k}'
n = len(clips)
total = min(fin_audio, HASTA) if HASTA else fin_audio
resp_ini = next(e['t'] for e in ESCENAS if e['tipo'] == 'respira')
resp_fin = next(e['t'] for e in ESCENAS if e.get('ancla') == 'Estás en el')
fc += (f"[{n}:a]loudnorm=I=-16:TP=-1.5,atrim=0:{total}[voz];"
       f"[{n + 1}:a]atrim=0:{total},loudnorm=I=-30:TP=-6,"
       f"volume='if(between(t,{resp_ini},{resp_fin}),2.2,1)':eval=frame,afade=t=in:d=3,afade=t=out:st={total - 4}:d=4[mus];"
       f"[voz][mus]amix=inputs=2:duration=first:normalize=0[a]")
salida = AQUI / ('prueba_40s.mp4' if HASTA else 'EL_REENCUENTRO_presentacion.mp4')
subprocess.run(['ffmpeg', '-v', 'error', '-y', *ins, '-i', VOZ, '-i', MUSICA, '-filter_complex', fc,
                '-map', f'[{prev}]' if n > 1 else '0:v', '-map', '[a]', '-c:v', 'libx264', '-preset', 'medium', '-crf', '18',
                '-c:a', 'aac', '-b:a', '192k', '-t', f'{total}', str(salida)], check=True)
print('listo:', salida)
