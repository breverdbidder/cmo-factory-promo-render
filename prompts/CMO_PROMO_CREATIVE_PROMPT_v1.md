# CMO FACTORY — BidDeed.AI Brand Promo · Creative Prompt v1 (34 s cut, corrected)

Repo target: breverdbidder/cmo-factory-promo-video → `docs/CREATIVE_PROMPT_v1.md` (paste this whole file into the issue BODY — cc-runner reads title + body only).
Source clip reviewed: VID-20260923-WA0519.mp4 · 1080×1920 · 30 fps · H.264/AAC · 34.5 s · music bed only, no voice · 14 beats @ ~2.5 s.
Status of this doc: v1 = the clip you already have, with the 8 defects below fixed. v2 (sticky) is a separate file.

## 0. Definition of done (M7 revenue DoD)
Done = rendered MP4 in Supabase storage + `qa_pass=true` verdict row + pinned on YouTube @biddeedai + embedded on biddeed.ai `/` hero and `/pricing` + `/r/<code>` short link live (302, UTMs) + PostHog `promo_view → county_check` funnel visible. Publish step stays human-click until `spi_gates.test_purchase` closes (M8).

## 1. Purpose · audience · promise
- Purpose: brand promo (not a property reel). Stops the scroll, states the category, proves it with one recorded sale, sends to the free county check.
- Audience: US and foreign bidders (canon: "the global solution for foreigners who can participate in US county foreclosure/tax deed auctions by bidding online"). Assume no prior knowledge that these are county-run real-estate auctions — say it on screen.
- Promise (canon hero stack, in this order): 1 "THE BEST PRICES IN US REAL ESTATE ARE SET AT FORECLOSURE AND TAX DEED AUCTIONS." 2 "Our data is your unfair advantage at every US county auction." 3 "We fought in the trenches for over two decades so you don't have to."
- Retired, never render: "Know your number before the gavel" and any dread framing ("close in minutes", "before the clerk opens the file"). Enthusiasm and the pull of the category, not fear.

## 2. Hard constraints (fail-closed — Director/QA returns `qa_pass=false` on any hit)
1. Never-list: no person names except Ariel Shapira (M7); no homeowner contact language; no foreclosure-relief framing; no vendor names (Esri/Maxar/Google imagery credit is a licence line, allowed at ≤ 18 px); no unverified numbers.
2. M10 — every figure on screen carries a source line in the same beat (clerk record, published report id, county roll, or `table.column @ timestamp`). No source → the number does not render.
3. SIGNAL$ spelling: all caps, `$` character, every context. Labels are `SIGNAL$ Max Bid` and `SIGNAL$ Property Report`. `Shapira max bid`, `S5`, `Property Card` never appear on screen.
4. Max-bid gate: while cli-anything-biddeed #20240 (ML rebuild) is open and `/pricing` reads "figures Withheld until the model is revalidated", a live/current max bid may not be shown. Historical published figures ARE allowed with date + source (the Marion 20 Jul 2026 case qualifies). Fallback beat if the gate is still open at render: value band (clearing band vs open-market band) instead of a max-bid number.
5. M9 — end card carries `biddeed.ai/r/<code>` + QR; a brand promo lands on `/` (county check), property reels land on `/deal/<county>/<case>`. Publish gate: target 200 signed-out within 24 h, `/r/` 302 with UTMs, QR decodes to the same code.
6. Sale type clarity: at least one beat says on screen that these are county foreclosure AND tax deed sales.
7. Nationwide positioning: no beat may scope the product to Florida alone. Florida is the proving market — say "67 Florida counties live" as a fact, never "Florida auctions" as the category.
8. Palette/type: house blue-and-white only — `#005EB8` brand blue, `#0A2540` ink, `#E6F0FA` / `#D7E3F1` tints, white ground. No green/red/amber. Inter (Google Fonts, fallback stack). No gradients beyond the soft blue blur field.

## 3. Stack (License V2 — all already ruled)
- Composition: Remotion, `licenseKey: "free-license"` (branded one-off lane; daily reels stay on revideo/motion-canvas). Render on the GHA runner, not locally.
- Voice: Kokoro EN (Apache-2.0, launch-approved English voice). No ElevenLabs spend. Word-timed captions via whisperX (BSD-2) burned in; ~92 % of feed viewers are sound-off.
- Music: CC0/own bed, −16 LUFS integrated, duck −8 dB under VO.
- Maps: satellite tiles as in the current clip; keep the imagery credit line; raise map-caption contrast to ≥ 4.5:1 (the current "From the whole state to one parcel" caption fails on the dark tile).
- Output: 1080×1920 @ 30 fps H.264 CRF 20, ≤ 12 MB, plus a 1920×1080 crop for the site hero.

## 4. Beat sheet — v1 corrected (34 s)
| t (s) | On-screen | VO (Kokoro) | Source line (≤ 18 px, ink 60 %) | Fix vs current clip |
|---|---|---|---|---|
| 0.0–2.5 | THE BEST PRICES IN US REAL ESTATE ARE SET AT **FORECLOSURE AND TAX DEED AUCTIONS.** | "The best prices in US real estate are set at foreclosure and tax deed auctions." | — | Replaces "Florida auctions close in minutes." (Florida-scoped + dread) |
| 2.5–7.5 | Satellite zoom: state → county → parcel. Caption: "From the whole state to one parcel. 67 Florida counties live." | "Run by US counties. Bid online, from anywhere." | Imagery credit line | Caption contrast fix |
| 7.5–10 | "You get one number to be right about." | "You get one number to be right about." | — | keep |
| 10–12.5 | Card: **SIGNAL$ MAX BID · $82,000** · "Walk away above this number. No exceptions." | — | "Marion County · published 20 Jul 2026 · SIGNAL$ Property Report" | Label was unlabeled/Shapira |
| 12.5–15 | Phone mock: Case 422021CA000414CAAXXX · Parcel pulled ✓ · Lien risk priced ✓ · Every figure cites its row ✓ | "The parcel. The liens. The risk. Priced before the sale — every figure cites its record." | "biddeed.ai workspace" | Replaces "before the clerk opens the file" (dread) |
| 15–19 | Workspace: Map · Calendar · Table · Spreadsheet "over the same rows" | "Map, calendar, table and spreadsheet — one set of rows." | — | keep |
| 19–24 | Outcome card: **Bid limit set $82,000 · Sale closed at $73,501 · Outcome: HELD.** Counter runs 0 → 73,501; the word HELD appears only after the counter lands. | "Published before the sale. Checked after it. The ceiling held." | "Marion County foreclosure, 20 Jul 2026 · published report + clerk's recorded sale" | Current cut shows $82,000 = $82,000 with "The ceiling held" for ~1 s (frames 9–10) — reads as a wrong result. Label `Shapira max bid` → `Bid limit set` |
| 24–28 | SIGNAL$ Property Report · 18 sections · sections tick in (Lien stack, Outcome scorecard…) · "One property. Every angle. $25." | "Eighteen sections on one property. Twenty-five dollars." | "biddeed.ai/buy-report" | keep |
| 28–31 | "One below-market win pays for years of biddeed.ai." · **Check Your County Free** · "No credit card for the county check." | "One below-market win pays for years of biddeed.ai. Check your county free." | — | keep |
| 31–34.5 | End card: **BidDeed.AI** · EVERY FORECLOSURE. EVERY TAX DEED. YOURS TO WIN. · For Everyone. Everywhere. · `biddeed.ai/r/<code>` + QR | "For everyone. Everywhere." | — | Current end card has no URL path/QR (M9) |

VO word count ≈ 95 words / 34 s ≈ 2.8 wps — Kokoro at speed 1.0, no cut-offs.

## 5. Director / QA verdict (write to `reel_variant_review` or the promo equivalent — evidence, not claims)
- [ ] ffprobe: 1080×1920, 30 fps, 34–35 s, audio present, loudness −16 ±1 LUFS
- [ ] OCR every 0.5 s frame: zero hits on the retired lines, `Shapira`, `S5`, `Property Card`, vendor names, person names other than Ariel Shapira
- [ ] every `$` figure has a source line in the same frame (OCR pairing)
- [ ] max-bid gate: if #20240 open, the only max-bid figure on screen is the dated Marion one
- [ ] "foreclosure and tax deed" appears on screen at least once; "Florida" never appears as the category
- [ ] end card: URL + QR present; QR decodes to `/r/<code>`; `/r/<code>` → 302 → target 200 signed-out
- [ ] whisperX caption word-error ≤ 5 % against the VO script
- [ ] colour gate: palette-gate.mjs passes on 10 sampled frames
- [ ] contrast: every caption ≥ 4.5:1 on its actual background frame

## 6. Open defects found on the live site while sourcing this (not fixable from this repo — owner in brackets)
1. `/pricing` Investor line says max-bid "figures Withheld until the model is revalidated" while the hero says "every member — free included — gets the published number before bidding starts". Two opposite promises on one page. [cli-anything-biddeed / biddeed-web copy lane, blocked on #20240]
2. Same page: "2,911 upcoming auctions across 67 Florida counties" (map) vs "2,911 live right now across 60 counties" (Plans). [copy lane]
3. Deal pages `/deal/broward/CACE-24-008115` and `/deal/lee/2026000141` render "Report unavailable for this county" beside "or Investor $99/mo →" — the two biggest markets tell the visitor the paid thing does not exist. [biddeed-web]
4. The promo's hero case (Marion 422021CA000414CAAXXX) has no live deal page (404 on every slug variant tried) — the sample report link on `/` goes to a Palm Beach property instead. Either publish the Marion deal page or point the promo's proof at a case that has one. [cli-anything-biddeed reels/deal-page lane]
