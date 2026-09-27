# M1 IMPLEMENTATION CONTRACT R1

This is the post-adoption implementation contract. It does not authorize implementation by this worker.

## 1. Smallest API

A future implementation SHOULD expose one generic entry point equivalent to:

`adjudicate_learned_empirical(input_bundle, family_rule_binding) -> LearnedEmpiricalDisposition`

No generic `validate(data)` API with implicit rule choice is lawful.

## 2. Input verification phase

Before family validation:
1. verify public object family/schema versions;
2. recompute exact semantic object identities;
3. verify exact refs/preimages;
4. verify authority snapshot closure;
5. verify DiscoveryResultReceipt -> DiscoveryAuthority/frontier/fact/query/predicate closure;
6. verify replay identities needed by the selected family;
7. verify exact state vocabulary and no impossible state combinations;
8. verify family-rule binding identity and authority;
9. verify explicit selection purpose/current-selection premise;
10. verify family/scope applicability;
11. verify all rule-declared prerequisite channels.

Failure before rule execution produces typed blocked/unresolved/integrity output; it never falls back.

## 3. Dispatch phase

The dispatcher indexes validators only by exact immutable validator identity, not by convenience alias.

Required lookup key is equivalent to:

`(claim_family_id, claim_rule_id, validator_authority_id, validator_authority_version, validator_authority_content_hash)`

A registry may accelerate lookup but may not infer currentness.

Exact current rule choice must already be governed in the binding.

## 4. Family validator interface

Each validator SHALL declare:
- accepted claim family/rule;
- exact authority identity;
- accepted input object families/states;
- constitutive proposition fields;
- required premise channels;
- source/universe/risk/topology/measure requirements;
- uncertainty/support semantics;
- coverage requirement;
- comparability/composition/measurement requirements;
- exact decision vocabulary;
- whether a truth-bearing semantic claim can be emitted;
- P1 claim-identity constructor if applicable;
- semantic ceiling;
- deterministic parameters/algorithm identity;
- determinant/explanation contract.

The validator returns a typed `FamilyValidationResult`; the generic M1 layer only wraps and verifies it.

## 5. No universal substantive defaults

The implementation SHALL NOT provide default:
- minimum N;
- p-value/significance threshold;
- effect-size threshold;
- association metric;
- distance/similarity threshold;
- missingness treatment;
- comparability assumption;
- pooling rule;
- weighting rule;
- estimator;
- causal interpretation;
- structural interpretation;
- semantic polarity.

Any such criterion belongs to an exact family rule authority.

## 6. Mandatory generic invariants

The generic implementation may enforce only constitutional invariants:
- exact identity and replay closure;
- explicit rule binding;
- exact rule-family match;
- exact applicability;
- exact required-authority presence;
- no semantic-ceiling widening;
- negative-state conservation;
- deterministic output projection;
- no M2/M3/I04 side effects.

## 7. Output construction

The wrapper SHALL preserve:
- the family validator's exact outcome;
- all conserved upstream evidence states;
- all blocking/negative refs;
- exact claim/proposition identity output, if any;
- exact validator and rule-selection authority;
- exact determinant manifest;
- exact semantic ceiling;
- replay/explanation refs.

The output identity is deterministic over the full adjudication projection.

## 8. Explanation contract

Every output must explain itself through structured determinants sufficient to answer:
- what exact claim/proposition was considered;
- which exact rule and authority governed;
- why that rule applied to this scope;
- which exact facts and query/predicate semantics were used;
- which support/uncertainty/coverage states mattered;
- which premise authorities were required and resolved;
- what exact reason produced the result;
- what the result does **not** authorize.

Narrative prose may be rendered from that structure but cannot be the authoritative determinant.

## 9. Replay contract

Replay from the same exact:
- input refs/preimages;
- rule binding;
- authority closure;
- validator identity/parameters;
- prerequisite states

must reproduce the same disposition object identity.

If replay differs:
`INTEGRITY_FAILURE`.

No automatic repair or newer-rule substitution is allowed during replay.

## 10. Side-effect firewall

M1 implementation SHALL have no authority to:
- publish a learned product;
- choose a current product;
- supersede/withdraw releases;
- create structural admission;
- grant Field Forge target use;
- create actor facts;
- mutate source authority.

These are downstream owners.

## 11. Adoption/implementation sequencing

1. HQ adopts this constitution or a corrected successor.
2. Implementation worker adds the smallest public/internal types required.
3. Source-free hostile tests prove invariants.
4. Family validators are registered only under explicit adopted bindings.
5. No live-source proving is needed to validate M1's generic jurisdiction mechanics.
6. Live empirical family adjudication occurs only when exact family rule and source prerequisites are separately authorized.
