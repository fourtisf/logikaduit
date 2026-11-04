# Episode 13: Bayar QRIS, kok lebih boros?

Video 9:16, 1080×1920. Episode pertama dengan rumus hook baru (lihat CLAUDE.md bagian 14): "Mau [hasil]? Coba trik ini", judul "X, kok Y?", tokoh "kamu" dengan ekspresi, satu riset utama, ditutup tantangan.
Timeline animasi asli 35,5 detik; versi final dengan narasi Gemini 42,5 detik.
Musik dan efek suara original dari `ep13-audio.py` (bebas hak cipta), loudness -14 LUFS. Ada versi tanpa musik (`LD_NO_MUSIC=1`). Caption ada di `ep13-copywriting.md`.
Halaman HTML disusun dari bagian bersama EP7 (teks layar, latar, penutup) ditambah adegan EP13.

## Kenapa topik ini

- Video Logika Duit tentang untung perusahaan (Alfamart 185 penonton) sepi, sedangkan video Ruang Pikir yang menjanjikan trik untuk penonton cepat viral (catatan EP14 Ruang Pikir: 722 suka dan 165 kali dikirim dalam sehari).
- Hampir semua anak muda bayar pakai QRIS tiap hari (tahun 2025 ada 15,5 miliar transaksi QRIS), jadi topiknya menyangkut penonton langsung.
- Triknya bisa langsung dicoba dan hasilnya bisa diceritakan di komentar.

## Hook (0 sampai 4,5 detik)

- Frame pertama (cover): judul "Bayar QRIS, kok lebih boros?" Di bawahnya:
  - tokoh "kamu" tersenyum sambil memegang HP di depan kode QR;
  - pil "Saldo e-wallet Rp500.000";
  - kalimat "Mau jajan lebih hemat?".
- Detik 0,35 sampai 1,85: empat kali scan dengan bunyi "bip". Kopi susu, seblak, boba, dan ojol beterbangan, dan saldo turun ke Rp420.000 tanpa terasa.
- Detik 2,75: adegan meredup, kartu "Coba trik ini: seminggu bayar pakai uang tunai" muncul, dan wajah tokoh berubah kaget.

## Voice over

| Detik | Voice over | Di layar |
|---|---|---|
| 0,0 | Mau jajan lebih hemat? Coba trik ini: seminggu bayar pakai uang tunai. | Judul, tokoh scan QRIS, saldo terkuras, kartu trik |
| 4,6 | Soalnya, scan QRIS itu nggak kerasa kayak ngeluarin duit. | HP memindai, "Pembayaran berhasil Rp25.000", meter "Kerasa ngeluarin duit?" hampir nol |
| 8,6 | Tahun dua ribu satu, peneliti MIT melelang tiket basket ke mahasiswa. | Tiket basket, palu lelang, "Peneliti MIT, 2001" |
| 12,6 | Yang harus bayar pakai kartu, berani nawar hampir dua kali lipat dibanding yang bayar tunai. | Batang "Bayar tunai 1×" vs "Bayar kartu ±2×", cap "Hampir 2× lipat" |
| 17,0 | Namanya rasa sakit membayar. Uang tunai yang lepas dari tangan bikin otak ngerem. Scan QRIS? Nggak ada rem. | Dua meter: tunai tinggi (wajah meringis, "Otak ngerem"), scan QR rendah (wajah senyum, "Nggak ada rem") |
| 22,0 | Rangkuman tujuh puluh satu penelitian juga nemu hal yang sama: bayar nontunai bikin kita ngeluarin uang lebih banyak. | 71 kartu penelitian, "17 negara, lebih dari 11.000 peserta (2024)" |
| 27,0 | Jadi coba seminggu bayar tunai, terus tulis sisa uangmu di komentar! | Tokoh memegang amplop "Jatah", tujuh hari dicentang, kotak komentar "Hari ke-7, sisa uangku Rp" |
| 31,0 | Biar nggak gampang ketipu harga, follow Logika Duit! | Logo, tombol "Follow Logika Duit" ditekan, struk sumber |

Di naskah TTS, "QRIS" ditulis "Kris" (cara baca resmi Bank Indonesia) dan "MIT" ditulis "Em-I-Te".

Perbaikan narasi: di percobaan pertama, "belanja" terbaca "belajar" dan kalimat 4 ikut membawa "Namanya rasa sakit membayar". Kalimat 6 lalu diganti jadi "ngeluarin uang lebih banyak" dan dibuat ulang bersama kalimat 5 sebagai konteks; batas kalimat 4/5 digeser ke jeda yang benar.

## Sumber (cek sebelum tayang)

- Prelec, D. & Simester, D. (2001). *Always Leave Home Without It: A Further Investigation of the Credit-Card Effect on Willingness to Pay.* Marketing Letters, 12(1), 5–12.
  - Mahasiswa MBA MIT menawar tiket pertandingan basket (Boston Celtics) dalam lelang tertutup. Separuh diberi tahu harus bayar tunai, separuh lagi harus bayar pakai kartu kredit.
  - Tawaran kelompok kartu kredit sekitar dua kali lipat. Angka persisnya ada di Tabel 1 makalah; di video ditulis "hampir 2× lipat".
- Prelec, D. & Loewenstein, G. (1998). *The Red and the Black: Mental Accounting of Savings and Debt.* Marketing Science, 17(1), 4–28. Asal istilah "rasa sakit membayar" (pain of paying).
- Schomburgk, L., Belli, A. & Hoffmann, A. O. I. (2024). *Less Cash, More Splash? A Meta-Analysis on the Cashless Effect.* Journal of Retailing, 100(3), 382–403.
  - 392 hasil dari 71 makalah, 17 negara, lebih dari 11.000 peserta.
  - Pembayaran nontunai membuat orang belanja lebih banyak. **Rata-rata efeknya kecil tapi nyata**; ini ditulis jujur di caption.
- Bank Indonesia lewat Kontan: 15,51 miliar transaksi QRIS sepanjang 2025, dan 59,98 juta pengguna per Januari 2026.
- Catatan supaya jujur:
  - Riset tahun 2001 memakai kartu kredit, bukan QRIS. Video menyebut "bayar pakai kartu" dan menjelaskan bahwa yang sama di semua cara nontunai adalah rasa sakit membayar yang lebih kecil.
  - Belum ada riset besar khusus QRIS, jadi judulnya berupa pertanyaan.
- Saldo, harga jajan, dan kode QR di video hanya ilustrasi. Kode QR tidak bisa dipindai. Logo QRIS tidak dipakai; nama QRIS hanya ditulis sebagai teks.

## Render

```bash
python3 -m http.server 8080            # dari folder repo
LD_TTS_OUT=build/suara.zip python3 video/ep13-tts-gemini.py
python3 video/ep13-mix.py prep build/suara.zip build/
python3 video/ep13-audio.py build/ build/warp.json
node video/render.js http://127.0.0.1:8080/video/ep13-qris-boros.html build/video.mp4 --warp build/warp.json --jobs 4
python3 video/ep13-mix.py final build/video.mp4 build/ build/ep13-final.mp4
LD_NO_MUSIC=1 python3 video/ep13-mix.py final build/video.mp4 build/ build/ep13-tanpa-musik.mp4
```
