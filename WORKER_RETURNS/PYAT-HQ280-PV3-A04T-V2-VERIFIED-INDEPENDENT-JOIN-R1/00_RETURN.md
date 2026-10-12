# PYAT HQ280 PV3 A04T — Actual V2 independent no-drop verifier join

**TERMINAL:** `HQ280_PV3_A04T_ACTUAL_V2_INDEPENDENT_NO_DROP_VERIFIER_JOIN_OR_EXACT_HOLD__NONISSUING__GITHUB_PUSHED`
**RESULT:** `PASS__INDEPENDENT_STDLIB_VERIFIER_JOINS_REAL_OWNER_CHAIN__44_TESTS_PASS__20_OF_20_HOSTILES_DETECTED__A04SR_FAILURES_CLOSED__A04_41_A05_18_UNCHANGED__SOURCEFREE_ONLY__NONISSUING`
**Branch:** `agent/rabochii-pyat-hq280-pv3-a04t-v2-verifier-join-r1`
**Sealed startup (verified before mutation):** `b68de0dd35a9885efcb46bcd8ec9cbe41dabf500`
**Authority:** HQD-2026-10-10-280; canonical `a70a069fa948e0f3c041b389edcc732b6b948a4f`; semantic PRE-MAIN `1f47063c3205a45888b3c55e81e7485943ed1390` (**unmutated**).
**Inheritance:** A04S `56574bec2176df7fc95d4b877dfab79469de9c03` · A04SR hostile `b50bdec108071432bd7fa8d3751e34e01eb3289f` · A05 oracle `9491d0296c95ee2942fe80eadc6aa9f54b07c634` (immutable, **never pretended v2-compatible**).

## 1. What was built

Two NEW files. **No A04/A04S/A05 file edited, no accepted owner touched** (tracked `git diff` on `rawlsing_next/` is empty).

| File | Blob | Lines | Role |
|---|---|---|---|
| `rawlsing_next/pre553_original_workload_v2_verifier_candidate.py` | `996c8e907f2befde93af09b60154b610c1ffeb63` | ~950 | stdlib-only independent verifier |
| `rawlsing_next/tests/test_pre553_original_workload_v2_verifier_candidate.py` | `5799900d58b9949ab2784ea489f170f1be2f14bc` | ~750 | 44 tests |
| `repro/a04t_join_worker.py` | (return dir) | ~230 | produce + blocked-verify subprocesses |

The verifier imports **nothing** from `rawlsing_next` — verified by a test that imports it in a fresh interpreter and asserts no sibling repository module is pulled in. It operates purely on plain-data payloads.

## 2. A04SR's four failures, each closed with executed proof

| A04SR finding | A04T closure | Executed proof |
|---|---|---|
| Copy-translation (`v2_to_a05_universe` copies v2 keys into A05 slots) | **Deleted as a join mechanism.** The verifier never takes an A05-shaped object; it recomputes every key from raw fields with its own code and rejects supplied keys on mismatch (`KEY_PREIMAGE_MISMATCH`). Interop is an audited mapping, never a translation. | `test_supplied_key_forgery_is_detected_not_trusted`, `test_forged_supplied_key_fails_the_join` |
| Semantic→dispatch 3:1 non-injective, no fail-closed | Migration audit checks set-level injectivity and declares `NONREPRESENTABLE__SHARED_A05_TRIPLE_WOULD_COLLIDE` (Y-RAW/Y-WEIGHTED share one A05 triple). Dispatch reuse ≠ job collision: produced→expected join is by exact owner-ref equality **plus** the producer's claimed mapping cross-checked. | `test_migration_audit_declares_nonrepresentable_honestly`, RAW/WEIGHTED collapse refused at bind |
| Issuer hash + asserted timestamp presented as provenance | `custodian_check` separates structural consistency from external authentication: matching digests → `STRUCTURALLY_CONSISTENT__EXTERNALLY_UNPROVEN`; mismatch → `CUSTODIAN_MISMATCH`; absent → `CUSTODIAN_ABSENT`. `EXTERNAL_CUSTODIAN_ISSUER_HOLD` is **unconditional**; timestamps recorded, never trusted. | H21, H22, `test_rewritten_frontier_plus_matching_custodian_still_holds` |
| Consumer MODELLED presented as satisfied | Structural join may pass while `actual_consumer_court` separately holds `REAL_CONSUMER_MODELLED_NOT_EXECUTED`; modelled receipts can never satisfy it in this scope. | `test_actual_consumer_court_holds_despite_structural_join`, H12 |

## 3. Genuine positive join (actual measured output)

Real source-free chain (A04S v2 → C11 → Route B/I03/I05 → Batch) in one process; verification in a **separate process** with the v2-candidate import blocked (block proved active in every verdict: `candidate_import_blocked: true`).

- C11 release: `95de34f09fa9ae4aac6c6a3c73ea7ff9dff5ef18189bac940805f30126fce88c`
- Batch: 6 units; reconciliation **ok=True**, 6 expected keys, 6 job keys, 0 omitted, 0 extra, 4 held visible
- Result classes all measured; frontier digest `fcd0abb637061dc6e79ec394a06c511dc775a10458795351bab47d935409cb78`
- Standing holds on the pass: `EXTERNAL_CUSTODIAN_ISSUER_HOLD`, `REAL_CONSUMER_MODELLED_NOT_EXECUTED`
- Verifier↔candidate cross-check: independently recomputed keys agree on honest input (agreement, not trust)

**Command:** `PYTHONPATH=. python3 repro/a04t_evidence_recorder.py`

## 4. Hostile court — 20/20 must-fail detected, 3/3 controls pass

Omissions (A-only, missing J2, missing B), extra job (undeclared yx query), same-count/different-keys (exact 1 omission + 1 extra), condition-order substitution, own-_dk fake joint (`CANDIDATE_OWN_DK_JOINT` on **both** expectation and produced sides), form/risk/source/measure swaps, laundering pair H11a (self-certified PASS, deliberately) vs H11b (frozen-universe FAIL), consumer omission with all jobs present, held invisibility, forged release (`FORGED_RELEASE` on matched **and** unmatched jobs), false null, unvisited discovery, coverage mispromotion (plus honest-reporting conservation control), duplicate jobs, missing results, zero-denominator, bind-time refusals (RAW/WEIGHTED collapse, measure-query swap), custodian forgery ×3, migration honesty.

Two defects found **by running** during this work and fixed in the open:
1. Pure owner-ref joining cannot see documentary-level key swaps → produced manifest now carries the producer's claimed mapping, which the verifier checks **and** cross-checks against owner refs (`CLAIMED_JOB_REF_MISMATCH`).
2. `SUPPORTED`-over-zero-denominator short-circuited the denominator check → check now precedes all promotion.

## 5. Old evidence untouched, old suites green

- A04S v2 module blob `08bb75c431d3352cb0d17e9a65f7d855b4d35e59` verified; A04 binder `7d8b3902…`, route_b `2385cd32…` (E18), discovery_exact `905f24d1…` (E19) all intact.
- A04S **26 passed** (here) · A04 **41 passed** (own worktree) · A05 **18/18** (own worktree) · owner spot suites pass · v2 **44 passed** here.

## 6. Ceilings and holds

Source-free development only (0 `.sav`/`.dta`). No original-source read, no all-35 eligibility, no model permission, no G0b/EE12, no operative publication, no canonical/PRE-MAIN mutation, no self-adoption, no merge, no ZIP relay. Issuer/custodian/consumer authority remain **HELD** (`EXTERNAL_CUSTODIAN_ISSUER_HOLD`, `REAL_CONSUMER_MODELLED_NOT_EXECUTED`); no real-source issuance; the v2 frontier is a development-grade expectation, not an issued authority. A structural PASS here is not external custody.

**Terminal:** `HQ280_PV3_A04T_ACTUAL_V2_INDEPENDENT_NO_DROP_VERIFIER_JOIN_OR_EXACT_HOLD__NONISSUING__GITHUB_PUSHED`.