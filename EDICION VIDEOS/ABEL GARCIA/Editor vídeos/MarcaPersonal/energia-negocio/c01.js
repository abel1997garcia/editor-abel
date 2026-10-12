/* c01 · F3 «energía y negocio» (generado por hacer_escenas.py). Un bloque por tramo de tablero */
const DEF = [[["t", "el éxito", "éxito", 470], ["t", "una parte de obsesión|ac", "obsesión", 600, 72], ["e", "🎯", "nadie", 790]], [["t", "cambias tu modo de vida", "cambiar", 480], ["g", "«igual estás obsesionado»", "igual", 640], ["e", "🙄", "obsesionado", 800]], [["t", "toda tu energía|ac", "energía", 480], ["g", "en una sola cosa", "eso", 600], ["t", "estrés", "estresado", 720, 80], ["e", "😵", "estresado", 840]], [["t", "mil|ac vueltas|ac", "mil", 520, 100], ["e", "🌀", "vueltas", 690], ["g", "no comprendes nada", "comprendes", 850]], [["g", "tu energía repartida en…", "destinando", 470], ["t", "80 cosas|ac", "80", 620, 120], ["t", "estrés", "estrés", 800]], [["t", "conectado|ac con algo", "conectado", 500], ["e", "🔗", "algo", 660], ["p", "UN PROYECTO", "proyecto", 830]], [["e", "🐎", "caballos", 560, 170], ["t", "anteojeras|ac", "ojos", 780, 80], ["g", "una sola dirección", "ojos", 870]]];
DEF.forEach((items, i) => { if (!TABLEROS[i]) return;
  bloque(...TABLEROS[i], (a) => {
    const els = items.map(([k, s, w, y, tam]) => { const t0 = en(w, a);
      const e = k === 'e' ? emoji(s, t0 - .1, tam || 120) : k === 'p' ? pastilla(s, t0, { ac: true, tam: tam || 46 })
              : texto(s, t0, { tam: tam || (k === 'g' ? 50 : 64), m: k === 'g' });
      return [k, e, y]; });
    return t => els.forEach(([k, e, y]) => (k === 'e' ? pe(e, t, 540, y) : pt(e, t, 540, y)));
  });
});
