# Episode 6: Harga snack nggak naik, isinya yang dikurangin

Video 9:16, 1080×1920, format pendek. Timeline animasi asli 27 detik; versi final dengan narasi Gemini sekitar 31 detik.
Musik dan efek suara original dari `ep06-audio.py` (bebas hak cipta), loudness -14 LUFS. Ada versi tanpa musik (`LD_NO_MUSIC=1`). Caption ada di `ep06-copywriting.md`.

## Hook (0 sampai 2 detik)

- Frame pertama: kemasan keripik besar dengan foil zamrud yang berkilau, label harga "Rp10.000", dan teks "Harga snack kamu nggak naik. Isinya yang dikurangin." Bisa dipakai sebagai cover.
- Detik 0,25 sampai 1,05: garis pemindai sinar-X turun dan memperlihatkan isi kemasan.
- Detik 1,1 sampai 1,8: tumpukan keripik turun dari garis 100 g ke 80 g, bagian atas jadi "Angin".
- Detik 1,85: cap "Harga sama" menghantam label harga, layar bergetar.

## Voice over

| Detik | Voice over | Di layar |
|---|---|---|
| 0,0 | Harga snack kamu nggak naik. Isinya yang dikurangin. | Pemindai sinar-X, isi turun 100 g → 80 g, cap "Harga sama" |
| 3,0 | Dulu seratus gram, sekarang delapan puluh. Harganya sama, tapi per gram naik dua puluh lima persen. | Kartu "Dulu" vs "Sekarang", harga per gram Rp100 → Rp125, cap "+25%" |
| 8,0 | Kenapa nggak naikin harga aja? Karena isi yang berkurang jarang kita sadari. | "Naikin harga: langsung ketahuan" vs "Kurangi isi: jarang disadari" |
| 11,6 | Riset belanja es krim di Chicago: pembeli empat kali lebih peka sama harga naik daripada isi yang dikurangi. | Angka besar "4×", dua bar (harga naik penuh, isi dikurangi seperempat) |
| 16,0 | Jadi cek beratnya, bukan cuma harganya. | Label rak, kaca pembesar ke "Berat bersih 80 g" lalu "Rp125 / gram" |
| 19,4 | Snack apa yang menurutmu makin kecil? Tulis di komentar! | Tiga kemasan mengecil, kotak komentar |
| 22,6 | Biar nggak gampang ketipu harga, follow Logika Duit! | Logo, tombol "Follow Logika Duit" ditekan, struk sumber |

## Sumber (cek sebelum tayang)

- Çakır, M. & Balagtas, J. V. (2014). *Consumer Response to Package Downsizing: Evidence from the Chicago Ice Cream Market.* Journal of Retailing, 90(1), 1–12. Dari data belanja rumah tangga, respons pembeli terhadap ukuran kemasan sekitar seperempat respons terhadap harga, jadi pembeli sekitar 4 kali lebih peka pada harga naik daripada isi yang dikurangi.
- Berat (100 g → 80 g), harga Rp10.000, dan kemasan keripik adalah ilustrasi. Hitungannya: Rp10.000 / 100 g = Rp100 per gram; Rp10.000 / 80 g = Rp125 per gram, naik 25%.

## Render

```bash
python3 -m http.server 8080            # dari folder repo
LD_TTS_OUT=build/suara.zip python3 video/ep06-tts-gemini.py
python3 video/ep06-mix.py prep build/suara.zip build/
python3 video/ep06-audio.py build/ build/warp.json
node video/render.js http://127.0.0.1:8080/video/ep06-snack-mengecil.html build/video.mp4 --warp build/warp.json --jobs 4
python3 video/ep06-mix.py final build/video.mp4 build/ build/ep06-final.mp4
LD_NO_MUSIC=1 python3 video/ep06-mix.py final build/video.mp4 build/ build/ep06-tanpa-musik.mp4
```
