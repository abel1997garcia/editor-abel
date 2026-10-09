/* PRUEBA F4 · «Todo es energía, aunque no la veas» — collage en el gancho y luego una imagen cada vez que nombra algo
   (cada una se queda ≥ 4,5 s salvo que entre la siguiente). Estética: esotérica y energética */
const G = ['img/grabado.jpg', '27% 55%'];
collage(['img/luz.jpg', G, 'img/estrellas.jpg'], .15, en('lo que pasa', 1.5) - .1);
imagen(G[0], en('se siente', 3) - .1, en('todas esas cosas', 8) - .1, { pos: G[1], w: 560, h: 600 });
imagen('img/loto.jpg', en('voz interior', 10) - .15, en('la vida de tus sueños', 13) - .1, { pos: '50% 40%' });
imagen('img/estrellas.jpg', en('la vida de tus sueños', 13) - .05, en('puedes tener', 18) + 1, { pos: '55% 50%' });
