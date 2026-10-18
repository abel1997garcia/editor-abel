// Render del vídeo de presentación de Allan, pensado para hacerlo en tu ordenador.
//
//   node render/render_local.mjs                 → versión CON los 3 momentos de sesión real
//   node render/render_local.mjs --prueba=0      → versión SIN ellos
//   node render/render_local.mjs --workers=6     → más procesos en paralelo (por defecto: núcleos - 1)
//   node render/render_local.mjs --desde=140 --hasta=180   → solo un tramo, para revisar
//
// Música: si existe audio/musica.mp3 se mezcla debajo de la voz y baja sola cuando Allan habla.
// Resultado: salida/Allan_Garcia_evento[_sin_prueba].mp4  (1920×1080, 30 fps)
import { chromium } from 'playwright';
import { spawn } from 'node:child_process';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const arg = (k, d) => { const a = process.argv.find(x => x.startsWith(`--${k}=`)); return a ? a.split('=')[1] : d; };
const CON = arg('prueba', '1') !== '0';
const WORKERS = Math.max(1, +arg('workers', Math.max(1, os.cpus().length - 1)));
const FPS = 30;
let ffmpegStatic = null;
try { ffmpegStatic = (await import('ffmpeg-static')).default; } catch { /* usa el ffmpeg del sistema */ }
const FFMPEG = process.env.FFMPEG || ffmpegStatic || 'ffmpeg';
const OUTDIR = path.join(ROOT, 'salida'), TMP = path.join(OUTDIR, 'tmp');
fs.mkdirSync(TMP, { recursive: true });
const NAME = CON ? 'Allan_Garcia_evento' : 'Allan_Garcia_evento_sin_prueba';
const url = pathToFileURL(path.join(ROOT, 'presentacion.html')).href + (CON ? '' : '?prueba=0');

function run(args, label) {
  return new Promise((res, rej) => {
    const p = spawn(FFMPEG, ['-hide_banner', '-loglevel', 'error', '-y', ...args], { stdio: ['ignore', 'inherit', 'inherit'] });
    p.on('close', c => c === 0 ? res() : rej(new Error(`ffmpeg falló en: ${label}`)));
  });
}

async function openPage(browser) {
  const p = await browser.newPage({ viewport: { width: 1920, height: 1080 } });
  await p.goto(url);
  await p.evaluate(() => window.fontsReady);
  await p.evaluate(() => document.getElementById('start')?.remove());
  return p;
}

// ---------- 1. fotogramas (en paralelo, cada proceso un tramo) ----------
async function renderPart(browser, i, f0, f1, onFrame) {
  const page = await openPage(browser);
  const out = path.join(TMP, `parte_${String(i).padStart(2, '0')}.mp4`);
  const ff = spawn(FFMPEG, ['-hide_banner', '-loglevel', 'error', '-y', '-f', 'image2pipe', '-framerate', String(FPS), '-c:v', 'mjpeg', '-i', '-',
    '-c:v', 'libx264', '-preset', 'medium', '-crf', '17', '-pix_fmt', 'yuv420p', '-r', String(FPS), out], { stdio: ['pipe', 'inherit', 'inherit'] });
  for (let f = f0; f < f1; f++) {
    // JPEG del canvas directamente (más rápido que una captura de pantalla)
    const b64 = await page.evaluate(async t => {
      await window.prepareFrame(t); window.renderFrame(t);
      return document.getElementById('c').toDataURL('image/jpeg', 0.93).split(',')[1];
    }, f / FPS);
    if (!ff.stdin.write(Buffer.from(b64, 'base64'))) await new Promise(r => ff.stdin.once('drain', r));
    onFrame();
  }
  ff.stdin.end();
  await new Promise(r => ff.on('close', r));
  await page.close();
  return out;
}

// ---------- 2. audio: voz limpia + clips de sesión + música con ducking ----------
async function buildAudio(plan, out, desde, hasta) {
  const A = f => path.join(ROOT, 'audio', f);
  const L = -plan.LEAD, cut = plan.cutV, V = plan.V, DUR = plan.DUR;
  const p2 = cut - L + V;
  const inputs = ['-i', A('voz_allan.mp3')];
  const clips = CON ? ['m1_cocina.wav', 'm2_peluche.wav', 'm3_athletic.wav'] : [];
  clips.forEach(c => inputs.push('-i', A(c)));
  const hasMusic = fs.existsSync(A('musica.mp3'));
  if (hasMusic) inputs.push('-stream_loop', '-1', '-i', A('musica.mp3'));
  let f = `[0:a]aresample=48000,aformat=channel_layouts=stereo,highpass=f=80,afftdn=nf=-25,loudnorm=I=-16:TP=-1.5:LRA=11,asplit=2[va][vb];`
        + `[va]atrim=${L}:${cut},asetpts=PTS-STARTPTS,afade=t=out:st=${(cut - L - 0.15).toFixed(3)}:d=0.15[v1];`
        + `[vb]atrim=start=${cut},asetpts=PTS-STARTPTS,afade=t=in:d=0.1,adelay=${Math.round(p2 * 1000)}:all=1[v2];`;
  const voices = ['[v1]', '[v2]'];
  clips.forEach((c, i) => {
    const st = Math.round(plan.clip_starts[i] * 1000);
    f += `[${i + 1}:a]aresample=48000,aformat=channel_layouts=stereo,loudnorm=I=-17:TP=-1.5,afade=t=in:d=0.08,areverse,afade=t=in:d=0.12,areverse,adelay=${st}:all=1[c${i}];`;
    voices.push(`[c${i}]`);
  });
  f += `${voices.join('')}amix=inputs=${voices.length}:normalize=0:duration=longest[voz]`;
  // paso 1: voz + clips → voz.wav (rellenado con silencio hasta el final del vídeo)
  const voz = path.join(TMP, 'voz.wav');
  fs.writeFileSync(path.join(TMP, 'filtro_audio.txt'), [...inputs, '-filter_complex', f].join('\n'));
  await run([...inputs, '-filter_complex', f, '-map', '[voz]', '-ar', '48000', '-c:a', 'pcm_s16le', path.join(TMP, 'voz_sin_relleno.wav')], 'audio voz');
  await run(['-i', path.join(TMP, 'voz_sin_relleno.wav'), '-af', 'apad', '-t', String(DUR), '-c:a', 'pcm_s16le', voz], 'relleno voz');
  // paso 2: música debajo, que baja sola cuando hay voz (sidechain), con fundidos
  let g, ins = ['-i', voz];
  if (hasMusic) {
    ins.push('-stream_loop', '-1', '-i', A('musica.mp3'));
    g = `[0:a]asplit=2[vz1][vz2];`
      + `[1:a]aresample=48000,aformat=channel_layouts=stereo,atrim=0:${DUR},asetpts=PTS-STARTPTS,volume=0.32[mus];`
      + `[mus][vz2]sidechaincompress=threshold=0.02:ratio=8:attack=30:release=600:makeup=1[musd];`
      + `[musd]afade=t=in:d=3,afade=t=out:st=${(DUR - 5).toFixed(2)}:d=5[mf];`
      + `[vz1][mf]amix=inputs=2:normalize=0:duration=first,alimiter=limit=0.95[mix];`;
  } else g = `[0:a]anull[mix];`;
  g += `[mix]atrim=${desde}:${hasta},asetpts=PTS-STARTPTS,afade=t=out:st=${Math.max(0, hasta - desde - 1.5).toFixed(2)}:d=1.5[out]`;
  await run([...ins, '-filter_complex', g, '-map', '[out]', '-ar', '48000', '-c:a', 'pcm_s16le', out], 'audio final');
  return hasMusic;
}

// ---------- principal ----------
const t0 = Date.now();
const browser = await chromium.launch({ args: ['--allow-file-access-from-files', '--disable-gpu-sandbox'] });
const probe = await openPage(browser);
const { DUR, plan } = await probe.evaluate(() => ({ DUR: window.DUR, plan: window.PLAN }));
await probe.close();
const desde = +arg('desde', 0), hasta = Math.min(+arg('hasta', DUR), DUR);
const F0 = Math.round(desde * FPS), F1 = Math.round(hasta * FPS), N = F1 - F0;
console.log(`Versión ${CON ? 'CON' : 'SIN'} sesiones reales · ${(hasta - desde).toFixed(1)} s · ${N} fotogramas · ${WORKERS} procesos`);

let done = 0, last = 0;
const tick = () => { done++; const pct = Math.floor(done / N * 100); if (pct !== last) { last = pct; const el = (Date.now() - t0) / 1000; process.stdout.write(`\r  fotogramas ${pct}% · faltan ~${Math.round(el / done * (N - done) / 60)} min   `); } };
const per = Math.ceil(N / WORKERS);
const parts = await Promise.all(Array.from({ length: WORKERS }, (_, i) => {
  const a = F0 + i * per, b = Math.min(F1, a + per);
  return a < b ? renderPart(browser, i, a, b, tick) : null;
})).then(r => r.filter(Boolean));
await browser.close();
console.log('\n  uniendo tramos…');
const list = path.join(TMP, 'lista.txt');
fs.writeFileSync(list, parts.map(p => `file '${p.replace(/\\/g, '/')}'`).join('\n'));
const mudo = path.join(TMP, 'video_mudo.mp4');
await run(['-f', 'concat', '-safe', '0', '-i', list, '-c', 'copy', mudo], 'unir tramos');

console.log('  mezclando audio…');
const wav = path.join(TMP, 'audio.wav');
const music = await buildAudio(plan, wav, desde, hasta);
const tramo = desde > 0 || hasta < DUR ? `_tramo_${Math.round(desde)}-${Math.round(hasta)}` : '';
const final = path.join(OUTDIR, `${NAME}${tramo}.mp4`);
await run(['-i', mudo, '-i', wav, '-map', '0:v', '-map', '1:a', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '256k', '-shortest', '-movflags', '+faststart', final], 'unir vídeo y audio');
console.log(`\nListo en ${Math.round((Date.now() - t0) / 60000)} min → ${final}`);
console.log(music ? 'Con música de fondo (audio/musica.mp3).' : 'Sin música: pon tu pista en audio/musica.mp3 y vuelve a lanzarlo.');
