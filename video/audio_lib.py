# Bahan bersama untuk musik dan efek suara video Logika Duit: instrumen, efek, reverb, dan penulisan WAV.
# Semua bunyi disintesis dengan numpy, jadi bebas hak cipta. Dipakai oleh ep03-audio.py, ep04-audio.py, dst.
# Urutan pemanggilan menentukan hasil acak (rng bersama), jadi hasil tiap episode selalu sama persis.
import json
import os
import wave
import numpy as np

SR = 48000
rng = np.random.default_rng(3)


def _interp(t, xs, ys):
    if t <= xs[0]:
        return ys[0] + (t - xs[0])
    if t >= xs[-1]:
        return ys[-1] + (t - xs[-1])
    return float(np.interp(t, xs, ys))


def timeline(dur, warp_path=None):
    """(W, Winv, durasi). W: waktu di timeline asli HTML -> waktu di video akhir; Winv kebalikannya.
    warp.json (dari mix.py) menggeser semua waktu supaya cocok dengan video yang temponya disesuaikan voice over."""
    if not warp_path:
        return (lambda t: t), (lambda t: t), dur
    w = json.load(open(warp_path))
    xs = np.array([a[0] for a in w['anchors']], float)
    ys = np.array([a[1] for a in w['anchors']], float)
    return (lambda t: _interp(t, xs, ys)), (lambda t: _interp(t, ys, xs)), float(w['duration'])


def T(d):
    return np.arange(int(d * SR)) / SR


def mtof(m):
    return 440.0 * 2 ** ((m - 69) / 12)


def fade_tail(x, ms=40):
    n = min(len(x), int(SR * ms / 1000))
    if n > 0:
        x[-n:] *= np.linspace(1, 0, n)
    return x


def place(buf, start, sig, gain=1.0, pan=0.0):
    """Tambahkan sinyal mono/stereo ke buffer stereo pada detik `start` (pan -1 kiri .. 1 kanan)."""
    i = int(round(start * SR))
    if i >= len(buf):
        return
    if sig.ndim == 1:
        a = (pan + 1) * np.pi / 4
        sig = np.stack([sig * np.cos(a), sig * np.sin(a)], 1) * np.sqrt(2)
    j0 = max(0, -i)
    n = min(len(sig) - j0, len(buf) - max(i, 0))
    if n > 0:
        buf[max(i, 0):max(i, 0) + n] += sig[j0:j0 + n] * gain


def fft_band(x, lo=None, hi=None, soft=0.25):
    """Filter frekuensi lewat FFT (untuk bunyi pendek): lo = highpass, hi = lowpass, Hz."""
    X = np.fft.rfft(x)
    f = np.fft.rfftfreq(len(x), 1 / SR)
    m = np.ones_like(f)
    if lo:
        m *= 1 / (1 + (lo / np.maximum(f, 1)) ** (2 / soft))
    if hi:
        m *= 1 / (1 + (f / hi) ** (2 / soft))
    return np.fft.irfft(X * m, len(x))


def sweep_filter(x, cut_from, cut_to, kind='lp', seg=2048):
    """Filter yang frekuensinya bergeser (whoosh, riser): overlap-add per potongan."""
    out = np.zeros(len(x) + seg)
    win = np.hanning(seg)
    hop = seg // 2
    f = np.fft.rfftfreq(seg, 1 / SR)
    nseg = max(1, (len(x) - seg) // hop + 1)
    for k in range(nseg + 1):
        a = k * hop
        chunk = np.zeros(seg)
        part = x[a:a + seg]
        chunk[:len(part)] = part
        p = min(1, a / max(1, len(x) - seg))
        c = cut_from * (cut_to / cut_from) ** p
        m = 1 / (1 + (f / c) ** 4) if kind == 'lp' else np.exp(-0.5 * ((np.log2(np.maximum(f, 1) / c)) / 0.7) ** 2)
        out[a:a + seg] += np.fft.irfft(np.fft.rfft(chunk * win) * m, seg)
    return out[:len(x)]


def reverb(st, seconds=2.2, mix=1.0):
    """Reverb konvolusi sederhana dengan respons impuls dari noise yang meluruh (stereo lebar)."""
    n = int(seconds * SR)
    t = np.arange(n) / SR
    ir = rng.standard_normal((n, 2)) * np.exp(-t / (seconds / 6.5))[:, None]
    ir[:, 0] = fft_band(ir[:, 0], lo=180, hi=7000)
    ir[:, 1] = fft_band(ir[:, 1], lo=180, hi=7000)
    ir /= np.sqrt((ir ** 2).sum(0))
    L = 1 << int(np.ceil(np.log2(len(st) + n)))
    out = np.zeros_like(st)
    for ch in range(2):
        y = np.fft.irfft(np.fft.rfft(st[:, ch], L) * np.fft.rfft(ir[:, ch], L), L)
        out[:, ch] = y[:len(st)]
    return out * mix


# ---------------- instrumen ----------------
def rhodes(f, d, vel=1.0):
    """Electric piano FM (mirip Rhodes), sedikit chorus kiri-kanan."""
    t = T(d)
    out = []
    for det in (0.9985, 1.0015):
        ff = f * det
        idx = 1.6 * vel * np.exp(-t / 0.3) + 0.2
        car = np.sin(2 * np.pi * ff * t + idx * np.sin(2 * np.pi * ff * t))
        tine = 0.12 * np.sin(2 * np.pi * ff * 7.0 * t) * np.exp(-t / 0.04)
        out.append((car + tine) * np.exp(-t / 1.7) * np.clip(t / 0.004, 0, 1))
    return np.stack([fade_tail(o) for o in out], 1) * vel


def bell(f, d=1.6, vel=1.0, ratio=3.5):
    t = T(d)
    idx = 2.2 * np.exp(-t / 0.25)
    s = np.sin(2 * np.pi * f * t + idx * np.sin(2 * np.pi * f * ratio * t))
    return fade_tail(s * np.exp(-t / (d / 3.2)) * np.clip(t / 0.002, 0, 1) * vel)


def pad(notes, d, vel=1.0):
    t = T(d)
    s = np.zeros((len(t), 2))
    for m in notes:
        for ch, det in enumerate((0.996, 1.004)):
            f = mtof(m) * det
            for h in range(1, 9):          # gergaji lembut, harmonik terbatas
                s[:, ch] += np.sin(2 * np.pi * f * h * t + h) / h ** 1.6
    env = np.clip(t / 0.9, 0, 1) * np.clip((d - t) / 0.9, 0, 1)
    return s * env[:, None] * vel / len(notes)


def bass(f, d, vel=1.0):
    t = T(d)
    s = np.sin(2 * np.pi * f * t) + 0.25 * np.sin(2 * np.pi * 2 * f * t)
    s = np.tanh(1.6 * s) * np.clip(t / 0.01, 0, 1) * np.exp(-t / 1.2)
    return fade_tail(s * vel, 30)


def kick(vel=1.0, low=45, d=0.45):
    t = T(d)
    f = low + 85 * np.exp(-t / 0.03)
    ph = 2 * np.pi * np.cumsum(f) / SR
    s = np.sin(ph) * np.exp(-t / 0.22) + 0.3 * fft_band(rng.standard_normal(len(t)), lo=2000) * np.exp(-t / 0.004)
    return fade_tail(np.tanh(1.5 * s) * vel)


def snare(vel=1.0):
    t = T(0.35)
    n = fft_band(rng.standard_normal(len(t)), lo=900, hi=9000) * np.exp(-t / 0.11)
    tone = np.sin(2 * np.pi * 190 * t) * np.exp(-t / 0.05)
    return fade_tail((0.8 * n + 0.6 * tone) * vel)


def hat(vel=1.0, open_=False):
    d = 0.35 if open_ else 0.08
    t = T(d)
    s = fft_band(rng.standard_normal(len(t)), lo=7000, hi=15000) * np.exp(-t / (0.12 if open_ else 0.025))
    return fade_tail(s * vel, 10)


# ---------------- efek suara ----------------
def whoosh(d=0.55, up=True, vel=1.0):
    t = T(d)
    n = rng.standard_normal(len(t))
    env = np.sin(np.pi * np.clip(t / d, 0, 1)) ** 2
    s = sweep_filter(n, 400 if up else 5000, 5000 if up else 400, kind='bp')
    return s * env * vel / (np.abs(s).max() + 1e-9)


def impact(vel=1.0, low=36, d=1.2):
    t = T(d)
    f = low + 60 * np.exp(-t / 0.05)
    boom = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.35)
    crash = fft_band(rng.standard_normal(len(t)), hi=3000) * np.exp(-t / 0.15) * .5
    return fade_tail(np.tanh(1.8 * (boom + crash)) * vel)


def tap(vel=1.0):
    t = T(0.06)
    return fade_tail((np.sin(2 * np.pi * 1700 * t) * np.exp(-t / 0.012) + fft_band(rng.standard_normal(len(t)), lo=3000) * np.exp(-t / 0.003) * .6) * vel, 5)


def pop(f0=420, f1=980, d=0.12, vel=1.0):
    t = T(d)
    f = f0 + (f1 - f0) * np.clip(t / (d * .6), 0, 1)
    return fade_tail(np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / (d / 2.5)) * vel, 8)


def tick(f=2600, vel=1.0):
    t = T(0.03)
    return fade_tail(np.sin(2 * np.pi * f * t) * np.exp(-t / 0.006) * vel, 4)


def riser(d=2.0, vel=1.0):
    t = T(d)
    n = sweep_filter(rng.standard_normal(len(t)), 300, 9000, kind='lp')
    n /= np.abs(n).max() + 1e-9
    tone = np.sin(2 * np.pi * np.cumsum(200 + 600 * (t / d) ** 2) / SR) * .25
    return (n * .7 + tone) * (t / d) ** 2.2 * vel


def write_wav(path, x):
    x = x / (np.abs(x).max() + 1e-9) * 0.89
    x[:int(.003 * SR)] *= np.linspace(0, 1, int(.003 * SR))[:, None]   # cegah bunyi "klik" di sampel pertama
    pcm = (np.clip(x, -1, 1) * 32767).astype('<i2')
    with wave.open(path, 'wb') as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(pcm.tobytes())


def save(out, music, sfx):
    """Tulis music.wav (dengan saturasi halus ala tape) dan sfx.wav ke folder out."""
    os.makedirs(out, exist_ok=True)
    m = np.tanh(1.3 * music / (np.abs(music).max() + 1e-9)) / np.tanh(1.3)
    write_wav(os.path.join(out, 'music.wav'), m)
    write_wav(os.path.join(out, 'sfx.wav'), sfx)
    print('selesai:', out)
