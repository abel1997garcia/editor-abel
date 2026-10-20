"""Carrusel de Allan «Cómo llegué a ser médium» v1 (13/10/2026). Microhistoria de 8 diapositivas, 3:4.
Guía: RUTINA_CARRUSELES_ALLAN.md · Hechos: HISTORIA_ALLAN.md (sus palabras, nada inventado)."""
import json
from pathlib import Path

AQUI = Path(__file__).resolve().parent
F = 'C:/Users/Clap/Desktop/EDICION VIDEOS/MEDIUM ALLAN/FOTOS ALLAN/'
G = str(AQUI / 'fotogramas') + '/'
SALIDA = 'C:/Users/Clap/Desktop/EDICION VIDEOS/MEDIUM ALLAN/CARRUSELES/01 · Cómo llegué a ser médium (v1)'

D = [
    (F + '5.jpg', "Tenía el trabajo soñado, mi casa recién comprada y mi segunda hija en camino.",
     ["Por fuera, el mejor momento de mi vida.",
      "Por dentro, cada mañana, al entrar a trabajar, me faltaba el aire. Esta es la historia de cómo me convertí en médium."], {}),
    (G + 'allan_campo_serio.png', "Nada más cruzar la puerta, se me caía todo de las manos:",
     ["el táper, la mochila, el agua. Me dolía la cabeza, el estómago, y tres veces casi pierdo el conocimiento en el baño.",
      "Fui al médico. Todo estaba perfecto. Pero yo sabía que algo no lo estaba."], {}),
    (F + '1.jpg', "Hasta que un día una voz me dijo: «Este no es tu lugar. Aquí ya no más».",
     ["Me senté en el sofá y le dije a mi mujer: «Sé que no lo vas a entender, pero tengo que dejarlo. Viene algo y tengo que esperar».",
      "Recuerdo su cara. Aun así, me apoyó, como siempre hace."], {'foco': [0.62, 0.45]}),
    (G + 'allan_casa_jardin.png', "Pasé más de un año en el jardín de casa,",
     ["de la mañana a la noche, mirando al cielo, esperando algo que no sabía qué era. No quería que nadie me hablara.",
      "Ya no me reconocía. Lloré muchísimo. Pensé que me estaba volviendo loco."], {}),
    (G + 'allan_campo_amanecer.png', "Un día me rendí.",
     ["Me metí en la cama, me tapé la cabeza y dije: «No puedo más. Hasta aquí he llegado».",
      "Esa noche soñé con mi abuela. Me dijo que no me preocupara, que ella me iba a ayudar. Fue más real que lo que toco ahora."], {}),
    (G + 'allan_campo_perfil.png', "Meses después, en una feria, un médium al que solo conocía de Instagram me miró y me dijo:",
     ["«Tú un día vas a ser médium. Vas a dejar tu trabajo y vas a ayudar a otras personas».",
      "No le creí. Pensé que me confundía con otro. Hoy Raúl Vaquero es mi amigo y mi maestro."], {}),
    (F + '3.jpg', "Hoy acompaño a personas que han perdido a alguien.",
     ["Familias que se rompen con un fallecimiento y que, con un mensaje, vuelven a ponerse en pie. No lo hago yo: yo solo soy el puente.",
      "Todo lo que viví, el vacío, no encajar, sentirme perdido, era para entender a quien hoy se sienta delante de mí."], {}),
    (F + '6.jpg', "Si hoy sientes que lo tienes todo y aun así te falta algo,",
     ["o has perdido a alguien y no sabes si sigue ahí…",
      "es transitorio. No estás solo. *Hay algo más*, y te está esperando."], {}),
]

DESCRIPCION = """Si has perdido a alguien, o si sientes que tu vida ya no encaja aunque por fuera lo tengas todo, esta historia es para ti. Así me convertí en médium.

Tenía el trabajo soñado, mi casa recién comprada y mi segunda hija en camino. Y aun así, cada mañana, al entrar a trabajar, me faltaba el aire. Se me caía todo de las manos, casi pierdo el conocimiento tres veces, y los médicos me decían que estaba perfecto.

Un día una voz me dijo: «Este no es tu lugar». Le hice caso. Lo dejé todo y pasé más de un año en el jardín de casa, mirando al cielo, esperando algo que no sabía qué era. Lloré muchísimo. Llegué a pensar que me había vuelto loco.

Hasta que me rendí. Y esa noche soñé con mi abuela.

Desde entonces entiendo que todo lo que viví, el vacío, no encajar, sentirme perdido, era para poder acompañar a quien hoy pierde a alguien y necesita saber que sigue ahí. Yo no hago nada: solo soy el puente.

Si estás en ese momento, es transitorio. No estás solo 🤍

👉 Si quieres información sobre las sesiones, comenta "INFO"."""

assert len({f for f, *_ in D}) == len(D), 'foto repetida'
c = {'salida': SALIDA, 'descripcion': DESCRIPCION,
     'diapositivas': [dict(foto=f, titular=t, lineas=l, **o) for f, t, l, o in D]}
json.dump(c, open(AQUI / 'como_llegue_a_ser_medium_v1.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('ok', len(D))
