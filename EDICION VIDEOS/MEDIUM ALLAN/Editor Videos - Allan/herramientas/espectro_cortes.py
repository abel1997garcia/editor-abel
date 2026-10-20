"""ESPECTROGRAMA de la voz montada (PASO 1, antes de renderizar el vídeo; Abel 17/10/2026: «primero el audio, una vez
optimizado montas el vídeo encima… aplicando en el audio el espectrograma»).

    python herramientas/espectro_cortes.py <reel>        (lee trabajo/reels/<reel>/voz.wav y su montaje.json)

Genera en trabajo/reels/<reel>/:
  - espectro_cortes.png : una viñeta por empalme (±1 s, línea CIAN = corte). Se busca: palabra a medias pegada a la
    línea (cola o arranque cortado), «eh»/«mmm» = franja horizontal lisa y sin consonantes junto al corte,
    respiración o chasquido de más, silencio largo.
  - espectro_voz.png    : la voz entera (con los cortes marcados) para ver de un vistazo muletillas largas y huecos.
"""
import json, subprocess, sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

sys.stdout.reconfigure(encoding='utf-8')
RAIZ = Path(__file__).resolve().parent.parent
MARGEN = 1.0             # segundos a cada lado del corte
ANCHO, ALTO = 600, 220   # viñeta
COLS = 3
try:
    FUENTE = ImageFont.truetype('arial.ttf', 16)
except OSError:
    FUENTE = ImageFont.load_default()


def espectro(wav, ini, dur, ancho, alto, destino):
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', f'{ini:.3f}', '-t', f'{dur:.3f}', '-i', str(wav),
                    '-lavfi', f'aformat=channel_layouts=mono,showspectrumpic=s={ancho}x{alto}:legend=0:'
                              f'scale=log:fscale=lin:stop=8000:color=intensity', str(destino)], check=True)
    return Image.open(destino).convert('RGB')


def main():
    nombre = sys.argv[1]
    carpeta = RAIZ / 'trabajo/reels' / nombre
    wav = carpeta / 'voz.wav'
    M = json.load(open(carpeta / 'montaje.json', encoding='utf-8'))
    cortes = [s['out'] for s in M['segmentos'][1:]]
    dur = M['duracion']
    tmp = carpeta / '_esp.png'

    filas = (len(cortes) + COLS - 1) // COLS
    hoja = Image.new('RGB', (COLS * ANCHO, filas * (ALTO + 24)), 'white')
    d = ImageDraw.Draw(hoja)
    for k, t in enumerate(cortes):
        a = max(0.0, t - MARGEN); b = min(dur, t + MARGEN)
        im = espectro(wav, a, b - a, ANCHO, ALTO, tmp)
        x0, y0 = (k % COLS) * ANCHO, (k // COLS) * (ALTO + 24)
        hoja.paste(im, (x0, y0 + 24))
        xc = x0 + int((t - a) / (b - a) * ANCHO)
        d.line([(xc, y0 + 24), (xc, y0 + 24 + ALTO)], fill=(0, 255, 255), width=3)
        d.text((x0 + 6, y0 + 3), f'empalme {k}|{k + 1}  t={t:.2f}s', fill='black', font=FUENTE)
    hoja.save(carpeta / 'espectro_cortes.png')

    # voz entera, en franjas de 15 s
    TRAMO, AW = 15.0, 1800
    n = int(dur // TRAMO) + 1
    total = Image.new('RGB', (AW, n * (ALTO + 24)), 'white')
    d = ImageDraw.Draw(total)
    for k in range(n):
        a = k * TRAMO; b = min(dur, a + TRAMO)
        if b - a < .2:
            continue
        im = espectro(wav, a, b - a, int(AW * (b - a) / TRAMO), ALTO, tmp)
        y0 = k * (ALTO + 24)
        total.paste(im, (0, y0 + 24))
        d.text((6, y0 + 3), f'{a:.0f}-{b:.0f} s', fill='black', font=FUENTE)
        for t in cortes:
            if a <= t < b:
                xc = int((t - a) / TRAMO * AW)
                d.line([(xc, y0 + 24), (xc, y0 + 24 + ALTO)], fill=(0, 255, 255), width=3)
    total.save(carpeta / 'espectro_voz.png')
    tmp.unlink(missing_ok=True)
    print(f'{nombre}: {len(cortes)} empalmes -> {carpeta / "espectro_cortes.png"} + espectro_voz.png')


if __name__ == '__main__':
    main()
