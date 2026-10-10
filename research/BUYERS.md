# Legal Lots — who buys, and how to find them by name

Researched 2026-10-10. Every claim carries its URL. Files cited as `data/raw/...` are in
`/Users/aidan/Desktop/legal-lots/data/raw/`.

## The answer first

- **OCM does not publish names of preliminarily approved applicants.** It publishes names only once a
  business is *licensed*. But the statute makes the names, designated address and application status of
  every applicant **public data** (Minn. Stat. 342.20 subd. 2, as amended 2026 c.123 s.30), so a
  **data practices request to OCM** returns the list we want. That request is the real channel.
- **The pool is big:** as of May 11, 2026, 1,344 cannabis applicants held preliminary approval and 546 were
  "qualified", against 209 licences issued. 1,070 of the preliminary approvals are microbusinesses.
- **The Jan 1, 2027 cliff hits *qualified* applicants, not preliminarily approved ones.** Anyone who was
  qualified before June 1, 2026 and has not moved to preliminary approval by Jan 1, 2027 is denied.
  Preliminary approvals run 18 months, plus a 6-month extension OCM *must* grant on request, plus a
  second 6 months at its discretion.

## 1. What OCM publishes

| File / page | What it holds | Names? | Local copy |
|---|---|---|---|
| Licensed businesses xlsx, updated weekly. Current: `https://mn.gov/ocm/assets/MN_OCM_licensed_businesses_100526_tcm1202-714418.xlsx` (Oct 5, 2026) | Sheet "Licensed cannabis businesses" (459 rows): License Number, License Type, Legal Business Name, D.B.A., Business Type, Medical Cannabis Retail, Social Equity Classified, Retail Site Address, **Site Contact, Email**, Local Authority, City, County, Site License Issued Date, License Expiration Date. Sheet "Licensed LPHE businesses" (3,174 rows), similar columns. | Yes, but **licence holders only** | `MN_OCM_licensed_businesses_100526_tcm1202-714418.xlsx` |
| Summary application table on `https://mn.gov/ocm/data-reports/application-data/` | Counts by licence type × status (withdrawn, denied, not selected, qualified, preliminarily approved, issued) | No — counts only | `OCM_application_data_page_wayback_20260518.html` (Wayback copy, May 11 data) |
| Lottery results, `https://mn.gov/ocm/businesses/licensing/lottery/lottery-results.jsp` — five "Official Drawing Record ... redacted" PDFs at `https://mn.gov/ocm/assets/Official_Drawing_Record_*` | Ordered draws of **application IDs** (e.g. `DIS-A25-000080`) for SE + general cultivator, manufacturer, mezzobusiness (June 5, 2025) and retailer (SE June 5, general July 22, 2025) | **No — IDs only** | `Official_Drawing_Record_*.pdf` |
| OCM 2026 law-change summary, `https://content.govdelivery.com/attachments/MNOCM/2026/05/26/file_attachments/3663662/Cannabis_Policy_Changes_2026.pdf` | Plain-English summary of 2026 c.123 | — | `OCM_2026_Legislative_Changes_Ch342.pdf` |

Access notes: every `mn.gov/ocm/*.jsp` page sits behind a Radware bot captcha (curl, WebFetch and headless
Chromium all blocked, 2026-10-10). The `/ocm/assets/` files are **not** walled — they download with plain
curl. The xlsx filename changes weekly (`MN_OCM_licensed_businesses_MMDDYY_tcm1202-714418.xlsx`, history
listed by the Wayback CDX API), so guess the latest Monday's date.

### The ID trick: which lottery winners still have no site

An application ID and its licence number share the same serial (`DIS-A25-000080` won the July 22 retail
draw; `DIS-L25-000080` is 255 Medical LLC, 4423 Nicollet Ave, Minneapolis, licensed Oct 2, 2026). Matching
the five drawing records against the Oct 5 licence file
(`data/raw/lottery_winners_vs_licensed_20261005.csv`):

| Draw | Winners | Licensed by Oct 5, 2026 | **No licence yet** |
|---|---|---|---|
| Retailer, social equity (6/5/25) | 75 | 9 | **66** |
| Retailer, general (7/22/25) | 75 | 9 | **66** |
| Mezzobusiness, SE + general (6/5/25) | 100 | 25 | **75** |
| Cultivator | 50 | 24 | 26 |
| Manufacturer | 24 | 3 | 21 |

So **132 retail lottery winners and 75 mezzobusiness winners hold no licence 15 months after the draw.**
The IDs are public; the names behind them come from the data request below.

Also in the licence file: 98 microbusinesses licensed for **cultivation only** (no retail site address), 13
of them in the metro — licence holders who may later add a retail location.

### Pipeline counts (OCM table, data as of May 11, 2026)

Source: Wayback copy of `https://mn.gov/ocm/data-reports/application-data/` (captured 2026-05-18).

| Type | Applicants | Qualified | Prelim. approved | Issued |
|---|---|---|---|---|
| Retailer | 854 | 70 | 83 | 9 |
| Mezzobusiness | 273 | 41 | 51 | 8 |
| Microbusiness | 1,854 | 351 | 1,070 | 159 |
| All cannabis types | 3,541 | 546 | 1,344 | 209 |

Later press figures: 1,332 preliminarily approved, 527 qualified, 240 issued
(`https://mncannabishub.com/news/minnesota-cannabis-mid-2026-licenses-omnibus-bill-testing-crisis`);
1,255 preliminarily approved and 350 issued by August
(`https://themarijuanaherald.com/2026/08/minnesota-has-issued-350-cannabis-business-licenses-with-1255-more-preliminarily-approved/`).

### Data practices: the names are public data

Minn. Stat. 342.20 subd. 2 (`https://www.revisor.mn.gov/statutes/cite/342.20`), as amended by 2026 c.123
s.30 (`https://www.revisor.mn.gov/laws/2026/0/Session+Law/Chapter/123/`):

> "(a) The following application data submitted by an applicant for a cannabis business license or hemp
> business license are public data: (1) the applicant's name and designated address; (2) data disclosing
> the ownership and control of the applicant; ... (4) data showing the legal possession of the premises
> where the business will operate; ... (b) The status of the applicant's application, except for an
> applicant's status as a social equity applicant, is public data."

So a request for "name, designated address, ownership, and application status of every applicant with
preliminary approval or qualified status" asks only for data the statute names as public. Social-equity
status is withheld, but the names are not. OCM's own data-request page (`https://mn.gov/ocm/connect/data-requests/`,
per search snippet; the page itself is bot-walled) says public data goes to "anyone who submits a valid
data request", in writing, at no charge under $50, "within a reasonable time". Star Tribune reported that
names of lottery winners "will not be released until they are fully licensed"
(`https://www.startribune.com/minnesota-holds-first-lotteries-for-cannabis-business-licenses-nearly-two-years-after-legalization/601367113`).
That was OCM policy in 2025, *before* the 2026 amendment made application status public. A request is the
test. See the `records-request` skill for drafting and chasing it.

The "designated address" matters twice. It may be a home address, or for some applicants the site they
hoped for. And subd. 2(a)(4) makes "legal possession of the premises" public, which shows who has a site.

## 2. The January 1, 2027 expiry — exact text

2026 Minn. Laws c.123 s.17, amending 342.14 subd. 3, new paragraph (f), effective the day after enactment
(`https://www.revisor.mn.gov/laws/2026/0/Session+Law/Chapter/123/`):

> "(f) An applicant's status as a qualified applicant under this section expires after six months. For an
> applicant who achieved qualified applicant status before June 1, 2026, qualified applicant status
> expires on January 1, 2027. The office must deny an application submitted by an applicant whose
> qualified applicant status has expired. An applicant whose qualified applicant status expired may apply
> anew according to this section."

OCM's summary says what qualified status is: the stage "during which an applicant must complete a
background check and submit their labor peace agreement" (`data/raw/OCM_2026_Legislative_Changes_Ch342.pdf`).
**Who loses on Jan 1, 2027: qualified applicants (546 as of May 11) who haven't reached preliminary
approval.** Their problem is the background check and labor peace agreement, not a site. They are not
the buyer until they clear that step.

Preliminary approval, c.123 s.19 amending 342.14 subd. 10:

> "(a) A preliminary license approval expires after 18 months unless the office revokes the preliminary
> license approval or grants an extension. The office must grant an initial extension of up to six months
> upon request by the applicant. The office may grant an additional extension of up to six months if an
> applicant has made good faith efforts to convert a preliminary license approval into a license."

Inference, not a published date: the lottery winners were drawn June 5 and July 22, 2025. If OCM issued
their preliminary approvals soon after, their 18 months end around **December 2026 to January 2027**, and
they need an extension request. "Made good faith efforts" for the second extension is where a site
search on paper helps. The 2026 law also adds a denial ground for final licensure: "(6) the applicant fails
to demonstrate that the proposed cannabis business's location complies with local zoning ordinances"
(c.123 s.18, amending 342.14 subd. 6).

### City caps (342.13, as amended by c.123)

> "A local government unit that issues a cannabis retailer registration under section 342.22 may, by
> ordinance, limit the number of licensed cannabis retailers, cannabis macrobusinesses with a retail
> operations endorsement, cannabis mezzobusinesses with a retail operations endorsement, and cannabis
> microbusinesses with a retail operations endorsement to no fewer than one registration for every 12,500
> residents. After each increment of 12,500 residents, the number of required registrations must be
> rounded up to the next whole number of registrations."

The 2026 law also struck the old county-level escape clause ("If a county has one active registration for
every 12,500 residents, a city or town within the county is not obligated to register a cannabis
business"). OCM's summary: a city "must apply the registration cap adopted regardless of how many have
been issued in the rest of the county."

CITY_CAPS_PLACEHOLDER

## 3. Named applicants and their own records

APPLICANTS_PLACEHOLDER

## 4. Super users

SUPERUSERS_PLACEHOLDER

## 5. What could kill it

KILL_PLACEHOLDER
