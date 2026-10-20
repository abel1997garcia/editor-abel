"""Reels «franjas azules» de «los objetos se impregnan de energia.mp4» (Escritorio). Original HORIZONTAL 1920x1080, Allan
centrado -> se compone con plantillas/fondo_franjas_azules.png. Sin banners (comprobado).
Subtítulos partidos a mano (<= 6 palabras), guiones leídos de corrido (congruencia), método de cortes aprobado."""
import json
from pathlib import Path

COMUN = {"estilo": "franjas_azules",
         "video": "C:/Users/Clap/Desktop/los objetos se impregnan de energia.mp4",
         "tiempos": "trabajo/objetos/tiempos.json",
         "componer": {"fondo": "plantillas/fondo_franjas_azules.png", "y": 588, "alto": 768}}

R = {
"objetos_01_cuidado": ("HAY OBJETOS QUE NUNCA DEBERÍAS TENER EN CASA", [
 # gancho
 [0,3,"Cuidado con los objetos"],[4,8,"que tienes en tu casa."],[9,11,"Podría ser peligroso."],
 [12,16,"Hay objetos que todos tenemos"],[17,19,"en nuestros hogares"],[26,30,"que pertenecen a otras personas,"],
 [31,33,"a otros lugares,"],[34,35,"o incluso"],[36,39,"coleccionistas que nos gustan"],[40,42,"los objetos antiguos."],
 # por qué
 [84,86,"Cuando ha habido"],[87,90,"algún hecho trágico fuerte,"],[91,95,"donde ha habido mucha emoción"],
 [96,98,"o mucho sufrimiento,"],[99,103,"siempre los lugares y los objetos"],[104,109,"se impregnan de esa energía."],
 [116,120,"Esas energías permanecen adheridas"],[121,128,"a los lugares y a los objetos."],
 # su experiencia
 [129,133,"He conocido personas, yo incluido,"],[134,136,"que siempre hemos"],[137,139,"tenido esa pasión"],
 [140,143,"por las cosas antiguas,"],[144,145,"de coleccionista."],
 [146,148,"O encontramos algo"],[149,153,"que nos llama la atención,"],[154,158,"que creemos que es antiguo,"],
 [159,164,"nos lo llevamos a nuestro hogar,"],[165,168,"lo tenemos con nosotros,"],[169,173,"lo ponemos en nuestro sitio,"],[174,176,"donde siempre estamos,"],
 [177,180,"donde trabajamos, donde dormimos."],
 [181,183,"Y esos objetos,"],[184,186,"no es que"],[187,190,"vaya a ocurrir nada,"],[191,193,"no es que"],
 [194,198,"te vaya a pasar nada,"],[199,204,"pero esos objetos emiten una vibración"],[205,207,"que tienen impregnada,"],[208,210,"y esa vibración"],
 [211,214,"suele ser de sufrimiento,"],[215,216,"de batallas,"],[217,219,"de cosas que"],[220,223,"han ocurrido muy trágicas."],
]),
"objetos_02_pesadillas": ("ESE REGALO PUEDE ESTAR AFECTÁNDOTE", [
 # gancho: su experiencia
 [246,249,"Yo he tenido casos,"],[250,254,"incluso por mi propia experiencia,"],[255,259,"donde empezaba a tener pesadillas,"],
 [260,264,"donde empezaba a encontrarme mal,"],[265,267,"donde no descansaba,"],[268,271,"soñaba con cosas extrañas,"],
 [272,274,"con energías densas,"],[275,277,"no podía moverme,"],[278,280,"me levantaba mal."],
 [281,284,"Tiene mucho que ver"],[285,287,"con esos objetos."],
 # los regalos
 [288,290,"Incluso objetos que"],[291,296,"en algún momento de tu vida"],[297,301,"te regalan o te dan"],[302,303,"una persona"],
 [304,309,"que cambia su energía hacia ti,"],[310,314,"cambia su energía, su pensamiento,"],
 [318,321,"lo que te manda,"],[322,325,"lo que te emite,"],[326,328,"y puede cambiar"],[329,334,"esa energía de ese objeto."],
 [335,338,"Es como un canal"],[339,341,"o una representación"],[342,346,"de la energía de esa persona"],[347,349,"cerca de ti."],
 [362,366,"Hay que tener muy claro"],[367,372,"qué tipo de objetos nos rodean,"],
 [373,377,"qué tipo de objetos tenemos"],[378,380,"en nuestra casa."],
 [445,449,"Porque siempre la energía negativa"],[460,463,"intenta no ser detectada,"],[464,466,"intenta pasar desapercibida,"],
 [467,469,"porque se mete,"],[470,473,"siembra poquito a poco"],[474,476,"y va aumentando."],
 # sin miedo, con conciencia
 [477,481,"Con esto no quiero decir"],[482,485,"que si tienes objetos"],[486,488,"que te asustes,"],[489,491,"que los tires,"],
 [492,495,"pero sí ser conscientes"],[496,500,"de que quizá nuestro hogar"],[501,504,"necesite mucha limpieza energética,"],
 [505,507,"necesite ventilarse mucho,"],[508,510,"necesite mucha luz."],
]),
"objetos_03_guerra": ("LOS OBJETOS DE GUERRA GUARDAN SU DOLOR", [
 # gancho
 [634,638,"Yo conozco personas que coleccionan"],[639,642,"cosas de la guerra,"],[643,646,"de la guerra mundial"],
 [647,651,"o de la guerra civil,"],[652,653,"balas, cartas,"],[654,657,"objetos de restos arqueológicos"],
 [658,660,"donde han tenido"],[661,665,"que ver algo con fallecidos,"],[666,669,"o con momentos históricos"],
 [670,674,"muy, muy, muy, muy movidos,"],[675,678,"con energía de miedo,"],[679,682,"de dolor, de muerte,"],[683,684,"de matanzas."],
 # cómo están
 [687,689,"Esos objetos especialmente"],[690,693,"están muy, muy impregnados,"],[694,697,"y yo siempre aconsejo"],
 [698,701,"tenerlos muy bien cerrados,"],[727,731,"porque aún y aún así"],[732,733,"esa energía"],
 [736,739,"puede emitirse, puede viajar."],
 [756,761,"Es muy difícil quitar esa energía,"],[762,765,"porque la energía oscura,"],[766,769,"la energía del dolor,"],
 [770,773,"siempre es muy densa."],
 # qué hacer
 [779,781,"Pero podemos hacer"],[782,785,"algún tipo de protección:"],[809,813,"poniendo algún tipo de símbolo"],
 [814,818,"o algún tipo de objeto"],[819,822,"que sea de protección."],
 [845,849,"Siempre hay que tenerlo vigilado"],[850,855,"y hay que tenerlo bien limitado,"],[856,858,"porque esa energía"],
 [859,864,"es muy sutil pero muy potente."],
]),
"objetos_04_tienda": ("EN ESA TIENDA NO PUEDO NI ENTRAR", [
 # gancho
 [2041,2046,"Es que ahí no puedo entrar."],[2047,2050,"Si yo entro ahí,"],[2051,2054,"ahí me siento triste,"],
 [2055,2060,"siento una sensación en mi garganta"],[2061,2064,"de no poder hablar,"],[2065,2068,"de injusticia, de tristeza."],
 # la anécdota
 [1943,1949,"A mí hay algo que me sucede"],[1950,1951,"como anécdota:"],[1952,1954,"y es que"],[1955,1958,"hay un centro comercial"],
 [1959,1961,"donde yo voy"],[1962,1965,"a una tienda específica"],[1969,1972,"que cuando yo entro"],
 [1973,1975,"me encuentro mal"],[1976,1979,"y canalizo la energía"],[1980,1982,"de la tristeza,"],
 [1983,1987,"la injusticia y la rabia"],[1988,1990,"de las personas"],[1991,1994,"que hay allí trabajando."],
 [1995,1998,"Y no les veo,"],[1999,2003,"no los observo a ellos,"],[2004,2006,"pero noto injusticia."],
 [2007,2009,"Es como si"],[2010,2013,"yo tuviese la sensación"],[2014,2016,"de que allí"],[2017,2020,"no se trata bien"],
 [2021,2023,"a las personas,"],[2024,2027,"se les hace daño."],
 [2070,2073,"No solamente un médium"],[2074,2078,"canaliza energías de los fallecidos,"],
 [2079,2083,"sino que también en las energías"],[2084,2086,"de los lugares"],[2087,2090,"y de las personas."],
 # los objetos de ese lugar
 [2096,2101,"Y los objetos que hay allí,"],[2102,2106,"las cosas que se venden"],[2107,2109,"en ese lugar,"],
 [2110,2112,"tienen esa energía."],[2127,2130,"Y no me gusta"],[2131,2135,"que vayamos o que vaya"],
 [2136,2140,"la gente de mi familia"],[2141,2146,"y que traiga cosas a casa,"],[2147,2150,"porque noto esa vibración"],
 [2151,2153,"de ese lugar."],
 [2160,2162,"Yo, como médium,"],[2163,2166,"que soy muy sensitivo,"],[2167,2169,"tengo esa percepción,"],
 [2170,2173,"pero hay muchas personas"],[2174,2178,"que no se dan cuenta"],[2179,2182,"que también pueden percibir."],
]),
"objetos_05_casa": ("TU CASA PUEDE ESTAR ESTANCANDO TU ENERGÍA", [
 # gancho (v2, feedback: «Hay casas, hay hogares…» tardaba en arrancar y no impactaba)
 [1605,1608,"Al final, la energía,"],[1609,1612,"si no se mueve,"],[1613,1614,"se queda"],[1615,1619,"o se va volviendo oscura."],
 # su experiencia
 [1130,1135,"Algunas veces he entrado en hogares"],[1136,1141,"en los que siento esa energía,"],[1142,1144,"porque siento que"],
 [1145,1148,"la casa, el hogar,"],[1149,1153,"está lleno de objetos"],[1154,1156,"con energía densa."],
 # consecuencias
 [1095,1100,"Y hace que incluso la energía"],[1101,1105,"en la casa no fluya,"],
 [1106,1108,"y son personas"],[1110,1114,"que quizás luego esas personas"],[1116,1117,"tengan enfermedades,"],
 [1118,1120,"estén siempre enfadados,"],[1121,1123,"no descansen bien."],
 # el contraste
 [996,1001,"Los espacios abiertos con pocas cosas,"],[1002,1007,"muy blancos, con muy poquitos objetos,"],
 [1008,1011,"siempre hay una energía"],[1012,1017,"más fluida, más tranquila, más blanca."],
 [1032,1036,"Descansamos mejor, estamos más tranquilos."],
 # renovar
 [1706,1711,"Cuando hacemos ese tipo de cosas"],[1712,1714,"realmente estamos canalizando"],[1715,1718,"esa energía que había"],
 [1719,1723,"y estamos limpiando y renovando"],[1724,1729,"para que entre una energía nueva."],
 [1748,1753,"Y se nota cuando una casa"],[1754,1759,"se pinta, se cambian los muebles,"],[1760,1764,"se sacan cosas, se vacía,"],
 [1765,1767,"se cambian objetos,"],[1768,1773,"cómo cambia la energía del hogar."],[1774,1776,"Se nota muchísimo."],
]),
}

if __name__ == "__main__":
    aqui = Path(__file__).resolve().parent
    for n, (t, l) in R.items():
        json.dump({**COMUN, "nombre": n, "titulo": t, "lineas": l}, open(aqui / f"{n}.json", "w", encoding="utf-8"),
                  ensure_ascii=False, indent=1)
