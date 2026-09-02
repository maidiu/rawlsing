# FFIF013 — NORMALIZED DISCOVERY-TO-FOLLOWUP ASSERTION BUNDLE R1

Status: `DESIGN_ONLY__REPRESENTATION_NEUTRAL__NO_TARGET_VALUES`

## Governing proposition form

Let:

- `S` = one frozen lawful discovery surface;
- `R_S` = its exact empirical-unit/risk-set law;
- `D` = one deterministic outcome-blind exact discovery procedure;
- `P = {p_1..p_k}` = the admitted exact predicate/profile/conjunction roster produced by `D` under a frozen roster rule;
- `X` = one external respondent/context operand outside `S`, or `F_X` = one finite preregistered family;
- `Q` = one exact follow-up query relation over `P × X` under a frozen empirical-unit/risk-set law.

The court asks whether challenger `W_j` can emit the same complete normalized assertion bundle and replay it lawfully.

## AS01 — exact discovery-surface identity

Freeze:

- discovery-surface ID/version;
- source/wave/context scope;
- empirical-unit identity;
- exact risk-set/coexposure definition;
- exact source-native operand identities;
- special/non-substantive native-state law;
- producer refs and immutable ancestry hashes;
- any constitutive routing/exposure refs;
- any constitutive TTAR/PRA refs already authorized upstream.

A changed risk set, unit, native-state equivalence, or semantic-input ancestry is a different comparison, not a representation result.

## AS02 — exact discovery-predicate identity

Freeze either:

1. every admitted predicate definition individually; or
2. a deterministic predicate-roster generator whose input surface and generation law are immutable, plus the resulting immutable roster hash before target follow-up inspection.

Every predicate identity must be reducible to exact source-native/authorized state conditions. Display names, clusters, motifs, geometry, and theory labels are nonconstitutive unless separately authorized and explicitly part of the claim, which this design forbids.

If execution cost requires a subset of an already discovered roster, the subset rule must be outcome-blind to `X`: use the complete bounded roster where feasible; otherwise use an ex ante deterministic ID/hash rule. Do not select by predicate × `X` relation, direction, rarity, surprise, predictive value, or downstream appeal.

## AS03 — exact original discovery support

For every admitted `p_i`, emit:

- exact support count/status on the frozen original discovery risk set;
- exact denominator/risk-set reference;
- exact special-state inclusion law;
- exact discovery receipt ancestry.

Support `1` remains an exact finite-sample existence fact. No minimum support, pooling, or stability threshold is introduced here.

## AS04 — exact external follow-up operand/context identity

Freeze:

- `X` ID/version and source-native identity;
- domain/state identity;
- source/wave/context scope;
- empirical-unit relation to `S`;
- routing/exposure/currentness authority where needed;
- proof that `X` was outside the discovery surface;
- outcome-firewall receipt proving `X` values/relations did not influence discovery-predicate selection.

`OUTSIDE_DISCOVERY_SURFACE` means `X` was not an operand of `D` and did not select/rank the discovered predicates. It does not mean `X` must come from another source if a same-source governed context fact is the clean lawful candidate.

## AS05 — exact follow-up query relation

The central successor must instantiate one normalized query relation before target output. The generic exact form is:

`Q(p, X, R_Q) -> exact relation/support/status`

The frozen query spec must bind:

- predicate roster ref;
- external operand ref;
- empirical-unit identity;
- follow-up risk set/eligibility/coexposure rule;
- conditioning/baseline relation if constitutive;
- estimand/weight target if applicable;
- exact output value/status domain;
- denominator and zero-denominator law;
- native-state/special-state treatment;
- source/replay dependencies.

A useful implementation may be an exact joint/conditional support table, but FFIF013 does not select a particular `X` or query schema.

## AS06 — exact follow-up support/result or typed abstention

For every frozen assertion key, the challenger emits exactly one normalized state from a predeclared domain such as:

- `EXACT_VALUE(value)`;
- `EXACT_SUPPORT(n)`;
- `VALID_EMPTY`;
- `ABSTAIN__ZERO_DENOMINATOR`;
- `UNSUPPORTED_OR_NOT_IDENTIFIED` where the query's inferential contract warrants that state;
- `OUT_OF_SCOPE`;
- `DENIED_OR_PROHIBITED`;
- `BLOCKED__AUTHORITY_OR_OBSERVABILITY`;
- `REPLAY_OR_INTEGRITY_FAILURE`;
- `UNDEFINED_FOR_OBJECT`.

A challenger that lacks the information/interface to answer a slot must emit `UNDEFINED_FOR_OBJECT`; it may not emit zero, false, missing, or an imputed scalar.

## AS07 — exact replay/source-native ancestry

Replay is stronger than answer persistence.

For each challenger, freeze the law by which an independent reviewer can regenerate the normalized answer from authoritative evidence available to that challenger:

- immutable producer/source refs;
- exact predicate/query specs;
- exact local materialization refs where constitutive;
- query-time producer dependencies;
- deterministic transform/query recipe;
- exact output normalization/status logic;
- dependency closure and permission refs.

`SAVED_ANSWER != REPLAY_CAPABILITY`.

A final-answer cache may be evidentiary capital, but it fails AS07 if no lawful deterministic regeneration path exists.

## AS08 — exact negative-state conservation

The court must distinguish at minimum:

`FALSE`

`!= OBSERVED_ZERO`

`!= VALID_EMPTY`

`!= ABSTAIN__ZERO_DENOMINATOR`

`!= UNSUPPORTED_OR_NOT_IDENTIFIED`

`!= OUT_OF_SCOPE`

`!= DENIED_OR_PROHIBITED`

`!= BLOCKED__AUTHORITY_OR_OBSERVABILITY`

`!= REPLAY_OR_INTEGRITY_FAILURE`

`!= UNDEFINED_FOR_OBJECT`.

No challenger earns sufficiency by coercing one state into another.

## Equality oracle

For exact slots, comparison is noncompensatory:

`ALL_CONSTITUTIVE_SLOTS_EXACT_AND_VALID -> CLAIM_RELATIVE_SUFFICIENCY`

Any constitutive exact mismatch, illegal state collapse, unresolved owed authority, invalid common input, or missing replay capability prevents a sufficiency PASS.

There is no averaging across slots and no engineering benefit can offset constitutive loss.
