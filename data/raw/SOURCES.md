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
