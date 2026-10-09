"""Verificador de AUDIO de un reel: «escucharlo» antes de darlo por bueno (Abel 08/10/2026: mirar fotogramas y texto no basta;
si no se entiende fluido, algo hay que cambiar).

    python verificar_audio.py <carpeta de trabajo del reel> <tiempos.json de la toma>     (reels F1/F2/F3/F4: out/_<reel>/)

Usa planos.json ([vf, [ini, fin, relleno], ...] en segundos de la toma) y voz.wav (su voz montada, a VELOCIDAD).
  1. TEXTO: vuelve a transcribir todo con Whisper y lo compara con lo que debería decir (palabras que faltan, sobran o se repiten).
  2. CADA CORTE, en el punto exacto (muestra a muestra):
     - CORTE SOBRE LA VOZ: hay sonido de voz justo en el corte (se ha partido una palabra o una respiración);
     - PEGADO / HUECO: el silencio que queda es < 0,08 s (no respira) o > 0,55 s (hueco muerto);
     - SE OYE DISTINTO: se vuelve a transcribir solo ese trozo (±2 s) y no coincide con lo esperado;
     - tipo «pausa» (solo se quitó silencio) o «salto» (se quitó texto o se reordenó). En los saltos: LEER LA UNIÓN EN VOZ
       ALTA («…antes ‖ después…»): si no suena a una sola frase natural, el corte está mal aunque no salte ningún aviso.
  3. RITMO: cortes por cada 10 s y planos de menos de 1 s (cortecitos que hacen que no sea fluido).
Código de salida 1 si hay algo grave. Los trozos de cada salto quedan en _cortes/ para escucharlos.
"""
import json, re, subprocess, sys, difflib
from pathlib import Path
import numpy as np
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, str(Path(__file__).resolve().parent))
from reel_yapping import VELOCIDAD

SR = 16000


def norm(x):
    x = x.lower()
    for a, b in zip('áéíóúü', 'aeiouu'): x = x.replace(a, b)
    return re.sub(r'[^a-z0-9ñ]', '', x)


def tokens(pal):
    """une los números que Whisper parte («550 .000» -> «550000»)"""
    out = []
    for p in pal:
        n = norm(p)
        if not n: continue
        if out and n.isdigit() and out[-1].isdigit() and p.strip().startswith(('.', ',')): out[-1] += n
        else: out.append(n)
    return out


def cargar(wav):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', str(wav), '-ac', '1', '-ar', str(SR), '-f', 's16le', '-'], capture_output=True).stdout
    return np.frombuffer(raw, np.int16).astype(np.float32) / 32768


def db(x): return 20 * np.log10(np.sqrt(np.mean(x ** 2)) + 1e-6) if len(x) else -120


def main(tmp, tiempos):
    tmp = Path(tmp); P = json.loads((tmp / 'planos.json').read_text())[1:]
    W = json.load(open(tiempos, encoding='utf-8')); W = W['palabras'] if isinstance(W, dict) else W
    a = cargar(tmp / 'voz.wav')
    cortes, T, esp_t = [], 0.0, []                     # esp_t: (palabra, segundo del reel) que debería oírse
    for k, (t0, t1, pd) in enumerate(P):
        if k:
            p0 = P[k - 1][1]; entre = [w for w in W if p0 - .02 < w['s'] < t0 - .02]
            cortes.append({'t': T / VELOCIDAD, 'tipo': 'pausa' if (0 <= t0 - p0 < 3 and not entre) else 'salto',
                           'quitado': ' '.join(w['w'] for w in entre)[:70]})
        esp_t += [(w['w'], (T + w['s'] - t0) / VELOCIDAD) for w in W if t0 - .02 <= w['s'] < t1 - .03]
        T += t1 - t0 + pd
    dur = T / VELOCIDAD
    env = np.array([db(a[i:i + 160]) for i in range(0, len(a) - 160, 160)])          # 10 ms
    nivel = np.percentile(env, 95); umbral = nivel - 24
    import torch  # noqa: F401  (sin esto faltan las DLL de cuBLAS)
    from faster_whisper import WhisperModel
    m = WhisperModel('large-v3', device='cuda', compute_type='float16')
    oir = lambda x: [(w.word.strip(), w.start, w.end, w.probability) for s in
                     m.transcribe(x, language='es', word_timestamps=True, vad_filter=False, condition_on_previous_text=False, beam_size=5)[0] for w in s.words]
    oido = oir(str(tmp / 'voz.wav'))
    graves, avisos = 0, []
    # 1) el texto entero
    A, B = tokens([p for p, _ in esp_t]), tokens([x[0] for x in oido])
    for op, i1, i2, j1, j2 in difflib.SequenceMatcher(None, A, B, autojunk=False).get_opcodes():
        if op != 'equal':
            avisos.append(f'TEXTO   esperaba «{" ".join(A[i1:i2])}» · se oye «{" ".join(B[j1:j2])}»'); graves += 1
    for i in range(1, len(B)):
        if B[i] == B[i - 1] and A.count(B[i]) < B.count(B[i]): avisos.append(f'REPITE  «{B[i]} {B[i]}»'); graves += 1
    # 2) cada corte
    (tmp / '_cortes').mkdir(exist_ok=True)
    print(f'\n{len(cortes)} cortes en {dur:.1f} s ({len(cortes) / dur * 10:.1f} cada 10 s) · {sum(c["tipo"] == "salto" for c in cortes)} saltos de contenido\n')
    for c in cortes:
        t = c['t']; s = int(t * SR); i = int(t * 100)
        voz_en_corte = max(db(a[s - 480:s - 80]), db(a[s + 80:s + 480])) > nivel - 14        # 5-30 ms a cada lado
        izq = next((k for k in range(i, max(0, i - 120), -1) if env[min(k, len(env) - 1)] > umbral), i - 120)
        der = next((k for k in range(i, min(len(env), i + 120)) if env[k] > umbral), i + 120)
        hueco = (der - izq) / 100
        w0, w1 = max(0, t - 2), min(dur, t + 2)
        loc = oir(a[int(w0 * SR):int(w1 * SR)])
        esp = tokens([p for p, tt in esp_t if w0 + .25 <= tt <= w1 - .45])
        got = tokens([x[0] for x in loc if x[1] + w0 >= w0 + .15 and x[1] + w0 <= w1 - .35])
        r = difflib.SequenceMatcher(None, esp, got, autojunk=False)
        malo = [(esp[i1:i2], got[j1:j2]) for op, i1, i2, j1, j2 in r.get_opcodes()     # los bordes de la ventana no cuentan
                if op != 'equal' and i1 > 0 and i2 < len(esp) and j1 > 0 and j2 < len(got)]
        antes = ' '.join(x[0] for x in oido if t - 2.2 < x[2] <= t + .1)
        despues = ' '.join(x[0] for x in oido if t - .1 <= x[1] < t + 2.2)
        pr = []
        if voz_en_corte: pr.append('CORTE SOBRE LA VOZ (parte una palabra o una respiración)')
        if hueco < .08: pr.append(f'PEGADO: solo {hueco:.2f} s de silencio, no respira')
        if hueco > .55: pr.append(f'HUECO de {hueco:.2f} s')
        if malo and len(esp) > 2: pr.append('SE OYE DISTINTO: ' + '; '.join(f'«{" ".join(e)}» → «{" ".join(g)}»' for e, g in malo))
        graves += bool(pr)
        print(f' {"✗" if pr else "·"} {t:6.2f}s {c["tipo"]:5s} silencio {hueco:.2f}s  «…{antes} ‖ {despues}…»'
              + (f'   [quitado: {c["quitado"]}]' if c['tipo'] == 'salto' and c['quitado'] else ''))
        for x in pr: print(f'           → {x}')
        if c['tipo'] == 'salto' or pr:
            subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', f'{max(0, t - 2.5):.2f}', '-t', '5', '-i', str(tmp / 'voz.wav'), str(tmp / '_cortes' / f'corte_{t:06.2f}.wav')])
    # 3) ritmo
    cortos = [(round((sum(p[1] - p[0] + p[2] for p in P[:k])) / VELOCIDAD, 2), round((p[1] - p[0]) / VELOCIDAD, 2)) for k, p in enumerate(P) if (p[1] - p[0]) / VELOCIDAD < 1]
    if cortos: print(f'\nRITMO: {len(cortos)} planos de menos de 1 s (cortecitos): ' + ', '.join(f'{t}s ({d}s)' for t, d in cortos))
    print('\nTEXTO OÍDO (léelo seguido en voz alta; ‖ = salto de contenido):\n')
    sal = [c['t'] for c in cortes if c['tipo'] == 'salto']; out, k = [], 0
    for x in oido:
        while k < len(sal) and x[1] >= sal[k] - .1: out.append('‖'); k += 1
        out.append(x[0])
    print(' '.join(out))
    for x in avisos: print('  ' + x)
    print(f'\n{"✗ " + str(graves) + " problemas: NO está listo" if graves else "✓ sin problemas detectados (aun así, leer las uniones ‖ en voz alta)"}')
    sys.exit(1 if graves else 0)


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
