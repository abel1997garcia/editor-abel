/* c03 · F3 «energía y negocio» (generado por hacer_escenas.py). Un bloque por tramo de tablero */
const DEF = [[["t", "el miedo", "miedo", 460, 72], ["p", "ES DEL EGO", "ego", 580], ["e", "🎬", "película", 740], ["g", "te creas una película", "película", 870]], [["t", "…y te la crees|ac", "crees", 480], ["g", "si no te has trabajado", "trabajado", 640], ["e", "🧱", "suficiente", 800]], [["t", "una barrera|ac invisible|ac", "barrera", 540, 80], ["e", "🚧", "invisible", 740]], [["g", "miedo al fracaso", "fracaso", 470], ["p", "AL FINAL ES MIEDO", "final", 620], ["t", "lo que tú sientes", "sientes", 800]], [["t", "¿desde qué intención?", "intención", 480, 68], ["t", "puro ego|ac", "puro", 650, 96], ["e", "🎭", "ego", 820]], [["e", "❤️", "corazón", 540, 150], ["t", "lo que se te da bien", "bien", 750], ["g", "lo sabes por dentro", "interiormente", 860]]];
DEF.forEach((items, i) => { if (!TABLEROS[i]) return;
  bloque(...TABLEROS[i], (a) => {
    const els = items.map(([k, s, w, y, tam]) => { const t0 = en(w, a);
      const e = k === 'e' ? emoji(s, t0 - .1, tam || 120) : k === 'p' ? pastilla(s, t0, { ac: true, tam: tam || 46 })
              : texto(s, t0, { tam: tam || (k === 'g' ? 50 : 64), m: k === 'g' });
      return [k, e, y]; });
    return t => els.forEach(([k, e, y]) => (k === 'e' ? pe(e, t, 540, y) : pt(e, t, 540, y)));
  });
});
