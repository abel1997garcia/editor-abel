/* =====================================================================
   ESCENAS — «Así empezaría mi marca personal desde 0 (CÓPIAME)». Usa herramientas/pizarra/libreria.js.
   Paleta: miedos = raíz, verdad/comunicar = garganta, autenticidad = corazón, dinero/energía = plexo, espiritual = corona.
   Todo dentro del 4:3 (x 350–1570). Cada escena = una ventana de edicion/montaje.json.
   ===================================================================== */
const titulo = (e, f, d, o = {}) => X(e, f, d, { tam: 96, y: 170, ...o });
const sub = (e, f, d, o = {}) => X(e, f, d, { tam: 64, m: true, ...o });
const fadeIn = (t, t0, d = .3) => P(t, t0 - .05, d, E.out3);
function circ(e, color = NEGRO, ancho = 7) { return trazo(e.svg, '', { ancho, color }); }
function pintarCirc(c, t, t0, x, y, r) { forma(c, () => circulo(x, y, r)); dibujar(c, dib(t, t0, .45)); }
function flechaE(e, color = NEGRO) { return fl(e.svg, 0, 0, 1, 1, { color }); }
function pintarFlecha(f, t, t0, x1, y1, x2, y2) { forma(f, () => flecha(x1, y1, x2, y2)); dibujar(f, dib(t, t0, .4)); }
function tachar(e, color = C.raiz) { return trazo(e.svg, '', { ancho: 9, color }); }
function pintarTachar(l, t, t0, el) { const o = el._o, { w } = medir(el), x = o.x - w * o.ax / 100; forma(l, () => linea(x - 20, o.y, x + w + 20, o.y, 0)); dibujar(l, dib(t, t0, .3)); }

/* 1 · los 3 pasos para tu marca personal desde cero */
escena('tres', e => {
  const z = X(e, 'te voy a explicar', 4.6, { tam: 60, m: true, gris: true, y: 150 });
  const a = titulo(e, '3 pasos|plexo', 5.5, { dice: 'los tres pasos', y: 280 });
  const nums = [0, 1, 2].map(() => circ(e, C.plexo)), n = ['1', '2', '3'].map((k, i) => texto(e, k, en('fundamentales', 5) + i * .35, { tam: 100, sonido: i === 0 }));
  const b = sub(e, 'tu marca personal desde cero', 8, { tam: 72, y: 930 });
  return (t, w) => { pt(z, t); pt(a, t); nums.forEach((c, i) => { pintarCirc(c, t, n[i]._t[0] - .15, 660 + i * 300, 600, 110); pt(n[i], t, { x: 660 + i * 300, y: 600 }); }); pt(b, t); };
});

/* 2 · un negocio auténtico y conectado contigo */
escena('autentico', e => {
  const a = X(e, 'un negocio que sea auténtico|corazon', 12, { tam: 84, y: 300 }), b = X(e, 'y conectado contigo', 13.5, { tam: 84, y: 760 });
  const cor = emoji(e, '❤️', 130, en('conectado', 13)), fls = [flechaE(e, C.corazon)];
  return (t, w) => { pt(a, t); pt(b, t); pe(cor, t, b._t[1], 960, 540); pintarFlecha(fls[0], t, b._t[0], 960, 400, 960, 460); };
});

/* 3 · no es descargarte Canva, ni tendencias, ni hacerte viral */
escena('canva', e => {
  const L = [['descargarte Canva', 17], ['buscar tendencias', 18.5], ['hacerte viral', 19.5]].map(([f, d]) => filaLista(e, f, en(f.split(' ')[0], d), { no: true, tam: 84 }));
  const tit = X(e, 'no significa', 16.5, { tam: 72, m: true, gris: true, y: 200 });
  return (t, w) => { pt(tit, t); L.forEach((f, i) => pintarFila(f, t, 640, 400 + i * 190)); };
});

/* 4 · la gran mayoría de las personas lo hacen mal */
escena('mayoria', e => {
  const a = X(e, 'la gran mayoría', 24.3, { tam: 96, y: 170 }), b = X(e, 'hacen mal|raiz', 25.5, { tam: 96, y: 960 });
  const g = [0, 1, 2, 3, 4, 5].map(() => stickman(e.svg)), xs = [0, 1, 2, 3, 4].map(() => trazo(e.svg, '', { ancho: 9, color: C.raiz }));
  return (t, w) => { pt(a, t); pt(b, t);
    g.forEach((s, i) => { const st = pintarStick(s, t, { x: 560 + i * 160, y: 820, s: .42, pose: i === 5 ? 'arriba' : 'pie', t0: w.a - .6 + i * .07 });
      if (i < 5) { forma(xs[i], () => cruz(st.cabeza.x, st.cabeza.y - 70, 1)); dibujar(xs[i], dib(t, b._t[1] + i * .06, .25)); } }); };
});

/* 5 · te ahorra tiempo, dolores de cabeza y energía */
escena('ahorrar', e => {
  const a = X(e, 'te va a ahorrar', 28.3, { tam: 84, y: 180 });
  const L = [['muchísimo tiempo', '⏳', 28.8], ['dolores de cabeza', '🤯', 29.8], ['mucha energía|plexo', '⚡', 30.6]].map(([f, ch, d]) => ({ tx: X(e, f, d, { tam: 72, ax: 0 }), em: emoji(e, ch, 90, en(f.split(' ')[0].replace(/\|.*/, ''), d)) }));
  return (t, w) => { pt(a, t); L.forEach((k, i) => { pe(k.em, t, k.tx._t[0], 640, 400 + i * 190); pt(k.tx, t, { x: 740, y: 400 + i * 190 }); }); };
});

/* 6 · desde lo más profundo de tu alma, desde tu autenticidad (silueta) */
escena('alma', e => {
  const sl = silueta(e.svg), luz = trazo(e.svg, '', { ancho: 12, color: C.corazon });
  const a = X(e, 'desde lo más profundo', 36.5, { tam: 64, x: 1150, y: 380 }), a2 = X(e, 'de tu alma', 37.6, { tam: 64, x: 1150, y: 480 }), b = X(e, 'desde tu autenticidad|corazon', 38.8, { tam: 72, x: 1150, y: 660 });
  return (t, w) => { const x = 560, y = 1010, s = .82; pintarSilueta(sl, t, { x, y, s, t0: w.a - .6 }); const c = centroSil(x, y, s, 'corazon');
    forma(luz, () => circulo(c.x, c.y, 16 + 5 * Math.sin(t * 6))); dibujar(luz, dib(t, b._t[2], .3)); pt(a, t); pt(a2, t); pt(b, t); };
});

/* 7 · soy Abel, 29 años, creando negocios por internet */
escena('abel', e => {
  const a = X(e, 'soy Abel', 41, { tam: 110, y: 200 }), b = X(e, '29 años', 41.8, { tam: 84, y: 340, gris: true }), v = X(e, 'toda mi vida', 43, { tam: 64, m: true, y: 470 });
  const c = X(e, 'crear negocios por internet', 44.5, { tam: 72, x: 1010, y: 640 }), d = X(e, 'ganar dinero|plexo', 46, { tam: 72, x: 1010, y: 820 });
  const pc = emoji(e, '💻', 100, c._t[0]), din = emoji(e, '💰', 100, d._t[0]);
  return (t, w) => { pt(a, t); pt(b, t); pt(v, t); pt(c, t); pt(d, t); pe(pc, t, c._t[0], 440, 640); pe(din, t, d._t[0], 640, 820); };
});

/* 8 · lo más importante es quién crea el negocio */
escena('quien', e => {
  const a = X(e, 'lo más importante', 49.2, { tam: 72, m: true, y: 180 }), b = X(e, 'es quién crea el negocio|garganta', 50.5, { tam: 88, y: 320 });
  const st = stickman(e.svg), f = flechaE(e, C.garganta), tienda = trazo(e.svg, '', { ancho: 7 }), mal = emoji(e, '💼', 110, b._t[3]);
  return (t, w) => { pt(a, t); pt(b, t); const s = pintarStick(st, t, { x: 700, y: 960, s: .7, pose: 'señala', t0: w.a - .6 });
    forma(tienda, () => caja(1050, 600, 340, 300)); dibujar(tienda, dib(t, b._t[3], .5)); pe(mal, t, b._t[3], 1220, 750); pintarFlecha(f, t, b._t[1], 820, 700, 1020, 720); };
});

/* 9 · mezclo dos mundos: desarrollo personal y marca personal */
escena('mundos', e => {
  const c1 = circ(e, C.corona), c2 = circ(e, C.garganta);
  const L = [['desarrollo personal', 53.2], ['espiritualidad|corona', 54.2], ['conciencia', 55]].map(([f, d]) => X(e, f, d, { tam: 56 }));
  const m = X(e, 'mezclar esos dos mundos', 56.5, { tam: 84, y: 170 }), r = X(e, 'marcas personales|garganta', 59.5, { tam: 60 }), au = X(e, 'desde la autenticidad|corazon', 60.4, { tam: 72, y: 970 });
  const tL = en('llegar', 55.2), ch = emoji(e, '✨', 80, tL);
  return (t, w) => { pintarCirc(c1, t, L[0]._t[0] - .2, 670, 580, 270); pintarCirc(c2, t, r._t[0] - .3, 1250, 580, 270); pe(ch, t, tL, 960, 330);
    L.forEach((el, i) => pt(el, t, { x: 670, y: 480 + i * 100 })); pt(m, t); pt(r, t, { x: 1250, y: 580 }); pt(au, t); };
});

/* 10 · no son 3 pasos: son 3 errores */
escena('errores', e => {
  const a = X(e, 'tres pasos', 63.8, { tam: 110, y: 260, gris: true }), b = X(e, 'tres errores|raiz', 64.6, { tam: 110, y: 460 }), tch = tachar(e);
  const q = X(e, 'que las personas cometen', 66.2, { tam: 64, m: true, y: 640 }), c = X(e, 'antes de empezar una marca personal', 68.5, { tam: 64, y: 860 });
  return (t, w) => { pt(a, t); pt(b, t); pt(q, t); pt(c, t); pintarTachar(tch, t, b._t[0] - .1, a); };
});

/* 11 · paso 1: ser honesto con tus miedos */
escena('paso1', e => {
  const p = X(e, 'Paso 1', 71, { tam: 110, y: 170, apartado: true, dice: 'el primer paso de todos' });
  const s0 = X(e, 'ser consciente', 72.8, { tam: 72, y: 330 }), a = X(e, 'ser honesto|garganta', 73.5, { tam: 80, y: 470 }), b = X(e, 'decirte la verdad', 74.6, { tam: 64, y: 600, m: true });
  const c = X(e, 'esos miedos más grandes|raiz', 77.2, { tam: 84, y: 820 });
  return (t, w) => { pt(p, t); pt(s0, t); pt(a, t); pt(b, t); pt(c, t); };
});

/* 12 · salir de tu zona de confort: resistencias, creencias, pensamientos */
escena('zona', e => {
  const z = circ(e, C.corazon), st = stickman(e.svg);
  const a = X(e, 'zona de confort', 88.4, { tam: 60 }), L = [['resistencias', 91.5], ['creencias limitantes|raiz', 92.4], ['pensamientos negativos', 94]].map(([f, d]) => X(e, f, d, { tam: 60, ax: 0 }));
  return (t, w) => { pintarCirc(z, t, w.a - .5, 640, 600, 220); pt(a, t, { x: 640, y: 330 });
    pintarStick(st, t, { x: lerp(640, 760, P(t, a._t[2], .8, E.io3)), y: 790, s: .4, pose: 'camina', t0: w.a - .5 });
    L.forEach((el, i) => pt(el, t, { x: 920, y: 420 + i * 150 })); };
});

/* 13 · te levantas: quiero empezar este proyecto… pero ahí están tus miedos */
escena('manana', e => {
  const st = stickman(e.svg), a = X(e, 'te levantas por la mañana', 96, { tam: 72, y: 170 }), sol = emoji(e, '☀️', 90, a._t[0]);
  const B = [['quiero lograr esto', 97.5, 330], ['quiero empezar este proyecto', 99.5, 520]].map(([f, d, y]) => ({ bo: bocadillo(e, f, ts(f, d), { tam: 60 }), y }));
  const b = X(e, 'todos tus miedos|raiz', 102.5, { tam: 88, y: 960 });
  return (t, w) => { pt(a, t); pe(sol, t, a._t[3], 1530, 170); const s = pintarStick(st, t, { x: 560, y: 860, s: .55, pose: 'pie', t0: w.a - .6 });
    B.forEach(k => pintarBocadillo(k.bo, t, k.bo.tx._t[0] - .2, 1110, k.y, s.cabeza.x + 60, s.cabeza.y)); pt(b, t); };
});

/* 14 · un autoconcepto sobre ti: lo que mereces, lo que eres capaz, lo que puedes ofrecer */
escena('autoconcepto', e => {
  const a = X(e, 'un autoconcepto|ojo', 108, { tam: 96, y: 170 }), so = X(e, 'sobre ti', 109.3, { tam: 64, m: true, gris: true, y: 290 });
  const L = [['lo que tú mereces', 110.5], ['lo que tú eres capaz de crear', 112], ['lo que realmente puedes ofrecer', 114.5]].map(([f, d]) => X(e, f, d, { tam: 64, ax: 0 }));
  const fl3 = L.map(() => flechaE(e, C.ojo));
  return (t, w) => { pt(a, t); pt(so, t); L.forEach((el, i) => { pt(el, t, { x: 520, y: 460 + i * 160 }); pintarFlecha(fl3[i], t, el._t[0] - .15, 380, 460 + i * 160, 470, 460 + i * 160); }); };
});

/* 15 · «lo hago como hobby» → lo pueden monetizar */
escena('hobby', e => {
  const st = stickman(e.svg), bo = bocadillo(e, 'esto lo hago como hobby', ts('esto lo hago como hobby', 129), { tam: 60 });
  const a = X(e, 'lo pueden monetizar|plexo', 132.3, { tam: 76, y: 740, x: 1080 }), m = movil(e.svg), din = emoji(e, '💰', 90, a._t[0]);
  const r = X(e, 'redes sociales', 134.8, { tam: 64, x: 1080, y: 900 });
  return (t, w) => { const s = pintarStick(st, t, { x: 480, y: 940, s: .55, pose: 'pie', t0: w.a - .6 });
    pintarBocadillo(bo, t, bo.tx._t[0] - .2, 960, 330, s.cabeza.x + 40, s.cabeza.y); pt(a, t); pe(din, t, a._t[2], 600, 740);
    pintarMovil(m, t, r._t[0] - .2, 1470, 880, .5); pt(r, t); };
});

/* 16 · primero entiende quién crea ese negocio y qué miedos tiene */
escena('quiencrea', e => {
  const a = X(e, 'quién crea ese negocio', 153.5, { tam: 88, y: 200 }), b = X(e, 'qué miedos tiene|raiz', 156, { tam: 88, y: 950 });
  const st = stickman(e.svg), nube = emoji(e, '😰', 100, b._t[1]);
  return (t, w) => { pt(a, t); pt(b, t); const s = pintarStick(st, t, { x: 960, y: 820, s: .6, pose: 'hundido', t0: w.a - .6 });
    pe(nube, t, b._t[1], s.cabeza.x + 160, s.cabeza.y - 60); };
});

/* 17 · el diálogo interno negativo */
escena('dialogo', e => {
  const st = stickman(e.svg);
  const B = [['no ser suficientemente listo', 171.6], ['o suficientemente válido', 173.6], ['la competencia es mejor que tú', 176], ['un programa mucho mejor', 179.3], ['no te van a comprar', 181.5]].map(([f, d], i) => ({ bo: bocadillo(e, f, ts(f, d), { tam: 56 }), y: 190 + i * 170 }));
  return (t, w) => { const s = pintarStick(st, t, { x: 480, y: 960, s: .55, pose: t > B[4].bo.tx._t[0] ? 'manosCabeza' : t > en('va', 177.3) ? 'sentado' : 'hundido', t0: w.a - .6 });
    B.forEach(k => pintarBocadillo(k.bo, t, k.bo.tx._t[0] - .2, 1080, k.y, s.cabeza.x + 50, s.cabeza.y)); };
});

/* 18 · más tiempo en la cabeza que accionando */
escena('aqui', e => {
  const a = X(e, 'más tiempo aquí|ojo', 197.4, { tam: 80, x: 640, y: 200 }), b = X(e, 'que accionando|plexo', 198.6, { tam: 80, x: 1280, y: 200 });
  const md = medidor(e.svg), c = X(e, 'conectando con quien eres realmente tú', 201, { tam: 64, y: 930 });
  return (t, w) => { pt(a, t); pt(b, t); pt(c, t); pintarMedidor(md, t, w.a - .3, 960, 680, lerp(.15, .85, P(t, c._t[0], 1.2, E.io3)), 1.2); };
});

/* 19 · habla con tu niño interior */
escena('nino', e => {
  const sl = silueta(e.svg), nino = stickman(e.svg), aura = trazo(e.svg, '', { ancho: 6, color: C.corazon });
  const a = X(e, 'tu niño interior|corazon', 206.5, { tam: 80, x: 1150, y: 300 }), b = X(e, 'o esa niña', 208.5, { tam: 60, m: true, x: 1150, y: 420 });
  const c = X(e, 'transmitirle toda esa confianza', 212.5, { tam: 56, x: 1150, y: 680 });
  return (t, w) => { const x = 560, y = 1010, s = .82; pintarSilueta(sl, t, { x, y, s, t0: w.a - .6 }); const cc = centroSil(x, y, s, 'corazon');
    pintarStick(nino, t, { x: cc.x, y: cc.y + 50, s: .14, pose: 'arriba', t0: a._t[1] }); forma(aura, () => circulo(cc.x, cc.y, 60 + 6 * Math.sin(t * 4))); dibujar(aura, dib(t, c._t[0], .4), .8);
    pt(a, t); pt(b, t); pt(c, t); };
});

/* 20 · un chute de energía para hacer lo que sabes que tienes que hacer */
escena('chute', e => {
  const a = X(e, 'un chute de energía|plexo', 225.5, { tam: 96, y: 180 }), ray = emoji(e, '⚡', 110, a._t[0]), st = stickman(e.svg);
  const b = X(e, 'las cosas que sabes', 227.3, { tam: 60, x: 1150, y: 430 }), g2 = X(e, 'que te gustaría lograr', 229.1, { tam: 56, m: true, x: 1150, y: 540 }), b2 = X(e, 'aquello que se te da bien', 230.5, { tam: 60, x: 1150, y: 660 }), c = X(e, 'ponerlo al servicio|corazon', 232.5, { tam: 68, x: 1150, y: 820 });
  return (t, w) => { pt(a, t); pe(ray, t, a._t[3], 700, 420); pintarStick(st, t, { x: 560, y: 960, s: .55, pose: t > a._t[3] ? 'arriba' : 'pie', t0: w.a - .6 }); pt(b, t); pt(g2, t); pt(b2, t); pt(c, t); };
});

/* 21 · nunca es blanco o negro: siempre hay matices */
escena('matices', e => {
  const a = X(e, 'blanco', 237.6, { tam: 96, x: 620, y: 420, gris: true }), b = X(e, 'negro', 238.2, { tam: 96, x: 1300, y: 420 }), c = X(e, 'matices|ojo', 240.5, { tam: 110, y: 760 });
  const f = [flechaE(e, C.ojo), flechaE(e, C.ojo)];
  return (t, w) => { pt(a, t); pt(b, t); pt(c, t); pintarFlecha(f[0], t, c._t[0] - .2, 680, 500, 860, 680); pintarFlecha(f[1], t, c._t[0] - .1, 1240, 500, 1060, 680); };
});

/* 22 · creer que el camino va a ser súper fácil */
escena('facil', e => {
  const a = X(e, 'súper fácil', 249.8, { tam: 110, y: 200, gris: true }), tch = tachar(e), cam = trazo(e.svg, '', { ancho: 8 });
  const b = X(e, 'saber el camino al 100%', 250.8, { tam: 64, y: 900 }), x2 = trazo(e.svg, '', { ancho: 10, color: C.raiz });
  return (t, w) => { pt(a, t); pintarTachar(tch, t, b._t[0], a);
    forma(cam, () => `M450,760 C700,520 800,840 1000,600 S1300,420 1480,560`); dibujar(cam, dib(t, w.a - .3, 1.2)); pt(b, t);
    forma(x2, () => cruz(1480, 560, 1.4)); dibujar(x2, dib(t, b._t[4] + .2, .3)); };
});

/* 23 · el camino se hace al andar */
escena('andar', e => {
  const a = X(e, 'el camino se hace al andar', 260.6, { tam: 84, y: 180 }), st = stickman(e.svg), cam = trazo(e.svg, '', { ancho: 8 });
  const b = X(e, 'tu negocio te acompaña|plexo', 264.5, { tam: 72, y: 950 }), neg = emoji(e, '💼', 90, b._t[1]);
  return (t, w) => { pt(a, t); const k = P(t, a._t[0], 4, E.io3); forma(cam, () => linea(420, 800, lerp(420, 1500, k), 800, 0)); dibujar(cam, 1);
    const s = pintarStick(st, t, { x: lerp(420, 1400, k), y: 800, s: .5, pose: 'camina', t0: w.a - .6 }); pt(b, t); pe(neg, t, b._t[1], s.cadera.x + 130, 700); };
});

/* 24 · no separes tu negocio de quien eres (gastas energía siendo otro) */
escena('separar', e => {
  const a = X(e, 'no tienes que separar tu negocio', 270.2, { tam: 64, y: 160 }), b = X(e, 'de quien eres tú|corazon', 272, { tam: 72, y: 270 });
  const c = X(e, 'gastando energía|raiz', 274, { tam: 64, y: 390 }), cp = X(e, 'de comportarte de una forma', 275, { tam: 56, m: true, y: 500 }), d = X(e, 'con una persona o con otra', 276.5, { tam: 56, y: 990 });
  const s1 = stickman(e.svg), s2 = stickman(e.svg), m1t = en('persona', 276), m2t = en('otra', 277), m1 = emoji(e, '🎭', 80, m1t), m2 = emoji(e, '🎭', 80, m2t);
  return (t, w) => { pt(a, t); pt(b, t); pt(c, t); pt(cp, t); pt(d, t); const p1 = pintarStick(s1, t, { x: 700, y: 900, s: .45, pose: 'pie', t0: w.a - .6 }), p2 = pintarStick(s2, t, { x: 1220, y: 900, s: .45, pose: 'pie', t0: w.a - .4 });
    pe(m1, t, m1t, p1.cabeza.x, p1.cabeza.y); pe(m2, t, m2t, p2.cabeza.x, p2.cabeza.y); };
});

/* 25 · tú eres tú: habilidades, hobbies, miedos, tu don */
escena('eres', e => {
  const a = X(e, 'tú eres tú', 280.5, { tam: 110, y: 540 }), c = circ(e, C.corazon);
  const L = [['tus habilidades', 282, 600, 220], ['tus hobbies', 283.2, 1320, 220], ['tus miedos|raiz', 284.4, 600, 830], ['tu don|corona', 287, 1320, 830]].map(([f, d, x, y]) => ({ el: X(e, f, d, { tam: 64 }), x, y }));
  const ay = X(e, 'tu capacidad de ayudar', 285.2, { tam: 56, m: true, y: 980 });
  return (t, w) => { pt(a, t); pintarCirc(c, t, a._t[0] - .1, 960, 540, 200); L.forEach(k => pt(k.el, t, { x: k.x, y: k.y })); pt(ay, t); };
});

/* 26 · paso 2: un problema, un cliente, con tus palabras */
escena('paso2', e => {
  const p = X(e, 'Paso 2', 304, { tam: 110, y: 170, apartado: true, dice: 'el paso número dos' });
  const b1 = X(e, 'todo el mundo', 305.4, { tam: 60, m: true, gris: true, x: 720, y: 300 }), b2 = X(e, 'hace mal|raiz', 308.2, { tam: 72, x: 1180, y: 300 }), s0 = X(e, 'solamente hablar de', 308.9, { tam: 56, m: true, y: 420 });
  const L = [['un problema|garganta', 309.6], ['a un cliente', 311], ['con tus palabras|corazon', 312.2]].map(([f, d]) => X(e, f, d, { tam: 80 }));
  return (t, w) => { pt(p, t); pt(b1, t); pt(b2, t); pt(s0, t); L.forEach((el, i) => pt(el, t, { y: 560 + i * 150 })); };
});

/* 27 · 50 gustos diferentes → no te diferencias */
escena('gustos', e => {
  const a = X(e, '50 gustos diferentes', 324.3, { tam: 96, y: 170 }), ems = ['⛵', '🎸', '⚽', '🍳', '📚', '🎮', '🧘', '📷'].map(ch => emoji(e, ch, 80, 0));
  const hb = X(e, 'y hablas de esos 50 gustos', 327.3, { tam: 56, m: true, y: 610 }), v = X(e, 'nada que ver unos con otros', 329.5, { tam: 60, y: 710 }), xg = trazo(e.svg, '', { ancho: 10, color: C.raiz }), tP = en('personal', 331);
  const b = X(e, 'no te vas a clasificar en ninguna parte', 332, { tam: 60, y: 830 }), c = X(e, 'muy difícil que te diferencies|raiz', 336.2, { tam: 68, y: 960 });
  return (t, w) => { pt(a, t); ems.forEach((m, i) => pe(m, t, w.a - .3 + i * .35, 520 + (i % 4) * 300, 350 + Math.floor(i / 4) * 170, 1 - .6 * P(t, b._t[0], .6))); forma(xg, () => cruz(960, 430, 4)); dibujar(xg, dib(t, tP, .4)); pt(hb, t); pt(v, t); pt(b, t); pt(c, t); };
});

/* 28 · haz un filtro: un solo problema para un solo cliente */
escena('filtro', e => {
  const emb = trazo(e.svg, '', { ancho: 8 }), a = X(e, 'hacer un filtro', 362.8, { tam: 84, y: 170 });
  const b = X(e, 'un solo problema|garganta', 366, { tam: 72, y: 820 }), c = X(e, 'para un solo cliente', 367.6, { tam: 72, y: 950 });
  const go = [0, 1, 2, 3, 4].map(() => trazo(e.svg, '', { ancho: 7, color: C.ojo }));
  return (t, w) => { pt(a, t); forma(emb, () => `M650,300 L1270,300 L1010,560 L1010,700 L910,700 L910,560 Z`); dibujar(emb, dib(t, a._t[2], .6));
    go.forEach((g, i) => { const k = (t * .7 + i * .2) % 1, x = lerp(720 + i * 120, 960, k), y = lerp(330, 680, k); forma(g, () => circulo(x, y, 14)); dibujar(g, dib(t, a._t[2] + .3 + i * .1, .2), 1 - k * .7); });
    pt(b, t); pt(c, t); };
});

/* 29 · dos mundos que se pueden unir */
escena('dosmundos', e => {
  const A = [['crecimiento personal', 379.4], ['conciencia', 380.8], ['energía', 382.4], ['espiritualidad|corona', 382.9]].map(([f, d]) => X(e, f, d, { tam: 56 }));
  const hab = X(e, 'las habilidades', 383.6, { tam: 56, x: 1260, y: 270 });
  const B = [['crear marca personal', 385.6], ['hacer los vídeos', 386.6], ['saber comunicar|garganta', 387.6]].map(([f, d]) => X(e, f, d, { tam: 56 }));
  const c = X(e, 'son dos mundos que se pueden unir', 390.5, { tam: 72, y: 950 }), cajas = [trazo(e.svg, '', { ancho: 7, color: C.corona }), trazo(e.svg, '', { ancho: 7, color: C.garganta })];
  const f1 = flechaE(e, C.corazon), tI = en('importante', 389);
  return (t, w) => { forma(cajas[0], () => caja(350, 200, 600, 580)); dibujar(cajas[0], dib(t, w.a - .4, .5)); forma(cajas[1], () => caja(970, 200, 600, 580)); dibujar(cajas[1], dib(t, hab._t[0] - .3, .5));
    A.forEach((el, i) => pt(el, t, { x: 650, y: 300 + i * 130 })); pt(hab, t, { x: 1270 }); B.forEach((el, i) => pt(el, t, { x: 1270, y: 420 + i * 120 }));
    pintarFlecha(f1, t, tI, 760, 830, 1160, 830); pt(c, t); };
});

/* 30 · si me gustasen los barcos… */
escena('barcos', e => {
  const a = X(e, 'me gustasen los barcos', 400.4, { tam: 84, y: 200 }), bar = emoji(e, '⛵', 150, a._t[3]);
  const b = X(e, 'muy difícil', 402.5, { tam: 68, y: 700, gris: true }), q = X(e, 'que yo complementara', 404.3, { tam: 60, m: true, y: 810 }), c = X(e, 'con mi marca personal|garganta', 407.3, { tam: 64, y: 930 }), x = trazo(e.svg, '', { ancho: 10, color: C.raiz }), ln = trazo(e.svg, '', { ancho: 6, color: GRIS }), tG = en('gusten', 404.5);
  return (t, w) => { pt(a, t); pe(bar, t, a._t[3], 960, 450); forma(ln, () => linea(1040, 440, 1080, 420, 0)); dibujar(ln, dib(t, tG, .5)); pt(b, t); pt(q, t); pt(c, t); forma(x, () => cruz(1120, 400, 1.3)); dibujar(x, dib(t, c._t[0], .3)); };
});

/* 31 · mi foco: la gente que quiere crear su marca personal con su autenticidad */
escena('enfoque', e => {
  const dd = [0, 1, 2].map(() => trazo(e.svg, '', { ancho: 7, color: C.corazon }));
  const a = X(e, 'no me estoy enfocando', 421.5, { tam: 64, y: 150, gris: true }), a2 = X(e, 'en hacer contenido', 422.6, { tam: 56, m: true, y: 250 });
  const tB = en('barcos', 424.5), bar = emoji(e, '⛵', 90, tB), q = X(e, 'me quiero enfocar|corazon', 425.4, { tam: 64, y: 350 });
  const b = X(e, 'la gente que quiere crear su marca personal', 426, { tam: 56, y: 880 }), c = X(e, 'con su autenticidad|corazon', 429.5, { tam: 64, y: 980 });
  return (t, w) => { pt(a, t); pt(a2, t); pt(q, t); dd.forEach((k, i) => { forma(k, () => circulo(960, 620, 200 * (1 - i * .33))); dibujar(k, dib(t, q._t[0] + i * .12, .4)); });
    pe(bar, t, tB, 1450, 620, 1 - .7 * P(t, b._t[0], .5)); pt(b, t); pt(c, t); };
});

/* 32 · lo que se te da bien, no lo que te gustaría hablar */
escena('bien', e => {
  const tit = X(e, 'qué es lo que realmente', 436.2, { tam: 64, m: true, gris: true, y: 200 });
  const a = filaLista(e, 'lo que se te da bien', en('se', 437.5), { tam: 72 }), b = filaLista(e, 'lo que te gustaría hablar', en('gustaría', 440), { tam: 72, no: true });
  const mk = trazo(e.svg, '', { ancho: 7, color: C.corazon }), tN = en('no', 443.3), im = X(e, 'esto es muy importante', 442, { tam: 60, m: true, y: 840 }), sp = X(e, 'eso es el siguiente paso', 444.3, { tam: 56, gris: true, y: 960 });
  return (t, w) => { pt(tit, t); pintarFila(a, t, 520, 420); pintarFila(b, t, 520, 640); forma(mk, () => caja(470, 350, 980, 140)); dibujar(mk, dib(t, tN, .5)); pt(im, t, { s: 1 + .03 * Math.sin(t * 4) * P(t, im._t[0], .3) }); pt(sp, t); };
});

/* 33 · muy densas, muy difíciles de entender */
escena('densas', e => {
  const L = [['muy densas', 471.8], ['muy difíciles de entender', 472.8], ['tanta información', 475]].map(([f, d]) => X(e, f, d, { tam: 64, ax: 0 }));
  const bum = emoji(e, '🤯', 130, L[2]._t[0]), pila = [0, 1, 2, 3].map(() => trazo(e.svg, '', { ancho: 6, fill: '#fff' }));
  return (t, w) => { L.forEach((el, i) => pt(el, t, { x: 780, y: 360 + i * 170 })); pila.forEach((p, i) => { forma(p, () => cajaR(400 + i * 10, 640 - i * 70, 300, 60, 10)); dibujar(p, dib(t, w.a - .4 + i * .15, .3)); }); pe(bum, t, L[2]._t[0], 550, 330); };
});

/* 34 · como una conversación de barra de bar */
escena('bar', e => {
  const a = X(e, 'barra de bar', 486.5, { tam: 110, y: 330 }), cer = emoji(e, '🍺', 120, a._t[0]);
  const b = X(e, 'de barrio', 487.6, { tam: 64, x: 760, y: 700, m: true }), c = X(e, 'de andar por casa', 488.6, { tam: 64, x: 1220, y: 700, m: true });
  return (t, w) => { pt(a, t); pe(cer, t, a._t[0], 960, 500); pt(b, t); pt(c, t); };
});

/* 35 · detecta el problema de tu cliente y soluciónalo con tus palabras */
escena('detectar', e => {
  const lupa = emoji(e, '🔍', 150, 0), a = X(e, 'el problema que tiene ese cliente|raiz', 501.5, { tam: 64, y: 600 });
  const so = X(e, 'cómo tú lo solucionas', 503.5, { tam: 64, m: true, y: 760 }), b = X(e, 'con tus palabras|corazon', 505.6, { tam: 84, y: 900 });
  return (t, w) => { pe(lupa, t, w.a - .3, 960 + 120 * Math.sin(t * 1.2), 330); pt(a, t); pt(so, t); pt(b, t); };
});

/* 36 · sin tantos guiones: una idea, un vídeo */
escena('guiones', e => {
  const a = X(e, 'tantos guiones preparados', 517.9, { tam: 72, y: 200, gris: true }), tch = tachar(e), hojas = [0, 1, 2].map(() => trazo(e.svg, '', { ancho: 6, fill: '#fff' }));
  const b = X(e, 'una idea|plexo', 520.5, { tam: 96, x: 620, y: 720 }), c = X(e, 'un vídeo|garganta', 522.4, { tam: 96, x: 1300, y: 720 }), f = flechaE(e);
  return (t, w) => { pt(a, t); hojas.forEach((h, i) => { forma(h, () => cajaR(780 + i * 40, 280 + i * 30, 220, 280, 12)); dibujar(h, dib(t, w.a - .3 + i * .12, .3), 1 - .8 * P(t, b._t[0], .4)); });
    pintarTachar(tch, t, b._t[0] - .2, a); pt(b, t); pt(c, t); pintarFlecha(f, t, c._t[0] - .2, 870, 720, 1050, 720); };
});

/* 37 · nunca te va a faltar negocio */
escena('negocio', e => {
  const a = X(e, 'nunca te va a faltar negocio|plexo', 544, { tam: 96, y: 540 }), din = emoji(e, '💼', 110, a._t[0]);
  return (t, w) => { pt(a, t, { s: 1 + .05 * P(t, a._t[4], .3) }); pe(din, t, a._t[0], 960, 340); };
});

/* 38 · pensamos que no somos suficientes y abrimos el abanico */
escena('abanico', e => {
  const a = X(e, 'no somos suficientemente buenos|raiz', 550, { tam: 72, y: 170 }), ac = X(e, 'en algo concreto', 553, { tam: 56, m: true, y: 280 }), dn = X(e, 'no vamos a generar suficiente dinero|plexo', 554.2, { tam: 60, y: 390 }), b = X(e, 'abrimos el abanico', 557, { tam: 84, y: 960 });
  const ab = [0, 1, 2, 3, 4, 5, 6].map(() => trazo(e.svg, '', { ancho: 7, color: C.ojo })), st = stickman(e.svg);
  return (t, w) => { pt(a, t); pt(ac, t); pt(dn, t); pt(b, t); pintarStick(st, t, { x: 960, y: 850, s: .45, pose: 'hundido', t0: w.a - .6 });
    ab.forEach((l, i) => { const ang = -Math.PI / 2 + (i - 3) * .32 * P(t, b._t[0], .6, E.out3); forma(l, () => linea(960, 610, 960 + 160 * Math.cos(ang), 610 + 160 * Math.sin(ang), 0)); dibujar(l, dib(t, b._t[0] - .2, .3)); }); };
});

/* 39 · cientos de canales: Minecraft, Clash Royale, automatización de YouTube */
escena('canales', e => {
  const ar = circ(e, '#FF0033'), yt = logoYT(e.svg), a = X(e, '800 canales', 569, { tam: 96, x: 860, y: 190 }), b = X(e, 'mil vídeos', 570.5, { tam: 64, m: true, x: 860, y: 300 }), hc = X(e, 'hablando a cámara', 571.9, { tam: 56, m: true, x: 860, y: 390 });
  const L = [['Minecraft', 574.5, '⛏️'], ['Clash Royale', 576.8, '👑'], ['automatización de YouTube', 578.2, '🤖']].map(([f, d, ch]) => ({ el: X(e, f, d, { tam: 64, ax: 0 }), em: emoji(e, ch, 80, en(f.split(' ')[0], d)) }));
  const q = X(e, '15 años', 575.4, { tam: 56, gris: true, x: 1250, y: 540 });
  return (t, w) => { pintarCirc(ar, t, w.a - .6, 1400, 200, 95); pintarLogo(yt, t, w.a - .6, 1400, 200, 1); pt(a, t); pt(b, t); pt(hc, t); pt(q, t); L.forEach((k, i) => { pe(k.em, t, k.el._t[0], 520, 540 + i * 150); pt(k.el, t, { x: 610, y: 540 + i * 150 }); }); };
});

/* 40 · a quién le vendo y qué vendo (no a este, a este, a este…) */
escena('vendo', e => {
  const a = X(e, 'a quien le vendo', 602.7, { tam: 80, x: 700, y: 180 }), b = X(e, 'y qué vendo', 604, { tam: 80, x: 1290, y: 180 });
  const g = [0, 1, 2, 3].map(() => stickman(e.svg)), xs = [0, 1, 2, 3].map(() => trazo(e.svg, '', { ancho: 9, color: C.raiz })), tA = en('este', 605);
  return (t, w) => { pt(a, t); pt(b, t); g.forEach((s, i) => { const st = pintarStick(s, t, { x: 560 + i * 270, y: 900, s: .45, pose: 'pie', t0: tA - .3 + i * .35 });
    forma(xs[i], () => cruz(st.cabeza.x, st.cabeza.y - 80, 1)); dibujar(xs[i], dib(t, tA + i * .35 + .2, .2)); }); };
});

/* 41 · en todos los lados y en ningún lado */
escena('ningun', e => {
  const st = stickman(e.svg), fs = [0, 1, 2, 3, 4, 5].map(() => flechaE(e, C.raiz));
  const a = X(e, 'en todos los lados', 612.1, { tam: 80, y: 180 }), b = X(e, 'en ningún lado|raiz', 614.3, { tam: 96, y: 960 });
  return (t, w) => { pt(a, t); pt(b, t); const s = pintarStick(st, t, { x: 960, y: 820, s: .5, pose: 'manosCabeza', t0: w.a - .5 });
    fs.forEach((f, i) => { const ang = i * Math.PI / 3, x1 = 960 + 140 * Math.cos(ang), y1 = 600 + 140 * Math.sin(ang); pintarFlecha(f, t, a._t[0] + i * .12, x1, y1, 960 + 360 * Math.cos(ang), 600 + 300 * Math.sin(ang)); }); };
});

/* 42 · paso 3: publica lo que piensas aunque incomode */
escena('paso3', e => {
  const p = X(e, 'Paso 3', 625, { tam: 110, y: 170, apartado: true, dice: 'el último paso' });
  const u = X(e, 'una de las cosas que veo', 625.9, { tam: 56, m: true, gris: true, y: 300 }), r = X(e, 'mucha reticencia', 628.4, { tam: 64, y: 400 }), a = X(e, 'publicar realmente lo que tú piensas|garganta', 629.5, { tam: 60, y: 520 });
  const L = [['aunque incomode', 633], ['aunque te ganes hate|raiz', 634.5]].map(([f, d]) => X(e, f, d, { tam: 72 })), en1 = emoji(e, '😡', 90, L[1]._t[0]);
  return (t, w) => { pt(p, t); pt(u, t); pt(r, t); pt(a, t); L.forEach((el, i) => pt(el, t, { y: 680 + i * 150 })); pe(en1, t, L[1]._t[0], 1480, 830); };
});

/* 43 · «es la nueva moda… no tengo ni idea, pero la voy a hacer» */
escena('moda', e => {
  const st = stickman(e.svg), a = X(e, 'la nueva moda', 659.8, { tam: 96, y: 180 }), fu = emoji(e, '🔥', 100, a._t[0]);
  const bo = bocadillo(e, 'no tengo ni puta idea', ts('no tengo ni puta idea', 660.5), { tam: 60 }), c = X(e, 'pero la voy a hacer', 664, { tam: 64, x: 1220, y: 760 });
  return (t, w) => { pt(a, t); pe(fu, t, a._t[2], 1360, 180); const s = pintarStick(st, t, { x: 600, y: 960, s: .55, pose: 'movil', t0: w.a - .6 });
    pintarBocadillo(bo, t, bo.tx._t[0] - .2, 1200, 470, s.cabeza.x + 40, s.cabeza.y); pt(c, t); };
});

/* 44 · vender cursos de trading que no practicas */
escena('trading', e => {
  const a = X(e, 'vender cursos de trading', 666.4, { tam: 88, y: 190 }), gr = emoji(e, '📈', 130, a._t[0]);
  const b = X(e, 'que yo no practico', 668.2, { tam: 64, y: 690, gris: true }), id = X(e, 'no tengo ni puta idea', 669.6, { tam: 60, m: true, y: 790 }), vv = X(e, 'lo voy a vender', 671, { tam: 56, y: 880 }), c = X(e, 'puedo ganar dinero|plexo', 672.6, { tam: 64, y: 980 }), x = trazo(e.svg, '', { ancho: 11, color: C.raiz });
  return (t, w) => { pt(a, t); pe(gr, t, a._t[1], 960, 450); pt(b, t); pt(id, t); pt(vv, t); pt(c, t); forma(x, () => cruz(960, 450, 2.4)); dibujar(x, dib(t, b._t[2], .3)); };
});

/* 45 · críticas: constructivas para crecer, por criticar para entrenarte */
escena('criticas', e => {
  const a = X(e, 'crítica constructiva', 688.1, { tam: 60, x: 650, y: 240 }), b = X(e, 'para crecer|corazon', 690.7, { tam: 64, x: 650, y: 400 });
  const c = X(e, 'crítica por criticar', 691.9, { tam: 60, x: 1270, y: 240 }), tb = X(e, 'también te va a servir', 693, { tam: 56, m: true, x: 1270, y: 400 }), d = X(e, 'para entrenarte|plexo', 694.5, { tam: 64, x: 1270, y: 530 });
  const f = [flechaE(e), flechaE(e)], z = X(e, 'que no te afecten las críticas', 696.5, { tam: 60, y: 820 });
  return (t, w) => { [a, b, c, tb, d, z].forEach(el => pt(el, t)); pintarFlecha(f[0], t, b._t[0] - .2, 650, 285, 650, 350); pintarFlecha(f[1], t, tb._t[0] - .2, 1270, 285, 1270, 350); };
});

/* 46 · te gusta, perfecto; no te gusta, perfecto también */
escena('perfecto', e => {
  const ln = trazo(e.svg, '', { ancho: 7, color: C.corazon }), a = X(e, 'te gusta perfecto', 734, { tam: 76, y: 360 }), b = X(e, 'no te gusta perfecto también', 735.4, { tam: 72, y: 600 });
  const u1 = emoji(e, '👍', 90, a._t[2]), u2 = emoji(e, '🤷', 90, b._t[3]);
  return (t, w) => { forma(ln, () => linea(560, 480, 1360, 480, 0)); dibujar(ln, dib(t, w.a - .6, .4)); pt(a, t); pt(b, t); pe(u1, t, a._t[2], 1480, 360); pe(u2, t, b._t[3], 1540, 600); };
});

/* 47 · si tu intención es buena, ¿qué más te da? */
escena('intencion', e => {
  const a = X(e, 'tu intención es buena|corazon', 758, { tam: 84, y: 180 }), si = X(e, 'si tu intención es buena', 759.7, { tam: 56, m: true, gris: true, y: 290 }), cor = emoji(e, '❤️', 120, a._t[0]);
  const b = X(e, 'qué más te da lo que te digan', 760.5, { tam: 64, y: 760 }), c = X(e, 'lo que gana es tu intención', 763.2, { tam: 72, y: 920 });
  return (t, w) => { pt(a, t); pt(si, t); pe(cor, t, a._t[3], 960, 500); pt(b, t); pt(c, t); };
});

/* 48 · aunque te pongan los cuernos: tu paz no te la quita nadie */
escena('cuernos', e => {
  const s1 = stickman(e.svg), s2 = stickman(e.svg), tC = en('cuernos', 768), roto = emoji(e, '💔', 100, tC);
  const a = X(e, 'has hecho las cosas que tenías que hacer', 769.6, { tam: 56, y: 170 }), ok = trazo(e.svg, '', { ancho: 10, color: C.corazon });
  const f1 = X(e, 'ha sido fiel', 771.4, { tam: 60, y: 860 }), di = X(e, 'da igual', 773.5, { tam: 60, x: 1380, y: 860 }), yh = X(e, 'yo he hecho lo que tenía que hacer', 779.5, { tam: 56, m: true, y: 300 }), dl = X(e, 'te podrá doler más o doler menos', 775.5, { tam: 56, m: true, y: 980 });
  const b = X(e, 'esa paz tuya interior|corazon', 778, { tam: 76, y: 860 }), sn = X(e, 'lo que yo sentía', 781, { tam: 56, m: true, gris: true, x: 1400, y: 600 }), c = X(e, 'nadie te lo va a poder quitar', 782.6, { tam: 60, y: 980 });
  return (t, w) => { pt(a, t); const p1 = pintarStick(s1, t, { x: 760, y: 700, s: .45, pose: 'pie', t0: w.a - .6 }), p2 = pintarStick(s2, t, { x: 1160, y: 700, s: .45, pose: 'pie', t0: w.a - .4 });
    pe(roto, t, tC, 960, 440); forma(ok, () => tick(p1.cabeza.x, p1.cabeza.y - 90, 1.3)); dibujar(ok, dib(t, a._t[2], .3));
    pt(f1, t, { o: 1 - P(t, b._t[0] - .3, .25) }); pt(di, t, { o: 1 - P(t, b._t[0] - .3, .25) }); pt(yh, t); pt(dl, t, { o: 1 - P(t, c._t[0] - .3, .25) }); pt(b, t); pt(sn, t); pt(c, t); };
});

/* 49 · muy espiritual y respeto a quien no lo es */
escena('espiritual', e => {
  const cc = circ(e, C.corona), a = X(e, 'muy espiritual|corona', 802.3, { tam: 96, x: 700, y: 360 }), est = emoji(e, '✨', 90, a._t[1]);
  const b = X(e, 'respeto', 803.6, { tam: 72, y: 600 }), c = X(e, 'a las personas que no son espirituales', 804.6, { tam: 60, y: 760 });
  return (t, w) => { pintarCirc(cc, t, w.a - .6, 1220, 360, 90); pt(a, t); pe(est, t, a._t[1], 1220, 360); pt(b, t); pt(c, t); };
});

/* 50 · te pones una máscara para que no te critiquen */
escena('mascara', e => {
  const st = stickman(e.svg), mk2 = emoji(e, '🎭', 110, en('máscara', 837)), a = X(e, 'te pones una máscara|raiz', 836.9, { tam: 72, x: 1120, y: 420 }), b = X(e, 'para que no te critiquen', 838.4, { tam: 60, x: 1120, y: 570 });
  return (t, w) => { const s = pintarStick(st, t, { x: 560, y: 940, s: .6, pose: 'pie', t0: w.a - .5 }); pe(mk2, t, a._t[3], s.cabeza.x, s.cabeza.y); pt(a, t); pt(b, t); };
});

/* 51 · la etiqueta: a quién vendo, qué vendo, cómo lo empaqueto */
escena('etiqueta', e => {
  const et = trazo(e.svg, '', { ancho: 8, color: C.plexo, fill: '#fff' });
  const L = [['a quién le vendo', 864.2, 'a quién coño le vendo'], ['qué vendo', 866.1, 'qué coño vendo'], ['lo que a mí se me da bien', 868, null], ['lo que yo sé explicar', 869.5, null], ['cómo lo empaqueto', 871.3, 'cómo coño lo empaqueto']].map(([f, d, dice]) => X(e, f, d, dice ? { tam: 64, dice } : { tam: 56, m: true }));
  const caja2 = emoji(e, '📦', 100, L[4]._t[0]);
  return (t, w) => { forma(et, () => `M520,220 L1300,220 L1420,540 L1300,860 L520,860 Z`); dibujar(et, dib(t, w.a - .4, .6)); L.forEach((el, i) => pt(el, t, { x: 900, y: 300 + i * 120 })); pe(caja2, t, L[4]._t[0], 1330, 540); };
});

/* 52 · cuando lo tienes claro, el contenido sale solo */
escena('solo', e => {
  const a = X(e, 'el contenido va a salir solo|plexo', 880.2, { tam: 76, y: 170 }), cl = X(e, 'si tú tienes claro lo que ofreces', 882, { tam: 56, m: true, gris: true, y: 290 });
  const L = [['a quién se lo ofreces', 884.5], ['y qué ofreces', 886.2], ['qué vídeos hacer|garganta', 888.3]].map(([f, d]) => filaLista(e, f, en(f.split(' ')[0].replace(/\|.*/, ''), d), { tam: 64 }));
  return (t, w) => { pt(a, t); pt(cl, t); L.forEach((f, i) => pintarFila(f, t, 560, 460 + i * 160)); };
});

/* 53 · solo tengo tres pautas */
escena('pautas', e => {
  const a = X(e, 'tres pautas', 901.9, { tam: 110, y: 300 }), nota = emoji(e, '📝', 110, a._t[0]), ls = [0, 1, 2].map(() => trazo(e.svg, '', { ancho: 8 }));
  return (t, w) => { pt(a, t); pe(nota, t, a._t[0], 1400, 300); ls.forEach((l, i) => { forma(l, () => linea(640, 560 + i * 120, 1280 - i * 80, 560 + i * 120, 0)); dibujar(l, dib(t, a._t[1] + .2 + i * .3, .4)); }); };
});

/* 54 · cuanto más auténtico, más te critican (por envidia, por miedo) */
escena('envidia', e => {
  const a = X(e, 'cuando tú eres auténtico|corazon', 953.5, { tam: 76, y: 160 }), st = stickman(e.svg), otros = [0, 1, 2].map(() => stickman(e.svg));
  const L = [['por envidia', 955.8], ['quiere ser auténtico', 959.5], ['decir lo que realmente piensa', 960.4], ['muchos no lo dicen', 962], ['tienen miedo|raiz', 963.6], ['lo critican', 964.6]].map(([f, d]) => X(e, f, d, { tam: 56 }));
  return (t, w) => { pt(a, t); pintarStick(st, t, { x: 520, y: 960, s: .55, pose: 'arriba', t0: w.a - .6 });
    otros.forEach((s, i) => pintarStick(s, t, { x: 740 + i * 100, y: 960, s: .3, pose: t > L[5]._t[0] ? 'señala' : 'pie', t0: L[0]._t[0] - .3 + i * .1 })); L.forEach((el, i) => pt(el, t, { x: 1220, y: 280 + i * 125 })); };
});

/* =========================== motor de la escena =========================== */
const CAMK = norm([[0, { x: CX, y: CY, s: 1 }]]);
function layout() {}
function estadoVideo(t) { const anim = enAnim(t); return { fondo: anim ? 1 : 0, persona: anim ? 0 : 1, halo: 0 }; }
const FONDOK = norm([[0, { vel: 26, brillo: 1 }]]);
const ESPACIO = null;
function render(t) {
  const cam = camara(t), s = cam.s * deriva(t), dx = -(cam.x - CX) * s, dy = -(cam.y - CY) * s;
  WORLD.style.transform = WORLDF.style.transform = `translate(${dx.toFixed(2)}px,${dy.toFixed(2)}px) scale(${s.toFixed(5)})`;
  pintarCapas(t, estadoVideo(t));
  pintarEscenas(t);
}
