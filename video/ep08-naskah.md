# Episode 8: Diskon 50% + 20% = berapa? (seri Jebakan 11.11, part 1)

Video 9:16, 1080×1920, format pendek. Timeline animasi asli 28,6 detik; versi final dengan narasi Gemini sekitar 35 detik.
Musik dan efek suara original dari `ep08-audio.py` (bebas hak cipta), loudness -14 LUFS. Ada versi tanpa musik (`LD_NO_MUSIC=1`). Caption ada di `ep08-copywriting.md`.
Halaman HTML disusun dari bagian bersama EP7 (teks layar, latar, penutup) ditambah adegan EP8.

## Hook (0 sampai 5 detik): kuis

- Frame pertama: label harga "Sepatu Rp100.000" dan pertanyaan "Diskon 50% + 20%. Jadi diskon berapa?" Bisa dipakai sebagai cover.
- Stiker "Diskon 50%" dan "Tambahan 20%" menempel di label, lalu muncul dua jawaban: 70% dan 60%.
- Jari ragu-ragu, lalu memilih 70%, jawaban yang paling sering dipilih orang.
- Cap "Salah" menghantam jawaban 70%, dan jawaban 60% menyala.

## Voice over

| Detik | Voice over | Di layar |
|---|---|---|
| 0,0 | Diskon lima puluh persen, ditambah diskon dua puluh persen. Jadi diskon berapa? | Label harga, dua stiker, kuis 70% vs 60%, jari memilih 70% |
| 3,2 | Kalau jawabmu tujuh puluh persen, kamu salah. | Cap "Salah" di 70%, 60% menyala |
| 5,6 | Diskon kedua dihitung dari harga yang sudah dipotong. | Struk belanja tercetak baris demi baris |
| 9,0 | Seratus ribu jadi lima puluh ribu, lalu jadi empat puluh ribu. Totalnya cuma diskon enam puluh persen. | Struk: Rp100.000, diskon 50%, subtotal Rp50.000, diskon 20% (dari Rp50.000), bayar Rp40.000, cap "Hemat 60%" |
| 14,0 | Dan salah hitung ini menguntungkan toko. | Toko A dan Toko B |
| 16,0 | Dalam riset di toko sungguhan, diskon dua puluh plus dua puluh lima persen lebih laku daripada diskon empat puluh persen. Padahal hasilnya sama persis. | Toko A diskon 40%, Toko B diskon 20% + 25%, sama-sama bayar Rp60.000; bar pembeli Toko B lebih panjang; cap "Sama persis" |
| 21,5 | Simpan video ini buat sebelas-sebelas. Kamu pernah salah hitung diskon? Tulis di komentar! | Ikon simpan ditekan lalu terisi, kotak komentar |
| 24,2 | Biar nggak gampang ketipu harga, follow Logika Duit! | Logo, tombol "Follow Logika Duit" ditekan, struk sumber |

## Sumber (cek sebelum tayang)

- Chen, H. & Rao, A. R. (2007). *When Two Plus Two Is Not Equal to Four: Errors in Processing Multiple Percentage Changes.* Journal of Consumer Research, 34(3), 327–340. Orang cenderung menjumlahkan persen diskon secara langsung (strategi "angka bulat"), sehingga salah menghitung. Di uji coba di toko sungguhan, diskon 20% lalu tambahan 25% menghasilkan lebih banyak pembeli, penjualan, dan keuntungan daripada diskon 40%, padahal hasilnya sama (0,8 × 0,75 = 0,6).
- Panjang bar "Pembeli" di video tidak menunjukkan angka, hanya arah hasilnya.
- Harga sepatu dan struk belanja adalah ilustrasi. Hitungannya: Rp100.000 × 50% = Rp50.000; Rp50.000 × 80% = Rp40.000; total diskon 60%.

## Render

```bash
python3 -m http.server 8080            # dari folder repo
LD_TTS_OUT=build/suara.zip python3 video/ep08-tts-gemini.py
python3 video/ep08-mix.py prep build/suara.zip build/
python3 video/ep08-audio.py build/ build/warp.json
node video/render.js http://127.0.0.1:8080/video/ep08-diskon-bertumpuk.html build/video.mp4 --warp build/warp.json --jobs 4
python3 video/ep08-mix.py final build/video.mp4 build/ build/ep08-final.mp4
LD_NO_MUSIC=1 python3 video/ep08-mix.py final build/video.mp4 build/ build/ep08-tanpa-musik.mp4
```
