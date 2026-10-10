# Raw layer sources

All layers were pulled on 2026-10-10 with `scripts/fetch_arcgis.py <layer> <out>`.
Each request used `f=geojson`, `outSR=26915` and `resultOffset` paging. Output is
**EPSG:26915 (UTM 15N, metres)** unless a row says otherwise. Every file records its
source URL in a top-level `source` member. "Edited" is the layer's ArcGIS
`lastEditDate`.

Base URLs used in the table:

- `MPLS` = https://services.arcgis.com/afSMGVsC7QlRK1kZ/arcgis/rest/services
- `STP` = https://services1.arcgis.com/9meaaHE3uiba0zr8/arcgis/rest/services
- `MNGEO` = https://enterprise.gisdata.mn.gov/aghost/rest/services (gisdata.mn.gov moved to gis.data.mn.gov in 2026)

## Zoning and the cities' own cannabis layers

| file | n | source | edited | notes |
|---|---|---|---|---|
| mpls_primary_zoning.geojson | 1308 | `MPLS/Planning_Primary_Zoning/FeatureServer/0` | 2026-10-02 | `Land_Use_Code` ∈ UN1-3, RM1-3, CM1-4, DT1-2, PR1-2, TR1 |
| mpls_cannabis_permitted_areas.geojson | 159 | `MPLS/Cannabis_Spacing_Requirements_WFL1/FeatureServer/10` "Areas where cannabis related business is permitted" | 2026-06-16 | the city's own answer, a cross-check |
| mpls_cannabis_3acre_commercial.geojson | 159 | same service, layer 9 "3 acres of commercial zoning boundary" | 2026-06-16 | the city's 3-acre contiguity result |
| mpls_cannabis_k12_school_parcels.geojson | 179 | same service, layer 3 "K-12 school" | 2026-06-16 | school **parcels** (PID, address), the polygons the city buffers |
| mpls_cannabis_k12_300ft_buffer.geojson | 179 | same service, layer 0 | 2026-06-16 | the city's 300 ft buffers (`BUFF_DIST`) |
| stp_principal_zoning.geojson | 1092 | `STP/Zoning/FeatureServer/6` | 2026-10-01 | `Zoning` ∈ B1-5, BC, CA, F1-6, H1-2, I1-3, IT, ITM, OS, PD, RL, RM1-3, T1-4, T1M/T3M/T4M, VP |
| stp_cannabis_regulation.geojson | 3 | `STP/CannabisRegulation/FeatureServer/0` (item 4b1265dc3ccf4d4d9267eca071aa5c1e) | 2026-09-17 | `PermittedUse`: Retail (as of **2026-07-15**), Full cultivation/production, Limited (<15,000 sf) |

Overlay districts are not downloaded, because neither ordinance references one. The
Saint Paul downtown exemption is by base district (B4–B5), and Minneapolis has no
downtown exemption. If an overlay is ever needed: Minneapolis is
`MPLS/Planning_Zoning_Overlay/FeatureServer` (12 layers), Saint Paul is
`STP/Zoning/FeatureServer/0-5`.

## Sensitive uses

| file | n | source | as of | notes |
|---|---|---|---|---|
| mn_mde_school_program_locations_sy2025_26.geojson | 5904 statewide (1431 Hennepin + Ramsey) | `MNGEO/us_mn_state_mde/struc_school_program_locs/FeatureServer/0` | SY2025-26 | points. `pubpriv`: Public 5316, Private or Nonpublic 588. Also includes non-K-12 programs (district offices, ECFE, ALC), so filter on `class` / `graderange` before buffering |
| mpls_charter_private_schools.geojson | 39 | `MPLS/Public_Charter_and_Private_Schools/FeatureServer/41` | unknown | points |
| stp_mde_school_parcels_sy2024_25.geojson | 138 | `STP/MDE_Saint_Paul_Schools_List_SY2024_25_Parcels/FeatureServer/0` | 2024-09-25 | school **parcels** (property lines). Saint Paul measures from these |
| stp_schools_points.geojson | 117 | `STP/Schools/FeatureServer/0` | 2024-07-23 | points with `type` and `grade` |
| mn_child_care_mngeo.geojson | 7814 | `MNGEO/us_mn_state_mngeo/econ_child_care/FeatureServer/0` | vintage UNVERIFIED (hub migration 2026-09-17) | **already geocoded** from DHS licensing: Family Child Care 5420, Child Care Center 1792, Certified Center 602. About 670 in Minneapolis and Saint Paul. Not buffered by either city |
| samhsa_sud_treatment_twin_cities.geojson | 148 | SAMHSA FindTreatment export, `https://findtreatment.gov/locator/exportsAsJson/v2?sAddr=44.96,-93.17&limitType=2&limitValue=40000&sType=SA` | 2026-10-10 | **EPSG:4326 lon/lat** (CRS84), not 26915. Federal locator, not the DHS licence list. Minneapolis 64, Saint Paul 44. Not buffered by either city |
| mpls_mprb_parks.geojson | 185 | `MPLS/MPRB_Parks/FeatureServer/29` | | MPRB park polygons |
| stp_city_parks.geojson | 205 | `STP/CityParks/FeatureServer/0` | | has amenity flags (playground, baseball, …) |
| stp_parks_property.geojson | 169 | `STP/saint_paul_parks_property/FeatureServer/0` | | parcel-level park property |
| metc_regional_park_admin_boundaries.geojson | 1601 | `https://arcgis.metc.state.mn.us/data1/rest/services/planning/Regional_Parks_Trails/FeatureServer/0` (2026 annual update) | 2026 | this host serves an incomplete TLS chain, so the fetcher falls back to curl |

**Licensed treatment programs from DHS, needs work.** The DHS Licensing Lookup
(https://licensinglookup.dhs.state.mn.us/, service type 56 "Substance Use Disorder
Treatment", 57 "Withdrawal Management", 39 "Detox") is an ASP.NET postback behind a
Radware captcha, and a scripted POST returns the captcha page. The lookup has a CSV
export, but only after a human search. That CSV has addresses only, so it would need
geocoding. The SAMHSA file above stands in for it. Neither city buffers treatment
facilities, so this layer is context only.

**Existing cannabis retailers.** Don't copy them, reuse
`/Users/aidan/Desktop/bricks/data/outreach/cannabis/mn_retailers.json`: 248 OCM
retailers with `lat`/`lon` (WGS84), 24 in Minneapolis and 16 in Saint Paul. Neither
city has a spacing rule. `MPLS/Existing_cannabis_retail` is a 2023 delta-9 snapshot
and was not used.

**Gap: building footprints.** Saint Paul measures to the shop's *principal
structure*, so an exact answer needs footprints. No Ramsey or Saint Paul footprint
service was found on the city org or the state hub. Candidates are Microsoft US
Building Footprints (MN) and OSM. Until one is loaded, use the parcel polygon, which
is conservative.

## Parcel owner mailing addresses (not bulk-downloaded)

The parcels on disk (`bricks/data/{hennepin,ramsey}_gis.duckdb`, table `parcels`) join
on `pin`.

**Hennepin.** Service:
`https://gis.hennepin.us/arcgis/rest/services/HennepinData/LAND_PROPERTY/MapServer/1`
("County Parcels"). Join on `PID` (13 chars, the same as `pin`).

- Owner: `OWNER_NM`.
- Mailing block: `TAXPAYER_NM`, `TAXPAYER_NM_1`, `TAXPAYER_NM_2`, `TAXPAYER_NM_3`.
  This is a free-form, space-padded address block. Name lines come first, then the
  street, then "CITY ST ZIP", and the number of name lines varies. Example:
  `KATHERINE ZOBRO` / `ARTHUR DANIELS` / `3033 29TH AVE S` / `MINNEAPOLIS MN 55406`.
- Also present: `MAILING_MUNIC_NM`, `ZIP_CD`, `MUNIC_NM`, `PR_TYP_NM1`, `LAT`, `LON`.
- Query by `PID IN (...)` for candidate lots only.

**Ramsey.** Service:
`https://maps.co.ramsey.mn.us/arcgis/rest/services/ParcelData/AttributedData/MapServer/0`
("Parcels MultiUse"). Join on `ParcelID` (12 chars, the same as `pin`).

- Owner: `OwnerName`, `OwnerName1`, `OwnerName2`, `OwnerAddress1`, `OwnerAddress2`,
  `OwnerCityStateZIP`.
- Tax mailing: `TaxName1`, `TaxName2`, `TaxAddress1`, `TaxAddress2`,
  `TaxCityStateZIP`. These are structured fields.
- Also present: `BusinessSquareFeet`, `LandUseCodeDescription`, `LastSaleDate`,
  `SalePrice`, `EMVTotal`.
- Filter by `SiteCityName='SAINT PAUL'`.

## Ordinance text

Code text was read through the Municode API with `scripts/fetch_municode.py`:

- Minneapolis: productId 11490, job 492538.
- Saint Paul: productId 10061, job 495421.
- Statute: https://www.revisor.mn.gov/statutes/cite/342.13

Quotes are in `research/RULES.md`.

## South metro: Cottage Grove, Apple Valley, Burnsville, Bloomington (added 2026-10-10)

Pulled 2026-10-10 with `scripts/fetch_arcgis.py` (EPSG:26915) unless noted. The three
parcel-based zoning layers were trimmed to the fields listed after download (the raw
layers carry owner and tax fields we already have in the bricks DuckDBs) and rounded
to 1 cm.

| file | n | source | edited | notes |
|---|---|---|---|---|
| cottage_grove_zoning_parcels.geojson | 16712 | `https://services9.arcgis.com/6YdigEOr80Ix0KD7/arcgis/rest/services/CGMN_Parcels/FeatureServer/0` ("Interactive_Zoning_Parcels_AGOL", city org cottagegrove_enterprise) | 2026-08 | `CurrentZoning` e.g. "M-U, Mixed Use"; the build takes the code before the comma. The org's `Zoning` (2022) and `Zoning_Districts` (2019) layers are older and were not used |
| cottage_grove_parks.geojson | 90 | same org, `Park_and_Open_Space/FeatureServer/0` | 2019-06 | park polygons, used only to clip OSM attractions |
| apple_valley_zoning_parcels.geojson | 16816 | `https://utility.arcgis.com/usrsvcs/servers/ee5041371142495abfc8d90b5ceede15/rest/services/CommDev/Revised_Zoning_Layers/FeatureServer/3` (behind the city's "Interactive Zoning Map", webmap e1b4c251768947bba244de1c91419b6e) | | `ZONING`, and for PD parcels `PDNUMBER` + `PDZONE`. The `Apple_Valley_Zoning_*` services on ArcGIS Online are Apple Valley **Utah/California**, not this city |
| apple_valley_parks.geojson | 55 | `https://services6.arcgis.com/kIEwMUNW6ZLWUVjA/arcgis/rest/services/Apple_Valley_Parks/FeatureServer/0` | | park polygons |
| dakota_parks.geojson | 564 | `https://gis2.co.dakota.mn.us/arcgis/rest/services/DCGIS_OL_ParksRecreation/MapServer/12` | | city + county park polygons (layer 11 is the same data) |
| burnsville_zoning_parcels.geojson | 19534 | `https://utility.arcgis.com/usrsvcs/servers/7a30d56d428a43db90b37644be6f0e90/rest/services/Planning/Zoning_FloodZones_Viewer/MapServer/4` (city "Zoning Lookup") | | `ZONING` codes without hyphens (B3, MIX, TOD, B4-GW = B-4 in the Gateway overlay) |
| bloomington_zoning.geojson | 440 | `https://gis.bloomingtonmn.gov/arcgis/rest/services/ComDev/PlanningPublic/MapServer/77` "Zoning Areas" | | `designation` |
| bloomington_cannabis_school_parcels.geojson | 23 | `https://services6.arcgis.com/eXHnzGr3m1c2gSiA/arcgis/rest/services/Cannabis_License_Location_Map_WFL1/FeatureServer/2` | 2024-08-02 | the city's own school parcels ("Proposed restrictions" map) |
| bloomington_cannabis_res_treatment.geojson | 2 | same service, layer 16 | 2024-08-02 | residential treatment parcels |
| bloomington_cannabis_park_attractions.geojson | 293 | same service, layer 11 "Attractions20240422" | 2024-08-02 | park attraction polygons |
| ocm_retail_sites_south_metro.geojson | 266 | `scripts/prep_ocm_sites.py`: OCM licensed list (2026-10-05 xlsx) → US Census batch geocoder, county-parcel address fallback | 2026-10-05 | 20 cannabis retail + 246 LPHE retail sites in/near the four cities. 15 unmatched (none in Cottage Grove or Apple Valley; the one near Cottage Grove is a Hastings Holiday on Point Douglas Dr); listed in the file's `unmatched` |
| osm_park_attractions_south_metro.geojson | 1408 | `scripts/prep_south_metro.py`: OpenStreetMap (Overpass, ODbL) playgrounds, pitches, tracks, shelters, toilets, picnic tables, disc golf, clipped to the park polygons above + Met Council regional parks | 2026-10-10 | raw Overpass answer cached in `osm_cache/attractions.json` |
| osm_bloomington_highway_barriers.geojson | 276 | same script, OSM motorway/trunk ways ref I 494, I 35W, MN 77 | 2026-10-10 | Bloomington s.14.280(c) "Measurements shall not extend across" these |
| samhsa_residential_south_metro.geojson | 4 | same script, findtreatment.gov exportsAsJson v2, MH + SA, residential settings within 12 km of Cottage Grove and Apple Valley | 2026-10-10 | **EPSG:26915**. Stand-in for the DHS list (captcha) |

Ordinance text for these cities was read in a headless browser (amlegal answers curl
with a Cloudflare challenge; Burnsville's iCompass content endpoint answers curl with
"Unauthorized") and saved verbatim under `data/raw/ordinances/`:

- Cottage Grove: amlegal `cottagegrovemn`, s.11-4-18 (node 0-0-0-8583) and the s.11-8-2 business-district use table (node 0-0-0-6909).
- Apple Valley: amlegal `applevalley`, s.155.320 (0-0-0-44372), ch.121 (0-0-0-43575), ch.155 App. F planned-development designations (0-0-0-17783; our PD-R reading in `apple_valley_pd_r_zones.json`). The city also posts a "Cannabis Buffer Map" PDF at https://www.applevalleymn.gov/DocumentCenter/View/21067/Cannabis-Buffer-Map (not used).
- Burnsville: https://burnsville.municipalcodeonline.com, 10-7-53 (zoning table 10-7-53-5) and ch.3-10.
- Bloomington: amlegal `bloomington`, s.21.302.22 (0-0-0-110996), s.14.276-14.286 Division L (0-0-0-98344), s.21.209 use tables (0-0-0-109730), s.21.205.06-08 and s.21.207.03.
