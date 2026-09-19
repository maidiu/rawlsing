# FIABC-B04 — Collapse hazards

The frozen candidate implementations contain several explicit fail-closed seams. Those seams are the controls that must survive any later packaging or optimization change.

## 1. Physical missingness → semantic missingness

`PhysicalMissingState` is source-incidence information, not a response-semantic decision. B computes a physical binding key from raw value + physical state + source missing declaration and requires a unique governed response rule. An unbound response value/state is an error. A reconstructs all three physical ingredients before delegating to B. C stores both physical missing state and projected response state in its state envelope; if a source-missing declaration cannot fit the frozen accelerator layout, C requires cacheless exact-source fallback.

**Hazard:** a future adapter that maps `SYSTEM_MISSING` directly to semantic `MISSING`, drops a source missing declaration, or treats a physically absent cell as `None` would silently manufacture semantics.

## 2. Routing unknown → false/nonmember

I03 `_risk_membership` explicitly rejects unresolved routing states. Missing exact routing/risk-set membership is stated to be absence of evidence, not zero membership. `INAPPLICABLE` remains an explicit state and is counted separately.

**Hazard:** booleanizing routing state, using Python truthiness, or defaulting missing routing to `False` destroys the difference among unknown, unavailable, inapplicable, and explicit nonmembership.

## 3. Typed absence → omitted field / `None`

C11 `TypedAbsence` states are explicit and its docstring says a missing Python key/value is never equivalent. B uses `TypedAbsence("NOT_APPLICABLE")` for genuinely not-applicable sections rather than silently omitting them.

**Hazard:** serialization layers that drop empty/None fields can erase `UNKNOWN`, `NOT_APPLICABLE`, `NONCOMPARABLE`, `DEFERRED`, `VALID_EMPTY`, and `INTEGRITY_FAILURE` distinctions.

## 4. Empty topology → all-missing → no event

The query evaluator treats topology as governed material. Non-substantive response events are converted to typed response-state payloads, while incompatible carrier/query topology raises. B also requires every projected physical slot to cover the full row replay map; an absent physical cell is not semantic absence.

**Hazard:** collapsing an empty multiselect, no event, all typed-missing events, and unsupported topology to a single empty list/None would change both denominator meaning and replay identity.

## 5. Unresolved/denied authority → positive default

Canonical authority refs are exact id/version/hash triples. Canonical object identity includes authority and dependency closure. `AuthoritySnapshot` rejects fuzzy/latest/default selection. Component-authority vector logic refuses scalarization when coverage is incomplete, governed-empty, denied, or noncomparable.

**Hazard:** fallback to latest authority, default authority, first matching value, or scalar default can convert a negative authority state into ordinary data.

## 6. Source-local uncertainty → semantic equivalence

I07 states that universes are distinct by default and that no relation kind implies another. Provenance and harmonization alias are descriptive and do not grant semantic equivalence, linkage, nonduplication, pooling, composition, or backfill.

**Hazard:** matching variable names, labels, provenance, or carrier layout must never be used to infer cross-source equivalence or authorize composition.

## 7. Governance `BLOCKED`/manual review → empirical state

The inspected public PRE553 state families do not contain `BLOCKED` or `MANUAL_REVIEW` as response/query/fact values. Those are governance/court dispositions over evidence. The underlying machine-readable states (`UNKNOWN`, `DEFERRED`, `UNRESOLVED`, authority errors, typed negatives) must remain intact beneath review.

**Hazard:** introducing `BLOCKED` as a semantic value, or replacing a blocked/manual-review condition with `VALID_EMPTY`, `UNKNOWN`, zero support, or `None`, mixes orchestration with empirical meaning.

## 8. Accelerator/cache → authority

C's module states that accelerators are optional content-addressed execution representations and never define semantic truth, candidate reachability, terminal states, or learned products. Its determinants bind exact source, projection, C11 release, replay manifest, and semantic-authority hashes. B's session cache checks source identity and rejects stale/tampered entries.

**Hazard:** a warm cache or persistent transformed representation must not become the authority simply because it is cheaper or already present.

## 9. Regenerable deletion → provenance deletion

The P2 deletion law allows deletion of P4 optional caches and P5 transient compiler artifacts, not P1 source, P2 governed products, or P3 replay/provenance determinants.

**Hazard:** a cleanup routine that deletes replay manifests, exact source refs, authority closure, or governed product refs while retaining only a fast carrier would make a later replay unprovable.

## 10. Held measurement → result

The sealed HQ checkpoint says measured P2X is held pending exact local stopped-ledger reconciliation.

**Hazard:** treating lack of a measured result as candidate failure, candidate success, valid empty, or evidence of semantic inequality would collapse orchestration state into empirical/court meaning.
