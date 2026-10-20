"""Preparar una grabación CASUAL (F5/F4, guion grabado con el móvil) antes de montar sus 3 reels (Abel 13/10/2026).
    python casual_prep.py <carpeta>          (en la carpeta: fuente.mp4)
1. Limpia la voz con DeepFilterNet -> _fuente_limpia.wav (el ruido del móvil engañaba al cortador y a Whisper).
2. Transcribe ESE audio limpio con tiempos por palabra -> tiempos.json.
3. Avisa de las palabras sospechosamente largas: suelen esconder una pausa o una repetición (13/10: «Australia» de 4 s
   escondía «…desde cero» dicho dos veces). Hay que revisarlas antes de montar.
reel_tablero.py usa _fuente_limpia.wav para cortar los F5 (si existe)."""
import json, shutil, subprocess, sys
from pathlib import Path
import torch  # noqa: F401
from faster_whisper import WhisperModel
AQUI = Path(__file__).resolve().parent
# Whisper «limpia» lo que dice: «Solo… solo publicas» lo escribía como UN «Solo» estirado y la trabazón quedaba medio cortada
# en el reel (Abel 14/10/2026). Con un ejemplo de habla con trabazones en el prompt las transcribe tal cual.
LITERAL = 'Eh... vale, pues... que, que digo, que... Solo, solo publicas. Te da, te da miedo... Te... te ma... Mmm, o sea, eh...'
sys.stdout.reconfigure(encoding='utf-8')


def limpia(fuente, destino, fuerza=40):
    tmp = destino.parent / '_df'; shutil.rmtree(tmp, ignore_errors=True); tmp.mkdir()
    ori = tmp / 'fuente.wav'
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(fuente), '-vn', '-ac', '1', '-ar', '48000', str(ori)], check=True)
    subprocess.run([str(AQUI / 'deepfilter' / 'deep-filter.exe'), '-D', '--pf', '-a', str(fuerza), '-o', str(tmp / 'out'), str(ori)], check=True, capture_output=True)
    shutil.move(str(tmp / 'out' / 'fuente.wav'), destino); shutil.rmtree(tmp, ignore_errors=True)


if __name__ == '__main__':
    d = Path(sys.argv[1]); lim = d / '_fuente_limpia.wav'
    if not lim.exists(): limpia(d / 'fuente.mp4', lim); print('voz limpia ->', lim.name)
    if (d / 'tiempos.json').exists() and '--rehacer' not in sys.argv: (d / 'tiempos.json').rename(d / 'tiempos_unapasada.json')
    m = WhisperModel('large-v3', device='cuda', compute_type='float16')
    # POR VENTANAS de 12 s (079-082, Abel 15/10/2026): de una pasada Whisper junta tomas repetidas en una palabra «larga» y
    # descoloca los tiempos («mundo» 1 s más tarde) → el cortador se comía la palabra buena. Ventana a ventana las oye todas.
    import numpy as np
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', str(lim), '-ac', '1', '-ar', '16000', '-f', 's16le', '-'], capture_output=True).stdout
    audio = np.frombuffer(raw, np.int16).astype(np.float32) / 32768; dur = len(audio) / 16000
    import re
    nrm = lambda w: re.sub(r'[^a-z0-9ñ]', '', w.lower().translate(str.maketrans('áéíóúü', 'aeiouu')))
    def pasada(inicio):                                   # ventanas de 14 s cada 12 s; cada palabra, de la ventana donde queda centrada
        out, a, corte = [], inicio, inicio
        while a < dur:
            x = audio[int(a * 16000):int(min(dur, a + 14) * 16000)]
            segs, _ = m.transcribe(x, language='es', word_timestamps=True, vad_filter=True, vad_parameters={'min_silence_duration_ms': 150},
                                   condition_on_previous_text=False, initial_prompt=LITERAL)
            hasta = a + 13 if a + 14 < dur else 1e9
            for s_ in segs:
                for w in s_.words:
                    t0 = a + w.start
                    if corte <= t0 < hasta: out.append((round(t0, 3), round(a + w.end, 3), w.word.strip(), round(w.probability, 2)))
            corte = hasta; a += 12
        return out
    A, B = pasada(0.0), pasada(6.0)                       # dos pasadas desplazadas 6 s: lo que una pierde en un borde, la otra lo oye entero
    todo = sorted(A + [b for b in B if b[0] < 6 or not any(abs(b[0] - x[0]) < .25 and nrm(b[2]) == nrm(x[2]) for x in A)
                       and not any(abs(b[0] - x[0]) < .08 for x in A)])
    W = [{'i': i, 'w': w, 's': s0, 'e': e0, 'score': sc, 'frase': 0} for i, (s0, e0, w, sc) in enumerate(todo)]
    json.dump(W, open(d / 'tiempos.json', 'w', encoding='utf-8'), ensure_ascii=False)
    print(' '.join(f"{w['i']}:{w['w']}@{w['s']:.2f}" for w in W))
    largas = [w for w in W if w['e'] - w['s'] > .35 + .09 * len(w['w'])]
    print('\nPALABRAS SOSPECHOSAMENTE LARGAS (revisar: pausa o repetición escondida):' if largas else '\nsin palabras sospechosas')
    for w in largas: print(f"  {w['i']}: «{w['w']}» {w['s']:.2f}–{w['e']:.2f} ({w['e'] - w['s']:.2f} s)")
