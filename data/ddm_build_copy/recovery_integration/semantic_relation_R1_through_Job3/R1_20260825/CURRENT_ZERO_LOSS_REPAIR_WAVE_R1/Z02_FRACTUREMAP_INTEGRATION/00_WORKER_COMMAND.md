# Z02 — FRACTURE-MAP PRODUCTION INTEGRATION / ADMISSION R1

Role: VOZHD TRII
Repository: `maidiu/rawlsing`
Worker branch: `agent/verkhovod-z02-fracturemap-integration-r1`
Exact starting HEAD: `c649d57c14ca6c0f84571beab4610c007c2484f2`

Read Authority 40 first.

Consume these exact sibling implementation refs as authorized inputs:
- I01 final `dd3f3aca306e303d5aea7b7d732f291f4bff330e`
- I02 final `9b6d6824739ba01ff9912fab20c740b05d6fef21`; tested code `f62f1646e0c5db102bdb006e401a675e12946d84`, CI 46/46
- I03 final `658dc1d610249eac97abf82a2bb61cb9ceb689b1`; tested code `3b5dece60b17bc774ea8de8829985eb62c5a23f3`, bounded CI 126/126
- I04 final `2474f8ef5907d5f5b70344e4a1c9ea9dbe14ecd8`
- accepted MX01R2 `1773c9a12b3f60489635c562ff60f7190e99a2f5`

Integrate the minimum production delta only. Do NOT merge branch histories wholesale. Recover exact files/deltas and reconcile interfaces under Authority 37/40.

Required integrated behavior:
1. I05 exact complete-frontier evaluator remains semantically unchanged.
2. `FractureMapControllerPolicy` + typed continuation/stop law become the controller's exact policy owner.
3. I02 result→next-frontier controller operates between complete I05 invocations, never mutating an open frontier.
4. I02 operational aggregate envelope is wired to I01 public `EmpiricalFractureMapReceipt@1.0.0` without copying empirical payload or inventing a warehouse.
5. I03 direct exact J=3 execution is active only under exact versioned authority with `maximum_target_arity_J >= 3`; J>3 fails closed.
6. I04 source/instrument-governed substantive target enumeration emits the complete J1/J2/J3 target frontier through I03. Demographic/positional coordinates remain conditioners, not attitude targets.
7. exact discovered-child handoff uses MX01R2 public/replayable semantics; no caller respondent-list reconstruction.
8. denominator grains, raw vs governed weight, typed special states, branch retention vs continuation, and PRE-V3/V3 firewall remain distinct.

Run full relevant repository tests, not only sibling focused suites. At minimum include empirical objects/authority, I03 query, I05 discovery, recursive handoff, fracture-map contract/controller, co-signature composition, replay audit, and hostile query frontier tests. Add/fix integration tests where sibling interfaces disagree.

Do not consume I05/I06/I07/I08 expected answers to implement generation behavior. Those remain post-integration judges.

Output exact tested integration commit, complete test receipt, changed-file ledger, interface reconciliation notes, and `RESULT.md/json`.

No MX04, MX05/C09, A/B/C selection, V553+ redesign, or V3 work.
