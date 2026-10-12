/* t01 · F3 «energía y negocio» (generado por hacer_escenas.py). Un bloque por tramo de tablero */
const DEF = [[["t", "estresado|ac", "estresado", 500, 96], ["e", "😵", "pensando", 680], ["g", "en eso, en eso, en eso…", "eso", 850]], [["t", "cambias tu modo de vida", "cambiar", 520], ["e", "🙄", "hostia", 740]], [["t", "una parte de obsesión|ac", "obsesión", 480, 68], ["g", "nadie consigue éxito sin ella", "nadie", 640], ["e", "🎯", "éxito", 800]], [["g", "sabes dónde vas", "dónde", 480], ["p", "FOCO", "foco", 620], ["t", "toda tu energía|ac", "energía", 790]], [["t", "energía bien usada|ac", "correcta", 500], ["e", "🔗", "conectado", 690], ["g", "conectado con algo", "algo", 860]], [["e", "🐎", "caballos", 560, 170], ["t", "anteojeras|ac", "ojos", 780, 80]]];
DEF.forEach((items, i) => { if (!TABLEROS[i]) return;
  bloque(...TABLEROS[i], (a) => {
    const els = items.map(([k, s, w, y, tam]) => { const t0 = en(w, a);
      const e = k === 'e' ? emoji(s, t0 - .1, tam || 120) : k === 'p' ? pastilla(s, t0, { ac: true, tam: tam || 46 })
              : texto(s, t0, { tam: tam || (k === 'g' ? 50 : 64), m: k === 'g' });
      return [k, e, y]; });
    return t => els.forEach(([k, e, y]) => (k === 'e' ? pe(e, t, 540, y) : pt(e, t, 540, y)));
  });
});
