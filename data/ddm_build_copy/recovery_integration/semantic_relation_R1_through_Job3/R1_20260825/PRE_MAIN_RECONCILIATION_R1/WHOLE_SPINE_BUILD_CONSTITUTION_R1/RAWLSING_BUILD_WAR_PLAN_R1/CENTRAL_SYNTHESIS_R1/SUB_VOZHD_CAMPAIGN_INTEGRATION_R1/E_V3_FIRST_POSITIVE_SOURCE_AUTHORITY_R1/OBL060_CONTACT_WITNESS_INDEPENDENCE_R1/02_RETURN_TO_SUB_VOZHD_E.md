# OBL060 CONTACT-WITNESS-INDEPENDENCE — RETURN TO SUB-VOZHD E R1

Terminal recommendation: `FAIL__OBL060_CONTACT_WITNESS_INDEPENDENCE__MALFORMED_BOOLEAN_TIMESTAMP_ACCEPTED`

Required return terminal:
`RABOCHII_SUBV_E_OBL060_CONTACT_WITNESS_INDEPENDENCE__RETURN_TO_SUB_VOZHD_E`

## Frozen candidate authority

Candidate identity:
`V3_CONTACT_WITNESS_INDEPENDENCE_SOURCE_AUTHORITY_CANDIDATE@1.0.0`

Receipt kind:
`V3_CONTACT_WITNESS_INDEPENDENCE_RECEIPT_CANDIDATE@1.0.0`

Frozen semantic candidate commit:
`996e89a1c44317174733d182f30208af5173126b`

Candidate artifacts:
- `rawlsing_next/v3_contact_witness_independence_source_authority_candidate_r1.py`
- `rawlsing_next/tests/test_v3_contact_witness_independence_source_authority_candidate_r1.py`
- `E_V3_FIRST_POSITIVE_SOURCE_AUTHORITY_R1/OBL060_CONTACT_WITNESS_INDEPENDENCE_R1/00_CANDIDATE_AUTHORITY.md`
- `E_V3_FIRST_POSITIVE_SOURCE_AUTHORITY_R1/OBL060_CONTACT_WITNESS_INDEPENDENCE_R1/01_GOVERNED_BOUNDED_COURT_MATRIX.md`

No candidate semantic file was modified after the freeze above.

## Exact jurisdiction

The candidate owns only the synthetic proof/receipt contract by which an already-identified exact contact-occurrence witness could be shown, for later ADP-010/OEE consumption, to be grounded in a source-owner record distinct from the occurrence authority.

It does not admit, create, validate, or activate an occurrence. It does not own ADP-019, realize OEE, create ENCOUNTER or actors, issue applicability or causal-use permission, install project-current independence, execute OBL055, or install current-positive OBL056 entries.

## Explicit occurrence-vs-independence non-identity

Occurrence authority input identity:
`V3_EXTERNAL_INTERACTION_EVENT_ADMISSION_RULE@1.0.0`

Independence source-owner candidate identity:
`V3_CONTACT_WITNESS_INDEPENDENCE_SOURCE_AUTHORITY_CANDIDATE@1.0.0`

These identities are intentionally and contractually distinct. An occurrence receipt is linkage material only and cannot self-certify independence or be reused as the independence source record/receipt. ADP-019 is not converted, aliased, or widened into witness-independence authority.

## Governed bounded-court evidence

Candidate execution-control commit:
`9e86ee0970936f7435f622ff31663969f8ee876e`

PR: `#267` — closed unmerged, execution-only.

Governed run: `34179018975`
Job: `101914090656`

Exact result:
- protocol self-test: `20 passed`
- court-spec validation: `PASS`
- candidate bounded court: `45 passed`
- governed job terminal: `success`

Receipt artifact:
- artifact id: `10038228744`
- artifact name: `rabochii-court-receipt-34179018975`
- artifact ZIP SHA-256: `6bd486dfce42bc505a0574a797c21db2f925d005d833bc77d1c05c4524bf69c4`

The candidate court covered the commissioned rejection set, laundering mixtures, wrong occurrence/authority/scope/bindings, malformed digest/object cases, stale/future/invalid-window receipts, synthetic-only gating, forbidden-effect absence, and one lawful `NONCURRENT_SYNTHETIC` positive control.

## Exactly ONE fresh independent hostile review

Reviewer identity:
`RABOCHII_SUBV_E_OBL060_INDEPENDENT_HOSTILE_REVIEWER_R1`

Reviewer branch:
`agent/rabochii-subv-e-obl060-contact-witness-independence-hostile-r1`

This identity is distinct from both the occurrence-authority identity and the candidate/source-owner identity.

Frozen hostile matrix:
`2ea2eef35e376bed9506e07ce1ede1e11bcae255`

Hostile test commit:
`06d63b5ac1937c67221e2bab2dd4bf14ed4325d6`

Hostile evidence-execution head:
`e2fa6b040e74e49f2bd782193caaa420b713edfd`

PR: `#268` — closed unmerged, exactly-one hostile review, no repair.

Governed hostile run: `34179159976`
Job: `101914504813`

Exact result:
- protocol self-test: `20 passed`
- court-spec validation: `PASS`
- hostile bounded court: `1 failed, 17 passed`
- governed job terminal: `failure`

Failed attack:
`test_h02_boolean_timestamp_encoding_is_malformed_and_must_fail_closed`

Observed failure:
`Failed: DID NOT RAISE IndependenceProofError`

Hostile receipt artifact:
- artifact id: `10038276837`
- artifact name: `rabochii-court-receipt-34179159976`
- artifact ZIP SHA-256: `24ae74679e0950e11cde3392eab9d676a0efc2dea63b9a23117c257f2c2553fd`

Hostile terminal:
`FAIL__FROZEN_OBL060_CANDIDATE_ACCEPTS_BOOLEAN_AS_INTEGER_TIMESTAMP`

No second reviewer was commissioned and no candidate repair was attempted after hostile review began.

## Smallest exact blocker

The frozen candidate uses Python `isinstance(value, int)` for receipt timestamp validation. In Python, `bool` is a subclass of `int`; therefore `issued_at_epoch=True` is accepted as an integer. A synthetic receipt can consequently be issued with a malformed boolean timestamp (`issued_at_epoch=True`, `expires_at_epoch=2`) instead of failing closed.

This violates the commissioned requirement that malformed receipts fail closed. The smallest prospective correction is to require exact integer type while explicitly excluding booleans for all receipt-time inputs, followed by a newly commissioned repair/review wave. This packet does not perform that correction.

## PASS/FAIL recommendation

`FAIL` — do not adopt the frozen candidate as OBL060 source authority in this wave.

## No-current-effect attestation

No project-current occurrence was admitted or created. No project-current witness-independence fact was created or installed. No actor was created/activated; no applicability or causal-use permission was issued; no ENCOUNTER or OEE was realized; OBL055 was not executed; no current-positive OBL056 entry was installed; no project-current authority index was updated; and no HQ adoption is claimed.

`RABOCHII_SUBV_E_OBL060_CONTACT_WITNESS_INDEPENDENCE__RETURN_TO_SUB_VOZHD_E`
