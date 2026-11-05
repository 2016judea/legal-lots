"""Geocode OCM-licensed retail sites near the cities whose ordinances space shops apart.

    python3 scripts/prep_ocm_sites.py

Reads data/raw/MN_OCM_licensed_businesses_100526_tcm1202-714418.xlsx (OCM list as of
2026-10-05), keeps every site with a street address in or next to Cottage Grove and
Apple Valley, geocodes with the free US Census batch geocoder, and writes
data/raw/ocm_retail_sites_south_metro.geojson in EPSG:26915.

`kind` is cannabis_retail | cannabis_other | lphe_retail. `liquor` flags an LPHE
retailer whose name says it is a liquor store or bar, because Cottage Grove
11-4-18.G.7.e(2) exempts those and does not count them against anyone.
"""
import csv, io, json, re, subprocess, urllib.request
from pathlib import Path
import openpyxl

ROOT = Path(__file__).resolve().parent.parent
XLSX = ROOT / "data/raw/MN_OCM_licensed_businesses_100526_tcm1202-714418.xlsx"
OUT = ROOT / "data/raw/ocm_retail_sites_south_metro.geojson"
NEAR = ["cottage grove", "woodbury", "saint paul park", "st. paul park", "newport", "inver grove heights",
        "hastings", "denmark", "grey cloud", "afton", "apple valley", "burnsville", "lakeville",
        "rosemount", "eagan", "savage", "bloomington"]
LIQUOR = re.compile(r"liquor|wine|spirits|beer|bar\b|pub\b|tavern|brew|taproom|saloon|lounge|grill", re.I)


def rows():
    wb = openpyxl.load_workbook(XLSX, read_only=True)
    for ws in wb.worksheets:
        it = ws.iter_rows(values_only=True)
        h = next(it)
        for r in it:
            d = dict(zip(h, r))
            addr = (d.get("Retail Site Address") or "").strip()
            auth = (d.get("Local Authority") or "")
            if not addr or addr == "N/A" or not any(n in (auth + " " + addr).lower() for n in NEAR):
                continue
            lt = d.get("License Type") or ""
            if ws.title.startswith("Licensed cannabis"):
                kind = "cannabis_retail" if (d.get("Business Type") == "Retail" or "Retail" in lt) else "cannabis_other"
            else:
                if "Retailer" not in lt:
                    continue
                kind = "lphe_retail"
            name = d.get("D.B.A. (Doing Business As)") or d.get("Legal Business Name")
            yield {"license": d["License Number"], "license_type": lt, "kind": kind, "name": name,
                   "address": addr, "authority": auth,
                   "liquor": bool(kind == "lphe_retail" and LIQUOR.search(f"{name} {d.get('Legal Business Name')}")),
                   "endorsements": str(d.get("Endorsements and Activities") or d.get("Business Type") or "")}


def split(addr):
    # "8711 E Point Douglas Road S, Unit# 108 Cottage Grove, MN 55016"
    m = re.match(r"(.+?),\s*(?:(?:Suite|Unit|Ste|Apt)#?\s*\S+\s+)?(.+?),\s*MN\s*(\d{5})", addr)
    if not m:
        return addr, "", ""
    return m.group(1), m.group(2), m.group(3)


def main():
    rs = list(rows())
    buf = io.StringIO()
    w = csv.writer(buf)
    for i, r in enumerate(rs):
        st, city, z = split(r["address"])
        w.writerow([i, st, city, "MN", z])
    body = buf.getvalue()
    res = subprocess.run(["curl", "-s", "-m", "300", "-F", "addressFile=@-;filename=a.csv",
                          "-F", "benchmark=Public_AR_Current",
                          "https://geocoding.geo.census.gov/geocoder/locations/addressbatch"],
                         input=body.encode(), capture_output=True, check=True).stdout.decode()
    pts = {}
    for line in csv.reader(io.StringIO(res)):
        if len(line) >= 6 and line[2] == "Match":
            lon, lat = map(float, line[5].split(","))
            pts[int(line[0])] = (lon, lat, line[4])
    feats, miss = [], []
    import duckdb
    con = duckdb.connect(); con.execute("install spatial; load spatial")
    for c in ("washington", "dakota", "hennepin", "scott", "ramsey"):
        con.execute(f"attach '{Path.home() / 'Desktop/workspace/bricks/data' / (c + '_gis.duckdb')}' as {c} (read_only)")
    for i, r in enumerate(rs):
        if i in pts:
            lon, lat, matched = pts[i]
            x, y = con.execute("select st_x(g), st_y(g) from (select st_transform(st_point(?, ?), 'EPSG:4326', 'EPSG:26915', always_xy := true) g)", [lon, lat]).fetchone()
        else:
            # fallback: the county parcel with the same house number and street-name token, in the same city
            st, city, _ = split(r["address"])
            m = re.match(r"(\d+)\s+(.*)", st)
            hit = None
            if m:
                toks = [t for t in re.split(r"[\s,]+", m.group(2).upper()) if t not in ("N", "S", "E", "W", "ST", "STREET", "AVE", "AVENUE", "RD", "ROAD", "DR", "DRIVE", "HWY", "HIGHWAY", "W.", "LANE", "LN", "BLVD", "BOULEVARD", "WAY", "MN-13", "COUNTY")]
                tok = toks[0] if toks else ""
                if tok.isdigit():
                    tok = tok + "%"   # '13' -> '13...', '98' -> '98th'
                for c in ("washington", "dakota", "hennepin", "scott", "ramsey"):
                    hit = con.execute(f"""select cx, cy, lon, lat, addr_house || ' ' || addr_street from {c}.parcels
                        where addr_house = ? and upper(addr_street) like ? and upper(coalesce(addr_city, munic)) like ?
                        order by area_sqft desc limit 1""", [int(m.group(1)), f"%{tok}%", f"%{city.upper()[:6]}%"]).fetchone()
                    if hit:
                        break
            if not hit:
                miss.append(r["address"]); continue
            x, y, lon, lat, matched = hit
            matched = "parcel:" + matched
        feats.append({"type": "Feature", "geometry": {"type": "Point", "coordinates": [x, y]},
                      "properties": {**r, "geocoded": matched, "lon": lon, "lat": lat}})
    json.dump({"type": "FeatureCollection", "crs": {"type": "name", "properties": {"name": "urn:ogc:def:crs:EPSG::26915"}},
               "source": f"{XLSX.name} + US Census batch geocoder (Public_AR_Current)", "unmatched": miss,
               "features": feats}, open(OUT, "w"), indent=0)
    print(f"{OUT.name}: {len(feats)} geocoded, {len(miss)} unmatched")
    for m in miss:
        print("  unmatched:", m)


if __name__ == "__main__":
    main()
