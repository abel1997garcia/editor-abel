"""Sincronía del AUDIO del reel (medir_sync.py solo mide la IMAGEN). Para cada trozo compara el audio del mp4 con el
del ORIGINAL en ese mismo corte (correlación) y da el desfase en ms. Debe salir ~0 (+1 ms = margen del corte) en todos.
Error que destapó (sigue_01, 17/10/2026): el audio de los trozos se iba adelantando hasta ~-50 ms.

    python herramientas/medir_sync_audio.py reels/<reel>.mp4 [...]
"""
import json, subprocess, sys
from pathlib import Path
import numpy as np

sys.stdout.reconfigure(encoding='utf-8')
RAIZ = Path(__file__).resolve().parent.parent
SR = 8000
LIMITE_MS = 10       # más de 10 ms (un tercio de fotograma) = aviso


def lee(p, a=None, d=None):
    pre = ['-ss', f'{a:.4f}', '-t', f'{d:.4f}'] if a is not None else []
    r = subprocess.run(['ffmpeg', '-v', 'error', *pre, '-i', str(p), '-vn', '-ac', '1', '-ar', str(SR), '-f', 's16le', '-'],
                       capture_output=True).stdout
    return np.frombuffer(r, np.int16).astype(float)


def main():
    malo = False
    for mp4 in sys.argv[1:]:
        nombre = Path(mp4).stem
        M = json.load(open(RAIZ / 'trabajo/reels' / nombre / 'montaje.json', encoding='utf-8'))
        x = lee(mp4)
        des = []
        for k, s in enumerate(M['segmentos']):
            d = s['fin'] - s['ini']
            if d < 0.4:
                continue
            o = lee(M['video'], s['ini'] + 0.1, d - 0.2)
            i0 = int((s['out'] + 0.1) * SR)
            best = (-2, 0)
            for l in range(-1200, 1201, 2):          # ±150 ms
                seg = x[i0 + l:i0 + l + len(o)]
                if i0 + l < 0 or len(seg) < len(o):
                    continue
                best = max(best, (np.corrcoef(seg, o)[0, 1], l))
            ms = best[1] / SR * 1000
            des.append(round(ms))
            if abs(ms - 1) > LIMITE_MS:
                print(f'   ¡¡AVISO AUDIO!! trozo {k} (reel {s["out"]:.2f} s): {ms:+.1f} ms (corr {best[0]:.2f})')
                malo = True
        print(f'{nombre}: audio vs original por trozo (ms): {des}')
    sys.exit(1 if malo else 0)


if __name__ == '__main__':
    main()
