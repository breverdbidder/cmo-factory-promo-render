"""Refresh the AuctionRadar figures from the live SSOT RPCs (shared by biddeed.ai + zonewise.ai).
Writes data/cal_oct.json (per-day counts for the month shown) and data/summary.json (upcoming / counties / records).
Usage: python scripts/fetch_calendar.py 2026-10-01 2026-10-31
M10: every radar/satellite-pill figure on screen is read from these two files — never typed into beats.py."""
import sys, json, urllib.request, os, datetime
try:
    from zoneinfo import ZoneInfo; now = datetime.datetime.now(ZoneInfo("America/New_York"))
except Exception:
    now = datetime.datetime.utcnow()
frm, to = (sys.argv[1], sys.argv[2]) if len(sys.argv) > 2 else ("2026-10-01", "2026-10-31")
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def get(u): return json.load(urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": "cmo-factory-promo-render"}), timeout=60))
cal = get(f"https://zonewise.ai/api/auctions/calendar?from={frm}&to={to}"); cal["fetched_at"] = now.date().isoformat()
summ = get("https://zonewise.ai/api/auctions/summary")
summ = {k: summ[k] for k in ["total", "upcoming", "counties", "counties_upcoming", "date_min", "date_max"]}; summ["fetched_at"] = now.date().isoformat()
json.dump(cal, open(os.path.join(root, "data/cal_oct.json"), "w"), indent=0)
json.dump(summ, open(os.path.join(root, "data/summary.json"), "w"), indent=1)
days = cal["days"]; top = max(days, key=lambda x: x["total"])
print(f"{len(days)} sale days · {sum(d['total'] for d in days):,} auctions · {sum(d['foreclosure_count'] for d in days):,} F · {sum(d['tax_deed_count'] for d in days):,} TD · busiest {top['date']} = {top['total']}")
print(f"summary: {summ['upcoming']:,} upcoming · {summ['counties_upcoming']} counties selling · {summ['total']:,} records · as of {summ['fetched_at']} ET")
