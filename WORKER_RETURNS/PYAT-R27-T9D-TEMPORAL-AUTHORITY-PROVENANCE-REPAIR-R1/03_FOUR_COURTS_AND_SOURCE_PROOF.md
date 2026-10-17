# R27 T9D — court execution and source proof

Runtime (measured, not asserted): `/usr/local/bin/python3`, CPython 3.11.3,
pytest 9.0.2, pandas 2.3.1, numpy 2.3.2, macOS. Every court ran in its own
fresh process through `guarded_runner_t9d.py` with `PYTHONDONTWRITEBYTECODE=1`,
`-B`, `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1`, plugin autoload disabled, explicit
`--rootdir`/`-c` config, per-import git blob SHA-1 (NUL preimage) verification
before execution, and full module receipts after execution. Real JUnit XML and
literal process exits; no result is synthesized.

## Source proof (actual SHA / NUL preimage)

- Staged V553 closure: **22 Python files, all byte-identical** to the T9C
  return's native closure and to the accepted originals. Per-file sha256 and
  `git_blob_sha1_NUL_preimage = sha1(b"blob <len>\0<bytes>")` are recorded in
  `06_EVIDENCE_FILE_HASHES.json`.
- Frozen transports are **byte-identical to their origin bytes** (verified
  pairwise against the T9C/T9B/T9R trees and the T9I court):
  `test_independent_clock_custody.py` (T9I court), `test_t9c_repair.py` +
  `01_SEVEN_DEFECT_CONTRACTS.json` (T9C), `test_t9b_temporal.py` +
  `01_PREDECLARED_SERIES_CLOCK_ORACLE.json` + `evidence/native_source_ledger.json`
  + `evidence/02_real_temporal_to_selected_world_two_times.json` (T9B/T9C),
  `test_t9r_delta.py` + `test_postinspection_hostiles.py` +
  `01B_FROZEN_COUPLED_BINDING_VECTORS.json` (T9R). None were edited.
- Repaired adapter `t9b_temporal.py`: sha256
  `77a4d25d9a6338cf747ca89185790a6d51b0ecbc0c450697a2e30215d92073ef`,
  NUL-preimage blob `d6710868d72d73f0b711224f18c8792c8b666666`. Real diff
  against the T9C adapter is `07_REAL_DIFF_T9C_TO_T9D.patch`.
- Imported project modules at runtime resolve INSIDE this return
  (`staging/pinned_candidate/...`); the ambient repository root is stripped from
  `sys.path`. Per-court `*_module_receipts.json` record `__file__`, sha256 and
  NUL-preimage blob for every loaded project module. No raw SAV/DTA, no private
  survey bytes, no respondent data, no credentials.

## Courts (separate; never pooled into an acceptance percentage)

| Court | Tests | PASS | FAIL | ERROR | SKIP | Exit | JUnit sha256 (prefix) |
|---|---:|---:|---:|---:|---:|---:|---|
| `frozen_t9i_independent_48` | 48 | 47 | 1 | 0 | 0 | 1 | `68d22ce5a7f5c847` |
| `t9c_own_repair_52` | 52 | 52 | 0 | 0 | 0 | 0 | `3bd32941338ca42c` |
| `inherited_original_v553_native_8` | 8 | 8 | 0 | 0 | 0 | 0 | `66ef2005135843ef` |
| `unchanged_t9b_author_28` | 28 | 27 | 1 | 0 | 0 | 1 | `05ddaa31c0e241a9` |
| `t9r_frozen_delta_50` | 50 | 50 | 0 | 0 | 0 | 0 | `edc2a6c113dc897f` |
| `t9r_postinspection_hostiles_7` | 7 | 7 | 0 | 0 | 0 | 0 | `65ab2f24b149a2f5` |
| `t9d_own_authority_provenance` | 22 | 22 | 0 | 0 | 0 | 0 | `61f37702d781f2e7` |

Full JUnit: `junit/*.xml`; stdout/stderr: `logs/*.log`; machine-readable
transcript: `evidence/t9d_seven_court_execution.json`.

### Observed old compatibility failures (explicit, expected, unedited)

1. `frozen_t9i_independent_48 :: test_two_time_original_consumer_and_numerical_products_reproduced`
   — asserts byte equality against the stored two-time artifact and the old
   `1990.opportunity_ids == ['ROUTE_DEFERRED_REVIEW']`. The R5/R7/T9D safety
   repair necessarily blocks that PROBE route and adds typed disclosure fields,
   so the artifact comparison fails. Arithmetic (0.20/0.60), basis, band and
   original provenance values are unchanged. Restoring the unsafe route to make
   the byte artifact equal was explicitly forbidden.

2. `unchanged_t9b_author_28 :: test_hostile_changed_temporal_source_with_same_structural_world_only_moves_the_channel`
   — asserts the two retrospective interpolated reads differ in
   `opportunity_ids`. Both are now correctly `('ROUTE_BLOCKED_NO_SUPPORT',)`
   (their exploratory lists differ). Preserved as historical compatibility
   evidence; no forbidden PROBE route was reopened.

### T9R's seven post-inspection attacks (now 7/7 green, unchanged falsifiers)

| Attack | Observed repaired behavior |
|---|---|
| `TWO_ANCHORS_EMPTY_GRANTS` (M0/M1/M2) | `authorized_opportunity=false`, `opportunity_ids=['ROUTE_BLOCKED_NO_SUPPORT']`, `actor_opportunity_entitlement=WITHHELD_NO_CURRENT_ACCESS_GRANT` |
| `UNUSED_FUTURE_AUTHORITY_UPGRADE` (M0/M2) | basis stays `('W0',)`, product key stays `PROBE_ONLY_TEMPORAL_KEY`, `authorized_opportunity=false`, no open route; W1 only in `archive_context_wave_ids` |
| `LAG_PLUS_RUPTURE` | `pub_lag_of == ('DELAYED',) ⊆ basis`; rupture typed as `rupture_crossed_year=1995` |
| `DUPLICATE_EXCLUDED_BASIS` | `refused_code=DUPLICATE_WAVE_ID_REFUSED` (refused before source filtering) |

### T9R's four unavailable precommitted gates (now 4/4 green)

D04 `ARCHIVAL_KNOWN_AT_BOUND_EXCEEDED` (value None, no basis);
D16 `SOURCE_GRANT_UNAVAILABLE_SOURCE_OR_EDITION_MISMATCH`;
D17 `SOURCE_GRANT_UNAVAILABLE_NOT_CURRENT`;
D17_WRONG_OWNER `SOURCE_GRANT_UNAVAILABLE_WRONG_SOURCE_OWNER`.
Each is an actual candidate call (`trace.actual_candidate_call=true`,
`output_rewritten=false`) through the typed capability API; raw traces in
`evidence/delta_observations.json`. No reviewer-side filter, substituted
refusal or invented gate exists.

## Downstream consumer negatives (executed, not asserted)

Duplicate wave identity; excluded-first/excluded-last source order; basis
source conflict; edition-mismatched grant; wrong source owner; non-current
grant; missing issuer under required claim; empty actor entitlement with two
anchors; future publication beyond an archival snapshot bound; held-product
authority under added future context; rupture carry; missing/NaN/infinite
observation; revoked and archived-nonrenewed sources; contradictory causal
clock; cohort/instrument/country mismatch. All live in
`staging/tests/test_t9d_authority_provenance.py`, the frozen T9R suites and the
unchanged T9I/T9B suites.

## Numerical and epistemic constants (unchanged)

AS_OF 1995 = 0.20 (W0 alone); RETROSPECTIVE 1995 M1 = 0.40
`INTERPOLATED_NOT_OBSERVED`; endpoints 0.20 (1990) / 0.60 (2000); linear slope
1/25 per year; midpoint 2/5; unconditioned identification set [0,1] with
worst-case absolute error 3/5; monotonicity-assumed set [1/5,3/5] with
worst-case 1/5; sampling error UNIDENTIFIED (no sample design or variance
supplied). These are identification bounds, not sampling confidence intervals.
