"""Paquete portable del sistema de edición (sin vídeos): python empaquetar.py -> Escritorio/PAQUETE_EDICION_ABEL.zip
Incluye el editor, la Fábrica de contenido, la música, las skills y las dos memorias de Claude. Guía: INSTALAR.md."""
import os, zipfile
from pathlib import Path

H = Path.home(); D = H / 'Desktop' / 'EDICION VIDEOS'
OUT = H / 'Desktop' / 'PAQUETE_EDICION_ABEL.zip'
FUERA_EXT = {'.mp4', '.mov', '.wav', '.m4a', '.mkv', '.psd', '.webm'}
FUERA_DIR = {'node_modules', 'out', '__pycache__', 'planos'}
FUENTES = [(D / 'ABEL GARCIA' / 'Editor vídeos', 'EDICION VIDEOS/ABEL GARCIA/Editor vídeos'),
           (D / 'FÁBRICA DE CONTENIDO', 'EDICION VIDEOS/FÁBRICA DE CONTENIDO'),
           (D / 'MUSICA', 'EDICION VIDEOS/MUSICA'),
           (H / '.claude/projects/C--Users-Clap-Desktop-EDICION-VIDEOS-ABEL-GARCIA-Editor-v-deos/memory', 'memoria/editor'),
           (H / '.claude/projects/C--Users-Clap-Desktop-EDICION-VIDEOS-F-BRICA-DE-CONTENIDO/memory', 'memoria/fabrica')]
FUENTES += [(H / '.claude/skills' / s, f'skills/{s}') for s in
            ['animaciones-horizontal-combinadas', 'copywriter-skool-scaling', 'disenador-lead-magnets-skool-scaling',
             'generador-ideas-skool-scaling', 'iterador-trial-reels-skool-scaling', 'planificador-contenido-skool-scaling']]

n = tam = 0
with zipfile.ZipFile(OUT, 'w', zipfile.ZIP_DEFLATED) as z:
    for src, dst in FUENTES:
        for root, dirs, files in os.walk(src):
            dirs[:] = [d for d in dirs if d not in FUERA_DIR]
            for f in files:
                p = Path(root) / f
                if p.suffix.lower() in FUERA_EXT: continue
                z.write(p, dst + '/' + p.relative_to(src).as_posix()); n += 1; tam += p.stat().st_size
    z.write(D / 'ABEL GARCIA' / 'Editor vídeos' / 'INSTALAR.md', 'INSTALAR.md')
print(f'{n} archivos, {tam / 1e6:.0f} MB -> {OUT} ({OUT.stat().st_size / 1e6:.0f} MB)')
