// Comprobador de la pizarra:  node revisar.mjs <proyecto de la skill>
// Para cada animación de edicion/montaje.json avisa de: primer fotograma vacío, ratos de > PARADO s sin que pase
// nada en el contenido (la deriva de cámara no cuenta), textos/emojis/flechas que se pisan, cualquier cosa fuera del
// 4:3 o texto < 56 px (el reel tiene que verlo todo), y en «consola:» los textos que no dicen lo que él dice.
import path from 'node:path';
import fs from 'node:fs';
import { pathToFileURL } from 'node:url';
const PARADO = 2, PASO = 1 / 6;   // con él hablando, algo nuevo cada ≤ 2 s
const pro = path.resolve(process.argv[2] || '.');
const { chromium } = await import(pathToFileURL(path.join(pro, 'node_modules/playwright-core/index.mjs')).href);
const { serve } = await import(pathToFileURL(path.join(pro, 'server.mjs')).href);
const m = JSON.parse(fs.readFileSync(path.join(pro, 'edicion/montaje.json'), 'utf8'));
const srv = await serve();
const b = await chromium.launch();
const p = await b.newPage({ viewport: { width: 1920, height: 1080 } });
p.on('console', x => x.type() === 'error' && console.log('consola:', x.text()));
await p.goto(`http://127.0.0.1:${srv.address().port}/index.html?render`);
await p.evaluate(() => window.__ready);
const en = async t => p.evaluate(async t => { await window.__render(t); return { h: huella(), s: solapes() }; }, t);
let avisos = 0;
for (const pl of m.planos.filter(x => x.tipo === 'anim')) {
  const a = pl.f0 / m.fps, z = pl.f1 / m.fps, msg = [];
  const r0 = await en(a + .04);
  if (!r0.h.match(/(^|\||#)([1-9]|10)/)) msg.push('primer fotograma vacío');
  let ult = r0.h, desde = a;
  for (let t = a + PASO; t < z; t += PASO) {
    const r = await en(t);
    if (r.h !== ult) { if (t - desde > PARADO) msg.push(`parada ${desde.toFixed(1)}–${t.toFixed(1)} s`); ult = r.h; desde = t; }
  }
  if (z - desde > PARADO + .8) msg.push(`parada ${desde.toFixed(1)}–${z.toFixed(1)} s (final)`);   // el final aguanta 0,5–1 s a propósito
  const fin = await en(z - .3);
  msg.push(...fin.s);
  if (msg.length) { avisos += msg.length; console.log(`${pl.id} (${a.toFixed(1)}–${z.toFixed(1)}): ${msg.join(' · ')}`); }
}
console.log(avisos ? `${avisos} avisos` : 'todo bien');
await b.close(); srv.close();
