"""REVISIÓN DE AUDIO de cada corte de un reel YA MONTADO (Abel 14/10/2026: «tiene que depender del audio… escuchar el vídeo
y decir: esto no está bien recortado, empieza con un silencio, media frase, se come una letra final»).
No mira la transcripción original: mira la ONDA del audio montado (out/_<reel>/voz.wav) y ESCUCHA lo que ha quedado.

    python revisar_cortes.py <reels.json> [reel ...]

Por cada corte (sus tiempos exactos salen de onda.json; los cortes van en fotogramas exactos):
  ONDA   · CORTE SOBRE VOZ: en los 20 ms a un lado u otro del corte sigue sonando voz (se come una letra o una palabra)
         · PEGADO (< 0,04 s de silencio) o HUECO (> 0,12 s)
         · MICROCORTE: trozo de menos de 0,35 s entre dos cortes
         · PRINCIPIO / FINAL con silencio (> 0,06 s al empezar, > 0,16 s al acabar)
  OÍDO   · se escuchan 2,5 s alrededor del corte y se compara con lo que suena en la grabación en esos dos trozos por separado:
           si junto no suena como la suma de las dos partes (palabra comida, letra perdida, trozo de otra toma) → ✗
Sale con código 1 si hay algún ✗. Cada ✗ se corrige (tramo, "quitar") y se repite hasta que no quede ninguno.
"""
import json, re, subprocess, sys
from pathlib import Path
import numpy as np
sys.stdout.reconfigure(encoding='utf-8')
SR = 16000
norm = lambda w: re.sub(r'[^a-z0-9ñ]', '', w.lower().translate(str.maketrans('áéíóúü', 'aeiouu')))


def leer(ruta, a=None, b=None):
    cmd = ['ffmpeg', '-v', 'error'] + (['-ss', f'{a:.3f}', '-to', f'{b:.3f}'] if a is not None else []) + ['-i', str(ruta), '-ac', '1', '-ar', str(SR), '-f', 's16le', '-']
    return np.frombuffer(subprocess.run(cmd, capture_output=True).stdout, np.int16).astype(np.float32) / 32768


def db(x): return 20 * np.log10(np.sqrt((x ** 2).mean()) + 1e-9) if len(x) else -120


if __name__ == '__main__':
    ruta = Path(sys.argv[1]).resolve(); cfg = json.load(open(ruta, encoding='utf-8')); base = ruta.parent
    lim = base / '_fuente_limpia.wav'; fuente = lim if lim.exists() else base / cfg['fuente']
    import torch  # noqa: F401
    from faster_whisper import WhisperModel
    m = WhisperModel('large-v3', device='cuda', compute_type='float16')
    sys.path.insert(0, str(Path(__file__).resolve().parent)); from casual_prep import LITERAL   # que oiga las trabazones, no que las limpie
    oir = lambda x: ' '.join(w.word.strip() for s in m.transcribe(x, language='es', word_timestamps=True, condition_on_previous_text=False, initial_prompt=LITERAL)[0] for w in s.words)
    malos = 0
    for nombre in sys.argv[2:] or cfg['reels']:
        tmp = base / cfg['salida'] / f'_{nombre}'; c = json.load(open(tmp / 'onda.json'))
        V = float((tmp / 'velocidad.txt').read_text()) if (tmp / 'velocidad.txt').exists() else 1.1
        a = leer(tmp / 'voz.wav'); env = np.array([db(a[i:i + 160]) for i in range(0, len(a) - 160, 160)])
        voz = np.percentile(env, 95); calla = voz - 30                  # por debajo: silencio
        ps, pads = c['ps'], c['pads']; T, cortes = 0.0, []
        for (t0, t1, _), p in zip(ps, pads):
            T += (t1 - t0) / V; cortes.append((T, p / V, t0, t1)); T += p / V
        dur = len(a) / SR; pr = []; huecos = []
        ini = next((k for k, e in enumerate(env) if e > calla), 0) / 100
        fin = dur - next((k for k, e in enumerate(env[::-1]) if e > calla), 0) / 100
        if ini > .06: pr.append(f' ✗   0.00s PRINCIPIO con {ini:.2f} s de silencio')
        if dur - fin > .16: pr.append(f' ✗ {fin:6.2f}s FINAL con {dur - fin:.2f} s de silencio')
        prev = 0.0
        for k, (t, pd, s0, s1) in enumerate(cortes[:-1]):
            sig = cortes[k + 1]; largo = t - prev
            if abs(sig[2] - s1) < .002 and pd == 0: continue          # no hay corte: el audio sigue tal cual de la grabación
            if largo < .35 and k: pr.append(f' ✗ {prev:6.2f}s MICROCORTE: trozo de {largo:.2f} s')
            i = int(t * SR); j = int((t + pd) * SR)
            fin_a, ini_b = db(a[max(0, i - 320):i]), db(a[j:j + 320])           # 20 ms antes y después del corte
            yo = []
            if fin_a > voz - 18: yo.append('CORTE SOBRE VOZ al acabar el trozo (se come el final)')
            if ini_b > voz - 18: yo.append('CORTE SOBRE VOZ al empezar el trozo (se come el principio)')
            zona = env[max(0, int(t * 100) - 5):int((t + pd) * 100) + 6] <= calla   # el silencio más largo alrededor del corte
            hueco, run = 0, 0
            for z in zona: run = run + 1 if z else 0; hueco = max(hueco, run)
            q = int(t * 100); izq = q
            while izq > 0 and env[izq - 1] <= calla: izq -= 1
            der = q + 1
            while der < len(env) and env[der] <= calla: der += 1
            hueco = max(hueco, der - izq - 1) / 100 if zona.any() else 0
            if hueco < .02: yo.append(f'PEGADO: {hueco:.2f} s de silencio')   # ritmo de Lavri: 0,02-0,05 s es lo buscado
            if hueco > .08: yo.append(f'HUECO: {hueco:.2f} s de silencio')
            huecos.append(hueco)
            # oído: lo que suena junto vs. lo que suena en la grabación a cada lado
            w0, w1 = max(0, t - 1.4), min(dur, t + pd + 1.4)
            junto = oir(a[int(w0 * SR):int(w1 * SR)])
            izq_f = leer(fuente, max(0, s1 - 1.4 * V), s1); der_f = leer(fuente, sig[2], sig[2] + 1.4 * V)
            suma = oir(np.concatenate([izq_f, np.zeros(int(.3 * SR), np.float32), der_f]))
            A, B = [norm(x) for x in junto.split()], [norm(x) for x in suma.split()]
            if A[1:-1] and ' '.join(A[1:-1]) not in ' '.join(B) and ' '.join(B[1:-1]) not in ' '.join(A):
                yo.append(f'SE OYE DISTINTO: junto «{junto}» · por separado «{suma}»')
            if yo: pr.append(f' ✗ {t:6.2f}s ' + ' · '.join(yo) + f'   (fuente {s1:.2f} → {sig[2]:.2f})')
            prev = t + pd
        print(f'##### {nombre}: {len(cortes) - 1} cortes · ' + ('✓ limpio' if not pr else f'{len(pr)} ✗') + (f' · silencios en los cortes: mediana {sorted(huecos)[len(huecos) // 2]:.2f} s, máx {max(huecos):.2f} s' if huecos else ''))
        for x in pr: print(x)
        malos += len(pr)
    sys.exit(1 if malos else 0)
