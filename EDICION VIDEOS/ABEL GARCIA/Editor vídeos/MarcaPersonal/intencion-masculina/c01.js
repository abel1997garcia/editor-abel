/* c01 · «Atraes a quien vibra como tú» (acento: corona). Un bloque por tramo de tablero (TABLEROS) */
const [T1, T2, T3, T4] = TABLEROS;

/* 1 · gancho: nunca se trata de la otra persona → atraes a quien está en tu misma frecuencia */
bloque(...T1, () => {
  const yo = stickman(), otra = stickman(), w = path('', '#bbb', 8), tO = en('otra', 0), tA = en('atraes', 1), tF = en('frecuencia', 3);
  const l1 = texto('tú', .1, { tam: 56, m: true, sonido: false }), l2 = texto('la otra persona', tO, { tam: 56, m: true });
  const p = pastilla('MISMA FRECUENCIA', tF, { ac: true }); p.classList.add('g');
  return t => {
    pintarStick(yo, t, -.4, 260, 830, .7); pintarStick(otra, t, tO - .2, 820, 830, .7, 0, t < tA ? .45 : 1);
    pt(l1, t, 260, 885); pt(l2, t, 820, 885);
    const kF = P(t, tF - .1, .4); w.setAttribute('stroke', kF > .5 ? AC : '#bbb');
    w.setAttribute('d', onda(370, 710, 620, lerp(10, 26, kF), t * 7, lerp(3, 5, kF))); dib(w, out(P(t, tA - .1, .6)));
    pt(p, t, 540, 500);
  };
});

/* 2 · vergüenza, culpabilidad, arrepentimiento… eso vibra (silueta) */
bloque(...T2, (a) => {
  const sl = silueta(), anillos = [0, 1, 2].map(() => path('', C.raiz, 6)), tV = en('vibra', 12);
  const L = ['vergüenza', 'culpabilidad', 'arrepentimiento'].map(w => texto(w + '|raiz', en(w, a), { tam: 64 }));
  suena(tV, 'swell', .3);
  return t => {
    const c = pintarSilueta(sl, t, a - .3, 300, 900, .6)('plexo');
    L.forEach((e, i) => pt(e, t, 720, 520 + i * 110));
    anillos.forEach((r, i) => { const rr = 40 + ((t - tV) * 70 + i * 30) % 90; r.setAttribute('d', circulo(c.x, c.y, rr)); dib(r, t > tV ? 1 : 0, 1 - rr / 140); });
  };
});

/* 3 · la realidad parece muy real (la tocas)… pero todo es como tú te sientes */
bloque(...T3, (a) => {
  const caja = path(cajaR(270, 470, 540, 220, 26), NEGRO, 8), r = texto('la realidad', a + .05, { tam: 72, sonido: false });
  const mano = emoji('✋', en('tocas', a - 1), 100), tP = en('pero todo', a), s = texto('todo es como tú|ac te sientes|ac', tP, { tam: 60 });
  const ok = texto('muy bien hecha', en('hecha', a), { tam: 52, m: true });
  return t => {
    const g = P(t, tP, .4); caja.setAttribute('stroke', g > .5 ? '#bbb' : NEGRO); dib(caja, out(P(t, a - .3, .5)));
    pt(r, t, 540, 580, 1 - .55 * g); pe(mano, t, 200 + 40 * Math.sin(Math.max(0, t - mano._t0) * 6) * (1 - g), 560);
    pt(ok, t, 540, 750, 1 - g); pt(s, t, 540, 850);
  };
});

/* 4 · cuando dejas de necesitar algo abres la puerta para atraerlo… es la frecuencia que tú emanas */
bloque(...T4, (a) => {
  const marco = path(cajaR(200, 470, 200, 380, 10), NEGRO, 8), hoja = path('', NEGRO, 7, '#fff'), fl = path('', AC, 8), yo = stickman(), ondas = [0, 1, 2].map(() => path('', AC, 6));
  const tAb = en('abres', a - .5), tAt = en('atraer', a), tI = en('inconsciente', a), tE = en('emanas', a);
  const i1 = texto('inconsciente', tI, { tam: 56, m: true }), e1 = texto('la frecuencia|ac que emanas', en('frecuencia', tI), { tam: 56 });
  return t => {
    dib(marco, out(P(t, a - .3, .5)));
    const k = out(P(t, tAb - .1, .6)), w = 200 * (1 - .7 * k); hoja.setAttribute('d', `M200,470 L${200 + w},${490 + 25 * k} L${200 + w},${830 - 25 * k} L200,850 Z`); dib(hoja, out(P(t, a - .2, .4)));
    fl.setAttribute('d', flecha(620, 660, 440, 660)); dib(fl, out(P(t, tAt - .1, .4)));
    const st = pintarStick(yo, t, tI - .3, 780, 880, .5);
    ondas.forEach((o, i) => { const rr = 70 + ((t - tE) * 90 + i * 45) % 140; o.setAttribute('d', circulo(780, st.pecho.y, rr)); dib(o, t > tE - .2 ? 1 : 0, 1 - rr / 230); });
    pt(i1, t, 780, 485); pt(e1, t, 540, 420);
  };
});
