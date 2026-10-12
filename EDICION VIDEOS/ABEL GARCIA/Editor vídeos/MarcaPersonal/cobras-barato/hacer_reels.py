"""reels_f1.json de «5 señales de que cobras barato»: 7 de publicar + 3 trials, cada uno con su propia estructura.
Tramos y énfasis fijados con frases sobre el .tiempos.json del horizontal."""
import json, sys
sys.path.insert(0, '../../herramientas')
from anclas import A

V = '../../VideosLargos/cobras-barato/'; H = V + '5 señales de que cobras BARATO con tu marca personal - horizontal'
a = A(H + '.tiempos.json'); T, f = a.T, a.find
K = 'ÉPICA/Kanye West - Runaway (Instrumental).mp3'; S = 'ÉPICA/ECHO SAX END but it sounds like Øneheart.mp3'
Z = 'ÉPICA/Hans Zimmer - Time (Inception) _ EPIC EMOTIONAL VERSION.mp3'; O = 'EMOCIONAL/Outro - M83 only the best part.mp3'
I = 'EMOCIONAL/Interstellar Official Soundtrack _ Cornfield Chase – Hans Zimmer _ WaterTower.mp3'; AU = 'ÉPICA/Ogryzek - AURA.mp3'

def R(titulo, musica, gancho, cuerpo, enfasis):
    return dict(gancho=[T(*g) for g in gancho], cuerpo=[T(*c) for c in cuerpo], enfasis=[T(*e) for e in enfasis], titulo=titulo, musica=musica)

r = {
 'c01_g1e7_F1': R('No es falta de preparación, es miedo a cobrar lo que vales:', K,
    [('si tú a la hora de decir tu precio flaqueas', 'más o menos preparado con el negocio')],
    [('sino que tiene que ver con todos los miedos', 'de lo que tú has vivido'),
     ('hay algo dentro de ti que no se siente merecedor', 'durante tres meses'),
     ('y eso lo que sucede es que se nota en tu energía', 'vale ese dinero')],
    [('te sientes como un impostor',), ('todos los miedos',), ('se nota en tu energía',)]),
 'c02_g2e2_F1': R('Porqué tu “low ticket” jamás te dará testimonios:', S,
    [('si te comparan por precio estás jodidísimo', 'a tirar para abajo')],
    [('y aparte pasa una cosa', 'tienen al principio'), ('y es que cuando tú pones un low ticket', 'de 3.000 euros'),
     ('luego sucede otra cosa', 'no generas testimonios'), ('antes de hacer un low ticket', 'que lo hagas gratis')],
    [('estás jodidísimo',), ('no hay tanto compromiso',), ('no generas testimonios',)]),
 'c03_g3e9_F1': R('Si necesitas que te compren, tu cliente lo nota:', S,
    [('una persona que realmente es abundante no necesita', 'no necesita absolutamente nada')],
    [('por mucho que luego lo pienses de cabeza', 'incluso por chat'), ('tú cuando sabes que una persona te va a vender', 'pasa exactamente igual'), ('siempre tienes que ser valiente', 'toda tu energía')],
    [('desde ese merecimiento',), ('lo presientes',)]),
 'c04_g4e12_F1': R('Regalar tu servicio no compromete a nadie:', Z,
    [('las personas nos movemos y ejecutamos cuando tenemos miedo de perder',)],
    [('ya sea perder la oportunidad', 'ya sabes la respuesta verdad'), ('bajo mi experiencia y bajo todos estos años', 'te lo aseguro')],
    [('el dinero filtra el compromiso',), ('ya sabes la respuesta',)]),
 'c05_g5e5_F1': R('Así es como regalar tu trabajo te acaba quemando:', O,
    [('tú das algo que de forma inconsciente', 'como le he ayudado me va a pagar')],
    [('y luego lo que pasa es que no te pagan', 'que de pedro'),
     ('si realmente tú quieres ofrecer un servicio porque quieres obtener testimonios', 'absolutamente nada'),
     ('y está bien porque también te va a servir', 'absolutamente todo al empezar')],
    [('te da rabia',), ('dice más de juan que de pedro',), ('ofrécelo gratis',)]),
 'c06_g6e13_F1': R('Justificar tu precio te está haciendo perder clientes:', K,
    [('no te tienes que justificar por qué coño pones un precio',)],
    [('vas a tener que pasar por la incomodidad', 'ni justificar tu precio ni nada'),
     ('cuando tú tienes que andar justificando tu valor', 'no es para ti'), ('di tu precio', 'tampoco es la persona')],
    [('pasar por la incomodidad',), ('no es para ti',), ('aguanta el silencio',)]),
 'c07_g7e1_F1': R('Bajar tu precio no te hará vender más:', S,
    [('tú no vendes nada tú te vendes a ti mismo',)],
    [('debes dejar de hacer descuentos', 'mi producto es bueno'), ('imagínate que hay 10 personas', 'te lo sepa vender bien'), ('entonces el problema no es de precio',)],
    [('hay un miedo',), ('te lo sepa vender bien',)]),
 't01_g8e11_F1': R('Me sabía mal cobrar a quien lo pasaba mal… y era un error:', I,
    [('a mí me ha pasado durante mucho tiempo y es que te sabe mal cobrar', 'que lo están pasando mal')],
    [('si tú quieres atraer a personas abundantes', 'no es su momento'),
     ('no le haces ningún favor a nadie cuando regalas', 'lo que tiene que hacer')],
    [('no es su momento',), ('ningún favor a nadie',)]),
 't02_g9e6_F1': R('Un cliente barato te roba más energía de la que paga:', K,
    [('nadie quiere tener clientes que no hacen nada', 'si les funciona o no')],
    [('tú tienes una energía determinada o limitada', 'no sé cuánto'),
     ('estar constantemente pendiente de una persona', 'que tú tienes que trabajar'),
     ('estoy hasta los cojones', 'lo que tú reflejas')],
    [('energía determinada o limitada',), ('hasta los cojones',), ('lo que tú reflejas',)]),
 't03_g10e4_F1': R('Cobrar poco te llena de clientes que se quejan:', Z,
    [('cuando tú quieres crear un negocio o un low ticket', 'que están encima tuyo')],
    [('es otro tipo de cliente', 'actuar en consecuencia'),
     ('cuando es algo que es gratis y barato', 'no tiene miedo de perder')],
    [('lo quieren en todo',), ('lo valorarás menos',)]),
}
c = {'fuente': H + '.mp4', 'tiempos': H + '.tiempos.json', 'montaje': H + '.montaje.json', 'salida': 'out_f1', 'reels': r}
json.dump(c, open('reels_f1.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('ok', len(r))
