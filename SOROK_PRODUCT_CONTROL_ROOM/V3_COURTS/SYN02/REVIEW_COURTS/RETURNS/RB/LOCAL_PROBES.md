# RB independent sourcefree probes

**Date:** 2026-10-27. **Targets:** SYN02-B `d8f8b4f7610a4a28d86cf6d0c08f5d297d74d6e3`; SYN02-D `f904955e1c6f4db2d7fdebf8d2a6b78029274a5f`. **Surface:** local macOS author worktrees, read-only; `PYTHONDONTWRITEBYTECODE=1`, `python3 -B`, `pytest -p no:cacheprovider`. No provider/model call, source edit, production edit or raw respondent data.

## P1 — SYN02-B 59 source identities and S50

```text
B SOURCE_PLANE_IDENTITIES: 59 declared paths; 59/59 SHA-256 exact; 0 missing/mismatch.
S50 selected manifest: 31/31 exact.
Local staging zip: 3f2c5ed925273153a4f300f75e54524729f0b4fef9974957be1f3cd887c91289
TD-R05 archive:  953c9149bd03877206e3cb440d1f4db35dea6473af30b97fd23b7e76c6fc0086
```

Whole-archive identity is not claimed; file-level identity is exact. B's caveat is correct.

## P2 — SYN02-D 116 sourcefree tests

Run from the author-worktree source roots, with the exact author test files:

```text
S44 + S45 tests: 31 passed in 81.88s
S46 + S47 tests: 34 passed in 107.48s
S48 tests:       12 passed in 8.90s
S49 + S51 tests: 26 passed in 45.81s
S52 tests:       13 passed in 53.29s
TOTAL:          116 passed, 0 failed
```

The counts match SYN02-D's receipt exactly. These are sourcefree test-only suites; no native C12/C11/A5.

## P3 — D key source hashes/imports

Verified SHA-256 for S37 producer/session/product, S36 pipeline/transaction/response_rules/target_rules, S42 session, S44 session/root, S45 session, S46 session/producer, S47 session/conditioning, S48 session/sources/product, S49 session/actor, S51 session, S52 session, PRE-MAIN C0/C11/Route B/source-local/SDTF. They match D's table. Exact values are in `INDEPENDENT_EVIDENCE.json`.

`S52.bootstrap.roots()` executed and returned S52/S51/S49 author paths plus the hardcoded:

```text
/Users/matthewsmith/Desktop/Rawlsing/rawlsing-r31j/WORKER_RETURNS/SOROK-20261021-R31J-GM01-PREC9-SOURCE-PERSON-R1/candidate/vendor/bp2/vendor/g18
```

This confirms D's portability defect. No source was modified.

## P4 — M26 literal derived write vs pure invariant

Sourcefree probe on `v3/core/derived.py` / `v3/core/state.py`:

```text
before compute_all_derived: registers={"public_expression_gate":50,"private_expression_gate":50,"inner_load":50}, metabolic_style={}
after  compute_all_derived: registers=same object values, metabolic_style={"current":"compartmentalizing","trend":"stabilizing"}
protected six derived names present as stored keys: []
```

Result: `compute_all_derived` still writes `state.metabolic_style` and `state.registers`; `assert_no_derived_fields_in_backbone` checks only six names. The **pure-derived invariant** is real; the **literal function** is not reusable unchanged. This is the basis for the RB correction to B's M26 `REUSE`.

## P5 — M29 immediate render vs M19/M30 later prose-to-psyche

```text
backbone hash before render_year: unchanged after render_year: true
warm prose + raw process:   narration_support.warmth=30, aperture=55.0
neutral prose + raw process:narration_support.warmth=20, aperture=54.0
warm prose + no process:    narration_support.warmth=30, aperture=50.0
```

Result: direct `render_year` is immediately nonmutating; the later `update_metabolization_and_plasticity_step` reads previous `rendered_output` and changes psychological capacity only with a raw/working process. RX03's severed-reader probe (monkeypatch `_analyze_narrative_for_support_quality` to constant (50,50,50)) removes the warm/neutral difference. This is historical source behavior, not native person evidence.

## P6 — D current path checks

- `ResponseRuleRegistry.production()` has `DEFAULT_ISSUED_RESPONSE_RULES = MappingProxyType({})`; `TargetRuleRegistry.production()` likewise empty.
- S37 `stage_s36` uses `TEST_ONLY_S37_CAN008_A` and requires `NO_CHANGE`/`NO_PROPOSAL`/zero target rows.
- S48 `candidate_specs()` returns `[]`; `issue_current_source()` raises `SOURCE_OWNER_HOLD`; `run_turn` accepts one source event and rejects `len(prospective)!=1`; `self_account` produces `SCI05_HOLD`.
- S49 `root_b_sources()` returns `[]`; controlled source is `PRIOR_B_REFUSAL`.
- C12 store has branch/episode/world_event/perception/checkpoint tables only; no actor-state/functional-organization table.
- S52 `verify()` contains `if getattr(self,"_OPENING",False) and base_ok: r["ok"]=True`; the existing tests do not exercise `base_ok=True` plus an S52-only error.
- No S37/S52 import of `pre553_*` or `source_backed_positioned_subject_possibility` was found; C0/C11 are implemented resources but disconnected from this C12 path.

## Limits

All results are sourcefree engineering evidence. No native C12/C11/A5, no empirical psychology, no production adoption, no source/actor/Pyat/CAN/ADP grant.
