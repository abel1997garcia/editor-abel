/* c03 · «Si te respetas, te van a respetar» (acento: plexo). Un bloque por tramo de tablero (TABLEROS) */
const [T1, T2, T3, T4] = TABLEROS;

/* 1 · gancho: si tú te respetas, los demás te respetan: las dinámicas sociales son un reflejo de cómo estás */
bloque(...T1, () => {
  const yo = stickman(), otros = [0, 1].map(() => stickman()), aura = path('', AC, 7), fl = [0, 1].map(() => path('', AC, 7));
  const tR = en('respetas', 0), tO = en('otras personas', 1), tP = en('respetar', 2), tF = en('reflejo', 3);
  const l = texto('tú', .1, { tam: 56, m: true, sonido: false }), ticks = [0, 1].map(() => path('', C.corazon, 9));
  const p = pastilla('UN REFLEJO DE CÓMO ESTÁS', tF, { ac: true, tam: 40 });
  suena(tP + .2, 'tick', .3);
  return t => {
    const st = pintarStick(yo, t, -.4, 260, 840, .7, out(P(t, tR, .5)) * .9);
    aura.setAttribute('d', circulo(st.cabeza.x, st.cabeza.y, 60 + 5 * Math.sin(t * 5))); dib(aura, out(P(t, tR, .4)));
    pt(l, t, 260, 885);
    otros.forEach((o, i) => { const x = 700 + i * 190, s2 = pintarStick(o, t, tO - .2 + i * .15, x, 840, .55);
      fl[i].setAttribute('d', flecha(x - 70, s2.pecho.y - 30 - i * 30, 360, 640 - i * 30)); dib(fl[i], out(P(t, tP - .3 + i * .1, .4)));
      ticks[i].setAttribute('d', tick(x, s2.cabeza.y - 90)); dib(ticks[i], out(P(t, tP + i * .1, .3))); });
    pt(p, t, 540, 470);
  };
});

/* 2 · sabes de tu valor, de tu trabajo, de cómo cuidas tu energía → cada vez más consciente */
bloque(...T2, (a) => {
  const F = [['tu valor', a + .05], ['tu trabajo', a + .25], ['tu energía|ac', en('energía', a)]].map(([w, t0]) => ({ e: texto(w, t0, { tam: 64 }), m: path('', C.corazon, 9), t0 }));
  const tC = en('consciente', a), b = barra(AC), lb = texto('más consciente', tC - .3, { tam: 52, m: true });
  suena(tC, 'subida', .3);
  return t => {
    F.forEach((f, i) => { const y = 490 + i * 100; f.m.setAttribute('d', tick(250, y)); dib(f.m, out(P(t, f.t0, .3))); pt(f.e, t, 290 + f.e.offsetWidth / 2, y); });
    pt(lb, t, 540, 770); pintarBarra(b, t, tC - .3, 260, 850, 560, .1 + .85 * out(P(t, tC - .3, 1.6)));
  };
});

/* 3 · entender desde dónde actúa la otra persona… porque tú lo has trabajado dentro (silueta) */
bloque(...T3, (a) => {
  const sl = silueta(), cor = path('', AC, 10), ond = [0, 1].map(() => path('', AC, 6)), tD = en('dentro', a);
  const d1 = texto('desde dónde actúa', a + .05, { tam: 56 }), d2 = texto('la otra persona', en('otra persona', a), { tam: 56, m: true });
  const d3 = texto('lo has trabajado|ac dentro|ac', en('lo has trabajado', a), { tam: 56 });
  suena(tD, 'brillo', .3);
  return t => {
    const c = pintarSilueta(sl, t, a - .3, 280, 900, .6)('corazon');
    cor.setAttribute('d', circulo(c.x, c.y, 12 + 3 * Math.sin(t * 6))); dib(cor, out(P(t, tD - .2, .3)));
    ond.forEach((o, i) => { const r = 30 + ((t - tD) * 60 + i * 35) % 70; o.setAttribute('d', circulo(c.x, c.y, r)); dib(o, t > tD ? 1 : 0, 1 - r / 110); });
    pt(d1, t, 700, 520); pt(d2, t, 700, 600); pt(d3, t, 700, 800);
  };
});

/* 4 · la intención con la que haces algo es lo más importante de todo */
bloque(...T4, (a) => {
  const tI = en('importante', a), med = emoji('🥇', tI - .1, 150);
  const i1 = texto('la intención|ac', a + .05, { tam: 96 }), i2 = texto('que tú pones', en('que tú pones', a), { tam: 56, m: true });
  const i3 = texto('lo más importante', en('lo más importante', a), { tam: 64 });
  return t => { pt(i1, t, 540, 480); pt(i2, t, 540, 580); pe(med, t, 540, 720); pt(i3, t, 540, 860); };
});
