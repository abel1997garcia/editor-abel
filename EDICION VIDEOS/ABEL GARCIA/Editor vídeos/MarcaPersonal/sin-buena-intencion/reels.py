"""HISTÓRICO (05/10/2026): sustituido por Editor vídeos/herramientas/reel_yapping.py (plantilla con título, 4:3, subtítulos y música).
Se conserva solo para rehacer los 3 reels entregados en 9:16 sin plantilla.
"""
"""Reels verticales a partir del vídeo largo (marca personal de Abel).

Cada reel es una lista de tramos [desde, hasta] en índices de palabra de edicion/tiempos.json (alineación forzada sobre
la toma), en el orden en que se oyen, con las palabras que sobran (muletillas, repeticiones) en «quitar».
Las palabras seguidas se agrupan en planos; entre planos el corte es seco y se alterna el encuadre (1,0 / 1,12) para
que el salto parezca un cambio de cámara. Pausas de más de PAUSA s dentro de un tramo también se cortan.

    python reels.py            -> out/reel_1.mp4 ... (1080x1920, 30 fps, -14 LUFS)
    python reels.py --texto    -> solo imprime el texto de cada reel y su duración
"""
import json, subprocess, sys
from pathlib import Path

TOMA = '../../Sin buena intención jamás obtendrás la bendición.mp4'
W = json.load(open('edicion/tiempos.json', encoding='utf-8'))
PW = json.load(open('edicion/transcripcion.json', encoding='utf-8'))['palabras']   # con la puntuación de Whisper
PRE, POST, PAUSA_DEF, COLA = .07, .12, .40, .40

REELS = {
    'reel_1_escoba': {
        # v2: sin «puedes hacer eso y puedes» ni «quiero es es», sin trocitos sueltos, pausas > 0,22 s fuera y final
        # en el final real de una frase («…ahí es cuando todo empieza a cobrar sentido», con pausa después)
        'tramos': [(2066, 2095), (2096, 2106), (2112, 2120), (2122, 2140), (1305, 1318), (1323, 1339), (2143, 2178),
                   (2186, 2195), (2004, 2008), (2012, 2014), (2016, 2061)],
        'quitar': set(), 'pausa': .22,
    },
    'reel_2_insuficiente': {
        'tramos': [(1157, 1166), (1180, 1191), (1195, 1219), (1141, 1153), (1135, 1139), (275, 319), (342, 357),
                   (1645, 1696), (1220, 1244)],
        'quitar': {1159, 1163, 1150, 1659, 1660, 1661, 1666, 1667, 1668, 1669, 1670, 1671, 1672, 1673, 1674, 1675, 1678},
    },
    'reel_3_dinero': {
        'tramos': [(802, 849), (696, 747), (616, 626), (628, 686)],
        'quitar': {818, 720, 650, 651, 654, 655, 656},
    },
}


def planos(reel):
    """[(t0, t1)] en segundos de la toma: palabras seguidas sin pausa larga forman un plano."""
    out, PAUSA = [], reel.get('pausa', PAUSA_DEF)
    for a, b in reel['tramos']:
        # un tramo acaba donde acaba la frase (feedback 05/10/2026: «vengo» sin «aquí», final a mitad de frase):
        # la puntuación de Whisper lo dice; el último tramo del reel, en final de frase (. ? !)
        fin = '.?!' if (a, b) == reel['tramos'][-1] else '.?!,;:'
        norm = lambda x: ''.join(c for c in x.lower() if c.isalnum())
        cand = [x for x in PW if abs(x['s'] - W[b]['s']) < .8 and norm(x['w']) == norm(W[b]['w'])] or PW
        p = min(cand, key=lambda x: abs(x['s'] - W[b]['s']))
        if not p['w'].rstrip('»"').endswith(tuple(fin)):
            print(f"AVISO: el tramo {a}-{b} acaba en «{W[b]['w']}» sin puntuación detrás (sigue: «{W[b + 1]['w']}»): revisa que la frase quede cerrada")
        grupo = []
        for i in range(a, b + 1):
            if i in reel['quitar']:
                if grupo: out.append(grupo); grupo = []
                continue
            if grupo and W[i]['s'] - W[grupo[-1]]['e'] > PAUSA:
                out.append(grupo); grupo = []
            grupo.append(i)
        if grupo: out.append(grupo)
    res = []
    for g in out:
        i0, i1 = g[0], g[-1]
        t0 = W[i0]['s'] - PRE
        if i0 > 0: t0 = max(t0, W[i0 - 1]['e'] + .02)          # sin arrastrar la palabra anterior
        t1 = W[i1]['e'] + POST
        if i1 + 1 < len(W): t1 = min(t1, W[i1 + 1]['s'] - .02)  # ni comerse la siguiente
        res.append([round(t0, 3), round(t1, 3), g])
    # el último plano respira: cola de COLA s (sin pisar la palabra siguiente de la toma)
    i1 = res[-1][2][-1]
    res[-1][1] = round(min(W[i1]['e'] + COLA, W[i1 + 1]['s'] - .02) if i1 + 1 < len(W) else W[i1]['e'] + COLA, 3)
    return [tuple(r) for r in res]


def centro_cara():
    """centro de la cara (mediana en 40 fotogramas) con YuNet, el detector que usa la skill (anim.py cortar)."""
    import cv2
    sys.path.insert(0, str(Path.home() / '.claude/skills/animaciones-horizontal-combinadas/scripts'))
    from cortar import modelo_cara
    cap = cv2.VideoCapture(TOMA)
    n = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    det = cv2.FaceDetectorYN.create(str(modelo_cara()), '', (1280, 720), 0.7, 0.3, 5)
    xs, ys = [], []
    for k in range(40):
        cap.set(cv2.CAP_PROP_POS_FRAMES, int(n * (k + .5) / 40))
        ok, f = cap.read()
        if not ok: continue
        _, caras = det.detect(f)
        if caras is not None and len(caras):
            x, y, w, h = max(caras, key=lambda c: c[2] * c[3])[:4]; xs.append(x + w / 2); ys.append(y + h / 2)
    xs.sort(); ys.sort()
    return xs[len(xs) // 2], ys[len(ys) // 2]


def montar(nombre, reel, cx, cy):
    ps = planos(reel)
    fil, n, z = [], len(ps), 1.12
    for k, (t0, t1, g) in enumerate(ps):
        # el encuadre cambia (1,0 <-> 1,12) solo en los cortes de contenido y en pausas largas; en las pausas cortas,
        # el mismo encuadre: cambiarlo cada 2 s haría bailar la imagen
        prev = ps[k - 1][2][-1] if k else None
        if k == 0 or g[0] != prev + 1 or W[g[0]]['s'] - W[prev]['e'] > .7: z = 1.0 if z != 1.0 else 1.12
        ch = 720 / z; cw = ch * 9 / 16
        x0 = min(max(cx - cw / 2, 0), 1280 - cw)
        y0 = min(max(cy - ch * .36, 0), 720 - ch)             # ojos hacia el tercio superior
        fil.append(f"[0:v]trim={t0}:{t1},setpts=PTS-STARTPTS,crop={cw:.1f}:{ch:.1f}:{x0:.1f}:{y0:.1f},"
                   f"scale=1080:1920:flags=lanczos,unsharp=5:5:0.6,setsar=1,fps=30[v{k}];")
        d = t1 - t0
        fil.append(f"[0:a]atrim={t0}:{t1},asetpts=PTS-STARTPTS,afade=t=in:d=0.008,afade=t=out:st={d - .008:.3f}:d=0.008[a{k}];")
    fil.append(''.join(f'[v{k}][a{k}]' for k in range(n)) + f'concat=n={n}:v=1:a=1[v][ab];')
    fil.append('[ab]loudnorm=I=-14:TP=-1.5:LRA=11,aresample=48000[a]')
    Path('out').mkdir(exist_ok=True)
    salida = f'out/{nombre}.mp4'
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', TOMA, '-filter_complex', ''.join(fil), '-map', '[v]', '-map', '[a]',
                    '-c:v', 'libx264', '-preset', 'slow', '-crf', '18', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '192k',
                    '-movflags', '+faststart', salida], check=True)
    return salida


if __name__ == '__main__':
    solo_texto = '--texto' in sys.argv
    cx, cy = (640, 300) if solo_texto else centro_cara()
    if not solo_texto: print(f'cara en x={cx:.0f} y={cy:.0f}')
    for nombre, reel in REELS.items():
        ps = planos(reel)
        dur = sum(t1 - t0 for t0, t1, _ in ps)
        print(f'\n== {nombre}: {dur:.1f} s en {len(ps)} planos')
        print(' | '.join(' '.join(W[i]['w'] for i in g) for _, _, g in ps))
        if not solo_texto: print('->', montar(nombre, reel, cx, cy))
