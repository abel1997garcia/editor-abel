"""Transcribe un audio con marcas de tiempo por palabra (sherpa-onnx + Parakeet v3).
Uso: python3 -I transcribir.py <modelo_dir> <entrada> <salida.json>
Corta el audio en trozos de ~20 s por los puntos más silenciosos y une las palabras."""
import json, subprocess, sys
import numpy as np
import sherpa_onnx

mdir, src, out = sys.argv[1:4]
SR = 16000
pcm = subprocess.run(['ffmpeg', '-v', 'error', '-i', src, '-ac', '1', '-ar', str(SR), '-f', 's16le', '-'],
                     capture_output=True, check=True).stdout
a = np.frombuffer(pcm, dtype=np.int16).astype(np.float32) / 32768

rec = sherpa_onnx.OfflineRecognizer.from_transducer(
    encoder=f'{mdir}/encoder.int8.onnx', decoder=f'{mdir}/decoder.int8.onnx',
    joiner=f'{mdir}/joiner.int8.onnx', tokens=f'{mdir}/tokens.txt',
    model_type='nemo_transducer', num_threads=4)

# energía cada 10 ms para cortar en silencios
hop = SR // 100
en = np.array([np.sqrt(np.mean(a[i:i + hop] ** 2) + 1e-12) for i in range(0, len(a), hop)])
cuts, pos = [0], 0
while pos + 22 * SR < len(a):
    lo, hi = (pos + 16 * SR) // hop, (pos + 24 * SR) // hop
    c = (lo + int(np.argmin(en[lo:hi]))) * hop
    cuts.append(c); pos = c
cuts.append(len(a))

words = []
for s, e in zip(cuts[:-1], cuts[1:]):
    st = rec.create_stream(); st.accept_waveform(SR, a[s:e]); rec.decode_stream(st)
    r = st.result
    off = s / SR
    cur = None
    for tok, ts in zip(r.tokens, r.timestamps):
        t = off + ts
        if tok.startswith(('▁', ' ')) or cur is None:
            if cur: words.append(cur)
            cur = {'w': tok.lstrip('▁ '), 't0': round(t, 2), 't1': round(t + .2, 2)}
        else:
            cur['w'] += tok; cur['t1'] = round(t + .2, 2)
    if cur: words.append(cur)
words = [w for w in words if w['w']]
json.dump({'dur': len(a) / SR, 'words': words}, open(out, 'w'), ensure_ascii=False)
print(len(words), 'palabras')
pass
