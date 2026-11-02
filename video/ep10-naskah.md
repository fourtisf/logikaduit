# Episode 10: Belanja Rp100 ribu di Alfamart, untungnya cuma Rp2.700

Video 9:16, 1080×1920, format pendek "bongkar bisnis merek". Timeline animasi asli 27 detik; versi final dengan narasi Gemini sekitar 29 detik.
Musik dan efek suara original dari `ep10-audio.py` (bebas hak cipta), loudness -14 LUFS. Ada versi tanpa musik (`LD_NO_MUSIC=1`). Caption ada di `ep10-copywriting.md`.
Halaman HTML disusun dari bagian bersama EP7 (teks layar, latar, penutup) ditambah adegan EP10.

## Kenapa topik ini

Data Instagram awal November 2026: video tentang merek yang dipegang orang tiap hari (Indomaret–Alfamart 1.396, Mixue 1.289, snack 1.193 penonton) ditonton 5–7 kali lebih banyak daripada video tentang konsep atau hitungan (gaji 217, diskon 238, antre 180). EP10 memakai pola yang sama: merek yang dikenal semua orang, satu fakta yang mengejutkan.

## Hook (0 sampai 4 detik)

- Frame pertama: uang Rp100.000 (ilustrasi, bukan desain uang asli) dengan teks "Belanja Rp100 ribu di Alfamart. Tebak, untungnya berapa?" Bisa dipakai sebagai cover.
- Detik 0,7 sampai 3,4: angka tebakan "Untung Alfamart dari belanjaanmu" berputar seperti mesin slot.
- Detik 3,4: berhenti di Rp2.700, cap "Cuma Rp2.700", lalu laser memotong 2,7% di ujung uang.

## Voice over

| Detik | Voice over | Di layar |
|---|---|---|
| 0,0 | Kamu belanja seratus ribu di Alfamart. Tebak, Alfamart untung berapa? | Uang Rp100.000, tebakan berputar |
| 3,4 | Cuma sekitar dua ribu tujuh ratus rupiah. | Cap "Cuma Rp2.700", laser memotong 2,7%, "Cuma 2,7%" |
| 6,4 | Sisanya buat bayar barang ke pemasok, gaji karyawan, sewa toko, listrik, dan pajak. | Koin mengalir ke ikon pemasok, gaji karyawan, sewa toko, listrik, pajak |
| 11,0 | Terus kok bisa jadi raksasa? Gerainya ada dua puluh empat ribu lebih. | Peta Indonesia (disederhanakan), titik gerai menyala, hitungan sampai 24.434 |
| 15,2 | Untungnya tipis, tapi dikali belanjaan sebanyak itu, setahun laba bersihnya tiga koma empat triliun rupiah. | "Rp3,41 triliun", koin berjatuhan, "2,7% × Rp126,7 triliun belanja" |
| 19,6 | Kamu tim Alfamart atau Indomaret? Tulis di komentar! | "Tim Alfamart" VS "Tim Indomaret", kotak komentar |
| 22,6 | Biar nggak gampang ketipu harga, follow Logika Duit! | Logo, tombol "Follow Logika Duit" ditekan, struk sumber |

## Sumber (cek sebelum tayang)

- PT Sumber Alfaria Trijaya Tbk, laporan keuangan 2025 (dipublikasikan 27 Maret 2026), seperti diberitakan Bisnis.com dan Kontan: pendapatan bersih Rp126,73 triliun, laba bersih Rp3,41 triliun, total 24.434 gerai di akhir 2025.
- 2,7% adalah hitungan sendiri: 3,41 ÷ 126,73 = 0,0269. Ini rata-rata seluruh grup, bukan untung tiap barang atau tiap gerai.
- Angka grup ikut menghitung anak usahanya (misalnya Alfamidi), jadi di layar ditulis "Grup Alfamart".
- Uang kertas, peta, dan sebaran titik gerai adalah ilustrasi. Logo dan warna merek Alfamart tidak dipakai.

## Render

```bash
python3 -m http.server 8080            # dari folder repo
LD_TTS_OUT=build/suara.zip python3 video/ep10-tts-gemini.py
python3 video/ep10-mix.py prep build/suara.zip build/
python3 video/ep10-audio.py build/ build/warp.json
node video/render.js http://127.0.0.1:8080/video/ep10-untung-alfamart.html build/video.mp4 --warp build/warp.json --jobs 4
python3 video/ep10-mix.py final build/video.mp4 build/ build/ep10-final.mp4
LD_NO_MUSIC=1 python3 video/ep10-mix.py final build/video.mp4 build/ build/ep10-tanpa-musik.mp4
```
