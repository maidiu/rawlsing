# SCRV3 — Metabolism Authority

**Authority:** `V3_EMPIRICAL_POSSIBILITY_METABOLISM_AUTHORITY@1.1.0`  
**Canonical core SHA-256:** `e0cd3c8a4443c59b7e97cc151a7db9298310f7a7e766b593fb90968546d66939`  
**Read matrix SHA-256:** `6a4227bb3df913b8564ba0d994ce5c2be81bf0f6e8d8b5a164ba546db59fa2d1`

This authority owns read permission, operation ceilings, lifecycle admission and replay obligations. It owns no actor-state domain semantics.

## Default-deny theorem

If a named V3 semantic owner does not itself explicitly bind `V3EmpiricalPossibilityInput` / PSEPF use in its accepted canonical rule/registry serialization, PSEPF transition effect is exactly zero.

The metabolism authority cannot amend ADP/CAN semantics merely by naming an operation.

## Current permissions

Current positive actor-transition rows: **none**.

Only `SCRV3-RP-V3M002-V2` is positive, for noncausal `EXACT_GEOMETRY_DEREFERENCE`.

Defined future-compatible operation classes are:

- `OWNER_RULE_CONSTRAINT_TEST` — may reject/retain an independently lawful candidate; cannot create one;
- `OWNER_RULE_CANDIDATE_ANNOTATION` — nonstate annotation only;
- `OWNER_RULE_CANDIDATE_FILTER` — removal only; cannot add candidates;
- `OWNER_RULE_CANDIDATE_WEIGHT` — exact owner transform over an already-lawful candidate set; stochastic selection remains ADP-020-owned.

None is presently enabled for actor transitions.

## Owner evidence

- ADP-010: `0eac41d081b112255dcfc6dd42a6afab15a2928b` @ `dd7720bf7201eb215e8a612cbd70952a728ca37b` — no PSEPF binding; encounter/exposure remain witness-bound.
- ADP-011 — no accepted canonical machine serialization located.
- CAN-008: `7bd28360ec6a74975bb7eb809f6ad397529491b3` @ `8468d5ab4a47513fc59cbf569de543033063e020` — no PSEPF binding.
- CAN-010: `219e2725223b110ef0dee7f3851c23a78f6ff7a6` @ `02354715c047bcc58a490e14d29f3a216e817815` — no PSEPF binding.
- CAN-011: `f2fc968757da69b9aa9d2e8c00bf301144d4646b` @ `5187cff1736813b5be857a48253c9bb83f049261` — no explicit PSEPF binding.
- CAN-012: `6463d48236ad6b0005a5fc63b0598315ad7db585` @ `8998c583b3687f974704368866efa91cd2787877` — PSEPF cannot substitute for causal parents/rupture basis.
- ADP-021: `1db081786d2b7d4465a9efa7d69b6a05741b47bc` @ `c83f0cfe2ee9039c7f8e3cf90b94941a1c186c5c` — no empirical lifecycle trigger.

These are exact Git blob content identities at the named accepted commits, not SCRV3-invented authority hashes.

## Geometry / source state

PSEPF geometry remains upstream. V3 records refs/hashes and exact component paths consulted, never copied mass tables or flattened summaries.

`OBSERVED_ZERO != ZERO_SUPPORT`; source disagreement remains source-indexed. Cross-source composition defaults to none. Provenance reachability is not pooling authority.

## Lifecycle / replay

V3 owns wrapper-only `V3_REBIND`. Comparator/query/field/source owners own `UPSTREAM_REQUERY` when upstream validity changes. Refresh never rewrites history.

Every consultation is receipted as `V3EmpiricalPossibilityReadReceipt@1.0.0` with exact permission, owner serialization/rule/transform, source/PSEPF hashes, component paths, causal parents, time receipt, candidate sets, ADP-020 receipts and pre/post state hashes.

Same prior may diverge through later lawful history or separately recorded RNG. Each exact authority/history/RNG record must replay identically. A deterministic RSC+EPI→persona shortcut remains forbidden.
