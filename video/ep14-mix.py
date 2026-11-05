# Selaraskan voice over EP14 dengan video, lalu mixing akhir (logikanya di mix.py).
#   python3 video/ep14-mix.py prep <suara.zip> <folder>              -> vo.wav dan warp.json
#   python3 video/ep14-mix.py final <video.mp4> <folder> <hasil.mp4>  -> video final dengan musik, efek, dan narasi
from mix import Episode, cli

# sama dengan awal teks layar (CAPS) di ep14-lapar-kalap.html
EP14 = Episode(
    cap=[0, 4.6, 9.0, 13.6, 18.0, 22.0, 27.0],
    end=31.5,
    pause={0: 0.3},                # jeda sebentar setelah hook supaya kartu trik sempat terbaca
    max_pause=0.26,                # Achird banyak jeda napas di tengah kalimat; dipendekkan supaya video tetap padat
    speed=1.05,
)

if __name__ == '__main__':
    cli(EP14)
