// Graba el tablero fotograma a fotograma:  node grabar.mjs <carpeta de trabajo> <segundos> <salida.mp4> [--sfx sfx.json] [--fotos t1,t2,...]
// La carpeta de trabajo tiene motor.html, datos.js, escenas.js, la fuente y frames/ (su vídeo, un JPG por fotograma).
// En paralelo (Abel 14/10/2026: «no puede ser que para editar tres reels llevemos cerca de una hora»): el reel se parte en
// PAGINAS tramos seguidos, cada pestaña graba el suyo en JPG y al final se unen sin recodificar.
import { chromium } from 'playwright-core';
import { pathToFileURL } from 'node:url';
import { readdirSync, writeFileSync, rmSync } from 'node:fs';
import { spawn } from 'node:child_process';
import { cpus } from 'node:os';
import path from 'node:path';
const [,, dir, dur, out, ...resto] = process.argv, FPS = 30, PAGINAS = Math.max(2, Math.floor(cpus().length / 3));   // 3 reels a la vez
const opc = k => { const i = resto.indexOf(k); return i >= 0 ? resto[i + 1] : null; };
const base = process.env.LOCALAPPDATA + '/ms-playwright', hs = readdirSync(base).find(d => d.startsWith('chromium_headless_shell-'));
const b = await chromium.launch({ executablePath: `${base}/${hs}/chrome-headless-shell-win64/chrome-headless-shell.exe`, args: ['--allow-file-access-from-files'] });
const errores = [];
const pagina = async () => {
  const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  p.on('console', m => m.type() === 'error' && errores.push(m.text())); p.on('pageerror', e => errores.push(String(e)));
  await p.goto(pathToFileURL(path.resolve(dir, 'motor.html')).href); await p.waitForFunction(() => document.title === 'listo', null, { timeout: 60000 });
  return p;
};
const toma = async (p, t, tipo) => { await p.evaluate(async t => { await window.cargarFoto(Math.round(t * 30)); window.pintar(t); if (window.esperar) await window.esperar(); }, t);
  return p.screenshot({ type: tipo, ...(tipo === 'jpeg' ? { quality: 92 } : {}), clip: { x: 0, y: 0, width: 1080, height: 1920 } }); };
const ffmpeg = (args, entrada) => new Promise((ok, mal) => { const f = spawn('ffmpeg', ['-v', 'error', '-y', ...args], { stdio: [entrada ? 'pipe' : 'ignore', 'inherit', 'inherit'] });
  f.on('close', c => c ? mal(new Error('ffmpeg ' + c)) : ok()); if (entrada) entrada(f.stdin); });
const p0 = await pagina();
if (errores.length) console.log('consola:', [...new Set(errores)].join('\n  '));
if (opc('--sfx')) writeFileSync(opc('--sfx'), JSON.stringify(await p0.evaluate(() => window.SFX)));
if (opc('--fotos')) {                                       // solo unos fotogramas para revisar
  for (const t of opc('--fotos').split(',').map(Number)) writeFileSync(path.join(out, `f_${t.toFixed(2)}.png`), await toma(p0, t, 'png'));
} else {
  const n = Math.round(+dur * FPS), paso = Math.ceil(n / PAGINAS), trozos = [];
  const paginas = [p0, ...await Promise.all(Array.from({ length: PAGINAS - 1 }, pagina))];
  await Promise.all(paginas.map(async (p, k) => {
    const a = k * paso, z = Math.min(n, a + paso); if (a >= z) return;
    const trozo = `${out}.${k}.mp4`; trozos[k] = trozo;
    await ffmpeg(['-f', 'image2pipe', '-framerate', String(FPS), '-c:v', 'mjpeg', '-i', '-', '-c:v', 'libx264', '-crf', '16', '-preset', 'veryfast', '-pix_fmt', 'yuv420p', trozo],
      async stdin => { for (let i = a; i < z; i++) { if (!stdin.write(await toma(p, i / FPS, 'jpeg'))) await new Promise(r => stdin.once('drain', r)); } stdin.end(); });
  }));
  const lista = `${out}.txt`; writeFileSync(lista, trozos.filter(Boolean).map(t => `file '${t.replace(/\\/g, '/')}'`).join('\n'));
  await ffmpeg(['-f', 'concat', '-safe', '0', '-i', lista, '-c', 'copy', out]);
  for (const t of [lista, ...trozos.filter(Boolean)]) rmSync(t);
  console.log(`  ${n} fotogramas en ${PAGINAS} pestañas`);
}
await b.close();
