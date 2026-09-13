# PRE-V3 Fourth-Wave Final Registry R1

Status: `W4_F01_F07_COMMISSION_BRANCHES_MINTED__PARALLEL_RELEASE_ACTIVE`

HQ third-wave fan-in authority: `3781860269c20006d82f9bec40df3a24b90861a0`
M3 R2 central integration merge: `9d35ed4bb6fca727982fb05035adb74f742b66ce`
M3 integration receipt commit: `e66392e1f0a9a828c2a8a67c3d33e1d723c3d796`

| ID | Branch | Commission tip | Exact grain | Library |
|---|---|---|---|---|
| F01 | `agent/rabochii-prev3-w4-f01-world-validity-first-root-r1` | `8d41bcfb3786d2606a056e1bb7b9f7ef19e9b473` | `PREV3_OBJECTIVE_WORLD_VALIDITY_BASIS_AND_FIRST_REAL_ROOT_R1_ONLY` | NO |
| F02 | `agent/rabochii-prev3-w4-f02-lits-selector-closure-r1` | `468fd77d624e6cb73f9c14825d6b75cb433cca36` | `PREV3_LITS1_Q310_Q311_C11_SELECTOR_CLOSURE_AND_LEARNED_FRONTIER_READOPTION_R1_ONLY` | CONDITIONAL / LIKELY — exact LiTS-I carrier only |
| F03 | `agent/rabochii-prev3-w4-f03-position-producer-authority-r1` | `1e92835767fcc3f81ff9d38f2ae615ad150d6cdb` | `PREV3_FFP014_Q73A_BEN0002_OBJECTIVE_POSITION_PRODUCER_AUTHORITY_BINDING_R1_ONLY` | NO by default |
| F04 | `agent/rabochii-prev3-w4-f04-nonevent-currentness-repair-r1` | `593ecbd65c0006803e6f61e1089d0f34b5f07c23` | `PREV3_NON_EVENT_ADAPTER_CURRENTNESS_RECEIPT_VALIDATION_REPAIR_R1_ONLY` | NO |
| F05 | `agent/rabochii-prev3-w4-f05-bounded-evidence-replay-repair-r1` | `abd63d4340d5c296d3ae483b98473a747e6b75db` | `PREV3_BOUNDED_EVIDENCE_REPLAY_PROVENANCE_COLLISION_REPAIR_R1_ONLY` | NO |
| F06 | `agent/rabochii-prev3-w4-f06-hb07-launch-packet-r1` | `71af94ad23a7bc3341a812109d2dd8df7094740e` | `HB07_FINAL_SCRATCH_WORKDIR_CLEANUP_LAUNCH_PACKET_R1_ONLY` | NO by default |
| F07 | `agent/rabochii-prev3-w4-f07-second-canary-instantiation-r1` | `7f5dd315c7fdbfea1e06cfb23e23899acf3eecfc` | `EXACT_SECOND_CANARY_PREV3_ADMISSION_RECEIPT_INSTANTIATION_AND_M1_V554_REPLAY_ONLY` | NO by default; narrow exact lookup only if indispensable |

Parallelism:
- F01-F07 may all begin now.
- F02 must finish before learned-world real-execution redispatch.
- F03 must finish before first real objective-position fact materialization.
- F04 must finish before independent non-event requalification.
- F05 must finish before independent degraded-policy requalification.
- F06 consumes accepted E09 peer `161ea51b80816450323091e566ce46e5b485b7c3`; C09 remains downstream of F06 plus a separate launch court.
- F07 must finish before second-canary independent qualification/composition.
- real-current-world non-event E2E remains additionally dependent on F01.

Closed / no-worker lanes:
- E04 SDTF P1-P5 remains CLOSED under current authority; no source recrawl or rule mint authorized.
- E06 M3 R2 is independently qualified and centrally integrated; no redundant fourth-wave worker commissioned.

No all-lanes barrier.
PRE-V3 remains `NOT_PROJECT_COMPLETE`.

Terminal: `PREV3_FOURTH_WAVE_F01_F07__COMMISSIONED__PARALLEL_RELEASE_ACTIVE__M3_R2_INTEGRATED`