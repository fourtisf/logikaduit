# Musik latar dan efek suara original untuk video EP3 (gratis ongkir). Semua disintesis di sini,
# jadi bebas hak cipta. Waktu efek suara mengikuti timeline di ep03-gratis-ongkir.html.
# Pakai: python3 video/ep03-audio.py <folder-output> [warp.json]   -> music.wav dan sfx.wav (48 kHz, stereo)
# warp.json (dari ep03-mix.py) menggeser semua waktu supaya cocok dengan video yang temponya disesuaikan voice over.
import sys, os, wave, json
import numpy as np

SR = 48000
DUR = 42.0
N = int(SR * DUR)
BPM = 60 / 0.55          # satu ketukan 0,55 detik, satu bar 2,2 detik: twist di detik 2,2 jatuh tepat di awal bar
BEAT = 0.55
BAR = 4 * BEAT
rng = np.random.default_rng(3)
WARP = None              # (detik_asli, detik_baru) dari warp.json; None = timeline asli


def _interp(t, xs, ys):
    if t <= xs[0]:
        return ys[0] + (t - xs[0])
    if t >= xs[-1]:
        return ys[-1] + (t - xs[-1])
    return float(np.interp(t, xs, ys))


def W(t):
    """Waktu di timeline asli HTML -> waktu di video akhir."""
    return t if WARP is None else _interp(t, WARP[0], WARP[1])


def Winv(t):
    """Waktu di video akhir -> waktu di timeline asli."""
    return t if WARP is None else _interp(t, WARP[1], WARP[0])


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


# ---------------- aransemen musik ----------------
CHORDS = {   # (bass, nada akor)
    'Fmaj9': (41, [57, 60, 64, 67]), 'G6': (43, [59, 62, 64, 67]),
    'Em7': (40, [55, 59, 62, 64]), 'Am9': (45, [55, 59, 60, 64]), 'Cmaj9': (36, [55, 59, 62, 64]),
}
PROG = ['Fmaj9', 'G6', 'Em7', 'Am9']


def section(t):
    """Intensitas per bagian video."""
    if t < 2.2: return 'hook'          # pertanyaan pembuka
    if t < 7.7: return 'full'          # twist dan perbandingan
    if t < 8.8: return 'drop'          # transisi ke eksperimen
    if t < 15.4: return 'light'        # eksperimen coklat
    if t < 18.6: return 'build'        # harga turun, menuju cap "Gratis"
    if t < 22.0: return 'after'        # setelah cap
    if t < 27.5: return 'full'         # hasil berbalik, persamaan
    if t < 30.8: return 'break'        # efek harga nol
    if t < 37.4: return 'full'         # kembali ke keranjang, tips
    return 'outro'


def music():
    dry = np.zeros((N, 2))
    wet_send = np.zeros((N, 2))
    g0 = W(2.2) - BAR                      # grid bar digeser supaya twist tetap jatuh di awal bar
    b = -1
    while g0 + b * BAR < DUR:
        t0 = g0 + b * BAR
        b += 1
        sec = section(Winv(t0 + 0.01))
        name = PROG[(b - 1) % 4] if sec != 'outro' else ('Fmaj9' if t0 < W(38) else 'Cmaj9')
        root, notes = CHORDS[name]
        # piano: pukulan di ketukan 1, "and" ketukan 2, dan ketukan 4
        if sec not in ('break', 'outro'):
            hits = [(0, 1.5, .9), (1.5, 1.5, .55), (3, 1.0, .65)] if sec != 'drop' else [(0, 4, .7)]
            for beat, ln, v in hits:
                for k, m in enumerate(notes):
                    s = rhodes(mtof(m), ln * BEAT + .25, v * (0.9 if k else 1.0))
                    place(dry, t0 + beat * BEAT + .006 * k, s, .21)
                    place(wet_send, t0 + beat * BEAT + .006 * k, s, .05)
        # bass
        if sec in ('full', 'build', 'after', 'light', 'hook'):
            v = {'full': 1, 'build': 1, 'after': .7, 'light': .55, 'hook': .8}[sec]
            for beat, ln, oc in [(0, 1.25, 0), (1.75, .5, 0), (2.5, 1.0, 0), (3.5, .45, 12)]:
                place(dry, t0 + beat * BEAT, bass(mtof(root + oc), ln * BEAT, v), .30)
        # drum
        for i in range(8):                 # hi-hat 1/8 dengan swing
            pos = (i // 2) + (0.58 if i % 2 else 0)
            tt = t0 + pos * BEAT
            s = section(Winv(tt))
            if s in ('drop', 'break', 'outro'):
                continue
            v = (.7 if i % 2 == 0 else .42) * {'light': .7, 'hook': .8}.get(s, 1)
            place(dry, tt, hat(v, open_=(i == 7 and s == 'full')), .22, pan=.25)
        for beat in (0, 1.75, 2.5):
            tt = t0 + beat * BEAT
            s = section(Winv(tt))
            if s in ('full', 'hook', 'build') or (s in ('light', 'after') and beat == 0):
                place(dry, tt, kick(.9 if beat == 0 else .6), .42 if s != 'light' else .28)
        for beat in (1, 3):
            tt = t0 + beat * BEAT
            s = section(Winv(tt))
            if s in ('full', 'build'):
                sn = snare(.8)
                place(dry, tt, sn, .3, pan=-.1)
                place(wet_send, tt, sn, .06)
    # drum roll menjelang cap "Gratis" (17,6 - 18,6 detik), makin rapat
    r0, r1 = W(17.6), W(18.55)
    tt = r0
    while tt < r1:
        p = (tt - r0) / (r1 - r0)
        place(dry, tt, snare(.35 + .5 * p), .22, pan=-.1)
        tt += 0.14 * (1 - .65 * p) * (r1 - r0) / 0.95
    # melodi lonceng saat eksperimen (rasa penasaran)
    for tt, m in [(8.8, 76), (9.35, 79), (9.9, 81), (10.45, 79), (11.0, 76), (12.1, 74), (12.65, 76), (13.2, 79),
                  (14.3, 84), (14.85, 83)]:
        s = bell(mtof(m), 1.4, .5)
        place(dry, W(tt), s, .10, pan=.3)
        place(wet_send, W(tt), s, .12)
    # breakdown "efek harga nol": pad + kilau
    pd = pad([57, 60, 64, 67, 71], W(31.3) - W(27.4), 1.0)
    place(dry, W(27.4), pd, .5)
    place(wet_send, W(27.4), pd, .25)
    for k, (tt, m) in enumerate([(27.7, 88), (28.2, 84), (28.75, 91), (29.3, 86), (29.9, 88), (30.4, 93)]):
        s = bell(mtof(m), 1.6, .35, ratio=2.0)
        place(wet_send, W(tt), s, .15, pan=(-.5 if k % 2 else .5))
    # penutup: akor Cmaj9 yang berdering
    root, notes = CHORDS['Cmaj9']
    for k, m in enumerate(notes):
        s = rhodes(mtof(m), DUR - W(38.05) + .2, .8)
        place(dry, W(38.05) + .02 * k, s, .2)
        place(wet_send, W(38.05) + .02 * k, s, .12)
    place(dry, W(38.05), bass(mtof(root), 3.0, .9), .3)
    place(dry, W(38.05), pad([48, 55, 59, 62, 64], DUR - W(38.05), .8), .35)
    out = dry + reverb(wet_send, 2.4)
    for ch in range(2):                    # buang sub di bawah 30 Hz (tidak terdengar di HP, hanya makan headroom)
        out[:, ch] = fft_band(out[:, ch], lo=30, soft=.5)
    # transisi lembut di awal (tetap langsung terdengar) dan fade out di akhir
    fade = np.ones(N)
    fade[-int(1.2 * SR):] = np.linspace(1, 0, int(1.2 * SR)) ** 1.5
    return out * fade[:, None]


# ---------------- efek suara (waktu = timeline video) ----------------
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


def sfx():
    s = np.zeros((N, 2))
    wet = np.zeros((N, 2))
    place(s, W(0.0), impact(.55, low=40, d=.9), .5)                # pembuka langsung "berbunyi"
    place(s, W(0.0), whoosh(.45, up=False, vel=.6), .25)
    place(s, W(0.90), tap(), .45, pan=.35)                          # jari menekan "+ Tambah"
    place(s, W(1.05), pop(), .35, pan=.2)                           # barang masuk keranjang
    for k, m in enumerate((84, 88, 91, 96)):                     # gratis ongkir tercapai
        b = bell(mtof(m), 1.0, .8, ratio=2.0)
        place(s, W(1.85) + .065 * k, b, .14, pan=.3)
        place(wet, W(1.85) + .065 * k, b, .1)
    place(s, W(1.7), riser(W(2.2) - W(1.7), .5), .25)
    place(s, W(2.2), impact(1.0), .75)                              # twist
    place(s, W(4.85), whoosh(.5), .3, pan=-.3)                      # kartu perbandingan masuk
    place(s, W(5.0), whoosh(.5), .3, pan=.3)
    for k in range(10):                                         # hitungan +Rp18.000
        place(s, W(5.7) + k * .06, tick(2000 + 90 * k, .7), .25, pan=.1)
    place(s, W(6.0), impact(.7, low=48, d=.8), .45)
    place(s, W(7.75), whoosh(.6, up=False), .3)                     # ke eksperimen
    place(s, W(8.25), whoosh(.5), .28, pan=-.4)
    place(s, W(8.45), whoosh(.5), .28, pan=.4)
    for k in range(14):                                         # 73% / 27%
        place(s, W(13.6) + k * .06, tick(1800 + 70 * k, .6), .22, pan=-.2)
    place(s, W(16.5), riser(W(18.6) - W(16.5), .9), .4)                           # menuju cap "Gratis"
    place(s, W(17.1), pop(950, 520, .16), .35, pan=-.35)            # 15 sen -> 14 sen
    place(s, W(17.5), pop(950, 520, .16), .35, pan=.35)             # 1 sen -> 0 sen
    place(s, W(18.6), impact(1.1, low=34, d=1.4), .9)               # cap "Gratis"
    place(s, W(18.6), fft_band(rng.standard_normal(int(.12 * SR)), lo=400, hi=4000) * np.exp(-T(.12) / .03), .4, pan=.3)
    for k in range(16):                                         # 31% / 69%
        place(s, W(21.6) + k * .06, tick(1600 + 90 * k, .6), .22, pan=.2)
    place(s, W(22.6), bell(mtof(91), 1.2, .7), .12, pan=.3)
    place(s, W(24.6), whoosh(.5), .3)                               # persamaan
    for k, tt in enumerate((W(25.8), W(25.95))):                       # dua angka 14 yang sama
        b = bell(mtof(88), 1.4, .7)
        place(s, tt, b, .13, pan=(-.4 if k == 0 else .4))
        place(wet, tt, b, .1)
    place(s, W(27.0), riser(W(27.6) - W(27.0), .6), .3)                            # angka 0
    place(s, W(27.6), impact(.6, low=30, d=1.6), .5)
    place(s, W(31.0), whoosh(.55), .3)                              # keranjang kembali
    place(s, W(34.05), whoosh(.5), .25)                             # kartu tips
    for k, m in enumerate((79, 86)):
        place(s, W(34.25) + .09 * k, bell(mtof(m), .9, .6, ratio=2.0), .12, pan=.2)
    place(s, W(38.05), impact(.7, low=38, d=1.6), .55)              # logo
    for k, m in enumerate((72, 76, 79, 83, 86)):
        b = bell(mtof(m), 2.4, .6, ratio=2.0)
        place(s, W(38.1) + .05 * k, b, .1, pan=(k - 2) * .2)
        place(wet, W(38.1) + .05 * k, b, .12)
    place(s, W(38.9), pop(380, 820, .14), .25, pan=-.1)          # tombol follow muncul
    place(s, W(40.3), tap(), .5, pan=.15)                        # jari menekan follow
    for k, m in enumerate((79, 84, 88, 91)):                     # berhasil follow
        b = bell(mtof(m), 1.2, .8, ratio=2.0)
        place(s, W(40.42) + .06 * k, b, .13, pan=.2)
        place(wet, W(40.42) + .06 * k, b, .1)
    return s + reverb(wet, 1.8)


def write_wav(path, x):
    x = x / (np.abs(x).max() + 1e-9) * 0.89
    x[:int(.003 * SR)] *= np.linspace(0, 1, int(.003 * SR))[:, None]   # cegah bunyi "klik" di sampel pertama
    pcm = (np.clip(x, -1, 1) * 32767).astype('<i2')
    with wave.open(path, 'wb') as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(pcm.tobytes())


if __name__ == '__main__':
    out = sys.argv[1] if len(sys.argv) > 1 else '.'
    os.makedirs(out, exist_ok=True)
    if len(sys.argv) > 2:
        w = json.load(open(sys.argv[2]))
        WARP = (np.array([a[0] for a in w['anchors']], float), np.array([a[1] for a in w['anchors']], float))
        DUR = float(w['duration'])
        N = int(SR * DUR)
    m = music()
    m = np.tanh(1.3 * m / (np.abs(m).max() + 1e-9)) / np.tanh(1.3)    # saturasi halus ala tape
    write_wav(os.path.join(out, 'music.wav'), m)
    write_wav(os.path.join(out, 'sfx.wav'), sfx())
    print('selesai:', out)
