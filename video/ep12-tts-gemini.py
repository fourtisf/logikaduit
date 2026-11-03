#!/usr/bin/env python3
# Naskah narasi EP12 (selama kamu nonton, BCA untung berapa) untuk Gemini TTS. Cara kerja dan pencarian API key: lihat tts_gemini.py.
# Pakai:
#   python3 video/ep12-tts-gemini.py               # suara default: Achird (sama dengan Ruang Pikir)
#   python3 video/ep12-tts-gemini.py --voice Leda  # suara lain
# Hasil: zip berisi 01.wav ... 07.wav, full.wav, dan lines.json (lokasi: LD_TTS_OUT, default /root/logikaduit-ep12-suara.zip).
# Singkatan bank ditulis per huruf ("Be-Ce-A", "Be-Er-I") supaya dieja dengan huruf Indonesia; teks layar tetap "BCA" dan "BRI".
import tts_gemini

LINES = [
    "Selama kamu nonton video ini, Be-Ce-A untung lebih dari lima puluh juta rupiah.",
    "Tahun lalu, laba bersihnya lima puluh tujuh koma lima triliun. Itu satu koma delapan juta tiap detik.",
    "Dari mana? Tabungan di bawah sepuluh juta, bunganya nol persen.",
    "Lalu uangnya dipinjamkan lagi, dengan bunga dasar sekitar tujuh sampai sembilan persen.",
    "Selisih bunga itulah mesin uang terbesarnya.",
    "Kamu nasabah Be-Ce-A, Be-Er-I, atau Mandiri? Tulis di komentar!",
    "Biar nggak gampang ketipu harga, follow Logika Duit!",
]

if __name__ == "__main__":
    tts_gemini.main(LINES, "/root/logikaduit-ep12-suara.zip")
