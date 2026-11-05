"""Every parcel in one city where a cannabis shop is legally allowed.

    python3 scripts/build_city.py minneapolis

Reads rules/<city>.json (the ordinance, as data), the city's zoning layer and the
sensitive-use layers in data/raw/, and the county parcels already joined in
bricks' GIS DuckDBs. Writes out/<city>/lots.csv and out/<city>/summary.json.

Method, so a planner can check it:
- A parcel's zoning is the district covering the largest share of the lot.
- A sensitive use given as a point is promoted to the parcel that contains it,
  so distance is measured property line to property line, which is how both
  Minneapolis and Saint Paul measure. A point with no parcel stays a point.
- Distance is the shortest gap between the two shapes in EPSG:26915 metres,
  reported in feet. "Whole lot" rules fall out of this for free: if any part of
  the lot is inside the radius, the shortest gap is under it.

Optional rule keys (added for the south-metro cities, 2026-10-10; absent keys
leave Minneapolis and Saint Paul exactly as they were):
- zoning_layer.code_sql: SQL expression that turns the layer's field into the
  district code (Cottage Grove stores "B-2, Retail Business").
- allowed_districts.retail_conditional: districts where retail needs a CUP or
  other discretionary approval. Those lots are listed with approval=conditional.
- buffers[].where: SQL filter on the sensitive layer (e.g. K-12 grade ranges).
- buffers[].name_field: the layer column that names each sensitive use.
- buffers[].only_where_zoned: keep a sensitive use only if it sits in one of
  these city districts (Cottage Grove counts day cares only in B1-B3, PB, MU).
- buffers[].promote_points: false keeps a point as a point. Use it where the code
  measures from the feature itself (a playground), not its property line.
- buffers[].barrier_layer: lines a measurement may not cross (Bloomington's
  I-494 / I-35W / MN-77). A pair whose shortest line crosses one is dropped.
"""
import csv, json, sys
from pathlib import Path

import duckdb

ROOT = Path(__file__).resolve().parent.parent
BRICKS = Path.home() / "Desktop/workspace/bricks/data"
FT = 3.28084


def main(city: str) -> None:
    rules = json.loads((ROOT / "rules" / f"{city}.json").read_text())
    out = ROOT / "out" / city
    out.mkdir(parents=True, exist_ok=True)

    con = duckdb.connect()
    con.execute("install spatial; load spatial")
    county = rules["county"].lower()
    con.execute(f"attach '{BRICKS / (county + '_gis.duckdb')}' as c (read_only)")

    use_col = "PR_TYP_NM1" if county == "hennepin" else "USECLASS1"
    con.execute(f"""
        create table parcels as
        select pin, owner, {'tax_name' if county=='hennepin' else 'null'} as tax_name,
               st_makevalid(geom) as geom, concat_ws(' ', addr_house, addr_street) as address, {use_col} as use,
               area_sqft, build_yr, market_value, sale_date, lon, lat
        from c.parcels where upper(munic) = upper(?) and geom is not null and not coalesce(is_condo, false)
    """, [rules.get("munic", rules["city"])])

    z = rules["zoning_layer"]
    code_sql = z.get("code_sql") or f'"{z["field"]}"'
    con.execute(f"""
        create table zoning as
        select {code_sql} as code, st_makevalid(geom) as geom from st_read('{ROOT / z['file']}')
    """)
    # zoning by largest overlap
    con.execute("""
        create table pz as
        select pin, code from (
          select p.pin, z.code, row_number() over (partition by p.pin
                 order by st_area(st_intersection(p.geom, z.geom)) desc) rn
          from parcels p join zoning z on st_intersects(p.geom, z.geom)
        ) where rn = 1
    """)

    allowed = rules["allowed_districts"]["retail"]
    conditional = rules["allowed_districts"].get("retail_conditional")
    con.execute("create table cand as select p.*, pz.code from parcels p join pz using(pin) where pz.code in (select unnest(?::varchar[]))", [allowed + (conditional or [])])
    n_zoned = con.execute("select count(*) from cand").fetchone()[0]

    # buffers
    reasons = {}
    every = []   # every (lot, rule, sensitive use) that fails, not just the nearest
    for b in rules["buffers"]:
        f = ROOT / b["layer"].split()[0]
        t = b["sensitive_type"]
        con.execute(f"create or replace table s as select * from st_read('{f}') where {b.get('where') or 'true'}")
        cols = [r[0] for r in con.execute("describe s").fetchall()]
        name_col = b.get("name_field") or next((c for c in ("MDENAME", "SchoolName", "NAME", "Name", "name", "ORGNAME", "SchoolNa_1", "OWNNAME", "STREETNM") if c in cols), None)
        num = "HOUSENUM" if "HOUSENUM" in cols else ("BuildingNumber" if "BuildingNumber" in cols else None)
        label = f"concat_ws(' ', cast(\"{num}\" as varchar), cast(\"{name_col}\" as varchar))" if num and name_col in ("STREETNM",) else (f'cast("{name_col}" as varchar)' if name_col else f"'{t}'")
        con.execute(f"create or replace table s as select {label} as name, geom from s")
        if b.get("only_where_zoned"):
            con.execute("""create or replace table s as select s.* from s where exists (
                select 1 from zoning z where st_intersects(z.geom, s.geom) and z.code in (select unnest(?::varchar[])))""",
                        [b["only_where_zoned"]])
        exempt = b.get("exempt_districts") or []
        # promote points to their containing parcel (property line)
        con.execute(f"""
            create or replace table s2 as
            select s.name, coalesce(any_value(p.geom), any_value(s.geom)) as geom
            from s left join c.parcels p on {'true' if b.get('promote_points', True) else 'false'}
                 and st_geometrytype(s.geom) = 'POINT' and st_contains(p.geom, s.geom)
            group by s.name, s.geom
        """)
        d_m = b["distance_ft"] / FT
        barrier = ""
        if b.get("barrier_layer"):
            con.execute(f"create or replace table bar as select st_union_agg(geom) geom from st_read('{ROOT / b['barrier_layer']}')")
            barrier = "and not st_intersects((select geom from bar), st_shortestline(c.geom, s2.geom))"
        rows = con.execute(f"""
            select c.pin, s2.name, min(st_distance(c.geom, s2.geom)) d
            from cand c join s2 on st_dwithin(c.geom, s2.geom, {d_m})
            where c.code not in (select unnest(?::varchar[])) {barrier}
            group by c.pin, s2.name
        """, [exempt or ["__none__"]]).fetchall()
        for pin, name, d in rows:
            every.append((pin, t, name, d))
            # ties (two schools sharing one lot) break by name, so reruns are byte-identical
            if pin not in reasons or (d, t, str(name)) < (reasons[pin][2], reasons[pin][0], str(reasons[pin][1])):
                reasons[pin] = (t, name, d)

    for lt in rules.get("location_tests") or []:
        if lt["type"] == "contiguous_area":
            con.execute(f"create or replace table area as select geom from st_read('{ROOT / lt['city_layer']}')")
            rows = con.execute("""
                select c.pin from cand c where not exists (
                  select 1 from area a where st_intersects(a.geom, c.geom)
                   and st_area(st_intersection(a.geom, c.geom)) > 0.5 * st_area(c.geom))
            """).fetchall()
            for (pin,) in rows:
                reasons.setdefault(pin, ("outside_3_acre_area", "not in a 3+ acre dispensary-zoned block", 0))

    cand = con.execute("select pin, address, code, use, owner, tax_name, area_sqft, build_yr, market_value, sale_date, lon, lat from cand").fetchall()
    cols = ["pin", "address", "zoning", "use", "owner", "taxpayer", "lot_sqft", "year_built", "market_value", "last_sale", "lon", "lat"]
    if conditional is not None:
        cols.append("approval")
        cand = [r + ("conditional" if r[2] in conditional else "permitted",) for r in cand]
    eligible = [r for r in cand if r[0] not in reasons]
    with open(out / "lots.csv", "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(cols)
        for r in sorted(eligible, key=lambda r: (r[2] or "", r[1] or "")):
            w.writerow(r)
    with open(out / "excluded.csv", "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["pin", "address", "zoning", "buffer", "nearest", "distance_ft"])
        for r in cand:
            if r[0] in reasons:
                t, n, d = reasons[r[0]]
                w.writerow([r[0], r[1], r[2], t, n, round(d * FT)])

    with open(out / "exclusions_all.csv", "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["pin", "rule", "sensitive_use", "distance_ft"])
        for pin, t, n, d in sorted(every, key=lambda r: (r[0], r[1], r[3], str(r[2]))):
            w.writerow([pin, t, n, round(d * FT)])

    summary = {
        "city": rules["city"], "parcels": con.execute("select count(*) from parcels").fetchone()[0],
        "in_allowed_district": n_zoned, "excluded_by_buffer": len(reasons), "eligible": len(eligible),
        "by_district": {}, "excluded_by_type": {},
    }
    for r in eligible:
        summary["by_district"][r[2]] = summary["by_district"].get(r[2], 0) + 1
    if conditional is not None:
        summary["eligible_permitted"] = sum(1 for r in eligible if r[-1] == "permitted")
        summary["eligible_conditional"] = sum(1 for r in eligible if r[-1] == "conditional")
    for t, _, _ in reasons.values():
        summary["excluded_by_type"][t] = summary["excluded_by_type"].get(t, 0) + 1
    (out / "summary.json").write_text(json.dumps(summary, indent=2))
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main(sys.argv[1])
