/* F3 LIGERO (Abel 13/10/2026): los gráficos del tablero salen solos de lo que dice, sin diseñar escena a escena.
   En cada tramo de tablero, su frase en grande palabra a palabra (aparece cuando la dice), la palabra clave en el color
   de acento con subrayado y «pop», y las cifras contando. Si la frase no cabe, se pasa de página dentro del tramo.
   CLAVES (opcional, en datos.js): palabras a destacar en este reel; si no, se elige sola (léxico de la marca o la más larga). */
const STOP = new Set('que de la el en y a los las un una no es lo se te tu tus por con para mas más pero o si me mi ya al del le les su sus muy eso esto este esta yo tú como cuando porque pues entonces también hay ha he has son era fue ser estar está estás tienes tiene tengo vas va voy hacer hace así todo toda todos nada algo bien'.split(' '));
const LEX = ['precio', 'precios', 'cobrar', 'cobras', 'cobro', 'clientes', 'cliente', 'agenda', 'vender', 'vendes', 'venta', 'ventas', 'marca', 'autentico', 'autentica', 'autenticidad',
  'miedo', 'miedos', 'verguenza', 'contenido', 'dinero', 'gratis', 'regalar', 'valor', 'testimonios', 'energia', 'exito', 'foco', 'obsesion', 'confianza', 'verdad', 'estres',
  'competencia', 'abundancia', 'ego', 'careta', 'esclavo', 'impostor', 'compromiso', 'barato', 'caro', 'perseguir', 'grabar', 'publicar', 'critica', 'hate', 'emociones'];
const limpia = w => w.replace(/^[¿¡«"“(]+|[.,;:!?»"”)…]+$/g, '');
const esCifra = w => /\d/.test(w);
function clave(ws) {
  const c = (typeof CLAVES !== 'undefined' ? CLAVES : []).map(norm);
  let i = ws.findIndex(w => c.includes(norm(w[0]))); if (i >= 0) return i;
  i = ws.findIndex(w => esCifra(w[0])); if (i >= 0) return i;
  i = ws.findIndex(w => LEX.includes(norm(w[0]))); if (i >= 0) return i;
  let best = -1, L = 5; ws.forEach((w, j) => { const n = norm(w[0]); if (!STOP.has(n) && n.length > L) { L = n.length; best = j; } }); return best;
}
const MAL_FIN = new Set('a de la el los las un una en con por para tu tus mi mis su sus que y o te se le lo me nos del al muy más mas'.split(' '));
const INICIO = new Set('porque pero y cuando que si para ese esa eso esto este esta como donde aunque entonces sino'.split(' '));
/* un trozo largo se parte por donde corta el sentido: pausas, antes de «porque/pero/y…», nunca tras «a/de/la/tu…» */
function partir(tz) {
  if (tz.length <= MAXPAL) return [tz];
  let mejor = -1, coste = 1e9;
  for (let i = 2; i <= tz.length - 2; i++) {
    const fin = norm(tz[i - 1].w[0]), ini = norm(tz[i].w[0]), hueco = tz[i].w[1] - tz[i - 1].w[2];
    const c = Math.abs(i - tz.length / 2) + (MAL_FIN.has(fin) ? 12 : 0) - (INICIO.has(ini) ? 3 : 0) - hueco * 25 + (esCifra(fin) ? 12 : 0);
    if (c < coste) { coste = c; mejor = i; }
  }
  return [...partir(tz.slice(0, mejor)), ...partir(tz.slice(mejor))];
}
const ANCHO = 930, ZONA = [440, 930], MAXPAL = 7;   // como mucho ~7 palabras por página: grande y con impacto        // los gráficos del tablero viven en y 420–930 (debajo, su tarjeta)

TABLEROS.forEach(([a, b], ti) => {
  const ws = PAL.filter(w => w[1] >= a - .05 && w[1] < b - .05 && limpia(w[0]));
  if (!ws.length) return;
  bloque(a, b, () => {
    let paginas = null; const raya = path('', AC, 14);          // la raya vive en el grupo de este bloque (se oculta con él)
    const items = ws.map(w => { const e = el('big', limpia(w[0])); e._t0 = w[1]; return { e, w }; });
    function maqueta() {                       // se mide con la fuente ya cargada (primer pintado)
      const base = ti === 0 ? 132 : 120, MIN = 88;
      const ancho = (it, s) => { it.e.style.fontSize = s + 'px'; return it.e.offsetWidth; };
      const lineas = (lst, s) => { const L = [[]]; let x = 0; for (const it of lst) { const wd = ancho(it, s), esp = s * .27;
        if (L.at(-1).length && x + esp + wd > ANCHO) { L.push([]); x = 0; } x += (L.at(-1).length ? esp : 0) + wd; L.at(-1).push([it, wd]); }
        const anchoL = ln => ln.reduce((x, [, wd]) => x + wd, 0) + s * .27 * (ln.length - 1);
        if (L.length > 1 && L.at(-1).length === 1 && L.at(-2).length >= 3) {          // sin una palabra sola en la última línea
          const m = L.at(-2).pop(); L.at(-1).unshift(m); if (anchoL(L.at(-1)) > ANCHO) L.at(-1).shift() && L.at(-2).push(m); }
        return L; };
      // páginas por las PAUSAS de su voz (o signos), no por número de palabras: cada pantalla es un trozo de frase con sentido
      const trozos = [[]];
      items.forEach((it, k) => { trozos.at(-1).push(it); const sig = items[k + 1];
        if (sig && (sig.w[1] - it.w[2] >= .18 || /[.,;:!?…]$/.test(it.w[0]))) trozos.push([]); });
      const grupos = [];
      for (const tz of trozos.filter(x => x.length)) {
        for (const g of partir(tz)) {
          const prev = grupos.at(-1);
          if (prev && (g.length <= 2 || prev.length <= 2) && prev.length + g.length <= MAXPAL + 2) prev.push(...g); else grupos.push(g);
        }
      }
      paginas = [];
      for (const g of grupos) {                                                         // cada página en ≤ 3 líneas (mejor 2) a ≥ MIN px
        let s = base, L = lineas(g, s);
        while ((L.length > 3 || (L.length === 3 && g.length <= 5)) && s > MIN) { s -= 6; L = lineas(g, s); }
        const k = clave(g.map(i => i.w));
        paginas.push({ t0: g[0].w[1] - .1, s, L, k: k >= 0 ? g[k] : null });
      }
      paginas.forEach((p, j) => { p.t1 = j + 1 < paginas.length ? paginas[j + 1].t0 : b + .45;
        const lh = p.s * 1.12, H = lh * p.L.length, y0 = (ZONA[0] + ZONA[1]) / 2 - H / 2 + lh / 2;
        p.L.forEach((ln, r) => { const W = ln.reduce((x, [, wd]) => x + wd, 0) + p.s * .27 * (ln.length - 1); let x = 540 - W / 2;
          ln.forEach(([it, wd]) => { it.x = x + wd / 2; it.y = y0 + r * lh; it.s = p.s; it.p = p; x += wd + p.s * .27; }); });
        if (p.k) suena(p.k.w[1] - .05, 'pop', .28);
      });
    }
    return t => {
      if (!paginas) maqueta();
      const p = paginas.find(q => t >= q.t0 && t < q.t1) || (t < paginas[0].t0 ? null : paginas.at(-1));
      const ent = p ? out(P(t, p.t0, .22)) : 0, sal = p ? 1 - P(t, p.t1 - .18, .18) : 0;
      for (const it of items) {                // la página entra entera en gris claro; cada palabra se enciende cuando la dice
        if (!p || it.p !== p) { it.e.style.opacity = 0; continue; }
        const dicha = t >= it.w[1] - .06, esK = p.k === it, u = P(t, it.w[1] - .06, esK ? .4 : .25);
        it.e.style.color = dicha ? (esK ? AC : NEGRO) : '#cdcdcd';
        const s = dicha ? (esK ? lerp(1.28, 1, back(u)) : lerp(1.1, 1, out(u))) : 1;
        if (esCifra(it.w[0])) { const m = it.w[0].match(/[\d.]+/)[0].replace(/\./g, ''), v = dicha ? Math.round(+m * out(P(t, it.w[1] - .06, .6))) : 0;
          it.e.textContent = limpia(it.w[0]).replace(/[\d.]+/, v.toLocaleString('es-ES')); }
        pon(it.e, it.x, it.y + 22 * (1 - ent), s, ent * sal * KT);
      }
      if (p && p.k) { const k = p.k, w2 = k.e.offsetWidth / 2, y = k.y + k.s * .55;
        raya.setAttribute('d', `M${(k.x - w2).toFixed(1)},${y.toFixed(1)} L${(k.x + w2).toFixed(1)},${y.toFixed(1)}`);
        dib(raya, out(P(t, k.w[1] + .05, .35)), sal * KT); } else dib(raya, 0, 0);
    };
  });
});
