# M2 — V554 -> V555 atomic route exact seam contract

**Authority:** dispositive M2 seam checksum  
**SCR554 accepted head:** `b5d745ac70c833324c8be0addf6c08ad72372263`  
**SCR555 independent head:** `49a9ce7cd830eb670cf1f9d381d4d33e56ddf682`  
**Result:** `M2_ACCEPTED__SCR555_EXACT_CONTRACT_CLOSED`  
**Production code:** unchanged / not authorized

## 1. Closure holding

M2 closes the only upstream identity seam left open by SCR555.

The binding is exact and asymmetric:

```text
SCR554 canonical F1_id
        |
        |  exact B1 proves same F1 + allowed_v555_structural_use + replay/reference closure
        v
EXACT_V554_F1_REF
        |
        v
V555 seven-field atomic route identity
```

`EXACT_V554_F1_REF` resolves to the canonical SCR554 `F1_id`. It does **not** resolve to an admission, V553 object, legacy seed, copied F2 condition, descriptive label, or current V554 implementation row.

B1 crosses the seam with the F1 because it proves exact upstream use permission and replay/reference closure. B1 is not an eighth V555 route semantic field.

## 2. The accepted upstream identity is not a positional tuple

SCR555's waiting handoff named an unresolved slot `canonical_f1_identity_tuple_order_and_equality_law`. Accepted SCR554 does not define F1 or B1 as positional tuples. It defines semantic IDs over canonical JSON named objects.

M2 therefore binds the upstream form **without translating it into a fabricated tuple**.

Accepted SCR554 canonicalization:

```text
Same canonical JSON rules as duplicate equivalence.
urn:rawlsing:<object-family>:sha256:<lowercase-hex-digest>
```

Canonical F1 identity, verbatim:

```text
urn:rawlsing:v554:f1:sha256:SHA256(canonical_json({contract_version, equivalence_key, canonical_basis_semantic_id, rule_id, rule_version, rule_hash, signature_id, target_use, authority_bundle_fingerprint}))
```

Canonical B1 identity, verbatim:

```text
urn:rawlsing:v554:b1:sha256:SHA256(canonical_json({contract_version, candidate_semantic_key, f1_id_or_null, sorted_f2_ids, allowed_v555_structural_use, decision_state, producer_reference_spine_fingerprint}))
```

That upstream named-object identity is final for M2. The **only** positional tuple here is the V555 route identity.

## 3. F1 route admission

The accepted SCR554 semantic nucleus is:

```text
F1 = BOUNDED_STRUCTURAL_AFFORDANCE
F1 positive state = ELIGIBLE
target_use = STRUCTURAL_MEDIATION_INPUT
```

One V555 route consumes exactly one canonical `ELIGIBLE` F1.

The associated B1 must bind that same F1 and satisfy the accepted SCR554 use law:

> `allowed_v555_structural_use = true` iff a positive F1 exists and no applicable nonpositive hard block owns the exact target use; runtime-deferred K01-K03 and K04 informational constraint do not by themselves make B1 false.

M2 therefore admits a positive V555 route candidate only when:

1. exact canonical F1 resolves;
2. F1 state is `ELIGIBLE`;
3. the exact target use is `STRUCTURAL_MEDIATION_INPUT`;
4. exact B1 resolves;
5. B1's `f1_id_or_null` equals that F1;
6. `allowed_v555_structural_use=true`;
7. B1 decision/reference spine/authority closure is intact;
8. the governed V555 route rule then independently matches.

B1 proves upstream permission and replay. It contributes **zero** route multiplicity and is not part of V555 route semantic identity.

## 4. Frozen V555 route identity survives unchanged

The exact route identity remains:

```text
1. EXACT_V554_F1_REF
2. route_rule_id@route_rule_version
3. route_shape_id@route_shape_version
4. channel_structural_role_id
5. EXACT_STRUCTURAL_CHANNEL_REF
6. receiving_constraint_kind
7. EXACT_TARGET_RECEIVING_POSITION_REF
```

M2 changes none of those seven fields. It resolves field 1 to the accepted canonical SCR554 `F1_id`.

Consequently, two routes with identical channel and receiver fields but different canonical F1 IDs remain different routes. No downstream-visible coincidence can erase the upstream semantic difference.

## 5. Duplicate direct/V553 provenance cannot multiply routes

Accepted SCR554 deliberately excludes `basis_kind` from duplicate equivalence. A direct admission basis and a V553 no-op restatement can therefore be recognized as one semantic support for the exact invocation.

The accepted selection law emits at most one canonical `ELIGIBLE` F1 per equivalence group. Same-kind aliases likewise count once and survive only as provenance aliases.

M2 sees **post-dedup canonical F1 identity**. It never re-runs dedup from labels, paths, V553 presence, or legacy identifiers.

Thus:

```text
direct basis + duplicate V553 path
    -> one canonical SCR554 semantic basis
    -> at most one ELIGIBLE F1
    -> at most one corresponding V555 route input
```

## 6. HQ mixed-authority snapshot guard

S554D correctly warned that authority-version differences cannot be allowed to manufacture false independent support. Accepted SCR554 supplies the required fail-closed ordering.

Its deterministic basis court runs:

```text
order 3  STATIC_AUTHORITY_COMPLETENESS
order 5  DUPLICATE_EQUIVALENCE
order 7  CONJUNCTIVE_F1
```

And the exact order-3 rule is:

```text
Missing required static authority -> K06/nonassertable;
unknown/conflicting required authority without governed precedence -> K07/nonassertable.
```

Therefore a **mixed/unresolved authority snapshot for one exact invocation** never reaches duplicate grouping as two positive supports. It fails upstream as K07/no-F1.

SCR554's identity-sensitive treatment of changed rule/semantic-authority version/hash applies only after the governing authority relation has itself been resolved. A version/hash difference by itself is not M2 permission to multiply F1s or V555 routes.

M2 does not create a new V554 compatibility court. It simply refuses any F1 that should have been nonassertable under SCR554's already accepted order-3 authority gate.

## 7. F2 ownership remains upstream

Canonical F2 remains V554-owned. B1 may carry sorted exact F2 IDs; V555 receives them only by exact reference.

V555 may not:

- copy F2 semantic content under a V555 identifier;
- rename F2 into a route-born predicate;
- re-evaluate the V554 predicate;
- assert a deferred runtime/genealogy condition satisfied;
- add F2 to route identity.

The independently governed V555 route-born predicate registry remains:

```text
V555_ROUTE_BORN_PREDICATE_REGISTRY@1.0.0
VALID_EMPTY
registered_predicate_count = 0
```

No inherited F2 or downstream demand may fill that registry.

## 8. No upstream bypass

A V555 route cannot be reconstructed from any of these without the exact canonical F1/B1 seam:

```text
StructuralEmpiricalAdmission
V553 object or V553 label
legacy V554 seed/readiness ID
current V554 implementation row
copied F2 prose
source/channel/receiver labels alone
```

Those may remain reachable as producer ancestry where lawful, but none substitutes for the accepted V554 semantic object.

## 9. Exact replay binding

SCR554's authority-bundle fingerprint requires, verbatim:

- `SCR554 contract id/version`;
- `V554 affordance authority id/version/hash`;
- `V554 applicability authority id/version/hash when F2 participates`;
- `V554 rule id/version/hash`;
- `signature id`;
- `selected basis semantic identity`;
- `all interpretation-critical positive authority refs`;
- `all interpretation-critical negative/limit refs relevant to the decision`;
- `source/universe/estimand/measure/weight authority refs relevant to interpretation`;
- `producer schema/reference-contract authority versions required for deterministic interpretation`.

Accepted SCR554 replay law:

> Same contract/rule/signature versions plus same exact canonical semantic authority bundle produce identical basis selection, equivalence groups, F1/F2/B1 IDs and decision states.

M2 adds no latest lookup, fuzzy rematch, default authority, or network fallback. The exact accepted F1/B1 binding becomes the upstream part of V555's already frozen replay key.

## 10. M1 staleness condition

M1 is not an M2 launch dependency. This closure is valid against:

```text
SCR554 head: b5d745ac70c833324c8be0addf6c08ad72372263
SCR554 EXACT_CONTRACT.json blob: 4bce143b087d5e38dbb4829a979a3f43abf9ab90
```

If M1 subsequently requires a **material** SCR554 contract change affecting basis mapping, duplicate equivalence, authority precedence, F1/F2/B1 identity, use permission, or replay/reference closure, this M2 return becomes stale. Whole-machine closure must re-run M2 against the changed exact SCR554 head/hash.

## 11. M2 checksum

M2 proves:

1. `EXACT_V554_F1_REF` resolves to accepted canonical SCR554 F1 identity.
2. One V555 route consumes exactly one `ELIGIBLE` canonical F1.
3. B1 proves exact V555 structural-use permission and upstream replay but is not a route semantic participant.
4. Different canonical F1 IDs cannot collapse when the other six route fields coincide.
5. Duplicate direct/V553 or alias provenance contributes at most one canonical F1 and cannot multiply routes.
6. Mixed/unresolved authority snapshots fail K07 before F1 emission.
7. F2 remains V554-owned exact-reference-only.
8. V555 route-born predicate registry remains valid-empty unless independently governed.
9. Admission/V553/legacy-seed bypass is forbidden.
10. The V555 seven-field identity is unchanged.
11. Replay binds exact SCR554 rule/signature/authority/reference closure.
12. No broad DAG edge changes and no production implementation occurs.

## 12. Closure

The SCR555 waiting seam is satisfied. No new V554 identity was invented, no V555 semantic field was added, and no authority conflict remains.

`M2_ACCEPTED__SCR555_EXACT_CONTRACT_CLOSED`
