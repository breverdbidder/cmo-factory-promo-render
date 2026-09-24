import sys, os, math, subprocess, json, glob
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import soundfile as sf
import qrcode

W, H, FPS = 1080, 1920, 30
INK = (10, 37, 64); BLUE = (0, 94, 184); TINT = (230, 240, 250); TINT2 = (215, 227, 241); WHITE = (255, 255, 255)
MUTED = (92, 110, 134)
import os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FD = os.path.join(ROOT, "assets/fonts/")
TMP = os.path.join(ROOT, "out")
_fc = {}
def F(size, w="SemiBold"):
    k = (size, w)
    if k not in _fc: _fc[k] = ImageFont.truetype(os.path.join(FD, f"Inter-{w}.ttf"), size)
    return _fc[k]

def ease(t): return 0 if t <= 0 else 1 if t >= 1 else (1 - math.cos(math.pi * t)) / 2
def clamp(x, a=0, b=1): return max(a, min(b, x))

# ---------- background ----------
def make_bg():
    s = Image.new("RGB", (W // 8, H // 8), WHITE)
    d = ImageDraw.Draw(s)
    for (cx, cy, r) in [(20, 40, 45), (120, 70, 50), (40, 190, 55), (110, 210, 40)]:
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(205, 222, 242))
    s = s.filter(ImageFilter.GaussianBlur(22)).resize((W, H), Image.BILINEAR)
    return s
BG = make_bg()

# ---------- text helpers ----------
def wrap(text, font, maxw):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if font.getlength(t.replace("*", "")) <= maxw: cur = t
        else: lines.append(cur); cur = w
    if cur: lines.append(cur)
    return lines

def draw_rich_line(d, x, y, line, font, color, accent=BLUE):
    """words wrapped in *..* render in accent colour"""
    cx = x
    for i, w in enumerate(line.split(" ")):
        col = color
        if w.startswith("*") and w.endswith("*") and len(w) > 1: w, col = w[1:-1], accent
        elif w.startswith("*"): w, col = w[1:], accent
        elif w.endswith("*") and len(w) > 1: w, col = w[:-1], accent
        d.text((cx, y), w, font=font, fill=col)
        cx += font.getlength(w + " ")

def headline(d, text, y, size=64, w="Bold", color=INK, maxw=920, align="center", lh=1.18):
    font = F(size, w)
    lines = wrap(text, font, maxw)
    for i, ln in enumerate(lines):
        plain = ln.replace("*", "")
        tw = font.getlength(plain)
        x = (W - tw) / 2 if align == "center" else 80
        draw_rich_line(d, x, y + i * size * lh, ln, font, color)
    return y + len(lines) * size * lh

def center_text(d, text, y, size, w="SemiBold", color=INK):
    font = F(size, w); tw = font.getlength(text)
    d.text(((W - tw) / 2, y), text, font=font, fill=color); return y + size * 1.2

def source_line(d, text):
    if not text: return
    font = F(24, "Medium"); tw = font.getlength(text)
    d.text(((W - tw) / 2, H - 330), text, font=font, fill=MUTED)

def card(d, x, y, w, h, r=28, fill=WHITE, outline=TINT2):
    d.rounded_rectangle([x, y, x + w, y + h], radius=r, fill=fill, outline=outline, width=3)

def money(n): return "$" + f"{int(n):,}"

# ---------- captions ----------
def caption(img, words, t, y=H - 240):
    """words: list of (text, start, end) in beat-local seconds. Show current sentence, highlight spoken word."""
    if not words: return
    # sentence chunks split on . ? — / keep short
    chunks, cur = [], []
    for wd in words:
        cur.append(wd)
        if wd[0].endswith((".", "?", "!", "—")) or len(cur) >= 7: chunks.append(cur); cur = []
    if cur: chunks.append(cur)
    active = None
    for ch in chunks:
        if ch[0][1] - 0.15 <= t <= ch[-1][2] + 0.35: active = ch; break
    if not active: return
    font = F(40, "SemiBold")
    text = " ".join(w[0] for w in active)
    tw = font.getlength(text); pad = 28
    d = ImageDraw.Draw(img)
    x0 = (W - tw) / 2 - pad
    d.rounded_rectangle([x0, y - 18, x0 + tw + 2 * pad, y + 62], radius=20, fill=(255, 255, 255), outline=TINT2, width=2)
    cx = (W - tw) / 2
    for w in active:
        col = BLUE if w[1] <= t <= w[2] + 0.05 else INK
        d.text((cx, y), w[0], font=font, fill=col); cx += font.getlength(w[0] + " ")

# ---------- VO ----------
_pipe = None
def synth(text, speed=1.0):
    global _pipe
    if _pipe is None:
        from kokoro import KPipeline
        _pipe = KPipeline(lang_code='a', repo_id='hexgrad/Kokoro-82M')
    auds, words, off = [], [], 0.0
    for r in _pipe(text, voice='am_michael', speed=speed):
        a = r.audio.numpy() if hasattr(r.audio, "numpy") else np.asarray(r.audio)
        if r.tokens:
            for tk in r.tokens:
                if tk.start_ts is None or tk.text.strip() in ("", ".", ",", "—"): continue
                words.append((tk.text, off + tk.start_ts, off + tk.end_ts))
        auds.append(a); off += len(a) / 24000
    a = np.concatenate(auds) if auds else np.zeros(1)
    return a, off, words

# ---------- QR ----------
def qr_img(url, size=300):
    q = qrcode.QRCode(box_size=10, border=1); q.add_data(url); q.make(fit=True)
    im = q.make_image(fill_color=INK, back_color="white").convert("RGB")
    return im.resize((size, size), Image.NEAREST)

# ---------- render ----------
def render(beats, out_mp4, music_wav, vo_speed=1.05, qr_url="https://biddeed.ai/"):
    # 1) synth VO, fix durations
    for b in beats:
        if b.get("vo"):
            a, dur, words = synth(b["vo"], vo_speed)
            b["_audio"], b["_words"] = a, words
            b["dur"] = max(b["min"], dur + 0.55)
        else:
            b["_audio"], b["_words"] = None, []; b["dur"] = b["min"]
    total = sum(b["dur"] for b in beats)
    print("TOTAL", round(total, 2), "s", [(b["id"], round(b["dur"], 2)) for b in beats])
    # 2) audio track
    sr = 24000; vo = np.zeros(int(total * sr) + sr)
    t0 = 0.0
    for b in beats:
        if b["_audio"] is not None:
            s = int((t0 + 0.25) * sr); vo[s:s + len(b["_audio"])] += b["_audio"]
        t0 += b["dur"]
    os.makedirs(TMP, exist_ok=True); vo_path = os.path.join(TMP, "vo_track.wav"); sf.write(vo_path, vo, sr)
    # 3) frames
    QR = qr_img(qr_url)
    n_frames = int(total * FPS)
    cmd = ["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-i", vo_path]
    if music_wav:
        cmd += ["-stream_loop", "-1", "-i", music_wav, "-filter_complex",
                "[2:a]volume=0.22,atrim=0:%f[m];[1:a]volume=1.0[v];[v][m]amix=inputs=2:duration=first:dropout_transition=0,loudnorm=I=-16:TP=-1.5:LRA=11[a]" % total, "-map", "0:v", "-map", "[a]"]
    else:
        cmd += ["-filter_complex", "[1:a]loudnorm=I=-16:TP=-1.5:LRA=11[a]", "-map", "0:v", "-map", "[a]"]
    cmd += ["-c:v", "libx264", "-profile:v", "main", "-level", "4.0", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p",
            "-c:a", "aac", "-b:a", "160k", "-ar", "44100", "-movflags", "+faststart", "-shortest", out_mp4]
    ff = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    bi, bstart = 0, 0.0
    for fi in range(n_frames):
        t = fi / FPS
        while bi < len(beats) - 1 and t >= bstart + beats[bi]["dur"]: bstart += beats[bi]["dur"]; bi += 1
        b = beats[bi]; tl = t - bstart; dur = b["dur"]
        base = b["draw"](tl, dur, QR)
        # beat opacity envelope
        op = ease(tl / 0.3) * ease((dur - tl) / 0.25)
        if op < 1:
            base = Image.blend(BG if not b.get("dark") else Image.new("RGB", (W, H), (8, 16, 28)), base, op)
        if b.get("_words"): caption(base, b["_words"], tl - 0.25)
        ff.stdin.write(base.tobytes())
        if fi % 300 == 0: print("frame", fi, "/", n_frames, flush=True)
    ff.stdin.close(); ff.wait()
    print("DONE", out_mp4)
