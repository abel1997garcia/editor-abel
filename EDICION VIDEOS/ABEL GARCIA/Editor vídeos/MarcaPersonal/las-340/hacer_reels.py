"""reels_f1.json de «Nadie sabía lo que me pasaba a las 3:40 de la mañana»: 7 de publicar (2 personales) + 3 trials con gancho
directo a la persona; cada uno con su estructura. Fuente: la grabación original (sin horizontal)."""
import json, sys
sys.path.insert(0, '../../herramientas')
from anclas import A

V = '../../VideosLargos/las-340/'
a = A(V + 'toma_tiempos.json'); T = a.T
K = 'ÉPICA/Kanye West - Runaway (Instrumental).mp3'; S = 'ÉPICA/ECHO SAX END but it sounds like Øneheart.mp3'
Z = 'ÉPICA/Hans Zimmer - Time (Inception) _ EPIC EMOTIONAL VERSION.mp3'; O = 'EMOCIONAL/Outro - M83 only the best part.mp3'
I = 'EMOCIONAL/Interstellar Official Soundtrack _ Cornfield Chase – Hans Zimmer _ WaterTower.mp3'

def R(titulo, musica, gancho, cuerpo, enfasis, quitar=()):
    q = [i for x in quitar for i in range(T(*x)[0], T(*x)[1] + 1)]
    return dict(gancho=[T(*g) for g in gancho], cuerpo=[T(*c) for c in cuerpo], enfasis=[T(*e) for e in enfasis], quitar=q, titulo=titulo, musica=musica)

r = {
 'c01_g1e1_F1': R('Vendía motivación mientras por dentro estaba hundido:', I,      # personal
    [('hace unos años subía vídeos', 'estaba hecho una puta mierda')],
    [('me levantaba por las mañanas', 'mi vida cambiaría'), ('aquí hay personas que están igual que yo', 'con una buena intención')],
    [('una puta mierda',), ('mi vida cambiaría',), ('ni son ellos',)]),
 'c02_g2e3_F1': R('Ganar más no arregla lo que llevas dentro:', Z,                  # personal
    [('cuando ganaba 17.000 euros al mes', 'estaba hecho una mierda')],
    [('porque no estaba siendo congruente', 'ni decía lo que sentía'),
     ('imagínate si en ese punto de mi vida', 'desconfianza absoluta en la vida')],
    [('bomba de relojería',), ('por interés',), ('desconfianza absoluta',)], [('hubiese tenido', 'ganar eso')]),
 'c03_g3e2_F1': R('Si tu marca ya no es tuya, eres su esclavo:', K,
    [('cuando tu marca personal deja de ser tuya', 'muy pero que muy egoísta')],
    [('no eres auténtico encima eso te quita energía', 'respecto a tu marca personal'),
     ('tenemos un ejemplo muy claro con los influencers', 'a nivel de toda la sociedad')],
    [('te estás fallando',), ('esclavos de lo que tienen que hacer',)]),
 'c04_g4e5_F1': R('Fingir que eres auténtico se nota (aunque no lo creas):', S,
    [('por mucho que tú quieras intentar aparentar', 'engañarte a ti mismo')],
    [('cuando tú intentas fingir algo', 'de lo otro'), ('lo importante para poder conseguir autenticidad', 'perdonarte')],
    [('no son gilipollas',), ('el más listo de la clase',), ('ser honesto con uno mismo',)]),
 'c05_g5e6_F1': R('Elegir entre 4 opciones no es pensar por ti mismo:', K,
    [('si todo tu entorno te dice', 'vas a acabar saliendo de fiesta')],
    [('si no eres una persona auténtica', 'miedo lo que sea'), ('tú tienes una opinión en general', 'propia personalidad'),
     ('imagínate estás en mcdonald\'s', 'buscar tu verdad'), ('la verdad os hará libres', 'conecta con los demás')],
    [('miedo a la crítica',), ('cuatro opciones',), ('buscar tu verdad',)]),
 'c06_g6e8_F1': R('Por esto te comparan por precio (y no te eligen):', S,
    [('si te comparan por precio', 'no estás siendo auténtico')],
    [('porque si realmente eres auténtico', 'aportar a las personas'),
     ('requiere de que te quites todas las máscaras', 'adaptarte a la sociedad'), ('te tienes que exponer', 'lo más importante'), ('si tú quieres conseguir una marca personal que venda', 'empezar a ser auténtico')],
    [('te quieren a ti',), ('por tu autenticidad',), ('empezar a ser auténtico',)]),
 'c07_g7e10_F1': R('Lo que mejor se te da es justo lo que infravaloras:', O,
    [('aquello que tú vas a dar a los demás', 'no crees en lo suficiente en eso')],
    [('porque para ti es algo normal', 'no le das el peso suficiente'), ('veía mi entorno', 'como un mundo')],
    [('te autosabotea',), ('como un mundo',)], [('te', None, a.find('te te autosabotea'))]),
 't01_g8e4_F1': R('Hasta tus seguidores te obligan a llevar una careta:', K,
    [('eres esclavo de tu marca personal', 'que no eres tú')],
    [('muchas personas tienen ese mismo conflicto', 'en base a eso mismo'), ('tienes que seguir aguantando', 'no creías'),
     ('todo el mundo puede vender', 'no está siendo auténtico')],
    [('se ponen máscaras',), ('seguir contentando',)]),
 't02_g9e7_F1': R('Quien te critica te está mirando en un espejo:', Z,
    [('las personas que no conecten contigo y que te critiquen', 'de espejo')],
    [('cuando tú eres auténtico y hablas desde tu verdad', 'valoran tu autenticidad'),
     ('porque esas mismas personas quieren ser auténticas', 'por eso lo critican'),
     ('el xokas es una persona', 'pasa por la cabeza')],
    [('vas a polarizar',), ('por eso lo critican',), ('dice lo que piensa',)]),
 't03_g10e9_F1': R('Le das vueltas a qué vender y lo tienes delante:', I,
    [('cuando quieres empezar tu negocio', 'hacer lo otro')],
    [('todo lo piensan desde aquí', 'muy fácil de hacer'), ('no se trata de que tengas que empaquetar nada', 'con tus palabras hablarlo')],
    [('nace de aquí',), ('esa es tu marca personal',)]),
}
c = {'fuente': 'C:/Users/Clap/Desktop/Nadie sabía lo que me pasaba a las 340 de la maña.mp4', 'tiempos': V + 'toma_tiempos.json',
     'salida': 'out_f1', 'reels': r}
json.dump(c, open('reels_f1.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('ok', len(r))
