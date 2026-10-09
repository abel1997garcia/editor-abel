import json,sys
sys.stdout.reconfigure(encoding='utf-8')
W=json.load(open(sys.argv[1],encoding='utf-8')); sys.argv=sys.argv[1:]
for n in sys.argv[1:]:
    M=json.load(open(f'trabajo/reels/{n}/montaje.json',encoding='utf-8'))
    S=M['segmentos']; print(f"\n== {n} {M['duracion']:.1f}s, {len(S)} trozos")
    for a,b in zip(S,S[1:]):
        x,y=a['palabras'][-1],b['palabras'][0]
        if y==x+1: q=f"pausa {W[y]['s']-W[x]['e']:.2f}s"
        elif x<y<x+12: q='QUITA: '+' '.join(W[k]['w'] for k in range(x+1,y))
        else: q='SALTO'
        print(f"  {b['out']:5.1f}s  …{W[x]['w']} | {W[y]['w']}…   {q}")
