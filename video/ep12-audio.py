# Musik latar dan efek suara original untuk video EP12 (selama kamu nonton, BCA untung berapa). Semua disintesis (bebas hak cipta),
# instrumennya ada di audio_lib.py. Waktu efek suara mengikuti timeline di ep12-untung-bca.html.
# Pakai: python3 video/ep12-audio.py <folder-output> [warp.json]   -> music.wav dan sfx.wav (48 kHz, stereo)
# warp.json (dari ep12-mix.py) menggeser semua waktu supaya cocok dengan video yang temponya disesuaikan voice over.
import sys
import numpy as np
from audio_lib import *   # noqa: F401,F403  (SR, rng, instrumen, efek, place, reverb, ...)

DUR = 29.5
N = int(SR * DUR)
BEAT = 0.55              # 109 BPM; satu bar 2,2 detik, angka "Rp57,5 triliun" (4,6 detik) jatuh tepat di awal bar
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
    if t < 4.1: return 'hook'          # penghitung untung berjalan
    if t < 4.6: return 'build'         # menuju laba setahun
    if t < 9.0: return 'full'          # Rp57,5 triliun, per hari / menit / detik
    if t < 13.4: return 'light'        # tabungan bunga 0%
    if t < 17.8: return 'build'        # dipinjamkan, bunga dasar kredit naik
    if t < 21.8: return 'full'         # selisih bunga = mesin uang
    if t < OUT - .4: return 'after'    # kamu nasabah bank apa?
    return 'outro'


def music():
    dry = np.zeros((N, 2))
    wet_send = np.zeros((N, 2))
    g0 = W(4.6) % BAR - BAR                # grid bar digeser supaya "Rp57,5 triliun" jatuh di awal bar
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
    # drum roll menjelang laba setahun (4,0 - 4,55) dan menjelang bunga dasar kredit (14,4 - 14,95), makin rapat
    for a0, a1 in ((4.0, 4.55), (14.4, 14.95)):
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


def sfx():
    s = np.zeros((N, 2))
    wet = np.zeros((N, 2))
    # hook: penghitung untung berjalan (detak meteran cepat + denyut tiap detik nyata)
    place(s, W(0.0), impact(.55, low=40, d=.9), .5)
    place(s, W(0.0), whoosh(.45, up=False, vel=.6), .25)
    b = bell(mtof(91), 1.4, .5, ratio=2.0)
    place(s, W(.3), b, .08, pan=.3)
    place(wet, W(.3), b, .1)
    k, tt = 0, W(.05)
    while tt < W(4.3):                                          # angka kecil berganti terus
        place(s, tt, tick(2300 if k % 2 else 1900, .4), .07, pan=.15)
        tt += 1 / 14
        k += 1
    sec = 1.0
    while sec < W(4.3):                                         # garis detik penuh: denyut kecil tiap detik video
        place(s, sec, pop(300, 620, .1, .6), .12)
        sec += 1.0
    # laba setahun Rp57,5 triliun, lalu per hari / menit / detik
    place(s, W(4.6), whoosh(.5), .25)
    place(s, W(4.75), impact(1.0, low=34, d=1.4), .8)
    for k, m in enumerate((84, 88, 91, 96)):
        b = bell(mtof(m), 1.2, .6, ratio=2.0)
        place(s, W(4.8) + .05 * k, b, .1, pan=.2)
        place(wet, W(4.8) + .05 * k, b, .08)
    tt = 4.8
    while tt < 5.9:
        place(s, W(tt), tick(2200, .45), .08, pan=.1)
        tt += .07
    for tt, pn in ((6.2, -.3), (6.9, .3)):
        place(s, W(tt), whoosh(.3, vel=.5), .12, pan=pn)
        place(s, W(tt + .1), pop(460, 1000, .1, .7), .16, pan=pn)
    place(s, W(7.6), impact(.6, low=48, d=.8), .45)               # per detik Rp1,8 juta
    stamp_hit(s, W(7.62), pan=0)
    for k in range(4):
        place(s, W(7.7) + .05 * k, clink(.7), .1, pan=(-.3, .3)[k % 2])
    place(s, W(8.55), whoosh(.4, up=False, vel=.7), .16)
    # tabungan: bunganya 0%
    place(s, W(9.0), whoosh(.5), .25)
    place(s, W(9.3), pop(380, 760, .1, .6), .14, pan=-.3)
    place(s, W(9.95), impact(.8, low=30, d=1.2), .6)              # "0%" menghantam
    for k, m in enumerate((79, 75, 72)):                          # tiga nada turun: "yah, nol"
        b = bell(mtof(m), 1.0, .6, ratio=2.0)
        place(s, W(10.0) + .12 * k, b, .1, pan=-.3)
        place(wet, W(10.0) + .12 * k, b, .1)
    place(s, W(10.6), whoosh(.35, vel=.6), .14, pan=.4)
    place(s, W(11.2), tick(1600, .6), .1, pan=.4)
    # dipinjamkan lagi: koin mengalir ke kanan, batang bunga kredit naik
    place(s, W(13.4), whoosh(.5), .25, pan=.3)
    for j in range(18):
        place(s, W(13.6 + j * .08 + .7), clink(.45), .045, pan=.4)
    place(s, W(14.1), riser(W(15.0) - W(14.1), .5), .14)
    place(s, W(15.0), impact(.9, low=36, d=1.2), .65)
    for k, m in enumerate((84, 88, 91)):
        b = bell(mtof(m), 1.2, .6, ratio=2.0)
        place(s, W(15.05) + .06 * k, b, .1, pan=.3)
        place(wet, W(15.05) + .06 * k, b, .08)
    # selisih bunga: panah naik, label, lalu koin masuk ke penghitung
    place(s, W(17.8), whoosh(.45, up=False, vel=.7), .2)
    place(s, W(17.9), riser(W(18.5) - W(17.9), .6), .12)
    place(s, W(18.45), impact(.6, low=50, d=.7), .45)
    place(s, W(18.5), pop(420, 980), .22)
    for j in range(18):
        place(s, W(18.6 + j * .13 + .75), clink(.55 + .02 * j), .06, pan=.35)
    for k, m in enumerate((88, 91, 96, 100)):                     # "cring": penghitung penuh
        b = bell(mtof(m), 1.4, .7, ratio=2.0)
        place(s, W(21.0) + .05 * k, b, .1, pan=.3)
        place(wet, W(21.0) + .05 * k, b, .1)
    # kamu nasabah bank apa?
    for k, tt in enumerate((21.8, 21.95, 22.1)):
        place(s, W(tt), whoosh(.4, vel=.6), .16, pan=(-.4, 0, .4)[k])
    place(s, W(22.6), whoosh(.35, vel=.6), .14)
    for k in range(5):
        place(s, W(22.9 + .45 * k), tick(2600, .5), .08, pan=(-.4, 0, .4)[k % 3])
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
