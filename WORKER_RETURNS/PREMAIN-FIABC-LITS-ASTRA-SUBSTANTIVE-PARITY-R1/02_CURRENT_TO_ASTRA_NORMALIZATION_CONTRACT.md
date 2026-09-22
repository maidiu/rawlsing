# Current → ASTRA Normalization Contract

Schema:

`FIABC_LITS_ASTRA_SHAPED_EMPIRICAL_SUMMARY@1.0.0`

## Purpose

The two sides have different object schemas and therefore different whole-object identities. The normalization contract does **not** make the schemas equal. It projects each side onto the exact empirical fields that ASTRA-D04-R2 accepted as truth and that the current PRE553 result can independently reproduce.

Expected and observed summaries have distinct provenance and are built by different entry points.

## Accepted side

`normalize_accepted_astra_summary()` consumes only immutable ASTRA-D04-R2 evidence:

- typed learned empirical product;
- 77-role execution receipt;
- source/replay receipt.

Before summary construction it checks:

- accepted source SHA, row count, and variable count;
- exact 50/77 frontier;
- identical product/replay frontier seal;
- exact lane counts;
- exact 77-role state and zero result reuse;
- historical R2/R7/R27 roots in both role and replay receipts;
- historical marginal/joint risk-set composition;
- P1's witness is actually non-product;
- P3 exact fractions reproduce the recorded signs;
- P3 is in fact validation-negative rather than a reversal.

Historical P3 labels such as `Q310V1_NEG` are normalized by an explicit closed alias table to current role labels such as `STRATUM:Q310V1:NEG`. No fuzzy aliasing exists.

## Current side

`normalize_current_lits_summary()` consumes the current candidate-neutral `ExactBoundedDiscoveryResult`.

It does not consume ASTRA outcomes.

For each candidate it traces:

- current candidate identity;
- exact rule identity;
- exact query-role list;
- `support_uncertainty_state.query_role_fact_refs`;
- the referenced current `EmpiricalFact` preimage;
- raw denominator;
- complete located cell projection;
- current fact state;
- exact risk-set member cardinality.

D03 roots come from the current adopted `FIABC_LITS_I_D03_RISK_SET_SUCCESSOR_AUTHORITY@1.0.0`. The current authority is itself exact-root pinned. Every logical role's actual fact must expose the member count of the required R2/R7/R27 root.

## Canonical sections

The summary is exact-compared section by section:

1. `frontier`
2. `d03_risk_sets`
3. `role_execution`
4. `role_risk_set_topology`
5. `P0`
6. `P1`
7. `P2`
8. `P3`
9. `P4`
10. `final_envelope`

Every section also receives expected/observed semantic identities in the parity receipt.

## P0 normalization

For each of five P0 candidates:

- require one role named `BASE`;
- resolve exactly one role fact;
- require R2 membership count;
- normalize ASTRA/current target cell integer vs exact-decimal representation;
- read the support from that exact located cell;
- conserve denominator, support, candidate hash, and terminal.

## P1 normalization

Require exact roles:

- `JOINT` → R27
- `MARGINAL_0` → R2
- `MARGINAL_1` → R7

The current side independently scans the located joint cells and returns the first exact cell for which:

`joint_count / joint_denominator != marginal_0_fraction × marginal_1_fraction`.

The witness carries all six counts/denominators plus cell location and candidate identity.

## P2 normalization

Each of 18 exact candidate hashes must have roles:

- `CONDITION` → R7
- `BASELINE` → R7

The current side independently scans the complete target-cell domain and returns the first exact cell satisfying the cross-multiplication inequality between conditioned and baseline distributions. The exact candidate-hash → witness mapping is compared, so candidate/witness permutations fail.

## P3 normalization

Require the exact eight-role grid under R7.

A current P3 valid-empty is accepted only if:

- receipt coverage is `EVALUATED_VALID_EMPTY`;
- receipt typed state is `VALID_EMPTY`;
- validator is `CONDITIONAL_REVERSAL`;
- every one of the eight role facts is `SUPPORTED`;
- every role denominator is positive;
- exact target-cell rates reproduce the accepted pooled and stratum signs;
- the computed reversal predicate is false.

Thus zero support, unavailable, unresolved, noncomparable, or any other empty mechanism cannot normalize to the accepted P3 truth.

## P4 normalization

Each of 25 P4 candidates must have one `BASE` role under R27.

The normalized truth key is the exact ordered target cell, not the candidate's position in a list and not the multiset of supports. This makes cell permutations fail.

## Hash-domain boundary

Historical ASTRA:

- whole execution product SHA;
- semantic replay hash.

Current PRE553:

- current execution receipt identity;
- current I05 replay identity;
- current canonical empirical summary identity.

Only the final empirical summary identities are required to match across domains. Historical/current whole-object hashes are never directly equated.

## Fail-closed law

Any malformed shape, missing role/fact, wrong root cardinality, wrong candidate identity, wrong cell, wrong fraction, wrong sign, wrong empty mechanism, wrong role count, or section mismatch raises `LitsAstraSubstantiveParityError`.

No tolerance, fuzzy matching, semantic inference from raw values, or fallback exists.
