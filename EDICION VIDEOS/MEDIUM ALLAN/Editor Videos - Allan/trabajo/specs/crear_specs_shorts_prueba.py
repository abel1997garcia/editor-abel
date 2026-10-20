"""Reels estilo «franja negra» (canalización) de «shorts prueba.mp4» (sesión con Ingrid, su padre Juan).
Índices de trabajo/shorts_prueba/tiempos.json. Cada línea: [palabra_ini, palabra_fin, "texto tal cual se dice"]."""
import json
from pathlib import Path

COMUN = {"estilo": "franja_negra", "video": "shorts prueba.mp4", "tiempos": "trabajo/shorts_prueba/tiempos.json",
         "titulo": ""}

R = {
"canal_01_eramos_cinco": [
 # gancho: dato concreto de Allan -> confirmación inmediata
 [579,586,"Me dice cinco. No sé por qué cinco."],[587,590,"No sé si sois..."],
 [591,592,"Éramos cinco."],[593,599,"Mi mamá, mis tres hermanos y él."],[600,601,"Eso es."],
 # el cuerpo al final -> falla multisistémica
 [193,202,"Y él es como, se quedó muy delgado, muy consumido."],
 [207,216,"En el momento de fallecer estuvo muy hinchado, muy hinchado."],[217,219,"Por el vientre."],
 [221,236,"Es como el páncreas y cosas así, me habla como de órganos, al final le afectan."],
 [237,241,"Sí, fue una falla multisistémica"],[242,250,"que terminó dándole al final por el infarto intestinal."],
 # carácter -> confirmación
 [390,402,"Es como un hombre muy nervioso, pero como llevar el nervio por dentro."],
 [425,426,"Eso es."],
 # todo muy rápido -> el miércoles
 [432,450,"Como si todo esto se descubre muy tarde, es como si no da tiempo. Él se lo lleva rápido."],
 [461,474,"Sí, mi papá, esto fue muy rápido, él estaba muy bien un día miércoles,"],[475,476,"almorzó conmigo."],
 [508,522,"Y el día, en la noche, empezó con un dolor en su estómago muy fuerte."],
 [532,537,"Y tenía un infarto intestinal fulminante."],
 # cierre: otro hombre en el plano espiritual -> su hijo
 [1009,1016,"Hay otro hombre aquí en el plano espiritual."],[1041,1043,"Es mi hijo."],
],
"canal_02_calma": [
 # gancho: la palabra que él usaba
 [1700,1704,"Él me pide como calma."],
 [1710,1722,"Que con el tiempo las cosas se irán poniendo en su sitio."],
 [1723,1729,"Esa era una palabra que usaba mucho."],[1730,1730,"Calma, calma, calma,"],[1731,1731,"calma."],
 # la casa -> la construcción sin terminar
 [288,304,"Y me habla y gesticula como que algo pasa con la casa, algo pasa con la casa,"],
 [308,327,"es como si no quiere que os vayáis o que os quiten la casa o que se pierda la casa."],
 [352,363,"Yo creo que tiene sentido porque él era, amaba mucho su casa,"],
 [364,376,"y últimamente dejó inconcluso algo porque él empezó a construir y no terminó."],[377,379,"Se fue antes."],
 # trabajó demasiado -> maestro carpintero
 [700,708,"Me habla de trabajar mucho o haber trabajado mucho."],
 [744,748,"Dice: creo que trabajé demasiado."],[749,749,"Sí."],[750,753,"Él era maestro carpintero."],
 # cierre: la señora mayor que tira besos
 [2236,2241,"Hay una mujer mayor aquí también."],
 [2273,2284,"Yo la veo delgada, como si falleció y quedó como muy delgadita."],
 [2288,2292,"Ella te tira muchos besos."],[2293,2298,"Sí, ella era de tirar besos."],
 # cierre emocional: lo que él le pide -> lo que ella vive
 [1805,1820,"Dice que pasar tanto tiempo allí no te hace bien, como que salgas un poco afuera."],
 [1832,1845,"Porque yo no quiero salir, no me dan ganas de salir de nada, porque"],
 [1846,1851,"todo el día éramos los dos."],[1852,1856,"Todo el día los dos."],
],
}

if __name__ == "__main__":
    aqui = Path(__file__).resolve().parent
    for n, l in R.items():
        json.dump({**COMUN, "nombre": n, "lineas": l}, open(aqui / f"{n}.json", "w", encoding="utf-8"),
                  ensure_ascii=False, indent=1)
