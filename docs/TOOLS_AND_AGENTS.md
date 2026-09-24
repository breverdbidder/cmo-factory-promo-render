# Tools, platforms, prompts and agents used — promo build, 23 Sep 2026

## Platforms
| Layer | What | Why / ruling |
|---|---|---|
| Orchestration | Claude (Fable 5.1) in the Claude mobile app, acting as AI Architect + editor | Reviewed the clip, wrote the prompts, wrote and ran the renderer, QA'd the frames |
| Compute | Claude sandbox (Ubuntu 24, Python 3.12, ffmpeg, CPU only) | ~3 min per render at 1080×1920×30fps |
| Source data | biddeed.ai (homepage, /pricing, /deal/*, sample report), zonewise.ai `/api/auctions/calendar` + `/api/auctions/summary` (SSOT RPCs) | Every on-screen figure was read live, not from memory (M10) |
| Memory/canon | Claude memory files: cmo-factory, winnerdata canon, biddeed-tiers, track-record, auctionradar-po-parity, v4-ensemble-ml-goal | Brand copy canon, never-list, M7/M8/M9/M10, max-bid withhold, retired lines |
| GitHub | connector (read-only, 403 on writes) + Supabase GitHub helper RPCs | reads/writes of private repos went through the DB helpers |
| Delivery | /mnt/user-data/outputs → Claude file cards → WhatsApp | WhatsApp re-encode: H.264 Main 4.0, AAC 44.1k, faststart, < 16 MB |

## Tools (all open source / free tier — Sep 12 2026 standing rule)
| Tool | Version / licence | Used for |
|---|---|---|
| ffmpeg / ffprobe | Ubuntu build | probe, frame extraction, audio extraction, rawvideo encode, amix + loudnorm, faststart |
| Pillow | 12.1 (HPND) | every frame: background blur field, cards, type, counters, calendar grid, phone/deal-page mocks |
| Inter | 4.0 (OFL 1.1) | brand type — Regular/Medium/SemiBold/Bold/ExtraBold |
| Kokoro-82M (`kokoro` 0.9, `am_michael`, speed 1.05) | Apache-2.0 | English VO — launch-approved voice, $0; token timestamps drive the captions |
| espeak-ng + spaCy en_core_web_sm | GPL-3 (system binary, not linked) / MIT | Kokoro phonemisation dependency |
| torch (CPU wheel) | BSD | Kokoro runtime — the CUDA wheel filled the disk; CPU index is mandatory |
| faster-whisper `tiny` | MIT | speech check on the source clip (result: no speech, music bed only) |
| qrcode | BSD | end-card QR → `https://biddeed.ai/auctions?utm_source=promo&utm_medium=video&utm_campaign=<v>` |
| soundfile / numpy | BSD | VO track assembly at 24 kHz |
| Esri World Imagery export | free, attribution in-frame | satellite deep zoom z7→z17 to 2813 Floresta Dr NE, Palm Bay (`fetch_tiles.py`) |
| numpy synth (`make_music.py`) | own code | 120 BPM Dm–Bb–F–C bed, riser + ding into the end card — same bed as the source clip |
| GitHub Actions | ubuntu-latest | `render.yml` — re-render on push/dispatch, canon gate, QA, artifacts only |
| Supabase `gh_api_req` / `gh_push_files_handler` (vault PAT, SECURITY DEFINER) | existing | created this repo and pushed it — the GitHub connector in chat is read-only (403) |

Rejected/not used here: ElevenLabs (spend), Remotion (kept for the private composition; this lane must never be the thing that adds a 4th seat), pyvideotrans (GPL), Coqui XTTS weights (non-commercial), Modal/Veo/Imagen (paid or quota-blocked).

## Agents / roles in this build (single Claude session, roles applied in sequence)
1. **Reviewer** — `scripts/review_clip.py` equivalent: ffprobe, 14-frame contact sheet, speech check; produced the 8-defect list in `docs/REVIEW_2026-09-23.md`.
2. **Researcher** — live reads of biddeed.ai and the calendar/summary RPCs; found the four live-site defects (max-bid withheld vs hero promise; 60 vs 67 counties; "Report unavailable" on Broward/Lee deal pages; Marion hero case has no deal page).
3. **Creative director** — `prompts/CMO_PROMO_CREATIVE_PROMPT_v1.md` and `..._STICKY_CLIP_v2.md`: beat tables, VO, source lines, hard constraints, QA verdicts.
4. **Renderer/engineer** — `src/render.py`, `src/beats.py`; voice-driven timeline; word captions.
5. **QA** — contact sheets of both renders; fixed the CTA subtitle overlap, VO-too-long beats, deep-zoom tile seams, and an in-video contradiction (satellite pill said 2,911 / 67 while the radar said 2,692 / 61) by wiring every count to `data/`.
6. **Distributor** — WhatsApp re-encode; file-card delivery.

## Prompts that produced the video (verbatim intent, in order)
- Ariel: "review the video and the repo and our github cmo factory… create our creative prompt and create another version with more information from our deal page and our website as sticky clip"
- Ariel: "Where is the actual video?" → render, don't spec (Sep 22 2026 standing rule: fix and deliver, not findings)
- Ariel: "The calendar radar I think is the best sticky page we have" → AuctionRadar becomes beats 2–3 of v2 and is inserted into v1; counts pulled from the calendar RPC
- Ariel: "I need to share this video via WhatsApp" → `scripts/whatsapp.sh`
- Ariel: "Create the github repo with all the code base including all the tools and platforms… and add it as github repo to our cmo factory" / "Fix everything needed and have the github repo with all the code and framework" → this repo; assets regenerated from code; registration PR on cmo-factory `registry/repos.md` (PR-only per cmo-factory CLAUDE.md)
- The full creative prompts are in `prompts/`; the VO lines are the `vo=` strings in `src/beats.py` and are the single source for both audio and captions.
