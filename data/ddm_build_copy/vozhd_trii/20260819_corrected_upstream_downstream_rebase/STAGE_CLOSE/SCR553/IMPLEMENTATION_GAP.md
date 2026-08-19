# SCR553 IMPLEMENTATION GAP

**Baseline inspected:** `baa257cb901ad8e5dc4d89faf2d81ea6f442ff8d`  
**Status:** `MATERIAL_IMPLEMENTATION_CONFORMANCE_GAPS__NO_ARCHITECTURE_REOPEN`  
**Production modification under SCR553:** `FORBIDDEN / NOT PERFORMED`

The local semantic contract is closed. Current V553 code is evidence of prior deliberate architecture, but it is not yet a conforming implementation of the corrected SCR553 contract.

## Gap ledger

### IG-553-01 — no native corrected `StructuralEmpiricalAdmission` ingress

`ddm_v553_canonical_harmonization.py` is still a V552J-facing trust/adapter surface and its required columns/manifest checks are tied to V552/V552J producer artifacts.

The corrected contract requires V553 semantic intake to begin from exact `StructuralEmpiricalAdmission` refs and to preserve admission identity, admission rule id/version/hash, source universe, exact EmpiricalFact/QuerySpec lineage, target structural proposition, temporal scope, support/uncertainty, negative authority, and replay closure.

**Conformance requirement:** implement an admission-native adapter. Legacy parity adapters may only feed it after exact StructuralEmpiricalAdmission authority is established; they may not recreate admission inside V553 from similarly named row fields.

### IG-553-02 — hidden `latest` repository discovery remains in current execution

`ddm_v553_temporal_pressure.py` imports `latest_run_root_for_wave` and defines `_resolve_latest_v552j_root`, which can discover repository state rather than consume only an exact immutable/hash-bound input ref.

That behavior is incompatible with SCR553 semantic selection.

**Conformance requirement:** semantic compilation must receive exact participant/source/authority refs. A convenience discovery helper may exist only outside semantic identity and must resolve to an explicitly chosen exact hash-bound object before V553 evaluation; it may never silently choose `latest`.

### IG-553-03 — temporal identity code is still survey-run identity normalization, not the closed generic key contract

At the commanded base, `ddm_v553_temporal_identity.py` chiefly normalizes one survey family, one country, wave labels, and calendar-year anchors. That is useful legacy evidence, but it is not the corrected generic content-addressed `TEMPORAL_KEY` contract over `StructuralEmpiricalAdmission`.

**Conformance requirement:** implement the exact `TEMPORAL_KEY` identity law from `EXACT_CONTRACT.*`, including source-universe/admission refs, governed temporal scope, rule authority, derivation refs, and deterministic SHA-256 identity.

### IG-553-04 — current schema surface is a legacy artifact/report schema, not the exact four-family semantic schema

The exact-base `ddm_v553_schema.py` exposes many pandas artifact schemas such as pressure fields, harmonization ledgers, interpolation manifests, readiness reports, audits, and handoff tables. The accepted stage law, now frozen by SCR553, recognizes exactly four semantic families.

The presence of a historical artifact table does not make it a semantic family or authority.

**Conformance requirement:** introduce explicit four-family semantic object validation/serialization and classify any retained report/ledger/projection as secondary, audit, compatibility, or implementation material. Secondary artifacts may not become semantic authority.

### IG-553-05 — current execution carries interpolation/secondary projection machinery without SCR553's explicit-use gate

Current code/schema includes interpolation functions/indices and country-year secondary projection machinery. Interpolation is not categorically forbidden, but it is never a default or nearest-time repair.

**Conformance requirement:** any interpolation/derived interval must be requested by an exact governed use, name exact participants and rule authority, and produce deterministic V553-owned semantics. Absent that authority, nearest-year or gap filling is forbidden and must fail closed.

### IG-553-06 — current code contains wall-clock/report metadata and readiness/probe scores

Current execution imports timestamp/provenance helpers and writes `created_at`/readiness/probe-style fields across many artifacts. Accepted V553 law already says readiness/probe/harmonization scores are nonsemantic.

**Conformance requirement:** wall-clock/session/filesystem state and readiness/probe scores must be excluded from semantic object identity, routing, comparability, and positive structural meaning. They may remain audit/operational metadata only.

### IG-553-07 — source/comparability authority remains entangled with legacy producer surface

The old implementation has comparability and harmonization fields, but the corrected contract requires a sharper separation:

```text
V553 temporal operation authority
!=
source-universe equivalence
!=
measure compatibility
!=
estimand compatibility
!=
respondent linkage
!=
pooling/composition authority
```

**Conformance requirement:** every compatibility-sensitive operation must consume explicit operation-specific prerequisite refs and fail closed on missing/unknown state. No shared columns, common source family, same year, canonical label, readiness, or provenance reachability can substitute.

### IG-553-08 — later-use demand needs a first-class request identity

Historical pipeline shape can encourage a once-per-run/once-per-wave temporalization classification. SCR553 requires every decision to bind the exact governed downstream use and rule.

**Conformance requirement:** implement `V553TemporalizationRequest` or an exactly equivalent control contract so the same admission can produce `V553_NOT_REQUIRED_FOR_THIS_USE` for U1 and later legitimately invoke V553 for U2 without mutating the admission.

### IG-553-09 — exact typed limit model must be enforced end to end

Historical limit/blocker/audit surfaces are evidence, but downstream code must distinguish semantic `TEMPORAL_LIMIT` from operational logging and preserve it by exact ref.

**Conformance requirement:** implement canonical limit states/reasons, ensure `OBSERVED_ZERO` is not collapsed into missingness, and ensure V554/V557/V558 consumers cannot interpret missing positive output as positive absence.

### IG-553-10 — deterministic four-family replay must be proven

Current artifact determinism and manifests are useful precedent, but SCR553 requires semantic replay at the exact request/ref/authority level.

**Conformance requirement:** canonical serialization + SHA-256 semantic identity, exact dependency closure, no wall-clock/session/random/latest inputs, and hostile replay fixtures from `HOSTILE_TEST_ORACLE.md`.

## Not a broad contradiction

Every gap above is a migration/conformance gap under an already-closed semantic ceiling. None requires:

- universal V553 transit;
- a new broad semantic owner;
- source-equivalence authority inside V553;
- D15 reopening;
- source/artifact retirement;
- production implementation during SCR553.

Therefore the proper classification is:

`IMPLEMENTATION_CONFORMANCE_FAILURE / DEBT__LOCAL_CONTRACT_CLOSED`

not `BROAD_TOPOLOGY_CONTRADICTION_FOUND`.
