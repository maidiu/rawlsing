# PYAT1002 — historical SRC04 / SRC17 evidence is fixture-grade, not a current source grant

**Historical cut inspected:** `1924499ef52403a0f331b8aff9b7c7eff99bf1e2`  
**Current use grant located:** none

The issue1002 brief calls the inherited SRC04/SRC17 positives "dated evidence"
and explicitly says they are not automatic new permitted source reads. The
inspection here confirms the more specific limit: the surviving `PASS`
artifacts are **nonrespondent fixture releases**, not original respondent
execution. They cannot be promoted into an original35 source-positive, a
current host/purpose permission, or a scientific claim.

## SRC04 — Arab Barometer Wave I

Artifacts inspected:

- `source_pre553_validation/SRC04/VALIDATION_RESULTS.json`
- `source_pre553_validation/SRC04/manifest.json`
- `source_pre553_validation/SRC04/EXCEPTIONS.json`

Exact facts:

1. `VALIDATION_RESULTS.json` has a call
   `"static original routing recipe validation"` whose input is
   `"ORIGINAL_SOURCE config (not physically expanded)"`, and the result records:
   - `"physical_row_expansion": "NOT_PERFORMED"`
   - `"typed_state": "ROUTING_UNKNOWN"`
   - `questions: 178`
   - `routing_entries: 178`
2. The positive release is from a separate fixture:
   - `fixture_id: "R157-ARAB-SRC04-NONRESPONDENT"`
   - `row_count: 8`
   - `fixture_source_sha256: "506d92179dcb76a3b1d5e0710d95472fa20313fcaf8b77cb6f548924c6e5d51b"`
   - release object id `"R157_FIXTURE_RELEASE/SRC04"`
3. The manifest states `physical_slots_total: 181`,
   `physical_slots_included: 181`, `items_total: 181`, `items_included: 181`,
   but this is a **fixture release** at
   `"R157_FIXTURE_RELEASE/SRC04"`, not an original respondent read.
4. `EXCEPTIONS.json` records that the portable recipe declares
   `row_selector=ALL` with typed routing `ROUTING_UNKNOWN` for every produced
   routing fact; it "does not invent eligibility, forms, populations or
   permissions." It also records:
   - no exact form/ballot/administration variable;
   - no source-native respondent key beyond physical row ordinal;
   - a source weight slot exists, but no exact design/estimand authority;
   - signed/canonical direction is not certified by the preparation.

Conclusion for SRC04: the inspected `PASS` is a **fixture positive** and source
preparation evidence. It is not an original respondent positive and it does not
establish current source-use permission.

## SRC17 — GSS 1973

Artifacts inspected:

- `source_pre553_validation/SRC17/SRC17.manifest.json`
- `source_pre553_validation/SRC17/SRC17.validation-results.json`
- `source_pre553_validation/SRC17/SRC17.exceptions.json`

Exact facts:

1. `SRC17.manifest.json` has a `limits` list with these exact statements:
   - `"Original GSS respondent execution is NOT performed or claimed."`
   - `"The positive native release is from a distinct nonrespondent fixture
     config and fixture bytes."`
   - `"Original construction requires permitted decode-produced row_native_keys
     and remains P3 reader/transport work."`
   - `"No cross-wave equivalence, pooling, canonical mapping, weight
     authorization or population claim is asserted."`
2. The native release is `"R157_GSS_FIXTURE_RELEASE/SRC17"`; the fixture source
   SHA-256 is `e85b8fc3d9c11f14bf123f32fdfea5bda3b6d37a99a0f7225cd827638c517805`,
   distinct from the original source SHA
   `59e65801dc26818bbcf15f9ed985cf8f1faafa65a3eb59e2d3180a7b13a5c1c2`.
3. `SRC17.validation-results.json` records:
   - 339 physical slots/items total;
   - 279 response-bound items;
   - 60 held items;
   - held roles: `ADMIN: 5`, `CONTINUOUS: 51`, `COORDINATE: 2`,
     `ROW_KEY: 1`, `WEIGHT_HELD: 1`.
4. `SRC17.exceptions.json` records:
   - `SRC17-NATIVE-ROW-KEY`: `DECODE_REQUIRED`;
   - `SRC17-ROUTING-UNKNOWN`: `ROUTING_UNKNOWN`;
   - `SRC17-SOURCE-AUTHORITY-DEFER`: `DEFER`;
   - `SRC17-CANONICAL-VALUE`: `NOT_AUTHORIZED`;
   - `SRC17-WEIGHT-HELD`: `HELD`;
   - `SRC17-FORM-ADMINISTRATION`: `UNKNOWN`;
   - `SRC17-SAMPLE-FRAME`: `UNRESOLVED`;
   - `SRC17-CONTINUOUS-NATIVE-FINITE-RULE` and
     `SRC17-ADMIN-NO-RESPONSE-SLOT` remain held.

Conclusion for SRC17: the inspected `PASS` is a **fixture positive**. Original
respondent execution is explicitly not performed or claimed. It is not a
current source grant and cannot support a population, temporal, causal or
original35 scientific claim.

## Why no expiry/revocation was invented

No historical **source-use** grant with or without an expiry/revocation
condition was located. What exists is engineering replay/protocol authority and
nonrespondent fixture authority, which explicitly disclaims source scientific
authority. Therefore:

- there is no historical source grant whose continued scope could be verified;
- there is no expiry to infer;
- there is no revocation to infer;
- the missing item is the current competent source-use grant itself.

This preserves the issue1002 instruction not to invent expiry/revocation when a
historical grant has no such condition. It also refuses the opposite error:
treating engineering/fixture `ALLOW` as a source grant.

## If a separate older original positive exists

The declared read set inspected here contains no original respondent
SRC04/SRC17 positive. If such a dated artifact exists outside this cut, it is
still dated evidence: it must be bound to the exact source SHA, host, purpose,
consumer use, semantic scope, retention/export limits, currentness and
revocation, and to a competent current owner. It cannot be used as a substitute
for the missing grant.

## Exact consequence

Both sources remain:

```text
current_permission.decision = UNKNOWN_OWNER_DECISION
original_respondent_positive = NONE_LOCATED
fixture_positive = NONRESPONDENT_FIXTURE_ONLY
source_native_execution = NOT_RUN
```

The single highest-impact unlock request is for SRC04, because its supported
slice is the smallest existing fixture-positive first-reader candidate and has
no configured weight slot. See `04_ONE_HIGHEST_IMPACT_GRANT.md`.
