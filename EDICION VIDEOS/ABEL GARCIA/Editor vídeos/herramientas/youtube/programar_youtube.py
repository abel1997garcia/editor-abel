"""Programa los reels en YouTube a través del flujo de n8n de Abel (n8n_programar_youtube.json).

    python programar_youtube.py              -> muestra el calendario que haría (no sube nada)
    python programar_youtube.py --subir      -> sube y programa de verdad
    python programar_youtube.py --ok adicciones c02   -> Abel da el OK a esos vídeos (mientras requiere_ok = true)
    python programar_youtube.py --subir --solo c01     -> solo los que contengan ese texto

· MarcaPersonal/publicar/semana_*/  -> canal principal: 5 al día, a las HORAS_PUBLICAR
· MarcaPersonal/trial/semana_*/     -> canal trial: 3 al día, a las HORAS_TRIAL
Cada vídeo usa el .txt de al lado: 1.ª línea = título (gancho), todo el texto = descripción.
Empieza mañana y rellena los huecos libres en orden (por semana y por día del nombre: lun, mar, mié…).
Lo ya programado queda en programados.json y no se vuelve a subir.
Configuración (URL del webhook y clave): youtube_config.json (no se comparte).
"""
import json, re, subprocess, sys, tempfile, datetime as dt
from pathlib import Path
from zoneinfo import ZoneInfo

AQUI = Path(__file__).resolve().parent
MP = AQUI.parents[1] / 'MarcaPersonal'
HORAS_PUBLICAR = ['16:00', '18:00', '20:00', '22:00', '24:00']   # Abel 08/10: 5 al día, hora de España (24:00 = medianoche, pensando en Latinoamérica)
HORAS_TRIAL = ['17:00', '19:00', '21:00']                         # 3 al día
ZONA = ZoneInfo('Europe/Madrid')
DIAS = ['lun', 'mar', 'mie', 'mié', 'jue', 'vie', 'sab', 'sáb', 'dom']
MAX_MB = 15                                               # límite habitual de subida a un webhook de n8n Cloud: si pesa más, se recomprime

def videos(carpeta):
    out = []
    for sem in sorted((MP / carpeta).glob('semana_*')):
        for v in sorted(sem.glob('*.mp4'), key=lambda p: (p.parent.name, DIAS.index(p.name.split('_')[0]) if p.name.split('_')[0] in DIAS else 9, p.name)):
            out.append(v)
    return out

def textos(v):
    t = v.with_suffix('.txt')
    if not t.exists(): return v.stem, ''
    s = t.read_text(encoding='utf-8').strip()
    titulo = s.split('\n')[0].strip()
    titulo = (titulo[:95] + '…') if len(titulo) > 96 else titulo
    return titulo, s

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
    if v.stat().st_size / 1e6 <= MAX_MB: return v
    tmp = Path(tempfile.gettempdir()) / ('yt_' + v.name)
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
                if any(x in v.name for x in nuevos): oks.add(str(v.relative_to(MP))); print('OK de Abel:', v.name)
        json.dump(sorted(oks), open(ok_p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1); return
    solo = sys.argv[sys.argv.index('--solo') + 1:] if '--solo' in sys.argv else None
    for carpeta, canal, horas in (('publicar', 'principal', HORAS_PUBLICAR), ('trial', 'trial', HORAS_TRIAL)):
        minimo = dt.datetime.now(ZONA) + dt.timedelta(hours=1 if cfg.get('requiere_ok', True) else 24)   # automático: ≥ 24 h de margen para poder quitarlo
        if cfg.get('desde'): minimo = max(minimo, dt.datetime.fromisoformat(cfg['desde']).replace(tzinfo=ZONA))   # no antes de esta fecha
        libres = huecos(horas, {o[len(canal):] for o in ocupados if o.startswith(canal)}, minimo)
        for v in videos(carpeta):
            clave = str(v.relative_to(MP))
            if clave in hecho: continue
            if cfg.get('requiere_ok', True) and clave not in oks: pendientes.append(clave); continue
            if solo and not any(x in v.name for x in solo): continue
            plan.append((v, canal, next(libres)))
    subir = '--subir' in sys.argv
    for v, canal, t in plan:
        titulo, desc = textos(v)
        print(f'{canal:9s} {t:%a %d/%m %H:%M}  {v.parent.name}/{v.name}  «{titulo}»')
        if not subir: continue
        f = ligero(v)
        r = subprocess.run(['curl', '-s', '-f', '--show-error', '-X', 'POST', cfg['webhook'], '-H', f"{cfg['cabecera']}: {cfg['clave']}",
                            '-F', f'video=@{f};type=video/mp4', '-F', f'canal={canal}', '-F', f'titulo={titulo}',
                            '-F', f'descripcion={desc}', '-F', f'publicar_en={t.astimezone(dt.timezone.utc):%Y-%m-%dT%H:%M:%SZ}'],
                           capture_output=True, text=True)
        if r.returncode: print('   ERROR al subir:', r.stderr or r.stdout); break
        hecho[str(v.relative_to(MP))] = {'canal': canal, 'cuando': t.isoformat(), 'respuesta': r.stdout.strip()}
        json.dump(hecho, open(est_p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
        print('   programado', r.stdout.strip())
    if pendientes: print('\nEsperando el OK de Abel (' + str(len(pendientes)) + '):', *pendientes, sep='\n  ')
    if not plan: print('Nada listo para programar.')
    elif not subir: print('\n(Solo calendario. Para subir de verdad: --subir)')

if __name__ == '__main__':
    main()
