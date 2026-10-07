// Captura las dos escenas de la muestra 3
import { chromium } from 'playwright-core';
import { pathToFileURL } from 'node:url';
import { readdirSync } from 'node:fs';
const base = process.env.LOCALAPPDATA + '/ms-playwright';
const dir = readdirSync(base).find(d => d.startsWith('chromium_headless_shell-'));
const b = await chromium.launch({ executablePath: `${base}/${dir}/chrome-headless-shell-win64/chrome-headless-shell.exe`, args: ['--allow-file-access-from-files'] });
const p = await b.newPage({ viewport: { width: 1920, height: 1080 } });
p.on('console', m => console.log(m.text()));
await p.goto(pathToFileURL(process.cwd() + '/muestra3.html').href);
await p.waitForFunction(() => document.title === 'listo');
await p.waitForTimeout(200);
await (await p.$('#e1')).screenshot({ path: 'muestra3_intencion.png' });
await (await p.$('#e2')).screenshot({ path: 'muestra3_iceberg.png' });
await b.close();
