# SUB-VOZHD B — B19Q/B20Q QUALIFICATION COMMISSION + CURRENT FLIGHT STATE R1

Status:
`B19_B20_IMPLEMENTATIONS_FROZEN__B19Q_B20Q_QUALIFICATION_ACTIVE_IN_PARALLEL__COMMON_HARNESS_AND_C09_GATED`

Campaign branch:
`agent/sub-vozhd-architecture-compiler-dva-chetiri-r1`

Qualification authorization:
`1c02ae8ce6f811a2e8a4fbf83f32acbf8003a5bf`

## B19Q

Branch:
`agent/rabochii-subv-b-as4i-route-a-adapter-qualification-r1`

Starting HEAD:
`390841ab32324276e68912d597a16056610e24c0`

Handoff:
`0adb463d97b9f4726eb4aad8cc112c9cc092ae13`

Exact job:
execute the already-committed B19 bounded pytest court twice in fresh processes; no code edits.

PASS:
`AS4I_ROUTE_A_ADAPTER_QUALIFICATION_COMPLETE__READY_FOR_COMMON_ABC_HARNESS_INTAKE`

## B20Q

Branch:
`agent/rabochii-subv-b-as4i-route-c-cacc1-cacc2-parity-qualification-r1`

Starting HEAD:
`a81f198dc03d64e65d81b5491fd88e352a6ead38`

Handoff:
`3cc730b04a4da31b97b80c8d1bf612da4301a9bf`

Exact job:
execute the already-committed B20 qualification driver under `pyarrow==25.0.1`, preserve internal two-process replay and an outer fresh repetition; no code edits.

PASS:
`AS4I_ROUTE_C_CACC1_CACC2_PARITY_QUALIFICATION_COMPLETE__READY_FOR_COMMON_ABC_HARNESS_INTAKE`

## Environment requirement

Neither B19Q nor B20Q requires Library or real survey source bytes.

They require:
- a real repository checkout at the exact branch tip;
- runnable Python subprocesses;
- pytest for B19Q;
- pyarrow 25.0.1 + pandas for B20Q.

A local machine, Codex/Work execution surface, or any equivalent repo-checkout execution host is acceptable.

## Failure law

Any red committed test/court:
- is a real blocker;
- must be preserved exactly;
- must not be repaired inside the qualification-only branch.

A separate repair worker will be commissioned if needed.

## Next gate

Only after BOTH B19Q and B20Q PASS:
- bank/adjudicate both exact implementations + qualification proof;
- commission HB04 common deterministic A/B/C harness.

WVS7 external semantic/replay certification remains independently open.

## Hard gates

No:
- C09 execution;
- WVS7 execution;
- A/B/C ranking;
- common harness before both qualifications;
- OBL037;
- architecture/topology selection;
- positive V3.

Terminal:
`SUB_VOZHD_B_B19Q_B20Q_QUALIFICATION_ACTIVE__COMMON_HARNESS_AND_C09_GATED`
