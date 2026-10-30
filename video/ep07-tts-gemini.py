#!/usr/bin/env python3
# Naskah narasi EP7 (gaji naik 5%, kok tetap bokek) untuk Gemini TTS. Cara kerja dan pencarian API key: lihat tts_gemini.py.
# Pakai:
#   python3 video/ep07-tts-gemini.py               # suara default: Puck
#   python3 video/ep07-tts-gemini.py --voice Leda  # suara lain
# Hasil: zip berisi 01.wav ... 08.wav, full.wav, dan lines.json (lokasi: LD_TTS_OUT, default /root/logikaduit-ep07-suara.zip).
import tts_gemini

LINES = [
    "Gaji naik dua persen, atau naik lima persen? Kamu pilih mana?",
    "Tapi yang lima persen, harga-harga juga naik empat persen.",
    "Jadi yang lima persen sebenarnya cuma naik satu persen. Yang dua persen tetap naik dua persen.",
    "Anehnya, sekitar dua dari tiga orang merasa yang lima persen lebih bahagia.",
    "Namanya ilusi uang: otak lihat angka di slip gaji, bukan apa yang bisa dibeli.",
    "Rumusnya: kenaikan gaji dikurangi kenaikan harga. Itu naik aslimu.",
    "Tahun ini gajimu naik berapa persen? Tulis di komentar!",
    "Biar nggak gampang ketipu harga, follow Logika Duit!",
]

if __name__ == "__main__":
    tts_gemini.main(LINES, "/root/logikaduit-ep07-suara.zip")
