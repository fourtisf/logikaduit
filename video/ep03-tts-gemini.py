#!/usr/bin/env python3
# Naskah narasi EP3 (gratis ongkir) untuk Gemini TTS. Cara kerja dan pencarian API key: lihat tts_gemini.py.
# Pakai:
#   python3 video/ep03-tts-gemini.py               # suara default: Puck
#   python3 video/ep03-tts-gemini.py --voice Leda  # suara lain
# Hasil: zip berisi 01.wav ... 15.wav, full.wav, dan lines.json (lokasi: LD_TTS_OUT, default /root/logikaduit-ep03-suara.zip).
import tts_gemini

LINES = [
    "Pernah nambah barang biar dapat gratis ongkir?",
    "Hemat ongkir sepuluh ribu, tapi nambah belanja dua puluh delapan ribu.",
    "Totalnya malah delapan belas ribu lebih mahal.",
    "Kok kita tetap merasa menang?",
    "Ada eksperimennya. Peneliti menjual dua coklat.",
    "Yang premium lima belas sen, yang biasa satu sen. Kamu pilih yang mana?",
    "Tujuh puluh tiga persen pilih yang premium. Masuk akal.",
    "Lalu dua-duanya diturunkan satu sen.",
    "Yang biasa jadi... gratis.",
    "Hasilnya berbalik: enam puluh sembilan persen pilih yang gratis.",
    "Padahal selisih harganya tetap empat belas sen.",
    "Kata gratis bikin otak berhenti menghitung. Namanya efek harga nol.",
    "Promo gratis ongkir pakai trik yang sama.",
    "Sebelum nambah barang, tanya dulu: kalau ongkirnya bayar, barang ini tetap kamu beli?",
    "Biar nggak gampang ketipu harga, follow Logika Duit!",
]

if __name__ == "__main__":
    tts_gemini.main(LINES, "/root/logikaduit-ep03-suara.zip")
