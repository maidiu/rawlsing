# SRC04 routing recheck — exact a108e7dc

**Candidate:** `a108e7dc7232b1f3487e71d4607f3e6ca3e9ebdf`  
**Review start:** `bdeace7866bcfaf7c94710b976c80b950bfe2968`  
**Metadata origin:** `056849e23a83d7f4fa33fe4dc8eb65eaf7e2a102`  
**Mode:** TEST_ONLY sourcefree metadata/instrument review; no original respondent read.

## Verdict

**`REVISE`** — the routing HOLD and all 42 unknown routing states are confirmed,
but the accepted q101 tally semantics are wrong.

- The replay is byte-identical to the candidate routing receipt:
  `3147604e6e395d0c79e4c10f82f3e10b3823d05f826ba765e9ab201d8a31d048`.
- Focused tests: **5 passed** in 0.03s.
- `q101` code-99 responses are **Decline to Answer**, but the source config maps
  code 99 to `SUBSTANTIVE_RESPONSE`; the accepted tally therefore reports
  `valid_answer=7162` and `explicit_nonresponse=171`.
- Correct q101 values are **7129 valid**, **204 explicit nonresponse**
  (`171 DK + 33 refusal`), **4 missing**, **7333 observed**, **7337 source
  records**.
- The exact Wave I instrument does **not** provide an explicit unconditional,
  ask-all, skip or routing rule for q101. No eligibility is inferred from counts.

## Exact routing verification

Accepted prior slice:

- Release: `fc111cfa78d0fc23b5c72c1dc4b45c39d35c66c394662d7b901f5422df3370ec`
- 42 selected response slots; 2 coordinate slots
- Slice selection: `aa0d5739b5cd30f7c4d68a01035556c8f69880b5dcace82684fee2851ef35803`
- Tally product: `d9d7f43b090c599d987a3f4957a321d26701b2ee175b8f9cf71ec033588abfc0`
- Focused recheck: PASS, `D1_OBSERVED_SAMPLE_DESCRIPTIVE_TALLY_ACCEPTED`

Replayed routing result:

- 178 config routing entries; 42 selected entries
- 42 `ROUTING_UNKNOWN`
- 42 unresolved risk-set refs
- 0 exact skip rules
- accepted routing binding: **false**
- eligibility/denominator binding: **false**
- routing inferred from observed counts: **false**

`q101` routing refs are both
`urn:rawlsing:r157:original:SRC04:q101:unresolved`, typed
`ROUTING_UNKNOWN`. `row_selector=ALL` in the source config is not treated as
eligibility authority because the same row remains unresolved.

## q101 tally defect

Accepted receipt / tally:

- valid answer: **7162**
- explicit nonresponse: **171**
- missing or unobserved: **4**
- observed response: 7333
- source-record denominator: 7337
- state counts: `SUBSTANTIVE_RESPONSE=7162`, `DK=171`, `MISSING=4`

Exact q101 native counts:

| native value | state in accepted tally | count |
|---:|---|---:|
| 1 | SUBSTANTIVE_RESPONSE | 257 |
| 2 | SUBSTANTIVE_RESPONSE | 2258 |
| 3 | SUBSTANTIVE_RESPONSE | 2399 |
| 4 | SUBSTANTIVE_RESPONSE | 2215 |
| 98 | DK | 171 |
| 99 | SUBSTANTIVE_RESPONSE | 33 |
| null | MISSING | 4 |

The source config maps q101 code 99 to `response_state=SUBSTANTIVE_RESPONSE`
and `canonical_value="99"`. That conflicts with all three available authorities:

1. Exact Wave I instrument page 2: `99 = Decline to Answer`
2. Wave 1 codebook: `99 = decline to answer`
3. Response-option authority: code 99 is `option_group=special`,
   `is_substantive=False`, `is_missing=True`, `is_refusal=True`

Correct q101 state counts are therefore:

- `SUBSTANTIVE_RESPONSE=7129` (`257+2258+2399+2215`)
- `DK=171`
- `REFUSAL=33`
- `MISSING=4`
- observed response `7333`; denominator `7337`; identity `7129+171+33+4=7337`

The 33 refusals must not be counted as valid answers. The routing return's
`consumer_probe` and `test_04` currently assert the incorrect `7162/171` pair;
the tests pass because they mirror the accepted tally rather than validate its
semantics.

The same code-99 -> `SUBSTANTIVE_RESPONSE` mapping is present in all 42 selected
source-config response slots. This review verifies q101 exactly and does not
issue a corrected aggregate for the other 41 fields.

## Instrument and eligibility evidence

Exact Wave I instrument:

- Path: `/Users/matthewsmith/Desktop/Rawlsing/data/Arabbarometer/ABI_Questionnaire_ENG.pdf`
- SHA-256: `0814f77bcfdad3c78d5e46f49012437f25ddcbfe8bea3e565d7a26874bab4118`
- 30 pages; q101 on PDF page 2
- `101q How would you rate the current overall economic condition of
  [respondent's country] today? ... 98 = Can't Choose/Don't know
  99 = Decline to Answer`

The instrument lists q101 as a main questionnaire item without a visible
skip/filter. A full extracted-text search found **no** occurrences of:

`ask all`, `all respondents`, `unconditional`, `skip`, `filter`, `if yes`,
`if no`, `go to`, `routing`, or `eligib`.

This is **no rule found in the examined instrument/metadata**, not proof that no
routing rule exists in the Wave I fieldwork or another authority. q101 remains
`ROUTING_UNKNOWN`; eligibility is not established. The `row_selector=ALL`
placeholder and the observed counts were not used to infer eligibility.

## Prior metadata review

Reused without reissuing metadata authority:

- Prior review commit: `bdeace7866bcfaf7c94710b976c80b950bfe2968`
- Prior checks: `8202036810494b2a632fafb31a0d5d693044d5993e0693d0d5e981fd6f0d9600`
- Source config file: `eb4c051ff2845bf3c8c7b5bfee08ea4c9879c7a5264cf1aa6290e3fd457bc900`
- Config canonical: `0e86814b62eb51dc9da22793b6de3e3598c3415632accb80f33bac965185f284`
- Crosswalk: `034d626365249941618d66f6103a557209fce5d95362e3ddf77e29f2fe7fba23`

## Required correction / remaining input

Required correction: fix the q101 code-99 state mapping and regenerate the
accepted q101 tally/test expectation (valid `7129`, explicit nonresponse `204`).

Still unresolved, in order:

1. Exact routing/skip rule and risk-set/eligibility denominator for the accepted
   42-slot slice, first at q101:
   `urn:rawlsing:r157:original:SRC04:q101:unresolved`.
2. R03 `GrammarPolicy` / authorized direction grant.

No routing rule, eligibility denominator, or authority was fabricated.

## Scope

Metadata and exact instrument only. No original SAV/DTA or respondent rows were
read; no original workload, new authority, production edit, merge, CI or adoption.
Only `WORKER_RETURNS/PYAT-REAL-METADATA-INDEPENDENT-REVIEW/routing-recheck/**`
was written.
