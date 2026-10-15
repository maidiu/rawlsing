# HQ300 — DISC_01 detector correction (RSM finding)

**Defect (RSM `00f5d9a66f5f641c1f88376994272bc570a625ef`, §2):** HQ298 SM's
`test_B_no_can008_coupling_rule_exists_in_runtime_modules` asserted `hits == []`
for any file under `rawlsing_next/` (excluding `tests/`) containing the *tokens*
`CAN008`, `CAN_008`, `coupling_rule`, `response_rule`, `V3ResponseEvaluationReceipt`
or `PRESSURE_FLOW`. RSM grade: `TEST_SCOPE_NOT_CLAIM`, severity LOW.

**Why it is a defect:** a whole-repo text scan conflates *string-constant mentions*
with *implementation surface*. In the full estate two files mention CAN008 strings
without implementing anything:

| File | Token | Actual kind |
|---|---|---|
| `rawlsing_next/gt34_obl031_q69b_comparator_resolver_r2.py:113` | `PSEPF_V3_MUTATION_METABOLISM_CAN008_V2` | denylist identifier constant in a list of rejected identifiers |
| `rawlsing_next/gt34_adp010_input_authority_acceptance.py:44` | `NO_CAN_008` | rejection-code string constant |

Neither is a coupling/response rule implementation. RSM's precise
implementation-surface scan (`class`/`def` names for coupling/response-rule/
owner-effect/target-effect/transition-producer) across the same tree finds **0
hits**. The substantive absence claim is correct; the *detector* was overbroad
and stage-scoped rather than estate-scoped.

## Correction applied (this commission)

1. **Detector tightened to implementation surface.** The reproduced court's
   detector now matches `class`/`def` declaration names only
   (`coupling|response_rule|owner_effect|target_effect|transition_producer|
   coupling_rule`), never bare tokens. Same correction class applied to the
   effect-vocabulary detector (implementation surface, not string presence).
2. **String mentions classified, not conflated.** The two known estate mentions
   are recorded with their classification (denylist identifier constant;
   rejection-code string constant) and asserted to be non-implementations
   (`test_G_disc01_string_mentions_are_denylist_codes_not_implementations`).
3. **Scope declared.** The corrected detector runs over the blob-verified staged
   closure; the new HQ300 court additionally asserts
   (`test_G_disc01_corrected_detector_production_surface_zero`) that the
   production surface has **0** implementation hits, and
   (`test_G_candidate_implementation_surface_is_confined_to_candidate_package`)
   that the only implementation surface that exists after this commission is the
   worker candidate package itself — never `rawlsing_next` production modules.

## Effect on results

| Suite | Before correction | After correction |
|---|---|---|
| RSM-reproduced HQ298 court (60 cases) | 59 PASS / 1 FAIL (DISC_01 overbroad scan fails in fuller trees) | **60 / 60 PASS** (`junit/rsm_court_junit.xml`) |
| Substantive absence claim | correct | correct (unchanged) |
| Earliest HOLD | `MISSING_IMPLEMENTATION` | unchanged |

**Non-claim discipline (restated):** text-match absence across a repo is never
evidence of producer absence. Producer absence is established by (a)
implementation-surface scan, (b) the imported zero-positive guard probe
(`DENY_ZERO_EFFECT / ZERO_POSITIVE_REGISTRY`), and (c) the GT0 blocked-path
probe (`BLOCKED_POSITIVE_ACTOR_PATH__SEMANTIC_CONSERVATION_PASS`).

## Files touched

- `rsm_court_reproduction/test_owner_effect_court.py` — vendored from HQ298 SM
  blob `65acd6be6361…` (29,727 bytes; header note added, detector-only patch).
  All non-detector assertions are byte-preserved.
- `rsm_court_reproduction/owner_effect_stub_TEST_ONLY.py` — unmodified vendored
  copy (blob `440eb1719553…`).
- `01_PREDECLARED_POSITIVE_CELL_AND_ARMS.json` — unmodified vendored frozen
  predeclaration (blob `d96941c66cf9…`), required by the court at `../`.
