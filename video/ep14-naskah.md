# Episode 14: Lapar, kok belanjanya kalap?

Video 9:16, 1080×1920, memakai rumus hook EP13 (lihat CLAUDE.md bagian 14): "Mau [hasil]? Coba trik ini", judul "X, kok Y?", tokoh "kamu" dengan ekspresi, satu riset utama, ditutup tantangan.
Timeline animasi asli 31,5 detik; versi final dengan narasi Gemini 36,9 detik.
Musik (lebih ceria: 120 BPM, progresi mayor) dan efek suara original dari `ep14-audio.py` (bebas hak cipta), termasuk bunyi perut keroncongan dan printer struk yang disintesis. Loudness -14 LUFS. Ada versi tanpa musik (`LD_NO_MUSIC=1`). Caption ada di `ep14-copywriting.md`.
Halaman HTML disusun dari bagian bersama EP7 (teks layar, latar, penutup) ditambah adegan EP14.

## Kenapa topik ini

- Semua orang pernah belanja atau scroll marketplace sambil lapar, jadi topiknya menyangkut penonton langsung.
- Hasil risetnya mengejutkan dan lucu: yang lapar belanja lebih banyak, dan yang dibeli **bukan makanan** (sampai penjepit kertas).
- Triknya gampang dicoba, dan waktunya pas menjelang 11.11.

## Hook (0 sampai 4,5 detik)

- Frame pertama (cover):
  - judul "Lapar, kok belanjanya kalap?";
  - tokoh "kamu" lapar (mulut terbuka, ngiler) memegang HP, gelembung "kruuuk...";
  - keranjang berisi 3 barang (Rp229.000);
  - kalimat "Mau nggak kalap belanja?".
- Detik 0,7 sampai 1,7: tiga barang lagi masuk keranjang, dan total naik ke Rp487.000.
- Detik 2,75: adegan meredup, lalu kartu "Coba trik ini: makan dulu sebelum buka keranjang" muncul.

## Voice over

| Detik | Voice over | Di layar |
|---|---|---|
| 0,0 | Mau nggak kalap belanja? Coba trik ini: makan dulu sebelum buka keranjang. | Tokoh lapar, keranjang terisi, kartu trik |
| 4,6 | Tahun dua ribu lima belas, peneliti memeriksa struk belanja orang yang keluar dari sebuah toserba. | Toserba, tiga struk tercetak, kaca pembesar, "Xu, Schwarz & Wyer, 2015" |
| 9,0 | Yang lagi lapar, ngeluarin uang enam puluh empat persen lebih banyak. Dan yang dibeli bukan makanan! | Struk "Kenyang" Rp178.000 vs "Lapar" Rp292.000, cap "+64%", "Yang dibeli bukan makanan!" |
| 13,6 | Di percobaan lain, yang paling lapar mengambil penjepit kertas paling banyak. Padahal nggak bisa dimakan. | Toples penjepit kertas, penjepit beterbangan ke tumpukan, "Bisa dimakan?" |
| 18,0 | Kata peneliti, lapar bikin otak masuk mode pengin dapet sesuatu, apa pun barangnya. | Magnet di atas kepala, sakelar "Mode pengin dapet sesuatu" menyala, barang tertarik |
| 22,0 | Jadi sebelum checkout sebelas sebelas, makan dulu. Terus tulis berapa barang yang kamu hapus dari keranjang! | Tokoh makan, 4 barang dicoret dari keranjang (Rp487.000 jadi Rp138.000), kotak komentar |
| 27,0 | Biar nggak gampang ketipu harga, follow Logika Duit! | Logo, tombol "Follow Logika Duit" ditekan, struk sumber |

Kalimat 3 di naskah TTS memakai "ngeluarin uang" (teks layar tetap "belanja 64% lebih banyak"), karena di EP13 kata "belanja" pernah terbaca "belajar".

## Sumber (cek sebelum tayang)

- Xu, A. J., Schwarz, N. & Wyer, R. S. (2015). *Hunger promotes acquisition of nonfood objects.* Proceedings of the National Academy of Sciences, 112(9), 2688–2692.
  - Studi lapangan: 81 pembeli dicegat saat keluar dari sebuah toserba, lalu struknya diperiksa. Yang melaporkan sedang lapar menghabiskan 64% lebih banyak dan membeli lebih banyak barang **bukan makanan**. Hasilnya tetap setelah suasana hati dan lama berada di toko diperhitungkan.
  - Studi lain: peserta yang paling lapar mengambil penjepit kertas (binder clip) gratis paling banyak, padahal rasa lapar tidak membuat mereka lebih menyukai penjepit itu.
  - Penjelasan peneliti: keinginan mendapat makanan memicu dorongan umum untuk "mendapat sesuatu".
  - Angka 64% diambil dari rilis USC dan liputan media (ScienceDaily, Medical Xpress). **Cek ulang di makalah PNAS** (doi 10.1073/pnas.1417712112) sebelum tayang.
- Catatan supaya jujur:
  - Riset dilakukan di toko fisik, bukan belanja online. Trik "makan dulu sebelum buka keranjang" adalah penerapan yang masuk akal, bukan hasil uji langsung di marketplace.
  - Isi struk, nama barang, dan harga di video hanya ilustrasi. Angkanya dibuat supaya pas 64% (Rp178.000 ke Rp292.000).

## Render

```bash
python3 -m http.server 8080            # dari folder repo
LD_TTS_OUT=build/suara.zip python3 video/ep14-tts-gemini.py
python3 video/ep14-mix.py prep build/suara.zip build/
python3 video/ep14-audio.py build/ build/warp.json
node video/render.js http://127.0.0.1:8080/video/ep14-lapar-kalap.html build/video.mp4 --warp build/warp.json --jobs 4
python3 video/ep14-mix.py final build/video.mp4 build/ build/ep14-final.mp4
LD_NO_MUSIC=1 python3 video/ep14-mix.py final build/video.mp4 build/ build/ep14-tanpa-musik.mp4
```
