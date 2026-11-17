"""Sing every J-POP pattern with DiffSinger (Opencpop, Mandarin model) by mapping
Japanese kana to the closest Mandarin phonemes. Run inside the DiffSinger repo:
  PYTHONPATH=. python ../tools/diffsinger/gen_jpop.py <generator_dir> <out_dir>
Writes <out_dir>/p<i>.wav and index.json."""
import sys, os, json, re
GEN, OUT = os.path.abspath(sys.argv[1]), os.path.abspath(sys.argv[2])
os.makedirs(OUT, exist_ok=True)
here = os.getcwd(); sys.path.insert(0, GEN); os.chdir(GEN)
import common
cap = {}
common.build = lambda tpl, audio, cfg, out: cap.update(cfg)
exec(open("jpop.py", encoding="utf-8").read().replace("from common import *", "from common import *\nbuild=common.build"), {"__name__": "jpop", "common": common})
os.chdir(here)

INIT = {"k": "k", "g": "g", "s": "s", "sh": "x", "z": "z", "j": "j", "t": "t", "ch": "q", "ts": "c", "d": "d",
        "n": "n", "h": "h", "f": "f", "b": "b", "p": "p", "m": "m", "y": "y", "r": "l", "w": "w"}
VOW = {"a": "a", "i": "i", "u": "u", "e": "ei", "o": "o"}
PAL = {"a": "ia", "u": "iu", "o": "iao", "e": "ie", "i": "i"}

def phones(rm):
    """romaji of one note (from common.kana_rm) -> (phone list, has_sokuon)"""
    sok = "'" in rm; core = rm.replace("'", "").replace("-", "")
    if core == "n": return ["en"], sok
    if core == "wo": core = "o"
    m = re.fullmatch(r"(ky|gy|ny|hy|my|ry|by|py|sh|ch|ts|j|[kgsztdnhfbpmyrw]?)([aiueo])", core)
    if not m: raise ValueError("cannot map " + rm)
    c, v = m.groups()
    if c in ("sh", "ch", "j") and v != "i": return [INIT[c], PAL[v]], sok
    if len(c) == 2 and c.endswith("y"): return [INIT[c[0]], PAL[v]], sok
    if c in ("s", "z") and v == "i": c = {"s": "sh", "z": "j"}[c]
    if c == "h" and v == "i": c = "sh"
    if c == "y" and v == "i": c = ""
    if c == "t" and v == "u": c = "ts"
    if c == "d" and v == "i": c = "j"
    ph = ([INIT[c]] if c else []) + [VOW[v]]
    return ph, sok

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

index = {}
for i, p in enumerate(cap["patterns"]):
    toks = [x for x in p["ly"].split() if x != "/"]
    rms = [common.kana_rm(t) for t in toks]
    v = p["v"].replace("|", ""); sd = 60 / p["bpm"] / p["sub"]
    notes = []; k = 0
    while k < len(v):
        if v[k] == "x":
            j = k + 1
            while j < len(v) and v[j] == "-": j += 1
            notes.append((k, j - k)); k = j
        else: k += 1
    mel = p.get("mel") or [0]
    ph, ns, ds, sl = [], [], [], []
    def add(phs, note, dur):
        for x in phs: ph.append(x); ns.append(note); ds.append(f"{dur:.4f}"); sl.append("0")
    t = 0
    for n, (st, ln) in enumerate(notes):
        if st > t: add(["SP"], "rest", (st - t) * sd)
        phs, sok = phones(rms[n]); nm = name(deg2midi(mel[n % len(mel)])); dur = ln * sd
        if sok: add(phs, nm, dur * .6); add(["SP"], "rest", dur * .4)
        else: add(phs, nm, dur)
        t = st + ln
    if t < len(v): add(["SP"], "rest", (len(v) - t) * sd)
    inp = {"text": "".join(toks), "ph_seq": " ".join(ph), "note_seq": " ".join(ns),
           "note_dur_seq": " ".join(ds), "is_slur_seq": " ".join(sl), "input_type": "phoneme"}
    print(i, p["t"], inp["ph_seq"])
    wav = infer.infer_once(inp)
    f = f"p{i}.wav"; save_wav(wav, os.path.join(OUT, f), hparams["audio_sample_rate"])
    print("  ->", len(wav) / hparams["audio_sample_rate"], "s, expected", len(v) * sd)
    index[str(i)] = f.replace(".wav", ".mp3")
json.dump(index, open(os.path.join(OUT, "index.json"), "w"))
