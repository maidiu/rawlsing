# OBL058 — CAUSAL_USE_PERMISSION — INDEPENDENT HOSTILE REVIEW R1 — RETURN

## Terminal

`FAIL__OBL058_CAUSAL_USE_PERMISSION_INDEPENDENT_HOSTILE_REVIEW__BLOCKING_FALSE_POSITIVE_SOURCE_AUTHENTICITY_AND_FIXTURE_BOUNDARY_FAILURES`

State after terminal: `CLOSURE_ONLY`.

This FAIL means the frozen candidate did not survive the commissioned fresh distinct independent hostile review. It is **not lawful for SUB-VOZHD E adoption adjudication or HQ adoption preparation in its frozen form**.

This worker does not repair the frozen candidate, adopt OBL058, create any project-current positive permission, execute OBL055, or authorize OBL061.

## Exact identities

- repository: `maidiu/rawlsing`
- worker branch: `agent/rabochii-subv-e-obl058-causal-use-permission-hostile-r1`
- exact commission / working-ancestry start: `86a16516cf6647a6de0fff4fe53cf36f8bfa3a06`
- frozen semantic candidate: `24496c37d07841b05d876c9f14cc8aa8066592e3`
- authority: `OBL058_CAUSAL_USE_PERMISSION_SOURCE_AUTHORITY_R1@1.0.0`
- independent attack-matrix freeze: `6db2efabb7532f623ff1c396cbb58d20fb1596e4`
- fresh hostile primary-test commit: `95d4554aa9a9ca6b06f71fbd5c9f14a62d12fa56`
- governed wrapper commit: `9b00318bd176716f3678ecd461d46a2d127164d1`
- governed evidence execution: `655cd385c9e0e60b0f514484e7a70066d5cd7cd2`
- evidence artifact commit: `830e3ecdd143f49b76b365ac8b11ac456dd126fa`
- execution-only PR: `#270`, closed unmerged
- PR synthetic merge identity: `80b09cbaeef4b794614c6d6bf937050c42269e53`
- final worker tip: reported out of band after this return commit because a file cannot contain its own immutable commit SHA without changing that SHA.

## Independent holding

The frozen candidate correctly states that a positive `CAUSAL_USE_PERMISSION` must come from an explicit source-owned basis bound to the exact tuple:

`(actor_id, world_id, subject_id, time_id, transition_id)`.

Its executable contract does not actually prove that condition.

A positive receipt can be created or forged using only caller-controlled/publicly reproducible material:

- `explicit_source_permission=True` at issuance;
- the literal basis kind `EXPLICIT_SOURCE_OWNED_CAUSAL_USE_PERMISSION`;
- an arbitrary nonempty `basis_id`;
- public authority/schema constants;
- public canonical SHA-256 digests.

The validator verifies consistency of those public fields but does not verify that a competent source owner issued the receipt, that the claimed source-owned basis exists, or that the basis is bound to the exact tuple. Therefore receipt integrity is not source authenticity.

The same defect allows a source-shaped `DENY` to be rewritten as `PERMIT` and publicly rehashed, and allows a surrogate-basis denial to be relabeled to the magic source-basis literal, rewritten to `PERMIT`, publicly rehashed, and accepted.

The candidate's `NONCURRENT_SYNTHETIC` guard is also label-only. `ExactScope.validate()` requires nonempty strings but does not bind those identifiers to a noncurrent-synthetic namespace or evidence class. A project-current-shaped scope, including the exact current first-canary subject identifier, can therefore be issued a synthetic-labeled `PERMIT` in the candidate court surface. This does not itself create project-current runtime state, but it defeats the candidate's claimed enforceable separation between noncurrent synthetic issuance and project-current identity.

## Blocking findings

### B1 — source-owner authenticity is not proven

`BLOCKING_FALSE_POSITIVE`

A handcrafted receipt never emitted by the source owner validates as `PERMIT` when the attacker supplies the public authority/schema strings, magic basis-kind literal, arbitrary basis ID, exact scope, and recomputed public hashes.

The digest proves only self-consistency of attacker-supplied fields. It does not prove issuer competence or source ownership.

### B2 — source-owned basis existence and exact-scope binding are not proven

`BLOCKING_FALSE_POSITIVE`

The issuer trusts the caller-supplied boolean `explicit_source_permission` and an unverified basis ID. The same attacker-chosen basis ID can be reused to mint positive receipts across different actor, world, subject, time, and transition scopes.

This directly contradicts the frozen semantic contract's requirement that the explicit source-owned permission basis be bound to the exact tuple.

### B3 — decision and basis truth can be rewritten under public rehash

`BLOCKING_FALSE_POSITIVE`

A valid `DENY` using the magic source basis can be changed to `PERMIT`, and a surrogate denial can be relabeled as the magic source basis and changed to `PERMIT`; recomputing the public receipt digest makes both validate.

Therefore the receipt digest is not an authority seal.

### B4 — fixture classification is not bound to scope identity

`BLOCKING_BOUNDARY_FAILURE`

The explicit string `fixture_class == PROJECT_CURRENT` is rejected, but current-shaped identifiers are accepted when the caller leaves the fixture label as `NONCURRENT_SYNTHETIC`.

The claimed no-current issuance boundary is therefore not enforced by the scope/receipt contract itself.

### B5 — the positive receipt carries no independently verifiable source-permission proof

`BLOCKING_PROOF_GAP`

The input assertion `explicit_source_permission` disappears from the receipt, and no competent basis receipt, authority membership, signature/seal, source-evidence digest, or other independently verifiable source-owned proof replaces it.

A later validator cannot distinguish a genuine source-owned positive decision from an attacker-shaped one that satisfies the public field grammar.

## Governed hostile evidence

- workflow: `Rabochii Governed Bounded Court`
- run: `34181741051`
- job: `101922045945`
- Python: `3.12.14` / `CPython`
- protocol self-test: `20 passed in 0.11s`
- court-spec validation: `PASS`
- hostile court: `20 passed in 0.08s`
- receipt result: `PASS`
- receipt exit code: `0`
- semantic candidate: `24496c37d07841b05d876c9f14cc8aa8066592e3`
- exact evidence execution: `655cd385c9e0e60b0f514484e7a70066d5cd7cd2`
- artifact ID: `10039136894`
- artifact ZIP SHA-256: `440cab1bc35097cec684288b3b75eaf484ca1d65020dab3eaa83fa4819f6189e`

The green hostile court proves the independently authored attack assertions executed as designed. Because H01-H16 assert reproducible blocking false-positive behavior, the separate semantic adjudication is FAIL.

## Preserved controls

The review does not dispute that the frozen candidate still rejects:

- a directly supplied `PROJECT_CURRENT` fixture label;
- wrong authority;
- wrong expected scope;
- known surrogate basis kinds during ordinary unmodified issuance;
- malformed/extra receipt keys under the existing grammar.

Those controls are insufficient because the blocking attacks remain inside the publicly reproducible accepted grammar.

## Smallest lawful blocker / required next action

`BLOCKER__OBL058_REQUIRES_REPAIRED_SOURCE_AUTHENTICITY_EXACT_BASIS_BINDING_AND_NONCURRENT_FIXTURE_BINDING_BEFORE_REVIEW_CAN_PASS`

The hostile reviewer does not prescribe a new architecture or modify the frozen candidate. At minimum, a repaired candidate must make `PERMIT` independently verifiable as a decision of the competent OBL058 source owner and bind the supporting source-owned basis to the exact actor/world/subject/time/transition tuple. It must also make the noncurrent-synthetic issuance boundary non-masqueradable rather than trusting only a caller-selected fixture label.

A repaired semantic candidate is a new review target. It requires a new governed bounded court and a fresh distinct independent hostile review; this FAIL must not be relabeled or reused as a PASS for a changed candidate.

Until then:

- OBL058 is lane-blocked;
- SUB-VOZHD E must not prepare an OBL058 HQ adoption packet from frozen candidate `24496c37d07841b05d876c9f14cc8aa8066592e3`;
- OBL061 remains blocked by the campaign gate;
- no current-positive causal-use permission is authorized.

## No-current-positive / non-action attestation

`PROJECT_CURRENT_POSITIVE_CAUSAL_USE_PERMISSION_CREATED = NO`

`PROJECT_CURRENT_OBL056_POSITIVE_ENTRY_INSTALLED = NO`

`OBL055_EXECUTED = NO`

`PROJECT_CURRENT_OEE_REALIZED = NO`

`ENCOUNTER_CREATED = NO`

`HQ_ADOPTION_CLAIMED = NO`

No central, PRE-MAIN, main, SUB-VOZHD integration branch, or sibling lane was moved by this hostile review.

## Return to SUB-VOZHD E

Frozen candidate `24496c37d07841b05d876c9f14cc8aa8066592e3` is returned as **not lawful for adoption consideration in its present form**.

Exact terminal:

`FAIL__OBL058_CAUSAL_USE_PERMISSION_INDEPENDENT_HOSTILE_REVIEW__BLOCKING_FALSE_POSITIVE_SOURCE_AUTHENTICITY_AND_FIXTURE_BOUNDARY_FAILURES`
