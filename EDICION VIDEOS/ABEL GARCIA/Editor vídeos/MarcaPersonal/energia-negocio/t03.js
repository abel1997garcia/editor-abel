/* t03 · F3 «energía y negocio» (generado por hacer_escenas.py). Un bloque por tramo de tablero */
const DEF = [[["e", "🤝", "manita", 540, 150], ["t", "que te cojan de la manita|ac", "cojan", 760]], [["t", "tu ego|ac", "ego", 540, 100], ["e", "🗣️", "dice", 740]], [["t", "¿cuántos vídeos?", "cuántos", 500], ["t", "¿qué hago exactamente?|ac", "exactamente", 660], ["e", "📋", "exactamente", 820]], [["t", "50 vídeos|ac", "50", 540, 100], ["e", "📺", "vídeos", 750]], [["t", "más energía", "energía", 500], ["t", "ganar más dinero|ac", "dinero", 660], ["e", "💰", "dinero", 820]], [["t", "ayudar a los demás|ac", "ayudar", 540], ["e", "🙌", "demás", 730]], [["g", "no falta información", "información", 520], ["p", "FALTA APLICACIÓN", "aplicación", 690]]];
DEF.forEach((items, i) => { if (!TABLEROS[i]) return;
  bloque(...TABLEROS[i], (a) => {
    const els = items.map(([k, s, w, y, tam]) => { const t0 = en(w, a);
      const e = k === 'e' ? emoji(s, t0 - .1, tam || 120) : k === 'p' ? pastilla(s, t0, { ac: true, tam: tam || 46 })
              : texto(s, t0, { tam: tam || (k === 'g' ? 50 : 64), m: k === 'g' });
      return [k, e, y]; });
    return t => els.forEach(([k, e, y]) => (k === 'e' ? pe(e, t, 540, y) : pt(e, t, 540, y)));
  });
});
