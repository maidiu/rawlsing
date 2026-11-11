# HQ266 — XOR source-free execution verified; G1 query-authority parity repair issued

**Decision:** `HQD-2026-10-09-266`.
**Checkpoint:** `20261009-PYAT-HQ266-G01-XOR-VERIFIED-QUERY-AUTHORITY-G2-PARITY-REPAIR-R1`.
**Inherited sealed HQ265:** `fd78868a021f8b8db6f2606f05b2e1fc6e744140`.
**Canonical parent:** `cd886bc59a16acc1c29efe7f1d9966654f91640b`.
**Semantic PRE-MAIN:** `1f47063c3205a45888b3c55e81e7485943ed1390` unchanged.
**Decision record:** `PYAT_CONTROL_ROOM/SPACE_BUNNY_OPENCODE_R1/ACTIVATION_RETURNS/HQ266_G01_XOR_EXECUTION_POSITIVE_G2_QUERY_AUTHORITY_INTEGRATION_HOLD_R1.md`.

## Exact HQ265 return

`agent/space-bunny-pyat-hq265-g01-fixture-regrounded-g2-xor-repair-r1 @ 8d42dbbe9d8c07aa2672abd7a970bf15373fe056`, 1 ahead/0 behind commission tip `c5e3ea36d8e6f1fab139821b9521c1740a7e46e9`, four return docs, zero code edits. Actual configured local model Space Bunny Max (`space-bunny-free`).

**Proved at author-run source-free fixture grain:** original same-four XOR C1 q1 distribution 1/2,1/2 denominator 2, q2 0/1,1/1 denominator 1; same source/release, distinct C1 identities. Fixture `c1_at08_at13_fixture.py` blob `0393cc8c17a313b7944b2a5287d0406d6cbe3849`.

**Not proved:** repaired owner C1→real applicability/G2→bound F8: draft had **17 PASS, 6 FAIL**, reverted. Original G01 22 author tests remain green but only on unchanged flawed code; G1 not adopted.

**Exact narrowed failure:** draft invoked `_query_snapshot()` instead of HQ253's working `_query_authority("c1-at09-xor")` and `_registry(source,qauth)`, causing `possibility_slice_evidence_or_null=None` and `consumer_result_or_null=None` in its owner setup. Historical HQ253 witness `test_pre553_scoped_rich_c1_f8_existing_api_discriminator.py` blob `17300a405d78820cd663618918e64bb0323f532e` at `e609be4f68c51182c5acb3a99c671949f1b71d34` already demonstrates real G2 and C1 output. Technical source-free G2 feasibility is NOT actual EE14 G0b permission.

## Active

**HQ266 G01** `agent/space-bunny-pyat-hq266-g01-query-authority-parity-repair-r1 @ dfab8607177e02872a2da6cfa65a6d97bed8bdda`.
Commission `WORKER_COMMISSIONS/PYAT-HQ266-G01-QUERY-AUTHORITY-PARITY-AND-G2-INTEGRATION-R1/00_COMMISSION.md`.
**Agent/model:** existing Space Bunny/OpenCode engineering worker; Space Bunny Max (`space-bunny-free`) / native Max.
**State:** ISSUED_NEEDS_HUMAN_LAUNCH, not running.
**Task:** first prove original query-authority C1 evidence nonnull and real G2-bound positive on exact fixture; only then minimal G01 unadopted ingress/test edits, typed/hostile evidence, clean-committed tests. Stop with precise tested diagnostic if original positive fails. Original C1/F8/SA/G2/B5/G3 and fixture frozen read-only. Independent clean-SHA review after actual corrected candidate.

## Preserved holds

Ghana R5/R9 two frozen SAVs missing; LiTS canonical 3.4GB P1 missing. No same-host retries, no source/read, no EE12 pair/FF02. G2 HQ259 adopted and G3 HQ262 local lifecycle accepted, but actual selected G1, G0b EE14 operative model-use grant, T1 CURRENT/as-of, T2 empirical world and V3 still absent.

**NEXT:** launch HQ266 author query-authority parity fix; separately arrange authorized custody restoration.
**Terminal:** `HQ266_G01_PARITY_REPAIR_ISSUED__NO_CODE_ADOPTION_G0B_T1_T2`.
