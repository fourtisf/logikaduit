# Selaraskan voice over EP15 dengan video, lalu mixing akhir (logikanya di mix.py).
#   python3 video/ep15-mix.py prep <suara.zip> <folder>              -> vo.wav dan warp.json
#   python3 video/ep15-mix.py final <video.mp4> <folder> <hasil.mp4>  -> video final dengan musik, efek, dan narasi
from mix import Episode, cli

# sama dengan awal teks layar (CAPS) di ep15-harga-coret.html
EP15 = Episode(
    cap=[0, 4.6, 8.4, 12.6, 17.0, 21.4, 25.6, 29.4],
    end=34.0,
    pause={0: 0.3},                # jeda sebentar setelah hook supaya kartu trik sempat terbaca
    max_pause=0.26,                # Achird banyak jeda napas di tengah kalimat; dipendekkan supaya video tetap padat
    speed=1.05,
)

if __name__ == '__main__':
    cli(EP15)
