# cmo-factory-promo-render

BidDeed.AI brand promo — the rendering lane of the CMO Factory. Everything that produced `BidDeed_promo_v1.mp4` (corrected 34→40.7 s cut) and `BidDeed_promo_v2.mp4` (68.9 s sticky cut, AuctionRadar centerpiece) on Wed 23 Sep 2026 is in this repo: the creative prompts, the beat sheet as code, the voice, captions, QR, WhatsApp re-encode, the review tooling used on the source clip, and a GitHub Actions lane that re-renders it with zero humans in the loop.

Related: `breverdbidder/cmo-factory-promo-video` (the Remotion ping-style v2 draft this corrects and extends; its tile fetcher and music synth are vendored here), `breverdbidder/cmo-factory` (SSOT — this repo is registered in `registry/repos.md`), `docs/FACTORY_REGISTRATION.md`.

Pinned prompt figures (`prompts/*.md`) are the numbers read on 23 Sep 2026; the rendered radar figures always come from `data/` at render time.

## Layout
```
prompts/   CMO_PROMO_CREATIVE_PROMPT_v1.md   the corrected v1 spec (constraints, beat table, QA gates, live-site defects)
           CMO_PROMO_STICKY_CLIP_v2.md       the sticky cut: retention mechanics + every figure with its source
src/       render.py   frame renderer (PIL → ffmpeg pipe), Kokoro VO, word-timed captions, QR, music duck, loudnorm
           beats.py    every beat as a draw function + VO line; V1 / V2 beat lists; `python src/beats.py v1|v2`
data/      cal_oct.json   live AuctionRadar per-day counts (calendar RPC) — month grid, badges, busiest-day drill-down + its VO line
           summary.json   live upcoming / counties selling / records — radar header strip + satellite pill
scripts/   fetch_calendar.py  refresh both data files from the SSOT RPCs (ET-dated)
           fetch_tiles.py     satellite deep-zoom tiles (vendored from cmo-factory-promo-video)
           make_music.py      the music bed (vendored from cmo-factory-promo-video, duration parameterised)
           fetch_fonts.sh     Inter 4.0
           review_clip.py     what was run on the source clip: ffprobe, contact sheet, speech check
           whatsapp.sh        H.264 Main/faststart re-encode, < 16 MB
assets/    generated, never committed: fonts/ (fetch_fonts.sh · Inter 4.0 OFL) · gev/z7…z17.jpg (fetch_tiles.py · Esri World Imagery, attribution in-frame) · music.wav (make_music.py · self-synthesized 120 BPM, no licence risk)
docs/      TOOLS_AND_AGENTS.md  full record of tools, platforms, prompts and agent roles used
           REVIEW_2026-09-23.md the review of the source clip + the live-site findings
.github/workflows/render.yml   GHA render lane → MP4 artifacts (no publish, M8)
```

## Run
```
sudo apt-get install ffmpeg espeak-ng
pip install torch --index-url https://download.pytorch.org/whl/cpu && pip install -r requirements.txt
pip install https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.8.0/en_core_web_sm-3.8.0-py3-none-any.whl
bash scripts/fetch_fonts.sh && python scripts/fetch_tiles.py && python scripts/make_music.py 90
python scripts/fetch_calendar.py 2026-10-01 2026-10-31
python src/beats.py v2          # → out/BidDeed_promo_v2.mp4
bash scripts/whatsapp.sh out/BidDeed_promo_v2.mp4
```
Every asset is regenerated from code, so a clean runner reproduces the cut with no binaries in git. The satellite beat is a multi-scale deep zoom composited from the six Esri levels (edge-feathered, finer levels faded in by size — no seams). Radar numbers move with the data: re-run `fetch_calendar.py` and the calendar, the busiest-day card and its VO line all update together.

Or push to main / run the workflow: **Actions → render-promo → Run workflow** → MP4s (plus `_whatsapp` versions < 16 MB) under the run's `promo-mp4` artifact.

## How timing works
Beat length = max(min_dur, VO length + 0.55 s). Kokoro is synthesised first, so the timeline is voice-driven and captions are word-timed from Kokoro's own token timestamps (no second ASR pass needed). Change a VO line and the beat stretches; nothing is hand-timed.

## Canon this code enforces (see prompts/ for the full list)
- Hook = canon hero line 1; "For Everyone. Everywhere." signature; "EVERY FORECLOSURE. EVERY TAX DEED. YOURS TO WIN." outro.
- `SIGNAL$` spelling everywhere; no `Shapira max bid`, `S5`, `Property Card`.
- M10: every `$` figure has a source line in the same beat. Radar counts come from `data/cal_oct.json`, never typed.
- Max-bid gate: only the dated Marion 20 Jul 2026 figure ($82,000 → $73,501) while #20240 is open.
- M9: end card carries a QR + URL with UTMs; nationwide framing, Florida stated as a fact not a category; no vendor or person names beyond the founder.
- Palette: #005EB8 / #0A2540 / #E6F0FA / #D7E3F1 on white; Inter.

## License notes
Code MIT. Inter font OFL 1.1. Kokoro-82M Apache-2.0. faster-whisper MIT. ffmpeg/libx264 as distributed by Ubuntu. Remotion is deliberately NOT used in this lane (it is the private repo's composition; this lane must stay free of the 3-seat tripwire).
