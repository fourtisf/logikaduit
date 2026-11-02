# Musik latar dan efek suara original untuk video EP9 (tanggal muda boros, tanggal tua mi instan). Semua disintesis
# (bebas hak cipta), instrumennya ada di audio_lib.py. Waktu efek suara mengikuti timeline di ep09-tanggal-tua.html.
# Pakai: python3 video/ep09-audio.py <folder-output> [warp.json]   -> music.wav dan sfx.wav (48 kHz, stereo)
# warp.json (dari ep09-mix.py) menggeser semua waktu supaya cocok dengan video yang temponya disesuaikan voice over.
import sys
import numpy as np
from audio_lib import *   # noqa: F401,F403  (SR, rng, instrumen, efek, place, reverb, ...)

DUR = 27.5
N = int(SR * DUR)
BEAT = 0.55              # 109 BPM; satu bar 2,2 detik, cap "Bokek" (2,75 detik) jatuh tepat di awal bar
BAR = 4 * BEAT
OUT = 23.0               # awal penutup
W = Winv = lambda t: t   # diganti timeline() di bawah kalau ada warp.json


# ---------------- aransemen musik ----------------
CHORDS = {   # (bass, nada akor)
    'Am9': (45, [55, 59, 60, 64]), 'Fmaj9': (41, [57, 60, 64, 67]), 'G6': (43, [59, 62, 64, 67]),
    'Em7': (40, [55, 59, 62, 64]), 'Cmaj9': (36, [55, 59, 62, 64]),
}
PROG = ['Am9', 'Fmaj9', 'G6', 'Em7']


def section(t):
    """Intensitas per bagian video (format pendek: hampir selalu penuh)."""
    if t < 1.9: return 'hook'          # saldo terkuras, kalender berjalan
    if t < 2.75: return 'build'        # menuju cap "Bokek"
    if t < 3.6: return 'full'
    if t < 7.2: return 'light'         # grafik belanja
    if t < 11.2: return 'full'         # kalori turun 10-15%
    if t < 15.4: return 'light'        # bias masa kini
    if t < 20.0: return 'full'         # 4 jatah mingguan
    if t < OUT - .4: return 'after'    # pertanyaan untuk komentar
    return 'outro'


def music():
    dry = np.zeros((N, 2))
    wet_send = np.zeros((N, 2))
    g0 = W(2.75) % BAR - BAR               # grid bar digeser supaya cap "Bokek" jatuh di awal bar
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
    # drum roll menjelang cap "Bokek" (1,9 - 2,7 detik), makin rapat
    r0, r1 = W(1.9), W(2.7)
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


def day_steps():
    """Waktu tiap pergantian tanggal di kalender hook (16 langkah, gerak ease-in-out antara 0,35 dan 2,6 detik)."""
    eio = lambda p: 4 * p ** 3 if p < .5 else 1 - (-2 * p + 2) ** 3 / 2
    out = []
    for k in range(1, 17):
        lo, hi = 0.0, 1.0
        for _ in range(40):                                       # cari p dengan eio(p) = k/16
            mid = (lo + hi) / 2
            lo, hi = (mid, hi) if eio(mid) < k / 16 else (lo, mid)
        out.append(.35 + lo * 2.25)
    return out


def sfx():
    s = np.zeros((N, 2))
    wet = np.zeros((N, 2))
    # hook: tanggal berjalan dari 25 ke 10, pengeluaran beterbangan, saldo habis
    place(s, W(0.0), impact(.55, low=40, d=.9), .5)
    place(s, W(0.0), whoosh(.45, up=False, vel=.6), .25)
    for k, tt in enumerate(day_steps()):
        place(s, W(tt), tick(2300 if k % 2 else 1900, .6), .16, pan=-.15)
    for i in range(7):                                            # pengeluaran
        place(s, W(.45 + i * .3), pop(950, 480, .12, .8), .18, pan=(-.4 if i % 2 == 0 else .4))
    place(s, W(2.75), impact(1.1, low=34, d=1.4), .9)             # cap "Bokek"
    stamp_hit(s, W(2.75))
    place(s, W(2.85), pop(600, 220, .3), .2, pan=.3)
    # grafik belanja
    place(s, W(3.6), whoosh(.5), .28)
    place(s, W(4.1), whoosh(1.2, vel=.6), .16, pan=-.3)
    place(s, W(4.4), pop(420, 980), .25, pan=-.3)                 # "Uang masuk"
    for k, m in enumerate((84, 88)):
        place(s, W(4.45) + .07 * k, bell(mtof(m), 1.0, .6, ratio=2.0), .1, pan=-.3)
    # kalori turun
    place(s, W(7.2), whoosh(.5), .28, pan=-.3)
    place(s, W(7.5), whoosh(.5), .28, pan=.3)
    place(s, W(8.9), impact(.7, low=44, d=.9), .5)
    for k in range(12):
        place(s, W(8.9) + k * (W(9.6) - W(8.9)) / 12, tick(1500 + 70 * k, .55), .16, pan=.2)
    # timbangan bias masa kini
    place(s, W(11.2), whoosh(.5), .28)
    place(s, W(12.0), whoosh(.6, up=False, vel=.6), .2, pan=-.4)
    place(s, W(12.55), impact(.6, low=50, d=.8), .45, pan=-.3)    # balok miring ke "senang sekarang"
    for k, m in enumerate((79, 84, 91)):
        b = bell(mtof(m), 1.4, .55, ratio=2.0)
        place(s, W(12.6) + .08 * k, b, .09, pan=-.3)
        place(wet, W(12.6) + .08 * k, b, .1)
    # gaji dibagi 4 jatah mingguan
    place(s, W(15.4), whoosh(.5), .28)
    place(s, W(16.3), pop(500, 1100, .12), .22)
    for i in range(4):
        place(s, W(16.5 + i * .15), whoosh(.35, vel=.6), .14, pan=(-.4 if i % 2 == 0 else .4))
        place(s, W(16.9 + i * .15), slap(.7), .22, pan=(-.4 if i % 2 == 0 else .4))
    for k, m in enumerate((84, 88, 91, 96)):                     # "tanggal tua tetap aman"
        b = bell(mtof(m), 1.2, .7, ratio=2.0)
        place(s, W(18.4) + .06 * k, b, .12, pan=.2)
        place(wet, W(18.4) + .06 * k, b, .1)
    # pertanyaan untuk komentar
    place(s, W(20.0), whoosh(.5), .25)
    for i in range(4):
        place(s, W(20.5 + i * .12), pop(500 + 60 * i, 1000 + 80 * i, .08, .6), .14, pan=-.3 + .2 * i)
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
