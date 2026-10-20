"""Busca en la VOZ montada sonido que NO es ninguna palabra del guion: «eh», «mmm», risas, respiraciones fuertes,
palabras sueltas que Whisper omitió (Whisper casi nunca escribe los «eh», así que no basta con transcribir).

    python herramientas/voz_sin_palabra.py <reel>          (usa trabajo/reels/<reel>/montaje.json y el original)
    python herramientas/voz_sin_palabra.py <reel> --oir    (además ESCUCHA cada sospechoso >= 0,15 s y > −38 dB en el
                                                            original con prompt de muletillas y dice qué suena ahí)

Para cada trozo mira la energía del ORIGINAL entre su inicio y su fin y lista los tramos con voz (>= 80 ms) que
quedan fuera de las palabras alineadas que conserva el trozo. Da el tiempo en el reel y en el original para ir a
escucharlo con oir.py y corregirlo con ini_fijo / fin_max / hueco_antes.
"""
import json, subprocess, sys
from pathlib import Path
import numpy as np

sys.stdout.reconfigure(encoding='utf-8')
RAIZ = Path(__file__).resolve().parent.parent
PASO = 0.01
MIN_VOZ = 0.08        # tramo con voz mínimo para avisar
TOL = 0.06            # holgura alrededor de cada palabra alineada (colas / ataques)


def energia(video, a, b):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-ss', f'{a:.3f}', '-t', f'{b - a:.3f}', '-i', video, '-vn', '-ac', '1',
                          '-ar', '16000', '-f', 's16le', '-'], capture_output=True).stdout
    x = np.frombuffer(raw, np.int16).astype(float) / 32768
    v = int(16000 * PASO); x = x[:len(x) // v * v]
    return 20 * np.log10(np.sqrt((x.reshape(-1, v) ** 2).mean(1)) + 1e-9)


def main():
    nombre = sys.argv[1]
    M = json.load(open(RAIZ / 'trabajo/reels' / nombre / 'montaje.json', encoding='utf-8'))
    spec = json.load(open(RAIZ / 'trabajo/specs' / f'{nombre}.json', encoding='utf-8'))
    T = {w['i']: w for w in json.load(open(RAIZ / spec['tiempos'], encoding='utf-8'))}
    video = M['video']
    # umbral de voz a partir de todo el reel: pico de voz − 30 dB
    todas = np.concatenate([energia(video, s['ini'], s['fin']) for s in M['segmentos']])
    umbral = np.percentile(todas, 95) - 30
    oir = '--oir' in sys.argv
    if oir:
        sys.path.insert(0, str(RAIZ / '.claude/skills/animaciones-horizontal-combinadas/scripts'))
        from transcribir import preparar_cuda; preparar_cuda()
        from faster_whisper import WhisperModel
        modelo = WhisperModel('large-v3', device='cuda', compute_type='float16')
        MULETILLAS = {'eh', 'em', 'ehm', 'mm', 'mmm', 'ah', 'este', 'pues', 'o', 'sea', 'no', 'bueno', 'vale', 'y', 'que'}
    n = 0
    for k, s in enumerate(M['segmentos']):
        E = energia(video, s['ini'], s['fin'])
        t = s['ini'] + np.arange(len(E)) * PASO
        cubierto = np.zeros(len(E), bool)
        for i in s['palabras']:
            w = T[i]
            cubierto |= (t >= w['s'] - TOL) & (t <= w['e'] + TOL)
        libre = (E > umbral) & ~cubierto
        j = 0
        while j < len(libre):
            if not libre[j]: j += 1; continue
            q = j
            while q < len(libre) and libre[q]: q += 1
            if (q - j) * PASO >= MIN_VOZ:
                a = s['ini'] + j * PASO; b = s['ini'] + q * PASO
                antes = max((T[i] for i in s['palabras'] if T[i]['e'] <= a + TOL), key=lambda w: w['e'], default=None)
                despues = min((T[i] for i in s['palabras'] if T[i]['s'] >= b - TOL), key=lambda w: w['s'], default=None)
                print(f'trozo {k:2d}  reel {s["out"] + a - s["ini"]:6.2f}s  original {a:8.2f}-{b:8.2f}  ({b - a:.2f} s, '
                      f'{E[j:q].max():.0f} dB)  entre «{antes["w"] if antes else "INICIO"}» y «{despues["w"] if despues else "FIN"}»')
                n += 1
                if oir and (b - a) >= 0.15 and E[j:q].max() > -38:
                    c0, c1 = max(0, a - 0.8), b + 0.4
                    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', f'{c0:.3f}', '-t', f'{c1 - c0:.3f}', '-i', video,
                                    '-ac', '1', '-ar', '16000', str(RAIZ / 'trabajo/_sos.wav')], check=True)
                    segs, _ = modelo.transcribe(str(RAIZ / 'trabajo/_sos.wav'), language='es', beam_size=5, temperature=0,
                                                condition_on_previous_text=False, word_timestamps=True,
                                                initial_prompt='Eh... mmm... pues, eh, o sea, este... eh, ¿no?')
                    ws = [(w.word.strip(), c0 + w.start, c0 + w.end) for sg in segs for w in sg.words]
                    dentro = [w for w in ws if w[2] > a + 0.03 and w[1] < b - 0.03]
                    plano = lambda t: t.lower().strip('.,¿?¡!… ')
                    sosp = [w[0] for w in dentro if plano(w[0]) in MULETILLAS]
                    print(f'        oído: {" ".join(w[0] for w in ws)}   ->  en el hueco: {" ".join(w[0] for w in dentro) or "—"}'
                          + ('   ¡¡MULETILLA!!' if sosp else ''))
            j = q
    print(f'{nombre}: {n} tramos con voz fuera de palabra (umbral {umbral:.0f} dB) -> escuchar cada uno')


if __name__ == '__main__':
    main()
