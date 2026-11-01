# First consumer and executed tests — RRIF-D5

**Scope:** sourcefree Git/source comparison and safe tests only. No raw survey, native P07, protected source, actor, model-use or PRE-MAIN execution.

## 1. Consumer map at current `8e44ca9c75`

| Candidate | Current receiving consumer | Consumer class | Production? |
|---|---|---|---|
| I01 lifecycle | none | UNKNOWN | no |
| N9/N10W progressive | `rawlsing_next/tests/test_pre553_n9_n10w_progressive_candidate.py`; `.github/workflows/pyat-programma-n10w-sourcefree.yml` | TEST_IMPORT + CI | no |
| N9 two-field reader | none | UNKNOWN | no |
| PE generic world | none | UNKNOWN | no |
| R3 seam witness | none | UNKNOWN | no |
| World binding | none | UNKNOWN | no |

Current production import graph relevant to these lineages:

- `pre553_n9_n10w_progressive_candidate.py` imports `pre553_empirical_possibility_provider`, `pre553_analytical_composition` and `source_backed_positioned_subject_possibility`.
- `pre553_empirical_possibility_provider.py` imports `source_backed_positioned_subject_possibility`.
- `pre553_analytical_composition.py` imports `source_backed_positioned_subject_possibility`.
- `pre553_learned_world_composition.py` imports `pre553_learned_product_lifecycle`.
- No production module imports `pre553_learned_world_composition.py`.
- No production module imports `pre553_universal_workload.py` or `pre553_native_workload_binding.py`.
- No current module implements an operative N9 selected-world resolver, N10W world-conditioned owner or a real source/world receiver.

The current E03 test/CI is a real receiver at test scope, not a production receiver. The historical I01 `serve()` is a real function and was tested by an independent reviewer, but it has no current importer.

## 2. Fault matrix

### Wrong world

| Lineage | Observed behavior | Grade |
|---|---|---|
| I01 | foreign release/index substitution is refused; `restore_product` checks the saved subject/checkpoint/index identity and foreign M2 release | negative supported at branch scope |
| N9/N10W | no external world parameter; a caller-supplied foreign mapping produces untyped `KeyError`; no N9 resolver | missing interface |
| N9C | wrong role/ref, misordered relation and registry substitution are refused; the real D2P producer refs are not the reader refs (RED) | local refusal, integration RED |
| PE | fabricated never-issued N9 world marked `SELECTED_IMMUTABLE` is accepted and returns `EXACT_SUPPORTED`; future/invalidated test-world states are refused | limitation: caller-declared world |
| R3 seam | source/release/risk mismatch and protected CURRENT are refused | negative supported at synthetic scope |
| World binding | foreign world source/release, foreign rows, foreign repository and wrong handle/snapshot are refused | negative supported at test scope |

### False historical time

| Lineage | Observed behavior | Grade |
|---|---|---|
| I01 | historical as-of after invalidation computes the exact previous output; cold resume refuses current and does not resurrect | positive at branch scope |
| N9/N10W | no as-of API; synthetic world only | not applicable |
| N9C | as-of before publication refuses; 2022-03-01 is partial only; 2022-07-08 reads two values; malformed/backdated clocks refuse | positive local, producer RED |
| PE | as-of at/after request time returns `FUTURE_TIME_AVAILABILITY_REFUSED`; invalidated current returns `INVALIDATED_CURRENT_REFUSED` | negative supported at test scope |
| R3 seam | no as-of API; synthetic bundle only | not applicable |
| World binding | as-of mismatch and unobserved temporal pair refuse; T0/T1 actual world/route variation is test-only | negative supported at test scope |

### Missing joint/conditional evidence

| Lineage | Observed behavior | Grade |
|---|---|---|
| I01 | progressive bundle evidence substitution is refused; exact denominators 32/16/8 and Y numerators 18/10/6 are checked | positive at branch scope |
| N9/N10W | one-conditioner joint returns typed `E03ProgressiveError`; full three-step chain matches the hand-derived oracle | positive/negative at current fixture scope |
| N9C | two distinct role refs are required; partial is `PARTIAL_TEST_ONLY_NOT_POSITIVE`; missing/refused fields remain in the readset | positive local |
| PE | `MULTI_CONDITION_INTERSECTION` requires at least two conditioners; missing denominator, self-target and unauthorized reverse refuse | negative supported at test scope |
| R3 seam | complete producer cell domain, fraction closure, step geometry and conditions are required; zero denominator and missing condition refuse | negative supported at synthetic scope |
| World binding | at least two world fields, exact joined field values, N10E steps, N10W consumptions and structural routes are required; mixed model/step severance refuse | negative supported at test scope |

### Fixture masquerading as native

| Lineage | Observed behavior | Grade |
|---|---|---|
| I01 | `security_mode=SOURCE_FREE`, `real_current=False`; rehashed artifact with `AUTHENTICATED`, forced source promotion, GT2 claim or protected CURRENT is refused | negative supported at branch scope |
| N9/N10W | 58 synthetic rows, `real_subject=False`, all effects false; test asserts never real CURRENT | negative supported at current fixture scope |
| N9C | `fixture_only=True`, `issued=False`, `real_N9_consumer=False`, no publisher/issuer forgery; real-current claim refused | honest fixture, but not producer lineage |
| PE | `SERVICE_GRADE=CANDIDATE_TEST_ONLY`; synthetic laws; no real-current field; caller can still declare a world selected because no resolver exists | test-only facade, N9 absent |
| R3 seam | `SOURCE_FREE_SYNTHETIC`, `qualified_real_source_value_read=False`, `real_current=False`; protected CURRENT and unissued GT2 refuse | negative supported at synthetic scope |
| World binding | `TEST_ONLY`, `operative_N9=False`, `operative_N10W=False`, `new_issuer=False`; pinned P41 runtime is test-only | test-only, no real receiver |

### Dependency severance

| Lineage | Observed behavior | Grade |
|---|---|---|
| I01 | current B5 lacks `verify_m2_release_subject_exact`; exact I01/selected/seam/durable overlay on current `rawlsing_next` fails `AttributeError`; missing artifact, foreign M2 and rehashed artifact refuse | RED at current integration |
| N9/N10W | selected world, seam, world-conditioned service and universal binding absent; no current dependency edge | missing interface |
| N9C | producer refs and reader refs have zero intersection; `UNKNOWN_EXACT_FIELD_REF`; 7 mandatory REDs; D2P2 repair not implemented | RED at integration |
| PE | fake model use, denominator mismatch, source hash forgery and invalidated world refuse; foreign world refs are not resolved | partial, missing resolver |
| R3 seam | source/risk mismatch, changed producer law under old roots, zero denominator and unissued GT2 refuse; one old test expects the superseded recompute behavior | 50 pass, 1 preserved RED |
| World binding | foreign runtime, step severance, revoked world/empirical, mixed model and foreign rows/repository refuse | negative supported at test scope |

## 3. Exact commands and observed results

Environment: macOS Darwin, Python `3.11.3`, pytest `9.0.2`. The current worktree is the exclusive D5 worktree at startup `8e44ca9c75`. Historical tests were run from `git archive` copies of the exact cuts under `/var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T/opencode/rrif_d5_hist/`; the world-binding tests used a sparse linked worktree at `849a76de`.

### Current E03

```bash
cd /Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat-rrif-d5-world-service-fates-20261031-r1
PYTHONPATH=. python3 -m pytest rawlsing_next/tests/test_pre553_n9_n10w_progressive_candidate.py -q -o addopts=''
# 18 passed in 6.27s
```

### Current owner baseline

```bash
PYTHONPATH=. python3 -m pytest -q \
  rawlsing_next/tests/test_pre553_learned_product_lifecycle.py \
  rawlsing_next/tests/test_pre553_learned_product_release.py \
  rawlsing_next/tests/test_pre553_ee14_selected_current_asof_hq260.py \
  rawlsing_next/tests/test_pre553_analytical_composition.py \
  rawlsing_next/tests/test_source_backed_positioned_subject_possibility.py \
  rawlsing_next/tests/test_pre553_empirical_possibility_provider.py \
  -o addopts=''
# 151 passed in 20.92s
```

### Historical I01

```bash
cd /var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T/opencode/rrif_d5_hist/i01
PYTHONPATH=. python3 -m pytest -q \
  rawlsing_next/tests/test_hq287_i01_sourcefree_world_lifecycle.py \
  rawlsing_next/tests/test_hq292_i01k_typed_selection_restore.py \
  -o addopts=''
# 17 passed in 24.50s
```

Current-owner overlay probe:

```bash
# current rawlsing_next + exact a1dc I01/selected/seam/durable files
PYTHONPATH=. python3 -c 'from rawlsing_next import pre553_i01_sourcefree_world_lifecycle_candidate as I; I.build_product(tempfile.mkdtemp())'
# AttributeError: 'LearnedProductLifecycleExecutor' object has no attribute 'verify_m2_release_subject_exact'
```

This is the exact dependency-severance finding. It is a current API mismatch, not a source-science claim.

### Historical N9C

```bash
cd /var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T/opencode/rrif_d5_hist/n9c
PYTHONPATH=. python3 -m pytest -q tests/test_hq297_n9c_two_field_reader.py -o addopts=''
# 47 passed in 0.12s

PYTHONPATH=. python3 -m pytest -q tests/test_hq297_n9c_two_field_reader.py -o addopts='' \
  -k '2021_observed_not_published or publication_backdate or revoked_field or current_and_operative_clocks or ecological_or_model or relation_self_issued or partial_not_positive'
# 11 passed, 36 deselected
```

The D2R/D2P2 producer-to-reader RED is not repaired by these local tests. It is the principal negative.

### Historical PE

```bash
cd /var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T/opencode/rrif_d5_hist/pe
PYTHONPATH=. python3 -m pytest -q \
  rawlsing_next/tests/test_postastra_pe_generic_world_possibility.py \
  rawlsing_next/tests/test_postastra_pe_fixture.py -o addopts=''
# 21 passed in 3.27s

PYTHONPATH=. python3 -m pytest -q rawlsing_next/tests/test_postastra_pe_generic_world_possibility.py -o addopts='' \
  -k 'negative_future_time or negative_invalidated_current or negative_missing_conditional or negative_new_unit or negative_reversed or negative_fake_model or negative_source_hash'
# 7 passed, 14 deselected
```

Foreign-world probe:

```python
from dataclasses import replace
from rawlsing_next.tests.test_postastra_pe_fixture import law_a_cases, make_n9_world_dependency
from rawlsing_next.pre553_postastra_pe_generic_world_possibility import serve_generic_world_situated_possibility
c = law_a_cases()["multi_binding_parent_context"]
req = replace(c["request"], n9_world=make_n9_world_dependency(tag="foreign-world-never-issued"))
r = serve_generic_world_situated_possibility(
    repository=c["repository"], empirical_query=c["empirical_query"], predicate=c["predicate"],
    authority_registry=c["registry"], release_refs=c["release_refs"], request=req,
    model_rule=c["model_rule"], condition_binding_witness=c["witness"])
print(r.result_state)
# EXACT_SUPPORTED
```

This proves the facade accepts a fabricated caller-declared world. It does not prove a real wrong world would be accepted by a future N9 owner; it proves this facade has no N9 resolver.

### Historical R3 seam

```bash
cd /var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T/opencode/rrif_d5_hist/seam
PYTHONPATH=. python3 -m pytest -q \
  rawlsing_next/tests/test_r3_s02_seam_witness.py \
  rawlsing_next/tests/test_pre553_selected_world_progressive_contract.py -o addopts=''
# 50 passed, 1 failed in 18.85s
# FAILED test_s00c_change_source_owned_synthetic_numeric_values_changes_result
```

Targeted negatives:

```bash
PYTHONPATH=. python3 -m pytest -q rawlsing_next/tests/test_r3_s02_seam_witness.py -o addopts='' \
  -k 'scope_and_risk_mismatch or zero_denominator or false_frozen_s00 or change_source_owned or unissued_real_gt2 or unused_read'
# 5 passed, 1 failed (the same stale positive)
```

The failure is preserved. The S00V3 producer-law binding refuses coherently changed values under old roots; the old test expects recomputation. Do not rename this green.

### Historical world binding

```bash
cd /var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T/opencode/rrif_d5_worldwt
PYTHONPATH=. python3 -m pytest -q \
  rawlsing_next/tests/test_universal_world_binding.py \
  rawlsing_next/tests/test_world_conditioned_progressive_service.py -o addopts=''
# 30 passed, 4 errors in 34.52s
# errors: three test_r06_actual_j42_* plus test_r06r4_context_authority_is_held_in_all_public_wrappers
# cause: sparse worktree lacks the full J42 return/fixture terrain, not a candidate assertion failure

PYTHONPATH=. python3 -m pytest -q rawlsing_next/tests/test_world_conditioned_progressive_service.py -o addopts=''
# 3 passed

PYTHONPATH=. python3 -m pytest -q rawlsing_next/tests/test_universal_world_binding.py -o addopts='' \
  -k 'not actual_j42 and not context_authority'
# 27 passed, 4 deselected

PYTHONPATH=. python3 -m pytest -q rawlsing_next/tests/test_universal_world_binding.py -o addopts='' \
  -k 'r110_foreign_world_identity or r110_empirical_revocation or r115_world_rows_hash or r115_world_source_repository or r117_mixed_prefix_model or r06r3_actual_step_severance or r107_refuses_wrong_handle'
# 7 passed, 24 deselected
```

## 4. What the tests establish

- The current E03 fixture is reproducible and correctly disclaims N9/N10W.
- I01 was a real sourcefree product at its branch cut, but current B5/M2 severance prevents current execution.
- N9C's local reader math and as-of refusals work, but its producer-to-reader lineage is RED.
- PE's test-only facade works at its declared scope, but its world is caller-declared and unresolved.
- The seam works at synthetic scope with one preserved stale positive.
- R117 works at scoped software level but depends on a branch-only P41 runtime and has no real receiver.

None of these tests establishes original source science, N9/N10W/N11/N12 issuance, a real person/world receiver, or production adoption.
