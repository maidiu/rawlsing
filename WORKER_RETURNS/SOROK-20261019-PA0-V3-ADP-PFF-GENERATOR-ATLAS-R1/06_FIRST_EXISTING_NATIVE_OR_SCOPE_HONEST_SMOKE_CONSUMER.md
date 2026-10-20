# PA0 — FIRST EXISTING NATIVE OR SCOPE-HONEST SMOKE CONSUMER

**Checkout:** `7623742bb9acd113d21de2d4528a1d5a35017989`.
**Script:** `smoke/smoke_consumer.py`.
**Machine receipt:** `evidence/smoke_run.json` (exit 0; stdout only; stderr empty).

The checkout has **no person generator** (zero Python references to `GeneratedPersonRecord`, `DevelopmentalEventLedger` or `V3RenderContext`). The smoke therefore exercises the two strongest *existing* producers without renaming them: an exact CURRENT_ACCEPTED nonactor subject materialization and the ADP-010 OEE actor-event executor. Neither is reported as a person, a native actor event or a C9 positive.

## Invocation A — CURRENT_ACCEPTED nonactor subject materialization (REAL current producer)

**Import path:** `rawlsing_next.gt34_u2_v3p1_authenticated_subject_materializer`
**Module git blob:** `b0cb39a9a975381f3f3b4a03e7e435b2932e89b9`
**Entrypoint:** `materialize_owner_bound_subject(material, CURRENT_ONE_OBJECT_MATERIALIZATION_PERMIT)`

**Exact input reconstruction.** The adopted OBL053 adoption JSON (`f561765b…`) gives the semantic projection facts and the content-addressing law; the repair artifact blob `14ff405c…` carries the exact projection. Canonical JSON of `prospective_semantic_object.semantic_projection` (1,769 bytes) hashes to:

`9a5fbe9a7c272cb2a60e425f09b206f0d25dd2d95caa07028bdb021130c32547`

equal to the adopted object hash and to the U2 root's `semantic_object_ref.sha256`. The material is built with the root's exact authority/evidence/provenance refs and the owner-binding hash computed by the module.

**Observed positive:**

| Field | Value |
|---|---|
| integrity_state | `AUTHENTICATED_FRESH_OBL053_ROOT__OWNER_BOUND_INPUT_VERIFIED` |
| subject_ref | `urn:rawlsing:v3:subject:sha256:a0d7805874dc8449fa81770254a59accde050871aed13501902502e317273f33` |
| receipt_hash | `e8bb714f46a12dd1643e71a0e4a209ba3f7253be9d350d212b696146da11807f` |
| adopted root hash | `1563a1661d3e0a76e6781633f1b590147e26ab21014674bbe732f68cef6acfa8` |
| permit hash | `3eeea2dcfa0a70f1a5b6ce15d41d9f83d84e39ecde816896150fff21e77573dc` |
| semantic_owner_transfer | `false` |
| semantic_fields_interpreted | `false` |
| facts | `NONACTOR_FACILITY / HEALTHCARE_DELIVERY / CLINIC / OUTPATIENT_HEALTHCARE_SERVICE_DELIVERY / PUBLIC_SECTOR` |

**Scope honesty.** This is a **nonactor facility subject-ref**. It is not a person, not an actor, and has no encounter/exposure history. It proves the U2 producer is live and exact; it does not prove person formation.

**Source-edge severances (same positive must disappear):**

| Edge changed | Observed typed result |
|---|---|
| append one byte to the semantic object bytes while keeping the adopted ref | `SubjectMaterializationError: semantic object bytes/hash mismatch` |
| replace the semantic owner id with a forged owner | `AcceptedOwnerAuthenticationError: semantic owner id mismatch` |
| use the historical invalid OBL053 adoption blob | `MaterializationPermitError: permit does not terminate in the current accepted OBL053 root` |

All three failed closed with no receipt.

## Invocation B — ADP-010 OEE actor-event executor (REAL code, NONCURRENT SYNTHETIC evidence)

**Import path:** `rawlsing_next.v3_adp010_oee_executor_authenticated`
**Module git blob:** `54d9acba40f0eb1db8bb03aec3c1bb900f849588`
**Entrypoints:** `_admit_available_noncurrent_for_test`, `_admit_opportunity_noncurrent_for_test`, `_admit_encounter_noncurrent_for_test` (the module's own synthetic noncurrent helpers), plus `validate_basis_available_opportunity_encounter_chain`.

**Observed positive:**

| Field | Value |
|---|---|
| states | `AVAILABLE → OPPORTUNITY → ENCOUNTER` |
| effect kinds | `null → OEE_OPPORTUNITY_ESTABLISHED → OEE_ENCOUNTER_OCCURRED` |
| authority | `V3_OPPORTUNITY_ENCOUNTER_EXPOSURE_REALIZATION_RULE` v1.0.0; registry `V3_OEE_REALIZATION_RULE_REGISTRY` |
| record hashes | `0e37b0b5…`, `6374fd78…`, `fafe20c3…` |
| encounter event id | `urn:rawlsing:v3:oee:event:sha256:57a7a267…` |
| subject_ref | `urn:rawlsing:v3:subject:sha256:ddeeedf9…` (synthetic) |

**Scope honesty.** `NONCURRENT_SYNTHETIC_TEST_ONLY__NOT_NATIVE_ADP010__NOT_A_PERSON`. The chain is real executor behavior with synthetic evidence; it is not an admitted native ADP-010 realization, not EXPOSURE, not a native actor event and not a person.

**Source-edge severances:**

| Edge changed | Observed typed result |
|---|---|
| contact semantic `COLOCATION` instead of `CONTACT_OCCURRENCE` | `OEEAdmissionError: contact witness does not assert CONTACT_OCCURRENCE` |
| AVAILABLE record passed as the OPPORTUNITY parent | `OEEAdmissionError: expected OPPORTUNITY parent` |
| NONCURRENT synthetic subject presented to the installed `CURRENT_ACCEPTED` executor | `OEEAdmissionError: subject currentness must be CURRENT_ACCEPTED` |

No ENCOUNTER record was produced in any severance.

## The first missing person producer (what the smoke cannot do)

The first real positive requires a **V3 person development engine** that emits `GeneratedPersonRecord`/`DevelopmentalEventLedger` and can feed a C10/C9 consumer. The exact contract is in `05_RECOVER_WIRE_BUILD_RESOURCE_DECISIONS.md` (FC-1). The minimal consumer-facing acceptance test is:

1. A source-qualified ADP007-activated actor and an admitted ADP019 event/ADP010 encounter exist.
2. The engine applies issued developmental rules and emits a durable `GeneratedPersonRecord` with exact source/clock/authority provenance.
3. A named C10 or C9 consumer reads the record and changes its own state; removing the event/rule/actor source makes the **same named consumer assertion RED**.
4. No native positive is published while the PSEPF guard denies or while RULE_A/RULE_T/ADP receipts are unissued.

Today steps 2–4 have no engine. Inventing a scripted record would be a false positive and is not done here.

## Reproduction

```text
cd <checkout>
python3 -B WORKER_RETURNS/SOROK-20261019-PA0-V3-ADP-PFF-GENERATOR-ATLAS-R1/smoke/smoke_consumer.py
```

Exit 0, stdout JSON, stderr empty. No file outside this return was written.
