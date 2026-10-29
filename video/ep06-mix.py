# Selaraskan voice over EP6 dengan video, lalu mixing akhir (logikanya di mix.py).
#   python3 video/ep06-mix.py prep <suara.zip> <folder>              -> vo.wav dan warp.json
#   python3 video/ep06-mix.py final <video.mp4> <folder> <hasil.mp4>  -> video final dengan musik, efek, dan narasi
from mix import Episode, cli

# sama dengan awal teks layar (CAPS) di ep06-snack-mengecil.html
EP6 = Episode(
    cap=[0, 3.0, 8.0, 11.6, 16.0, 19.4, 22.6],
    end=27.0,
)

if __name__ == '__main__':
    cli(EP6)
