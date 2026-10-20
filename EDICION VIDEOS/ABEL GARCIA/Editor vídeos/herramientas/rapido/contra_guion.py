"""CONTROL OBLIGATORIO antes de dar un reel por bueno (Abel 19/10/2026: «siempre que edites, toma de referencia el guion del Drive»).
Compara FRASE A FRASE el texto montado (edl.json) con el guion del Drive (<carpeta>/guion.txt, el doc tal cual):
  ✗ A MEDIAS / FUERA DEL GUION: frase del reel que no se parece a ninguna del guion (p. ej. «O tapas las fugas, pero no cargas.»
    cuando el guion dice «O tapas las fugas, pero no haces nada que te cargue, y vives sin dolor…»): se escucha y se decide.
  ✗ FALTA: idea del guion que no aparece en el reel (¿se grabó? ¿se cortó de más?).
Cada ✗ se revisa A MANO contra el guion: que cada frase esté COMPLETA y tenga sentido, no solo que no falten palabras.
    python herramientas/rapido/contra_guion.py <carpeta> [reel ...]
"""
import difflib, json, re, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from elegir import guion_de, pal


def frases(t):
    return [f.strip() for f in re.split(r'(?<=[.?!…])\s+', t) if len(pal(f)) >= 2]


def contiene(a, b):
    """cuánto de la frase a está dentro de b (0-1): bloques comunes / largo de a"""
    A, B = pal(a), pal(b)
    if not A or not B: return 0
    return sum(m.size for m in difflib.SequenceMatcher(None, A, B, autojunk=False).get_matching_blocks()) / len(A)


if __name__ == '__main__':
    d = Path(sys.argv[1]); plan = json.loads((d / 'plan.json').read_text(encoding='utf-8'))
    hooks, cuerpo = guion_de((d / 'guion.txt').read_text(encoding='utf-8'))
    G = [f for t in cuerpo for f in frases(t)]; todo_g = ' '.join(G + hooks)
    # FINAL CORTADO (Abel 20/10/2026, historia11: el reel acababa y su voz seguía; «Diego» era «llega»): lo grabado DESPUÉS de la última
    # toma usada se escucha siempre; si es el cierre de verdad (aunque Whisper lo transcriba raro), entra.
    L = json.loads((d / 'islas.json').read_text(encoding='utf-8')); L = L['islas'] if isinstance(L, dict) else L
    usadas = [x if isinstance(x, int) else (x['isla'] if isinstance(x, dict) else x[0]) for c in [plan['cuerpo']] + [r.get('cuerpo', []) for r in plan['reels'].values()] for x in c]
    for i in range(max(usadas) + 1, len(L)):
        if (L[i].get('texto') or '').strip(): print(f'  ⚠ DESPUÉS DEL FINAL hay voz (ESCUCHAR: ¿es el cierre?): isla {i} «{L[i]["texto"]}»')
    for r in (sys.argv[2:] or plan['reels']):
        texto = ' '.join(w[0] for w in json.loads((d / 'out_rapido' / r / 'edl.json').read_text(encoding='utf-8'))['pal'])
        R = frases(texto); malas = 0
        print(f'##### {d.name} {r}')
        for k, f in enumerate(R[1:], 1):                                 # la 1.ª es el gancho
            sc, g = max((contiene(f, g), g) for g in G) if G else (0, '')
            entera = contiene(g, ' '.join(R[k - 1:k + 2]))                  # ¿está la frase del guion ENTERA (en esta y la siguiente)?
            if sc >= .6 and entera < .6 and len(pal(g)) > len(pal(f)) + 3:
                malas += 1; print(f'  ✗ A MEDIAS: «{f}»\n      el guion dice: «{g}»')
            elif sc < .3:
                print(f'  · con otras palabras (comprobar que está completa y tiene sentido): «{f}»')
        for g in G:
            if contiene(g, texto) < .45: malas += 1; print(f'  ✗ FALTA ({contiene(g, texto):.0%}): «{g}»')
        print('  ✓ ninguna frase a medias ni falta nada del guion' if not malas else f'  → {malas} a revisar A MANO')
