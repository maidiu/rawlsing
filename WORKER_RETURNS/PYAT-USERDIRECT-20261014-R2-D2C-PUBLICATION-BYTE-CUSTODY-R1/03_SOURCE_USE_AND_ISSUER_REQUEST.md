# D2C — exact archival acquisition, reuse-law and original field-issuer docket

**Disposition: DOCUMENTARY_TABLES_VERIFIED / BINARY_ARCHIVE_AND_SOURCE_RIGHTS_HOLD. No self-issuance.**

## Decision A — publisher archive custody, GSS

**Requested of:** Ghana Statistical Service 2021 PHC reports/archive office, **2021phc@statsghana.gov.gh** (contact published on the official 2021 PHC news page).

**Provide a read-only certified original 24 February 2022 release binary** for `Ghana 2021 PHC General Report Volume 3K — Housing Characteristics`, file convention `Volume 3K_Housing Characteristics_240222.pdf`, current official URL:
`https://census2021.statsghana.gov.gh/gssmain/fileUpload/reportthemesub/Volume%203K_Housing%20Characteristics_240222.pdf`.

Requested exact preservation package:
1. Original whole PDF raw bytes (or archive-managed authenticated download), byte count, `sha256`, publication/creation/edit dates and PDF Info/XMP metadata (metadata as corroboration, not binary identity).
2. Initial February 24 issue upload/press notice/object id, current publisher object URL, full redirect/Last-Modified/ETag history **if actually retained**, each revised edition/erratum/supersession notice and effective publication date. If none, publisher must explicitly attest rather than worker asserting no revisions.
3. Table 5.10 rural occupied-dwelling lighting: native census questions/category codebook, occupied/secondary/vacant exclusions, census reference and enumeration method, sources for all five electricity subtypes, exact Table 5.10 version history, known reporting/coverage correction or quality limitations.
4. Specific rights/conditions for machine-processing the *published aggregate* 2,388,192 of 3,288,063 (plus five categories) into a proprietary/open Rawlsing-generated-context engine, storing minimal numeric derived fields and citations, caching/replaying with versioned provenance. Distinguish permission to read/cite statistical numbers, reproduction/distribution of PDFs, republishing whole tables, derivative/persistent model use, and any restriction on commercial or publicly accessible processing. No respondent data requested.

**Current legal finding:** GSS Statistical Service Act 2019 (Act 1003) §52 governs publication, metadata and significant-correction notifications; §§50/52 protect confidential microdata. GSS census website footer states *all rights reserved*. GSS microdata portal [policies](https://microdata.statsghana.gov.gh/index.php/policies-and-procedures) impose dataset-specific redistribution and confidentiality restrictions; **those microdata terms must not be mechanically projected onto public aggregate tables**, yet also cannot be read as an open licence for their republishing. No explicit publication-specific CC/open-data licence or Rawlsing reuse grant verified for this Volume 3K PDF. Legal/source-use steward decision remains necessary.

## Decision B — publisher archive custody, NCA

**Requested of:** National Communications Authority, **Director, Research, Innovation, Policy and Strategy Division**, **rips@nca.org.gh**, with **info@nca.org.gh** (contact given inside the bulletin's initial pages).

**Provide certified original July 8, 2022 released binary** for *Quarterly Statistical Bulletin on Communications in Ghana, Volume 6 Issue 4, Fourth Quarter October–December 2021*; current official PDF:
`https://nca.org.gh/wp-content/uploads/2022/07/Q4-2021-statistical-Bulletin.pdf`.

Request original issue versus current whole-byte SHAs/sizes/recorded upload timestamps, any revised report/erratum/backfill/replaced PDF, correction dates and reconciliation. Resolve the web announcement path `/2022/07/08/quarterly-statistical-bulletin-on-communications-2022-q4/` as administrative slug versus **2021 Q4 official content**. Certify Table 10 origin (mobile-data subscription aggregation from licensed provider reports), Q4 time snapshot, 90-day upload/download traffic threshold, technical coverage, prepaid/postpaid counting, SIM/service-level duplicate treatment, corrections/late-provider returns, and limitations of population or regional interpretation. If retained, supply an archive-issued stable file reference plus server Last-Modified/ETag; these do not substitute for a hash of downloaded bytes.

**Rights ask:** permission/conditions for automated reuse of the **national aggregate mobile-data subscription counts** 23,414,527 = 23,237,338 prepaid + 177,189 postpaid, in a contextual historical model, with attributed official citation and exact edition provenance. Request written differentiation among quoting published statistical facts, reproducing the PDF/figure, storing parsed data fields and distribution to users. Do **not** request licensee proprietary respondent/SIM records.

**Current legal finding:** NCA site states © 2021 National Communications Authority, all rights reserved. Its [8 July 2022 announcement](https://nca.org.gh/2022/07/08/quarterly-statistical-bulletin-on-communications-2022-q4/) says the statutory publication mandate is §26(2)(a) of Electronic Communications Act 2008 (Act 775), and explains the bulletin is compiled from licensee reports. **An agency's authority to publish is not necessarily a downstream automated-reuse licence.** No issue-specific open-content permission was found. This is an identified legal decision requirement, not an assertion that citing bare statistics is forbidden.

## Decision C — source science, independent of bytes and copyright

Two scientific subject authorities or a suitably competent independent methodology reviewer must separately countersign:

- **GSS measurement validity**: 2021 census occupied dwelling-unit category, rural boundary/geography, exclusion logic, five distinct electric-main-lighting types versus mains-only versus separate solar lamp, 72.632...% rounded to 72.6; explicit non-sampling limitations and corrected-edition currentness.
- **NCA measurement validity**: active *subscription* records with preceding 90-day recorded traffic, national Q4 2021 aggregate, sum to 23,414,527, any duplicate-account/report revision method, missing subnational/unique-person fields.

No individual exposure, all-household internet penetration, or cross-field person/joint probability may be supplied without a new, separately accepted measurement design.

## Decision D — Rawlsing N5/N6 objective-field issuer, then N7/EE13

**Exact narrow input:** the two packets `05_GSS_DOCUMENTARY_PACKET.json` and `06_NCA_DOCUMENTARY_PACKET.json` after publisher byte roots, editions, method decisions, source-use rights, and immutable archival refs are filled by verified receipts. Proposed product type `ExternalPublishedAggregateField` is a **candidate name**, not a granted law. Authorized N5/N6 objective field issuer must create **two separate** source-backed fields with exact numeric value, denominator where meaningful, category, native unit, geography, measured/ref/publication/as-of clocks, exact allowed-use authority and edition-specific replay/refusal. No survey microdata retrieval; no implied EE13.

Only a separate **N7/EE13 relation issuer** could subsequently permit these two exact refs' **NONPOOLED_CONTEXTUAL_CO_PRESENCE_ONLY**. The relation contains no measured joint events, no shared respondent or household sampling unit, and no cross-source covariance. The earliest documentary both-known as-of is **2022-07-08**, *subject to authenticated editions and permission gates*. Report 2021 publication knowledge as unavailable.

## Decision E — historical N9/OC05 consumer and independent court

The existing D2I sourcefree **40/40** local test-only result `2653fff57ac59fe2eaeffd24a0611c45f16f3b54` demonstrated values-read and source-specific synthetic ±1 replay. It is **not a published-source issuer, not an N5/N6 adoption and not original PDF custody**. A genuinely operative historical N9/OC05 reviewer must dereference actual newly issued fields, enforce both publisher identity and issued use ceilings, use **two independent read receipts**, hold when a required source is not yet published/available, preserve original/corrected editions, reject national-subscription→rural-person inference, and replay only descendants of a corrected publisher item.

Minimum independent acceptance:
- Read and hash each complete official PDF with locally reproduced byte length, manifest, metadata and archived release/ref (not URL hashing); compare first/current/revised editions and errata under signed source custody.
- Independently check source science categories, counts, rounding, as-of, licensing and exact distinct issuer signatures.
- Reuse or extend accepted owner N5/N6 published aggregate producer behind lawful direct route, without D2C worker creating an issuing authority.
- Commission independent review and then owner/HQ adoption; **no automatic N12 wake, no EE13 or OC05 self-adoption, no physical weld, no V3**.

**Archival block escalation:** If publisher download continues to fail, send the two precise archival requests above. Until entire binaries enter an authorized hash-capable environment, their `sha256`, `byte_length`, original-vs-current equivalence and binary content-metadata fields MUST remain `null` in the documentary packets and ledger. Public browser screenshots cannot repair this custody gap.
