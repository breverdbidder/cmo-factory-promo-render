"""Self-synthesized 120 BPM bed — no licensing risk (vendored from cmo-factory-promo-video/make_music.py, duration parameterised).
Usage: python scripts/make_music.py [seconds]   -> assets/music.wav  (Dm-Bb-F-C, kick/hats/bass/pad, riser + ding into the end card)"""
import sys, os, wave
import numpy as np
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sr = 44100; dur = float(sys.argv[1]) if len(sys.argv) > 1 else 72.0
t = np.arange(int(sr * dur)) / sr; beat = 0.5; mix = np.zeros_like(t)
def env(n, a, d):
    e = np.ones(n); an = max(1, int(a * sr)); dn = max(1, int(d * sr)); e[:an] = np.linspace(0, 1, an)
    if dn < n: e[n - dn:] *= np.linspace(1, 0, dn)
    return e
def place(sig, start):
    i = int(start * sr); j = min(len(mix), i + len(sig))
    if 0 <= i < j: mix[i:j] += sig[:j - i]
chords = [[146.83, 174.61, 220.00], [116.54, 146.83, 174.61], [174.61, 220.00, 261.63], [130.81, 164.81, 196.00]]
bass_notes = [73.42, 58.27, 87.31, 65.41]
for bar in range(int(dur / (beat * 4)) + 1):
    ch = chords[bar % 4]; b0 = bar * 4 * beat
    n = int(4 * beat * sr); tt = np.arange(n) / sr; pad = np.zeros(n)
    for f in ch: pad += np.sin(2 * np.pi * f * tt) * 0.5 + np.sin(2 * np.pi * f * 2.001 * tt) * 0.12
    place(pad * env(n, 0.25, 0.6) * 0.05, b0)
    for k in range(8):
        n2 = int(0.22 * sr); tt2 = np.arange(n2) / sr; f = bass_notes[bar % 4] * (2 if k % 4 == 3 else 1)
        place(np.sin(2 * np.pi * f * tt2) * env(n2, 0.004, 0.18) * 0.16, b0 + k * beat / 2)
    for k in range(4):
        n3 = int(0.16 * sr); tt3 = np.arange(n3) / sr; f0 = 120 * np.exp(-tt3 * 18) + 42
        place(np.sin(2 * np.pi * np.cumsum(f0) / sr) * np.exp(-tt3 * 22) * 0.9, b0 + k * beat)
    rng = np.random.default_rng(bar)
    for k in range(8):
        n4 = int(0.05 * sr); hp = np.diff(rng.standard_normal(n4), prepend=0)
        place(hp * np.exp(-np.arange(n4) / sr * 90) * 0.07, b0 + k * beat / 2 + beat / 4)
    for k in (1, 3):
        n5 = int(0.12 * sr); place(rng.standard_normal(n5) * np.exp(-np.arange(n5) / sr * 35) * 0.10, b0 + k * beat)
n6 = int(2.0 * sr); tt6 = np.arange(n6) / sr
place(np.sin(2 * np.pi * (300 + 500 * tt6 / 2) * tt6) * np.linspace(0, 0.05, n6), dur - 2.6)
n7 = int(0.9 * sr); tt7 = np.arange(n7) / sr
place((np.sin(2 * np.pi * 880 * tt7) + 0.5 * np.sin(2 * np.pi * 1320 * tt7)) * np.exp(-tt7 * 4) * 0.12, dur - 2.2)
mix = np.tanh(mix * 1.4) * 0.8; stereo = np.stack([mix, mix], axis=1)
out = os.path.join(ROOT, "assets/music.wav"); os.makedirs(os.path.dirname(out), exist_ok=True)
w = wave.open(out, "wb"); w.setnchannels(2); w.setsampwidth(2); w.setframerate(sr)
w.writeframes((stereo * 32767).astype("<i2").tobytes()); w.close(); print("music", dur, "s ->", out)
