# R2 — bind consumed later-relation evidence

**Result: the three R1 relation-source REDs now PASS, unchanged.** All 91 supplied regression tests and the exact Git M3 three-test court still pass. Fourteen new targeted controls pass. Frozen M1/I2 compatibility failures remain unchanged. This is a provisional sourcefree implementation result, pending fresh independent review.

Parent publication: `6805da13bf2291837c9620784b2d31b82103c3a3`, branch `agent/experimental-sorok-m2-preimage-custody-r1`. The user authorized fixing the reported gap. This follow-up adds only `WORKER_RETURNS/SOROK-M2-RELATION-PREIMAGE-REPAIR-R2/`; the previous return, supplied original candidate, original M2/M3 and canonical stores remain unchanged. No new HQ commission/seal or semantic authority is claimed.

## Implementation

`m2_patch/kernel.py` now uses one `_relation_sources()` predicate for candidate eligibility and source snapshotting. For each relation-conditioned mode, a proposal records the exact relevance receipt, child's observed counterpart history and independent history witness that enabled it. The existing objective event hashes continue to bind the encounter itself.

When multiple valid relation alternatives exist, initial selection is deterministic. Historical validation then checks that the **actually consumed** alternative still exists with its original hashes; it does not switch to a newly preferred alternative or freeze every relation in the scene. Thus deleting/changing a used receipt or replacing the observed history with refreshed witness hashes refuses, while adding an alternative or changing unconsumed/private history remains lawful. Append recomputes the source snapshot, detecting a source change between proposal and commit even with a renewed fixture grant.

NO_CHANGE records no unused relation dependency and still returns the same state. Future relevance receipts and unwitnessed counterpart observations cannot enable relation modes. This implementation versions the rule as `M2_INTERPRETATION_SOURCE_TEMPORAL_IDENTITY@0.4.0_CANDIDATE`.

Kernel SHA-256: `88bb8c65dfd88efd1843f16e1bb6d51e1fa01a0dc1fdccb13e03a9b2b394d8d3`.

## Executed courts

| Court | Result |
|---|---|
| Original supplied M2 / M3 lawful / packaged three / additional regressions | **41 + 32 + 3 + 15 = 91 PASS** |
| Exact Git M3 historical preimage court on R2 | **3 PASS** |
| Same exact Git court on unchanged original M2 | **3 RED**, preserved |
| R1 local hostile court, unchanged test bytes | **11 PASS**, previously 8 PASS / 3 RED |
| New relation-custody controls | **14 PASS** |
| Frozen original M1 on original M1 | **37 PASS** |
| Frozen I2 on original M1 | **14 PASS / 9 RED** |
| Frozen M1 on original M2 and R2 | **18 PASS / 19 RED** on each |
| Frozen I2 on original M2 and R2 | **13 PASS / 10 RED** on each |

Zero errors/skips/xfails. The historical compatibility failure names, not just counts, match R1. These overlapping sourcefree courts are separately graded and not a pooled independent acceptance total. The exact original M3 Git reproducer remains distinct from its reformatted package equivalent.

New controls exercise all six mutating later modes; changed observation witnesses; added/reordered valid relation alternatives; removing unconsumed alternatives; unchanged private histories' freedom; proposal-to-append source replacement; genuine NO_CHANGE; future evidence; and unwitnessed activity. `evidence/later_relation_probe.json` now records `SOURCE_PREIMAGE_IDENTITY_COLLISION` for all three original attacks. The R1 failing receipts are retained in `evidence/baseline/` and compared against the parent Git commit.

## Reproduce and audit

```sh
python3 run_courts.py
python3 verify_evidence.py
```

`execution_receipts.json` contains commands, actual exits and JUnit counts. Every test subprocess records the actually loaded kernel file/hash. `source_refs.json` pins original M2/M3 and the frozen archives; `input_sources.json` verifies copied tests against the parent publication. `candidate_vs_r1.patch` is the implementation delta. Portable logs sanitize local paths/hostnames without editing source, frozen tests or archives. `artifact_manifest.json` seals delivered files. The first implementation passed the affected regressions; no frozen assertion was weakened to obtain PASS.

## Scope and remaining requirements

No remaining failure was observed in the targeted relation-source courts. The historical M1/I2 REDs and original M2 three REDs remain intentionally unmodified. The earlier packet's unrelated missing Track B files remain outside this repair.

This remains a test-only in-memory candidate. Synthetic witness hashes and fixture grants are not authenticated ADP authority. Hash integrity assumes a trusted retained state: a privileged editor able to rewrite both state and witness data is not excluded by these tests. No old-lineage migration contract, append-only production database, actor psychology, CAN/ADP grant, B3 integration, actor memory entitlement or empirical calibration is established. Old relation interpretations without the required snapshot fail closed; this is not an authorized migration or retroactive rewrite of them.

A distinct fresh reviewer must reproduce the exact published SHA and challenge dependency completeness before acceptance or integration. This worker authored R2 and cannot issue its independent acceptance. Publication uses the existing user-authorized provisional branch with a non-force push and direct remote verification; final SHA is reported outside its own preimage.
