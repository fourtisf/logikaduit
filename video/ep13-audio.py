# Musik latar dan efek suara original untuk video EP13 (bayar QRIS, kok lebih boros?). Semua disintesis (bebas hak cipta),
# instrumennya ada di audio_lib.py. Waktu efek suara mengikuti timeline di ep13-qris-boros.html.
# Pakai: python3 video/ep13-audio.py <folder-output> [warp.json]   -> music.wav dan sfx.wav (48 kHz, stereo)
# warp.json (dari ep13-mix.py) menggeser semua waktu supaya cocok dengan video yang temponya disesuaikan voice over.
import sys
import numpy as np
from audio_lib import *   # noqa: F401,F403  (SR, rng, instrumen, efek, place, reverb, ...)

DUR = 35.5
N = int(SR * DUR)
BEAT = 0.55              # 109 BPM; satu bar 2,2 detik, kartu trik (2,75 detik) jatuh tepat di awal bar
BAR = 4 * BEAT
OUT = 31.0               # awal penutup
W = Winv = lambda t: t   # diganti timeline() di bawah kalau ada warp.json


# ---------------- aransemen musik ----------------
CHORDS = {   # (bass, nada akor)
    'Am9': (45, [55, 59, 60, 64]), 'Fmaj9': (41, [57, 60, 64, 67]), 'G6': (43, [59, 62, 64, 67]),
    'Em7': (40, [55, 59, 62, 64]), 'Cmaj9': (36, [55, 59, 62, 64]),
}
PROG = ['Fmaj9', 'G6', 'Am9', 'Em7']


def section(t):
    """Intensitas per bagian video."""
    if t < 2.2: return 'hook'          # scan, scan, scan... saldo terkuras
    if t < 2.75: return 'build'        # menuju kartu trik
    if t < 4.6: return 'full'          # "Coba trik ini: seminggu bayar tunai"
    if t < 8.6: return 'light'         # scan, bip, nggak kerasa
    if t < 12.6: return 'after'        # riset 2001: lelang tiket basket
    if t < 15.4: return 'build'        # tawaran tunai vs kartu
    if t < 17.0: return 'full'         # cap "Hampir 2x lipat"
    if t < 22.0: return 'light'        # rasa sakit membayar
    if t < 27.0: return 'full'         # 71 penelitian
    if t < OUT - .4: return 'after'    # tantangan seminggu
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
    # drum roll menjelang kartu trik (2,2 - 2,7) dan menjelang cap "Hampir 2x lipat" (14,85 - 15,35), makin rapat
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


def beep(f=1900, d=.09, vel=1.0):
    """Bunyi "bip" mesin pembayaran: nada sinus pendek dengan sedikit harmonik."""
    t = T(d)
    tone = np.sin(2 * np.pi * f * t) + .25 * np.sin(2 * np.pi * 2 * f * t)
    return fade_tail(tone * np.clip(t / .004, 0, 1) * np.exp(-t / (d * .9)) * vel, 8)


def sfx():
    s = np.zeros((N, 2))
    wet = np.zeros((N, 2))
    # hook: scan QR berkali-kali, saldo terkuras tanpa terasa
    place(s, W(0.0), impact(.55, low=40, d=.9), .5)
    place(s, W(0.0), whoosh(.45, up=False, vel=.6), .25)
    for k, c in enumerate((.35, .85, 1.35, 1.85)):
        place(s, W(c - .28), riser(.25, .35), .05, pan=.35)               # garis pindai menyapu
        place(s, W(c), beep(1900 + 60 * k, .09, .8), .16, pan=.35)
        place(s, W(c + .1), beep(2500 + 60 * k, .07, .6), .1, pan=.35)
        place(s, W(c + .05), pop(480 + 40 * k, 1050 + 50 * k, .1, .7), .14, pan=.15)
    place(s, W(2.75), impact(1.0, low=34, d=1.4), .8)                   # "Coba trik ini"
    place(s, W(2.75), whoosh(.45), .2)
    for k, m in enumerate((84, 88, 91, 96)):
        b = bell(mtof(m), 1.2, .6, ratio=2.0)
        place(s, W(2.8) + .05 * k, b, .1, pan=.2)
        place(wet, W(2.8) + .05 * k, b, .08)
    place(s, W(4.15), whoosh(.4, up=False, vel=.7), .16)
    # scan, bip, selesai
    place(s, W(4.6), whoosh(.5), .25, pan=.3)
    place(s, W(4.9), riser(W(5.7) - W(4.9), .4), .07, pan=.3)
    place(s, W(5.7), beep(1900, .1, .9), .2, pan=.3)
    place(s, W(5.82), beep(2500, .09, .7), .14, pan=.3)
    for k, m in enumerate((88, 91, 96)):
        b = bell(mtof(m), 1.0, .5, ratio=2.0)
        place(s, W(5.75) + .06 * k, b, .08, pan=.3)
        place(wet, W(5.75) + .06 * k, b, .08)
    place(s, W(8.15), whoosh(.4, up=False, vel=.7), .16)
    # riset 2001: tiket basket dilelang, palu diketuk
    place(s, W(8.6), whoosh(.5), .25)
    place(s, W(9.3), whoosh(.3, vel=.5), .12, pan=.4)
    place(s, W(9.76), impact(.8, low=60, d=.5), .6, pan=.3)
    place(s, W(9.76), fft_band(tap(), lo=200, hi=3000), .4, pan=.3)
    place(s, W(10.2), pop(420, 980), .2)
    place(s, W(12.15), whoosh(.4, up=False, vel=.7), .16)
    # tawaran tunai vs kartu
    place(s, W(12.6), whoosh(.5), .25)
    place(s, W(13.0), riser(.7, .4), .08, pan=-.3)
    place(s, W(13.5), pop(380, 760, .1, .7), .16, pan=-.3)
    place(s, W(14.0), riser(W(15.1) - W(14.0), .55), .12, pan=.3)
    place(s, W(14.8), pop(520, 1200, .12, .8), .2, pan=.3)
    place(s, W(15.4), impact(1.1, low=34, d=1.4), .9)                    # cap "Hampir 2x lipat"
    stamp_hit(s, W(15.42), pan=-.2)
    for k, m in enumerate((88, 91, 96)):
        b = bell(mtof(m), 1.2, .7, ratio=2.0)
        place(s, W(15.45) + .06 * k, b, .12, pan=.2)
        place(wet, W(15.45) + .06 * k, b, .08)
    place(s, W(16.55), whoosh(.4, up=False, vel=.7), .16)
    # rasa sakit membayar: meter tunai naik tinggi, meter scan nyaris diam
    place(s, W(17.0), whoosh(.5), .22)
    place(s, W(17.1), pop(380, 760, .1, .6), .12, pan=-.35)
    place(s, W(17.3), pop(420, 820, .1, .6), .12, pan=.35)
    place(s, W(18.2), riser(W(19.0) - W(18.2), .6), .12, pan=-.35)
    place(s, W(18.65), impact(.5, low=45, d=.5), .35, pan=-.35)          # "aduh"
    place(s, W(19.0), pop(460, 1000), .2, pan=-.35)
    place(s, W(19.6), bell(mtof(91), .8, .5, ratio=2.0), .08, pan=.35)
    place(s, W(20.2), pop(460, 1000), .18, pan=.35)
    place(s, W(21.55), whoosh(.4, up=False, vel=.7), .16)
    # 71 penelitian
    place(s, W(22.0), whoosh(.5), .25)
    place(s, W(22.1), impact(.8, low=36, d=1.1), .6)
    for i in range(0, 71, 3):
        place(s, W(22.25 + i * .018), tick(2600 + 8 * i, .4), .06, pan=-.5 + i / 71)
    place(s, W(24.0), pop(420, 980), .22)
    for k, m in enumerate((84, 88, 91)):
        b = bell(mtof(m), 1.2, .6, ratio=2.0)
        place(s, W(24.05) + .06 * k, b, .1)
        place(wet, W(24.05) + .06 * k, b, .08)
    place(s, W(26.55), whoosh(.4, up=False, vel=.7), .16)
    # tantangan seminggu: tujuh hari dicentang
    place(s, W(27.0), whoosh(.5), .25, pan=-.3)
    for i in range(7):
        place(s, W(27.7 + i * .22), pop(440 + 45 * i, 980 + 70 * i, .1, .7), .15, pan=.1 + .05 * i)
    place(s, W(28.6), whoosh(.35, vel=.6), .14)
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
