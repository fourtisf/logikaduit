# Episode 11: Beli Indomie di Alfamart, siapa yang untung lebih gede?

Video 9:16, 1080×1920, format pendek "bongkar bisnis merek", lanjutan EP10. Timeline animasi asli 29,5 detik; versi final mengikuti panjang narasi Gemini.
Musik dan efek suara original dari `ep11-audio.py` (bebas hak cipta), loudness -14 LUFS. Ada versi tanpa musik (`LD_NO_MUSIC=1`). Caption ada di `ep11-copywriting.md`.
Halaman HTML disusun dari bagian bersama EP7 (teks layar, latar, penutup) ditambah adegan EP11.

## Kenapa topik ini

- EP10 (Alfamart untung Rp2.700) memakai pola yang paling banyak ditonton: merek yang dipegang orang tiap hari plus satu fakta mengejutkan.
- Komentar yang di-pin di EP10 sudah menjanjikan episode ini.
- Indomie dan Alfamart dikenal semua orang. Pertanyaan "siapa yang untung lebih gede" membuat penonton menebak dulu, dan jawabannya berlawanan dengan dugaan banyak orang: yang untung besar pabriknya, bukan tokonya.

## Hook (0 sampai 4,5 detik)

- Frame pertama: bungkus mi instan (ilustrasi umum, bukan kemasan asli) dan dua kartu "Yang jualan: Alfamart ?" VS "Yang bikin: Indofood ?", dengan teks "Beli Indomie di Alfamart. Siapa yang untung lebih gede?" Bisa dipakai sebagai cover.
- Detik 1,6 sampai 4,0: sorotan berpindah bolak-balik di antara dua kartu, seolah bertanya "yang mana?".

## Voice over

| Detik | Voice over | Di layar |
|---|---|---|
| 0,0 | Beli Indomie di Alfamart. Siapa yang untung lebih gede, Alfamart atau Indofood yang bikin? | Bungkus mi, kartu "Yang jualan" VS "Yang bikin" |
| 4,6 | Alfamart: dari tiap seratus ribu, untungnya cuma dua ribu tujuh ratus. | Tiga koin jatuh, "Rp2.700" |
| 8,6 | Indofood, pembuat Indomie: dua belas ribu tiga ratus. Lebih dari empat kali lipat! | Dua belas koin menumpuk, "Rp12.300", cap "Lebih dari 4×" |
| 13,0 | Rahasianya: merek. Toko harus rebutan pembeli, tapi Indomie selalu dicari. | Dua minimarket (Alfamart dan Indomaret) rebutan pembeli, bungkus mi menyala di dua-duanya |
| 18,0 | Setahun, laba bersih Indofood sembilan koma dua triliun rupiah. | "Rp9,22 triliun", "12,3% × Rp74,9 triliun penjualan", bungkus mi berjatuhan |
| 22,0 | Kamu tim Indomie goreng atau kuah? Tulis di komentar! | "Goreng" VS "Kuah", kotak komentar "Aku tim" |
| 25,0 | Biar nggak gampang ketipu harga, follow Logika Duit! | Logo, tombol "Follow Logika Duit" ditekan, struk sumber |

Di naskah TTS, "Indofood" ditulis "Indofud" supaya dibaca berlogat Indonesia.
Jeda napas di dalam kalimat dipendekkan (paling lama 0,26 detik) dan narasi dipercepat 5% (`max_pause` dan `speed` di `ep11-mix.py`). Hasilnya 33,7 detik; tanpa itu 37,5 detik.

## Sumber (cek sebelum tayang)

- PT Indofood CBP Sukses Makmur Tbk (ICBP), laporan keuangan 2025, seperti diberitakan Bisnis.com (30 Maret 2026) dan Kontan:
  - penjualan neto Rp74,85 triliun, naik 3,1% dari Rp72,59 triliun;
  - laba Rp9,22 triliun, naik 30,3% dari Rp7,08 triliun.
- PT Sumber Alfaria Trijaya Tbk (Alfamart), laporan keuangan 2025 (lihat EP10): pendapatan Rp126,73 triliun, laba bersih Rp3,41 triliun.
- Hitungan sendiri:
  - Indofood CBP: 9,22 ÷ 74,85 = 12,3%.
  - Alfamart: 3,41 ÷ 126,73 = 2,7%.
  - Perbandingannya 12,3 ÷ 2,7 = 4,6, jadi ditulis "lebih dari 4×".
- Catatan supaya jujur:
  - "Untung dari tiap Rp100 ribu" dihitung dari penjualan masing-masing perusahaan, bukan dari satu struk belanja yang sama.
  - Angka Indofood CBP adalah rata-rata semua produknya (mi instan, susu, makanan ringan, bumbu, nutrisi, minuman), bukan Indomie saja. Indofood CBP adalah anak usaha PT Indofood Sukses Makmur Tbk.
  - Laba 2025 naik 30% padahal penjualan hanya naik 3%, jadi sebagian kenaikannya dari pos di luar jualan. Dengan angka 2024 (7,08 ÷ 72,59 = 9,8%), untung Indofood CBP tetap sekitar Rp9.800 per Rp100 ribu, jauh di atas Alfamart. Ini ditulis di caption.
- Bungkus mi, toko, dan papan nama hanya ilustrasi. Logo, kemasan asli, dan warna merek tidak dipakai.

## Render

```bash
python3 -m http.server 8080            # dari folder repo
LD_TTS_OUT=build/suara.zip python3 video/ep11-tts-gemini.py
python3 video/ep11-mix.py prep build/suara.zip build/
python3 video/ep11-audio.py build/ build/warp.json
node video/render.js http://127.0.0.1:8080/video/ep11-indomie-alfamart.html build/video.mp4 --warp build/warp.json --jobs 4
python3 video/ep11-mix.py final build/video.mp4 build/ build/ep11-final.mp4
LD_NO_MUSIC=1 python3 video/ep11-mix.py final build/video.mp4 build/ build/ep11-tanpa-musik.mp4
```
