/* =====================================================================
   ELEMENTOS — «Cómo dejar ir las emociones» v3 (2 primeros min + gancho, modo cara, 05/10/2026)
   Estilo de los vídeos largos de Abel (memoria estilo-videos-largos-stickman):
   - su grabación tal cual (pantalla partida) intercalada con animaciones a pantalla completa;
   - fondo blanco, Inter ExtraBold, destacados con los colores de los centros energéticos;
   - líneas perfiladas que se dibujan solas y NO tiemblan (cada forma con su semilla fija);
   - personaje: la silueta de su boceto (cabeza ovalada + un contorno continuo), sin cara;
   - diagramas variados (flechas, ✓, ✗, estrellas, ecuaciones, índice de pasos, barras), emoji solo una vez;
   - el texto entra con la voz y todo recuadro se mide a partir de su texto.
   ===================================================================== */
const grid = $('grid'), glowN = $('glowN'), glowA = $('glowA'), glowB = $('glowB');
const NS = 'http://www.w3.org/2000/svg', NEGRO = '#111111', GRIS = '#8a8a8a';
// colores de los centros energéticos (en tonos que se leen sobre blanco)
const C = { raiz: '#C8372D', sacro: '#E06A1B', plexo: '#C99A00', corazon: '#1E7A46', garganta: '#1D7FD1', ojo: '#3F3FB5', corona: '#7A3FC4' };
// qué color lleva cada idea en este vídeo
const COL = { mente: C.ojo, emocion: C.sacro, energia: C.plexo, conciencia: C.corona, cuerpo: C.raiz, amor: C.corazon, calma: C.corazon, ok: C.corazon, no: C.raiz };

css(`
@font-face{font-family:InterV;src:url(assets/fonts/Inter-Variable.ttf);font-weight:100 900;font-display:block}
#fondo{background:#fff}
#grid,.glow,#vignette,#noise{display:none}
.tx{font-family:InterV;font-variation-settings:'wght' 800,'opsz' 14;letter-spacing:-.02em;color:${NEGRO};white-space:nowrap;line-height:1.12}
.tx.m{font-variation-settings:'wght' 600,'opsz' 14;letter-spacing:-.01em}
.tx.gris span{color:${GRIS}}
.tx span{display:inline-block;margin-right:.24em}
.tx span:last-child{margin-right:0}
.ceja{font-family:InterV;font-variation-settings:'wght' 700,'opsz' 14;letter-spacing:.22em;font-size:28px;white-space:nowrap}
.emoji{font-family:'Segoe UI Emoji','Noto Color Emoji',sans-serif;line-height:1}
`);

/* ---------- trazos ---------- */
function lienzo() {
  const s = document.createElementNS(NS, 'svg');
  s.setAttribute('width', 1920); s.setAttribute('height', 1080); s.setAttribute('viewBox', '0 0 1920 1080');
  s.style.cssText = 'position:absolute;left:0;top:0;overflow:visible;z-index:3;display:none';
  WORLD.appendChild(s); return s;
}
// pulso de mano determinista. NADA TIEMBLA: cada forma guarda su semilla y la reutiliza en cada fotograma.
let _sem = 5, _n = 1;
const az = () => (_sem = (_sem * 16807) % 2147483647) / 2147483647 - .5;
const linea = (x1, y1, x2, y2, j = 3) => `M${x1},${y1} Q${((x1 + x2) / 2 + az() * j * 2).toFixed(1)},${((y1 + y2) / 2 + az() * j * 2).toFixed(1)} ${x2},${y2}`;
function caja(x, y, w, h) {
  const p = [[x - 4, y + 3], [x + w + 3, y - 2], [x + w - 2, y + h + 3], [x + 3, y + h - 2]];
  let d = ''; for (let i = 0; i < 4; i++) { const a = p[i], b = p[(i + 1) % 4]; d += linea(a[0], a[1], b[0], b[1]) + ' '; }
  return d + linea(p[0][0], p[0][1], p[0][0] + 12, p[0][1] - 1);
}
const circulo = (cx, cy, r) => { const a = -.35, x2 = cx + r * Math.cos(Math.PI + a), y2 = cy + r * Math.sin(Math.PI + a);
  return `M${cx - r},${cy + 2} A${r},${r} 0 1 1 ${cx + r},${cy} A${r},${r} 0 0 1 ${cx - r},${cy} A${r},${r} 0 0 1 ${x2.toFixed(1)},${y2.toFixed(1)}`; };
const flecha = (x1, y1, x2, y2) => { const a = Math.atan2(y2 - y1, x2 - x1), k = 22;
  return linea(x1, y1, x2, y2, 2) + ` M${(x2 - k * Math.cos(a - .5)).toFixed(1)},${(y2 - k * Math.sin(a - .5)).toFixed(1)} L${x2},${y2} L${(x2 - k * Math.cos(a + .5)).toFixed(1)},${(y2 - k * Math.sin(a + .5)).toFixed(1)}`; };
const tick = (x, y, s = 1) => `M${x - 22 * s},${y} L${x - 6 * s},${y + 17 * s} L${x + 26 * s},${y - 22 * s}`;
const cruz = (x, y, s = 1) => `M${x - 18 * s},${y - 18 * s} L${x + 18 * s},${y + 18 * s} M${x + 18 * s},${y - 18 * s} L${x - 18 * s},${y + 18 * s}`;
const estrella = (x, y, r) => { let d = ''; for (let i = 0; i < 10; i++) { const a = -Math.PI / 2 + i * Math.PI / 5, rr = i % 2 ? r * .45 : r;
  d += (i ? 'L' : 'M') + (x + rr * Math.cos(a)).toFixed(1) + ',' + (y + rr * Math.sin(a)).toFixed(1) + ' '; } return d + 'Z'; };
function trazo(g, d, o = {}) {
  const e = document.createElementNS(NS, 'path');
  e.setAttribute('d', d); e.setAttribute('fill', o.fill || 'none'); e.setAttribute('stroke', o.color || NEGRO);
  e.setAttribute('stroke-width', o.ancho || 6); e.setAttribute('stroke-linecap', 'round'); e.setAttribute('stroke-linejoin', 'round');
  e.setAttribute('pathLength', '1'); e._sem0 = (_n++ * 7919) % 2147483646 + 1; g.appendChild(e); return e;
}
// fija la forma de un trazo que se recoloca en cada fotograma (siempre con su misma semilla: no tiembla)
function forma(e, fn) { _sem = e._sem0; e.setAttribute('d', fn()); }
function dibujar(e, p, o = 1) {
  if (p <= 0 || o <= .002) { e.style.opacity = 0; return; }
  e.style.opacity = o.toFixed(3); e.style.strokeDasharray = p >= 1 ? 'none' : '1 1'; e.style.strokeDashoffset = (1 - p).toFixed(4);
}
const dib = (t, t0, dur = .6) => P(t, t0, dur, E.io3);

/* ---------- texto que entra palabra a palabra ----------
   'palabra|color' = palabra destacada en ese color (color = clave de COL o de C). */
function texto(frase, tiempos, o = {}) {
  const pal = frase.split(' ');
  if (tiempos.length > 1 && tiempos.length !== pal.length) console.error(`texto «${frase}»: ${pal.length} palabras y ${tiempos.length} tiempos`);
  const el = mk('div', 'L tx z5' + (o.m ? ' m' : '') + (o.gris ? ' gris' : ''), o.padre || WORLD, pal.map(w => {
    const m = w.match(/^(.*?)\|([a-z]+)(.*)$/); return m ? `<span><b style="font-weight:inherit;color:${COL[m[2]] || C[m[2]]}">${m[1]}</b>${m[3]}</span>` : `<span>${w}</span>`; }).join(''));
  el.style.fontSize = (o.tam || 64) + 'px';
  el._sp = [...el.children]; el._t = pal.map((_, i) => tiempos[Math.min(i, tiempos.length - 1)]);
  return el;
}
function escribir(el, t) {
  el._sp.forEach((s, i) => { const k = P(t, el._t[i] - .05, .32, E.out3);
    s.style.opacity = clamp(k * 1.5).toFixed(3); s.style.transform = `translateY(${((1 - k) * 14).toFixed(1)}px)`; });
}
const medir = el => ({ w: el.offsetWidth, h: el.offsetHeight });

/* ---------- la silueta (boceto de Abel): cabeza ovalada + un contorno continuo, simétrico ---------- */
const MITAD = [[[-30, 128], [-52, 140], [-62, 162]], [[-76, 205], [-86, 300], [-86, 398]], [[-86, 432], [-60, 436], [-58, 404]],
  [[-56, 330], [-50, 262], [-44, 222]], [[-44, 300], [-46, 362], [-44, 424]], [[-48, 505], [-50, 585], [-46, 662]],
  [[-44, 694], [-14, 694], [-12, 662]], [[-10, 592], [-8, 524], [0, 466]]];
function siluetaD() {
  const f = ([x, y]) => `${x},${y}`, m = ([x, y]) => [-x, y], ini = [-13, 122];
  let d = `M${f(ini)} `; MITAD.forEach(([a, b, c]) => d += `C${f(a)} ${f(b)} ${f(c)} `);
  for (let i = MITAD.length - 1; i >= 0; i--) { const [a, b] = MITAD[i]; d += `C${f(m(b))} ${f(m(a))} ${f(m(i ? MITAD[i - 1][2] : ini))} `; }
  return d;
}
const CABEZA = 'M-40,58 C-40,22 -18,4 2,4 C24,4 40,26 40,60 C40,92 22,112 0,112 C-22,112 -40,94 -40,58 Z';
const CENTRO = { corona: -18, ojo: 56, garganta: 140, corazon: 224, plexo: 306, sacro: 384, raiz: 446 };
function silueta(g) { return { cabeza: trazo(g, CABEZA, { ancho: 6.5 }), cuerpo: trazo(g, siluetaD(), { ancho: 6.5 }) }; }
function dibujarSilueta(s, t, t0, o = 1) { dibujar(s.cabeza, dib(t, t0, .45), o); dibujar(s.cuerpo, dib(t, t0 + .25, 1.0), o); }
const grupo = sv => { const g = document.createElementNS(NS, 'g'); sv.appendChild(g); return g; };
const pos = (g, x, y, s = 1) => g.setAttribute('transform', `translate(${x.toFixed(1)},${y.toFixed(1)}) scale(${s.toFixed(4)})`);
// punto de un centro: relleno + anillo que late
function punto(g, x, y, color) { return { p: trazo(g, circulo(x, y, 7), { color, ancho: 10 }), a: trazo(g, circulo(x, y, 22), { color, ancho: 4 }) }; }
function pintarPunto(pt, t, t0) { dibujar(pt.p, t > t0 - .05 ? 1 : 0); dibujar(pt.a, dib(t, t0 - .05, .35), .6 + .4 * Math.sin((t - t0) * 4)); }

/* ---------- cabecera de paso: «PASO 2» + cuatro puntos de progreso + título ---------- */
function cabecera(n, titulo, tiempos, entra, sv) {
  const ceja = mk('div', 'L ceja z5', WORLD, `PASO ${n}`); ceja.style.color = COL.ok;
  const pts = [0, 1, 2, 3].map(i => trazo(sv, circulo(CX - 45 + i * 30, 140, 7), { color: i < n ? COL.ok : '#c8c8c8', ancho: i === n - 1 ? 10 : 5 }));
  return { ceja, pts, tit: texto(titulo, tiempos, { tam: 76 }), entra };
}
function pintarCabecera(c, t) {
  const p = P(t, c.entra, .4, E.out3);
  put(c.ceja, { x: CX, y: 98 - (1 - p) * 10, o: p });
  c.pts.forEach((e, i) => dibujar(e, dib(t, c.entra + .1 + i * .06, .3)));
  escribir(c.tit, t); put(c.tit, { x: CX, y: 210, o: 1 });
}
const apagar = (...els) => els.flat().forEach(off);

/* =====================================================================
   1 · GANCHO (1,9–6,0): sueltas el control y la mente; la emoción recorre el cuerpo
   ===================================================================== */
const s1 = lienzo(), g1 = grupo(s1), sil1 = silueta(g1);
const t1a = texto('Sueltas el control', [0.72, 1.08, 1.26], { tam: 60 }), t1b = texto('Sueltas la mente|mente', [1.92, 2.32, 2.42], { tam: 60 });
const x1a = trazo(s1, '', { color: COL.no, ancho: 7 }), x1b = trazo(s1, '', { color: COL.no, ancho: 7 });
const t1c = texto('y la emoción|emocion se distribuye', [3.32, 4.00, 4.76], { tam: 52, m: true });
const ondas1 = [0, 1, 2, 3, 4].map(() => trazo(g1, '', { color: COL.emocion, ancho: 5 }));
sfx(1.95, 'aire', { vol: .35 }); sfx(2.5, 'tick-suave', { vol: .4 }); sfx(4.0, 'swell', { vol: .3 });
function esc1(t) {
  const on = dentro(t, V.gancho); s1.style.display = on ? 'block' : 'none';
  if (!on) return apagar(t1a, t1b, t1c);
  pos(g1, 1380, 220, 1.05); dibujarSilueta(sil1, t, 1.7);
  [[t1a, x1a, 360, 1.35], [t1b, x1b, 470, 2.45]].forEach(([el, x, y, tc]) => {
    escribir(el, t); put(el, { x: 260, y, ax: 0, o: 1 });
    const { w } = medir(el); forma(x, () => cruz(260 + w + 50, y, 1)); dibujar(x, dib(t, tc, .25));
  });
  escribir(t1c, t); put(t1c, { x: 260, y: 620, ax: 0, o: 1 });
  // la emoción baja por el cuerpo: ondas naranjas que nacen en el pecho y se reparten hacia abajo
  ondas1.forEach((e, i) => {
    if (t < 4.0) return dibujar(e, 0);
    const k = ((t - 4.0) / 1.3 + i / 5) % 1, y = CENTRO.corazon + k * 300;
    forma(e, () => `M-60,${y.toFixed(1)} Q0,${(y + 26).toFixed(1)} 60,${y.toFixed(1)}`); dibujar(e, 1, (1 - k) * P(t, 4.0, .3));
  });
}

/* =====================================================================
   2 · TÍTULO (12,0–14,0): el mecanismo de dejar ir
   ===================================================================== */
const s2 = lienzo();
const t2 = texto('El mecanismo de dejar|emocion ir|emocion', [12.45, 12.59, 13.37, 13.55, 13.89], { tam: 92 });
const c2 = trazo(s2, '', { ancho: 7 }), sub2 = trazo(s2, '', { color: COL.emocion, ancho: 9 });
sfx(12.0, 'aire', { vol: .35 }); sfx(13.55, 'golpe-corto', { vol: .45 });
function esc2(t) {
  const on = dentro(t, V.titulo); s2.style.display = on ? 'block' : 'none';
  if (!on) return apagar(t2);
  escribir(t2, t); put(t2, { x: CX, y: 540, o: 1 });
  const { w, h } = medir(t2);
  forma(c2, () => caja(CX - w / 2 - 70, 540 - h / 2 - 56, w + 140, h + 112)); dibujar(c2, dib(t, 11.8, .9));
  const sp = t2._sp[3].getBoundingClientRect(), sp2 = t2._sp[4].getBoundingClientRect(), r = WORLD.getBoundingClientRect(), k = 1920 / r.width;
  forma(sub2, () => linea((sp.left - r.left) * k, 540 + h / 2 - 2, (sp2.right - r.left) * k, 540 + h / 2 - 4, 2)); dibujar(sub2, dib(t, 13.9, .35));
}

/* =====================================================================
   3 · NIVELES (17,2–23,0): elevar tu energía, tu emoción y atraer niveles de conciencia
   ===================================================================== */
const s3 = lienzo();
const NIV = [['Energía', 'energia', 17.71, .62], ['Emoción', 'emocion', 18.87, .74], ['Conciencia', 'conciencia', 21.55, .92]];
const t3 = texto('Elevar tu nivel', [16.58, 17.21, 17.35], { tam: 70 });
const barras3 = NIV.map(([n, c, t0]) => ({ eje: trazo(s3, ''), barra: trazo(s3, '', { color: COL[c], ancho: 70 }), fl: trazo(s3, '', { color: COL[c], ancho: 7 }), et: texto(`${n}|${c}`, [t0], { tam: 48 }) }));
NIV.forEach(([, , t0]) => sfx(t0, 'subida', { vol: .25 }));
function esc3(t) {
  const on = dentro(t, V.niveles); s3.style.display = on ? 'block' : 'none';
  if (!on) return apagar(t3, barras3.map(b => b.et));
  escribir(t3, t); put(t3, { x: CX, y: 160, o: 1 });
  barras3.forEach((b, i) => {
    const [, , t0, alto] = NIV[i], x = 620 + i * 340, base = 880, top = base - 560 * alto * P(t, t0 + .05, .9, E.out3);
    forma(b.eje, () => linea(x - 90, base + 6, x + 90, base + 4, 1)); dibujar(b.eje, dib(t, 16.45 + i * .1, .4));
    b.barra.setAttribute('d', `M${x},${base - 4} L${x},${Math.min(base - 4, top).toFixed(1)}`); dibujar(b.barra, t > t0 ? 1 : 0);
    forma(b.fl, () => flecha(x + 70, base - 120, x + 70, Math.min(base - 160, top))); dibujar(b.fl, dib(t, t0 + .5, .5));
    escribir(b.et, t); put(b.et, { x, y: base + 70, o: 1 });
  });
}

/* =====================================================================
   4 · MENTE Y CUERPO (25,5–35,6): mente → pensamiento; cuerpo = emoción + sensación; 4 pasos
   ===================================================================== */
const s4 = lienzo(), g4 = grupo(s4), sil4 = silueta(g4);
const lM = texto('Mente|mente', [25.54], { tam: 60 }), lMs = texto('pensamiento', [25.9], { tam: 38, m: true, gris: true });
const lC = texto('Cuerpo|cuerpo', [27.30], { tam: 60 }), eq4 = texto('= emoción|emocion + sensación|emocion', [29.80, 29.98, 30.72, 31.08], { tam: 46, m: true });
const fM = trazo(s4, '', { color: COL.mente, ancho: 5 }), fC = trazo(s4, '', { color: COL.cuerpo, ancho: 5 }), aura4 = trazo(g4, circulo(0, 58, 70), { color: COL.mente, ancho: 4 });
const tit4 = texto('4 pasos para dejar|emocion ir|emocion', [32.60, 32.94, 33.90, 34.38, 34.66], { tam: 60 });
const PASOS = ['Identifica', 'Sal de la mente', 'Permite que fluya', 'Observa sin juzgar'];
const filas4 = PASOS.map((n, i) => ({ num: texto(`${i + 1}`, [33.0 + i * .16], { tam: 44 }), nom: texto(n, [33.0 + i * .16], { tam: 44, gris: true }), caja: trazo(s4, '', { ancho: 5 }) }));
sfx(25.5, 'aire', { vol: .35 }); sfx(25.54, 'tick-suave', { vol: .4 }); sfx(27.3, 'tick-suave', { vol: .4 }); sfx(32.6, 'nota', { vol: .35 });
const SIL4 = norm([[25.3, { x: 860, y: 230, s: 1.05 }], [32.0, {}], [32.6, { x: 420, y: 260, s: .9 }, E.io3]]);
function esc4(t) {
  const on = dentro(t, V.cuerpo); s4.style.display = on ? 'block' : 'none';
  if (!on) return apagar(lM, lMs, lC, eq4, tit4, filas4.flatMap(f => [f.num, f.nom]));
  const f = KF(t, SIL4); pos(g4, f.x, f.y, f.s); dibujarSilueta(sil4, t, 25.3);
  dibujar(aura4, dib(t, 25.6, .5), .7 * (1 - P(t, 32.0, .3)));
  const q = P(t, 32.0, .35, E.in3), cab = f.y + 58 * f.s, tr = f.y + 300 * f.s;
  // etiquetas alineadas hacia la figura y flechas que empiezan 26 px después del texto (nada se pisa)
  escribir(lM, t); put(lM, { x: f.x - 270, y: cab - 14, ax: 100, o: 1 - q }); escribir(lMs, t); put(lMs, { x: f.x - 270, y: cab + 40, ax: 100, o: 1 - q });
  forma(fM, () => flecha(f.x - 244, cab - 14, f.x - 80 * f.s, cab - 14)); dibujar(fM, dib(t, 25.7, .4), 1 - q);
  escribir(lC, t); put(lC, { x: f.x + 270, y: tr - 26, ax: 0, o: 1 - q }); escribir(eq4, t); put(eq4, { x: f.x + 270, y: tr + 36, ax: 0, o: 1 - q });
  forma(fC, () => flecha(f.x + 244, tr - 26, f.x + 95 * f.s, tr - 26)); dibujar(fC, dib(t, 27.4, .4), 1 - q);
  escribir(tit4, t); put(tit4, { x: 1180, y: 250, o: 1 });
  filas4.forEach((fi, i) => {
    const y = 370 + i * 116, o = P(t, 32.9 + i * .16, .3);
    escribir(fi.num, t); put(fi.num, { x: 860, y, o }); escribir(fi.nom, t); put(fi.nom, { x: 930, y, ax: 0, o });
    forma(fi.caja, () => caja(820, y - 44, 720, 88)); dibujar(fi.caja, dib(t, 32.85 + i * .16, .5));
  });
}

/* =====================================================================
   5 · PASO 1 (37,8–42,9): ¿dónde sientes la emoción? — cada zona con el color de su centro
   ===================================================================== */
const s5 = lienzo(), g5 = grupo(s5), sil5 = silueta(g5);
const cab5 = cabecera(1, '¿Dónde sientes|emocion la emoción?', [37.82, 38.12, 38.50, 38.58], 37.55, s5);
const ZONAS = [['Pecho', 'corazon', 0, CENTRO.corazon, 39.74], ['Garganta', 'garganta', 0, CENTRO.garganta, 40.24], ['Estómago', 'plexo', 0, CENTRO.plexo, 41.09], ['Piernas', 'raiz', -30, 560, 42.01]];
const pts5 = ZONAS.map(([, c, x, y]) => punto(g5, x, y, C[c]));
const et5 = ZONAS.map(([n, c, , , t0]) => texto(`${n}|${c}`, [t0], { tam: 50 })), ln5 = ZONAS.map(([, c]) => trazo(s5, '', { color: C[c], ancho: 4 }));
ZONAS.forEach(([, , , , t0]) => sfx(t0, 'tick-suave', { vol: .4 })); sfx(37.82, 'nota', { vol: .35 });
function esc5(t) {
  const on = dentro(t, V.donde); s5.style.display = on ? 'block' : 'none';
  if (!on) return apagar(cab5.ceja, cab5.tit, et5);
  pintarCabecera(cab5, t);
  const sx = 800, sy = 300, se = .95; pos(g5, sx, sy, se); dibujarSilueta(sil5, t, 37.6);
  ZONAS.forEach(([, , px, py, t0], i) => {
    pintarPunto(pts5[i], t, t0);
    const ey = 360 + [1, 0, 2, 3][i] * 140, x = sx + px * se, y = sy + py * se;    // etiquetas en el orden del cuerpo
    escribir(et5[i], t); put(et5[i], { x: 1150, y: ey, ax: 0, o: 1 });
    forma(ln5[i], () => linea(x + 34, y, 1120, ey, 2)); dibujar(ln5[i], dib(t, t0, .35));
  });
}

/* =====================================================================
   6 · EMOCIÓN = ENERGÍA (42,9–47,5): pura energía; dejar que se manifieste ✓
   ===================================================================== */
const s6 = lienzo();
const e6a = texto('Emoción|emocion', [43.39], { tam: 96 }), e6b = texto('=', [43.73], { tam: 96 }), e6c = texto('energía|energia', [44.05], { tam: 96 });
const rayo6 = trazo(s6, '', { color: COL.energia, ancho: 7 });
const ok6 = texto('Dejar que se manifieste', [46.09, 46.65, 46.81, 46.95], { tam: 54 }), tk6 = trazo(s6, '', { color: COL.ok, ancho: 9 }), bx6 = trazo(s6, '', { ancho: 5 });
sfx(43.4, 'aire', { vol: .35 }); sfx(44.05, 'golpe-corto', { vol: .45 }); sfx(46.95, 'tick', { vol: .4 });
function esc6(t) {
  const on = dentro(t, V.energia1); s6.style.display = on ? 'block' : 'none';
  if (!on) return apagar(e6a, e6b, e6c, ok6);
  [e6a, e6b, e6c].forEach(e => escribir(e, t));
  const wa = medir(e6a).w, wb = medir(e6b).w, wc = medir(e6c).w, gap = 40, tot = wa + wb + wc + 2 * gap, x0 = CX - tot / 2;
  put(e6a, { x: x0, y: 420, ax: 0, o: 1 }); put(e6b, { x: x0 + wa + gap, y: 420, ax: 0, o: 1 }); put(e6c, { x: x0 + wa + wb + 2 * gap, y: 420, ax: 0, o: 1 });
  const xr = x0 + tot + 60;      // rayo de energía junto a la palabra
  forma(rayo6, () => `M${xr + 20},${330} L${xr - 14},${430} L${xr + 14},${430} L${xr - 18},${520}`); dibujar(rayo6, dib(t, 44.15, .4));
  escribir(ok6, t); const { w, h } = medir(ok6); put(ok6, { x: CX + 40, y: 700, o: 1 });
  forma(bx6, () => caja(CX - w / 2 - 70, 700 - h / 2 - 36, w + 150, h + 72)); dibujar(bx6, dib(t, 45.9, .5));
  forma(tk6, () => tick(CX - w / 2 - 20, 700, 1)); dibujar(tk6, dib(t, 46.95, .3));
}

/* =====================================================================
   7 · PENSAMIENTO ≠ EMOCIÓN (54,7–59,3): y la emoción es lo más importante ★★★★★
   ===================================================================== */
const s7 = lienzo();
const p7 = texto('Pensamiento|mente', [55.63], { tam: 70 }), ne7 = texto('≠', [56.22], { tam: 90 }), m7 = texto('Emoción|emocion', [57.05], { tam: 70 });
const bp7 = trazo(s7, '', { color: COL.mente, ancho: 6 }), bm7 = trazo(s7, '', { color: COL.emocion, ancho: 6 });
const imp7 = texto('lo más importante', [58.22, 58.32, 58.50], { tam: 50, m: true });
const est7 = [0, 1, 2, 3, 4].map(() => trazo(s7, '', { color: COL.energia, ancho: 5, fill: 'none' }));
sfx(55.63, 'tick-suave', { vol: .4 }); sfx(57.05, 'tick-suave', { vol: .4 }); [0, 1, 2, 3, 4].forEach(i => sfx(58.5 + i * .09, 'tick', { vol: .3 }));
function esc7(t) {
  const on = dentro(t, V.pensemo); s7.style.display = on ? 'block' : 'none';
  if (!on) return apagar(p7, ne7, m7, imp7);
  const g = P(t, 57.74, .5, E.out3);              // «la emoción es lo más importante»: la caja de la emoción crece
  [p7, ne7, m7].forEach(e => escribir(e, t));
  put(p7, { x: 560, y: 470, o: 1 - .45 * g }); put(ne7, { x: CX, y: 466, o: 1 }); put(m7, { x: 1360, y: 470, s: 1 + .12 * g, o: 1 });
  const a = medir(p7), b = medir(m7);
  forma(bp7, () => caja(560 - a.w / 2 - 50, 470 - a.h / 2 - 40, a.w + 100, a.h + 80)); dibujar(bp7, dib(t, 55.5, .5), 1 - .45 * g);
  const sb = 1 + .12 * g; forma(bm7, () => caja(1360 - b.w * sb / 2 - 50, 470 - b.h * sb / 2 - 40, b.w * sb + 100, b.h * sb + 80)); dibujar(bm7, dib(t, 56.9, .5));
  escribir(imp7, t); put(imp7, { x: 1360, y: 640, o: 1 });
  est7.forEach((e, i) => { forma(e, () => estrella(1220 + i * 70, 730, 26)); dibujar(e, dib(t, 58.5 + i * .09, .25));
    e.setAttribute('fill', t > 58.6 + i * .09 ? COL.energia : 'none'); });
}

/* =====================================================================
   8 · PASO 2 (65,8–71,3): sal de la mente — los pensamientos se tachan y caen
   ===================================================================== */
const s8 = lienzo();
const cab8 = cabecera(2, 'Sal de la mente|mente', [65.86, 66.06, 66.16, 66.28], 65.6, s8);
const cir8 = trazo(s8, circulo(960, 650, 150), { color: COL.mente, ancho: 7 }), lbl8 = texto('mente', [66.3], { tam: 40, m: true, gris: true });
const PENS = [['¿Por qué me pasa esto?', 67.44, 480, 520], ['La historia', 68.74, 1450, 560], ['Pensamientos', 69.30, 1420, 840]];
const pens8 = PENS.map(([txt, tc]) => ({ el: texto(txt, [66.5], { tam: 44 }), caja: trazo(s8, '', { ancho: 5 }), tacha: trazo(s8, '', { color: COL.no, ancho: 6 }), lin: trazo(s8, '', { color: COL.mente, ancho: 4 }), tc }));
const calma8 = trazo(s8, '', { color: COL.calma, ancho: 9 });
sfx(65.86, 'nota', { vol: .35 }); PENS.forEach(([, tc]) => sfx(tc, 'descarte', { vol: .35 }));
function esc8(t) {
  const on = dentro(t, V.mente); s8.style.display = on ? 'block' : 'none';
  if (!on) return apagar(cab8.ceja, cab8.tit, lbl8, pens8.map(p => p.el));
  pintarCabecera(cab8, t);
  dibujar(cir8, dib(t, 65.6, .6)); escribir(lbl8, t); put(lbl8, { x: 960, y: 650, o: 1 });
  forma(calma8, () => tick(960, 715, 1.0)); dibujar(calma8, dib(t, 70.3, .35));       // «no quieras entenderlo»: ✓ calma
  pens8.forEach((p, i) => {
    const [, , x, y] = PENS[i], ap = P(t, 66.4 + i * .18, .35, E.out3), cae = P(t, p.tc + .35, .6, E.in2);
    const { w, h } = medir(p.el), yy = y + cae * 140, o = ap * (1 - cae);
    escribir(p.el, t); put(p.el, { x, y: yy, o });
    forma(p.caja, () => caja(x - w / 2 - 40, yy - h / 2 - 26, w + 80, h + 52)); dibujar(p.caja, dib(t, 66.4 + i * .18, .5), o);
    forma(p.tacha, () => linea(x - w / 2 - 14, yy + 4, x + w / 2 + 14, yy - 4, 2)); dibujar(p.tacha, dib(t, p.tc - .04, .3), o);
    const ang = Math.atan2(yy - 650, x - 960), bx = 960 + 160 * Math.cos(ang), by = 650 + 160 * Math.sin(ang), fx = x - (w / 2 + 50) * Math.sign(x - 960);
    forma(p.lin, () => linea(bx, by, fx, yy, 2)); dibujar(p.lin, dib(t, 66.6 + i * .18, .4), o * .8);
  });
}

/* =====================================================================
   9 · PASO 3 (80,0–85,3): permite que fluya — respira, repite «Puedo permitirme estar aquí», no te vas a morir 😌
   ===================================================================== */
const s9 = lienzo();
const cab9 = cabecera(3, 'Permite que fluya|calma', [80.55, 81.11, 81.29], 79.8, s9);
const onda9 = trazo(s9, '', { color: COL.calma, ancho: 6 }), resp9 = texto('respira', [81.81], { tam: 40, m: true, gris: true });
const rep9 = texto('y repite:', [82.49, 82.61], { tam: 40, m: true, gris: true });
const cita9 = texto('«Puedo permitirme estar aquí|calma»', [83.19, 83.43, 83.93, 84.17], { tam: 66 }), caja9 = trazo(s9, '', { ancho: 6 });
const sub9 = texto('No te vas a morir.', [84.55, 84.67, 84.77, 84.93, 84.99], { tam: 46, m: true });
const emo9 = mk('div', 'L emoji z5', WORLD, '😌'); emo9.style.fontSize = '64px';       // el único emoji del vídeo
sfx(80.55, 'nota', { vol: .35 }); sfx(81.81, 'aire', { vol: .3 }); sfx(83.19, 'tick-suave', { vol: .4 }); sfx(84.99, 'pop', { vol: .3 });
function esc9(t) {
  const on = dentro(t, V.fluye); s9.style.display = on ? 'block' : 'none';
  if (!on) return apagar(cab9.ceja, cab9.tit, resp9, rep9, cita9, sub9, emo9);
  pintarCabecera(cab9, t);
  let d = ''; const A = 44 * (1 + .25 * Math.sin(t * 1.4));
  for (let x = 300; x <= 1620; x += 12) d += (x === 300 ? 'M' : 'L') + x + ',' + (430 + A * Math.sin((x - 300) / 1320 * Math.PI * 4 - t * 1.6)).toFixed(1) + ' ';
  onda9.setAttribute('d', d); dibujar(onda9, dib(t, 79.8, 1.2));
  escribir(resp9, t); put(resp9, { x: 300, y: 350, ax: 0, o: 1 }); escribir(rep9, t); put(rep9, { x: CX, y: 580, o: 1 });
  escribir(cita9, t); const { w, h } = medir(cita9); put(cita9, { x: CX, y: 700, o: 1 });
  forma(caja9, () => caja(CX - w / 2 - 56, 700 - h / 2 - 40, w + 112, h + 80)); dibujar(caja9, dib(t, 82.6, .6));
  escribir(sub9, t); const ws = medir(sub9).w; put(sub9, { x: CX - 40, y: 860, o: 1 });
  const pe = P(t, 84.99, .35, E.back); put(emo9, { x: CX - 40 + ws / 2 + 60, y: 856, s: lerp(.4, 1, pe), o: clamp(pe * 2) });
}

/* =====================================================================
   10 · EXPRÉSALA (92,0–99,0): que se exprese, te inunde, te atraviese, se expanda, que fluya ✓
   ===================================================================== */
const s10 = lienzo(), g10 = grupo(s10), sil10 = silueta(g10);
const ondas10 = [0, 1, 2, 3].map(() => trazo(g10, '', { color: COL.emocion, ancho: 5 }));
const cruza10 = trazo(s10, '', { color: COL.emocion, ancho: 7 });
const tit10 = texto('Deja que la emoción|emocion…', [92.52, 93.16, 93.40, 93.52], { tam: 62 });
const VERB = [['se exprese|garganta', [93.96, 94.08]], ['te inunde|emocion', [94.70, 94.82]], ['te atraviese|emocion', [95.96, 96.06]], ['se expanda|energia', [97.94, 98.04]], ['y fluya|calma', [98.54, 98.70]]];
const verb10 = VERB.map(([v, ts]) => ({ el: texto(v, ts, { tam: 52 }), tk: trazo(s10, '', { color: COL.ok, ancho: 8 }), t0: ts[1] }));
sfx(92.1, 'aire', { vol: .35 }); VERB.forEach(([, ts]) => sfx(ts[1], 'tick', { vol: .35 })); sfx(96.06, 'barrido', { vol: .3 }); sfx(98.04, 'swell', { vol: .3 });
function esc10(t) {
  const on = dentro(t, V.expresa); s10.style.display = on ? 'block' : 'none';
  if (!on) return apagar(tit10, verb10.map(v => v.el));
  const fx = 560, fy = 230; pos(g10, fx, fy, 1.05); dibujarSilueta(sil10, t, 91.8);
  const rmax = t < 98.04 ? 170 : lerp(170, 330, P(t, 98.04, .8, E.out3));
  ondas10.forEach((e, i) => {
    if (t < 94.08) return dibujar(e, 0);
    const k = ((t - 94.08) / 1.6 + i / 4) % 1, r = 20 + k * rmax;
    forma(e, () => circulo(0, CENTRO.corazon, r)); dibujar(e, 1, (1 - k) * P(t, 94.08, .3) * .9);
  });
  forma(cruza10, () => flecha(fx - 300, fy + CENTRO.corazon * 1.05, fx + 330, fy + CENTRO.corazon * 1.05)); dibujar(cruza10, dib(t, 96.0, .45), 1 - P(t, 97.9, .4));
  escribir(tit10, t); put(tit10, { x: 1040, y: 220, ax: 0, o: 1 });
  verb10.forEach((v, i) => { const y = 350 + i * 100; escribir(v.el, t); put(v.el, { x: 1120, y, ax: 0, o: 1 });
    forma(v.tk, () => tick(1070, y, .9)); dibujar(v.tk, dib(t, v.t0 + .1, .3)); });
}

/* =====================================================================
   11 · PASO 4 (111,3–118,4): observa sin juzgar — indiferencia amorosa, hasta que se disipe
   ===================================================================== */
const s11 = lienzo();
const cab11 = cabecera(4, 'Observa sin juzgar', [112.25, 113.05, 113.29], 111.1, s11);
const ojo11 = trazo(s11, 'M700,560 C800,450 1120,450 1220,560 C1120,670 800,670 700,560 Z', { ancho: 7 }), iris11 = trazo(s11, circulo(960, 560, 46), { color: COL.mente, ancho: 7 });
const ind11 = texto('Indiferencia amorosa|amor', [115.09, 115.81], { tam: 60 });
const has11 = texto('hasta que se disipe', [116.47, 116.81, 116.99, 117.31], { tam: 44, m: true, gris: true });
const emo11 = [0, 1, 2, 3, 4, 5].map(() => trazo(s11, '', { color: COL.emocion, ancho: 5 }));
sfx(112.25, 'nota', { vol: .35 }); sfx(115.81, 'tick-suave', { vol: .4 }); sfx(117.31, 'aire-salida', { vol: .35 });
function esc11(t) {
  const on = dentro(t, V.observa); s11.style.display = on ? 'block' : 'none';
  if (!on) return apagar(cab11.ceja, cab11.tit, ind11, has11);
  pintarCabecera(cab11, t);
  dibujar(ojo11, dib(t, 111.1, .7)); dibujar(iris11, dib(t, 111.6, .4));
  escribir(ind11, t); put(ind11, { x: CX, y: 770, o: 1 }); escribir(has11, t); put(has11, { x: CX, y: 860, o: 1 });
  const dis = P(t, 117.31, .9, E.out3);
  emo11.forEach((e, i) => {
    const a = i / 6 * Math.PI * 2 + t * .2, r = 300 + dis * 160, a2 = a + .5;
    e.setAttribute('d', `M${(960 + r * Math.cos(a)).toFixed(1)},${(560 + r * .55 * Math.sin(a)).toFixed(1)} A${r},${r * .55} 0 0 1 ${(960 + r * Math.cos(a2)).toFixed(1)},${(560 + r * .55 * Math.sin(a2)).toFixed(1)}`);
    dibujar(e, dib(t, 112.6 + i * .08, .4), 1 - dis);
  });
}

const CAMK = norm([[0, { x: CX, y: CY, s: 1 }]]);
function layout() {}
function estadoVideo(t) { const anim = enAnim(t); return { fondo: anim ? 1 : 0, persona: anim ? 0 : 1, halo: 0 }; }
const FONDOK = norm([[0, { vel: 26, brillo: 1 }]]);
const ESPACIO = null;

function render(t) {
  const cam = camara(t), dx = -(cam.x - CX) * cam.s, dy = -(cam.y - CY) * cam.s;
  WORLD.style.transform = WORLDF.style.transform = `translate(${dx.toFixed(2)}px,${dy.toFixed(2)}px) scale(${cam.s.toFixed(5)})`;
  pintarCapas(t, estadoVideo(t));
  esc1(t); esc2(t); esc3(t); esc4(t); esc5(t); esc6(t); esc7(t); esc8(t); esc9(t); esc10(t); esc11(t);
}

/* =========================== FIN DE LA DEMO =========================== */
