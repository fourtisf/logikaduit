# Musik latar dan efek suara original untuk video EP10 (Alfamart untung berapa). Semua disintesis (bebas hak cipta),
# instrumennya ada di audio_lib.py. Waktu efek suara mengikuti timeline di ep10-untung-alfamart.html.
# Pakai: python3 video/ep10-audio.py <folder-output> [warp.json]   -> music.wav dan sfx.wav (48 kHz, stereo)
# warp.json (dari ep10-mix.py) menggeser semua waktu supaya cocok dengan video yang temponya disesuaikan voice over.
import sys
import numpy as np
from audio_lib import *   # noqa: F401,F403  (SR, rng, instrumen, efek, place, reverb, ...)

DUR = 27.0
N = int(SR * DUR)
BEAT = 0.55              # 109 BPM; satu bar 2,2 detik, jawaban "Rp2.700" (3,4 detik) jatuh tepat di awal bar
BAR = 4 * BEAT
OUT = 22.6               # awal penutup
W = Winv = lambda t: t   # diganti timeline() di bawah kalau ada warp.json


# ---------------- aransemen musik ----------------
CHORDS = {   # (bass, nada akor)
    'Am9': (45, [55, 59, 60, 64]), 'Fmaj9': (41, [57, 60, 64, 67]), 'G6': (43, [59, 62, 64, 67]),
    'Em7': (40, [55, 59, 62, 64]), 'Cmaj9': (36, [55, 59, 62, 64]),
}
PROG = ['Fmaj9', 'G6', 'Am9', 'Em7']


def section(t):
    """Intensitas per bagian video (format pendek: hampir selalu penuh)."""
    if t < 2.6: return 'hook'          # uang Rp100.000, tebakan berputar
    if t < 3.4: return 'build'         # menuju jawaban "Rp2.700"
    if t < 6.4: return 'full'          # laser memotong 2,7%
    if t < 11.0: return 'light'        # sisanya ke pemasok, gaji, sewa, listrik, pajak
    if t < 19.6: return 'full'         # 24 ribu gerai, laba Rp3,41 triliun
    if t < OUT - .4: return 'after'    # tim Alfamart vs tim Indomaret
    return 'outro'


def music():
    dry = np.zeros((N, 2))
    wet_send = np.zeros((N, 2))
    g0 = W(3.4) % BAR - BAR                # grid bar digeser supaya jawaban "Rp2.700" jatuh di awal bar
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
    # drum roll menjelang jawaban "Rp2.700" (2,6 - 3,35 detik), makin rapat
    r0, r1 = W(2.6), W(3.35)
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


def clink(vel=1.0):
    """Bunyi koin: dua dentingan logam tinggi yang cepat."""
    a, b = bell(mtof(100), .5, vel, ratio=2.76), bell(mtof(103), .45, vel, ratio=2.76)
    d = int(.035 * SR)
    a[d:d + len(b)] += .6 * b[:len(a) - d]
    return a


def laser(d=.5, vel=1.0):
    """Laser memotong: nada tinggi yang turun cepat ditambah desis."""
    t = T(d)
    f = 3200 * np.exp(-t / (d / 2.5)) + 500
    tone = np.sin(2 * np.pi * np.cumsum(f) / SR)
    hiss = fft_band(rng.standard_normal(len(t)), lo=2500, hi=10000) * .35
    return fade_tail((tone + hiss) * np.exp(-t / (d / 1.5)) * np.clip(t / .005, 0, 1) * vel, 20)


def sfx():
    s = np.zeros((N, 2))
    wet = np.zeros((N, 2))
    # hook: uang Rp100.000, tebakan berputar seperti mesin slot
    place(s, W(0.0), impact(.55, low=40, d=.9), .5)
    place(s, W(0.0), whoosh(.45, up=False, vel=.6), .25)
    b = bell(mtof(91), 1.4, .5, ratio=2.0)
    place(s, W(.3), b, .08, pan=.3)
    place(wet, W(.3), b, .1)
    k, tt = 0, .7
    while tt < 3.38:                                            # angka tebakan berganti 11 kali per detik
        place(s, W(tt), tick(2400 if k % 2 else 2000, .55), .13, pan=.2)
        tt += 1 / 11
        k += 1
    place(s, W(3.4), impact(1.1, low=34, d=1.4), .9)              # jawaban: cuma Rp2.700
    stamp_hit(s, W(3.4))
    for k, m in enumerate((88, 91, 96)):
        b = bell(mtof(m), 1.2, .7, ratio=2.0)
        place(s, W(3.45) + .06 * k, b, .12, pan=.2)
        place(wet, W(3.45) + .06 * k, b, .08)
    place(s, W(3.5), laser(W(4.1) - W(3.5) + .1), .25, pan=.3)    # laser memotong 2,7%
    place(s, W(4.1), whoosh(.45), .2, pan=.4)
    place(s, W(4.6), pop(420, 980), .25, pan=.2)                  # "Cuma 2,7%"
    # sisanya ke pemasok, gaji, sewa, listrik, pajak
    place(s, W(6.4), whoosh(.5, up=False), .28)
    for i in range(5):
        place(s, W(6.7 + i * .18), pop(480 + 60 * i, 950 + 80 * i, .09, .6), .14, pan=-.4 + .2 * i)
    for j in range(30):
        i = j % 5
        place(s, W(7.3 + (j // 5) * .45 + i * .09 + .6), clink(.5), .05, pan=-.4 + .2 * i)
    # 24 ribu gerai menyala di peta
    place(s, W(11.0), whoosh(.55), .28)
    place(s, W(11.5), riser(W(14.3) - W(11.5), .5), .18)
    tt = 11.5
    while tt < 14.3:                                            # kilau titik gerai, makin rapat
        place(s, W(tt), tick(3000 + 1500 * rng.random(), .35), .08, pan=rng.uniform(-.6, .6))
        tt += .11 - .08 * (tt - 11.5) / 2.8
    place(s, W(14.3), impact(.6, low=48, d=.8), .45)
    for k, m in enumerate((84, 88, 91)):
        b = bell(mtof(m), 1.2, .6, ratio=2.0)
        place(s, W(14.35) + .06 * k, b, .1, pan=.2)
        place(wet, W(14.35) + .06 * k, b, .08)
    # laba bersih setahun, koin berjatuhan
    place(s, W(15.2), impact(.9, low=32, d=1.6), .7)
    for j in range(30):
        place(s, W(15.3 + j * .07 + 1.0), clink(.45), .05, pan=(-.5 if j % 2 else .5))
    place(s, W(16.8), whoosh(.4), .18)
    # tim Alfamart vs tim Indomaret
    place(s, W(19.6), whoosh(.5), .25, pan=-.4)
    place(s, W(19.75), whoosh(.5), .25, pan=.4)
    place(s, W(20.25), impact(.6, low=50, d=.7), .45)
    place(s, W(20.6), whoosh(.35, vel=.6), .14)
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
