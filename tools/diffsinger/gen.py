"""Sing the audition phrase with DiffSinger (MoonInTheRiver, Opencpop e2e model).
Run from inside the cloned DiffSinger repo with PYTHONPATH=. ; writes OUT wav."""
import sys, numpy as np
from inference.svs.ds_e2e import DiffSingerE2EInfer
from utils.hparams import set_hparams, hparams
from utils.audio import save_wav

OUT = sys.argv[1]
# audition.html PAT at 96 BPM (16th = 0.15625 s); E major degrees -> note names
s16 = 60 / 96 / 4
notes = ["G#4/Ab4", "B4", "B4", "C#5/Db5", "B4", "G#4/Ab4", "F#4/Gb4", "G#4/Ab4", "E4", "G#4/Ab4", "B4", "G#4/Ab4"]
lens = [2, 4, 2, 4, 2, 1, 1, 2, 3, 3, 2, 8]
text = "晚风吹过城市的光我想着你"  # original lyric, 12 syllables
inp = {"text": text, "notes": " | ".join(notes),
       "notes_duration": " | ".join(f"{l * s16:.5f}" for l in lens), "input_type": "word"}
set_hparams(config="usr/configs/midi/e2e/opencpop/ds100_adj_rel.yaml", exp_name="0228_opencpop_ds100_rel", print_hparams=False)
infer = DiffSingerE2EInfer(hparams)
wav = infer.infer_once(inp)
save_wav(wav, OUT, hparams["audio_sample_rate"])
print("saved", OUT, len(wav) / hparams["audio_sample_rate"], "s")
