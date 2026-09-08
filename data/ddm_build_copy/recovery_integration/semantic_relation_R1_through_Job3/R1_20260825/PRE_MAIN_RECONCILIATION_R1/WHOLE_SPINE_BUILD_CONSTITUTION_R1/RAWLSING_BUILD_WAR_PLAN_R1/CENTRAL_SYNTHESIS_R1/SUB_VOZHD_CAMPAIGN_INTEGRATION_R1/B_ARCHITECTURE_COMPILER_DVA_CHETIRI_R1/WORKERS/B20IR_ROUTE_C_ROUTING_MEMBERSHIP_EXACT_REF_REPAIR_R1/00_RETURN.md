# B20IR RETURN — ROUTE C ROUTING-MEMBERSHIP EXACT-REF IMPLEMENTATION REPAIR R1

Status: **PASS — IMPLEMENTATION REPAIR SCOPE ONLY**

Terminal:
`B20_ROUTE_C_ROUTING_MEMBERSHIP_EXACT_REF_NORMALIZATION_REPAIR_COMPLETE__READY_FOR_B20Q2_FULL_QUALIFICATION`

Branch:
`agent/rabochii-subv-b-as4i-route-c-routing-membership-exact-ref-repair-r1`

## Authoritative repaired implementation

Commit:
`9a98bc8b52f5fb5088afbe86f7917351091ee216`

Implementation:
- Git blob: `abfdc91a71ef5e18c4a8a6bf62fa65750d8d9889`
- SHA-256: `a07e73c514c6216c350ac7a69cb099256cf71680a49fe0796aac6729483b417d`

The already repaired B20 driver remained unchanged:
- Git blob: `5377c70b5b3b9110cfd719b62ae1c3e2ceb07843`
- SHA-256: `73d9d9efd5bf70a181a7ddac3d98a5e8f7a90277765945862c402b4656c67350`

## Exact repair

Within `_routing_membership()` only:

- `fact.scoped_respondent_ref` is normalized with repo-native `exact_ref(...)` before tuple/dict-key use;
- `fact.question_or_target_ref` is normalized with `exact_ref(...)` before tuple/dict-key use;
- `fact.risk_set_ref` is normalized with `exact_ref(...)` before set/common-risk comparison.

No qref construction, routing fact, routing state, common-risk law, CACC1 layout, CACC2, query, discovery, or parity semantics changed.

## Repair-history note

The first implementation commit `f089f8e…` encoded literal `\\n` text into the new tuple expression and was syntax-invalid. That was a mechanical serialization error in the authorized repair itself, not a Rawlsing semantic defect. It was corrected without widening scope.

The authoritative corrected repair is `9a98bc8…`, committed before the authoritative smoke.

## Authoritative smoke

GitHub Actions run:
`34279192861`

Exact executed tree:
`9a98bc8b52f5fb5088afbe86f7917351091ee216`

Environment:
- CPython 3.13.15
- pyarrow 25.0.1
- pandas 3.0.5

Exit code: `0`

The smoke proved:
- repaired driver fixture completes;
- `_routing_membership()` completes;
- first CACC1 build enters and completes;
- 3 rows materialized;
- CACC1 logical hash `e683af11b8c3ae9f7ee897c4f6c5080cfefc8d2bd9636624678a3b0205919a2c`;
- CACC1 physical-byte SHA-256 `5f70745f40fe8b21b7bcde8892a17b8f3fd62fdca1111af73c3fba3734d9b2c7`.

B20IR does **not** claim Route-C qualification PASS. The next lawful court is B20Q2, consuming both the repaired driver and repaired implementation.

Zero C09, zero WVS7, zero common harness, zero ranking, zero OBL037, zero architecture selection, zero positive V3.
