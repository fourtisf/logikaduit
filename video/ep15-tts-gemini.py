#!/usr/bin/env python3
# Naskah narasi EP15 (harga dicoret, kok kerasa murah?) untuk Gemini TTS. Cara kerja dan pencarian API key: lihat tts_gemini.py.
# Pakai:
#   python3 video/ep15-tts-gemini.py               # suara default: Achird (sama dengan Ruang Pikir)
#   python3 video/ep15-tts-gemini.py --voice Leda  # suara lain
# Hasil: zip berisi 01.wav ... 08.wav, full.wav, dan lines.json (lokasi: LD_TTS_OUT, default /root/logikaduit-ep15-suara.zip).
# MIT dieja per huruf ("Em-I-Te") dan 11.11 ditulis "sebelas sebelas"; teks layar tetap ejaan asli.
import tts_gemini

LINES = [
    "Mau nggak ketipu harga coret pas sebelas sebelas? Coba trik ini: tutup harga coretnya pakai jempol.",
    "Soalnya, otak kita gampang berjangkar ke angka pertama yang dilihat.",
    "Peneliti Em-I-Te menyuruh mahasiswa menulis dua angka terakhir nomor identitas mereka, lalu menawar barang.",
    "Yang angkanya besar, nawar sekitar tiga kali lipat. Padahal angkanya acak!",
    "Rangkuman riset harga coret juga nemu: harga pembanding bikin barang kerasa lebih berharga, dan bikin kita malas cek toko lain.",
    "Jadi tutup harga coretnya, terus tanya: harga segini wajar nggak? Cek juga di toko lain.",
    "Barang apa yang mau kamu checkout pas sebelas sebelas? Tulis di komentar!",   # "apa pas" terbaca "apa apa", "bareng" terbaca "barang"
    "Biar nggak gampang ketipu harga, follow Logika Duit!",
]

if __name__ == "__main__":
    tts_gemini.main(LINES, "/root/logikaduit-ep15-suara.zip")
