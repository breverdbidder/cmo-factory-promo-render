"""Satellite deep-zoom tiles for the 'state → parcel' beat (vendored from cmo-factory-promo-video/fetch_tiles.py).
Free Esri World Imagery export; attribution is rendered in-frame (required). Target: 2813 Floresta Dr NE, Palm Bay (auction parcel).
Usage: python scripts/fetch_tiles.py   -> assets/gev/z7.jpg … z17.jpg"""
import math, os, urllib.request
LAT, LNG = 28.0226309, -80.5872705
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def lat_to_y(lat): return math.log(math.tan(math.pi / 4 + math.radians(lat) / 2))
def y_to_lat(y): return math.degrees(2 * math.atan(math.exp(y)) - math.pi / 2)
y0 = lat_to_y(LAT); os.makedirs(os.path.join(ROOT, "assets/gev"), exist_ok=True)
for z in [7, 9, 11, 13, 15, 17]:
    span = 360.0 * 4 / (2 ** z); hl = span / 2; hy = math.radians(span) / 2
    bbox = f"{LNG - hl},{y_to_lat(y0 - hy)},{LNG + hl},{y_to_lat(y0 + hy)}"
    url = ("https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/export"
           f"?bbox={bbox}&bboxSR=4326&imageSR=4326&size=1024,1024&format=jpg&f=image")
    out = os.path.join(ROOT, f"assets/gev/z{z}.jpg")
    urllib.request.urlretrieve(url, out); print(z, out, os.path.getsize(out))
