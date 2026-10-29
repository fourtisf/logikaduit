#!/usr/bin/env python3
# Naskah narasi EP5 (duit Mixue dari mana) untuk Gemini TTS. Cara kerja dan pencarian API key: lihat tts_gemini.py.
# Format pendek: kalimat singkat. "Mixue" ditulis "Miksue" supaya dibaca seperti orang Indonesia menyebutnya.
# Pakai:
#   python3 video/ep05-tts-gemini.py               # suara default: Puck
#   python3 video/ep05-tts-gemini.py --voice Leda  # suara lain
# Hasil: zip berisi 01.wav ... 07.wav, full.wav, dan lines.json (lokasi: LD_TTS_OUT, default /root/logikaduit-ep05-suara.zip).
import tts_gemini

LINES = [
    "Hampir semua duit Miksue bukan dari es krim yang kamu beli.",
    "Sembilan puluh tujuh koma enam persen pendapatannya dari jualan bahan dan alat ke pemilik gerai.",
    "Gula, susu, cup, sampai mesin es krim, dibeli pemilik gerai dari pusat.",
    "Jadi makin banyak gerai buka, makin cuan pusatnya.",
    "Miksue lebih mirip pemasok daripada toko es krim.",
    "Menurut kamu, buka gerai Miksue masih untung nggak? Tulis di komentar!",
    "Biar nggak gampang ketipu harga, follow Logika Duit!",
]

if __name__ == "__main__":
    tts_gemini.main(LINES, "/root/logikaduit-ep05-suara.zip")
