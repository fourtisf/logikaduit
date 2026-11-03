# Musik latar dan efek suara original untuk video EP11 (Indomie di Alfamart, siapa yang untung). Semua disintesis (bebas hak cipta),
# instrumennya ada di audio_lib.py. Waktu efek suara mengikuti timeline di ep11-indomie-alfamart.html.
# Pakai: python3 video/ep11-audio.py <folder-output> [warp.json]   -> music.wav dan sfx.wav (48 kHz, stereo)
# warp.json (dari ep11-mix.py) menggeser semua waktu supaya cocok dengan video yang temponya disesuaikan voice over.
import sys
import numpy as np
from audio_lib import *   # noqa: F401,F403  (SR, rng, instrumen, efek, place, reverb, ...)

DUR = 29.5
N = int(SR * DUR)
BEAT = 6.7 / 12           # sekitar 107 BPM; tiap 3 bar = 6,7 detik, jadi detik 4,6 (tumpukan Alfamart), 11,3 (cap "Lebih dari 4x")
                         # dan 18,0 (laba Rp9,22 triliun) sama-sama jatuh di awal bar
BAR = 4 * BEAT
OUT = 25.0               # awal penutup
W = Winv = lambda t: t   # diganti timeline() di bawah kalau ada warp.json


# ---------------- aransemen musik ----------------
CHORDS = {   # (bass, nada akor)
    'Am9': (45, [55, 59, 60, 64]), 'Fmaj9': (41, [57, 60, 64, 67]), 'G6': (43, [59, 62, 64, 67]),
    'Em7': (40, [55, 59, 62, 64]), 'Cmaj9': (36, [55, 59, 62, 64]),
}
PROG = ['Fmaj9', 'G6', 'Am9', 'Em7']


def section(t):
    """Intensitas per bagian video (format pendek: hampir selalu penuh)."""
    if t < 3.9: return 'hook'          # bungkus mi, "yang jualan vs yang bikin?"
    if t < 4.6: return 'build'         # menuju jawaban pertama
    if t < 8.6: return 'light'         # tumpukan Alfamart: cuma Rp2.700
    if t < 11.3: return 'build'        # tumpukan Indofood naik terus
    if t < 13.0: return 'full'         # cap "Lebih dari 4x"
    if t < 18.0: return 'after'        # rahasianya: merek
    if t < 22.0: return 'full'         # laba Rp9,22 triliun
    if t < OUT - .4: return 'after'    # tim goreng vs tim kuah
    return 'outro'


def music():
    dry = np.zeros((N, 2))
    wet_send = np.zeros((N, 2))
    g0 = W(11.3) % BAR - BAR               # grid bar digeser supaya cap "Lebih dari 4x" jatuh di awal bar
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
    # drum roll menjelang jawaban pertama (3,9 - 4,55) dan menjelang cap "Lebih dari 4x" (10,5 - 11,25), makin rapat
    for a0, a1 in ((3.9, 4.55), (10.5, 11.25)):
        r0, r1 = W(a0), W(a1)
        tt = r0
        while tt < r1:
            p = (tt - r0) / (r1 - r0)
            place(dry, tt, snare(.35 + .5 * p), .22, pan=-.1)
            tt += 0.14 * (1 - .65 * p) * (r1 - r0) / 0.75
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


def crinkle(d=.12, vel=1.0):
    """Bunyi bungkus plastik: desis pendek bertekstur."""
    t = T(d)
    n = fft_band(rng.standard_normal(len(t)), lo=1800, hi=9000) * (rng.random(len(t)) > .55)
    return fade_tail(n * np.exp(-t / (d / 3)) * vel, 10)


def sfx():
    s = np.zeros((N, 2))
    wet = np.zeros((N, 2))
    # hook: bungkus mi muncul, sorotan bergantian "yang jualan" vs "yang bikin"
    place(s, W(0.0), impact(.55, low=40, d=.9), .5)
    place(s, W(0.0), whoosh(.45, up=False, vel=.6), .25)
    place(s, W(.05), crinkle(.25), .18, pan=.1)
    b = bell(mtof(91), 1.4, .5, ratio=2.0)
    place(s, W(.3), b, .08, pan=.3)
    place(wet, W(.3), b, .1)
    for k, tt in enumerate((1.9, 2.5, 3.1, 3.7)):
        pn = -.5 if k % 2 == 0 else .5
        place(s, W(tt), pop(520 + 40 * k, 1100 + 60 * k, .1, .8), .2, pan=pn)
        place(s, W(tt), tick(2600, .4), .08, pan=pn)
    place(s, W(4.15), whoosh(.45), .22)
    # Alfamart: tiga koin jatuh, cuma Rp2.700
    place(s, W(4.6), whoosh(.5, up=False), .25, pan=-.3)
    for k in range(3):
        place(s, W(5.4 + k * .3 + .32), clink(.75), .12, pan=-.35)
    b = bell(mtof(76), 1.0, .5, ratio=2.0)
    place(s, W(6.35), b, .07, pan=-.3)
    # Indofood: dua belas koin, makin tinggi, lalu cap "Lebih dari 4x"
    place(s, W(8.6), whoosh(.5), .25, pan=.35)
    place(s, W(9.2), riser(W(11.3) - W(9.2), .5), .14)
    for k in range(12):
        place(s, W(9.3 + k * .13 + .32), clink(.6 + .03 * k), .1, pan=.35)
    place(s, W(11.3), impact(1.1, low=34, d=1.4), .9)
    stamp_hit(s, W(11.3), pan=0)
    for k, m in enumerate((88, 91, 96)):
        b = bell(mtof(m), 1.2, .7, ratio=2.0)
        place(s, W(11.35) + .06 * k, b, .12, pan=.2)
        place(wet, W(11.35) + .06 * k, b, .08)
    place(s, W(12.55), whoosh(.4, up=False, vel=.7), .16)
    # rahasianya merek: dua minimarket muncul, pembeli bolak-balik, bungkus mi menyala di dua-duanya
    place(s, W(13.0), whoosh(.5), .25, pan=-.4)
    place(s, W(13.15), whoosh(.5), .25, pan=.4)
    tt = 13.9
    while tt < 17.6:                                            # langkah pembeli, kiri-kanan
        place(s, W(tt), tap(.5), .05, pan=rng.uniform(-.5, .5))
        tt += .23
    place(s, W(15.3), pop(420, 980), .25)
    for k, m in enumerate((84, 88, 91)):
        b = bell(mtof(m), 1.2, .6, ratio=2.0)
        place(s, W(15.35) + .06 * k, b, .1, pan=(-.4, 0, .4)[k])
        place(wet, W(15.35) + .06 * k, b, .08)
    place(s, W(17.55), whoosh(.4, up=False, vel=.7), .16)
    # laba setahun Rp9,22 triliun, bungkus mi berjatuhan
    place(s, W(18.0), impact(.9, low=32, d=1.6), .7)
    tt = 18.2
    while tt < 19.4:                                            # angka berjalan naik
        place(s, W(tt), tick(2200, .5), .09, pan=.1)
        tt += .07
    for j in range(14):
        place(s, W(18.1 + j * .16), crinkle(.1, .8), .07, pan=(-.6 if j % 2 else .6))
    b = bell(mtof(96), 1.2, .6, ratio=2.0)
    place(s, W(19.42), b, .1)
    place(wet, W(19.42), b, .1)
    place(s, W(19.4), whoosh(.4), .18)
    # tim goreng vs tim kuah
    place(s, W(22.0), whoosh(.5), .25, pan=-.4)
    place(s, W(22.15), whoosh(.5), .25, pan=.4)
    place(s, W(22.6), impact(.6, low=50, d=.7), .45)
    place(s, W(22.9), whoosh(.35, vel=.6), .14)
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
