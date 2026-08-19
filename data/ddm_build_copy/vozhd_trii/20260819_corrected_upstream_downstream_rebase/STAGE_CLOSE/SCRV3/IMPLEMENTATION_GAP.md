# SCRV3 — Implementation Gap

## Status

This court changes **no production code**. The exact common base contains no top-level current production `v3/` tree; accepted V3 ADP/CAN authorities and recovered historical V3 remain specification/continuity evidence. SCRV3 therefore closes the contract, not an implementation.

## Required future implementation work

A lawful implementation must provide, without reopening this contract:

1. `V3EmpiricalPossibilityInput@1.0.0` schema/type and canonical content hashing.
2. Exact immutable PSEPF dereference by ref/hash with no geometry copy.
3. Per-source typed state validation preserving negative/disagreement distinctions.
4. `SCRV3_EFFECTIVE_TIME_ALIGNMENT_V1`.
5. Lifecycle validator with separate `V3_REBIND` and `UPSTREAM_REQUERY` dispositions.
6. Intake causal-parent receipt creation binding ordered V3 causal parents separately from empirical prior provenance.
7. Metabolism-authority validation and the normative read-permission matrix.
8. Owner-rule empirical-use bindings for any CAN-008/CAN-010/CAN-011/CAN-012 rule that actually intends PSEPF effect. **No such formula is invented by SCRV3.** Until one exists, its PSEPF effect is zero.
9. ADP-020 integration only after owner-produced exact candidates/weights exist; ADP-020 must never read PSEPF directly.
10. Replay validation covering exact history, scheduler order, rule versions, RNG receipts, intake/provenance and peer-prior identities.
11. Hostile tests from `HOSTILE_TEST_ORACLE.md`.
12. Final joint V3 input signature after SCR5578 freezes the exact terminal `ResolvedStructuralContext` contract.

## Explicit non-gaps

The following are not implementation latitude:

- copying empirical geometry into the thin input;
- using mass/modal/source disagreement as actor state;
- converting `ActorComparatorReceipt` into a V3 prior;
- converting `ReplayReceipt` into authority;
- silently using mutable latest;
- defaulting or collapsing typed negatives;
- repairing stale empirical fields inside V3;
- merging structural and empirical priors;
- treating same priors as same life;
- using nondeterministic replay.

## Only remaining specification dependency

The only unresolved exact-contract datum is the terminal `ResolvedStructuralContext` integration signature owned by SCR5578. All SCRV3-local semantics are frozen.
