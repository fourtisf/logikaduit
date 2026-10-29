# Narasi (voice over) video Logika Duit dengan Gemini TTS. Dipakai oleh ep03-tts-gemini.py, ep04-tts-gemini.py, dst.;
# file episode hanya berisi daftar kalimatnya.
# Seluruh naskah dibacakan dalam SATU permintaan (hemat kuota: akun gratis hanya dapat beberapa permintaan
# TTS per hari per model), lalu dipotong otomatis per kalimat berdasarkan jeda bicara dan dicek dengan transkrip.
# Key TIDAK pernah dicetak atau dikirim ke mana pun selain ke API Google. Urutan pencarian key:
#   1. variabel lingkungan GEMINI_API_KEY (dan GEMINI_TTS_MODEL kalau ada)
#   2. /var/www/ruangpikir/.env
#   3. ~/.config/ruangpikir/gemini.env
# Hanya pakai library bawaan Python.
import array, base64, io, json, math, os, re, sys, time, urllib.error, urllib.request, wave, zipfile

# arahan gaya dibuat singkat dan dalam bahasa Inggris supaya tidak ikut dibacakan
DIRECTION = "Say in a warm, upbeat, casual Indonesian content-creator voice, slightly fast, with a clear pause between paragraphs:"
MODELS = ["gemini-3.8-flash-tts", "gemini-3.8-flash-lite-tts", "gemini-3.1-flash-tts-preview",
          "gemini-2.5-flash-preview-tts", "gemini-2.5-pro-preview-tts"]
BASE = os.environ.get("GEMINI_BASE", "https://generativelanguage.googleapis.com")


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
    return key, model


class QuotaHabis(Exception):
    pass


def tts(key, model, voice, text):
    body = {
        "contents": [{"parts": [{"text": text}]}],
        "generationConfig": {"responseModalities": ["AUDIO"],
                             "speechConfig": {"voiceConfig": {"prebuiltVoiceConfig": {"voiceName": voice}}}},
    }
    req = urllib.request.Request(f"{BASE}/v1beta/models/{model}:generateContent", data=json.dumps(body).encode(),
                                 headers={"Content-Type": "application/json", "x-goog-api-key": key}, method="POST")
    for attempt in range(1, 5):
        try:
            with urllib.request.urlopen(req, timeout=300) as r:
                data = json.load(r)
            part = data["candidates"][0]["content"]["parts"][0]["inlineData"]
            rate = int((re.search(r"rate=(\d+)", part.get("mimeType", "")) or [0, 24000])[1])
            return base64.b64decode(part["data"]), rate
        except urllib.error.HTTPError as e:
            msg = e.read().decode(errors="replace")
            if e.code == 429 and ("PerDay" in msg or "per day" in msg.lower() or attempt >= 3):
                raise QuotaHabis(model)
            if e.code == 404:
                raise QuotaHabis(model)        # model tidak tersedia untuk akun ini: coba model lain
            if e.code in (429, 500, 502, 503, 504) and attempt < 4:
                wait = int(e.headers.get("Retry-After") or 0) or 20 * attempt
                print(f"   server sibuk ({e.code}), coba lagi dalam {wait} detik...")
                time.sleep(wait)
                continue
            sys.exit(f"GAGAL dari Gemini ({e.code}): {msg[:400]}")
        except (KeyError, IndexError, ValueError) as e:
            if attempt < 4:
                print(f"   jawaban tanpa audio, coba lagi ({attempt})...")
                time.sleep(5)
                continue
            sys.exit(f"GAGAL: jawaban Gemini tidak berisi audio ({e}).")
        except urllib.error.URLError as e:
            if attempt < 4:
                time.sleep(5 * attempt)
                continue
            sys.exit(f"GAGAL tersambung ke Gemini: {e}")
    raise QuotaHabis(model)


def syllables(text):
    return max(1, len(re.findall(r"[aiueo]+", text.lower())))


def split_lines(pcm, rate, lines):
    """Potong audio satu-naskah menjadi n kalimat: pilih jeda (hening) yang paling cocok dengan panjang kalimat."""
    x = array.array("h"); x.frombytes(pcm)
    hop = rate // 100                                  # bingkai 10 ms
    env = [math.sqrt(sum(v * v for v in x[i:i + hop]) / hop) for i in range(0, len(x) - hop, hop)]
    peak = max(env) or 1
    loud = [e > peak * 10 ** (-36 / 20) for e in env]
    on = [i for i, v in enumerate(loud) if v]
    first, last = on[0], on[-1]
    gaps, i = [], first                                # kandidat potongan: jeda >= 180 ms (bukan jeda di dalam konsonan)
    while i <= last:
        if not loud[i]:
            j = i
            while j <= last and not loud[j]:
                j += 1
            if j - i >= 18:
                gaps.append(((i + j) / 2, (j - i) / 100))
            i = j
        else:
            i += 1
    n_lines = len(lines)
    exp = [syllables(t) for t in lines]
    total = (last - first)
    exp = [e / sum(exp) * total for e in exp]          # perkiraan panjang tiap kalimat (bingkai)
    k = n_lines - 1
    if len(gaps) < k:
        raise ValueError(f"hanya {len(gaps)} jeda terdeteksi, butuh {k}")
    pos = [first] + [g[0] for g in gaps] + [last]
    gl = [0] + [g[1] for g in gaps] + [0]
    C = len(pos)
    NEG = -1e18
    best = [[NEG] * C for _ in range(k + 2)]
    back = [[-1] * C for _ in range(k + 2)]
    best[0][0] = 0
    for s in range(1, k + 2):                          # s = jumlah segmen sampai titik c
        for c in range(1, C):
            if s <= k and c == C - 1:
                continue
            if s == k + 1 and c != C - 1:
                continue
            for p in range(c):
                if best[s - 1][p] == NEG:
                    continue
                L = pos[c] - pos[p]
                err = ((L - exp[s - 1]) / exp[s - 1]) ** 2
                bonus = math.log(max(gl[c], .05) / .1) if c != C - 1 else 0
                v = best[s - 1][p] - 3 * err + bonus
                if v > best[s][c]:
                    best[s][c], back[s][c] = v, p
    cuts, c = [], C - 1
    for s in range(k + 1, 0, -1):
        cuts.append(c); c = back[s][c]
    cuts = sorted(cuts)[:-1]
    bounds = [0] + [int(pos[c] * hop) for c in cuts] + [len(x)]
    return [x[bounds[i]:bounds[i + 1]].tobytes() for i in range(n_lines)]


def pauses(pcm, rate, min_s=0.18):
    """Jeda (mulai, selesai) dalam detik di satu potongan."""
    x = array.array("h"); x.frombytes(pcm)
    hop = rate // 100
    env = [math.sqrt(sum(v * v for v in x[i:i + hop]) / hop) for i in range(0, len(x) - hop, hop)]
    peak = max(env) or 1
    loud = [e > peak * 10 ** (-36 / 20) for e in env]
    out, i = [], 0
    while i < len(loud):
        if not loud[i]:
            j = i
            while j < len(loud) and not loud[j]:
                j += 1
            if (j - i) / 100 >= min_s:
                out.append((i / 100, j / 100))
            i = j
        else:
            i += 1
    return out


def words(t):
    return re.findall(r"[a-z]+", t.lower().replace("nggak", "enggak"))


def transcribe(key, model, pcm, rate):
    body = {"contents": [{"parts": [
        {"text": "Transkripsikan audio ini kata demi kata persis seperti yang diucapkan. Jawab hanya teks transkripnya."},
        {"inlineData": {"mimeType": "audio/wav", "data": base64.b64encode(wav_bytes(pcm, rate)).decode()}}]}],
        "generationConfig": {"temperature": 0}}
    req = urllib.request.Request(f"{BASE}/v1beta/models/{model}:generateContent", data=json.dumps(body).encode(),
                                 headers={"Content-Type": "application/json", "x-goog-api-key": key}, method="POST")
    for attempt in range(4):
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                return json.load(r)["candidates"][0]["content"]["parts"][0]["text"].strip()
        except urllib.error.HTTPError as e:
            if e.code == 429:
                time.sleep(15 * (attempt + 1)); continue
            return None
        except Exception:
            time.sleep(3)
    return None


def text_model(key):
    """Model teks ringan untuk transkrip (kuota terpisah dari model suara)."""
    try:
        req = urllib.request.Request(f"{BASE}/v1beta/models?pageSize=200", headers={"x-goog-api-key": key})
        names = [m["name"].split("/")[1] for m in json.load(urllib.request.urlopen(req, timeout=30))["models"]
                 if "generateContent" in m.get("supportedGenerationMethods", [])]
    except Exception:
        return None
    lite = [n for n in names if re.fullmatch(r"gemini-[\d.]+-flash-lite", n)]
    return sorted(lite, key=lambda n: [int(v) for v in re.findall(r"\d+", n)])[-1] if lite else None


def verify_and_fix(key, parts, rate, lines):
    """Transkrip tiap potongan. Kalau kata-kata terakhir sebuah kalimat terbawa ke potongan berikutnya (atau
    sebaliknya), pindahkan batasnya ke jeda terpanjang di dekatnya, lalu cek ulang. Mengembalikan (parts, laporan)."""
    model = text_model(key)
    if not model:
        return parts, ["(transkrip dilewati: tidak ada model teks)"]
    tr = [transcribe(key, model, p, rate) for p in parts]
    tr = [t if t is not None else transcribe(key, model, p, rate) for t, p in zip(tr, parts)]   # sekali lagi kalau gagal
    fixed = set()
    for i in range(len(parts) - 1):
        a, b = tr[i], tr[i + 1]
        if a is None or b is None:
            continue
        li, ln = words(lines[i]), words(lines[i + 1])
        wa, wb = words(a), words(b)
        # berapa kata (maksimal 3) yang terbawa: ekor kalimat i di awal potongan i+1, atau awal kalimat i+1 di akhir potongan i.
        # Kalau lebih dari satu kata, jeda koma ikut terbawa, jadi batas baru = jeda terpanjang (akhir kalimat).
        tail = max((k for k in range(1, 4) if wb[:k] == li[-k:] and wb[:k] != ln[:k]), default=0)
        head = max((k for k in range(1, 4) if wa[-k:] == ln[:k] and wa[-k:] != li[-k:]), default=0)
        longest = lambda gs: max(gs, key=lambda g: g[1] - g[0])
        if tail:
            gaps = [g for g in pauses(parts[i + 1], rate) if g[0] > 0.05][:tail]
            if gaps:
                g = longest(gaps)
                k = int((g[0] + g[1]) / 2 * rate) * 2
                parts[i], parts[i + 1] = parts[i] + parts[i + 1][:k], parts[i + 1][k:]
                fixed.update((i, i + 1))
        elif head:
            gaps = [g for g in pauses(parts[i], rate) if g[1] < len(parts[i]) / 2 / rate - 0.05][-head:]
            if gaps:
                g = longest(gaps)
                k = int((g[0] + g[1]) / 2 * rate) * 2
                parts[i], parts[i + 1] = parts[i][:k], parts[i][k:] + parts[i + 1]
                fixed.update((i, i + 1))
    for i in sorted(fixed):
        tr[i] = transcribe(key, model, parts[i], rate)
    report = [f"{i + 1:2d} {'(diperbaiki) ' if i in fixed else ''}{'' if t is None or match(lines[i], t) else 'TIDAK COCOK, '}terdengar: {t}"
              for i, t in enumerate(tr)]
    return parts, report


NUMBER_WORDS = set("nol satu dua tiga empat lima enam tujuh delapan sembilan sepuluh sebelas belas puluh ratus seratus ribu seribu "
                   "juta koma persen".split())


def match(expected, heard):
    """True kalau sebagian besar kata naskah terdengar di potongan dan potongan tidak jauh lebih panjang (kalimat menyatu).
    Angka tidak dihitung, karena transkrip menulisnya dengan digit ("97,6%")."""
    e = [w for w in words(expected) if w not in NUMBER_WORDS]
    h = words(heard)
    return len(set(e) & set(h)) >= .6 * len(set(e)) and len(h) <= 1.6 * len(e) + 2


def split_checked(key, pcm, rate, lines):
    """Potong per kalimat. Model kadang ikut membacakan arahan gaya di awal (tidak menentu, arahan yang sama
    pernah aman); kalau transkrip awal audio berisi arahan itu, potong jadi satu bagian lebih lalu buang yang pertama."""
    model = text_model(key)
    head = pcm[:min(len(pcm), rate * 2 * 8)]           # 8 detik pertama
    heard = transcribe(key, model, head, rate) if model else None
    if heard and len(set(words(DIRECTION)) & set(words(heard))) >= 4:
        print("Arahan gaya ikut dibacakan di awal; bagian itu dibuang.")
        return split_lines(pcm, rate, [DIRECTION] + lines)[1:]
    return split_lines(pcm, rate, lines)


def wav_bytes(pcm, rate):
    b = io.BytesIO()
    with wave.open(b, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(rate); w.writeframes(pcm)
    return b.getvalue()


def main(lines, default_out):
    """Buat narasi untuk daftar kalimat `lines`; hasil zip ke LD_TTS_OUT atau default_out."""
    out = os.environ.get("LD_TTS_OUT", default_out)
    voice = sys.argv[sys.argv.index("--voice") + 1] if "--voice" in sys.argv else "Puck"
    key, model = find_config()
    if not key:
        sys.exit("BERHENTI: GEMINI_API_KEY tidak ditemukan (pengaturan environment atau /var/www/ruangpikir/.env).")
    models = ([model] if model else []) + [m for m in MODELS if m != model]
    script = DIRECTION + "\n\n" + "\n\n".join(lines)
    for m in models:
        print(f"Membuat narasi: model {m}, suara {voice}, {len(lines)} kalimat dalam satu permintaan...")
        try:
            pcm, rate = tts(key, m, voice, script)
            break
        except QuotaHabis:
            print(f"   kuota {m} habis atau tidak tersedia, pindah ke model berikutnya")
    else:
        sys.exit("GAGAL: kuota semua model TTS habis untuk hari ini. Coba lagi besok, atau aktifkan billing di Google AI Studio.")
    dur = len(pcm) / 2 / rate
    expected = sum(syllables(t) for t in lines) / 5.0
    print(f"Narasi {dur:.1f} detik (perkiraan {expected:.0f} detik)")
    if dur > expected * 1.8:
        print("PERINGATAN: narasi jauh lebih panjang dari naskah. Mungkin arahan gaya ikut dibacakan; cek full.wav.")
    parts = split_checked(key, pcm, rate, lines)
    print("Memeriksa tiap potongan dengan transkrip...")
    parts, report = verify_and_fix(key, parts, rate, lines)
    print("\n".join(report))
    if any("TIDAK COCOK" in r for r in report):
        print("PERINGATAN: ada potongan yang tidak cocok dengan naskah. Dengarkan full.wav dan potongannya sebelum dipakai.")
    meta = {"model": m, "voice": voice, "lines": [], "transkrip": report}
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("full.wav", wav_bytes(pcm, rate))
        for i, (text, p) in enumerate(zip(lines, parts), 1):
            name = f"{i:02d}.wav"
            z.writestr(name, wav_bytes(p, rate))
            meta["lines"].append({"file": name, "text": text, "seconds": round(len(p) / 2 / rate, 2)})
            print(f"{i:2d}/{len(lines)}  {len(p) / 2 / rate:4.1f} dtk  {text}")
        z.writestr("lines.json", json.dumps(meta, ensure_ascii=False, indent=1))
    print(f"\nSelesai: {out}")

