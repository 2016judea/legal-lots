# Where a cannabis shop may legally open: Minneapolis and Saint Paul

Researched 2026-10-10. Every quote is copied from the codified text. Municode was read
through its public API (`scripts/fetch_municode.py`), not from a summary.

- **Minneapolis:** Code of Ordinances, Supp. 73 Update 1, *"Codified through
  Ordinance No. 2026-020, adopted June 25, 2026."* Web:
  https://library.municode.com/mn/minneapolis/codes/code_of_ordinances (Title 20, Zoning Code).
- **Saint Paul:** Legislative Code, Supp. 133 Update 1, *"Codified through
  Ordinance No. 26-26, adopted May 13, 2026."* Web:
  https://library.municode.com/mn/st._paul/codes/code_of_ordinances (Title VIII, Zoning Code).
- **State:** Minn. Stat. § 342.13, https://www.revisor.mn.gov/statutes/cite/342.13

Machine-readable versions: `rules/minneapolis.json` and `rules/saint-paul.json`.

---

## The answer, one table

| | Minneapolis | Saint Paul |
|---|---|---|
| Retail allowed in | CM2, CM3, CM4, DT1, DT2, PR1 (PR1 capped at 5,000 sf) | T2, T3, T4, B1, BC, B2, B3, B4, B5, IT, I1, I2, F2–F6 |
| Micro/mezzo with retail endorsement | Same districts, plus PR2 when the shop is **accessory** to cultivation or manufacturing (≤5,000 sf) | Same as retail. The city layer says so directly |
| School buffer | 300 ft from K-12, **lot line to lot line** → whole lot out if any part is inside | 300 ft from primary/secondary school, **school property line → principal structure of the shop**. Not applied in B4–B5 (downtown) |
| Daycare / treatment / park buffers | None | None |
| Other location test | Must sit inside a **contiguous ≥3-acre** block of dispensary-permitting districts | None |
| Spacing between shops | None (the 300 ft spacing rule was struck by amendment) | None |
| Cap on registrations | None in code | *"There is no limit"* (§ 420.03(a)) |
| Discretionary approval | None. A permitted use with a zoning permit | CUP only for new construction covering >15,000 sf of land (not in industrial districts) |

---

## Minneapolis

Adopted as Ord. No. 2024-041 on 10-31-2024 (council vote 12–1), signed 11-05-2024,
effective 11-09-2024 (city page:
https://www.minneapolismn.gov/business-services/planning-zoning/amendments/proposed-adopted/cannabis/).
Registration chapter 355 came later, by Ord. No. 2025-017 on 4-17-2025.

### Districts: Table 545-1, § 545.100

Columns: UN1 UN2 UN3 RM1 RM2 RM3 CM1 **CM2 CM3 CM4 DT1 DT2 PR1** PR2 TR1. The row reads:

> Cannabis dispensary | | | | | | | | P | P | P | P | P | 5P | | | X+

The blank cells are UN1–CM1. CM2, CM3, CM4, DT1 and DT2 are "P". PR1 is "5P". PR2
and TR1 are blank.

§ 545.20(d) defines the number: *"The number preceding a "P" or "C" in the use table
indicates the maximum gross floor area for that use in that district in multiples of
one thousand (1,000) square feet."* That makes the PR1 limit **5,000 sf**.

§ 545.20(b) says a "P" use is *"permitted as of right … Persons wishing to establish
a permitted use shall obtain a zoning permit."* There is no conditional use permit.

The GIS layer uses the same codes. `Land_Use_Code` in `mpls_primary_zoning.geojson`
holds exactly CM1 CM2 CM3 CM4 DT1 DT2 PR1 PR2 RM1 RM2 RM3 TR1 UN1 UN2 UN3.

### Specific use standards: § 545.210(f)(3), "Cannabis dispensary"

> a. The use shall be located at least three hundred (300) feet from a school, grades K-12.
> b. The use shall be located within a contiguous commercial or industrial area of at least three (3) acres. The minimum acreage required shall be comprised of contiguous zoning districts where a dispensary is a permitted principal use.
> c. The use shall only be allowed as a principal use unless accessory to a cannabis cultivation use or a cannabis manufacturing use.
> d. The use shall not share a common entrance with any use that is not a cannabis business.
> e. The use shall submit an odor control and air filtration plan. …

### How distance is measured: § 520.160(11)

> Distance shall be measured in a straight line, from lot line to lot line, except as otherwise provided in this zoning ordinance.

§ 545.210 provides nothing otherwise. So the test runs from the dispensary lot's line
to the school lot's line, and **a lot fails if any part of it is within 300 ft of a
school lot**. That matches the plan's "whole lot out" reading.

### Micro and mezzo businesses

§ 565.40 says the zoning code regulates the activity on the land, not the state
licence: *"For zoning purposes, "cannabis business" pertains to the land use activity at
a site, not the state-issued license. Such businesses are subject to the specific use
standards found in Chapter 545, Article II, Specific Use Standards, which apply to each
use occurring on the property."* A micro or mezzo with a retail endorsement is
therefore a dispensary use plus a manufacturing and/or cultivation use, and each use
has to be allowed on its own.

- Manufacturing ("Cannabis and lower-potency hemp edible manufacturing", Table 545-1)
  is P in CM2, CM3, CM4, DT1, DT2, PR1 and PR2. § 545.230 then adds conditions:
  *"In the CM2 and CM3 Districts, the main entrance shall open into a cannabis
  dispensary … equal to not less than fifteen (15) percent of the floor area"*. In
  CM4, DT1 and DT2 that share is 30 percent. *"Except in the PR1 and PR2 Districts,
  the portion of the use dedicated to production … shall not exceed five thousand
  (5,000) square feet."*
- Cultivation ("Urban farm") is P in PR1 and PR2 only. § 545.630 also allows it
  *"accessory to a cannabis manufacturing use only in the production districts."*
- Accessory dispensary, § 545.450: *"Cannabis dispensaries shall be allowed accessory
  to urban farm uses that cultivate cannabis and to cannabis and lower-potency hemp
  edible manufacturing … In the production districts, a cannabis dispensary shall not
  exceed five thousand (5,000) square feet of the floor area of the use."*
- A 2026 CPED ordinance interpretation, as summarised on the city page: accessory
  dispensaries *"can be accessory to cannabis cultivation or manufacturing uses in the
  PR2 District. They must follow the three-acre contiguous acreage rule."*

Net effect: a micro or mezzo shopfront may go in CM2, CM3, CM4, DT1, DT2 or PR1, under
the same tests as a retailer. It may also go in **PR2** when it is accessory to
on-site cultivation or manufacturing, capped at 5,000 sf, and still subject to the
300 ft and 3-acre tests.

### Spacing between shops

None. The August 2024 draft had *"Five hundred (500) feet from an existing dispensary,
except: In the downtown (DT1 and DT2)"* (public information session deck,
https://www.minneapolismn.gov/media/-www-content-assets/documents/planning-and-zoning/Adult-Use-Cannabis-Amendment-Public-Information-Session.pdf).
The adopted § 545.210(f)(3) contains no spacing clause. KSTP reported that *"an
amendment introduced by Council Member Aurin Chowdhury … did away with a proposed
300-foot buffer between dispensaries"*
(https://kstp.com/kstp-news/local-news/minneapolis-sets-cannabis-business-zoning-rules-including-contiguous-commercial-requirement/).

### Cap and registrations

Chapter 355, "Local Registration of Selected State-Licensed Cannabis and Hemp
Retailers", sets no number limit. § 355.20(a) requires registration for *"cannabis
microbusiness with a retail operations endorsement, cannabis mezzobusiness with a
retail operations endorsement, cannabis retailer, medical cannabis retailer, medical
cannabis combination business, or lower-potency hemp edible retailer."* The 2024 draft
deck said *"No license caps."* KSTP noted the state floor would require *"at least 34
dispensaries"* (1 per 12,500 residents) if a cap were ever adopted.

### The city's own map

The city publishes a layer called Cannabis_Spacing_Requirements_WFL1, last edited
2026-06-16. It has "Areas where cannabis related business is permitted" (159
polygons, CM2–PR1), "3 acres of commercial zoning boundary", "K-12 school" (179 school
parcels) and "300 fee[t] from K-12 school". Viewer:
https://cityoflakes.maps.arcgis.com/apps/instant/basic/index.html?appid=127b5782076c4119bebd89bc3040c5d4.
Its caveat: *"Applicants should not rely on this map alone for land use
verification."* Treat the layer as a cross-check on our own computation, not as the
source of truth.

---

## Saint Paul

Zoning text: Ord 24-21, 9-18-24 (unanimous). Registration chapter 420: Ord. No.
25-66, 11-19-25.

### Districts: use tables

`Cannabis retail` row in each use table:

| Table | Columns | Row |
|---|---|---|
| 66.321 Traditional neighborhood | T1 T2 T3 T4 | – P/C P/C P/C |
| 66.421 Business | OS B1 BC B2 B3 B4 B5 | – P/C P/C P/C P/C P/C P/C |
| 66.521 Industrial | IT I1 I2 I3 | P P P – |
| 66.921 Ford | F1 F2 F3 F4 F5 F6 | – P/C P/C P/C P/C P/C |

Residential districts (66.221) do not allow it. "P/C" means permitted, with the CUP
trigger in § 65.511(a).

### Standards: § 65.511, "Cannabis retail"

> A cannabis business with a license or endorsement authorizing the retail sale of cannabis flower, plants, cannabis products, and lower-potency hemp products, including cannabis products sold for on-site consumption.
> (a) Except in industrial districts, a conditional use permit is required for new construction covering more than fifteen thousand (15,000) square feet of land to ensure size and design compatibility with the location.
> (b) Except in B4—B5, cannabis businesses with a retail license or a cannabis retail endorsement shall be located a minimum distance of three hundred (300) feet from any primary and secondary school, measured from the property line of the school to the principal structure of the cannabis retail business.
> (c) [24/7 CCTV]
> (d) A cannabis retail use is prohibited from sharing a common entrance with a business licensed as a tobacco products shop.

**Measurement.** The distance runs from the school's property line to the shop's
**building**, not its lot. A lot that is partly inside the 300 ft ring can still pass
if the principal structure sits outside it. Computing that exactly needs building
footprints. Using the parcel polygon instead is conservative: it only ever turns a
yes into a no.

**Downtown exemption.** The school buffer does not apply in B4 or B5.

**Micro and mezzo.** The definition covers *"a license or endorsement authorizing the
retail sale"*, and § 65.511(b) names *"a cannabis retail endorsement"*. The city's
CannabisRegulation layer
(https://services1.arcgis.com/9meaaHE3uiba0zr8/arcgis/rest/services/CannabisRegulation/FeatureServer/0,
item 4b1265dc3ccf4d4d9267eca071aa5c1e) states that its Retail polygon *"shows locations
that will allow businesses with a cannabis retail license or a micro/mezzo business
license with a retail endorsement can operate. … The "Retail" category is currently
accurate as of July 15th, 2026."* On-site production adds its own district test.
Limited production and processing covers up to 15,000 sf of cannabis
cultivation/manufacturing (§ 65.780(3)) and is allowed in T2–T4, B3, B5, IT, I1, I2
and F3–F6. The layer also has a "Limited cultivation or production (under 15,000 sq
ft)" polygon.

### Daycares, youth centers, parks

**None in the code.** § 65.511 names schools only. The belief from Fox9 coverage that
Saint Paul buffers daycares and youth centers is not in the codified text (Supp. 133,
current through May 2026). Mark that belief UNVERIFIED-and-contradicted. The 2024
Early Notification System document
(https://stpaul.gov/sites/default/files/2024-08/Cannabis_ENS.pdf) may have proposed
more buffers before adoption.

### Cap and registrations

§ 420.03(a): *"No registration limits. There is no limit on the total number of
registrations issued to retailers by the City."* § 420.01 covers micro and mezzo
businesses with retail endorsements, cannabis retailers, medical combination retail
and LPHE retailers. § 420.03(b)(3) requires the parcel ID, plus a lease or purchase
agreement when the applicant does not own the premises. § 420.03(d) has the city
certify zoning compliance to OCM. Hours (§ 420.06): 8am–10pm Monday to Saturday,
11am–6pm Sunday.

---

## State floor: Minn. Stat. § 342.13

History line: 2023 c 63 art 1 s 13; 2024 c 121 art 2 s 64; 2025 c 31 s 41.

> (c) … A local unit of government may prohibit the operation of a cannabis business within 1,000 feet of a school, or 500 feet of a day care, residential treatment facility, or an attraction within a public park that is regularly used by minors, including a playground or athletic field.
> (h) A local government unit that issues a cannabis retailer registration under section 342.22 may, by ordinance, limit the number of licensed cannabis retailers, cannabis mezzobusinesses with a retail operations endorsement, and cannabis microbusinesses with a retail operations endorsement to no fewer than one registration for every 12,500 residents.

Those are **ceilings on what a city may impose**. Both cities chose much less: 300 ft,
schools only. § 342.13(f): *"The office may not issue a license if the local unit of
government informs the office that the cannabis business does not meet local zoning
and land use laws."* That makes the city zoning certification the gate.

The OCM summary of the 2026 session (`data/raw/OCM_2026_Legislative_Changes_Ch342.pdf`,
placed by another session) does not mention new buffer rules. Two of its changes
matter to buyers: preliminary approvals get an automatic 6-month extension plus a
second discretionary 6-month extension, and new retailer and mezzo licence windows
move up to July 1, 2027.

---

## UNVERIFIED

1. **Mpls: how PR2 acreage counts toward the 3-acre test** for an accessory
   dispensary. § 545.210(f)(3)(b) counts only *"districts where a dispensary is a
   permitted principal use"*, and PR2 is not one. The 2026 CPED interpretation says
   PR2 accessory shops *"must follow"* the rule, but we have not read its text. It
   was not found online. Ask a planner via 311.
2. **Mpls: whether "contiguous" bridges streets.** The city's 3-acre layer (159
   polygons) is the operative reading. We have not confirmed whether
   right-of-way between two zoned blocks breaks contiguity. Compare our computation
   to layer 9.
3. **Mpls: what counts as a "school, grades K-12".** Undefined in § 545.210. The
   city's layer has 179 school parcels. It is not confirmed whether that includes
   private and charter schools or school-district offices.
4. **Saint Paul: "primary and secondary school".** Not confirmed against the
   § 65.xxx definition. The city layer uses the MDE SY2024-25 participating-schools
   list, 138 parcels.
5. **Saint Paul: master-plan districts T1M–T4M and ITM.** They take the base
   T/IT use table, but an adopted master plan *"may include additional regulations"*
   (§ 66.344). Treat as allowed and flag each one.
6. **Saint Paul: PD, CA and VP districts** are not in the four use tables. PD
   (planned development) follows its own plan. CA (Capitol Area) is zoned by the
   state CAAPB. Treat as excluded and flag.
7. **Fox9 report of daycare and youth-center buffers in Saint Paul.** Contradicted by
   codified § 65.511. Any amendment after Ord. 26-26 (May 2026) is not checked.
8. **Registrations issued.** Neither city publishes a list we could find, so there is
   no cap to exhaust. As a proxy, `bricks/data/outreach/cannabis/mn_retailers.json`
   (OCM-licensed retailers) has **24 in Minneapolis and 16 in Saint Paul**.
9. **§ 342.13 after the 2026 session.** The revisor history ends at 2025 c 31. The
   2026 omnibus bill may not yet be shown there.
10. **Mpls LIMS file 2024-00947** (ordinance as amended and staff report) sits behind
    Cloudflare and could not be fetched. The codified text was used instead.
