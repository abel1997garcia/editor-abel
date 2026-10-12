"""reels_f1.json de «ESTO le pasa a tu energía sexual cuando tu negocio…»: 7 de publicar + 3 trials, cada uno con su estructura.
REGLA de los vídeos de energía (Abel): en los reels no se habla de energía sexual, retención, transmutar, recaídas ni contenido
para adultos; se quedan solo los trozos que valen para cualquier emprendedor. Fuente: la grabación original."""
import json, sys
sys.path.insert(0, '../../herramientas')
from anclas import A

V = '../../VideosLargos/energia-negocio-2/'
a = A(V + 'toma_tiempos.json'); T, f = a.T, a.find
K = 'ÉPICA/Kanye West - Runaway (Instrumental).mp3'; S = 'ÉPICA/ECHO SAX END but it sounds like Øneheart.mp3'
Z = 'ÉPICA/Hans Zimmer - Time (Inception) _ EPIC EMOTIONAL VERSION.mp3'; O = 'EMOCIONAL/Outro - M83 only the best part.mp3'
I = 'EMOCIONAL/Interstellar Official Soundtrack _ Cornfield Chase – Hans Zimmer _ WaterTower.mp3'

def R(titulo, musica, gancho, cuerpo, enfasis, quitar=()):
    q = [i for x in quitar for i in range(T(*x)[0], T(*x)[1] + 1)]
    return dict(gancho=[T(*g) for g in gancho], cuerpo=[T(*c) for c in cuerpo], enfasis=[T(*e) for e in enfasis], quitar=q, titulo=titulo, musica=musica)

r = {
 'c01_g1e1_F1': R('Tu miedo no es al fracaso, es al éxito:', Z,
    [('y justo en el momento perfecto que dices', 'y te desconectas')],
    [('te quedas sin motivación', 'es miedo al éxito'), ('incluso yo que he hecho un viaje', 'para sentirte con valor'),
     ('recuerda que cuando tú tienes más confianza', 'con quien eres y ya está')],
    [('te desconectas',), ('tengo miedo al puto éxito',), ('más miedo a la caída',)], [('inventido',)]),
 'c02_g2e2_F1': R('Celebrar cada venta te está frenando:', S,
    [('cuando tú recibas alguna compra de algún cliente', 'manos a la obra')],
    [('porque esto aunque parezca contraproducente', 'tener ese subidón'),
     ('por eso es importante que cuando tú realmente consigas una pequeña victoria', 'vuelvas al trabajo otra vez'),
     ('vuelve a la carga', 'el trabajo que tienes que hacer')],
    [('manos a la obra',), ('vuelvas al trabajo',)]),
 'c03_g3e3_F1': R('Nadie te enseñó a regularte (y se nota en tu negocio):', I,
    [('nunca en la vida has aprendido', 'no te enseñaron')],
    [('porque básicamente hay muy pocas personas', 'de forma emocional'), ('que parece que tienes que estar perfecto', 'no eres capaz de controlar'),
     ('hay personas que aprenden a regularse con el tabaco', 'todo funciona de esta manera')],
    [('no te enseñaron',), ('incluso con la rabia',), ('regularse emocionalmente',)]),
 'c04_g4e4_F1': R('Trabajar por obligación te está quemando:', K,
    [('el tema no es que seas un esclavo del trabajo', 'no puede parar de hacer cosas')],
    [('y esto te lo digo no para que tú pienses', 'para ayudar a otras personas'),
     ('desde esa intención', 'algo algo innato'), ('vas a poder poder conectar más con la devoción', 'desde una intención positiva')],
    [('esclavo del trabajo',), ('vuelves a generar estrés',), ('desde una intención positiva',)]),
 'c05_g5e5_F1': R('Es en tus ratos muertos donde más peligras:', O,
    [('cuando tú tienes tiempos muertos es donde tú peligras más',)],
    [('porque cuando tú tienes tiempos muertos', 'tienes que estar'),
     ('crees una rutina', 'tus puntos débiles'), ('después de haber grabado', 'poniéndote a prueba')],
    [('peligras más',), ('tus puntos débiles',), ('no te aportan nada',)], [('y esto es a tanto porque esto es importante que tú sepas',)]),
 'c06_g6e6_F1': R('Si no aguantas equivocarte, tu negocio no va a funcionar:', K,
    [('vas a tener que ser muy pero que muy resiliente', 'muchísimo'), ('si no eres una persona resiliente', 'nunca lo vas a tener todo claro')],
    [('nunca vas a acertar toda la primera', 'lo suficiente'),
     ('equivocarte meterte hostias es lo más importante', 'para no llegar a este resultado'),
     ('una persona inteligente no cae dos veces', 'lo que te ha llevado ahí')],
    [('nunca lo vas a tener todo claro',), ('meterte hostias',), ('dos veces en la misma piedra',)]),
 'c07_g7e7_F1': R('«Ya he grabado vídeos» es la excusa que te frena:', S,
    [('aunque tu mente y tu ego te diga', 'qué más quieres que haga')],
    [('vuelve a grabar', 'si no usas'), ('esa energía te va a acabar atropellando', 'para el gimnasio'),
     ('porque te vas a desconectar', 'quedarte sin energía'), ('si tú realmente te quieres tomar todo esto en serio', 'que valga la pena'),
     ('vas a tener que aprender a gestionar los impulsos',)], [('vuelve a grabar',), ('te va a acabar atropellando',)], [('vas a vamos',)]),
 't01_g8e8_F1': R('Hoy tienes una llamada importante y te sientes fatal:', Z,
    [('cuando llegas a este punto de situaciones críticas', 'tengo baja confianza')],
    [('porque me he fallado a mí mismo', 'y es normal'),
     ('y aceptar todo esto', 'de una determinada manera')],
    [('me siento fatal',), ('te baja el respeto',), ('presión extra',)], [('manera', None, f('manera manera') + 1), ('llega', None, f('llega llega ese punto') + 1)]),
 't02_g9e9_F1': R('Justo cuando vendes, tu cabeza te ataca:', I,
    [('y si no te paga', 'y si lo decepcionas')],
    [('las personas tienen miedo al éxito y esas mismas personas', 'tienen miedo al éxito'),
     ('ese subidón a nivel emocional', 'por así decirlo'), ('cuando tú estás arriba automáticamente tu inconsciente', 'te va a atacar'),
     ('entonces esa energía o esa sensación extra', 'y por tanto estrés'),
     ('pues es un miedo de mucho tiempo atrás', 'para sentirte con valor')],
    [('y si no eres suficiente',), ('en tu contra',), ('para sentirte con valor',)]),
 't03_g10e10_F1': R('Pasas de estar genial a estar fatal (y no sabes por qué):', O,
    [('y de repente de pasas de estar de puta madre a estar mal',)],
    [('muchas veces las personas tenemos ciertos momentos', 'no has hecho nada'),
     ('y eso es algo que pasa en cualquier situación', 'aprender de todo este proceso'),
     ('cuando vayas obteniendo más beneficios', 'este tipo de momentos clave')],
    [('tu propio amigo',), ('mayor autocontrol',)], [('de', None, f('de repente de pasas') + 2)]),
}
c = {'fuente': 'C:/Users/Clap/Desktop/ESTO le pasa a tu energía sexual cuando tu negocio.mp4', 'tiempos': V + 'toma_tiempos.json',
     'salida': 'out_f1', 'reels': r}
json.dump(c, open('reels_f1.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('ok', len(r))
