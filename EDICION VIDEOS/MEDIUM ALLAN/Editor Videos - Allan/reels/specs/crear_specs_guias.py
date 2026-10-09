"""Reels «franjas azules» de «Cómo Conectar con tus Guías Espirituales_ Qué son_ _ Médium Allan García.mp4».
Original HORIZONTAL 1280x720 (Allan fijo en el centro) -> se compone con plantillas/fondo_franjas_azules.png.
OJO: banner «RESERVA TU CITA AHORA» + QR en 430-440 s y 749-758 s: no usar esos tramos.
Subtítulos partidos a mano en frases naturales de <= 6 palabras (feedback: nada de frases largas).
v2 (feedback 2026-10-07): sin redundancias («realmente… realmente»), con los conectores que dan contexto y congruencia."""
import json
from pathlib import Path

COMUN = {"estilo": "franjas_azules",
         "video": "Cómo Conectar con tus Guías Espirituales_ Qué son_ _ Médium Allan García.mp4",
         "tiempos": "trabajo/guias/tiempos.json",
         "componer": {"fondo": "plantillas/fondo_franjas_azules.png", "y": 588, "alto": 768, "x": 100}}

R = {
"guias_01_abuelos": ("TUS ABUELOS NUNCA SE FUERON DEL TODO", [
 # gancho
 [306,310,"Los ángeles de la guarda"],[311,313,"son nuestros abuelos,"],[314,315,"nuestros ancestros,"],
 [316,319,"nuestros padres, nuestras madres."],
 # quiénes son
 [133,135,"Los más cercanos,"],[136,138,"los más inmediatos,"],[139,143,"los que siempre están ahí"],
 [144,146,"y hacen mucho"],[147,152,"por mandarnos señales de alguna forma,"],[153,155,"suelen ser familiares:"],
 [156,157,"abuelos, abuelas,"],[158,161,"incluso bisabuelos o bisabuelas,"],[162,163,"generaciones anteriores."],
 # cómo nos sienten
 [328,331,"Porque yo creo que"],[332,334,"no nos ven"],[335,338,"como nosotros entendemos ver,"],
 [346,352,"sino que hay una conexión espiritual"],[353,356,"a nivel de sensación."],
 [360,363,"Nos ven como energías"],[364,368,"y nos sienten como energías."],
 # se unen a nosotros
 [440,443,"Se unen a nosotros"],[444,447,"y a nuestros hijos,"],[448,451,"a nuestras generaciones siguientes,"],
 [457,460,"como a modo de"],[461,464,"ángel de la guarda,"],[467,468,"una ayuda,"],[469,471,"un acompañamiento constante."],
 [482,484,"Son almas increíbles"],[485,488,"y es como si"],[489,491,"hicieran un compromiso"],
 [496,499,"de protegernos a nosotros"],[500,503,"o a nuestros hijos."],
 # cierre práctico
 [640,643,"Muchas veces decimos: oye,"],[644,646,"abuelita, abuelo, ayúdame"],[647,650,"por favor con esto,"],
 [651,654,"mándame tal, mándame cual,"],[658,662,"se arregla el día siguiente."],
]),
"guias_02_suenos": ("NO TODOS LOS SUEÑOS SON SUEÑOS", [
 # gancho
 [1257,1259,"Cuando hay sueños"],[1260,1265,"que sabemos que es más real"],[1266,1268,"que un sueño,"],
 [1269,1272,"donde hablamos con ellos"],[1273,1278,"y donde podemos recordar exactamente todo,"],
 [1281,1283,"todas las palabras,"],[1284,1288,"todo lo que se ve,"],[1289,1293,"todo lo que se siente"],
 [1294,1296,"en el sueño,"],[1297,1301,"incluso la temperatura, el olor,"],[1302,1303,"la textura."],
 [1306,1308,"Eso nos indica"],[1309,1314,"que realmente no es un sueño"],[1325,1327,"sino que es"],
 [1328,1331,"una experiencia de encuentro"],[1332,1335,"donde ellos se acercan"],[1336,1341,"y nos hablan o nos ayudan."],
 # lo que NO es una visita
 [1168,1173,"No siempre que soñemos con ellos"],[1174,1179,"quiere decir que son ellos realmente."],
 [1222,1227,"Y tenemos esos sueños tan extraños"],[1231,1234,"donde les vemos sufriendo"],
 [1235,1240,"o que están enfadados con nosotros."],[1241,1244,"Eso tiene que ver"],
 [1245,1248,"más con nuestras preocupaciones"],[1249,1251,"y nuestros miedos,"],[1252,1255,"más con nuestro duelo."],
 # su experiencia
 [1128,1133,"Yo las experiencias que he tenido"],[1134,1139,"con mi ángel de la guarda"],[1140,1141,"más cercano,"],
 [1142,1145,"que en este caso"],[1146,1148,"es mi abuela,"],[1149,1153,"siempre ha sido un sueño."],
 [1427,1429,"En un momento"],[1430,1434,"en el que me rendí,"],[1441,1444,"tiré la toalla completamente"],
 [1445,1446,"y dije:"],[1454,1457,"haz lo que quieras,"],[1458,1463,"yo me rindo, no puedo más."],
 [1464,1469,"En ese momento soñé con ella."],[1475,1477,"Y es curioso"],[1478,1480,"porque me trajo"],
 [1481,1485,"a otro de mis ancestros"],[1486,1489,"que necesitaba el perdón"],[1490,1493,"para continuar su alma."],
 [1498,1500,"Yo le perdoné"],[1501,1503,"y nos abrazamos."],
 [1523,1528,"Era tan real que sé"],[1529,1532,"que no es un sueño."],
]),
"guias_03_desgracias": ("POR QUÉ TUS GUÍAS NO EVITAN LAS DESGRACIAS", [
 # gancho (sin el segundo «realmente»)
 [820,823,"Realmente no somos humanos,"],[825,826,"somos almas"],[827,830,"viviendo en un cuerpo."],
 # la pregunta
 [726,729,"Y es muy normal"],[730,732,"el no entender"],[733,738,"por qué permiten que sucedan cosas"],
 [739,743,"o desgracias en las familias."],
 # libre albedrío
 [744,748,"Pero ahí tenemos que hablar"],[749,751,"del libre albedrío."],
 [761,765,"Hay una especie de contrato"],[766,770,"no plasmado, pero sí existente,"],
 [771,774,"donde no pueden interferir"],[775,780,"en lo que tenga que ocurrirnos"],[781,783,"o el aprendizaje"],
 [784,789,"por el que tengamos que atravesar."],
 # almas en un cuerpo
 [790,793,"Nosotros vemos la vida"],[794,799,"como si esto fuese lo único,"],
 [800,805,"o como si el ser humano"],[806,810,"es lo único que existe,"],[811,814,"no hay nada más,"],
 [815,819,"pero para nada es así."],
 [846,851,"Tenemos que tener un cuerpo material"],[852,854,"porque si no"],[855,859,"no podríamos vivir esta experiencia."],
 [860,863,"Entonces, se nos olvida"],[864,867,"que realmente la importancia"],[868,870,"es el alma"],
 [871,877,"y no es la funda, el cuerpo."],
 # el camino corto
 [887,890,"Por eso, muchas veces,"],[891,895,"si el camino del alma"],[896,899,"es un camino corto,"],
 [901,904,"tiene que ser así,"],[905,910,"porque ese alma ya lo pactó"],[911,915,"o porque es mejor así,"],
 [916,919,"si de alguna forma"],[920,921,"el aprendizaje"],[922,926,"o lo que ese alma"],[927,929,"vino a enseñar"],
 [930,931,"está cumplido."],[932,935,"La misión está cumplida."],
 [936,941,"Realmente hay que vernos como almas"],[942,945,"y no como cuerpos."],
]),
"guias_04_creer_para_ver": ("NUNCA TE CONTESTARÁN CUANDO TÚ QUIERAS", [
 # gancho
 [2403,2408,"Hay que creer para poder ver,"],[2409,2412,"no ver para creer."],[2413,2416,"Es completamente al revés."],
 # el error
 [1983,1985,"Si queremos comunicarnos,"],[1997,2002,"lo primero que tenemos que hacer"],[2003,2004,"es olvidarnos"],
 [2005,2006,"de que"],[2010,2013,"queremos que se comporten"],[2014,2017,"como si fueran humanos."],
 [2018,2021,"Eso es lo primero"],[2022,2025,"que nos hace frustrarnos,"],[2026,2031,"porque nunca nos van a contestar"],
 [2032,2036,"cuando queremos que nos contesten."],
 # lo que sí podemos hacer
 [2037,2042,"Pero sí podemos facilitarles el trabajo."],
 [2045,2047,"Podemos darles gracias,"],[2048,2050,"podemos pedirles señales,"],[2051,2054,"pero creer en ellos,"],
 [2055,2058,"no cuestionar sus señales:"],
 [2065,2067,"números, sensaciones, canciones,"],[2068,2070,"colores, personas, intuiciones,"],[2071,2071,"sueños."],
 [2176,2181,"Y en mi caso funcionó así,"],[2182,2187,"que lo mejor es dejarse guiar,"],[2188,2191,"dejarse llevar y confiar."],
 [2192,2197,"Es que confiar es la clave"],[2198,2200,"de todo esto."],
 [2276,2279,"Ellos nos llevan siempre"],[2280,2285,"y cuando nosotros soltemos el control."],
 # su método
 [2580,2581,"Por ejemplo,"],[2582,2586,"a mí me funciona mucho:"],[2587,2592,"tengo un cuaderno solo para ellos"],
 [2593,2598,"y yo cuando me quiero comunicar"],[2599,2603,"con ellos, pongo la fecha,"],
 [2611,2615,"medito, me relajo, me tranquilizo,"],[2630,2633,"y les digo que"],[2634,2636,"si hay algo"],
 [2637,2640,"que me quieran decir."],[2641,2646,"Y lo primero que me llegue,"],[2647,2650,"aunque sea una canción,"],
 [2651,2653,"yo lo escribo."],[2665,2669,"Siempre hay un mensaje profundo"],[2670,2674,"que me da una respuesta"],
 [2675,2679,"a algo que yo necesitaba"],[2680,2681,"ese día."],
]),
}

if __name__ == "__main__":
    aqui = Path(__file__).resolve().parent
    for n, (t, l) in R.items():
        json.dump({**COMUN, "nombre": n, "titulo": t, "lineas": l}, open(aqui / f"{n}.json", "w", encoding="utf-8"),
                  ensure_ascii=False, indent=1)
