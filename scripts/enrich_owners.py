"""Turn out/<city>/lots.csv into the report a buyer pays for.

    python3 scripts/enrich_owners.py minneapolis

Keeps the lots a shop could actually go on (commercial or industrial, built or
vacant), adds the owner's mailing address from the county parcel service, years
held, and any licensed cannabis retailer already on or near the lot. Writes
out/<city>/report.csv.
"""
import csv, json, re, sys, time
from datetime import date
from math import cos, radians, hypot
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parent.parent
SERVICES = {
    "hennepin": ("https://gis.hennepin.us/arcgis/rest/services/HennepinData/LAND_PROPERTY/MapServer/1/query",
                 "PID", ["PID", "OWNER_NM", "TAXPAYER_NM", "TAXPAYER_NM_1", "TAXPAYER_NM_2", "TAXPAYER_NM_3"]),
    "ramsey": ("https://maps.co.ramsey.mn.us/arcgis/rest/services/ParcelData/AttributedData/MapServer/2/query",
               "ParcelID", ["ParcelID", "OwnerName", "TaxName1", "TaxName2", "TaxAddress1", "TaxAddress2",
                            "TaxCityStateZIP", "BusinessSquareFeet", "EMVBuilding"]),
    "dakota": ("https://gis2.co.dakota.mn.us/arcgis/rest/services/DC_OL_DCPI/MapServer/4/query",
               "TAXPIN", ["TAXPIN", "FULLNAME", "OWN_ADD_L1", "OWN_ADD_L2", "OWN_ADD_L3", "USE1_DESC", "SITEADDRESS", "BLDGVAL"]),
    "washington": ("https://maps.co.washington.mn.us/arcgis/rest/services/GISViewer/Parcels/MapServer/0/query",
                   "PIN", ["PIN", "OWNER_NAME", "OWN_ADD_L1", "OWN_ADD_L2", "OWN_ADD_L3", "USE1_DESC", "SITUS_ADDRESS", "EMV_BLDG"]),
}
# Washington publishes USE1_DESC as a code; 3xx is commercial and 4xx industrial
# (checked: Kwik Trip's Cottage Grove lot is 300). Dakota publishes words.
WASH_SHOP = re.compile(r"^[34]\d\d$")
SHOP_USES = re.compile(r"COMMERCIAL|INDUSTRIAL|3A ", re.I)


def fetch(county, pins):
    url, key, fields = SERVICES[county]
    out = {}
    for i in range(0, len(pins), 150):
        chunk = pins[i:i + 150]
        where = f"{key} IN (" + ",".join(f"'{p}'" for p in chunk) + ")"
        for attempt in range(4):
            try:
                r = requests.post(url, data={"where": where, "outFields": ",".join(fields),
                                             "returnGeometry": "false", "f": "json"}, timeout=60)
                feats = r.json()["features"]
                break
            except Exception:
                time.sleep(2 * (attempt + 1))
        else:
            raise SystemExit(f"{county} service failed on chunk {i}")
        for f in feats:
            a = f["attributes"]
            out[str(a[key]).strip()] = a
        print(f"  {min(i + 150, len(pins))}/{len(pins)}", end="\r", flush=True)
    print()
    return out


def mailing(county, a):
    if county == "hennepin":
        lines = [(a.get(k) or "").strip() for k in ("TAXPAYER_NM", "TAXPAYER_NM_1", "TAXPAYER_NM_2", "TAXPAYER_NM_3")]
        lines = [re.sub(r"\s+", " ", l) for l in lines if l]
        return lines[0] if lines else "", ", ".join(lines[1:]), ""
    if county in ("dakota", "washington"):
        name = (a.get("FULLNAME") or a.get("OWNER_NAME") or "").strip()
        addr = ", ".join(x.strip() for x in (a.get("OWN_ADD_L1"), a.get("OWN_ADD_L2"), a.get("OWN_ADD_L3")) if x and x.strip())
        return name, addr, ""
    name = " ".join(x for x in ((a.get("TaxName1") or "").strip(), (a.get("TaxName2") or "").strip()) if x)
    addr = ", ".join(x.strip() for x in (a.get("TaxAddress1"), a.get("TaxAddress2"), a.get("TaxCityStateZIP")) if x and x.strip())
    return name, addr, a.get("BusinessSquareFeet") or ""


def retailers(city):
    """Licensed cannabis retailers in this city, from the bricks directory scrape."""
    p = Path.home() / "Desktop/bricks/data/outreach/cannabis/mn_retailers.json"
    rows = json.loads(p.read_text())
    rows = rows if isinstance(rows, list) else rows.get("retailers", [])
    want = city.replace("-", " ").lower()
    out = []
    for r in rows:
        c = re.sub(r"^(st\.?|saint) ", "saint ", (r.get("city") or "").lower())
        lat, lon = r.get("lat") or r.get("latitude"), r.get("lon") or r.get("lng") or r.get("longitude")
        if c == want and lat and lon:
            out.append((r.get("name") or r.get("business_name") or "", float(lat), float(lon)))
    return out


def main(city):
    rules = json.loads((ROOT / "rules" / f"{city}.json").read_text())
    county = rules["county"].lower()
    lots = list(csv.DictReader(open(ROOT / "out" / city / "lots.csv")))
    if county in ("dakota", "washington"):
        got = fetch(county, [r["pin"] for r in lots])
        for r in lots:
            a = got.get(r["pin"], {})
            r["use"] = (a.get("USE1_DESC") or "").strip()
            r["address"] = r["address"] or (a.get("SITEADDRESS") or a.get("SITUS_ADDRESS") or "").strip()
        ok = (lambda u: WASH_SHOP.match(u)) if county == "washington" else (lambda u: SHOP_USES.search(u))
        lots = [r for r in lots if ok(r["use"])]
    else:
        lots = [r for r in lots if SHOP_USES.search(r["use"] or "")]
        got = fetch(county, [r["pin"] for r in lots])
    print(f"{city}: {len(lots)} commercial/industrial lots")
    shops = retailers(city)
    this_year = date.today().year
    cols = ["pin", "address", "zoning", "use", "lot_sqft", "building_sqft", "year_built", "market_value",
            "owner", "mail_to", "mailing_address", "years_held", "nearest_cannabis_store", "store_distance_ft",
            "vacant", "map"]
    with open(ROOT / "out" / city / "report.csv", "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(cols)
        for r in lots:
            a = got.get(r["pin"], {})
            name, addr, bsf = mailing(county, a) if a else ("", "", "")
            held = ""
            if r["last_sale"] and r["last_sale"][:4].isdigit():
                held = this_year - int(r["last_sale"][:4])
            near, dft = "", ""
            if shops and r["lat"]:
                la, lo = float(r["lat"]), float(r["lon"])
                k = cos(radians(la))
                best = min(shops, key=lambda s: hypot(s[1] - la, (s[2] - lo) * k))
                dft = round(hypot(best[1] - la, (best[2] - lo) * k) * 364000)
                near = best[0]
            w.writerow([r["pin"], r["address"].title(), r["zoning"], r["use"].title(), round(float(r["lot_sqft"] or 0)),
                        bsf, r["year_built"], r["market_value"], (r["owner"] or a.get("OWNER_NM") or a.get("OwnerName") or "").strip(),
                        name, addr, held, near, dft,
                        int(bool(re.match(r"LAND|VACANT", r["use"] or "")) if county == "hennepin" else (a.get("EMVBuilding", a.get("BLDGVAL", a.get("EMV_BLDG"))) in (0, 0.0))),
                        f"https://www.google.com/maps/search/?api=1&query={r['lat']},{r['lon']}"])
    print(f"wrote out/{city}/report.csv ({len(lots)} rows, {sum(1 for r in lots if r['pin'] in got)} with mailing address)")


if __name__ == "__main__":
    main(sys.argv[1])
