#!/usr/bin/env python3
# Naskah narasi EP8 (diskon 50% + 20%) untuk Gemini TTS. Cara kerja dan pencarian API key: lihat tts_gemini.py.
# Pakai:
#   python3 video/ep08-tts-gemini.py               # suara default: Puck
#   python3 video/ep08-tts-gemini.py --voice Leda  # suara lain
# Hasil: zip berisi 01.wav ... 08.wav, full.wav, dan lines.json (lokasi: LD_TTS_OUT, default /root/logikaduit-ep08-suara.zip).
import tts_gemini

LINES = [
    "Diskon lima puluh persen, ditambah diskon dua puluh persen. Jadi diskon berapa?",
    "Kalau jawabmu tujuh puluh persen, kamu salah.",
    "Diskon kedua dihitung dari harga yang sudah dipotong.",
    "Seratus ribu jadi lima puluh ribu, lalu jadi empat puluh ribu. Totalnya cuma diskon enam puluh persen.",
    "Dan salah hitung ini menguntungkan toko.",
    "Dalam riset di toko sungguhan, diskon dua puluh plus dua puluh lima persen lebih laku daripada diskon empat puluh persen. Padahal hasilnya sama persis.",
    "Simpan video ini buat sebelas-sebelas. Kamu pernah salah hitung diskon? Tulis di komentar!",
    "Biar nggak gampang ketipu harga, follow Logika Duit!",
]

if __name__ == "__main__":
    tts_gemini.main(LINES, "/root/logikaduit-ep08-suara.zip")
