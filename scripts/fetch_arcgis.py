"""Page an ArcGIS FeatureServer layer to GeoJSON in EPSG:26915.

usage: python3 scripts/fetch_arcgis.py <layer_url> <out.geojson> [where]
Pages by resultOffset; writes a FeatureCollection with a crs member naming 26915.
"""
import json, subprocess, sys, urllib.error, urllib.parse, urllib.request

def get(url, params):
    q = url + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(q, headers={"User-Agent": "legal-lots/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            return json.load(r)
    except urllib.error.URLError as e:
        # arcgis.metc.state.mn.us serves an incomplete cert chain; curl uses the system store
        if "CERTIFICATE_VERIFY_FAILED" not in str(e):
            raise
        return json.loads(subprocess.run(["curl", "-s", "--max-time", "120", q], capture_output=True, check=True).stdout)

def main(layer, out, where="1=1"):
    meta = get(layer, {"f": "json"})
    page = min(meta.get("maxRecordCount") or 1000, 2000)
    feats, off = [], 0
    while True:
        d = get(layer + "/query", {"where": where, "outFields": "*", "outSR": 26915,
                                   "f": "geojson", "resultOffset": off,
                                   "resultRecordCount": page, "orderByFields": meta.get("objectIdField") or "OBJECTID"})
        if "error" in d:
            raise SystemExit(f"{layer}: {d['error']}")
        fs = d.get("features", [])
        feats += fs
        off += len(fs)
        if not fs or (len(fs) < page and not d.get("exceededTransferLimit") and not d.get("properties", {}).get("exceededTransferLimit")):
            break
    fc = {"type": "FeatureCollection",
          "crs": {"type": "name", "properties": {"name": "urn:ogc:def:crs:EPSG::26915"}},
          "source": layer, "features": feats}
    json.dump(fc, open(out, "w"))
    print(f"{out}: {len(feats)} features")

if __name__ == "__main__":
    main(*sys.argv[1:])
