import sys, glob, math
from PIL import Image, ImageDraw
from render import *

import os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SAT = sorted(glob.glob(os.path.join(ROOT, 'assets/sat/*.jpg')))

def new(): return BG.copy()

# ---------------- beat draw functions ----------------
def b_hook(tl, dur, QR):
    im = new(); d = ImageDraw.Draw(im)
    y = 620
    headline(d, "THE BEST PRICES IN US REAL ESTATE ARE SET AT", y, 58, "Bold", INK, 900)
    a = ease((tl - 0.5) / 0.4)
    if a > 0:
        y2 = headline(d, "*FORECLOSURE* *AND* *TAX* *DEED* *AUCTIONS.*", 800, 70, "ExtraBold", INK, 940)
    if tl > 1.6:
        center_text(d, "Run by US counties. Bid online, from anywhere.", 1040, 36, "Medium", MUTED)
    return im

GEV = {z: Image.open(os.path.join(ROOT, f"assets/gev/z{z}.jpg")).convert("RGB") for z in (7, 9, 11, 13, 15, 17)
       if os.path.exists(os.path.join(ROOT, f"assets/gev/z{z}.jpg"))}

_FEATHER = {}
def _feather(n):
    """edge-feathered alpha mask so a finer tile blends into the coarser one (no visible seams)"""
    if n not in _FEATHER:
        import numpy as _np
        r = _np.linspace(-1, 1, n); a = _np.clip((1 - _np.abs(r)) / 0.35, 0, 1)
        _FEATHER[n] = Image.fromarray((_np.minimum.outer(a, a) * 255).astype("uint8"), "L")
    return _FEATHER[n]

def gev_frame(p):
    """Multi-scale deep zoom through Esri tiles (z7 state → z17 parcel). p in 0..1."""
    im = Image.new("RGB", (W, H), (8, 16, 28))
    if not GEV: return im
    zf = 7 + 10 * p                      # continuous zoom level
    hv = 4 / 2 ** zf                     # world span shown over the frame height
    for z in sorted(GEV):
        D = (4 / 2 ** z) / hv * H        # displayed tile size in px
        if D < 60: continue
        t = GEV[z]
        if D <= H:
            n = int(D); tile = t.resize((n, n), Image.BILINEAR)
            if z == min(GEV):
                im.paste(tile, (int((W - n) / 2), int((H - n) / 2)))
            else:
                k = clamp((D / H - 0.45) / 0.55)          # fade a finer level in as it grows — no pop, no dark square
                if k <= 0: continue
                m = _feather(n).point(lambda v: int(v * k))
                im.paste(tile, (int((W - n) / 2), int((H - n) / 2)), m)
        else:
            ch = 1024 * H / D; cw = 1024 * W / D
            box = (512 - cw / 2, 512 - ch / 2, 512 + cw / 2, 512 + ch / 2)
            im = t.resize((W, H), Image.BILINEAR, box=box)
    return im

def b_sat(tl, dur, QR):
    p = ease(clamp((tl - 0.2) / max(0.1, dur - 1.2)))
    im = gev_frame(p)
    if p > 0.97:
        d0 = ImageDraw.Draw(im); d0.rectangle([W / 2 - 46, H / 2 - 46, W / 2 + 46, H / 2 + 46], outline=(255, 255, 255), width=5)
    ImageDraw.Draw(im).text((24, H - 44), "Imagery: Esri World Imagery (Esri, Maxar, Earthstar Geographics)", font=F(20, "Medium"), fill=(220, 228, 238))
    d = ImageDraw.Draw(im)
    # contrast-safe caption pill
    font = F(44, "Bold"); text = "From the whole state to one parcel."
    tw = font.getlength(text); x0 = (W - tw) / 2 - 30
    d.rounded_rectangle([x0, 1250, x0 + tw + 60, 1250 + 90], radius=22, fill=(255, 255, 255))
    d.text(((W - tw) / 2, 1270), text, font=font, fill=INK)
    if tl > 1.4:
        font2 = F(38, "SemiBold"); t2 = f"{_SUM['upcoming']:,} upcoming auctions · {_SUM['counties_upcoming']} Florida counties selling"
        tw2 = font2.getlength(t2); x1 = (W - tw2) / 2 - 26
        d.rounded_rectangle([x1, 1360, x1 + tw2 + 52, 1360 + 76], radius=20, fill=(255, 255, 255))
        d.text(((W - tw2) / 2, 1376), t2, font=font2, fill=BLUE)
        font3 = F(24, "Medium"); t3 = f"AuctionRadar summary RPC · {_ASOF} · every lot has its own deal page"
        tw3 = font3.getlength(t3); x2 = (W - tw3) / 2 - 16
        d.rounded_rectangle([x2, 1456, x2 + tw3 + 32, 1456 + 44], radius=12, fill=(255, 255, 255))
        d.text(((W - tw3) / 2, 1464), t3, font=font3, fill=MUTED)
    return im

def b_one_number(tl, dur, QR):
    im = new(); d = ImageDraw.Draw(im)
    headline(d, "You get one number to be *right* *about.*", 560, 64, "Bold", INK, 900)
    a = ease((tl - 1.1) / 0.4)
    if a > 0:
        cy = 860 + int((1 - a) * 40)
        card(d, 140, cy, 800, 330)
        center_text(d, "SIGNAL$ MAX BID", cy + 40, 30, "Bold", BLUE)
        n = int(82000 * ease((tl - 1.1) / 0.8))
        center_text(d, money(n), cy + 95, 120, "ExtraBold", INK)
        center_text(d, "Walk away above this number. No exceptions.", cy + 250, 30, "Medium", MUTED)
    source_line(d, "Marion County · SIGNAL$ Property Report published 20 Jul 2026")
    return im

def b_phone(tl, dur, QR):
    im = new(); d = ImageDraw.Draw(im)
    headline(d, "The parcel. The liens. The risk. Priced *before* *the* *sale.*", 300, 56, "Bold", INK, 900)
    # phone
    px, py, pw, ph = 250, 640, 580, 940
    d.rounded_rectangle([px - 14, py - 14, px + pw + 14, py + ph + 14], radius=70, fill=INK)
    d.rounded_rectangle([px, py, px + pw, py + ph], radius=58, fill=WHITE)
    d.rounded_rectangle([px, py, px + pw, py + 70], radius=58, fill=BLUE)
    d.rectangle([px, py + 40, px + pw, py + 70], fill=BLUE)
    d.text((px + 34, py + 20), "biddeed.ai", font=F(28, "Bold"), fill=WHITE)
    d.text((px + pw - 170, py + 22), "Workspace", font=F(24, "Medium"), fill=(200, 220, 245))
    d.text((px + 36, py + 100), "FORECLOSURE · MARION COUNTY", font=F(20, "Bold"), fill=MUTED)
    d.text((px + 36, py + 132), "Case 422021CA000414CAAXXX", font=F(28, "SemiBold"), fill=INK)
    d.text((px + 36, py + 172), "Auction · 20 July 2026", font=F(22, "Medium"), fill=MUTED)
    d.rounded_rectangle([px + 36, py + 230, px + pw - 36, py + 370], radius=22, fill=TINT)
    d.text((px + 60, py + 250), "SIGNAL$ MAX BID", font=F(20, "Bold"), fill=BLUE)
    d.text((px + 60, py + 282), "$82,000", font=F(60, "ExtraBold"), fill=INK)
    d.text((px + 60, py + 344), "published before the sale", font=F(18, "Medium"), fill=MUTED)
    items = ["Parcel pulled", "Lien risk priced", "Every figure cites its record"]
    for i, it in enumerate(items):
        if tl > 1.2 + i * 0.5:
            yy = py + 420 + i * 78
            d.ellipse([px + 40, yy, px + 76, yy + 36], fill=BLUE)
            d.text((px + 49, yy + 4), "✓", font=F(24, "Bold"), fill=WHITE)
            d.text((px + 96, yy + 2), it, font=F(28, "SemiBold"), fill=INK)
    source_line(d, "biddeed.ai workspace · Marion County clerk record")
    return im

def b_workspace(tl, dur, QR):
    im = new(); d = ImageDraw.Draw(im)
    tabs = ["Map", "Calendar", "Table", "Spreadsheet"]
    active = min(int(tl / 0.9), 3)
    card(d, 80, 520, 920, 760)
    d.rounded_rectangle([80, 520, 1000, 590], radius=28, fill=TINT); d.rectangle([80, 560, 1000, 590], fill=TINT)
    x = 110
    for i, tb in enumerate(tabs):
        f = F(26, "SemiBold"); tw = f.getlength(tb)
        if i == active: d.rounded_rectangle([x - 14, 532, x + tw + 14, 578], radius=14, fill=BLUE)
        d.text((x, 540), tb, font=f, fill=WHITE if i == active else INK); x += tw + 60
    # content
    if active == 0:
        for (cx, cy) in [(260, 760), (480, 700), (700, 820), (880, 720), (330, 1000), (620, 1080), (820, 1000), (450, 900)]:
            d.ellipse([cx - 12, cy - 12, cx + 12, cy + 12], fill=BLUE)
    elif active == 1:
        for r in range(4):
            for c in range(7):
                xx, yy = 120 + c * 125, 640 + r * 140
                d.rounded_rectangle([xx, yy, xx + 110, yy + 120], radius=12, fill=TINT if (r * 7 + c) % 3 else WHITE, outline=TINT2)
                if (r * 7 + c) % 3 == 0: d.text((xx + 12, yy + 80), "sale", font=F(20, "Medium"), fill=BLUE)
    else:
        for r in range(8):
            yy = 640 + r * 74
            d.line([120, yy + 60, 960, yy + 60], fill=TINT2, width=2)
            for c, wdt in enumerate([260, 200, 180, 120]):
                xx = 120 + sum([260, 200, 180, 120][:c]) + c * 30
                d.rounded_rectangle([xx, yy + 14, xx + wdt - 40, yy + 44], radius=8, fill=TINT if r else BLUE)
    headline(d, "Map, calendar, table and spreadsheet over the *same* *rows.*", 1340, 48, "Bold", INK, 900)
    source_line(d, "biddeed.ai workspace")
    return im

def b_outcome(tl, dur, QR):
    im = new(); d = ImageDraw.Draw(im)
    headline(d, "Published before the sale. Checked after it.", 420, 54, "Bold", INK, 900)
    card(d, 100, 720, 880, 520)
    d.text((140, 760), "MARION COUNTY · CASE 422021CA000414CAAXXX", font=F(22, "Bold"), fill=MUTED)
    d.text((140, 830), "Bid limit set", font=F(26, "Medium"), fill=MUTED)
    d.text((140, 868), "$82,000", font=F(76, "ExtraBold"), fill=INK)
    d.text((600, 830), "Sale closed at", font=F(26, "Medium"), fill=MUTED)
    p = ease((tl - 0.9) / 1.3); n = int(73501 * p)
    d.text((600, 868), money(n), font=F(76, "ExtraBold"), fill=BLUE if p >= 1 else INK)
    if p >= 1 and tl > 2.4:
        f = F(56, "Bold"); t = "The ceiling HELD."; tw = f.getlength(t)
        d.text(((W - tw) / 2, 1090), t, font=f, fill=BLUE)
        d.text((140, 1180), "Outcome scorecard re-issued the same day", font=F(24, "Medium"), fill=MUTED)
    source_line(d, "Marion County foreclosure, 20 Jul 2026 · published report + clerk's recorded sale")
    return im

def deal_page(tl, addr, kind, sold, assessed, pct, url, dt):
    im = new(); d = ImageDraw.Draw(im)
    card(d, 70, 330, 940, 1120)
    d.rounded_rectangle([70, 330, 1010, 400], radius=28, fill=TINT); d.rectangle([70, 370, 1010, 400], fill=TINT)
    d.text((100, 350), "biddeed.ai/deal/…", font=F(24, "Medium"), fill=MUTED)
    d.text((110, 440), f"{kind} · {dt}", font=F(24, "Bold"), fill=BLUE)
    yy = headline(d, addr, 490, 44, "Bold", INK, 860, "left")
    d.text((110, yy + 10), "Sold at auction · won by a third-party bidder", font=F(26, "Medium"), fill=MUTED)
    # aerial placeholder block
    d.rounded_rectangle([110, yy + 70, 970, yy + 330], radius=20, fill=(220, 231, 244))
    d.text((130, yy + 290), "Aerial · county roll", font=F(20, "Medium"), fill=MUTED)
    by = yy + 370
    p = ease((tl - 0.8) / 0.9)
    for i, (lab, val) in enumerate([("Sold Price", money(int(sold * p))), ("Assessed Value", money(int(assessed * p)))]):
        x = 110 + i * 440
        d.text((x, by), lab, font=F(24, "Medium"), fill=MUTED)
        d.text((x, by + 36), val, font=F(64, "ExtraBold"), fill=INK)
    if tl > 1.9:
        d.rounded_rectangle([110, by + 140, 970, by + 240], radius=22, fill=BLUE)
        f = F(44, "Bold"); t = f"{pct}% below assessed value"; tw = f.getlength(t)
        d.text(((W - tw) / 2, by + 165), t, font=f, fill=WHITE)
    source_line(d, f"{url} · sale {dt} · county roll")
    return im

def b_deal_a(tl, dur, QR): return deal_page(tl, "4071 NW 3 Ter, Deerfield Beach 33064", "FORECLOSURE SALE · BROWARD COUNTY", 279200, 464650, 40, "biddeed.ai/deal/broward/CACE-24-008115", "1 Sep 2026")
def b_deal_b(tl, dur, QR): return deal_page(tl, "2753 NW 41st Ave, Cape Coral 33993", "TAX DEED SALE · LEE COUNTY", 101100, 155040, 35, "biddeed.ai/deal/lee/2026000141", "1 Sep 2026")

def b_report(tl, dur, QR):
    im = new(); d = ImageDraw.Draw(im)
    card(d, 90, 360, 900, 900)
    d.text((130, 400), "SIGNAL$ Property Report", font=F(34, "Bold"), fill=INK)
    d.text((770, 406), "18 sections", font=F(24, "Medium"), fill=MUTED)
    secs = ["Subject property", "Value bands", "Comparable sales", "Transaction history", "Zoning read", "Lien stack", "Red flags", "SIGNAL$ Max Bid", "Outcome scorecard"]
    for i, s in enumerate(secs):
        if tl > 0.3 + i * 0.22:
            yy = 470 + i * 52
            d.rounded_rectangle([130, yy, 950, yy + 40], radius=10, fill=TINT if i % 2 else WHITE)
            d.text((150, yy + 6), s, font=F(24, "SemiBold"), fill=INK)
            d.text((880, yy + 8), "✓", font=F(24, "Bold"), fill=BLUE)
    if tl > 2.4:
        d.text((130, 960), "Auction clearing band", font=F(22, "Medium"), fill=MUTED)
        d.text((130, 992), "$110,882 – $125,038", font=F(40, "ExtraBold"), fill=INK)
        d.text((130, 1060), "Open-market band", font=F(22, "Medium"), fill=MUTED)
        d.text((130, 1092), "$285,525 – $321,975", font=F(40, "ExtraBold"), fill=BLUE)
        d.text((130, 1170), "Sample · 8497 Juddith Ave, Palm Beach County · CMA n = 6", font=F(20, "Medium"), fill=MUTED)
    headline(d, "One property. Every angle. *$25.*", 1310, 56, "Bold", INK, 900)
    source_line(d, "biddeed.ai/buy-report · sample report on biddeed.ai")
    return im

def b_d4d(tl, dur, QR):
    im = new(); d = ImageDraw.Draw(im)
    headline(d, "Pick the lots. biddeed.ai *builds* *the* *route.*", 340, 56, "Bold", INK, 900)
    card(d, 90, 560, 900, 620)
    pts = [(200, 700), (420, 660), (640, 760), (860, 700), (760, 940), (520, 1020), (300, 960)]
    p = ease((tl - 0.4) / 1.6); nseg = int(p * (len(pts) - 1) * 100) / 100
    for i in range(len(pts) - 1):
        if nseg >= i:
            frac = min(1, nseg - i)
            x0, y0 = pts[i]; x1, y1 = pts[i + 1]
            d.line([x0, y0, x0 + (x1 - x0) * frac, y0 + (y1 - y0) * frac], fill=BLUE, width=6)
    for i, (x, y) in enumerate(pts):
        d.ellipse([x - 18, y - 18, x + 18, y + 18], fill=BLUE if i <= nseg + 0.01 else TINT2)
        d.text((x - 8, y - 14), str(i + 1), font=F(22, "Bold"), fill=WHITE)
    stats = [("7", "lots driven"), ("2", "worth bidding"), ("1", "off-auction find")]
    for i, (n, l) in enumerate(stats):
        if tl > 1.4 + i * 0.4:
            x = 140 + i * 290
            d.text((x, 1240), n, font=F(80, "ExtraBold"), fill=INK)
            d.text((x, 1330), l, font=F(26, "Medium"), fill=MUTED)
    source_line(d, "The Palm Bay run · biddeed.ai · Drive for Dollars")
    return im

def b_projects(tl, dur, QR):
    im = new(); d = ImageDraw.Draw(im)
    headline(d, "Win it. Budget it. Track it to the *closing* *table.*", 380, 56, "Bold", INK, 900)
    card(d, 100, 640, 880, 560)
    d.text((140, 680), "5400 PINA VISTA DR, MELBOURNE · 25-LINE REHAB", font=F(22, "Bold"), fill=MUTED)
    p = ease((tl - 0.6) / 1.2)
    d.text((140, 740), "Under budget", font=F(26, "Medium"), fill=MUTED)
    d.text((140, 780), "$" + f"{60140.61 * p:,.2f}", font=F(70, "ExtraBold"), fill=BLUE)
    d.text((140, 900), "Projected gross profit", font=F(26, "Medium"), fill=MUTED)
    d.text((140, 940), "$" + f"{68209.39 * p:,.2f}", font=F(70, "ExtraBold"), fill=INK)
    d.text((140, 1060), "Budget · scopes of work · bids · actuals — per property", font=F(24, "Medium"), fill=MUTED)
    source_line(d, "biddeed.ai · Projects · Pro Plus")
    return im

def b_founder(tl, dur, QR):
    im = new(); d = ImageDraw.Draw(im)
    center_text(d, "I bid with my own money first.", 380, 48, "Bold", INK)
    center_text(d, "Ariel Shapira · Founder · Developer · Builder", 450, 26, "Medium", MUTED)
    rows = [("Rainsville · tax deed", 5330, 398600), ("Lakewood · tax deed", 20100, 320000)]
    for i, (lab, a, b) in enumerate(rows):
        if tl > 0.5 + i * 1.2:
            yy = 600 + i * 330
            card(d, 100, yy, 880, 280)
            d.text((140, yy + 30), lab.upper(), font=F(22, "Bold"), fill=MUTED)
            p = ease((tl - 0.5 - i * 1.2) / 1.0)
            d.text((140, yy + 80), money(a), font=F(64, "ExtraBold"), fill=INK)
            d.text((470, yy + 88), "→", font=F(56, "Bold"), fill=BLUE)
            d.text((560, yy + 80), money(int(b * p)), font=F(64, "ExtraBold"), fill=BLUE)
            sub = "Ground-up build · both figures on the clerk's record" if i == 0 else "$1,256 a door in · $20,000 a door out · 16 units"
            d.text((140, yy + 190), sub, font=F(24, "Medium"), fill=MUTED)
    source_line(d, "Publicly recorded closings · everestcapitalusa.com")
    return im

def b_plans(tl, dur, QR):
    im = new(); d = ImageDraw.Draw(im)
    headline(d, "One below-market win pays for *years* of biddeed.ai.", 340, 54, "Bold", INK, 900)
    plans = [("Free", "$0", "forever · every county"), ("Investor", "$99", "/mo · reports + scorecard"), ("Pro", "$199", "/mo · zoning + D4D routes"), ("Pro Plus", "$399", "/mo · to the closing table")]
    for i, (n, pr, sub) in enumerate(plans):
        if tl > 0.3 + i * 0.35:
            yy = 600 + i * 190
            card(d, 100, yy, 880, 160, fill=TINT if i == 1 else WHITE)
            d.text((140, yy + 34), n, font=F(40, "Bold"), fill=INK)
            d.text((140, yy + 92), sub, font=F(24, "Medium"), fill=MUTED)
            f = F(64, "ExtraBold"); tw = f.getlength(pr)
            d.text((940 - tw, yy + 40), pr, font=f, fill=BLUE)
    source_line(d, "biddeed.ai/pricing · Sep 2026")
    return im

def b_cta(tl, dur, QR):
    im = new(); d = ImageDraw.Draw(im)
    headline(d, "Check your county *free.*", 460, 68, "ExtraBold", INK, 980)
    center_text(d, "No credit card for the county check.", 580, 32, "Medium", MUTED)
    if tl > 0.5:
        d.rounded_rectangle([240, 780, 840, 890], radius=30, fill=BLUE)
        center_text(d, "Check Your County Free", 808, 40, "Bold", WHITE)
    if tl > 1.0:
        im.paste(QR, (390, 980))
        center_text(d, "biddeed.ai", 1310, 44, "Bold", INK)
    return im

def b_end(tl, dur, QR):
    im = new(); d = ImageDraw.Draw(im)
    f = F(120, "ExtraBold"); t1, t2 = "BidDeed", ".AI"; w1, w2 = f.getlength(t1), f.getlength(t2)
    x = (W - w1 - w2) / 2
    d.text((x, 680), t1, font=f, fill=INK); d.text((x + w1, 680), t2, font=f, fill=BLUE)
    headline(d, "EVERY FORECLOSURE. EVERY TAX DEED. YOURS TO WIN.", 860, 38, "Bold", INK, 900)
    center_text(d, "For Everyone. Everywhere.", 980, 40, "Medium", MUTED)
    if tl > 0.6:
        d.rounded_rectangle([390, 1120, 690, 1196], radius=24, fill=BLUE)
        center_text(d, "biddeed.ai", 1136, 32, "Bold", WHITE)
    return im



# ---------------- beat lists ----------------
B = lambda id, draw, mn, vo, **kw: dict(id=id, draw=draw, min=mn, vo=vo, **kw)

HOOK = B("hook", b_hook, 3.0, "The best prices in US real estate are set at foreclosure and tax deed auctions.")
SAT_ = B("sat", b_sat, 4.0, "Run by US counties. Bid online, from anywhere.", dark=True)
ONE = B("one", b_one_number, 3.5, "You get one number to be right about.")
PHONE = B("phone", b_phone, 3.5, "The parcel, the liens, the risk. Priced before the sale.")
WORK = B("work", b_workspace, 3.6, "Map, calendar, table and spreadsheet — one set of rows.")
OUT = B("out", b_outcome, 4.2, "Published before the sale. Checked after it. The ceiling held.")
REPORT = B("report", b_report, 4.5, "Eighteen sections on one property. Twenty-five dollars.")
CTA = B("cta", b_cta, 3.2, "Check your county free. No card.")
END = B("end", b_end, 3.0, "For everyone. Everywhere.")

DEAL_A = B("deal_a", b_deal_a, 4.0, "Every sale gets a deal page. Sold price, assessed value, the gap.")
DEAL_B = B("deal_b", b_deal_b, 3.6, "Foreclosure or tax deed. Same page.")
D4D = B("d4d", b_d4d, 4.0, "Pick the lots. biddeed.ai builds the route.")
PROJ = B("proj", b_projects, 3.4, "Win it. Budget it. Track it to closing.")
FOUNDER = B("founder", b_founder, 4.0, "We fought in the trenches for over two decades, so you don't have to.")
PLANS = B("plans", b_plans, 3.6, "Free forever. One below-market win pays for years.")


# ---------------- AuctionRadar (the sticky page) ----------------
import json, calendar as _cal
_CAL = json.load(open(os.path.join(ROOT, 'data/cal_oct.json')))
_OCT = {x['date'][8:]: x for x in _CAL['days']}
_SUM = json.load(open(os.path.join(ROOT, 'data/summary.json')))
_ASOF = __import__("datetime").date.fromisoformat(_SUM.get("fetched_at", "2026-09-23")).strftime("%-d %b %Y")
_TOP = max(_CAL['days'], key=lambda x: x['total'])            # busiest sale day in the month — drives the tap-a-day beat
_TOPD = __import__("datetime").date.fromisoformat(_TOP['date'])
_MONTH = _TOPD.strftime("%B %Y")

def draw_month(d, tl, x0=70, y0=560, cw=134, ch=118, highlight=None, reveal=True):
    d.rounded_rectangle([x0, y0 - 80, x0 + 7 * cw, y0 + 5 * ch + 8], radius=26, fill=WHITE, outline=TINT2, width=3)
    d.text((x0 + 26, y0 - 62), _MONTH, font=F(30, "Bold"), fill=INK)
    d.text((x0 + 7 * cw - 300, y0 - 56), "‹ Prev   Today   Next ›", font=F(22, "Medium"), fill=MUTED)
    for i, wd in enumerate(["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]):
        d.text((x0 + i * cw + 12, y0 - 14), wd, font=F(18, "SemiBold"), fill=MUTED)
    _y, _m = int(_CAL['from'][:4]), int(_CAL['from'][5:7])
    first_wd, ndays = _cal.monthrange(_y, _m)          # Mon=0; month derived from the data file, not hard-coded
    rows = -(-(first_wd + ndays) // 7); ch = ch * 5 // rows  # 6-row months shrink cells instead of dropping days
    for day in range(1, ndays + 1):
        idx = first_wd + day - 1; r, c = divmod(idx, 7)
        cx, cy = x0 + c * cw, y0 + 10 + r * ch
        key = f"{day:02d}"; info = _OCT.get(key)
        hl = highlight == day
        d.rectangle([cx + 2, cy, cx + cw - 2, cy + ch - 4], fill=TINT if hl else WHITE, outline=(238, 243, 250))
        d.text((cx + 8, cy + 4), str(day), font=F(18, "SemiBold"), fill=BLUE if hl else MUTED)
        if info and (not reveal or tl > 0.25 + day * 0.04):
            if info['foreclosure_count']:
                d.rounded_rectangle([cx + 6, cy + 32, cx + cw - 8, cy + 66], radius=8, fill=BLUE)
                d.text((cx + 12, cy + 38), f"{info['foreclosure_count']} F", font=F(19, "Bold"), fill=WHITE)
            if info['tax_deed_count']:
                d.rounded_rectangle([cx + 6, cy + 72, cx + cw - 8, cy + 106], radius=8, fill=INK)
                d.text((cx + 12, cy + 78), f"{info['tax_deed_count']} TD", font=F(19, "Bold"), fill=WHITE)

def b_radar(tl, dur, QR):
    im = new(); d = ImageDraw.Draw(im)
    d.text((80, 300), "AUCTIONRADAR", font=F(26, "Bold"), fill=BLUE)
    headline(d, "Every sale in every county, on *one* *calendar.*", 340, 52, "Bold", INK, 920, "left")
    draw_month(d, tl)
    if tl > 2.0:
        for i, (n, l) in enumerate([(f"{_SUM['upcoming']:,}", "upcoming sales"), (str(_SUM['counties_upcoming']), "counties selling"), (f"{_SUM['total']:,}", "auction records")]):
            x = 90 + i * 320
            d.text((x, 1290), n, font=F(56, "ExtraBold"), fill=INK)
            d.text((x, 1352), l, font=F(24, "Medium"), fill=MUTED)
    source_line(d, f"biddeed.ai/auctions · calendar counts RPC · {_ASOF}")
    return im

def b_radar_day(tl, dur, QR):
    im = new(); d = ImageDraw.Draw(im)
    d.text((80, 300), "AUCTIONRADAR · TAP A DAY", font=F(26, "Bold"), fill=BLUE)
    headline(d, "Foreclosure *and* tax deed. Both, every day they sell.", 340, 52, "Bold", INK, 920, "left")
    draw_month(d, tl, highlight=_TOPD.day, reveal=False)
    if tl > 0.8:
        card(d, 90, 1200, 900, 280, fill=TINT)
        d.text((130, 1230), _TOPD.strftime("%A %-d %B %Y").upper(), font=F(22, "Bold"), fill=MUTED)
        p = ease((tl - 0.8) / 0.8)
        d.text((130, 1270), str(int(_TOP['total'] * p)), font=F(96, "ExtraBold"), fill=INK)
        d.text((330, 1300), "sales", font=F(30, "Medium"), fill=MUTED)
        if tl > 1.7:
            d.text((520, 1262), f"{_TOP['foreclosure_count']} foreclosures", font=F(30, "SemiBold"), fill=BLUE)
            d.text((520, 1310), f"{_TOP['tax_deed_count']} tax deeds", font=F(30, "SemiBold"), fill=INK)
            d.text((520, 1360), "Open as map · table · spreadsheet", font=F(22, "Medium"), fill=MUTED)
    source_line(d, f"biddeed.ai/auctions · calendar counts RPC · {_ASOF}")
    return im

RADAR = B("radar", b_radar, 4.6, "AuctionRadar. Every sale, every county, one calendar.")
def _ord(n): return str(n) + ("th" if 11 <= n % 100 <= 13 else {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th"))
RADAR_DAY = B("radar_day", b_radar_day, 4.2, f"Tap a day. {_TOP['total']} sales on {_TOPD.strftime('%B')} {_ord(_TOPD.day)}.")

V1 = [HOOK, SAT_, RADAR, ONE, PHONE, OUT, REPORT, CTA, END]
V2 = [HOOK, RADAR, RADAR_DAY, SAT_, ONE, OUT, DEAL_A, DEAL_B, REPORT, D4D, PROJ, FOUNDER, PLANS, CTA, END]

if __name__ == "__main__":
    import copy
    which = sys.argv[1]
    beats = copy.deepcopy(V1 if which == "v1" else V2)
    utm = "v1_corrected" if which == "v1" else "sticky_v2"
    os.makedirs(os.path.join(ROOT, "out"), exist_ok=True)
    out = os.path.join(ROOT, f"out/BidDeed_promo_{which}.mp4")
    music = os.path.join(ROOT, "assets/music.wav")
    render(beats, out, music if os.path.exists(music) else None, vo_speed=1.05, qr_url=f"https://biddeed.ai/auctions?utm_source=promo&utm_medium=video&utm_campaign={utm}")
