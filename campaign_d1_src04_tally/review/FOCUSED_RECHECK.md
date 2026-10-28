# D1 SRC04 observed-sample tally — focused recheck

**Verdict: `PASS` at bounded D1 descriptive tally grade.**

This focused recheck was performed by the substituted qualified existing reviewer
`ses_e84b9fb79ffedqgfCcG6ZXZKRS`. The original independent reviewer
`ses_e81fc42a8ffeAbvo6M8l4YG4nK` lost its CLI handle; its original RED/REVISE
files are preserved unaltered and its 42-field/630,990-object recomputation is
reused unchanged and attributed. This reviewer did not author D1.

Candidate: `af18287a5a5c3a01f0ce993b43e6808aad701b6a` (merge of
`ccc268b7c02d46e500bb81a9b2c16d800e2c8db1` and author repair
`e1a57513196be0af1c68ae66d569e8c2d39a2fc1`).

## Reused baseline

The prior independent tally `.r61/d1-review/independent_tally.json` has SHA-256
`a601fcfc022c06a373a339a0e045466c70d644c1fc91736c66e7684b77d4e699` and already
independently reproduced all 42 fields over all 630,990 accepted local C11 public
objects. The product remains:

- product SHA-256 `d9d7f43b090c599d987a3f4957a321d26701b2ee175b8f9cf71ec033588abfc0`
- tally ref `87e297bb8795ae3628603a730c83ca0b90107556236c9e1cb7dba27858722022`
- replay ref `8c7205dc775fd9123ab09985e61b91671f38127e0ae22a6ae3d58e39dfd41b4f`

I did not repeat the expensive full-object oracle. The prior partial focused
stdout (`ff59adcb…`) is treated as external partial evidence only; it stopped
after initial evidence reads and produced no final focused disposition.

## D1-D01 — held authority refusal: PASS

Independent call through the existing owner:

```text
materialize_public_object -> AuthoritySnapshot (DEFER)
require_positive_authority -> Pre553AuthorityError
```

Actual authority: `R157-SRC04-R157_MAP_SOURCE_CODE_TOKEN_IDENTITY`,
`NATIVE_CANONICAL_MAPPING_HARMONIZATION`, state `DEFER`, on the same accepted
release `fc111cfa…`. Result: **REFUSED**, matching the author evidence. This is
not a local dummy and no I03/I05 fact was manufactured.

## D1-D02 — clean checkout primary/replay: PASS

A clean archive was made with `git archive HEAD`. It contained the committed
grant (`f51de878…`) and program (`9e292a10…`) copies and no author-private
`.r61` runtime dependency.

```sh
PYTHONPATH=. python3 campaign_d1_src04_tally/run.py --mode primary
PYTHONPATH=. python3 campaign_d1_src04_tally/run.py --mode replay
PYTHONPATH=. python3 -m pytest campaign_d1_src04_tally/tests -q -o addopts=
```

Results:

- primary: exit 0, `PRIMARY_TALLY_COMPLETE`
- replay: exit 0, `COLD_REPLAY_COMPLETE`
- tally ref match, replay ref match, 42/42 field counts match
- tests: **9 passed in 114.56s**

## D1-D03 — mutated receipt_override refusal and restoration: PASS

Independent mutations through the Campaign D1 adapter:

| Mutation | Result |
|---|---|
| `source_sha256` | REFUSED — `SOURCE_IDENTITY_MISMATCH` |
| `source_release_manifest_hash` | REFUSED — `SOURCE_RELEASE_MANIFEST_MISMATCH` |
| `replay_manifest_ref` | REFUSED — `RELEASE_REPLAY_MANIFEST_MISMATCH` |
| `release_ref` | REFUSED — `RELEASE_IDENTITY_MISMATCH` |

Restoration with normal `build_tally()` matches the unchanged product document
and file (`d9d7f43b…`); tally and replay refs are unchanged.

## Integrity

- `RETURN.json` SHA-256 `f2597972e8ecff7491174aa2746cef53d05f03875a03920310ea96961dd34054`
- 27/27 `artifact_manifest` entries match actual files.
- Source: SRC04 `2a48ba4b…`, 7,337 records, 181 columns, 42 accepted fields.
- Event presence 308,154; observed response 298,819; substantive 277,582;
  DK 14,784; source-specific special 6,453; missing 9,335.
- `ROUTING_UNKNOWN`; canonicalization `WITHHELD_DEFER_NO_SCIENTIFIC_ALLOW`;
  zero canonical values, zero weight facts, no population/eligibility claim.
- Only aggregate counts and exact refs are committed; respondent-level objects
  remain local. No original SAV was reread by D1.

## Acceptance and limits

Affected criteria D1-C08, D1-C09 and D1-C12 now **PASS**. The previously accepted
42-field product and its descriptive counts remain unchanged. Bounded grade:
**D1_OBSERVED_SAMPLE_DESCRIPTIVE_TALLY_ACCEPTED**.

This is not M2/M3, F1–F4, N11/N12, or an issued I03 `EmpiricalFact`; a properly
issued I03 positive remains a separate future obligation, not a gate for this
typed D1 tally. No new authority, canonical, weight, population, directional or
structural claim is made.
