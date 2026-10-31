# Musik latar dan efek suara original untuk video EP8 (diskon 50% + 20%). Semua disintesis (bebas hak cipta),
# instrumennya ada di audio_lib.py. Waktu efek suara mengikuti timeline di ep08-diskon-bertumpuk.html.
# Pakai: python3 video/ep08-audio.py <folder-output> [warp.json]   -> music.wav dan sfx.wav (48 kHz, stereo)
# warp.json (dari ep08-mix.py) menggeser semua waktu supaya cocok dengan video yang temponya disesuaikan voice over.
import sys
import numpy as np
from audio_lib import *   # noqa: F401,F403  (SR, rng, instrumen, efek, place, reverb, ...)

DUR = 28.6
N = int(SR * DUR)
BEAT = 0.55              # 109 BPM; satu bar 2,2 detik, cap "Salah" (4,6 detik) jatuh tepat di awal bar
BAR = 4 * BEAT
OUT = 24.2               # awal penutup
W = Winv = lambda t: t   # diganti timeline() di bawah kalau ada warp.json


# ---------------- aransemen musik ----------------
CHORDS = {   # (bass, nada akor)
    'Am9': (45, [55, 59, 60, 64]), 'Fmaj9': (41, [57, 60, 64, 67]), 'G6': (43, [59, 62, 64, 67]),
    'Em7': (40, [55, 59, 62, 64]), 'Cmaj9': (36, [55, 59, 62, 64]),
}
PROG = ['Fmaj9', 'Em7', 'Am9', 'G6']


def section(t):
    """Intensitas per bagian video (format pendek: hampir selalu penuh)."""
    if t < 2.9: return 'hook'          # label harga, stiker diskon, kuis
    if t < 4.6: return 'build'         # memilih 70%, menuju cap "Salah"
    if t < 5.6: return 'full'
    if t < 10.0: return 'light'        # struk tercetak
    if t < 14.0: return 'full'         # bayar Rp40.000, hemat 60%
    if t < 17.6: return 'light'        # salah hitung menguntungkan toko
    if t < 21.5: return 'full'         # riset di toko, "sama persis"
    if t < OUT - .4: return 'after'    # ajakan simpan
    return 'outro'


def music():
    dry = np.zeros((N, 2))
    wet_send = np.zeros((N, 2))
    g0 = W(4.6) % BAR - BAR                # grid bar digeser supaya cap "Salah" jatuh di awal bar
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
    # drum roll menjelang cap "Salah" (3,7 - 4,55 detik), makin rapat
    r0, r1 = W(3.7), W(4.55)
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


def slap(vel=1.0):
    """Stiker ditempel: tepukan kertas pendek."""
    t = T(.09)
    return fade_tail((fft_band(rng.standard_normal(len(t)), lo=600, hi=6000) * np.exp(-t / .012) + .5 * np.sin(2 * np.pi * 160 * t) * np.exp(-t / .03)) * vel, 6)


def buzz(vel=1.0):
    """Bunyi "salah": dua nada rendah pendek."""
    out = np.zeros(int(.42 * SR))
    for k in range(2):
        t = T(.15)
        x = np.tanh(3 * np.sin(2 * np.pi * 185 * t)) * np.clip(t / .005, 0, 1) * np.clip((.15 - t) / .02, 0, 1)
        i = int(k * .2 * SR); out[i:i + len(x)] += fft_band(x, hi=2500)
    return out * vel


def printer(d, vel=1.0):
    """Printer struk: ketukan cepat yang rapat."""
    n = int(d * SR)
    x = np.zeros(n)
    for i in range(0, n - 400, int(SR / 55)):
        g = 300
        x[i:i + g] += rng.standard_normal(g) * np.exp(-np.arange(g) / 60)
    return fft_band(x, lo=1500, hi=8000) * vel


def sfx():
    s = np.zeros((N, 2))
    wet = np.zeros((N, 2))
    # hook: label harga, dua stiker menempel, kuis 70% vs 60%
    place(s, W(0.0), impact(.55, low=40, d=.9), .5)
    place(s, W(0.0), whoosh(.45, up=False, vel=.6), .25)
    place(s, W(.45), impact(.5, low=60, d=.5), .3)
    place(s, W(.45), slap(), .35, pan=.3)
    place(s, W(1.05), impact(.4, low=70, d=.4), .25)
    place(s, W(1.05), slap(.8), .3, pan=.4)
    for k, tt in enumerate((1.6, 1.72)):
        place(s, W(tt), pop(500 + 120 * k, 1000 + 150 * k, .1), .22, pan=(-.3 if k == 0 else .3))
    for k, tt in enumerate((2.1, 2.5)):                            # jari ragu-ragu
        place(s, W(tt), tick(2200 if k % 2 else 1900, .5), .12, pan=(.3 if k == 0 else -.3))
    place(s, W(2.9), fft_band(tap(), hi=6000), .32, pan=-.3)        # memilih 70%
    place(s, W(2.92), bell(mtof(88), 1.0, .6, ratio=2.0), .1, pan=-.3)
    place(s, W(4.6), impact(1.1, low=34, d=1.4), .9)                # cap "Salah"
    stamp_hit(s, W(4.6), pan=-.3)
    place(s, W(4.68), buzz(), .14, pan=-.3)
    for k, m in enumerate((86, 91)):                             # 60% menyala
        b = bell(mtof(m), 1.2, .7, ratio=2.0)
        place(s, W(4.75) + .07 * k, b, .12, pan=.3)
        place(wet, W(4.75) + .07 * k, b, .08)
    # struk tercetak baris demi baris
    place(s, W(5.6), whoosh(.5), .28)
    for tt in (6.0, 6.6, 7.2, 7.8, 8.2, 10.0):
        place(s, W(tt), printer(.32), .16, pan=.1)
    place(s, W(8.05), bell(mtof(84), 1.0, .5, ratio=2.0), .08, pan=.2)
    place(s, W(10.05), impact(.5, low=50, d=.7), .35)
    for k, m in enumerate((84, 88, 91)):
        b = bell(mtof(m), 1.2, .6, ratio=2.0)
        place(s, W(10.1) + .06 * k, b, .1, pan=.2)
        place(wet, W(10.1) + .06 * k, b, .08)
    place(s, W(11.6), impact(1.0, low=36, d=1.2), .8)               # cap "Hemat 60%"
    stamp_hit(s, W(11.6), pan=.3)
    # riset di toko
    place(s, W(14.0), whoosh(.5), .28, pan=-.3)
    place(s, W(14.2), whoosh(.5), .28, pan=.3)
    for k, tt in enumerate((14.6, 14.85, 15.1)):
        place(s, W(tt), slap(.8), .28, pan=(-.4 if k == 0 else .4))
    place(s, W(17.6), riser(W(18.9) - W(17.6), .4), .16)
    for k in range(12):
        place(s, W(17.6) + k * (W(18.9) - W(17.6)) / 12, tick(1600 + 90 * k, .5), .13, pan=.2)
    place(s, W(18.95), pop(420, 980), .25, pan=.35)                 # "lebih laku"
    place(s, W(19.9), pop(500, 1100, .12), .22)                     # tanda "="
    place(s, W(20.2), impact(1.0, low=36, d=1.2), .8)               # cap "Sama persis"
    stamp_hit(s, W(20.2))
    # ajakan simpan
    place(s, W(21.5), whoosh(.5), .25)
    place(s, W(22.75), fft_band(tap(), hi=6000), .32)
    for k, m in enumerate((79, 84, 88, 91)):
        b = bell(mtof(m), 1.2, .7, ratio=2.0)
        place(s, W(22.8) + .06 * k, b, .12, pan=.2)
        place(wet, W(22.8) + .06 * k, b, .1)
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
