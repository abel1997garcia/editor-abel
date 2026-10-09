/* c05 · «No existe ninguna casualidad» (acento: corona) */
const [T1, T2, T3, T4, T5, T6] = TABLEROS;

/* te aseguro que en la vida no existe ninguna casualidad (el dado, tachado) */
bloque(...T1, (a) => {
  const d = emoji('🎲', a + .05, 130), c = texto('casualidad|ac', en('casualidad', a), { tam: 104 }), x = path('', C.raiz, 12), tX = en('casualidad', a) + .45;
  suena(tX, 'descarte', .35);
  return t => { pe(d, t, 540, 520, 1); pt(c, t, 540, 720); x.setAttribute('d', `M${540 - c.offsetWidth / 2 - 10},726 L${540 + c.offsetWidth / 2 + 10},712`); dib(x, out(P(t, tX, .3))); };
});
/* la persona indicada en el momento indicado, perfecta para ti */
bloque(...T2, (a) => {
  const A = stickman(), B = stickman(), r = emoji('⏰', en('momento', a), 90), m = texto('el momento indicado|ac', en('momento', a), { tam: 68 }), p = texto('perfecta para ti', en('perfecta', a), { tam: 56, m: true });
  return t => { const k = out(P(t, en('perfecta', a) - .2, .8)); pintarStick(A, t, a - .2, 300 + 130 * k, 900, .45); pintarStick(B, t, a - .1, 780 - 130 * k, 900, .45);
    pe(r, t, 540, 470); pt(m, t, 540, 580); pt(p, t, 540, 660); };
});
/* en ese momento justo, cuando estás preparado */
bloque(...T3, (a) => {
  const P1 = emoji('🧩', a + .05, 110), P2 = emoji('🧩', a + .25, 110), tP = en('preparado', a), pr = texto('preparado|ac', tP, { tam: 104 }), j = texto('justo', en('justo', a), { tam: 60, m: true });
  return t => { const k = out(P(t, tP - .4, .5)); pe(P1, t, 360 + 100 * k, 560); pe(P2, t, 720 - 100 * k, 560); pt(j, t, 540, 460); pt(pr, t, 540, 760); };
});
/* la clave: vivir la vida con paz (es fácil decirlo… pero es así) */
bloque(...T4, (a) => {
  const pz = texto('con paz|ac', a + .05, { tam: 110 }), pa = emoji('🕊️', a + .1, 110), f = texto('muy fácil decirlo', en('fácil', a), { tam: 56, m: true }), r = texto('pero es así', en('pero es así', a), { tam: 64 });
  return t => { pe(pa, t, 540, 470); pt(pz, t, 540, 620); pt(f, t, 540, 740, 1 - P(t, r._t0, .2)); pt(r, t, 540, 740); };
});
/* queremos controlar y pactar todo el camino… pero no funciona así */
bloque(...T5, (a) => {
  const rec = path('M200,720 L880,720', '#9a9a9a', 8), cur = path('', AC, 8), x = path('', C.raiz, 10), tC = en('controlar', a), tN = en('no funciona', a);
  const c = texto('controlar|raiz', tC, { tam: 84 }), n = texto('no funciona así', tN, { tam: 60, m: true }), A = emoji('📍', a + .05, 70), B = emoji('🏁', a + .05, 70);
  return t => { pt(c, t, 540, 480); pe(A, t, 200, 680); pe(B, t, 880, 680); dib(rec, out(P(t, tC, .6))); x.setAttribute('d', cruz(540, 720, 1.4)); dib(x, out(P(t, tN, .3)));
    let d = 'M200,720 '; for (let i = 1; i <= 40; i++) { const xx = 200 + 17 * i; d += `L${xx},${720 + 70 * Math.sin(i / 40 * Math.PI * 3) * Math.sin(i / 40 * Math.PI)} `; } cur.setAttribute('d', d); dib(cur, out(P(t, tN + .2, .8)));
    pt(n, t, 540, 860); };
});
/* nunca puedes pensar en el cómo, porque nunca lo has hecho */
if (T6) bloque(...T6, (a) => {
  const q = texto('¿cómo?', en('cómo', a), { tam: 120, m: true }), x = path('', C.raiz, 12), n = texto('nunca lo has hecho|ac', en('nunca lo has hecho', a), { tam: 72 });
  return t => { pt(q, t, 540, 540); x.setAttribute('d', cruz(540, 540, 4)); dib(x, out(P(t, n._t0, .3))); pt(n, t, 540, 760); };
});
