"""PASO 1b del proceso rápido: ELIGE LAS TOMAS solo, a partir de las islas (islas.py) y del guion del Drive (guion.txt).
Regla de Abel: de cada frase repetida, la ÚLTIMA toma COMPLETA. Una isla se descarta si:
  · está vacía o es un fragmento de ≤ 2 palabras que no es una frase («Acabando.», «¿Crees?», «Que...»);
  · se queda a medias («...») o una isla de poco después EMPIEZA IGUAL (es una toma anterior de la misma frase).
Los GANCHOS son las islas que se parecen a los hooks del guion (o que van antes del cuerpo): un reel por gancho distinto.
Las frases que no están en el guion se marcan «?» para que el editor decida (Abel las improvisa a veces).

    python herramientas/rapido/elegir.py <carpeta>      → <carpeta>/plan.json (sin títulos ni música: los pone el editor)
"""
import difflib, json, re, sys
from pathlib import Path
nz = lambda w: re.sub(r'[^a-z0-9ñ]', '', str(w).lower().translate(str.maketrans('áéíóúü', 'aeiouu')))
pal = lambda t: [nz(w) for w in str(t).split() if nz(w)]


def parecido(a, b):
    A, B = pal(a), pal(b)
    return difflib.SequenceMatcher(None, A, B, autojunk=False).ratio() if A and B else 0


def guion_de(txt):
    """guion.txt = el doc del Drive tal cual (Hooks numerados + Guion)"""
    hooks, cuerpo, zona = [], [], None
    for l in txt.splitlines():
        titulo = l.strip().startswith('# ') and not l.strip().startswith('## ')
        l = l.strip().strip('#').strip('*').strip()
        if not l: continue
        if titulo: hooks.append(l); continue                              # el TÍTULO del guion también es un gancho (Abel lo graba como tal)
        if l.lower().startswith('hooks'): zona = 'h'; continue
        if l.lower().startswith('guion'): zona = 'g'; continue
        if zona == 'h': hooks.append(re.sub(r'^\d+[\\.)]*\s*', '', l))
        elif zona == 'g': cuerpo += [s for s in re.split(r'(?<=[.?!…])\s+', l) if len(pal(s)) >= 2]
    return hooks, cuerpo


def hasta_unico(ws, q):
    """palabras que acaban en ws[q] y NO se repiten en la isla (montar busca «hasta» desde el final: «conjunto» sale dos veces)"""
    W = [nz(w) for w in ws]
    for n in range(1, q + 2):
        f = W[q - n + 1:q + 1]
        if sum(W[k:k + n] == f for k in range(len(W))) == 1: return ' '.join(w.strip('.,?!') for w in ws[q - n + 1:q + 1])
    return ws[q].strip('.,?!')


def empieza_igual(a, b, n=3):
    A, B = pal(a), pal(b); n = min(n, len(A), len(B))
    return n >= 2 and A[:n] == B[:n]


if __name__ == '__main__':
    d = Path(sys.argv[1]); islas = json.loads((d / 'islas.json').read_text(encoding='utf-8'))
    hooks, cuerpo = guion_de((d / 'guion.txt').read_text(encoding='utf-8'))
    vivas = []
    gancho_ = lambda txt: max([parecido(txt, h) for h in hooks] or [0]) > max([parecido(txt, c) for c in cuerpo] or [0])
    frase_de = lambda txt: max(range(len(cuerpo)), key=lambda i: parecido(txt, cuerpo[i])) if cuerpo else None
    for k, s in enumerate(islas):
        t = s['texto'].strip(); n = len(pal(t))
        if n == 0 or re.search(r'(?i)subtitles|amara|subtitulado por|gracias por ver', t): continue   # lo que se inventa el reconocedor en el silencio
        if n <= 2 and not re.search(r'[.?!]$', t): continue                      # fragmento a medias
        if n <= 2 and max([parecido(t, x) for x in hooks + cuerpo] or [0]) < .5: continue   # «Acabando.», «¿Crees?»
        hk = lambda txt: max(range(len(hooks)), key=lambda i: parecido(txt, hooks[i])) if hooks and gancho_(txt) else None
        posteriores = [islas[j] for j in range(k + 1, min(len(islas), k + 7)) if islas[j]['a'] - s['b'] < 25
                       and not (hk(t) is not None and hk(islas[j]['texto']) is not None and hk(t) != hk(islas[j]['texto']))]   # otro GANCHO no es otra toma de este
        if (t.endswith('...') or t.endswith('…')) and n <= 4: continue
        if n <= 3 and not gancho_(t) and any(set(pal(t)) <= set(pal(x['texto'])) and len(pal(x['texto'])) > 3 * n for x in posteriores[:3]): continue   # «Claro, claro.» antes de la frase entera
        if n <= 6 and not gancho_(t) and any(frase_de(x['texto']) == frase_de(t) and len(pal(x['texto'])) > 2 * n and not re.search(r'(\.\.\.|…)$', x['texto'].strip())
                                            and parecido(x['texto'], cuerpo[frase_de(t)]) > parecido(t, cuerpo[frase_de(t)]) for x in posteriores): continue   # arranque suelto («Sí, sí, eso dímelo a mí», «Claro, claro») de una frase que luego sale entera            # fragmento a medias («Por supuesto, va...», «Ya se te...»)
        mejor = lambda x: not re.search(r'(\.\.\.|…)$', x['texto'].strip()) or re.search(r'(\.\.\.|…)$', t) or len(pal(x['texto'])) >= n   # la posterior vale si está COMPLETA (o esta tampoco lo está)
        if any(empieza_igual(t, x['texto']) and (not (gancho_(t) and gancho_(x['texto'])) or parecido(t, x['texto']) >= .45 or t.endswith('...') or n <= 4) and mejor(x) for x in posteriores): continue   # toma posterior de la MISMA frase (dos GANCHOS distintos pueden empezar igual)
        anteriores = [islas[j] for j in range(max(0, k - 6), k) if s['a'] - islas[j]['b'] < 25 and not re.search(r'(\.\.\.|…)$', islas[j]['texto'].strip())]
        if re.search(r'(\.\.\.|…)$', t) and any(parecido(t, x['texto']) >= .45 and len(pal(x['texto'])) >= n for x in anteriores): continue   # toma INCOMPLETA de una frase que ya estaba entera antes
        if any(parecido(t, x['texto']) >= .6 and mejor(x) for x in posteriores): continue       # retoma cambiando una palabra («tampoco basta» → «no basta»)
        A = pal(t); juntas = pal(' '.join(x['texto'] for x in posteriores[:2]))     # la repite partida en las DOS islas siguientes
        if n >= 4 and sum(b.size for b in difflib.SequenceMatcher(None, A, juntas, autojunk=False).get_matching_blocks()) >= .7 * n            and parecido(t, ' '.join(x['texto'] for x in posteriores[:2])) >= .45: continue
        if n <= 6 and any(sum(b.size for b in difflib.SequenceMatcher(None, A, pal(x['texto']), autojunk=False).get_matching_blocks()) >= .8 * n for x in posteriores[:2]): continue   # «Contenido que explique.» repetida dentro de la siguiente
        if t.endswith('...') or t.endswith('…'):                               # toma a medias: casi todas sus palabras salen en una toma posterior
            A = pal(t)
            if any(sum(b.size for b in difflib.SequenceMatcher(None, A, pal(x['texto']), autojunk=False).get_matching_blocks()) >= .5 * len(A) for x in posteriores): continue
        vivas.append(s)
    for k, s in enumerate(islas):                                           # remate corto PEGADO a una frase buena («…no te haya escrito nadie. Entonces hablamos.»)
        t = s['texto'].strip()
        if s not in vivas and k and islas[k - 1] in vivas and s['a'] - islas[k - 1]['b'] < .3 and 2 <= len(pal(t)) <= 4 and re.search(r'[.!?]$', t)                 and not any(re.search(r'(\.\.\.|…)$', x['texto'].strip()) is None and parecido(t, x['texto']) > .5 for x in islas[k + 1:k + 4]):
            vivas.insert(vivas.index(islas[k - 1]) + 1, s)
    # ganchos: las islas que más se parecen a un hook (o van antes de la 1.ª frase del cuerpo)
    def es_hook(s): return max([parecido(s['texto'], h) for h in hooks] or [0]) >= max([parecido(s['texto'], c) for c in cuerpo] or [0])
    inicio = next((k for k, s in enumerate(vivas) if not es_hook(s)), len(vivas))
    ganchos, resto = vivas[:inicio], vivas[inicio:]
    plan = json.loads((d / 'plan.json').read_text(encoding='utf-8')) if (d / 'plan.json').exists() else {}
    piezas = []
    for k, s in enumerate(resto):                                           # frase improvisada que repite la idea de la isla siguiente → se recorta
        frases = [f for f in re.split(r'(?<=[.?!])\s+', s['texto']) if pal(f)]
        sig = pal(resto[k + 1]['texto'])[:5] if k + 1 < len(resto) else []
        corte = None
        for q, f in enumerate(frases[1:], 1):
            F = pal(f); big = {tuple(F[i:i + 2]) for i in range(len(F) - 1)}
            if max([parecido(f, c) for c in cuerpo] or [0]) < .3 and big & {tuple(sig[i:i + 2]) for i in range(len(sig) - 1)}:
                ws = s['texto'].split(); corte = hasta_unico(ws, len(' '.join(frases[:q]).split()) - 1); break
        desde = None                                                            # trabazón DENTRO de la isla: se queda desde el último arranque
        trozos_ = re.split(r'\.\.\.|…', s['texto'])                              # («Porque te voy a asegur... porque te aseguro una cosa»)
        if len(trozos_) > 1:
            ini = pal(trozos_[0])[:1]
            for tz in trozos_[1:]:
                tw = [w for w in tz.split() if nz(w)]
                if tw and ini and nz(tw[0]) == ini[0] and len(tw) >= 3: desde = ' '.join(tw[:3])
        if desde: print(f"  ✂ isla {s['id']}: desde «{desde}» (trabazón al principio)")
        if not corte and re.search(r'(\.\.\.|…)$', s['texto'].strip()) and k + 1 < len(resto):   # acaba empezando OTRA VEZ la frase que sigue
            sigp = pal(resto[k + 1]['texto'])[:2]; ws = s['texto'].split()
            for q in range(len(ws) - 2, 0, -1):
                if [nz(w) for w in ws[q:q + 2]] == sigp and q > 2:
                    corte = hasta_unico(ws, q - 1); print(f"  ✂ isla {s['id']}: hasta «{corte}» (al final vuelve a empezar la frase siguiente)"); break
        piezas.append([s['id'], desde, corte] if (corte or desde) else s['id'])
        if corte: print(f"  ✂ isla {s['id']}: se queda hasta «{corte}» (lo de después lo repite la isla siguiente)")
    plan.update({'velocidad': plan.get('velocidad', 1.07), 'guion': ' '.join(cuerpo), 'cuerpo': piezas})
    viejos = plan.get('reels', {})
    plan['reels'] = {f'r{i + 1}': {**viejos.get(f'r{i + 1}', {'titulo': '', 'musica': ''}), 'gancho': [g['id']]} for i, g in enumerate(ganchos)}
    (d / 'plan.json').write_text(json.dumps(plan, ensure_ascii=False, indent=1), encoding='utf-8')
    print('GANCHOS:'); [print(f"  r{i + 1}: isla {g['id']:3d}  {g['texto']}") for i, g in enumerate(ganchos)]
    print('CUERPO:')
    for s in resto:
        m = max([parecido(s['texto'], c) for c in cuerpo] or [0])
        print(f"  {'?' if m < .3 else ' '} isla {s['id']:3d}  {s['texto']}")
    print('DESCARTADAS:', [s['id'] for s in islas if s not in vivas])
