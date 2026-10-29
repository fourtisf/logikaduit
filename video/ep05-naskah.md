# Episode 5: Duit Mixue ternyata dari mana?

Video 9:16, 1080×1920, format pendek. Timeline animasi asli 25 detik; versi final dengan narasi Gemini sekitar 27 detik.
Musik dan efek suara original dari `ep05-audio.py` (bebas hak cipta), loudness -14 LUFS. Ada juga versi tanpa musik (`LD_NO_MUSIC=1`) untuk ditambah suara yang sedang tren di aplikasi. Caption ada di `ep05-copywriting.md`.

## Kenapa format pendek

EP3 dan EP4 (sekitar 50 detik) sepi penonton. Perubahan di EP5:
- 25–30 detik, satu poin saja.
- Kalimat pertama langsung pernyataan berani yang menyangkut penonton, terdengar sejak detik 0.
- Contoh lokal yang dikenal semua orang (Mixue), bukan eksperimen luar negeri.
- Ditutup pertanyaan yang memancing komentar sebelum ajakan follow.

## Hook (0 sampai 2 detik)

- Frame pertama: "Hampir semua duit Mixue bukan dari es krim yang kamu beli" + es krim besar, jadi bisa dipakai sebagai cover.
- Detik 0,1 sampai 1,4: koin dari tokoh "Kamu" melompat masuk ke es krim.
- Detik 1,65: cap "Bukan dari sini" menghantam es krim, layar bergetar.

## Voice over

| Detik | Voice over | Di layar |
|---|---|---|
| 0,0 | Hampir semua duit Mixue bukan dari es krim yang kamu beli. | Koin masuk ke es krim, cap "Bukan dari sini" |
| 3,2 | Sembilan puluh tujuh koma enam persen pendapatannya dari jualan bahan dan alat ke pemilik gerai. | Donat 97,6% vs biaya waralaba 2,4% |
| 7,4 | Gula, susu, cup, sampai mesin es krim, dibeli pemilik gerai dari pusat. | Barang terbang dari "Pusat" ke gerai, uang kembali ke pusat |
| 11,0 | Jadi makin banyak gerai buka, makin cuan pusatnya. | Gerai bertambah jadi 24, bar "Pemasukan pusat" penuh |
| 14,4 | Mixue lebih mirip pemasok daripada toko es krim. | "Toko es krim" dicoret, cap "Pemasok" |
| 17,6 | Menurut kamu, buka gerai Mixue masih untung nggak? Tulis di komentar! | Kartu pilihan "Masih untung" / "Udah nggak" |
| 20,8 | Biar nggak gampang ketipu harga, follow Logika Duit! | Logo, tombol "Follow Logika Duit" ditekan, struk sumber |

Di naskah TTS, "Mixue" ditulis "Miksue" supaya dibaca seperti orang Indonesia menyebutnya.

## Sumber (cek sebelum tayang)

- Mixue Group (2025). *Prospektus Global Offering.* Bursa Efek Hong Kong. Pendapatan Januari–September 2024: penjualan barang dan peralatan ke pemilik waralaba 97,6%, biaya waralaba 2,4%. Laporan tahunan 2024 memberi perbandingan yang hampir sama (barang dan peralatan RMB24.208,8 juta, waralaba RMB620,1 juta, sekitar 97,5%).
- Gambar es krim, gerai, dan jumlah gerai di animasi adalah ilustrasi. Tidak memakai logo atau maskot Mixue.

## Render

```bash
python3 -m http.server 8080            # dari folder repo
LD_TTS_OUT=build/suara.zip python3 video/ep05-tts-gemini.py
python3 video/ep05-mix.py prep build/suara.zip build/
python3 video/ep05-audio.py build/ build/warp.json
node video/render.js http://127.0.0.1:8080/video/ep05-mixue.html build/video.mp4 --warp build/warp.json --jobs 4
python3 video/ep05-mix.py final build/video.mp4 build/ build/ep05-final.mp4
LD_NO_MUSIC=1 python3 video/ep05-mix.py final build/video.mp4 build/ build/ep05-tanpa-musik.mp4
```
