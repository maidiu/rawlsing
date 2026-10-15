# SOROK HQ311 OUT6 — source-free outbox repair implementation return

**Disposition:** `IMPLEMENTATION_RETURNED__REPAIR_CANDIDATE__OUT5_EXACT_14_NOT_EXECUTED__OUTP_POLICY_HOLD__SEPARATE_I2_REQUIRED__NO_ADOPTION`.

**Branch:** `agent/rabochii-sorok-r3-hq311-out6-out5-sourcefree-four-defect-repair-r1`.
**Exact sealed startup:** `065d3aabf0bada9d6c8fe8d8d9a4dee07bba1e92`. Writes only in this worker's assigned return.

## Actual source-free execution

OUT4 pinned author `2afa3022e5551df71b739cf8689e832db85e1196`, original imported source Git blob `c7bb4169d43c715de7dd113b24d3ce897e37beab`. OUT3 exact unpublished? NO: original 22-test archive is **published** at independent return `0ab31e4198299708e700840c1b68e0d94a2ced06`, Git blob `a9c4ee7344526fa335605d76d08def2ac5dcba2a`, SHA256 `fc876b665bd9af6328deec86aa66e93ec0eebf9048ca7a5a0d7d0630cd48bddd`, all verified locally byte-for-byte. Source-free Python 3.13.5, pytest 9.0.2, subprocess, real cold-process os._exit(79) and Git 2.47.3 operational.

| Court | BEFORE | AFTER |
|---|---|---|
| Unchanged original 137 | 135 PASS / 2 RED | 135 PASS / 2 RED |
| Exact OUT3 independent 22 | 22 PASS | 22 PASS |
| OUT4 author 29 | 29 PASS | 29 PASS |
| OUT6 NEW actual-API hostile | 4 PASS / 9 RED in initial 13-case source | 18 PASS / 0 RED, final expanded 18-case source |
| **Combined after repair** | — | **204 PASS / 2 RED across 206; pytest exit 1, zero skips/errors** |

Historical REDs preserved verbatim: S27 authored expectation of forbidden unissued mug movement; stale-two-writer lost-update excluded from single-writer grant. No oracle/test files changed. Full local evidence archive contains complete per-case matrix and the nine actual pre/post XML/log pairs.

## Exact implementation and verified identities

A checked unified patch `OUT6_EXACT_SOURCE.patch` applied to OUT4's original `outbox_prototype.py` recreates the **actually executed** candidate Git blob `aa002cb634e81cb980820c14220a1ab55bc5e015` (SHA256 `b58da0f58a79c562cda5019d6c5c3389c6a5616ff9acc297ae778c125db97e23`). `test_out6_receipt_repair.py.xz` decompresses to the exact executed 18-case file Git blob `c1bbfdddf0cffe9a5988aaa11b13e5065dc01406`, SHA256 `57f38cc664fa6be68728d04611fb1a7814c3809c1958a973363d587e2f866928`. Binary files are test/evidence transports, not production candidate adoption.

Repairs at ACTUAL API:
1. `Outbox.fail_to` and `Outbox.fail` preserve terminal `ACKNOWLEDGED` receipts, including attempts/ACK-count. Failure of never-sent receipt is inert. Failed unacknowledged receipt can retry with a fresh attempt as before.
2. No-viewer `emit()` and global `retry()` refuse when sole previously authorized viewer is revoked (including after genuine cold recovery). An independently valid remaining viewer permits legitimate retry.
3. `validate_state()` rejects a client receipt for any never-authorized viewer during detached `restore()` and rehashed cold journal recover, while preserving historical receipts for explicitly revoked viewers and failure atomicity.

## Scientific ceiling, unsupported source/rights, next step

**OUT5's exact original 14 new tests are not published at pinned GitHub SHA and were NOT executed unchanged here.** The reported four defects are grouped into three mechanisms; their four literal test identities cannot be claimed from a remotely authenticated test file. We reproduced direct API failures in independently **NEW** tests, not the original OUT5 bank.

**OUTP owner HOLD:** legacy-fixture admission and whether ACK requires prior projection opportunity remain unadjudicated by this implementer. Nothing in this repair changes either as policy. Sourcefree fixture callback != ADP019 issuer; POSIX-like isolated journal != multiwriter durability; opportunity/ACK != human perception. No original survey data, model/provider calls, production code or registry, V3, PRE-MAIN/CURRENT, semantic adoption or real material/world authority.

**Independent I2:** rerun exact original 137 + OUT3 22 + OUT4 29 + new OUT6 18; add independent adverse controls for ACK/retry and forged client identity after cold crash; distinguish OUT5 evidence HOLD and OUTP policy HOLD from passing author controls.
