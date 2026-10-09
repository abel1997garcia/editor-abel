/* c02 · «Todo es energía aunque no la veas» (acento: corazón). Un bloque por tramo de tablero (TABLEROS) */
const [T1, T2, T3, T4] = TABLEROS;
const CH = ['corona', 'ojo', 'garganta', 'corazon', 'plexo', 'sacro', 'raiz'];

/* 1 · gancho: todo es energía (los centros se encienden); no se ve, pero se siente (aura) */
bloque(...T1, () => {
  const sl = silueta(), pts = CH.map(c => path('', C[c], 16)), aura = [0, 1].map(() => path('', AC, 6));
  const tE = en('energía', 0), tN = en('no se ve', 3), tS = en('siente', 4);
  const a = texto('no se ve', tN, { tam: 64, m: true }), b = texto('se siente|ac', tS, { tam: 72 });
  suena(tE, 'brillo', .3); suena(tS + .1, 'swell', .3);
  return t => {
    const c = pintarSilueta(sl, t, -.4, 540, 900, .62);
    pts.forEach((p, i) => { const q = c(CH[i]); p.setAttribute('d', circulo(q.x, q.y, 9 + 2 * Math.sin(t * 6 + i))); dib(p, out(P(t, tE - .1 + i * .12, .2))); });
    aura.forEach((o, i) => { const r = 230 + i * 50 + 10 * Math.sin(t * 3 + i); o.setAttribute('d', `M${540 - r * .55},${690} A${r * .55},${r} 0 1 1 ${540 + r * .55},690 A${r * .55},${r} 0 1 1 ${540 - r * .55},690`); dib(o, out(P(t, tS - .1 + i * .15, .6)), .8); });
    pt(a, t, 230, 560); pt(b, t, 860, 560);
  };
});

/* 2 · todas esas cosas las vas a ir sintiendo… escucha tu voz interior */
bloque(...T2, (a) => {
  const sl = silueta(), oreja = path('', AC, 7), tV = en('voz interior', a);
  const L = [['ansiedad', 'raiz'], ['estrés', 'raiz'], ['decir que sí', 'garganta']].map(([w, c], i) => texto(`${w}|${c}`.replace(/ (?=\S+\|)/g, ' '), a + .1 + i * .3, { tam: 60 }));
  const v = texto('tu voz interior|ac', tV, { tam: 72 });
  return t => {
    const c = pintarSilueta(sl, t, a - .3, 300, 900, .6)('corazon');
    L.forEach((e, i) => pt(e, t, 760, 500 + i * 100, 1 - .55 * P(t, tV, .3)));
    oreja.setAttribute('d', onda(c.x + 40, 600, c.y, 12, t * 8, 3)); dib(oreja, out(P(t, tV - .1, .5)));
    pt(v, t, 760, 820);
  };
});

/* 3 · la pareja que más te complemente, el entorno… o sea, todo */
bloque(...T3, (a) => {
  const yo = stickman(), ella = stickman(), cor = emoji('❤️', en('complemente', a - .5), 90), circ = path('', AC, 7);
  const gente = [0, 1, 2, 3].map(() => stickman('#9a9a9a')), tEn = en('entorno', a), tT = en('todo', tEn);
  const p = pastilla('TODO', tT, { ac: true, tam: 64 });
  return t => {
    pintarStick(yo, t, a - .4, 450, 820, .6); pintarStick(ella, t, a - .25, 630, 820, .6);
    pe(cor, t, 540, 520);
    gente.forEach((g, i) => pintarStick(g, t, tEn - .1 + i * .08, [190, 300, 780, 890][i], 860, .38));
    circ.setAttribute('d', 'M120,680 A420,265 0 1 1 960,680 A420,265 0 1 1 120,680'); dib(circ, out(P(t, tEn, .6)));
    pt(p, t, 540, 470);
  };
});

/* 4 · ten en cuenta desde qué intención haces las cosas: de ahí depende toda tu vida (flecha → diana) */
bloque(...T4, (a) => {
  const d = [0, 1, 2].map(() => path('', AC, 8)), f = path('', NEGRO, 9);
  const tI = en('intención', a), tV = en('toda tu vida', tI);
  const p = pastilla('INTENCIÓN', tI, { ac: true, tam: 56 }), v = texto('toda tu vida', tV, { tam: 80 });
  suena(tV, 'golpe', .35);
  return t => {
    d.forEach((c, i) => { c.setAttribute('d', circulo(800, 640, 140 * (1 - i * .33))); dib(c, out(P(t, a - .3 + i * .1, .4))); });
    const k = io(P(t, tI - .1, tV - tI + .1)); f.setAttribute('d', flecha(160, 640, lerp(200, 790, k), 640, 32)); dib(f, k > 0 ? 1 : 0);
    pt(p, t, 400, 470); pt(v, t, 540, 870);
  };
});
