# Legal Lots — who buys, and how to find them by name

Researched 2026-10-10. Every claim carries its URL. Files cited as `data/raw/...` are in
`/Users/aidan/Desktop/workspace/legal-lots/data/raw/`.

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

Metro city caps found (checked 2026-10-10; "(snippet)" means a search-engine summary, not the page itself).
Brooklyn Center, Edina, Woodbury and Cottage Grove returned 403 / Cloudflare.

| City | Cap | Full? | How allocated | Source |
|---|---|---|---|---|
| Saint Paul | **no cap** ("no limit or cap... at this time") | no | — | https://www.stpaul.gov/node/134211 |
| Bloomington | **no cap** (2024 report) | no | — | Sun Current, "Bloomington sets retail regulations" (hometownsource.com) |
| Burnsville | **no cap, no buffers** | no | — | https://www.burnsvillemn.gov/2414 |
| Brooklyn Park | 7 | "five ... awarded or in process" (snippet) | — | https://codelibrary.amlegal.com/codes/brooklynpark (sec. 127.04) |
| Brooklyn Center | 3 | 1 selected Jan 2026 | **lottery**; entry needs OCM preliminary approval + local application; later lottery Apr 27 (snippet) | brooklyncentermn.gov cannabis-registration page (403) |
| Blaine | 7 | **all 7 issued** (3 active, 4 pending OCM); 2 in queue | **queue** | https://www.blainemn.gov/4126/CannabisLower-Potency-Hemp-Business-Regi |
| Eagan | 8 (5 commercial + 3 industrial) | ? | first come, first served | https://www.cityofeagan.com/cannabis |
| Lakeville | 6 | ? | first come, first served | https://www.lakevillemn.gov/1187 |
| Woodbury | 7 (snippet) | ? | ? | https://www.woodburymn.gov/1033/Adult-use-Cannabis |
| Edina | 5 (snippet) | ? | ? | https://www.edinamn.gov/2099/Cannabis-Licenses |
| St. Louis Park | 5 (staff-proposed) | ? | ? | citizenportal.ai 6297822 |
| Inver Grove Heights | 4 | ? | ? | ighmn.gov DocumentCenter/View/17933 |
| Richfield | 3 | ? | ? | Sun Current, "Richfield sets business parameters" |
| Ramsey (Anoka Co.) | 2 | **FULL** | **waitlist** by email to businesslicensing@cityoframsey.com | cityoframseymn.gov cannabis-retail-license page |
| Minneapolis | cap not found; city registers retailers itself | ? | ? | — |

Hennepin County Ord. 27 (1 per 12,500) covers the cities that delegated: Chanhassen, Greenwood, Hanover,
Loretto, Medicine Lake, Minnetonka Beach, Orono and Spring Park. Not determined: Plymouth, Maple Grove,
Eden Prairie, Coon Rapids, Apple Valley, Maplewood, Cottage Grove, Roseville, Andover, Fridley, Savage,
Chaska, Prior Lake, Shoreview, West St. Paul.

Retail is concentrating where there is no cap. Of the 182 metro licences in the Oct 5 file, Minneapolis
has 24 retail-type sites and Saint Paul 17; no other metro city has more than 4.

## 3. Named applicants and their own records

`research/applicants.csv` has **10 rows**. Each is a named applicant, not in the OCM licensed file as of
2026-10-05, with their own public record. Every name was checked against the licence file on legal name,
DBA, site contact and email. Rows dropped because they turned out to be licensed: 5D Dispensary (Brittney
Yares), Great Northern Greens, Redux Cannabis, Laketown Farms (Charles Levine), Prairie Wind / Chillwater,
Kaps LLC (Josh Kasprzyk of BKR Brands), Northcare Wellness (Abbey Johnson), The Warrior's Garden.

**The best leads lost a site and are still on the clock:**
- **The Tobacco Store**, Mike Malik, Apple Valley. Council denied the setback variance on 11/25/2025.
- **HiRISH Acres**, Apple Valley. Denied in May 2025.
- **Venus Creations LLC**, Cottage Grove. CUP and variance denied by the Planning Commission on 12/15/2025.
- **Green Lane Express**, Brian Bartley. More than 20 landlord rejections, Star Tribune 10/15/2025.

**Aaron Beauchaine** won a retail lottery slot and is targeting Plymouth to Prior Lake. He is also a broker at
Meta Commercial Cannabis Real Estate, so he is both a buyer and a super user.

Marcus Harcus (North Minneapolis) was described as preliminarily approved in Oct 2025 by Sahan Journal. His
own Substack says he gave up: "I applied for two Minnesota Cannabis business licenses, but didn't get one."
(https://wdla.substack.com/p/dispensary-dreams-deferred). He is excluded.

**Which sources worked.** City zoning records produced new names: CUP staff reports, council resolutions and
permit files (West St. Paul, Bloomington, Apple Valley, Burnsville). Their limit is that most of those
applicants already have a building, so the **denials** are the valuable rows. News produced four people.
LinkedIn, GoFundMe/Wefunder and "coming soon" searches returned nothing through WebSearch. Reddit (Arctic
Shift) was down.

## 4. Super users

| Who | Org | Why they matter | Own record |
|---|---|---|---|
| Christopher D. Luehr | Lommen Abdo (cannabis practice lead) | "We advise cannabis businesses on real estate matters, including property acquisition, leasing, zoning considerations, and local compliance issues." 612.339.8131 | https://lommen.com/practice-areas/cannabis-laws-attorney-minnesota-and-western-wisconsin/ |
| Trina Sjoberg, Gerald Fornwald, Nicholas Valle, Rachel Kurth | Winthrop & Weinstine | "First, preliminary licensees need to determine where they will be allowed to operate." | https://winthrop.com/bold-perspectives/from-lottery-to-launch-what-comes-next-for-minnesota-cannabis-licensees/ |
| Jason Tarasek, Yolanda Clarke | Vicente LLP, Minneapolis (Tarasek is also on the Sota Cann board) | Feb 2026 Lucky Leaf panel on "zoning issues" (snippet) | https://vicentellp.com/insights/jason-tarasek-yolanda-clarke-lucky-leaf-expo-minneapolis-2026/ |
| Doug Junker, Bill Griffith | Larkin Hoffman | Junker was Bloomington's licence examiner for 20 years; Griffith does land use | https://www.lexblog.com/?p=2947505 |
| Carol Moss | Hellmuth & Johnson; OCM Cannabis Advisory Council | On local barriers: "approximately 20 municipalities have enacted conflicting restrictions" (firm paraphrase) | https://hjlawfirm.com/news/hellmuth-johnsons-carol-moss-addresses-local-cannabis-business-barriers-in-minnesota/ |
| Jeffrey O'Brien, Jonathon Duffy | Husch Blackwell | Zoning "is just as much about educating the municipal staff" | https://www.lexblog.com/?p=3310377 |
| Michael Sly | Dorsey & Whitney; Cannabis Advisory Council | — | https://www.dorsey.com/newsresources/news/press-releases/2024/2/sly-mn-cannabis-advisory-council |
| Mitchel Chargo | Hinshaw & Culbertson (CRE + cannabis) | Landlord-side counsel | https://minnlawyer.com/2024/09/06/what-landlords-should-know-about-cannabis-businesses/ |
| Thomas Howard | Collateral Base / Howard Law Group | "This timeline allows applicants to identify and prepare a compliant site." | https://www.cannabisindustrylawyer.com/how-to-open-a-dispensary-in-minnesota/ |
| Jen Randolph Reise | North Star Cannabis Consulting / North Star Accelerator | Accelerator for craft and social-equity applicants; runs a newsletter | https://ganjapreneur.com/business/north-star-cannabis-consulting/ |
| Leili Fatehi, Laura Monn Ginsburg | Blunt Strategies | MN's first cannabis-only consultancy | https://tcbmag.com/tcb-100-people/leili-fatehi-and-laura-monn-ginsburg/ |
| Sumer Thomas | Canna Advisors | MN licensing guide | https://thinkcanna.com/blog/apply-minnesota-cannabis-license/ |
| Stephen Dombrovski; Aaron Beauchaine | Meta Commercial Cannabis (Minnetonka) | Cannabis-only CRE brokerage | https://rejournals.com/green-rush-minnesotas-1-5-billion-cannabis-market-needs-brokers-now/ |
| Mike Phelan | Mid-America Real Estate MN | Retail broker who writes on cannabis zoning | https://midamericagrp.com/?p=10509 |
| Green Zoned Realty (no person named) | Troy, MI | Lists a Roseville dispensary site, 1899 Perimeter Rd | https://www.420property.com/listing/minnesota-recreational-cannabis-dispensary/ |
| Fatima Moore | Sota Cann (MN cannabis trade association, 515 N Washington Ave #250, Mpls), Executive Director | Membership tiers include vendors and law firms; no member count published | https://sotacann.org |
| Stephen Eigenmann | Canna Connect / Cannaverse newsletter, founder | Runs a recurring event series; Oct 15 is in **Duluth** | https://cannaverse-newsletter.beehiiv.com/p/october-7th-cannaverse-newsletter-inside-mn-cannabis-growth-celebration-community |
| Jess Jackson | OCM, Director of Community and Economic Development | Hosts the Oct 22 fair | same newsletter |

"MN Cannabis Co-op" and a "Cannabis Growers Association of MN" left no findable public record. The
Minnesota Marijuana Association (Frank Ongaro, acting ED) appeared only in a search snippet and is unverified.

**Events**
- **OCM Resource & Hiring Fair, Thu Oct 22, 2026**, UROC Plymouth Room (Rm 105), 2001 Plymouth Ave N,
  Minneapolis 55411. The 1 to 6 p.m. time comes from a search snippet. The bulletin says it brings together
  "grantees, community partners, applicants and resource providers"
  (https://content.govdelivery.com/accounts/MNOCM/bulletins/426f237). Organisations sign up through an
  interest form (https://officeofcannabismanagement.formstack.com/forms/resource_and_hiring). Nothing
  published says whether that gets a vendor a table. **Applicants will be in the room.**
- **Canna Connect, Thu Oct 15, 2026, Clyde Iron Works, Duluth.** Three events: an industry luncheon for
  "operators, sponsors, vendors, professional service providers", a cultivation expo and an after-party
  (https://www.eventbrite.com/o/canna-connect-69612730803). Sponsorship exists. It is not in the metro.
- No other metro cannabis business events found for Oct to Dec 2026.

## 5. What could kill it

- **Applicants are anonymous online, not in law.** OCM publishes IDs, not names, until licensure. But
  342.20 subd. 2 makes name, designated address, ownership and (since 2026) application status public. This
  is solved with one written data request to OCM, not by search. If OCM refuses, that refusal is the
  thing that would kill the direct channel. The 2025 "not until licensed" line predates the 2026 amendment.
- **Many buyers already have a site.** The public record skews toward applicants mid-CUP. The report is
  worth most to (a) site denials and (b) the 132 retail and 75 mezzo lottery winners with no licence 15
  months on, whose clocks end around Dec 2026 to Jan 2027.
- **Cap-free cities shrink the "where is it legal" question to zoning plus buffers**: Saint Paul,
  Bloomington and Burnsville. Capped cities that are full (Blaine, Ramsey) make the question "is there a
  slot", which a lot list doesn't answer. The report should carry the cap and queue status per city.
- **Jan 1, 2027 is a qualified-applicant cliff, not a preliminary-approval cliff.** Pitching it as "you
  lose your approval Jan 1" would be wrong for the core buyer. The correct urgency for them is the 18-month
  expiry and the "good faith efforts" test for a second extension.
