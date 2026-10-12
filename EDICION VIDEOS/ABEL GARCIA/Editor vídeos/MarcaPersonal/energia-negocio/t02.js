/* t02 · F3 «energía y negocio» (generado por hacer_escenas.py). Un bloque por tramo de tablero */
const DEF = [[["t", "5 personas", "cinco", 470], ["e", "👥", "personas", 610, 76], ["t", "venden lo mismo|ac", "venden", 770], ["e", "🛒", "cliente", 880, 80]], [["p", "MENTIRA", "mentira", 500], ["g", "creencias limitantes", "creencias", 650], ["t", "está todo|ac inventado|ac", "inventado", 800, 70]], [["t", "tus experiencias|ac", "experiencias", 520], ["e", "🌍", "mundo", 720]], [["t", "abundancia|ac", "abundancia", 560, 100], ["g", "puedes invertir en varios", "invertir", 780]], [["t", "la experiencia de uno", "experiencia", 480], ["e", "🔁", "revés", 660], ["t", "el juego es abundancia|ac", "juego", 830]]];
DEF.forEach((items, i) => { if (!TABLEROS[i]) return;
  bloque(...TABLEROS[i], (a) => {
    const els = items.map(([k, s, w, y, tam]) => { const t0 = en(w, a);
      const e = k === 'e' ? emoji(s, t0 - .1, tam || 120) : k === 'p' ? pastilla(s, t0, { ac: true, tam: tam || 46 })
              : texto(s, t0, { tam: tam || (k === 'g' ? 50 : 64), m: k === 'g' });
      return [k, e, y]; });
    return t => els.forEach(([k, e, y]) => (k === 'e' ? pe(e, t, 540, y) : pt(e, t, 540, y)));
  });
});
