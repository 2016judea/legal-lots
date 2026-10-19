"""Every number on a city page is read from out/<city>/; pin that the page and its data agree."""
import csv, json, re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
CITIES = json.loads((ROOT / "site_cities.json").read_text())


@pytest.mark.parametrize("slug", list(CITIES))
def test_city_page_headline_matches_the_report(slug):
    rows = list(csv.DictReader(open(ROOT / "out" / slug / "report.csv")))
    lots = {r["pin"] for r in csv.DictReader(open(ROOT / "out" / slug / "lots.csv")) if r["lat"]}
    page = (ROOT / "site" / slug / "index.html").read_text()
    n = sum(1 for r in rows if r["pin"] in lots)
    assert re.search(r"<div class=big>([\d,]+)</div>", page).group(1) == f"{n:,}"
    assert f"<title>{n:,} lots in" in page
    vacant = sum(int(r["vacant"]) for r in rows if r["pin"] in lots)
    assert f"{vacant:,} of them are vacant land" in page


@pytest.mark.parametrize("slug", list(CITIES))
def test_report_is_a_subset_of_the_legal_lots(slug):
    lots = {r["pin"] for r in csv.DictReader(open(ROOT / "out" / slug / "lots.csv"))}
    rows = list(csv.DictReader(open(ROOT / "out" / slug / "report.csv")))
    assert {r["pin"] for r in rows} <= lots
    assert len({r["pin"] for r in rows}) == len(rows)
    for r in rows:
        if r["years_held"]:
            assert 0 <= int(r["years_held"]) < 100, r["pin"]


def test_summary_counts_add_up():
    for slug in CITIES:
        s = json.loads((ROOT / "out" / slug / "summary.json").read_text())
        assert s["in_allowed_district"] == s["excluded_by_buffer"] + s["eligible"], slug
        assert sum(s["by_district"].values()) == s["eligible"], slug


def test_every_page_loads_analytics():
    for p in [ROOT / "site/index.html", *(ROOT / "site" / s / "index.html" for s in CITIES)]:
        h = p.read_text()
        assert "/_vercel/insights/script.js" in h and "posthog.init" in h, p
