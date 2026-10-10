# Legal Lots

**Live:** https://legal-lots.vercel.app

Every lot in a Minnesota city where a cannabis shop is legally allowed, with who owns it. A $900 report for licence holders still looking for a site.

- `DATA_MODEL.md`: the ideal model, written first, and how reality measures against it.
- `rules/<city>.json`: each city's cannabis zoning ordinance as data, with citations (`research/RULES.md`).
- `scripts/build_city.py <city>` → `out/<city>/lots.csv`: zoning + buffers + location tests over county parcels (bricks GIS DuckDBs).
- `scripts/crosscheck.py`: agreement with the city's own published map.
- `scripts/enrich_owners.py <city>` → `out/<city>/report.csv`: the paid deliverable (owner, mailing address, years held, nearest store).
- `scripts/build_site.py` → `site/`: one page per city + `/for/<token>/` pages. Deploy: `cd site && npx vercel deploy --prod`.
- Buy link: https://buy.stripe.com/eVq4gycto2hP5W663L0Jq3H (Brick & Mortar Stripe, `client_reference_id` = city). Fulfilment is by hand: email `out/<city>/report.csv` to the buyer.
- `research/BUYERS.md`: who buys, and how to find them by name. Outreach ledger: `outreach/`.
