/* c01 · «Las adicciones no existen» (acento: sacro). Un bloque por tramo de tablero; gráficos en y 420–900 */
const [T1, T2, T3, T4, T5] = TABLEROS;

/* las adicciones como tal no existen: es compensar */
bloque(...T1, (a) => {
  const ad = texto('adicción', a + .05, { tam: 120 }), x = path('', C.raiz, 14), tE = en('existen', a), c = texto('= compensar|ac', en('compensar', a), { tam: 84 });
  suena(tE, 'descarte', .35);
  return t => { pt(ad, t, 540, 540); x.setAttribute('d', cruz(540, 540, 5.5)); dib(x, out(P(t, tE, .35))); pt(c, t, 540, 740); };
});
/* compensar una cosa con otra · si tienes mucho vacío y emociones densas */
bloque(...T2, (a) => {
  const sl = silueta(), hueco = path('', C.raiz, 6, 'rgba(200,55,45,.15)'), tV = en('vacío', a);
  const v = texto('vacío|raiz', tV, { tam: 96 }), d = texto('emociones densas', en('densas', a), { tam: 60, m: true }), o = texto('una cosa con otra', a + .1, { tam: 56, m: true });
  return t => { const c = pintarSilueta(sl, t, a - .3, 290, 900, .6)('plexo'); hueco.setAttribute('d', circulo(c.x, c.y + 10, 30 + 20 * out(P(t, tV, .6)))); dib(hueco, out(P(t, tV - .1, .4)));
    pt(o, t, 740, 470, 1 - P(t, tV, .2)); pt(v, t, 740, 600); pt(d, t, 740, 720); };
});
/* para simplemente sobrevivir · cuando tienen ansiedad */
bloque(...T3, (a) => {
  const s = texto('sobrevivir', a + .05, { tam: 96 }), st = stickman(), z = [0, 1, 2].map(() => path('', C.raiz, 6)), tA = en('ansiedad', a), an = texto('ansiedad|raiz', tA, { tam: 72 });
  return t => { pt(s, t, 540, 470); const p = pintarStick(st, t, a - .2, 400, 880, .55);
    z.forEach((q, i) => { const ang = -2.4 + i * .9, r0 = 70, r1 = 120; q.setAttribute('d', `M${p.cabeza.x + r0 * Math.cos(ang)},${p.cabeza.y + r0 * Math.sin(ang)} l${(r1 - r0) / 3 * Math.cos(ang) + 12},${(r1 - r0) / 3 * Math.sin(ang)} l${(r1 - r0) / 3 * Math.cos(ang) - 24},${(r1 - r0) / 3 * Math.sin(ang)} l${(r1 - r0) / 3 * Math.cos(ang) + 12},${(r1 - r0) / 3 * Math.sin(ang)}`); dib(q, out(P(t, tA + i * .08, .25))); });
    pt(an, t, 760, 680); };
});
/* comiendo · lo que necesitas es placer para sentirte en equilibrio */
bloque(...T4, (a) => {
  const e = emoji('🍔', en('comiendo', a - .5), 120), pl = texto('placer|ac', en('placer', a), { tam: 104 }), tq = en('equilibrio', a), eq = texto('equilibrio', tq, { tam: 64, m: true });
  const viga = path('', NEGRO, 8), base = path('', NEGRO, 8);
  return t => { pe(e, t, 290, 560); pt(pl, t, 720, 560); const k = 1 - out(P(t, tq, .6)), r = -10 * k;
    viga.setAttribute('d', `M${540 - 260 * Math.cos(r * Math.PI / 180)},${790 - 260 * Math.sin(r * Math.PI / 180)} L${540 + 260 * Math.cos(r * Math.PI / 180)},${790 + 260 * Math.sin(r * Math.PI / 180)}`); base.setAttribute('d', 'M540,790 L500,860 L580,860 Z');
    dib(viga, out(P(t, tq - .3, .4))); dib(base, out(P(t, tq - .3, .4))); pt(eq, t, 540, 720); };
});
/* comida basura: sabes que no te hace bien… pero lo vas a hacer */
bloque(...T5, (a) => {
  const E = ['🍟', '🍕', '🍩'].map((ch, i) => emoji(ch, a + .1 + i * .25, 104)), cb = texto('comida basura|raiz', en('comida basura', a), { tam: 88 });
  const nb = texto('no te hace bien', en('no te hace bien', a), { tam: 60, m: true }), p = pastilla('PERO LO VAS A HACER', en('pero lo vas', a), { ac: true });
  return t => { E.forEach((e, i) => pe(e, t, 270 + i * 270, 660)); pt(cb, t, 540, 480); pt(nb, t, 540, 800, 1 - P(t, p._t0, .2)); pt(p, t, 540, 800); };
});
