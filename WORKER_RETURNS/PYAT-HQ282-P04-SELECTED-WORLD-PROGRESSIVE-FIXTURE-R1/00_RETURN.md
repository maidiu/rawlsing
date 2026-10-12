# PYAT HQ282 P04 — Source-free selected-world → progressive-consumer contract

**TERMINAL:** `PYAT_HQ282_P04_RESOURCE_AWARE_ISSUED_COMMISSION_ONLY__MUST_BIND_ACTUAL_EXECUTION_RESOURCE__NO_SELF_ADOPTION`
**RESULT:** `PASS__BOUNDED_PRODUCT_REAL_OWNERS__24_TESTS_PASS__SELECTED_WORLD_CONTRACT_BINDS_E03_CHAIN__N9_N10W_G0B_ABSENCE_TYPED_HOLD__SOURCEFREE_ONLY__NONISSUING`

**Branch:** `agent/rabochii-pyat-hq282-p04-selected-world-progressive-fixture-r1`
**Sealed startup (verified before mutation):** `91169010041f9c2ee79a6bc1426a2a7901d9677c`
**E03 candidate (reused):** `0e0ed50dbce2dd1434d3a3c84b937b9a956adba9`
**Authority:** HQD-2026-10-10-280; canonical `a70a069fa948e0f3c041b389edcc732b6b948a4f`; semantic PRE-MAIN `1f47063c3205a45888b3c55e81e7485943ed1390` (**unmutated**).

## 1. What was built (new files only — zero owner edits)

| File | Role |
|---|---|
| `rawlsing_next/pre553_selected_world_progressive_contract.py` | the selected-world contract candidate (`PYAT_HQ282_P04_SELECTED_WORLD_PROGRESSIVE_CONTRACT@1.0.0`) |
| `rawlsing_next/tests/test_pre553_selected_world_progressive_contract.py` | 24 tests |
| `rawlsing_next/pre553_n9_n10w_progressive_candidate.py` | E03 candidate (reused from `0e0ed50db`) |
| `rawlsing_next/tests/test_pre553_n9_n10w_progressive_candidate.py` | E03 tests (reused from `0e0ed50db`) |
| `WORKER_RETURNS/…/repro/p04_evidence_recorder.py` | evidence recorder |
| `WORKER_RETURNS/…/repro/p04_evidence.json` | recorded evidence |

No existing owner was edited. The E03 candidate and its tests were brought in from the E03 commit unchanged.

## 2. The selected-world contract

`SelectedWorldContract` is a frozen dataclass that binds:
- `contract_id` — `PYAT_HQ282_P04_SELECTED_WORLD_PROGRESSIVE_CONTRACT@1.0.0`
- `world_tag` — `p04-selected-world`
- `source_universe_ref` — the synthetic universe's exact ref
- `release_ref` — the synthetic release ref
- `risk_set_ref` — the shared risk set ref
- `selection_metadata` — synthetic selection block with explicit HOLDs
- `real_current` — hard-coded `False`

`select_world()` builds the synthetic 58-respondent fixture and emits the contract. `run_selected_world_progressive_chain()` verifies the contract's bindings against the world, then runs the full E03 chain.

## 3. Real owner chain — actually executed, matches the oracle exactly

| step | owner invoked | denominator | cells | P(Y=1) exact | consumer |
|---|---|---|---|---|---|
| P(Y\|A=1) | **N10E** `provide_empirical_possibility_slice` | 32 | {0:14, 1:18} | **9/16** | `EXACT_SUPPORTED` |
| P(Y\|A=1,B=1) | **C1** `compose_positioned_subject_possibility` | 16 | {0:6, 1:10} | **5/8** | `EXACT_SUPPORTED` |
| P(Y\|A=1,B=1,C=1) | **C1** `compose_positioned_subject_possibility` | 8 | {0:2, 1:6} | **3/4** | `EXACT_SUPPORTED` |

Each step's own produced evidence object was handed to the real plain **F8** evaluator as a separate consumption invocation — produced/ref-consumed identity verified equal for all three steps.

**Conservation, verified:** same `release_ref` and same `risk_set_ref` across all steps; both minority alternatives present in every step (min count 2 at depth 3); `UNCERTAINTY_UNQUANTIFIED` preserved.

**Command:** `PYTHONPATH=. python3 WORKER_RETURNS/PYAT-HQ282-P04-SELECTED-WORLD-PROGRESSIVE-FIXTURE-R1/repro/p04_evidence_recorder.py`

## 4. Owner-absent edges — typed HOLDs

1. **N9** (publication/resolution/lifecycle world-serving): ABSENT. E01 API graph: `implemented: false`. `select_world()` is a bounded simulation, not an N9 implementation.
2. **N10W** (progressive multi-condition world binding): ABSENT. E01: `implemented: false`. Progressive conditioning demonstrated through real C1 multi-conditioner owner.
3. **G0b** (model-use grant): ABSENT. Not fabricated, not issued.
4. **B5 CURRENT selection**: ABSENT. Not selected.

## 5. Hostiles — refusals demonstrated by execution

| hostile | observed refusal |
|---|---|
| unauthorized world substitution (foreign universe) | `P04WorldSubstitutionError` / `SOURCE_UNIVERSE_MISMATCH` |
| wrong release ref | `P04WorldSubstitutionError` |
| wrong risk set ref | `P04WorldSubstitutionError` |
| changed selected context (different tag) | `P04WorldSubstitutionError` |
| unordered conditioner list [B,A] vs witness [A,B] | `ConditionValueRelationMismatch` |
| empty predicate (zero-support) | `no matching producer leaf` |
| own-topic joint (A=1,A=1) | `duplicate conditioner binding` |
| exact stratum absence | `UNRESOLVED / EXACT_POSITIONED_STRATUM_ABSENT` |
| walkback proxy presented as exact | `EXACT_UNRESOLVED_PROXY_AVAILABLE` (labelled, exact_evidence None) |
| replay determinism | identical evidence hashes across runs |

## 6. Tests and scope

- P04 candidate suite: **24 passed**.
- E03 candidate suite (reused): **18 passed**.
- Combined: **42 passed** in 12.51s.
- Source-free: 0 .sav/.dta; no respondent row; no G0b/model-use/Field-Forge/temporal/CURRENT/V3 right; no canonical/accepted-owner edit; no self-adoption.
