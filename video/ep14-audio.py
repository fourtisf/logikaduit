# Musik latar dan efek suara original untuk video EP14 (lapar, kok belanjanya kalap?). Semua disintesis (bebas hak cipta),
# instrumennya ada di audio_lib.py. Waktu efek suara mengikuti timeline di ep14-lapar-kalap.html.
# Pakai: python3 video/ep14-audio.py <folder-output> [warp.json]   -> music.wav dan sfx.wav (48 kHz, stereo)
# warp.json (dari ep14-mix.py) menggeser semua waktu supaya cocok dengan video yang temponya disesuaikan voice over.
import sys
import numpy as np
from audio_lib import *   # noqa: F401,F403  (SR, rng, instrumen, efek, place, reverb, ...)

DUR = 31.5
N = int(SR * DUR)
BEAT = 0.5               # 120 BPM, lebih ceria dan memantul; kartu trik (2,75 detik) jatuh tepat di awal bar
BAR = 4 * BEAT
OUT = 27.0               # awal penutup
W = Winv = lambda t: t   # diganti timeline() di bawah kalau ada warp.json


# ---------------- aransemen musik ----------------
CHORDS = {   # (bass, nada akor)
    'Am9': (45, [55, 59, 60, 64]), 'Fmaj9': (41, [57, 60, 64, 67]), 'G6': (43, [59, 62, 64, 67]),
    'Em7': (40, [55, 59, 62, 64]), 'Cmaj9': (36, [55, 59, 62, 64]),
}
PROG = ['Cmaj9', 'Am9', 'Fmaj9', 'G6']   # progresi mayor yang ceria


def section(t):
    """Intensitas per bagian video."""
    if t < 2.2: return 'hook'          # perut keroncongan, keranjang penuh
    if t < 2.75: return 'build'        # menuju kartu trik
    if t < 4.6: return 'full'          # "Coba trik ini: makan dulu"
    if t < 9.0: return 'light'         # riset 2015: struk pembeli toserba
    if t < 10.9: return 'build'        # struk lapar memanjang
    if t < 13.6: return 'full'         # cap "+64%"
    if t < 18.0: return 'after'        # penjepit kertas
    if t < 19.0: return 'build'        # menuju "mode pengin dapet sesuatu"
    if t < 22.0: return 'full'         # magnet menarik barang
    if t < OUT - .4: return 'after'    # tantangan: hapus isi keranjang
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
    # drum roll menjelang kartu trik (2,2 - 2,7) dan menjelang cap "+64%" (10,35 - 10,85), makin rapat
    for a0, a1 in ((2.2, 2.7), (10.35, 10.85)):
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


def growl(d=.7, vel=1.0):
    """Perut keroncongan: nada rendah yang bergelombang dengan sedikit desis."""
    t = T(d)
    f = 95 + 35 * np.sin(2 * np.pi * 7 * t) + 25 * np.sin(2 * np.pi * 2.3 * t)
    body = np.sin(2 * np.pi * np.cumsum(f) / SR) * (1 + .5 * np.sin(2 * np.pi * 13 * t))
    gurgle = fft_band(rng.standard_normal(len(t)), lo=150, hi=900) * .25
    env = np.sin(np.pi * np.clip(t / d, 0, 1)) ** .7
    return fade_tail((body + gurgle) * env * vel, 20)


def printer(d=.6, vel=1.0):
    """Printer struk: deretan klik cepat bernada."""
    out = np.zeros(int(d * SR))
    k = 0
    for tt in np.arange(0, d - .02, 1 / 38):
        c = fft_band(rng.standard_normal(int(.012 * SR)), lo=1500, hi=7000) * np.exp(-T(.012) / .003)
        i = int(tt * SR)
        out[i:i + len(c)] += c[:len(out) - i] * (.8 if k % 2 else 1)
        k += 1
    return out * vel


def sfx():
    s = np.zeros((N, 2))
    wet = np.zeros((N, 2))
    # hook: perut keroncongan, barang masuk keranjang
    place(s, W(0.0), impact(.5, low=40, d=.9), .45)
    place(s, W(0.05), growl(.75, .9), .3, pan=-.3)
    place(s, W(1.25), growl(.6, .8), .26, pan=-.3)
    for k, c in enumerate((.7, 1.2, 1.7)):
        place(s, W(c), pop(500 + 50 * k, 1100 + 60 * k, .1, .8), .18, pan=.35)
        place(s, W(c + .05), clink(.55), .06, pan=.35)
    place(s, W(2.75), impact(1.0, low=34, d=1.4), .8)                   # "Coba trik ini"
    place(s, W(2.75), whoosh(.45), .2)
    for k, m in enumerate((84, 88, 91, 96)):
        b = bell(mtof(m), 1.2, .6, ratio=2.0)
        place(s, W(2.8) + .05 * k, b, .1, pan=.2)
        place(wet, W(2.8) + .05 * k, b, .08)
    place(s, W(4.15), whoosh(.4, up=False, vel=.7), .16)
    # riset 2015: toserba, struk tercetak, kaca pembesar
    place(s, W(4.6), whoosh(.5), .25)
    for k, tt in enumerate((5.4, 5.7, 6.0)):
        place(s, W(tt), printer(.55, .8), .07, pan=(-.4, 0, .4)[k])
    place(s, W(6.6), riser(W(8.4) - W(6.6), .3), .06)
    place(s, W(7.0), pop(420, 980), .2)
    place(s, W(8.55), whoosh(.4, up=False, vel=.7), .16)
    # kenyang vs lapar: struk lapar memanjang, cap +64%
    place(s, W(9.0), whoosh(.5), .25)
    place(s, W(9.1), pop(400, 820, .1, .6), .12, pan=-.35)
    place(s, W(9.4), pop(440, 880, .1, .6), .12, pan=.35)
    place(s, W(9.6), printer(W(10.6) - W(9.6), .9), .08, pan=.35)
    place(s, W(10.9), impact(1.1, low=34, d=1.4), .9)
    stamp_hit(s, W(10.92), pan=.3)
    for k, m in enumerate((88, 91, 96)):
        b = bell(mtof(m), 1.2, .7, ratio=2.0)
        place(s, W(10.95) + .06 * k, b, .12, pan=.3)
        place(wet, W(10.95) + .06 * k, b, .08)
    place(s, W(12.0), pop(460, 1000), .2)
    place(s, W(13.15), whoosh(.4, up=False, vel=.7), .16)
    # penjepit kertas berpindah dari toples ke tumpukan
    place(s, W(13.6), whoosh(.5), .25)
    place(s, W(13.7), pop(380, 760, .1, .6), .12, pan=-.4)
    for i in range(16):
        place(s, W(14.4 + i * .12 + .5), tick(3200 + 60 * (i % 5), .5), .06, pan=.2)
        place(s, W(14.4 + i * .12 + .5), clink(.35), .03, pan=.2)
    place(s, W(16.6), pop(360, 1400, .16, .9), .2, pan=.2)              # "Bisa dimakan?"
    place(s, W(17.55), whoosh(.4, up=False, vel=.7), .16)
    # mode pengin dapet sesuatu: magnet menyala, barang tertarik
    place(s, W(18.0), whoosh(.5), .25)
    place(s, W(18.4), pop(420, 900), .18)
    place(s, W(19.0), fft_band(tap(), hi=6000), .3)                       # sakelar dinyalakan
    place(s, W(19.02), impact(.8, low=40, d=1.0), .6)
    place(s, W(19.0), riser(W(20.9) - W(19.0), .5), .1)
    for i in range(12):
        place(s, W(19.2 + i * .14), whoosh(.3, vel=.4), .05, pan=(-.5 if i % 2 else .5))
        place(s, W(19.2 + i * .14 + .9), clink(.4), .04)
    place(s, W(21.55), whoosh(.4, up=False, vel=.7), .16)
    # tantangan: makan dulu, hapus isi keranjang
    place(s, W(22.0), whoosh(.5), .25, pan=-.3)
    place(s, W(22.3), pop(420, 900), .16, pan=.3)
    for k, tt in enumerate((23.2, 23.6, 24.0, 24.4)):
        place(s, W(tt), whoosh(.25, up=False, vel=.5), .1, pan=.35)
        place(s, W(tt + .3), tick(1800 - 120 * k, .6), .1, pan=.35)
    place(s, W(24.8), pop(460, 1000), .2)
    for k, m in enumerate((84, 88, 91)):
        b = bell(mtof(m), 1.2, .6, ratio=2.0)
        place(s, W(24.85) + .06 * k, b, .1)
        place(wet, W(24.85) + .06 * k, b, .08)
    place(s, W(25.4), whoosh(.35, vel=.6), .14)
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
