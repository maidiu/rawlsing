# S553R HOSTILE FIXTURES

**Purpose:** non-dispositive test oracles for SCR553 and M1. These fixtures test only the frozen R03/V553 routing/source-comparability ceiling. They do not choose implementation or SCR554 duplicate-key internals.

## Fixture H01 — one admission, two uses, opposite routes

### Given

`A` is a positive `StructuralEmpiricalAdmission` with exact effective time `1985` and all source/applicability refs required for a same-point use.

- `U1`: V554 asks whether `A` is eligible for one bounded structural affordance at 1985.
- `U2`: a later governed use asks whether the same structural condition persisted from 1985 to 1995, using another lawfully admitted observation.

### Expected

- `ROUTE(A,U1) = DIRECT A -> V554` if the exact V554 direct-basis rule admits it.
- `ROUTE(A,U2) = V553 temporal relation/limit -> downstream` when the exact V553 relation authority exists.
- The U1 bypass decision must not be stored or interpreted as a permanent `A.is_non_temporal = true` property.

### Failure oracle

Fail if U2 reuses U1's direct-bypass classification without evaluating the later temporal relation demand.

---

## Fixture H02 — timestamp present, no temporal transform

### Given

`A` carries exact source year/time and historical provenance. `U` asks only for a same-time bounded V554 affordance. A legacy compatibility process can construct a V553-shaped observation with the same time fields.

### Expected

Direct V554, provided the exact direct-basis rule is positive.

### Failure oracle

Fail if timestamp/history metadata, V553 artifact presence, stage numbering, or compatibility-view existence forces V553.

---

## Fixture H03 — derived interval requires V553

### Given

`A` is an exact point observation. `U` requires a governed effective interval derived from observation timing.

### Expected

- V553 required if the exact interval-derivation authority exists.
- If authority is absent/unknown, no positive route; a `TEMPORAL_LIMIT` is allowed only under an exact limit rule covering the attempted operation.

### Failure oracle

Fail if V554 treats point time as the required interval, or if V553 invents an interval without authority.

---

## Fixture H04 — same year, same labels, different universes

### Given

`U1` and `U2` are distinct `EmpiricalUniverse`/source identities. Both have year `1990`, canonical label `employment=unemployed`, similar support, and identical displayed structural proposition text. No explicit source relation/comparability authority exists for the requested cross-source temporal use.

### Expected

- No positive cross-source temporal relation.
- No pooling, respondent linkage, or synthetic same-source identity.
- Preserve source plurality.
- Emit/preserve typed noncomparability/missing-source-authority state where the exact V553 negative contract owns the attempted temporal operation; otherwise fail closed with no positive output.

### Failure oracle

Fail if same year/label/value creates source equivalence or direct positive comparison.

---

## Fixture H05 — comparison authorized, pooling not authorized

### Given

Two distinct universes have an explicit source relation authority permitting one exact temporal comparison/harmonization. No sample-pooling, respondent-linkage, or estimand-composition authority exists.

### Expected

V553 may produce the authorized temporal comparison/limit. Source components remain separately identified. No pooled source or combined respondent sample is created.

### Failure oracle

Fail if `COMPARABLE_FOR_TEMPORAL_OPERATION` is treated as `POOLING_AUTHORIZED`, `LINKAGE_AUTHORIZED`, or `SAME_UNIVERSE`.

---

## Fixture H06 — source relation positive, temporal operation authority missing

### Given

Source relation/comparability is positively governed for the two source observations. The requested operation is `PERSISTENCE`, but no exact V553 persistence rule/version is available.

### Expected

No positive persistence semantic. A negative/limit may be recorded only if an exact limit rule owns missing-operation authority for that attempt.

### Failure oracle

Fail if source comparability alone is treated as authority to create persistence/drift/change.

---

## Fixture H07 — V553 authority positive, source relation unknown

### Given

A V553 delta rule exists, but the requested cross-source pair has no positive source relation/comparability authority.

### Expected

No positive delta. V553 cannot bootstrap its own input comparability. Preserve/emit typed source/temporal limit where governed.

### Failure oracle

Fail if existence of the delta rule converts source relation `UNKNOWN` into `COMPARABLE`.

---

## Fixture H08 — temporal noncomparability cannot downgrade to direct basis

### Given

For exact use `U`, V553 has a governed `TEMPORAL_LIMIT(INSUFFICIENT_COMPARABILITY)` or equivalent negative over the relevant admission pair. A direct `StructuralEmpiricalAdmission` object is physically available and V554 supports direct basis for some uses.

### Expected

For `U`, the negative/limit blocks a positive direct basis that would assert the same temporal/comparative meaning.

### Failure oracle

Fail if code chooses direct admission merely because it is available and thereby erases the limit.

---

## Fixture H09 — negative is use-scoped, not globally poisonous

### Given

Same materials as H08, but a distinct use `U2` asks only for a same-source same-point affordance and does not rely on the blocked cross-source comparison.

### Expected

`U2` may route directly if its own admission, source/applicability, temporal completeness, and V554 rule predicates pass.

### Failure oracle

Fail if a negative on U1 permanently invalidates A for all unrelated uses.

---

## Fixture H10 — insufficient periods

### Given

A persistence/change request has only one eligible period after exact source/applicability filtering.

### Expected

`TEMPORAL_LIMIT(INSUFFICIENT_PERIODS)` or exact equivalent. No positive persistence/change relation.

### Failure oracle

Fail if latest/only observation is reused directly as proof of persistence or no-change.

---

## Fixture H11 — baseline unavailable

### Given

A governed delta/change operation requires a baseline, but the baseline is absent/unavailable under the exact risk/source/temporal scope.

### Expected

`TEMPORAL_LIMIT(BASELINE_UNAVAILABLE)` or exact equivalent. No invented baseline and no direct positive fallback for the same use.

### Failure oracle

Fail if earliest available point, global average, or another source is substituted without explicit authority.

---

## Fixture H12 — conflict does not select a winner

### Given

Two separately lawful source/time observations conflict under an attempted governed temporal relation. Both are individually admissible; no authority declares one source superior or composable.

### Expected

Preserve conflict/noncomparability/limit state and both source identities. No majority, higher-support, local-source, newer-source, or latest-authority winner.

### Failure oracle

Fail if confidence/support/recency chooses a positive relation.

---

## Fixture H13 — V553 artifact presence is not precedence

### Given

A direct-eligible admission and a legacy/no-op V553 compatibility object representing the same time point both exist. The target use requires no V553-created temporal semantic.

### Expected

Routing is determined by exact use/rule authority, not artifact presence. The direct basis is the lawful route under the frozen broad law; exact duplicate-equivalence handling belongs to SCR554/M1.

### Failure oracle

Fail if V553 wins because it exists, is newer, has a higher stage number, or is listed first.

---

## Fixture H14 — raw EmpiricalFact ingress

### Given

An exact `EmpiricalFact` has time metadata and appears perfectly suitable for a temporal comparison, but no positive `StructuralEmpiricalAdmission` exists.

### Expected

Reject structural ingress. V553 cannot create generic empirical-to-structural meaning.

### Failure oracle

Fail if time metadata or query exactness permits raw fact -> V553/V554.

---

## Fixture H15 — observed zero versus noncomparability

### Given

Source A has an admitted observed zero under exact measure authority. Source B is not comparable to A for the requested temporal relation.

### Expected

- Preserve A's observed zero as measurement.
- Preserve B/A noncomparability separately.
- Do not coerce noncomparability to zero or zero to missing.
- No semantic delta across the noncomparable pair.

### Failure oracle

Fail if all three states collapse into one null/zero/absence code.

---

## Fixture H16 — comparison grant is operation-specific

### Given

A source relation authority permits cross-source comparison for one specific construct/time pair and rule version. A later use requests a different construct, geography, or estimand composition.

### Expected

Re-evaluate source prerequisites for the new use. Prior positive relation is not a blanket source-equivalence grant.

### Failure oracle

Fail if a prior `COMPARABLE` result becomes a global pairwise source flag authorizing unrelated comparisons or pooling.

---

## Fixture H17 — source-specific direct uses survive denied cross-source use

### Given

U1-sourceA and U1-sourceB each independently support same-point direct V554 uses. A separate U2 asks for cross-source comparison and fails source-comparability authority.

### Expected

- Both source-specific direct U1 uses remain independently lawful if their own predicates pass.
- U2 fails closed or yields negative/limit.
- No source is dropped merely because U2 is noncomparable.

### Failure oracle

Fail if cross-source noncomparability erases lawful per-source structural meaning.

---

## Fixture H18 — replay preserves routing reason

### Given

Historical routing decision was direct for U1 and V553-negative for U2 under exact authority versions. Later authority versions change.

### Expected

Replay recovers the original use identities, source relation authority refs, V553 operation authority refs, temporal completeness inputs, negative/limit object, and route decision. Later authority may produce a new decision/object but cannot reinterpret the historical one in place.

### Failure oracle

Fail if replay substitutes latest authority, reconstructs from labels, or loses why U1 and U2 routed differently.

---

# M1 seam oracle

M1 should consider the SCR553/SCR554 seam unsafe unless all of these hold simultaneously:

```text
USE_SCOPED_ROUTING
AND SOURCE_RELATION_AUTHORITY_SEPARATE
AND UNKNOWN_SOURCE_RELATION_FAILS_CLOSED
AND UNKNOWN_TEMPORAL_NEED_FAILS_CLOSED
AND APPLICABLE_TEMPORAL_NEGATIVE_BLOCKS_DIRECT_FOR_SAME_USE
AND DIFFERENT_USE_CAN_REEVALUATE_INDEPENDENTLY
AND NO_TIMESTAMP_OR_ARTIFACT_PRECEDENCE
AND NO_SOURCE_POOLING_FROM_COMPARABILITY_OR_PROVENANCE
```

These fixtures are feeder oracles only. SCR553 and M1 remain dispositive within their authorized jurisdictions.
