# GT3/GT4 T3 — OBL055 S3 ADP-010 V3-P5 OEE EXECUTOR HOSTILE AUDIT R1

## Terminal

`FAIL__GT34_T3_OBL055_S3_ADP010_V3P5_EXECUTOR_AUTHENTICATION_AND_REPLAY_INTEGRITY_GAPS`

This is an independent hostile-review return. It is not an adoption and does not modify the S3 target candidate in place.

Terminal SHA is the final branch tip containing this return and is reported with the worker handoff.

## Exact execution boundary

- repository: `maidiu/rawlsing`
- branch: `agent/rabochii-gt34-t3-obl055-s3-adp010-executor-hostile-audit-r1`
- exact working-ancestry start: `d7c5f2270bdc2bdb78c347dd1c9b9c67205dd635`
- immutable instruction ref: `146eb938a568ae8b8c853b502860c29491956372`
- executed only: `WORKER T3 — OBL055 S3 ADP-010 V3-P5 OEE EXECUTOR HOSTILE AUDIT R1`
- target semantic candidate: `5bed04b83f0dc61e500da26130892e46ce9c86ff`
- target evidence execution: `c70808c993b7e236e5535a03e22fe89cc3759d1e`
- target governed court: run `34017875248`, job `101444831011`
- target module: `rawlsing_next/v3_adp010_oee_executor.py`
- target module blob: `cd6e978eea25384482ef2ab75547b8d33bcc4fb7`
- target test blob: `0d29a69e9f88beb72ebfb4ddb85bdb5c40fc74d5`
- target modified by T3: **NO**
- self-adoption: **NO**
- sibling T1/T2 in-flight conclusions consumed: **NO**
- PRE-MAIN moved: **NO**
- `main` moved: **NO**

Independent machine-readable evidence:

`01_HOSTILE_AUDIT_EVIDENCE.json`

Independent hostile probes:

`rawlsing_next/tests/test_gt34_t3_s3_adp010_oee_executor_hostile_audit.py`

## Accepted authorities independently checked

### ADP-010

- authority: `V3_OPPORTUNITY_ENCOUNTER_EXPOSURE_REALIZATION_RULE@1.0.0`
- registry: `V3_OEE_REALIZATION_RULE_REGISTRY@1.0.0`
- authority artifact blob: `0eac41d081b112255dcfc6dd42a6afab15a2928b`
- bounded rules under audit:
  - `OEE_CORE_AVAILABLE_BASIS_V1`
  - `OEE_CORE_OPPORTUNITY_FROM_EXPLICIT_BASIS_V1`
  - `OEE_CORE_ENCOUNTER_FROM_EXPLICIT_CONTACT_WITNESS_V1`

The accepted registry requires exact input authority signatures/use permissions, phase/applicability/runtime requirements, temporal scope, causal witnesses, candidate identity, stochastic policy, provenance/replay, and rule hash.

The accepted provenance minimum includes ADP-010 authority/registry/rule hashes, ADP-008 phase hash, parent OEE records, repository/resolver/structural/generated-input receipts where used, effective time/granularity, witness hashes, ledger anchor/index/hash, event/OEE hash, and reconstructible replay material.

### ADP-008

- authority: `V3_DEVELOPMENTAL_PHASE_RULE@1.1.0`
- artifact blob: `c6564c5c2793e9ed86ec0c5cecbcf84ff6f427d6`
- required lived-OEE base phase: `V3DP_DEVELOPMENT_ACTIVE`
- canonical state record: `V3DevelopmentalPhaseState`

ADP-008's replay/provenance contract requires exact phase-state/registry/rule provenance rather than a caller-supplied active-phase string alone.

### ADP-020

- authority: `ADP-020@1.0.0`
- artifact blob: `1f13dc7ccc69bda562613d6215acc996a9c092e4`
- S3 core-v1 disposition: `ZERO_DRAW`

T3 found no ambient RNG or hidden random identity input in S3. This part passes.

## Original S3 court verification

T3 independently re-read the recorded S3 Actions run.

Run:

`34017875248`

Job:

`101444831011`

Head/evidence execution SHA:

`c70808c993b7e236e5535a03e22fe89cc3759d1e`

Conclusion:

`success`

The original S3 bounded executor court genuinely passed its recorded 22 tests on that evidence execution SHA.

That fact is not in dispute.

The problem is that the original court does not cover several canonical authentication/replay invariants below.

## Independent T3 hostile court

T3 added eight independent hostile probes without changing S3.

Hostile-audit semantic candidate:

`266faab11a97e087e0a1356964f13d4d0468a0a2`

Exact hostile evidence execution SHA:

`8b339dd2232a316f4c70fc0806867e6460128c05`

Governed court:

- run: `34018914265`
- job: `101447751674`
- workflow conclusion: `success`
- protocol self-test: `20 passed`
- combined S3 + T3 bounded court: `30 passed`
- original S3 tests included: `22`
- independent hostile probes included: `8`
- Python: `3.12.14`
- pytest: `9.1.1`
- determinism: `EXACT`
- court spec SHA-256: `ab7b71b3a469e66b00ef8015fc94cfc062f867c1da8c410c3ba7f4c291c865be`
- receipt artifact ID: `9984817454`
- receipt artifact ZIP SHA-256: `fbc294c2fc2545ec014d7e4d44010baff1a799f560f518c63dd11acf857bf9df`

The hostile court being green means **the hostile reproductions are stable**. It is evidence for this FAIL disposition, not evidence that S3 is lawful.

The temporary branch-specific workflow trigger was removed after execution. The workflow is restored byte-for-byte to blob:

`a974469aa1d83514d896e3de591d7618310ca493`

## What S3 gets right

T3 did not manufacture failures where none exist.

The following portions are sound at this bounded grain:

1. top-level ADP-010 authority/registry IDs and versions are reproduced;
2. public admission functions enforce `AVAILABLE -> OPPORTUNITY -> ENCOUNTER` parent sequencing;
3. admitted parent actor continuity is enforced;
4. admitted parent exact subject-ref continuity is enforced;
5. the literal `V3DP_DEVELOPMENT_ACTIVE` requirement and exact ADP-008 top-level ID/version/blob constants are checked;
6. core-v1 execution is ZERO_DRAW and no random source contaminates identity;
7. directly supplied witness kinds such as `COLOCATION`, `COPRESENCE`, shared endpoint, structural target, institution class and narrative plausibility are rejected as contact witnesses;
8. actor/subject/time/`CONTACT_OCCURRENCE` equality is checked on the caller-supplied contact-witness object;
9. no EXPOSURE API is exposed or inferred;
10. no comparator, PSEPF, metabolism, CAN-008 or V2 authority is created;
11. the bounded executor does not mutate broader actor state;
12. admission-produced timezone-equivalent instants and canonical ref ordering are deterministic;
13. duplicate exact admission calls are idempotent.

Those properties are worth preserving in repair.

## Adoption-blocking defect 1 — subject ingress is shaped, not authenticated

`SubjectIngressEvidence` accepts:

- any nonempty `subject_ref`;
- any nonempty semantic-owner authority ID/version;
- any SHA-256-shaped owner/object hashes;
- any well-formed `ExactRef` as the materialization receipt;
- any well-formed `ExactRef` as the causal-use permission;
- arbitrary nonempty provenance refs.

It never proves that:

- the subject ref is the content-addressed output of the supplied materialization receipt;
- the materialization receipt resolves to the same owner/object;
- the owner authority hash is the authority that actually owns that object;
- the causal-use permission is actually a permission owned by a competent authority;
- those refs form one mutually bound immutable ingress chain.

The hostile court admitted an AVAILABLE record using:

- free-form `subject_ref = "caller-supplied-free-form-subject"`;
- arbitrary owner `UNACCEPTED_CALLER_OWNER@999.999`;
- a supposed materialization receipt whose ref kind was `COLOCATION`;
- a supposed causal-use permission whose ref kind was `SAME_GEOGRAPHY_TIME`.

That is not exact ADP-010 basis authentication.

It violates the accepted `BASIS_TO_AVAILABLE` requirement for exact basis identity, authority/version/epistemic class, causal-use permission, and provenance/integrity.

## Adoption-blocking defect 2 — exact ADP-008 phase state is not identity-bound

S3 checks:

- the caller's phase-authority ID/version/blob constants;
- `phase_state_ref.kind == "V3DevelopmentalPhaseState"`;
- `base_phase_id == V3DP_DEVELOPMENT_ACTIVE`.

But the exact `phase_state_ref` is not bound into S3's candidate replay hash or record identity.

T3 supplied two different exact `V3DevelopmentalPhaseState` refs for the same actor, both with the caller-declared active base phase.

Result:

- different record body `phase_state_ref`;
- same `source_candidate_replay_hash`;
- same `record_id`;
- same `record_hash`.

Thus two materially different phase-state evidences collapse to one OEE identity.

That is incompatible with ADP-008/ADP-010 replay provenance.

## Adoption-blocking defect 3 — applicability authority signature is not bound

`PositiveApplicabilityReceipt` contains:

- authority ID;
- authority version;
- authority content hash;
- receipt ref;
- result;
- provenance.

S3 verifies only that the authority strings/hashes are syntactically well formed and `result == "POSITIVE"`.

Its candidate material carries the applicability **receipt ref**, but not the applicability authority ID/version/content hash.

T3 changed all three authority-signature values while holding the receipt ref constant.

Result:

- same candidate replay hash;
- same OPPORTUNITY record identity.

Therefore exact input-authority signature divergence does not produce replay divergence.

That contradicts ADP-010's explicit exact-input-authority requirement.

## Adoption-blocking defect 4 — contact authority and independence are not authenticated

S3 checks that the caller-created witness object says:

- witness ref kind = `CONTACT_OCCURRENCE_WITNESS`;
- semantic = `CONTACT_OCCURRENCE`;
- actor and subject match;
- occurrence time matches;
- independence ref kind = `CONTACT_WITNESS_INDEPENDENCE`.

But it does **not** establish that the witness authority is accepted/competent or that the independence ref is an authority-backed proof linked to the witness.

Any nonempty witness authority ID/version plus SHA-shaped hash is accepted.

T3 changed the witness authority ID/version/content hash while keeping the exact witness/independence refs unchanged.

Result:

- same ENCOUNTER candidate replay hash;
- same ENCOUNTER record identity.

The supposedly authoritative source of contact occurrence is therefore not part of the causal identity.

## Adoption-blocking defect 5 — co-location can be laundered through relabeling

S3 correctly rejects a ref whose direct kind is literally `COLOCATION` or another listed insufficient class.

But because it trusts the caller-created `ContactOccurrenceWitness` wrapper, T3 supplied:

- arbitrary unaccepted witness owner;
- caller-labeled `CONTACT_OCCURRENCE_WITNESS`;
- caller-labeled `CONTACT_WITNESS_INDEPENDENCE`;
- provenance consisting only of `COLOCATION` and `SAME_GEOGRAPHY_TIME`.

S3 emitted:

`OEE_ENCOUNTER_OCCURRED`.

So the protection is lexical, not authoritative.

The accepted law is stronger:

co-location/co-presence/geographic overlap/shared endpoint/structural target/institution class are insufficient **regardless of how a caller relabels them**.

## Adoption-blocking defect 6 — `validate_record` cannot validate its replay bindings

This is the most direct integrity failure.

Starting from a valid S3 OPPORTUNITY record, T3 changed all of the following without changing `record_id`, `record_hash`, or `source_candidate_replay_hash`:

- `source_candidate_id`;
- context/world refs;
- applicability refs;
- `phase_state_ref`;
- position/constraint refs;
- prior ledger anchor;
- provenance refs.

T3 replaced them with semantically contradictory kinds including:

- `COLOCATION`;
- `NEGATIVE_APPLICABILITY`;
- `NARRATIVE_PLAUSIBILITY`;
- an unrelated ledger ref.

`validate_record()` accepted the tampered record.

Why: it treats `source_candidate_replay_hash` as an opaque trusted string. It does not reconstruct the candidate material from persisted evidence and recompute the hash.

Therefore fields that are supposed to be transitively protected by replay identity are in fact mutable without detection.

## Adoption-blocking defect 7 — required rule/authority hash provenance is not enforced

Accepted ADP-010 provenance requires exact authority/registry/rule hashes and the registry explicitly lists `rule hash` among required rule semantics.

S3 does not require any such exact provenance ref.

A record can be emitted with arbitrary generic provenance and no mechanical ADP-010 authority/registry/rule content-hash binding.

The module's top-level Git blob constants do not repair this omission because they are not required in each record's reconstructible replay provenance.

## Adoption-blocking defect 8 — `source_candidate_id` is not derived or validated

`V3OEERealizationRecord` requires both:

- `source_candidate_id`;
- `source_candidate_replay_hash`.

S3 creates a content-address-looking candidate ID during admission, but `validate_record()` does not check it.

T3 replaced `source_candidate_id` with arbitrary non-content-addressed text.

The record retained the same record ID/hash and validated successfully.

That makes persisted future-canary replay identity internally inconsistent.

## Item 20 — future real-canary identity compatibility

T3's answer is **NO: the current S3 candidate is not identity-compatible enough for a future real canary**.

The canonical record field list is present, but presence is not sufficient.

The missing/transitively uncommitted material includes at least:

- exact ADP-008 phase-state evidence;
- applicability authority ID/version/content hash;
- contact-witness authority ID/version/content hash;
- authenticated subject-owner/materialization/use linkage;
- required ADP-010 authority/registry/rule hash provenance;
- validated derivation of `source_candidate_id`;
- reconstructible material sufficient to recompute `source_candidate_replay_hash`.

A real invocation built on the current implementation could therefore produce one content-addressed OEE ID for materially different authority/evidence states, or accept a persisted record whose body no longer corresponds to the candidate identity it claims.

That is adoption-blocking.

## Synthetic-fixture / current-canary boundary

The S3 test fixture itself was not persisted as project current truth, and the original S3 return correctly declared that its synthetic ENCOUNTER was not a current positive canary invocation.

T3 also performed no real subject materialization or real OEE invocation.

However, because the executor trusts caller-supplied authority wrappers and its emitted record does not independently authenticate those wrappers, the current implementation does not mechanically provide enough protection to rely on that procedural distinction after adoption.

This is covered by the authentication/replay repair requirement; T3 does not add a new fixture-only field to the canonical record contract.

## Smallest exact repair requirement

Do **not** redesign ADP-010.

Do **not** modify S1/S2 semantic authority.

Repair only the S3 executor authentication/replay seam:

1. authenticate the exact externally supplied subject ingress chain so `subject_ref`, semantic owner ID/version/hash, semantic object identity, materialization receipt, causal-use permission and provenance are mutually bound to the same immutable object;
2. authenticate the exact ADP-008 phase-state record/receipt and bind its exact state ref/hash plus required accepted authority/registry identity into replay;
3. authenticate positive applicability against its exact owning authority and bind authority ID/version/content hash + receipt identity into candidate replay;
4. authenticate a separately competent contact-occurrence witness authority/receipt and its independence proof; caller labels alone must never establish contact occurrence;
5. ensure co-location/co-presence/proximity cannot be laundered by changing ref-kind strings or wrapping them in an unauthenticated witness object;
6. require exact accepted ADP-010 authority/registry/rule hash provenance under the existing canonical law;
7. derive and validate `source_candidate_id` from exact candidate material;
8. persist enough exact candidate material/refs to recompute `source_candidate_replay_hash`;
9. make every mutable record field either directly record-identity-bound or transitively committed by a replay hash that `validate_record()` actually recomputes;
10. rerun S3's original court plus these T3 hostile probes under the governed bounded court.

No broader semantic authority is needed for this repair.

## Disposition

S3 is **not lawful for bounded adoption in its current banked form**.

The correct T3 terminal is:

`FAIL__GT34_T3_OBL055_S3_ADP010_V3P5_EXECUTOR_AUTHENTICATION_AND_REPLAY_INTEGRITY_GAPS`

T3 does not adopt, repair, or rewrite S3.
