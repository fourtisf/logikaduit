// Render video Logika Duit (halaman HTML dengan window.render(t)) jadi MP4 1080x1920.
// Pakai (dari folder repo, dengan server lokal: python3 -m http.server 8080):
//   node video/render.js http://127.0.0.1:8080/video/ep03-gratis-ongkir.html out.mp4
//   node video/render.js <url> <folder> --stills 0,2.5,10      (PNG di detik tertentu, untuk cek cepat)
// Opsi:
//   --jobs 3          render beberapa bagian sekaligus (lebih cepat di mesin multi-core), lalu digabung
//   --warp warp.json  ubah tempo: {"duration": D, "anchors": [[detik_asli, detik_baru], ...]}
//                     dipakai supaya animasi pas dengan voice over (dibuat oleh ep03-mix.py)
// Butuh Playwright (Chromium) dan ffmpeg dengan libx264.
const { chromium } = require('playwright');
const { spawn, execFileSync } = require('child_process');
const fs = require('fs');
const os = require('os');
const path = require('path');

const [url, out] = process.argv.slice(2);
const flag = name => { const i = process.argv.indexOf(name); return i > 0 ? process.argv[i + 1] : null; };
const FPS = +(flag('--fps') || 30);
const JOBS = Math.max(1, +(flag('--jobs') || 1));
if (!url || !out) { console.error('pakai: node video/render.js <url> <out.mp4|folder> [--stills 0,1.5] [--fps 30] [--jobs 3] [--warp warp.json]'); process.exit(1); }

// waktu baru -> waktu asli di timeline HTML (linear per potongan)
const warp = flag('--warp') ? JSON.parse(fs.readFileSync(flag('--warp'), 'utf8')) : null;
function toOrig(t) {
  if (!warp) return t;
  const a = warp.anchors;
  if (t <= a[0][1]) return a[0][0] + (t - a[0][1]);
  for (let i = 1; i < a.length; i++) if (t <= a[i][1]) {
    const [o0, n0] = a[i - 1], [o1, n1] = a[i];
    return o0 + (o1 - o0) * (t - n0) / (n1 - n0);
  }
  const [o, n] = a[a.length - 1]; return o + (t - n);
}

async function openPage(browser, errors) {
  const page = await browser.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
  page.on('pageerror', e => errors.push(e.message));
  page.on('console', m => { if (m.type() === 'error') errors.push(m.text()); });
  await page.goto(url, { waitUntil: 'networkidle' });
  await page.evaluate(() => window.ready);
  return page;
}

// render frame [from, to) ke satu file MP4 (tanpa audio)
async function renderRange(browser, errors, from, to, file, label) {
  const page = await openPage(browser, errors);
  const stage = await page.$('#stage');
  const ff = spawn('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', String(FPS), '-i', '-',
    '-c:v', 'libx264', '-preset', JOBS > 1 ? 'medium' : 'slow', '-crf', '16', '-profile:v', 'high', '-pix_fmt', 'yuv420p',
    '-r', String(FPS), '-g', String(FPS * 2), file], { stdio: ['pipe', 'inherit', 'inherit'] });
  const done = new Promise((res, rej) => ff.on('close', c => c === 0 ? res() : rej(new Error('ffmpeg keluar dengan kode ' + c))));
  for (let i = from; i < to; i++) {
    await page.evaluate(tt => window.render(tt), toOrig(i / FPS));
    const buf = await stage.screenshot({ type: 'png' });
    if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
    if ((i - from) % 150 === 0) console.log(`${label}: frame ${i - from}/${to - from}`);
  }
  ff.stdin.end();
  await done;
  await page.close();
}

(async () => {
  const browser = await chromium.launch();
  const errors = [];
  const stills = flag('--stills');
  if (stills) {
    const page = await openPage(browser, errors);
    const stage = await page.$('#stage');
    fs.mkdirSync(out, { recursive: true });
    for (const t of stills.split(',').map(Number)) {
      await page.evaluate(tt => window.render(tt), toOrig(t));
      await stage.screenshot({ path: path.join(out, `t${String(t.toFixed(2)).padStart(5, '0')}.png`) });
    }
  } else {
    const probe = await openPage(browser, errors);
    const dur = warp ? warp.duration : await probe.evaluate(() => window.DURATION);
    await probe.close();
    const n = Math.round(dur * FPS);
    const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'ld-render-'));
    const per = Math.ceil(n / JOBS);
    const parts = [];
    const jobs = [];
    for (let j = 0; j < JOBS; j++) {
      const from = j * per, to = Math.min(n, from + per);
      if (from >= to) break;
      const file = path.join(tmp, `part${j}.mp4`);
      parts.push(file);
      jobs.push(renderRange(browser, errors, from, to, file, `bagian ${j + 1}/${JOBS}`));
    }
    await Promise.all(jobs);
    // gabung bagian video, lalu tambahkan jalur audio kosong (suara ditambahkan terpisah)
    fs.writeFileSync(path.join(tmp, 'list.txt'), parts.map(p => `file '${p}'`).join('\n'));
    execFileSync('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', path.join(tmp, 'list.txt'),
      '-f', 'lavfi', '-i', 'anullsrc=r=48000:cl=stereo', '-map', '0:v', '-map', '1:a', '-shortest',
      '-c:v', 'copy', '-c:a', 'aac', '-b:a', '128k', '-movflags', '+faststart', out]);
    fs.rmSync(tmp, { recursive: true, force: true });
  }
  await browser.close();
  if (errors.length) { console.error('Error di halaman:\n' + errors.join('\n')); process.exit(1); }
  console.log('selesai:', out);
})();
