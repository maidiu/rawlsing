# GT3/GT4 OBL056 A1 — ADP-010 INPUT AUTHORITY ACCEPTANCE BINDING AUTHORITY R1 — RETURN

## Terminal

`PASS__GT34_OBL056_ADP010_INPUT_AUTHORITY_ACCEPTANCE_BINDING_CANDIDATE_GREEN__NO_ADOPTION`

Candidate only. OBL056 is **not adopted** by this worker.

## Exact ancestry and proof identities

- exact working-ancestry start: `ee71ea855e722742f97309de36294f55c35623b2`
- frozen semantic candidate: `966aea1a42b30840670f4b69f779999bfd4a2307`
- governed evidence execution SHA: `f53df8dc7534e41792e2920ff7c8b65f293aa1b2`
- PR synthetic merge SHA: `0788e4dfbf56272d274bec3691b2531e2599ff8a`
- final worker tip: reported out of band after this return is committed, because this file cannot contain its own commit SHA without changing that SHA.

The semantic candidate, evidence execution SHA, PR synthetic merge SHA, and final worker tip are distinct identities and are not substituted for one another.

## Holding

The frozen terminal claim is proven.

A narrow content-addressed candidate authority/registry/receipt contract now exists that can prove that one exact already-existing authority identity is separately accepted for one exact ADP-010 input role and exact consumer/transition/use/family/subject/object scope.

The candidate owns **acceptance binding only**. It does not create the underlying semantic proposition.

A caller cannot obtain positive competence merely by choosing an authority ID/version/content hash/currentness and hashing those fields. Positive validation requires an exact separately issued receipt whose body is bound to an exact immutable registry entry and exact governing evidence material.

## Candidate identity

Authority / registry identity:

`GT34_ADP010_INPUT_AUTHORITY_ACCEPTANCE_REGISTRY@1.0.0`

Exact authority content hash:

`41b79e7f622f3c9eb0d6df649254c812fcb769db45cf6e47a808a95eebe2a50f`

Exact registry content hash:

`9ef38509ad5798c038bbcfa1b3a6e343df5a7c4f2a1ed4fd2af33f31f19e3a9e`

Receipt schema:

`GT34_ADP010_INPUT_AUTHORITY_ACCEPTANCE_RECEIPT@1.0.0`

Exact consumer:

`V3_OPPORTUNITY_ENCOUNTER_EXPOSURE_REALIZATION_RULE@1.0.0`

Status:

`CANDIDATE_NOT_ADOPTED`

## Exact roles

The candidate recognizes exactly these role atoms:

1. `CAUSAL_USE_PERMISSION`
2. `POSITIVE_APPLICABILITY`
3. `CONTACT_OCCURRENCE_WITNESS`
4. `CONTACT_WITNESS_INDEPENDENCE`

No role implies another role. A receipt for one role cannot satisfy another role.

## Acceptance binding

Every positive receipt binds:

- acceptance authority ID/version/content hash;
- registry ID/version/content hash;
- exact immutable registry-entry ref/hash;
- receipt schema/version;
- exact role;
- exact accepted authority ID/version/content hash;
- accepted authority owner/jurisdiction ref/hash;
- exact source acceptance/adoption/current-selection evidence ref/hash;
- decision state;
- exact ADP-010 consumer;
- exact transition/use scope;
- exact family scope;
- exact subject scope;
- exact object scope;
- negative/limit refs;
- currentness;
- immutable provenance;
- deterministic receipt identity/hash.

Exact validation is registry-membership based. There is no latest/default/fuzzy/fallback selector and no positive derivation from caller-selected authority strings.

## Current / synthetic boundary

The candidate has **zero current positive registry entries**.

That is intentional and lawful. No project-current causal-use, positive-applicability, contact-occurrence, or contact-independence semantic authority was invented.

Mechanical positive fixtures are issued only under a distinct synthetic issuer/registry with currentness:

`NONCURRENT_SYNTHETIC_TEST_ONLY`

Synthetic receipts cannot validate as `CURRENT_ACCEPTED` and cannot masquerade as the candidate/current registry.

A future current positive entry therefore requires a separately established exact competent source authority plus governing acceptance/adoption/current-selection evidence. This worker does not perform that adoption.

## Contact-independence separation

For the contact path the candidate mechanically requires:

- occurrence acceptance role = `CONTACT_OCCURRENCE_WITNESS`;
- independence acceptance role = `CONTACT_WITNESS_INDEPENDENCE`;
- distinct accepted authority identities;
- distinct acceptance receipt identities/hashes.

One acceptance receipt cannot be reused for both roles, and one accepted authority cannot occupy both roles under this candidate.

This is identity/acceptance separation only. It does not assert that contact occurred and does not create an independence fact.

## Authority ceiling

The candidate explicitly creates none of the following:

- subject identity/classification;
- causal-use semantic truth;
- applicability semantic truth;
- contact occurrence;
- contact independence fact;
- encounter;
- exposure;
- external-event admission;
- comparator authority;
- PSEPF authority;
- metabolism authority;
- CAN-008 authority;
- V2 authority;
- positive-V3 actor mutation authority;
- generic project-wide authority admission.

Underlying semantic truth remains owned by the competent source authorities.

## Exact candidate files

Implementation:

`rawlsing_next/gt34_adp010_input_authority_acceptance.py`

Frozen semantic-candidate blob:

`62b9cc43b0acf7cecc4647215929ef12ada955f2`

Focused tests:

`rawlsing_next/tests/test_gt34_obl056_adp010_input_authority_acceptance.py`

Frozen test blob:

`a5144ff943497d6636810fd6a593d7d0e76e222d`

Candidate registry artifact:

`01_CANDIDATE_AUTHORITY_REGISTRY.json`

Frozen blob:

`6435b489a37c16f21dfb1ded63bcbd825e4cb65e`

Receipt schema / synthetic example artifact:

`02_RECEIPT_SCHEMA_AND_SYNTHETIC_EXAMPLE.json`

Frozen blob:

`68c77894d320ac91826efbee4c812bc468cb2dd2`

Governed evidence:

`03_GOVERNED_EVIDENCE.json`

## Governed bounded court

Existing repository court:

`Rabochii Governed Bounded Court`

- run: `34059241185`
- job: `101556671724`
- evidence execution SHA: `f53df8dc7534e41792e2920ff7c8b65f293aa1b2`
- semantic candidate declared by spec/receipt: `966aea1a42b30840670f4b69f779999bfd4a2307`
- PR synthetic merge SHA: `0788e4dfbf56272d274bec3691b2531e2599ff8a`
- determinism mode: `EXACT`
- Python: `3.12.14` / CPython
- protocol self-test: `20 passed in 0.10s`
- bounded-court spec validation: `PASS`
- focused candidate court: `21 passed in 0.12s`
- court receipt result: `PASS`
- court receipt exit code: `0`
- court spec SHA-256: `7296f077b0cdb1c9f434b0b4fc74b2d99b59527c4bf4f2e3b4514f9a566c78f2`
- artifact ID: `9996930772`
- artifact name: `rabochii-court-receipt-34059241185`
- artifact ZIP SHA-256: `4df1ce3c4f78108fc4c1a5770e45af3ff02f992efbfe00b28833428ad53b7c47`

The execution-only draft PR was `#233`. It was closed unmerged after evidence capture. It did not adopt or integrate the candidate.

## Required hostile controls

Governed focused tests prove:

1. arbitrary caller authority cannot self-issue acceptance;
2. exact separately issued positive synthetic receipt validates in noncurrent-test mode;
3. authority ID mutation fails;
4. authority version mutation fails;
5. authority content-hash mutation fails;
6. role mutation fails;
7. consumer mutation fails;
8. transition/use-scope mutation fails;
9. source acceptance/adoption/current-selection evidence mutation fails;
10. currentness mutation fails;
11. receipt content/hash mismatch fails;
12. absent entry/receipt fails closed;
13. one role's receipt cannot satisfy another;
14. contact occurrence and independence cannot use the same accepted authority;
15. contact occurrence and independence cannot use the same receipt;
16. synthetic receipt cannot masquerade as current;
17. exact replay/idempotence holds;
18. acceptance emits no underlying semantic proposition;
19. no downstream authority widening is created.

## Scope / mutation audit

Exact start-to-semantic-candidate comparison showed four additions only:

- the candidate acceptance module;
- the focused hostile test file;
- the candidate registry artifact;
- the receipt-schema/synthetic-example artifact.

`rawlsing_next/v3_adp010_oee_executor_authenticated.py` was **not modified**.

This worker did not:

- repair W2;
- execute current OEE;
- adopt OBL056;
- invent project-current semantic authorities;
- move central;
- move PRE-MAIN;
- move main;
- move any SUB-VOZHD branch.

## Independent-review readiness

The candidate is mechanically green and bounded at the commissioned authority grain.

It is ready for the separately commissioned independent hostile review required before any HQ adoption decision.

## Terminal

`PASS__GT34_OBL056_ADP010_INPUT_AUTHORITY_ACCEPTANCE_BINDING_CANDIDATE_GREEN__NO_ADOPTION`
