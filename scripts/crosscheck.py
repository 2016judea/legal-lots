"""Agreement between our eligible lots and the city's own published cannabis map."""
import csv, json, sys
import duckdb
city, layer, where = sys.argv[1], sys.argv[2], (sys.argv[3] if len(sys.argv) > 3 else "true")
con = duckdb.connect(); con.execute("install spatial; load spatial")
con.execute(f"create table m as select st_makevalid(geom) geom from st_read('{layer}') where {where}")
con.execute(f"create table e as select pin, st_transform(st_point(lon::double, lat::double), 'EPSG:4326', 'EPSG:26915', always_xy := true) g from read_csv_auto('out/{city}/lots.csv', all_varchar=true)")
con.execute(f"create table x as select pin, st_transform(st_point(0,0),'EPSG:4326','EPSG:26915') g from read_csv_auto('out/{city}/excluded.csv', all_varchar=true) limit 0")
inside = con.execute("select count(*) from e where exists (select 1 from m where st_contains(m.geom, e.g))").fetchone()[0]
n = con.execute("select count(*) from e").fetchone()[0]
print(json.dumps({"city": city, "eligible": n, "inside_city_map": inside, "share": round(inside / max(n, 1), 4)}))
