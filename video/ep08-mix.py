# Selaraskan voice over EP8 dengan video, lalu mixing akhir (logikanya di mix.py).
#   python3 video/ep08-mix.py prep <suara.zip> <folder>              -> vo.wav dan warp.json
#   python3 video/ep08-mix.py final <video.mp4> <folder> <hasil.mp4>  -> video final dengan musik, efek, dan narasi
from mix import Episode, cli

# sama dengan awal teks layar (CAPS) di ep08-diskon-bertumpuk.html
EP8 = Episode(
    cap=[0, 3.2, 5.6, 9.0, 14.0, 16.0, 21.5, 24.2],
    end=28.6,
    pause={0: 0.45},               # jeda sebentar setelah "Jadi diskon berapa?" supaya penonton sempat menebak
)

if __name__ == '__main__':
    cli(EP8)
