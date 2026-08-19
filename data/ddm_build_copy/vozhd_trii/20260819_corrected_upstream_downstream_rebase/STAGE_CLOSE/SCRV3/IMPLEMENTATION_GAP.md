# SCRV3 — Implementation / Authority Gap

SCRV3 closes the stage contract; it does not authorize production implementation.

## 1. No current positive actor-transition PSEPF owner binding

The accepted owner serializations inspected do not currently bind PSEPF / `V3EmpiricalPossibilityInput` as an actor-transition input:

- ADP-010 blob `0eac41d081b112255dcfc6dd42a6afab15a2928b` @ `dd7720bf7201eb215e8a612cbd70952a728ca37b`;
- ADP-011: no accepted canonical machine serialization located;
- CAN-008 blob `7bd28360ec6a74975bb7eb809f6ad397529491b3` @ `8468d5ab4a47513fc59cbf569de543033063e020`;
- CAN-010 blob `219e2725223b110ef0dee7f3851c23a78f6ff7a6` @ `02354715c047bcc58a490e14d29f3a216e817815`;
- CAN-011 blob `f2fc968757da69b9aa9d2e8c00bf301144d4646b` @ `5187cff1736813b5be857a48253c9bb83f049261`;
- CAN-012 blob `6463d48236ad6b0005a5fc63b0598315ad7db585` @ `8998c583b3687f974704368866efa91cd2787877`;
- ADP-021 blob `1db081786d2b7d4465a9efa7d69b6a05741b47bc` @ `c83f0cfe2ee9039c7f8e3cf90b94941a1c186c5c`.

Therefore implementation must not enable PSEPF actor-transition effect merely because SCRV3 defines constraint/annotation/filter/weight operation classes.

## 2. Future owner amendment gate

Any future positive owner must itself serialize: exact EPI schema/version; exact SCRV3 permission+operation; exact source/component semantics; independently lawful pre-PSEPF candidate/basis; source-state/composition treatment; exact predicate/filter/weight transform ID/version/hash; pre/post candidate-set identity; causal-parent nonpromotion; effective-time rule; replay receipt; ADP-020 binding if stochastic; explicit no-direct-state-assignment ceiling.

Until then: `NO_PSEPF_TRANSITION_EFFECT`.

## 3. Runtime work

EPV3 did not establish a current terminal top-level V3/V2 production implementation tree. Runtime implementation must add exact validation for:

- `V3EmpiricalPossibilityInput@1.1.0`;
- metabolism core hash `e0cd3c8a4443c59b7e97cc151a7db9298310f7a7e766b593fb90968546d66939`;
- read matrix hash `6a4227bb3df913b8564ba0d994ce5c2be81bf0f6e8d8b5a164ba546db59fa2d1`;
- effective-time hash `2f9f2319975d8f7a45a31722b11436c21922866cc12ba5faccb7de96794fb8c4`;
- exact source-state/geometry dereference and `V3EmpiricalPossibilityReadReceipt@1.0.0`;
- rebind/requery handling with no current actor-transition read grants.

## 4. Scheduler seam

SCRV3 may classify `V3_REBIND` or `UPSTREAM_REQUERY`, but ADP-021 v1 has no empirical lifecycle trigger. A later accepted scheduler/orchestration binding must carry that disposition without turning it into actor history.

## 5. M4/M5

SCR5578 local head `06eefed7bb8e7db7fd2465aa262653ed95461e84` is sufficient for bounded peer-interface preparation only. The final exact `ResolvedStructuralContext` integration signature must wait for accepted M4 producer bindings.

## 6. M6 is already exact

The positive V3→V2 type is accepted ADP-017 `ActorAccessibleRenderEnvelope`, blob `eece4f3f2f3f9288ab9bbc645dc81e20a99e1280` at `614775fa05c5d904adff4b53f353637b869e6842`. V2 must not dereference opaque upstream provenance for persona/voice/belief/response semantics.

No exact committed SV3A/SV3B/SV3C/SV3F return was visible at this adjudication point; SCRV3 did not wait or infer their contents.
