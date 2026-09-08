# OBL058 — CAUSAL_USE_PERMISSION — R2 BOUNDED REPAIR — RETURN TO SUB-VOZHD E

## Terminal

`PASS__OBL058_R2_BOUNDED_REPAIR_GREEN__FROZEN_REPAIRED_CANDIDATE_AWAITS_FRESH_DISTINCT_INDEPENDENT_REVIEW`

State after terminal: `CLOSURE_ONLY`.

This PASS is strictly a producer-side bounded-repair court PASS. It is **not** an independent review PASS, SUB-VOZHD E adjudication, or HQ adoption decision.

## Exact identities

- repository: `maidiu/rawlsing`
- worker branch: `agent/rabochii-subv-e-obl058-causal-use-permission-bounded-repair-r2`
- exact starting HEAD: `1ab64593c8892c1d48d6a38e45c7d847c1947979`
- frozen repaired semantic candidate: `f735c85393280557284b3a309cafc0847fb48aec`
- repaired authority: `OBL058_CAUSAL_USE_PERMISSION_SOURCE_AUTHORITY_R1@1.1.0`
- repaired receipt schema: `OBL058_CAUSAL_USE_PERMISSION_RECEIPT@2.0.0`
- repair court test commit: `59a8aae6fbf372907f94fdde7fcb8eae40a00a54`
- approved-wrapper commit: `69552ed486ac3797c927e834f3c76fdd2d31f4d2`
- governed court binding / evidence execution: `4f8b37358ef721a6a259b7795f2483231aea0f27`
- governed evidence artifact commit: `77631a0d3920effa2e766c68a05cd045b91e87d1`
- execution-only PR: `#275`, closed unmerged
- PR synthetic merge identity: `dbec3355fe3593479fa2b6ce352ea84b1d7e8ba5`
- final worker tip: reported out of band after this return commit because a file cannot contain its own immutable commit SHA without changing that SHA.

## Repair holding

R2 repairs the five defects returned by the prior independent review without widening the OBL058 lane.

### 1. Source-owner provenance

The validator no longer treats any caller-created Mapping with matching public fields and hashes as a source-authority receipt. Accepted receipts must carry source-issued provenance from the bounded authority instance.

### 2. Source-owned basis existence and exact binding

The public issuance contract no longer accepts `explicit_source_permission` or caller-selected `basis_kind`. Positive issuance is derived only from a frozen source-owned basis registry, and the registered positive basis is bound to one exact scope digest.

### 3. Decision/basis rewriting under public rehash

The public digest is treated only as content integrity. It is no longer sufficient to establish authority provenance. Issued receipt mappings are read-only, and copied/reconstructed mappings fail source-issued provenance validation even if their public digest is recomputed.

### 4. Noncurrent-synthetic fixture binding

Every exact scope field must use its field-specific `NONCURRENT_SYNTHETIC` namespace with a nonempty suffix. Project-current-shaped actor/world/subject/time/transition identifiers, including the exact current first-canary subject identifier, fail closed on this candidate surface.

### 5. Positive basis proof

Positive receipts carry and validate both `basis_scope_digest` and `basis_proof_digest` against the frozen source-owned basis record. The discarded caller assertion from R1 is no longer part of the issuance contract.

## Governed court

- workflow: `Rabochii Governed Bounded Court`
- run: `34189967948`
- job: `101945838419`
- Python: `3.12.14` / `CPython`
- protocol self-tests: `20 passed in 0.11s`
- court-spec validation: `PASS`
- bounded repair court: `26 passed in 0.08s`
- receipt result: `PASS`
- receipt exit code: `0`
- semantic candidate: `f735c85393280557284b3a309cafc0847fb48aec`
- evidence execution: `4f8b37358ef721a6a259b7795f2483231aea0f27`
- artifact ID: `10041842927`
- artifact ZIP SHA-256: `9326196e16ed503fdcdae6e501a03d3be706d5f5f05c517e4351e0791d969f03`

A preliminary non-evidence run failed only at court-spec path validation before the repair tests executed; the candidate was unchanged. The approved wrapper corrected that protocol plumbing, and the subsequent governed execution above is the evidence run.

## No self-review

`FRESH_DISTINCT_INDEPENDENT_REVIEW_PERFORMED_BY_THIS_WORKER = NO`

`INDEPENDENT_REVIEW_COUNT_FOR_REPAIRED_CANDIDATE = 0`

The repaired candidate must now be handed to a different worker for exactly one fresh distinct independent review. This producer court cannot satisfy or substitute for that requirement.

## No-current-positive / non-action attestation

`PROJECT_CURRENT_POSITIVE_CAUSAL_USE_PERMISSION_CREATED = NO`

`PROJECT_CURRENT_OBL056_POSITIVE_ENTRY_INSTALLED = NO`

`OBL055_EXECUTED = NO`

`PROJECT_CURRENT_OEE_REALIZED = NO`

`ENCOUNTER_CREATED = NO`

`HQ_ADOPTION_CLAIMED = NO`

No central, PRE-MAIN, main, SUB-VOZHD integration, or sibling-lane branch was moved by this repair worker. PR `#275` was closed unmerged after evidence capture.

## Return

The R2 repaired candidate is returned to SUB-VOZHD E as **producer-court green but not yet independently reviewed**.

Exact terminal:

`PASS__OBL058_R2_BOUNDED_REPAIR_GREEN__FROZEN_REPAIRED_CANDIDATE_AWAITS_FRESH_DISTINCT_INDEPENDENT_REVIEW`
