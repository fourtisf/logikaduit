# Selaraskan voice over EP3 dengan video, lalu mixing akhir (logikanya di mix.py).
#   python3 video/ep03-mix.py prep <suara.zip> <folder>              -> vo.wav dan warp.json
#   python3 video/ep03-mix.py final <video.mp4> <folder> <hasil.mp4>  -> video final dengan musik, efek, dan narasi
from mix import Episode, cli

EP3 = Episode(
    cap=[0, 2.2, 4.8, 6.6, 8.15, 10.6, 13.5, 16.5, 19.0, 21.5, 24.5, 27.5, 31.0, 34.0, 38.0],
    end=42.0,
    pause={5: 0.6, 7: 0.6},        # jeda lebih panjang: setelah "Kamu pilih yang mana?" dan sebelum "Yang biasa jadi gratis"
    marks=[(18.6, 7)],              # cap "Gratis" jatuh tepat setelah "diturunkan satu sen"
)

if __name__ == '__main__':
    cli(EP3)
