/* c02 · F3 «energía y negocio» (generado por hacer_escenas.py). Un bloque por tramo de tablero */
const DEF = [[["g", "creencias limitantes", "creencias", 470], ["t", "está todo|ac inventado|ac", "está", 620, 76], ["e", "💡", "inventado", 800]], [["t", "tus experiencias|ac", "experiencias", 500], ["e", "🌍", "mundo", 680], ["g", "tu forma de ver el mundo", "manera", 850]], [["t", "abundancia|ac", "abundancia", 580, 110], ["e", "🌱", "abundancia", 780]], [["t", "5 personas", "cinco", 470], ["e", "👥", "personas", 630, 80], ["t", "venden lo mismo|ac", "venden", 800]], [["g", "«descarta a las demás»", "descarta", 480], ["p", "MENTIRA", "mentira", 650], ["e", "❌", "mentira", 820]], [["t", "la experiencia de uno", "experiencia", 470], ["g", "no la tiene el otro", "tiene", 570], ["e", "🔁", "revés", 700], ["t", "el juego es abundancia|ac", "juego", 860]]];
DEF.forEach((items, i) => { if (!TABLEROS[i]) return;
  bloque(...TABLEROS[i], (a) => {
    const els = items.map(([k, s, w, y, tam]) => { const t0 = en(w, a);
      const e = k === 'e' ? emoji(s, t0 - .1, tam || 120) : k === 'p' ? pastilla(s, t0, { ac: true, tam: tam || 46 })
              : texto(s, t0, { tam: tam || (k === 'g' ? 50 : 64), m: k === 'g' });
      return [k, e, y]; });
    return t => els.forEach(([k, e, y]) => (k === 'e' ? pe(e, t, 540, y) : pt(e, t, 540, y)));
  });
});
