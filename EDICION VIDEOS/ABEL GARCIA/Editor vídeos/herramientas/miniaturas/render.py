"""Miniaturas de Abel: HTML -> PNG y simulación en YouTube (modo claro y oscuro).

  python render.py v1.html v2.html ...          -> v1.png (1280x720) y v1_hd.png (1920x1080)
  python render.py --mock v1.png v2.png ...     -> mock_claro.png y mock_oscuro.png junto a la primera
     (rejilla de 3 columnas como la de YouTube, con miniaturas reales de otros canales alrededor)
"""
import subprocess, sys, pathlib, random
from PIL import Image, ImageDraw, ImageFont

CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
AQUI = pathlib.Path(__file__).resolve().parent
REFS = AQUI.parent.parent / "Miniaturas" / "_referencias"
INTER = str(AQUI.parent / "pizarra" / "assets" / "fonts" / "Inter-Variable.ttf")


def render(html):
    html = pathlib.Path(html).resolve()
    for escala, sufijo in ((1, ""), (1.5, "_hd")):
        out = html.with_name(html.stem + sufijo + ".png")
        subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--allow-file-access-from-files",
                        f"--force-device-scale-factor={escala}", "--window-size=1280,720", "--virtual-time-budget=3000",
                        f"--screenshot={out}", html.as_uri()], check=True, capture_output=True)
        print(out.name, Image.open(out).size)


def recortes_referencia():
    """Saca las miniaturas de las capturas de rejilla de _referencias (zonas no blancas con forma 16:9)."""
    tiles = []
    for f in sorted(REFS.glob("*.webp")):
        im = Image.open(f).convert("RGB"); g = im.convert("L"); w, h = im.size; px = g.load()
        def oscuro_col(x, y0, y1): return sum(px[x, y] < 235 for y in range(y0, y1, 3))
        filas = [y for y in range(h) if sum(px[x, y] < 235 for x in range(0, w, 4)) > w / 4 * .5]
        # bloques de filas seguidas
        bloques, ini = [], None
        for i, y in enumerate(filas):
            if ini is None: ini = y
            if i + 1 == len(filas) or filas[i + 1] != y + 1:
                if y - ini > 120: bloques.append((ini, y))
                ini = None
        for y0, y1 in bloques:
            cols = [x for x in range(w) if oscuro_col(x, y0, y1) > (y1 - y0) / 3 * .6]
            ini = None
            for i, x in enumerate(cols):
                if ini is None: ini = x
                if i + 1 == len(cols) or cols[i + 1] != x + 1:
                    if x - ini > 200: tiles.append(im.crop((ini, y0, x, y1)))
                    ini = None
    return tiles


def mock(pngs):
    pngs = [pathlib.Path(p).resolve() for p in pngs]
    vecinas = recortes_referencia(); random.Random(4).shuffle(vecinas)
    TW, TH, GAP, M = 420, 236, 16, 24
    cols, filas = 3, 3
    celdas = [("mia", p) for p in pngs]
    while len(celdas) < cols * filas: celdas.append(("otra", vecinas[len(celdas) % len(vecinas)]))
    # las tuyas repartidas entre las de otros canales
    orden = [celdas[0], celdas[3], celdas[4], celdas[5], celdas[1], celdas[6], celdas[7], celdas[8], celdas[2]] if len(pngs) == 3 else celdas
    f_tit = ImageFont.truetype(INTER, 17); f_tit.set_variation_by_axes([600])
    f_meta = ImageFont.truetype(INTER, 14)
    for modo, fondo, txt, meta in (("claro", "#FFFFFF", "#0F0F0F", "#606060"), ("oscuro", "#0F0F0F", "#F1F1F1", "#AAAAAA")):
        W = M * 2 + cols * TW + (cols - 1) * GAP; H = M * 2 + filas * (TH + 92)
        lienzo = Image.new("RGB", (W, H), fondo); d = ImageDraw.Draw(lienzo)
        for i, (tipo, src) in enumerate(orden):
            x = M + (i % cols) * (TW + GAP); y = M + (i // cols) * (TH + 92)
            im = (Image.open(src) if tipo == "mia" else src).convert("RGB").resize((TW, TH), Image.LANCZOS)
            mask = Image.new("L", (TW, TH), 0); ImageDraw.Draw(mask).rounded_rectangle((0, 0, TW - 1, TH - 1), 12, fill=255)
            lienzo.paste(im, (x, y), mask)
            d.rounded_rectangle((x + TW - 52, y + TH - 28, x + TW - 8, y + TH - 8), 4, fill="#141414")
            d.text((x + TW - 47, y + TH - 26), "24:18", font=f_meta, fill="#ffffff")
            d.text((x, y + TH + 12), "Título del vídeo que va aquí" if tipo == "mia" else "Vídeo de otro canal", font=f_tit, fill=txt)
            d.text((x, y + TH + 40), "Abel García · 1,2 K visualizaciones" if tipo == "mia" else "Otro canal · 3,4 K visualizaciones", font=f_meta, fill=meta)
        out = pngs[0].with_name(f"mock_{modo}.png"); lienzo.save(out); print(out.name, lienzo.size)
        # y a tamaño de móvil (la miniatura a ~ 170 px de ancho, como en la portada del móvil)
        lienzo.resize((W * 170 // TW, H * 170 // TW), Image.LANCZOS).save(pngs[0].with_name(f"mock_{modo}_movil.png"))


if __name__ == "__main__":
    a = sys.argv[1:]
    if a and a[0] == "--mock": mock(a[1:])
    else: [render(h) for h in a]
