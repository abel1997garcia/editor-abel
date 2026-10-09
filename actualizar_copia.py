"""Copia de seguridad del sistema de edición de Abel → este repositorio (GitHub) y, si se pide, un zip para USB.

    python actualizar_copia.py            → deja el repositorio igual que el ordenador (solo sistema: código, textos, skills, memoria…)
    python actualizar_copia.py --subir    → además hace commit y push a GitHub
    python actualizar_copia.py --usb      → además crea en el Escritorio PAQUETE_EDICION_ABEL_<fecha>.zip = repositorio + FOTOS MIAS

Qué NO se copia nunca:
- contraseñas y claves: settings.json de Claude, youtube_config.json, «CONTRASEÑAS…», .env;
- vídeos en bruto, renders y temporales (mp4/mov, out/, frames/, node_modules…);
- archivos de más de 45 MB.
Las fotos personales (FOTOS MIAS) van solo en el zip del USB, no a GitHub.
"""
import os, shutil, subprocess, sys, zipfile, datetime
from pathlib import Path

REPO = Path(__file__).resolve().parent
HOME = Path.home()
EV = HOME / 'Desktop' / 'EDICION VIDEOS'
CL = HOME / '.claude'
PROY = CL / 'projects'

# (origen, destino en el repo, modo) · modo «sistema» = filtra medios pesados; «todo» = copia entera (salvo secretos)
MAPA = [
    (EV / 'ABEL GARCIA' / 'Editor vídeos', 'EDICION VIDEOS/ABEL GARCIA/Editor vídeos', 'sistema'),
    (EV / 'FÁBRICA DE CONTENIDO', 'EDICION VIDEOS/FÁBRICA DE CONTENIDO', 'todo'),
    (EV / 'MUSICA', 'EDICION VIDEOS/MUSICA', 'todo'),
    (EV / 'IMAGENES', 'EDICION VIDEOS/IMAGENES', 'todo'),
    (EV / 'MEDIUM ALLAN', 'EDICION VIDEOS/MEDIUM ALLAN', 'sistema'),
    (CL / 'skills', 'skills', 'skills'),
    (CL / 'scheduled-tasks', 'tareas-programadas', 'todo'),
    (PROY / 'C--Users-Clap-Desktop-EDICION-VIDEOS-ABEL-GARCIA-Editor-v-deos' / 'memory', 'memoria/editor', 'todo'),
    (PROY / 'C--Users-Clap-Desktop-EDICION-VIDEOS-F-BRICA-DE-CONTENIDO' / 'memory', 'memoria/fabrica', 'todo'),
    (PROY / 'C--Users-Clap-Desktop-EDICION-VIDEOS-MEDIUM-ALLAN-Editor-Videos---Allan' / 'memory', 'memoria/medium-allan', 'todo'),
]
SUELTOS = ['LOGO-ABEL.png', 'FONDO-REELS.png', 'FONDO BLANCO TABLET.PNG', 'suscribe.png', 'SUSCRIBETE.mp4', 'MINIATURA BASE.psd', 'PROYECTO.psd']

SECRETOS = {'settings.json', 'settings.local.json', 'youtube_config.json', '.env', 'credentials.json', 'token.json'}
DIRS_FUERA = {'node_modules', '.git', '__pycache__', 'out', 'out_trial', 'frames', 'clips', '_f', '_ext2', '_ext3', '_extraidos',
              '_cortes', 'video-use', 'FOTOS MIAS', '.cache', 'trabajo_tmp'}
MEDIOS = {'.mp4', '.mov', '.mkv', '.avi', '.m4a', '.webm', '.mxf', '.wav', '.mp3', '.aac', '.flac'}
LIGEROS = {'herramientas', 'skills', 'skill', 'sonidos', 'tablero', 'fuentes'}       # aquí sí van audios cortos (efectos, fuentes)
MAX = 45 * 1024 * 1024


def secreto(p: Path):
    n = p.name.lower()
    return p.name in SECRETOS or 'contraseña' in n or 'contrasena' in n or 'password' in n


def vale(p: Path, modo):
    if secreto(p): return False
    try:
        if p.stat().st_size > MAX: return False
    except OSError: return False
    if modo == 'todo': return True
    partes = set(p.parts)
    if p.suffix.lower() in MEDIOS and not (partes & LIGEROS): return False
    if p.suffix.lower() in {'.mp4', '.mov'}: return p.stat().st_size < 3 * 1024 * 1024   # solo clips cortos de herramientas
    return True


def recorrer(origen: Path, modo):
    for raiz, dirs, archivos in os.walk(origen):
        dirs[:] = [d for d in dirs if d not in DIRS_FUERA and not (modo != 'todo' and d.startswith('_') and d not in {'_por-tema', '_plantillas', '_herramientas', '_instaladores', '_indice'})]
        for a in archivos:
            p = Path(raiz) / a
            if vale(p, modo): yield p


def espejo(origen: Path, destino: Path, modo):
    if not origen.exists(): print('  (no existe)', origen); return 0
    vistos, n = set(), 0
    for p in recorrer(origen, modo):
        rel = p.relative_to(origen); d = destino / rel; vistos.add(d)
        if not d.exists() or d.stat().st_size != p.stat().st_size or d.stat().st_mtime < p.stat().st_mtime - 1:
            d.parent.mkdir(parents=True, exist_ok=True); shutil.copy2(p, d); n += 1
    for raiz, _, archivos in os.walk(destino):                      # borrar lo que ya no existe en el ordenador
        for a in archivos:
            d = Path(raiz) / a
            if d not in vistos: d.unlink()
    return n


def main():
    total = 0
    for origen, dst, modo in MAPA:
        n = espejo(origen, REPO / dst, 'todo' if modo in ('todo', 'skills') else modo)
        print(f'  {dst}: {n} archivos nuevos o cambiados'); total += n
    for s in SUELTOS:
        p = EV / s
        if p.exists() and vale(p, 'todo'):
            d = REPO / 'EDICION VIDEOS' / s; d.parent.mkdir(parents=True, exist_ok=True); shutil.copy2(p, d)
    print(f'Total: {total} archivos actualizados')
    if '--subir' in sys.argv:
        subprocess.run(['git', '-C', str(REPO), 'add', '-A'], check=True)
        fecha = datetime.date.today().isoformat()
        r = subprocess.run(['git', '-C', str(REPO), 'commit', '-m', f'Copia de seguridad {fecha}'], capture_output=True, text=True)
        print(r.stdout.strip().splitlines()[0] if r.stdout.strip() else r.stderr.strip())
        subprocess.run(['git', '-C', str(REPO), 'push'], check=True)
    if '--usb' in sys.argv:
        z = HOME / 'Desktop' / f'PAQUETE_EDICION_ABEL_{datetime.date.today().isoformat()}.zip'
        fotos = EV / 'ABEL GARCIA' / 'Editor vídeos' / 'MarcaPersonal' / 'FOTOS MIAS'
        with zipfile.ZipFile(z, 'w', zipfile.ZIP_DEFLATED, compresslevel=5) as zf:
            for raiz, dirs, archivos in os.walk(REPO):
                dirs[:] = [d for d in dirs if d != '.git']
                for a in archivos:
                    p = Path(raiz) / a; zf.write(p, p.relative_to(REPO))
            for raiz, _, archivos in os.walk(fotos):
                for a in archivos:
                    p = Path(raiz) / a
                    if not secreto(p):
                        zf.write(p, Path('EDICION VIDEOS/ABEL GARCIA/Editor vídeos/MarcaPersonal/FOTOS MIAS') / p.relative_to(fotos),
                                 compress_type=zipfile.ZIP_STORED)
        print(f'USB: {z} ({z.stat().st_size / 1e9:.2f} GB)')


if __name__ == '__main__':
    main()
