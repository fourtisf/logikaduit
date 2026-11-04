#!/usr/bin/env python3
# Naskah narasi EP13 (bayar QRIS, kok lebih boros?) untuk Gemini TTS. Cara kerja dan pencarian API key: lihat tts_gemini.py.
# Pakai:
#   python3 video/ep13-tts-gemini.py               # suara default: Achird (sama dengan Ruang Pikir)
#   python3 video/ep13-tts-gemini.py --voice Leda  # suara lain
# Hasil: zip berisi 01.wav ... 08.wav, full.wav, dan lines.json (lokasi: LD_TTS_OUT, default /root/logikaduit-ep13-suara.zip).
# QRIS ditulis "Kris" (cara baca resmi Bank Indonesia), MIT dieja per huruf ("Em-I-Te"); teks layar tetap ejaan asli.
import tts_gemini

LINES = [
    "Mau jajan lebih hemat? Coba trik ini: seminggu bayar pakai uang tunai.",
    "Soalnya, scan Kris itu nggak kerasa kayak ngeluarin duit.",
    "Tahun dua ribu satu, peneliti Em-I-Te melelang tiket basket ke mahasiswa.",
    "Yang harus bayar pakai kartu, berani nawar hampir dua kali lipat dibanding yang bayar tunai.",
    "Namanya rasa sakit membayar. Uang tunai yang lepas dari tangan bikin otak ngerem. Scan Kris? Nggak ada rem.",
    "Rangkuman tujuh puluh satu penelitian juga nemu hal yang sama: bayar nontunai bikin kita ngeluarin uang lebih banyak.",   # "belanja" pernah terbaca "belajar"
    "Jadi coba seminggu bayar tunai, terus tulis sisa uangmu di komentar!",
    "Biar nggak gampang ketipu harga, follow Logika Duit!",
]

if __name__ == "__main__":
    tts_gemini.main(LINES, "/root/logikaduit-ep13-suara.zip")
