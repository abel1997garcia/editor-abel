# Dibujos de pizarra para los reels

> **Desde el 19/10 los genero yo con Nano Banana** (`herramientas/pizarra_replicate.py`), en PNG transparente y por contexto (ver `IMAGENES/LEEME.md`). Los prompts de ChatGPT de abajo ya no se usan; la lista de escenas sigue valiendo como guía.

Para el formato «pizarra digital» de los guiones virales y las listas: diapositivas en la zona oscura del reel de tablet, con un título y UN dibujo que cuenta la escena. Personaje ROJO = la persona cuando se abandona (lo que hace mal); AZUL = la misma persona cuando se elige (la solución).

## Cómo hacerlos (en ChatGPT)
1. **Primero, el personaje (una sola vez):** pide la «hoja del personaje» (prompt A). Guárdala: es la referencia de todos los demás.
2. **Cada dibujo:** abre un chat, adjunta la hoja del personaje y pega el prompt B con la escena de la lista.
3. **Guárdalos aquí** (`IMAGENES/pizarra/`) con el nombre de la lista (por ejemplo `p01_compañero_te_pasa_trabajo.png`). Yo les quito el fondo negro, los centro y los sincronizo con el audio.

### Prompt A · hoja del personaje
```
Crea la hoja de personaje para una serie de dibujos de pizarra. Estilo: ilustración de LÍNEA, trazo blanco uniforme de grosor medio sobre fondo NEGRO puro (#000000), sin sombras, sin degradados, sin rellenos, sin texto. Minimalista, legible en tamaño pequeño, como un pictograma narrativo moderno.
Personaje: una persona joven sencilla (sirve para hombre o mujer), cabeza redonda, pelo corto apenas insinuado, cuerpo de silueta simple, cara con ojos y boca mínimos que dejan ver la emoción.
Dibújalo 6 veces en la misma hoja: de frente tranquilo, triste, agobiado, con miedo, en paz con los ojos cerrados y con la mano levantada diciendo «para». Las 3 primeras con el trazo del personaje en ROJO (#F05050) y las 3 últimas en AZUL (#2E7BFF); todo lo demás, en blanco.
```

### Prompt B · cada dibujo
```
Dibujo de pizarra con el MISMO personaje de la hoja adjunta y el mismo estilo: ilustración de LÍNEA, trazo blanco uniforme sobre fondo NEGRO puro (#000000), sin sombras, sin degradados, sin rellenos, SIN TEXTO NI LETRAS, sin marcas de agua. El personaje, con el trazo en [ROJO #F05050 | AZUL #2E7BFF]; todo lo demás, en blanco.
Escena: [ESCENA DE LA LISTA].
Que se entienda en un segundo, en tamaño pequeño. Composición centrada, formato cuadrado 1024×1024, 12 % de margen alrededor, como mucho 3 elementos además del personaje.
```

## Lo que ya hay en la biblioteca y sirve (vectorizado)
Bocetos cotidianos: escritorio con reloj y persona sola trabajando (`escritorio_reloj_silueta`), persona desbordada con muchas tareas (`multitarea_desbordada_boceto`), reunión en una mesa (`reunion_mesa_boceto`), subir una montaña (`subir_montana_boceto`), trabajando de noche en el ordenador (`trabajando_ordenador`). Esquemas: silueta en el campo toroidal (`toroide_silueta_negra`), cuerpo-mente-espíritu (`espiritu_cuerpo_alma`), chakras (`prana_vayus_meditacion`, `toroide_chakras_columna`), miedo/amor (`miedo_amor_toroide`), integrar la sombra (`integrar_la_sombra`). El arte visionario a color no sirve para este formato.

## La lista (lo que falta, por guion; R = rojo, A = azul)
**Genéricos, se reutilizan en muchos guiones**
- g01 R · El personaje con una batería casi vacía sobre la cabeza, hombros caídos.
- g02 R · El personaje sentado en la cama de noche, mirando el móvil, con un reloj que marca las 3:00.
- g03 R · El personaje sonriendo con una máscara sonriente sujeta delante de la cara; detrás, su cara triste.
- g04 R · El personaje con una mano en el pecho y una nube oscura dentro del pecho (el miedo que no reconoce).
- g05 A · El personaje sentado con los ojos cerrados y una mano en el pecho, en paz, con ondas suaves a su alrededor.
- g06 A · El personaje de pie, tranquilo, dentro de un campo de energía en forma de toro (líneas curvas alrededor).
- g07 A · Dos personajes sentados hablando; uno escucha con atención al otro (compartirlo).
- g08 A · El personaje con la mano levantada diciendo «para», firme y tranquilo.

**Decir que no también es quererte**
- p01 R · Un compañero le deja una pila alta de carpetas en la mesa; reloj de pared a las 19:00.
- p02 R · El compañero se va por la puerta con la chaqueta; el personaje se queda solo en la mesa, agotado.
- p03 A · El personaje dice «déjame que lo mire» con una mano levantada y un reloj de arena al lado. (Puede usarse g08.)

**Cuanto menos actúas para gustar, más te quieren**
- p04 R · El personaje en una cena con varias personas, sonriendo forzado con una máscara (o g03).
- p05 R · El personaje llegando a casa vacío, apoyado en la puerta, con la máscara en la mano.
- p06 A · El personaje hablando tranquilo y natural en la mesa, sin máscara, y dos personas mirándole con cariño.

**Te tratan como te tratas**
- p07 R · El personaje mirándose al espejo; en el espejo, su reflejo con cara de desprecio.
- p08 R · Una rueda/círculo de flechas con tres iconos: un corazón triste, una cabeza con nube y un personaje encogido (la rueda sentir → pensar → actuar).
- p09 A · La misma rueda de flechas, ahora con un corazón tranquilo, una cabeza despejada y el personaje erguido.

**No tienes mala suerte, es tu energía**
- p10 R · El personaje en la cola del supermercado detrás de un carro lleno, resoplando.
- p11 R · El personaje con una nube de tormenta solo encima de su cabeza.
- p12 A · El personaje de pie con los ojos cerrados respirando y la nube deshaciéndose. (O g05.)

**Deja de leer libros de autoestima y haz esto**
- p13 R · El personaje sentado detrás de una torre de libros subrayados, con cara de seguir igual.
- p14 A · El personaje cerrando un libro y llevándose la mano al pecho.

**Lo más difícil de cambiar no es el esfuerzo**
- p15 R · El personaje saltando entre tres caminos (pesas, libro, cojín de meditar) sin avanzar.
- p16 A · El personaje mirando hacia dentro: una brújula dibujada en su pecho.

**Si solo intentas entenderte, por eso no cambias**
- p17 R · El personaje con una cabeza enorme llena de engranajes y un cuerpo pequeño y quieto.
- p18 A · El personaje caminando, moviéndose, con la mano en el pecho y una persona al lado que le acompaña.

**Nunca te hables como no le hablarías a tu mejor amigo**
- p19 R · El personaje con un bocadillo de cómic lleno de rayones y tachones dirigido a sí mismo.
- p20 A · El personaje con el brazo sobre el hombro de su propio reflejo, como un amigo.

**Te sientes ridículo cuando empiezas a quererte, y es perfecto**
- p21 R · El personaje diciendo «no» con la voz temblorosa (ondas temblorosas saliendo de la boca) y la cara roja.
- p22 A · El personaje erguido, tranquilo, con una línea de ondas estables saliendo de la boca.

**Deja de buscar tu sitio, tu sitio eres tú**
- p23 R · El personaje con una maleta, ante tres señales que apuntan a ciudades distintas, perdido.
- p24 A · El personaje sentado tranquilo con una casa dibujada en su pecho.

**Visualiza cada mañana la vida en la que te quieres**
- p25 R · El personaje en la cama al despertar con una nube oscura de pensamientos.
- p26 A · El personaje en la cama, medio dormido, con una burbuja de pensamiento en la que se ve a sí mismo en paz.

**Enseña todo lo que eres, no solo lo que gusta**
- p27 R · El personaje enseñando solo una foto sonriente y escondiendo detrás una caja con muchas cosas suyas.
- p28 A · El personaje abriendo la caja y enseñando lo que había dentro.

**No te aplauden por cambiar, pero te están mirando**
- p29 R · El personaje en un escenario vacío, esperando aplausos; butacas vacías.
- p30 A · El personaje caminando tranquilo; desde detrás de unas cortinas o ventanas le miran varias caras.

**Es imposible que fracases en tu cambio**
- p31 R · El personaje dando la vuelta en una escalera, a un escalón de llegar arriba, mientras varias personas le miran raro.
- p32 A · El personaje subiendo el escalón aunque le miren, con paso firme.

**Elegirte a ti no es para débiles**
- p33 R · Varias personas alejándose de espaldas del personaje, que se queda solo.
- p34 A · El personaje de pie y en paz mientras a su alrededor todo tiembla (líneas de movimiento en el suelo).

**La era de fingir que estás bien se está muriendo**
- p35 R · Un escaparate con la foto de una vida perfecta; detrás, el personaje real triste.
- p36 A · El personaje contando algo con las manos abiertas y otra persona escuchando con cariño. (O g07.)

**Lo que escondes te pesa cada día más**
- p37 R · El personaje cargando una mochila enorme y oscura a la espalda, encorvado.
- p38 A · Dos personajes sentados; el primero deja la mochila en el suelo mientras habla.
