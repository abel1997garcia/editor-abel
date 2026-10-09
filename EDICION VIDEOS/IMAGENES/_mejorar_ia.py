"""Mejora con IA (Real-ESRGAN) las imágenes de la biblioteca desde su recorte limpio (_originales/):
fotos/pinturas/visionario -> realesrgan-x4plus; grabados/bocetos/esquemas -> realesrgan-x4plus-anime (líneas limpias).
Se guardan a ×3 del recorte (las coordenadas de las traducciones siguen valiendo) y luego se rehacen las traducciones."""
import json, os, subprocess, sys
from PIL import Image
os.chdir(os.path.dirname(os.path.abspath(__file__)))
EXE = 'C:/Users/Clap/Desktop/EDICION VIDEOS/ABEL GARCIA/Editor vídeos/herramientas/realesrgan/realesrgan-ncnn-vulkan.exe'
cat = json.load(open('catalogo.json', encoding='utf-8'))
os.makedirs('_tmp', exist_ok=True)
for k, v in cat.items():
    src = '_originales/' + k.replace('/', '__')
    if not os.path.exists(src): print('sin original', k); continue
    modelo = 'realesrgan-x4plus-anime' if v['familia'] in ('grabado', 'boceto', 'esquema') else 'realesrgan-x4plus'
    tmp = '_tmp/' + k.replace('/', '__')
    subprocess.run([EXE, '-i', src, '-o', tmp, '-n', modelo], capture_output=True, check=True)
    w, h = Image.open(src).size
    Image.open(tmp).resize((w * 3, h * 3), Image.LANCZOS).save(k)
    v['resolucion'] = f'{w * 3}x{h * 3} (mejorada con IA: {modelo})'
    print('ok', k)
json.dump(cat, open('catalogo.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
for s in ('_traducir_lote1.py', '_traducir_lote2.py'):
    subprocess.run([sys.executable, s], check=True)
