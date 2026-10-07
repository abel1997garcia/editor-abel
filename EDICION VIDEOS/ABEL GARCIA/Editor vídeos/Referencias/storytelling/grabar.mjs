// Graba historia.html a 30 fps (fotograma a fotograma, cada uno función de t) -> frames/f_0000.png
import { chromium } from 'playwright-core';
import { pathToFileURL } from 'node:url';
import { readdirSync, mkdirSync } from 'node:fs';
const DUR = +(process.argv[2] || 12), FPS = 30;
const base = process.env.LOCALAPPDATA + '/ms-playwright';
const dir = readdirSync(base).find(d => d.startsWith('chromium_headless_shell-'));
const b = await chromium.launch({ executablePath: `${base}/${dir}/chrome-headless-shell-win64/chrome-headless-shell.exe`, args: ['--allow-file-access-from-files'] });
const p = await b.newPage({ viewport: { width: 1920, height: 1080 } });
await p.goto(pathToFileURL(process.cwd() + '/historia.html').href);
await p.waitForFunction(() => document.title === 'listo');
mkdirSync('frames', { recursive: true });
for (let i = 0; i < DUR * FPS; i++) {
  await p.evaluate(t => window.pintar(t), i / FPS);
  await p.screenshot({ path: `frames/f_${String(i).padStart(4, '0')}.png` });
}
await b.close();
