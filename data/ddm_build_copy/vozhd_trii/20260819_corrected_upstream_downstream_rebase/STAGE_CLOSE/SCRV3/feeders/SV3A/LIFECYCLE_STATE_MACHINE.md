# SV3A — V3 Input Lifecycle State Machine

## Principle

The V3 empirical-possibility boundary requires **orthogonal state axes**. A single `READY`, `AVAILABLE`, `VALID`, confidence score, or freshness scalar cannot preserve the distinctions required by R03.

Lifecycle classification is boundary metadata. It never grants causal permission and never converts PSEPF evidence into actor state.

## Axis A — envelope integrity

- `VALID` — exact wrapper schema/hash/root/component bindings verify.
- `INVALID_FAIL_CLOSED` — any indispensable identity/hash/schema/reference/component-manifest invariant fails.

Integrity failure dominates consumption. It is not equivalent to an empirical negative, unsupported source, valid-empty field, stale field, or missing authority.

## Axis B — freshness

- `FRESH` — the exact bound lifecycle authority classifies the exact PSEPF root as fresh for the supplied effective-time basis.
- `STALE` — the exact bound lifecycle authority classifies it as stale.
- `FRESHNESS_UNKNOWN` — required freshness authority/basis is missing or cannot lawfully determine fresh versus stale.
- `FRESHNESS_INTEGRITY_FAILED` — claimed freshness authority/basis is present but fails identity/hash/schema verification.

### Freshness non-authorizations

`FRESH` does not mean causally usable. `STALE` does not by itself decide whether contextual, review, explanatory or causal use is lawful. Those read permissions belong to the final SCRV3 metabolism/read-permission authority.

Freshness MUST NOT be inferred from hidden wall clock, file mtime, branch recency, ingestion order, current/latest aliases or source popularity.

## Axis C — refresh requirement

- `REFRESH_NOT_REQUIRED` — an exact separately-owned refresh authority positively says no refresh is required for the governed condition.
- `REFRESH_REQUIRED` — exact authority positively requires requery/regeneration.
- `REFRESH_AUTHORITY_UNBOUND` — no exact accepted refresh authority binding is present; the wrapper may not invent one.
- `REFRESH_REQUIREMENT_UNKNOWN` — an authority exists but the requirement cannot be determined under supplied exact inputs.
- `REFRESH_BINDING_INTEGRITY_FAILED` — refresh authority/request/basis identity or hash fails.

Freshness and refresh requirement are not aliases. A field may be stale while refresh authority is unbound; a refresh may be required for reasons other than age; and a fresh field may still be subject to an authority-required refresh event. The exact external authority decides, not SV3A.

## Axis D — per-source component evidentiary state

Every source component is independently classified:

- `POSITIVE`
- `UNSUPPORTED`
- `VALID_EMPTY`
- `NONCOMPARABLE`
- `UNKNOWN`
- `CONFLICT`
- `INTEGRITY_FAILURE`

The wrapper MUST preserve exact producer subtypes and authority refs when the PSEPF distinguishes finer states such as low support, observed zero, zero support, source-specific negative authority, or a named noncomparability reason.

A source component state is not a lifecycle state for the whole wrapper and cannot be collapsed into one global bit.

## Axis E — replay verification

- `REPLAY_VERIFIED_EXACT` — the exact required replay bindings, content identities and authority versions have been verified.
- `REPLAY_NOT_YET_VERIFIED` — verification has not been performed; this is not a negative semantic claim.
- `REPLAY_UNVERIFIABLE_MISSING_BINDING` — a required immutable replay binding is absent/unavailable.
- `REPLAY_INTEGRITY_FAILED` — a claimed replay identity/hash/version/content binding conflicts or fails.

Replay verification proves reproducibility/audit correspondence. It grants no causal read permission and no actor semantic authority.

## State transition law

Allowed transitions are caused only by exact new authority/material, never by convenience inference.

### Initial admission

1. Verify wrapper schema and canonical hash.
2. Verify exact PSEPF root and complete component manifest.
3. Verify generation-subject/binding consistency.
4. Classify component states by exact producer/PSEPF state refs.
5. Resolve freshness only under exact lifecycle authority.
6. Resolve refresh requirement only under exact refresh authority.
7. Classify replay verification independently.

Failure of steps 1–3 yields `INVALID_FAIL_CLOSED`; it must not be represented as `UNSUPPORTED`, `UNKNOWN`, `VALID_EMPTY`, or `STALE`.

### Fresh -> stale

A transition from `FRESH` to `STALE` is lawful only when the bound lifecycle authority and exact effective-time basis produce that classification. The wrapper does not use ambient time by itself.

### Any state -> refresh required

`REFRESH_REQUIRED` requires an exact external refresh authority decision or exact authority-defined condition. V3 intake cannot self-trigger from age, low mass, source disagreement, missing preferred source, or a newer artifact merely existing.

### Refresh completion

Refresh completion never mutates the old wrapper. It produces:

`old PSEPF/root + old wrapper` -> historical immutable objects  
`new requery/regeneration output` -> `new PSEPF root` -> `new V3EmpiricalPossibilityInput`.

The new wrapper is admitted through the same exact verification path. No continuity of ID is presumed.

### Replay transition

A wrapper may move from `REPLAY_NOT_YET_VERIFIED` to `REPLAY_VERIFIED_EXACT` only after exact verification. Verification failure becomes `REPLAY_INTEGRITY_FAILED`; it cannot be downgraded to merely unverified.

## Forbidden composite shortcuts

The following are forbidden:

- `READY=true` standing in for integrity + freshness + source states + replay + permission;
- `AVAILABLE=true` because any one source is positive;
- `UNAVAILABLE=true` because one source is unsupported;
- `STALE => REFRESH_REQUIRED` without exact refresh authority;
- `FRESH => CAUSAL_ALLOWED`;
- `REPLAY_VERIFIED => CAUSAL_ALLOWED`;
- `VALID => EMPIRICALLY_SUPPORTED`;
- `VALID_EMPTY => ZERO_PROBABILITY_ACTOR_STATE`;
- `NONCOMPARABLE => NEGATIVE`;
- `UNKNOWN => FALSE/ZERO/NEUTRAL`;
- scalar quality/readiness/fidelity scores used as state precedence.

## Determinism

Given the same exact wrapper bytes, PSEPF/content bindings, lifecycle authority, refresh authority, effective-time basis and replay bindings, lifecycle classification MUST be identical. Wall clock, filesystem/database order, network state, mutable latest, cache state, randomness, model judgment and display labels are forbidden semantic inputs.
