/* c04 · «Todo lo que callas sale algún día» (acento: corazón) */
const [T1, T2, T3, T4, T5, T6] = TABLEROS;
const COLS = [C.raiz, C.sacro, C.plexo, C.ojo, C.garganta];

/* vas sacando un montón de emoción que has ido reprimiendo toda tu vida */
bloque(...T1, (a) => {
  const sl = silueta(), bol = COLS.map(c => path('', c, 7, 'rgba(255,255,255,.01)')), tE = en('emoción', a);
  const r = texto('reprimiendo|raiz', en('reprimiendo', a), { tam: 84 }), v = texto('toda tu vida', en('toda tu vida', a), { tam: 60, m: true });
  return t => { const c = pintarSilueta(sl, t, a - .3, 280, 900, .6)('plexo');
    bol.forEach((b, i) => { const k = P(t, tE + i * .25, 2.2), y = c.y - 170 * out(k) - i * 10; b.setAttribute('d', circulo(c.x + (i - 2) * 26 + 30 * Math.sin(k * 6 + i), y, 16)); dib(b, k > 0 ? 1 : 0, 1 - .6 * k); });
    pt(r, t, 740, 560); pt(v, t, 740, 690); };
});
/* un día con un vacío increíble y muchísimo miedo a la soledad */
bloque(...T2, (a) => {
  const st = stickman(), ais = path('', '#bbb', 6), v = texto('vacío|raiz', en('vacío', a), { tam: 104 }), m = texto('miedo a la soledad', en('miedo', a), { tam: 56, m: true });
  return t => { pintarStick(st, t, a - .2, 300, 880, .5); ais.setAttribute('d', circulo(300, 740, 180)); ais.style.strokeDasharray = '0.02 0.02'; ais.style.opacity = out(P(t, a, .5)) * .9;
    pt(v, t, 760, 560); pt(m, t, 760, 700); };
});
/* y empecé a llorar… 15-20 minutos sin parar */
bloque(...T3, (a) => {
  const e = emoji('😢', en('llorar', a), 150), n = texto('15-20 minutos|ac', en('15-20', a), { tam: 96 }), s = texto('llorando sin parar', en('sin parar', a), { tam: 56, m: true });
  return t => { pe(e, t, 540, 520, 1 + .05 * Math.sin(t * 5)); pt(n, t, 540, 700); pt(s, t, 540, 820); };
});
/* Australia, a 15.000 km… y aquí, a 20 minutos de mi pueblo */
bloque(...T4, (a) => {
  const k1 = texto('15.000 km', a + .05, { tam: 76, sonido: false }), a1 = texto('Australia', a + .05, { tam: 52, m: true, sonido: false }), g1 = emoji('🌏', a + .05, 96);
  const k2 = texto('20 minutos|ac', en('20 minutos', a), { tam: 76 }), a2 = texto('mi pueblo', en('pueblo', a), { tam: 52, m: true }), g2 = emoji('🏠', en('20 minutos', a), 96), vs = texto('vs', a + .3, { tam: 56, m: true, sonido: false });
  return t => { pe(g1, t, 280, 520); pt(k1, t, 280, 660); pt(a1, t, 280, 750); pt(vs, t, 540, 620); pe(g2, t, 800, 520); pt(k2, t, 800, 660); pt(a2, t, 800, 750); };
});
/* esa soledad tan grande · cuando sacas esa emoción */
bloque(...T5, (a) => {
  const so = texto('soledad|raiz', en('soledad', a), { tam: 110 }), sl = silueta(), f = path('', AC, 8), s = texto('sacas esa emoción', en('sacas', a), { tam: 56, m: true });
  return t => { pt(so, t, 540, 470, 1 - P(t, s._t0, .2)); const c = pintarSilueta(sl, t, s._t0 - .3, 300, 900, .6)('corazon');
    f.setAttribute('d', flecha(c.x + 40, c.y, 640, 560)); dib(f, out(P(t, s._t0, .5))); pt(s, t, 760, 640); };
});
/* deja que se exprese, sin barreras · todo te enseña */
bloque(...T6, (a) => {
  const muro = [0, 1, 2].map(() => path('', NEGRO, 7)), tB = en('barreras', a), e = texto('dejar que se exprese', en('dejar', a), { tam: 64 }), en2 = texto('todo te enseña|ac', en('te enseña', a), { tam: 88 });
  suena(tB, 'descarte', .3);
  return t => { pt(e, t, 540, 460); const k = out(P(t, tB, .5));
    muro.forEach((m, i) => { m.setAttribute('d', cajaR(330 + i * 140, 560 + (i % 2) * 20 + 160 * k * (i - 1) * (i - 1), 130, 80, 8)); m.setAttribute('transform', `rotate(${(i - 1) * 25 * k} ${395 + i * 140} 600)`); dib(m, out(P(t, a - .2 + i * .1, .3)), 1 - .8 * k); });
    pt(en2, t, 540, 820); };
});
