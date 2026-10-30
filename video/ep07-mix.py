# Selaraskan voice over EP7 dengan video, lalu mixing akhir (logikanya di mix.py).
#   python3 video/ep07-mix.py prep <suara.zip> <folder>              -> vo.wav dan warp.json
#   python3 video/ep07-mix.py final <video.mp4> <folder> <hasil.mp4>  -> video final dengan musik, efek, dan narasi
from mix import Episode, cli

# sama dengan awal teks layar (CAPS) di ep07-gaji-naik.html
EP7 = Episode(
    cap=[0, 2.2, 5.0, 9.0, 13.0, 17.0, 21.0, 24.0],
    end=28.5,
    pause={0: 0.45},               # jeda sebentar setelah "Kamu pilih mana?" supaya penonton sempat memilih
)

if __name__ == '__main__':
    cli(EP7)
