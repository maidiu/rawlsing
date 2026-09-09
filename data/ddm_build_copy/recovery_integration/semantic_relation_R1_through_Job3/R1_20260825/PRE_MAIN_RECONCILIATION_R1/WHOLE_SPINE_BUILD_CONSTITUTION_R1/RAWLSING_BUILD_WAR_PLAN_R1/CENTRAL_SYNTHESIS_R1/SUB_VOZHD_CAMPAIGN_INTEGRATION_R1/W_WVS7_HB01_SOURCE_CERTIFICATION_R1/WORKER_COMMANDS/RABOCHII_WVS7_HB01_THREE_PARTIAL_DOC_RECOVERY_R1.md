# RABOCHII WVS7/HB01 — THREE PARTIAL COUNTRY UNIVERSE DOCUMENT RECOVERY R1

Repository:
`maidiu/rawlsing`

Worker branch:
`agent/rabochii-subv-w-hb01-wvs7-three-partial-doc-recovery-r1`

Commissioning campaign:
`agent/sub-vozhd-wvs7-hb01-source-certification-r1`

Commissioning campaign HEAD before this command:
`155ae2d1416b89f9a0035ca0cc284183ed069224`

Authorized grain:
`WVS7_THREE_PARTIAL_COUNTRY_UNIVERSE_DOCUMENT_RECOVERY_ONLY`

## Exact residual

Recover only the one missing D11 documentary claim for each previously PARTIAL country:

1. New Zealand 2019/2020 — missing: `target population / coverage`
   - already accepted: frame + actual design.
   - exact IHSN catalog: `12291`
   - exact methodology resource: `104847` — `WVS7 Methodology Report New Zealand 2019`
   - exact sample-design resource: `104850`.

2. Romania 2017/2018 — missing: `target population / coverage`
   - already accepted: frame + actual design.
   - preserve the historical sample-size contradiction exactly: target sample size `1200` and later allocation-formula `n=1500`; no repair by preference.

3. Ukraine 2020 — missing: `sampling frame`
   - already accepted: target + actual design.
   - exact IHSN catalog: `12310`
   - exact methodology resource: `104954`
   - exact sample-design resource: `104956`
   - country report resource: `104958`.

## Current recoverable evidence

### Romania

Country/source-team page:
`https://www.romanianvalues.ro/rezultate-pentru-publicul-larg/various-posts/first-public-release-of-the-romanian-evswvs-20172018-data`

The Romanian WVS/EVS team explicitly states that the WVS was collected November 2017-February 2018 and that both samples were randomly drawn from the Romanian non-institutionalized population and were nationally representative. This is direct positive country/year source-team target/coverage evidence.

Adjudicate this claim at exact source-owner/source-team grain; do not import unrelated historical Romanian WVS universes.

### New Zealand

IHSN catalog `12291` identifies the WVS7 country deposit and exact methodology/sample-design PDFs. The public study page states that WVS prefers a full probability sample age 18+, but preference/baseline is not itself proof that the exact New Zealand Wave-7 target had no country-specific qualification.

Do not promote target from:
- electoral-roll frame alone;
- neighboring WVS waves;
- WVS generic preferred-sample language;
- a secondary source saying 18+ general public.

Only promote if exact WVS7 New Zealand country-grain documentary body or equivalent source-owner evidence establishes the target.

### Ukraine

IHSN catalog `12310` exposes exact resource `104956` as `WVS7 Sample Design Ukraine 2020`.

The accepted Ukraine country report establishes target/coverage and multistage stratified random design but states that each selection stage is detailed in the full report. That is not enough to infer the exact sampling frame.

Do not substitute:
- EVS Ukraine sampling frame;
- generic WVS sampling practice;
- country geography;
- observed regions/PSUs;
- another Ukraine survey.

Only promote frame from exact WVS7 Ukraine country-grain positive evidence.

## Retrieval law

Use, in order:

1. Library exact files/bundles if present;
2. IHSN/WVSA/GESIS source-owner or authorized mirror body text;
3. country-team/source-team authoritative mirrors;
4. other readable mirrors only when document identity and source-owner provenance can be exactly tied.

If exact public document identity is known but body transport remains inaccessible, record:
`EXACT_DOCUMENT_IDENTIFIED__BODY_TRANSPORT_BLOCKED`
with exact catalog/resource ID.

Do not relabel transport failure as epistemic absence.

## Required return

Bank under:
`.../W_WVS7_HB01_SOURCE_CERTIFICATION_R1/WORKER_RETURNS/THREE_PARTIAL_DOC_RECOVERY_R1/`

At minimum:
- `RESULT.md`
- `RESULT.json`
- `CLAIM_ADJUDICATION.csv`
- `DOCUMENT_ACQUISITION_LEDGER.csv`
- `CHANGED_FILES.txt`

PASS may be partial. Each country is independently adjudicated.

Allowed per-claim terminal states:
- `RECOVERED_SOURCE_OWNER_AUTHORITY`
- `EXACT_DOCUMENT_IDENTIFIED__BODY_TRANSPORT_BLOCKED`
- `DOCUMENT_IDENTIFIED_CONTENT_NOT_RECOVERED`
- `DOCUMENT_NOT_LOCATED`

No inference state is permitted.

If Romania target is accepted, return that Romania is now documentary-full and ready for a **new D11 materialization commission**. Do not mutate or widen the old 3-country D11 materializer.

PASS target:
`WVS7_THREE_PARTIAL_DOCUMENT_RECOVERY_COMPLETE__EACH_MISSING_CLAIM_EXACTLY_ADJUDICATED__NEW_D11_SUPPORT_READY_WHERE_PROVED`
