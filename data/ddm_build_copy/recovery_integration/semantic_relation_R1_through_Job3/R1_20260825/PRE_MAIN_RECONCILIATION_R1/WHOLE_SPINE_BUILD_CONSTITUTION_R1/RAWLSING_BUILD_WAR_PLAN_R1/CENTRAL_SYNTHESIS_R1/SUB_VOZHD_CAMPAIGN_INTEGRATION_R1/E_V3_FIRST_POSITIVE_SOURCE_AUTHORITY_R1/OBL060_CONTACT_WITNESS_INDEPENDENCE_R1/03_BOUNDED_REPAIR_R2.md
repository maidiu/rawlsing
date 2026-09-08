# OBL060 CONTACT-WITNESS-INDEPENDENCE — BOUNDED REPAIR R2

Worker branch:
`agent/rabochii-subv-e-obl060-contact-witness-independence-bounded-repair-r2`

Exact start:
`0fa24d2eec0dea8257b975b2ef357b6adbc716a1`

## Repair authority

R1 returned terminal:
`FAIL__OBL060_CONTACT_WITNESS_INDEPENDENCE__MALFORMED_BOOLEAN_TIMESTAMP_ACCEPTED`

The single R1 hostile review proved that Python `bool` values satisfy `isinstance(value, int)`, allowing `issued_at_epoch=True` to pass the frozen R1 issuance check.

This R2 wave is bounded to that exact blocker. The failed R1 candidate and its evidence remain immutable.

## R2 successor

Successor module:
`rawlsing_next/v3_contact_witness_independence_source_authority_candidate_r2.py`

Successor court:
`rawlsing_next/tests/test_v3_contact_witness_independence_source_authority_candidate_r2.py`

The R2 successor delegates all substantive OBL060 source-owner, occurrence-vs-independence non-identity, mandatory-rejection, receipt-binding, synthetic-only, and forbidden-effect semantics to the frozen R1 candidate. It adds only an exact built-in integer guard using `type(value) is int` for:

- `issued_at_epoch` at issuance;
- `expires_at_epoch` at issuance;
- receipt `issued_at_epoch` at validation;
- receipt `expires_at_epoch` at validation;
- `now_epoch` at validation.

Therefore booleans and integer subclasses fail closed rather than entering receipt-time comparisons.

## Jurisdiction preserved

Occurrence authority remains:
`V3_EXTERNAL_INTERACTION_EVENT_ADMISSION_RULE@1.0.0`

Independence candidate identity remains:
`V3_CONTACT_WITNESS_INDEPENDENCE_SOURCE_AUTHORITY_CANDIDATE@1.0.0`

They remain contractually distinct. R2 does not admit or create occurrences, become occurrence authority, create/activate actors, issue applicability or causal-use permission, create ENCOUNTER, realize OEE, execute OBL055, install current-positive OBL056, install project-current independence, update a project-current authority index, or claim HQ adoption.

All positive fixtures remain `NONCURRENT_SYNTHETIC` only.

## R2 regression additions

The bounded court retains the complete R1 commissioned court and adds attacks proving fail-closed behavior for:

- `issued_at_epoch=True` and `False`;
- `expires_at_epoch=True` and `False`;
- tampered receipt boolean issue/expiry fields;
- `now_epoch=True` and `False`;
- an `int` subclass at issuance.

No unrelated semantic repair is authorized by this packet.
