"""limpieza.json de «5 señales de que cobras barato»: lo que se quita y las frases clave, fijado con frases (anclas)."""
import json, sys
sys.path.insert(0, '../../herramientas')
from anclas import A

a = A('toma_tiempos.json'); f, T = a.find, a.T
r = lambda x: list(range(x[0], x[1] + 1))
Q = []
uno = lambda frase, k, desde=0: Q.append(f(frase, desde) + k)        # quita la palabra k de esa frase
uno('todos todos tenemos', 1); uno('ejemplo ejemplo imagínate', 1); uno('porque siempre si te comparan', 1)
uno('lo lo mismo', 1); uno('yo yo te recomiendo', 1); uno('quieras quieres crear', 0); uno('empezar empezar a reformular', 1)
uno('les les voy', 1); uno('absolutamente absolutamente nada', 1); uno('para para crear', 1); uno('después detrás de pensar', 0)
uno('fundamental mental y es', 1); uno('internet internet pero', 1); uno('la la hora de ofrecer', 1); uno('haberle le he dicho', 1)
uno('la la otra persona te va', 1); uno('te te comportas', 1); uno('sé sé lo que', 1); uno('energía energía que tenías', 1)
uno('la la gente no lo valora', 1); uno('y y justificando', 1); uno('no no estás ofreciendo', 1); uno('etc etcétera y obviamente', 0)
Q += r(T('como te digo', None, f('ya sabes lo que hacer')))
Q += r(T('cómo puede ser', None, f('me tiemblan las piernas a')))
Q += r(T('x o y', None, f('cuánto vale tu negocio')))
Q += r(T('esa experiencia', None, f('es esa experiencia esa información')))
i = f('lo que bajo mi experiencia y bajo'); j = f('porque bajo mi experiencia y bajo todos'); Q += list(range(i, j))
Q += r(T('qué es lo', None, f('qué es lo que es lo que sucede')))
i = f('todo lo que te has lo que te'); Q += list(range(i, i + 5))

def F(texto, desde, hasta, cerca=0): i, j = T(desde, hasta, cerca); return [texto, i, j]
frases = [
    F('NUNCA cobres\\Nbarato.', 'nunca en la vida debes cobrar barato', 'cobrar barato'),
    F('No vendes nada:\\NTE VENDES A TI.', 'tú no vendes nada', 'a ti mismo'),
    F('Si te comparan por precio,\\NESTÁS JODIDO.', 'si te comparan por precio estás', 'jodidísimo'),
    F('Lo que dice Juan de Pedro\\Ndice MÁS DE JUAN.', 'lo que dice juan de pedro', 'que de pedro'),
    F('Una persona abundante\\NNO PERSIGUE.', 'no va persiguiendo clientes', 'convencer a nadie'),
    F('El dinero filtra\\nEL COMPROMISO.'.replace('\\n', '\\N'), 'el dinero filtra el compromiso', 'compromiso', f('el dinero filtra')),
    F('Di tu precio\\Ny AGUANTA EL SILENCIO.', 'di tu precio', 'aguanta el silencio'),
]
cfg = {"fuente": "../../../../../5 señales de que cobras BARATO con tu marca person.mp4", "tiempos": "toma_tiempos.json",
       "salida": "5 señales de que cobras BARATO con tu marca personal - horizontal.mp4",
       "quitar": sorted(set(Q)), "zooms": [], "intacto_desde": f('así que ya sabes lo que tienes que hacer si quieres'), "frases": frases}
json.dump(cfg, open('limpieza.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
W = a.F
for t, i, j in frases: print(f"{W[i]['s']:7.1f}s  {t}")
print(len(Q), 'palabras quitadas')
