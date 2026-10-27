# Episode 3: Gratis ongkir, kok bikin belanja lebih mahal?

Video 9:16, 1080×1920, 42 detik. Sumber visual: `ep03-gratis-ongkir.html`, render dengan `render.js`.
Ada dua versi: tanpa suara, dan dengan musik + efek suara original dari `ep03-audio.py` (bebas hak cipta, -14 LUFS). Voice over di bawah bisa ditambahkan di atas versi musik.

## Hook (0 sampai 3 detik)

- Frame pertama sudah berisi pertanyaan dan keranjang belanja, jadi bisa dipakai sebagai cover.
- Detik 0,3 sampai 1,4: jari menekan "+ Tambah", barang masuk keranjang, bar gratis ongkir penuh dan menyala.
- Detik 2,2: twist. "Hemat ongkir Rp10.000, tapi nambah belanja Rp28.000."

## Voice over (bahasa santai, sekitar 2,5 kata per detik)

| Detik | Voice over | Teks di layar |
|---|---|---|
| 0,0 | Pernah nambah barang biar dapat gratis ongkir? | Pernah nambah barang biar dapat gratis ongkir? |
| 2,2 | Hemat ongkir sepuluh ribu, tapi nambah belanja dua puluh delapan ribu. | Hemat ongkir Rp10.000, tapi nambah belanja Rp28.000. |
| 4,8 | Totalnya malah delapan belas ribu lebih mahal. | Totalnya malah Rp18.000 lebih mahal. |
| 6,6 | Kok kita tetap merasa menang? | Kok kita tetap merasa menang? |
| 8,2 | Ada eksperimennya. Peneliti menjual dua coklat. | Ada eksperimennya. Peneliti menjual dua coklat. |
| 10,6 | Yang premium lima belas sen, yang biasa satu sen. Kamu pilih yang mana? | Premium 15 sen, biasa 1 sen. Kamu pilih yang mana? |
| 13,5 | Tujuh puluh tiga persen pilih yang premium. Masuk akal. | 73% pilih yang premium. Masuk akal. |
| 16,5 | Lalu dua-duanya diturunkan satu sen. | Lalu dua-duanya diturunkan 1 sen. |
| 19,0 | Yang biasa jadi gratis. | Yang biasa jadi gratis. |
| 21,5 | Hasilnya berbalik: enam puluh sembilan persen pilih yang gratis. | Hasilnya berbalik: 69% pilih yang gratis. |
| 24,5 | Padahal selisih harganya tetap empat belas sen. | Padahal selisih harganya tetap 14 sen. |
| 27,5 | Kata "gratis" bikin otak berhenti menghitung. Namanya efek harga nol. | Kata "gratis" bikin otak berhenti menghitung. |
| 31,0 | Promo gratis ongkir pakai trik yang sama. | Promo gratis ongkir pakai trik yang sama. |
| 34,0 | Sebelum nambah barang, tanya dulu: kalau ongkirnya bayar, barang ini tetap kamu beli? | Sebelum nambah barang, tanya dulu: (kartu tips) |
| 38,0 | Biar nggak gampang ketipu harga, follow Logika Duit! | Biar nggak gampang ketipu harga, follow Logika Duit! (logo, tombol "Follow Logika Duit" ditekan, struk sumber) |

## Caption untuk Instagram dan TikTok

> Gratis ongkir minimal Rp50 ribu, kurang Rp8 ribu lagi... akhirnya nambah barang Rp28 ribu. 🙃
>
> Ternyata ada eksperimennya: begitu satu coklat jadi gratis, pilihan orang langsung berbalik, padahal selisih harganya sama persis. Namanya efek harga nol.
>
> Tips: sebelum nambah barang, tanya dulu "kalau ongkirnya bayar, barang ini tetap kubeli?"
>
> Kamu pernah begini juga? Cerita di komentar, dan follow Logika Duit buat episode berikutnya.
>
> Sumber: Shampanier, Mazar & Ariely (2007), Marketing Science; Ariely (2008), Predictably Irrational, bab 3. Harga keranjang hanya ilustrasi.
>
> #logikaduit #gratisongkir #belanjaonline #edukasikeuangan #ekonomi #psikologibelanja #hemat

## Sumber (cek sebelum tayang)

- Shampanier, K., Mazar, N. & Ariely, D. (2007). *Zero as a Special Price: The True Value of Free Products.* Marketing Science, 26(6), 742–757.
- Ariely, D. (2008). *Predictably Irrational,* bab 3 ("The Cost of Zero Cost"). Angka 73% dan 27%, lalu 31% dan 69%, diambil dari eksperimen coklat di bab ini. Cocokkan dulu dengan bukunya sebelum tayang.
- Angka di keranjang (Rp42.000, Rp28.000, ongkir Rp10.000, minimal belanja Rp50.000) adalah ilustrasi.

## Render ulang

```bash
python3 -m http.server 8080            # dari folder repo
node video/render.js http://127.0.0.1:8080/video/ep03-gratis-ongkir.html ep03.mp4 --jobs 3
node video/render.js http://127.0.0.1:8080/video/ep03-gratis-ongkir.html cek/ --stills 0,2.2,19
```

## Dengan narasi Gemini (voice over)

1. Di VPS: `logikaduit-deploy && python3 /opt/logikaduit/video/ep03-tts-gemini.py` (atau `--voice Leda`).
   Hasilnya `/root/logikaduit-ep03-suara.zip`, berisi satu WAV per kalimat.
2. Di mesin render:
   ```bash
   python3 video/ep03-mix.py prep suara.zip build/        # vo.wav + warp.json (tempo menyesuaikan suara)
   python3 video/ep03-audio.py build/ build/warp.json     # music.wav + sfx.wav ikut tempo baru
   node video/render.js http://127.0.0.1:8080/video/ep03-gratis-ongkir.html build/video.mp4 --warp build/warp.json --jobs 3
   python3 video/ep03-mix.py final build/video.mp4 build/ ep03-final.mp4   # musik mengecil saat narasi, -14 LUFS
   ```
