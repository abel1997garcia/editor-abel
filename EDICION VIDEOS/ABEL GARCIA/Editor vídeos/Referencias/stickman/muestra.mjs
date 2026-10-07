// Captura la muestra con dos combinaciones de fondo y tipografía manuscrita
import { chromium } from 'playwright-core';
import { pathToFileURL } from 'node:url';
import { readdirSync } from 'node:fs';

const base = process.env.LOCALAPPDATA + '/ms-playwright';
const dir = readdirSync(base).find(d => d.startsWith('chromium_headless_shell-'));
const exe = `${base}/${dir}/chrome-headless-shell-win64/chrome-headless-shell.exe`;
const b = await chromium.launch({ executablePath: exe, args: ['--allow-file-access-from-files'] });
const p = await b.newPage({ viewport: { width: 1920, height: 1080 } });
await p.goto(pathToFileURL(process.cwd() + '/muestra.html').href);
const variantes = [['A_inkfree_blanco', 'Mano', '#FFFFFF'], ['B_segoeprint_papel', 'Print', '#FAF7F0']];
for (const [nombre, fuente, fondo] of variantes) {
  await p.evaluate(([f, bg]) => { const s = document.getElementById('s'); s.style.setProperty('--f', f); s.style.setProperty('--bg', bg); }, [fuente, fondo]);
  await p.evaluate(() => document.fonts.ready);
  await p.waitForTimeout(300);
  await p.screenshot({ path: `muestra_${nombre}.png` });
}
await b.close();
