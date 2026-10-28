# Selaraskan voice over EP4 dengan video, lalu mixing akhir (logikanya di mix.py).
#   python3 video/ep04-mix.py prep <suara.zip> <folder>              -> vo.wav dan warp.json
#   python3 video/ep04-mix.py final <video.mp4> <folder> <hasil.mp4>  -> video final dengan musik, efek, dan narasi
from mix import Episode, cli

# sama dengan awal teks layar (CAPS) di ep04-antre-viral.html
EP4 = Episode(
    cap=[0, 2.6, 4.8, 8.2, 11.8, 14.2, 17.6, 20.0, 22.6, 26.4, 28.8, 33.0, 34.8, 39.4, 43.8],
    end=48.0,
    pause={2: 0.7, 8: 0.45},       # jeda lebih panjang: setelah "Kamu pilih yang mana?" dan sebelum "nggak ada kejadian apa-apa"
)

if __name__ == '__main__':
    cli(EP4)
