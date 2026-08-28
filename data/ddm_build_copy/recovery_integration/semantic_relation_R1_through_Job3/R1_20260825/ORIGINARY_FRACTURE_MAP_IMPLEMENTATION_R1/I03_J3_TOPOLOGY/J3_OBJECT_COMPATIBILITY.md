# J3 Object Compatibility — Authority 37 / I03 R1

## Decision

No new public empirical object family is required for the authorized J=3 extension.

The exact extension reuses:

- `EmpiricalQuerySpec@1.0.0`;
- `EmpiricalFact@1.0.0`;
- existing exact AuthoritySnapshot, predicate, universe, routing, response-topology and replay refs.

This preserves D04's reuse-before-invention holding.

## Query compatibility

Historical exact query authorities that do not carry a target-arity field retain the accepted legacy ceiling:

`LEGACY_MAXIMUM_TARGET_ARITY_J = 2`

J=3 requires an exact query authority whose versioned/content-addressed `scope_envelope` explicitly contains:

`maximum_target_arity_J: 3`

(or another positive value at least 3; the implementation itself is still capped at 3).

Multiple exact query authorities compose by the strictest declared target-arity ceiling.

For a J=3 query the executor additionally requires:

1. exactly three exact target refs;
2. no duplicate target refs;
3. `CANONICAL_SET_ORDER`;
4. the supplied triple is already canonical exact-ref sorted;
5. exactly three target components corresponding positionally to those refs.

Malformed or unauthorized triples fail closed rather than being silently reordered during execution. Producers/controllers must canonicalize before minting the query identity.

## Fact compatibility

J<=2 `EmpiricalFact@1.0.0` serialization is intentionally unchanged.

Only J=3 facts extend `target_topology` with:

- canonical target refs;
- implementation maximum J=3;
- exact denominator conservation material;
- direct higher-order evidence marker;
- pairwise-non-equivalence marker;
- exact same-respondent member refs on each complete J=3 cell.

The denominator block is:

`AUTHORITY37_J3_DENOMINATOR_CONSERVATION@1.0.0`

and contains distinct source/risk, branch, three per-target, and three-way-joint membership/count surfaces.

## Response topology / multiplicity / typed states

No new response-value coercion was introduced.

The J=3 executor invokes the same existing component resolver used by J<=2. Therefore each target continues to obey its exact:

- source-native topology authority;
- target-domain replay ref;
- response-semantic authority refs;
- included typed response states;
- ordered/ranked/repeated/multiselect/componentized representation;
- multiplicity/order metadata where that topology requires it.

The executed hostile regression suite includes ordered, ranked, repeated-event and typed-special-state fixtures.

## Raw versus weighted

Raw and governed-weighted measures remain separate semantic facts because the existing measure basis and execution profile remain identity-bearing.

For J=3, both the top-level fact support and the new denominator block preserve this separation. Weighted material uses exact rational support; it is not substituted for raw respondent counts.

## Replay compatibility

The query execution contract ID remains:

`PRE553_I03_EXACT_EMPIRICAL_QUERY@1.0.0`

Changing it globally would perturb lawful J<=2 replay/fact identities. Instead, J=3 identity is distinguished by the exact J=3 query authority, triple topology, denominator material, exact member refs and direct three-way cells.

J=3 replay material now pins:

- exact query/predicate/releases;
- exact target-domain identity;
- exact source/risk and branch membership;
- exact per-target membership;
- exact three-way joint membership;
- exact same-respondent cell membership/counts;
- raw/weighted measure material.

## I05 compatibility

`pre553_discovery_exact.py` was not extended with controller enumeration.

It now rejects any DiscoveryAuthority or candidate grammar claiming `maximum_target_arity_J > 3`. Existing J<=2 grammars remain valid. J=3 templates are accepted only when the underlying exact I03 query authority also authorizes J=3.

The historical J=4 success test was removed because Authority 37 explicitly defines J=3 as the present ceiling.

## Not implemented here

I03 does not implement:

- deterministic target-triple enumeration from fracture families;
- recursive generation traversal;
- branch-handoff consumption policy for a future controller;
- `EmpiricalFractureMapReceipt@1.0.0`;
- discovered N -> sealed N+1 frontier composition.

Those remain controller work outside this worker.
