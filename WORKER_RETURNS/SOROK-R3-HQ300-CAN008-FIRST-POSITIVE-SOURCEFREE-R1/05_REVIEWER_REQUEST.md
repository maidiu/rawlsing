# HQ300 — independent acceptance reviewer request and hostile acceptance matrix

**Discipline:** the author may not serve as independent acceptance reviewer. A
distinct competent **I2 reviewer** (commission: independent GPT-6 High semantic
court on the returned code) must adjudicate before any acceptance.

## What the reviewer adjudicates

1. **Frozen-matrix integrity** — `01_FROZEN_EXPECTED_MATRIX.json` sha256
   `38226170254da35ae077c0e04fe87d0d5397d6cfcc63b16c53c1279892ada331`
   recorded before any execution (`outputs/matrix_freeze.json`); confirm no
   frozen expectation was edited to fit code.
2. **Adopted-interface fidelity** — re-derive `candidate/adopted_contract.py`
   constants against the pinned authority blobs (CAN008_R2 `b80dd692…`, ADP016
   `c6619a28…`, ADP017 `eece4f3f…`); confirm the 23-item rule binding, the
   ADP-016 7 formation gates / 16 fail-closed states, the ADP-017 knowledge and
   belief gates / first-person mapping are transcribed, not invented.
3. **The positive chain** — re-run `candidate/positive_chain.py`; confirm the
   admitted event causes a target-owner effect **stored in causal order**, one
   later event reads it and produces a typed response difference (DEFLECT vs
   AMPLIFY control), and full replay is exact.
4. **Registry distinction** — confirm the candidate chain runs against the
   WORKER fixture registry while the imported production zero-positive guard
   still returns `DENY_ZERO_EFFECT / ZERO_POSITIVE_REGISTRY` for the identical
   transition and its registry remains empty. Any production registry mutation
   is a hard rejection.
5. **K3/K5 semantics** — confirm inaccessible origin never grants
   self-explanation (first-person `DENY`, trace not recallable, sole-basis
   fail-closed) and public standing vs private belief do not collapse
   (belief byte-identical across witness-power arms; knowledge gate truth-not-
   sufficient; no automatic implications).
6. **The 9 hostiles** — confirm each refuses with the frozen typed code and
   mutates nothing.
7. **DISC_01 correction** — confirm the detector now measures implementation
   surface (class/def), classifies the two estate string mentions as
   denylist/rejection codes, and that the RSM court is 60/60 after correction.
8. **Preservation** — confirm the 220 pinned owner tests run unmodified and the
   GT0/SDTF/M6 negative guards are byte-unchanged.

## Hostile acceptance matrix (commission-required)

| Hostile | Expected code | Test | Result |
|---|---|---|---|
| H1 no admission | `BLOCK_UNADMITTED_EVENT` | `test_F_H1_no_admission` | PASS |
| H2 forged issuer | `BLOCK_FORGED_OR_MISMATCHED_ISSUER` | `test_F_H2_forged_issuer` | PASS |
| H3 stale/as-of world | `BLOCK_STALE_OR_MISMATCHED_WORLD_ASOF` | `test_F_H3_stale_asof_world` | PASS |
| H4 wrong actor scope | `BLOCK_WRONG_ACTOR_SCOPE` | `test_F_H4_wrong_actor_scope` | PASS |
| H5 hidden-future leak | `BLOCK_HIDDEN_FUTURE_LEAK` | `test_F_H5_hidden_future_leak` | PASS |
| H6 duplicate event | `BLOCK_DUPLICATE_EVENT_IDENTITY` | `test_F_H6_duplicate_event` | PASS |
| H7 disallowed memory | `INELIGIBLE_NONCAUSAL_SOURCE` | `test_F_H7_disallowed_memory` | PASS |
| H8 invalid trace | `PARENT_EVENT_HASH_MISMATCH` / `PRE_STATE_HASH_MISMATCH` | `test_F_H8_invalid_trace` | PASS |
| H9 reverse chronology | `BLOCK_REVERSE_CHRONOLOGY_CAUSAL_PARENT` | `test_F_H9_reverse_chronology` | PASS |
| preserved: production guard denies | `DENY_ZERO_EFFECT / ZERO_POSITIVE_REGISTRY` | `test_B_imported_production_guard_still_denies`, `test_H_no_production_registry_mutation` | PASS |
| preserved: GT0 blocked path | `BLOCKED_POSITIVE_ACTOR_PATH__SEMANTIC_CONSERVATION_PASS` | `test_B_imported_gt0_still_blocks_positive_actor_path` | PASS |
| preserved: DELETE_MEMORY forbidden | `UNAUTHORIZED_TRANSITION` | `test_H_delete_memory_forbidden` | PASS |
| preserved: rehydration forbidden | `UNAUTHORIZED_OBJECTIVE_HISTORY_REHYDRATION` | `test_H_rehydration_forbidden` | PASS |

## Out of scope for this reviewer

- Promotion of the candidate rule to accepted law (owner act).
- The production registry entry decision (owner act; the guard explicitly awaits
  a "separately accepted authority change").
- V3 actor operation or any adopted-rule claim.

## Requested reviewer terminal

`REVIEW_PASS | REVIEW_REVISE | REVIEW_REJECT | REVIEW_HOLD` with exact failed
predicates. Even `REVIEW_PASS` adopts nothing.

## Reviewer qualification

I2-high CAN008/ADP016/ADP017 competence; must read the adopted R2 blob
`b80dd692…` and the HQ299 RSM findings (`00f5d9a6…`) before adjudicating; must
re-run the candidate court and the preserved suites independently; must not be
the author.
