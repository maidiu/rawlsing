# IG01-W08-FINAL-INTEGRATION-003 — FINAL CLEAN-MACHINE INTEGRATION

You are **Worker #8 — `CHAT-SINSP` — most recent submitting agent `IG_INTEGRATION_ACCEPTANCE_PREFLIGHT` → new agent `IG_FINAL_INTEGRATION`**.

**Class:** SUB-VOZHD  
**Repository:** `maidiu/rawlsing`  
**Mission branch:** `agent/vozhd-trii-ig-final-integration`  
**EXACT BASE:** `d5fd39126ecd0ca277759e1cfa47af4b138c584c`

## Mission

Assemble and test the exact clean sideline machine now that M1→M6 and bounded render are accepted. This is a finite integration/composition job, not semantic design.

Read your accepted preflight at `IMPLEMENTATION_GATE/IG_INTEGRATION_ACCEPTANCE_PREFLIGHT/` first. Its composition law controls except where this assignment supplies the now-known accepted render binding.

## Frozen accepted inputs

- M1 `e5f4871fbdea74bdb1b19067d9161e381ca359ba`
- M2 `935749537b7f69a3861fe9434a48743ff70f3cb4`
- M3 `f67c09948310fac9b48bcc4a223358fc6f590b94`
- M4 `83694e95e853651c3a34ea1c11008521ba67f072`
- M5 `b2d86364fa57940c54304206c5d161a521359087`
- M6 `c7dfd69131d0909cd0e4a7bec223ba64ec5d6167`
- bounded render **accepted** `d5fd39126ecd0ca277759e1cfa47af4b138c584c`
- PSEPF guard `dbed67bd83887afe310d9eeab827518d8cbf3a57`
- integration fixture scaffold `9fd7694049d8b6e79534c98cdd93a9f141302215`
- integration preflight `a0e9392ea9947d643acacb49597b86d10c2b2aa9`

Accepted render blobs:
- `rawlsing_next/render_bounded_expression.py` → `eef88095d1d647b5332aa5186a3a5df218fcf9f8`
- `rawlsing_next/tests/test_render_bounded_expression.py` → `80bdec5d9dc66603c1bc0fcbdf7506a56b2b0f35`

Accepted PSEPF blobs:
- `rawlsing_next/v3_psepf_zero_positive_guard.py` → `e0528d65215cb431196570c38bac4eae94217a1b`
- `rawlsing_next/tests/test_psepf_zero_positive_guard.py` → `21cfdee118d70d41def6ba654bbada5214cc1112`

## Before writing

Verify mission branch HEAD equals exact base `d5fd39126ecd0ca277759e1cfa47af4b138c584c`. Fail closed otherwise. Do not rebase onto mutable branch tips.

## Required composition

1. Preserve the complete M1→M6→render tree byte-for-byte.
2. Add **only the exact two PSEPF file contents** from the accepted PSEPF head. Do not merge its branch history.
3. Verify both resulting PSEPF blobs equal the pins above.
4. Create exactly one executable whole-machine hostile harness:
   `rawlsing_next/tests/test_whole_machine_integration.py`
5. Bind H01–H20 from the accepted fixture scaffold to the actual accepted runtime surfaces. IDs and expected verdicts are immutable.
6. Run every existing package-local test unchanged plus the whole-machine harness.
7. Prove replay/noncollapse/path-law closure and exact additive sideline isolation.

## Whole-machine obligations

At minimum prove:
- temporal negatives cannot launder into positive support;
- duplicate basis/routes do not multiply semantic support;
- V555 seven-field identity and V556 role/order/cardinality/multiplicity survive end-to-end;
- `resolver_allowed_uses ⊆ V557_allowed_uses ⊆ producer_allowed_uses` across required closure;
- provenance never creates source-composition authority;
- `RSC != V3EmpiricalPossibilityInput != ActorCausalState`;
- M5 structural eligibility has zero direct actor effect;
- PSEPF positive actor-transition registry remains exactly empty;
- actor-accessibility is the sole positive M6 ingress;
- stale/deny/defer/integrity/session state never restores access;
- no hidden claim joins or permission/component/scope widening;
- renderer consumes only an admitted plan bound to exact M6 projection and cannot invent semantic equivalence;
- blocked situated phenomenology/disclosure/salience/inhibition/affect/interlocutor/register semantics remain `BLOCKED_NAMED_AUTHORITY_REQUIRED` and are not inferred by render;
- typed absence/valid-empty/denial/noncomparability/unknown/zero/defer/stale/integrity stay distinct;
- deterministic exact-history replay and lawful divergent lives remain compatible;
- no fabricated RSC;
- no legacy runtime import, stage-close-artifact runtime read, mutable-latest, fuzzy/nearest/network/model/random/default/session repair.

## Write allowlist

Runtime/test:
- `rawlsing_next/v3_psepf_zero_positive_guard.py`
- `rawlsing_next/tests/test_psepf_zero_positive_guard.py`
- `rawlsing_next/tests/test_whole_machine_integration.py`

Governance result record only:
- `data/ddm_build_copy/vozhd_trii/20260819_corrected_upstream_downstream_rebase/IMPLEMENTATION_GATE/IG_INTEGRATION_FINAL/RESULT.md`
- `.../RESULT.json`
- `.../FINAL_TREE_BINDINGS.json`
- `.../HOSTILE_TEST_RESULTS.json`

Do not modify any already accepted M1–M6/render runtime or test file.

## Forbidden

No legacy `data/ddm_build/**` or non-Vozhd `data/ddm_build_copy/**` runtime writes. No PSEPF whole-branch merge. No semantic harmonization. No positive SPDM implementation. No cutover/deployment. No source/artifact retirement. No broad-topology change.

If an implementation fails a frozen invariant, return it to its owner; do not alter semantics here.

## Return

On exact success return:

`IG_INTEGRATION_COMPLETE__READY_FOR_FINAL_RECLOSURE_ADJUDICATION`

Otherwise return exactly one of:
- `IG_INTEGRATION_BOUNDED_EXACT_BINDING_FAILURE`
- `IG_INTEGRATION_IMPLEMENTATION_SEMANTIC_VIOLATION`
- `IG_INTEGRATION_SEMANTIC_CONFLICT_FOUND`

Include exact HEAD, final changed-path list, blob pins, test command/results, H01–H20 verdicts, and confirmation that deployment/cutover remain false.
