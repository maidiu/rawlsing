# Z02 Interface Reconciliation Notes

## Scope

Authority 40 authorizes integration of I01–I04 plus accepted MX01R2 only. Exact sibling production blobs are reused wherever interfaces already agree; integration changes only the seams required to compose them.

## I01 ↔ I02 — controller policy ownership

I01 introduced the exact versioned `FractureMapControllerPolicy` and typed `FractureMapContinuationDecision`.

I02 independently carried a local `Authority37ControllerPolicy`. Z02 removes that duplicate authority owner: `pre553_fracture_map_controller.py` imports and requires I01's policy class. Compatibility names alias to the same I01 type; they do not create another policy identity.

Source-specific response morphology is not controller-policy meaning. The controller now reads optional exact target-component semantic material:
- `non_substantive_domain`;
- `presence_labels_by_cell`.

Those fields remain part of exact query topology/identity and are consumed under the target's source-native response-semantic authorities.

## I01 ↔ I02 — public aggregate admission

I02's operational `OperationalRefEnvelope` is extended with exact:
- policy ref and authority ref;
- root query and parent branch predicate;
- source releases;
- candidate grammar;
- evaluated frontier;
- DiscoveryAuthority;
- discovery-result receipt refs;
- empirical-fact refs;
- MX01 handoff refs;
- depth.

`FractureMapReceiptAccumulator` consumes only refs plus typed continuation decisions and I04 closure refs. Its `seal()` creates I01's public `EmpiricalFractureMapReceipt@1.0.0` with `copied_empirical_payload=False`.

No branch/node/fact warehouse is introduced.

## I01 ↔ I02 — retention / continuation

I02's local string-only stop vocabulary is reconciled to I01's exact typed dispositions.

Authority-37 V1 examples:
- raw n < 25 -> retain low-support state + report-only stop;
- 25 <= raw n < 50 -> retain result with limitation + report-only stop;
- raw n >= 50 with remaining lawful candidates and depth below 4 -> retain and continue eligible;
- depth ceiling -> retain terminal stop;
- no remaining lawful predictors -> retain terminal stop.

`STOP_RECURSION != DELETE_BRANCH` remains binding.

## I02 ↔ MX01R2

The accepted MX01R2 production module is reused byte-for-byte from:
`1773c9a12b3f60489635c562ff60f7190e99a2f5`.

The controller continues to use the public `RecursiveBranchHandoff`, `recursive_parent_atom`, and exact handoff-aware I05 execution path. No integration code reconstructs child membership from a caller-provided respondent list.

## I03 ↔ I04 — direct J3

I03 had already proved direct exact J3 execution; I04's high-level composer still declared a J2 integrated ceiling.

Z02 raises only that integration seam:
`CURRENT_EXECUTOR_MAXIMUM_TARGET_ARITY_J = 3`.

When exact composition authority permits J3, I04 enumerates every canonical target triple, mints exact queries, and executes them through I03. J3 validation requires:
- direct same-respondent higher-order evidence marker;
- exact target-triple identity;
- `pairwise_projection_not_identity_equivalent = true`;
- `AUTHORITY37_J3_DENOMINATOR_CONSERVATION@1.0.0`;
- distinct source/risk, branch, per-target and three-way-joint member/count surfaces;
- exact same-respondent cell-member refs;
- supported-cell partition of the exact joint denominator.

J>3 remains fail closed.

## I04 closure receipt

`BranchCosignatureTopologyClosureReceipt@1.0.0` remains operational/ref-only. It now includes J3 query/fact refs, expected/evaluated triple counts, maximum completed target arity, and exact J1/J2/J3 coverage state. It does not copy empirical cell payload.

## I05 noninterference

Z02 does not alter I05's evaluate-all complete-frontier algorithm or allow partial-result adaptation.

The imported I03 delta in `pre553_discovery_exact.py` is the Authority-37 J<=3 authority/grammar ceiling. The controller's pre-existing open-frontier guard remains the temporal firewall: generation N+1 cannot be composed while generation N is still open.

## PRE-V3 / V3 firewall

The public fracture-map receipt preserves zero direct actor/persona/belief/V3 effects and requires separate downstream semantic/structural/actor/V3 authority. Controller, J3, and co-signature execution remain actor-independent empirical PRE-V3 functions.

## Acceptance-oracle isolation

No I05/I06/I07/I08 expected-answer artifact was read as an implementation input.

An overbroad post-implementation test command accidentally included a frozen whole-machine blob-pin acceptance surface. Its pre-integration expected-hash failure was quarantined and was not used to change production. The successful final run uses the Authority-40-mandated Z02 suites plus the new integration regression.
