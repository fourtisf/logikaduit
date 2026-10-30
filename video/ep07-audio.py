# Musik latar dan efek suara original untuk video EP7 (gaji naik 5%, kok tetap bokek). Semua disintesis (bebas hak cipta),
# instrumennya ada di audio_lib.py. Waktu efek suara mengikuti timeline di ep07-gaji-naik.html.
# Pakai: python3 video/ep07-audio.py <folder-output> [warp.json]   -> music.wav dan sfx.wav (48 kHz, stereo)
# warp.json (dari ep07-mix.py) menggeser semua waktu supaya cocok dengan video yang temponya disesuaikan voice over.
import sys
import numpy as np
from audio_lib import *   # noqa: F401,F403  (SR, rng, instrumen, efek, place, reverb, ...)

DUR = 28.5
N = int(SR * DUR)
BEAT = 0.55              # 109 BPM; satu bar 2,2 detik, cap "Lebih untung" (7,4 detik) jatuh tepat di awal bar
BAR = 4 * BEAT
OUT = 24.0               # awal penutup
W = Winv = lambda t: t   # diganti timeline() di bawah kalau ada warp.json


# ---------------- aransemen musik ----------------
CHORDS = {   # (bass, nada akor)
    'Am9': (45, [55, 59, 60, 64]), 'Fmaj9': (41, [57, 60, 64, 67]), 'G6': (43, [59, 62, 64, 67]),
    'Em7': (40, [55, 59, 62, 64]), 'Cmaj9': (36, [55, 59, 62, 64]),
}
PROG = ['Am9', 'G6', 'Fmaj9', 'Em7']


def section(t):
    """Intensitas per bagian video (format pendek: hampir selalu penuh)."""
    if t < 2.2: return 'hook'          # kuis dua slip gaji
    if t < 5.0: return 'light'         # harga naik 4%
    if t < 7.4: return 'build'         # diagram naik asli, menuju cap "Lebih untung"
    if t < 13.0: return 'full'         # 2 dari 3 orang
    if t < 14.55: return 'light'       # "+5%" sebelum berubah
    if t < 17.0: return 'full'         # ilusi uang
    if t < 21.0: return 'after'        # rumus
    if t < OUT - .4: return 'light'    # pertanyaan untuk komentar
    return 'outro'


def music():
    dry = np.zeros((N, 2))
    wet_send = np.zeros((N, 2))
    g0 = W(7.4) % BAR - BAR                # grid bar digeser supaya cap "Lebih untung" jatuh di awal bar
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
    # drum roll menjelang cap "Lebih untung" (6,5 - 7,35 detik), makin rapat
    r0, r1 = W(6.5), W(7.35)
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


def glitch(d=.4, vel=1.0):
    """Bunyi "rusak" digital: noise yang dipotong-potong kasar, untuk angka +5% yang berubah jadi +1%."""
    n = int(d * SR)
    x = rng.standard_normal(n)
    gate = np.repeat(rng.random(n // 600 + 1) > .45, 600)[:n].astype(float)
    x = np.round(x * gate * 3) / 3                               # dikasarkan seperti bitcrush
    return fft_band(x, lo=500, hi=7000) * np.exp(-np.arange(n) / (n / 2)) * vel


def sfx():
    s = np.zeros((N, 2))
    wet = np.zeros((N, 2))
    # hook: dua slip gaji, jari ragu-ragu lalu memilih B
    place(s, W(0.0), impact(.55, low=40, d=.9), .5)
    place(s, W(0.0), whoosh(.45, up=False, vel=.6), .25)
    place(s, W(.0), whoosh(.4, vel=.5), .15, pan=-.3)
    place(s, W(.1), whoosh(.4, vel=.5), .15, pan=.3)
    for k, tt in enumerate((.55, 1.05, 1.5)):                      # jari pindah pilihan
        place(s, W(tt), tick(2200 if k % 2 else 1900, .5), .12, pan=(-.3 if k % 2 == 0 else .3))
    place(s, W(1.95), fft_band(tap(), hi=6000), .32, pan=.3)        # memilih B
    for k, m in enumerate((84, 88, 91)):
        b = bell(mtof(m), 1.0, .7, ratio=2.0)
        place(s, W(1.97) + .06 * k, b, .12, pan=.3)
        place(wet, W(1.97) + .06 * k, b, .08)
    # harga naik 4%
    place(s, W(2.5), whoosh(.5), .25, pan=-.3)
    place(s, W(2.6), whoosh(.5), .25, pan=.3)
    for i in range(3):
        place(s, W(3.1 + i * .22), pop(500 + 80 * i, 1000 + 120 * i, .1), .2, pan=.35)
    # diagram naik asli, cap "Lebih untung"
    place(s, W(5.0), whoosh(.5), .3)
    place(s, W(5.6), riser(W(6.6) - W(5.6), .4), .18)
    for k in range(12):
        place(s, W(5.6) + k * (W(6.6) - W(5.6)) / 12, tick(1600 + 90 * k, .5), .14, pan=-.2)
    place(s, W(7.4), impact(1.1, low=34, d=1.4), .9)
    stamp_hit(s, W(7.4), pan=-.3)
    # 2 dari 3 orang
    place(s, W(9.0), whoosh(.5), .28)
    for k in range(20):
        place(s, W(9.9 + k * .055), pop(500 + 20 * k, 900 + 30 * k, .06, .5), .07, pan=-.5 + .05 * k)
    place(s, W(10.9), impact(.5, low=50, d=.7), .35)
    for k, m in enumerate((84, 91)):
        place(s, W(10.95) + .07 * k, bell(mtof(m), 1.2, .6, ratio=2.0), .1, pan=.2)
    # ilusi uang: +5% berubah jadi +1%
    place(s, W(13.0), whoosh(.6), .3)
    place(s, W(13.0), impact(.5, low=36, d=1.2), .35)
    place(s, W(13.9), riser(W(14.3) - W(13.9), .5), .2)
    place(s, W(14.3), glitch(W(14.75) - W(14.3)), .3)
    place(s, W(14.55), impact(.9, low=36, d=1.2), .7)
    place(s, W(15.0), whoosh(.4), .18, pan=.2)
    # rumus
    place(s, W(17.0), whoosh(.5), .28)
    for k, tt in enumerate((17.6, 18.3, 19.1)):
        place(s, W(tt), pop(420 + 100 * k, 900 + 150 * k, .1), .22, pan=-.3 + .3 * k)
    for k, m in enumerate((86, 91)):
        b = bell(mtof(m), 1.4, .7, ratio=2.0)
        place(s, W(19.15) + .07 * k, b, .12, pan=.3)
        place(wet, W(19.15) + .07 * k, b, .1)
    # pertanyaan untuk komentar
    place(s, W(21.0), whoosh(.5), .25)
    for i in range(4):
        place(s, W(21.5 + i * .12), pop(500 + 60 * i, 1000 + 80 * i, .08, .6), .14, pan=-.3 + .2 * i)
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
