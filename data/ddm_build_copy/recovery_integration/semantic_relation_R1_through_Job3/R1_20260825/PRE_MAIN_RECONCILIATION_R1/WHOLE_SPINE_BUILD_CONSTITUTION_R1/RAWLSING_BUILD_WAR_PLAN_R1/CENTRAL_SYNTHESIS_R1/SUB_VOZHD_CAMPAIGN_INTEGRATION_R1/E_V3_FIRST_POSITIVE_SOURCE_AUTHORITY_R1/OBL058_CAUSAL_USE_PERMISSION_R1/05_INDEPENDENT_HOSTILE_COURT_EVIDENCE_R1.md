# OBL058 — CAUSAL_USE_PERMISSION — INDEPENDENT HOSTILE COURT EVIDENCE R1

## Exact identities

- commission / working-ancestry start: `86a16516cf6647a6de0fff4fe53cf36f8bfa3a06`
- frozen semantic candidate: `24496c37d07841b05d876c9f14cc8aa8066592e3`
- authority: `OBL058_CAUSAL_USE_PERMISSION_SOURCE_AUTHORITY_R1@1.0.0`
- independent attack-matrix freeze: `6db2efabb7532f623ff1c396cbb58d20fb1596e4`
- fresh hostile primary-test commit: `95d4554aa9a9ca6b06f71fbd5c9f14a62d12fa56`
- governed wrapper commit: `9b00318bd176716f3678ecd461d46a2d127164d1`
- governed evidence execution / exact checkout: `655cd385c9e0e60b0f514484e7a70066d5cd7cd2`
- PR synthetic merge identity: `80b09cbaeef4b794614c6d6bf937050c42269e53`

The semantic candidate remained frozen. The hostile reviewer changed only review/court artifacts and the transient root court specification needed to execute the review. After evidence capture the root court specification was restored byte-for-byte to its commissioning-start source-court blob `47813bc4b9657f20608f834c38162b67850fa052` at commit `183c67ecb8d47ef42ee135fe2be9555a70e9a023`.

## Independent hostile surface

Attack matrix:

`04_INDEPENDENT_HOSTILE_ATTACK_MATRIX_R1.json`

Attack-family count:

`20`

Fresh lane-local hostile test:

`test_independent_hostile_review.py`

Governed wrapper:

`rawlsing_next/tests/test_subv_e_obl058_causal_use_permission_hostile_court.py`

The hostile assertions deliberately encode reproducible adversarial constructions. For blocking families H01-H16, a green test means the frozen candidate accepted the hostile construction as predicted. Therefore a green governed test program is evidence of the false-positive paths; candidate adjudication is a separate step and is not implied by the court receipt's `PASS` result.

## Governed hostile court

Workflow:

`Rabochii Governed Bounded Court`

Execution-only PR:

`#270 — EXECUTION-ONLY COURT — DO NOT MERGE — OBL058 independent hostile review`

PR disposition after evidence capture:

`CLOSED_UNMERGED`

Exact governed evidence:

- run: `34181741051`
- job: `101922045945`
- exact checkout / evidence execution: `655cd385c9e0e60b0f514484e7a70066d5cd7cd2`
- semantic candidate declared by court: `24496c37d07841b05d876c9f14cc8aa8066592e3`
- PR synthetic merge identity: `80b09cbaeef4b794614c6d6bf937050c42269e53`
- Python: `3.12.14` / `CPython`
- determinism: `EXACT`
- protocol self-test: `20 passed in 0.11s`
- court-spec validation: `PASS`
- governed hostile court: `20 passed in 0.08s`
- court receipt schema: `RABOCHII_BOUNDED_COURT_RECEIPT@1.0.0`
- court receipt result: `PASS`
- court receipt exit code: `0`
- court receipt elapsed seconds: `0.289773`
- court-spec SHA-256: `05888c0d32b7a8206d751f495c651fe4f7e8d5f41ce7967dcabbf71ec199e68e`
- artifact ID: `10039136894`
- artifact name: `rabochii-court-receipt-34181741051`
- artifact size: `610` bytes
- artifact ZIP SHA-256: `440cab1bc35097cec684288b3b75eaf484ca1d65020dab3eaa83fa4819f6189e`

The first execution-only attempt, run `34181682043`, stopped at court-spec validation because the governed protocol requires tests under `rawlsing_next/tests/*.py`. Protocol self-tests were green, the hostile court did not execute, and no receipt was produced. The allowed-path wrapper repaired only that court-protocol wiring; it did not alter the frozen semantic candidate or the attack matrix. The exact governed evidence above is run `34181741051`.

## Reproduced blocking false-positive classes

The green hostile execution reproduced all of the following against the frozen candidate:

1. caller-supplied `explicit_source_permission=True` plus the magic source-basis literal and an attacker-chosen nonempty basis ID yields `PERMIT`;
2. a handcrafted receipt never issued by the source owner validates as `PERMIT` after computing the public receipt digest;
3. a legitimate exact-scope `DENY` using the magic basis kind can be changed to `PERMIT`, publicly rehashed, and then validate;
4. a surrogate-basis `DENY` can be relabeled to the magic basis kind, changed to `PERMIT`, publicly rehashed, and then validate;
5. arbitrary and whitespace-only basis identifiers can support positive issuance;
6. a forged positive receipt can carry a non-string JSON-serializable `basis_id` and still validate;
7. the same unverified basis ID can be reused to mint independent `PERMIT` receipts across different actor, world, subject, time, and transition scopes;
8. project-current-shaped scope identifiers can pass the `NONCURRENT_SYNTHETIC` fixture guard because fixture class is only a caller-controlled label and scope identity is not bound to that classification;
9. the exact current first-canary subject identifier can be embedded in such a synthetic-labeled positive receipt;
10. possession of public authority/schema strings plus public SHA-256 recomputation is sufficient to impersonate issuance;
11. the positive receipt drops the `explicit_source_permission` assertion and contains no independently verifiable proof that the claimed source-owned permission basis existed and was bound to the exact tuple.

## Controls preserved

The court also confirms that several existing local checks still work:

- wrong authority is rejected;
- known surrogate basis kinds deny at ordinary issuance;
- wrong expected scope is rejected;
- an explicit `fixture_class == PROJECT_CURRENT` issuance request is rejected.

These controls do not cure the blocking false-positive paths because the hostile constructions satisfy or rewrite the publicly recomputable fields that those controls inspect.

## No-current-positive / no-runtime attestation

This hostile review created no project-current permission instance. It did not create an actor, perform an ADP-008 transition, admit an ADP-019 event, install a positive OBL056 entry, execute OBL055, realize OEE, create ENCOUNTER, or claim HQ adoption.

The current/synthetic masquerade tests are noncurrent hostile fixtures proving that the frozen candidate does not cryptographically/semantically bind its fixture label to scope identity; they are not project-current runtime execution.
