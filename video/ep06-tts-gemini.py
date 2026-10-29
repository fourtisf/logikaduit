#!/usr/bin/env python3
# Naskah narasi EP6 (isi snack makin kecil) untuk Gemini TTS. Cara kerja dan pencarian API key: lihat tts_gemini.py.
# Pakai:
#   python3 video/ep06-tts-gemini.py               # suara default: Puck
#   python3 video/ep06-tts-gemini.py --voice Leda  # suara lain
# Hasil: zip berisi 01.wav ... 07.wav, full.wav, dan lines.json (lokasi: LD_TTS_OUT, default /root/logikaduit-ep06-suara.zip).
import tts_gemini

LINES = [
    "Harga snack kamu nggak naik. Isinya yang dikurangin.",
    "Dulu seratus gram, sekarang delapan puluh. Harganya sama, tapi per gram naik dua puluh lima persen.",
    "Kenapa nggak naikin harga aja? Karena isi yang berkurang jarang kita sadari.",
    "Riset belanja es krim di Chicago: pembeli empat kali lebih peka sama harga naik daripada isi yang dikurangi.",
    "Jadi cek beratnya, bukan cuma harganya.",
    "Snack apa yang menurutmu makin kecil? Tulis di komentar!",
    "Biar nggak gampang ketipu harga, follow Logika Duit!",
]

if __name__ == "__main__":
    tts_gemini.main(LINES, "/root/logikaduit-ep06-suara.zip")
