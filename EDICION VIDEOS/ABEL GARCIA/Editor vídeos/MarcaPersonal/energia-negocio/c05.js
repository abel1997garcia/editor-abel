/* c05 · F3 «energía y negocio» (generado por hacer_escenas.py). Un bloque por tramo de tablero */
const DEF = [[["t", "nada te llena|ac", "llene", 500, 84], ["e", "🏋️", "gimnasio", 690], ["g", "el gimnasio está bien", "gimnasio", 850]], [["t", "energía extra|ac", "energía", 480], ["g", "¿dónde la pones?", "ponerla", 620], ["t", "3 veces al gimnasio", "tres", 780], ["e", "❌", "gimnasio", 880, 80]], [["e", "🎥", "grabo", 540, 150], ["t", "me grabo un vídeo|ac", "vídeo", 750], ["g", "explico algo", "explico", 860]], [["t", "lo que has aprendido", "aprendido", 480], ["t", "ayuda a los demás|ac", "ayudar", 640], ["e", "✨", "bien", 800]], [["t", "más conectado|ac", "conectado", 480], ["g", "con quien eres tú", "quien", 590], ["e", "🚀", "petardo", 760, 130]], [["g", "tu marca personal", "marca", 480], ["p", "EL VERDADERO PODER", "verdadero", 640], ["e", "⚡", "poder", 800]], [["e", "🔋", "pilas", 520, 130], ["t", "una persona real", "persona", 700], ["t", "su propia experiencia|ac", "experiencia", 830]]];
DEF.forEach((items, i) => { if (!TABLEROS[i]) return;
  bloque(...TABLEROS[i], (a) => {
    const els = items.map(([k, s, w, y, tam]) => { const t0 = en(w, a);
      const e = k === 'e' ? emoji(s, t0 - .1, tam || 120) : k === 'p' ? pastilla(s, t0, { ac: true, tam: tam || 46 })
              : texto(s, t0, { tam: tam || (k === 'g' ? 50 : 64), m: k === 'g' });
      return [k, e, y]; });
    return t => els.forEach(([k, e, y]) => (k === 'e' ? pe(e, t, 540, y) : pt(e, t, 540, y)));
  });
});
