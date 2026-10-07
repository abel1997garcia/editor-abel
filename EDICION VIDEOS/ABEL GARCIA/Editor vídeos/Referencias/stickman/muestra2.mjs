// Captura la muestra 2: escena y personaje
import { chromium } from 'playwright-core';
import { pathToFileURL } from 'node:url';
import { readdirSync } from 'node:fs';

const base = process.env.LOCALAPPDATA + '/ms-playwright';
const dir = readdirSync(base).find(d => d.startsWith('chromium_headless_shell-'));
const b = await chromium.launch({ executablePath: `${base}/${dir}/chrome-headless-shell-win64/chrome-headless-shell.exe`, args: ['--allow-file-access-from-files'] });
const p = await b.newPage({ viewport: { width: 1920, height: 1080 } });
p.on('console', m => console.log('consola:', m.text()));
await p.goto(pathToFileURL(process.cwd() + '/muestra2.html').href);
await p.waitForFunction(() => document.title === 'listo');
await p.waitForTimeout(300);
await (await p.$('#escena')).screenshot({ path: 'muestra2_escena.png' });
await (await p.$('#pers')).screenshot({ path: 'muestra2_personaje.png' });
await b.close();
