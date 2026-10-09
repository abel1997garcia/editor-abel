/* c02 · «A nadie le importas tanto como crees» (acento: garganta) */
const [T1, T2, T3, T4, T5] = TABLEROS;

/* con 20 años tenías miedo a que te criticasen… no les importabas */
bloque(...T1, (a) => {
  const v = texto('20 años|ac', en('20', a), { tam: 120 }), m = texto('miedo a que te criticasen', en('miedo', a), { tam: 56, m: true }), e = emoji('😨', en('miedo', a), 96);
  const p = pastilla('NO LES IMPORTABAS', en('importabas', a));
  return t => { pt(v, t, 540, 500); pe(e, t, 540, 640, 1); pt(m, t, 540, 740); pt(p, t, 540, 850); };
});
/* nunca se fijaron, nunca les importaste: no tiene validez, es siempre tu cabeza */
bloque(...T2, (a) => {
  const ojos = emoji('👀', a + .05, 110), x = path('', C.raiz, 12), tF = en('fijaron', a), f = texto('nunca se fijaron', en('nunca', a), { tam: 72 });
  const nv = texto('no tiene validez', en('validez', a), { tam: 60, m: true }), c = emoji('🧠', en('siempre', a), 110);
  suena(tF + .1, 'descarte', .3);
  return t => { pe(ojos, t, 300, 560); x.setAttribute('d', cruz(300, 560, 2.8)); dib(x, out(P(t, tF + .1, .3))); pt(f, t, 700, 520); pt(nv, t, 700, 640); pe(c, t, 700, 800); };
});
/* pensamos que sentir nos hace débiles */
bloque(...T3, (a) => {
  const sl = silueta(), cor = path('', AC, 12), tS = en('sentir', a), s = texto('sentir|ac', tS, { tam: 104 }), d = texto('= débil', en('débiles', a), { tam: 88 });
  const em = texto('escuchar tus emociones', en('escuchar', a), { tam: 52, m: true });
  return t => { const c = pintarSilueta(sl, t, a - .3, 280, 900, .6)('corazon'); cor.setAttribute('d', circulo(c.x, c.y, 10 + 3 * Math.sin(t * 6))); dib(cor, out(P(t, tS - .2, .3)));
    pt(em, t, 720, 470); pt(s, t, 720, 600); pt(d, t, 720, 740); };
});
/* todo eso es una puta mierda: está normalizado, actúan en automático */
bloque(...T4, (a) => {
  const m = texto('una puta mierda|raiz', en('una puta', a), { tam: 92 }), n = texto('normalizado', en('normalizado', a), { tam: 64, m: true });
  const gente = [0, 1, 2, 3, 4].map(() => stickman('#9a9a9a'));
  return t => { pt(m, t, 540, 500); pt(n, t, 540, 640); gente.forEach((g, i) => pintarStick(g, t, n._t0 - .2 + i * .1, 220 + i * 160, 900, .38)); };
});
/* nadie piensa en criticarte: cada uno está con su propia película */
bloque(...T5, (a) => {
  const tP = en('película', a), n = texto('nadie piensa en criticarte', a + .05, { tam: 56, m: true }), p = texto('su propia película|ac', en('su propia', a), { tam: 72 });
  const gente = [0, 1, 2].map(() => stickman()), pel = [0, 1, 2].map(i => emoji('🎬', tP + i * .12, 70));
  return t => { pt(n, t, 540, 450); pt(p, t, 540, 545); gente.forEach((g, i) => { const s = pintarStick(g, t, a - .2 + i * .1, 270 + i * 270, 900, .45); pe(pel[i], t, s.cabeza.x, s.cabeza.y - 85); }); };
});
