/* =====================================================================
   Librería de la pizarra blanca de Abel (vídeos largos horizontales). Se carga dentro del index.html del modo «cara»
   de la skill animaciones-horizontal-combinadas, antes de las escenas de cada vídeo.
   Reglas (memoria estilo-videos-largos-stickman): blanco puro, Inter 800–900, colores de los centros, texto grande
   (títulos 110–130, principal 80–96, etiquetas 64–72, mín. 56), todo lo importante en la zona 4:3 (x 240–1680),
   líneas perfiladas que se dibujan solas y NO tiemblan, el personaje de su boceto con posturas según la historia.
   ===================================================================== */
const grid = $('grid'), glowN = $('glowN'), glowA = $('glowA'), glowB = $('glowB');
const NS = 'http://www.w3.org/2000/svg', NEGRO = '#111111', GRIS = '#8a8a8a';
const C = { raiz: '#C8372D', sacro: '#E06A1B', plexo: '#C99A00', corazon: '#1E7A46', garganta: '#1D7FD1', ojo: '#3F3FB5', corona: '#7A3FC4' };
const COL = { mente: C.ojo, emocion: C.sacro, sexual: C.sacro, energia: C.plexo, conciencia: C.corona, cuerpo: C.raiz,
  amor: C.corazon, calma: C.corazon, ok: C.corazon, no: C.raiz, dopa: C.sacro, expresion: C.garganta };
const Z43 = { x0: 280, x1: 1640 };                     // su plantilla 2 de reels deja ver x ≈ 257–1671 (medido en su captura); con margen

css(`
@font-face{font-family:InterV;src:url(assets/fonts/Inter-Variable.ttf);font-weight:100 900;font-display:block}
#fondo{background:#fff}
#grid,.glow,#vignette,#noise{display:none}
.esc{position:absolute;left:0;top:0;width:1920px;height:1080px;display:none}
.esc svg{position:absolute;left:0;top:0;overflow:visible}
.tx{position:absolute;left:0;top:0;font-family:InterV;font-variation-settings:'wght' 850,'opsz' 32;letter-spacing:-.025em;color:${NEGRO};white-space:nowrap;line-height:1.06}
.tx.m{font-variation-settings:'wght' 600,'opsz' 32;letter-spacing:-.01em}
.tx.gris{color:${GRIS}}
.tx span{display:inline-block;margin-right:.24em}
.tx span:last-child{margin-right:0}
.emo{position:absolute;left:0;top:0;font-family:'Segoe UI Emoji','Noto Color Emoji',sans-serif;line-height:1}
.ceja{position:absolute;left:0;top:0;font-family:InterV;font-variation-settings:'wght' 800,'opsz' 32;letter-spacing:.22em;font-size:40px;white-space:nowrap;color:${C.corazon}}
`);

/* ---------- escenas: cada una en su capa; la librería la enciende solo dentro de su ventana del montaje ---------- */
const ESCENAS = [];
let _VA = -9;                                  // inicio de la ventana en curso: lo que se dice en su primer 0,6 s ya está al cortar
const _alCorte = t0 => t0 < _VA + .6 ? Math.min(t0, _VA - .1) : t0;
function escena(id, crear) {
  const div = mk('div', 'esc', WORLD), svg = document.createElementNS(NS, 'svg');
  svg.setAttribute('width', 1920); svg.setAttribute('height', 1080); svg.setAttribute('viewBox', '0 0 1920 1080');
  div.appendChild(svg);
  const e = { id, div, svg }; e.pintar = crear(e); ESCENAS.push(e); return e;
}
function pintarEscenas(t) {
  for (const e of ESCENAS) {
    const w = V[e.id], pl = planoEn(t), on = !!w && (PLANOS.length ? !!pl && pl.tipo === 'anim' && pl.id === e.id : dentro(t, w));   // solo en su plano: nada se cuela entre dos animaciones seguidas
    e.div.style.display = on ? 'block' : 'none';
    if (on) { _VA = w.a; e.pintar(t, w); }
  }
}

/* ---------- trazos que se dibujan solos (semilla fija por forma: nada tiembla) ---------- */
let _sem = 5, _n = 1;
const az = () => (_sem = (_sem * 16807) % 2147483647) / 2147483647 - .5;
const linea = (x1, y1, x2, y2, j = 3) => `M${x1},${y1} Q${((x1 + x2) / 2 + az() * j * 2).toFixed(1)},${((y1 + y2) / 2 + az() * j * 2).toFixed(1)} ${x2},${y2}`;
function caja(x, y, w, h) {
  const p = [[x - 4, y + 3], [x + w + 3, y - 2], [x + w - 2, y + h + 3], [x + 3, y + h - 2]];
  let d = ''; for (let i = 0; i < 4; i++) { const a = p[i], b = p[(i + 1) % 4]; d += linea(a[0], a[1], b[0], b[1]) + ' '; }
  return d + linea(p[0][0], p[0][1], p[0][0] + 12, p[0][1] - 1);
}
const cajaR = (x, y, w, h, r = 22) => `M${x + r},${y} L${x + w - r},${y} Q${x + w},${y} ${x + w},${y + r} L${x + w},${y + h - r} Q${x + w},${y + h} ${x + w - r},${y + h} L${x + r},${y + h} Q${x},${y + h} ${x},${y + h - r} L${x},${y + r} Q${x},${y} ${x + r},${y} Z`;
const circulo = (cx, cy, r) => { const a = -.35, x2 = cx + r * Math.cos(Math.PI + a), y2 = cy + r * Math.sin(Math.PI + a);
  return `M${cx - r},${cy + 2} A${r},${r} 0 1 1 ${cx + r},${cy} A${r},${r} 0 0 1 ${cx - r},${cy} A${r},${r} 0 0 1 ${x2.toFixed(1)},${y2.toFixed(1)}`; };
const flecha = (x1, y1, x2, y2, k = 26) => { const a = Math.atan2(y2 - y1, x2 - x1);
  return linea(x1, y1, x2, y2, 2) + ` M${(x2 - k * Math.cos(a - .5)).toFixed(1)},${(y2 - k * Math.sin(a - .5)).toFixed(1)} L${x2},${y2} L${(x2 - k * Math.cos(a + .5)).toFixed(1)},${(y2 - k * Math.sin(a + .5)).toFixed(1)}`; };
const tick = (x, y, s = 1) => `M${x - 24 * s},${y} L${x - 6 * s},${y + 19 * s} L${x + 28 * s},${y - 24 * s}`;
const cruz = (x, y, s = 1) => `M${x - 20 * s},${y - 20 * s} L${x + 20 * s},${y + 20 * s} M${x + 20 * s},${y - 20 * s} L${x - 20 * s},${y + 20 * s}`;
const estrella = (x, y, r) => { let d = ''; for (let i = 0; i < 10; i++) { const a = -Math.PI / 2 + i * Math.PI / 5, rr = i % 2 ? r * .45 : r;
  d += (i ? 'L' : 'M') + (x + rr * Math.cos(a)).toFixed(1) + ',' + (y + rr * Math.sin(a)).toFixed(1) + ' '; } return d + 'Z'; };
const bucle = (cx, cy, r) => `M${cx + r},${cy} A${r},${r} 0 1 1 ${(cx + r * Math.cos(-.6)).toFixed(1)},${(cy + r * Math.sin(-.6)).toFixed(1)} M${(cx + r * Math.cos(-.6) - 6).toFixed(1)},${(cy + r * Math.sin(-.6) - 30).toFixed(1)} L${(cx + r * Math.cos(-.6)).toFixed(1)},${(cy + r * Math.sin(-.6)).toFixed(1)} L${(cx + r * Math.cos(-.6) + 30).toFixed(1)},${(cy + r * Math.sin(-.6) + 4).toFixed(1)}`;
/* o.k = 'flecha' | 'marca': el comprobador vigila que no pisen textos */
function trazo(g, d, o = {}) {
  const e = document.createElementNS(NS, 'path');
  e.setAttribute('d', d); e.setAttribute('fill', o.fill || 'none'); e.setAttribute('stroke', o.color || NEGRO);
  e.setAttribute('stroke-width', o.ancho || 7); e.setAttribute('stroke-linecap', 'round'); e.setAttribute('stroke-linejoin', 'round');
  e.setAttribute('pathLength', '1'); e._sem0 = (_n++ * 7919) % 2147483646 + 1; if (o.k) e.dataset.k = o.k; g.appendChild(e); return e;
}
function forma(e, fn) { _sem = e._sem0; e.setAttribute('d', fn()); }
function dibujar(e, p, o = 1) {
  if (p <= 0 || o <= .002) { e.style.opacity = 0; return; }
  e.style.opacity = o.toFixed(3); e.style.strokeDasharray = p >= 1 ? 'none' : '1 1'; e.style.strokeDashoffset = (1 - p).toFixed(4);
}
const dib = (t, t0, dur = .6) => P(t, t0, dur, E.io3);
const fl = (g, x1, y1, x2, y2, o = {}) => trazo(g, flecha(x1, y1, x2, y2), { ancho: 7, k: 'flecha', ...o });

/* ---------- efectos de sonido: cada texto, emoji y marca suena (sin amontonarse: ≥ 0,3 s entre dos) ---------- */
const _SONIDOS = [];
function suena(t, id, vol = .3) { if (_SONIDOS.some(x => Math.abs(x - t) < .3)) return; _SONIDOS.push(t); sfx(t, id, { vol }); }
const grupo = (padre, tr = '') => { const g = document.createElementNS(NS, 'g'); if (tr) g.setAttribute('transform', tr); padre.appendChild(g); return g; };
const mover = (g, x, y, s = 1, r = 0) => g.setAttribute('transform', `translate(${x.toFixed(1)},${y.toFixed(1)}) rotate(${r.toFixed(2)}) scale(${s.toFixed(4)})`);

/* ---------- texto: entra palabra a palabra con la voz. 'palabra|color' = destacada (clave de COL o de C) ---------- */
function texto(e, frase, tiempos, o = {}) {
  const pal = frase.split(' ');
  if (Array.isArray(tiempos) && tiempos.length > 1 && tiempos.length !== pal.length) console.error(`texto «${frase}»: ${pal.length} palabras y ${tiempos.length} tiempos`);
  const ts = Array.isArray(tiempos) ? tiempos : [tiempos];
  const el = mk('div', 'tx' + (o.m ? ' m' : '') + (o.gris ? ' gris' : ''), e.div, pal.map(w => {
    const m = w.match(/^(.*?)\|([a-z]+)(.*)$/);
    return m ? `<span><b style="font-weight:inherit;color:${COL[m[2]] || C[m[2]]}">${m[1]}</b>${m[3]}</span>` : `<span>${w}</span>`; }).join(''));
  el.style.fontSize = (o.tam || 84) + 'px';
  el._sp = [...el.children]; el._t = pal.map((_, i) => ts[Math.min(i, ts.length - 1)]);
  el._o = { x: CX, y: CY, ax: 50, ay: 50, ...o };
  if (o.sonido !== false && el._t[0] > 0) suena(el._t[0], ...((o.tam || 84) >= 100 ? ['golpe-corto'] : ['tick-suave', .22]));
  return el;
}
/* pinta el texto: cada palabra entra con su tiempo; k = {x, y, o, s} opcionales sobre los de creación */
function pt(el, t, k = {}) {
  const o = { ...el._o, ...k }, op = k.o ?? 1;
  el._sp.forEach((s, i) => { const p = P(t, _alCorte(el._t[i]) - .22, .3, E.out3);   // la palabra asoma justo antes de oírse
    s.style.opacity = clamp(p * 1.5).toFixed(3); s.style.transform = `translateY(${((1 - p) * 16).toFixed(1)}px)`; });
  el.style.opacity = op.toFixed(3);
  el.style.transform = `translate(${o.x.toFixed(1)}px,${o.y.toFixed(1)}px) translate(${-o.ax}%,${-o.ay}%) scale(${(k.s ?? 1).toFixed(4)})`;
}
const medir = el => ({ w: el.offsetWidth, h: el.offsetHeight });
function emoji(e, ch, tam = 110, t0) { const el = mk('div', 'emo', e.div, ch); el.style.fontSize = tam + 'px'; if (t0 > 0) suena(t0, 'pop'); return el; }
function pe(el, t, t0, x, y, o = 1) {     // emoji que entra con un pequeño rebote
  const p = P(t, _alCorte(t0) - .22, .4, E.back);
  el.style.opacity = (clamp(p * 2) * o).toFixed(3);
  el.style.transform = `translate(${x}px,${y}px) translate(-50%,-50%) scale(${lerp(.3, 1, p).toFixed(3)})`;
}

/* ---------- personajes ----------
   · stickman(): para dar contexto (historias, situaciones). Dibujado de una pieza: cabeza, tronco, brazos y piernas
     como trazos continuos (mano–codo–hombro–codo–mano y pie–rodilla–cadera–rodilla–pie). x, y = suelo bajo sus pies.
   · silueta(): la silueta grande del boceto de Abel (cabeza ovalada + un contorno continuo), SOLO cuando se habla de
     centros energéticos, emociones o el cuerpo por dentro. x, y = suelo bajo sus pies.
   Pose del stickman: bI, bD = brazos (0 = caídos; + = se abren/suben), cI, cD = codo (+ hacia fuera, − hacia dentro),
   pI, pD = piernas (+ se abren), rI, rD = rodillas, m = muslo (1 de pie; .35 sentado de frente), cab = {x, y} cabeza. */
const POSES = {
  pie: { bI: 14, bD: 14, cI: 0, cD: 0, pI: 6, pD: 6, rI: 0, rD: 0, m: 1, cab: { x: 0, y: 0 } },
  arriba: { bI: 150, bD: 150, cI: 10, cD: 10, pI: 10, pD: 10, rI: 0, rD: 0, m: 1, cab: { x: 0, y: -4 } },
  manosCabeza: { bI: 135, bD: 135, cI: 75, cD: 75, pI: 6, pD: 6, rI: 0, rD: 0, m: 1, cab: { x: 0, y: 10 } },
  hundido: { bI: 4, bD: 4, cI: 0, cD: 0, pI: 5, pD: 5, rI: 0, rD: 0, m: 1, cab: { x: 14, y: 26 } },
  sentado: { bI: 20, bD: 20, cI: -50, cD: -50, pI: 16, pD: 16, rI: 16, rD: 16, m: .35, cab: { x: 0, y: 0 } },
  movil: { bI: 8, bD: 20, cI: 0, cD: -135, pI: 6, pD: 6, rI: 0, rD: 0, m: 1, cab: { x: 8, y: 16 } },
  sentadoMovil: { bI: 20, bD: 20, cI: -50, cD: -135, pI: 16, pD: 16, rI: 16, rD: 16, m: .35, cab: { x: 8, y: 16 } },
  señala: { bI: 8, bD: 95, cI: 0, cD: 0, pI: 6, pD: 6, rI: 0, rD: 0, m: 1, cab: { x: 0, y: 0 } },
  escribe: { bI: 25, bD: 25, cI: -75, cD: -75, pI: 16, pD: 16, rI: 16, rD: 16, m: .35, cab: { x: 0, y: 18 } },
  camina: { bI: 20, bD: 20, cI: 10, cD: 10, pI: 14, pD: 14, rI: 0, rD: 0, m: 1, cab: { x: 0, y: 0 } },
};
const mezclaPose = (a, b, k) => { const o = {}; for (const key in a) o[key] = key === 'cab' ? { x: lerp(a.cab.x, b.cab.x, k), y: lerp(a.cab.y, b.cab.y, k) } : lerp(a[key], b[key], k); return o; };
const _dir = (lado, a) => [lado * Math.sin(a * Math.PI / 180), Math.cos(a * Math.PI / 180)];
function stickman(padre) {
  const g = grupo(padre), o = { ancho: 8 };
  return { g, cabeza: trazo(g, '', o), tronco: trazo(g, '', o), brazos: trazo(g, '', o), piernas: trazo(g, '', o) };
}
/* devuelve las posiciones de manos, cabeza y cadera en el lienzo (para colocar un móvil en la mano, un bocadillo…) */
function pintarStick(f, t, { x, y, s = 1, pose = 'pie', t0 = -1, o = 1 }) {
  const p = typeof pose === 'string' ? POSES[pose] : pose, Ls = 130 * p.m, Li = 130;
  const muslo = l => _dir(l, l < 0 ? p.pI : p.pD), cana = l => _dir(l, l < 0 ? p.pI - p.rI : p.pD - p.rD);
  const alto = Math.max(muslo(-1)[1], muslo(1)[1]) * Ls + Math.max(cana(-1)[1], cana(1)[1]) * Li;
  const P0 = (dx, dy) => [x + dx * s, y + dy * s], cad = [0, -alto], hom = [0, -alto - 210];
  const pie = l => { const [a, b] = muslo(l), [c, d] = cana(l); const k = [cad[0] + a * Ls, cad[1] + b * Ls]; return [k, [k[0] + c * Li, k[1] + d * Li]]; };
  const mano = l => { const A = l < 0 ? p.bI : p.bD, Cc = l < 0 ? p.cI : p.cD, [a, b] = _dir(l, A), [c, d] = _dir(l, A + Cc);
    const k = [hom[0] + l * 14 + a * 105, hom[1] + 8 + b * 105]; return [k, [k[0] + c * 95, k[1] + d * 95]]; };
  const cab = [p.cab.x, hom[1] - 62 + p.cab.y], pt2 = q => P0(...q).map(v => v.toFixed(1)).join(',');
  const [kI, fI] = pie(-1), [kD, fD] = pie(1), [cI, mI] = mano(-1), [cD, mD] = mano(1);
  f.cabeza.setAttribute('d', circulo(...P0(...cab), 50 * s));
  f.tronco.setAttribute('d', `M${pt2([cab[0] * .4, hom[1] - 12])} L${pt2(cad)}`);
  f.brazos.setAttribute('d', `M${pt2(mI)} L${pt2(cI)} L${pt2([-14, hom[1] + 8])} L${pt2([14, hom[1] + 8])} L${pt2(cD)} L${pt2(mD)}`);
  f.piernas.setAttribute('d', `M${pt2(fI)} L${pt2(kI)} L${pt2(cad)} L${pt2(kD)} L${pt2(fD)}`);
  f.g.setAttribute('stroke-width', 8);
  const d = (e, dt, dur) => dibujar(e, t0 < 0 ? 1 : dib(t, t0 + dt, dur), o);
  d(f.cabeza, 0, .35); d(f.tronco, .25, .25); d(f.brazos, .4, .35); d(f.piernas, .5, .35);
  return { manoI: { x: +P0(...mI)[0], y: +P0(...mI)[1] }, manoD: { x: P0(...mD)[0], y: P0(...mD)[1] }, cabeza: { x: P0(...cab)[0], y: P0(...cab)[1] }, cadera: { x: P0(...cad)[0], y: P0(...cad)[1] }, s };
}
/* la silueta grande (boceto de Abel) */
const MITAD = [[[-30, 128], [-52, 140], [-62, 162]], [[-76, 205], [-86, 300], [-86, 398]], [[-86, 432], [-60, 436], [-58, 404]],
  [[-56, 330], [-50, 262], [-44, 222]], [[-44, 300], [-46, 362], [-44, 424]], [[-48, 505], [-50, 585], [-46, 662]],
  [[-44, 694], [-14, 694], [-12, 662]], [[-10, 592], [-8, 524], [0, 466]]];
function _siluetaD() {
  const f = ([x, y]) => `${x},${y}`, m = ([x, y]) => [-x, y], ini = [-13, 122];
  let d = `M${f(ini)} `; MITAD.forEach(([a, b, c]) => d += `C${f(a)} ${f(b)} ${f(c)} `);
  for (let i = MITAD.length - 1; i >= 0; i--) { const [a, b] = MITAD[i]; d += `C${f(m(b))} ${f(m(a))} ${f(m(i ? MITAD[i - 1][2] : ini))} `; }
  return d;
}
const SIL_CABEZA = 'M-40,58 C-40,22 -18,4 2,4 C24,4 40,26 40,60 C40,92 22,112 0,112 C-22,112 -40,94 -40,58 Z';
const CENTROS = { corona: -18, ojo: 56, garganta: 140, corazon: 224, plexo: 306, sacro: 384, raiz: 446 };
function silueta(padre) { const g = grupo(padre); return { g, cabeza: trazo(g, SIL_CABEZA, { ancho: 6.5 }), cuerpo: trazo(g, _siluetaD(), { ancho: 6.5 }) }; }
function pintarSilueta(sl, t, { x, y, s = 1, t0 = -1, o = 1 }) {
  mover(sl.g, x, y - 694 * s, s);
  dibujar(sl.cabeza, t0 < 0 ? 1 : dib(t, t0, .45), o); dibujar(sl.cuerpo, t0 < 0 ? 1 : dib(t, t0 + .25, 1.0), o);
}
const centroSil = (x, y, s, c) => ({ x, y: y - 694 * s + CENTROS[c] * s });

/* sofá de frente (créalo ANTES que la figura para que quede detrás). x, y = suelo bajo el centro */
function sofa(padre) { const g = grupo(padre);
  return { g, l: [trazo(g, cajaR(-230, -330, 460, 230, 40), { ancho: 6.5, fill: '#fff' }), trazo(g, cajaR(-250, -150, 500, 90, 26), { ancho: 6.5, fill: '#fff' }),
    trazo(g, cajaR(-290, -240, 80, 220, 30), { ancho: 6.5, fill: '#fff' }), trazo(g, cajaR(210, -240, 80, 220, 30), { ancho: 6.5, fill: '#fff' }),
    trazo(g, linea(-240, -20, -240, 0, 0) + ' ' + linea(240, -20, 240, 0, 0), { ancho: 6.5 })] }; }
function pintarSofa(so, t, t0, x, y, s = 1) { mover(so.g, x, y, s); so.l.forEach((l, i) => dibujar(l, dib(t, t0 + i * .08, .45))); }
/* ---------- piezas ---------- */
function movil(padre, w = 150, h = 270) {        // móvil con pantalla y líneas de contenido
  const g = grupo(padre);
  return { g, w, h, marco: trazo(g, cajaR(-w / 2, -h / 2, w, h, 26), { ancho: 6, fill: '#fff' }),
    lineas: [0, 1, 2, 3].map(i => trazo(g, linea(-w / 2 + 26, -h / 2 + 50 + i * 46, w / 2 - 26 - (i % 2) * 30, -h / 2 + 50 + i * 46, 0), { ancho: 5, color: '#bbb' })) };
}
function pintarMovil(m, t, t0, x, y, s = 1, r = 0, scroll = 0) {
  mover(m.g, x, y, s, r); dibujar(m.marco, dib(t, t0, .4));
  m.lineas.forEach((l, i) => { const yy = ((i * 46 + scroll) % 184) - 92 + 10; l.setAttribute('transform', `translate(0,${(yy - (-m.h / 2 + 50 + i * 46) + 0).toFixed(1)})`); dibujar(l, dib(t, t0 + .2 + i * .05, .3)); });
}
function logoYT(padre) {                          // logo de YouTube (rojo con triángulo blanco)
  const g = grupo(padre);
  const fondo = document.createElementNS(NS, 'path'); fondo.setAttribute('d', cajaR(-60, -42, 120, 84, 24)); fondo.setAttribute('fill', '#FF0033'); g.appendChild(fondo);
  const tri = document.createElementNS(NS, 'path'); tri.setAttribute('d', 'M-16,-22 L-16,22 L24,0 Z'); tri.setAttribute('fill', '#fff'); g.appendChild(tri);
  return g;
}
function pintarLogo(g, t, t0, x, y, s = 1) { const p = P(t, t0 - .05, .4, E.back); g.style.opacity = clamp(p * 2).toFixed(3); mover(g, x, y, s * lerp(.4, 1, p)); }
/* medidor de aguja (0..1) */
function medidor(padre, r = 160) {
  const g = grupo(padre);
  return { g, r, arco: trazo(g, `M${-r},0 A${r},${r} 0 0 1 ${r},0`, { ancho: 8 }), rojo: trazo(g, `M${r * Math.cos(-Math.PI * .22)},${r * Math.sin(-Math.PI * .22)} A${r},${r} 0 0 1 ${r},0`, { ancho: 14, color: C.raiz }),
    aguja: trazo(g, `M0,0 L${-r * .8},0`, { ancho: 9 }), eje: trazo(g, circulo(0, 0, 10), { ancho: 8 }) };
}
function pintarMedidor(m, t, t0, x, y, v, s = 1) {   // v 0..1
  mover(m.g, x, y, s); dibujar(m.arco, dib(t, t0, .5)); dibujar(m.rojo, dib(t, t0 + .3, .3)); dibujar(m.eje, dib(t, t0 + .4, .2));
  m.aguja.setAttribute('transform', `rotate(${(v * 180).toFixed(2)})`); dibujar(m.aguja, dib(t, t0 + .45, .2));
}
/* bocadillo de pensamiento/diálogo a la medida de su texto; cola hacia (cx, cy) */
function bocadillo(e, frase, tiempos, o = {}) {
  const tx = texto(e, frase, tiempos, { tam: o.tam || 72, ...o }), b = trazo(e.svg, '', { ancho: 6, fill: '#fff' });
  e.svg.appendChild(b); return { tx, b };   // el texto (HTML) queda por encima del SVG
}
function pintarBocadillo(bo, t, t0, x, y, cx, cy) {
  pt(bo.tx, t, { x, y }); const { w, h } = medir(bo.tx), W = w + 100, H = h + 70, x0 = x - W / 2, y0 = y - H / 2;
  const bx = clamp(cx, x0 + 60, x0 + W - 60);
  forma(bo.b, () => `M${x0 + 30},${y0} L${x0 + W - 30},${y0} Q${x0 + W},${y0} ${x0 + W},${y0 + 30} L${x0 + W},${y0 + H - 30} Q${x0 + W},${y0 + H} ${x0 + W - 30},${y0 + H} L${bx + 40},${y0 + H} L${cx},${cy} L${bx - 10},${y0 + H} L${x0 + 30},${y0 + H} Q${x0},${y0 + H} ${x0},${y0 + H - 30} L${x0},${y0 + 30} Q${x0},${y0} ${x0 + 30},${y0} Z`);
  dibujar(bo.b, dib(t, t0, .45));
}
/* recuadro a la medida de un texto (≥ 40 px de aire) */
function marco(e, el, o = {}) { const m = trazo(e.svg, '', { ancho: o.ancho || 6, color: o.color || NEGRO }); m._el = el; m._pad = o.pad || 44; return m; }
function pintarMarco(m, t, t0) {
  const o = m._el._o, { w, h } = medir(m._el), x = o.x - w * o.ax / 100, y = o.y - h * o.ay / 100, p = m._pad;
  forma(m, () => caja(x - p, y - p * .7, w + 2 * p, h + 1.4 * p)); dibujar(m, dib(t, t0, .5));
}
/* fila de lista con ✓ o ✗ */
function filaLista(e, frase, t0, o = {}) { return { tx: texto(e, frase, t0, { tam: o.tam || 72, ax: 0, ...o }), marca: trazo(e.svg, '', { ancho: 9, color: o.no ? COL.no : COL.ok }), no: o.no, t0 }; }
function pintarFila(f, t, x, y) { pt(f.tx, t, { x: x + 80, y }); forma(f.marca, () => f.no ? cruz(x + 20, y, .9) : tick(x + 20, y, .9)); dibujar(f.marca, dib(t, f.t0 + .1, .3)); }

/* ---------- tiempos de la voz: TW = [[palabra, inicio, fin], ...] (lo inyecta injertar.py desde trabajo/tiempos.json) ----------
   ts('frase dicha', desde) -> inicio de cada palabra, buscando la frase a partir de ~desde (s). Falla en consola si no está. */
const _nrm = w => w.toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '').replace(/[^a-z0-9ñ]/g, '');
function ts(frase, desde = 0) {
  const f = frase.replace(/\|[a-z]+/g, '').split(' ').map(_nrm);
  for (let k = 0; k < TW.length; k++) {
    if (TW[k][1] < desde - 1) continue;
    if (f.every((w, j) => k + j < TW.length && _nrm(TW[k + j][0]) === w)) return f.map((_, j) => TW[k + j][1]);
  }
  console.error(`ts: no encuentro «${frase}» desde ${desde}`); return f.map(() => desde);
}
const en = (palabra, desde) => ts(palabra, desde)[0];
const finDe = (frase, desde) => { const r = ts(frase, desde); const k = TW.findIndex(x => x[1] === r[r.length - 1]); return TW[k][2]; };
/* texto que se escribe con la voz: X(e, 'lo que se ve', desde, { dice: 'lo que dice si es distinto', ...opciones }) */
/* Lo que se escribe es lo que dice, casi literal. Solo un título de apartado («Fase 2», «Pilar 1»…) puede resumirlo:
   { apartado: true }. Si no, X() avisa cuando el texto no se parece a lo que dice. */
const _NUM = { un: '1', una: '1', uno: '1', primero: '1', dos: '2', segundo: '2', tres: '3', tercero: '3', cuatro: '4', cinco: '5', seis: '6', siete: '7', ocho: '8', nueve: '9', diez: '10' };
const _mismo = (a, b) => a === b || (Math.min(a.length, b.length) >= 3 && (a.startsWith(b.slice(0, 4)) || b.startsWith(a.slice(0, 4))));
const _parecido = (a, b) => { const p = x => x.replace(/\|[a-z]+/g, '').split(/[\s:·–-]+/).map(_nrm).filter(Boolean).map(w => _NUM[w] || w);
  const A = p(a), B = p(b); return A.filter(w => B.some(v => _mismo(w, v))).length / A.length; };
const X = (e, frase, desde, o = {}) => { if (o.dice && !o.apartado && _parecido(frase, o.dice) < .5) console.error(`X «${frase}»: no es lo que dice («${o.dice}»): usa sus palabras o { apartado: true }`); const d = o.dice ? ts(o.dice, desde) : ts(frase, desde), n = frase.split(' ').length;
  return texto(e, frase, d.length === n ? d : Array.from({ length: n }, (_, i) => n < 2 ? d[0] : lerp(d[0], d[d.length - 1], i / (n - 1))), o); };

/* ---------- siempre pasa algo: la cámara se acerca despacio durante cada animación ---------- */
function deriva(t) { const p = planoEn(t), w = p && p.tipo === 'anim' ? V[p.id] : null; return w ? 1 + .04 * clamp((t - w.a) / (w.b - w.a)) : 1; }

/* ---------- comprobador (herramientas/pizarra/revisar.mjs) ----------
   solapes(): textos, emojis y flechas que se pisan, o textos fuera de la zona 4:3. huella(): estado del contenido
   (sin la cámara) para medir cuánto tiempo se queda parada una animación. */
function _visibles() {
  const e = ESCENAS.find(x => x.div.style.display === 'block'); if (!e) return [];
  const r0 = STAGE.getBoundingClientRect(), k = 1920 / r0.width;   // coordenadas de la pantalla: con el acercamiento de la cámara, que empuja hacia los bordes
  const caja = el => { const r = el.getBoundingClientRect(); return { x0: (r.left - r0.left) * k, y0: (r.top - r0.top) * k, x1: (r.right - r0.left) * k, y1: (r.bottom - r0.top) * k }; };
  const vis = el => +getComputedStyle(el).opacity > .5;
  const out = [];
  e.div.querySelectorAll('.tx').forEach(el => { const sp = [...el.children].filter(vis); if (vis(el) && sp.length) {
    const cs = sp.map(caja); out.push({ tipo: 'texto', n: el.textContent, r: { x0: Math.min(...cs.map(c => c.x0)), y0: Math.min(...cs.map(c => c.y0)), x1: Math.max(...cs.map(c => c.x1)), y1: Math.max(...cs.map(c => c.y1)) } }); } });
  e.div.querySelectorAll('.emo').forEach(el => vis(el) && out.push({ tipo: 'emoji', n: el.textContent, r: caja(el) }));
  e.div.querySelectorAll('path[data-k]').forEach(el => { if (!vis(el)) return; const L = el.getTotalLength(), m = el.getScreenCTM(), sv = el.ownerSVGElement.getBoundingClientRect();
    const pts = []; for (let i = 0; i <= 24; i++) { const q = el.getPointAtLength(L * i / 24).matrixTransform(m); pts.push([(q.x - r0.left) * k, (q.y - r0.top) * k]); }
    out.push({ tipo: el.dataset.k, n: el.dataset.k, pts }); });
  return out;
}
function solapes() {
  const v = _visibles(), msg = [], dentroR = (p, r, m = 8) => p[0] > r.x0 - m && p[0] < r.x1 + m && p[1] > r.y0 - m && p[1] < r.y1 + m;
  const cruzan = (a, b) => a.x0 < b.x1 - 4 && b.x0 < a.x1 - 4 && a.y0 < b.y1 - 4 && b.y0 < a.y1 - 4;
  v.forEach((a, i) => {
    if (a.r && (a.r.x0 < Z43.x0 || a.r.x1 > Z43.x1)) msg.push(`fuera del 4:3: «${a.n}»`);
    v.slice(i + 1).forEach(b => {
      if (a.r && b.r && cruzan(a.r, b.r)) msg.push(`se pisan «${a.n}» y «${b.n}»`);
      const [r, p] = a.r && b.pts ? [a, b] : b.r && a.pts ? [b, a] : [];
      if (r && p.pts.some(q => dentroR(q, r.r))) msg.push(`${p.tipo} pisa «${r.n}»`);
    });
  });
  // en el reel (4:3) tiene que verse TODO, también dibujos y personajes, y el texto tiene que leerse
  const e = ESCENAS.find(x => x.div.style.display === 'block'), r0 = STAGE.getBoundingClientRect(), k = 1920 / r0.width;
  if (e) e.svg.querySelectorAll('path').forEach(el => { if (+getComputedStyle(el).opacity < .5) return; const r = el.getBoundingClientRect();
    if ((r.left - r0.left) * k < Z43.x0 || (r.right - r0.left) * k > Z43.x1) msg.push('dibujo fuera del 4:3'); });
  if (e) e.div.querySelectorAll('.tx').forEach(el => parseFloat(el.style.fontSize) < 56 && msg.push(`texto pequeño para el reel: «${el.textContent}»`));
  return [...new Set(msg)];
}
function huella() {
  const e = ESCENAS.find(x => x.div.style.display === 'block'); if (!e) return '';
  const q = (v, n = 10) => Math.round(+v * n);
  return [...e.div.querySelectorAll('.tx span, .emo, .ceja')].map(el => q(getComputedStyle(el).opacity) + el.textContent).join('|') + '#' +
    [...e.svg.querySelectorAll('path')].map(el => q(el.style.opacity || 0) + ':' + q(el.style.strokeDashoffset || 0, 20) + ':' + (el.getAttribute('d') || '').length + (el.getAttribute('transform') || '')).join('|');
}


/* ---------- flechas entre dos textos: salen del borde de la caja de uno y llegan al borde del otro (nunca los pisan) ---------- */
function _cajaTexto(el, pad = 44) { const o = el._o, { w, h } = medir(el), x = o.x - w * o.ax / 100, y = o.y - h * o.ay / 100;
  return { x0: x - pad, y0: y - pad * .7, x1: x + w + pad, y1: y + h + pad * .7, cx: x + w / 2, cy: y + h / 2 }; }
function _borde(c, dx, dy) { const tx = dx ? ((dx > 0 ? c.x1 : c.x0) - c.cx) / dx : Infinity, ty = dy ? ((dy > 0 ? c.y1 : c.y0) - c.cy) / dy : Infinity, k = Math.min(Math.abs(tx), Math.abs(ty)); return [c.cx + dx * k, c.cy + dy * k]; }
function unir(e, A, B, o = {}) { return { A, B, f: fl(e.svg, 0, 0, 1, 1, o), hueco: o.hueco ?? 22 }; }
function pintarUnion(u, t, t0, dur = .4) {
  const a = _cajaTexto(u.A), b = _cajaTexto(u.B), dx = b.cx - a.cx, dy = b.cy - a.cy, L = Math.hypot(dx, dy), ux = dx / L, uy = dy / L;
  const p = _borde(a, ux, uy), q = _borde(b, -ux, -uy);
  forma(u.f, () => flecha(p[0] + ux * u.hueco, p[1] + uy * u.hueco, q[0] - ux * u.hueco, q[1] - uy * u.hueco)); dibujar(u.f, dib(t, t0, dur));
}
/* móvil pequeño en la mano del stickman */
function movilMano(e) { return trazo(e.svg, '', { ancho: 5, fill: '#fff' }); }
function pintarMovilMano(m, t, t0, mano, s = 1) { forma(m, () => cajaR(mano.x - 22 * s, mano.y - 70 * s, 44 * s, 76 * s, 8 * s)); dibujar(m, dib(t, t0, .3)); }
