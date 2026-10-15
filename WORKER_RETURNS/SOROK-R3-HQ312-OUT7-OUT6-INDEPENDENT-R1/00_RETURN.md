# SOROK HQ312 OUT7 — Independent OUT6 sourcefree court

**Verdict: REVIEW_REVISE — two distinct new restored-state integrity failures; no adoption.**

## Custody and scope
- Directly verified sealed startup ff1d2240ef43c8de717abc751cd7dee739e26a73.
- Reviewed OUT6 673233571b7d899c309dd26f9b9cd2508404c0b6; exact imported source native Git blob aa002cb634e81cb980820c14220a1ab55bc5e015.
- Exact OUT3 22-test archive Git blob a9c4ee7344526fa335605d76d08def2ac5dcba2a; SHA256 fc876b665bd9af6328deec86aa66e93ec0eebf9048ca7a5a0d7d0630cd48bddd. Archive bytes and extracted test source independently verified.
- OUT4 29-test source byte-matched pinned OUT4 archive. All 137 original sources and original 22, 29 and 18 test sources unmodified. Original source identities in evidence archive.
- Frozen S01–S28 semantic oracle Git blob 782ba75ee94f24908100b1f3464e7035497d546c directly read; no semantic override.
- Actual Python 3.13.5, pytest 9.0.2, Git 2.47.3 and subprocess; actual os._exit(79) pre/post rename and cold recovery. No human perception owner.

## Actually reproduced
| Suite | PASS | FAIL | TOTAL |
|---|---:|---:|---:|
| Original 137 | 135 | 2 | 137 |
| Exact unchanged OUT3 | 22 | 0 | 22 |
| OUT4 author 29 | 29 | 0 | 29 |
| OUT6 author 18 | 18 | 0 | 18 |
| **Inherited total** | **204** | **2** | **206** |
| New independent OUT7 hostiles | 17 | 4 | 21 |
| **Full actual combined court** | **221** | **6** | **227** |

All 227 cases actually executed in the completed combined run in 24.52s; zero skips/errors; pytest exit 1. Complete per-case JUnit, raw stdout, source identities, independently authored 21-test Python source and expectation freezes retained in the committed core evidence archive.

## New independent RED 1 — Aggregate transport ACK forged on restore (I08, I13)
Under STRICT admitted viewer-bound event, client V remained DELIVERED_UNACKED, ack_count=0. Replacing aggregate record with state ACKNOWLEDGED and ack_count=1 passes OutboxPrototype.restore even though the public aggregate ACK entrypoint requires an actual ACKed client. The same internally impossible state survives actual cold Journal.recover after recomputing the journal unkeyed SHA256. It is a receipt congruence failure, **not** a policy verdict on whether ACK requires prior projection opportunity.

## New independent RED 2 — Forged revoked viewer zero-attempt client receipt (I09, I14)
Starting with only A authorized, a forged snapshot adds revoked_viewers[event]=[B] and a synthetic B client receipt NOT_SENT with attempts=0. Restore and cold Journal.recover accept that as historical delivery, though normal emit_to never persists a zero-attempt client delivery. Check structural reachable client receipt transitions; do not pretend a recomputable digest proves external historical authorization provenance.

## Preserved historical REDs
1. test_s27_material_move_needs_world_owner — unissued mug physical movement expected by historic test; world owner remains MISSING.
2. test_replay_manual_two_writers_can_lose_first_committed_event — stale two-writer overwrite outside single-writer durability claim.

Seventeen new hostile positives/negatives PASSED: ACK terminal idempotence, legitimate failed retry, sole-viewer revocation after cold restore, second-viewer continuation, ordinary unauthorized ghost-client refusal, counter corruption rejection, atomic restore refusal, no human perception from ACK, cold rehashed-ghost refusal, and real crash boundaries.

## Owner HOLDS and limitations
OUT5 unpublished exact fourteen new tests NOT RUN and NOT implied by new OUT7 tests. OUTP L1/L2 legacy-fixture admission and A1/A2 ACK opportunity policy HOLD: only competent owner chooses. No ADP019 issuance, genuine human perception, external trusted journaling, original sources/model calls, production promotion, multiwriter durability, protected CURRENT/PRE-MAIN or V3 operation.

## Retained evidence
OUT7_REMOTE_CORE_EVIDENCE.tar.xz authenticated Git blob 4801d1918437a926e0e2e5a4836bf43fca528533; SHA256 0b4eb689965b04b17dad6c0a3eb2594e833571f30cfc581255da9a0299547a89. Contains full 227-case XML and stdout, per-suite JUnit/logs, independent hostile source, frozen expectations, detailed matrix, environment passport, reproducibility and owner instructions.
