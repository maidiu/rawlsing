# R03C — HOSTILE COUNTEREXAMPLES / FIXTURES

**Status:** non-dispositive adversarial fixtures for R03 synthesis and later stage close-reads  
**Base:** `138ded52ae6c7d26e9a3671e39d779965b5dc6f4`  
**Production execution:** none

These fixtures attack only provenance, replay, source-universe separation and standalone closure. They do not grant runtime semantic authority to provenance or replay receipts.

## FX-C01 — no copied query/measure/admission payload on V555/V556

### Given

A corrected structural root has this semantic ancestry:

```text
V556 interaction/topology
-> V555 route
-> V554 affordance
-> StructuralEmpiricalAdmission
-> EmpiricalFact
-> EmpiricalQuerySpec
-> EmpiricalUniverse
-> routing/risk-set authority
-> WeightMeasureFact / design authority
-> historical AuthoritySnapshot(s)
-> exact C11 content/replay identity
```

No V553 node is present because this fixture uses a temporally complete direct-V554 admission class.

### Hostile mutation

Remove every copied `EmpiricalQuerySpec`, universe label, denominator, weight field and admission payload from V555 and V556. Retain only the exact producer references required by their own semantics.

### Passing construction

The V556 root closure deterministically walks exact, role-declared references through V555 and V554 to the admission and its empirical provenance. Every required node has:

- authoritative object ID;
- producer/build/schema identity where applicable;
- content hash;
- reference-contract ID/version/hash and role;
- immutable packaged content or an exact packaged hash-bound resolution contract.

The exact query AST, universe identity, risk set, measure/design authority and historical authority are recoverable without interpreting prose or querying a mutable `latest` catalog.

### Failing construction

The admission contains `query_id = q17`, but `q17` is not physically in the closure and its only locator is `queries/current/q17.json` without an immutable content hash/resolution contract.

**Expected result:**

`MISSING_REQUIRED_TRANSITIVE_DEPENDENCY` or mutable-identity failure. Do not reconstruct from the admission description.

### Attack conclusion

R02's no-copy minimality survives. A chain of unresolved identifiers does not qualify as transitive semantic closure.

---

## FX-C02 — standalone V558, producer stage directories physically absent

### Given

A V558 repository bundle claims to publish one V556 root with its complete mixed-producer ancestry.

### Hostile environment

Before resolution:

```text
raw V553 directory = ABSENT
raw V554 directory = ABSENT
raw V555 directory = ABSENT
raw V556 directory = ABSENT
```

The resolver may access only the immutable V558 repository bundle and external locators explicitly packaged under an immutable hash-bound resolution contract.

### Passing construction

The repository contains or exactly immutable-addresses:

- source V557 publication bundle/manifest identity and hashes;
- collection registry;
- producer-preserving object locators;
- role-preserving transitive reference graph;
- producer material store and manifest;
- closure digests;
- required indexes;
- negative/fidelity state;
- exact governance/policy bindings;
- every interpretation-critical producer object/authority dependency.

V3-facing structural resolution succeeds without asking where `V555/latest` lives.

### Failing construction A — raw-stage repair

A locator resolves via:

```text
../V555/latest/routes.json
```

**Expected result:** `V558_REPAIR_ATTEMPT` / mutable-latest failure.

### Failing construction B — hash-only orphan

The closure records `sha256:abc...` for an admission authority but packages neither the authority bytes nor any immutable resolver contract capable of retrieving those exact bytes.

**Expected result:** `MISSING_REQUIRED_TRANSITIVE_DEPENDENCY`.

### Attack conclusion

Standalone closure is a physical/integrity obligation even when semantic payload copying is minimized. The accepted architecture requires this; current superseded V557/V558 code is not proof that the fixture passes.

---

## FX-C03 — conflicting source universes with overlapping labels

### Given

```text
Universe U_A:
  respondent display id = "0007"
  question display label = "TRUST"
  governed result = distribution A

Universe U_B:
  respondent display id = "0007"
  question display label = "TRUST"
  governed result = distribution B

A != B
```

No source-pooling authority is supplied.

### Hostile mutation

A convenience index groups both by normalized source/question labels and emits one averaged result.

### Expected result

Reject the merge.

The following propositions remain distinct:

```text
same display label
!= same EmpiricalUniverse
!= semantic equivalence
!= respondent identity linkage
!= sample pooling authority
```

The exact U_A and U_B identities remain separate. A lawful structural admission may preserve plural source-specific evidence or a governed conflict/noncomparability state, depending on its authority. It may not invent an average.

### Attack conclusion

Source-universe separation survives only if exact universe identity is itself part of the immutable provenance closure and indexes remain nonsemantic lookup aids.

---

## FX-C04 — replay under superseded historical authority

### Given

At time T1:

```text
StructuralAdmissionAuthority = A@1
content hash = H1
rule permits admission X under exact conditions C1
```

A durable admission receipt X is produced and binds `A@1/H1`.

At time T2:

```text
current StructuralAdmissionAuthority = A@2
content hash = H2
rule changes C1 and would deny the same new request
```

### Hostile replay

Replay X by resolving logical name `A` through `current` and applying A@2.

### Expected result

Reject. Historical X must dereference `A@1/H1`.

If A@1/H1 cannot be exactly located:

`FAIL_CLOSED__HISTORICAL_AUTHORITY_UNAVAILABLE`

The missing historical authority is preserved as the exact unknown. A@2 cannot reinterpret X.

### Attack conclusion

An authority name/version string is not sufficient by itself. Exact historical content or an immutable hash-bound resolver contract is required.

---

## FX-C05 — exact risk-set and measure recovery after convenience-copy stripping

### Given

An `EmpiricalFact` is computed from:

- Universe U;
- exact predicate P;
- target Q;
- routing/risk-set R;
- exact respondent member set `M_R` or deterministic member-set rule with all parent predicates;
- authorized weighted estimand W under design authority D;
- raw denominator/support N;
- typed missing/routed states;
- uncertainty state/method where governed.

A structural admission uses that fact. Later V555/V556 objects copy none of the above fields.

### Hostile variants

#### Variant A — same denominator, different members

Construct risk set R2 with:

```text
|M_R2| = |M_R|
M_R2 != M_R
```

A replay system compares only denominator N and treats R2 as equivalent.

**Expected result:** reject. Equal denominator does not prove equal risk set.

#### Variant B — same displayed percentage, different weight design

Use the same displayed weighted percentage under a different weight basis/design authority.

**Expected result:** reject. Measure/estimand identity and design authority are semantic provenance.

#### Variant C — missing routing parent rule

The risk-set identifier resolves, but one deterministic routing parent predicate is unavailable.

**Expected result:** `REPLAY_INPUT_MISSING`; do not infer membership from the old denominator.

### Attack conclusion

Weight and risk-set fields need not be repeated downstream, but their exact authoritative definitions and replay material must remain recoverable transitively.

---

## FX-C06 — cross-universe respondent join without linkage authority

### Given

```text
U_A respondent namespace: "0007"
U_B respondent namespace: "0007"
```

No positive respondent-identity linkage relation is present between U_A and U_B.

### Hostile mutation

Join those rows because their display identifiers match, then treat the joined record as one respondent for a same-person conjunction or double-count correction.

### Expected result

`LINKAGE_NOT_AUTHORIZED`

No join occurs.

Source semantic equivalence, respondent identity linkage, sample pooling authority and generated-actor comparability remain separate authority families. None can substitute for another.

### Attack conclusion

Universe-scoped respondent identity is mandatory replay information. Same-label joins are forbidden by default.

---

## FX-C07 — ReplayReceipt as a runtime semantic prior

### Given

Two structural roots are identical in producer semantics, producer permission and exact domain evidence. Their historical replay receipts differ only in administrative replay metadata:

```text
root R1 -> ReplayReceipt old algorithm/version
root R2 -> ReplayReceipt newer algorithm/version
```

Both receipts verify their respective historical productions exactly.

### Hostile mutations

Attempt any of the following:

1. prefer R2 in V558 because its replay algorithm is newer;
2. assign R2 a higher structural weight because its receipt is `VERIFIED`;
3. use receipt recency as a V3 developmental probability;
4. use receipt presence as source-composition weight;
5. let a receipt widen a producer/V557 denial.

### Expected result

All five are rejected.

A receipt may:

- identify a historical replay;
- verify exact input/authority/algorithm bindings;
- expose integrity failure;
- support migration/equivalence audit.

It may not create positive structural or actor meaning.

An integrity gate that blocks use of a corrupt/unverifiable object remains an integrity gate; it does not turn the receipt into a prior.

### Attack conclusion

R02-H09 survives attack unchanged.

---

## Cross-fixture closure test

The combined hostile acceptance condition is:

```text
NO_REDUNDANT_FIELD_COPYING
AND ROLE_PRESERVING_REFERENCE_CONTRACTS
AND EXACT PRODUCER ID/VERSION/HASH
AND PACKAGED MATERIAL OR IMMUTABLE HASH-BOUND RESOLUTION
AND EXACT HISTORICAL AUTHORITY
AND EXACT SOURCE-UNIVERSE / LINKAGE / POOLING STATE
AND EXACT RISK-SET / ROUTING / MEASURE RECOVERY
AND FAIL-CLOSED BROKEN REFERENCES
AND NO RAW-STAGE OR MUTABLE-LATEST REPAIR
AND REPLAY RECEIPT REMAINS NONSEMANTIC
```

Anything weaker is insufficient to prove the R02 reference-closure theorem for standalone corrected V558 publication.
