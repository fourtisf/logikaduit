#!/usr/bin/env python3
# Naskah narasi EP4 (antre makanan viral) untuk Gemini TTS. Cara kerja dan pencarian API key: lihat tts_gemini.py.
# Pakai:
#   python3 video/ep04-tts-gemini.py               # suara default: Puck
#   python3 video/ep04-tts-gemini.py --voice Leda  # suara lain
# Hasil: zip berisi 01.wav ... 15.wav, full.wav, dan lines.json (lokasi: LD_TTS_OUT, default /root/logikaduit-ep04-suara.zip).
# Angka tahun ditulis dengan kata supaya dibaca dalam bahasa Indonesia.
import tts_gemini

LINES = [
    "Kenapa kita rela antre dua jam buat makanan viral?",
    "Padahal rasanya... biasa aja.",
    "Dua warung, menu sama, harga sama. Kamu pilih yang mana?",
    "Kebanyakan orang pilih yang ramai. Kata otak: pasti enak.",
    "Ada eksperimennya. New York, tahun seribu sembilan ratus enam puluh sembilan.",
    "Satu orang disuruh berdiri di trotoar, menatap jendela lantai enam.",
    "Yang ikut berhenti cuma empat persen.",
    "Lalu yang menatap ditambah jadi lima belas orang.",
    "Yang ikut berhenti melonjak jadi empat puluh persen. Sepuluh kali lipat!",
    "Padahal di atas sana nggak ada kejadian apa-apa.",
    "Namanya efek ikut-ikutan. Makin panjang antrean, makin banyak yang ikut antre.",
    "Label terlaris juga begitu.",
    "Di restoran di Beijing, menu berlabel paling laris dipesan tiga belas sampai dua puluh persen lebih banyak.",
    "Jadi ingat: antrean panjang itu bukti ramai, bukan bukti enak. Cek dulu ulasannya.",
    "Biar nggak gampang ketipu harga, follow Logika Duit!",
]

if __name__ == "__main__":
    tts_gemini.main(LINES, "/root/logikaduit-ep04-suara.zip")
