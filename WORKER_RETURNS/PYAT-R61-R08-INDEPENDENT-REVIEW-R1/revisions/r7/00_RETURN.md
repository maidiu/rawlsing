# R61-R08V R7 independent review — return

Verdict: **REVISE (bounded diagnostic/refusal-code defect only; no measurement
or ownership bypass found).** The R61AF canonical read-only owner descriptor is
present and independently holds across all thirteen owner classes, descriptor
pins, no-admission transport, native positives, verifier-only re-export and cold
replay. One configured-restriction path still loses its explicit typed migration
code: with nonempty legacy `trusted_binding_hashes`, import/export raise
`LEGACY_BINDING_PINS_REQUIRE_MIGRATION`, but a `resolve` cache hit collapses the
same configuration to `UNKNOWN` / `STALE_OR_UNAUTHENTICATED_CACHE`. No support is
served; the defect is that the primary resolve path does not return the explicit
migration/configuration limit required by R61AF.

## Custody actually checked

- Exact stable root: `/Users/matthewsmith/Desktop/Rawlsing_Worktrees/r61-r08v-r4`;
  branch `agent/opencode-pyat-r61-r08v-r7-independent-review-r1`; preflight
  `pwd`/toplevel/branch/status matched and the tree was clean.
- Candidate/startup: `ea39bd324d297a93bb9e87ede9b9da75dfa8750a`.
- Code commit: `992236d245e165dcf5842411ad0a4733433fd7de`.
- Module blob `00312f84afa5677c94193cefd94cdfd951f05222`; test blob
  `0dae12308157735f188bc11163a224229563d8a4` (working tree matches).
- Frozen R7 EXPECTATIONS:
  `17484296abb50e2f24775db53d7765cdbe10dab1`, committed before R7 candidate
  code or author conclusions.
- Prior R6 review `c42b4abee4e54340659ec6b1f8f6760dfbef9411` is primary
  regression/oracle; R5 `4a5d9a9f8...` and R4 `d1baa92...` preserved. Their
  probes were replayed from exact copies and no archived original was edited.
- Candidate delta `6abd49f..ea39bd3` is exactly the two R08 code/test paths plus
  the author R7 return root; the precode contract/fixtures/harness are author
  return material. No native owner/evaluator/archived/HQ/other-node edit.
- Author R7 manifest independently recomputed: all 14 listed artifacts match
  byte-for-byte; `manifest.json` explicitly self-excludes.
- Direct remote readback at start: R7 branch at candidate `ea39bd...`.

## Fixture/harness verification

The extracted fixtures were verified against candidate startup `ea39bd...` and
the original repository blobs:

- R2 `02_VALUE_RELATION_ORACLE.json` blob `c6acafae...`, 14199 bytes, SHA256
  `b8a29223...`;
- R2 `03_SYNTHETIC_AUTHORITY_FREEZE.json` blob `333989fa...`, 16335 bytes,
  SHA256 `ae159afe...`;
- R2 `04_SLICE_PROJECTION.json` blob `8e5bd3d2...`, 7195 bytes, SHA256
  `bab72ceb...`;
- R3 `02_OWNER_NATIVE_AUTHORITY_SCOPE_FREEZE.json` blob `5d1583dc...`, 12394
  bytes, SHA256 `838c76dd...`;
- R8 `04_CURRENT_AT07_IDENTITY_SPINE.json` blob `462bb282...`, 5683 bytes,
  SHA256 `a4416c48...`.

All extracted blobs equal the original startup blobs. The harness
`sitecustomize.py` only rebinds the native fixture path constants to the
extracted fixture root; it does not patch implementation, evaluator, provider,
native semantics or expected oracle. Author 126/126 was reproduced with this
harness; the initial setup failure remains facility evidence, not qualification.

## What R7 actually establishes

- Cache schema `R61_AUTHENTICATED_EVIDENCE_CACHE@5`; one
  `R61_CACHE_OWNER_DESCRIPTOR@1` with exactly six fields; thirteen owner
  classes; descriptor hash distinct from live `binding_hash`; no
  `producer_binding` or admission in new-format cache.
- Independent positive from the pinned AT07 rows: `yes=54`, `no=6`,
  denominator 60; changed source law `yes=54`, `no=16`, denominator 70; actual
  observed zero (60, `no=0`), actual ZERO_SUPPORT (0), VALID_NULL/DIFFUSE/
  VALID_EMPTY/OBSERVED_ZERO, typed bool/int/null, currentness and Z UNRESOLVED16
  controls retained.
- Independent table-driven inventory: all 13 owner classes mutate/remove/
  duplicate/type-alias; public descriptor/seal recomputation; import/read/
  re-export/second-import refuses; pristine baseline restores 60. Trusted
  synthetic signed owner-envelope disagreements for all 13 classes refuse.
- Unknown/admission fields at descriptor/owner/entry/envelope boundaries refuse;
  descriptor hash/owner hash/schema shapes refuse; legacy @4/@3 schemas refuse.
- `trusted_descriptor_hashes` are distinct and enforced on import/export/replay;
  legacy `trusted_binding_hashes` import/export raise
  `LEGACY_BINDING_PINS_REQUIRE_MIGRATION`.
- Missing live producer pin call count 0; verifier-only import/read/re-export/
  second import never invokes a producer; original envelope signature and signed
  provenance preserved; cold process 60 with separate stdin key; no local
  unsigned delivery label in qualified output.
- Author suite 126/126. Independent R7 probes: 75 passed, 1 failed (the legacy
  cache-hit refusal code below). R6 immutable probe: 9 passed, 2 removed-
  transport/local-label superseded expectations; semantic adapters for both
  invariants pass 3/3. R5: 6 pass, 2 superseded old grade/import expectations;
  R4: 7 pass, 2 lawful `EvidenceAssociationError`. All outcomes accounted.

## Remaining defect

### R7-AF-01 — legacy binding-pin cache replay loses the explicit migration code

Location: `EvidenceResolver._replay_cache`
(`rawlsing_next/pre553_universal_evidence_binding.py`). It calls
`_check_cache_configuration()`, which correctly raises
`EvidenceCacheIntegrityError("LEGACY_BINDING_PINS_REQUIRE_MIGRATION")`, but the
broad `except (Pre553IntegrityError, ...)` converts it to
`_result_refusal(request, REFUSAL_STALE_CACHE)`.

Reproducer
(`probes/test_r08v_r7_independent_boundary.py::test_legacy_binding_pin_cache_replay_has_explicit_migration_code`):

1. `resolver = _resolver(trusted_binding_hashes=("a"*64,))`.
2. Bind the canonical request and resolve once: `SUPPORTED`, 60 (live execution
   is not a cache operation).
3. Resolve the same request again (cache hit): observed `UNKNOWN` /
   `STALE_OR_UNAUTHENTICATED_CACHE`; expected explicit
   `LEGACY_BINDING_PINS_REQUIRE_MIGRATION` per R61AF/R7 contract.
4. No support is served; import/export already return the explicit code.

Observed JSON: `outcomes/r7_observations.json` key `legacy_pin_cache_replay`.

Minimal missing function: preserve the explicit
`LEGACY_BINDING_PINS_REQUIRE_MIGRATION` (and, consistently, the distinct
descriptor-pin refusal) through `_replay_cache` rather than collapsing every
cache integrity error to `STALE_OR_UNAUTHENTICATED_CACHE`; add a resolve-path
assertion for the configured legacy pin.

This is a diagnostic/configuration-limit gap, not a wrong-measurement,
forged-owner, admission, live-producer or root-retention defect. The scoped
trust boundary otherwise holds.

## Limits

- `trusted_descriptor_hashes` wrong-pin replay likewise reports generic
  `UNKNOWN`; import/export report `CACHE_OWNER_DESCRIPTOR_NOT_PINNED`. The
  contract requires enforcement on replay (it is enforced, no support) but does
  not name a distinct replay code.
- Full live J42/P41/E04 integration remains NOT_REACHED and future-owner work.
- No original data/science, source rights, production/CI, N11/N12, F6/F7/F8,
  actor, Sorok, J52/W52, R03/R09 or protected-capture authority is claimed. No
  adoption, author wake, candidate edit or new session.

Artifacts: `EXPECTATIONS.md` (frozen), `defects.md`, `limits.md`, `RESUME.md`,
`FACILITY_HISTORY.md`, `proof_witness.json`, `SHA256manifest.json`,
`outcomes/r7_observations.json`, `outcomes/r7_semantic_adapters.json`,
`outcomes/r4/r5/r6` probe replay observations, `probes/*`, `junit/*.xml`,
`logs/stdout.jsonl`.
