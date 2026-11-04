# SRC04 original questionnaire authority — 42 fields

**Base:** `6d1ddb9844a5117d466bb0c3a8bc5260196c4249`
**Branch:** `agent/pyat-pdev01-gap007-sourcefree-r1`
**Mode:** TEST_ONLY original questionnaire metadata trace; no respondent read.

## Verdict

**`HOLD_ROUTING_UNKNOWN_AND_14_AUTHORITY__28_CERTIFIED_PRESERVED__PDF_EVIDENCE_EXACT`**

The supplied Wave 1 questionnaire editions are byte-identical. Exact item
citations are now recorded for all 42 fields: **42/42 explicitly print
`99 = Decline to Answer`**. This is response evidence, not a routing rule.
No skip, filter or ask-all instruction appears in the questionnaire.

Routing therefore remains `ROUTING_UNKNOWN` for **42/42** fields. The 14 held
refusal codes have exact source evidence but their option-authority status
remains `preserved_not_certified`; no correction was applied.

## Edition comparison

Both supplied files are the same artifact:

```text
/Users/matthewsmith/Desktop/Rawlsing/data/original codebook pdfs/Arab Bar W1 Questionnaire_ENG.pdf
/Users/matthewsmith/Desktop/Rawlsing/data/Arabbarometer/ABI_Questionnaire_ENG.pdf
sha256 0814f77bcfdad3c78d5e46f49012437f25ddcbfe8bea3e565d7a26874bab4118
bytes 1075090
pages 30
```

`byte_identical=true`, `extracted_text_identical=true`, `edition_delta=NONE`.
Both PDF metadata titles identify the same Arab Barometer W1 codebook/questionnaire.
There is no independent second edition in the supplied pair.

## Exact item citations

`evidence/QUESTIONNAIRE_ITEM_CITATIONS.csv` records, for each of the 42 fields:

- PDF page and printed page
- exact question label
- question line
- response `99` page and line
- literal response evidence `99 = Decline to Answer`
- exact option-authority status
- certified/held state

Examples:

| Field | Question PDF page | Printed page | Response evidence |
|---|---:|---:|---|
| q101 | 2 | 3 | 99 = Decline to Answer |
| q202 | 3 | 4 | 99 = Decline to Answer |
| q207 | 4 | 5 | 99 = Decline to Answer |
| q2312 | 7 | 8 | 99 = Decline to Answer |
| q234 | 8 | 9 | 99 = Decline to Answer |

All 42 citations are present in the CSV; 42/42 have the exact `99` label.
The questionnaire was read as metadata only; no respondent rows were opened.

## Routing evidence

The full questionnaire text scan returned:

```text
skip=0 filter=0 routing=0 ask all=0 go to=0 routed=0
eligib=0 screened=0 screen=0 unconditional=0
exact_route_instruction_count=0
```

Occurrences of `if` and `only` on pages 6, 7, 10, 14, 18, 20, 21 and 7, 11,
18, 24, 28, 29 are substantive question prose, not filters or skip instructions.
No route, form or eligibility rule is stated.

The existing configuration interface remains unchanged and was validated through
the normal schema owner:

```text
source_configuration.data.SRC04.source.config.json:routing[]
schema_owner=rawlsing_next.source_configuration.schema.validate_source_config
valid=true
config_changed=false
selected_route_entries=42
exact_route_bindings=0
exact_eligible_denominators=0
```

Every selected entry remains `ROUTING_UNKNOWN`; every `routing_rule_ref` and
`risk_set_ref` is unresolved. `row_selector=ALL` was not promoted into
eligibility authority. Supported route bindings: **0**.

## Remaining 14 held refusal codes

The 14 fields retain exact per-item questionnaire evidence for code 99, but their
option-authority status remains `preserved_not_certified`:

```text
q202 q207 q210 q212 q216 q222 q224 q226 q227 q228 q2301 q2302 q2311 q2312
```

Their exact evidence is recorded in `evidence/RESPONSE_AUTHORITY_14.csv`, including
PDF page, printed page and response line. No correction was applied.

**Exact missing premise:** competent item-specific authority certification for
the code-99 response semantics; the source label is explicit, but the current
authority row is `preserved_not_certified`.

**Owner:** ARAB lane / P3 integration owner; later competent source-semantics
authority. Their eligible/routed-out state remains `UNKNOWN`.

## Retained aggregate invariants

The accepted 28-entry overlay is preserved; the 14 held code-99 counts
(**1645**) are not applied.

| Selected 42 | Old | Corrected 28 |
|---|---:|---:|
| Valid answer | 277582 | **275397** |
| Explicit nonresponse | 21237 | **23422** |
| Refusal | 0 | **2185** |
| Missing | 9335 | 9335 |
| Observed | 298819 | 298819 |
| Source records | 308154 | 308154 |

Identity: **275397 + 23422 + 9335 = 308154**. q101 remains 7129 valid, 204
explicit nonresponse, 4 missing, 7337 total.

## State exercise

`state_machine.py` exercises three distinct outcomes without respondent data:

- `ROUTING_UNKNOWN` for unknown route;
- `ROUTED_OUT` for ineligible route;
- `DECLINED` for certified code-99;
- `RESPONSE_SEMANTICS_HELD` for code-99 without certification;
- `ELIGIBLE_RESPONSE` for a substantive eligible response.

These states are not conflated. No ineligible or routed-out count was inferred.

## Runtime/passport

`PASSPORT.json` is sanitized. Runtime import verified: Python `3.11.3`,
`pypdf 6.4.0`, normal configuration schema imported and source config loaded.
Quota: **UNKNOWN** (not observed). Browser local checkout: false.

## Tests

`test_questionnaire_authority.py`: **7 passed** in 0.04s. It checks edition
identity, 42/42 exact citations, 28/14 partition, held authority status,
zero route bindings, actual schema validation, aggregate conservation and
distinct state transitions.

## Engineering / science / authority

- **Engineering:** `HOLD_EXACT_ROUTING_EVIDENCE_MISSING`.
- **Science:** `HOLD_ABSENT_ORIGINAL_EXECUTION_GRANT`; no empirical claim made.
- **Authority:** `HOLD_PRODUCTION_AND_ISSUANCE_NOT_GRANTED`; no production
  config or issuance crossed.

No original SAV/DTA or respondent rows were read. No workload, production
adoption, policy, universal code rule, merge or CI was created. Distinct
focused review of this changed evidence binding is required.
