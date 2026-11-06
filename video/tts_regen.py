#!/usr/bin/env python3
# Buat ulang SATU kalimat narasi tanpa mengulang seluruh naskah, lalu ganti potongannya di zip suara.
#   python3 video/tts_regen.py <suara.zip> <hasil.zip> <nomor kalimat, mulai 1> "<teks baru>"
# Cara kerja (lihat catatan Gemini TTS di CLAUDE.md bagian 14):
#  - kalimat dikirim bersama kalimat sebelumnya sebagai konteks (arahan gaya + dua paragraf), karena kalimat yang
#    dikirim sendirian membuat arahan ikut dibacakan atau logatnya jadi Inggris;
#  - model kadang menambah kalimat sendiri di akhir ("Terima kasih ya, ..."): kata-kata setelah kata terakhir naskah
#    dikenali dari transkrip lalu dibuang;
#  - ekor pendek setelah jeda panjang (napas atau "hah") dibuang;
#  - hasilnya dicek dengan transkrip. Kalau "TIDAK COCOK", dengarkan dulu sebelum dipakai.
# Untuk kalimat pertama (nomor 1), konteksnya kalimat kedua dan potongan yang diambil bagian pertama.
import io, json, sys, wave, zipfile
import numpy as np
import tts_gemini as T


def trim_tail(part, rate):
    """Buang ekor pendek (< 0,8 dtk) yang muncul setelah jeda lebih dari 0,8 dtk."""
    x = np.frombuffer(part, '<i2').astype(float)
    hop = rate // 100
    env = np.array([np.sqrt((x[i:i + hop] ** 2).mean()) for i in range(0, len(x) - hop, hop)])
    loud = env > env.max() * 10 ** (-36 / 20)
    segs, s0 = [], None
    for i, v in enumerate(loud):
        if v and s0 is None:
            s0 = i
        if not v and s0 is not None:
            segs.append((s0, i)); s0 = None
    if s0 is not None:
        segs.append((s0, len(loud)))
    if len(segs) > 1 and segs[-1][0] - segs[-2][1] > 80 and segs[-1][1] - segs[-1][0] < 80:
        print('ekor setelah jeda panjang dibuang')
        return part[:int((segs[-2][1] + 25) / 100 * rate) * 2]
    return part


def main():
    src, dst, n, new = sys.argv[1], sys.argv[2], int(sys.argv[3]), sys.argv[4]
    key, _ = T.find_config()
    if not key:
        sys.exit("BERHENTI: GEMINI_API_KEY tidak ditemukan.")
    z = zipfile.ZipFile(src)
    meta = json.loads(z.read('lines.json'))
    lines = [l['text'] for l in meta['lines']]
    lines[n - 1] = new
    rate = wave.open(io.BytesIO(z.read(meta['lines'][0]['file']))).getframerate()
    pair, pick = ([lines[n - 2], new], 1) if n > 1 else ([new, lines[1]], 0)
    pcm, r2 = T.tts(key, meta.get('model') or T.MODELS[0], meta.get('voice') or T.VOICE, T.DIRECTION + "\n\n" + "\n\n".join(pair))
    assert r2 == rate, f'sample rate berbeda: {r2} vs {rate}'
    model = T.text_model(key)
    heard_all = T.transcribe(key, model, pcm, rate) or ''
    hw, last = T.words(heard_all), T.words(pair[-1])[-1]
    idx = max((i for i, w in enumerate(hw) if w == last), default=None)
    tail = hw[idx + 1:] if idx is not None else []
    if len(tail) >= 3:
        print('kalimat tambahan dari model dibuang:', ' '.join(tail))
        pair = pair + [' '.join(tail)]
    part = trim_tail(T.split_lines(pcm, rate, pair)[pick], rate)
    heard = T.transcribe(key, model, part, rate)
    print(f"{n} {'cocok' if heard and T.match(new, heard) else 'TIDAK COCOK'}, terdengar: {heard}")
    with zipfile.ZipFile(dst, 'w', zipfile.ZIP_DEFLATED) as o:
        for name in z.namelist():
            if name == meta['lines'][n - 1]['file']:
                o.writestr(name, T.wav_bytes(part, rate))
            elif name == 'lines.json':
                meta['lines'][n - 1].update(text=new, seconds=round(len(part) / 2 / rate, 2))
                meta['transkrip'] = meta.get('transkrip', []) + [f'(kalimat {n} dibuat ulang dengan tts_regen.py: {heard})']
                o.writestr(name, json.dumps(meta, ensure_ascii=False, indent=1))
            else:
                o.writestr(name, z.read(name))
    print('selesai:', dst)


if __name__ == '__main__':
    main()
