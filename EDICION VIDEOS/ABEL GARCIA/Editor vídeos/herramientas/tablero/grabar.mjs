// Graba el tablero fotograma a fotograma:  node grabar.mjs <carpeta de trabajo> <segundos> <salida.mp4> [--sfx sfx.json] [--fotos t1,t2,...]
// La carpeta de trabajo tiene motor.html, datos.js, escenas.js, la fuente y frames/ (su vídeo, un JPG por fotograma).
import { chromium } from 'playwright-core';
import { pathToFileURL } from 'node:url';
import { readdirSync, writeFileSync } from 'node:fs';
import { spawn } from 'node:child_process';
import path from 'node:path';
const [,, dir, dur, out, ...resto] = process.argv, FPS = 30;
const opc = k => { const i = resto.indexOf(k); return i >= 0 ? resto[i + 1] : null; };
const base = process.env.LOCALAPPDATA + '/ms-playwright', hs = readdirSync(base).find(d => d.startsWith('chromium_headless_shell-'));
const b = await chromium.launch({ executablePath: `${base}/${hs}/chrome-headless-shell-win64/chrome-headless-shell.exe`, args: ['--allow-file-access-from-files'] });
const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
const errores = []; p.on('console', m => m.type() === 'error' && errores.push(m.text())); p.on('pageerror', e => errores.push(String(e)));
await p.goto(pathToFileURL(path.resolve(dir, 'motor.html')).href); await p.waitForFunction(() => document.title === 'listo', null, { timeout: 60000 });
if (errores.length) console.log('consola:', [...new Set(errores)].join('\n  '));
if (opc('--sfx')) writeFileSync(opc('--sfx'), JSON.stringify(await p.evaluate(() => window.SFX)));
const toma = async t => { await p.evaluate(async t => { await window.cargarFoto(Math.round(t * 30)); window.pintar(t); if (window.esperar) await window.esperar(); }, t);
  return p.screenshot({ type: 'png', clip: { x: 0, y: 0, width: 1080, height: 1920 } }); };
if (opc('--fotos')) {                                       // solo unos fotogramas para revisar
  for (const t of opc('--fotos').split(',').map(Number)) writeFileSync(path.join(out, `f_${t.toFixed(2)}.png`), await toma(t));
} else {
  const ff = spawn('ffmpeg', ['-v', 'error', '-y', '-f', 'image2pipe', '-framerate', String(FPS), '-c:v', 'png', '-i', '-', '-c:v', 'libx264', '-crf', '16', '-preset', 'veryfast', '-pix_fmt', 'yuv420p', out], { stdio: ['pipe', 'inherit', 'inherit'] });
  const n = Math.round(+dur * FPS);
  for (let i = 0; i < n; i++) {
    const buf = await toma(i / FPS);
    if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
    if (i % 300 === 0) console.log(`  ${i}/${n}`);
  }
  ff.stdin.end(); await new Promise(r => ff.on('close', r));
}
await b.close();
