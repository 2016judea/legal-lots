"""Build the derived sensitive-use layers for Cottage Grove, Apple Valley and Bloomington.

    python3 scripts/prep_south_metro.py

Writes, all EPSG:26915:
- data/raw/osm_park_attractions_south_metro.geojson: OpenStreetMap playgrounds, pitches,
  tracks, shelters, toilets, picnic tables, disc golf, inside a PUBLIC park polygon
  (Cottage Grove parks, Apple Valley parks, Dakota County park layer, Met Council regional
  parks). Both ordinances buffer from the attraction, not the park line. (c) OSM
  contributors, ODbL.
- data/raw/osm_bloomington_highway_barriers.geojson: I-494, I-35W and MN-77 carriageways.
  Bloomington 14.280(c): "Measurements shall not extend across" them.
- data/raw/samhsa_residential_south_metro.geojson: SAMHSA FindTreatment facilities (MH and
  SUD) whose service setting includes residential, within 12 km of Cottage Grove and Apple
  Valley. A stand-in for the DHS licence list, which sits behind a captcha.
"""
import json, subprocess, urllib.parse
from pathlib import Path
import duckdb

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data/raw"
BBOX = "44.68,-93.42,44.89,-92.85"
CRS = {"type": "name", "properties": {"name": "urn:ogc:def:crs:EPSG::26915"}}


def overpass(q, cache):
    """Overpass answer, cached in data/raw/osm_cache/<cache>.json (delete the file to refresh)."""
    f = RAW / "osm_cache" / f"{cache}.json"
    if f.exists():
        return json.loads(f.read_text())["elements"]
    import time
    for i in range(6):
        host = ("https://overpass-api.de/api/interpreter", "https://overpass.kumi.systems/api/interpreter")[i % 2]
        out = subprocess.run(["curl", "-s", "-m", "240", "-A", "legal-lots/1.0", "--data-urlencode", f"data={q}", host],
                             capture_output=True).stdout
        try:
            els = json.loads(out)["elements"]
            f.parent.mkdir(exist_ok=True)
            f.write_text(json.dumps({"elements": els}))
            return els
        except ValueError:
            time.sleep(20)   # rate-limited or busy
    raise SystemExit("overpass unavailable")


def geom(e):
    if e["type"] == "node":
        return {"type": "Point", "coordinates": [e["lon"], e["lat"]]}
    if e["type"] == "way":
        pts = [[p["lon"], p["lat"]] for p in e["geometry"]]
        if len(pts) > 3 and pts[0] == pts[-1]:
            return {"type": "Polygon", "coordinates": [pts]}
        return {"type": "LineString", "coordinates": pts}
    # relation: use its outer member ways as lines (rare for these tags)
    lines = [[[p["lon"], p["lat"]] for p in m["geometry"]] for m in e.get("members", []) if m.get("geometry")]
    return {"type": "MultiLineString", "coordinates": lines}


def to_26915(con, feats, out, source):
    con.execute("create or replace table t (props varchar, g geometry)")
    for f in feats:
        con.execute("insert into t select ?, st_transform(st_geomfromgeojson(?), 'EPSG:4326', 'EPSG:26915', always_xy := true)",
                    [json.dumps(f["properties"]), json.dumps(f["geometry"])])
    rows = con.execute("select props, st_asgeojson(g) from t").fetchall()
    json.dump({"type": "FeatureCollection", "crs": CRS, "source": source,
               "features": [{"type": "Feature", "properties": json.loads(p), "geometry": json.loads(g)} for p, g in rows]},
              open(out, "w"))
    print(f"{out.name}: {len(rows)} features")


def main():
    con = duckdb.connect(); con.execute("install spatial; load spatial")

    # park attractions
    q = f"""[out:json][timeout:180];(
      nwr["leisure"~"^(playground|pitch|track|disc_golf_course|picnic_table|fitness_station)$"]({BBOX});
      nwr["amenity"~"^(toilets|shelter)$"]({BBOX});
      nwr["building"~"^(pavilion|shelter|toilets)$"]({BBOX}););out geom;"""
    feats = [{"properties": {"osm": f"{e['type']}/{e['id']}",
                             "kind": e["tags"].get("leisure") or e["tags"].get("amenity") or e["tags"].get("building")},
              "geometry": geom(e)} for e in overpass(q, "attractions")]
    tmp = RAW / "_osm_attr_4326.geojson"
    to_26915(con, feats, tmp, "overpass")
    parks = []
    for f, name in [("cottage_grove_parks.geojson", "NAME"), ("apple_valley_parks.geojson", "Name"),
                    ("dakota_parks.geojson", "PARKNAME"), ("metc_regional_park_admin_boundaries.geojson", None)]:
        nm = f'cast("{name}" as varchar)' if name else "'regional park'"
        parks.append(f"select {nm} as park, geom from st_read('{RAW / f}')")
    con.execute("create or replace table parks as " + " union all ".join(parks))
    rows = con.execute(f"""
        select a.osm, a.kind, any_value(p.park), st_asgeojson(a.geom) from st_read('{tmp}') a
        join parks p on st_intersects(a.geom, p.geom)
        group by a.osm, a.kind, a.geom""").fetchall()
    out = RAW / "osm_park_attractions_south_metro.geojson"
    fs = []
    for osm, kind, park, g in rows:
        fs.append({"type": "Feature", "geometry": json.loads(g),
                   "properties": {"osm": osm, "kind": kind, "name": f"{park} ({kind})"}})
    json.dump({"type": "FeatureCollection", "crs": CRS, "source": "OpenStreetMap via Overpass (ODbL), clipped to public park polygons", "features": fs}, open(out, "w"))
    tmp.unlink()
    print(f"{out.name}: {len(fs)} attractions inside public parks")

    # Bloomington highway barriers
    q = """[out:json][timeout:180];way["highway"~"^(motorway|trunk)$"]["ref"~"(I 494|I 35W|MN 77)"](44.76,-93.42,44.87,-93.15);out geom;"""
    feats = [{"properties": {"ref": e["tags"].get("ref"), "osm": f"way/{e['id']}"}, "geometry": geom(e)} for e in overpass(q, "highways")]
    to_26915(con, feats, RAW / "osm_bloomington_highway_barriers.geojson", "OpenStreetMap via Overpass (ODbL)")

    # SAMHSA residential
    seen, feats = set(), []
    for lat, lon in [(44.8277, -92.9438), (44.7319, -93.2177)]:
        for st in ("MH", "SA"):
            u = f"https://findtreatment.gov/locator/exportsAsJson/v2?sAddr={lat},{lon}&limitType=2&limitValue=12000&sType={st}&pageSize=500&page=1"
            d = json.loads(subprocess.run(["curl", "-s", "-m", "120", u], capture_output=True, check=True).stdout)
            for r in d.get("rows", []):
                setting = "; ".join(s.get("f3", "") for s in r.get("services", []) if "Setting" in s.get("f1", ""))
                key = (r["name1"], r["street1"])
                if "esidential" not in setting or key in seen:
                    continue
                seen.add(key)
                feats.append({"properties": {"name": r["name1"], "address": f"{r['street1']}, {r['city']}", "setting": setting, "type": r.get("typeFacility")},
                              "geometry": {"type": "Point", "coordinates": [float(r["longitude"]), float(r["latitude"])]}})
    to_26915(con, feats, RAW / "samhsa_residential_south_metro.geojson", "findtreatment.gov exportsAsJson v2, MH+SA, residential settings")


if __name__ == "__main__":
    main()
