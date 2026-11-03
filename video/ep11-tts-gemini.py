#!/usr/bin/env python3
# Naskah narasi EP11 (Indomie di Alfamart, siapa yang untung) untuk Gemini TTS. Cara kerja dan pencarian API key: lihat tts_gemini.py.
# Pakai:
#   python3 video/ep11-tts-gemini.py               # suara default: Achird (sama dengan Ruang Pikir)
#   python3 video/ep11-tts-gemini.py --voice Leda  # suara lain
# Hasil: zip berisi 01.wav ... 07.wav, full.wav, dan lines.json (lokasi: LD_TTS_OUT, default /root/logikaduit-ep11-suara.zip).
# "Indofud" ditulis sesuai ucapan supaya tidak dibaca berlogat Inggris; teks layar tetap "Indofood".
import tts_gemini

LINES = [
    "Beli Indomie di Alfamart. Siapa yang untung lebih gede, Alfamart atau Indofud yang bikin?",
    "Alfamart: dari tiap seratus ribu, untungnya cuma dua ribu tujuh ratus.",
    "Indofud, pembuat Indomie: dua belas ribu tiga ratus. Lebih dari empat kali lipat!",
    "Rahasianya: merek. Toko harus rebutan pembeli, tapi Indomie selalu dicari.",
    "Setahun, laba bersih Indofud sembilan koma dua triliun rupiah.",
    "Kamu tim Indomie goreng atau kuah? Tulis di komentar!",
    "Biar nggak gampang ketipu harga, follow Logika Duit!",
]

if __name__ == "__main__":
    tts_gemini.main(LINES, "/root/logikaduit-ep11-suara.zip")
