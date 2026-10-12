"""Escenas F3 de «energía y negocio»: un bloque por tramo de tablero; cada elemento entra con la palabra que lo dice.
Elemento: (tipo, texto, palabra, y[, tam]) · tipo t = texto (|ac colorea la palabra), g = texto gris pequeño, p = pastilla de acento, e = emoji."""
import json
from pathlib import Path

E = {
 'c01': [[('t', 'el éxito', 'éxito', 470), ('t', 'una parte de obsesión|ac', 'obsesión', 600, 72), ('e', '🎯', 'nadie', 790)],
         [('t', 'cambias tu modo de vida', 'cambiar', 480), ('g', '«igual estás obsesionado»', 'igual', 640), ('e', '🙄', 'obsesionado', 800)],
         [('t', 'toda tu energía|ac', 'energía', 480), ('g', 'en una sola cosa', 'eso', 600), ('t', 'estrés', 'estresado', 720, 80), ('e', '😵', 'estresado', 840)],
         [('t', 'mil|ac vueltas|ac', 'mil', 520, 100), ('e', '🌀', 'vueltas', 690), ('g', 'no comprendes nada', 'comprendes', 850)],
         [('g', 'tu energía repartida en…', 'destinando', 470), ('t', '80 cosas|ac', '80', 620, 120), ('t', 'estrés', 'estrés', 800)],
         [('t', 'conectado|ac con algo', 'conectado', 500), ('e', '🔗', 'algo', 660), ('p', 'UN PROYECTO', 'proyecto', 830)],
         [('e', '🐎', 'caballos', 560, 170), ('t', 'anteojeras|ac', 'ojos', 780, 80), ('g', 'una sola dirección', 'ojos', 870)]],
 'c02': [[('g', 'creencias limitantes', 'creencias', 470), ('t', 'está todo|ac inventado|ac', 'está', 620, 76), ('e', '💡', 'inventado', 800)],
         [('t', 'tus experiencias|ac', 'experiencias', 500), ('e', '🌍', 'mundo', 680), ('g', 'tu forma de ver el mundo', 'manera', 850)],
         [('t', 'abundancia|ac', 'abundancia', 580, 110), ('e', '🌱', 'abundancia', 780)],
         [('t', '5 personas', 'cinco', 470), ('e', '👥', 'personas', 630, 80), ('t', 'venden lo mismo|ac', 'venden', 800)],
         [('g', '«descarta a las demás»', 'descarta', 480), ('p', 'MENTIRA', 'mentira', 650), ('e', '❌', 'mentira', 820)],
         [('t', 'la experiencia de uno', 'experiencia', 470), ('g', 'no la tiene el otro', 'tiene', 570), ('e', '🔁', 'revés', 700), ('t', 'el juego es abundancia|ac', 'juego', 860)]],
 'c03': [[('t', 'el miedo', 'miedo', 460, 72), ('p', 'ES DEL EGO', 'ego', 580), ('e', '🎬', 'película', 740), ('g', 'te creas una película', 'película', 870)],
         [('t', '…y te la crees|ac', 'crees', 480), ('g', 'si no te has trabajado', 'trabajado', 640), ('e', '🧱', 'suficiente', 800)],
         [('t', 'una barrera|ac invisible|ac', 'barrera', 540, 80), ('e', '🚧', 'invisible', 740)],
         [('g', 'miedo al fracaso', 'fracaso', 470), ('p', 'AL FINAL ES MIEDO', 'final', 620), ('t', 'lo que tú sientes', 'sientes', 800)],
         [('t', '¿desde qué intención?', 'intención', 480, 68), ('t', 'puro ego|ac', 'puro', 650, 96), ('e', '🎭', 'ego', 820)],
         [('e', '❤️', 'corazón', 540, 150), ('t', 'lo que se te da bien', 'bien', 750), ('g', 'lo sabes por dentro', 'interiormente', 860)]],
 'c04': [[('g', 'no falta información', 'información', 480), ('p', 'FALTA APLICACIÓN', 'aplicación', 640), ('e', '🛠️', 'lograr', 800)],
         [('t', 'si no lo tengo estructurado|ac', 'estructurado', 500, 64), ('e', '📋', 'súper', 680), ('g', '…no hago nada', 'mierda', 850)],
         [('e', '🤝', 'manita', 540, 150), ('t', 'que te cojan de la manita|ac', 'cojan', 750), ('g', 'por todos los procesos', 'procesos', 860)],
         [('g', '¿quién lo tiene que hacer?', 'adivina', 460), ('p', 'TÚ', 'tú', 580), ('t', '50 vídeos|ac', '50', 740, 84), ('e', '📺', 'vídeos', 860)],
         [('t', 'más confianza', 'confianza', 480), ('t', 'más energía', 'energía', 600), ('e', '💪', 'hombre', 760)],
         [('t', 'ayudar a los demás|ac', 'ayudar', 520), ('e', '🙌', 'demás', 690), ('g', 'con lo que se te da bien', 'aportando', 850)]],
 'c05': [[('t', 'nada te llena|ac', 'llene', 500, 84), ('e', '🏋️', 'gimnasio', 690), ('g', 'el gimnasio está bien', 'gimnasio', 850)],
         [('t', 'energía extra|ac', 'energía', 480), ('g', '¿dónde la pones?', 'ponerla', 620), ('t', '3 veces al gimnasio', 'tres', 780), ('e', '❌', 'gimnasio', 880, 80)],
         [('e', '🎥', 'grabo', 540, 150), ('t', 'me grabo un vídeo|ac', 'vídeo', 750), ('g', 'explico algo', 'explico', 860)],
         [('t', 'lo que has aprendido', 'aprendido', 480), ('t', 'ayuda a los demás|ac', 'ayudar', 640), ('e', '✨', 'bien', 800)],
         [('t', 'más conectado|ac', 'conectado', 480), ('g', 'con quien eres tú', 'quien', 590), ('e', '🚀', 'petardo', 760, 130)],
         [('g', 'tu marca personal', 'marca', 480), ('p', 'EL VERDADERO PODER', 'verdadero', 640), ('e', '⚡', 'poder', 800)],
         [('e', '🔋', 'pilas', 520, 130), ('t', 'una persona real', 'persona', 700), ('t', 'su propia experiencia|ac', 'experiencia', 830)]],
 't01': [[('t', 'estresado|ac', 'estresado', 500, 96), ('e', '😵', 'pensando', 680), ('g', 'en eso, en eso, en eso…', 'eso', 850)],
         [('t', 'cambias tu modo de vida', 'cambiar', 520), ('e', '🙄', 'hostia', 740)],
         [('t', 'una parte de obsesión|ac', 'obsesión', 480, 68), ('g', 'nadie consigue éxito sin ella', 'nadie', 640), ('e', '🎯', 'éxito', 800)],
         [('g', 'sabes dónde vas', 'dónde', 480), ('p', 'FOCO', 'foco', 620), ('t', 'toda tu energía|ac', 'energía', 790)],
         [('t', 'energía bien usada|ac', 'correcta', 500), ('e', '🔗', 'conectado', 690), ('g', 'conectado con algo', 'algo', 860)],
         [('e', '🐎', 'caballos', 560, 170), ('t', 'anteojeras|ac', 'ojos', 780, 80)]],
 't02': [[('t', '5 personas', 'cinco', 470), ('e', '👥', 'personas', 610, 76), ('t', 'venden lo mismo|ac', 'venden', 770), ('e', '🛒', 'cliente', 880, 80)],
         [('p', 'MENTIRA', 'mentira', 500), ('g', 'creencias limitantes', 'creencias', 650), ('t', 'está todo|ac inventado|ac', 'inventado', 800, 70)],
         [('t', 'tus experiencias|ac', 'experiencias', 520), ('e', '🌍', 'mundo', 720)],
         [('t', 'abundancia|ac', 'abundancia', 560, 100), ('g', 'puedes invertir en varios', 'invertir', 780)],
         [('t', 'la experiencia de uno', 'experiencia', 480), ('e', '🔁', 'revés', 660), ('t', 'el juego es abundancia|ac', 'juego', 830)]],
 't03': [[('e', '🤝', 'manita', 540, 150), ('t', 'que te cojan de la manita|ac', 'cojan', 760)],
         [('t', 'tu ego|ac', 'ego', 540, 100), ('e', '🗣️', 'dice', 740)],
         [('t', '¿cuántos vídeos?', 'cuántos', 500), ('t', '¿qué hago exactamente?|ac', 'exactamente', 660), ('e', '📋', 'exactamente', 820)],
         [('t', '50 vídeos|ac', '50', 540, 100), ('e', '📺', 'vídeos', 750)],
         [('t', 'más energía', 'energía', 500), ('t', 'ganar más dinero|ac', 'dinero', 660), ('e', '💰', 'dinero', 820)],
         [('t', 'ayudar a los demás|ac', 'ayudar', 540), ('e', '🙌', 'demás', 730)],
         [('g', 'no falta información', 'información', 520), ('p', 'FALTA APLICACIÓN', 'aplicación', 690)]],
}
JS = """/* {nom} · F3 «energía y negocio» (generado por hacer_escenas.py). Un bloque por tramo de tablero */
const DEF = {defs};
DEF.forEach((items, i) => {{ if (!TABLEROS[i]) return;
  bloque(...TABLEROS[i], (a) => {{
    const els = items.map(([k, s, w, y, tam]) => {{ const t0 = en(w, a);
      const e = k === 'e' ? emoji(s, t0 - .1, tam || 120) : k === 'p' ? pastilla(s, t0, {{ ac: true, tam: tam || 46 }})
              : texto(s, t0, {{ tam: tam || (k === 'g' ? 50 : 64), m: k === 'g' }});
      return [k, e, y]; }});
    return t => els.forEach(([k, e, y]) => (k === 'e' ? pe(e, t, 540, y) : pt(e, t, 540, y)));
  }});
}});
"""
for nom, defs in E.items():
    Path(f'{nom}.js').write_text(JS.format(nom=nom, defs=json.dumps(defs, ensure_ascii=False)), encoding='utf-8')
print('ok', list(E))
