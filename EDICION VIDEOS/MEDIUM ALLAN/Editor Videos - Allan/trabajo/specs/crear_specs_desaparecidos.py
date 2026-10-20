"""Reels «franjas azules» de «¿Qué Ocurre con los Seres Queridos Desaparecidos_ + Anécdotas _ Médium Allan García.mp4».
El original es HORIZONTAL (1280x720) sin franjas: se compone el vertical con plantillas/fondo_franjas_azules.png.
Índices de trabajo/desaparecidos/tiempos.json. Cada línea: [palabra_ini, palabra_fin, "subtítulo tal cual se dice"]."""
import json
from pathlib import Path

COMUN = {"estilo": "franjas_azules",
         "video": "¿Qué Ocurre con los Seres Queridos Desaparecidos_ + Anécdotas _ Médium Allan García.mp4",
         "tiempos": "trabajo/desaparecidos/tiempos.json",
         "componer": {"fondo": "plantillas/fondo_franjas_azules.png", "y": 588, "alto": 768, "x": 90}}

R = {
"desap_01_la_cara": ("SU CARA ENCAJÓ EXACTA EN LA DE SU NIETA", [
 # gancho
 [564,569,"Veo la cara de la mujer"],[570,585,"y él se coloca por detrás y encaja su cara exactamente en la cara de ella."],
 [586,591,"Me dio un vuelco el corazón."],
 # la historia
 [231,237,"Conocí a una persona que me eligió"],[238,240,"para que yo"],[259,262,"le hiciese una lectura."],
 [263,275,"Era una persona que no se sabía nada, que desapareció hace mucho tiempo."],
 [278,288,"Resulta que yo empecé a cerrar mis ojos, empecé a percibir,"],[294,298,"y ocurrió algo muy curioso."],
 [299,319,"Y es que vi a una persona con un uniforme de la Guerra Mundial, digamos, como si fuera de los alemanes."],
 [332,337,"Esta persona era su abuelo,"],[343,348,"y que le llamaban el alemán."],
 [349,362,"Resulta que este hombre tuvo que huir de Alemania porque tenía un apellido judío."],
 [379,382,"Conoció a una mujer,"],[429,432,"esta mujer quedó embarazada."],
 [496,511,"La persona que me pidió esta sesión es la nieta, que ya es una mujer mayor."],
 # la confirmación
 [609,613,"Y es que eran exactos."],[614,616,"Ella me confirmó"],[618,623,"que decían que su abuelo era"],
 [625,628,"una viva copia suya."],[664,668,"Esas casualidades que no existen."],
]),
"desap_02_sabia_que_no_volveria": ("SABÍA QUE NO IBA A VOLVER A VERLA", [
 # gancho
 [823,838,"Sabía, cuando iba en ese coche, que no iba a volver a ver a su amada."],
 [839,848,"Él sabía que nunca más iba a volver a verla."],
 # lo que le mostró
 [688,698,"Me explicó que hubo como una cacería, una especie de cacería,"],
 [699,707,"donde todas las personas con origen alemán eran perseguidas."],
 [718,720,"Pero lo cogieron"],[721,734,"y él me mostró que le pusieron una pistola en un lado del vientre"],
 [736,746,"y lo metieron en un coche y condujeron por la noche"],[747,750,"y lo llevaron lejos."],
 [756,768,"Había más personas en ese coche y hubo más viajes en aquella noche."],
 [772,775,"A mí me mostraba"],[777,780,"un final muy trágico."],[795,801,"Y él fue uno más, incluso semienterrados."],
 # sentirlo en su cuerpo
 [1000,1017,"Él lo sabía, él iba en silencio sabiendo que no iba a volver a ver a los suyos."],
 # el cierre
 [1075,1083,"Al menos pude dar a esa familia ese cierre."],
 [1111,1116,"Esta persona, cuando llegó a Uruguay,"],[1117,1120,"me mandó un audio"],
 [1122,1133,"dándome las gracias y diciendo que iba a hablar con su familia."],
 [1250,1258,"La sensación que tuve fue de una paz tremenda."],
]),
"desap_03_el_hermano": ("LE CONTÉ CÓMO MURIÓ SIN SABER QUE LO BUSCABAN", [
 # gancho: lo que Allan vio -> la revelación
 [1601,1616,"A mí me enseñaron también cómo lo sacaron con un coche de la ciudad, varias personas,"],
 [1619,1621,"acabaron con él."],
 [1662,1672,"Y me dijo: mira, realmente yo he cogido la sesión porque"],
 [1673,1688,"mi hermano desaparecido hace más de dos años fue secuestrado y no sabemos nada de él."],
 # cómo empezó
 [1523,1535,"Y era una mujer joven que me enseñó una foto de un hermano."],
 [1551,1568,"Le dije que tenía problemas o que a alguien le estorbaba y que lo habían quitado del medio"],
 [1569,1574,"por las cosas que él decía."],[1583,1593,"Pero él hablaba, influenciaba a muchas personas y molestaba a otros."],
 [1622,1637,"Fijaros que esta mujer, cuando voy contándole la fe de vida, yo notaba un silencio, algo."],
 [1693,1698,"Yo me quedé un poco impresionado."],
 # el padre
 [1749,1774,"Para su padre era muy importante, ya que todos los días tenía la esperanza de encontrarle y decía que no iba a morirse hasta no encontrarlo."],
 [1784,1785,"Ella mentía"],[1786,1789,"una mentira piadosa"],[1790,1792,"a su padre"],[1793,1800,"diciéndole que había pistas, que lo habían visto."],
 # el cierre
 [1823,1838,"Pero que ella me aseguró que ella sospechaba, porque ella había soñado con él varias veces,"],
 [1839,1850,"que él no estaba entre nosotros, que estaba en el otro plano."],
]),
"desap_04_no_es_adivinar": ("UN MÉDIUM NO ESTÁ PARA ADIVINAR NOMBRES", [
 # gancho
 [1989,1999,"Es muy importante, el trabajo de un médium es muy serio"],
 [2000,2017,"y no es sólo adivinar o acertar o a ver si digo un nombre o si no lo digo."],
 [2249,2257,"El trabajo de un médium es más que mostrarse"],[2258,2268,"en redes sociales a ver si contacta con nuestro ser querido."],
 [2269,2271,"Hay mucho más."],
 # lo que también es
 [1427,1433,"No es solo despedirse o dar mensajes."],
 [1434,1444,"A veces también hay que buscar, cerrar ciclos, cerrar historias, encontrar"],
 [1445,1464,"esa parte que queda pendiente, esos pendientes que yo siempre digo que el alma puede arrastrar durante toda una eternidad."],
 [1947,1960,"Esas familias que buscan a sus seres queridos y que acuden a los médiums."],
 [2131,2134,"A veces los médiums"],[2136,2142,"colaboramos con equipos de búsqueda en secreto."],
 [2186,2198,"El médium también ayuda a las familias a cerrar esos ciclos, esa agonía"],
 [2199,2217,"de no saber de sus seres queridos, de no saber si están vivos, si no están vivos, dónde están."],
 # cierre
 [2286,2298,"Yo reivindico y lucharé siempre por elevar el significado de la palabra médium"],
 [2299,2312,"hasta donde tiene que llegar, porque es un significado muy grande y muy amplio."],
]),
}

if __name__ == "__main__":
    aqui = Path(__file__).resolve().parent
    for n, (t, l) in R.items():
        json.dump({**COMUN, "nombre": n, "titulo": t, "lineas": l}, open(aqui / f"{n}.json", "w", encoding="utf-8"),
                  ensure_ascii=False, indent=1)
