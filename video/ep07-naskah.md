# Episode 7: Gaji naik 5%, kok tetap bokek?

Video 9:16, 1080×1920, format pendek. Timeline animasi asli 28,5 detik; versi final dengan narasi Gemini sekitar 31 detik.
Musik dan efek suara original dari `ep07-audio.py` (bebas hak cipta), loudness -14 LUFS. Ada versi tanpa musik (`LD_NO_MUSIC=1`). Caption ada di `ep07-copywriting.md`.

## Hook (0 sampai 3 detik): kuis

- Frame pertama: dua slip gaji, "Pilihan A" naik 2% dan "Pilihan B" naik 5%, dengan pertanyaan "Gaji naik 2% atau naik 5%? Kamu pilih mana?" Bisa dipakai sebagai cover.
- Jari ragu-ragu di antara dua slip, lalu menekan Pilihan B, yang biasanya dipilih penonton juga.
- Twist berikutnya: harga barang di Pilihan B ikut naik 4%, jadi kenaikan aslinya cuma 1%. Cap "Lebih untung" mendarat di Pilihan A.

## Voice over

| Detik | Voice over | Di layar |
|---|---|---|
| 0,0 | Gaji naik dua persen, atau naik lima persen? Kamu pilih mana? | Dua slip gaji, jari memilih B |
| 2,2 | Tapi yang lima persen, harga-harga juga naik empat persen. | Daftar harga: A tetap, B naik 4% |
| 5,0 | Jadi yang lima persen sebenarnya cuma naik satu persen. Yang dua persen tetap naik dua persen. | Diagram batang "naik asli" +2% vs +1%, cap "Lebih untung" di A |
| 9,0 | Anehnya, sekitar dua dari tiga orang merasa yang lima persen lebih bahagia. | 30 orang, 20 menyala, "2 dari 3" |
| 13,0 | Namanya ilusi uang: otak lihat angka di slip gaji, bukan apa yang bisa dibeli. | "+5%" besar bergetar lalu berubah jadi "+1%" |
| 17,0 | Rumusnya: kenaikan gaji dikurangi kenaikan harga. Itu naik aslimu. | Rumus 5% − 4% = 1% |
| 21,0 | Tahun ini gajimu naik berapa persen? Tulis di komentar! | Kotak komentar dengan pilihan 0%, 3%, 5%, 10% |
| 24,0 | Biar nggak gampang ketipu harga, follow Logika Duit! | Logo, tombol "Follow Logika Duit" ditekan, struk sumber |

## Sumber (cek sebelum tayang)

- Shafir, E., Diamond, P. & Tversky, A. (1997). *Money Illusion.* Quarterly Journal of Economics, 112(2), 341–374. Cerita Ann (gaji naik 2%, tanpa inflasi) dan Barbara (gaji naik 5%, inflasi 4%). Saat ditanya siapa yang lebih untung secara ekonomi, kebanyakan memilih Ann; saat ditanya siapa yang lebih bahagia, sekitar dua pertiga memilih Barbara. Hasilnya diulang dengan hasil serupa oleh studi 2021 di Journal of Economic Psychology.
- Gaji Rp5.000.000, harga beras, bensin, kopi, dan inflasi 4% adalah ilustrasi (angka 2%, 5%, dan 4% sama dengan cerita di penelitian).

## Render

```bash
python3 -m http.server 8080            # dari folder repo
LD_TTS_OUT=build/suara.zip python3 video/ep07-tts-gemini.py
python3 video/ep07-mix.py prep build/suara.zip build/
python3 video/ep07-audio.py build/ build/warp.json
node video/render.js http://127.0.0.1:8080/video/ep07-gaji-naik.html build/video.mp4 --warp build/warp.json --jobs 4
python3 video/ep07-mix.py final build/video.mp4 build/ build/ep07-final.mp4
LD_NO_MUSIC=1 python3 video/ep07-mix.py final build/video.mp4 build/ build/ep07-tanpa-musik.mp4
```
