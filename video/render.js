// Render video Logika Duit (halaman HTML dengan window.render(t)) jadi MP4 1080x1920.
// Pakai (dari folder repo, dengan server lokal: python3 -m http.server 8080):
//   node video/render.js http://127.0.0.1:8080/video/ep03-gratis-ongkir.html out.mp4
//   node video/render.js <url> <folder> --stills 0,2.5,10      (PNG di detik tertentu, untuk cek cepat)
// Butuh Playwright (Chromium) dan ffmpeg dengan libx264.
const { chromium } = require('playwright');
const { spawn } = require('child_process');
const fs = require('fs');
const path = require('path');

const [url, out] = process.argv.slice(2);
const flag = name => { const i = process.argv.indexOf(name); return i > 0 ? process.argv[i + 1] : null; };
const FPS = +(flag('--fps') || 30);
if (!url || !out) { console.error('pakai: node video/render.js <url> <out.mp4|folder> [--stills 0,1.5] [--fps 30]'); process.exit(1); }

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
  const errors = [];
  page.on('pageerror', e => errors.push(e.message));
  page.on('console', m => { if (m.type() === 'error') errors.push(m.text()); });
  await page.goto(url, { waitUntil: 'networkidle' });
  await page.evaluate(() => window.ready);
  const dur = await page.evaluate(() => window.DURATION);
  const stage = await page.$('#stage');

  const stills = flag('--stills');
  if (stills) {
    fs.mkdirSync(out, { recursive: true });
    for (const t of stills.split(',').map(Number)) {
      await page.evaluate(tt => window.render(tt), t);
      await stage.screenshot({ path: path.join(out, `t${String(t.toFixed(2)).padStart(5, '0')}.png`) });
    }
  } else {
    const ff = spawn('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', String(FPS), '-i', '-',
      '-f', 'lavfi', '-i', 'anullsrc=r=48000:cl=stereo',
      '-map', '0:v', '-map', '1:a', '-shortest',
      '-c:v', 'libx264', '-preset', 'slow', '-crf', '16', '-profile:v', 'high', '-pix_fmt', 'yuv420p', '-r', String(FPS),
      '-c:a', 'aac', '-b:a', '128k', '-movflags', '+faststart', out], { stdio: ['pipe', 'inherit', 'inherit'] });
    const done = new Promise((res, rej) => ff.on('close', c => c === 0 ? res() : rej(new Error('ffmpeg keluar dengan kode ' + c))));
    const n = Math.round(dur * FPS);
    for (let i = 0; i < n; i++) {
      await page.evaluate(tt => window.render(tt), i / FPS);
      const buf = await stage.screenshot({ type: 'png' });
      if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
      if (i % 150 === 0) console.log(`frame ${i}/${n}`);
    }
    ff.stdin.end();
    await done;
  }
  await browser.close();
  if (errors.length) { console.error('Error di halaman:\n' + errors.join('\n')); process.exit(1); }
  console.log('selesai:', out);
})();
