# SCR553 V553 EXACT CONTRACT

**Contract:** `SCR553_V553_TEMPORAL_JURISDICTION_V1`  
**Identity law:** `SCR553_V553_IDENTITY_V1`  
**Scope:** V553 local semantic/input/reference/replay jurisdiction only.

## 1. Jurisdiction

V553 consumes only exact `StructuralEmpiricalAdmission` references and creates only new temporal semantics required by one exact governed use chain. It is neither a universal stage wrapper nor an empirical-admission court.

The core invariant is:

```text
V553_REQUIRED(A, U)
iff
U requires at least one new V553-owned temporal operation
not already lawfully supplied by A for U
and every authority prerequisite for that operation is exact and positive.
```

`A` is never permanently classified as temporal or non-temporal. The predicate is evaluated for `(admission set, governed use, use-rule version/hash)`.

## 2. Exact intake/reference adapter

### 2.1 Lawful semantic intake

The request contains `1..n` exact references of kind `STRUCTURAL_EMPIRICAL_ADMISSION`.

Every reference must carry:

```text
kind
object_id
content_hash   # lowercase SHA-256
```

Resolution must recover the frozen D15 admission semantics: exact EmpiricalFact and EmpiricalQuerySpec refs, source-universe identity, admission rule id/version/hash/effective period, target structural meaning, interpreted proposition, temporal scope, support/uncertainty, replay/provenance refs, negative/limit authority, typed admission state, and downstream producer/use permission.

A mutable path or locator may be implementation lookup machinery, but it is never semantic authority. It must resolve the exact `(object_id, content_hash)` requested. Resolution by latest run, latest version, directory order, file mtime, score, or nearest label/time is forbidden.

### 2.2 Forbidden intake

The following cannot cross the V553 semantic boundary directly:

```text
EmpiricalFact
DiscoveryResultReceipt
raw C11 incidence
V552 row/packet
V552J row/packet/handoff
readiness/probe/harmonization score
provenance pointer without StructuralEmpiricalAdmission
```

A compatibility adapter may exist later only if it first resolves or constructs the **already-authorized** exact `StructuralEmpiricalAdmission` under the frozen admission authority. V553 itself may not reconstruct admission from legacy fields.

### 2.3 Typed upstream negatives

A resolved admission with a denied, noncomparable, missing-authority, negative-authority-only, or other nonpositive typed state is not promoted. For the requested use:

- if V553 owns an exact temporal negative/limit classification, emit only the corresponding `TEMPORAL_LIMIT`;
- otherwise preserve the exact upstream negative by reference and return no positive V553 semantic object.

## 3. Governed-use request

`V553TemporalizationRequest` is control-plane input, not a fifth published semantic family. Its semantic identity includes:

```text
request_contract_version
governed_use_id
use_owner
use_rule_ref
participants[]:
    role
    ordinal
    structural_empirical_admission_ref
required_temporal_operations[]
temporal_operation_rule_refs[]
required_external_compatibility_refs[]
```

Allowed temporal operations are:

```text
CANONICALIZE_TEMPORAL_SCOPE
EXPRESS_TIME_SCOPED_OBSERVATION
HARMONIZE_TEMPORAL_REPRESENTATIONS
COMPARE_ACROSS_TIME
DERIVE_EFFECTIVE_INTERVAL
DERIVE_SEQUENCE_OR_TIMING
DERIVE_TEMPORAL_RELATION
EVALUATE_TEMPORAL_LIMIT
```

Participants are explicit. V553 does not search for the previous, next, nearest, best, latest, or most similar observation/source.

## 4. Need predicate

The deterministic decision sequence is:

1. resolve and hash-verify every admission ref;
2. bind the exact governed use and use-rule authority;
3. forbid positive output if upstream admission does not positively permit the requested use;
4. compute the new temporal operations actually required by this use;
5. if none are new, return `V553_NOT_REQUIRED_FOR_THIS_USE` and create zero `TEMPORAL_*` objects;
6. require exact temporal rule id/version/hash for every new operation;
7. require every operation-declared source/measure/estimand/linkage prerequisite;
8. if any required authority is missing, unknown, negative, or noncomparable, fail closed with typed `TEMPORAL_LIMIT` where V553 owns that limit, otherwise no positive output;
9. only then create the mapped canonical temporal family objects.

These are categorical anti-inferences:

```text
HAS_TIMESTAMP
HISTORICAL_SOURCE
V553_ARTIFACT_PRESENT
!= NEEDS_V553

SAME_YEAR
SAME_LABEL
SAME_CANONICAL_VALUE
!= SOURCE_COMPARABILITY_AUTHORITY

PROVENANCE_REACHABILITY
!= POOLING_OR_COMPOSITION_AUTHORITY

EARLIER_DIRECT_USE
!= PERMANENT_V553_EXEMPTION
```

## 5. TEMPORAL_KEY

**Grain:** one canonical governed temporal identity/scope for one source-indexed admitted structural basis, or one derived temporal scope whose exact derivation participants and rule are referenced.

Required semantic fields:

```text
family = TEMPORAL_KEY
schema_version
temporal_key_id
source_universe_ref
admission_ref
canonical_temporal_scope
temporal_rule_ref
derivation_participant_refs[]
authority_closure_refs[]
semantic_hash
```

Rules:

- A key exists only when the use requires new V553 temporal identity.
- A key never fuses independent source universes because dates/labels coincide.
- A derived interval names every exact participant and derivation rule.
- Unknown/ambiguous time that prevents exact identity produces `TEMPORAL_LIMIT`; no guessed key is created.

## 6. TEMPORAL_OBSERVATION

**Grain:** one admitted structural proposition/value/status expressed at one exact `TEMPORAL_KEY`.

Required semantic fields:

```text
family = TEMPORAL_OBSERVATION
schema_version
temporal_observation_id
temporal_key_ref
admission_ref
source_universe_ref
admitted_value_or_status
value_owner_ref
support_uncertainty_state
temporal_rule_ref
authority_closure_refs[]
semantic_hash
```

Rules:

- value/proposition validity remains upstream/admission-owned;
- V553 may time-scope/canonicalize it but cannot improve support or infer empirical validity;
- `OBSERVED_ZERO` is a measurement, not missingness, valid-empty, or a limit;
- missing/unavailable/noncomparable/conflicting states remain typed and cannot be turned into a zero.

## 7. TEMPORAL_RELATION

**Grain:** one governed relation over explicit role/order-preserving exact temporal participants.

Required semantic fields:

```text
family = TEMPORAL_RELATION
schema_version
temporal_relation_id
relation_kind
relation_rule_ref
participants[]
source_universe_refs[]
required_external_compatibility_refs[]
result_state
result_payload
support_uncertainty_state
authority_closure_refs[]
semantic_hash
```

`relation_kind` has no fallback/default; exact rule authority supplies it. Accepted law includes kinds such as `DELTA`, `PERSISTENCE`, `DRIFT`, `REVERSAL`, `RUPTURE`, `REVISION`, and `COINCIDENCE`.

Positive relation law:

```text
POSITIVE_TEMPORAL_RELATION
requires
exact relation rule
+ exact participants
+ exact temporal comparability authority
+ every operation-declared external compatibility prerequisite.
```

For cross-source/cross-universe operations, same year or label similarity is never enough. If the relation requires measure or estimand compatibility, those authorities must already be positive. A same-respondent longitudinal claim additionally requires separately governed respondent linkage.

V553 does **not** create pooling, respondent linkage, cross-universe composition, or source equivalence. If a downstream operation needs a pooled/composed empirical fact, that composition must occur at its lawful owner and arrive as a separately admitted structural proposition.

Temporal delta direction is distinct from producer structural source→target direction.

## 8. TEMPORAL_LIMIT

`TEMPORAL_LIMIT` is a canonical semantic negative/limit family, not diagnostic exhaust.

Required fields:

```text
family = TEMPORAL_LIMIT
schema_version
temporal_limit_id
governed_use_id
requested_operation
limit_state
limit_reason
participant_refs[]
blocked_output_family
missing_or_negative_authority_refs[]
upstream_negative_refs[]
temporal_rule_ref
authority_closure_refs[]
semantic_hash
```

Allowed `limit_state`:

```text
BLOCKED
NONCOMPARABLE
VALID_EMPTY
UNRESOLVED
OUT_OF_JURISDICTION
EXECUTION_LIMIT
```

Allowed `limit_reason`:

```text
MISSING_TEMPORAL_AUTHORITY
MISSING_SOURCE_COMPARABILITY_AUTHORITY
MISSING_ESTIMAND_COMPATIBILITY_AUTHORITY
MISSING_MEASURE_COMPATIBILITY_AUTHORITY
MISSING_RESPONDENT_LINKAGE_AUTHORITY
NONCOMPARABLE
TEMPORAL_SCOPE_MISSING
TEMPORAL_SCOPE_AMBIGUOUS
TEMPORAL_SCOPE_MISMATCH
INSUFFICIENT_PERIODS
BASELINE_UNAVAILABLE
CONFLICT
UPSTREAM_NEGATIVE_AUTHORITY
UNSUPPORTED_OPERATION
BACKEND_UNAVAILABLE
MALFORMED_ADMISSION_REFERENCE
HASH_OR_VERSION_MISMATCH
UNKNOWN
VALID_EMPTY
OUT_OF_JURISDICTION
```

An execution limit such as `BACKEND_UNAVAILABLE` asserts only that the governed operation could not execute; it does not imply empirical absence or noncomparability.

A limit never licenses positive substitution, nearest-time fallback, latest-run fallback, source pooling, or silent direct-basis downgrade.

## 9. Exact family mapping

| Operation | Positive family outcome | If blocked |
|---|---|---|
| `CANONICALIZE_TEMPORAL_SCOPE` | `TEMPORAL_KEY` | `TEMPORAL_LIMIT` |
| `EXPRESS_TIME_SCOPED_OBSERVATION` | `TEMPORAL_KEY` + `TEMPORAL_OBSERVATION` | `TEMPORAL_LIMIT` |
| `DERIVE_EFFECTIVE_INTERVAL` | derived `TEMPORAL_KEY` | `TEMPORAL_LIMIT` |
| `DERIVE_SEQUENCE_OR_TIMING` | `TEMPORAL_RELATION` | `TEMPORAL_LIMIT` |
| `COMPARE_ACROSS_TIME` | `TEMPORAL_RELATION` | `TEMPORAL_LIMIT` |
| `HARMONIZE_TEMPORAL_REPRESENTATIONS` | canonical `TEMPORAL_KEY` object(s); relation only if rule explicitly creates one | `TEMPORAL_LIMIT` |
| `DERIVE_TEMPORAL_RELATION` | `TEMPORAL_RELATION` | `TEMPORAL_LIMIT` |
| `EVALUATE_TEMPORAL_LIMIT` | `TEMPORAL_LIMIT` | `TEMPORAL_LIMIT` |

No-op temporal wrapping is forbidden. If the admitted temporal scope is already sufficient for the use and the use requests no new V553 operation, the only lawful V553 result is `V553_NOT_REQUIRED_FOR_THIS_USE` with zero semantic objects.

## 10. Source/comparability boundary

Default:

```text
PRESERVE_SOURCE_PLURALITY
NO_COMPOSITION
```

Positive temporal comparison may consume separately governed comparability prerequisites. It never becomes the owner of those prerequisites.

Forbidden transformations include:

```text
same calendar time -> source equivalence
shared labels -> source equivalence
reachable provenance -> pooling
temporal comparability -> estimand compatibility
temporal comparability -> respondent linkage
temporal comparability -> cross-universe composition
```

Unknown/missing applicability/comparability authority is fail-closed.

## 11. Deterministic identity

Canonical serialization is UTF-8 JSON with:

- object keys lexicographically sorted;
- no insignificant whitespace;
- arrays preserving declared semantic order;
- set-like arrays deduplicated and lexicographically sorted only when the governing rule declares order-insensitivity;
- NaN/Infinity forbidden.

Hash: `SHA-256`.

Object ID:

```text
V553:<FAMILY>:SCR553_V1:<sha256(canonical_identity_material)>
```

Identity material excludes the ID/hash fields themselves and excludes wall-clock timestamps, session IDs, randomness, filesystem order, mutable latest-run state, and nonsemantic probe/readiness scores.

## 12. Replay

For the same exact request, exact referenced content, and exact authority versions/hashes, replay must produce:

```text
same route decision
same semantic object set
same semantic hashes
same object IDs
```

An authority/content hash change is a new replay basis. The machine may not silently substitute a later authority or source snapshot. Hash mismatch or missing immutable dependency fails closed.

`ReplayReceipt` remains audit/replay-only.

## 13. Later-use semantics

Example:

```text
A = exact admitted 1985 proposition

U1:
  consumes 1985 proposition as-is
  -> V553_NOT_REQUIRED_FOR_THIS_USE
  -> zero V553 objects

U2 later:
  asks whether A persisted to 1995
  -> exact U2 temporal demand evaluated independently
  -> if rule + participants + comparability authority positive: V553 relation
  -> otherwise typed limit / no positive output
```

U1 does not mutate A and does not grant U2 a permanent bypass.

## 14. M1 boundary

SCR553 exports exact V553 references:

```text
TEMPORAL_KEY_REF
TEMPORAL_OBSERVATION_REF
TEMPORAL_RELATION_REF
TEMPORAL_LIMIT_REF
```

Each ref minimally binds:

```text
family
object_id
content_hash
schema_version
```

SCR553 does **not** decide V554 `basis_kind`, direct eligibility, duplicate equivalence, precedence, or F1/F2/B1 identity. Those are SCR554 jurisdiction.

Binding negative seam rule:

```text
V553 TEMPORAL_LIMIT / negative for temporal demand U
cannot be silently bypassed by
positive DIRECT_STRUCTURAL_EMPIRICAL_ADMISSION basis for the same U.
```

M1 must jointly prove that rule with SCR554's exact basis/precedence contract.
