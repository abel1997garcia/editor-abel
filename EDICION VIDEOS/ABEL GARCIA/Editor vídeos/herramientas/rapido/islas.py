"""PASO 1 del proceso rápido (Abel 15/10/2026: «céntrate primero en el audio»). Parte la grabación en ISLAS de voz separadas por
silencios reales y ESCUCHA cada isla SUELTA una sola vez (el reconocedor se carga una vez). Así:
  · los cortes caen SIEMPRE en silencio (nunca se come una palabra: «marca», «información», «mundo»);
  · cada toma repetida es una isla distinta con su texto (se ve qué es resto: «o no», «un…», «Me…», «Ah»);
  · los tiempos de cada palabra son exactos dentro de su isla (subtítulos cuadrados).

    python herramientas/rapido/islas.py <carpeta>        (carpeta con _fuente_limpia.wav, de casual_prep.py)
Escribe <carpeta>/islas.json y muestra la lista numerada.
"""
import json, subprocess, sys
from pathlib import Path
import numpy as np
AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parent))
import onda

SILENCIO = .10      # un hueco de al menos esto separa dos islas (así ninguna pausa DENTRO de una isla pasa de 0,1 s)
VOZ_DB = 33         # voz = por encima de (pico − 33 dB), con los agudos (+20 dB) para no perder ninguna «s»
MARGEN_A, MARGEN_B = .03, .05   # aire que se deja delante (el golpe de una «p», «t») y detrás (la cola de la vocal / «s»)


def detectar(E, P=onda.PASO):
    pico = np.percentile(E, 95); voz = E > pico - VOZ_DB
    islas, k, n = [], 0, len(voz)
    while k < n:
        if not voz[k]: k += 1; continue
        j = k
        while j < n:
            if voz[j]: j += 1; continue
            h = j
            while h < n and not voz[h]: h += 1
            if (h - j) * P >= SILENCIO or h >= n: break
            j = h
        if (j - k) * P >= .06: islas.append([round(k * P, 3), round(j * P, 3)])
        k = j
    return islas


if __name__ == '__main__':
    import torch  # noqa: F401
    from faster_whisper import WhisperModel
    from casual_prep import LITERAL
    d = Path(sys.argv[1]); f = d / '_fuente_limpia.wav'
    _, E = onda.envolvente(str(f))
    x0 = np.frombuffer(subprocess.run(['ffmpeg', '-v', 'error', '-i', str(f), '-ac', '1', '-ar', '16000', '-f', 's16le', '-'],
                                      capture_output=True).stdout, np.int16).astype(np.float32) / 32768
    dur = len(x0) / 16000
    m = WhisperModel('large-v3', device='cuda', compute_type='float16')
    out = []
    for i, (a, b) in enumerate(detectar(E)):
        a0, b0 = max(0, a - MARGEN_A), min(dur, b + MARGEN_B)
        x = np.concatenate([np.zeros(4000, np.float32), x0[int(a0 * 16000):int(b0 * 16000)], np.zeros(4000, np.float32)])
        segs, _ = m.transcribe(x, language='es', word_timestamps=True, initial_prompt=LITERAL, condition_on_previous_text=False)
        pal = [[w.word.strip(), round(a0 + w.start - .25, 3), round(a0 + w.end - .25, 3)] for s in segs for w in s.words]
        texto = ' '.join(p[0] for p in pal)
        if any(t in texto for t in ('Subtitulado', 'Amara', 'Subtitles', 'Gracias.')) and len(pal) <= 8: texto, pal = '', []   # alucinación en silencio/ruido
        out.append({'id': len(out), 'a': a0, 'b': b0, 'texto': texto, 'pal': pal})
        print(f"{len(out) - 1:3d}  {a0:7.2f}-{b0:7.2f}  {texto}")
    (d / 'islas.json').write_text(json.dumps(out, ensure_ascii=False, indent=0), encoding='utf-8')
