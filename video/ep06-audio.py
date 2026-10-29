# Musik latar dan efek suara original untuk video EP6 (isi snack makin kecil). Semua disintesis (bebas hak cipta),
# instrumennya ada di audio_lib.py. Waktu efek suara mengikuti timeline di ep06-snack-mengecil.html.
# Pakai: python3 video/ep06-audio.py <folder-output> [warp.json]   -> music.wav dan sfx.wav (48 kHz, stereo)
# warp.json (dari ep06-mix.py) menggeser semua waktu supaya cocok dengan video yang temponya disesuaikan voice over.
import sys
import numpy as np
from audio_lib import *   # noqa: F401,F403  (SR, rng, instrumen, efek, place, reverb, ...)

DUR = 27.0
N = int(SR * DUR)
BEAT = 0.55              # 109 BPM; satu bar 2,2 detik, cap "Harga sama" (1,85 detik) jatuh tepat di awal bar
BAR = 4 * BEAT
OUT = 22.6               # awal penutup
W = Winv = lambda t: t   # diganti timeline() di bawah kalau ada warp.json


# ---------------- aransemen musik ----------------
CHORDS = {   # (bass, nada akor)
    'Am9': (45, [55, 59, 60, 64]), 'Fmaj9': (41, [57, 60, 64, 67]), 'G6': (43, [59, 62, 64, 67]),
    'Em7': (40, [55, 59, 62, 64]), 'Cmaj9': (36, [55, 59, 62, 64]),
}
PROG = ['Fmaj9', 'G6', 'Em7', 'Am9']


def section(t):
    """Intensitas per bagian video (format pendek: hampir selalu penuh)."""
    if t < 1.85: return 'hook'         # pemindai sinar-X, isi turun
    if t < 8.0: return 'full'          # "harga sama", per gram naik 25%
    if t < 11.6: return 'light'        # kenapa nggak naikin harga
    if t < 16.0: return 'full'         # 4x lebih peka
    if t < 19.4: return 'after'        # cek beratnya
    if t < OUT - .4: return 'light'    # pertanyaan untuk komentar
    return 'outro'


def music():
    dry = np.zeros((N, 2))
    wet_send = np.zeros((N, 2))
    g0 = W(1.85) - BAR                     # grid bar digeser supaya cap pertama jatuh di awal bar
    b = -1
    while g0 + b * BAR < DUR:
        t0 = g0 + b * BAR
        b += 1
        sec = section(Winv(t0 + 0.01))
        name = PROG[(b - 1) % 4] if sec != 'outro' else ('Fmaj9' if t0 < W(OUT) else 'Cmaj9')
        root, notes = CHORDS[name]
        # piano: pukulan di ketukan 1, "and" ketukan 2, dan ketukan 4
        if sec != 'outro':
            for beat, ln, v in [(0, 1.5, .9), (1.5, 1.5, .55), (3, 1.0, .65)]:
                for k, m in enumerate(notes):
                    s = rhodes(mtof(m), ln * BEAT + .25, v * (0.9 if k else 1.0))
                    place(dry, t0 + beat * BEAT + .006 * k, s, .21)
                    place(wet_send, t0 + beat * BEAT + .006 * k, s, .05)
            v = {'full': 1, 'build': 1, 'after': .7, 'light': .6, 'hook': .85}[sec]
            for beat, ln, oc in [(0, 1.25, 0), (1.75, .5, 0), (2.5, 1.0, 0), (3.5, .45, 12)]:
                place(dry, t0 + beat * BEAT, bass(mtof(root + oc), ln * BEAT, v), .30)
        # drum
        for i in range(8):                 # hi-hat 1/8 dengan swing
            pos = (i // 2) + (0.58 if i % 2 else 0)
            tt = t0 + pos * BEAT
            s = section(Winv(tt))
            if s == 'outro':
                continue
            v = (.7 if i % 2 == 0 else .42) * {'light': .75, 'after': .8}.get(s, 1)
            place(dry, tt, hat(v, open_=(i == 7 and s == 'full')), .22, pan=.25)
        for beat in (0, 1.75, 2.5):
            tt = t0 + beat * BEAT
            s = section(Winv(tt))
            if s in ('full', 'hook', 'build') or (s in ('light', 'after') and beat == 0):
                place(dry, tt, kick(.9 if beat == 0 else .6), .42 if s != 'light' else .3)
        for beat in (1, 3):
            tt = t0 + beat * BEAT
            s = section(Winv(tt))
            if s in ('full', 'build'):
                sn = snare(.8)
                place(dry, tt, sn, .3, pan=-.1)
                place(wet_send, tt, sn, .06)
    # drum roll menjelang "4x" (10,7 - 11,55 detik), makin rapat
    r0, r1 = W(10.7), W(11.55)
    tt = r0
    while tt < r1:
        p = (tt - r0) / (r1 - r0)
        place(dry, tt, snare(.35 + .5 * p), .22, pan=-.1)
        tt += 0.14 * (1 - .65 * p) * (r1 - r0) / 0.95
    # penutup: akor Cmaj9 yang berdering
    root, notes = CHORDS['Cmaj9']
    for k, m in enumerate(notes):
        s = rhodes(mtof(m), DUR - W(OUT + .05) + .2, .8)
        place(dry, W(OUT + .05) + .02 * k, s, .2)
        place(wet_send, W(OUT + .05) + .02 * k, s, .12)
    place(dry, W(OUT + .05), bass(mtof(root), 3.0, .9), .3)
    place(dry, W(OUT + .05), pad([48, 55, 59, 62, 64], DUR - W(OUT + .05), .8), .35)
    out = dry + reverb(wet_send, 2.4)
    for ch in range(2):                    # buang sub di bawah 30 Hz (tidak terdengar di HP, hanya makan headroom)
        out[:, ch] = fft_band(out[:, ch], lo=30, soft=.5)
    fade = np.ones(N)
    fade[-int(1.2 * SR):] = np.linspace(1, 0, int(1.2 * SR)) ** 1.5
    return out * fade[:, None]


# ---------------- efek suara (waktu = timeline video) ----------------
def stamp_hit(s, t, pan=.3):
    place(s, t, fft_band(rng.standard_normal(int(.12 * SR)), lo=400, hi=4000) * np.exp(-T(.12) / .03), .4, pan=pan)


def scanner(d, vel=1.0):
    """Dengung pemindai sinar-X: nada naik dengan getaran cepat, ditambah desis halus."""
    t = T(d)
    f = 320 + 900 * (t / d) ** 1.5
    tone = np.sin(2 * np.pi * np.cumsum(f) / SR) * (.6 + .4 * np.sin(2 * np.pi * 28 * t))
    hiss = fft_band(rng.standard_normal(len(t)), lo=3000, hi=9000) * .25
    env = np.clip(t / .05, 0, 1) * np.clip((d - t) / .08, 0, 1)
    return (tone + hiss) * env * vel


def crinkle(d, vel=1.0, rate=60):
    """Gemerisik kemasan plastik: butiran noise pendek yang acak."""
    n = int(d * SR)
    x = np.zeros(n)
    for _ in range(int(d * rate)):
        i = int(rng.random() * (n - 800))
        g = int(200 + rng.random() * 600)
        x[i:i + g] += rng.standard_normal(g) * np.exp(-np.arange(g) / (g / 4)) * (.3 + .7 * rng.random())
    return fft_band(x, lo=1800, hi=9000) * vel


def sfx():
    s = np.zeros((N, 2))
    wet = np.zeros((N, 2))
    # hook: pemindai sinar-X turun, isi berkurang 100 g -> 80 g, cap "Harga sama"
    place(s, W(0.0), impact(.55, low=40, d=.9), .5)
    place(s, W(0.0), whoosh(.45, up=False, vel=.6), .25)
    place(s, W(.22), tick(3200, .8), .2)
    place(s, W(.25), scanner(W(1.05) - W(.25)), .16, pan=-.1)
    place(s, W(1.05), tick(3600, .8), .2)
    place(s, W(1.1), crinkle(W(1.8) - W(1.1)), .22, pan=.15)       # keripik "hilang"
    for k in range(20):                                         # 100 g -> 80 g
        place(s, W(1.1) + k * (W(1.8) - W(1.1)) / 20, tick(2400 - 40 * k, .5), .14, pan=-.2)
    place(s, W(1.5), pop(600, 300, .2), .2, pan=-.2)                # muncul "Angin"
    place(s, W(1.45), riser(W(1.85) - W(1.45), .5), .25)
    place(s, W(1.85), impact(1.1, low=34, d=1.4), .9)
    stamp_hit(s, W(1.85))
    # dulu vs sekarang, harga per gram
    place(s, W(3.0), whoosh(.5), .3, pan=-.3)
    place(s, W(3.2), whoosh(.5), .3, pan=.3)
    for k in range(10):                                         # isi turun
        place(s, W(3.9) + k * (W(4.6) - W(3.9)) / 10, tick(2000 - 60 * k, .5), .14, pan=.3)
    place(s, W(5.0), whoosh(.4), .2)
    for k in range(14):                                         # Rp100 -> Rp125
        place(s, W(5.3) + k * (W(6.1) - W(5.3)) / 14, tick(1700 + 80 * k, .6), .2, pan=.1)
    place(s, W(6.15), impact(.6, low=48, d=.8), .45)
    stamp_hit(s, W(6.15), pan=.2)
    # naikin harga vs kurangi isi
    place(s, W(8.0), whoosh(.5), .28, pan=-.2)
    place(s, W(8.25), whoosh(.5), .28, pan=.2)
    place(s, W(9.6), pop(420, 980), .25, pan=.1)
    for k, m in enumerate((84, 88)):
        place(s, W(9.65) + .08 * k, bell(mtof(m), 1.0, .6, ratio=2.0), .1, pan=.2)
    # 4x lebih peka
    place(s, W(11.6), impact(.8, low=32, d=1.6), .6)
    for k, (tt, m) in enumerate([(11.7, 88), (12.0, 91), (12.3, 96)]):
        b = bell(mtof(m), 1.6, .5, ratio=2.0)
        place(s, W(tt), b, .08, pan=(-.4 if k % 2 else .4))
        place(wet, W(tt), b, .12)
    place(s, W(12.8), whoosh(.6, vel=.7), .2, pan=-.2)
    place(s, W(13.4), whoosh(.4, vel=.5), .14, pan=.2)
    # label rak dan kaca pembesar
    place(s, W(16.0), whoosh(.5), .28)
    place(s, W(16.6), whoosh(.5, vel=.6), .15, pan=.3)
    place(s, W(17.1), pop(500, 1100, .1), .2, pan=.2)
    place(s, W(17.9), whoosh(.4, vel=.6), .14, pan=.2)
    place(s, W(18.4), bell(mtof(91), 1.0, .6, ratio=2.0), .12, pan=.3)
    # pertanyaan untuk komentar: tiga kemasan mengecil
    place(s, W(19.4), whoosh(.5), .25)
    for i in range(3):
        place(s, W(19.95 + i * .25), pop(800 - 120 * i, 400 - 60 * i, .14), .2, pan=-.3 + .3 * i)
    # penutup: logo, tombol follow muncul lalu ditekan (sama dengan episode lain)
    place(s, W(OUT + .05), impact(.7, low=38, d=1.6), .55)
    for k, m in enumerate((72, 76, 79, 83, 86)):
        b = bell(mtof(m), 2.4, .6, ratio=2.0)
        place(s, W(OUT + .1) + .05 * k, b, .1, pan=(k - 2) * .2)
        place(wet, W(OUT + .1) + .05 * k, b, .12)
    place(s, W(OUT + .9), pop(380, 820, .14), .25, pan=-.1)
    place(s, W(OUT + 2.3), fft_band(tap(), hi=6000), .32, pan=.15)
    for k, m in enumerate((79, 84, 88, 91)):
        b = bell(mtof(m), 1.2, .8, ratio=2.0)
        place(s, W(OUT + 2.42) + .06 * k, b, .13, pan=.2)
        place(wet, W(OUT + 2.42) + .06 * k, b, .1)
    return s + reverb(wet, 1.8)


if __name__ == '__main__':
    W, Winv, DUR = timeline(DUR, sys.argv[2] if len(sys.argv) > 2 else None)
    N = int(SR * DUR)
    save(sys.argv[1] if len(sys.argv) > 1 else '.', music(), sfx())
