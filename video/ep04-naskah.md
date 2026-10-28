# Episode 4: Kenapa kita rela antre 2 jam buat makanan viral?

Video 9:16, 1080×1920. Timeline animasi asli 48 detik; versi final dengan narasi Gemini sekitar 51 detik (tempo animasi mengikuti narasi).
Musik dan efek suara original dari `ep04-audio.py` (bebas hak cipta), loudness -14 LUFS. Caption, hashtag, dan komentar pin ada di `ep04-copywriting.md`.

## Hook (0 sampai 3 detik)

- Frame pertama sudah berisi pertanyaan, warung "Lagi viral", dan antrean panjang, jadi bisa dipakai sebagai cover.
- Detik 0 sampai 1,8: kamera mundur dan antrean terlihat makin panjang sampai keluar layar. Jam "Waktu antre" berputar cepat sampai 2:00:00.
- Detik 2,6: punchline. Kartu rating jatuh: 3 dari 5 bintang, "Padahal rasanya… biasa aja."

## Voice over (bahasa santai, sekitar 2,5 kata per detik)

| Detik | Voice over | Di layar |
|---|---|---|
| 0,0 | Kenapa kita rela antre dua jam buat makanan viral? | Antrean panjang, jam antre sampai 2 jam |
| 2,6 | Padahal rasanya... biasa aja. | Kartu rating 3 dari 5 |
| 4,8 | Dua warung, menu sama, harga sama. Kamu pilih yang mana? | Warung A ramai, warung B sepi; tokoh "Kamu" bingung |
| 8,2 | Kebanyakan orang pilih yang ramai. Kata otak: pasti enak. | "Kamu" ikut antre di warung A; gelembung "Pasti enak" |
| 11,8 | Ada eksperimennya. New York, tahun 1969. | Jalan kota, gedung, trotoar |
| 14,2 | Satu orang disuruh berdiri di trotoar, menatap jendela lantai enam. | 1 orang menatap, garis tatapan ke jendela "Lantai 6" |
| 17,6 | Yang ikut berhenti cuma empat persen. | Penghitung 4% |
| 20,0 | Lalu yang menatap ditambah jadi lima belas orang. | 14 orang muncul, semua garis tatapan menuju jendela |
| 22,6 | Yang ikut berhenti melonjak jadi empat puluh persen. Sepuluh kali lipat! | Penghitung 40%, cap "10× lipat", pejalan kaki ikut berhenti |
| 26,4 | Padahal di atas sana nggak ada kejadian apa-apa. | Kamera zoom ke jendela kosong, bunyi jangkrik |
| 28,8 | Namanya efek ikut-ikutan. Makin panjang antrean, makin banyak yang ikut antre. | Antrean warung A bertambah, warung B meredup; kartu "Efek ikut-ikutan" |
| 33,0 | Label terlaris juga begitu. | Menu dengan cap "Terlaris" |
| 34,8 | Di restoran di Beijing, menu berlabel paling laris dipesan tiga belas sampai dua puluh persen lebih banyak. | Bar pesanan naik, "+13–20%" |
| 39,4 | Jadi ingat: antrean panjang itu bukti ramai, bukan bukti enak. Cek dulu ulasannya. | Kartu tips |
| 43,8 | Biar nggak gampang ketipu harga, follow Logika Duit! | Logo, tombol "Follow Logika Duit" ditekan, struk sumber |

## Caption

Lihat `ep04-copywriting.md` (Instagram, TikTok, komentar pin, judul alternatif, Story).

## Sumber (cek sebelum tayang)

- Milgram, S., Bickman, L. & Berkowitz, L. (1969). *Note on the Drawing Power of Crowds of Different Size.* Journal of Personality and Social Psychology, 13(2), 79–82.
  Angka 4% (1 orang menatap) dan 40% (15 orang menatap) adalah persentase pejalan kaki yang **ikut berhenti**. Ringkasan di internet kadang menulis angka lain (misalnya 45%, atau angka "ikut menengok" 42% dan 86%), jadi cocokkan dulu dengan grafik di papernya sebelum tayang.
- Banerjee, A. V. (1992). *A Simple Model of Herd Behavior.* Quarterly Journal of Economics, 107(3), 797–817. Banerjee meraih Nobel Ekonomi 2019.
- Cai, H., Chen, Y. & Fang, H. (2009). *Observational Learning: Evidence from a Randomized Natural Field Experiment.* American Economic Review, 99(3), 864–882. Eksperimen di jaringan restoran di Beijing: menampilkan 5 menu terlaris menaikkan pesanan menu itu 13–20% (dari abstrak papernya).
- Warung, nama menu, harga, rating 3/5, dan "antre 2 jam" adalah ilustrasi.

## Render

```bash
python3 -m http.server 8080            # dari folder repo
node video/render.js http://127.0.0.1:8080/video/ep04-antre-viral.html ep04.mp4 --jobs 3
node video/render.js http://127.0.0.1:8080/video/ep04-antre-viral.html cek/ --stills 0,2.6,24,27.8
```

## Dengan narasi Gemini (voice over)

Butuh `GEMINI_API_KEY` di pengaturan environment Claude Code (lihat CLAUDE.md bagian 14):
```bash
LD_TTS_OUT=build/suara.zip python3 video/ep04-tts-gemini.py   # satu permintaan, dipotong dan dicek otomatis
python3 video/ep04-mix.py prep build/suara.zip build/
python3 video/ep04-audio.py build/ build/warp.json
node video/render.js http://127.0.0.1:8080/video/ep04-antre-viral.html build/video.mp4 --warp build/warp.json --jobs 4
python3 video/ep04-mix.py final build/video.mp4 build/ build/ep04-final.mp4
```
