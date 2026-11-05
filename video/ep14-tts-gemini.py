#!/usr/bin/env python3
# Naskah narasi EP14 (lapar, kok belanjanya kalap?) untuk Gemini TTS. Cara kerja dan pencarian API key: lihat tts_gemini.py.
# Pakai:
#   python3 video/ep14-tts-gemini.py               # suara default: Achird (sama dengan Ruang Pikir)
#   python3 video/ep14-tts-gemini.py --voice Leda  # suara lain
# Hasil: zip berisi 01.wav ... 07.wav, full.wav, dan lines.json (lokasi: LD_TTS_OUT, default /root/logikaduit-ep14-suara.zip).
# Kalimat 3 memakai "ngeluarin uang", bukan "belanjanya": di EP13 kata "belanja" pernah terbaca "belajar".
import tts_gemini

LINES = [
    "Mau nggak kalap belanja? Coba trik ini: makan dulu sebelum buka keranjang.",
    "Tahun dua ribu lima belas, peneliti memeriksa struk belanja orang yang keluar dari sebuah toserba.",
    "Yang lagi lapar, ngeluarin uang enam puluh empat persen lebih banyak. Dan yang dibeli bukan makanan!",
    "Di percobaan lain, yang paling lapar mengambil penjepit kertas paling banyak. Padahal nggak bisa dimakan.",
    "Kata peneliti, lapar bikin otak masuk mode pengin dapet sesuatu, apa pun barangnya.",
    "Jadi sebelum checkout sebelas sebelas, makan dulu. Terus tulis berapa barang yang kamu hapus dari keranjang!",
    "Biar nggak gampang ketipu harga, follow Logika Duit!",
]

if __name__ == "__main__":
    tts_gemini.main(LINES, "/root/logikaduit-ep14-suara.zip")
