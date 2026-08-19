# VELIKII VOZHD — CHAT REASSIGNMENT WAVE 02

Status: `ACTIVE__EXISTING_CHAT_FOLDER_ORDERS_INSTALLED`
Common semantic base: `baa257cb901ad8e5dc4d89faf2d81ea6f442ff8d`
R03 broad topology: `CLOSED_UNCHANGED`
Production implementation: `FORBIDDEN`

## Operating rule

Each reassigned chat receives `00_NEW_ROLE_AND_TASK.md` inside its CURRENT/OLD worker folder on its CURRENT/OLD branch. For completed workers, the accepted semantic return remains pinned to the exact pre-reassignment head recorded below. The administrative reassignment commit does not amend or supersede that accepted return.

The worker must read `00_NEW_ROLE_AND_TASK.md`, then switch to the NEW mission branch named there before writing mission outputs. It must not write new mission outputs onto the old accepted branch.

User dispatch can therefore be exactly: `Check your folder instructions for your new role and task.`

## Assignment map

1. OLD CHAT `S554D` — accepted head `a2073b851c91c16e8d8cc77b5fa7a1e581a7c0f4` -> NEW CLASS `SEAM BINDER` -> `M1_BINDER` -> branch `agent/vozhd-trii-dr-r03-seam-m1-temporal-v554`.
2. OLD CHAT `SCR555` — accepted/local head `49a9ce7cd830eb670cf1f9d381d4d33e56ddf682` -> NEW CLASS `SEAM BINDER` -> `M2_BINDER` -> branch `agent/vozhd-trii-dr-r03-seam-m2-atomic-route`.
3. CHAT `SCRV3` -> CLASS `SUB-VOZHD` -> continue standing `SCRV3` branch `agent/vozhd-trii-dr-r03-close-v3-empirical-possibility`.
4. OLD CHAT `SCR5578` — accepted/local head `06eefed7bb8e7db7fd2465aa262653ed95461e84` -> NEW CLASS `FLOATING SPECIALIST` -> `SV3A` -> branch `agent/vozhd-trii-dr-r03-spec-v3-input-lifecycle`.
5. OLD CHAT `SCRV2APP` — accepted/local head `24f8811bb7d2eaa18cfac1cb907c48bba8d08f23` -> NEW CLASS `FLOATING SPECIALIST` -> `SV3B` -> branch `agent/vozhd-trii-dr-r03-spec-v3-comparator-snapshot`.
6. OLD CHAT `SCR553` — accepted head `b261ff885b2b7fd2cd065917b862eb541e24c4a2` -> NEW CLASS `FLOATING SPECIALIST` -> `SV3C` -> branch `agent/vozhd-trii-dr-r03-spec-v3-effective-time-source-state`.
7. OLD CHAT `SV3M` — accepted feeder head `0ce8eb656fec6a3ac0d2a36a12c9ba217603e7cb` -> NEW CLASS `FLOATING SPECIALIST` -> `SV3F` -> branch `agent/vozhd-trii-dr-r03-spec-v3-structural-peer-prior`.
8. CHAT `SINSP` -> CLASS `INSPECTORATE` -> continue existing branch `agent/vozhd-trii-dr-r03-inspectorate-stage-close` with updated exact-head attack set.
9. OLD CHAT `SCR556` — accepted/local head `9cfefc722f51cfab64952f004afef67fe65eb4a5` -> NEW CLASS `SEAM PREFLIGHT SPECIALIST` -> `M3_PREFLIGHT` -> branch `agent/vozhd-trii-dr-r03-seam-m3-preflight`.
10. OLD CHAT `S5578C` — accepted feeder head `50d9b9f0ea36c95bd2423206901aa39e3b48092a` -> NEW CLASS `SEAM PREFLIGHT SPECIALIST` -> `M4_PREFLIGHT` -> branch `agent/vozhd-trii-dr-r03-seam-m4-preflight`.

## Explicitly not reassigned in this wave

`SCR554` remains banked at accepted local head `b5d745ac70c833324c8be0addf6c08ad72372263` and is not consuming a worker slot.

## Dependency law

M1 and M2 may run now. M3 preflight and M4 preflight are non-dispositive only. Final M3 remains blocked on accepted M2; final M4 remains blocked on accepted M3; M5 remains blocked on accepted M4 + SCRV3; M6 remains blocked on accepted SCRV3.
