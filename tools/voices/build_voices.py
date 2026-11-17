"""Build sample voices for audition.html (run in GitHub Actions; needs internet).

Outputs into OUT dir (default _site/voices):
  piper_<vowel>.wav  Piper TTS (en_US-ljspeech, public-domain dataset) saying la/lay/lee/low/loo
  choir_aahs.js / voice_oohs.js  real recorded voice samples from FluidR3_GM soundfont
  meta.json  estimated pitch (Hz) of each Piper clip, so the page can retune it
"""
import json, subprocess, sys, urllib.request, wave, pathlib
import numpy as np

OUT = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "_site/voices")
OUT.mkdir(parents=True, exist_ok=True)
HF = "https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/ljspeech/medium/"
SF = "https://gleitz.github.io/midi-js-soundfonts/FluidR3_GM/"

def get(url, dest):
    print("download", url)
    urllib.request.urlretrieve(url, dest)

model = OUT.parent.parent / "piper_model.onnx"
get(HF + "en_US-ljspeech-medium.onnx", model)
get(HF + "en_US-ljspeech-medium.onnx.json", str(model) + ".json")
try:
    get(HF + "MODEL_CARD", OUT / "PIPER_MODEL_CARD.txt")
except Exception as e:
    print("model card not found", e)

def load(path):
    with wave.open(str(path)) as w:
        sr = w.getframerate()
        x = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768
    return x, sr

def save(path, x, sr):
    y = (np.clip(x, -1, 1) * 32767).astype(np.int16)
    with wave.open(str(path), "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr); w.writeframes(y.tobytes())

def f0(x, sr):
    # autocorrelation pitch over the loudest 100 ms, range 70-400 Hz
    n = int(sr * .1)
    e = np.convolve(x * x, np.ones(n), "valid")
    s = int(np.argmax(e)); seg = x[s:s + n] - x[s:s + n].mean()
    ac = np.correlate(seg, seg, "full")[n - 1:]
    lo, hi = int(sr / 400), int(sr / 70)
    return sr / (lo + int(np.argmax(ac[lo:hi])))

meta = {}
for vow, word in {"a": "la", "e": "lay", "i": "lee", "o": "low", "u": "loo"}.items():
    raw = OUT / f"raw_{vow}.wav"
    subprocess.run([sys.executable, "-m", "piper", "-m", str(model), "-f", str(raw), "--length-scale", "1.6"],
                   input=word + ".", text=True, check=True)
    x, sr = load(raw); raw.unlink()
    th = .02 * np.abs(x).max(); idx = np.where(np.abs(x) > th)[0]
    x = x[max(0, idx[0] - int(sr * .005)): idx[-1] + int(sr * .02)]
    x = x / np.abs(x).max() * .9
    save(OUT / f"piper_{vow}.wav", x, sr)
    meta[vow] = round(float(f0(x, sr)), 1)
    print(word, len(x) / sr, "s", meta[vow], "Hz")
(OUT / "meta.json").write_text(json.dumps(meta))

for name in ["choir_aahs", "voice_oohs"]:
    get(SF + f"{name}-mp3.js", OUT / f"{name}.js")
try:
    get("https://raw.githubusercontent.com/gleitz/midi-js-soundfonts/gh-pages/README.md", OUT / "SOUNDFONT_README.txt")
    print(open(OUT / "SOUNDFONT_README.txt", encoding="utf-8").read()[:3000])
except Exception as e:
    print("soundfont readme not found", e)
