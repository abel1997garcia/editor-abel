/* c04 · «Todo lo que callas sale algún día» (acento: corazón) · gancho: su momento (llorar 15-20 min, la soledad) */
const [T1, T2, T3, T4, T5] = TABLEROS;

/* estuve 15-20 minutos llorando sin parar, pensando que me había vuelto loco */
bloque(...T1, (a) => {
  const e = emoji('😢', a + .05, 150), n = texto('15-20 minutos|ac', en('15-20', a), { tam: 96 }), s = texto('llorando sin parar', en('llorando', a), { tam: 56, m: true });
  const l = texto('me había vuelto loco', en('vuelto loco', a), { tam: 56, m: true });
  return t => { pe(e, t, 540, 500, 1 + .05 * Math.sin(t * 5)); pt(n, t, 540, 680); pt(s, t, 540, 790, 1 - P(t, l._t0, .2)); pt(l, t, 540, 790); };
});
/* Australia a 15.000 km… y aquí, a 20 minutos de mi pueblo */
bloque(...T2, (a) => {
  const k1 = texto('15.000 km', a + .05, { tam: 76, sonido: false }), a1 = texto('Australia', a + .05, { tam: 52, m: true, sonido: false }), g1 = emoji('🌏', a + .05, 96);
  const k2 = texto('20 minutos|ac', en('20 minutos', a), { tam: 76 }), a2 = texto('mi pueblo', en('pueblo', a), { tam: 52, m: true }), g2 = emoji('🏠', en('20 minutos', a), 96), vs = texto('vs', a + .3, { tam: 56, m: true, sonido: false });
  return t => { pe(g1, t, 280, 520); pt(k1, t, 280, 660); pt(a1, t, 280, 750); pt(vs, t, 540, 620); pe(g2, t, 800, 520); pt(k2, t, 800, 660); pt(a2, t, 800, 750); };
});
/* esa soledad tan grande · cuando sacas esa emoción */
bloque(...T3, (a) => {
  const so = texto('soledad|raiz', en('soledad', a - 1), { tam: 110 }), sl = silueta(), f = path('', AC, 8), s = texto('sacas esa emoción', en('sacas', a), { tam: 56, m: true });
  return t => { pt(so, t, 540, 470, 1 - P(t, s._t0, .2)); const c = pintarSilueta(sl, t, s._t0 - .3, 300, 900, .6)('corazon');
    f.setAttribute('d', flecha(c.x + 40, c.y, 640, 560)); dib(f, out(P(t, s._t0, .5))); pt(s, t, 760, 640); };
});
/* sin poner barreras: vas sacando un montón de emoción */
bloque(...T4, (a) => {
  const muro = [0, 1, 2].map(() => path('', NEGRO, 7)), tB = en('barreras', a), m = texto('un montón de emoción|ac', en('montón', a), { tam: 72 });
  const COLS = [C.raiz, C.sacro, C.plexo, C.ojo, C.garganta], bol = COLS.map(c => path('', c, 7));
  suena(tB, 'descarte', .3);
  return t => { const k = out(P(t, tB, .5));
    muro.forEach((w, i) => { w.setAttribute('d', cajaR(330 + i * 140, 600, 130, 80, 8)); w.setAttribute('transform', `translate(0,${(160 * k * (i - 1) * (i - 1)).toFixed(1)}) rotate(${(i - 1) * 25 * k} ${395 + i * 140} 640)`); dib(w, out(P(t, a - .2 + i * .1, .3)), 1 - .8 * k); });
    bol.forEach((b, i) => { const q = P(t, m._t0 + i * .15, 1.6); b.setAttribute('d', circulo(380 + i * 80, 640 - 140 * out(q), 18)); dib(b, q > 0 ? 1 : 0, 1 - .5 * q); });
    pt(m, t, 540, 830); };
});
/* diciendo que sí cuando querías decir que no · todo te enseña */
bloque(...T5, (a) => {
  const si = texto('«sí»', en('sí', a - .5), { tam: 96, m: true }), x = path('', '#9a9a9a', 10), no = texto('querías decir «no»|raiz', en('querías', a), { tam: 64 });
  const ens = texto('todo te enseña|ac', en('te enseña', a), { tam: 92 });
  return t => { const o = 1 - P(t, ens._t0 - .3, .3); pt(si, t, 540, 480, o); x.setAttribute('d', 'M470,484 L610,476'); dib(x, out(P(t, no._t0, .3)), o); pt(no, t, 540, 620, o); pt(ens, t, 540, 560); };
});
