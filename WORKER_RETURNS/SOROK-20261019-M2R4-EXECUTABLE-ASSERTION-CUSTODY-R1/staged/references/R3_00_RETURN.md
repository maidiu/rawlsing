# SOROK M2 R3 — counterpart action-owner custody repair (user-directed candidate)

**DISPOSITION: `R3_AUTHOR_EXECUTED_GREEN__FRESH_INDEPENDENT_I2_PENDING`.**

This is a bounded *user-directed* implementation return, not a new HQ-issued seal, independent reviewer attestation, CAN/ADP rule, B3 adapter adoption, actor trial, or empirical source grant. **No branch/startup was issued by HQ for this successor**; do not misstate the known Git parent as an HQ-issued sealed startup. The immutable R2 `e8f375e9feae187e8a1add2343100ca05d9fffc4`, the M3/M1/I2 originals and the review `e8b2d6be5ba243729f387cda4048cc30a52664d2` are not edited.

## Defect and change

Exact R2 source kernel SHA-256: `88bb8c65dfd88efd1843f16e1bb6d51e1fa01a0dc1fdccb13e03a9b2b394d8d3`. The fresh R2 I2 court showed that an independently *witnessed* child's own `ENCOUNTER` action enabled all six other-person interpretation modes. Observation independence is not action-owner independence.

R3 candidate (version `M2_INTERPRETATION_SOURCE_TEMPORAL_IDENTITY@0.4.1_CANDIDATE`) makes the latter explicit:

1. `_relation_sources()` requires `e.action_owner` be a *different actor* from the interpreting `actor_id`.
2. `Relevance.observed_action_owner` explicitly names that actual actor, and must equal `e.action_owner` in the already immutable-hashed observed event.
3. The child's observed `History.observed_action_owner` also names that actor, and must agree with both the relevance and event. Its independently witnessed history-source hash remains included in the consumed historical readset.
4. Existing independent-action history requirements, event/clock checks, self-versus-other witness requirements, deterministic consumed-alternative choice, source preimage replay, proposed-to-append recomputation, and NO_CHANGE nonmutation remain unchanged.

`None` is permitted in the *data schema* for non-observation histories or old records, but does **not** grant an other-person relation mode. Old R2 records are not migrated; new source fields and changed RULE_HASH require a separate explicit source/owner migration authority, which is not issued here.

## Author-run source-free execution (actual Python/pytest)

A verified in-memory original kernel and copied original unmodified tests were staged to a fresh candidate folder. All test source hashes were checked against exact R2 bytes before execution. Each subprocess imported the candidate `kernel.py`, printed and verified its SHA-256, and produced an actual log and JUnit XML. The original R2 was independently rerun as a control and retained the expected child-self-action RED.

| Court | Author-run result |
|---|---|
| Original M2 41 | 41 PASS |
| M3 lawful 32 | 32 PASS |
| Packaged M3 three | 3 PASS |
| Additional source-preimage 15 | 15 PASS |
| Exact Git M3 historical three | 3 PASS |
| Prior hostile 11 | 11 PASS |
| R2 relation-custody 14 | 14 PASS |
| Fresh I2 heldout 2 | 2 PASS (formerly 1 PASS / 1 RED) |
| Newly authored R3 actor-identity and source-replay controls | 14 PASS |
| **Total against R3** | **135 PASS, 0 RED, 0 SKIP, 0 ERROR** |
| Original unmodified R2 on fresh I2 heldout | 1 PASS, **1 RED** (expected) |

Frozen original M1/I2 tar courts were **NOT_RERUN** here. All those original failures remain historical; nothing was modified or claimed resolved. The R3 checks do not grant native authentication: synthetic witnesses and `fixture_grant()` remain test fixtures only.

## Fresh I2 court required before scoped adoption

Review the exact R3 candidate SHA and Git blob; independently reconstruct both genuine owner examples (`other_P`, `other_Q`) and child-self-action with *all* receipt fields matching child; verify a second nonself observer does not launder self-action, any missing/mismatched action-owner fields refuse, changed consumed history/relevance fails continuation, unrelated unconsumed alternatives remain free, proposal→append replacements refuse, NO_CHANGE stays state-identical, and all 119 inherited R2 tests plus 2 prior heldout and 14 new ones pass unmodified. Preserve frozen M1/I2 incompatibilities; independently review rule hash, fail-closed earlier histories and whether the new field-level witness binding is sufficient at sourcefree grade. The candidate author must **not** sign that review.

B3 is permitted only read-only, quarantined, sourcefree research on candidate menus until a separate competent owner issues integration permissions. No native ADP019/021 occurrence, ADP015 other, ADP016/017 memory, CAN008/011 psychological selection, actor-state issuance, product wake, or empirical calibration is established.

## Reproduction

Materialize exact R2 inherited tests from `WORKER_RETURNS/SOROK-M2-RELATION-PREIMAGE-REPAIR-R2/` at commit `e8f375e9feae187e8a1add2343100ca05d9fffc4`; place the new candidate kernel alongside them and add `test_r3_counterpart_actor_custody.py` from this return. The existing heldout is byte-identical to `WORKER_RETURNS/SOROK-20261018-M2R2-FRESH-I2-EXECUTION-R1/test_heldout_actor_independence.py` at `e8b2d6be5ba243729f387cda4048cc30a52664d2`.

Use `PYTHONPATH=. python3 -m pytest -q --import-mode=importlib` over the inherited suites and R3 tests. See `execution_receipts.json`, `case_matrix.json` and JUnit/stdout evidence for exact commands and results.
