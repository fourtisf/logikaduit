# Episode 15: Harga dicoret, kok kerasa murah?

Video 9:16, 1080×1920, memakai rumus hook EP13 (lihat CLAUDE.md bagian 14). Timeline animasi asli 34 detik; versi final dengan narasi Gemini 44,5 detik.
Musik (tegang ala flash sale: sekitar 130 BPM, progresi minor) dan efek suara original dari `ep15-audio.py` (bebas hak cipta), termasuk detak hitung mundur dan dentang jangkar. Loudness -14 LUFS. Ada versi tanpa musik (`LD_NO_MUSIC=1`). Caption ada di `ep15-copywriting.md`.
Halaman HTML disusun dari bagian bersama EP7 (teks layar, latar, penutup) ditambah adegan EP15.

## Kenapa topik ini

- Menjelang 11.11 hampir semua barang di marketplace ditampilkan dengan harga coret. Topiknya menyangkut penonton langsung.
- Triknya sangat sederhana dan bisa langsung dicoba di HP: tutup harga coretnya pakai jempol.
- Riset jangkar dengan "dua angka terakhir nomor identitas" terdengar aneh dan lucu, jadi gampang diceritakan ulang.

## Hook (0 sampai 4,5 detik)

- Frame pertama (cover):
  - judul "Harga dicoret, kok kerasa murah?";
  - tokoh "kamu" dengan mata bintang memegang HP;
  - kartu produk: headphone nirkabel Rp299.000, harga coret Rp899.000, label "−67%", dan hitung mundur flash sale 11.11;
  - kalimat "Mau nggak ketipu harga coret?".
- Detik 2,75: adegan meredup, lalu kartu "Coba trik ini: tutup harga coretnya pakai jempol" muncul.

## Voice over

| Detik | Voice over | Di layar |
|---|---|---|
| 0,0 | Mau nggak ketipu harga coret pas sebelas sebelas? Coba trik ini: tutup harga coretnya pakai jempol. | Kartu produk dengan harga coret, hitung mundur, kartu trik |
| 4,6 | Soalnya, otak kita gampang berjangkar ke angka pertama yang dilihat. | Jangkar jatuh menghantam "Rp899.000", "Angka pertama = jangkar" |
| 8,4 | Peneliti MIT menyuruh mahasiswa menulis dua angka terakhir nomor identitas mereka, lalu menawar barang. | Dua kartu identitas (berakhiran 12 dan 87), "Ariely, Loewenstein & Prelec, 2003" |
| 12,6 | Yang angkanya besar, nawar sekitar tiga kali lipat. Padahal angkanya acak! | Keyboard nirkabel yang sama: $16 vs $56, cap "Padahal acak!" |
| 17,0 | Rangkuman riset harga coret juga nemu: harga pembanding bikin barang kerasa lebih berharga, dan bikin kita malas cek toko lain. | Kartu produk, meter "Kerasa untung? Banget", "Cek toko lain? Ah, males" |
| 21,4 | Jadi tutup harga coretnya, terus tanya: harga segini wajar nggak? Cek juga di toko lain. | Jempol menutup harga coret, meter turun ke "Biasa", "Wajar nggak? Cek toko lain" |
| 25,6 | Barang apa yang mau kamu checkout pas sebelas sebelas? Tulis di komentar! | Tokoh dan daftar barang incaran, kotak komentar "Mau checkout:" |
| 29,4 | Biar nggak gampang ketipu harga, follow Logika Duit! | Logo, tombol "Follow Logika Duit" ditekan, struk sumber |

Di naskah TTS, "MIT" ditulis "Em-I-Te" dan "11.11" ditulis "sebelas sebelas".

Perbaikan narasi: di percobaan pertama kalimat 7 terbaca "Mau checkout apa apa sebelah-sebelah". Kalimatnya lalu diganti dan dibuat ulang bersama kalimat 6. Model menambah kalimat sendiri di akhir, dan bagian itu dibuang. Ekor ", kita nilai bareng" (terbaca "barang") juga dipotong. Hasil akhirnya: "Barang apa yang mau kamu checkout pas sebelas sebelas? Tulis di komentar!"

## Sumber (cek sebelum tayang)

- Ariely, D., Loewenstein, G. & Prelec, D. (2003). *"Coherent Arbitrariness": Stable Demand Curves Without Stable Preferences.* Quarterly Journal of Economics, 118(1), 73–105.
  - Mahasiswa MBA MIT menulis dua angka terakhir nomor jaminan sosial (nomor identitas AS) mereka, menjawab apakah mau membayar sebesar angka itu, lalu menawar beberapa barang.
  - Peserta dengan angka di atas median menawar 57–107% lebih tinggi daripada yang di bawah median.
  - Tawaran kelompok 20% teratas (angka 80–99) biasanya sekitar tiga kali tawaran kelompok 20% terbawah (00–19). Contoh keyboard nirkabel: rata-rata $56 vs $16.
  - Angka "216–346%" yang sering beredar di internet **tidak** dipakai, karena tidak bisa dipastikan dari makalah aslinya.
  - Catatan jujur: replikasi oleh Fudenberg, Levine & Maniadis (2012) menemukan efek jangkar yang jauh lebih kecil. Efeknya nyata, tapi besarnya bisa berbeda.
- Compeau, L. D. & Grewal, D. (1998). *Comparative Price Advertising: An Integrative Review.* Journal of Public Policy & Marketing, 17(2), 257–273. Meta-analisis: adanya harga pembanding menaikkan harga acuan di kepala pembeli dan persepsi nilai, serta mengurangi niat mencari di toko lain.
- Situs makalah (cmu.edu) tidak bisa dibuka dari sesi pembuatan video. Angka di atas berasal dari kutipan makalah di hasil pencarian. **Cek ulang di makalah asli** sebelum tayang.
- Produk, harga Rp, dan nomor identitas di video hanya ilustrasi.

## Render

```bash
python3 -m http.server 8080            # dari folder repo
LD_TTS_OUT=build/suara.zip python3 video/ep15-tts-gemini.py
python3 video/ep15-mix.py prep build/suara.zip build/
python3 video/ep15-audio.py build/ build/warp.json
node video/render.js http://127.0.0.1:8080/video/ep15-harga-coret.html build/video.mp4 --warp build/warp.json --jobs 4
python3 video/ep15-mix.py final build/video.mp4 build/ build/ep15-final.mp4
LD_NO_MUSIC=1 python3 video/ep15-mix.py final build/video.mp4 build/ build/ep15-tanpa-musik.mp4
```
