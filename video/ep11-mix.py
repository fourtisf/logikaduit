# Selaraskan voice over EP11 dengan video, lalu mixing akhir (logikanya di mix.py).
#   python3 video/ep11-mix.py prep <suara.zip> <folder>              -> vo.wav dan warp.json
#   python3 video/ep11-mix.py final <video.mp4> <folder> <hasil.mp4>  -> video final dengan musik, efek, dan narasi
from mix import Episode, cli

# sama dengan awal teks layar (CAPS) di ep11-indomie-alfamart.html
EP11 = Episode(
    cap=[0, 4.6, 8.6, 13.0, 18.0, 22.0, 25.0],
    end=29.5,
    pause={0: 0.45},               # jeda sebentar setelah pertanyaan pembuka supaya penonton sempat menebak
    max_pause=0.26,                # Achird banyak jeda napas di tengah kalimat; dipendekkan supaya video tetap pendek
    speed=1.05,
)

if __name__ == '__main__':
    cli(EP11)
