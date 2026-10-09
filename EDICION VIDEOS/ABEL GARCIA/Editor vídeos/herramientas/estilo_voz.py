"""Estilo de la voz de Abel en un reel → música que AMPLIFIQUE el mensaje (Abel 09/10/2026: «si hablo calmado y desde el amor y me
pones una canción cañera, el mensaje se pierde; la música siempre es un amplificador del mensaje»).

    python estilo_voz.py <voz.wav del reel> [--base <audio de la toma entera>]      -> estilo + canciones recomendadas

Voz (comparada con SU forma normal de hablar, la toma entera; si no se da, con valores medios suyos):
  ritmo (golpes de sílaba por segundo), entonación (cuánto sube y baja el tono, en semitonos), fuerza (volumen y contraste entre
  golpes), pausas. -> energía de -1 (calmado, desde el amor) a +1 (intenso, confrontación).
Música: «intensidad» de cada canción en MUSICA/catalogo.json (1 íntima, 2 media o que crece, 3 cañera; puesta a mano, las medidas
automáticas no distinguían bien phonk de piano). Las canciones nuevas se añaden con su intensidad y su «caracter».
Se recomiendan las canciones cuya energía encaja con la de la voz; entre ellas se elige por el «caracter» del catálogo y el mensaje.
"""
import json, subprocess, sys
from pathlib import Path
import numpy as np
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, str(Path(__file__).resolve().parent))
from reel_yapping import MUSICA, VELOCIDAD
SR = 16000
BASE_ABEL = {'ritmo': 4.2, 'tono_sd': 2.6, 'fuerza_sd': 6.5, 'pausas': .22}     # se recalibra con --base


def cargar(p, sr=SR, ss=None, t=None):
    cmd = ['ffmpeg', '-v', 'error'] + (['-ss', str(ss)] if ss is not None else []) + (['-t', str(t)] if t else []) + ['-i', str(p), '-vn', '-ac', '1', '-ar', str(sr), '-f', 's16le', '-']
    return np.frombuffer(subprocess.run(cmd, capture_output=True).stdout, np.int16).astype(np.float32) / 32768


def voz(a):
    import librosa
    rms = librosa.feature.rms(y=a, frame_length=512, hop_length=160)[0]; db = 20 * np.log10(rms + 1e-6)
    hablando = db > np.percentile(db, 95) - 25
    on = librosa.onset.onset_detect(y=a, sr=SR, hop_length=160, units='time')
    seg_voz = hablando.sum() * 160 / SR
    f0, v, _ = librosa.pyin(a, fmin=70, fmax=320, sr=SR, frame_length=1024, hop_length=320)
    f0 = f0[v & ~np.isnan(f0)]
    st = 12 * np.log2(f0 / np.median(f0)) if len(f0) > 20 else np.zeros(1)
    return {'ritmo': len(on) / max(seg_voz, 1), 'tono_sd': float(np.std(st)), 'fuerza_sd': float(np.std(db[hablando])),
            'pausas': float(1 - hablando.mean())}


def energia_voz(m, b):
    """las pausas no cuentan (las quita la edición); el ritmo del reel se compara sin la aceleración de 1,10x"""
    z = [(m['ritmo'] - b['ritmo']) / (.18 * b['ritmo']), (m['tono_sd'] - b['tono_sd']) / (.25 * b['tono_sd']),
         (m['fuerza_sd'] - b['fuerza_sd']) / (.2 * b['fuerza_sd'])]
    return float(np.clip(np.mean(z) / 1.5, -1, 1))


def main():
    m = voz(cargar(sys.argv[1]))
    if '--toma' not in sys.argv: m['ritmo'] /= VELOCIDAD                 # el reel va a 1,10x
    b = voz(cargar(sys.argv[sys.argv.index('--base') + 1])) if '--base' in sys.argv else BASE_ABEL
    e = energia_voz(m, b)
    estilo = 'CALMADO, DESDE EL AMOR' if e < -.25 else 'INTENSO, CONFRONTACIÓN' if e > .25 else 'FIRME Y CERCANO'
    print(f"voz: ritmo {m['ritmo']:.2f}/s (normal {b['ritmo']:.2f}) · entonación {m['tono_sd']:.1f} st ({b['tono_sd']:.1f}) · "
          f"fuerza {m['fuerza_sd']:.1f} dB ({b['fuerza_sd']:.1f}) · pausas {m['pausas']:.0%} ({b['pausas']:.0%})")
    print(f'ESTILO: {estilo}  (energía {e:+.2f})')
    nivel = 1 if e < -.25 else 3 if e > .25 else 2                                  # intensidad de música que le corresponde
    C = json.load(open(MUSICA / 'catalogo.json', encoding='utf-8'))
    print(f'MÚSICA que amplifica este estilo (intensidad {nivel}: 1 íntima · 2 media/crece · 3 cañera); elegir por el «caracter» y el mensaje:')
    for k in sorted([k for k in C if C[k].get('intensidad') == nivel], key=lambda k: C[k].get('tipo', '')):
        print(f"  {k}  — {C[k].get('caracter', '')}")

if __name__ == '__main__':
    main()
