"""Monta un reel vertical estilo «franjas azules» (Allan médium) a partir de un guion de cortes palabra a palabra.

Uso:
    python herramientas/reel_franjas.py <spec.json> [--video "historia allan medium.mp4"] [--tiempos trabajo/tiempos.json]
                                        [--borrador] [--solo-hoja]

spec.json:
    {"nombre": "01_la_voz", "titulo": "UNA VOZ ME DIJO QUE LO DEJARA TODO",
     "lineas": [[476, 479, "Una voz me dijo"], [480, 484, "este no es tu lugar"], ...]}
    Cada línea = palabras [a..b] (índices de trabajo/tiempos.json) que se quedan + el texto del subtítulo tal cual se ve.
    El orden de las líneas es el orden del reel (el gancho puede ir primero aunque sea de más adelante).
    Lo que no está en ninguna línea (muletillas, repeticiones, equivocaciones) se corta.

Estilo (ver ESTILO_REELS_FRANJAS_AZULES.md):
    título  Montserrat ExtraBold 50 px (= 33 de OpusClip), MAYÚSCULAS, centrado, negro, sin fondo, franja de arriba.
    subtítulos  Montserrat Bold 66 px (= 44 de OpusClip), una línea, minúsculas salvo inicio de frase, negro, franja de abajo.
"""
import argparse
import json
import math
import re
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

RAIZ = Path(__file__).resolve().parent.parent
FPS = 30
SR = 48000
W_, H_ = 1080, 1920

# --- estilo (lo fija el usuario en px: título 60, subtítulos 44) ---
TITULO_FUENTE = RAIZ / "fuentes" / "Montserrat-ExtraBold.ttf"
TITULO_PX = 60
TITULO_INTERLINEA = 67
TITULO_BASE_ULTIMA = 553       # línea base de la última línea del título (la franja de arriba acaba en y≈590)
TITULO_ANCHO_MAX = 900
SUB_FUENTE = RAIZ / "fuentes" / "Montserrat-Bold.ttf"
SUB_PX = 44
SUB_PX_MIN = 38
SUB_BASE = 1445                # línea base del subtítulo (la franja de abajo empieza en y≈1356)
SUB_ANCHO_MAX = 960
COLOR = (0, 0, 0, 255)
# no dejar estas palabras colgando al final de una línea al partir
DEBILES = {"a", "al", "de", "del", "el", "la", "los", "las", "lo", "un", "una", "y", "e", "o", "que", "en", "con", "por",
           "para", "mi", "mis", "tu", "su", "me", "te", "se", "le", "nos", "es", "muy", "no", "sin", "como", "si", "ya"}


def debil(linea):
    return re.sub(r"[^\wáéíóúñü]", "", linea.split()[-1].lower()) in DEBILES

# --- estilo «franja negra» (canalizaciones): subtítulos OpusClip dentro de la franja negra, sin título ---
NEGRA_FUENTE = RAIZ / "fuentes" / "Montserrat-Bold.ttf"
NEGRA_PX = 60                  # medido en los reels del usuario (39 de OpusClip ≈ 59–60 px reales)
NEGRA_CENTRO_Y = 959           # centro de las mayúsculas = centro de la franja (en el bruto, franja y = 858–1060)
NEGRA_ANCHO_MAX = 900
NEGRA_MAX_PALABRAS = 3
BLANCO = (255, 255, 255, 255)

# --- cortes ---
PRE = 0.12        # margen antes de la primera sílaba de un trozo (solo si no hay audio para refinar)
POST = 0.20       # margen tras la última sílaba (solo si no hay audio para refinar)
MAX_PAUSA = 0.55  # pausas más largas se recortan (feedback: «demasiado silencio»); quedan ~0,25 s de respiración
RESP_FIN = 0.13   # respiración que se deja tras el final REAL de la voz (medido en el audio)
RESP_INI = 0.10   # y antes del arranque REAL de la voz
AUDIO = None      # (muestras 16 kHz mono, sr) del original, para colocar cada corte en el silencio real
FUNDIDO = 0.025   # fundido de audio en cada empalme (cae en la respiración): empalmes suaves, no bruscos


def utf8():
    for s in (sys.stdout, sys.stderr):
        try:
            s.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError, OSError):
            pass


def fq(t):
    return round(t * FPS) / FPS


def trozos(W, lineas):
    """Agrupa las palabras de las líneas en trozos continuos de la toma original."""
    orden = []   # (indice_palabra, n_linea)
    for n, (a, b, _) in enumerate(lineas):
        for k in range(a, b + 1):
            orden.append((k, n))
    segs = []
    for j, (k, n) in enumerate(orden):
        nuevo = (j == 0 or orden[j - 1][0] != k - 1 or (W[k]["s"] - W[k - 1]["e"]) > MAX_PAUSA
                 or "hueco_antes" in W[k] or "ini_fijo" in W[k] or (k > 0 and "fin_max" in W[k - 1]))
        if nuevo:
            segs.append({"palabras": [k]})
        else:
            segs[-1]["palabras"].append(k)
    for s in segs:
        a, b = s["palabras"][0], s["palabras"][-1]
        ini = W[a]["s"] - PRE
        if a > 0:
            ini = max(ini, W[a - 1]["e"] + 0.02)
        if "hueco_antes" in W[a]:              # muletilla extirpada a mano justo antes de esta palabra
            ini = max(ini, W[a]["hueco_antes"][1])
        fin = W[b]["e"] + POST
        if "fin_max" in W[b]:                  # muletilla pegada DESPUÉS de esta palabra («alemanes, ¿no?»)
            fin = min(fin, W[b]["fin_max"])
        if b + 1 < len(W):
            fin = min(fin, W[b + 1]["s"] - 0.03)
            if "hueco_antes" in W[b + 1]:
                fin = min(fin, W[b + 1]["hueco_antes"][0])
        s["ini"], s["fin"] = fq(ini), fq(fin)
        if s["fin"] <= s["ini"]:
            s["fin"] = s["ini"] + 1 / FPS
    if AUDIO is not None:
        refinar_bordes(W, segs)
    quitar_rafagas(W, segs)
    t = 0.0
    for s in segs:
        s["out"] = t
        t += s["fin"] - s["ini"]
    return segs, round(t * FPS) / FPS


def _rms(t0, t1):
    y, sr = AUDIO
    hop = sr // 100                                   # 10 ms
    i0, i1 = max(0, int(t0 * sr)), min(len(y), int(t1 * sr))
    if i1 - i0 < hop:
        return np.array([t0]), np.array([0.0])
    n = (i1 - i0) // hop
    blk = y[i0:i0 + n * hop].reshape(n, hop)
    return t0 + np.arange(n) / 100.0, np.sqrt((blk ** 2).mean(1))


def _umbral(t0, t1):
    _, r = _rms(t0 - 1.0, t1 + 1.0)
    ruido, pico = np.percentile(r, 10), np.percentile(r, 95)
    return max(60.0, ruido * 1.8, ruido + 0.06 * (pico - ruido))


def _rms_agudos(t0, t1):
    """Energía de la parte aguda (diferencia de muestras): ahí suenan s, f, j, que casi no tienen energía total."""
    y, sr = AUDIO
    hop = sr // 100
    i0, i1 = max(1, int(t0 * sr)), min(len(y), int(t1 * sr))
    if i1 - i0 < hop:
        return np.array([0.0])
    n = (i1 - i0) // hop
    d = (y[i0:i0 + n * hop] - y[i0 - 1:i0 + n * hop - 1]).reshape(n, hop)
    return np.sqrt((d ** 2).mean(1))


def _huecos(t0, t1, u, minimo=0.04):
    """Huecos de silencio (sin voz NI fricativas durante >= 40 ms) entre t0 y t1: lista de (inicio, fin)."""
    ts, r = _rms(t0, t1)
    ra = _rms_agudos(t0, t1)[:len(r)]
    _, ra_ctx = _rms(t0 - 1.0, t1 + 1.0)
    ra_ctx = _rms_agudos(t0 - 1.0, t1 + 1.0)
    ua = max(ra_ctx.min() * 1.0 + 1e-6, np.percentile(ra_ctx, 10) * 2.2)
    if len(ra) < len(r):
        ra = np.pad(ra, (0, len(r) - len(ra)))
    bajo = (r < u) & (ra < ua)
    out, k = [], 0
    while k < len(r):
        if bajo[k]:
            m = k
            while m < len(r) and bajo[m]:
                m += 1
            if (m - k) / 100.0 >= minimo:
                out.append((ts[k], ts[k] + (m - k) / 100.0))
            k = m
        else:
            k += 1
    return out, ts, r


def refinar_bordes(W, segs):
    """Coloca cada corte en el silencio REAL (energía del audio), no donde dice la alineación.
    Feedback del usuario: «a veces cortas la palabra, otras no acaba la palabra y la cortas, otras dejas demasiado
    silencio». La alineación falla sobre todo en las palabras DESCARTADAS vecinas (muletillas, tartamudeos), así que
    no se usan como límite duro: se buscan los huecos de silencio reales (>= 40 ms) y se elige el más cercano a la
    frontera entre palabras, dejando una respiración corta que nunca llega a la voz vecina."""
    for sg in segs:
        a, b = sg["palabras"][0], sg["palabras"][-1]
        # ---- final del trozo ----
        frontera = W[b]["e"]
        t0 = max(W[b]["s"] + 0.05, frontera - 0.25)
        t1 = (W[b + 1]["e"] if b + 1 < len(W) else frontera + 1.0)
        t1 = max(t1, frontera + 0.3)
        if b + 1 < len(W) and "hueco_antes" in W[b + 1]:
            t1 = min(t1, W[b + 1]["hueco_antes"][1])
        if "fin_max" in W[b]:
            t1 = min(t1, W[b]["fin_max"] + 0.3)
        u = _umbral(t0, t1)
        huecos, ts, r = _huecos(t0, t1, u, minimo=0.06)
        # REGLA DURA (error repetido 2 veces: «exist», «cort»): las oclusivas (t, p, c, d) hacen un silencio de
        # 50-90 ms DENTRO de la palabra. Nunca se acepta un hueco que empiece antes del final alineado de la palabra.
        suelo = frontera - 0.03
        if "fin_max" in W[b] and W[b]["fin_max"] < frontera:
            suelo = W[b]["fin_max"] - 0.15
        validos = [h for h in huecos if h[0] >= suelo]
        if "fin_max" in W[b]:
            validos = [h for h in validos if h[0] <= W[b]["fin_max"] + 0.02]
        if validos:
            h0, h1 = min(validos, key=lambda h: h[0])     # el primer silencio DESPUÉS de acabar la palabra
            fin = h0 + min(RESP_FIN, max(0.0, (h1 - h0) - 0.03))
        else:                                            # sin silencio: valle de energía justo después del final
            cerca = (ts >= frontera) & (ts <= frontera + 0.15)
            fin = ts[cerca][int(np.argmin(r[cerca]))] if cerca.any() else frontera + 0.05
        fin = max(fin, frontera if "fin_max" not in W[b] else min(frontera, W[b]["fin_max"]))
        if "fin_max" in W[b]:
            fin = min(fin, W[b]["fin_max"])
        if "fin_max" in W[b]:
            fin = min(fin, W[b]["fin_max"])
        sg["fin"] = math.floor(fin * FPS + 1e-6) / FPS if math.ceil(fin * FPS - 1e-6) / FPS > fin + 0.02 else math.ceil(fin * FPS - 1e-6) / FPS
        # ---- inicio del trozo ----
        frontera = W[a]["s"]
        t1 = min(W[a]["e"] - 0.02, frontera + 0.25)
        t0 = (W[a - 1]["s"] if a > 0 else frontera - 1.0)
        t0 = min(t0, frontera - 0.3)
        if "hueco_antes" in W[a]:
            t0 = max(t0, W[a]["hueco_antes"][0])
            frontera = max(frontera, W[a]["hueco_antes"][1])
        if a > 0 and "fin_max" in W[a - 1]:
            t0 = max(t0, W[a - 1]["fin_max"])
        u = _umbral(t0, t1)
        huecos, ts, r = _huecos(max(0.0, t0), t1, u, minimo=0.06)
        if "hueco_antes" in W[a]:
            huecos = [h for h in huecos if h[1] >= W[a]["hueco_antes"][1] - 0.02] or huecos
        # REGLA DURA: el inicio nunca cae DESPUÉS del arranque alineado de la palabra (no comerse su principio)
        validos = [h for h in huecos if h[1] <= frontera + 0.03]
        if validos:
            h0, h1 = max(validos, key=lambda h: h[1])     # el último silencio ANTES de que empiece la palabra
            ini = h1 - min(RESP_INI, max(0.0, (h1 - h0) - 0.03))
        else:
            cerca = (ts >= frontera - 0.15) & (ts <= frontera)
            ini = ts[cerca][int(np.argmin(r[cerca]))] if cerca.any() else frontera - 0.05
        ini = min(ini, frontera)
        if "ini_fijo" in W[a]:                           # arranque medido ESCUCHANDO (buscar_inicio.py): manda,
            ini = W[a]["ini_fijo"] + 0.03                # con margen y redondeando HACIA DELANTE (si no, asoma la muletilla)
            sg["ini"] = math.ceil(ini * FPS - 1e-6) / FPS
            if sg["fin"] <= sg["ini"]:
                sg["fin"] = sg["ini"] + 1 / FPS
            continue
        if "hueco_antes" in W[a]:
            ini = max(ini, W[a]["hueco_antes"][0] if not huecos else ini)
        sg["ini"] = math.ceil(ini * FPS - 1e-6) / FPS if math.floor(ini * FPS + 1e-6) / FPS < ini - 0.02 else math.floor(ini * FPS + 1e-6) / FPS
        if sg["fin"] <= sg["ini"]:
            sg["fin"] = sg["ini"] + 1 / FPS


def revisar_cortes(segs):
    """Aviso si un trozo empieza o acaba con voz sonando (corte a mitad de palabra)."""
    if AUDIO is None:
        return
    for i, sg in enumerate(segs):
        u = _umbral(sg["ini"], sg["fin"])
        _, r0 = _rms(sg["ini"], sg["ini"] + 0.03)
        _, r1 = _rms(sg["fin"] - 0.03, sg["fin"])
        _, rv = _rms(sg["ini"], sg["fin"])
        alto = 0.35 * np.percentile(rv, 90)
        if r1.mean() > max(u, alto):
            print(f"   AVISO corte con voz al FINAL del trozo {i} ({sg['fin']:.2f} s)")
        if r0.mean() > max(u, alto):
            print(f"   AVISO corte con voz al INICIO del trozo {i} ({sg['ini']:.2f} s)")


def quitar_rafagas(W, segs, ventana=3.0, pausa_max=0.8):
    """3 cortes en < 3 s suenan a «corte, corte, corte» (feedback del usuario). Si pasa, se CONSERVA la pausa más corta
    del grupo (solo pausas entre palabras seguidas de hasta 0,6 s: con 1,2 s quedaba «demasiado silencio»). Se repite."""
    while True:
        t, outs = 0.0, []
        for sg in segs:
            outs.append(t)
            t += sg["fin"] - sg["ini"]
        hecho = False
        for j in range(1, len(segs) - 2):
            if outs[j + 2] - outs[j] >= ventana:
                continue
            cands = []
            for b in (j - 1, j, j + 1):            # frontera entre segs[b] y segs[b+1]
                x, y = segs[b]["palabras"][-1], segs[b + 1]["palabras"][0]
                gap = W[y]["s"] - W[x]["e"]
                manual = "hueco_antes" in W[y] or "ini_fijo" in W[y] or "fin_max" in W[x]   # cortes puestos a mano: no se deshacen
                if y == x + 1 and not manual and gap <= pausa_max:
                    cands.append((gap, b))
            if cands:
                _, b = min(cands)
                segs[b] = {"palabras": segs[b]["palabras"] + segs[b + 1]["palabras"],
                           "ini": segs[b]["ini"], "fin": segs[b + 1]["fin"]}
                del segs[b + 1]
                hecho = True
                break
        if not hecho:
            return


def recortar_silencios(video, segs, W):
    """La alineación forzada a veces estira una palabra sobre el silencio que la sigue (sobre todo la última de una
    frase de la persona por videollamada: «dos» duró 2,6 s y el reel acabó con silencio). Aquí se mira la energía real
    del audio de cada trozo y se recorta el silencio del principio y del final, dejando los márgenes PRE/POST."""
    for sg in segs:
        d = sg["fin"] - sg["ini"]
        raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{sg['ini']:.4f}", "-t", f"{d:.4f}", "-i", str(video),
                              "-vn", "-ac", "1", "-ar", "16000", "-f", "s16le", "-"], capture_output=True).stdout
        y = np.frombuffer(raw, np.int16).astype(np.float32)
        if len(y) < 640:
            continue
        hop = 320                                           # 20 ms
        rms = np.sqrt(np.array([np.mean(y[i:i + hop] ** 2) for i in range(0, len(y) - hop, hop)]))
        # umbral adaptativo: 3× el ruido de fondo del trozo o 25 % del pico (el micro de la videollamada mete ruido)
        umbral = max(150.0, 3 * np.percentile(rms, 10), 0.25 * np.percentile(rms, 95))
        # voz = al menos 60 ms seguidos por encima del umbral (un chasquido o el arranque de la palabra siguiente no cuentan)
        alto = (rms > umbral).astype(int)
        sost = np.convolve(alto, np.ones(3, int), mode="same") >= 3
        voz = np.where(np.convolve(sost.astype(int), np.ones(3, int), mode="same") > 0)[0]
        if not len(voz):
            continue
        t_ini = voz[0] * hop / 16000
        t_fin = (voz[-1] + 1) * hop / 16000
        nuevo_ini = fq(sg["ini"] + max(0.0, t_ini - PRE))
        nuevo_fin = fq(sg["ini"] + min(d, t_fin + POST))
        # SOLO donde la alineación estiró la palabra (> 1 s) y sobra silencio de verdad (> 0,3 s). Recortar por energía en
        # cualquier trozo se comía palabras dichas muy flojito («que con el tiempo» de Allan).
        k0, kf = sg["palabras"][0], sg["palabras"][-1]
        if sg["fin"] - nuevo_fin < 0.3 or W[kf]["e"] - W[kf]["s"] <= 1.0:
            nuevo_fin = sg["fin"]
        if nuevo_ini - sg["ini"] < 0.3 or W[k0]["e"] - W[k0]["s"] <= 1.0:
            nuevo_ini = sg["ini"]
        if nuevo_fin < sg["fin"] - 0.15 or nuevo_ini > sg["ini"] + 0.15:
            print(f"   (silencio recortado en el trozo de «{W[sg['palabras'][0]]['w']} … {W[sg['palabras'][-1]]['w']}»: "
                  f"{sg['ini']:.2f}-{sg['fin']:.2f} -> {nuevo_ini:.2f}-{nuevo_fin:.2f})")
        if nuevo_fin > nuevo_ini:
            sg["ini"], sg["fin"] = nuevo_ini, nuevo_fin
    t = 0.0
    for sg in segs:
        sg["out"] = t
        t += sg["fin"] - sg["ini"]
    return round(t * FPS) / FPS


def tiempo_salida(segs, k, W):
    for s in segs:
        if k in s["palabras"]:
            return s["out"] + max(0.0, W[k]["s"] - s["ini"])
    raise KeyError(k)


def limpiar_sub(txt):
    txt = re.sub(r"[.,;:…]+", "", txt).strip()
    return re.sub(r"\s+", " ", txt)


def envolver(texto, fuente, ancho):
    """Reparte el texto en el mínimo de líneas que caben y, con ese número, lo más equilibradas posible."""
    palabras = texto.split()
    n = len(palabras)
    import itertools
    for nl in range(1, n + 1):
        mejor = None
        for cortes in itertools.combinations(range(1, n), nl - 1):
            idx = (0,) + cortes + (n,)
            ls = [" ".join(palabras[idx[i]:idx[i + 1]]) for i in range(nl)]
            anchos = [fuente.getlength(l) for l in ls]
            if max(anchos) > ancho:
                continue
            # equilibrio; a igualdad, la de abajo un poco más larga (pirámide)
            nota = (sum(debil(l) for l in ls[:-1]), max(anchos) - min(anchos), -anchos[-1])
            if mejor is None or nota < mejor[0]:
                mejor = (nota, ls)
        if mejor:
            return mejor[1]
    return [texto]


SUB_LEGIBLE_PX = 760     # más ancho que esto se lee con prisa en un reel (feedback: «frase muy larga, no se entiende»)
SUB_MAX_PALABRAS = 6


def partir_lineas(lineas):
    """Subtítulos largos se parten SIEMPRE por palabras (nunca se encoge la letra): máx. 6 palabras y ~760 px.
    Si el texto no tiene las mismas palabras que el tramo de audio, el corte de tiempo se reparte proporcionalmente.
    (Error ya cometido: con nº de palabras distinto no partía y encogía la letra a 38 px -> frase ilegible.)"""
    f = ImageFont.truetype(str(SUB_FUENTE), SUB_PX)
    out = []
    pendientes = list(lineas)
    while pendientes:
        a, b, txt = pendientes.pop(0)
        pals = txt.split()
        n_idx = b - a + 1
        larga = f.getlength(limpiar_sub(txt)) > SUB_LEGIBLE_PX or len(pals) > SUB_MAX_PALABRAS
        if not larga or len(pals) < 2:
            out.append([a, b, txt])
            continue
        if n_idx < 2:
            print(f"   AVISO: «{txt}» es larga pero su audio es una sola palabra alineada: no se puede repartir el tiempo")
            out.append([a, b, txt])
            continue
        mejor = None
        for jj in range(1, len(pals)):
            w1 = f.getlength(limpiar_sub(" ".join(pals[:jj])))
            w2 = f.getlength(limpiar_sub(" ".join(pals[jj:])))
            nota = max(w1, w2) + (400 if debil(" ".join(pals[:jj])) else 0)
            if mejor is None or nota < mejor[0]:
                mejor = (nota, jj)
        jj = mejor[1]
        # índice de audio donde empieza la 2.ª parte (exacto si coinciden las palabras; si no, proporcional)
        k = a + jj if len(pals) == n_idx else a + max(1, min(n_idx - 1, round(jj * n_idx / len(pals))))
        pendientes[0:0] = [[a, k - 1, " ".join(pals[:jj])], [k, b, " ".join(pals[jj:])]]
    return out


def comprobar_subtitulos(subs):
    """Comprobación dura antes de renderizar: ningún subtítulo encogido ni ilegible."""
    f = ImageFont.truetype(str(SUB_FUENTE), SUB_PX)
    malos = [x["txt"] for x in subs if x["txt"] and (f.getlength(x["txt"]) > SUB_ANCHO_MAX)]
    largos = [x["txt"] for x in subs if x["txt"] and (f.getlength(x["txt"]) > SUB_LEGIBLE_PX
                                                      or len(x["txt"].split()) > SUB_MAX_PALABRAS)]
    for t in malos:
        print(f"   ¡¡ERROR SUBTÍTULO!! no cabe a {SUB_PX}px: «{t}»")
    for t in largos:
        if t not in malos:
            print(f"   AVISO subtítulo largo: «{t}»")
    return not malos


def lienzo_titulo(titulo):
    im = Image.new("RGBA", (W_, H_), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    f = ImageFont.truetype(str(TITULO_FUENTE), TITULO_PX)
    lineas = envolver(titulo.upper(), f, TITULO_ANCHO_MAX)
    for i, l in enumerate(lineas):
        y = TITULO_BASE_ULTIMA - (len(lineas) - 1 - i) * TITULO_INTERLINEA
        d.text((W_ / 2, y), l, font=f, fill=COLOR, anchor="ms")
    return im, lineas


def lienzo_sub(base, txt):
    im = base.copy()
    if not txt:
        return im, SUB_PX
    d = ImageDraw.Draw(im)
    px = SUB_PX
    f = ImageFont.truetype(str(SUB_FUENTE), px)
    while f.getlength(txt) > SUB_ANCHO_MAX and px > SUB_PX_MIN:
        px -= 2
        f = ImageFont.truetype(str(SUB_FUENTE), px)
    d.text((W_ / 2, SUB_BASE), txt, font=f, fill=COLOR, anchor="ms")
    return im, px


def palabras_lineas(lineas):
    """[(indice_palabra, texto_visible)] repartiendo el texto de cada línea entre sus índices."""
    out = []
    for a, b, txt in lineas:
        pals = txt.split()
        n = b - a + 1
        for j, p in enumerate(pals):
            pos = j * n / len(pals)                      # posición (fraccionaria) dentro del tramo de índices
            k = a + min(n - 1, int(pos))
            out.append((k, p, j == len(pals) - 1, pos - int(pos)))
    return out


def trocear_negra(pals):
    """Grupos de 1–3 palabras (como OpusClip). Cada frase (hasta puntuación o fin de línea) se reparte con programación
    dinámica: mejor 2 palabras, nunca acabar en palabra débil («ÉL SE», «AQUÍ EN»), nunca pasar del ancho."""
    f = ImageFont.truetype(str(NEGRA_FUENTE), NEGRA_PX)
    frases, actual = [], []
    for k, p, fin_linea, frac in pals:
        actual.append((k, p, frac))
        if re.search(r"[.,;:?!…]$", p) or fin_linea:
            frases.append(actual)
            actual = []
    if actual:
        frases.append(actual)

    def coste(g, ultimo):
        txt = limpiar_sub(" ".join(x[1] for x in g)).upper()
        c = {1: 1.2, 2: 0.0, 3: 0.5}[len(g)]
        if f.getlength(txt) > NEGRA_ANCHO_MAX:
            c += 100
        if not ultimo and debil(g[-1][1]):
            c += 4
        return c

    grupos = []
    for fr in frases:
        n = len(fr)
        mejor = [0.0] + [1e9] * n
        corte = [0] * (n + 1)
        for e in range(1, n + 1):
            for l in range(1, NEGRA_MAX_PALABRAS + 1):
                if e - l < 0:
                    break
                c = mejor[e - l] + coste(fr[e - l:e], e == n)
                if c < mejor[e]:
                    mejor[e], corte[e] = c, e - l
        partes, e = [], n
        while e > 0:
            partes.append(fr[corte[e]:e])
            e = corte[e]
        grupos += partes[::-1]
    return grupos


def lienzo_negra(txt):
    im = Image.new("RGBA", (W_, H_), (0, 0, 0, 0))
    if txt:
        d = ImageDraw.Draw(im)
        f = ImageFont.truetype(str(NEGRA_FUENTE), NEGRA_PX)
        alto_may = f.getbbox("H")[3] - f.getbbox("H")[1]
        d.text((W_ / 2, NEGRA_CENTRO_Y + alto_may / 2), txt, font=f, fill=BLANCO, anchor="ms")
    return im


def main():
    utf8()
    ap = argparse.ArgumentParser()
    ap.add_argument("spec")
    ap.add_argument("--video", default=str(RAIZ / "historia allan medium.mp4"))
    ap.add_argument("--tiempos", default=str(RAIZ / "trabajo" / "tiempos.json"))
    ap.add_argument("--salida", default=str(RAIZ / "reels"))
    ap.add_argument("--borrador", action="store_true", help="render rápido a 540x960")
    ap.add_argument("--solo-hoja", action="store_true", help="solo guion y PNG de muestra, sin render")
    a = ap.parse_args()

    spec = json.loads(Path(a.spec).read_text(encoding="utf-8"))
    estilo = spec.get("estilo", "franjas_azules")
    if "video" in spec:
        a.video = str(RAIZ / spec["video"])
    if "tiempos" in spec:
        a.tiempos = str(RAIZ / spec["tiempos"])
    W = json.loads(Path(a.tiempos).read_text(encoding="utf-8"))
    ajustes = Path(a.tiempos).parent / "ajustes_tiempos.json"
    if ajustes.exists():
        for k, v in json.loads(ajustes.read_text(encoding="utf-8")).items():
            if k.isdigit():
                W[int(k)].update({c: v[c] for c in ("w", "s", "e", "hueco_antes", "fin_max", "ini_fijo") if c in v})
    global AUDIO
    wav16 = Path(a.tiempos).parent / "audio16k.wav"
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(wav16 if wav16.exists() else a.video), "-vn", "-ac", "1",
                          "-ar", "16000", "-f", "s16le", "-"], capture_output=True).stdout
    AUDIO = (np.frombuffer(raw, np.int16).astype(np.float32), 16000)
    lineas = partir_lineas(spec["lineas"]) if estilo == "franjas_azules" else spec["lineas"]
    segs, dur = trozos(W, lineas)
    for k in sorted({k for sg in segs for k in sg["palabras"]}):
        if W[k]["e"] - W[k]["s"] > 1.2:
            print(f"   AVISO palabra sospechosa: [{k}] «{W[k]['w']}» dura {W[k]['e'] - W[k]['s']:.1f} s (alineación estirada)")
    dur = recortar_silencios(a.video, segs, W)
    revisar_cortes(segs)
    nombre = spec["nombre"]
    tmp = RAIZ / "trabajo" / "reels" / nombre
    tmp.mkdir(parents=True, exist_ok=True)
    salida = Path(a.salida)
    salida.mkdir(parents=True, exist_ok=True)

    # --- subtítulos en la línea de tiempo del reel ---
    subs = []
    for n, (ka, kb, txt) in enumerate(lineas):
        t0 = tiempo_salida(segs, ka, W)
        subs.append({"t0": t0, "txt": limpiar_sub(txt), "a": ka, "b": kb})
    for i, s in enumerate(subs):
        s["t0"] = fq(max(0.0, s["t0"] - 0.03)) if i else 0.0
    for i, s in enumerate(subs):
        s["t1"] = subs[i + 1]["t0"] if i + 1 < len(subs) else dur

    if estilo == "franja_negra":
        subs = []
        pals_todas = palabras_lineas(lineas)
        for g in trocear_negra(pals_todas):
            k0, kf = g[0][0], g[-1][0]
            t0 = tiempo_salida(segs, k0, W) + g[0][2] * (W[k0]["e"] - W[k0]["s"])
            seg_fin = next(sg for sg in segs if kf in sg["palabras"])
            # si la palabra alineada cubre varias escritas («calma» x2), el grupo acaba en su parte proporcional
            sig = [x for x in pals_todas if x[0] == kf and x[3] > g[-1][2]]
            fin_k = W[kf]["s"] + sig[0][3] * (W[kf]["e"] - W[kf]["s"]) if sig else W[kf]["e"]
            t1 = seg_fin["out"] + min(fin_k - seg_fin["ini"] + (0.0 if sig else 0.15), seg_fin["fin"] - seg_fin["ini"])
            subs.append({"t0": fq(max(0.0, t0 - 0.03)), "t1": fq(t1),
                         "txt": limpiar_sub(" ".join(x[1] for x in g)).upper()})
        for i in range(len(subs) - 1):
            subs[i]["t1"] = min(subs[i]["t1"], subs[i + 1]["t0"])
            if subs[i + 1]["t0"] - subs[i]["t1"] < 0.25:      # huecos mínimos: sin parpadeos
                subs[i]["t1"] = subs[i + 1]["t0"]
        subs[-1]["t1"] = min(subs[-1]["t1"], dur)
        # línea de tiempo completa con huecos vacíos (en los silencios no hay subtítulo)
        llenos, t = [], 0.0
        for sb in subs:
            if sb["t0"] > t + 1e-6:
                llenos.append({"t0": t, "t1": sb["t0"], "txt": ""})
            llenos.append(sb)
            t = sb["t1"]
        if t < dur - 1e-6:
            llenos.append({"t0": t, "t1": dur, "txt": ""})
        subs = [x for x in llenos if x["t1"] - x["t0"] > 1e-6]
        base, tl = None, []
    else:
        base, tl = lienzo_titulo(spec["titulo"])
        if not comprobar_subtitulos(subs):
            sys.exit("Hay subtítulos que no caben: corrige el guion antes de renderizar.")
    print(f"== {nombre}  duración {dur:.1f} s  ({len(segs)} trozos, {len(subs)} subtítulos)")
    if tl:
        print("   título: " + " / ".join(tl))
    guion = []
    for s in subs:
        guion.append(f"{s['t0']:6.2f}-{s['t1']:6.2f}  {s['txt']}")
    (tmp / "guion.txt").write_text("\n".join(guion) + "\n", encoding="utf-8")
    print("\n".join("   " + g for g in guion))
    # densidad de cortes: más de 2 cortes en 3 s suena a «corte, corte, corte» (no fluido)
    cortes = [sg["out"] for sg in segs[1:]]
    for i in range(len(cortes) - 2):
        if cortes[i + 2] - cortes[i] < 3.0:
            print(f"   AVISO ráfaga de cortes: {cortes[i]:.1f}s, {cortes[i + 1]:.1f}s, {cortes[i + 2]:.1f}s "
                  "-> deja alguna pausa o une los trozos")
    if not 50 <= dur <= 90:
        print(f"   AVISO: duración {dur:.1f} s fuera de 50–90 s")

    # --- PNG por subtítulo + lista ffconcat ---
    lista = ["ffconcat version 1.0"]
    for i, s in enumerate(subs):
        if estilo == "franja_negra":
            im, px = lienzo_negra(s["txt"]), SUB_PX
        else:
            im, px = lienzo_sub(base, s["txt"])
        if px < SUB_PX:
            print(f"   (subtítulo reducido a {px}px: «{s['txt']}»)")
        f = tmp / f"sub_{i:03d}.png"
        im.save(f)
        lista += [f"file '{f.as_posix()}'", f"duration {s['t1'] - s['t0']:.4f}"]
    lista.append(f"file '{(tmp / f'sub_{len(subs) - 1:03d}.png').as_posix()}'")
    (tmp / "capas.ffconcat").write_text("\n".join(lista) + "\n", encoding="utf-8")
    json.dump({"estilo": estilo, "video": a.video, "componer": spec.get("componer"), "segmentos": segs, "subtitulos": subs, "duracion": dur}, open(tmp / "montaje.json", "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    if a.solo_hoja:
        return

    # --- trozos: imagen y audio SIEMPRE del mismo corte (sincronía por construcción) ---
    # Cada trozo se corta del original con su vídeo y su audio juntos y luego se pegan en el orden del reel.
    # (Error ya cometido: elegir fotogramas con select= los deja en el orden del original y descuadra el gancho.)
    lista_t = ["ffconcat version 1.0"]
    for i, sg in enumerate(segs):
        d = sg["fin"] - sg["ini"]
        n = int(round(d * FPS))                      # fotogramas exactos del trozo
        f = tmp / f"trozo_{i:03d}.mkv"
        # OJO SINCRONÍA: el corte va 1 ms ANTES del fotograma. Redondear el instante hacia arriba (595.4667 > 595.46666…)
        # hacía que ffmpeg descartase el primer fotograma -> imagen 1 fotograma tarde por trozo, acumulándose
        # (medido: hasta 3 fotogramas en desap_03). Además se fija el nº exacto de fotogramas (clonando el último si falta).
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{max(0.0, sg['ini'] - 0.001):.4f}", "-i", a.video,
                        "-t", f"{d:.4f}", "-frames:v", str(n),
                        "-map", "0:v:0", "-map", "0:a:0",
                        "-vf", f"fps={FPS},setpts=PTS-STARTPTS,tpad=stop_mode=clone:stop=3",
                        "-af", f"aresample={SR},afade=t=in:d={FUNDIDO},afade=t=out:st={max(0, d - FUNDIDO):.4f}:d={FUNDIDO}",
                        "-c:v", "libx264", "-preset", "veryfast", "-crf", "12", "-g", "30",
                        "-c:a", "pcm_s16le", "-ac", "2", str(f)], check=True)
        info = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v", "-count_frames", "-show_entries",
                               "stream=nb_read_frames,start_time", "-of", "csv=p=0", str(f)],
                              capture_output=True, text=True).stdout.strip().split(",")
        if len(info) == 2 and (int(info[1]) != n or abs(float(info[0])) > 1e-3):
            print(f"   ¡¡AVISO SINCRONÍA!! trozo {i}: {info[1]} fotogramas (esperados {n}), empieza en {info[0]} s")
        lista_t.append(f"file '{f.as_posix()}'")
    (tmp / "trozos.ffconcat").write_text("\n".join(lista_t) + "\n", encoding="utf-8")

    escala = ",scale=540:960" if a.borrador else ""
    comp = spec.get("componer")
    if comp:
        # vídeo horizontal sin franjas: se compone el vertical = fondo azul de plantilla + vídeo en el hueco central
        # OJO SINCRONÍA: la capa principal del overlay marca el ritmo. Si es el fondo (imagen en bucle), la imagen de
        # Allan se reajusta a sus tiempos y se va desfasando de la voz (medido: hasta 3 fotogramas). Por eso la capa
        # principal es SIEMPRE el vídeo (con pad a 1080x1920) y el fondo va encima con un hueco transparente.
        y0, alto, x = comp.get("y", 588), comp.get("alto", 768), comp.get("x", "(iw-1080)/2")
        fondo_png = Image.open(RAIZ / comp.get("fondo", "plantillas/fondo_franjas_azules.png")).convert("RGBA")
        fondo_png = fondo_png.resize((W_, H_))
        alfa = fondo_png.split()[3].point(lambda v: 255)
        ImageDraw.Draw(alfa).rectangle([0, y0, W_, y0 + alto - 1], fill=0)
        fondo_png.putalpha(alfa)
        fondo = str(tmp / "fondo_hueco.png")
        fondo_png.save(fondo)
        video_v = (f"[0:v]setpts=PTS-STARTPTS,scale=-2:{alto},crop=1080:{alto}:{x}:0,"
                   f"pad=1080:1920:0:{y0}:black,format=yuv420p[vid];"
                   f"[2:v]format=rgba[fon];"
                   f"[vid][fon]overlay=0:0:format=auto:eof_action=repeat,format=yuv420p[v];")
    else:
        video_v = "[0:v]setpts=PTS-STARTPTS,format=yuv420p[v];"
    filtro = (video_v +
              f"[1:v]fps={FPS},format=rgba[c];"
              f"[v][c]overlay=0:0:format=auto:shortest=0:eof_action=repeat{escala},format=yuv420p[o];"
              f"[0:a]loudnorm=I=-14:TP=-1.5:LRA=11,aresample={SR}[a]")
    (tmp / "filtro.txt").write_text(filtro, encoding="utf-8")
    final = salida / (f"{nombre}_borrador.mp4" if a.borrador else f"{nombre}.mp4")
    cmd = ["ffmpeg", "-v", "error", "-stats", "-y",
           "-f", "concat", "-safe", "0", "-i", str(tmp / "trozos.ffconcat"),
           "-f", "concat", "-safe", "0", "-i", str(tmp / "capas.ffconcat"),
           *(["-i", fondo] if comp else []),
           "-filter_complex_script", str(tmp / "filtro.txt"),
           "-map", "[o]", "-map", "[a]", "-t", f"{dur:.4f}",
           "-c:v", "libx264", "-preset", "veryfast" if a.borrador else "medium", "-crf", "26" if a.borrador else "18",
           "-r", str(FPS), "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", str(final)]
    subprocess.run(cmd, check=True)
    print(f"   -> {final}")


if __name__ == "__main__":
    main()
