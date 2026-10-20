"""Reels «franjas azules» de «aunque todo se repita, sigue.mp4» (Escritorio). Original HORIZONTAL 1920x1080, Allan
caminando por el campo -> se compone con plantillas/fondo_franjas_azules.png. Método de cortes aprobado.
Subtítulos partidos a mano (<= 6 palabras); guiones leídos de corrido (congruencia, conectores, sin redundancias)."""
import json
from pathlib import Path

COMUN = {"estilo": "franjas_azules",
         "video": "C:/Users/Clap/Desktop/aunque todo se repita, sigue.mp4",
         "tiempos": "trabajo/sigue/tiempos.json",
         "componer": {"fondo": "plantillas/fondo_franjas_azules.png", "y": 588, "alto": 768}}

R = {
"sigue_01_despertar": ("EL DESPERTAR ESPIRITUAL NO OCURRE UNA SOLA VEZ", [
 # gancho: la pregunta que se hace todo el que lo vive
 [0,5,"¿Por qué si ya he pasado"],[6,9,"por un despertar espiritual"],[10,15,"vuelvo a sentirme con el tiempo"],
 [16,18,"otra vez igual?"],[19,23,"Pues eso es muy normal."],
 [24,26,"El despertar espiritual"],[27,31,"no sucede de una vez,"],[32,36,"no es solo una vez"],
 [37,41,"y ya está para siempre."],[45,48,"Es un proceso cíclico."],
 [50,53,"Te lo digo yo:"],[55,57,"lo he sufrido"],[58,60,"en mis carnes"],[61,64,"y lo sigo sufriendo"],
 [65,68,"a día de hoy."],
 # cómo llega
 [69,72,"Cuando todo se acomoda,"],[73,77,"cuando todo parece estar bien,"],[78,81,"cuando todo marcha mejor,"],
 [82,84,"siempre sucede algo,"],[85,88,"siempre hay un cambio,"],[89,93,"hay algo que nos saca"],
 [94,98,"de nuestra zona de confort"],[125,130,"y nos pone una nueva prueba."],
 [131,135,"Eso es así, eso sucede"],[136,138,"y es inevitable."],
 # muchos despertares
 [152,155,"Realmente el despertar espiritual"],[156,158,"son muchos despertares,"],
 [159,164,"unos más fuertes, otros más suaves,"],[165,170,"pero siempre es la misma energía."],
 [171,174,"Es un cambio radical,"],[175,178,"es un caerse todo"],[179,181,"cuando está acomodado,"],
 [182,185,"lleno de muchas cosas,"],[186,191,"de muchas situaciones, de muchos logros,"],
 [192,195,"de personas, de trabajos,"],[209,214,"y que al final se caen."],
]),
"sigue_02_pendiente": ("LO QUE MÁS LAMENTAN LOS QUE YA SE FUERON", [
 # gancho: su autoridad de médium
 [1110,1113,"Como médium, cada día"],[1114,1117,"lidio con esas personas"],[1118,1123,"que dejaron para después las cosas"],
 [1124,1126,"y nunca sucedieron:"],[1127,1128,"esa charla,"],[1129,1132,"ese te quiero,"],[1133,1134,"ese perdóname,"],
 [1135,1139,"ese he pensado en ti,"],[1140,1145,"ese no debíamos de habernos separado."],
 [1147,1153,"No solo en parejas, también en familias."],
 # lo que ve en las sesiones
 [1585,1589,"Hago sesiones todos los días"],[1590,1593,"y me quedo impresionado"],[1594,1596,"de que la mayoría"],
 [1598,1600,"de los casos"],[1601,1604,"siempre quedó algo pendiente."],[1605,1609,"Siempre quedó algo por hacer,"],
 [1610,1614,"porque no vivimos el presente,"],[1615,1618,"porque vivimos siempre construyendo"],[1619,1621,"un posible futuro."],[1622,1626,"Eso es un grave error."],
 # lo que hacemos todos
 [1537,1539,"Siempre estamos pensando:"],[1540,1545,"el año que viene hago esto,"],[1546,1549,"el mes que viene"],
 [1550,1552,"hago lo otro,"],[1553,1556,"dentro de cinco años"],[1557,1560,"me compraré una casa,"],
 [1561,1566,"cuando me jubile viviré y disfrutaré."],[1567,1570,"Os aseguro que eso"],[1571,1574,"a veces no llega,"],
 [1575,1577,"muchas veces más"],[1578,1584,"de los que os podéis imaginar."],
 # cierre
 [1636,1641,"Y nunca se sabe si mañana"],[1642,1646,"nos vamos a despertar,"],[1647,1652,"o si dentro de cinco minutos"],
 [1653,1656,"ya no estamos aquí."],[1660,1663,"Así que el presente"],[1664,1668,"es lo único que existe."],
]),
"sigue_03_soledad": ("UNA PARTE DE MÍ SIEMPRE ESTARÁ SOLA", [
 # gancho personal
 [657,659,"Tengo una familia,"],[660,661,"pero realmente"],[662,666,"hay una parte de mí"],[667,670,"que siempre está solo"],
 [671,675,"y siempre ha estado solo"],[676,681,"y sabe que siempre estará solo."],
 # la idea
 [237,240,"La soledad es inevitable,"],[241,247,"la soledad siempre va a estar ahí."],
 [630,634,"Y hay que mostrarse uno"],[635,639,"como es y quién es,"],[640,645,"y ir así por la vida."],
 [646,649,"¿Eso conlleva la soledad?"],[650,650,"Sí."],
 [682,685,"Y no es malo,"],[686,688,"no es malo."],[689,692,"Esa soledad es mía,"],[693,695,"es mi parte,"],
 [696,698,"es algo íntimo"],[699,702,"que tengo solo conmigo"],[703,708,"y que nunca compartiría con nadie."],
 # el error
 [709,712,"Y si lo compartimos"],[713,715,"y lo abrimos,"],[716,719,"es un grave error,"],[720,723,"porque si dejamos entrar"],
 [724,726,"a otra persona"],[727,729,"con otra energía,"],[730,733,"otras vivencias, otras formas"],
 [734,737,"de vivir, de pensar,"],[738,741,"de ver las cosas,"],[742,743,"pues imaginaos"],
 [744,748,"el grave error de siempre:"],[749,751,"dejando nuestra felicidad"],[752,755,"en manos de otros."],
 [756,759,"No, no hagamos eso."],
 # cierre
 [1283,1288,"Y las personas que pasan"],[1289,1291,"por nuestra vida"],[1292,1293,"nos marcan."],
 [1294,1297,"Unos se quedan más,"],[1298,1301,"otros se quedan menos."],[1302,1307,"Unos son cicatrices, otros son sonrisas,"],
 [1308,1312,"pero tenemos que continuar andando"],[1313,1317,"y el camino es solitario."],
]),
"sigue_04_cicatrices": ("TUS HERIDAS SON LO QUE TE HACE ÚNICO", [
 # gancho
 [920,923,"Cuando vemos un león,"],[929,932,"un tigre, algún animal"],[933,935,"con muchas cicatrices,"],
 [936,938,"eso quiere decir"],[939,943,"que ha luchado grandes batallas."],[944,948,"Le da como un estatus,"],
 [949,952,"le da un bagaje,"],[953,956,"le da una sabiduría,"],[957,962,"le da una presencia, una credibilidad."],
 # nuestras cicatrices
 [886,891,"Nuestro alma está llena de cicatrices,"],[892,897,"unas más grandes, otras más pequeñas,"],
 [909,914,"pero esas cicatrices son grandes aprendizajes."],
 # para qué
 [814,818,"Pero apártalo y consigue ver"],[819,822,"un poquito más allá:"],[823,825,"¿qué es esto?"],
 [826,829,"¿Para qué ha sucedido?"],[838,843,"Realmente, cuando nos quitamos esa parte"],[844,848,"de ¿por qué a mí?,"],
 [849,853,"nos damos cuenta y entendemos"],[855,858,"que era para algo."],[859,864,"Hay algo ahí, siempre hay algo."],
 # conviértelas
 [972,975,"Además, la combinación de"],[976,980,"heridas, aunque sean muy parecidas"],[981,982,"todas, realmente"],[983,986,"cada uno ha vivido"],[987,989,"alguna cosa diferente."],[990,990,"Entonces,"],[991,994,"coge todas esas heridas,"],[995,998,"coge todas esas cicatrices"],[999,1003,"y conviértelas en algo único,"],
 [1004,1008,"algo que nadie más tenga."],[1013,1018,"Y eso será tu gran personalidad,"],[1019,1021,"tu gran alma."],
 # cierre
 [1166,1169,"El dolor es necesario"],[1170,1175,"para aprender esas cicatrices del alma."],
 [1176,1180,"Esos son nuestro código único"],[1181,1183,"de cada uno."],
]),
}

if __name__ == "__main__":
    aqui = Path(__file__).resolve().parent
    for n, (t, l) in R.items():
        json.dump({**COMUN, "nombre": n, "titulo": t, "lineas": l}, open(aqui / f"{n}.json", "w", encoding="utf-8"),
                  ensure_ascii=False, indent=1)
