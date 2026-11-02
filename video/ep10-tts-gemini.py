#!/usr/bin/env python3
# Naskah narasi EP10 (Alfamart untung berapa) untuk Gemini TTS. Cara kerja dan pencarian API key: lihat tts_gemini.py.
# Pakai:
#   python3 video/ep10-tts-gemini.py               # suara default: Achird (sama dengan Ruang Pikir)
#   python3 video/ep10-tts-gemini.py --voice Leda  # suara lain
# Hasil: zip berisi 01.wav ... 07.wav, full.wav, dan lines.json (lokasi: LD_TTS_OUT, default /root/logikaduit-ep10-suara.zip).
import tts_gemini

LINES = [
    "Kamu belanja seratus ribu di Alfamart. Tebak, Alfamart untung berapa?",
    "Cuma sekitar dua ribu tujuh ratus rupiah.",
    "Sisanya buat bayar barang ke pemasok, gaji karyawan, sewa toko, listrik, dan pajak.",
    "Terus kok bisa jadi raksasa? Gerainya ada dua puluh empat ribu lebih.",
    "Untungnya tipis, tapi dikali belanjaan sebanyak itu, setahun laba bersihnya tiga koma empat triliun rupiah.",
    "Kamu tim Alfamart atau Indomaret? Tulis di komentar!",
    "Biar nggak gampang ketipu harga, follow Logika Duit!",
]

if __name__ == "__main__":
    tts_gemini.main(LINES, "/root/logikaduit-ep10-suara.zip")
