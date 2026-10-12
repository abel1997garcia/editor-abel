/* c04 · F3 «energía y negocio» (generado por hacer_escenas.py). Un bloque por tramo de tablero */
const DEF = [[["g", "no falta información", "información", 480], ["p", "FALTA APLICACIÓN", "aplicación", 640], ["e", "🛠️", "lograr", 800]], [["t", "si no lo tengo estructurado|ac", "estructurado", 500, 64], ["e", "📋", "súper", 680], ["g", "…no hago nada", "mierda", 850]], [["e", "🤝", "manita", 540, 150], ["t", "que te cojan de la manita|ac", "cojan", 750], ["g", "por todos los procesos", "procesos", 860]], [["g", "¿quién lo tiene que hacer?", "adivina", 460], ["p", "TÚ", "tú", 580], ["t", "50 vídeos|ac", "50", 740, 84], ["e", "📺", "vídeos", 860]], [["t", "más confianza", "confianza", 480], ["t", "más energía", "energía", 600], ["e", "💪", "hombre", 760]], [["t", "ayudar a los demás|ac", "ayudar", 520], ["e", "🙌", "demás", 690], ["g", "con lo que se te da bien", "aportando", 850]]];
DEF.forEach((items, i) => { if (!TABLEROS[i]) return;
  bloque(...TABLEROS[i], (a) => {
    const els = items.map(([k, s, w, y, tam]) => { const t0 = en(w, a);
      const e = k === 'e' ? emoji(s, t0 - .1, tam || 120) : k === 'p' ? pastilla(s, t0, { ac: true, tam: tam || 46 })
              : texto(s, t0, { tam: tam || (k === 'g' ? 50 : 64), m: k === 'g' });
      return [k, e, y]; });
    return t => els.forEach(([k, e, y]) => (k === 'e' ? pe(e, t, 540, y) : pt(e, t, 540, y)));
  });
});
