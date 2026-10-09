/* c01 · trial «Tu adicción no es el problema» — UNA idea: la adicción compensa emociones que no ves (acento: sacro).
   Un bloque por cada tramo de tablero (08/10: con los cortes nuevos hay 8; si sobran tramos sin bloque, el tablero sale vacío). */
const [T1, T2, T3, T4, T5, T6, T7, T8] = TABLEROS;
const balanza = (tC, izq, der) => { const viga = path('', NEGRO, 8), base = path('M540,880 L500,950 L580,950 Z', NEGRO, 8), L = emoji(izq, tC, 90), Rr = emoji(der, tC + .3, 90);
  return t => { const k = out(P(t, tC, .8)), r = (-14 + 14 * k) * Math.PI / 180;
    viga.setAttribute('d', `M${540 - 280 * Math.cos(r)},${880 - 280 * Math.sin(r)} L${540 + 280 * Math.cos(r)},${880 + 280 * Math.sin(r)}`);
    dib(viga, out(P(t, tC - .3, .4)), KT); dib(base, out(P(t, tC - .3, .4)), KT);
    pe(L, t, 540 - 280 * Math.cos(r), 880 - 280 * Math.sin(r) - 70); pe(Rr, t, 540 + 280 * Math.cos(r), 880 + 280 * Math.sin(r) - 70); }; };

/* gancho: la adicción no es mala, compensa una cosa con otra (balanza que se equilibra) */
bloque(...T1, (a) => {
  const ad = texto('la adicción', a + .05, { tam: 84 }), nm = texto('no es mala|ac', en('no es mala', a), { tam: 104 }), b = balanza(en('compensar', a), '🕳️', '🍩');
  return t => { pt(ad, t, 540, 450); pt(nm, t, 540, 570); b(t); };
});
/* lo que no eres consciente · mucho vacío (silueta con un hueco en el plexo) */
bloque(...T2, (a) => {
  const sl = silueta(), hueco = path('', C.raiz, 6, 'rgba(200,55,45,.15)'), tV = en('vacío', a);
  const c = texto('no eres', en('no eres consciente', a), { tam: 52, m: true }), c2 = texto('consciente', en('consciente', a), { tam: 72 });
  const v = texto('vacío|raiz', tV, { tam: 110 });
  return t => { const p = pintarSilueta(sl, t, a - .3, 280, 900, .6)('plexo'); hueco.setAttribute('d', circulo(p.x, p.y + 10, 30 + 20 * out(P(t, tV, .6)))); dib(hueco, out(P(t, tV - .1, .4)), KT);
    pt(c, t, 740, 480); pt(c2, t, 740, 570); pt(v, t, 740, 740); };
});
/* más adicción para equilibrar eso: la balanza otra vez */
bloque(...T3, (a) => {
  const m = texto('más adicción|raiz', a + .05, { tam: 84 }), e = texto('para equilibrar', en('equilibrar', a), { tam: 56, m: true });
  const b = balanza(en('equilibrar', a), '🕳️', '🚬');
  return t => { pt(m, t, 540, 450); pt(e, t, 540, 560); b(t); };
});
/* con ansiedad, lo compensan: fumando, contenido para adultos */
bloque(...T4, (a) => {
  const an = texto('ansiedad|raiz', a + .05, { tam: 96 }), c = texto('lo compensan', en('compensan', a), { tam: 60, m: true });
  const E = [['🚬', 'fumando'], ['📱', 'contenido']].map(([ch, p]) => emoji(ch, en(p, a), 120));
  return t => { pt(an, t, 540, 460); pt(c, t, 540, 580); E.forEach((e, i) => pe(e, t, 380 + i * 320, 780)); };
});
/* su experiencia: comía por ansiedad */
bloque(...T5, (a) => {
  const y = texto('yo', a + .05, { tam: 60, m: true }), c = texto('comía', en('comía', a), { tam: 96 }), an = texto('por ansiedad|raiz', en('ansiedad', a), { tam: 80 });
  const e = emoji('🍔', en('comía', a) + .2, 120);
  return t => { pt(y, t, 540, 440); pt(c, t, 540, 540); pt(an, t, 540, 650); pe(e, t, 540, 820); };
});
/* lo que necesitas es placer para sentirte en equilibrio */
bloque(...T6, (a) => {
  const n = texto('lo que necesitas', en('necesitas', a), { tam: 56, m: true }), p = texto('placer|ac', en('placer', a), { tam: 130 });
  const e = texto('para sentirte en equilibrio', en('sentirte', a), { tam: 52, m: true });
  return t => { pt(n, t, 540, 470); pt(p, t, 540, 610); pt(e, t, 540, 760); };
});
/* estás sobreviviendo · siempre vas a comer cosas que te den placer */
bloque(...T7, (a) => {
  const s = texto('sobreviviendo|raiz', en('sobreviviendo', a), { tam: 96 }), c = texto('siempre vas a comer…', en('siempre', a), { tam: 56, m: true });
  const E = ['🍟', '🍕', '🍩'].map((ch, i) => emoji(ch, en('comer', a) + i * .2, 110));
  return t => { pt(s, t, 540, 460); pt(c, t, 540, 580); E.forEach((e, i) => pe(e, t, 270 + i * 270, 760)); };
});
/* comida basura: sabes que no te hace bien… pero lo vas a hacer */
bloque(...T8, (a) => {
  const cb = texto('comida basura', en('comida basura', a), { tam: 84 }), nb = texto('sabes que no te hace bien', en('sabes', a), { tam: 52, m: true });
  const lh = texto('pero lo vas a hacer|raiz', en('pero lo vas', a), { tam: 72 }), x = path('', C.raiz, 12), tX = en('pero lo vas', a);
  suena(tX, 'golpe-corto', .3);
  return t => { pt(cb, t, 540, 460); pt(nb, t, 540, 580); pt(lh, t, 540, 740); };
});
