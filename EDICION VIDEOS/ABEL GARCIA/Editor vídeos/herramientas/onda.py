"""Ver la PISTA DE AUDIO de un reel terminado, como en un editor (Abel 13/10/2026: «que veas las ondas del audio para saber
al 100 % dónde cortar»). Dibuja la forma de onda de la voz, marca en ROJO todo hueco sin voz de más de 0,10 s (también al
principio y al final) y en gris los cortes de plano. Devuelve código 1 si hay algún hueco rojo.

    python herramientas/onda.py <voz.wav|reel.mp4> [...]          -> <x>.onda.png al lado + informe
LA ONDA MANDA (Abel 14/10/2026): se pasa sobre out/_<reel>/voz.wav ANTES del render (reel_tablero/reel_yapping --voz ya lo hacen).
    python onda.py --hueco 0.55 --final 0.4 <reels>                 -> con otros límites (reels de Allan: su ritmo es más pausado)

Se mide sobre el vídeo final (voz + música): la música va 13,5 dB por debajo, así que el umbral se fija respecto a la voz.
"""
import subprocess, sys
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont

HUECO = .10          # pausa máxima (Abel 13/10/2026, ritmo de Lavri; antes 0,15), también al principio y al final
PASO = .01           # envolvente cada 10 ms
FINAL = .16          # tras la última palabra se permite un poco más de aire (Lavri deja 0,16 s)


def envolvente(ruta):
    """dB cada 10 ms. Se toma lo más alto entre la voz entera y sus agudos (> 2,5 kHz, +20 dB): una «s» o una «f» final
    suenan flojas y sin esto contaban como silencio y se cortaban («Borras» → «borra», Abel 14/10/2026)"""
    def lee(af):
        raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', str(ruta), '-vn', '-ac', '1', '-ar', '16000', *af, '-f', 's16le', '-'],
                             capture_output=True).stdout
        x = np.frombuffer(raw, np.int16).astype(float) / 32768; v = int(16000 * PASO); return x[:len(x) // v * v].reshape(-1, v)
    X, A = lee([]), lee(['-af', 'highpass=f=2500,highpass=f=2500'])
    db = lambda Y: 20 * np.log10(np.sqrt((Y ** 2).mean(1)) + 1e-9)
    n = min(len(X), len(A)); return X[:n], np.maximum(db(X[:n]), db(A[:n]) + 20)


def agudos(ruta):
    """dB cada 10 ms solo de los agudos (> 3 kHz): una «s», «f» o «z» casi no tiene energía en graves, pero sí aquí"""
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', str(ruta), '-vn', '-ac', '1', '-ar', '16000', '-af', 'highpass=f=3000,highpass=f=3000',
                          '-f', 's16le', '-'], capture_output=True).stdout
    x = np.frombuffer(raw, np.int16).astype(float) / 32768; v = int(16000 * PASO); x = x[:len(x) // v * v].reshape(-1, v)
    return 20 * np.log10(np.sqrt((x ** 2).mean(1)) + 1e-9)


def graves(ruta):
    """dB cada 10 ms solo de los graves (< 1,2 kHz): ahí suena la voz (vocales, «v», «m») pero NO una «s»"""
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', str(ruta), '-vn', '-ac', '1', '-ar', '16000', '-af', 'lowpass=f=1200,lowpass=f=1200',
                          '-f', 's16le', '-'], capture_output=True).stdout
    x = np.frombuffer(raw, np.int16).astype(float) / 32768; v = int(16000 * PASO); x = x[:len(x) // v * v].reshape(-1, v)
    return 20 * np.log10(np.sqrt((x ** 2).mean(1)) + 1e-9)


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
        if largo > (FINAL if j >= len(sil) else HUECO) + 1e-9: out.append((k * PASO, j * PASO))
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
    salida = Path(ruta).with_suffix('.onda.png'); im.save(salida); return salida


def revisar(ruta):
    """dibuja la onda, imprime los huecos rojos y devuelve si hay alguno"""
    X, E = envolvente(ruta); hs, umbral = huecos(E); png = dibujar(ruta, X, E, hs, umbral, cortes_de_plano(ruta))
    dur = len(E) * PASO
    print(f'== {Path(ruta).parent.name}/{Path(ruta).name}  ({dur:.2f} s) -> {png}')
    for a, b in hs:
        donde = 'PRINCIPIO' if a < .05 else 'FINAL' if b > dur - .05 else 'en medio'
        print(f'   ✗ hueco {b - a:.2f} s  de {a:.2f} a {b:.2f} s  ({donde})')
    if not hs: print(f'   ✓ sin huecos > {HUECO:.2f} s'.replace('.', ','))
    return bool(hs)


if __name__ == '__main__':
    import argparse
    ap = argparse.ArgumentParser(); ap.add_argument('reels', nargs='+')
    ap.add_argument('--hueco', type=float, default=HUECO); ap.add_argument('--final', type=float, default=FINAL)
    a = ap.parse_args(); HUECO, FINAL = a.hueco, a.final
    sys.exit(1 if any([revisar(r) for r in a.reels]) else 0)
