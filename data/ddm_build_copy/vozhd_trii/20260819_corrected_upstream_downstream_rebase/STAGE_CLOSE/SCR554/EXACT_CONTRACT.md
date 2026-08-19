# SCR554 — Exact V554 basis / dedup / affordance contract

**Authority:** dispositive local stage-close contract only  
**Contract:** `SCR554_V554_BASIS_DEDUP_AFFORDANCE_EXACT_CONTRACT@1.0.0`  
**Broad topology:** unchanged / R03 closed  
**Implementation:** not authorized

## 1. Local closure holding

V554 has exactly two lawful semantic basis kinds:

```text
DIRECT_STRUCTURAL_EMPIRICAL_ADMISSION
V553_TEMPORAL_OBJECT
```

They are not interchangeable transport lanes. The exact V554 rule invocation determines which kind may count as semantic support.

The accepted ADP-001 signature IDs remain the rule grammar:

```text
V554-SIG-001-NONTEMPORAL-EXACT
V554-SIG-002-TEMPORAL-POINT-EXACT
V554-SIG-003-TEMPORAL-RELATIONAL-EXACT
```

SCR554 closes their corrected basis interpretation without minting a new V554 semantic family:

| signature | semantic basis kind that may count | rule |
|---|---|---|
| `SIG-001` | `DIRECT_STRUCTURAL_EMPIRICAL_ADMISSION` | V553 material may remain contextual/provenance only; it contributes zero support to this invocation. |
| `SIG-002` | `V553_TEMPORAL_OBJECT` | exact V553 key + observation semantics required. |
| `SIG-003` | `V553_TEMPORAL_OBJECT` | exact V553 key + relation + all rule-required support/limit semantics required. |

This is the corrected post-admission ingress law. A generic V552/V552J bundle, raw `EmpiricalFact`, discovery receipt, PSEPF, legacy V554 seed row, interpolation product, or score/readiness surface is not a V554 semantic basis.

## 2. Exact direct-admission consumer contract

A direct basis MUST expose, either inline as exact immutable refs or by deterministic content-addressed dereference:

- `structural_empirical_admission_id` + immutable content hash;
- admission authority ID/version/hash and exact admission decision state;
- focal structural proposition identity and all identity-bearing structural refs required by the V554 rule;
- native source/geographic/scope identity and grain;
- exact target-use permission authority;
- effective-time/interval refs required by the exact target use;
- exact source-universe, estimand, measure and weight-authority refs material to interpretation;
- applicable denial/negative/noncomparability refs;
- interpretation-critical semantic authority refs;
- an immutable replay/reference root reaching the underlying empirical fact/query/universe/measure authority.

These names are V554 **consumer slots**. SCR554 does not re-own or require upstream producers to duplicate their payloads. Exact transitive reference closure satisfies the slot.

## 3. Exact V553-basis consumer contract

A V553 basis MUST expose, directly or by immutable dereference:

- V553 object ID, content hash and object family;
- exact originating `StructuralEmpiricalAdmission` ref set;
- focal structural proposition ref;
- all V553 semantic refs required by the selected point/relational signature;
- native scope identity;
- source-universe, estimand, measure/weight-authority refs material to interpretation;
- source-relation/comparability authority refs where the requested temporal operation requires them;
- applicable V553 limit/noncomparability/gap/absence refs;
- interpretation-critical semantic authority refs;
- immutable replay/reference root.

SCR554 does **not** legislate SCR553's internal schema. M1 must prove that the accepted SCR553 object projects losslessly into these consumer slots. Missing or inferred source equivalence is not a legal projection.

## 4. Target-use temporal completeness

Machine contract: `V554_TARGET_USE_TEMPORAL_COMPLETENESS@1.0.0`.

A candidate is `COMPLETE_FOR_DIRECT_V554` iff all of the following hold for the exact V554 invocation:

1. target use is `STRUCTURAL_MEDIATION_INPUT` under `V554-SIG-001-NONTEMPORAL-EXACT`;
2. the admitted structural proposition is complete for that invocation;
3. every time/interval/scope fact required by the invocation is already exact and governed, or the invocation expressly requires no additional temporal discrimination;
4. the invocation requires **no new V553-owned meaning**: no new cross-time comparability/harmonization, temporal point support construction, relation/delta, derived period/interval, sequence, persistence, drift, change, reversal, rupture, revision, temporal limit/noncomparability, or typed temporal gap/absence decision;
5. every material source/time/applicability relation is positively governed;
6. no applicable denial, noncomparability, required gap/absence, unknown source relation, or unresolved authority blocks the invocation.

The other exact states are:

```text
REQUIRES_V553_OWNED_TEMPORAL_MEANING
BLOCKED_BY_APPLICABLE_TEMPORAL_OR_SOURCE_NEGATIVE
UNKNOWN_FAIL_CLOSED
NOT_APPLICABLE_TO_TARGET_USE
```

A timestamp, wave label, historical-source membership, or V553 artifact's physical existence never by itself requires V553.

An applicable temporal/source negative may not be escaped by silently downgrading a point/relational invocation to direct. A genuinely different direct invocation is lawful only when it has its own rule/signature/use identity and the negative is outside that invocation's governed scope.

## 5. Exact source-sensitive duplicate equivalence

Machine contract: `V554_SOURCE_SENSITIVE_DUPLICATE_EQUIVALENCE@1.0.0`.

Canonicalization uses UTF-8 canonical JSON, lexicographically sorted object keys, exact-deduplicated + bytewise-sorted semantically unordered ref arrays, governed order for semantically ordered arrays, then SHA-256.

The duplicate-equivalence key contains:

```text
focal_structural_proposition_ref
target_use
v554_rule_id
v554_rule_version
v554_rule_hash
rule_relevant_structural_semantic_identity_fingerprint
native_scope_identity_fingerprint
rule_relevant_effective_time_semantics_fingerprint
originating_structural_empirical_admission_lineage_fingerprint
source_universe_fingerprint
estimand_fingerprint
measure_and_weight_authority_fingerprint
rule_relevant_source_relation_comparability_authority_fingerprint
interpretation_critical_semantic_authority_fingerprint
```

`basis_kind` is deliberately **not** in the equivalence key. Otherwise direct and V553 paths could never be recognized as duplicate support.

Likewise excluded: run ID, path, filename, row number, enumeration order, wall clock, legacy seed type/scope, scores/readiness, and a nonsemantic locator change with unchanged immutable content.

Two candidates are equivalent only when every required material component resolves exactly and canonical bytes are identical. They are non-equivalent only when at least one exactly resolved **material** component differs.

If any required component is missing, ambiguous, mutable, hash-mismatched, not deterministically dereferenceable, or its materiality cannot be established:

```text
EQUIVALENCE_UNKNOWN -> FAIL_CLOSED
```

No F1 may be emitted for the affected collision set. Exact unresolved/conflict refs may be preserved as K07-compatible nonpositive context where semantically meaningful.

### Source plurality

Label equality and canonical proposition-text equality are never sufficient. Source universe, risk set, estimand, measure/weight authority, scope, admission lineage and semantic authority distinctions remain distinct whenever they can change interpretation or lawful use.

Conversely, extra V553 material that the exact rule does **not** require does not turn a no-op restatement into independent support. Only rule-relevant temporal meaning participates in the equivalence key.

## 6. Deterministic precedence — no winner heuristic exists

Machine contract: `V554_BASIS_SELECTION_AND_PRECEDENCE@1.0.0`.

Order:

1. **Integrity.** Schema/hash/reference/coherence failure -> `INTEGRITY_FAILURE`; no fabricated semantic F2/B1 denial.
2. **Producer precedence.** Honor exact precedence already governed by the producer; V554 invents none.
3. **Applicable denial/hard negative.** Exact target-use denial, temporal noncomparability, or required gap/absence blocks F1.
4. **Static authority completeness.** Missing -> K06. Unknown/conflicting without governed precedence -> K07.
5. **Temporal-completeness + signature gate.** Signature fixes required `basis_kind`; unresolved completeness -> no route.
6. **Duplicate equivalence.** Build source-sensitive groups; unknown equivalence fails the affected group closed.
7. **Canonical basis kind.**
   - `SIG-001` counts direct admission only.
   - `SIG-002/003` count V553 temporal basis only.
   - nonrequired/no-op duplicate physical objects contribute zero support.
8. **Conjunctive F1.** One equivalence group can emit at most one `ELIGIBLE` F1.
9. **Deferred/informational F2.** K01-K03 may coexist with F1; K04 remains informational. They neither add support nor determine basis precedence.

Forbidden precedence mechanisms:

```text
latest
highest score
readiness
confidence
majority
file order
row order
filename
artifact presence
descriptive specificity
```

### Same-kind aliases/reissues

If several physical refs of the same basis kind are exactly semantically equivalent, they count once. The machine does not choose a physical “winner.” It derives one canonical semantic-basis ID and preserves all equivalent physical refs in bytewise-sorted `provenance_alias_refs`.

### Distinct evidence

If material equivalence-key components differ, candidates remain distinct. No averaging, netting, winner selection, or majority collapse is allowed.

## 7. Canonical F1 / F2 / B1 identity

All identities are semantic, content-derived and independent of run/file/row order:

```text
urn:rawlsing:<family>:sha256:<digest>
```

### Canonical basis semantic ID

```text
SHA256({
  equivalence_key,
  required_basis_kind,
  selected_rule_relevant_basis_semantics
})
```

### F1

```text
F1 state = ELIGIBLE only

F1_id = SHA256({
  SCR554 contract version,
  equivalence_key,
  canonical_basis_semantic_id,
  rule id/version/hash,
  signature id,
  target use,
  authority_bundle_fingerprint
})
```

Rejected duplicate-path existence or alias enumeration does not change F1 identity.

### F2

F2 remains exactly the nine ADP-001 kinds canonicalized by CAN-001. SCR554 creates no tenth kind.

```text
F2_id = SHA256({
  SCR554 contract version,
  candidate_semantic_key,
  F1_id or null,
  condition_kind_id,
  predicate_id/version,
  semantic_owner,
  resolution_owner,
  binding_producer,
  evaluator_owner,
  canonical argument-envelope fingerprint,
  target use,
  exact producer negative/requirement refs
})
```

K01-K03 remain runtime-deferred; K06/K07 are missing/unknown static authority; K05/K08/K09 are hard-use-block context. These may not be collapsed.

### B1

B1 is a governed boundary identity, not a third semantic family:

```text
B1_id = SHA256({
  SCR554 contract version,
  candidate_semantic_key,
  F1_id or null,
  sorted F2_ids,
  allowed_v555_structural_use,
  decision_state,
  producer_reference_spine_fingerprint
})
```

`allowed_v555_structural_use = true` iff a positive F1 exists and no applicable hard nonpositive state blocks the target use. K01-K03 deferred requirements and K04 informational constraints do not by themselves make it false.

Producer/rule-backed K05-K09 context may cross B1 with `allowed_v555_structural_use=false`. Integrity failure never becomes semantic B1 context.

## 8. Authority-bundle fingerprint and replay

The authority-bundle fingerprint covers the SCR554 contract version, ADP-001 authority, CAN-001 authority when applicable, exact V554 rule/signature, selected semantic basis, all interpretation-critical positive and negative refs, material source/universe/estimand/measure/weight authority, and producer schema/reference-contract authority needed for deterministic interpretation.

It excludes row/file order, wall clock, legacy scores/readiness and rejected duplicate-path existence.

Therefore:

- identical canonical authority bundles replay to identical basis choice, support count, F1/F2/B1 IDs and decision states;
- input permutation changes nothing;
- a changed rule, material source universe, estimand, measure authority, semantic authority, or rule-relevant temporal semantic changes identity rather than silently reusing an old object;
- no fuzzy rematch, mutable latest lookup, network fallback, or default interpolation is legal during replay.

Each duplicate-equivalence group contributes **at most one** semantic support basis to one proposition/use/rule invocation.

## 9. Typed negative / unknown precedence

ADP-001 §9 remains controlling, extended only for the new basis/dedup ingress:

| state | V554 result |
|---|---|
| `INTEGRITY_FAILURE` | presemantic; no F1 and no fabricated semantic denial |
| explicit use denial | no F1; K05 where governed |
| required temporal noncomparability/gap | no F1; K08/K09 |
| missing required static authority | no F1; K06 |
| unknown/conflicting required authority | no F1; K07 |
| `EQUIVALENCE_UNKNOWN` | affected group fails closed; no F1 |
| all gates pass | one `ELIGIBLE` F1 |
| coherent zero candidates | `VALID_EMPTY`; no filler |

Observed numeric zero remains a measurement. It is not missing authority, denial, or a low-score rejection.

A negative blocks only the exact proposition/use/rule scope it governs. V554 may neither broaden it nor evade it by route downgrade.

## 10. Hostile bypass controls

The contract explicitly rejects:

- raw `EmpiricalFact` / discovery receipt / PSEPF at V554 semantic ingress;
- direct basis when new V553-owned temporal meaning is required;
- V553 semantic support for `SIG-001` merely because a V553 artifact exists;
- temporal signature downgrade to evade denial/noncomparability/gap;
- source-insensitive, text-only, label-only, score-based, latest-based or order-based dedup;
- `EQUIVALENCE_UNKNOWN`;
- interpolation/backfill/nearest-wave/country-year projection as F1 authority;
- legacy seed/readiness IDs as canonical F1/F2/B1 identity;
- `StructuralEmpiricalAdmission -> V555/V556` semantic bypass.

## 11. Seam handoff

### M1 — SCR553 + SCR554

SCR553 must provide an exact immutable projection sufficient for the V553 consumer slots above. M1 must prove:

- direct and temporal basis kinds are mutually typed;
- later use-chain temporalization remains possible without object-global classification;
- source relation/comparability is never invented by V553/V554;
- applicable temporal/source negatives cannot silently become direct positive basis;
- duplicate equivalence is source-sensitive and deterministic.

### M2 — SCR554 + SCR555

SCR555 receives exactly one canonical F1 per route by exact `F1_id`/`B1_id`. Inherited F2 is V554-owned and travels by `F2_id` reference only. V555 may not reconstruct V554 meaning from admission objects, V553 labels, legacy seed IDs or copied condition prose.

### M4 — producer publication

V557/V558 must preserve V554 canonical IDs/hashes, typed negative state, authority bundle and reference spine without re-ID or reownership.

## 12. Closure

No evidence requires an added/deleted/reversed broad DAG edge. The missing exact basis/dedup machinery was explicitly delegated to SCR554 and is closed here with fail-closed semantics.

Production code remains untouched and implementation remains separately gated.
