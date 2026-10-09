/* c05 · trial «Algo me dijo que no» (550.000 €) — UNA idea: decir que no le salvó, porque no estaba preparado.
   Su discurso EN SU ORDEN, casi de corrido (Abel 08/10: la versión reordenada «muy mal cortada»). El 550.000 solo lo dice él (no repetirlo en pantalla).
   Fotos SOLO de la época de cada frase (memoria fotos-vida-abel); lo que no pasó (fiesta y descontrol) → solo gráficos. Zona de gráficos y 400–950. Acento: corona */
const [T1, T2, T3, T4, T5, T6, T7] = TABLEROS;
const FM = 'img/', DIN = FM + '05-canal-automatizacion-ganaba-dinero/';
const sale = (e, t, x, y, sig) => pt(e, t, x, y, 1 - P(t, sig - .1, .15));
const izq = (src, t0, t1, pos = '50% 40%', r = -3) => foto(src, t0, t1, { w: 400, h: 500, pos, x: 290, y: 690, r });

/* gancho: me ofrecieron 550.000 € por ese canal → el canal (la placa, lo que ganaba) */
bloque(...T1, (a) => {
  const pl = izq(DIN + 'abel_placa_100k_suscriptores_youtube.jpg', a + .05, T1[1], '50% 35%');
  const c = texto('ese canal:', en('por ese canal', a), { tam: 48, m: true }), s = texto('100.000|ac', en('por ese canal', a) + .25, { tam: 92 });
  const s2 = texto('suscriptores', en('por ese canal', a) + .4, { tam: 48, m: true }), f = texto('17.000 €/mes', en('no me digas', a), { tam: 64 });
  return t => { pf(pl, t); pt(c, t, 760, 500); pt(s, t, 760, 600); pt(s2, t, 760, 690); pt(f, t, 760, 820); };
});
/* nunca pasa por casualidad · la persona que era en ese pasado (época del dinero: Budapest) */
bloque(...T2, (a) => {
  const f = izq(DIN + 'abel_budapest.jpg', en('me di cuenta', a), T2[1]);
  const n = texto('nunca pasa por', a + .05, { tam: 52, m: true }), c = texto('casualidad|ac', en('casualidad', a), { tam: 96 });
  const p = texto('la persona', en('la persona', a), { tam: 60 }), e = texto('que era', en('que era', a), { tam: 60 });
  return t => { const k = P(t, f.t0 - .1, .3);
    pt(n, t, lerp(540, 760, k), lerp(560, 480, k)); pt(c, t, lerp(540, 760, k), lerp(680, 580, k), 1, lerp(1, .8, k)); pf(f, t); pt(p, t, 760, 720); pt(e, t, 760, 810); };
});
/* obviamente no estaba preparado · generaba dinero, por supuesto (el estadio, la época del dinero) */
bloque(...T3, (a) => {
  const f = izq(DIN + 'abel_estadio_futbol.jpg', a + .05, T3[1], '50% 40%', 3);
  const n = texto('NO|raiz', en('no estaba preparado', a), { tam: 130 }), p = texto('estaba preparado', en('preparado', a), { tam: 56 });
  const g = texto('generaba dinero', en('generaba', a), { tam: 52, m: true });
  return t => { pf(f, t); pt(n, t, 760, 530); pt(p, t, 760, 650); pt(g, t, 760, 800); };
});
/* no estaba bien emocionalmente · dependencia emocional · me validaba (Menorca → La Roca Village, de compras) */
bloque(...T4, (a) => {
  const tV = en('validaba', a);
  const f1 = izq(DIN + 'abel_menorca_paseo_costa.jpg', a + .05, tV - .1, '50% 45%');
  const f2 = izq(DIN + 'abel_la_roca_village_noche.jpg', tV, T4[1], '50% 50%', 3);
  const b = texto('no estaba bien|raiz', en('no estaba bien', a), { tam: 58 }), d = texto('dependencia', en('dependencia', a), { tam: 70 });
  const e = texto('emocional', en('emocional', a), { tam: 52, m: true }), v = texto('me validaba|ac', tV, { tam: 64 });
  return t => { pf(f1, t); pf(f2, t); pt(b, t, 760, 480); pt(d, t, 760, 610); pt(e, t, 760, 690); pt(v, t, 760, 820); };
});
/* si lo hubiera vendido, me hubiese jodido la vida (no pasó: solo gráficos) */
bloque(...T5, (a) => {
  const tJ = en('jodido', a), s = texto('si lo hubiera', a + .05, { tam: 60 }), vd = texto('VENDIDO|raiz', en('vendido', a), { tam: 130 });
  const yt = texto('mi canal de YouTube', en('YouTube', a), { tam: 48, m: true });
  const j = texto('me hubiese jodido', tJ, { tam: 72 }), v = texto('la vida|raiz', en('la vida', a), { tam: 120 });
  suena(tJ, 'golpe-corto', .3);
  return t => { const k = P(t, tJ - .15, .2); pt(s, t, 540, 470, 1 - k); pt(vd, t, 540, 620, 1 - k); pt(yt, t, 540, 750, 1 - k);
    pt(j, t, 540, 560); pt(v, t, 540, 720); };
});
/* gastado y mal gastado en fiesta (no pasó: solo gráficos, sin fotos de otra época) */
bloque(...T6, (a) => {
  const g = texto('gastado', a + .05, { tam: 100 }), mg = texto('y MAL|raiz gastado', en('mal gastado', a), { tam: 100 });
  const fi = texto('en fiesta', en('fiesta', a), { tam: 60, m: true });
  suena(en('mal gastado', a), 'descarte', .25);
  return t => { pt(g, t, 540, 480); pt(mg, t, 540, 640); pt(fi, t, 540, 800); };
});
/* aprendido · evolucionado · crecimiento: las teles de 70 kg → Ha Long → leyendo en su primera casa de Australia */
bloque(...T7, (a) => {
  const t2 = en('evolucionado', a), t3 = en('me hubiese metido', a);
  const v1 = clip('teles', 240, a + .05, t2 - .1, { w: 400, h: 480, pos: '50% 40%', y: 730, r: 3 });
  const f2 = foto(FM + '09-sudeste-asiatico/abel_bahia_ha_long_vietnam.jpg', t2, t3 - .1, { w: 460, h: 480, pos: '50% 50%', y: 730, r: -3 });
  const f3 = foto(FM + '08-australia/abel_leyendo_sudadera_azul_primera_casa.png', t3, T7[1] + 1, { w: 400, h: 480, pos: '50% 40%', y: 730, r: 3 });
  const L = [['aprendido', a + .05, t2], ['evolucionado|ac', t2, t3], ['autoconocimiento|ac', t3, 1e9]].map(([s, t0, sig]) => [texto(s, t0, { tam: 72 }), sig]);
  return t => { pf(v1, t); pf(f2, t); pf(f3, t); L.forEach(([e, sig]) => sale(e, t, 540, 440, sig)); };
});
