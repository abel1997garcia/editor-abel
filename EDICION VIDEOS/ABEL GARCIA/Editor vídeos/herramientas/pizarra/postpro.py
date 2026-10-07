"""Frases destacadas bajo Abel en el horizontal: Inter 900 blanca con sombra suave, centradas y dentro del 4:3.
    python postpro.py <proyecto de la skill> <citas.json> <montaje.mp4> <salida.mp4>
citas.json: [["texto (\\N = salto)", "frase donde entra", desde ~s, "frase donde sale (+0,8 s)" | null = hasta la siguiente animación o el final]]
Solo van sobre su cara (si pisan una animación, se avisa). La voz y el final no se tocan: el audio es su voz tal cual
(edicion/voz_cortada.wav, sin normalizar) + los efectos de la mezcla de la skill a la misma proporción; solo un
limitador para los picos."""
import json, re, shutil, subprocess, sys, tempfile
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from ventanas import buscar

FUENTE = Path(__file__).resolve().parents[1] / 'fuentes/InterCita.ttf'
lufs = lambda f: float(re.findall(r'I:\s+(-?[\d.]+) LUFS', subprocess.run(['ffmpeg', '-hide_banner', '-nostats', '-i', str(f), '-af', 'ebur128', '-f', 'null', '-'], capture_output=True, text=True).stderr)[-1])
ts_ass = lambda s: f'{int(s // 3600)}:{int(s % 3600 // 60):02d}:{s % 60:05.2f}'


def main(pro, citas, entrada, salida):
    pro = Path(pro)
    W = json.load(open(pro / 'trabajo/tiempos.json', encoding='utf-8'))
    m = json.load(open(pro / 'edicion/montaje.json', encoding='utf-8'))
    fps, anims, dur = m['fps'], [p for p in m['planos'] if p['tipo'] == 'anim'], m['planos'][-1]['f1'] / m['fps']
    ev = []
    for texto, ini, desde, fin in json.load(open(citas, encoding='utf-8')):
        a, _ = buscar(W, ini, desde); t0 = W[a]['s'] - .1
        t0 = max([t0] + [p['f1'] / fps for p in anims if p['f0'] / fps < t0 < p['f1'] / fps])   # entra al volver a su cara
        if fin: _, b = buscar(W, fin, t0); t1 = W[b]['e'] + .8
        else: t1 = min([p['f0'] / fps for p in anims if p['f0'] / fps > t0] + [dur])
        if any(p['f0'] / fps < t1 and p['f1'] / fps > t0 for p in anims): sys.exit(f'la cita «{texto}» pisa una animación')
        ef = r'{\pos(960,1010)\fad(160,160)\fscx92\fscy92\t(0,220,\fscx100\fscy100)}'
        ev += [f'Dialogue: 0,{ts_ass(t0)},{ts_ass(t1)},Sombra,,0,0,0,,{ef}{{\\blur12}}{texto}',
               f'Dialogue: 1,{ts_ass(t0)},{ts_ass(t1)},Cita,,0,0,0,,{ef}{texto}']
    tmp = Path(tempfile.mkdtemp())                       # libass y ffmpeg sin acentos en la ruta
    (tmp / 'citas.ass').write_text(f"""[Script Info]
ScriptType: v4.00+
PlayResX: 1920
PlayResY: 1080
WrapStyle: 2

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Cita,Inter Cita,100,&H00FFFFFF,&H00FFFFFF,&H00000000,&H00000000,0,0,0,0,100,100,-2,0,1,0,0,2,0,0,0,1
Style: Sombra,Inter Cita,100,&H70000000,&H70000000,&H70000000,&H00000000,0,0,0,0,100,100,-2,0,1,6,0,2,0,0,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
""" + '\n'.join(ev) + '\n', encoding='utf-8')
    shutil.copy(FUENTE, tmp / 'InterCita.ttf')
    voz, efe = (pro / 'edicion/voz_cortada.wav').resolve(), (pro / 'trabajo/pistas/efectos.wav').resolve()
    g = lufs(voz) - lufs(pro / 'trabajo/pistas/voz.wav')        # la skill normalizó la voz: los efectos suben/bajan igual
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(Path(entrada).resolve()), '-i', str(voz), '-i', str(efe), '-filter_complex',
                    f'[0:v]subtitles=citas.ass:fontsdir=.,format=yuv420p[v];[2:a]volume={g:.2f}dB[e];'
                    f'[1:a][e]amix=inputs=2:normalize=0:duration=first,alimiter=limit=0.891:level=0[a]',
                    '-map', '[v]', '-map', '[a]', '-c:v', 'libx264', '-preset', 'medium', '-crf', '17', '-c:a', 'aac', '-b:a', '256k', '-ar', '48000',
                    str(Path(salida).resolve())], check=True, cwd=tmp)
    print(f'{len(ev) // 2} citas -> {salida}')


if __name__ == '__main__':
    main(*sys.argv[1:5])
