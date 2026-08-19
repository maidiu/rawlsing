# SV3A — Refresh / Requery Interaction Contract

## Jurisdiction

SV3A freezes what `V3EmpiricalPossibilityInput` must **carry** so refresh/requery can later be governed exactly. It does not create refresh trigger, scheduler, source-query, regeneration or metabolism authority.

The wrapper is a historical immutable boundary object. It is not a live subscription.

## Required refresh-facing metadata

The wrapper MUST contain `refresh_requirement_state` and enough exact authority/basis information to distinguish whether the state is positively governed, unbound, unknown or corrupt.

When an external accepted refresh/requery authority exists, the wrapper MAY carry:

- `refresh_authority_id`;
- `refresh_authority_version`;
- `refresh_authority_hash`;
- exact `refresh_basis_refs`;
- exact `refresh_reason_code` supplied by that authority;
- an authority-produced `next_refresh_boundary_ref` or exact boundary value plus its derivation authority;
- an authority-produced `requery_request_ref`/hash;
- per-source refresh state/refs if source components have distinct refresh requirements.

When no exact authority is bound, the required state is `REFRESH_AUTHORITY_UNBOUND`. V3 intake must not manufacture a schedule or silently substitute a default policy.

## What does not authorize refresh

None of the following alone authorizes refresh or requery:

- wall-clock age;
- file mtime;
- wrapper creation time;
- presence of a newer file/build/branch;
- mutable `latest`;
- one source becoming unsupported;
- one source becoming positive;
- disagreement between sources;
- low support;
- a modal mass threshold;
- actor state change;
- `ResolvedStructuralContext` refresh metadata;
- runtime convenience or cache expiry;
- model/LLM judgment.

Any of these may be an input to a separately accepted authority if that authority explicitly says so. SV3A itself creates no such rule.

## Freshness versus refresh

`freshness_state` and `refresh_requirement_state` are separate.

Examples that must be representable:

- `FRESH + REFRESH_NOT_REQUIRED`;
- `FRESH + REFRESH_REQUIRED` because an exact non-age event rule requires regeneration;
- `STALE + REFRESH_REQUIRED`;
- `STALE + REFRESH_AUTHORITY_UNBOUND`;
- `FRESHNESS_UNKNOWN + REFRESH_REQUIREMENT_UNKNOWN`;
- valid wrapper + refresh binding integrity failure.

Neither axis decides causal read permission. SCRV3's final metabolism/read-permission contract owns what, if anything, a stale or refresh-required field may do before replacement.

## Requery request law

A requery request, if carried, MUST be an exact immutable reference to a request owned by the proper refresh/source-query authority. The wrapper does not create or mutate its contents.

A lawful request reference must bind whatever the governing requery authority requires to prevent accidental semantic drift, including exact source/universe/query/comparator/effective-time/position bindings where applicable.

No fuzzy source match, latest query spec, nearest cohort, current comparator, or implicit default may fill a missing request field.

## Replacement law

A completed refresh/requery follows:

1. external authority creates or authorizes the exact requery;
2. the lawful PSEPF producer produces a **new exact PSEPF root**;
3. V3 intake constructs and verifies a **new wrapper** under the same contract;
4. subject binding, source component manifest, lifecycle, replay and integrity are re-evaluated from exact new bindings;
5. the old PSEPF and wrapper remain immutable and replay-addressable.

Forbidden:

- update PSEPF bytes under the same content identity;
- mutate source-component states under the same wrapper identity;
- swap a `latest` root behind an existing wrapper;
- retain old wrapper ID while changing refresh authority, component manifest or exact root hash;
- silently treat refreshed PSEPF as the same empirical object.

## Cross-lane separation from SCR5578

V558/`ResolvedStructuralContext` may have its own deterministic refresh/context-change metadata under SCR5578 authority. That does not become PSEPF refresh authority merely because both arrive at V3.

The two lanes remain separately identified:

- PSEPF wrapper refresh/requery binding: empirical-possibility lane;
- `ResolvedStructuralContext` refresh/requery binding: structural repository/context lane.

SCRV3 may later define a stage-level coordination policy only under accepted authority. SV3A forbids inferring that one lane's refresh event automatically invalidates, refreshes, regenerates or causally authorizes the other.

## Replay requirements

For a historical wrapper, replay/audit must bind the exact historical PSEPF root, wrapper identity/hash, source component manifest, lifecycle authority/version/hash, refresh authority/version/hash if present, effective-time basis and replay bindings.

A later refresh must not retroactively change the historical wrapper's freshness classification basis or source states by replacing historical authority with current/latest authority.

`ReplayReceipt` remains audit-only. It can establish which historical inputs/authorities were used; it cannot grant causal permission or substitute current empirical content.
