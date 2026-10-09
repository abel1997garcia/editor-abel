/* =====================================================================
   ESCENAS — «La intención y la energía masculina». Usa herramientas/pizarra/libreria.js.
   Cada escena = una ventana de edicion/montaje.json (ventanas.py). Los tiempos salen de la voz con ts()/X()/en().
   Paleta del vídeo: energía masculina = sol (plexo, dorado: «energía solar»), femenina = luna (tercer ojo, índigo),
   intención = garganta. Pieza firma: la flecha (dirección, masculina) que va a la diana (destino, femenina).
   Stickman para dar contexto; silueta grande solo para energía y cuerpo. Revisar con herramientas/pizarra/revisar.mjs.
   ===================================================================== */
COL.masc = C.plexo; COL.fem = C.ojo; COL.int = C.garganta;
const tarjetaVideo = (g, x, y, w, h) => trazo(g, cajaR(x - w / 2, y - h / 2, w, h, 18), { ancho: 6, fill: '#fff' });
const play = (g, x, y, r = 26) => trazo(g, `M${x - r * .5},${y - r * .7} L${x - r * .5},${y + r * .7} L${x + r * .7},${y} Z`, { ancho: 6, color: C.raiz, fill: C.raiz });
const fadeIn = (t, t0, d = .3) => P(t, t0 - .05, d, E.out3);
const ceja = (e, txt, color = NEGRO) => { const c = mk('div', 'ceja', e.div, txt); c.style.color = color; return c; };
const pintarCeja = (c, t, t0, x, y) => { c.style.opacity = fadeIn(t, t0); c.style.transform = `translate(${x}px,${y}px) translate(-50%,-50%)`; };
const ver = (el, t, t0, t1 = 1e9) => pt(el, t, { o: t < t1 ? 1 : clamp(1 - (t - t1) / .25) });   // texto que se va

/* sol (energía masculina) y luna (femenina): se dibujan solos; los rayos del sol giran despacio */
function sol(e, color = C.plexo) { return { c: trazo(e.svg, '', { ancho: 7, color }), r: [0, 1, 2, 3, 4, 5, 6, 7].map(() => trazo(e.svg, '', { ancho: 7, color })) }; }
function pintarSol(s, t, t0, x, y, R = 70, o = 1) {
  forma(s.c, () => circulo(x, y, R)); dibujar(s.c, dib(t, t0, .45), o);
  s.r.forEach((r, i) => { const a = i * Math.PI / 4 + t * .25, r0 = R + 22, r1 = R + 58 + 6 * Math.sin(t * 4 + i);
    forma(r, () => linea(x + r0 * Math.cos(a), y + r0 * Math.sin(a), x + r1 * Math.cos(a), y + r1 * Math.sin(a), 0)); dibujar(r, dib(t, t0 + .3 + i * .04, .2), o); });
}
function luna(e, color = C.ojo) { return trazo(e.svg, '', { ancho: 7, color }); }
function pintarLuna(l, t, t0, x, y, R = 70, o = 1) {
  forma(l, () => `M${x + R * .35},${y - R} A${R},${R} 0 1 0 ${x + R * .35},${y + R} A${R * .78},${R * .78} 0 1 1 ${x + R * .35},${y - R} Z`); dibujar(l, dib(t, t0, .5), o);
}
/* diana (destino) */
function diana(e, color = C.ojo) { return [0, 1, 2].map(() => trazo(e.svg, '', { ancho: 7, color })); }
function pintarDiana(d, t, t0, x, y, R = 150, o = 1) { d.forEach((c, i) => { forma(c, () => circulo(x, y, R * (1 - i * .33))); dibujar(c, dib(t, t0 + i * .12, .4), o); }); }
/* falda triangular sobre un stickman (las mujeres de las historias) */
function vestido(e, color = C.ojo) { return trazo(e.svg, '', { ancho: 6, color, fill: '#fff' }); }
function pintarVestido(v, t, t0, st) { const c = st.cadera, s = st.s;
  forma(v, () => `M${c.x - 14 * s},${c.y - 90 * s} L${c.x - 80 * s},${c.y + 60 * s} L${c.x + 80 * s},${c.y + 60 * s} L${c.x + 14 * s},${c.y - 90 * s} Z`); dibujar(v, dib(t, t0, .35)); }
/* onda entre dos puntos (frecuencia) */
const onda = (x1, x2, y, A, fase, k = 5) => { let d = ''; for (let i = 0; i <= 60; i++) { const x = lerp(x1, x2, i / 60); d += (i ? 'L' : 'M') + x.toFixed(1) + ',' + (y + A * Math.sin(i / 60 * Math.PI * 2 * k + fase)).toFixed(1) + ' '; } return d; };
/* columna de pasos con número */
function paso(e, n, frase, desde, o = {}) { return { n: texto(e, n, en(o.num || frase.replace(/\|[a-z]+/g, '').split(' ')[0], desde) - .05, { tam: o.tam || 72, ax: 50, sonido: false }), tx: X(e, frase, desde, { tam: o.tam || 72, ax: 0, ...o }) }; }
function pintarPaso(p, t, x, y, o = 1) { pt(p.n, t, { x, y, o }); pt(p.tx, t, { x: x + 70, y, o }); }

/* 1 · PROMESA: todos los vídeos que veas sobre retención y energía sexual… */
escena('promesa', e => {
  const tit = X(e, 'todos los vídeos que veas', 5.6, { tam: 88, y: 190 });
  const tj = [['beneficios de retención seminal', 7.2], ['la energía sexual|sacro', 9.1]].map(([f, d]) => ({ c: tarjetaVideo(e.svg, 0, 0, 1180, 150), p: play(e.svg, 0, 0, 24), tx: X(e, f, d, { tam: 60, ax: 0 }), t0: en(f.split(' ')[0].replace(/\|[a-z]+/, ''), d) }));
  const fondo = [0, 1, 2].map(() => tarjetaVideo(e.svg, 0, 0, 1180, 150));
  return (t, w) => {
    pt(tit, t);
    fondo.forEach((c, i) => { c.setAttribute('transform', `translate(${960 + (i - 1) * 14},${880 + i * 12})`); dibujar(c, dib(t, w.a - .7 + i * .1, .35), .35); });
    tj.forEach((k, i) => { const y = 470 + i * 200, p = P(t, k.t0 - .3, .4, E.back), x = 960 + (1 - p) * 80;
      k.c.setAttribute('transform', `translate(${x},${y})`); k.p.setAttribute('transform', `translate(${x - 510},${y})`);
      dibujar(k.c, dib(t, k.t0 - .3, .3)); dibujar(k.p, dib(t, k.t0 - .1, .2)); pt(k.tx, t, { x: x - 450, y }); });
  };
});

/* 2 · BENEFICIO: el que todo el mundo busca, sobre todo si eres hombre */
escena('beneficio', e => {
  const a = X(e, 'uno de los beneficios', 13.5, { tam: 96, y: 170 }), b = X(e, 'que todo el mundo busca', 14.4, { tam: 64, m: true, y: 290 });
  const gente = [0, 1, 2, 3, 4].map(() => stickman(e.svg)), es = trazo(e.svg, '', { ancho: 7, color: C.plexo, fill: '#fff' });
  const tB = en('busca', 15), tH = en('hombre', 15.5), h = X(e, 'si eres hombre|plexo', 15.8, { tam: 72, y: 1000 });
  suena(tB, 'brillo', .25);
  return (t, w) => {
    pt(a, t); pt(b, t); pt(h, t);
    forma(es, () => estrella(960, 520, 70 + 6 * Math.sin(t * 4))); dibujar(es, dib(t, tB - .2, .4));
    gente.forEach((g, i) => pintarStick(g, t, { x: 700 + i * 130, y: 920, s: .42, pose: i === 2 && t > tH ? mezclaPose(POSES.pie, POSES.arriba, P(t, tH, .4)) : 'pie', t0: w.a - .7 + i * .08, o: i === 2 || t < tH ? 1 : .35 }));
  };
});

/* 3 · ATRAÍDAS: las mujeres se ven más atraídas hacia ti */
escena('atraidas', e => {
  const yo = stickman(e.svg), aura = trazo(e.svg, '', { ancho: 6, color: C.plexo }), ellas = [0, 1].map(() => ({ s: stickman(e.svg), v: vestido(e) }));
  const tit = X(e, 'las mujeres|ojo', 23.2, { tam: 96, y: 170 }), b = X(e, 'se ven más atraídas', 24.1, { tam: 80, y: 990 });
  const tM = en('mujeres', 23.2), tA = en('atraídas', 24.4), ojos = emoji(e, '👀', 90, tA);
  const fls = [0].map(() => fl(e.svg, 0, 0, 1, 1, { color: C.ojo }));
  return (t, w) => {
    pt(tit, t); pt(b, t);
    const st = pintarStick(yo, t, { x: 680, y: 880, s: .55, pose: 'pie', t0: w.a - .7 });
    forma(aura, () => circulo(st.cabeza.x, st.cabeza.y, 62 + 6 * Math.sin(t * 5))); dibujar(aura, dib(t, tA, .4), .8);
    ellas.forEach((k, i) => { const x = 1200 + i * 220, s2 = pintarStick(k.s, t, { x, y: 880, s: .5, pose: 'pie', t0: tM - .3 + i * .15 }); pintarVestido(k.v, t, tM + i * .15, s2); });
    fls.forEach((f, i) => { forma(f, () => flecha(1110, 600, 850, 600)); dibujar(f, dib(t, tA - .1 + i * .1, .4)); });
    pe(ojos, t, tA, 1300, 380);
  };
});

/* 4 · HOMBRES: afecta más a los hombres */
escena('hombres', e => {
  const tit = X(e, 'afecta más a los hombres', 31.8, { tam: 88, y: 200 });
  const lH = texto(e, 'hombres', 0, { tam: 64, ax: 0, sonido: false }), lM = texto(e, 'mujeres', 0, { tam: 64, ax: 0, sonido: false });
  const bH = trazo(e.svg, '', { ancho: 60, color: C.plexo }), bM = trazo(e.svg, '', { ancho: 60, color: C.ojo }), eje = trazo(e.svg, '', { ancho: 6 });
  const tH = en('hombres', 32.7), pg = X(e, 'por lo general', 30, { tam: 60, m: true, gris: true, y: 990 });
  return (t, w) => {
    pt(tit, t); pt(pg, t); pt(lH, t, { x: 420, y: 470, o: fadeIn(t, w.a - .5) }); pt(lM, t, { x: 420, y: 740, o: fadeIn(t, w.a - .3) });
    forma(eje, () => linea(400, 380, 400, 860, 0)); dibujar(eje, dib(t, w.a - .7, .4));
    const vH = .2 + .35 * P(t, en('aspecto', 30.8), .8, E.out3) + .4 * P(t, tH - .2, .6, E.out3) + .01 * Math.sin(t * 3);
    bH.setAttribute('d', `M440,580 L${(440 + 1140 * vH).toFixed(1)},580`); dibujar(bH, 1);
    bM.setAttribute('d', `M440,850 L${(440 + 1140 * .32).toFixed(1)},850`); dibujar(bM, dib(t, w.a - .3, .4));
  };
});

/* 5 · EN ESTE VÍDEO 1: el porqué del beneficio */
escena('envideo', e => {
  const cj = ceja(e, 'EN ESTE VÍDEO', C.garganta), n1 = texto(e, '1', en('por', 35.5) - .05, { tam: 120, x: 460, y: 330, sonido: false });
  const tit = X(e, 'el porqué del beneficio', 35.2, { dice: 'el por qué del beneficio', tam: 96, x: 560, y: 330, ax: 0 });
  const q = texto(e, '?', en('qué', 35.5), { tam: 220, x: 960, y: 640, sonido: false });
  const b = X(e, 'que la gran mayoría de los hombres busca', 37.6, { tam: 60, m: true, gris: true, y: 900 });
  return (t, w) => { pintarCeja(cj, t, w.a - .7, 960, 170); pt(n1, t); pt(tit, t); pt(q, t, { s: 1 + .05 * Math.sin(t * 5) }); pt(b, t); };
});

/* 6 · 2: la esencia de la energía masculina (el sol) */
escena('esencia', e => {
  const cj = ceja(e, 'EN ESTE VÍDEO', C.garganta), n2 = texto(e, '2', 0, { tam: 120, x: 460, y: 330, sonido: false });
  const tit = X(e, 'la energía masculina|plexo', 42.0, { dice: 'de la energía masculina', tam: 96, x: 560, y: 330, ax: 0 });
  const s = sol(e), h = X(e, 'un hombre como dios manda', 44.5, { tam: 72, y: 920 });
  suena(en('energía', 42), 'swell', .25);
  return (t, w) => { pintarCeja(cj, t, w.a - .7, 960, 170); pt(n2, t, { o: fadeIn(t, w.a - .7) }); pt(tit, t); pintarSol(s, t, en('energía', 42) - .2, 960, 640, 80); pt(h, t); };
});

/* 7 · INTENCIÓN (pieza firma): la flecha de la intención va a la diana */
escena('intencion', e => {
  const tit = X(e, 'la intención|garganta', 47.3, { tam: 120, y: 220 }), sub = X(e, 'con lo que haces algo', 48.1, { tam: 64, m: true, y: 340 });
  const d = diana(e, C.garganta), f = trazo(e.svg, '', { ancho: 9, color: C.garganta }), imp = X(e, 'lo más importante|garganta de todo', 52.5, { dice: 'lo más importante de todo', tam: 80, y: 960 });
  const tP = en('pones', 50), tI = en('importante', 52.5);
  suena(tI, 'golpe', .35);
  return (t, w) => {
    pt(tit, t); pt(sub, t); pt(imp, t);
    pintarDiana(d, t, w.a - .7, 1350, 650, 150);
    const k = P(t, tP - .2, tI - tP + .2, E.io3), x2 = lerp(560, 1340, k);
    forma(f, () => flecha(460, 650, x2, 650, 34)); dibujar(f, k > 0 ? 1 : 0);
  };
});

/* 8 · ENERGÍA: detrás de la intención va la energía */
escena('energia', e => {
  const iA = texto(e, 'Intención|garganta', 0, { tam: 96, x: 560, y: 540, sonido: false }), iB = X(e, 'Energía|plexo', 56.9, { dice: 'energía', tam: 96, x: 1370, y: 540 });
  const mA = marco(e, iA, { color: C.garganta }), mB = marco(e, iB, { color: C.plexo }), u = unir(e, iA, iB), dt = X(e, 'detrás va', 56.3, { tam: 64, m: true, y: 380 });
  return (t, w) => { pt(iA, t, { o: fadeIn(t, w.a - .7) }); pintarMarco(mA, t, w.a - .6); pt(dt, t); pintarUnion(u, t, en('detrás', 56) - .1, .6); pt(iB, t); pintarMarco(mB, t, iB._t[0] - .1); };
});

/* 9 · DIVIDIDO: el mundo, mitad masculina (sol) y mitad femenina (luna) */
escena('dividido', e => {
  const cir = trazo(e.svg, circulo(960, 560, 250), { ancho: 8 }), mitad = trazo(e.svg, '', { ancho: 8 });
  const tit = X(e, 'el mundo', 62.4, { tam: 96, y: 150 }), d = X(e, 'está dividido', 64.3, { tam: 72, m: true, x: 960, y: 250 });
  const s = sol(e), l = luna(e), tM = en('masculina', 65.6), tF = en('femenina', 67);
  const lm = X(e, 'masculina|plexo', 65.6, { dice: 'energía masculina', tam: 72, x: 700, y: 930 }), lf = X(e, 'femenina|ojo', 66.9, { dice: 'energía femenina', tam: 72, x: 1220, y: 930 });
  return (t, w) => {
    pt(tit, t); pt(d, t); dibujar(cir, dib(t, w.a - .7, .6));
    forma(mitad, () => linea(960, 300, 960, 820, 2)); dibujar(mitad, dib(t, en('dividido', 64.3) - .1, .4));
    pintarSol(s, t, tM - .2, 840, 560, 50); pintarLuna(l, t, tF - .2, 1090, 560, 60); pt(lm, t); pt(lf, t);
  };
});

/* 10 · BORRAR: se está intentando borrar las dos partes */
escena('borrar', e => {
  const cir = trazo(e.svg, circulo(960, 560, 250), { ancho: 8 }), mitad = trazo(e.svg, '', { ancho: 8 }), s = sol(e), l = luna(e);
  const goma = trazo(e.svg, '', { ancho: 6, color: C.raiz, fill: '#fff' });
  const tit = X(e, 'se está intentando borrar|raiz', 75.4, { tam: 88, y: 150 });
  const b = X(e, 'esas dos partes', 77.2, { tam: 64, m: true, y: 900 }), c = X(e, 'dentro de cada persona', 78.7, { tam: 64, y: 990 });
  const tB = en('borrar', 76.3);
  suena(tB, 'barrido', .3);
  return (t, w) => {
    pt(tit, t); pt(b, t); pt(c, t); dibujar(cir, dib(t, w.a - .7, .5));
    const k = P(t, tB, 1.6, E.io3), o = 1 - .75 * k;
    forma(mitad, () => linea(960, 300, 960, 820, 2)); dibujar(mitad, dib(t, w.a - .6, .3), o);
    pintarSol(s, t, w.a - .5, 840, 560, 50, o); pintarLuna(l, t, w.a - .4, 1090, 560, 60, o);
    const y = 300 + 520 * k + 30 * Math.sin(k * Math.PI * 6);
    forma(goma, () => cajaR(900, y - 40, 120, 80, 14)); dibujar(goma, dib(t, tB - .3, .3));
  };
});

/* 11 · MEZCLADAS: en los hombres predomina la masculina; en las mujeres, la femenina */
escena('mezcladas', e => {
  const hom = stickman(e.svg), muj = stickman(e.svg), v = vestido(e);
  const lH = X(e, 'en los hombres', 91.7, { tam: 64, x: 640, y: 260 }), lM = X(e, 'en las mujeres', 95.4, { tam: 64, x: 1280, y: 260 });
  const pr = X(e, 'predomina', 93.6, { tam: 72, gris: true, y: 140 }), qH = X(e, 'más que la femenina', 94, { dice: 'más que la energía femenina', tam: 56, m: true, x: 640, y: 350 }), qM = X(e, 'más que la masculina', 97.1, { tam: 56, m: true, x: 1280, y: 350 });
  const B = [['plexo', 640, 880, .9, 93.6], ['ojo', 640, 950, .3, 93.6], ['plexo', 1280, 880, .3, 95.6], ['ojo', 1280, 950, .9, 95.6]].map(([c, x, y, v0, d]) => ({ b: trazo(e.svg, '', { ancho: 40, color: C[c] }), x, y, v0, t0: d }));
  return (t, w) => {
    pt(lH, t); pt(lM, t); pt(pr, t); pt(qH, t); pt(qM, t);
    pintarStick(hom, t, { x: 640, y: 790, s: .5, pose: 'pie', t0: w.a - .7 });
    const s2 = pintarStick(muj, t, { x: 1280, y: 790, s: .5, pose: 'pie', t0: en('mujeres', 95.4) - .4 }); pintarVestido(v, t, en('mujeres', 95.4) - .2, s2);
    B.forEach(k => { const vv = .1 + (k.v0 - .1) * P(t, k.t0, .6, E.out3); k.b.setAttribute('d', `M${k.x - 200},${k.y} L${(k.x - 200 + 400 * vv).toFixed(1)},${k.y}`); dibujar(k.b, t > k.t0 - .3 ? 1 : 0); });
  };
});

/* 12 · ¿POR QUÉ?: ¿te has parado a pensar por qué sucede? */
escena('porque', e => {
  const f = stickman(e.svg), q = X(e, '¿Por qué?', 134.4, { dice: 'por qué', tam: 150, x: 1180, y: 420 });
  const b = X(e, 'te has parado a pensar', 135.6, { tam: 64, m: true, x: 1180, y: 600 });
  const qs = [0, 1, 2].map(i => texto(e, '?', en('pensar', 136) + i * .15, { tam: 90, gris: true, sonido: false }));
  return (t, w) => {
    const st = pintarStick(f, t, { x: 620, y: 960, s: .62, pose: 'manosCabeza', t0: w.a - .7 }); pt(q, t, { s: 1 + .03 * Math.sin(t * 6) }); pt(b, t);
    qs.forEach((k, i) => pt(k, t, { x: st.cabeza.x - 120 + i * 120, y: st.cabeza.y - 140 - (i % 2) * 40 + 8 * Math.sin(t * 3 + i) }));
  };
});

/* 13 · POLOS: masculino y femenino, cada uno donde tiene que estar → tensión */
escena('polos', e => {
  const s = sol(e), l = luna(e), ondas = [0, 1, 2].map(() => trazo(e.svg, '', { ancho: 6, color: C.corona }));
  const tit = X(e, 'los polos', 144.7, { tam: 110, y: 160 });
  const lm = X(e, 'masculina|plexo', 146.2, { dice: 'energía masculina', tam: 64, x: 520, y: 740 }), lf = X(e, 'femenina|ojo', 147.1, { dice: 'energía femenina', tam: 64, x: 1400, y: 740 });
  const an = X(e, 'bien anclados|ok', 150.7, { dice: 'están bien anclados', tam: 88, y: 940 }), ancla = emoji(e, '⚓', 90, en('anclados', 151));
  return (t, w) => {
    pt(tit, t); pt(lm, t); pt(lf, t); pt(an, t);
    pintarSol(s, t, w.a - .7, 520, 520, 70); pintarLuna(l, t, w.a - .5, 1400, 520, 80);
    ondas.forEach((o, i) => { forma(o, () => onda(660, 1290, 470 + i * 50, 18 + 10 * Math.sin(t * 2 + i), t * 8 + i, 6)); dibujar(o, dib(t, en('femenina', 147) + .2 + i * .1, .5), .8); });
    pe(ancla, t, en('anclados', 151), 960, 780);
  };
});

/* 14 · SE DESCONECTA: la batería se vacía con cada palabra → pierde energía masculina */
escena('desconecta', e => {
  const f = stickman(e.svg), bat = trazo(e.svg, cajaR(1360, 330, 170, 340, 20), { ancho: 7 }), tapa = trazo(e.svg, cajaR(1410, 300, 70, 30, 8), { ancho: 6 }), nivel = trazo(e.svg, '', { ancho: 4, color: C.plexo, fill: C.plexo });
  const L = ['se desconecta', 'se anestesia', 'se desenergiza'].map((p, i) => ({ el: X(e, p, 158.8 + i * 1.3, { tam: 64, ax: 0 }), t0: en(p.split(' ')[1], 158.8 + i * 1.3) }));
  const tit = X(e, 'pierde energía masculina|plexo', 165.9, { tam: 80, y: 940 }), tn = X(e, 'al ceder ante la tentación', 163.6, { tam: 56, m: true, gris: true, ax: 0 });
  return (t, w) => {
    const st = pintarStick(f, t, { x: 500, y: 790, s: .5, pose: mezclaPose(POSES.pie, POSES.hundido, P(t, L[2].t0, .6)), t0: w.a - .7 });
    L.forEach((k, i) => pt(k.el, t, { x: 700, y: 360 + i * 130 }));
    dibujar(bat, dib(t, w.a - .7, .5)); dibujar(tapa, dib(t, w.a - .5, .2));
    const n = 3 - L.filter(k => t > k.t0).length - (t > en('pierde', 165.9) ? .7 : 0), v = Math.max(.05, n / 3 * .95);
    const top = 650 - 300 * v; nivel.setAttribute('d', cajaR(1380, top, 130, 650 - top, 12)); nivel.setAttribute('stroke', v < .4 ? C.raiz : C.plexo); nivel.setAttribute('fill', v < .4 ? C.raiz : C.plexo); dibujar(nivel, t > w.a - .4 ? 1 : 0);
    pt(tit, t); pt(tn, t, { x: 700, y: 760 });
  };
});

/* 15 · ENERGÍA SOLAR LATENTE */
escena('solar', e => {
  const s = sol(e), tit = X(e, 'energía solar|plexo latente', 174, { dice: 'energía solar latente', tam: 104, y: 900 });
  const tL = en('latente', 175);
  return (t, w) => { const k = 1 + .08 * Math.sin((t - tL) * 6) * (t > tL); pintarSol(s, t, w.a - .7, 960, 470, 130 * k); pt(tit, t); };
});

/* 16 · TRANSMUTAS: te la quedas, la subes y la usas → 1: más energía (silueta) */
escena('transmuta', e => {
  const sl = silueta(e.svg), pto = trazo(e.svg, '', { ancho: 14, color: C.plexo }), sube = trazo(e.svg, '', { ancho: 8, color: C.plexo });
  const a = X(e, 'la transmutas|plexo', 181.2, { tam: 96, x: 1260, y: 250 }), b = X(e, 'te la quedas', 182.8, { tam: 64, m: true, x: 1260, y: 380 }), c = X(e, 'y la usas', 183.6, { tam: 64, m: true, x: 1260, y: 470 });
  const n = texto(e, '1', en('uno', 188) - .05, { tam: 110, x: 1000, y: 760, sonido: false }), m = X(e, 'más energía|plexo', 188.8, { dice: 'tener más energía', tam: 88, x: 1080, y: 760, ax: 0 });
  const tT = en('transmutas', 181.2);
  suena(tT, 'subida', .3);
  return (t, w) => {
    const x = 640, y = 1040, s = .95; pintarSilueta(sl, t, { x, y, s, t0: w.a - .7 });
    const c0 = centroSil(x, y, s, 'sacro'), c1 = centroSil(x, y, s, 'corazon'), k = P(t, tT, 1.2, E.io3), cy = lerp(c0.y, c1.y, k);
    forma(pto, () => circulo(x, cy, 12 + 4 * Math.sin(t * 6))); dibujar(pto, dib(t, w.a - .3, .3));
    forma(sube, () => flecha(x + 130, c0.y, x + 130, c1.y)); dibujar(sube, dib(t, tT, 1));
    pt(a, t); pt(b, t); pt(c, t); pt(n, t); pt(m, t);
  };
});

/* 17 · SEGURA: no cede ante sus impulsos y los usa a su favor → persona segura */
escena('segura', e => {
  const f = stickman(e.svg), imp = [0, 1, 2].map(() => trazo(e.svg, '', { ancho: 7, color: C.raiz, k: 'flecha' }));
  const a = X(e, 'no cede ante sus impulsos|raiz', 196.5, { tam: 80, y: 160 }), b = X(e, 'sabe usar esos impulsos a su favor', 198.2, { tam: 60, m: true, y: 270 });
  const c = X(e, 'una persona segura|ok', 203.4, { tam: 96, y: 960 }), mc = marco(e, c, { color: C.corazon });
  const tC = en('cede', 196.5), tU = en('usar', 198.8), mb = X(e, 'muy pero que muy bueno', 201.4, { tam: 64, m: true, y: 380 });
  return (t, w) => {
    pt(a, t); pt(b, t); pt(c, t); pt(mb, t); pintarMarco(mc, t, c._t[0] - .1);
    pintarStick(f, t, { x: 620, y: 830, s: .55, pose: t > tU ? mezclaPose(POSES.pie, POSES.arriba, P(t, tU, .5)) : 'pie', t0: w.a - .7 });
    imp.forEach((r, i) => { const t0 = tC - .3 + i * .3, k = P(t, t0, .5, E.out3), x = lerp(1520, 860, k) + (t > tU ? 300 * P(t, tU, .6) : 0), y = 520 + i * 90;
      forma(r, () => `M${x + 160},${y} L${x + 110},${y - 22} L${x + 60},${y + 22} L${x},${y}`); dibujar(r, t > t0 ? 1 : 0, 1 - P(t, tU + .4, .3)); });
  };
});

/* 18 · FRECUENCIA: atraes a la persona que está en tu misma frecuencia */
escena('frecuencia', e => {
  const yo = stickman(e.svg), otro = stickman(e.svg), w1 = trazo(e.svg, '', { ancho: 7, color: C.corona });
  const a = X(e, 'nunca se trata de la otra persona', 220.6, { tam: 72, y: 160 }), b = X(e, 'tú atraes', 222.7, { tam: 96, y: 290 });
  const c = X(e, 'la misma frecuencia|corona', 224.8, { tam: 88, y: 970 });
  const tF = en('frecuencia', 225);
  return (t, w) => {
    pt(a, t); pt(b, t); pt(c, t);
    pintarStick(yo, t, { x: 560, y: 860, s: .5, pose: 'pie', t0: w.a - .7 }); pintarStick(otro, t, { x: 1360, y: 860, s: .5, pose: 'pie', t0: en('atraes', 222.7) - .2 });
    forma(w1, () => onda(680, 1240, 640, 28, t * 7, 5)); dibujar(w1, dib(t, tF - .4, .6));
  };
});

/* 19 · EMOCIÓN: vergüenza, culpa, arrepentimiento vibran → lo proyectas en la realidad (silueta) */
escena('emocion', e => {
  const sl = silueta(e.svg), ond = [0, 1, 2].map(() => trazo(e.svg, '', { ancho: 6, color: C.raiz })), real = trazo(e.svg, '', { ancho: 7 }), haz = [0, 1].map(() => trazo(e.svg, '', { ancho: 5, color: C.raiz }));
  const L = ['vergüenza', 'culpabilidad', 'arrepentimiento'].map((p, i) => X(e, p + '|raiz', 232 + i * .7, { dice: p, tam: 64 }));
  const vi = X(e, 'eso vibra', 234.6, { tam: 64, x: 1400, y: 800 });
  const re = X(e, 'la realidad', 238.6, { tam: 64, x: 1400, y: 500 }), pr = X(e, 'vas a proyectar', 237.9, { tam: 64, m: true, y: 1000 });
  const tV = en('vibra', 234.6), tP = en('proyectar', 237.9);
  suena(tP, 'barrido', .25);
  return (t, w) => {
    const x = 900, y = 900, s = .75; pintarSilueta(sl, t, { x, y, s, t0: w.a - .7 });
    L.forEach((el, i) => pt(el, t, { x: 560, y: 340 + i * 130 }));
    const c = centroSil(x, y, s, 'plexo');
    ond.forEach((o, i) => { const r = 40 + ((t - tV) * 60 + i * 25) % 75; forma(o, () => circulo(c.x, c.y, r)); dibujar(o, t > tV ? 1 : 0, t > tV ? 1 - r / 125 : 0); });
    forma(real, () => caja(1220, 380, 360, 240)); dibujar(real, dib(t, tP - .3, .5)); pt(re, t); pt(vi, t); pt(pr, t);
    haz.forEach((h, i) => { forma(h, () => linea(c.x + 90, c.y, 1200, 410 + i * 180, 0)); dibujar(h, dib(t, tP, .4)); });
  };
});

/* 20 · MESES: uno, dos meses, no solo retener: transmutar → ejercicio, leer, emprender */
escena('meses', e => {
  const cal = trazo(e.svg, cajaR(420, 200, 320, 260, 22), { ancho: 7, fill: '#fff' }), bar = trazo(e.svg, linea(420, 270, 740, 270, 0), { ancho: 7 });
  const m1 = X(e, '1 mes', 255.4, { dice: 'un mes', tam: 72, x: 580, y: 370 }), m2 = X(e, '2 meses', 256.1, { dice: 'dos meses', tam: 72, x: 580, y: 370 });
  const r = X(e, 'retener', 258.3, { tam: 72, gris: true, x: 1180, y: 260 }), tach = trazo(e.svg, '', { ancho: 9, color: GRIS }), tr = X(e, 'transmutar|plexo', 259.5, { tam: 88, x: 1180, y: 390 });
  const I = [['🏋️', 'ejercicio', 261.2], ['📖', 'leer', 262.2], ['💻', 'emprender', 263.1]].map(([ch, p, d], i) => ({ em: emoji(e, ch, 110, en(p, d)), tx: X(e, p, d, { tam: 60, m: true }), t0: en(p, d), x: 640 + i * 320 }));
  const t2 = en('meses', 256.1), tS = en('sino', 258.7);
  return (t, w) => {
    dibujar(cal, dib(t, w.a - .7, .5)); dibujar(bar, dib(t, w.a - .4, .3));
    pt(m1, t, { o: t < t2 - .1 ? 1 : 0 }); pt(m2, t); pt(r, t); pt(tr, t);
    forma(tach, () => linea(1050, 262, 1310, 255, 1)); dibujar(tach, dib(t, tS, .3));
    I.forEach(k => { pe(k.em, t, k.t0, k.x, 720); pt(k.tx, t, { x: k.x, y: 860 }); });
  };
});

/* 21 · ANCLADO: más anclado, más energía, más presencia, más confianza */
escena('anclado', e => {
  const F = [['más anclado|plexo', 'anclado'], ['más energía|plexo', 'energía'], ['más presencia|plexo', 'presencia'], ['más confianza|plexo', 'confianza']].map(([f, p]) => filaLista(e, f, en(p, 269), { tam: 80 }));
  const st = stickman(e.svg);
  return (t, w) => {
    F.forEach((f, i) => pintarFila(f, t, 380, 280 + i * 160));
    pintarStick(st, t, { x: 1420, y: 900, s: .55, pose: mezclaPose(POSES.pie, POSES.arriba, P(t, F[3].t0, .5)), t0: w.a - .7 });
  };
});

/* 22 · POLARIDAD (pieza firma): el hombre pone la dirección (flecha), la mujer el destino (diana) */
escena('polaridad', e => {
  const s = sol(e), d = diana(e), f = trazo(e.svg, '', { ancho: 9, color: C.plexo });
  const a = X(e, 'el hombre pone la dirección|plexo', 287.9, { dice: 'el hombre siempre pone la dirección', tam: 72, y: 170 });
  const b = X(e, 'la mujer pone el objetivo|ojo', 289.9, { tam: 72, y: 950 }), c = X(e, 'o el destino', 291.8, { tam: 64, m: true, x: 1300, y: 790 });
  const tD = en('dirección', 288.9), tO = en('objetivo', 291);
  suena(tO, 'golpe', .3);
  return (t, w) => {
    pt(a, t); pt(b, t); pt(c, t);
    pintarSol(s, t, w.a - .7, 470, 560, 45); pintarDiana(d, t, w.a - .5, 1300, 560, 160);
    const k = P(t, tD - .2, tO - tD + .2, E.io3); forma(f, () => flecha(580, 560, lerp(620, 1290, k), 560, 34)); dibujar(f, k > 0 ? 1 : 0);
  };
});

/* 23 · BALANZA: más ganas de crecer, menos necesidad de aprobación y de mujeres → tu propósito */
escena('balanza', e => {
  const R = [['más ganas de crecer|ok', 'más esas ganas de crecer', 307.9, 1], ['menos necesidad de aprobación', 'menos la necesidad de aprobación', 310.5, 0], ['menos necesidad de mujeres', 'menos necesidad de mujeres', 312.5, 0]].map(([f, d, t0, up]) => ({ tx: X(e, f, t0, { dice: d, tam: 72, ax: 0, gris: !up }), fl: trazo(e.svg, '', { ancho: 8, color: up ? C.corazon : C.raiz }), up }));
  const p = X(e, 'tu propósito|plexo', 315.5, { dice: 'tu propósito', tam: 110, y: 900 }), mp = marco(e, p, { color: C.plexo }), me = X(e, 'vas a estar metido', 314.1, { dice: 'vas a estar como metido', tam: 60, m: true, y: 750 });
  return (t, w) => {
    R.forEach((r, i) => { const y = 250 + i * 160; pt(r.tx, t, { x: 520, y });
      forma(r.fl, () => r.up ? flecha(430, y + 40, 430, y - 40, 24) : flecha(430, y - 40, 430, y + 40, 24)); dibujar(r.fl, dib(t, r.tx._t[0] - .15, .3)); });
    pt(p, t); pt(me, t); pintarMarco(mp, t, p._t[0] - .1);
  };
});

/* 24 · REFLEJO: cuando dejas de necesitar… todo es un reflejo (espejo) */
escena('reflejo', e => {
  const yo = stickman(e.svg), esp = trazo(e.svg, '', { ancho: 8, color: C.corona }), refl = stickman(e.svg);
  const a = X(e, 'dejas de necesitar', 324.2, { tam: 80, y: 160 }), b = X(e, 'todo es un reflejo|corona', 327, { tam: 96, y: 960 }), at = X(e, 'la atención de las mujeres', 325.3, { tam: 60, m: true, gris: true, y: 270 });
  return (t, w) => {
    pt(a, t); pt(b, t); pt(at, t);
    pintarStick(yo, t, { x: 700, y: 820, s: .5, pose: 'señala', t0: w.a - .7 });
    forma(esp, () => `M1250,320 A190,270 0 1 1 1249,320`); dibujar(esp, dib(t, w.a - .6, .6));
    pintarStick(refl, t, { x: 1250, y: 760, s: .4, pose: 'señala', t0: w.a - .2, o: .45 }); refl.g.setAttribute('transform', 'translate(2500,0) scale(-1,1)');
  };
});

/* 25 · ELEVADA: un hombre hecho y derecho, con la energía masculina elevada → ellas lo notan */
escena('elevada', e => {
  const yo = stickman(e.svg), med = medidor(e.svg, 130), ellas = [0, 1].map(() => ({ s: stickman(e.svg), v: vestido(e) }));
  const a = X(e, 'un hombre hecho y derecho', 335.5, { tam: 80, y: 160 }), b = X(e, 'energía masculina elevada|plexo', 337.9, { dice: 'energía masculina elevada', tam: 64, x: 960, y: 290 });
  const c = X(e, 'te vean', 341.9, { tam: 64, x: 1320, y: 690 });
  const tE = en('elevada', 338.8), tM = en('mujeres', 340.7);
  return (t, w) => {
    pt(a, t); pt(b, t); pt(c, t);
    pintarStick(yo, t, { x: 640, y: 940, s: .55, pose: 'pie', t0: w.a - .7 });
    pintarMedidor(med, t, w.a - .6, 1300, 560, .15 + .8 * P(t, tE - .3, .7, E.out3));
    ellas.forEach((k, i) => { const s2 = pintarStick(k.s, t, { x: 1220 + i * 200, y: 990, s: .34, pose: 'pie', t0: tM - .3 + i * .12 }); pintarVestido(k.v, t, tM + i * .12, s2); });
  };
});

/* 26 · EMANAS: es todo inconsciente, la frecuencia que emanas (ondas) */
escena('emanas', e => {
  const yo = stickman(e.svg), ond = [0, 1, 2, 3].map(() => trazo(e.svg, '', { ancho: 6, color: C.corona }));
  const a = X(e, 'todo inconsciente', 348.9, { dice: 'es todo inconsciente', tam: 88, y: 160 }), b = X(e, 'la frecuencia que tú emanas|corona', 350.8, { tam: 72, y: 970 });
  return (t, w) => {
    pt(a, t); pt(b, t);
    const st = pintarStick(yo, t, { x: 960, y: 820, s: .5, pose: 'pie', t0: w.a - .7 }), cy = (st.cabeza.y + st.cadera.y) / 2;
    ond.forEach((o, i) => { const r = 110 + ((t - w.a) * 80 + i * 45) % 180; forma(o, () => circulo(960, cy, r)); dibujar(o, t > w.a - .3 ? 1 : 0, 1 - r / 300); });
  };
});

/* 27 · HOGAR: el hombre pone la casa; la mujer la convierte en un hogar: puro amor */
escena('hogar', e => {
  const casa = trazo(e.svg, '', { ancho: 8 }), cor = trazo(e.svg, '', { ancho: 8, color: C.corazon, fill: '#fff' });
  const a = X(e, 'el hombre pone la casa|plexo', 367.5, { dice: 'el hombre puede poner la casa', tam: 72, y: 160 }), b = X(e, 'un hogar|corazon', 370.6, { tam: 88, y: 960 });
  const c = X(e, 'puro amor|corazon', 372.6, { tam: 72, x: 1420, y: 560 });
  const tC = en('casa', 368.4), tH = en('hogar', 370.8);
  return (t, w) => {
    pt(a, t); pt(b, t); pt(c, t);
    forma(casa, () => `M700,800 L700,560 L900,400 L1100,560 L1100,800 Z M860,800 L860,690 L940,690 L940,800`); dibujar(casa, dib(t, Math.min(tC, w.a + .1) - .4, .8));
    const k = lerp(.6, 1, P(t, tH, .4, E.back)) * (1 + .05 * Math.sin(t * 6)), x = 900, y = 600;
    forma(cor, () => `M${x},${y + 50 * k} C${x - 90 * k},${y - 10 * k} ${x - 50 * k},${y - 80 * k} ${x},${y - 40 * k} C${x + 50 * k},${y - 80 * k} ${x + 90 * k},${y - 10 * k} ${x},${y + 50 * k} Z`); dibujar(cor, dib(t, tH - .1, .4));
  };
});

/* 28 · MUJER: amor, buenas relaciones, familia, amigos ✓ */
escena('mujer', e => {
  const st = stickman(e.svg), v = vestido(e);
  const F = [['tiene amor|corazon', 'amor'], ['buenas relaciones', 'buenas'], ['su familia', 'familia'], ['sus amigos', 'amigos']].map(([f, p]) => filaLista(e, f, en(p, 392.5), { tam: 64 }));
  return (t, w) => {
    const s2 = pintarStick(st, t, { x: 600, y: 900, s: .55, pose: mezclaPose(POSES.pie, POSES.arriba, P(t, F[3].t0, .5)), t0: w.a - .7 }); pintarVestido(v, t, w.a - .5, s2);
    F.forEach((f, i) => pintarFila(f, t, 880, 300 + i * 150));
  };
});

/* 29 · OBJETIVOS: más energía, motivación, objetivos… y una parte de ti: «¿y si atraigo mujeres?» */
escena('objetivos', e => {
  const F = [['más energía|plexo', 'energía'], ['más motivación', 'motivación'], ['más objetivos', 'objetivos']].map(([f, p]) => filaLista(e, f, en(p, 416.3), { tam: 72 }));
  const st = stickman(e.svg), bo = bocadillo(e, 'y si atraigo a mujeres', ts('y si atraigo a personas a mujeres', 422.5).filter((_, i) => [0, 1, 2, 5, 6].includes(i)), { tam: 60 });
  const m = X(e, 'pues mejor que mejor', 424.4, { tam: 60, m: true, x: 640, y: 960 }), guino = emoji(e, '😏', 90, en('mujeres', 423.8)), pa = X(e, 'una parte de ti', 421, { tam: 60, m: true, x: 1250, y: 470 });
  return (t, w) => {
    F.forEach((f, i) => pintarFila(f, t, 350, 260 + i * 140));
    const s2 = pintarStick(st, t, { x: 1300, y: 1040, s: .4, pose: 'pie', t0: w.a - .7 });
    pintarBocadillo(bo, t, bo.tx._t[0] - .2, 1110, 650, 1290, s2.cabeza.y - 60);
    pt(m, t); pt(pa, t); pe(guino, t, en('mujeres', 423.8), 1520, 850);
  };
});

/* 30 · APEGOS: el paso definitivo hacia tu mejor versión: soltar los apegos (✂️) */
escena('apegos', e => {
  const esc = trazo(e.svg, '', { ancho: 8 }), f = stickman(e.svg), cuerdas = [0, 1].map(() => trazo(e.svg, '', { ancho: 6, color: C.raiz }));
  const a = X(e, 'el paso definitivo', 427, { tam: 64, m: true, x: 1260, y: 230 }), b = X(e, 'tu mejor versión|corona', 428.7, { tam: 88, x: 1260, y: 340 });
  const c = X(e, 'soltar todos los apegos|raiz', 430.6, { tam: 80, y: 970 });
  const tA = en('apegos', 431.7), tij = emoji(e, '✂️', 90, tA);
  suena(tA + .1, 'corte', .3);
  return (t, w) => {
    pt(a, t); pt(b, t); pt(c, t);
    forma(esc, () => 'M400,860 L560,860 L560,760 L720,760 L720,660 L880,660 L880,560 L1040,560 L1040,460'); dibujar(esc, dib(t, w.a - .7, .6));
    const k = P(t, tA + .2, 1.2, E.io3), x = lerp(640, 960, k), y = lerp(760, 560, k);
    const st = pintarStick(f, t, { x, y, s: .3, pose: 'camina', t0: w.a - .6 });
    cuerdas.forEach((c2, i) => { forma(c2, () => linea(st.cadera.x, st.cadera.y, 420 + i * 50, 1000, 4)); dibujar(c2, dib(t, w.a - .4, .4), 1 - P(t, tA + .1, .3)); });
    pe(tij, t, tA, 380, 900);
  };
});

/* 31 · VALIDACIÓN: falso ego: «las mujeres me están viendo» = validación */
escena('validacion', e => {
  const st = stickman(e.svg), bo = bocadillo(e, 'las mujeres me están viendo', ts('las mujeres me están viendo', 465.9), { tam: 60 });
  const eg = X(e, 'es un ego', 464.7, { tam: 64, m: true, gris: true, y: 280 }), a = X(e, 'falso ego|raiz', 463.3, { tam: 110, y: 160 }), b = X(e, 'validación|raiz', 468, { tam: 96, y: 960 }), mb = marco(e, b, { color: C.raiz });
  return (t, w) => {
    pt(a, t); pt(eg, t); const s2 = pintarStick(st, t, { x: 640, y: 850, s: .46, pose: 'arriba', t0: w.a - .7 });
    pintarBocadillo(bo, t, bo.tx._t[0] - .2, 1120, 460, s2.cabeza.x + 60, s2.cabeza.y - 40);
    pt(b, t); pintarMarco(mb, t, b._t[0] - .1);
  };
});

/* 32 · PATRONES: abres la puerta y vuelves a los patrones anteriores (bucle) */
escena('patrones', e => {
  const marcoP = trazo(e.svg, cajaR(560, 360, 280, 460, 10), { ancho: 8 }), hoja = trazo(e.svg, '', { ancho: 7, fill: '#fff' }), lp = trazo(e.svg, bucle(1320, 560, 170), { ancho: 9, color: C.raiz }), f = fl(e.svg, 0, 0, 1, 1);
  const a = X(e, 'abriendo la puerta', 511.9, { tam: 80, y: 160 }), b = X(e, 'patrones anteriores|raiz', 515, { tam: 64, x: 1320, y: 840 }), c = X(e, 'los hábitos', 516.4, { tam: 60, m: true, gris: true, x: 1320, y: 930 });
  const tP = en('puerta', 512.5), tB = en('patrones', 515);
  return (t, w) => {
    pt(a, t); pt(b, t); pt(c, t); dibujar(marcoP, dib(t, w.a - .7, .5));
    const k = P(t, tP - .1, .6, E.out3), ww = 280 * (1 - .7 * k); forma(hoja, () => `M560,360 L${560 + ww},${380 + 30 * k} L${560 + ww},${800 - 30 * k} L560,820 Z`); dibujar(hoja, dib(t, w.a - .5, .4));
    forma(f, () => flecha(880, 590, 1110, 590)); dibujar(f, dib(t, tB - .4, .4));
    dibujar(lp, dib(t, tB - .2, .6)); lp.setAttribute('transform', `rotate(${(Math.max(0, t - tB) * 60).toFixed(1)} 1320 560)`);
  };
});

/* 33 · ELECCIÓN: ¿lo quiero para algo más (me llena a nivel del ser) o aquí te pillo, aquí te mato? */
escena('eleccion', e => {
  const st = stickman(e.svg), fa = fl(e.svg, 0, 0, 1, 1, { color: C.corazon }), fb = fl(e.svg, 0, 0, 1, 1, { color: C.raiz });
  const a = X(e, '¿lo quiero para algo más?', 526.9, { dice: 'lo quiero para algo más', tam: 80, y: 160 });
  const l1 = X(e, 'me llena|corazon', 528.5, { tam: 80, x: 600, y: 430 }), l2 = X(e, 'a nivel del ser', 529.4, { tam: 56, m: true, x: 600, y: 530 });
  const r1 = X(e, 'aquí te pillo|raiz', 534.4, { tam: 80, x: 1320, y: 430 }), r2 = X(e, 'aquí te mato', 534.9, { tam: 56, m: true, x: 1320, y: 530 });
  const cor = emoji(e, '❤️', 80, en('llena', 528.5)), l3 = X(e, 'de lo que presiento', 531, { tam: 56, m: true, x: 600, y: 610 }), l4 = X(e, 'de su energía', 532.2, { tam: 56, m: true, x: 600, y: 690 });
  const r3 = X(e, 'nos hemos atraído', 535.8, { dice: 'como nos hemos atraído', tam: 56, m: true, x: 1320, y: 610 }), r4 = X(e, 'ya está', 536.9, { tam: 56, m: true, x: 1320, y: 690 });
  return (t, w) => {
    pt(a, t); pt(l1, t); pt(l2, t); pt(r1, t); pt(r2, t); pt(l3, t); pt(l4, t); pt(r3, t); pt(r4, t);
    const s2 = pintarStick(st, t, { x: 960, y: 990, s: .48, pose: 'pie', t0: w.a - .7 });
    forma(fa, () => flecha(890, s2.cabeza.y + 40, 740, s2.cabeza.y + 40)); dibujar(fa, dib(t, l1._t[0] - .3, .4));
    forma(fb, () => flecha(1030, s2.cabeza.y + 40, 1180, s2.cabeza.y + 40)); dibujar(fb, dib(t, r1._t[0] - .3, .4));
    pe(cor, t, en('llena', 528.5), 600, 300);
  };
});

/* 34 · DOS INTENCIONES: elevarte y dar amor ↑ / por ego, intención negativa ↓ */
escena('dosintenciones', e => {
  const st = stickman(e.svg), up = trazo(e.svg, '', { ancho: 9, color: C.corazon }), dn = trazo(e.svg, '', { ancho: 9, color: C.raiz });
  const a = X(e, 'elevarte espiritualmente|corazon', 547.2, { tam: 80, y: 170 }), b = X(e, 'dar amor', 548.8, { tam: 64, m: true, y: 280 }), b2 = X(e, 'compartir un momento bonito', 550.1, { tam: 56, m: true, gris: true, y: 380 });
  const ev = X(e, 'estás evolucionando|corazon', 552.4, { tam: 56, x: 600, y: 560 }), c = X(e, 'por ego|raiz', 554.6, { tam: 96, y: 850 }), d = X(e, 'intención negativa', 555.3, { dice: 'una intención negativa', tam: 64, m: true, y: 960 });
  return (t, w) => {
    pt(a, t); pt(b, t); pt(c, t); pt(d, t); pt(ev, t); pt(b2, t);
    pintarStick(st, t, { x: 960, y: 700, s: .38, pose: 'pie', t0: w.a - .7 });
    forma(up, () => flecha(1320, 620, 1320, 450)); dibujar(up, dib(t, a._t[0] - .1, .4));
    forma(dn, () => flecha(1320, 650, 1320, 780)); dibujar(dn, dib(t, c._t[0] - .2, .4));
  };
});

/* 35 · FUEGO: cuando sientas el impulso: gimnasio, leer, grabar 40 vídeos → ese fuego a tu favor (silueta) */
escena('fuego', e => {
  const sl = silueta(e.svg), fuego = emoji(e, '🔥', 90, en('impulso', 570));
  const I = [['🏋️', 'ir al gimnasio', 570.8], ['📖', 'leer', 572.2], ['🎥', 'grabar 40 vídeos', 572.7]].map(([ch, p, d], i) => ({ em: emoji(e, ch, 90, en(p.split(' ')[0], d)), tx: X(e, p, d, { tam: 56, ax: 0 }), f: fl(e.svg, 0, 0, 1, 1, { color: C.sacro }), t0: en(p.split(' ')[0], d), y: 300 + i * 200 }));
  const a = X(e, 'ese fuego|sacro', 576.2, { tam: 80, x: 1300, y: 920 }), ex = X(e, 'esa energía extra|plexo', 575.3, { tam: 60, m: true, x: 1300, y: 820 }), fav = X(e, 'a tu favor|ok', 578.5, { tam: 64, x: 1300, y: 1015 });
  return (t, w) => {
    const x = 560, y = 1040, s = .9; pintarSilueta(sl, t, { x, y, s, t0: w.a - .7 });
    const c = centroSil(x, y, s, 'sacro'); pe(fuego, t, en('impulso', 570), c.x, c.y);
    fuego.style.transform += ` scale(${(1 + .1 * Math.sin(t * 9)).toFixed(3)})`;
    I.forEach(k => { forma(k.f, () => flecha(c.x + 80, c.y - 20, 960, k.y)); dibujar(k.f, dib(t, k.t0 - .3, .3)); pe(k.em, t, k.t0, 1040, k.y); pt(k.tx, t, { x: 1110, y: k.y }); });
    pt(a, t); pt(ex, t); pt(fav, t);
  };
});

/* 36 · DINÁMICAS SOCIALES: un reflejo de cómo estás tú */
escena('dinamicas', e => {
  const yo = stickman(e.svg), otro = stickman(e.svg), u = [0, 1].map(() => fl(e.svg, 0, 0, 1, 1, { color: C.corona }));
  const a = X(e, 'las dinámicas sociales', 599, { tam: 96, y: 170 }), b = X(e, 'un reflejo|corona', 601.1, { tam: 88, y: 960 });
  return (t, w) => {
    pt(a, t); pt(b, t);
    pintarStick(yo, t, { x: 640, y: 820, s: .5, pose: 'señala', t0: w.a - .7 }); pintarStick(otro, t, { x: 1280, y: 820, s: .5, pose: 'señala', t0: w.a - .5 });
    otro.g.setAttribute('transform', 'translate(2560,0) scale(-1,1)');
    u.forEach((f, i) => { forma(f, () => i ? flecha(1160, 640, 760, 640) : flecha(760, 560, 1160, 560)); dibujar(f, dib(t, en('dinámicas', 599) + i * .3, .4)); });
  };
});

/* 37 · VALOR: no vas a aceptar menos: tu valor, tu trabajo, cómo cuidas tu energía */
escena('valor', e => {
  const a = X(e, 'no vas a aceptar menos|raiz', 606.7, { tam: 88, y: 160 });
  const F = [['tu valor', 'valor'], ['el trabajo que pones', 'trabajo'], ['cómo cuidas tu energía|plexo', 'cuidas']].map(([f, p]) => filaLista(e, f, en(p, 609), { tam: 72 }));
  const dia = emoji(e, '💎', 130, en('valor', 609.5));
  return (t, w) => { pt(a, t); F.forEach((f, i) => pintarFila(f, t, 520, 440 + i * 150)); pe(dia, t, en('valor', 609.5), 1400, 330, 1); };
});

/* 38 · NOVATO: te dejas llevar por las ganas de su atención… sin recibirla */
escena('novato', e => {
  const st = stickman(e.svg), cuerda = trazo(e.svg, '', { ancho: 6, color: C.sacro });
  const a = X(e, 'te dejes llevar un poquito', 637.4, { tam: 80, y: 160 });
  const b = X(e, 'la atención|sacro', 641.4, { tam: 80, x: 1320, y: 470 }), c = X(e, 'de las mujeres', 642, { tam: 60, m: true, x: 1320, y: 610 });
  const d = X(e, 'sin recibirlo', 644.2, { tam: 64, m: true, gris: true, y: 970 }), mb = marco(e, b, { color: C.sacro });
  const tG = en('ganas', 640);
  return (t, w) => {
    pt(a, t); pt(b, t); pt(c, t); pt(d, t); pintarMarco(mb, t, b._t[0] - .1);
    const k = P(t, tG, 3, E.io3), paso = Math.sin((t - tG) * 7) * (k > 0 && k < 1);
    const s2 = pintarStick(st, t, { x: lerp(560, 760, k), y: 880, s: .5, pose: { ...POSES.camina, pI: 6 + 12 * paso, pD: 6 - 12 * paso, bD: 80 }, t0: w.a - .7 });
    forma(cuerda, () => linea(s2.manoD.x, s2.manoD.y, 1060, 500, 6)); dibujar(cuerda, dib(t, tG - .3, .4));
  };
});

/* 39 · DIVINO: crecer, aprovechar al máximo tu energía → el divino masculino / femenino (silueta) */
escena('divino', e => {
  const sl = silueta(e.svg), sube = trazo(e.svg, '', { ancho: 8, color: C.plexo }), corona = [0, 1].map(() => trazo(e.svg, '', { ancho: 7, color: C.corona }));
  const a = X(e, 'crecer como persona', 655.1, { tam: 72, x: 1240, y: 230 }), b = X(e, 'al máximo tu energía|plexo', 656.5, { dice: 'aprovechar al máximo tu energía', tam: 64, m: true, x: 1240, y: 340 });
  const c = X(e, 'divino masculino|plexo', 660, { tam: 76, x: 1240, y: 560 }), d = X(e, 'divino femenino|ojo', 661.2, { tam: 76, x: 1240, y: 680 }), f = X(e, 'en todos lados', 663.5, { tam: 64, m: true, x: 1240, y: 860 });
  const tD = en('divino', 660);
  return (t, w) => {
    const x = 600, y = 1040, s = .95; pintarSilueta(sl, t, { x, y, s, t0: w.a - .7 });
    const c0 = centroSil(x, y, s, 'sacro'), c1 = centroSil(x, y, s, 'corona');
    forma(sube, () => flecha(x + 130, c0.y, x + 130, c1.y + 60)); dibujar(sube, dib(t, en('energía', 657) - .2, 1));
    corona.forEach((k, i) => { forma(k, () => circulo(x, c1.y + 10, 70 + i * 30 + 6 * Math.sin(t * 4 + i))); dibujar(k, dib(t, tD + i * .15, .4), .8); });
    pt(a, t); pt(b, t); pt(c, t); pt(d, t); pt(f, t);
  };
});

/* 40 · GIMNASIO (lo aplicable, paso a paso): 1 calentarte → 2 ir al gimnasio → 3 el mayor peso de tu vida → todo es energía */
escena('gimnasio', e => {
  const cj = ceja(e, 'PRUÉBALO', C.plexo);
  const p1 = paso(e, '1', 'calentarte', 669.9, { tam: 64 }), p2 = paso(e, '2', 'ir al gimnasio', 674.9, { tam: 64 }), p3 = paso(e, '3', 'el mayor peso de tu vida|plexo', 677.9, { dice: 'el mayor peso que hayas levantado en tu vida', num: 'mayor', tam: 64 });
  const st = stickman(e.svg), barra = trazo(e.svg, '', { ancho: 10 }), discos = [0, 1].map(() => trazo(e.svg, '', { ancho: 8, fill: '#fff' }));
  const ex = X(e, 'energía extra|plexo', 680.5, { dice: 'una energía extra', tam: 80, y: 480 }), te = X(e, 'todo es energía|plexo', 681.5, { tam: 120, y: 640 });
  const tL = en('levantar', 677.3), tE = en('energía', 680.5) - .3, fg = emoji(e, '🔥', 80, en('notes', 671.5)), as = X(e, 'acto seguido', 673.4, { tam: 56, m: true, gris: true, x: 900, y: 405, ax: 0 });
  suena(tL + .3, 'golpe-grave', .3);
  return (t, w) => {
    pintarCeja(cj, t, w.a - .7, 960, 150);
    const o = 1 - P(t, tE - .3, .3); pintarPaso(p1, t, 380, 330, o); pintarPaso(p2, t, 380, 480, o); pintarPaso(p3, t, 380, 630, o); pt(as, t, { o }); pe(fg, t, en('notes', 671.5), 1420, 520, o);
    const k = P(t, tL, .8, E.out3), s2 = pintarStick(st, t, { x: 1420, y: 940, s: .45, pose: mezclaPose(POSES.pie, POSES.arriba, k), t0: w.a - .7, o });
    const by = lerp(s2.cadera.y - 40, s2.cabeza.y - 70, k);
    forma(barra, () => linea(1260, by, 1580, by, 0)); dibujar(barra, dib(t, en('gimnasio', 675) - .2, .3), o);
    discos.forEach((d, i) => { forma(d, () => cajaR(i ? 1540 : 1270, by - 50, 30, 100, 8)); dibujar(d, dib(t, en('gimnasio', 675), .3), o); });
    pt(ex, t, { o: t > tE ? 1 : 0 }); pt(te, t, { s: 1 + .04 * bump(t, te._t[0] + .3, .5) });
  };
});

/* 41 · SENTIR: la energía no se ve, pero se siente: ansiedad, estrés, decir que sí queriendo decir que no (silueta) */
escena('sentir', e => {
  const sl = silueta(e.svg), pts = ['plexo', 'garganta'].map(c => trazo(e.svg, '', { ancho: 14, color: C[c] }));
  const a = X(e, 'no se ve', 686.3, { tam: 96, gris: true, x: 640, y: 170 }), b = X(e, 'se siente|corazon', 687.2, { dice: 'sí se siente', tam: 96, x: 1280, y: 170 });
  const L = [['ansiedad|raiz', 692, 560, 480], ['estrés|raiz', 693, 560, 640], ['dices que sí', 694, 1330, 480], ['querías decir que no|garganta', 694.8, 1330, 640]].map(([f, d, x, y]) => ({ el: X(e, f, d, { tam: f.length > 18 ? 56 : 72 }), x, y }));
  return (t, w) => {
    const x = 950, y = 1040, s = .75; pintarSilueta(sl, t, { x, y, s, t0: w.a - .7 });
    pt(a, t); pt(b, t); L.forEach(k => pt(k.el, t, { x: k.x, y: k.y }));
    const c1 = centroSil(x, y, s, 'plexo'), c2 = centroSil(x, y, s, 'garganta');
    forma(pts[0], () => circulo(c1.x, c1.y, 10 + 3 * Math.sin(t * 7))); dibujar(pts[0], dib(t, L[0].el._t[0], .3));
    forma(pts[1], () => circulo(c2.x, c2.y, 10 + 3 * Math.sin(t * 7))); dibujar(pts[1], dib(t, L[3].el._t[0], .3));
  };
});

/* 42 · VOZ INTERIOR: tu voz interior, conectada con tu niño interior → la vida de tus sueños (silueta + niño) */
escena('vozinterior', e => {
  const sl = silueta(e.svg), nino = stickman(e.svg), aura = trazo(e.svg, '', { ancho: 6, color: C.corazon });
  const a = X(e, 'tu voz interior|corona', 700.3, { dice: 'esa voz interior', tam: 88, y: 150 }), b = X(e, 'tu niño interior|corazon', 702.6, { tam: 72, x: 1300, y: 380 });
  const L = [['la vida de tus sueños|corona', 705.6], ['la pareja', 706.4], ['que más te complemente', 708.1]].map(([f, d]) => X(e, f, d, { tam: f.length > 20 ? 56 : 60, m: !f.includes('|') }));
  const tN = en('niño', 702.7);
  return (t, w) => {
    const x = 620, y = 1040, s = .95; pintarSilueta(sl, t, { x, y, s, t0: w.a - .7 });
    const c = centroSil(x, y, s, 'corazon'); pintarStick(nino, t, { x: c.x, y: c.y + 40, s: .13, pose: 'arriba', t0: tN - .2 });
    forma(aura, () => circulo(c.x, c.y, 60 + 6 * Math.sin(t * 4))); dibujar(aura, dib(t, tN, .4), .8);
    pt(a, t); pt(b, t); L.forEach((el, i) => pt(el, t, { x: 1260, y: 560 + i * 120 }));
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
