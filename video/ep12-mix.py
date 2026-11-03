# Selaraskan voice over EP12 dengan video, lalu mixing akhir (logikanya di mix.py).
#   python3 video/ep12-mix.py prep <suara.zip> <folder>              -> vo.wav dan warp.json
#   python3 video/ep12-mix.py final <video.mp4> <folder> <hasil.mp4>  -> video final dengan musik, efek, dan narasi
from mix import Episode, cli

# sama dengan awal teks layar (CAPS) di ep12-untung-bca.html
EP12 = Episode(
    cap=[0, 4.6, 9.0, 13.4, 17.8, 21.8, 25.0],
    end=29.5,
    pause={0: 0.35},               # jeda sebentar setelah kalimat pembuka supaya penghitung sempat terlihat berjalan
    max_pause=0.26,                # Achird banyak jeda napas di tengah kalimat; dipendekkan supaya video tetap pendek
    speed=1.05,
)

if __name__ == '__main__':
    cli(EP12)
