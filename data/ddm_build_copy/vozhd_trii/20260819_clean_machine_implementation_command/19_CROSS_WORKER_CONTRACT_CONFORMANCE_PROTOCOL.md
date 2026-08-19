# 19 — CROSS-WORKER CONTRACT CONFORMANCE PROTOCOL

## 1. Governing principle

Producer and consumer implementations are not mutually compatible merely because each passes its own unit tests.

Every shared interface must be proven from both sides against one frozen machine-readable contract.

## 2. Contract conformance triad

For each canonical interface G4/G5 maintain three independent test classes:

1. **producer conformance** — producer emits only lawful states/fields/identities;
2. **consumer conformance** — consumer accepts every lawful state it owns and rejects every forbidden/unknown input correctly;
3. **seam conformance** — actual producer output is consumed without translation drift, hidden defaults, information loss, re-ID, permission widening or semantic reownership.

A green producer suite plus green consumer suite does not waive seam conformance.

## 3. Canonical contract vectors

Every interface should have finite contract vectors covering where applicable:

- ordinary positive case;
- valid-empty;
- zero / observed-zero;
- unsupported / not-applicable;
- missing authority;
- unknown;
- denied;
- low support / uncertainty;
- noncomparability;
- conflicting source components;
- stale/effective-time mismatch;
- malformed/integrity failure;
- hash mismatch;
- historical-version replay;
- n-ary role/order/cardinality cases;
- direct versus transitive reference cases.

No worker may silently omit a canonical negative vector because current happy-path code does not produce it yet.

## 4. Independent producer/consumer construction

Where practical, producer and consumer rabochii implement independently from the same frozen contract rather than copying each other's internal types.

This makes interface mismatches observable instead of inherited.

Shared generated schema/types are lawful only when G3/G4 explicitly own them as canonical contract artifacts.

## 5. Semantic checksum

Every interface receipt records a semantic checksum over:

- contract ID/version/hash;
- object family/grain;
- identity tuple;
- state vocabulary;
- cardinality/order/role law;
- time semantics;
- authority bindings;
- reference roles;
- forbidden inputs/edges;
- fixture vector IDs.

Two sides with different semantic checksums are incompatible even if serialization happens to parse.

## 6. Round-trip and no-loss tests

Where an interface is serialized/materialized, tests must prove:

`producer semantic object -> serialized form -> consumer interpretation`

preserves all interpretation-critical meaning.

For content-addressed/reference-heavy paths also test:

- raw producer directories absent where standalone law requires;
- exact immutable dereference;
- broken required reference fails closed;
- role/order/cardinality survives reference traversal;
- provenance remains nonsemantic where governed as such.

## 7. Database seam tests

Any interface crossing the physical substrate must additionally prove:

- exact key mapping;
- no accidental many-to-many expansion;
- no source-universe cross join;
- denominator/risk-set preservation;
- weight/measure basis preservation;
- typed absence preservation;
- deterministic ordering only where semantics require ordering;
- transaction/idempotency behavior under retry.

## 8. Cross-domain seam receipt

Before Integration Command admits a producer/consumer pair, the responsible Vozhds jointly sign a `CROSS_DOMAIN_SEAM_RECEIPT` containing:

- producer branch/head;
- consumer branch/head;
- frozen contract hash;
- substrate contract hash;
- semantic checksums from both sides;
- contract vector results;
- canonical hostile-fixture results;
- Inspectorate disposition;
- unresolved implementation debt;
- exact statement that neither side changed shared semantics locally.

## 9. Differential legacy tests

Legacy behavior may be used as an oracle only for behaviors explicitly classified `PRESERVE_PARITY` or equivalent under salvage authority.

A legacy mismatch is not automatically a defect when accepted authority supersedes legacy behavior.

Every differential test therefore states whether it is:

- parity-required;
- migration-only;
- diagnostic;
- expected-divergence under new authority.

## 10. Release condition

No shared interface is considered implementation-closed until producer, consumer and seam conformance all pass the same contract epoch/hash and the Inspectorate has no unresolved stop disposition.
