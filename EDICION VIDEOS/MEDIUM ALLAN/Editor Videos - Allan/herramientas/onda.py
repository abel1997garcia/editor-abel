"""Ver la PISTA DE AUDIO de un reel terminado, como en un editor (Abel 13/10/2026: «que veas las ondas del audio para saber
al 100 % dónde cortar»). Dibuja la forma de onda de la voz, marca en ROJO todo hueco sin voz de más de 0,10 s (también al
principio y al final) y en gris los cortes de plano. Devuelve código 1 si hay algún hueco rojo.

    python herramientas/onda.py <reel.mp4> [<reel2.mp4> ...]      -> trabajo/reels/<reel>/<reel>.onda.png + informe (nunca en reels/)
    python onda.py --hueco 0.55 --final 0.4 <reels>                 -> con otros límites (reels de Allan: su ritmo es más pausado)

Se mide sobre el vídeo final (voz + música): la música va 13,5 dB por debajo, así que el umbral se fija respecto a la voz.
"""
import subprocess, sys
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont

HUECO = .10          # pausa máxima (Abel 13/10/2026, ritmo de Lavri; antes 0,15), también al principio y al final
PASO = .01           # envolvente cada 10 ms
INICIO = None        # aire máximo antes de la primera palabra (--inicio; Allan 0,10: el reel arranca YA con la frase)
FINAL = .16          # tras la última palabra se permite un poco más de aire (Lavri deja 0,16 s)


def envolvente(ruta):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', str(ruta), '-vn', '-ac', '1', '-ar', '16000', '-f', 's16le', '-'],
                         capture_output=True).stdout
    x = np.frombuffer(raw, np.int16).astype(float) / 32768; v = int(16000 * PASO); x = x[:len(x) // v * v]
    return x.reshape(-1, v), 20 * np.log10(np.sqrt((x.reshape(-1, v) ** 2).mean(1)) + 1e-9)


def cortes_de_plano(ruta):
    """cambios de plano del vídeo (escena > 0,25) para dibujarlos como líneas grises"""
    r = subprocess.run(['ffmpeg', '-i', str(ruta), '-vf', "select='gt(scene,0.25)',showinfo", '-an', '-f', 'null', '-'],
                       capture_output=True, text=True, errors='ignore').stderr
    return [float(l.split('pts_time:')[1].split()[0]) for l in r.splitlines() if 'pts_time:' in l]


def huecos(E):
    """tramos sin voz: por debajo de (pico de voz − 27 dB). La música queda por debajo de ese umbral."""
    umbral = np.percentile(E, 95) - 27
    sil = E < umbral; out, k = [], 0
    while k < len(sil):
        if not sil[k]: k += 1; continue
        j = k
        while j < len(sil) and sil[j]: j += 1
        largo = (j - k) * PASO
        lim = FINAL if j >= len(sil) else (INICIO if k == 0 and INICIO is not None else HUECO)
        if largo > lim + 1e-9: out.append((k * PASO, j * PASO))
        k = j
    return out, umbral


def dibujar(ruta, X, E, hs, umbral, cortes):
    dur = len(E) * PASO; W, H = max(1600, int(dur * 40)), 300
    im = Image.new('RGB', (W, H + 40), 'white'); d = ImageDraw.Draw(im)
    pico = np.abs(X).max(1); pico = pico / (pico.max() + 1e-9)
    for a, b in hs: d.rectangle((a / dur * W, 0, b / dur * W, H), fill=(255, 200, 200))
    for c in cortes: d.line((c / dur * W, 0, c / dur * W, H), fill=(170, 170, 170))
    for i, p in enumerate(pico):
        x = i / len(pico) * W; h = p * (H / 2 - 4)
        d.line((x, H / 2 - h, x, H / 2 + h), fill=(40, 90, 200) if E[i] >= umbral else (150, 170, 210))
    f = ImageFont.truetype('arial.ttf', 14)
    for s in range(int(dur) + 1): d.line((s / dur * W, H, s / dur * W, H + 6), fill='black'); d.text((s / dur * W + 2, H + 8), f'{s}s', font=f, fill='black')
    for a, b in hs: d.text((a / dur * W + 2, 4), f'{b - a:.2f}s', font=f, fill=(200, 0, 0))
    # La carpeta reels/ es la DEFINITIVA para subir: solo el mp4 y su .txt (Abel 18/10/2026). La onda va a trabajo/.
    ruta = Path(ruta).resolve(); raiz = Path(__file__).resolve().parent.parent
    carpeta = ruta.parent if 'trabajo' in ruta.parts else raiz / 'trabajo' / 'reels' / ruta.stem
    carpeta.mkdir(parents=True, exist_ok=True)
    salida = carpeta / f'{ruta.stem}.onda.png'; im.save(salida); return salida


if __name__ == '__main__':
    import argparse
    ap = argparse.ArgumentParser(); ap.add_argument('reels', nargs='+')
    ap.add_argument('--hueco', type=float, default=HUECO); ap.add_argument('--final', type=float, default=FINAL)
    ap.add_argument('--inicio', type=float, default=None)
    a = ap.parse_args(); HUECO, FINAL, INICIO = a.hueco, a.final, a.inicio
    malo = False
    for ruta in a.reels:
        X, E = envolvente(ruta); hs, umbral = huecos(E); png = dibujar(ruta, X, E, hs, umbral, cortes_de_plano(ruta))
        dur = len(E) * PASO
        print(f'== {Path(ruta).name}  ({dur:.2f} s) -> {png.name}')
        for a, b in hs:
            donde = 'PRINCIPIO' if a < .05 else 'FINAL' if b > dur - .05 else 'en medio'
            print(f'   ✗ hueco {b - a:.2f} s  de {a:.2f} a {b:.2f} s  ({donde})')
        if not hs: print(f'   ✓ sin huecos > {HUECO:.2f} s'.replace('.', ','))
        malo |= bool(hs)
    sys.exit(1 if malo else 0)
