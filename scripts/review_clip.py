"""Review tooling used on the source clip (Sep 23 2026): probe, contact sheet, speech check.
Usage: python scripts/review_clip.py path/to/clip.mp4  -> out/review/contact.jpg + transcript.txt"""
import sys, os, subprocess, glob
from PIL import Image
clip = sys.argv[1]; out = "out/review"; os.makedirs(out, exist_ok=True)
print(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration,size:stream=codec_name,width,height,r_frame_rate", "-of", "default=nw=1", clip], capture_output=True, text=True).stdout)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", clip, "-vf", "fps=1/2.5,scale=270:-1", f"{out}/f_%02d.jpg"])
fs = sorted(glob.glob(f"{out}/f_*.jpg")); ims = [Image.open(f) for f in fs]; w, h = ims[0].size; cols = 7; rows = (len(ims) + cols - 1) // cols
sheet = Image.new("RGB", (cols * w, rows * h), "black")
for i, im in enumerate(ims): sheet.paste(im, ((i % cols) * w, (i // cols) * h))
sheet.save(f"{out}/contact.jpg", quality=85); print("contact sheet:", f"{out}/contact.jpg", len(ims), "frames")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", clip, "-vn", "-ac", "1", "-ar", "16000", f"{out}/audio.wav"])
from faster_whisper import WhisperModel
segs, info = WhisperModel("tiny", device="cpu", compute_type="int8").transcribe(f"{out}/audio.wav", vad_filter=True)
lines = [f"{s.start:.1f}-{s.end:.1f} {s.text}" for s in segs]
open(f"{out}/transcript.txt", "w").write("\n".join(lines) or "NO SPEECH DETECTED (music bed only)")
print("\n".join(lines) or "NO SPEECH DETECTED (music bed only)")
