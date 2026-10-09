/* Piezas de las miniaturas de Abel: mismo trazo que sus vídeos de pizarra (herramientas/pizarra/libreria.js). */
const NEGRO = '#111111', GRIS = '#9a9a9a';
const C = { raiz: '#C8372D', sacro: '#E06A1B', plexo: '#C99A00', corazon: '#1E7A46', garganta: '#1D7FD1', ojo: '#3F3FB5', corona: '#7A3FC4' };
const NS = 'http://www.w3.org/2000/svg';
const GROSOR = 1.4;   // las miniaturas se ven a ~170 px de ancho en el móvil: trazos más gordos que en el vídeo
let _sem = 7;
const az = () => (_sem = (_sem * 16807) % 2147483647) / 2147483647 - .5;
const linea = (x1, y1, x2, y2, j = 3) => `M${x1},${y1} Q${((x1 + x2) / 2 + az() * j * 2).toFixed(1)},${((y1 + y2) / 2 + az() * j * 2).toFixed(1)} ${x2},${y2}`;
const flecha = (x1, y1, x2, y2, k = 26) => { const a = Math.atan2(y2 - y1, x2 - x1);
  return linea(x1, y1, x2, y2) + ` M${(x2 - k * Math.cos(a - .5)).toFixed(1)},${(y2 - k * Math.sin(a - .5)).toFixed(1)} L${x2},${y2} L${(x2 - k * Math.cos(a + .5)).toFixed(1)},${(y2 - k * Math.sin(a + .5)).toFixed(1)}`; };

function svg(padre = document.getElementById('escena')) {
  const s = document.createElementNS(NS, 'svg'); s.setAttribute('viewBox', '0 0 1280 720'); s.classList.add('capa'); padre.appendChild(s); return s; }
function grupo(padre, x = 0, y = 0, s = 1, r = 0) {
  const g = document.createElementNS(NS, 'g'); g.setAttribute('transform', `translate(${x},${y}) rotate(${r}) scale(${s})`); padre.appendChild(g); return g; }
function trazo(g, d, o = {}) {
  const p = document.createElementNS(NS, 'path'); p.setAttribute('d', d);
  p.setAttribute('fill', o.relleno || 'none'); p.setAttribute('stroke', o.color || NEGRO);
  p.setAttribute('stroke-width', (o.ancho || 7) * GROSOR); p.setAttribute('stroke-linecap', 'round'); p.setAttribute('stroke-linejoin', 'round');
  if (o.vector !== false) p.setAttribute('vector-effect', 'non-scaling-stroke');
  g.appendChild(p); return p; }

/* la silueta grande (boceto de Abel): 694 de alto, eje x = 0, pies en y = 694 */
const MITAD = [[[-30, 128], [-52, 140], [-62, 162]], [[-76, 205], [-86, 300], [-86, 398]], [[-86, 432], [-60, 436], [-58, 404]],
  [[-56, 330], [-50, 262], [-44, 222]], [[-44, 300], [-46, 362], [-44, 424]], [[-48, 505], [-50, 585], [-46, 662]],
  [[-44, 694], [-14, 694], [-12, 662]], [[-10, 592], [-8, 524], [0, 466]]];
function siluetaD() {
  const f = ([x, y]) => `${x},${y}`, m = ([x, y]) => [-x, y], ini = [-13, 122];
  let d = `M${f(ini)} `; MITAD.forEach(([a, b, c]) => d += `C${f(a)} ${f(b)} ${f(c)} `);
  for (let i = MITAD.length - 1; i >= 0; i--) { const [a, b] = MITAD[i]; d += `C${f(m(b))} ${f(m(a))} ${f(m(i ? MITAD[i - 1][2] : ini))} `; }
  return d; }
const SIL_CABEZA = 'M-40,58 C-40,22 -18,4 2,4 C24,4 40,26 40,60 C40,92 22,112 0,112 C-22,112 -40,94 -40,58 Z';
const CENTROS = { corona: -18, ojo: 56, garganta: 140, corazon: 224, plexo: 306, sacro: 384, raiz: 446 };
/* x = eje, y = pies; devuelve una función para pasar coordenadas de la silueta al lienzo */
function silueta(s, x, y, esc = 1, o = {}) {
  const g = grupo(s, x, y - 694 * esc, esc);
  trazo(g, SIL_CABEZA, { ancho: o.ancho || 7, relleno: o.relleno }); trazo(g, siluetaD(), { ancho: o.ancho || 7, relleno: o.relleno });
  return (px, py) => [x + px * esc, y - 694 * esc + py * esc]; }

/* stickman sencillo de una pieza (cabeza + cuerpo), x = eje, y = pies */
function stickman(s, x, y, esc = 1, pose = {}) {
  const g = grupo(s, x, y, esc), b = pose.brazos || [[-40, -150], [40, -150]], p = pose.piernas || [[-26, 0], [26, 0]];
  trazo(g, 'M0,-232 m-26,0 a26,26 0 1,0 52,0 a26,26 0 1,0 -52,0');
  trazo(g, `M0,-206 L0,-96 M0,-180 L${b[0]} M0,-180 L${b[1]} M0,-96 L${p[0]} M0,-96 L${p[1]}`.replace(/L(-?\d+),(-?\d+)/g, 'L$1,$2'));
  return g; }

function texto(html, o = {}) {
  const el = document.createElement('div'); el.className = 'tx ' + (o.clase || ''); el.innerHTML = html;
  Object.assign(el.style, { left: (o.x ?? 60) + 'px', top: (o.y ?? 60) + 'px', fontSize: (o.tam || 110) + 'px' }, o.css || {});
  document.getElementById('escena').appendChild(el); return el; }

/* contorno continuo a partir de media silueta (lista de tramos cúbicos), reflejada en x = 0 */
function contornoD(mitad, ini) {
  const f = ([x, y]) => `${x},${y}`, m = ([x, y]) => [-x, y];
  let d = `M${f(ini)} `; mitad.forEach(([a, b, c]) => d += `C${f(a)} ${f(b)} ${f(c)} `);
  for (let i = mitad.length - 1; i >= 0; i--) { const [a, b] = mitad[i]; d += `C${f(m(b))} ${f(m(a))} ${f(m(i ? mitad[i - 1][2] : ini))} `; }
  return d; }
/* silueta de mujer en el mismo trazo que la de Abel (contorno continuo, pelo largo, vestido); x = eje, y = pies */
const MUJER = [[[-20, 128], [-44, 134], [-54, 154]], [[-64, 200], [-68, 280], [-68, 336]], [[-68, 354], [-52, 356], [-52, 340]],
  [[-52, 300], [-48, 240], [-44, 206]], [[-42, 250], [-34, 280], [-36, 302]], [[-42, 360], [-78, 460], [-90, 540]],
  [[-60, 548], [-32, 548], [-24, 546]], [[-24, 600], [-24, 660], [-24, 686]], [[-24, 698], [-6, 698], [-6, 686]], [[-6, 640], [-4, 600], [0, 560]]];
const MUJER_PELO = 'M-34,48 C-40,4 40,4 34,48 C40,92 44,140 58,176 C44,182 34,170 30,150 M-34,48 C-40,92 -44,140 -58,176 C-44,182 -34,170 -30,150';
function siluetaMujer(s, x, y, esc = 1, o = {}) {
  const g = grupo(s, x, y - 694 * esc, esc), w = o.ancho || 7;
  trazo(g, MUJER_PELO, { ancho: w });
  trazo(g, 'M-34,60 C-34,26 -16,10 2,10 C22,10 34,30 34,62 C34,92 20,110 0,110 C-20,110 -34,92 -34,60 Z', { ancho: w, relleno: '#fff' });
  trazo(g, contornoD(MUJER, [-12, 112]), { ancho: w });
  return (px, py) => [x + px * esc, y - 694 * esc + py * esc]; }

/* Abel colocado por su cara: caja = [x0,y0,x1,y1] normalizada (de caras.json), la cara se centra en (cx, cy) con alto `alto` */
function fotoCara(src, caja, { cx = 880, cy = 267, alto = 270, W = 1920, H = 1080 } = {}) {
  const k = alto / ((caja[3] - caja[1]) * H), fx = (caja[0] + caja[2]) / 2 * W, fy = (caja[1] + caja[3]) / 2 * H;
  return foto(src, { x: cx - fx * k, y: cy - fy * k, ancho: W * k }); }

/* foto recortada de Abel: el recorte es el fotograma entero (1920x1080) con fondo transparente */
function foto(src, o = {}) {
  const im = document.createElement('img'); im.src = src; im.className = 'abel' + (o.clase ? ' ' + o.clase : '');
  Object.assign(im.style, { left: (o.x || 0) + 'px', top: (o.y || 0) + 'px', width: (o.ancho || 1920) + 'px' }, o.css || {});
  document.getElementById('escena').appendChild(im); return im; }
