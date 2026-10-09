/* c03 · «No te fías de lo que sientes» (acento: tercer ojo) */
const [T1, T2, T3, T4, T5, T6] = TABLEROS;

/* quieren manifestar, pero no se fían ni una mierda de lo que sienten y de su intuición */
bloque(...T1, (a) => {
  const sl = silueta(), luz = path('', AC, 7), tI = en('intuición', a);
  const L = [['quieren manifestar', 'manifestar', 60, true], ['no se fían|raiz', 'fían', 84], ['de lo que sienten', 'sienten', 56, true], ['su intuición|ac', 'intuición', 72]].map(([f, p, tam, m]) => texto(f, en(p, a), { tam, m }));
  return t => { const c = pintarSilueta(sl, t, a - .3, 260, 900, .6)('ojo'); luz.setAttribute('d', circulo(c.x, c.y, 20 + 6 * Math.sin(t * 5))); dib(luz, out(P(t, tI - .1, .3)));
    L.forEach((e, i) => pt(e, t, 720, 480 + i * 115)); };
});
/* se han topado con la misma persona, el mismo tipo de relación… (bucle) */
bloque(...T2, (a) => {
  const lp = path('', C.raiz, 9), m = texto('la misma persona|raiz', en('misma persona', a), { tam: 68 }), r = texto('el mismo tipo de relación', en('mismo tipo', a), { tam: 54, m: true });
  const st = stickman();
  return t => { const ang = (t - a) * 1.6; lp.setAttribute('d', `M${540 + 190 * Math.cos(ang)},${680 + 150 * Math.sin(ang)} A190,150 0 1 1 ${540 + 190 * Math.cos(ang - .5)},${680 + 150 * Math.sin(ang - .5)} l18,-28`); dib(lp, out(P(t, a - .3, .6)));
    pintarStick(st, t, a - .2, 540, 760, .35); pt(m, t, 540, 460); pt(r, t, 540, 880); };
});
/* escuchar lo que quieres, lo que necesitas y para lo que estás aquí */
bloque(...T3, (a) => {
  const F = [['lo que quieres', 'quieres'], ['lo que necesitas', 'necesitas'], ['para lo que estás aquí|ac', 'estás aquí']].map(([f, p]) => ({ e: texto(f, en(p, a), { tam: 64 }), m: path('', C.corazon, 9), t0: en(p, a) }));
  const o = texto('escuchar', a + .05, { tam: 56, m: true });
  return t => { pt(o, t, 540, 460); F.forEach((f, i) => { const y = 580 + i * 110; f.m.setAttribute('d', tick(190, y)); dib(f.m, out(P(t, f.t0, .3))); pt(f.e, t, 240 + f.e.offsetWidth / 2, y); }); };
});
/* una voz te dice: por aquí no, por aquí no… y dejas de trabajar allí */
bloque(...T4, (a) => {
  const st = stickman(), fl = [0, 1, 2].map(() => path('', NEGRO, 7)), xs = [0, 1, 2].map(() => path('', C.raiz, 10));
  const ts = [en('no', a), en('aquí no', a + .5) + .2, en('aquí no', a + 2) + .2], tD = en('dejas', a);
  const tr = texto('trabajo', a + .05, { tam: 60 }), caja = path(cajaR(640, 760, 300, 110, 18), NEGRO, 7), xg = path('', C.raiz, 12);
  const D = [[300, 470], [540, 450], [780, 470]];
  ts.forEach(x => suena(x, 'descarte', .3));
  return t => { const p = pintarStick(st, t, a - .2, 300, 900, .5);
    D.forEach(([x, y], i) => { fl[i].setAttribute('d', flecha(p.cabeza.x, p.cabeza.y - 60, x, y + 40)); dib(fl[i], out(P(t, a + i * .1, .3))); xs[i].setAttribute('d', cruz(x, y, 1.1)); dib(xs[i], out(P(t, ts[i], .25))); });
    dib(caja, out(P(t, a - .2, .4))); pt(tr, t, 790, 815); xg.setAttribute('d', cruz(790, 815, 3)); dib(xg, out(P(t, tD, .3))); };
});
/* todos dirán que estás loco… pero si tú lo sientes, aunque no sepas por qué */
bloque(...T5, (a) => {
  const lo = texto('loco', a + .05, { tam: 80, m: true }), x = path('', '#9a9a9a', 9), s = texto('lo sientes|ac', en('sientes', a), { tam: 104 }), l = texto('sin lógica', en('lógica', a), { tam: 60, m: true });
  const sl = silueta(), cor = path('', AC, 12);
  return t => { pt(lo, t, 760, 470); x.setAttribute('d', 'M680,472 L840,466'); dib(x, out(P(t, s._t0 - .1, .3))); pt(s, t, 760, 620); pt(l, t, 760, 760);
    const c = pintarSilueta(sl, t, a - .3, 260, 900, .6)('corazon'); cor.setAttribute('d', circulo(c.x, c.y, 12 + 4 * Math.sin(t * 6))); dib(cor, out(P(t, s._t0, .3))); };
});
/* lo que sientes es lo que luego crea tu propia vida */
if (T6) bloque(...T6, (a) => {
  const sl = silueta(), cor = path('', AC, 12), f = path('', AC, 8), v = texto('tu propia vida|ac', en('propia vida', a), { tam: 84 }), s = texto('lo que sientes', a + .05, { tam: 60, m: true });
  return t => { const c = pintarSilueta(sl, t, a - .3, 260, 900, .6)('corazon'); cor.setAttribute('d', circulo(c.x, c.y, 12)); dib(cor, 1);
    f.setAttribute('d', flecha(c.x + 60, c.y, 600, 640)); dib(f, out(P(t, en('crea', a) - .2, .5))); pt(s, t, 760, 500); pt(v, t, 780, 700); };
});
