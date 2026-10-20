"""Kit para llevar TODO el sistema de Abel a otro ordenador (portátil), en módulos separados y comprimidos.

    python kit_portatil.py [--sin-material]   → crea en el Escritorio la carpeta «KIT ABEL <fecha>» con:
        0_COMUN.zip          skills generales de Claude, tareas programadas, MUSICA, IMAGENES, logos y el INSTALADOR
        1_EDITOR_ABEL.zip    Editor vídeos (herramientas, skills del proyecto, MarcaPersonal con FOTOS MIAS, Referencias…) + su memoria
        2_EDITOR_ALLAN.zip   MEDIUM ALLAN (editor de Allan, fotos, trabajos) + su memoria
        3_FABRICA.zip        FÁBRICA DE CONTENIDO (la carpeta local) + su memoria
        4_MATERIAL_PROPIO.zip  lo grabado que NO se tira: ABEL GARCIA (MARCA PERSONAL, fotos, músicas…) y MEDIUM ALLAN
                             (TESTIMONIOS, REELS SI ALLAN, evento…) fuera de los editores, y los vídeos grandes de FOTOS MIAS
        INSTALAR.bat · instalar.py · LEEME.txt

En el otro ordenador: copiar la carpeta, doble clic en INSTALAR.bat. El instalador descomprime cada módulo en su sitio,
pone la memoria de Claude donde toca (aunque el usuario de Windows se llame distinto) e instala los programas y librerías.
Nunca entra: settings.json, claves, «CONTRASEÑAS…», .env, vídeos en bruto ni renders (filtros de editor-abel/actualizar_copia.py).
"""
import datetime, os, re, shutil, sys, zipfile
from pathlib import Path

HOME = Path.home()
EV = HOME / 'Desktop' / 'EDICION VIDEOS'
CL = HOME / '.claude'
sys.path.insert(0, str(HOME / 'editor-abel'))
from actualizar_copia import recorrer, secreto, vale   # mismos filtros que la copia de seguridad


def cod(p):
    """nombre de la carpeta de memoria de Claude para un proyecto (la ruta con todo lo que no es letra o número → «-»)"""
    return re.sub(r'[^A-Za-z0-9]', '-', str(p))


EDITOR = EV / 'ABEL GARCIA' / 'Editor vídeos'
ALLAN = EV / 'MEDIUM ALLAN'
FABRICA = EV / 'FÁBRICA DE CONTENIDO'
MODULOS = {
    '0_COMUN': [(CL / 'skills', 'claude/skills', 'todo'), (CL / 'scheduled-tasks', 'claude/scheduled-tasks', 'todo'),
                (EV / 'MUSICA', 'EDICION VIDEOS/MUSICA', 'todo'), (EV / 'IMAGENES', 'EDICION VIDEOS/IMAGENES', 'todo')],
    '1_EDITOR_ABEL': [(EDITOR, 'EDICION VIDEOS/ABEL GARCIA/Editor vídeos', 'sistema'),
                      (EDITOR / 'MarcaPersonal' / 'FOTOS MIAS', 'EDICION VIDEOS/ABEL GARCIA/Editor vídeos/MarcaPersonal/FOTOS MIAS', 'completo'),
                      (CL / 'projects' / cod(EDITOR) / 'memory', 'claude/memoria/editor', 'todo')],
    '2_EDITOR_ALLAN': [(ALLAN, 'EDICION VIDEOS/MEDIUM ALLAN', 'sistema'),
                       (CL / 'projects' / cod(ALLAN / 'Editor Videos - Allan') / 'memory', 'claude/memoria/allan', 'todo')],
    '3_FABRICA': [(FABRICA, 'EDICION VIDEOS/FÁBRICA DE CONTENIDO', 'todo'),
                  (CL / 'projects' / cod(FABRICA) / 'memory', 'claude/memoria/fabrica', 'todo')],
    '4_MATERIAL_PROPIO': [(EV / 'ABEL GARCIA', 'EDICION VIDEOS/ABEL GARCIA', 'completo'),
                          (ALLAN, 'EDICION VIDEOS/MEDIUM ALLAN', 'completo')],
}
EDITORES = {EDITOR, ALLAN / 'Editor Videos - Allan'}   # ya van en sus módulos


def completo(origen):
    """todo, sin límite de tamaño (material propio), salvo secretos y las carpetas de los editores"""
    for raiz, dirs, archivos in os.walk(origen):
        dirs[:] = [d for d in dirs if Path(raiz) / d not in EDITORES and d not in {'node_modules', '.git', '__pycache__'}]
        for a in archivos:
            if not secreto(Path(raiz) / a) and not any(k in a.lower() for k in ('token', 'clave', 'api key', 'credencial')): yield Path(raiz) / a
SUELTOS = ['LOGO-ABEL.png', 'FONDO-REELS.png', 'FONDO BLANCO TABLET.PNG', 'suscribe.png', 'SUSCRIBETE.mp4', 'MINIATURA BASE.psd', 'PROYECTO.psd']
FUERA_COMUN = {'video-use'}   # público: lo clona el instalador


def main():
    kit = HOME / 'Desktop' / f'KIT ABEL {datetime.date.today().isoformat()}'
    kit.mkdir(exist_ok=True)
    sin_material = '--sin-material' in sys.argv          # 4_MATERIAL_PROPIO (lo grabado, decenas de GB) solo si se pide
    for nombre, partes in MODULOS.items():
        if sin_material and nombre == '4_MATERIAL_PROPIO': continue
        z = kit / f'{nombre}.zip'; n = 0
        with zipfile.ZipFile(z, 'w', zipfile.ZIP_DEFLATED, compresslevel=6) as zf:
            for origen, dst, modo in partes:
                if not origen.exists(): print('  (no existe)', origen); continue
                for p in (completo(origen) if modo == 'completo' else recorrer(origen, modo)):
                    rel = p.relative_to(origen)
                    if nombre == '0_COMUN' and rel.parts and rel.parts[0] in FUERA_COMUN: continue
                    tipo = zipfile.ZIP_STORED if p.suffix.lower() in {'.jpg', '.jpeg', '.png', '.mp3', '.mp4', '.webp', '.zip'} else zipfile.ZIP_DEFLATED
                    zf.write(p, Path(dst) / rel, compress_type=tipo); n += 1
            if nombre == '0_COMUN':
                for s in SUELTOS:
                    p = EV / s
                    if p.exists() and vale(p, 'todo'): zf.write(p, Path('EDICION VIDEOS') / s); n += 1
        print(f'{z.name}: {n} archivos, {z.stat().st_size / 1e6:.0f} MB')
    for a in ('INSTALAR.bat', 'instalar.py', 'LEEME.txt'):
        shutil.copy2(Path(__file__).parent / 'kit' / a, kit / a)
    print('Kit listo en', kit)


if __name__ == '__main__':
    main()
