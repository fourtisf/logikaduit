#!/usr/bin/env python3
# Buat suara narasi (voice over) EP3 dengan Gemini TTS, satu file WAV per kalimat.
# Cara utama: dijalankan langsung di sesi Claude Code, dengan GEMINI_API_KEY disimpan di pengaturan environment
# (bukan di chat, bukan di repo). Cadangan: dijalankan di VPS ALFA yang punya key di .env.
# Key TIDAK pernah dicetak atau dikirim ke mana pun selain ke API Google. Urutan pencarian key:
#   1. variabel lingkungan GEMINI_API_KEY (dan GEMINI_TTS_MODEL kalau ada)
#   2. /var/www/ruangpikir/.env
#   3. ~/.config/ruangpikir/gemini.env
# Pakai:
#   python3 /opt/logikaduit/video/ep03-tts-gemini.py              # suara default: Puck
#   python3 /opt/logikaduit/video/ep03-tts-gemini.py --voice Leda # suara lain
# Hasil: /root/logikaduit-ep03-suara.zip (WAV per kalimat + lines.json). Hanya pakai library bawaan Python.
import base64, io, json, os, re, sys, time, urllib.error, urllib.request, wave, zipfile

LINES = [
    "Pernah nambah barang biar dapat gratis ongkir?",
    "Hemat ongkir sepuluh ribu, tapi nambah belanja dua puluh delapan ribu.",
    "Totalnya malah delapan belas ribu lebih mahal.",
    "Kok kita tetap merasa menang?",
    "Ada eksperimennya. Peneliti menjual dua coklat.",
    "Yang premium lima belas sen, yang biasa satu sen. Kamu pilih yang mana?",
    "Tujuh puluh tiga persen pilih yang premium. Masuk akal.",
    "Lalu dua-duanya diturunkan satu sen.",
    "Yang biasa jadi... gratis.",
    "Hasilnya berbalik: enam puluh sembilan persen pilih yang gratis.",
    "Padahal selisih harganya tetap empat belas sen.",
    "Kata gratis bikin otak berhenti menghitung. Namanya efek harga nol.",
    "Promo gratis ongkir pakai trik yang sama.",
    "Sebelum nambah barang, tanya dulu: kalau ongkirnya bayar, barang ini tetap kamu beli?",
    "Biar nggak gampang ketipu harga. Logika Duit.",
]
STYLE = ("Bacakan dalam bahasa Indonesia dengan gaya kreator konten edukasi di TikTok: santai, hangat, "
         "percaya diri, sedikit antusias, tempo agak cepat, seperti ngobrol sama teman. "
         "Ucapkan hanya kalimat berikut, tanpa tambahan apa pun:\n")
DEFAULT_MODEL = "gemini-3.8-flash-tts"   # model yang sudah dipakai ALFA di Ruang Pikir
BASE = os.environ.get("GEMINI_BASE", "https://generativelanguage.googleapis.com")
OUT = os.environ.get("LD_TTS_OUT", "/root/logikaduit-ep03-suara.zip")


def read_env_file(path):
    vals = {}
    try:
        with open(os.path.expanduser(path)) as f:
            for line in f:
                m = re.match(r'\s*(?:export\s+)?([A-Z0-9_]+)\s*=\s*(.*)\s*$', line)
                if m:
                    vals[m.group(1)] = m.group(2).strip().strip('"').strip("'")
    except OSError:
        pass
    return vals


def find_config():
    key, model = os.environ.get("GEMINI_API_KEY"), os.environ.get("GEMINI_TTS_MODEL")
    for path in ("/var/www/ruangpikir/.env", "~/.config/ruangpikir/gemini.env"):
        if key:
            break
        vals = read_env_file(path)
        key = vals.get("GEMINI_API_KEY")
        model = model or vals.get("GEMINI_TTS_MODEL")
        if key:
            print(f"API key ditemukan di {path} (tidak ditampilkan).")
    return key, model or DEFAULT_MODEL


def tts(key, model, voice, text):
    body = {
        "contents": [{"parts": [{"text": STYLE + text}]}],
        "generationConfig": {"responseModalities": ["AUDIO"],
                             "speechConfig": {"voiceConfig": {"prebuiltVoiceConfig": {"voiceName": voice}}}},
    }
    req = urllib.request.Request(f"{BASE}/v1beta/models/{model}:generateContent", data=json.dumps(body).encode(),
                                 headers={"Content-Type": "application/json", "x-goog-api-key": key}, method="POST")
    for attempt in range(1, 7):
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                data = json.load(r)
            part = data["candidates"][0]["content"]["parts"][0]["inlineData"]
            rate = int((re.search(r"rate=(\d+)", part.get("mimeType", "")) or [0, 24000])[1])
            return base64.b64decode(part["data"]), rate
        except urllib.error.HTTPError as e:
            msg = e.read().decode(errors="replace")[:400]
            if e.code in (429, 500, 502, 503, 504) and attempt < 6:
                wait = int(e.headers.get("Retry-After") or 0) or 15 * attempt
                print(f"   server sibuk ({e.code}), coba lagi dalam {wait} detik...")
                time.sleep(wait)
                continue
            sys.exit(f"GAGAL dari Gemini ({e.code}): {msg}")
        except (KeyError, IndexError, ValueError) as e:
            if attempt < 6:
                print(f"   jawaban tanpa audio, coba lagi ({attempt})...")
                time.sleep(5)
                continue
            sys.exit(f"GAGAL: jawaban Gemini tidak berisi audio ({e}).")
        except urllib.error.URLError as e:
            if attempt < 6:
                time.sleep(5 * attempt)
                continue
            sys.exit(f"GAGAL tersambung ke Gemini: {e}")


def main():
    voice = sys.argv[sys.argv.index("--voice") + 1] if "--voice" in sys.argv else "Puck"
    key, model = find_config()
    if not key:
        sys.exit("BERHENTI: API key Gemini tidak ditemukan (GEMINI_API_KEY di /var/www/ruangpikir/.env).")
    print(f"Model: {model}, suara: {voice}, {len(LINES)} kalimat")
    meta = {"model": model, "voice": voice, "lines": []}
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as z:
        for i, text in enumerate(LINES, 1):
            pcm, rate = tts(key, model, voice, text)
            wav = io.BytesIO()
            with wave.open(wav, "wb") as w:
                w.setnchannels(1); w.setsampwidth(2); w.setframerate(rate); w.writeframes(pcm)
            name = f"{i:02d}.wav"
            z.writestr(name, wav.getvalue())
            dur = len(pcm) / 2 / rate
            meta["lines"].append({"file": name, "text": text, "seconds": round(dur, 2)})
            print(f"{i:2d}/{len(LINES)}  {dur:4.1f} dtk  {text}")
            time.sleep(1)
        z.writestr("lines.json", json.dumps(meta, ensure_ascii=False, indent=1))
    with open(OUT, "wb") as f:
        f.write(buf.getvalue())
    total = sum(l["seconds"] for l in meta["lines"])
    print(f"\nSelesai: {OUT} (total suara {total:.1f} detik). Download file ini lewat SFTP, lalu upload ke chat Claude.")


if __name__ == "__main__":
    main()
