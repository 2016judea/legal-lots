"""Static site: one page per city, plus per-recipient /for/<token>/ pages.

    python3 scripts/build_site.py

Free on the page: every legal storefront lot on a map and in a list, with zoning,
lot size and years held. Paid ($900, Stripe): the same list with owner of record
and mailing address, as CSV. Every number on a page is read from out/<city>/.
"""
import csv, html, json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "site"
BUY = "https://buy.stripe.com/eVq4gycto2hP5W663L0Jq3H"
TRACK = (SITE / "reader_events.js").read_text()
CITIES = json.loads((ROOT / "site_cities.json").read_text())

CSS = """
:root{--bg:#f7f5f0;--paper:#fff;--ink:#16202a;--ink2:#56606b;--rule:#ddd8cc;--go:#1d6b45;--go-soft:#dcefe4;--accent:#b8461b}
@media (prefers-color-scheme:dark){:root:not([data-theme=light]){--bg:#11171d;--paper:#18212a;--ink:#edf0f2;--ink2:#a5aeb8;--rule:#2d3944;--go:#6fd39a;--go-soft:#1c3a2a;--accent:#ff8a5c}}
:root[data-theme=dark]{--bg:#11171d;--paper:#18212a;--ink:#edf0f2;--ink2:#a5aeb8;--rule:#2d3944;--go:#6fd39a;--go-soft:#1c3a2a;--accent:#ff8a5c}
*{box-sizing:border-box}html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--bg);color:var(--ink);font:17px/1.5 -apple-system,BlinkMacSystemFont,"Segoe UI",system-ui,sans-serif}
.wrap{max-width:860px;margin:0 auto;padding:0 16px 56px}
h1{font-size:clamp(28px,7vw,44px);line-height:1.08;letter-spacing:-.02em;margin:28px 0 10px}
h2{font-size:22px;margin:30px 0 8px}
p{margin:0 0 12px;max-width:62ch}.muted{color:var(--ink2)}
a{color:var(--accent)}
.big{font-size:clamp(56px,16vw,96px);font-weight:800;line-height:1;letter-spacing:-.03em;color:var(--go)}
.buy{display:block;text-align:center;background:var(--go);color:#fff;text-decoration:none;font-weight:700;padding:15px 18px;border-radius:12px;margin:18px 0 6px;font-size:18px}
@media (prefers-color-scheme:dark){:root:not([data-theme=light]) .buy{color:#0d1a12}}
#map{height:46vh;min-height:280px;border:1px solid var(--rule);border-radius:12px;margin:16px 0}
.cities{display:grid;gap:10px;margin:18px 0}
.cities a{display:flex;justify-content:space-between;align-items:baseline;padding:14px 16px;background:var(--paper);border:1px solid var(--rule);border-radius:12px;text-decoration:none;color:var(--ink);font-weight:600}
.cities b{color:var(--go);font-size:20px}
.filters{display:flex;gap:8px;flex-wrap:wrap;margin:8px 0}
.chip{border:1px solid var(--rule);background:var(--paper);color:var(--ink);border-radius:999px;padding:7px 12px;font-size:15px}
.chip[aria-pressed=true]{background:var(--go-soft);border-color:var(--go);color:var(--go)}
input[type=search]{width:100%;font-size:16px;padding:11px 12px;border:1px solid var(--rule);border-radius:10px;background:var(--paper);color:var(--ink);margin:8px 0}
.list{list-style:none;padding:0;margin:8px 0}
.list li{padding:11px 0;border-bottom:1px solid var(--rule);display:grid;grid-template-columns:minmax(0,1fr) auto;gap:4px 10px}
.list .a{font-weight:600}.list .m{color:var(--ink2);font-size:14px;grid-column:1/-1}
.lock{color:var(--ink2);font-size:14px}
.note{background:var(--paper);border:1px solid var(--rule);border-left:4px solid var(--go);border-radius:8px;padding:12px 14px;margin:16px 0}
.more{display:block;margin:10px auto;padding:10px 16px}
footer{margin-top:40px;color:var(--ink2);font-size:14px}
"""

HEAD = """<!doctype html><html lang=en><head><meta charset=utf-8>
<meta name=viewport content="width=device-width,initial-scale=1">
<title>{title}</title><meta name=description content="{desc}">
<meta property=og:title content="{title}"><meta property=og:description content="{desc}">
<style>{css}</style>{extra}</head><body>
<script defer src="/_vercel/insights/script.js"></script>
<script>{track}</script>
"""

FOOT = """<footer>Built by Aidan Jude at <a href="https://brickandmortar.dev">Brick &amp; Mortar</a> from public county parcel records and each city's own zoning code.
Not legal advice: confirm a lot with the city's planner before you sign anything. <a href="mailto:aidan@brickandmortar.dev">aidan@brickandmortar.dev</a></footer>"""


def tidy(a):
    """'1 26TH AVE N E' -> '1 26th Ave NE'; placeholder addresses -> ''."""
    a = (a or "").strip()
    if not a or "PENDING" in a.upper() or a.split()[0] == "0":
        return ""
    out = []
    for w in a.split():
        u = w.upper()
        if u in ("N", "S", "E", "W", "NE", "NW", "SE", "SW"):
            out.append(u)
        elif w[:1].isdigit():
            out.append(w.lower())
        else:
            out.append(w.capitalize())
    return re.sub(r"\b(N|S) (E|W)$", r"\1\2", " ".join(out))


def load(slug):
    rows = list(csv.DictReader(open(ROOT / "out" / slug / "report.csv")))
    lots = list(csv.DictReader(open(ROOT / "out" / slug / "lots.csv")))
    ll = {r["pin"]: (round(float(r["lat"]), 5), round(float(r["lon"]), 5)) for r in lots if r["lat"]}
    summary = json.loads((ROOT / "out" / slug / "summary.json").read_text())
    rules = json.loads((ROOT / "rules" / f"{slug}.json").read_text())
    return rows, ll, summary, rules


def rule_sentence(rules):
    bits = []
    for b in rules["buffers"]:
        what = b["sensitive_type"].replace("_", " ").replace("k12", "K-12").replace("primary secondary", "K-12")
        ex = f" (downtown {', '.join(b['exempt_districts'])} exempt)" if b.get("exempt_districts") else ""
        bits.append(f"{b['distance_ft']:,} ft from a {what}{ex}")
    for t in rules.get("location_tests") or []:
        if t["type"] == "contiguous_area":
            bits.append(f"inside a {t['min_acres']}-acre block zoned for dispensaries")
    zones = ", ".join(rules["allowed_districts"]["retail"])
    return f"zoned {zones}; " + "; ".join(bits)


def city_page(slug, meta, rows, ll, summary, rules, hero=None):
    pts = []
    for r in rows:
        if r["pin"] not in ll:
            continue
        la, lo = ll[r["pin"]]
        pts.append([la, lo, tidy(r["address"]) or f"Parcel {r['pin']} (no street address)", r["zoning"], int(float(r["lot_sqft"] or 0)),
                    int(r["years_held"]) if r["years_held"] else None,
                    int(r["vacant"])])
    pts.sort(key=lambda p: (p[2].startswith("Parcel "), not 2500 <= p[4] <= 40000, -(p[5] or 0)))
    n = len(pts)
    vacant = sum(p[6] for p in pts)
    long_held = sum(1 for p in pts if p[5] and p[5] >= 20)
    title = f"{n:,} lots in {meta['name']} where a cannabis shop is legal"
    desc = f"Every commercial lot in {meta['name']} that passes the city's cannabis zoning, with who owns it."
    extra = ('<link rel=stylesheet href="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.css">'
             '<script src="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.js"></script>')
    xc = meta.get("crosscheck")
    cross = (f" We checked our answer against the city's own published map: {xc} of our lots fall inside it." if xc else "")
    body = f"""<div class=wrap>
{hero or ''}
<h1>{html.escape(meta['name'])}: where a cannabis shop can legally open</h1>
<div class=big>{n:,}</div>
<p><b>commercial and industrial lots</b> pass {html.escape(meta['name'])}'s cannabis zoning today. {vacant:,} of them are vacant land. {long_held:,} have had the same owner for 20 years or more.</p>
<a class=buy href="{BUY}?client_reference_id={slug}">Get all {n:,} with owner names and mailing addresses: $900</a>
<p class="muted" style="text-align:center;font-size:14px">A spreadsheet, delivered by email within two business days.</p>
<div id=map role=img aria-label="Map of legal lots"></div>
<div class=filters aria-label=filter>
<button class=chip aria-pressed=true data-f=all>All</button>
<button class=chip aria-pressed=false data-f=vacant>Vacant land</button>
<button class=chip aria-pressed=false data-f=held>Owner 20+ years</button>
<button class=chip aria-pressed=false data-f=big>Lot over 10,000 sq ft</button>
</div>
<input type=search id=q placeholder="Search a street" aria-label="Search a street">
<ul class=list id=list></ul>
<button class="chip more" id=more>Show more</button>
<div class=note><b>How we decided.</b> A lot counts if it is {html.escape(rule_sentence(rules))}, measured property line to property line. Rules from {html.escape(rules['ordinance']['number'])}, read from the city code on {rules['as_of']}.{cross}</div>
<h2>What the $900 list adds</h2>
<p>For each lot: the owner of record, where the county mails their tax bill (the address you write to), building and lot size, what it was last valued at, how long they've owned it, and the nearest open cannabis store. Sort it any way you like.</p>
<a class=buy href="{BUY}?client_reference_id={slug}">Get the {meta['name']} list: $900</a>
{FOOT}
</div>
<script>
var P={json.dumps(pts, separators=(',', ':'))};
var f='all',q='',shown=40;
var map=L.map('map',{{scrollWheelZoom:false}});
L.tileLayer('https://tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png',{{attribution:'© OpenStreetMap',maxZoom:19}}).addTo(map);
var layer=L.layerGroup().addTo(map);
function ok(p){{if(f=='vacant'&&!p[6])return false;if(f=='held'&&!(p[5]>=20))return false;if(f=='big'&&p[4]<10000)return false;return !q||p[2].toLowerCase().indexOf(q)>=0}}
function draw(){{layer.clearLayers();var s=P.filter(ok),b=[];
s.forEach(function(p){{L.circleMarker([p[0],p[1]],{{radius:4,weight:0,fillOpacity:.75,fillColor:'#1d6b45'}}).bindPopup(p[2]+'<br>'+p[3]+' · '+p[4].toLocaleString()+' sq ft lot').addTo(layer);b.push([p[0],p[1]])}});
if(b.length)map.fitBounds(b,{{padding:[16,16],maxZoom:16}});
var ul=document.getElementById('list');ul.innerHTML='';
s.slice(0,shown).forEach(function(p){{var li=document.createElement('li');
li.innerHTML='<span class=a></span><span>'+p[3]+'</span><span class=m></span>';
li.querySelector('.a').textContent=p[2];
li.querySelector('.m').textContent=p[4].toLocaleString()+' sq ft lot'+(p[6]?' · vacant':'')+(p[5]!=null?' · same owner '+p[5]+' yrs':'')+' · owner: in the full list';
li.onclick=function(){{map.setView([p[0],p[1]],17)}};ul.appendChild(li)}});
document.getElementById('more').style.display=s.length>shown?'block':'none'}}
document.querySelectorAll('[data-f]').forEach(function(b){{b.onclick=function(){{f=b.dataset.f;shown=40;document.querySelectorAll('[data-f]').forEach(function(x){{x.setAttribute('aria-pressed',x===b)}});draw()}}}});
document.getElementById('q').oninput=function(e){{q=e.target.value.toLowerCase();shown=40;draw()}};
document.getElementById('more').onclick=function(){{shown+=60;draw()}};
draw();
</script></body></html>"""
    return HEAD.format(title=html.escape(title), desc=html.escape(desc), css=CSS, extra=extra, track=TRACK) + body, n


def main():
    counts = {}
    for slug, meta in CITIES.items():
        rows, ll, summary, rules = load(slug)
        page, n = city_page(slug, meta, rows, ll, summary, rules)
        counts[slug] = n
        d = SITE / slug
        d.mkdir(exist_ok=True)
        (d / "index.html").write_text(page)
    # per-recipient pages: their own record first, then their city's page
    for tok, r in json.loads((ROOT / "recipients.json").read_text()).items():
        slug = r["city"]
        rows, ll, summary, rules = load(slug)
        hero = f'<div class=note style="border-left-color:var(--accent)">{r["hero_html"]}</div>'
        page, _ = city_page(slug, CITIES[slug], rows, ll, summary, rules, hero=hero)
        page = page.replace("<head>", "<head><meta name=robots content=noindex>", 1)
        d = SITE / "for" / tok
        d.mkdir(parents=True, exist_ok=True)
        (d / "index.html").write_text(page)
    items = "".join(f'<a href="/{s}/">{html.escape(m["name"])} <b>{counts[s]:,}</b></a>' for s, m in CITIES.items())
    home = HEAD.format(title="Legal Lots", desc="Every lot in your city where a cannabis shop is legal, and who owns it.",
                       css=CSS, extra="", track=TRACK) + f"""<div class=wrap>
<h1>Every lot in your city where a cannabis shop is legal, and who owns it.</h1>
<p class=muted>For Minnesota licence holders still looking for a site. Pick your city.</p>
<div class=cities>{items}</div>
<p class=muted>Your city not here? <a href="mailto:aidan@brickandmortar.dev?subject=Legal%20Lots%20city%20request">Tell me which one</a> and I'll build it.</p>
{FOOT}</div></body></html>"""
    (SITE / "index.html").write_text(home)
    print(json.dumps(counts))


if __name__ == "__main__":
    main()
