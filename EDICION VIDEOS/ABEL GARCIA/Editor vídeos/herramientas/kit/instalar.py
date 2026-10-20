"""Instalador del sistema de Abel en otro ordenador. Lo lanza INSTALAR.bat (doble clic).
1) Descomprime cada módulo (0_COMUN, 1_EDITOR_ABEL, 2_EDITOR_ALLAN, 3_FABRICA) en su sitio: Escritorio\\EDICION VIDEOS y .claude.
2) Pone la memoria de Claude en la carpeta del proyecto, aunque el usuario de Windows tenga otro nombre (y cambia las rutas).
3) Instala librerías de Python, dependencias de Node, el navegador de Playwright y la skill pública video-use.
"""
import os, re, shutil, subprocess, sys, zipfile
from pathlib import Path

AQUI = Path(__file__).resolve().parent
HOME = Path.home()
EV = HOME / 'Desktop' / 'EDICION VIDEOS'
CL = HOME / '.claude'
VIEJO = 'Clap'                       # usuario del ordenador original
NUEVO = HOME.name
TEXTOS = {'.py', '.md', '.json', '.mjs', '.js', '.html', '.txt', '.bat', '.css', '.csv'}


def cod(p):
    return re.sub(r'[^A-Za-z0-9]', '-', str(p))


MEMORIAS = {
    'claude/memoria/editor': EV / 'ABEL GARCIA' / 'Editor vídeos',
    'claude/memoria/allan': EV / 'MEDIUM ALLAN' / 'Editor Videos - Allan',
    'claude/memoria/fabrica': EV / 'FÁBRICA DE CONTENIDO',
}


def destino(nombre_zip: str):
    n = nombre_zip.replace('\\', '/')
    if n.startswith('EDICION VIDEOS/'): return EV.parent / n
    if n.startswith('claude/skills/'): return CL / 'skills' / n[len('claude/skills/'):]
    if n.startswith('claude/scheduled-tasks/'): return CL / 'scheduled-tasks' / n[len('claude/scheduled-tasks/'):]
    for pref, proy in MEMORIAS.items():
        if n.startswith(pref + '/'): return CL / 'projects' / cod(proy) / 'memory' / n[len(pref) + 1:]
    return None


def arreglar_rutas(p: Path):
    if NUEVO == VIEJO or p.suffix.lower() not in TEXTOS: return
    try: t = p.read_text(encoding='utf-8')
    except Exception: return
    t2 = (t.replace(f'C:\\Users\\{VIEJO}', f'C:\\Users\\{NUEVO}').replace(f'C:/Users/{VIEJO}', f'C:/Users/{NUEVO}')
           .replace(f'C:\\\\Users\\\\{VIEJO}', f'C:\\\\Users\\\\{NUEVO}').replace(f'/c/Users/{VIEJO}', f'/c/Users/{NUEVO}')
           .replace(f'C--Users-{VIEJO}-', f'C--Users-{NUEVO}-'))
    if t2 != t: p.write_text(t2, encoding='utf-8')


def descomprimir():
    for z in sorted(AQUI.glob('*.zip')):
        print(f'· {z.name}')
        with zipfile.ZipFile(z) as zf:
            for i in zf.infolist():
                if i.is_dir(): continue
                d = destino(i.filename)
                if d is None: continue
                d.parent.mkdir(parents=True, exist_ok=True)
                with zf.open(i) as src, open(d, 'wb') as out: shutil.copyfileobj(src, out)
                arreglar_rutas(d)


def run(cmd, **kw):
    print('  >', ' '.join(map(str, cmd))); return subprocess.run(cmd, **kw).returncode == 0


def instalar_entorno():
    py = [sys.executable, '-m', 'pip', 'install', '--upgrade']
    nvidia = shutil.which('nvidia-smi') is not None
    if nvidia: run(py + ['torch==2.6.0', 'torchaudio==2.6.0', '--index-url', 'https://download.pytorch.org/whl/cu124'])
    if nvidia: run(py + ['nvidia-cublas-cu12', 'nvidia-cudnn-cu12'])   # Whisper en la gráfica (int8): montar.py y transcripciones
    else: run(py + ['torch', 'torchaudio'])
    run(py + ['faster-whisper', 'ctranslate2', 'av', '--only-binary=:all:'])
    run(py + ['opencv-python', 'onnxruntime', 'numpy', 'pillow', 'pillow-heif', 'fonttools', 'scipy', 'soundfile', 'librosa', 'nltk', 'requests', 'yt-dlp'])
    tablero = EV / 'ABEL GARCIA' / 'Editor vídeos' / 'herramientas' / 'tablero'
    npm = shutil.which('npm') or shutil.which('npm.cmd')
    if tablero.exists() and npm:
        run([npm, 'install'], cwd=tablero)
        run([shutil.which('npx') or 'npx.cmd', '-y', 'playwright', 'install', 'chromium'], cwd=tablero)
    anim = CL / 'skills' / 'animaciones-horizontal-combinadas' / 'scripts' / 'anim.py'
    if anim.exists(): run([sys.executable, str(anim), 'entorno', '--instalar'])
    vu = CL / 'skills' / 'video-use'
    if not vu.exists() and shutil.which('git'): run(['git', 'clone', 'https://github.com/browser-use/video-use', str(vu)])


if __name__ == '__main__':
    print(f'Usuario de Windows: {NUEVO}  ·  Escritorio: {EV.parent}')
    descomprimir()
    print('Archivos en su sitio. Instalando librerías (puede tardar un rato)…')
    instalar_entorno()
    print('\nLISTO. Lee LEEME.txt para los últimos pasos (abrir Claude y conectar Google).')
