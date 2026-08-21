# R2-04 OPEN-WORLD ORACLE PLAN

Status: `DESIGN_ONLY__REPRESENTATION_NEUTRAL__NO_RUNTIME_MUTATION`

## 1. Court target

Test whether any later P0 implementation preserves frozen I03/I05/I04 behavior when every nonauthoritative accelerator is absent, stale, corrupt, or simply ignorant of the workload.

The oracle does not compare physical bytes to R4. Expected truth comes from frozen semantic contracts plus R03's independent respondent-incidence evaluator.

## 2. Freeze order

Before selecting the blind workload, freeze:

1. candidate commit/build identity;
2. physical profile and compiler configuration;
3. exact source/release fixture identities;
4. exact authority snapshot set;
5. exact hashes of all I03/I05 workloads used for physical/index tuning;
6. oracle version.

Then record a nonce and deterministically select a blind exact frontier excluding the disclosed tuning hashes.

## 3. Mandatory execution modes

For the identical logical fixture and query/discovery bundle:

- `M0_NO_CACHE`: delete every nonauthoritative bitmap/index/branch/query cache;
- `M1_WARM_CACHE`: build all candidate-declared accelerators;
- `M2_CACHE_DELETED_AGAIN`: delete them after warm execution;
- `M3_STALE_CACHE`: substitute a cache from another exact release/authority dependency set;
- where implementation supports multiple organizations, run `LONG_SHARDED`, `QUESTION_BLOCKED_LONG`, and/or `HYBRID_DENSE_PLUS_EXPLICIT` shadow variants independently.

M0 is the capability gate. M1 may prove speed only. M2 must reproduce M0. M3 must reject/rebuild before semantic output.

## 4. I03 membership oracle

For each exact universe, independently enumerate scoped respondents and evaluate the frozen predicate AST per respondent from canonical observations.

Compare candidate versus independent expected truth for:

- exact respondent membership, not counts only;
- risk-set membership;
- denominator membership;
- target event multiset/sequence;
- raw and weighted supports;
- typed positive/negative/failure state;
- full `EmpiricalFact` semantic projection/ref.

Mandatory predicates:

1. single uncached response value;
2. uncached exact high-cardinality/string value;
3. valid empty string;
4. 3+ leaf AND;
5. OR containing cached + uncached leaves;
6. NOT with out-of-risk physical rows present;
7. nested `NOT(OR(AND(...), ...))`;
8. typed-response-state leaf;
9. routing/applicability leaf;
10. coordinate leaf with exact time;
11. derived branch cohort after branch-cache deletion.

Mandatory target/risk/measure cases:

- scalar;
- componentized;
- multiselect/MR;
- repeated;
- ordered/ranked;
- routed response;
- pair joint;
- k >= 3 joint;
- exact weight positive;
- missing/invalid/unauthorized weight;
- unresolved routing;
- absent routing fact;
- explicit inapplicable;
- zero support;
- observed zero;
- valid empty;
- noncomparable/source-relation failure;
- source-indexed multi-universe;
- authorized composite positive and negative.

## 5. I05 blind-frontier oracle

After freeze, include at minimum where authority permits:

- `PAIR_RESPONSE_COTRAVEL`;
- `BOUNDED_K_WAY_RESPONSE_CONFIGURATION` with k >= 3;
- `CONDITIONAL_REVERSAL_OR_SIMPSON`;
- `RECURSIVE_SUBGROUP_FORK`;
- `BRANCH_CONDITIONED_DISTRIBUTION`;
- `BRANCH_CONDITIONED_COTRAVEL`;
- uncached string/high-cardinality conditioners;
- nested AND/OR/NOT condition;
- cross-block target/condition placement;
- source-indexed multi-universe query template;
- joint/co-signature facts used for a cloud-like diagnostic.

Before evaluation, compare candidate frontier identity against the frozen/independent compiler:

- candidate count;
- exact candidate IDs/hashes;
- exact canonical order;
- query-role refs.

After evaluation compare:

- covered candidate count;
- terminal coverage state for every candidate;
- all exact fact refs;
- all `DiscoveryResultReceipt` projections/replay refs;
- valid-empty/noncomparability/authority-limited distinctions.

Any candidate missing because no index exists is a hard failure.

## 6. Diagnostic ablation

Run the same frontier with diagnostic ranking/scoring disabled or deliberately permuted.

Required invariant:

- candidate IDs/count/order unchanged;
- empirical fact refs unchanged;
- discovery coverage unchanged;
- I04 inputs/outputs unchanged.

Diagnostic report/ranking bytes themselves need not be equal.

## 7. I04 oracle

For exact query/fact pairs from the I03/I05 court, run the frozen admission service and an independent precedence check.

Inject individually and in combinations:

- integrity failure;
- missing admission authority;
- conflicting required authority;
- denial;
- negative-authority-only;
- source not applicable;
- empirical fact noncomparable;
- temporal mismatch;
- structural target unresolved;
- insufficient evidence;
- deferred;
- valid empty;
- positive admitted.

Compare exact decision state, public typed state, reason/blocking refs, receipt identity and positive-projection permission. Only `ADMITTED` can produce positive direct structural projection.

## 8. Negative-completeness fault injection

Construct a canonical fixture where the only refuting/matching respondent lies in a physical block that an optional accelerator falsely marks absent.

Required behavior:

- M0 scan finds the respondent;
- stale/false-negative accelerator is ignored/discarded or used only as nonexcluding hint;
- candidate never returns zero/empty based solely on the accelerator;
- if a canonical completeness structure is used to prune the block, mutate that structure and require integrity failure before semantic output.

## 9. Profile metamorphs

Repack identical logical material by varying:

- question-block width;
- row-group/partition boundaries;
- physical insertion order;
- cache policy;
- dense versus explicit-event physical profile where both are lawful.

Exact respondent membership, semantic projections, refs, discovery coverage and admission must remain unchanged.

## 10. Acceptance rule

`PASS` only if M0 no-cache execution matches frozen + independent truth for every applicable case and all cache/profile metamorphs preserve semantics.

One reproducible mismatch is hard failure. Performance is considered only after semantic pass.
