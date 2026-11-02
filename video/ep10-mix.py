# Selaraskan voice over EP10 dengan video, lalu mixing akhir (logikanya di mix.py).
#   python3 video/ep10-mix.py prep <suara.zip> <folder>              -> vo.wav dan warp.json
#   python3 video/ep10-mix.py final <video.mp4> <folder> <hasil.mp4>  -> video final dengan musik, efek, dan narasi
from mix import Episode, cli

# sama dengan awal teks layar (CAPS) di ep10-untung-alfamart.html
EP10 = Episode(
    cap=[0, 3.4, 6.4, 11.0, 15.2, 19.6, 22.6],
    end=27.0,
    pause={0: 0.45},               # jeda sebentar setelah "Tebak, Alfamart untung berapa?" supaya penonton sempat menebak
)

if __name__ == '__main__':
    cli(EP10)
