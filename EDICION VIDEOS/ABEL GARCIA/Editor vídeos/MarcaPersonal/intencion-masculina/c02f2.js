/* c02 · F2 «Deja de ignorar tu voz interior» (acento: corazón). Abajo (940–1920) predomina la imagen; lo importante fuera
   de la interfaz (x < 930, y < 1600). Pastillas que entran con su palabra; al final, esquema en blanco: flecha → diana */
const c1 = en('vida de tus sueños', 6) - .2, c2 = en('todo es energía', 10) - .2, c3 = en('puedes sentir cuando', 18) - .2,
      c4 = en('puedes tener', 24) - .2, c5 = en('así que', 29) - .2;
imagen('img/nino.jpg', 0, c1, { fx: .45, fy: .35 });
imagen('img/pareja.jpg', c1, c2, { fx: .5, fy: .45 });
imagen('img/sentir.jpg', c2, c3, { fx: .5, fy: .35 });
imagen('img/estres.jpg', c3, c4, { fx: .62, fy: .4 });
imagen('img/pareja.jpg', c4, c5, { fx: .45, fy: .5, zoom: .12 });
imagen(null, c5, DUR);
const Y1 = 1095, Y2 = 1010;     // pastillas en lo alto del hueco (cielo, pared, frente): nunca sobre caras ni bocas

/* gancho: tu voz interior → tu niño interior */
bloque(0, c1, () => {
  const a = pastilla('TU VOZ INTERIOR', en('voz interior', 0)), b = pastilla('TU NIÑO INTERIOR', en('niño', 2), { ac: true });
  return t => { pt(a, t, 465, Y1, 1 - P(t, b._t0, .2)); pt(b, t, 465, Y1); };
});
/* la vida de tus sueños, la pareja, el entorno */
bloque(c1, c2, () => {
  const a = pastilla('LA VIDA DE TUS SUEÑOS', en('vida de tus sueños', 6), { ac: true }), b = pastilla('LA PAREJA', en('pareja', 7)), c = pastilla('EL ENTORNO', en('entorno', 9));
  return t => { pt(a, t, 465, Y2); pt(b, t, 300, Y1); pt(c, t, 640, Y1); };
});
/* todo es energía: no se ve, pero se siente */
bloque(c2, c3, () => {
  const a = pastilla('TODO ES ENERGÍA', en('todo es energía', 10)), b = pastilla('NO SE VE', en('no se ve', 14)), c = pastilla('SE SIENTE', en('siente', 15), { ac: true });
  const tachon = path('', '#fff', 10);
  return t => { pt(a, t, 465, Y1, 1 - P(t, b._t0, .2)); pt(b, t, 290, Y2); pt(c, t, 640, Y2);
    tachon.setAttribute('d', `M${290 - b.offsetWidth / 2 + 30},${Y2 + 2} L${290 + b.offsetWidth / 2 - 30},${Y2 - 4}`); dib(tachon, out(P(t, c._t0 - .1, .3)), .9); };
});
/* ansiedad, estrés, decir que sí queriendo decir que no */
bloque(c3, c4, () => {
  const L = [['ANSIEDAD', 'ansiedad'], ['ESTRÉS', 'estrés'], ['DECIR QUE SÍ', 'dices que sí']].map(([w, p], i) => pastilla(w, en(p, 18), { tam: 38 }));
  const s = pastilla('LO VAS A IR SINTIENDO', en('sintiendo', 22), { ac: true, tam: 38 });
  return t => { L.forEach((e, i) => pt(e, t, [165, 440, 715][i], Y2, 1 - P(t, s._t0, .2))); pt(s, t, 300, Y2); };
});
/* más capacidad de manifestación: la vida que tú quieras */
bloque(c4, c5, () => {
  const a = pastilla('MANIFESTACIÓN', en('manifestación', 24), { ac: true }), b = pastilla('LA VIDA QUE TÚ QUIERAS', en('vida que tú quieras', 27));
  return t => { pt(a, t, 465, Y2); pt(b, t, 465, Y1); };
});
/* cierre (blanco): ten en cuenta desde qué intención haces las cosas → de ahí depende toda tu vida */
bloque(c5, DUR, () => {
  const d = [0, 1, 2].map(() => path('', AC, 9)), f = path('', NEGRO, 10), tI = en('intención', 32), tV = en('toda tu vida', tI);
  const p = pastilla('INTENCIÓN', tI, { ac: true }), v = pastilla('TODA TU VIDA', tV);
  suena(tV, 'golpe', .35);
  return t => {
    d.forEach((c, i) => { c.setAttribute('d', circulo(700, 1250, 150 * (1 - i * .33))); dib(c, out(P(t, c5 + .1 + i * .1, .4))); });
    const k = io(P(t, tI - .1, tV - tI + .1)); f.setAttribute('d', flecha(150, 1250, lerp(190, 690, k), 1250, 34)); dib(f, k > 0 ? 1 : 0);
    pt(p, t, 330, 1060); pt(v, t, 700, 1470);
  };
});
