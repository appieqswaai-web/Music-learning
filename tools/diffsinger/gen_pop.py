"""Sing every 流行樂 (pages/pop.html) pattern with DiffSinger (Opencpop, Mandarin) at 70/90/120 BPM.
Patterns come from tools/diffsinger/pop_patterns.json (exported from pop.html). Run inside the DiffSinger repo:
  PYTHONPATH=. python ../tools/diffsinger/gen_pop.py ../tools/diffsinger/pop_patterns.json <out_dir>
Writes <out_dir>/p<i>_<bpm>.wav and index.json ({"bpms":[...], "files":{"<i>_<bpm>":"p<i>_<bpm>.mp3"}})."""
import sys, os, json, glob
from pypinyin import lazy_pinyin
PAT, OUT = sys.argv[1], os.path.abspath(sys.argv[2])
os.makedirs(OUT, exist_ok=True)
BPMS = [70, 90, 120]

# pinyin -> Opencpop phonemes, from the dictionary shipped in the DiffSinger repo
dic = {}
cands = glob.glob("inference/svs/opencpop/*pinyin2ph*.txt") + glob.glob("**/*pinyin2ph*.txt", recursive=True)
if not cands: raise SystemExit("pinyin2ph dictionary not found")
for line in open(cands[0], encoding="utf-8"):
    parts = line.strip().split("|") if "|" in line else line.split()
    if len(parts) >= 2: dic[parts[0].strip()] = parts[1].strip().split()
print("dictionary", cands[0], len(dic))

def phones(ch):
    py = lazy_pinyin(ch)[0].replace("ü", "v")
    if py in dic: return dic[py]
    raise ValueError(f"no phonemes for {ch} ({py})")

def name(m):
    n = ["C", "C#4/Db4", "D", "D#4/Eb4", "E", "F", "F#4/Gb4", "G", "G#4/Ab4", "A", "A#4/Bb4", "B"][m % 12]
    o = m // 12 - 1
    return n.replace("4", str(o)) if "/" in n else n + str(o)
SCALE = [0, 2, 4, 5, 7, 9, 11]
def deg2midi(d): return 64 + (d // 7) * 12 + SCALE[d % 7]

from inference.svs.ds_e2e import DiffSingerE2EInfer
from utils.hparams import set_hparams, hparams
from utils.audio import save_wav
set_hparams(config="usr/configs/midi/e2e/opencpop/ds100_adj_rel.yaml", exp_name="0228_opencpop_ds100_rel", print_hparams=False)
infer = DiffSingerE2EInfer(hparams)

files = {}
for i, p in enumerate(json.load(open(PAT, encoding="utf-8"))):
    chars = list(p["ly"]); v = p["v"].replace("|", ""); mel = p.get("mel") or [0]
    notes = []; k = 0
    while k < len(v):
        if v[k] == "x":
            j = k + 1
            while j < len(v) and v[j] == "-": j += 1
            notes.append((k, j - k)); k = j
        else: k += 1
    assert len(notes) == len(chars), (p["t"], len(notes), len(chars))
    for bpm in BPMS:
        sd = 60 / bpm / p["sub"]
        ph, ns, ds, sl = [], [], [], []
        def add(phs, note, dur):
            for x in phs: ph.append(x); ns.append(note); ds.append(f"{dur:.4f}"); sl.append("0")
        t = 0
        for n, (st, ln) in enumerate(notes):
            if st > t: add(["SP"], "rest", (st - t) * sd)
            add(phones(chars[n]), name(deg2midi(mel[n % len(mel)])), ln * sd)
            t = st + ln
        if t < len(v): add(["SP"], "rest", (len(v) - t) * sd)
        inp = {"text": p["ly"], "ph_seq": " ".join(ph), "note_seq": " ".join(ns),
               "note_dur_seq": " ".join(ds), "is_slur_seq": " ".join(sl), "input_type": "phoneme"}
        print(i, bpm, p["t"], inp["ph_seq"])
        wav = infer.infer_once(inp)
        f = f"p{i}_{bpm}.wav"; save_wav(wav, os.path.join(OUT, f), hparams["audio_sample_rate"])
        print("  ->", round(len(wav) / hparams["audio_sample_rate"], 2), "s, expected", round(len(v) * sd, 2))
        files[f"{i}_{bpm}"] = f.replace(".wav", ".mp3")
json.dump({"bpms": BPMS, "files": files}, open(os.path.join(OUT, "index.json"), "w"))
