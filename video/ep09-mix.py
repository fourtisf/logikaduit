# Selaraskan voice over EP9 dengan video, lalu mixing akhir (logikanya di mix.py).
#   python3 video/ep09-mix.py prep <suara.zip> <folder>              -> vo.wav dan warp.json
#   python3 video/ep09-mix.py final <video.mp4> <folder> <hasil.mp4>  -> video final dengan musik, efek, dan narasi
from mix import Episode, cli

# sama dengan awal teks layar (CAPS) di ep09-tanggal-tua.html
EP9 = Episode(
    cap=[0, 3.6, 7.2, 11.2, 15.4, 20.0, 23.0],
    end=27.5,
)

if __name__ == '__main__':
    cli(EP9)
