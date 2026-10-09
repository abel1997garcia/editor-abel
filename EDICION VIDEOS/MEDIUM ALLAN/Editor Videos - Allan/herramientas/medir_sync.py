"""Mide si la IMAGEN de un reel corresponde a su AUDIO (sincronía), trozo a trozo.

Uso:
    python herramientas/medir_sync.py reels/01_la_voz.mp4 [...] [--video "historia allan medium.mp4"]

Para cada trozo del montaje (trabajo/reels/<nombre>/montaje.json) compara todos sus fotogramas con los del original desplazados
-5..+5 fotogramas respecto al instante del que se sacó el audio. Imprime el desfase en fotogramas (0 = sincronizado; + = la
imagen va adelantada respecto a la voz). Decodifica cada vídeo una sola vez a baja resolución (rápido).
"""
import argparse
import json
import subprocess
import sys
from pathlib import Path

import numpy as np

RAIZ = Path(__file__).resolve().parent.parent
FPS = 30
W, H = 54, 38   # zona de la cara (franja central del vídeo), muy reducida


ZONA = {"franjas_azules": "crop=1080:770:0:590", "franja_negra": "crop=1080:760:0:80"}


def decodificar(src, ini=0.0, dur=None, zona=ZONA["franjas_azules"]):
    cmd = ["ffmpeg", "-v", "error", "-ss", f"{ini:.4f}", "-i", str(src)]
    if dur:
        cmd += ["-t", f"{dur:.4f}"]
    cmd += ["-vf", f"fps={FPS},{zona},scale={W}:{H}", "-f", "rawvideo", "-pix_fmt", "gray", "-"]
    raw = subprocess.run(cmd, capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.uint8).reshape(-1, H * W).astype(np.float32)


def main():
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser()
    ap.add_argument("reels", nargs="+")
    ap.add_argument("--video", default=str(RAIZ / "historia allan medium.mp4"))
    a = ap.parse_args()
    for mp4 in a.reels:
        nombre = Path(mp4).stem.replace("_borrador", "")
        M = json.load(open(RAIZ / "trabajo" / "reels" / nombre / "montaje.json", encoding="utf-8"))
        zona = ZONA[M.get("estilo", "franjas_azules")]
        zona_o = zona
        comp = M.get("componer")
        if comp:   # original horizontal: aplicar la misma transformación que en el montaje
            alto = comp.get("alto", 768)
            zona = f"crop=1080:{alto}:0:{comp.get('y', 588)}"
            zona_o = f"scale=-2:{alto},crop=1080:{alto}:{comp.get('x', '(iw-1080)/2')}:0"
        R = decodificar(mp4, zona=zona)
        lo = max(0.0, min(s["ini"] for s in M["segmentos"]) - 2)
        hi = max(s["fin"] for s in M["segmentos"]) + 2
        O = decodificar(M.get("video", a.video), lo, hi - lo, zona_o)
        des = []
        for s in M["segmentos"]:
            n = int(round((s["fin"] - s["ini"]) * FPS))
            r0 = int(round(s["out"] * FPS))
            o0 = int(round((s["ini"] - lo) * FPS))
            m = min(n, len(R) - r0)
            if m < 6:
                continue
            # media de TODOS los fotogramas del trozo para cada desfase candidato (robusto si está quieto)
            err = {d: np.mean([np.abs(O[o0 + k + d] - R[r0 + k]).mean() for k in range(2, m - 2)])
                   for d in range(-5, 6) if 0 <= o0 + 2 + d and o0 + m - 2 + d < len(O)}
            des.append(min(err, key=err.get))
        malos = [d for d in des if d != 0]
        estado = "OK, sincronizado" if not malos else f"DESFASE en {len(malos)} trozos"
        print(f"{nombre}: {len(des)} trozos medidos -> {estado}   desfases: {des}")


if __name__ == "__main__":
    main()
