/* =====================================================================
   ESCENAS — «Regula tu dopamina y cambiarás». Usa herramientas/pizarra/libreria.js.
   Cada escena = una ventana de edicion/montaje.json (ventanas.py). Los tiempos salen de la voz con ts()/X()/en().
   Stickman para dar contexto; silueta grande solo para energía y cuerpo. Revisar con herramientas/pizarra/revisar.mjs.
   ===================================================================== */
const tarjetaVideo = (g, x, y, w, h) => trazo(g, cajaR(x - w / 2, y - h / 2, w, h, 18), { ancho: 6, fill: '#fff' });
const play = (g, x, y, r = 26) => trazo(g, `M${x - r * .5},${y - r * .7} L${x - r * .5},${y + r * .7} L${x + r * .7},${y} Z`, { ancho: 6, color: C.raiz, fill: C.raiz });
const fadeIn = (t, t0, d = .3) => P(t, t0 - .05, d, E.out3);
const ceja = (e, txt, color = NEGRO) => { const c = mk('div', 'ceja', e.div, txt); c.style.color = color; return c; };
const pintarCeja = (c, t, t0, x, y) => { c.style.opacity = fadeIn(t, t0); c.style.transform = `translate(${x}px,${y}px) translate(-50%,-50%)`; };

/* 1 · INFO (gancho): tu problema no es de información */
escena('info', e => {
  const a = X(e, 'tu problema', 2.2, { tam: 96, y: 250 }), b = X(e, 'no es de información|ojo', 2.6, { tam: 104, y: 380 });
  const tj = [0, 1, 2].map(() => ({ c: tarjetaVideo(e.svg, 0, 0, 300, 190), p: play(e.svg, 0, 0) }));
  const x = trazo(e.svg, '', { ancho: 14, color: C.raiz, k: 'marca' }), tx = en('información', 3.0);
  suena(tx + .35, 'descarte', .4);
  return (t, w) => {
    pt(a, t); pt(b, t);
    tj.forEach((k, i) => { const xx = 960 + (i - 1) * 360, yy = 740 + (i === 1 ? -20 : 10) + 8 * Math.sin(t * 2 + i);
      k.c.setAttribute('transform', `translate(${xx},${yy}) rotate(${(i - 1) * 4})`); k.p.setAttribute('transform', `translate(${xx},${yy})`);
      dibujar(k.c, dib(t, w.a - .7 + i * .12, .4)); dibujar(k.p, dib(t, w.a - .4 + i * .12, .2)); });
    forma(x, () => cruz(960, 720, 7)); dibujar(x, dib(t, tx + .35, .3));
  };
});

/* 2 · VÍDEOS: en el sofá con el móvil, le llegan vídeos de energía sexual, retención, transmutación */
escena('videos', e => {
  const so = sofa(e.svg), f = stickman(e.svg), mv = movilMano(e);
  const tit = X(e, 'constantemente viendo vídeos', 6.5, { tam: 84, y: 150 });
  const temas = [['Energía sexual|sacro', 'sexual'], ['Retención|sacro', 'retención'], ['Transmutación|sacro', 'transmutación']].map(([n, p]) => {
    const t0 = en(p, 7.71); return { t0, c: tarjetaVideo(e.svg, 0, 0, 560, 130), p: play(e.svg, 0, 0, 22), tx: texto(e, n, t0, { tam: 60, ax: 0 }) }; });
  return (t, w) => {
    pintarSofa(so, t, w.a - .8, 620, 960, .78);
    const st = pintarStick(f, t, { x: 620, y: 960, s: .78, pose: 'sentadoMovil', t0: w.a - .7 }); pintarMovilMano(mv, t, w.a - .3, st.manoD, .9);
    pt(tit, t);
    temas.forEach((k, i) => { const y = 400 + i * 175, p = P(t, k.t0 - .1, .4, E.back), x = 1330 + (1 - p) * 60;
      k.c.setAttribute('transform', `translate(${x},${y})`); k.p.setAttribute('transform', `translate(${x - 220},${y})`);
      dibujar(k.c, dib(t, k.t0 - .1, .3)); dibujar(k.p, dib(t, k.t0, .2)); pt(k.tx, t, { x: x - 175, y, o: clamp(p * 2) }); });
  };
});

/* 3 · BUCLE: un vídeo más… y el contador sube sin parar */
escena('bucle', e => {
  const lp = trazo(e.svg, bucle(960, 520, 330), { ancho: 9, color: C.sacro });
  const tx = X(e, 'un vídeo más|sacro', 16.88, { tam: 120, y: 500 });
  const t1 = en('más', 17.38), t2 = en('información', 18.38);
  const cont = texto(e, 'vídeo nº 1', t1, { tam: 64, m: true, gris: true, y: 640 });
  return (t, w) => {
    dibujar(lp, dib(t, w.a - .7, .9)); lp.setAttribute('transform', `rotate(${((t - w.a) * 40).toFixed(1)} 960 520)`);
    pt(tx, t);
    cont._sp[2].textContent = t < t1 ? 1 : Math.round(1 + 799 * P(t, t1, t2 + .6 - t1, E.io3)); pt(cont, t);
  };
});

/* 4 · SALIR: «en este vídeo»: 1 · salir del bucle (sale del círculo caminando) */
escena('salir', e => {
  const cj = ceja(e, 'EN ESTE VÍDEO', C.corazon), lp = trazo(e.svg, bucle(720, 720, 190), { ancho: 8, color: C.sacro }), f = stickman(e.svg);
  const n1 = X(e, '1', 24.1, { dice: 'primero', tam: 120, x: 520, y: 260 }), tit = X(e, 'Salir del bucle|ok', 24.1, { dice: 'salir de ese bucle', tam: 104, x: 620, y: 260, ax: 0 });
  const ts0 = en('salir', 24.1);
  suena(ts0, 'barrido', .3);
  return (t, w) => {
    pintarCeja(cj, t, w.a - .7, 960, 140); pt(n1, t); pt(tit, t);
    dibujar(lp, dib(t, w.a - .7, .6), 1 - .6 * P(t, ts0, 1)); lp.setAttribute('transform', `rotate(${((t - w.a) * 30).toFixed(1)} 720 720)`);
    const k = P(t, ts0, 1.6, E.io3), paso = Math.sin((t - ts0) * 9) * (k > 0 && k < 1);
    pintarStick(f, t, { x: lerp(720, 1300, k), y: 960, s: .62, pose: { ...POSES.camina, pI: 6 + 16 * paso, pD: 6 - 16 * paso, bI: 10 - 20 * paso, bD: 10 + 20 * paso }, t0: w.a - .7 });
  };
});

/* 5 · TRANSFORMA: 2 · transformar tu vida — la energía a tu favor (silueta: energía) */
escena('transforma', e => {
  const sl = silueta(e.svg), rayos = [0, 1, 2, 3, 4, 5, 6].map(() => trazo(e.svg, '', { ancho: 7, color: C.plexo })), pto = trazo(e.svg, '', { ancho: 12, color: C.plexo });
  const n2 = X(e, '2', 27.34, { dice: 'segundo', tam: 120, x: 520, y: 200 }), tit = X(e, 'Transformar tu vida|plexo', 27.74, { dice: 'transformar tu vida', tam: 104, x: 620, y: 200, ax: 0 });
  const en0 = en('energía', 30.54), lab = X(e, 'la energía|plexo a tu favor', 30.54, { dice: 'esa energía a tu favor', tam: 72, x: 1320, y: 640 });
  const ent = X(e, 'entiende qué pasa', 30.2, { dice: 'entendiendo qué es lo que está pasando', tam: 64, m: true, x: 1320, y: 500 });
  suena(en0, 'swell', .3);
  return (t, w) => {
    pt(n2, t); pt(tit, t); pt(lab, t); pt(ent, t);
    const x = 760, y = 1040, s = .95; pintarSilueta(sl, t, { x, y, s, t0: w.a - .7 });
    const c = centroSil(x, y, s, 'plexo'); forma(pto, () => circulo(c.x, c.y, 9)); dibujar(pto, dib(t, w.a + .3, .3));
    rayos.forEach((r, i) => { const a = -Math.PI / 2 + (i - 3) * .42, r0 = 110, r1 = 110 + (100 + 20 * Math.sin(t * 5 + i)) * P(t, en0 + i * .04, .5, E.out3);
      forma(r, () => linea(c.x + r0 * Math.cos(a), c.y + r0 * Math.sin(a), c.x + r1 * Math.cos(a), c.y + r1 * Math.sin(a), 1)); dibujar(r, t > en0 ? 1 : 0); });
  };
});

/* 6 · SABES: sé que sabes mucho — la pila de información crece sobre su cabeza */
escena('sabes', e => {
  const f = stickman(e.svg), libros = [0, 1, 2, 3, 4, 5, 6].map(i => trazo(e.svg, '', { ancho: 6, fill: '#fff', color: i % 3 ? NEGRO : C.ojo }));
  const tA = X(e, 'sabes mucho', 34.54, { tam: 110, x: 1240, y: 400 }), tB = X(e, 'toda la información|ojo', 36.05, { tam: 80, x: 1240, y: 540 });
  const t0 = en('sabes', 34.54), t1 = finDe('toda la información', 36.05);
  return (t, w) => {
    pt(tA, t); pt(tB, t);
    const st = pintarStick(f, t, { x: 640, y: 1040, s: .7, pose: mezclaPose(POSES.pie, POSES.manosCabeza, P(t, t1 - .4, .5)), t0: w.a - .7 });
    const n = Math.floor(1 + 6 * P(t, t0 - .3, t1 - t0 + .3));
    libros.forEach((l, i) => { const y = st.cabeza.y - 60 - i * 44, ww = 230 - (i % 3) * 30, bal = 6 * Math.sin(t * 3 + i) * (i / 6);
      forma(l, () => caja(640 - ww / 2 + (i % 2 ? 12 : -10) + bal, y - 40, ww, 40)); dibujar(l, i < n ? dib(t, t0 - .3 + i * (t1 - t0) / 7, .2) : 0); });
  };
});

/* 7 · CAMBIO: información → ¿cambio? */
escena('cambio', e => {
  const iA = X(e, 'Información|ojo', 43.62, { tam: 96, x: 560, y: 560 }), iB = X(e, 'Cambio', 44.46, { dice: 'cambiara', tam: 96, x: 1380, y: 560 });
  const mA = marco(e, iA, { color: C.ojo }), mB = marco(e, iB), u = unir(e, iA, iB);
  const gente = [0, 1, 2, 3, 4].map(() => stickman(e.svg)), tPe = en('persona', 44.8);
  const tq = en('cambiara', 44.46), q = texto(e, '?', tq + .3, { tam: 160, x: 970, y: 400 });
  return (t, w) => {
    pt(iA, t); pintarMarco(mA, t, iA._t[0] - .3); pintarUnion(u, t, iA._t[0] + .2, tq - iA._t[0] - .3);
    gente.forEach((g, i) => pintarStick(g, t, { x: 760 + i * 100, y: 1000, s: .26, pose: 'pie', t0: w.a - .5 + i * (tPe - w.a + .5) / 4 }));
    pt(iB, t); pintarMarco(mB, t, tq - .1); pt(q, t, { s: lerp(.6, 1, P(t, tq + .3, .4, E.back)) * (1 + .04 * Math.sin(t * 6)) });
  };
});

/* 8 · SUEÑOS: tú ahora → la persona que quieres ser */
escena('sueños', e => {
  const yo = stickman(e.svg), ideal = stickman(e.svg), aura = trazo(e.svg, '', { ancho: 6, color: C.corona }), f8 = fl(e.svg, 0, 0, 1, 1);
  const l1 = X(e, 'La vida de tus sueños|corona', 47.96, { dice: 'la vida de sus sueños', tam: 88, y: 170 });
  const l2 = X(e, 'la persona que quieres ser', 49.14, { dice: 'la persona que quiere ser', tam: 64, m: true, x: 1300, y: 990 });
  const tp = en('persona', 49.14);
  return (t, w) => {
    pt(l1, t); pt(l2, t);
    pintarStick(yo, t, { x: 620, y: 900, s: .62, pose: 'pie', t0: w.a - .7, o: .5 });
    forma(f8, () => flecha(760, 620, 1120, 620)); dibujar(f8, dib(t, tp - .3, .5));
    const st = pintarStick(ideal, t, { x: 1300, y: 900, s: .62, pose: mezclaPose(POSES.pie, POSES.arriba, P(t, tp + .4, .6, E.io3)), t0: tp - .2 });
    forma(aura, () => circulo(st.cabeza.x, st.cabeza.y, 60 + 8 * Math.sin(t * 4))); dibujar(aura, dib(t, tp + .5, .5), .8);
  };
});

/* 9 · PARÁLISIS POR ANÁLISIS: manos a la cabeza; le llueve información; la barra de «preparado» nunca llega */
escena('paralisis', e => {
  const tit = X(e, 'Parálisis por análisis|raiz', 70.98, { tam: 110, y: 170 }), f = stickman(e.svg);
  const pila = Array.from({ length: 10 }, () => ({ c: tarjetaVideo(e.svg, 0, 0, 150, 94), p: play(e.svg, 0, 0, 15) }));
  const tA = en('parálisis', 70.98), tB = en('información', 75.98), tP = en('preparado', 78.98);
  const qs = [0, 1, 2].map(i => texto(e, '?', tA + .4 + i * .5, { tam: 90, gris: true }));
  const eje = trazo(e.svg, '', { ancho: 6 }), barra = trazo(e.svg, '', { ancho: 54, color: C.plexo });
  const lab = X(e, '¿Preparado?', 78.98, { dice: 'preparado', tam: 80, x: 1300, y: 520 }), pct = texto(e, '90 %', tP, { tam: 64, m: true, x: 1300, y: 760, sonido: false });
  const nun = X(e, 'nunca es suficiente|raiz', 81, { dice: 'nunca sientes que tienes toda la información', tam: 64, x: 1300, y: 880 });
  pila.forEach((_, i) => i % 3 === 0 && suena(tA + .8 + i * (tB + .5 - tA) / 10, 'pop', .2));
  return (t, w) => {
    pt(tit, t);
    const st = pintarStick(f, t, { x: 600, y: 1000, s: .66, pose: 'manosCabeza', t0: w.a - .7 });
    qs.forEach((q, i) => pt(q, t, { x: st.cabeza.x - 150 + i * 150, y: st.cabeza.y - 150 - (i % 2) * 40 + 10 * Math.sin(t * 3 + i) }));
    pila.forEach((k, i) => { const t0 = tA + .8 + i * (tB + .5 - tA) / 10, p = P(t, t0, .35, E.out3), x = 300 + (i % 2) * 560 + (i % 3) * 30 - 15, y = 980 - Math.floor(i / 2) * 64 - (1 - p) * 260;
      k.c.setAttribute('transform', `translate(${x},${y}) rotate(${(i % 3 - 1) * 7})`); k.p.setAttribute('transform', `translate(${x},${y})`);
      dibujar(k.c, t > t0 ? 1 : 0, clamp(p * 2)); dibujar(k.p, t > t0 ? 1 : 0, clamp(p * 2)); });
    pt(lab, t);
    forma(eje, () => caja(1050, 610, 500, 60)); dibujar(eje, dib(t, tP - .3, .4));
    const v = .9 * P(t, tP, 1.2, E.out3) + .02 * Math.sin((t - tP) * 7) * (t > tP + 1.2);
    barra.setAttribute('d', `M1080,640 L${(1080 + 440 * v).toFixed(1)},640`); dibujar(barra, t > tP ? 1 : 0);
    pt(pct, t); pt(nun, t);
  };
});

/* 10 · CUERPO (silueta): nunca te has sentido seguro → para tu cuerpo es desconocido */
escena('cuerpo', e => {
  const sl = silueta(e.svg), pc = trazo(e.svg, '', { ancho: 10, color: C.corazon }), pp = trazo(e.svg, '', { ancho: 10, color: C.plexo });
  const anillo = trazo(e.svg, '', { ancho: 5, color: C.corazon });
  const tD = en('desconocido', 97.09), qs = [0, 1, 2].map(i => texto(e, '?', tD + i * .15, { tam: 110, gris: true, sonido: false }));
  const t1 = X(e, 'tu cuerpo|raiz', 90.86, { tam: 96, x: 960, y: 260, ax: 0 }), t2 = X(e, 'no está acostumbrado', 91.36, { tam: 72, m: true, x: 960, y: 370, ax: 0 });
  const t3 = X(e, 'a sentirse seguro|corazon', 96.09, { dice: 'una persona segura', tam: 80, x: 960, y: 560, ax: 0 });
  const t4 = X(e, '= desconocido|raiz', 98.09, { dice: 'algo desconocido', tam: 96, x: 960, y: 760, ax: 0 });
  const tN = en('nunca', 92.6), tS = en('segura', 96.09);
  suena(tN, 'brillo', .25);
  return (t, w) => {
    const x = 640, y = 1030, s = .95; pintarSilueta(sl, t, { x, y, s, t0: w.a - .7 });
    const c1 = centroSil(x, y, s, 'corazon'), c2 = centroSil(x, y, s, 'plexo');
    forma(pc, () => circulo(c1.x, c1.y, 8)); forma(pp, () => circulo(c2.x, c2.y, 8)); dibujar(pc, dib(t, tN, .2)); dibujar(pp, dib(t, tN + .3, .2));
    forma(anillo, () => circulo(c1.x, c1.y, 34 + 18 * Math.sin((t - tS) * 4))); dibujar(anillo, dib(t, tS, .4), .7);
    pt(t1, t); pt(t2, t); pt(t3, t); pt(t4, t);
    qs.forEach((q, i) => pt(q, t, { x: x - 160 + i * 160, y: y - 694 * s - 70 - (i % 2) * 40 }));
  };
});

/* 11 · ZONA DE CONFORT: dentro, segura porque la conoces; fuera, la zona expansiva */
escena('confort', e => {
  const ext = trazo(e.svg, 'M400,560 A560,420 0 1 1 1520,560 A560,420 0 1 1 400,560', { ancho: 6, color: C.corazon }), int = trazo(e.svg, circulo(960, 640, 220), { ancho: 8 });
  const so = sofa(e.svg), f = stickman(e.svg);
  const t1 = X(e, 'zona de confort', 105.42, { tam: 64, x: 960, y: 900 }), t2 = X(e, 'zona expansiva|corazon', 107.73, { tam: 72, x: 960, y: 95 });
  const t3 = X(e, 'segura|ok porque la conoces', 110.47, { dice: 'segura porque la conoces', tam: 56, m: true, x: 960, y: 1010 });
  const tE = en('expansiva', 107.73);
  return (t, w) => {
    dibujar(int, dib(t, w.a - .7, .6)); pintarSofa(so, t, w.a - .6, 960, 780, .42); pintarStick(f, t, { x: 960, y: 780, s: .42, pose: 'sentado', t0: w.a - .5 });
    const tPe = en('pero', 106.5); dibujar(ext, dib(t, tPe, tE - tPe + .3)); 
    pt(t1, t); pt(t2, t); pt(t3, t);
  };
});

/* 12 · CADENA: aplicas → resultados → te sientes diferente → eliges tu vida */
escena('cadena', e => {
  const P4 = [['Aplicas|ok', 'hasta', 560, 360], ['Resultados|plexo', 'resultados', 1360, 360], ['Te sientes diferente|corazon', 'diferente', 1220, 740], ['Eliges tu vida|corona', 'elijas', 520, 740]];
  const nodos = P4.map(([n, p, x, y]) => { const t0 = en(p, 119.38); const el = texto(e, n, t0, { tam: 72, x, y }); return { el, m: marco(e, el), t0 }; });
  const us = [0, 1, 2].map(i => unir(e, nodos[i].el, nodos[i + 1].el)), tCo = en('conseguir', 127.5);
  const cons = X(e, 'conscientemente', 129.5, { tam: 56, m: true, gris: true, x: 520, y: 860 });
  return (t, w) => {
    nodos.forEach((n, i) => { pt(n.el, t, { s: 1 + .05 * bump(t, n.t0, .5) }); pintarMarco(n.m, t, n.t0 - (i ? .15 : .5)); });
    const tOb = en('obtengas', 122.5);
    us.forEach((u, i) => i === 1 ? pintarUnion(u, t, tOb, nodos[2].t0 - tOb) : i < 2 ? pintarUnion(u, t, nodos[i + 1].t0 - .35) : pintarUnion(u, t, tCo, nodos[3].t0 - tCo)); pt(cons, t);
  };
});

/* 13 · APUNTES: haz apuntes — escribir pone todo el foco */
escena('apuntes', e => {
  const f = stickman(e.svg), mesa = trazo(e.svg, '', { ancho: 7, fill: '#fff' }), cuaderno = trazo(e.svg, '', { ancho: 6, fill: '#fff' });
  const rengl = [0, 1, 2, 3, 4].map(() => trazo(e.svg, '', { ancho: 5, color: C.garganta }));
  const tit = X(e, 'Haz apuntes|garganta', 135.71, { dice: 'hacer apuntes', tam: 110, x: 1240, y: 270 });
  const t2 = X(e, 'se te quedan mucho mejor', 137.21, { tam: 64, m: true, x: 1240, y: 400 }), t3 = X(e, 'todo el foco|plexo', 142.57, { tam: 88, x: 1240, y: 860 });
  const tE = en('escribes', 136.21), lapiz = emoji(e, '✍️', 110, tE);
  return (t, w) => {
    pintarStick(f, t, { x: 560, y: 1000, s: .7, pose: 'escribe', t0: w.a - .7 });
    forma(mesa, () => caja(320, 840, 480, 36) + ' ' + linea(360, 876, 360, 1060, 1) + ' ' + linea(760, 876, 760, 1060, 1)); dibujar(mesa, dib(t, w.a - .6, .5));
    forma(cuaderno, () => caja(1000, 500, 480, 260)); dibujar(cuaderno, dib(t, tE - .2, .4));
    rengl.forEach((r, i) => { const p = P(t, tE + .3 + i * 1.2, 1.1, E.io3), y = 560 + i * 42; r.setAttribute('d', `M1040,${y} L${(1040 + 400 * p * (i === 4 ? .6 : 1)).toFixed(1)},${y}`); dibujar(r, p > 0 ? 1 : 0); });
    const k = rengl.findIndex((_, i) => P(t, tE + .3 + i * 1.2, 1.1) < 1), kk = Math.max(0, k), ly = 560 + kk * 42, lx = 1040 + 400 * P(t, tE + .3 + kk * 1.2, 1.1, E.io3);
    pe(lapiz, t, tE, k < 0 ? 1440 : lx + 30, ly - 40);
    pt(tit, t); pt(t2, t); pt(t3, t);
  };
});

/* 14 · REGULA TU DOPAMINA: neurociencia, espiritualidad, psicología → el mismo resultado */
escena('regula', e => {
  const tit = X(e, 'Regula tu dopamina|sacro', 165.82, { dice: 'regular tu dopamina', tam: 120, y: 210 }), m = marco(e, tit, { color: C.sacro });
  const res = X(e, 'Mismo resultado|ok', 174.83, { dice: 'el resultado', tam: 72, x: 1360, y: 640 }), mr = marco(e, res, { color: C.corazon });
  const vias = [['Neurociencia|ojo', 'neurociencia'], ['Espiritualidad|corona', 'espiritualidad'], ['Psicología|garganta', 'psicológico']].map(([n, p], i) => {
    const t0 = en(p, 167.82), el = texto(e, n, t0, { tam: 68, x: 300, y: 500 + i * 140, ax: 0 }); return { t0, el, u: unir(e, el, res, { hueco: 18 }) }; });
  const igual = X(e, 'da igual el camino', 169, { dice: 'da igual si lo quieres aplicar', tam: 64, m: true, gris: true, y: 360 }), tFi = en('final', 175);
  const tR = en('mismo', 174.83);
  suena(tR, 'nota', .35);
  return (t, w) => {
    pt(tit, t); pintarMarco(m, t, w.a - .7);
    pt(igual, t); vias.forEach((v, i) => { pt(v.el, t, { s: 1 + .05 * bump(t, v.t0, .5) }); pintarUnion(v.u, t, tFi - .2 + i * .25); });
    pt(res, t); pintarMarco(mr, t, tR - .1);
  };
});

/* 15 · NOVEDAD: el cerebro acostumbrado a novedad súper alta — scroll infinito */
escena('novedad', e => {
  const med = medidor(e.svg, 190), mv = movil(e.svg, 220, 400);
  const t1 = X(e, 'Novedad|sacro', 180.2, { tam: 110, x: 700, y: 250 }), t2 = X(e, 'súper altos', 182.21, { tam: 72, m: true, x: 700, y: 360 });
  const t3 = X(e, 'scroll infinito', 188.05, { dice: 'estás scrolleando', tam: 72, x: 1380, y: 960 });
  const tCe = en('cerebro', 180), cer = emoji(e, '🧠', 110, tCe);
  const tA = en('súper', 182.21), tR = en('redes', 186.05);
  suena(tA, 'subida', .3); suena(tR, 'notificacion', .3);
  return (t, w) => {
    pt(t1, t); pt(t2, t); pt(t3, t); pe(cer, t, tCe, 700, 490);
    pintarMedidor(med, t, w.a - .7, 700, 780, .2 + .78 * P(t, tA - .3, .8, E.out3) + .02 * Math.sin(t * 9) * (t > tA));
    pintarMovil(mv, t, tR - .4, 1380, 640, 1, 0, Math.max(0, t - tR) * 260);
  };
});

/* 16 · PLACER CEREBRAL: comida basura, donut… sabes que no te hace bien */
escena('placer', e => {
  const tit = X(e, 'Placer cerebral|sacro', 202.43, { tam: 110, y: 220 });
  const tH = en('comida', 203.43), tD = en('donut', 205.43), tB = en('bien', 209.94);
  const hb = emoji(e, '🍔', 220, tH), dn = emoji(e, '🍩', 260, tD), x = trazo(e.svg, '', { ancho: 16, color: C.raiz });
  const tCb = en('cerebral', 208.5), cb = emoji(e, '🧠', 110, tCb), tSa = en('sabes', 209.5);
  const lab = X(e, 'no te hace bien|raiz', 209.94, { tam: 80, y: 900 });
  suena(tB, 'descarte', .35);
  return (t, w) => {
    pt(tit, t); pe(hb, t, tH, 680, 560 + 10 * Math.sin(t * 3), 1 - .7 * P(t, tD, .4)); pe(dn, t, tD, 1180, 560 + 10 * Math.sin(t * 3 + 1));
    pe(cb, t, tCb, 960, 370); forma(x, () => cruz(1180, 560, 5)); dibujar(x, dib(t, tSa + .3, .8)); pt(lab, t);
  };
});

/* 17 · EL GRAN ERROR: dopamina con todo lo demás — fumar, contenido, móvil */
escena('error', e => {
  const tit = X(e, 'El gran error|raiz', 229.0, { dice: 'estás cometiendo el gran error', tam: 120, y: 220 });
  const it = [['🚬', 'fumando'], ['📺', 'contenido'], ['📱', 'móvil']].map(([em, p], i) => { const t0 = en(p, 230.5);
    return { t0, em: emoji(e, em, 200, t0), d: texto(e, '+dopamina|sacro', t0 + .2, { tam: 56, x: 500 + i * 460, y: 840, sonido: false }) }; });
  const sub = trazo(e.svg, '', { ancho: 8, color: C.sacro }), tOt = en('otras cosas', 233.5);
  const cte = X(e, 'dopamina constante|sacro', 232, { dice: 'constantemente tener dopamina', tam: 72, y: 360 });
  return (t, w) => { pt(tit, t); pt(cte, t); const rc = medir(cte); forma(sub, () => linea(960 - rc.w / 2, 404, 960 + rc.w / 2, 400, 2)); dibujar(sub, dib(t, tOt, .5)); it.forEach((k, i) => { pe(k.em, t, k.t0, 500 + i * 460, 580 + 8 * Math.sin(t * 3 + i)); pt(k.d, t, { y: 840 - 10 * P(t, k.t0 + .2, .6) }); }); };
});

/* 18 · ABURRIDO: silencio, ejercicio, leer… al principio, una puta mierda */
escena('aburrido', e => {
  const filas = [['🧘', 'Silencio 5–10 min', 'silencio'], ['🏋️', 'Ejercicio', 'ejercicio'], ['📖', 'Leer', 'leer']].map(([em, n, p], i) => { const t0 = en(p, 250.69);
    return { t0, em: emoji(e, em, 110), tx: texto(e, n, t0, { tam: 80, x: 460, y: 300 + i * 190, ax: 0 }) }; });
  { const q = ts('silencio 5 o 10 minutos', 253); filas[0].tx._t = [q[0], q[1], q[4]]; }
  const conf = X(e, '+ confianza|corazon', 259, { dice: 'generan confianza', tam: 64, x: 460, y: 860, ax: 0 });
  const f = stickman(e.svg), sello = X(e, 'ABURRIDO|raiz', 259.46, { dice: 'puta mierda', tam: 120, x: 1360, y: 900, sonido: false });
  const tM = en('mierda', 259.46), tBe = en('benefician', 258), oks = [0, 1, 2].map(() => trazo(e.svg, '', { ancho: 9, color: C.corazon }));
  suena(tM, 'golpe', .4); suena(tBe, 'tick', .3);
  return (t, w) => {
    filas.forEach((k, i) => { pe(k.em, t, k.t0, 370, 300 + i * 190); pt(k.tx, t); const r = medir(k.tx); forma(oks[i], () => tick(460 + r.w + 70, 300 + i * 190, 1.1)); dibujar(oks[i], dib(t, tBe + i * .25, .3)); });
    pt(conf, t);
    pintarStick(f, t, { x: 1360, y: 760, s: .6, pose: mezclaPose(POSES.pie, POSES.hundido, P(t, tM - .5, .6, E.io3)), t0: w.a - .2 });
    pt(sello, t, { s: lerp(1.6, 1, P(t, tM, .25, E.out3)) }); sello.style.transform += ' rotate(-6deg)';
  };
});

/* 19 · EL MONO (silueta: el cuerpo): el cerebro pide más novedad — síndrome de abstinencia */
escena('mono', e => {
  const sl = silueta(e.svg), ondas = [0, 1, 2, 3].map(() => trazo(e.svg, '', { ancho: 5, color: C.ojo }));
  const t1 = X(e, '¡más novedad!|sacro', 267.65, { dice: 'más novedad', tam: 88, x: 1180, y: 300 }), b = trazo(e.svg, '', { ancho: 6 });
  const t2 = X(e, 'Síndrome de abstinencia|raiz', 270.65, { tam: 80, x: 1150, y: 640 }), t3 = X(e, '(el mono)', 273.3, { dice: 'el mono', tam: 72, m: true, x: 1150, y: 760 });
  const tS = en('señales', 267.33), tN = en('novedad', 267.65);
  suena(tS, 'brillo', .25);
  return (t, w) => {
    const x = 520, y = 1030, s = .95; pintarSilueta(sl, t, { x, y, s, t0: w.a - .7 });
    const hd = centroSil(x, y, s, 'ojo');
    ondas.forEach((o, i) => { if (t < tS) return dibujar(o, 0); const k = ((t - tS) / 1.2 + i / 4) % 1, yy = hd.y + 70 + k * 420;
      forma(o, () => `M${x - 70},${yy.toFixed(1)} Q${x},${(yy + 30).toFixed(1)} ${x + 70},${yy.toFixed(1)}`); dibujar(o, 1, (1 - k) * P(t, tS, .3)); });
    pt(t1, t); const r = medir(t1);
    forma(b, () => `M${1180 - r.w / 2 - 50},${300 - r.h / 2 - 30} L${1180 + r.w / 2 + 50},${300 - r.h / 2 - 30} L${1180 + r.w / 2 + 50},${300 + r.h / 2 + 30} L${820},${300 + r.h / 2 + 30} L${hd.x + 70},${hd.y - 20} L${760},${300 + r.h / 2 + 30} L${1180 - r.w / 2 - 50},${300 + r.h / 2 + 30} Z`);
    dibujar(b, dib(t, tN - .3, .4)); pt(t2, t); pt(t3, t);
  };
});

/* 20 · CEREBRAL vs CORPORAL */
escena('cerebral', e => {
  const iz = X(e, 'Placer cerebral|sacro', 282.31, { dice: 'placer cerebral', tam: 80, x: 600, y: 640 }), de = X(e, 'Placer corporal|corazon', 283.31, { dice: 'placer corporal', tam: 80, x: 1320, y: 640 });
  const tA = en('cerebral', 282.31), tB = en('corporal', 283.31);
  const e1 = emoji(e, '🧠', 200), e2 = emoji(e, '💪', 200), div = trazo(e.svg, linea(960, 260, 960, 860, 2), { ancho: 6, color: '#bbb' });
  return (t, w) => { dibujar(div, dib(t, w.a - .7, .4)); pe(e1, t, tA - .2, 600, 440 + 8 * Math.sin(t * 3)); pe(e2, t, tB - .2, 1320, 440 + 8 * Math.sin(t * 3 + 1)); pt(iz, t); pt(de, t); };
});

/* 21 · COLOR: al día siguiente las cosas tienen mucho más color */
const hexRGB = h => [1, 3, 5].map(i => parseInt(h.slice(i, i + 2), 16));
escena('color', e => {
  const cs = Object.values(C), bol = cs.map(() => trazo(e.svg, '', { ancho: 8 }));
  const tx = X(e, 'mucho más color', 291.64, { tam: 110, y: 330 }), tC = en('color', 293.65);
  suena(tC, 'brillo', .35);
  return (t, w) => {
    pt(tx, t);
    bol.forEach((b, i) => { const x = 960 + (i - 3) * 190, y = 680 + (i % 2) * 40 + 10 * Math.sin(t * 3 + i), k = P(t, tC + i * .06, .4);
      forma(b, () => circulo(x, y, 70)); b.setAttribute('stroke', mix([170, 170, 170], hexRGB(cs[i]), k)); b.setAttribute('fill', k > 0 ? cs[i] : 'none');
      b.style.fillOpacity = (k * .9).toFixed(3); dibujar(b, dib(t, w.a - .7 + i * .05, .4)); });
    const sp = tx._sp[2]; if (sp) sp.style.color = mix([17, 17, 17], hexRGB(C.corona), P(t, tC, .4));
  };
});

/* 22 · LOS 3 PILARES: ayuno, ejercicio, ducha fría */
escena('pilares', e => {
  const tit = X(e, 'Restaura tu dopamina|sacro', 296.65, { dice: 'si quieres restaurar tus niveles de dopamina', tam: 96, y: 200 });
  const PIL = [['🍽️', 'Ayuno|plexo', 'ayuno'], ['🏃', 'Ejercicio|raiz', 'ejercicio'], ['🚿', 'Ducha fría|garganta', 'ducha']].map(([em, n, p], i) => { const t0 = en(p, 298.65);
    return { t0, em: emoji(e, em, 170), n: texto(e, `${i + 1}`, t0, { tam: 64, gris: true, x: 520 + i * 440, y: 420, sonido: false }), tx: texto(e, n, t0, { tam: 72, x: 520 + i * 440, y: 800 }) }; });
  const sub = trazo(e.svg, '', { ancho: 9, color: C.sacro }), tSo = en('sobre', 301), mas = [0, 1].map(() => trazo(e.svg, '', { ancho: 9 })), tCb = en('combinar', 303), tYu = en('una ducha', 305.5);
  return (t, w) => { pt(tit, t); const r = medir(tit); forma(sub, () => linea(960 - r.w / 2, 262, 960 + r.w / 2, 258, 2)); dibujar(sub, dib(t, tSo, .5));
    mas.forEach((m, i) => { const x = 740 + i * 440; forma(m, () => `M${x - 26},600 L${x + 26},600 M${x},574 L${x},626`); dibujar(m, dib(t, i ? tYu : tCb, .3)); });
    PIL.forEach((k, i) => { pe(k.em, t, k.t0, 520 + i * 440, 600 + 8 * Math.sin(t * 3 + i)); pt(k.n, t); pt(k.tx, t); }); };
});

/* 23 · COMIDAS: yo como una vez al día; hay quien come cinco — cada comida, una recompensa */
escena('comidas', e => {
  const cj = ceja(e, 'PILAR 1 · AYUNO', C.plexo);
  const corta = X(e, 'Cortas el placer|raiz', 308.5, { dice: 'estás cortando todos los placeres', tam: 88, y: 290 });
  const yo = X(e, 'Yo: 1 vez al día|ok', 313.5, { dice: 'yo solamente como una vez al día', tam: 72, x: 960, y: 450 });
  const otros = X(e, 'Otros: 5 veces|raiz', 316.51, { dice: 'cinco veces', tam: 72, x: 960, y: 730 });
  const tY = en('una vez', 314.5), tC = en('tres', 314.51), t5 = en('cinco', 316.51), tp = i => tC + i * (t5 + .3 - tC) / 5;
  const p1 = emoji(e, '🍽️', 110, tY), p5 = [0, 1, 2, 3, 4].map(i => emoji(e, '🍽️', 90, tp(i)));
  const mas = [0, 1, 2, 3, 4].map(() => trazo(e.svg, '', { ancho: 6, color: C.sacro, fill: C.sacro }));
  const niv = X(e, 'a nivel de comida', 312.5, { tam: 56, m: true, gris: true, y: 370 });
  return (t, w) => {
    pintarCeja(cj, t, w.a - .7, 960, 180); pt(corta, t);
    pt(yo, t); pe(p1, t, tY, 960, 570); pt(otros, t);
    pt(niv, t); p5.forEach((p, i) => { const x = 660 + i * 150; pe(p, t, tp(i), x, 870); forma(mas[i], () => estrella(x + 52, 812, 16)); dibujar(mas[i], dib(t, tp(i) + .2, .3)); });
  };
});

/* 24 · CORTAR DE RAÍZ: el ayuno corta la dopamina de la comida */
escena('cortar', e => {
  const tit = X(e, 'Cortar de raíz|raiz', 343.75, { dice: 'cortar de raíz', tam: 120, y: 230 });
  const tC = en('cortar', 343.75), pl = emoji(e, '🍽️', 180), cable = trazo(e.svg, '', { ancho: 8, color: C.sacro }), tij = emoji(e, '✂️', 140);
  const ali = X(e, 'de los alimentos', 347.5, { tam: 56, m: true, gris: true, x: 560, y: 780 });
  const dop = X(e, 'dopamina|sacro', 345.25, { tam: 88, x: 1400, y: 620 });
  suena(tC + .3, 'corte', .45);
  return (t, w) => {
    pt(tit, t); pe(pl, t, w.a - .7, 560, 620); pt(dop, t); pt(ali, t);
    const k = P(t, tC + .3, .3);
    forma(cable, () => `M680,620 L${lerp(1180, 930, k)},${620 + 30 * k} M${lerp(1180, 1000, k)},${620 - 30 * k} L1180,620`); dibujar(cable, dib(t, w.a - .6, .4));
    pe(tij, t, tC, 960, 540 + 80 * P(t, tC, .4, E.io3));
  };
});

/* 25 · CALENDARIO: un día a la semana… dos o tres días una vez al mes */
escena('calendario', e => {
  const sem = 'L M X J V S D'.split(' ').map(d => ({ c: trazo(e.svg, '', { ancho: 5 }), tx: texto(e, d, 0, { tam: 56, m: true, gris: true, sonido: false }) }));
  const mes = Array.from({ length: 28 }, () => trazo(e.svg, '', { ancho: 4, color: '#999' })), marc = trazo(e.svg, '', { ancho: 9, color: C.plexo });
  const marcMes = trazo(e.svg, '', { ancho: 9, color: C.plexo });
  const l1 = X(e, '1 día a la semana', 352.24, { dice: 'un día a la semana', tam: 72, x: 960, y: 170 }), l2 = X(e, '2–3 días al mes', 354.74, { dice: 'dos días durante una vez al mes', tam: 72, x: 960, y: 560 });
  const tD = en('semana', 352.24), t2 = en('dos', 354.74), t3 = en('tres', 356.73);
  const okc = trazo(e.svg, '', { ancho: 10, color: C.corazon }), tEj = en('ejemplo', 360.3);
  suena(tD, 'tick', .3); suena(t3, 'tick', .3); suena(tEj, 'tick', .3);
  return (t, w) => {
    pt(l1, t); pt(l2, t);
    sem.forEach((k, i) => { const x = 450 + i * 170; forma(k.c, () => caja(x - 60, 260, 120, 120)); dibujar(k.c, dib(t, w.a - .7 + i * .04, .3)); pt(k.tx, t, { x, y: 320 }); });
    forma(marc, () => circulo(450 + 2 * 170, 320, 82)); dibujar(marc, dib(t, tD, .4));
    mes.forEach((c, i) => { const x = 570 + (i % 7) * 115, y = 660 + Math.floor(i / 7) * 95; forma(c, () => caja(x - 45, y - 38, 90, 76)); dibujar(c, dib(t, t2 - .4 + i * .015, .25)); });
    const n = 2 + P(t, t3, 1.2, E.io3); forma(marcMes, () => caja(570 + 2 * 115 - 55, 660 + 95 - 46, 115 * (n - 1) + 110, 92)); dibujar(marcMes, dib(t, t2 + .3, .4));
    forma(okc, () => tick(1440, 700, 1.4)); dibujar(okc, dib(t, tEj, .35));
  };
});

/* 26 · EXPLOSIÓN: la de comer tras el ayuno es natural; la de los videojuegos, no */
escena('explosion', e => {
  const ex1 = trazo(e.svg, '', { ancho: 7, color: C.corazon }), ex2 = trazo(e.svg, '', { ancho: 7, color: C.raiz });
  const tCm = en('volver', 386), tEx = en('explosión', 387.5), tGe = en('general', 391.5), tQn = en('que no', 393.5), tE3 = en('explosión de dopamina', 394.5);
  const mala = X(e, 'no es mala|ok', 389, { dice: 'no tiene por qué ser mala', tam: 56, m: true, x: 600, y: 790 }), dv = trazo(e.svg, linea(960, 300, 960, 980, 2), { ancho: 6, color: '#bbb' }), vs = texto(e, 'vs', tQn, { tam: 72, gris: true, x: 960, y: 560 });
  const tE2 = en('explosión', 390.5), boom = emoji(e, '💥', 110, tE2);
  const tV = en('videojuegos', 394.59), tE = en('volver', 385.1);
  const pl = emoji(e, '🍽️', 120), vj = emoji(e, '🎮', 140);
  const a = X(e, 'Natural|ok', 389.46, { dice: 'más natural', tam: 88, x: 600, y: 900 }), b = X(e, 'Videojuegos|raiz', 394.59, { dice: 'jugar a videojuegos', tam: 88, x: 1320, y: 900 });
  suena(en('explosión', 385.6), 'impacto', .3); suena(tV, 'glitch', .3);
  const rafaga = (x, y, r, n, k) => { let d = ''; for (let i = 0; i <= 2 * n; i++) { const an = i * Math.PI / n, rr = i % 2 ? r * .55 : r * (1 + .12 * Math.sin(i * k));
    d += (i ? 'L' : 'M') + (x + rr * Math.cos(an)).toFixed(1) + ',' + (y + rr * Math.sin(an)).toFixed(1) + ' '; } return d + 'Z'; };
  return (t, w) => {
    forma(ex1, () => rafaga(600, 560, 190 * (.4 + .6 * P(t, tEx, .5, E.back)) * (1 + .02 * Math.sin(t * 6)), 9, 1)); dibujar(ex1, t > tEx - .2 ? 1 : 0);
    pe(pl, t, tCm, 600, 560); pt(a, t); pt(mala, t); dibujar(dv, dib(t, tGe, .6)); pt(vs, t); pe(boom, t, tE2, 760, 380);
    forma(ex2, () => rafaga(1320, 560, 270 * (.4 + .6 * P(t, tE3, .4, E.back)) * (1 + .03 * Math.sin(t * 30)), 14, 7)); dibujar(ex2, t > tE3 - .1 ? 1 : 0);
    pe(vj, t, tV - .1, 1320, 560); pt(b, t);
  };
});

/* 27 · EJERCICIO: pilar 2 — camina, pero que sudes */
escena('ejercicio', e => {
  const cj = ceja(e, 'PILAR 2', C.raiz);
  const tit = X(e, 'Ejercicio|raiz', 397.76, { dice: 'hacer ejercicio', tam: 120, x: 1220, y: 300 }), f = stickman(e.svg);
  const sud = X(e, 'que sudes|garganta', 405.26, { dice: 'es importante que sudes', tam: 104, x: 1220, y: 820 });
  const tS = en('sudes', 405.26), gotas = [0, 1, 2].map(i => emoji(e, '💦', 90, i ? 0 : tS));
  return (t, w) => {
    pintarCeja(cj, t, w.a - .7, 1220, 190); pt(tit, t); pt(sud, t);
    const k = Math.sin((t - w.a) * 7), x = 600 + Math.max(0, t - w.a) * 14;
    const st = pintarStick(f, t, { x, y: 1000, s: .74, pose: { ...POSES.camina, bI: 18 + 26 * k, bD: 18 - 26 * k, pI: 4 + 18 * k, pD: 4 - 18 * k }, t0: w.a - .7 });
    gotas.forEach((g, i) => pe(g, t, tS + i * .12, st.cabeza.x + (i - 1) * 120, st.cabeza.y - 40 + (i % 2) * 50 + 30 * ((t * 1.5 + i / 3) % 1)));
  };
});

/* 28 · DUCHA FRÍA: pilar 3 — aunque sea el último minuto; incómodo de cojones */
escena('ducha', e => {
  const cj = ceja(e, 'PILAR 3', C.garganta);
  const tit = X(e, 'Ducha fría|garganta', 415.32, { dice: 'ducha fría', tam: 120, x: 1240, y: 300 });
  const tubo = trazo(e.svg, 'M520,80 L520,170 Q520,200 560,200 L640,200', { ancho: 8 }), alca = trazo(e.svg, 'M600,200 L680,200 L720,260 L560,260 Z', { ancho: 7, fill: '#fff' });
  const gotas = Array.from({ length: 14 }, () => trazo(e.svg, '', { ancho: 6, color: C.garganta })), f = stickman(e.svg);
  const ult = X(e, 'el último minuto', 418.82, { tam: 72, x: 1240, y: 520 }), tM = en('minuto', 419.82), crono = texto(e, '1:00', tM, { tam: 120, x: 1240, y: 650, sonido: false });
  const inc = X(e, 'incómodo de cojones|raiz', 424.7, { tam: 80, x: 1240, y: 880 }), tI = en('incómodo', 424.7);
  suena(tI, 'golpe-corto', .35);
  return (t, w) => {
    pintarCeja(cj, t, w.a - .7, 1240, 190); pt(tit, t); dibujar(tubo, dib(t, w.a - .7, .3)); dibujar(alca, dib(t, w.a - .5, .3));
    gotas.forEach((g, i) => { const k = ((t * 1.6 + i / 14) % 1), x = 590 + (i % 7) * 24 - 72, y = 280 + k * 640;
      g.setAttribute('d', `M${x},${y.toFixed(1)} L${x - 4},${(y + 34).toFixed(1)}`); dibujar(g, t > w.a - .3 ? 1 : 0, 1 - k * .6); });
    pintarStick(f, t, { x: 640, y: 1040, s: .7, pose: mezclaPose(POSES.pie, POSES.manosCabeza, P(t, tI - .3, .5, E.io3)), t0: w.a - .7 });
    pt(ult, t); const s = Math.max(0, 60 - Math.floor(Math.max(0, t - tM - .3) * 8)); crono._sp[0].textContent = s === 60 ? '1:00' : `0:${String(s).padStart(2, '0')}`;
    pt(crono, t); pt(inc, t);
  };
});

/* 29 · ALERTA: el último recurso es el placer; lo primero, la supervivencia */
escena('alerta', e => {
  const cj = ceja(e, 'PRIORIDADES DEL CUERPO');
  const tS = en('supervivencia', 458.16);
  const sup = X(e, '1 · Supervivencia|raiz', 458.16, { dice: 'la supervivencia', tam: 96, x: 960, y: 380 });
  const pla = X(e, 'Último · Placer|sacro', 455.66, { dice: 'el último de los recursos es el placer', tam: 96, x: 960, y: 800 });
  const ms = marco(e, sup, { color: C.raiz }), u = unir(e, sup, pla, { hueco: 40 });
  return (t, w) => {
    pintarCeja(cj, t, w.a - .7, 960, 200);
    pt(pla, t); pt(sup, t, { s: 1 + .04 * bump(t, tS, .5) }); pintarMarco(ms, t, tS); pintarUnion(u, t, tS + .3);
  };
});

/* 30 · NADA DE: contenido pornográfico, contenido hipersexualizado */
escena('nada', e => {
  const tit = X(e, 'Nada de…', 479.34, { dice: 'nada de', tam: 110, y: 260 });
  const filas = [filaLista(e, 'Contenido pornográfico', en('pornográfico', 480.5), { no: true, tam: 80 }), filaLista(e, 'Contenido hipersexualizado', en('hipersexualizado', 484.5), { no: true, tam: 80 })];
  const emj = emoji(e, '🔞', 150), nn = X(e, 'ni nada de nada|raiz', 482, { tam: 64, y: 380 });
  filas.forEach(f => suena(f.t0 + .1, 'descarte', .35));
  return (t, w) => { pt(tit, t); pt(nn, t); filas.forEach((f, i) => pintarFila(f, t, 340, 520 + i * 170)); pe(emj, t, en('sobre todo', 483), 960, 900); };
});

/* 31 · SCROLL: 5 minutos… y acabas una hora — enganchado */
escena('scroll', e => {
  const mv = movil(e.svg, 240, 440), tE = en('enganchado', 505.24), anz = emoji(e, '🎣', 140, tE);
  const m5 = X(e, '5 min', 501.24, { dice: 'cinco minutos', tam: 104, x: 1300, y: 380 }), tach = trazo(e.svg, '', { ancho: 10, color: C.raiz });
  const h1 = X(e, '1 hora|raiz', 503.23, { dice: 'una hora', tam: 120, x: 1300, y: 560 }), eng = X(e, 'enganchado|sacro', 505.24, { tam: 88, x: 1300, y: 800 });
  const tH = en('hora', 503.23);
  return (t, w) => {
    pintarMovil(mv, t, w.a - .7, 640, 600, 1, 0, Math.max(0, t - w.a) * 220);
    pt(m5, t); const r = medir(m5); forma(tach, () => linea(1300 - r.w / 2 - 20, 386, 1300 + r.w / 2 + 20, 376, 2)); dibujar(tach, dib(t, tH - .2, .25));
    pt(h1, t); pt(eng, t); pe(anz, t, tE, 640, 290 + 10 * Math.sin(t * 4));
  };
});

/* 32 · FASES: fase 1 regula tu dopamina (este vídeo) — fase 2 usa tu fuego (otro vídeo) */
escena('fases', e => {
  const f1 = X(e, 'Fase 1', 531.09, { dice: 'esto es como la primera fase', tam: 72, gris: true, x: 520, y: 330, ax: 0 }), f1b = texto(e, 'Regula tu dopamina|sacro', en('primera', 531.09), { tam: 80, x: 520, y: 430, ax: 0 });
  const tk = trazo(e.svg, tick(420, 400, 1.6), { ancho: 10, color: C.corazon, k: 'marca' });
  const f2 = X(e, 'Fase 2', 532.39, { dice: 'segunda fase', tam: 72, gris: true, x: 520, y: 640, ax: 0 }), f2b = X(e, 'Usa tu fuego|raiz', 534.89, { dice: 'mucho fuego', tam: 80, x: 520, y: 740, ax: 0 });
  const tF = en('fuego', 534.89), tO = en('otro', 542.7), fuego = emoji(e, '🔥', 120, tF), yt = logoYT(e.svg), prox = X(e, 'próximo vídeo', 542.7, { dice: 'otro vídeo', tam: 56, m: true, x: 1400, y: 840 });
  const lu = X(e, 'lujuria|sacro', 537.9, { tam: 72, x: 1400, y: 470 }), cul = X(e, 'culpa', 540.4, { dice: 'has culpado', tam: 64, m: true, gris: true, x: 1400, y: 570 });
  const ext = X(e, 'energía extra|plexo', 536, { tam: 72, x: 1400, y: 250 }), tach = trazo(e.svg, '', { ancho: 8, color: C.raiz }), tM = en('maldecido', 540.9);
  suena(tO, 'notificacion', .3);
  return (t, w) => {
    pt(f1, t); pt(f1b, t); dibujar(tk, dib(t, en('primera', 531.09) + .3, .3)); pt(f2, t); pt(f2b, t);
    pe(fuego, t, tF, 420, 700 + 6 * Math.sin(t * 5)); pt(ext, t); pt(lu, t); pt(cul, t);
    const r = medir(cul); forma(tach, () => linea(1400 - r.w / 2 - 14, 572, 1400 + r.w / 2 + 14, 566, 2)); dibujar(tach, dib(t, tM, .25));
    pintarLogo(yt, t, tO - .1, 1400, 740, 1.1); pt(prox, t);
  };
});

/* 33 · LO FÁCIL: en el sofá con el móvil, sin hacer nada… y la recompensa de subir el Everest 25 veces */
escena('facil', e => {
  const so = sofa(e.svg), f = stickman(e.svg), mv = movilMano(e);
  const mont = trazo(e.svg, 'M1060,880 L1300,420 L1380,560 L1440,470 L1640,880 Z', { ancho: 7, fill: '#fff' });
  const nieve = trazo(e.svg, 'M1250,516 L1300,420 L1350,516 L1320,500 L1300,530 L1280,500 Z', { ancho: 6, color: C.garganta }), bandera = trazo(e.svg, 'M1300,420 L1300,330 L1360,350 L1300,370', { ancho: 6, color: C.raiz });
  const tSc = en('ver', 565.21), tv = emoji(e, '📺', 110, tSc);
  const nada = X(e, 'esfuerzo: 0', 569.5, { dice: 'absolutamente nada', tam: 64, m: true, x: 560, y: 990 });
  const ev = X(e, 'Everest', 573.71, { dice: 'monte verés', tam: 72, x: 1350, y: 960 }), x25 = X(e, '×25|plexo', 574.21, { dice: '25 veces', tam: 140, x: 1540, y: 320, sonido: false });
  const rec = X(e, 'Recompensa|sacro', 570.22, { dice: 'la recompensa', tam: 88, x: 1250, y: 200 });
  const tSi = en('simplemente', 564.5), relax = emoji(e, '😌', 90, tSi), tSx = en('sexual', 566.5), xx = emoji(e, '🔞', 80, tSx), tScr = en('scrolleas', 568.5), dedo = emoji(e, '👆', 80, tScr);
  const tR = en('recompensa', 570.22), tM = en('monte', 573.71), t25 = en('25', 574.21);
  suena(t25, 'golpe', .4);
  return (t, w) => {
    pintarSofa(so, t, w.a - .8, 560, 900, .7);
    const st = pintarStick(f, t, { x: 560, y: 900, s: .7, pose: 'sentadoMovil', t0: w.a - .7 }); pintarMovilMano(mv, t, w.a - .3, st.manoD, .85);
    pe(tv, t, tSc, 860, 420); pe(xx, t, tSx, 860, 540); pe(relax, t, tSi, st.cabeza.x - 120, st.cabeza.y - 40); pe(dedo, t, tScr, st.manoD.x + 60, st.manoD.y - 30 - 25 * Math.abs(Math.sin((t - tScr) * 5)) * (t > tScr)); pt(nada, t); pt(rec, t);
    dibujar(mont, dib(t, tR, 2.2)); dibujar(nieve, dib(t, tR + .5, .3)); dibujar(bandera, dib(t, tM, .3)); pt(ev, t);
    pt(x25, t, { s: lerp(1.5, 1, P(t, t25, .3)) });
  };
});

/* 34 · 50 LIBROS, 800 VÍDEOS, PODCAST… tu vida no cambia */
escena('libros', e => {
  const it = [['📚', '50 libros', 'comer'], ['▶️', '800 vídeos', 'vídeos'], ['🎙️', 'podcasts', 'podcast']].map(([em, n, p], i) => { const t0 = en(p, 612.83);
    return { t0, em: emoji(e, em, 130, t0), tx: texto(e, n, t0, { tam: 72, x: 480 + i * 480, y: 470, sonido: false }) }; });
  const f34 = fl(e.svg, 960, 560, 960, 700);
  const fin = X(e, 'Tu vida no cambia|raiz', 618.62, { dice: 'tu vida no va a cambiar', tam: 104, y: 820 }), tV = en('vida', 618.62);
  suena(en('cambiar', 618.62), 'descarte', .35);
  const tQu = en('quieras', 618), cifra = [50, 800];
  return (t, w) => { it.forEach((k, i) => { pe(k.em, t, k.t0, 480 + i * 480, 320 + 8 * Math.sin(t * 3 + i)); if (i < 2) k.tx._sp[0].textContent = Math.round(cifra[i] * P(t, k.t0, .9, E.out3)); pt(k.tx, t); });
    dibujar(f34, dib(t, tQu, tV - tQu)); pt(fin, t); };
});

/* 35 · RECAP: los tres pilares ✓ y nada de contenido hipersexualizado ✗ */
escena('recap', e => {
  const cj = ceja(e, 'LOS 3 PILARES', C.corazon);
  const filas = [['Sudoración', 'sudoración'], ['Ejercicio físico', 'ejercicio'], ['Ducha fría', 'ducha']].map(([n, p]) => filaLista(e, n, en(p, 633.22), { tam: 80 }));
  const no = filaLista(e, 'Contenido hipersexualizado', en('nada de contenido', 637), { tam: 80, no: true });
  [...filas, no].forEach(f => suena(f.t0 + .1, f.no ? 'descarte' : 'tick', .35));
  return (t, w) => { pintarCeja(cj, t, w.a - .7, 960, 190); filas.forEach((f, i) => pintarFila(f, t, 400, 340 + i * 150)); pintarFila(no, t, 400, 820); };
});

/* 36 · SIN ENERGÍA: me siento mal — energía y motivación vacías */
escena('energia', e => {
  const f = stickman(e.svg), nube = emoji(e, '🌧️', 130), bats = [['Energía|plexo', 'energía'], ['Motivación|sacro', 'motivación']].map(([n, p], i) => { const t0 = en(p, 661.48);
    return { t0, tx: texto(e, n, t0, { tam: 72, x: 1000, y: 330 + i * 300, ax: 0 }), c: trazo(e.svg, '', { ancho: 7 }), r: trazo(e.svg, '', { ancho: 50, color: C.raiz }) }; });
  const tCn = en('construir', 665), tPr = en('proyectos', 668), blq = [0, 1, 2].map(() => trazo(e.svg, '', { ancho: 6, fill: '#fff' })), pro = X(e, 'tus proyectos', 668, { dice: 'mis proyectos', tam: 56, m: true, gris: true, x: 450, y: 1000 });
  bats.forEach(b => suena(b.t0 + .6, 'fallo', .25));
  return (t, w) => {
    const st = pintarStick(f, t, { x: 620, y: 1000, s: .74, pose: 'hundido', t0: w.a - .7 });
    pe(nube, t, w.a - .3, st.cabeza.x, st.cabeza.y - 150 + 8 * Math.sin(t * 2)); pt(pro, t);
    blq.forEach((b, i) => { forma(b, () => caja(380 + (i % 2) * 50, 880 - i * 70, 120, 64)); dibujar(b, dib(t, tCn + i * .6, .35), i === 2 ? 1 - .7 * P(t, tPr, .5) : 1); });
    bats.forEach((b, i) => { const y = 440 + i * 300; pt(b.tx, t);
      forma(b.c, () => caja(1000, y - 45, 520, 90) + ' ' + linea(1528, y - 18, 1528, y + 18, 0)); dibujar(b.c, dib(t, b.t0 - .2, .35));
      const v = lerp(.8, .06, P(t, b.t0 + .2, .9, E.io3)); b.r.setAttribute('d', `M1030,${y} L${(1030 + 460 * v).toFixed(1)},${y}`);
      b.r.setAttribute('stroke', v > .3 ? C.corazon : C.raiz); dibujar(b.r, t > b.t0 - .1 ? 1 : 0); });
  };
});

/* 37 · REAJUSTE: «me estoy aburriendo… pero mi dopamina se está reajustando» */
escena('reajuste', e => {
  const f = stickman(e.svg), bo = bocadillo(e, 'me estoy aburriendo', ts('me estoy aburriendo', 720.1), { tam: 64 });
  const med = medidor(e.svg, 170), tx = X(e, 'se está reajustando|ok', 724.11, { dice: 'se están reajustando', tam: 80, x: 1240, y: 920 });
  const tR = en('reajustando', 724.11), dop = X(e, 'mi dopamina|sacro', 722.11, { dice: 'mi dopamina', tam: 64, x: 1240, y: 450 });
  suena(tR, 'nota-doble', .35);
  return (t, w) => {
    const st = pintarStick(f, t, { x: 560, y: 1010, s: .7, pose: 'pie', t0: w.a - .7 });
    pintarBocadillo(bo, t, w.a - .3, 760, 300, st.cabeza.x + 20, st.cabeza.y - 60);
    pt(dop, t); pintarMedidor(med, t, en('dopamina', 722.11) - .3, 1240, 720, lerp(.95, .5, P(t, tR - .3, 1, E.io3)) + .03 * Math.sin(t * 5));
    pt(tx, t);
  };
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
