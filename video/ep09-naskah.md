# Episode 9: Tanggal muda boros, tanggal tua mi instan

Video 9:16, 1080×1920, format pendek. Timeline animasi asli 27,5 detik; versi final dengan narasi Gemini sekitar 32 detik.
Musik dan efek suara original dari `ep09-audio.py` (bebas hak cipta), loudness -14 LUFS. Ada versi tanpa musik (`LD_NO_MUSIC=1`). Caption ada di `ep09-copywriting.md`.
Halaman HTML disusun dari bagian bersama EP7 (teks layar, latar, penutup) ditambah adegan EP9.

## Hook (0 sampai 3 detik)

- Frame pertama: kartu "Saldo Rp5.000.000" dan kalender dengan tanggal 25 menyala sebagai hari gajian, plus teks "Tanggal 25 gajian, tanggal 10 bokek. Kamu juga?" Bisa dipakai sebagai cover.
- Detik 0,35 sampai 2,6: penanda tanggal berjalan cepat dari 25 ke 10, tanggal yang lewat meredup, saldo terkuras sampai Rp43.000, dan pengeluaran (ngopi, checkout, nongkrong, ojol, konser, skincare, makan enak) beterbangan ke samping.
- Detik 2,75: cap "Bokek" menghantam kartu saldo, layar bergetar.

## Voice over

| Detik | Voice over | Di layar |
|---|---|---|
| 0,0 | Tanggal dua puluh lima gajian, tanggal sepuluh udah bokek. Kamu juga? | Saldo terkuras, kalender berjalan, cap "Bokek" |
| 3,6 | Riset di Amerika: begitu uang bulanan masuk, belanja orang langsung naik. | Grafik belanja harian melonjak setelah "Uang masuk", lalu turun |
| 7,2 | Riset lain: di minggu terakhir, kalori yang dimakan turun sepuluh sampai lima belas persen. | Piring penuh di minggu pertama vs mi instan di minggu terakhir, "-10–15%" |
| 11,2 | Namanya bias masa kini: otak lebih mementingkan senang sekarang daripada aman nanti. | Timbangan miring ke "Senang sekarang" |
| 15,4 | Triknya: begitu gajian, langsung bagi jadi empat jatah mingguan. Biar tanggal tua tetap aman. | Gaji Rp4.000.000 terbagi jadi 4 amplop Rp1.000.000, "Tanggal tua tetap aman" |
| 20,0 | Biasanya gajimu habis tanggal berapa? Tulis di komentar! | Kotak komentar dengan pilihan tanggal |
| 23,0 | Biar nggak gampang ketipu harga, follow Logika Duit! | Logo, tombol "Follow Logika Duit" ditekan, struk sumber |

Kalimat penutup di versi final memakai potongan narasi EP8 (kalimatnya sama), karena di narasi EP9 kata "Duit" terdengar seperti "Diet".

## Sumber (cek sebelum tayang)

- Stephens, M. (2003). *"3rd of tha Month": Do Social Security Recipients Smooth Consumption Between Checks?* American Economic Review, 93(1), 406–422. Pengeluaran penerima tunjangan pensiun di AS naik setelah cek bulanan diterima, terutama pada rumah tangga yang penghasilan utamanya dari tunjangan itu.
- Shapiro, J. M. (2005). *Is There a Daily Discount Rate? Evidence from the Food Stamp Nutrition Cycle.* Journal of Public Economics, 89(2–3), 303–325. Kalori yang dimakan penerima kupon makanan di AS turun 10–15% antara minggu pertama dan minggu terakhir bulan kupon.
- Saldo, daftar pengeluaran, dan bentuk grafik belanja adalah ilustrasi.

## Render

```bash
python3 -m http.server 8080            # dari folder repo
LD_TTS_OUT=build/suara.zip python3 video/ep09-tts-gemini.py
python3 video/ep09-mix.py prep build/suara.zip build/
python3 video/ep09-audio.py build/ build/warp.json
node video/render.js http://127.0.0.1:8080/video/ep09-tanggal-tua.html build/video.mp4 --warp build/warp.json --jobs 4
python3 video/ep09-mix.py final build/video.mp4 build/ build/ep09-final.mp4
LD_NO_MUSIC=1 python3 video/ep09-mix.py final build/video.mp4 build/ build/ep09-tanpa-musik.mp4
```
