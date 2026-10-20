"""Tanda 2 (13/10/2026) de «5 señales de que cobras barato»: 3 reels F1 con ideas que NO salieron en la tanda 1 (035-044).
e14 · la información está en internet, tu diferenciador eres tú (marca personal) · PUBLICAR
e15 · rebajar el precio cuando el cliente duda = fallarte y perder tu autenticidad · PUBLICAR
e16 · te cuesta decir tu precio como si estuvieras necesitado; saber cuánto vale de verdad · TRIAL"""
import json, sys
sys.path.insert(0, '../../herramientas')
from anclas import A

V = '../../VideosLargos/cobras-barato/'; H = V + '5 señales de que cobras BARATO con tu marca personal - horizontal'
a = A(H + '.tiempos.json'); T = a.T
K = 'ÉPICA/Kanye West - Runaway (Instrumental).mp3'; S = 'ÉPICA/ECHO SAX END but it sounds like Øneheart.mp3'
Z = 'ÉPICA/Hans Zimmer - Time (Inception) _ EPIC EMOTIONAL VERSION.mp3'


def R(titulo, musica, gancho, cuerpo, enfasis):
    return dict(gancho=[T(*g) for g in gancho], cuerpo=[T(*c) for c in cuerpo], enfasis=[T(*e) for e in enfasis], titulo=titulo, musica=musica)


r = {
 'c08_g12e14_F1': R('Perfeccionar tu información no te hará vender más:', Z,
    [('la gran mayoría de la información', 'cuál es tu diferenciador')],
    [('por mucho que pienses que tiene todo que ver', 'que se entienda bien etcétera'),
     ('no es absolutamente nada de eso',),
     ('lo primero es ser una persona auténtica', 'lo que hagan los demás'),
     ('tú te tienes que involucrar al 100% con la persona',),
     ('eso es lo que siempre las personas buscan',),
     ('que te la explique una persona que ha vivido ese proceso',),
     ('por eso sé cómo piensas', 'el verdadero poder de la marca personal')],
    [('cuál es tu diferenciador',), ('ser una persona auténtica',), ('el verdadero poder de la marca personal',)]),
 'c09_g13e15_F1': R('Si rebajas tu precio cuando el cliente duda, te estás fallando:', K,
    [('si tienes que adaptarte a la otra persona', 'estás perdiendo toda tu autenticidad')],
    [('muchas veces la persona la que tienes delante', 'estoy dudando'),
     ('y en esa duda de la otra persona',),
     ('tú te enganches a esa misma baja vibración y digas',),
     ('bueno le voy a hacer un descuento',),
     ('te aseguro de que esto le ha pasado a todos', 'desde cero'),
     ('cómo se supera ese miedo', 'enfrentándonos'),
     ('cuando llevas meses trabajando y lo haces de una forma inteligente',),
     ('te vas a dar cuenta que todas tus expectativas', 'son simples ilusiones')],
    [('ya te estás fallando',), ('le voy a hacer un descuento',), ('son simples ilusiones',)]),
 't04_g14e16_F1': R('Te cuesta decir tu precio porque no sabes lo que vales:', S,
    [('parece que te cuesta hablar del precio', 'que estás necesitado')],
    [('cuando cobras barato parece como que es más fácil hablar del precio', 'tengamos una buena conversación'),
     ('si tú coges tu precio y tu servicio', 'como qué dices'),
     ('no tiene nada que ver contigo',),
     ('tú tienes que saber al 100% cuánto vale tu negocio', 'de estar enfadado con el mundo')],
    [('que estás necesitado',), ('cuánto vale tu negocio',), ('el coste de oportunidad',)]),
}
c = {'fuente': H + '.mp4', 'tiempos': H + '.tiempos.json', 'montaje': H + '.montaje.json', 'salida': 'out_f1', 'reels': r}
json.dump(c, open('reels_f1_2.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('ok', len(r))
