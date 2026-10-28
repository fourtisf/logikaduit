# Musik latar dan efek suara original untuk video EP4 (antre makanan viral). Semua disintesis (bebas hak cipta),
# instrumennya ada di audio_lib.py. Waktu efek suara mengikuti timeline di ep04-antre-viral.html.
# Pakai: python3 video/ep04-audio.py <folder-output> [warp.json]   -> music.wav dan sfx.wav (48 kHz, stereo)
# warp.json (dari ep04-mix.py) menggeser semua waktu supaya cocok dengan video yang temponya disesuaikan voice over.
import sys
import numpy as np
from audio_lib import *   # noqa: F401,F403  (SR, rng, instrumen, efek, place, reverb, ...)

DUR = 48.0
N = int(SR * DUR)
BEAT = 0.55              # 109 BPM; satu bar 2,2 detik, punchline "biasa aja" (2,6 detik) jatuh tepat di awal bar
BAR = 4 * BEAT
OUT = 43.8               # awal penutup
W = Winv = lambda t: t   # diganti timeline() di bawah kalau ada warp.json


# ---------------- aransemen musik ----------------
CHORDS = {   # (bass, nada akor)
    'Am9': (45, [55, 59, 60, 64]), 'Fmaj9': (41, [57, 60, 64, 67]), 'Cmaj9': (36, [55, 59, 62, 64]), 'G6': (43, [59, 62, 64, 67]),
}
PROG = ['Am9', 'Fmaj9', 'Cmaj9', 'G6']


def section(t):
    """Intensitas per bagian video."""
    if t < 2.6: return 'hook'          # pertanyaan pembuka, jam antre berputar
    if t < 4.8: return 'full'          # "rasanya biasa aja"
    if t < 11.8: return 'light'        # dua warung
    if t < 13.0: return 'drop'         # pindah ke New York
    if t < 20.0: return 'light'        # eksperimen 1 orang
    if t < 22.6: return 'build'        # 15 orang menatap, menuju 40%
    if t < 26.4: return 'full'         # 40%, sepuluh kali lipat
    if t < 28.8: return 'break'        # "nggak ada apa-apa": musik diam, jangkrik
    if t < 33.0: return 'full'         # antrean makin panjang
    if t < 39.4: return 'after'        # label terlaris
    if t < OUT - .4: return 'full'     # tips
    return 'outro'


def music():
    dry = np.zeros((N, 2))
    wet_send = np.zeros((N, 2))
    g0 = W(2.6) - BAR                      # grid bar digeser supaya punchline jatuh di awal bar
    b = -1
    while g0 + b * BAR < DUR:
        t0 = g0 + b * BAR
        b += 1
        sec = section(Winv(t0 + 0.01))
        name = PROG[(b - 1) % 4] if sec != 'outro' else ('Fmaj9' if t0 < W(OUT) else 'Cmaj9')
        root, notes = CHORDS[name]
        # piano: pukulan di ketukan 1, "and" ketukan 2, dan ketukan 4
        if sec not in ('break', 'outro'):
            hits = [(0, 1.5, .9), (1.5, 1.5, .55), (3, 1.0, .65)] if sec != 'drop' else [(0, 4, .7)]
            for beat, ln, v in hits:
                for k, m in enumerate(notes):
                    s = rhodes(mtof(m), ln * BEAT + .25, v * (0.9 if k else 1.0))
                    place(dry, t0 + beat * BEAT + .006 * k, s, .21)
                    place(wet_send, t0 + beat * BEAT + .006 * k, s, .05)
        # bass
        if sec in ('full', 'build', 'after', 'light', 'hook'):
            v = {'full': 1, 'build': 1, 'after': .7, 'light': .55, 'hook': .8}[sec]
            for beat, ln, oc in [(0, 1.25, 0), (1.75, .5, 0), (2.5, 1.0, 0), (3.5, .45, 12)]:
                place(dry, t0 + beat * BEAT, bass(mtof(root + oc), ln * BEAT, v), .30)
        # drum
        for i in range(8):                 # hi-hat 1/8 dengan swing
            pos = (i // 2) + (0.58 if i % 2 else 0)
            tt = t0 + pos * BEAT
            s = section(Winv(tt))
            if s in ('drop', 'break', 'outro'):
                continue
            v = (.7 if i % 2 == 0 else .42) * {'light': .7, 'hook': .8, 'after': .8}.get(s, 1)
            place(dry, tt, hat(v, open_=(i == 7 and s == 'full')), .22, pan=.25)
        for beat in (0, 1.75, 2.5):
            tt = t0 + beat * BEAT
            s = section(Winv(tt))
            if s in ('full', 'hook', 'build') or (s in ('light', 'after') and beat == 0):
                place(dry, tt, kick(.9 if beat == 0 else .6), .42 if s != 'light' else .28)
        for beat in (1, 3):
            tt = t0 + beat * BEAT
            s = section(Winv(tt))
            if s in ('full', 'build'):
                sn = snare(.8)
                place(dry, tt, sn, .3, pan=-.1)
                place(wet_send, tt, sn, .06)
    # drum roll menjelang 40% (21,6 - 22,55 detik), makin rapat
    r0, r1 = W(21.6), W(22.55)
    tt = r0
    while tt < r1:
        p = (tt - r0) / (r1 - r0)
        place(dry, tt, snare(.35 + .5 * p), .22, pan=-.1)
        tt += 0.14 * (1 - .65 * p) * (r1 - r0) / 0.95
    # melodi lonceng saat eksperimen New York (rasa penasaran)
    for tt, m in [(14.4, 76), (14.95, 79), (15.5, 81), (16.05, 79), (16.6, 76), (17.7, 74), (18.25, 76), (18.8, 79), (19.35, 84)]:
        s = bell(mtof(m), 1.4, .5)
        place(dry, W(tt), s, .10, pan=.3)
        place(wet_send, W(tt), s, .12)
    # "nggak ada apa-apa": hanya pad rendah yang nyaris tak terdengar
    pd = pad([45, 52, 57, 60], W(28.9) - W(26.3), .8)
    place(dry, W(26.3), pd, .22)
    place(wet_send, W(26.3), pd, .12)
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


# ---------------- bunyi khusus episode ini ----------------
def fades(n, sec=.4):
    i = np.arange(n)
    return np.minimum(1, np.minimum(i, n - i) / (sec * SR))


def murmur(d, voices=8):
    """Riuh orang mengobrol di antrean: noise di rentang suara manusia, dipotong-potong seperti suku kata."""
    n = int(d * SR)
    out = np.zeros((n, 2))
    for v in range(voices):
        x = fft_band(rng.standard_normal(n), lo=220 + 40 * v, hi=1600 + 120 * v)
        k = int(SR / (3 + 3 * rng.random()))              # 3-6 suku kata per detik
        env = np.repeat(rng.random(n // k + 2) ** 2, k)[:n]
        env = np.convolve(env, np.ones(2400) / 2400, mode='same')
        a = (rng.uniform(-.7, .7) + 1) * np.pi / 4
        out[:, 0] += x * env * np.cos(a)
        out[:, 1] += x * env * np.sin(a)
    return out * fades(n)[:, None] / (np.abs(out).max() + 1e-9)


def traffic(d):
    """Dengung jalan kota yang jauh."""
    n = int(d * SR)
    x = np.stack([fft_band(rng.standard_normal(n), lo=40, hi=280) for _ in range(2)], 1)
    x *= (.75 + .25 * np.sin(2 * np.pi * .13 * np.arange(n) / SR))[:, None] * fades(n, .6)[:, None]
    return x / (np.abs(x).max() + 1e-9)


def step(vel=1.0):
    t = T(.12)
    s = fft_band(rng.standard_normal(len(t)), lo=80, hi=900) * np.exp(-t / .02) + .6 * np.sin(2 * np.pi * 95 * t) * np.exp(-t / .035)
    return fade_tail(s * vel, 10)


def cricket(vel=1.0):
    """Satu "krik" jangkrik: tiga denyut pendek 4,4 kHz."""
    t = T(.2)
    gate = sum(((t >= a) & (t < a + .022)).astype(float) for a in (0, .04, .08))
    gate = np.convolve(gate, np.hanning(96) / 48, mode='same')
    return fade_tail(np.sin(2 * np.pi * 4400 * t) * (1 + .3 * np.sin(2 * np.pi * 60 * t)) * gate * vel, 10)


# ---------------- efek suara (waktu = timeline video) ----------------
def sfx():
    s = np.zeros((N, 2))
    wet = np.zeros((N, 2))
    # hook: riuh antrean, jam antre berputar makin cepat sampai 2 jam
    place(s, W(0.0), impact(.5, low=40, d=.9), .45)
    place(s, W(0.0), murmur(W(4.8) - W(0.0)), .16)
    tt, k = .2, 0
    while tt < 2.3:
        place(s, W(tt), tick(2300 if k % 2 else 1900, .8), .2, pan=-.15)
        tt += .2 - .15 * min(1, (tt - .2) / 1.3)
        k += 1
    for k, m in enumerate((88, 91)):                             # jam berhenti di 2:00:00
        b = bell(mtof(m), 1.0, .7, ratio=2.0)
        place(s, W(2.35) + .06 * k, b, .12, pan=-.2)
        place(wet, W(2.35) + .06 * k, b, .08)
    place(s, W(2.1), riser(W(2.6) - W(2.1), .5), .25)
    place(s, W(2.6), impact(1.0), .75)                             # kartu rating jatuh: "biasa aja"
    for i in range(3):                                            # tiga bintang
        place(s, W(3.0 + .2 * i), pop(500 + 120 * i, 1100 + 150 * i, .12), .28, pan=.15)
    place(s, W(3.7), pop(700, 380, .18), .2, pan=.2)                # dua bintang kosong
    # dua warung
    place(s, W(4.8), whoosh(.5, up=False), .3)
    place(s, W(4.85), whoosh(.5), .28, pan=-.4)
    place(s, W(5.0), whoosh(.5), .28, pan=.4)
    place(s, W(5.0), murmur(W(11.8) - W(5.0)), .09)
    for k in range(10):                                         # orang di antrean muncul
        place(s, W(5.0 + k * .05), pop(500 + 40 * k, 900 + 40 * k, .08, .6), .1, pan=-.3)
    for k, tt in enumerate((5.9, 6.05)):                        # menu dan harga sama
        b = bell(mtof(88), 1.2, .7)
        place(s, W(tt), b, .12, pan=(-.4 if k == 0 else .4))
        place(wet, W(tt), b, .08)
    place(s, W(6.9), pop(380, 820, .14), .25, pan=.3)              # "kamu" muncul
    place(s, W(7.2), pop(600, 1300, .1), .2, pan=.35)              # tanda tanya
    for k in range(5):                                          # "kamu" berjalan ke antrean
        place(s, W(8.4) + k * (W(9.5) - W(8.4)) / 5, step(.8), .3, pan=.1 - .08 * k)
    place(s, W(10.5), pop(420, 980), .3, pan=-.1)                  # gelembung "pasti enak"
    for k, m in enumerate((84, 88)):
        place(s, W(10.6) + .08 * k, bell(mtof(m), 1.0, .6, ratio=2.0), .1, pan=-.2)
    # New York 1969
    place(s, W(11.75), whoosh(.6, up=False), .3)
    place(s, W(11.8), traffic(W(26.4) - W(11.8)), .22)
    place(s, W(12.0), murmur(W(26.4) - W(12.0)), .07)
    place(s, W(14.3), pop(380, 820, .14), .25, pan=-.2)            # 1 orang menatap
    b = bell(mtof(96), 1.6, .5, ratio=2.0)
    place(s, W(14.6), b, .06, pan=.4)
    place(wet, W(14.6), b, .1)
    for k in range(4):                                          # 4%
        place(s, W(17.65) + k * .12, tick(1800 + 120 * k, .6), .22, pan=-.2)
    for i in range(14):                                         # 14 orang lagi
        place(s, W(20.0 + i * .08), pop(420 + 30 * i, 900 + 50 * i, .09, .7), .12, pan=-.4 + .05 * i)
    place(s, W(20.6), riser(W(22.6) - W(20.6), .9), .4)
    place(s, W(22.6), impact(1.1, low=34, d=1.4), .9)              # 40%
    for k in range(16):
        place(s, W(22.65) + k * .06, tick(1600 + 90 * k, .6), .22, pan=-.2)
    place(s, W(25.0), impact(.6, low=48, d=.8), .45)               # cap "10x lipat"
    place(s, W(25.0), fft_band(rng.standard_normal(int(.12 * SR)), lo=400, hi=4000) * np.exp(-T(.12) / .03), .35, pan=-.3)
    # jendela kosong: hening, lalu jangkrik
    place(s, W(26.4), whoosh(.9, vel=.8), .3)
    for k, tt in enumerate((27.0, 27.5, 28.0)):
        c = cricket()
        place(s, W(tt), c, .1, pan=(.3 if k % 2 else -.3))
        place(wet, W(tt), c, .05)
    # antrean makin panjang
    place(s, W(28.8), whoosh(.55), .3)
    place(s, W(29.0), murmur(W(33.0) - W(29.0)), .14)
    for j in range(16):                                         # tiap orang baru masuk antrean
        place(s, W(29.2 + j * .17 + .9), pop(450 + 25 * j, 900 + 40 * j, .1, .7), .12, pan=.4 - .05 * j)
    # label terlaris
    place(s, W(33.0), whoosh(.5), .3)
    for k in range(2):
        place(s, W(33.55 + .3 * k), impact(.4, low=60, d=.5), .3)
        place(s, W(33.55 + .3 * k), pop(900, 1400, .08), .18, pan=.2)
    place(s, W(35.9), riser(W(36.4) - W(35.9), .5), .2)
    for k in range(12):                                         # +13-20%
        place(s, W(36.6) + k * .075, tick(1800 + 80 * k, .6), .22, pan=.1)
    place(s, W(37.5), bell(mtof(91), 1.2, .7), .12, pan=.3)
    # tips
    place(s, W(39.45), whoosh(.5), .25)
    for k, m in enumerate((79, 86)):
        place(s, W(39.65) + .09 * k, bell(mtof(m), .9, .6, ratio=2.0), .12, pan=.2)
    # penutup: logo, tombol follow muncul lalu ditekan (sama dengan EP3)
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
