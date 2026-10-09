"""Comprueba que un reel montado no se come palabras ni deja restos en los cortes.

Uso:
    python herramientas/comprobar_reel.py reels/01_la_voz.mp4 [reels/02_...mp4 ...]

Vuelve a transcribir el MP4 con Whisper y lo compara con el guion de subtítulos (trabajo/reels/<nombre>/montaje.json).
Lista las palabras que faltan (posible corte que se come una palabra) y las que sobran (resto de muletilla o de la
palabra siguiente), con el segundo del reel donde ocurre. Whisper también se equivoca: revisa a oído solo lo marcado.
"""
import difflib
import json
import re
import subprocess
import sys
import unicodedata
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / ".claude" / "skills" / "animaciones-horizontal-combinadas" / "scripts"))


def plano(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode("ascii").lower()
    return re.sub(r"[^a-z0-9]", "", s)


def main():
    for st in (sys.stdout, sys.stderr):
        try:
            st.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError, OSError):
            pass
    from transcribir import preparar_cuda
    preparar_cuda()
    from faster_whisper import WhisperModel
    try:
        model = WhisperModel("large-v3", device="cuda", compute_type="float16")
    except Exception:
        model = WhisperModel("medium", device="cpu", compute_type="int8")
    for mp4 in sys.argv[1:]:
        mp4 = Path(mp4)
        nombre = mp4.stem.replace("_borrador", "")
        montaje = json.load(open(RAIZ / "trabajo" / "reels" / nombre / "montaje.json", encoding="utf-8"))
        esperado = []
        for s in montaje["subtitulos"]:
            for w in s["txt"].split():
                esperado.append((plano(w), w, s["t0"]))
        wav = RAIZ / "trabajo" / "reels" / nombre / "comprobar.wav"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(mp4), "-ac", "1", "-ar", "16000", str(wav)], check=True)
        segs, _ = model.transcribe(str(wav), language="es", word_timestamps=True, beam_size=5,
                                   condition_on_previous_text=False, vad_filter=False,
                                   initial_prompt="Eh, pues, o sea, bueno... mmm, es que, este, ¿no?")
        oido = [(plano(w.word), w.word.strip(), w.start) for s in segs for w in (s.words or []) if plano(w.word)]
        A = [e[0] for e in esperado]
        B = [o[0] for o in oido]
        sm = difflib.SequenceMatcher(None, A, B, autojunk=False)
        print(f"== {mp4.name}: {len(A)} palabras en el guion, {len(B)} oídas, parecido {sm.ratio():.3f}")
        for op, i1, i2, j1, j2 in sm.get_opcodes():
            if op == "equal":
                continue
            t = oido[j1][2] if j1 < len(oido) else esperado[i1][2] if i1 < len(esperado) else 0
            g = " ".join(e[1] for e in esperado[i1:i2])
            o = " ".join(x[1] for x in oido[j1:j2])
            print(f"  {t:6.2f}s  {op:8s} guion: «{g}»  oído: «{o}»")


if __name__ == "__main__":
    main()
