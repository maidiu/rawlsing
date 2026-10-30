# RCF-B — compatibility architecture and priority

Observed FINDING: the modern estate is not one selectable stack. It contains a working BP2P4J/C12 episode edge, a separate C9 R3B test-only actor SQL/mirror stack, component repairs for G17/M04R/F1CR, and a C12 anchor/version conflict. Causal INTERPRETATION: the missing artifact is an owner-authorized compatibility contract that joins immutable episode origin, C9 writer/reader/mirror schema and the C8/S36 source cut; newest-wins selection would merge incompatible writer/readset contracts. Proposed HQ ACTION: select only the tested BP4R/BP2P4J C12 episode edge now; route every other cut to its owner with the exact gaps below. Accountable OWNER: BP4/C12, C9R, R31J/F1C, G17/M04 and PRE-MAIN owners.

## Version-select matrix

| Family | Exact cuts | Compatibility finding | Decision |
|---|---|---|---|
| BP2P4J / B3AS | BP2P4J `5b3e657`; B3AS `1a25b19d` | B3AS is accepted only at schema/readset grain; it does not supply a BP2P4J C9/C12 adapter. BP2P4J C9 writer is `vendor/bp2/vendor/c9r/candidate/transaction.py` blob `1a9c15b8…`; C12 store is `vendor/bp4/bp4/store.py` blob `69a58f43…` (old local store), not the repaired external C12. | `REUSE_REVIEWED` only inside BP2P4J; no whole-stack transfer |
| BP4 C12 | Original `68b05865` `store.py` `c94cd131…` + `c12_integrity.py` `402c2b02…`; BP4R `693d25bf` guard `e0d9d904…` | Original fork conflated sealed body origin with SQL location; BP4R separates immutable origin from current location and rejects `@2`. BP4R is an overlay candidate, not adopted. | `NEEDS_OWNER_REVIEW`; selected for bounded probe only |
| C9 R3B writer | `fac064c9` / staging `b8923db1` `c9_actor_r3.py` `67f34f69…`; old writer `1e99681f` same blob; BP4R patched C9 `b9000cdb…`; reader `actor_reader.py` `5ef6a278…` | C9 R3B accepts only `BP4_C12_STORE@1`; `@2` refused by BP4R gate. Old-count C9/C12 suffix conflict remains 14 PASS/1 FAIL at `tests/test_c9_r3.py:476`. Reader/mirror is a separate actor DB, not BP2P4J C9. | `HOLD_C9_ACTOR_DURABLE`; do not substitute for BP2P4J C9 |
| G17 / G17I2 | G17 `90d0eb79` originals `c9318dcf…`, `fc954993…`, `47e59c12…`; G17I2 `95f15026` candidate `8b9a39da…` | 11/3 RED repaired to 14/14 reviewer and 13/13 author; no durable C9 adopter; M2/MP and C9 E1/RULE_A/T/E2 HOLD. | `NEEDS_OWNER_REVIEW`; component only |
| M04 / M04R | M04 `2309a73b` patch `5ba929…`; M04I2 `09497812`; M04R `8f200fd6` candidate `d9efd3f5…` | M04R closes direct unjournaled ADP017 restore at 51/51 and preserves 587/587; nine CAN3 REDs remain; owner/reviewer pending. | `NEEDS_OWNER_REVIEW`; component only |
| F1C / F1CR | F1C `bcea367e` program blob `104f5bd7…`; F1CR `03be5c2` docs; patched `bf7e625e…` | The F1CR executable is **not present at any commit path**; `bf7e625e…` is absent and `104f5bd7…` is only a loose blob. The 13/13 outcomes and three mutation refusals are attributed, not runnable from the tree. Targetless REFUSE/SILENCE/C10 is HOLD. | `NOT_SELECTED__SOURCE_NOT_COMMITTED` |
| OC5 / OC5E | OC5E `67a4f156` 49 novel + 10 prior REDs; owner docs `b83f474f…` | C8 provenance/capsule trust is not owner-issued; no self-issued trust. | `HOLD_NATIVE` |
| Native F1 | 17 RED/X3 historical | Preserved; no native Rule A/T, world, or actor grant. | `HOLD_NATIVE` |

## Causal difference matrix (same sourcefree test case)

| Difference | Current executable support | Status |
|---|---|---|
| A prior capability unlocked by resource | F1C/F1CR `SHARE`, `NO_B_RESOURCE`, `ENCUMBERED_B_TOOL`, `DUPLICATE_TOOL`, `B_SOURCE_SEVERED/RESTORED` | Attributed 13/13; F1CR executable absent; sourcefree only |
| B does it | F1C `SHARE`; B free hours 12→11; B performs alongside A | Sourcefree TEST_ONLY intervention; no native B or independent biography |
| Acquired practice | BP2P4J E2 `inspect_with_tool` materialized into A projects/tools; A2 completed_units 3→4 | TEST_ONLY E2→A2; **not** CAN011 acquired practice |
| Unsupported transfer | BP4R C9 `@2` refused; G17 forged material refused; C9 R3B `TRUE_NO_CHANGE` requires Rule T | Fail-closed checks exist; no native authority |
| True admitted NOCHANGE | C9 R3B `TRUE_NO_CHANGE_EVALUATED` with issued Rule T | Test-only; native Rule T unissued |
| HELD no rule | C9 R3B `HELD_MISSING_RULE` / requalification hold | Test-only; owner grant required |
| Targetless REFUSE/SILENCE | JOIN `joined/refusal.py` read-only 1/1; F1C not linked; C10 has no targetless read path | HOLD_OWNER_SEMANTICS |
| Original B material time-cost | F1C `SHARE` B free hours 12→11; physical tool/material ledger A=3,B=0,spent=1 | Sourcefree only |
| Durable C9/C12 recurrence | BP2P4J C12 store + BP4R guard; C9 R3B actor SQL separate | C12 episode edge green; durable C9 actor integration absent |

## Selected sourcefree subset

**Select for bounded compatibility only:** `BP2P4J 5b3e657` + F2 verifier `0636d257` + BP4R C12 guard `e0d9d904` + BP4R C9 writer gate `b9000cdb`.

Evidence: 9/9 actual BP4R candidate tests on the BP2P4J base (legitimate episode fork, cold reopen, forged transplant refused, C9 `@2` refused, schema-gate severance/restore, `@1` ready). This is a sourcefree test edge, not a whole-person product and not an adopted C9/C12 contract.

**Do not select:** C9 R3B actor SQL as BP2P4J's C9 writer (no adapter; old-count 14/1 RED; anchor HOLD); F1CR executable (not committed); G17/M04R as integrated chain (component-only; owner review pending); any native C12/CAN/ADP/SCI05/person claim.

## Adapter gaps and owner decisions

1. **C12 owner:** ratify immutable-origin/location semantics and the supported writer-schema set (`@1` only); decide C12 external anchor/custodian and whether `@2` needs migration or refusal. The BP4R guard is a candidate.
2. **C9R owner:** decide old-writer vs repaired-writer version split, C9 R3B actor schema freeze, mirror/outbox atomicity and cross-database status. The 14/1 old-count conflict must remain a separate versioned test.
3. **F1C/R31J owner:** commit the exact F1CR executable at a tree path and provide a targetless REFUSE/SILENCE/C10 adapter; otherwise keep the 13 outcomes attributed only.
4. **G17/C9 owner:** accept/reject G17I2 14/14 and provide the C9 durable handoff adapter; preserve M2/MP and C9 E1/RULE_A/T/E2 HOLD.
5. **M04/CAN3 owner:** accept/reject M04R 51/51 and preserve 9 CAN3 RED; provide the native CAN3/C9 path.
6. **PRE-MAIN/HQ:** no canonical merge until protected owner CAS and independent review; QF2/QF1 remain NOT_MERGED.

## Priority

1. C12 origin/anchor and C9 supported-schema decision (unblocks the selected edge).
2. C9 old-count/version split and C9 R3B owner freeze.
3. F1CR executable commit + targetless adapter.
4. G17I2/M04R owner review and component adoption.
5. Durable C9/C12 actor integration, C10 targetless, real A0–A5 human trial.

DONE: version matrix, causal differences, selected subset, gaps and priority. REMAINING: owner decisions and independent review. CRITICAL BLOCKERS: C12 anchor, C9 old-count/version split, F1CR source absence, native person. LARGEST MOVE: owner decision on C12 origin/anchor + C9 schema, then commit F1CR code. FLIGHT: no integration, no PRE-MAIN/PR mutation. DELTA: one tested C12 episode edge is selected; the rest is explicitly held rather than falsely joined.
