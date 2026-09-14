# RAWLSING HQ OPERATIVE HANDOFF — CHECKPOINT R2

Schema: `RAWLSING_HQ_HANDOFF@1.0.0`

Checkpoint ID: `20260914T1346-0400-r2`

This checkpoint supersedes handoff checkpoint `20260914T1346-0400` only as the **current operative handoff**. It does not supersede or alter Rawlsing semantic authority.

Semantic PRE-MAIN tip remains:

`f156405aeee7076b5a582257d1eee5b3b976b314`

Latest substantive HQ authority remains:

`323555568a5320dbd6c1ad307dbc40f701e4864e`

## Mandatory handoff-maintenance law

After every material HQ state change, HQ MUST:

1. append any durable decision needed to prevent rediscovery/regression to `HQ_HANDOFF/DECISION_LEDGER.jsonl`;
2. create a new immutable checkpoint directory containing `CURRENT.md` and `CURRENT.json`;
3. advance `HQ_HANDOFF/LATEST.json` to the exact commit containing that checkpoint;
4. resolve `LATEST.json` and verify that it reproduces the intended checkpoint before treating the transition as sealed.

A handoff is stale if material operative state changed after the checkpoint named by `LATEST.json`.

Material changes include authority adoption/rejection/supersession/quarantine; qualified code integration; fan-in that changes blockers/wake conditions; active-lane changes; new canonical roots/releases; project-critical execution-gate changes; or any decision a successor must know to avoid redoing work or taking an unlawful next step.

## Constitutional state

PRE-V3 = governed objective world only. V3 owns person/persona/subjective state/realized development.

Preserve:

- `OBJECTIVE_ACTOR_POSITION != PERSON_STATE`
- `OBJECTIVE_OPPORTUNITY != ACTOR_UPTAKE`
- `EVENT_IN_WORLD != ACTOR_EXPERIENCE`
- `STRUCTURAL_RELATION != PSYCHOLOGICAL_DISPOSITION`
- `POPULATION_EVIDENCE != PERSON_TRAIT`
- `WORLD != BIOGRAPHY`
- `PROJECT_CURRENT_OBJECTIVE_WORLD_RELEASE != PRESENT_DAY_WORLD_TRUTH`
- `GIT_ANCESTRY != CURRENT_SEMANTIC_AUTHORITY`
- OBL063 driver/type/person-terminal semantics remain quarantined.

## Current world state

Root #1 exists and replays:

`PREV3WORLD:800a9301ce81207e82c849ee81b220131d31800676deff93801b7dc659946146`

Qualified objective-position fact:

`PREV3POS:c823a816ce6f71431c99b1a466c7313f3766e5d1e7832fc36b6a31f15835dd02`

Adopted two-constituent successor release:

`PREV3REL:c1973cf59447e3ed973713feab18b499856902a1a48d348a62bf4d8628ce5108`

World-currentness receipt:

`cee63962a249f1e9f55f6ddef7a3e7cd88df3cbf8042ecd30af54c2c10315d07`

Root #2 is not yet banked at this checkpoint.

## Active workers

### O01

Branch: `agent/rabochii-prev3-w13-o01-second-world-root-r1`

Commission tip: `4e2658a5dcc1b7f0d860c8184df858b14e088815`

Grain: `PREV3_SECOND_REAL_WORLD_ROOT_CONSTRUCTION_AND_SUCCESSION_REPLAY_R1_ONLY`

Library: `NO`

### O02

Branch: `agent/rabochii-prev3-w13-o02-objective-structural-canary-replacement-r1`

Commission tip: `a6368733ee22e87689b6cc81b5fc31234ba32b24`

Grain: `PREV3_OBJECTIVE_STRUCTURAL_CANARY_REPLACEMENT_SELECTION_AND_OWNER_ADJUDICATION_R1_ONLY`

Library: `NO by default`

## Dormant gates

### Governed courts

N04 return: `72270bf8c8d9390f6f18c43d4c55532bb4df3fcd`

External blocker: GitHub-hosted `ubuntu-latest` runner allocation fails before step execution (`runner_id: 0`).

Do not wake court-dependent lanes until N04 neutral smoke actually receives a runner, executes, and emits a valid receipt.

Then wake M02 qualification, M04 OP014 qualification, and M05 structural-topology qualification in parallel. M04 PASS wakes actual C09.

### LiTS materialization

N02 return: `a06e49fa5ccaa29bd757663c3ca9cf088d963b74`

Exact carrier: `file_0000000036dc81f8b8b546e356590a03`, version 1, `LITS-2006-data.dta`, SHA-256 `7cac43e2ca5b31cb658dc2b3a6cfbcec99363ca8c47da457df90e31b588efc09`.

Blocked until accepted `decode_dta(..., encoding="latin1")` can execute with `pyreadstat`.

Pandas diagnostic counts remain quarantined and are not authority.

## SIG-004

N03 return: `ffa637eca658136ac215a521e332ff18af3ebe7c`

Structural-topology promotion is closed at current authority. Q86A is disposition/attitude-only, not a receiving objective structural position; SDTF P5 is class-only and supplies no concrete channel.

Do not rescue SIG-004 by semantic promotion. O02 searches for a genuinely objective structural canary instead.

## Succession instructions

1. verify O01/O02 branch heads before treating them as returned;
2. fan in genuine returns and make exact HQ decisions;
3. do not relaunch court-dependent work while runner allocation remains broken;
4. do not promote quarantined LiTS diagnostics to authority;
5. do not reopen SIG-004 structural promotion absent new competent evidence;
6. after any material state change, update the handoff checkpoint and `LATEST.json` **in the same HQ cycle** before considering the transition sealed;
7. do not use the user as the sync bus.

Protocol: `HQ_HANDOFF/PROTOCOL.md`

Decision ledger: `HQ_HANDOFF/DECISION_LEDGER.jsonl`
