"""Programa los reels en YouTube a través del flujo de n8n de Abel (n8n_programar_youtube.json).

    python programar_youtube.py              -> muestra el calendario que haría (no sube nada)
    python programar_youtube.py --subir      -> sube y programa de verdad
    python programar_youtube.py --simular    -> calendario como si todo tuviera su OK (no sube nada)
    python programar_youtube.py --ok adicciones c02   -> Abel da el OK a esos vídeos (mientras requiere_ok = true)
    python programar_youtube.py --subir --solo c01     -> solo los que contengan ese texto

Todo lo listo está en MarcaPersonal/REELS/, numerado en el orden de subida (Abel 12/10/2026: una sola carpeta, sin semanas):
  «NNN · PUBLICAR · <vídeo> · e<N>-g<N> · <título>.mp4» -> canal principal: 6 al día, a las HORAS_PUBLICAR
  «NNN · TRIAL · <vídeo> · e<N>-g<N> · <título>.mp4»    -> 3 canales de trials (Abel 16/10/2026), 3 al día cada uno = 9 al día:
        Abel García Clips (salida «trial» de n8n) 15-18-21 h · Abel Viralidad («instagram») 16-19-22 h · Club Unidad («club») 17-20-23 h
     Cada canal alimenta su flujo de repurpose.io → Instagram (trial reels). Los 9 de un día son de 9 vídeos DISTINTOS (las versiones
     de un mismo vídeo, mismo cuerpo con otro gancho, nunca el mismo día) y cada versión de un vídeo va a un canal distinto.
e<N>-g<N> = estructura y gancho dentro de ese vídeo. (La regla de 45 días se quitó el 16/10/2026: «no tiene sentido».)
Cada vídeo usa el .txt de al lado: 1.ª línea = título; el resto = descripción (sin repetir el título).
Rellena los huecos libres mezclando vídeos (nunca dos seguidos del mismo si hay de otros). Al programarse, el vídeo y su .txt pasan a REELS/programados/ (y a programados.json).
Configuración (URL del webhook y clave): youtube_config.json (no se comparte).
"""
import json, re, subprocess, sys, tempfile, datetime as dt
from pathlib import Path
from zoneinfo import ZoneInfo

AQUI = Path(__file__).resolve().parent
MP = AQUI.parents[1] / 'MarcaPersonal'
HORAS_PUBLICAR = ['14:00', '16:00', '18:00', '20:00', '22:00', '23:00', '24:00']   # Abel 12/10: 7 al día (cada ~2 h + una a las 23 h), hora de España (24:00 = medianoche, Latinoamérica)
CANALES_TRIAL = {'trial': ['15:00', '18:00', '21:00'],            # Abel García Clips
                 'instagram': ['16:00', '19:00', '22:00'],        # Abel Viralidad
                 'club': ['17:00', '20:00', '23:00']}             # Club Unidad  (Abel 16/10/2026: 3 por canal y día, uno por hora a Instagram)
POR_DIA_VIDEO = 2                                                  # variedad: como mucho 2 reels del mismo vídeo al día, y nunca en huecos seguidos
ZONA = ZoneInfo('Europe/Madrid')
SUBIDAS_DIA = {'trial': 3}                                         # canal trial ANTIGUO (sin verificar, corta las subidas). Ya no se usa: desde el 13/10/2026 los trials van al canal «instagram»
# Abel 13/10/2026: los TRIALS van al canal «YouTube · canal trial1» (salida «instagram» de n8n), verificado y sin límite de subidas;
# repurpose.io publica de ahí 3 al día en Instagram. El canal «trial» antiguo se borra tras el 15/10. Comparten calendario (no dos en la misma hora).
CANAL_TRIAL = 'instagram'
MAX_MB = 15                                               # límite habitual de subida a un webhook de n8n Cloud: si pesa más, se recomprime

REELS = MP / 'REELS'

def videos(tipo):
    """en orden de subida, MEZCLANDO vídeos (Abel 12/10/2026: «si pones todos de empezar, va a ser muy de lo mismo»): uno de cada
    vídeo por turno, empezando por el que tiene más pendientes; dentro de cada vídeo, por número"""
    from collections import defaultdict
    g = defaultdict(list)
    for v in sorted(v for v in REELS.glob('*.mp4') if f' · {tipo.upper()} · ' in v.name): g[v.name.split(' · ')[2]].append(v)
    out = []
    while any(g.values()):
        for k in sorted((k for k in g if g[k]), key=lambda k: -len(g[k])): out.append(g[k].pop(0))
    return out

def textos(v):
    t = v.with_suffix('.txt')
    if not t.exists(): return v.stem, ''
    s = t.read_text(encoding='utf-8').strip()
    titulo = s.split('\n')[0].strip()
    titulo = (titulo[:95] + '…') if len(titulo) > 96 else titulo
    # la descripción es el resto del .txt, SIN el título (Abel 12/10/2026: «que sea un complemento, no la misma frase»)
    return titulo, s.split('\n', 1)[1].strip() if '\n' in s else ''

def familia(nombre):
    """{'empezar-e9', 'empezar-g2'} a partir de «NNN · TIPO · empezar · e9-g2 · título»"""
    p = nombre.split(' · ')
    return {f'{p[2]}-{c}' for c in p[3].split('-')} if len(p) > 4 else set()

def huecos(horas, ocupados, minimo):
    d = minimo.date()
    while True:
        for h in horas:
            hh, mm = map(int, h.split(':'))
            t = dt.datetime(d.year, d.month, d.day, hh % 24, mm, tzinfo=ZONA) + dt.timedelta(days=hh // 24)
            if t < minimo: continue
            if t.isoformat() not in ocupados: yield t
        d += dt.timedelta(days=1)

def ligero(v):
    tmp = Path(tempfile.gettempdir()) / f'yt_{v.name[:3]}.mp4'     # nombre ASCII: curl en Windows no abre rutas con «·», «», tildes
    if v.stat().st_size / 1e6 <= MAX_MB:
        import shutil; shutil.copy(v, tmp); return tmp
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(v), '-c:v', 'libx264', '-crf', '23', '-preset', 'slow', '-maxrate', '3M', '-bufsize', '6M',
                    '-c:a', 'aac', '-b:a', '160k', '-movflags', '+faststart', str(tmp)], check=True)
    return tmp

def main():
    cfg = json.load(open(AQUI / 'youtube_config.json', encoding='utf-8'))
    est_p = AQUI / 'programados.json'
    hecho = json.load(open(est_p, encoding='utf-8')) if est_p.exists() else {}
    ocupados = {v['canal'] + v['cuando'] for v in hecho.values()}
    plan, pendientes = [], []
    ok_p = AQUI / 'ok.json'; oks = set(json.load(open(ok_p, encoding='utf-8'))) if ok_p.exists() else set()
    if '--ok' in sys.argv:                                        # Abel da el OK: --ok <trozo del nombre> ...
        nuevos = sys.argv[sys.argv.index('--ok') + 1:]
        for c in ('publicar', 'trial'):
            for v in videos(c):
                if any(x in v.name for x in nuevos): oks.add(v.name); print('OK de Abel:', v.name)
        json.dump(sorted(oks), open(ok_p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1); return
    solo = sys.argv[sys.argv.index('--solo') + 1:] if '--solo' in sys.argv else None
    if '--simular' in sys.argv and '--subir' not in sys.argv: cfg['requiere_ok'] = False   # calendario como si Abel hubiera dado el OK a todo (no sube nada)
    for carpeta, canal, horas in (('publicar', 'principal', HORAS_PUBLICAR),):
        minimo = dt.datetime.now(ZONA) + dt.timedelta(hours=1 if cfg.get('requiere_ok', True) else 24)   # automático: ≥ 24 h de margen para poder quitarlo
        if cfg.get('desde'): minimo = max(minimo, dt.datetime.fromisoformat(cfg['desde']).replace(tzinfo=ZONA))   # no antes de esta fecha
        gen = huecos(horas, {o[len(canal):] for o in ocupados if o.startswith(canal)}, minimo)
        pool = [next(gen) for _ in range(len(horas) * 400)]
        fechas = [(familia(k), dt.datetime.fromisoformat(x['cuando'])) for k, x in hecho.items()] + [(familia(v.name), t) for v, _, t in plan]
        vid = lambda f: next(iter(f)).rsplit('-', 1)[0] if f else None
        mismo = [(vid(f), u) for f, u in fechas]
        for v in videos(carpeta):
            clave = v.name
            if clave in hecho: continue
            if cfg.get('requiere_ok', True) and clave not in oks: pendientes.append(clave); continue
            if solo and not any(x in v.name for x in solo): continue
            fam = familia(v.name)
            yo = vid(fam)
            def cabe(t):
                if yo:
                    hoy = [u for w, u in mismo if w == yo and u.date() == t.date()]
                    if len(hoy) >= POR_DIA_VIDEO or any(abs((t - u).total_seconds()) < 2.5 * 3600 for w, u in mismo if w == yo): return False
                return True
            t = next(t for t in pool if cabe(t))
            pool.remove(t); fechas.append((fam, t)); mismo.append((yo, t)); plan.append((v, canal, t))
    # TRIALS: 9 huecos al día (3 canales × 3 horas), en orden de hora
    minimo = dt.datetime.now(ZONA) + dt.timedelta(hours=1 if cfg.get('requiere_ok', True) else 24)
    if cfg.get('desde'): minimo = max(minimo, dt.datetime.fromisoformat(cfg['desde']).replace(tzinfo=ZONA))
    pool = []
    for c, hs in CANALES_TRIAL.items():
        gen = huecos(hs, {o[len(c):] for o in ocupados if o.startswith(c)}, minimo)
        pool += [(t, c) for t in (next(gen) for _ in range(len(hs) * 120))]
    pool.sort()
    vid_de = lambda n: n.split(' · ')[2] if len(n.split(' · ')) > 3 else n
    usado = [(vid_de(k), dt.datetime.fromisoformat(x['cuando']).astimezone(ZONA).date(), x['canal']) for k, x in hecho.items() if x['canal'] in CANALES_TRIAL]
    for v in videos('trial'):
        if v.name in hecho: continue
        if cfg.get('requiere_ok', True) and v.name not in oks: pendientes.append(v.name); continue
        if solo and not any(x in v.name for x in solo): continue
        yo = vid_de(v.name)
        libre = [(t, c) for t, c in pool if not any(w == yo and d == t.date() for w, d, _ in usado)]   # NUNCA dos versiones del mismo vídeo el mismo día
        canales_ya = {c for w, _, c in usado if w == yo}
        t, c = next(((t, c) for t, c in libre if c not in canales_ya), libre[0])                   # cada versión, a un canal distinto (si quedan)
        pool.remove((t, c)); usado.append((yo, t.date(), c)); plan.append((v, c, t))
    plan.sort(key=lambda x: x[2])
    subir = '--subir' in sys.argv
    for v, canal, t in plan:
        titulo, desc = textos(v)
        print(f'{canal:9s} {t:%a %d/%m %H:%M}  {v.name}')
        if not subir: continue
        hoy = dt.datetime.now(ZONA).date().isoformat()
        if sum(1 for x in hecho.values() if x['canal'] == canal and x.get('subido', '')[:10] == hoy) >= SUBIDAS_DIA.get(canal, 99):
            print(f'   (hoy ya van {SUBIDAS_DIA[canal]} subidas al canal {canal}: se sube otro día)'); continue
        f = ligero(v)
        r = subprocess.run(['curl', '-s', '-f', '--show-error', '-X', 'POST', cfg['webhook'], '-H', f"{cfg['cabecera']}: {cfg['clave']}",
                            '-F', f'video=@{f};type=video/mp4', '-F', f'canal={canal}', '-F', f'titulo={titulo}',
                            '-F', f'descripcion={desc}', '-F', f'publicar_en={t.astimezone(dt.timezone.utc):%Y-%m-%dT%H:%M:%SZ}'],
                           capture_output=True, text=True)
        # sin «"ok":true» no se ha subido (13/10/2026: YouTube devolvió uploadLimitExceeded y n8n respondió vacío)
        if r.returncode or '"ok":true' not in r.stdout.replace(' ', ''):
            print('   ERROR al subir (¿límite de subidas de YouTube?):', r.stderr or r.stdout or 'respuesta vacía'); break
        hecho[v.name] = {'canal': canal, 'cuando': t.isoformat(), 'respuesta': r.stdout.strip(), 'subido': dt.datetime.now(ZONA).isoformat()}
        json.dump(hecho, open(est_p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
        (REELS / 'programados').mkdir(exist_ok=True)
        for x in (v, v.with_suffix('.txt')):
            if x.exists(): x.rename(REELS / 'programados' / x.name)
        print('   programado', r.stdout.strip())
    if pendientes: print('\nEsperando el OK de Abel (' + str(len(pendientes)) + '):', *pendientes, sep='\n  ')
    if not plan: print('Nada listo para programar.')
    elif not subir: print('\n(Solo calendario. Para subir de verdad: --subir)')

if __name__ == '__main__':
    main()
