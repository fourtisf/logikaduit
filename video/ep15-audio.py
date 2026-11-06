# Musik latar dan efek suara original untuk video EP15 (harga dicoret, kok kerasa murah?). Semua disintesis (bebas hak cipta),
# instrumennya ada di audio_lib.py. Waktu efek suara mengikuti timeline di ep15-harga-coret.html.
# Pakai: python3 video/ep15-audio.py <folder-output> [warp.json]   -> music.wav dan sfx.wav (48 kHz, stereo)
# warp.json (dari ep15-mix.py) menggeser semua waktu supaya cocok dengan video yang temponya disesuaikan voice over.
import sys
import numpy as np
from audio_lib import *   # noqa: F401,F403  (SR, rng, instrumen, efek, place, reverb, ...)

DUR = 34.0
N = int(SR * DUR)
BEAT = 0.46              # sekitar 130 BPM, tegang ala flash sale; kartu trik (2,75 detik) jatuh tepat di awal bar
BAR = 4 * BEAT
OUT = 29.4               # awal penutup
W = Winv = lambda t: t   # diganti timeline() di bawah kalau ada warp.json


# ---------------- aransemen musik ----------------
CHORDS = {   # (bass, nada akor)
    'Am9': (45, [55, 59, 60, 64]), 'Fmaj9': (41, [57, 60, 64, 67]), 'G6': (43, [59, 62, 64, 67]),
    'Em7': (40, [55, 59, 62, 64]), 'Cmaj9': (36, [55, 59, 62, 64]),
}
PROG = ['Am9', 'Fmaj9', 'G6', 'Em7']   # progresi minor yang tegang ala flash sale


def section(t):
    """Intensitas per bagian video."""
    if t < 2.2: return 'hook'          # flash sale, harga dicoret, hitung mundur
    if t < 2.75: return 'build'        # menuju kartu trik
    if t < 4.6: return 'full'          # "Coba trik ini: tutup pakai jempol"
    if t < 8.4: return 'full'          # jangkar menghantam angka
    if t < 12.6: return 'light'        # riset: dua angka terakhir nomor identitas
    if t < 15.4: return 'build'        # tawaran $16 vs $56
    if t < 17.0: return 'full'         # cap "Padahal acak!"
    if t < 21.4: return 'after'        # harga coret = jangkar, malas cek toko lain
    if t < 25.6: return 'light'        # jempol menutup harga coret
    if t < OUT - .4: return 'after'    # mau checkout apa?
    return 'outro'


def music():
    dry = np.zeros((N, 2))
    wet_send = np.zeros((N, 2))
    g0 = W(2.75) % BAR - BAR               # grid bar digeser supaya kartu trik jatuh di awal bar
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
    # drum roll menjelang kartu trik (2,2 - 2,7) dan menjelang cap "Padahal acak!" (14,85 - 15,35), makin rapat
    for a0, a1 in ((2.2, 2.7), (14.85, 15.35)):
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


def clang(vel=1.0):
    """Dentang logam berat untuk jangkar yang mendarat."""
    a, b = bell(mtof(43), 2.2, vel, ratio=2.76), bell(mtof(50), 1.6, vel * .7, ratio=3.1)
    a[:len(b)] += .6 * b
    return a


def sfx():
    s = np.zeros((N, 2))
    wet = np.zeros((N, 2))
    # hook: flash sale, harga dicoret, hitung mundur berdetak
    place(s, W(0.0), impact(.55, low=40, d=.9), .45)
    place(s, W(0.0), whoosh(.45, up=False, vel=.6), .22)
    for k, m in enumerate((91, 96, 100)):                               # mata berbinar
        b = bell(mtof(m), .9, .5, ratio=2.0)
        place(s, W(.2) + .07 * k, b, .07, pan=-.4)
        place(wet, W(.2) + .07 * k, b, .08)
    tt, k = 0.0, 0
    while tt < 2.7:                                                     # detak hitung mundur
        place(s, W(tt), tick(2000 if k % 2 else 1500, .6), .1, pan=.35)
        tt += .5
        k += 1
    place(s, W(2.75), impact(1.0, low=34, d=1.4), .8)                   # "Coba trik ini"
    place(s, W(2.75), whoosh(.45), .2)
    for k, m in enumerate((84, 88, 91, 96)):
        b = bell(mtof(m), 1.2, .6, ratio=2.0)
        place(s, W(2.8) + .05 * k, b, .1, pan=.2)
        place(wet, W(2.8) + .05 * k, b, .08)
    place(s, W(4.15), whoosh(.4, up=False, vel=.7), .16)
    # jangkar jatuh menghantam angka pertama
    place(s, W(4.7), pop(400, 900, .12, .8), .2)
    place(s, W(5.0), whoosh(.55, up=False, vel=.9), .3)
    place(s, W(5.56), impact(1.2, low=30, d=1.6), 1.0)
    c = clang(.9)
    place(s, W(5.56), c, .16)
    place(wet, W(5.56), c, .14)
    place(s, W(6.0), pop(380, 760, .1, .6), .12, pan=-.4)
    place(s, W(6.6), pop(460, 1000), .18)
    place(s, W(7.95), whoosh(.4, up=False, vel=.7), .16)
    # riset: kartu identitas, dua angka terakhir menyala
    place(s, W(8.4), whoosh(.5), .22)
    place(s, W(8.5), whoosh(.35, vel=.5), .12, pan=-.4)
    place(s, W(8.8), whoosh(.35, vel=.5), .12, pan=.4)
    place(s, W(9.8), tick(2600, .6), .1, pan=-.4)
    place(s, W(10.1), tick(3000, .6), .1, pan=.4)
    place(s, W(10.6), pop(420, 980), .2)
    place(s, W(12.15), whoosh(.4, up=False, vel=.7), .16)
    # tawaran $16 vs $56, cap "Padahal acak!"
    place(s, W(12.6), whoosh(.5), .25)
    place(s, W(12.9), riser(.7, .4), .08, pan=-.3)
    place(s, W(13.4), pop(380, 760, .1, .7), .16, pan=-.3)
    place(s, W(13.8), riser(W(15.0) - W(13.8), .55), .12, pan=.3)
    place(s, W(14.7), pop(520, 1200, .12, .8), .2, pan=.3)
    place(s, W(15.4), impact(1.1, low=34, d=1.4), .9)
    stamp_hit(s, W(15.42), pan=-.2)
    for k, m in enumerate((88, 91, 96)):
        b = bell(mtof(m), 1.2, .7, ratio=2.0)
        place(s, W(15.45) + .06 * k, b, .12, pan=-.2)
        place(wet, W(15.45) + .06 * k, b, .08)
    place(s, W(15.9), pop(460, 1000), .18)
    place(s, W(16.55), whoosh(.4, up=False, vel=.7), .16)
    # harga coret = jangkar; "Cek toko lain? Ah, males"
    place(s, W(17.0), whoosh(.5), .25)
    place(s, W(17.6), riser(.8, .4), .07)
    place(s, W(19.3), pop(300, 220, .14, .7), .16)                       # nada turun: "males"
    # jempol menutup harga coret, meter turun
    place(s, W(21.5), whoosh(.5, vel=.8), .22, pan=.2)
    place(s, W(22.2), fft_band(tap(), hi=6000), .3, pan=.2)
    place(s, W(22.2), impact(.5, low=50, d=.6), .35)
    for k, m in enumerate((84, 79, 76)):                                 # meter "kerasa untung" turun
        b = bell(mtof(m), .8, .5, ratio=2.0)
        place(s, W(22.3) + .12 * k, b, .07)
    place(s, W(22.8), pop(460, 1000), .2)
    for k, m in enumerate((84, 88, 91)):
        b = bell(mtof(m), 1.2, .6, ratio=2.0)
        place(s, W(22.85) + .06 * k, b, .1)
        place(wet, W(22.85) + .06 * k, b, .08)
    place(s, W(25.15), whoosh(.4, up=False, vel=.7), .16)
    # mau checkout apa?
    place(s, W(25.6), whoosh(.5), .25, pan=-.3)
    for i in range(4):
        place(s, W(26.0 + i * .2), pop(460 + 50 * i, 1000 + 80 * i, .1, .7), .15, pan=.3)
    place(s, W(26.8), whoosh(.35, vel=.6), .14)
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
