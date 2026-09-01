# FFIF006 — FFX002 R2 EXECUTION IMPLICATIONS

## Holding

FFX002 R2 needs, in addition to the byte-identical `COMMON_SEMANTIC_INPUT_MANIFEST`, a separate frozen CIM and CITC for every atomic query battery entry. A query ID, `CANARY_LOCAL`, and prose `loss_tolerance` cell are not enough.

## Required freeze before Phase 3

During Phase B / before independent view production, execution must freeze:

1. atomic `CLAIM_IDENTITY_MANIFEST` objects;
2. `CLAIM_INVARIANT_TOLERANCE_CONTRACT` objects;
3. support/uncertainty contracts;
4. bundle-requirement contracts only where co-requirement is independently justified;
5. a query-manifest row binding all hashes;
6. a freeze receipt proving these predate comparative outputs and final-holdout inspection.

Suggested execution carriers:

- `05_QUERY_MANIFEST.tsv` — add CIM/CITC/support/bundle refs and hashes;
- `05A_CLAIM_IDENTITY_MANIFESTS.jsonl`;
- `05B_CLAIM_INVARIANT_TOLERANCE_CONTRACTS.jsonl`;
- `05C_CLAIM_BUNDLE_REQUIREMENT_CONTRACTS.jsonl`, only if used;
- `05D_CLAIM_CONTRACT_FREEZE_RECEIPT.md`.

## Current query-battery disposition

The existing Q01–Q11 rows are valuable design prompts, not execution-ready claim identities. `CANARY_LOCAL` is not a sufficient scope; each row still needs exact operands, risk set, population/context, estimand, quantifier, conditioning, baseline, scale, TTAR/PRA bindings, and assertion slots.

Broad rows must split where needed. For example:

- Q01 exact configuration existence/support and Q01 conditional-distribution fidelity are separate atomic claims unless bundled;
- Q02 minority existence and minority mass estimation are separate;
- Q08 compression is a utility/fidelity claim, not general representational truth;
- Q09 is necessarily representation-indexed and must name its exact view-specific invariant;
- Q11 remains outside the first canary and requires transport-specific claim authority.

## Threshold disposition

Existing numeric guidance—including TV `0.02`, recall `0.90/0.95`, `10%` log-loss gain, `4x` compression, and geometry stability cutoffs—must not be treated as universal empirical materiality authority.

- exact `1.0` preservation may be derived where the claim is explicitly exact;
- TV/recall/mass margins require claim/source/error-model authority;
- log-loss gain is predictive/downstream utility unless the claim is target-specific predictive adequacy;
- `4x` compression is engineering utility after fidelity;
- geometry stability thresholds govern view admissibility/sensitivity, not truth of unrelated claims;
- conventional confidence/permutation thresholds require an explicit inferential contract.

FFIF006 does not set replacement values.

## Phase and output changes

Phase C may begin only after all mandatory arms attest to:

- common semantic input hash;
- proposition hash per query;
- comparison claim hash per query;
- CITC hash per query;
- support/uncertainty contract hash per query.

`VIEW_DISAGREEMENT` and future CVCR payloads must replace `material_difference_metric` alone with componentwise:

- loss dimension;
- observed value/state;
- CITC row ref;
- uncertainty state;
- materiality state;
- critical-invariant veto;
- utility-only metrics separately typed.

## Execution blockers

If a claim or tolerance lacks authority, do not improvise. Return:

- `CLAIM_UNDERSPECIFIED`, or
- `TOLERANCE_AUTHORITY_UNRESOLVED`.

The whole canary need not fail if other preregistered atomic claims are complete, but no incomplete claim may contribute to representation dependence, weaker-object sufficiency, multi-view necessity, or bounded nonreducibility.

## Exact FFX002 implication

**FFX002 R2 is design-ready only after its query prose and provisional numeric guidance are converted into immutable, authority-backed CIM/CITC pairs before Phase 3; otherwise it may produce raw view evidence but cannot lawfully adjudicate material disagreement, sufficiency, or bounded nonreducibility.**

