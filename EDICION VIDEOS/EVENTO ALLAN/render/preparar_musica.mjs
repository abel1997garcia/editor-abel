// Adapta una pista para el fondo del vídeo: más lenta, más cálida y con más espacio (reverb suave).
//
//   node render/preparar_musica.mjs "C:\ruta\a\pista.mp3"            → audio/musica.mp3
//   node render/preparar_musica.mjs pista.mp3 --lento=0.88 --eco=0.4   (opcional: ajustar)
//
// --lento : velocidad (1 = original, 0.9 = 10 % más lenta; el tono no cambia)
// --eco   : cantidad de reverb (0 = nada, 0.3 suave, 0.6 mucha)
import { spawn } from 'node:child_process';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
let ffmpegStatic = null;
try { ffmpegStatic = (await import('ffmpeg-static')).default; } catch { /* usa el ffmpeg del sistema */ }
const FFMPEG = process.env.FFMPEG || ffmpegStatic || 'ffmpeg';
const src = process.argv[2];
if (!src) { console.log('Uso: node render/preparar_musica.mjs <pista.mp3> [--lento=0.9] [--eco=0.3]'); process.exit(1); }
const arg = (k, d) => { const a = process.argv.find(x => x.startsWith(`--${k}=`)); return a ? +a.split('=')[1] : d; };
const lento = arg('lento', 0.9), eco = arg('eco', 0.3);
const out = path.join(ROOT, 'audio', 'musica.mp3');

const f = [
  'aresample=48000', 'aformat=channel_layouts=stereo',
  `atempo=${lento}`,                                   // más lenta sin cambiar el tono
  'highpass=f=40', 'lowpass=f=11000',                  // quita graves sucios y agudos chillones
  'equalizer=f=250:t=q:w=1:g=2',                       // un poco más de calidez
  'equalizer=f=3000:t=q:w=1.2:g=-2',                   // deja hueco a la voz de Allan
  `aecho=0.8:0.88:${[90, 170, 260].join('|')}:${[eco, eco * 0.7, eco * 0.45].map(x => x.toFixed(2)).join('|')}`,
  'stereotools=mlev=1:slev=1.25',                      // más amplitud estéreo
  'loudnorm=I=-18:TP=-2:LRA=9',
  'afade=t=in:d=4',
].join(',');

const p = spawn(FFMPEG, ['-hide_banner', '-loglevel', 'error', '-y', '-i', src, '-af', f, '-c:a', 'libmp3lame', '-b:a', '256k', out], { stdio: 'inherit' });
p.on('close', c => {
  if (c === 0) console.log(`Música preparada → ${out}\n(velocidad ${lento}, reverb ${eco}). Ahora: npm run render`);
  else { console.error('ffmpeg falló preparando la música'); process.exit(1); }
});
