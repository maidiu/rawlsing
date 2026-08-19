# SV3M DIVERGENCE / REPLAY HOSTILE HARNESS

## Purpose

Prove both halves simultaneously:

1. identical upstream priors do **not** force identical developed lives;
2. each exact lawful life replays deterministically when its own causal history, authority versions, and ADP-020 RNG receipts are fixed.

This harness is a contract/test oracle, not implementation.

## Fixture H0 — common branch state

Construct two actor-run branches A and B with identical content-addressed inputs:

```text
initial_actor_state_hash = S0
resolved_structural_context_hash = RSC0
v3_empirical_possibility_input_hash = EPI0
psepf_set_hashes = P0[]
objective_actor_fact_snapshot_hash = OAF0
metabolism_authority = V3_EMPIRICAL_POSSIBILITY_METABOLISM_AUTHORITY@1.0.0#H
effective_time = T0
```

Assertions before branching:

- A and B have identical `S0`, `RSC0`, `EPI0`, `P0[]`, `OAF0`, authority binding and T0.
- all source-indexed J-way geometry is reachable by exact immutable references;
- no modal/top-k/scalar substitute is present in the canonical V3 input;
- ActorComparatorReceipt is reachable only as provenance;
- no actor state was derived from PSEPF while creating the fixture.

## Fixture H1 — lawful post-branch divergence by history

At T1, give A an exact ADP-010-admissible encounter/exposure witness chain and give B a lawful nonoccurrence/absence of that witness.

If the owner transition consults PSEPF:
- both runs consult the same exact EPI/PSEPF;
- any read must pass the same metabolism permission row;
- the read can constrain/annotate an already-lawful candidate only;
- the encounter/exposure occurrence still comes from the witness/history distinction, not from PSEPF.

At T2+, allow resulting owner-governed transitions:
- A may form a causal memory only through ADP-016;
- A may acquire a belief/knowledge/claim-access state only through ADP-017 with a typed epistemic effect;
- B remains without those states unless its own lawful history creates them.

Expected:
`state_A_final_hash != state_B_final_hash` is lawful.

Required proof:
every differing field in the final actor states is traceable to a post-branch V3 causal parent chain, not to different priors.

## Fixture H2 — lawful divergence by recorded causal RNG

Hold the same prior and same lawful candidate set semantics, but use different **recorded** ADP-020 decision receipts in two distinct causal runs/scopes.

Requirements:
- candidate set exists independently of RNG;
- the owning transition, not ADP-020, defines candidate semantics;
- ADP-020 stream/scope/rule-invocation/candidate-set identity is exact;
- different run seed/receipt lineage may lawfully select different candidates;
- selected candidates remain inside the lawful set.

Expected:
different selected transition histories may produce different developed states.

Forbidden:
- ambient RNG;
- unrecorded LLM sampling as causal truth;
- using PSEPF mass itself as the RNG draw;
- adding fallback candidates because the field has support.

## Fixture H3 — exact-history replay

For each run independently, freeze:

```text
all authority IDs/versions/content hashes
all V3 input/PSEPF/source component hashes
all exact cells/component paths actually read
all owner-transform IDs/versions/hashes
all causal parent refs
all pre/post candidate-set hashes
all ADP-020 receipts
all committed event/transition IDs
all pre/post actor-state hashes
all effective times
```

Replay assertions:

- Replay(A receipts) -> exact A event sequence and final state hash.
- Replay(B receipts) -> exact B event sequence and final state hash.
- Repeat replay is byte/content-hash stable.
- Removing a consulted-field receipt, owner-transform hash, causal parent, or RNG receipt -> fail closed.
- Replacing any authority/field with mutable `latest` -> fail closed.
- Substituting B's RNG receipt into A changes replay identity or fails exact-coordinate validation; it never silently produces accepted A replay.

## Fixture H4 — deterministic-collapse hostile

Construct an illicit engine:
`persona_vector = deterministic_function(RSC0, EPI0)`.

Even if deterministic and replayable, it fails because:
- it bypasses V3 event/history owners;
- it makes identical priors determine identical lives;
- it converts peer priors into finished actor state;
- its replay demonstrates shortcut determinism, not lawful causal replay.

Expected: hard rejection.

## Fixture H5 — mass -> belief

Attempt:
`ActorEpistemicState.belief_probability = PSEPF.mass(cell)`.

Expected:
- metabolism layer returns `READ_DENIED` or owner contract rejects the operation;
- no ADP-017 epistemic transition is committed;
- actor-state hash unchanged;
- any audit receipt records `NO_PSEPF_TRANSITION_EFFECT`.

## Fixture H6 — modal cell -> response

Attempt:
`response = argmax(PSEPF)`.

Expected:
- rejected even when CAN-008 is a conditionally permitted reader;
- a CAN-008 owner-specific candidate set and explicit transform would be required;
- modal-cell identity alone has no response semantics;
- no mutation.

## Fixture H7 — survey cell -> memory/knowledge

Attempt direct memory and knowledge creation from a supported configuration.

Expected:
- ADP-016/017 read permissions are denied;
- no memory object;
- no ActorEpistemicEffect;
- no claim-access permission;
- no mutation.

## Fixture H8 — comparator receipt as prior

Give V3 a positive ActorComparatorReceipt but no PSEPF input.

Expected:
- comparator receipt cannot satisfy metabolism intake;
- no field semantics reconstructed from comparator metadata;
- no causal mutation.

## Fixture H9 — generated structural-position reconstruction

Attempt to infer ADP-009 generated position from PSEPF conditioner coordinates or matching labels.

Expected:
- reject;
- no objective actor fact created;
- no comparator feedback loop.

## Fixture H10 — source-majority and source conflict

Provide three source components:
- U1 supports candidate C;
- U2 supports alternative D;
- U3 is noncomparable.

Attempt `majority/strongest source wins`.

Expected:
- source conflict/noncomparability preserved;
- no pooled or voted actor truth;
- operation proceeds only if an exact owner-specific source-composition rule exists; otherwise typed no-effect/deny.

## Fixture H11 — hidden scalarization

Provide a source-indexed J-way multimodal field with a supported minority cell that changes the result of any full-geometry owner predicate.

Attempt to replace it with:
- modal cell;
- top-k;
- marginals;
- pairwise projections;
- latent scalar;
- averaged source score.

Expected:
- canonical input still points to full exact field;
- substitute summary cannot satisfy exact read contract;
- if an owner transform exists, its exact ID/version/hash and cells read are recorded;
- hidden transform -> reject.

## Fixture H12 — wrapper geometry truncation

Remove one minority component from a copied wrapper summary while canonical PSEPF still contains it.

Expected:
- wrapper summary is nonsemantic;
- semantic read dereferences canonical PSEPF;
- if code attempts to use the copied summary instead, hash/contract mismatch causes fail closed.

## Pass criterion

The harness passes only if all are true:

```text
same upstream priors permit >1 lawful developed history
AND
each exact history replays deterministically
AND
every prior consultation is permissioned and receipt-bound
AND
no direct prior-to-state shortcut survives
AND
no source plurality or exact geometry is silently collapsed
```
