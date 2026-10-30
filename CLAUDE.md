# Logika Duit: website logikaduit.com

> **Prompt pembuka untuk Claude Code** (salin ke chat pertama):
>
> Baca file CLAUDE.md di folder ini sampai habis, lalu kerjakan semua poin di bagian "Tugasmu". Website-nya sudah jadi di index.html, jadi jangan dibuat ulang. Tugas utamamu: cek, rapikan kalau ada yang rusak, lalu online-kan di https://logikaduit.com lewat Hostinger. Tanya saya hanya kalau kamu butuh akses (login hPanel, FTP, atau SSH). Laporkan hasilnya dalam bahasa Indonesia yang sederhana, karena saya bukan programmer.

---

## 1. Tugasmu

1. Baca file ini dan `index.html` sampai paham struktur, gaya, dan aturannya.
2. Jalankan website secara lokal (misalnya `npx serve .` atau `python3 -m http.server`), lalu cek di lebar desktop (1440px) dan HP (390px). Pastikan tidak ada error di console dan tidak ada scroll ke samping di HP.
3. Pastikan animasi 3D di bagian atas jalan, label bisa diputar dengan diseret, dan tombol "Bulatkan ke atas" membalik label. Matikan WebGL atau blok CDN Three.js untuk memastikan cadangan SVG muncul.
4. Online-kan ke **https://logikaduit.com** di Hostinger (lihat bagian 9). Aktifkan HTTPS. Arahkan `www.logikaduit.com` dan `http://` ke `https://logikaduit.com`.
5. Jalankan checklist di bagian 12, lalu kirim laporan singkat plus screenshot desktop dan HP ke ALFA.
6. Kalau ALFA mengirim link TikTok, isi di objek `LINKS` (bagian 8). Tombol TikTok otomatis muncul.

Jangan membangun ulang situs ini dengan framework (React, Next.js, Tailwind build, dan sejenisnya) kecuali ALFA memintanya. Situs ini sengaja dibuat **satu file HTML statis** supaya gampang di-upload dan cepat.

---

## 2. Tentang brand

- **Nama:** Logika Duit. Di video dan logo hanya ditulis "Logika Duit" atau "LOGIKA DUIT", tanpa username.
- **Instagram:** @logika_duit. **TikTok:** @logikaduit_ (https://www.tiktok.com/@logikaduit_).
- **Isi:** video pendek (sekitar 40 detik, format 9:16) yang menjelaskan ekonomi sehari-hari. Contohnya: kenapa minimarket buka sebelahan, kenapa harga berakhiran 9, matematika diskon. Setiap klaim harus berbasis riset dan sumbernya dicantumkan.
- **Tagline:** "Ekonomi sehari-hari, kok bisa?"
- **Gaya bahasa:** bahasa Indonesia santai tapi jelas, dengan "kamu" dan "nggak". Kalimatnya pendek, tanpa istilah yang bikin pusing.
- **Penonton:** anak muda Indonesia (18 sampai 35 tahun) yang suka belanja dan penasaran soal uang.
- Logika Duit adalah brand **terpisah** dari "Ruang Pikir" (brand psikologi milik ALFA yang berwarna ungu). Jangan dicampur.
- **Logo:** lampu ide dengan filamen spiral, warna hijau zamrud, dalam kotak gelap membulat. Tidak ada simbol "Rp" di logo.

---

## 3. Isi paket

```
logikaduit-website/
├── index.html          ← SELURUH website (HTML + CSS + JS dalam satu file)
├── og-image.png        ← gambar pratinjau saat link dibagikan (1200×630)
├── .htaccess           ← redirect ke https://logikaduit.com, cache, gzip (Hostinger)
├── CLAUDE.md           ← file ini
└── assets/
    ├── logikaduit-icon.png            ← ikon app (dipakai sebagai apple-touch-icon)
    ├── logikaduit-icon.svg            ← logo lampu versi vektor
    ├── logikaduit-logo-horizontal.png ← logo + wordmark
    └── logikaduit-foto-profil.png     ← foto profil Instagram/TikTok
```

Yang wajib di-upload ke server adalah `index.html`, `og-image.png`, folder `assets/`, dan `.htaccess` (hanya setelah SSL aktif, lihat bagian 9). `CLAUDE.md` tidak perlu di-upload.

Font dimuat dari Google Fonts. Three.js r128 dimuat dari cdnjs, dengan cadangan jsDelivr, dan dimuat **async** oleh script utama (bukan tag `<script src>` yang menahan tampilan). Tidak ada file JS atau CSS lain.

---

## 4. Design system

### Warna (sudah ada sebagai CSS variable di `:root`)

| Token | Hex | Dipakai untuk |
|---|---|---|
| `--ink` | `#03100B` | latar halaman (hijau-hitam) |
| `--deep` | `#071C15` | permukaan / panel |
| `--moss` | `#103426` | garis, panel terang |
| `--emerald` | `#2EE6A0` | aksen brand, tombol utama, angka penting |
| `--mint` | `#9DF5CF` | aksen lembut, garis tipis |
| `--ice` | `#E6FFF4` | teks utama |
| `--sage` | `#8BA79B` | teks redup / keterangan |

Pendukung: zamrud tua `#0E8F64` dan `#0B4D38` untuk gradasi dan cahaya latar.

### Tipografi
- **Plus Jakarta Sans** (400, 500, 700, 800) untuk semua teks. Judul besar memakai 800 dengan letter-spacing negatif (sekitar −0.035em) dan line-height rapat.
- **JetBrains Mono** (500 dan 700) **hanya** untuk "struk sumber" dan nomor barcode, sebagai gaya kertas struk kasir.
- Angka memakai `font-feature-settings: "tnum"` supaya harga sejajar.

### Gaya visual
- Latar gelap dengan cahaya zamrud statis (radial gradient) dan butiran halus (noise SVG). Latarnya `position: fixed`, jadi **tidak boleh ada pita atau kotak beda warna** saat di-scroll.
- Panel kaca gelap: gradasi hijau tua, garis tipis mint transparan (`inset box-shadow`), dan bayangan lembut.
- Tombol utama berbentuk pil dengan gradasi zamrud dan glow. Tombol kedua berbentuk pil transparan dengan garis mint tipis.
- Elemen khas brand: **label harga** (hero), **struk kasir** (kotak sumber dengan tepi bergerigi), dan **peta jalan dengan pin toko** (simulasi Hotelling).

### Aturan gaya (wajib)
- **Jangan** memakai latar terang atau putih, skema hitam-emas, atau warna merah/pink.
- **Jangan** memakai pemisah titik tengah "·" dan label kecil ALL CAPS di atas judul. Pengecualian: wordmark logo "LOGIKA DUIT".
- Pakai sentence case untuk judul dan tombol.
- Teks tombol harus menyebut aksinya ("Follow di Instagram", "Bulatkan ke atas"), tanpa panah "→".
- Gerakan otomatis seperlunya saja. Satu momen utama ada di hero 3D. Jangan menambah animasi fade-up di setiap section.

---

## 5. Struktur halaman (urutan section)

1. **Header** (sticky, blur): logo lampu, wordmark LOGIKA DUIT, menu (Episode, Segera tayang, Tentang), dan tombol "Follow". Di HP menunya disembunyikan dan hanya tombol Follow yang tampil.
2. **Hero:** judul "Ekonomi sehari-hari, kok bisa?", paragraf pengantar, dan tombol (Follow di Instagram, TikTok kalau link ada, Lihat episode). Di sebelah kanan ada **label harga 3D** (bagian 6), dua kotak keterangan ("Yang dibaca otak" dan "Selisih sebenarnya"), petunjuk, serta tombol "Bulatkan ke atas" / "Kembalikan harga toko".
3. **Episode** (`#episode`): setiap episode berupa `<article class="ep">` dengan dua kolom. Kolom kiri berisi nomor episode, pertanyaan (h3), penjelasan, dan struk sumber. Kolom kanan berisi panel interaktif "Coba sendiri".
   - Episode 1: Kenapa Indomaret dan Alfamart selalu sebelahan? (Hukum Hotelling)
   - Episode 2: Harga Rp99.900, kok kerasa jauh lebih murah dari Rp100.000? (efek digit kiri)
4. **Segera tayang** (`#segera`): tiga topik yang sedang diriset, ditambah kotak ajakan "Kirim lewat DM".
5. **Tentang** (`#tentang`): satu kalimat besar tentang Logika Duit dan tiga prinsip (Riset dulu, baru bikin / Satu menit cukup / Sumbernya selalu ada).
6. **Footer:** logo besar, "Biar nggak gampang ketipu harga.", tombol Follow, dan © 2026 Logika Duit.

---

## 6. Animasi 3D di hero (Three.js r128)

**Konsep:** label harga 3D yang menggantung di rel besi. Sisi depan bertuliskan **Rp99.900** (hijau, digit kiri diberi kotak). Sisi belakang bertuliskan **Rp100.000** (putih, digit "1" diberi kotak). Ini memvisualkan inti brand: harga yang terasa vs harga yang dibayar.

**Komponen scene** (semuanya ada di fungsi `initLD3D()` di index.html):
- Label: `ExtrudeGeometry` berbentuk segi lima dengan lubang tali, dengan bevel tipis.
  - Permukaan memakai `MeshPhysicalMaterial` hijau gelap dengan clearcoat.
  - Sisi tebalnya memakai bahan zamrud yang menyala (emissive).
- Teks depan dan belakang adalah `CanvasTexture` yang digambar dengan font Plus Jakarta Sans, lalu dipasang di plane tipis tepat di atas permukaan label. Teks digambar ulang setelah font selesai dimuat.
- Tali tipis, rel silinder metalik, dan paku.
- Cahaya zamrud di belakang label (plane dengan radial gradient, additive blending).
- Enam koin "Rp" 3D yang melayang dan berputar pelan di belakang label, ditambah partikel debu cahaya.
- Pencahayaan: ambient mint, directional putih, point light zamrud kiri-bawah, dan rim light di belakang.

**Interaksi:**
- Saat halaman dibuka, label masuk dengan ayunan dan putaran lalu tenang (fisika pegas teredam). Setelah itu label bergoyang pelan.
- Seret ke kiri atau kanan untuk memutar label (sumbu Y) dan mengayunkannya (sumbu Z). Saat dilepas, label kembali menghadap depan.
- Tombol "Bulatkan ke atas" membalik label 180° (sekitar 1,1 detik, ease-in-out) ke sisi Rp100.000. Tombol berubah jadi "Kembalikan harga toko". Teks di kotak keterangan ikut berubah.
- Kamera sedikit bergeser mengikuti posisi kursor (parallax).

**Wajib dipertahankan:**
- **Cadangan:** kalau WebGL tidak ada atau Three.js gagal dimuat dari cdnjs **dan** jsDelivr, label SVG 2D otomatis dipakai (class `.is3d` tidak ditambahkan, atau dilepas lagi).
  - Urutannya: script utama membuat konteks WebGL di `#tag3d` dulu. Kalau tidak ada, atau GPU-nya software (SwiftShader, llvmpipe), SVG langsung dipakai dan Three.js **tidak diunduh**. Kalau ada GPU sungguhan, `.is3d` dipasang (ruangnya disiapkan, jadi tidak ada pergeseran tata letak), lalu Three.js dimuat async dan `initLD3D(gl)` dipanggil. Kalau dua CDN gagal atau lewat 8 detik, SVG mengambil alih lewat event `svgmode`.
  - Mesin uji Lighthouse/PageSpeed tidak punya GPU, jadi skornya mengukur versi SVG. Untuk menguji jalur 3D di mesin tanpa GPU, samarkan nama renderer (`UNMASKED_RENDERER_WEBGL`) di skrip tes, jangan di index.html.
- **Tepi kanvas:** `#tag3d` memakai `mask-image` yang memudar di tepi kiri-kanan, supaya cahaya zamrud tidak terpotong jadi kotak samar.
- **Hemat baterai:** render berhenti saat hero tidak terlihat (IntersectionObserver) atau tab disembunyikan. `pixelRatio` maksimal 2.
- **`prefers-reduced-motion`:** tanpa ayunan atau putaran otomatis, dan pembalikan label langsung tanpa animasi.
- **Warna:** Three.js r128 menganggap warna hex sebagai linear. Karena itu semua warna dilewatkan ke `C(hex)` (`convertSRGBToLinear()`), dan `renderer.outputEncoding = sRGBEncoding`.
  - Kalau suatu saat Three.js di-upgrade ke r152+, ganti ke `outputColorSpace` / `ColorManagement` dan cek ulang warnanya. Tanpa itu, label akan terlihat pucat atau terlalu terang.
- Di HP, seret vertikal tetap menggulir halaman (`touch-action: pan-y`).

**Ide 3D tambahan (opsional, hanya kalau ALFA minta):** logo lampu 3D yang menyala di footer, atau koin yang jatuh saat tombol Follow di-hover. Tetap hanya satu momen 3D utama, jangan sampai halaman berat.

---

## 7. Interaksi lain

### Episode 1: simulasi Hukum Hotelling
- SVG jalan dengan 24 rumah dan dua pin toko (A berwarna zamrud, B berwarna putih es).
- Pin bisa diseret, atau difokus lalu digeser dengan tombol panah (`role="slider"`).
- Setiap rumah berbelanja di toko terdekat. Warna rumah dan persentase pembeli diperbarui langsung.
- Tombol "Biarkan mereka bersaing" membuat toko bergeser bergantian ke tengah sampai sebelahan (posisi 44% dan 56%). Tombolnya lalu berubah jadi "Ulangi".

### Episode 2: Keranjang jujur
- Daftar barang (harga ilustrasi berakhiran 900) dengan checkbox, plus input "Tambah harga".
- Tiga total: **Kalau cuma baca angka depan** (dibulatkan ke bawah per ribuan), **Yang dibayar di kasir** (asli), dan **Kalau dibulatkan ke atas**. Di bawahnya ada kalimat yang menyebut selisih yang "nggak kerasa".

---

## 8. Link (ubah di satu tempat)

Di awal `<script>` utama:
```js
const LINKS = {
  instagram: 'https://www.instagram.com/logika_duit/',
  dm: 'https://ig.me/m/logika_duit',
  tiktok: 'https://www.tiktok.com/@logikaduit_'   // kosongkan ('') untuk menyembunyikan tombol TikTok
};
```
Elemen dengan `data-link="..."` otomatis memakai link ini. Kalau nilainya kosong, elemen disembunyikan.

---

## 9. Deploy ke Hostinger

**DNS saat ini** (di hPanel → Domain → logikaduit.com → DNS):
- `A  @  31.97.111.49` (TTL 300)
- `CNAME  www  logikaduit.com` (TTL 300)

Cari tahu dulu jenis hostingnya. Kalau di hPanel → **Websites** ada logikaduit.com, berarti shared/cloud hosting. Kalau IP 31.97.111.49 adalah **VPS** milik ALFA, berarti VPS. Kalau ragu, tanya ALFA.

### A. Shared / Cloud hosting (paling umum)
1. hPanel → Websites → logikaduit.com → **File Manager** → buka `public_html`. Cara lain: pakai FTP. Kredensial FTP ada di hPanel → Files → FTP Accounts, dan **harus diminta ke ALFA**.
2. Hapus file bawaan Hostinger (misalnya `default.php` atau `index.php` bawaan).
3. Upload `index.html`, `og-image.png`, dan folder `assets/`.
4. hPanel → Security → **SSL**: pasang SSL gratis untuk logikaduit.com dan www, lalu aktifkan **Force HTTPS**.
5. **Setelah SSL aktif**, upload `.htaccess` (sudah ada di repo) ke `public_html`. Kalau di-upload sebelum SSL aktif, semua pengunjung diarahkan ke https yang belum jalan. Server Hostinger memakai LiteSpeed, jadi aturan Apache berlaku. Isinya:
   ```apache
   DirectoryIndex index.html

   RewriteEngine On
   RewriteCond %{HTTPS} off [OR]
   RewriteCond %{HTTP_HOST} ^www\. [NC]
   RewriteRule ^ https://logikaduit.com%{REQUEST_URI} [L,R=301]

   <IfModule mod_expires.c>
     ExpiresActive On
     ExpiresByType text/html "access plus 10 minutes"
     ExpiresByType image/png "access plus 30 days"
     ExpiresByType image/svg+xml "access plus 30 days"
   </IfModule>
   <IfModule mod_deflate.c>
     AddOutputFilterByType DEFLATE text/html text/css application/javascript image/svg+xml
   </IfModule>
   ```

### B. VPS (yang dipakai sekarang)
31.97.111.49 adalah VPS Ubuntu milik ALFA (`srv1042502`, nginx). Server ini juga menjalankan ruangpikir.id, jadi jangan ubah konfigurasi situs lain. ALFA menjalankan perintah sendiri lewat Termius; Claude tidak punya akses SSH.

- **Pasang pertama kali** (sebagai root):
  ```bash
  git clone -b main https://github.com/fourtisf/logikaduit.git /opt/logikaduit && bash /opt/logikaduit/deploy/setup-vps.sh
  ```
  `deploy/setup-vps.sh` memastikan nginx yang memegang port 80/443, menyalin file publik ke `/var/www/logikaduit.com`, meminta SSL Let's Encrypt (webroot, dengan reload nginx saat perpanjangan), lalu menulis `/etc/nginx/sites-available/logikaduit.com`: http dan www diarahkan 301 ke `https://logikaduit.com`, gzip, cache 10 menit untuk html dan 30 hari untuk png/svg. Kalau `nginx -t` gagal, konfigurasi logikaduit.com dikembalikan dan nginx tidak di-reload. Aman dijalankan ulang.
- **Update berikutnya:** `logikaduit-deploy` (ambil commit terbaru dari cabang di `/etc/logikaduit-branch`). Untuk kembali ke versi lama: `logikaduit-deploy <commit>`. Hanya `index.html`, `og-image.png`, dan `assets/` yang di-upload; `.htaccess` tidak dipakai nginx.
- Cabang yang di-deploy adalah `main`. Server yang dipasang dari cabang kerja lama (`claude/new-session-bn6437`) cukup dipindah sekali: `echo main > /etc/logikaduit-branch && logikaduit-deploy`.
- Alur kerja: perubahan dikerjakan di cabang kerja, lalu digabung ke `main` setelah dicek. Server hanya mengambil dari `main`.

**Keamanan:** jangan pernah menyimpan password, kredensial FTP/SSH, atau API key di file proyek, commit, atau log.

---

## 10. Fakta & sumber (jangan diubah tanpa cek sumber)

- **Hukum Hotelling:** Hotelling, H. (1929). *Stability in Competition.* The Economic Journal, 39(153), 41–57. Isinya: dua penjual di satu "jalan" akan bergeser ke tengah sampai berdampingan.
- **Efek digit kiri:** Thomas, M. & Morwitz, V. (2005). *Penny Wise and Pound Foolish: The Left-Digit Effect in Price Cognition.* Journal of Consumer Research, 32(1), 54–64.
- **Baju $39 vs $34:** Anderson, E. & Simester, D. (2003). *Mind Your Pricing Cues.* Harvard Business Review, 81(9). Dalam uji katalog baju wanita, menaikkan harga dari $34 ke $39 justru menaikkan permintaan sekitar sepertiga.
- Harga barang di "Keranjang jujur" adalah **ilustrasi** (dan ditulis begitu di halaman).

Kalau menambah episode, setiap klaim angka wajib punya sumber yang bisa dicek, dan sumbernya ditulis di struk.

---

## 11. Cara menambah episode baru

Salin satu blok `<article class="ep" id="epN">` lalu ganti:
- `ep-no` menjadi "Episode N".
- `h3` berisi pertanyaannya, ditulis seperti judul video.
- Dua paragraf penjelasan. Konsep kunci ditebalkan dengan `<strong>`.
- `.receipt` berisi daftar sumber (format: Penulis (Tahun). *Judul.* Jurnal, volume(nomor), halaman).
- Panel `.lab` berisi interaksi kecil yang membuktikan konsepnya. Kalau belum ada, boleh diganti tombol "Tonton di Instagram".
- Pindahkan topik itu dari daftar "Segera tayang".

Ide interaksi untuk topik yang sedang diriset:
- **Diskon 50% + 20%:** dua slider diskon dengan hasil 1 − (1−a)(1−b). Contoh: 50% + 20% = 60%, bukan 70%.
- **Popcorn bioskop:** perbandingan margin tiket vs makanan, pakai sumber riset.
- **Beli 2 gratis 1:** kalkulator harga per unit vs kebutuhan sebenarnya.

---

## 12. Checklist selesai

- [ ] https://logikaduit.com terbuka dengan gembok HTTPS. `www` dan `http` diarahkan ke situ.
- [ ] Label 3D tampil, bisa diseret, dan tombol "Bulatkan ke atas" membalik label. Cadangan SVG tampil kalau WebGL mati.
- [ ] Tidak ada error di console (desktop dan HP).
- [ ] Lebar 390px tidak bisa di-scroll ke samping. Teks tidak terpotong.
- [ ] Simulasi Hotelling dan Keranjang jujur berfungsi, termasuk dengan keyboard.
- [ ] Lighthouse (mobile): Performance ≥ 85, Accessibility ≥ 95, Best Practices ≥ 95, SEO ≥ 95.
- [ ] Pratinjau link (WhatsApp / X / Facebook) menampilkan og-image.png dan judulnya.
- [ ] Ikon tab (favicon) berupa lampu Logika Duit.
- [ ] Link Instagram, DM, dan TikTok benar. Tombol TikTok tampil di hero dan footer.
- [ ] Tidak ada latar putih atau terang dan tidak ada pita warna aneh saat di-scroll.

## 13. Cara melapor ke ALFA

Pakai bahasa Indonesia sederhana tanpa jargon. Sampaikan:
1. Link website yang sudah online.
2. Apa saja yang dicek dan hasilnya.
3. Apa yang diubah, kalau ada.
4. Apa yang masih butuh keputusan atau akses dari ALFA.

Sertakan screenshot desktop dan HP.

---

## 14. Video pendek (Reels/TikTok)

Sumber video ada di folder `video/` (tidak ikut di-deploy ke website). Contoh lengkap: Episode 3 (gratis ongkir, `ep03-*`), Episode 4 (antre makanan viral, `ep04-*`), Episode 5 (duit Mixue, `ep05-*`), Episode 6 (isi snack makin kecil, `ep06-*`), dan Episode 7 (gaji naik 5%, `ep07-*`); EP5 sampai EP7 format pendek. Tiap episode punya:
- `epNN-<judul>.html`: animasi 9:16 (1080×1920) dengan `window.render(t)`, gaya visual sama dengan website.
- `epNN-naskah.md`: voice over per detik dan sumber.
- `epNN-copywriting.md`: caption Instagram dan TikTok, hashtag, komentar pin, judul alternatif, Story.
- `epNN-audio.py`: aransemen musik dan waktu efek suara episode itu.
- `epNN-tts-gemini.py`: naskah narasi (satu kalimat per teks layar).
- `epNN-mix.py`: awal tiap teks layar (sama dengan `CAPS` di HTML) dan jeda khusus.

Bahan bersama (dipakai semua episode, jangan disalin ke file episode):
- `audio_lib.py`: instrumen dan efek suara yang disintesis (bebas hak cipta), reverb, penulisan WAV.
- `tts_gemini.py`: narasi Gemini TTS, satu WAV per kalimat.
- `mix.py`: menyelaraskan tempo animasi dengan narasi (`warp.json`), lalu mixing akhir (-14 LUFS, musik mengecil saat narasi).
- `render.js`: render per frame lewat Playwright ke MP4 (`--jobs 3` untuk paralel, `--warp` untuk tempo baru).

Episode baru: salin file `ep05-*`, ganti isinya, dan pastikan jumlah kalimat narasi sama dengan jumlah teks layar.

**Format video (pelajaran dari EP3 dan EP4, sekitar 50 detik, sepi penonton):**
- Durasi 20–30 detik, satu poin saja.
- Kalimat pertama berupa pernyataan berani yang menyangkut penonton, terdengar sejak detik 0, dan frame pertama bisa jadi cover.
- Pakai contoh lokal yang dikenal semua orang (Mixue, Indomaret, Shopee, gaji UMR). Riset tetap wajib, tapi cukup ditulis di struk dan caption.
- Tutup dengan pertanyaan yang memancing komentar, lalu ajakan follow.
- Buat juga versi tanpa musik (`LD_NO_MUSIC=1 python3 video/epNN-mix.py final ...`), supaya ALFA bisa menambah suara yang sedang tren di aplikasi.
- Jangan memakai logo atau maskot merek; cukup sebut namanya.

**Suara AI:** butuh `GEMINI_API_KEY` di pengaturan environment Claude Code (menu environment di judul sesi, lalu Edit). ALFA menyimpannya sendiri; **jangan pernah minta key ditempel di chat**, dan jangan mencetak atau menyimpannya di repo. Kalau key ada, buat video lengkap langsung di sesi ini (contoh EP3; untuk episode lain ganti `ep03` dan nama file HTML-nya):
```bash
python3 -m http.server 8080 &                                       # dari folder repo
LD_TTS_OUT=build/suara.zip python3 video/ep03-tts-gemini.py        # --voice Leda untuk suara cewek
python3 video/ep03-mix.py prep build/suara.zip build/
python3 video/ep03-audio.py build/ build/warp.json
node video/render.js http://127.0.0.1:8080/video/ep03-gratis-ongkir.html build/video.mp4 --warp build/warp.json --jobs 3
python3 video/ep03-mix.py final build/video.mp4 build/ build/ep03-final.mp4
```
Kalau key belum ada, kirim versi musik + efek suara dan jelaskan cara menyimpan key ke ALFA. Render 42 detik butuh sekitar 10 sampai 20 menit. Angka dari riset di video wajib dicek ke sumber aslinya sebelum tayang.

Catatan Gemini TTS (akun ALFA, Oktober 2026):
- Akun gratis: kuota TTS kecil per hari **per model**. Karena itu seluruh naskah dibacakan dalam **satu permintaan**, lalu dipotong per kalimat. Kalau kuota satu model habis, skrip pindah ke model TTS lain (`gemini-3.8-flash-tts`, `gemini-3.8-flash-lite-tts`, `gemini-3.1-flash-tts-preview`, dan seterusnya).
- Arahan gaya harus singkat dan berbahasa Inggris. Arahan panjang berbahasa Indonesia ikut dibacakan oleh model 3.8.
- Hasil potongan dicek otomatis dengan transkrip (`gemini-3.5-flash-lite`, kuota terpisah). Transkrip harus **satu klip per permintaan**; kalau banyak klip dikirim sekaligus, model mencampur isi antar-klip.
- Model `gemini-2.5-flash` dan `gemini-2.5-flash-lite` sudah tidak tersedia untuk akun ini.
- Tahun ditulis dengan kata di naskah ("seribu sembilan ratus enam puluh sembilan"), supaya dibaca dalam bahasa Indonesia. Nama merek ditulis sesuai ucapan ("Miksue" untuk Mixue); teks layar tetap ejaan asli.
- Model kadang ikut membacakan arahan gaya di awal, tidak menentu (arahan yang sama pernah aman; terjadi di EP5, EP6, EP7). `tts_gemini.py` mengenalinya dari transkrip potongan pertama, lalu memotong ulang dan membuang bagian itu otomatis. Transkrip 8 detik pertama tidak bisa dipakai untuk ini, karena model transkrip melewatkan kalimat bahasa Inggris di tengah audio. Arahan lain ("energetic, punchy") lebih sering ikut dibacakan, jadi jangan diganti.
- Transkrip yang jauh dari naskah ditandai "TIDAK COCOK". Kalau muncul, dengarkan potongannya sebelum dipakai.
- Membuat ulang **satu kalimat saja**: jangan kirim kalimat itu sendirian. Dengan arahan gaya, arahannya ikut dibacakan; tanpa arahan, kalimat yang diawali kata Inggris ("Follow ...") dibaca berlogat Inggris. Kirim bersama kalimat sebelumnya sebagai konteks (dua paragraf + arahan), lalu potong di jeda terpanjang dan cek transkripnya.

**Penutup video:** setiap video diakhiri ajakan follow, di suara dan di layar ("Biar nggak gampang ketipu harga, follow Logika Duit!" plus tombol "Follow Logika Duit" yang ditekan). Tanpa username.
