import json,re,sys
n=lambda x: re.sub(r'[^a-z0-9ñ]','',x.lower().translate(str.maketrans('áéíóúü','aeiouu')))
class A:
    def __init__(s,ruta): s.F=json.load(open(ruta,encoding='utf-8')); s.P=[n(w['w']) for w in s.F]
    def find(s,fr,desde=0):
        t=[n(x) for x in fr.split()]
        for i in range(desde,len(s.P)-len(t)+1):
            if s.P[i:i+len(t)]==t: return i
        sys.exit('no encuentro: '+fr)
    def T(s,a,b=None,desde=0):
        i=s.find(a,desde)
        if b is None: return [i,i+len(a.split())-1]
        j=s.find(b,i); return [i,j+len(b.split())-1]
