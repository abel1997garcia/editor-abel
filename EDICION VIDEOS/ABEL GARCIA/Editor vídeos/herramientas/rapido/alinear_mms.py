"""Alineación FINA (letra a letra, ~20 ms) con el modelo MMS de torchaudio (ya en caché): dónde EMPIEZA y ACABA de verdad cada
palabra dentro de una isla. Whisper se equivoca hasta 0,2 s y «rellena» palabras cortadas (oye «trabajo» aunque falte la «o»);
en un corte A MITAD DE TOMA (sin silencio) eso se comía la última letra («trabaj», «tiemp»; 099, Abel 16/10/2026).

    from alinear_mms import palabras;  palabras(wav, a, b, texto) -> [(palabra, inicio, fin), ...] en segundos de la grabación
"""
import re, subprocess, unicodedata
import numpy as np
_M = {}


def _modelo():
    if not _M:
        import torch
        from torchaudio.pipelines import MMS_FA as B
        _M['m'] = B.get_model().to('cuda' if torch.cuda.is_available() else 'cpu').eval()
        _M['dic'] = B.get_dict(); _M['alin'] = B.get_aligner(); _M['tok'] = B.get_tokenizer()
    return _M


def limpia(w):
    w = unicodedata.normalize('NFD', w.lower().replace('ñ', 'n')); w = ''.join(c for c in w if unicodedata.category(c) != 'Mn')
    return re.sub(r'[^a-z]', '', w)


NUM = {'1': 'uno', '2': 'dos', '3': 'tres', '4': 'cuatro', '5': 'cinco', '6': 'seis', '7': 'siete', '8': 'ocho', '9': 'nueve', '10': 'diez',
       '100': 'cien', '15': 'quince', '%': 'por ciento'}


def palabras(wav, a, b, texto):
    import torch
    M = _modelo()
    x = np.frombuffer(subprocess.run(['ffmpeg', '-v', 'error', '-ss', f'{a:.3f}', '-to', f'{b:.3f}', '-i', str(wav), '-ac', '1', '-ar', '16000', '-f', 's16le', '-'],
                                     capture_output=True).stdout, np.int16).astype(np.float32) / 32768
    orig = [w for w in texto.split() if limpia(NUM.get(w.strip(',.?!¿¡'), w))]
    ws = [limpia(NUM.get(w.strip(',.?!¿¡'), w)).replace(' ', '') for w in orig]
    dev = next(M['m'].parameters()).device
    with torch.inference_mode():
        em, _ = M['m'](torch.from_numpy(x)[None].to(dev))
    spans = M['alin'](em[0].cpu(), M['tok'](ws))
    r = em.shape[1] / len(x) * 16000                                     # tramas por segundo
    return [(o, round(a + s[0].start / r, 3), round(a + s[-1].end / r, 3)) for o, s in zip(orig, spans)]
