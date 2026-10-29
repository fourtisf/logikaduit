# Selaraskan voice over EP5 dengan video, lalu mixing akhir (logikanya di mix.py).
#   python3 video/ep05-mix.py prep <suara.zip> <folder>              -> vo.wav dan warp.json
#   python3 video/ep05-mix.py final <video.mp4> <folder> <hasil.mp4>  -> video final dengan musik, efek, dan narasi
from mix import Episode, cli

# sama dengan awal teks layar (CAPS) di ep05-mixue.html
EP5 = Episode(
    cap=[0, 3.2, 7.4, 11.0, 14.4, 17.6, 20.8],
    end=25.0,
)

if __name__ == '__main__':
    cli(EP5)
