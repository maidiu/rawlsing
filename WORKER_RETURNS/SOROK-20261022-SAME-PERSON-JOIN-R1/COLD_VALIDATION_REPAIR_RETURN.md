# SOROK JOIN-E — cold validation repair

**STATUS:** `COLD_VALIDATION_BOUND_TO_PERSISTED_C12_BINDING__NEW_SESSIONS_CANNOT_DOWNGRADE_TO_LEGACY__GENUINE_LEGACY_REOPEN_PRESERVED__NOT_NATIVE__NOT_SELF_ADOPTED`
**BRANCH:** `codex/sorok-join-e-b-event`
**BASE:** `b327d1423da1e0f94e1b4846059fa1d7c9423261`
**GRADE:** `TEST_ONLY_SOURCEFREE_NOT_NATIVE`
**REVIEW EVIDENCE:** `HQ_INTAKE.md` (cold receipt bypass by deleting the optional contract key)

## 1. FINDING | INTERPRETATION AND RIVALS | ACTION | OWNER

| FINDING | INTERPRETATION AND RIVALS | ACTION | OWNER |
|---|---|---|---|
| **C1. The receipt requirement is persisted in the C12 source branch, not only session metadata.** `JoinedSession.start` appends one `B_EVENT_BINDING` episode containing the contract, exact B event ref/hash, performer receipt hash and disposition. `JoinedSession.open` reads that append-only episode and requires the metadata contract and receipt whenever it exists. | The rival — treating a missing metadata marker as legacy — is rejected: the persisted binding still marks the session as new, so deleting `b_event_contract`, `b_performer_receipt`, or both yields `J_PROVENANCE_MISMATCH` before a session opens. | Retain; no new store, no vendor edit. | JOIN-E + C12 owner |
| **C2. Genuine legacy sessions still cold-reopen.** A pre-B-event session has no `B_EVENT_BINDING` episode and no B-event metadata; the persisted-binding check is not required and the existing provenance path remains positive. | A blanket “receipt always required” rule would break the accepted legacy encounter. The test constructs a genuine old-path session instead of deleting fields from a new one. | Preserve. | JOIN-E + JOIN-V |
| **C3. Existing provenance now includes the same binding check.** `joined/provenance.py` validates the persisted binding against meta and the actual product source, so a direct provenance call cannot skip it. | The rival — duplicate open-only guard — is avoided; both cold open and provenance compare the persisted C12 binding. | Retain. | JOIN-E |
| **C4. Accepted encounter and targetless paths remain intact.** The focus suite includes the full encounter/cold reentry, nonmutating cold reopen/fork, B-event positive/omission/refusal, targetless provenance/fork and foreign-root rejection. | The repair changes only receipt requirement persistence and cold validation, not C8/C9/C12/encounter semantics. | Preserve; independent review of this boundary follows. | JOIN-E + JOIN-V/HQ |

## 2. CHANGED PATHS

Only inside `WORKER_RETURNS/SOROK-20261022-SAME-PERSON-JOIN-R1/`:

- `joined/b_event.py`: persisted `B_EVENT_BINDING` body, reader and binding validator.
- `joined/session.py`: append the binding episode at start; require meta contract + receipt when persisted evidence or legacy metadata marks a B-event session.
- `joined/provenance.py`: same binding check in `validate_join`.
- `tests/test_cold_validation.py` (new): 6 cold-validation tests.
- `evidence/cold_validation_repair.json` (new): scoped receipt.
- `COLD_VALIDATION_REPAIR_RETURN.md` (this file).
- `HQ_INTAKE.md`: updated PROGRAMMA_DELTA.

No vendor, JOIN-V, targetless implementation, store or scientific-rule file was edited.

## 3. EXACT COMMANDS AND RESULTS

```text
PYTHONDONTWRITEBYTECODE=1 python3 -B -m pytest -q \
  WORKER_RETURNS/SOROK-20261022-SAME-PERSON-JOIN-R1/tests/test_cold_validation.py \
  -p no:cacheprovider --tb=short
6 passed in 6.37s
```

```text
PYTHONDONTWRITEBYTECODE=1 python3 -B -m pytest -q \
  WORKER_RETURNS/SOROK-20261022-SAME-PERSON-JOIN-R1/tests/test_b_event.py \
  WORKER_RETURNS/SOROK-20261022-SAME-PERSON-JOIN-R1/tests/test_join.py::test_full_encounter_positive_and_cold_reentry \
  WORKER_RETURNS/SOROK-20261022-SAME-PERSON-JOIN-R1/tests/test_join.py::test_cold_reopen_is_nonmutating_and_fork_diverges \
  WORKER_RETURNS/SOROK-20261022-SAME-PERSON-JOIN-R1/tests/test_join.py::test_b_source_edge_help_observable_and_targetless_no_target \
  WORKER_RETURNS/SOROK-20261022-SAME-PERSON-JOIN-R1/tests/test_join.py::test_targetless_provenance_lineage_and_fork \
  WORKER_RETURNS/SOROK-20261022-SAME-PERSON-JOIN-R1/tests/test_join.py::test_foreign_and_r29p_roots_are_refused_without_donor_mutation \
  -p no:cacheprovider --tb=short
12 passed in 8.64s
```

## 4. COLD VALIDATION RECEIPT

`evidence/cold_validation_repair.json`.

| Case | Cold/in-process | Fresh process |
|---|---|---|
| New B-event session, intact | opens, verify true, `HELP_ACCEPT` | opens, verify true, binding episode present, branch `first_session` |
| Genuine legacy session, intact | opens, verify true, `HELP_ACCEPT` | opens, verify true, no binding episode, branch `first_session` |
| New session, delete `b_event_contract` | `J_PROVENANCE_MISMATCH` | `J_PROVENANCE_MISMATCH` |
| New session, delete `b_performer_receipt` | `J_PROVENANCE_MISMATCH` | `J_PROVENANCE_MISMATCH` |
| New session, delete both fields | `J_PROVENANCE_MISMATCH` | `J_PROVENANCE_MISMATCH` |
| New session, tamper receipt hash | `J_PROVENANCE_MISMATCH` | — |
| Targetless refusal, cold | opens, verify true, `HELP_REFUSE`, no target | — |

## 5. PROGRAMMA_DELTA

```text
PROGRAMMA_DELTA — JOIN-E cold validation repair
- Identity: codex/sorok-join-e-b-event@<scoped-commit>; base b327d1423da1e0f94e1b4846059fa1d7c9423261. SAME-PERSON-JOIN return subtree only.
- Function/interface: new B-event sessions append a persisted C12 B_EVENT_BINDING episode binding contract + exact B event ref/hash + performer receipt hash + disposition. JoinedSession.open and validate_join require the metadata contract and receipt whenever that persisted evidence exists. Deletion of marker, receipt, or both is typed J_PROVENANCE_MISMATCH; genuine pre-B-event sessions without the episode still cold-reopen.
- Evidence: 6 focused cold-validation tests and 12 preserved-path tests pass; evidence/cold_validation_repair.json. New intact and genuine legacy positives, three deletion cuts, receipt tamper, targetless refusal and accepted encounter/cold/fork all executed.
- PROGRAMMA effect: closes the review-identified optional-metadata bypass at the exact repaired cut; no C8/C9/C12 semantics, targetless path, vendor source or native authority changed.
- Next: independent exact-cut review of the persisted binding and cold deletion matrix; owner adoption and native C10 semantics remain external.
```

## 6. LIMITS

Native C8/C10/C11/C12 trust, CAN/ADP/Pyat issuance, provider calls, human A5, production deployment and scientific issuance remain `NOT_RUN`/`HOLD`. This repair makes no receipt-tamper protection claim beyond the persisted C12 binding and existing provenance; same-user custody remains the existing `TRUST_CUSTODY_HOLD` residual.
