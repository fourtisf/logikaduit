#!/usr/bin/env python3
# Naskah narasi EP9 (tanggal muda boros, tanggal tua mi instan) untuk Gemini TTS. Cara kerja dan pencarian API key: lihat tts_gemini.py.
# Pakai:
#   python3 video/ep09-tts-gemini.py               # suara default: Achird (sama dengan Ruang Pikir)
#   python3 video/ep09-tts-gemini.py --voice Leda  # suara lain
# Hasil: zip berisi 01.wav ... 07.wav, full.wav, dan lines.json (lokasi: LD_TTS_OUT, default /root/logikaduit-ep09-suara.zip).
import tts_gemini

LINES = [
    "Tanggal dua puluh lima gajian, tanggal sepuluh udah bokek. Kamu juga?",
    "Riset di Amerika: begitu uang bulanan masuk, belanja orang langsung naik.",
    "Riset lain: di minggu terakhir, kalori yang dimakan turun sepuluh sampai lima belas persen.",
    "Namanya bias masa kini: otak lebih mementingkan senang sekarang daripada aman nanti.",
    "Triknya: begitu gajian, langsung bagi jadi empat jatah mingguan. Biar tanggal tua tetap aman.",
    "Biasanya gajimu habis tanggal berapa? Tulis di komentar!",
    "Biar nggak gampang ketipu harga, follow Logika Duit!",
]

if __name__ == "__main__":
    tts_gemini.main(LINES, "/root/logikaduit-ep09-suara.zip")
