# Factory registration

Done 23 Sep 2026: row added to `breverdbidder/cmo-factory` → `registry/repos.md` via pull request (cmo-factory rule: PR-only, never self-merged). The issue body below is the follow-on work for the ops repo.

# Register this lane in the CMO Factory — paste as a cli-anything-biddeed issue (title + body only; cc-runner reads nothing else)

**Title:** CP3d — promo render lane: adopt breverdbidder/cmo-factory-promo-render

**Body:**
Adopt `breverdbidder/cmo-factory-promo-render` as the brand-promo render lane of the CMO Factory.
1. Add it to `docs/gtm/CMO_FACTORY_META_PROMPT.md` under video stack → "branded one-offs" beside the Remotion composition (`cmo-factory-promo-video`), and to unified_context `cmo_factory_meta_v1.repos`.
2. Mirror `prompts/*.md` into `docs/gtm/promo/` and register both as content-audit rows with a SOURCE column (M10).
3. Wire `render.yml` artifacts into the LMS `/reels` review screen as `pending_approval` rows (asset_kind = brand_promo); publish stays human-click (M8) until `spi_gates.test_purchase` closes.
4. Add `scripts/fetch_calendar.py` counts to the QA verdict: any radar figure on screen must equal `data/cal_oct.json` (OCR pairing).
5. Attach the live-site defects in `docs/REVIEW_2026-09-23.md` to their owning lanes (#20240 for the max-bid withhold; biddeed-web for the deal-page "Report unavailable" and the 60/67 county count; reels lane for the missing Marion deal page).
Definition of done (M7): the v2 clip is pinned on @biddeedai and embedded on `/` and `/pricing`, PostHog `promo_view → county_check` funnel visible, and the first `county_check` from a `utm_campaign=sticky_v2` session is recorded. Terminal states: FIXED / BLOCKED (name the blocker) / DECIDED-AGAINST (say why).
Never-list, M7 (no person names but the founder), M9 (end card → own page), M10 (sourced figures) apply.
