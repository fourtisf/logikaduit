# Selaraskan voice over EP3 dengan video, lalu mixing akhir.
#   python3 video/ep03-mix.py prep <suara.zip> <folder>
#       -> <folder>/vo.wav (narasi di posisi akhir) dan <folder>/warp.json (tempo baru untuk video, musik, efek)
#   python3 video/ep03-mix.py final <video.mp4> <folder> <hasil.mp4>
#       -> gabung video + music.wav + sfx.wav + vo.wav dari <folder>; musik otomatis mengecil saat ada suara,
#          lalu loudness -14 LUFS (standar TikTok/Reels). Video dikompres ke ukuran kecil yang tetap HD (CRF 23).
# Zip berasal dari ep03-tts-gemini.py (01.wav ... 15.wav + lines.json).
import io, json, os, subprocess, sys, tempfile, wave, zipfile
import numpy as np

SR = 48000
# awal tiap teks di layar pada timeline asli HTML (urutan sama dengan kalimat narasi)
CAP = [0, 2.2, 4.8, 6.6, 8.15, 10.6, 13.5, 16.5, 19.0, 21.5, 24.5, 27.5, 31.0, 34.0, 38.0]
END = 42.0
STAMP = 18.6          # cap "Gratis" di timeline asli
LEAD = 0.12           # teks muncul sedikit sebelum suara
GAP = 0.22            # jeda normal antar kalimat
PAUSE = {5: 0.6, 7: 0.6}   # jeda lebih panjang: setelah "Kamu pilih yang mana?" dan sebelum "Yang biasa jadi gratis"
MIN_SCALE = 0.7       # adegan paling cepat 70% dari durasi aslinya


def load_line(raw):
    """WAV dari zip -> mono float 48 kHz (resample lewat ffmpeg), tanpa hening di awal/akhir."""
    with tempfile.NamedTemporaryFile(suffix='.wav') as src:
        src.write(raw); src.flush()
        pcm = subprocess.run(['ffmpeg', '-v', 'error', '-i', src.name, '-ac', '1', '-ar', str(SR), '-f', 's16le', '-'],
                             check=True, capture_output=True).stdout
    x = np.frombuffer(pcm, '<i2').astype(float) / 32768
    env = np.convolve(np.abs(x), np.ones(480) / 480, mode='same')
    on = np.where(env > env.max() * 10 ** (-38 / 20))[0]
    pad = int(.04 * SR)
    x = x[max(0, on[0] - pad):on[-1] + pad] if len(on) else x
    # buang dengung rendah, samakan kekerasan suara antar kalimat
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR)
    x = np.fft.irfft(X / (1 + (70 / np.maximum(f, 1)) ** 4), len(x))
    voiced = x[env[:len(x)] > env.max() * 0.1] if len(x) else x
    rms = np.sqrt((voiced ** 2).mean()) if len(voiced) else 1
    x = x * (10 ** (-20 / 20) / max(rms, 1e-6))
    return np.tanh(x * 1.1) / 1.1 if np.abs(x).max() > .95 else x


def prep(zpath, outdir):
    os.makedirs(outdir, exist_ok=True)
    z = zipfile.ZipFile(zpath)
    meta = json.loads(z.read('lines.json'))
    lines = [load_line(z.read(l['file'])) for l in meta['lines']]
    assert len(lines) == len(CAP), f'zip berisi {len(lines)} kalimat, seharusnya {len(CAP)}'
    d = [len(x) / SR for x in lines]
    L = [(CAP[i + 1] if i + 1 < len(CAP) else END) - CAP[i] for i in range(len(CAP))]
    v, n = [0.08], [0.0]
    for i in range(1, len(CAP)):
        vi = v[-1] + d[i - 1] + PAUSE.get(i - 1, GAP)
        vi = max(vi, n[-1] + MIN_SCALE * L[i - 1] + LEAD)
        v.append(vi); n.append(vi - LEAD)
    end = max(n[-1] + 0.85 * L[-1], v[-1] + d[-1] + 1.3)
    stamp_new = v[7] + d[7] + 0.08                 # cap jatuh tepat setelah "diturunkan satu sen"
    anchors = sorted([[CAP[i], round(n[i], 3)] for i in range(len(CAP))] + [[STAMP, round(stamp_new, 3)], [END, round(end, 3)]])
    news = [a[1] for a in anchors]
    assert all(b > a for a, b in zip(news, news[1:])), 'urutan waktu baru tidak naik'
    json.dump({'duration': round(end, 3), 'anchors': anchors, 'voice': meta.get('voice'), 'model': meta.get('model')},
              open(os.path.join(outdir, 'warp.json'), 'w'), indent=1)
    vo = np.zeros(int(end * SR) + SR)
    for x, t in zip(lines, v):
        i = int(t * SR); vo[i:i + len(x)] += x[:len(vo) - i]
    vo = vo[:int(end * SR)]
    with wave.open(os.path.join(outdir, 'vo.wav'), 'wb') as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((np.clip(vo, -1, 1) * 32767).astype('<i2').tobytes())
    print(f"suara: {meta.get('voice')} ({meta.get('model')}), durasi video baru {end:.1f} detik (asli {END:.0f})")
    for i, l in enumerate(meta['lines']):
        print(f"{i + 1:2d}  suara {v[i]:5.2f}-{v[i] + d[i]:5.2f}  teks {n[i]:5.2f} (asli {CAP[i]:5.2f}, x{((n[i + 1] if i + 1 < len(n) else end) - n[i]) / L[i]:.2f})  {l['text']}")


def loudness_json(args, filt):
    r = subprocess.run(['ffmpeg', '-hide_banner', '-nostats'] + args + ['-filter_complex', filt + ',loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json', '-f', 'null', '-'],
                       capture_output=True, text=True)
    txt = r.stderr
    return json.loads(txt[txt.rindex('{'):txt.rindex('}') + 1])


def mix_filter(k):
    """Filter mixing; k = nomor input pertama (music, lalu sfx, lalu vo).
    Musik mengecil otomatis saat narasi terdengar (sidechain), efek suara di tengah, narasi paling depan."""
    return (f'[{k + 2}:a]aformat=channel_layouts=stereo,asplit=2[vo][key];'
            f'[{k}:a]volume=0.34[mu];[mu][key]sidechaincompress=threshold=0.02:ratio=6:attack=20:release=420:makeup=1[duck];'
            f'[{k + 1}:a]volume=0.62[fx];'
            '[duck][fx][vo]amix=inputs=3:normalize=0:duration=longest')


def video_codec():
    """Video final dikompres ulang supaya kecil tapi tetap HD: x264 CRF 23 (sekitar 10 MB untuk 50 detik).
    Gradasi gelap tetap mulus berkat aq-mode 3. LD_VIDEO_CRF=copy untuk menyimpan master tanpa kompres ulang."""
    crf = os.environ.get('LD_VIDEO_CRF', '23')
    if crf == 'copy':
        return ['-c:v', 'copy']
    return ['-c:v', 'libx264', '-preset', 'slow', '-crf', crf, '-tune', 'film', '-x264-params', 'aq-mode=3',
            '-profile:v', 'high', '-pix_fmt', 'yuv420p']


def final(video, folder, out):
    ins = ['-i', os.path.join(folder, 'music.wav'), '-i', os.path.join(folder, 'sfx.wav'), '-i', os.path.join(folder, 'vo.wav')]
    m = loudness_json(ins, mix_filter(0))
    ln = (f"loudnorm=I=-14:TP=-1.5:LRA=11:measured_I={m['input_i']}:measured_TP={m['input_tp']}:"
          f"measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true")
    # limiter setelah loudnorm: mode linear bisa menaikkan puncak di atas 0 dBFS (suara pecah).
    # lowpass 16 kHz + batas -3 dB supaya klik tajam tidak melonjak lagi saat dikompres ke AAC
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', video] + ins + ['-filter_complex', mix_filter(1) + ',' + ln + ',aresample=48000,lowpass=f=16000,alimiter=limit=0.7:attack=2:release=60:level=false[a]',
                    '-map', '0:v', '-map', '[a]'] + video_codec() + ['-c:a', 'aac', '-b:a', '128k', '-movflags', '+faststart', '-shortest', out],
                   check=True)
    print('selesai:', out)


if __name__ == '__main__':
    cmd = sys.argv[1] if len(sys.argv) > 1 else ''
    if cmd == 'prep' and len(sys.argv) == 4:
        prep(sys.argv[2], sys.argv[3])
    elif cmd == 'final' and len(sys.argv) == 5:
        final(sys.argv[2], sys.argv[3], sys.argv[4])
    else:
        sys.exit('pakai: ep03-mix.py prep <zip> <folder> | final <video.mp4> <folder> <hasil.mp4>')
