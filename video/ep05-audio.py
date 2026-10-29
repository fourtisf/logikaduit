# Musik latar dan efek suara original untuk video EP5 (duit Mixue dari mana). Semua disintesis (bebas hak cipta),
# instrumennya ada di audio_lib.py. Waktu efek suara mengikuti timeline di ep05-mixue.html.
# Pakai: python3 video/ep05-audio.py <folder-output> [warp.json]   -> music.wav dan sfx.wav (48 kHz, stereo)
# warp.json (dari ep05-mix.py) menggeser semua waktu supaya cocok dengan video yang temponya disesuaikan voice over.
import sys
import numpy as np
from audio_lib import *   # noqa: F401,F403  (SR, rng, instrumen, efek, place, reverb, ...)

DUR = 25.0
N = int(SR * DUR)
BEAT = 0.55              # 109 BPM; satu bar 2,2 detik, cap "Bukan dari sini" (1,65 detik) jatuh tepat di awal bar
BAR = 4 * BEAT
OUT = 20.8               # awal penutup
W = Winv = lambda t: t   # diganti timeline() di bawah kalau ada warp.json


# ---------------- aransemen musik ----------------
CHORDS = {   # (bass, nada akor)
    'Am9': (45, [55, 59, 60, 64]), 'Fmaj9': (41, [57, 60, 64, 67]), 'G6': (43, [59, 62, 64, 67]),
    'Em7': (40, [55, 59, 62, 64]), 'Cmaj9': (36, [55, 59, 62, 64]),
}
PROG = ['Am9', 'Fmaj9', 'G6', 'Em7']


def section(t):
    """Intensitas per bagian video (format pendek: hampir selalu penuh)."""
    if t < 1.65: return 'hook'         # koin masuk ke es krim
    if t < 7.4: return 'full'          # "bukan dari sini", 97,6%
    if t < 11.0: return 'light'        # barang dari pusat ke gerai
    if t < 14.4: return 'full'         # gerai bertambah, pusat makin cuan
    if t < 15.85: return 'build'       # menuju cap "Pemasok"
    if t < 17.6: return 'full'
    if t < OUT - .4: return 'after'    # pertanyaan untuk komentar
    return 'outro'


def music():
    dry = np.zeros((N, 2))
    wet_send = np.zeros((N, 2))
    g0 = W(1.65) - BAR                     # grid bar digeser supaya cap pertama jatuh di awal bar
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
    # drum roll menjelang cap "Pemasok" (14,9 - 15,8 detik), makin rapat
    r0, r1 = W(14.9), W(15.8)
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
def clink(vel=1.0):
    """Bunyi koin: dua dentingan logam tinggi yang cepat."""
    a, b = bell(mtof(100), .5, vel, ratio=2.76), bell(mtof(103), .45, vel, ratio=2.76)
    d = int(.035 * SR)
    a[d:d + len(b)] += .6 * b[:len(a) - d]
    return a


def stamp_hit(s, t, pan=.3):
    place(s, t, fft_band(rng.standard_normal(int(.12 * SR)), lo=400, hi=4000) * np.exp(-T(.12) / .03), .4, pan=pan)


def sfx():
    s = np.zeros((N, 2))
    wet = np.zeros((N, 2))
    # hook: koin dari "kamu" masuk ke es krim, lalu cap "Bukan dari sini"
    place(s, W(0.0), impact(.55, low=40, d=.9), .5)
    place(s, W(0.0), whoosh(.45, up=False, vel=.6), .25)
    for i in range(5):
        place(s, W(.12 + i * .2), whoosh(.3, vel=.5), .08, pan=-.3)
        place(s, W(.67 + i * .2), clink(.7), .1, pan=.05 * i)
    place(s, W(1.2), riser(W(1.65) - W(1.2), .6), .3)
    place(s, W(1.65), impact(1.1, low=34, d=1.4), .9)
    stamp_hit(s, W(1.65))
    place(s, W(2.05), pop(700, 380, .18), .22, pan=.2)              # es krim meredup
    # 97,6%
    place(s, W(3.2), whoosh(.5), .3)
    for k in range(14):
        place(s, W(3.5) + k * (W(4.6) - W(3.5)) / 14, tick(1700 + 80 * k, .6), .22, pan=.1)
    place(s, W(4.6), impact(.6, low=48, d=.8), .45)
    for k, m in enumerate((84, 91)):
        b = bell(mtof(m), 1.2, .7, ratio=2.0)
        place(s, W(4.62) + .07 * k, b, .12, pan=.2)
        place(wet, W(4.62) + .07 * k, b, .1)
    place(s, W(4.4), whoosh(.4), .2, pan=-.2)
    # pusat mengirim barang ke gerai, uang kembali ke pusat
    place(s, W(7.4), whoosh(.5, up=False), .3)
    place(s, W(7.5), impact(.4, low=60, d=.5), .3)
    for k in range(5):
        place(s, W(7.6 + k * .08), pop(500 + 50 * k, 900 + 60 * k, .08, .6), .12, pan=-.4 + .2 * k)
    for i, t0 in enumerate((8.0, 8.35, 8.7, 9.05)):
        place(s, W(t0), whoosh(.4, vel=.6), .14, pan=-.2 + .15 * i)
        place(s, W(t0 + .8), pop(420, 980, .1), .2, pan=-.2 + .15 * i)
    for j in range(5):
        place(s, W(9.6 + j * .1 + .7), clink(.6), .08, pan=-.3 + .15 * j)
    # makin banyak gerai, makin cuan pusatnya
    place(s, W(11.0), whoosh(.55), .3)
    for k in range(19):
        place(s, W(11.5 + k * .075), pop(450 + 25 * k, 900 + 40 * k, .07, .5), .07, pan=-.5 + .05 * k)
    for j in range(0, 24, 2):
        place(s, W(11.7 + j * .1 + .7), clink(.5), .06, pan=(-.3 if j % 4 else .3))
    place(s, W(13.0), riser(W(14.0) - W(13.0), .5), .2)
    # "Toko es krim" dicoret, cap "Pemasok"
    place(s, W(14.4), whoosh(.5), .3)
    place(s, W(15.2), whoosh(.3, vel=.8), .25, pan=.2)
    place(s, W(15.85), impact(1.0, low=36, d=1.2), .8)
    stamp_hit(s, W(15.85), pan=.2)
    place(s, W(16.2), bell(mtof(88), 1.2, .6), .1, pan=.3)
    # pertanyaan untuk komentar
    place(s, W(17.6), whoosh(.5), .25)
    for k, m in enumerate((79, 86)):
        place(s, W(17.8) + .09 * k, bell(mtof(m), .9, .6, ratio=2.0), .12, pan=.2)
    for k, tt in enumerate((18.9, 19.5, 20.1)):                   # jari pindah pilihan
        place(s, W(tt), tick(2200 if k % 2 else 1900, .5), .12, pan=.3)
    # penutup: logo, tombol follow muncul lalu ditekan (sama dengan EP3/EP4)
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
