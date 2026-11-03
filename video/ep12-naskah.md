# Episode 12: Selama kamu nonton video ini, BCA untung Rp50 juta lebih

Video 9:16, 1080×1920, format pendek "bongkar bisnis merek". Timeline animasi asli 29,5 detik; versi final dengan narasi Gemini 33,1 detik.
Musik dan efek suara original dari `ep12-audio.py` (bebas hak cipta), loudness -14 LUFS. Ada versi tanpa musik (`LD_NO_MUSIC=1`). Caption ada di `ep12-copywriting.md`.
Halaman HTML disusun dari bagian bersama EP7 (teks layar, latar, penutup) ditambah adegan EP12.

## Kenapa topik ini

- Pola yang paling banyak ditonton adalah merek yang dipakai tiap hari ditambah satu angka yang mengejutkan. BCA adalah bank yang dipakai banyak anak muda.
- Hook-nya menyangkut penonton secara langsung: penghitung di layar berjalan selama mereka menonton, jadi ada alasan untuk menonton sampai habis.
- Pertanyaan penutup ("Kamu nasabah BCA, BRI, atau Mandiri?") gampang dijawab dengan satu kata.

## Penghitung waktu nyata

- Penghitung "Untung BCA sejak kamu mulai nonton" dihitung dari detik video yang sebenarnya, bukan dari timeline animasi. `render.js` mengisi `window.REAL_T` dengan detik di video jadi (setelah tempo disesuaikan dengan narasi).
- Rumusnya: laba 2025 Rp57,56 triliun ÷ 31.536.000 detik setahun = Rp1.825.203 per detik.
- Di akhir video (sekitar 33 detik) angkanya sekitar Rp60 juta. Karena itu teksnya "Rp50 juta lebih".
- Digit kecil berganti tiap frame, digit besar menggulung seperti meteran, dan angka nol di depan dibuat redup.

## Hook (0 sampai 4,5 detik)

- Frame pertama: kartu penghitung "Rp00.000.000" dengan teks "Selama kamu nonton video ini, BCA untung Rp50 juta lebih." Untuk cover, frame di sekitar detik 2–3 lebih menarik karena angkanya sudah jutaan.
- Penghitung langsung berjalan, dan garis detik di bawahnya penuh tiap satu detik.
- Setelah hook, kartu berubah jadi pil kecil di bawah layar yang terus berjalan sampai pertanyaan penutup.

## Voice over

| Detik | Voice over | Di layar |
|---|---|---|
| 0,0 | Selama kamu nonton video ini, BCA untung lebih dari lima puluh juta rupiah. | Penghitung berjalan dari Rp0 |
| 4,6 | Tahun lalu, laba bersihnya lima puluh tujuh koma lima triliun. Itu satu koma delapan juta tiap detik. | "Rp57,5 triliun", per hari Rp157,7 miliar, per menit Rp109,5 juta, per detik Rp1,8 juta |
| 9,0 | Dari mana? Tabungan di bawah sepuluh juta, bunganya nol persen. | Batang "Tabungan" 0%, kartu "Saldo Rp9.800.000, bunga setahun Rp0" |
| 13,4 | Lalu uangnya dipinjamkan lagi, dengan bunga dasar sekitar tujuh sampai sembilan persen. | Koin mengalir ke batang "Pinjaman", "6,8–9,1%" |
| 17,8 | Selisih bunga itulah mesin uang terbesarnya. | Panah "Selisih bunga", koin masuk ke penghitung |
| 21,8 | Kamu nasabah BCA, BRI, atau Mandiri? Tulis di komentar! | Kartu BCA, BRI, Mandiri, kotak komentar "Aku nasabah" |
| 25,0 | Biar nggak gampang ketipu harga, follow Logika Duit! | Logo, tombol "Follow Logika Duit" ditekan, struk sumber |

Di naskah TTS, "BCA" dan "BRI" ditulis "Be-Ce-A" dan "Be-Er-I" supaya dieja dengan huruf Indonesia.

## Sumber (cek sebelum tayang)

- PT Bank Central Asia Tbk, kinerja 2025 (dirilis 27 Januari 2026), seperti diberitakan Bisnis.com, Kontan, dan Investortrust:
  - laba bersih konsolidasi Rp57,56 triliun, naik 4,9% dari Rp54,85 triliun;
  - pendapatan bunga bersih per November 2025 sekitar Rp73 triliun, sumber pendapatan terbesar BCA.
- Suku bunga Tahapan BCA (tabungan utama BCA), berlaku sejak 1 Maret 2025: saldo di bawah Rp10 juta 0% per tahun. Saldo lebih besar dapat bunga kecil (sekitar 0,01–0,02%).
- Suku Bunga Dasar Kredit (SBDK) BCA, data 30 Juni 2026, seperti diberitakan Kontan:
  - korporasi 6,81%, ritel 7,74%, kecil 8,04%, menengah 8,10%, mikro 6,95%;
  - KPR 9,14%.
  - SBDK adalah bunga paling rendah sebelum ditambah premi risiko, jadi bunga kredit sebenarnya bisa lebih tinggi.
- Hitungan sendiri:
  - per hari: 57,56 triliun ÷ 365 = Rp157,7 miliar;
  - per menit: Rp109,5 juta;
  - per detik: Rp1,8 juta.
- Catatan supaya jujur:
  - "Dipinjamkan lagi" adalah penyederhanaan. Bank menyalurkan kredit dari seluruh dana simpanan (giro, tabungan, deposito). Deposito dibayar bunga lebih tinggi (sekitar 2,5–3%), tapi sebagian besar dana BCA (sekitar 83%) berupa giro dan tabungan yang bunganya sangat kecil.
  - Untung bersih masih dipotong biaya operasional, cadangan kredit macet, dan pajak.
- Situs bca.co.id tidak bisa dibuka dari sesi pembuatan video. Angka bunga Tahapan dan SBDK di atas berasal dari berita dan cuplikan pencarian, jadi **cek ulang di bca.co.id** (halaman "Suku Bunga Dasar Kredit" dan RIPLAY Tahapan) sebelum tayang.
- Ikon gedung bank hanya ilustrasi. Logo dan warna merek bank tidak dipakai.

## Render

```bash
python3 -m http.server 8080            # dari folder repo
LD_TTS_OUT=build/suara.zip python3 video/ep12-tts-gemini.py
python3 video/ep12-mix.py prep build/suara.zip build/
python3 video/ep12-audio.py build/ build/warp.json
node video/render.js http://127.0.0.1:8080/video/ep12-untung-bca.html build/video.mp4 --warp build/warp.json --jobs 4
python3 video/ep12-mix.py final build/video.mp4 build/ build/ep12-final.mp4
LD_NO_MUSIC=1 python3 video/ep12-mix.py final build/video.mp4 build/ build/ep12-tanpa-musik.mp4
```
