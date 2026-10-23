# R61-R08V R8 independent review — defects

## No remaining scoped defect

R7-AF-01 is verified closed. The R8 code/test delta is limited to
`EvidenceResolver._replay_cache` and one author test addition; no schema,
descriptor, envelope, admission, live-producer or native-owner change.

### Verified closure

- Legacy `trusted_binding_hashes=("a"*64,)`:
  live first resolve `SUPPORTED` 60; cache-hit second resolve `UNKNOWN` /
  `LEGACY_BINDING_PINS_REQUIRE_MIGRATION`; no support.
- Wrong `trusted_descriptor_hashes` on a cache hit:
  `UNKNOWN` / `CACHE_OWNER_DESCRIPTOR_NOT_PINNED`; correct descriptor pin
  imports/reads 60.
- Missing verifier on a cache hit:
  `UNKNOWN` / `NO_CONFIGURED_TRUST_ROOT`.
- Genuine stale/unauthoritative cache state:
  `UNKNOWN` / `STALE_OR_UNAUTHENTICATED_CACHE`; no support.
- Import/export retain explicit `LEGACY_BINDING_PINS_REQUIRE_MIGRATION`.

Probes:
`probes/test_r08v_r8_targeted_refusal_codes.py` (5/5) and the R7 successor
legacy/descriptor probes now pass 76/76. Observed values are in
`outcomes/r8_targeted_observations.json` and
`outcomes/r7_successor_observations.json`.

No crash/import/setup error is counted as a refusal. No forged owner,
admission, root, live producer or wrong measurement was found.

## Retained regression accounting

- Author suite: 126/126.
- R7 successor independent probes: 76/76.
- R7 semantic adapters: 3/3.
- R6 immutable replay: 9 pass / 2 removed-transport/local-label superseded.
- R5 immutable replay: 6 pass / 2 old grade/import superseded.
- R4 immutable replay: 7 pass / 2 lawful `EvidenceAssociationError`.
- No copied archived probe was edited.
