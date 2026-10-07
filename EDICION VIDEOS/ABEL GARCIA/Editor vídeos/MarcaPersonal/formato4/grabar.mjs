// Graba el dibujo fotograma a fotograma: node grabar.mjs <html> <segundos> <salida.mp4>
import { chromium } from 'playwright-core';
import { pathToFileURL } from 'node:url';
import { readdirSync } from 'node:fs';
import { spawn } from 'node:child_process';
const [,, html, dur, out] = process.argv, FPS = 30;
const base = process.env.LOCALAPPDATA + '/ms-playwright', dir = readdirSync(base).find(d => d.startsWith('chromium_headless_shell-'));
const b = await chromium.launch({ executablePath: `${base}/${dir}/chrome-headless-shell-win64/chrome-headless-shell.exe`, args: ['--allow-file-access-from-files'] });
const p = await b.newPage({ viewport: { width: 1080, height: 960 } });
await p.goto(pathToFileURL(process.cwd() + '/' + html).href); await p.waitForFunction(() => document.title === 'listo');
const ff = spawn('ffmpeg', ['-v', 'error', '-y', '-f', 'image2pipe', '-framerate', String(FPS), '-c:v', 'png', '-i', '-', '-c:v', 'libx264', '-crf', '14', '-preset', 'veryfast', '-pix_fmt', 'yuv420p', out], { stdio: ['pipe', 'inherit', 'inherit'] });
for (let i = 0; i < Math.round(+dur * FPS); i++) {
  await p.evaluate(t => window.pintar(t), i / FPS);
  const buf = await p.screenshot({ type: 'png', clip: { x: 0, y: 0, width: 1080, height: 960 } });
  if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
}
ff.stdin.end(); await new Promise(r => ff.on('close', r)); await b.close();
