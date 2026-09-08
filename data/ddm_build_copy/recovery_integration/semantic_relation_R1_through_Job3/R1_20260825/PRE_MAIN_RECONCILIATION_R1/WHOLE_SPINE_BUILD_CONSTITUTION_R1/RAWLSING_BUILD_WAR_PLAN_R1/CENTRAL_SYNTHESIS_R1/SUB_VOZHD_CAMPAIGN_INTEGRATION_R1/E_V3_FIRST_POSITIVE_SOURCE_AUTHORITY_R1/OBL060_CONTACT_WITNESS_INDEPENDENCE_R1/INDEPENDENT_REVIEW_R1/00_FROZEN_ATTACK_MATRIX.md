# OBL060 R2 LAWFUL INDEPENDENT REVIEW R1 — FROZEN ATTACK MATRIX

Reviewer identity:

`RABOCHII_SUBV_E_OBL060_R2_LAWFUL_INDEPENDENT_REVIEWER_R1`

Commissioned review branch:

`agent/rabochii-subv-e-obl060-contact-witness-independence-r2-independent-review-r1`

Exact commissioned start:

`865d2cbe9aa323d334b2eae42150f1cf2db03a4d`

Frozen repaired candidate:

`c35d98db1ef787fb3a4986a963d7c389bd841432`

Candidate module under review:

`rawlsing_next/v3_contact_witness_independence_source_authority_candidate_r2.py`

## Review law

This is the one fresh independent review commissioned by SUB-VOZHD E for the frozen OBL060 R2 repaired candidate. Review only. No repair, candidate mutation, semantic widening, adoption, or current-positive installation is authorized in this wave.

The reviewer is independent from both the occurrence authority identity and the candidate/source-owner implementation identity. A review failure returns the smallest exact blocker and stops. A review pass makes the frozen repaired candidate eligible only for SUB-VOZHD-E consideration; it does not adopt or activate anything.

## Jurisdiction that must remain preserved

The candidate may only prove contact-witness independence for ADP-010 use from a distinct source-owner witness record. It does not admit an occurrence. `V3_EXTERNAL_INTERACTION_EVENT_ADMISSION_RULE@1.0.0` remains the occurrence authority and must not become, alias, or self-certify witness independence. OBL060 must not create an actor, issue positive applicability, issue causal-use permission, create ENCOUNTER, realize OEE, install project-current independence, execute OBL055, install current-positive OBL056 entries, or update a current authority index.

Only `NONCURRENT_SYNTHETIC` fixtures may pass in this review.

## Frozen attack families

Any single unlawful acceptance is terminal FAIL.

1. **Target and reviewer non-identity**
   - candidate authority identity must differ from occurrence authority identity;
   - reviewer identity must differ from both;
   - R2 wrapper must preserve the R1 authority/reference identities rather than minting a second authority.

2. **Occurrence-authority collapse**
   - source-owner authority equal to occurrence authority fails;
   - receipt authority equal to occurrence authority fails;
   - wrong occurrence authority fails.

3. **Occurrence receipt self-certification / reuse**
   - occurrence receipt id cannot be the source record id;
   - occurrence receipt id cannot be the independence receipt id;
   - occurrence receipt digest cannot be reused as source evidence;
   - source record id cannot substitute for independence receipt id.

4. **Mandatory rejection bases — each independently**
   - `SELF_CERTIFICATION`
   - `AUTHORITY_IDENTITY_REUSE`
   - `RECEIPT_REUSE`
   - `CO_LOCATION`
   - `CO_PRESENCE`
   - `SAME_GEOGRAPHY_TIME`
   - `SHARED_ENDPOINT`
   - `INSTITUTION_CLASSIFICATION`
   - `NARRATIVE_PLAUSIBILITY`

5. **Basis laundering**
   - positive basis mixed with any rejected basis fails;
   - multiple rejected bases fail;
   - unknown basis mixed with the positive basis fails;
   - duplicate/variant narrative material cannot substitute for the exact positive contract.

6. **Wrong occurrence / authority / scope / binding**
   - wrong expected occurrence;
   - wrong source occurrence;
   - wrong occurrence scope;
   - wrong independence scope;
   - wrong source-owner authority;
   - wrong receipt authority;
   - wrong receipt occurrence-authority binding;
   - wrong occurrence-receipt binding;
   - wrong source-record binding.

7. **Malformed and tampered digests / kinds / objects**
   - malformed occurrence digest;
   - malformed source evidence digest;
   - malformed independence receipt digest;
   - source-record digest mismatch;
   - receipt digest tamper;
   - wrong receipt kind;
   - wrong source-record kind;
   - malformed/non-dataclass receipt object.

8. **Synthetic-only boundary**
   - project-current/current/missing/non-synthetic fixture classes fail;
   - one lawful `NONCURRENT_SYNTHETIC` control must pass.

9. **R2 repaired issuance timestamp typing**
   - `True` and `False` fail as `issued_at_epoch`;
   - `True` and `False` fail as `expires_at_epoch`;
   - an `int` subclass fails in either issuance timestamp field;
   - float/string/None fail.

10. **R2 repaired validation timestamp typing**
    - boolean receipt `issued_at_epoch` fails;
    - boolean receipt `expires_at_epoch` fails;
    - integer-subclass receipt timestamps fail;
    - boolean/integer-subclass/float/string/None `now_epoch` fails.

11. **No laundering of an R1-malformed receipt through R2**
    - construct a receipt through the frozen R1 issuer using a boolean timestamp that R1 historically accepted;
    - R2 validation must reject it before it can become lawful independence proof.

12. **Temporal validity**
    - equal/reversed issue-expiry windows fail;
    - stale receipts fail;
    - not-yet-valid receipts fail;
    - valid exact-integer window passes only with otherwise lawful proof.

13. **Receipt basis mutation**
    - a valid receipt mutated to contain a rejected or unknown basis fails, irrespective of digest recomputation attempts.

14. **Positive control remains narrow**
    - one lawful synthetic occurrence envelope + one distinct candidate-owned source record + one exact positive basis may issue and validate;
    - occurrence and independence identities/receipt ids remain distinct.

15. **No effect-surface expansion**
    - candidate module exposes none of the forbidden effect surfaces;
    - candidate imports no network/database/subprocess/file-writing mechanism;
    - review tests create no project-current occurrence or independence fact.

16. **Repair narrowness / wrapper integrity**
    - R2 delegates inherited semantic checks to frozen R1 rather than replacing occurrence/source/basis jurisdiction;
    - R2 adds exact-integer gates to issuance and validation only;
    - exact-built-in-`int` behavior must be visible in source and no permissive `isinstance(value, int)` repair may reappear in R2.

## Terminal law

PASS only if every attack passes and the lawful synthetic control passes. FAIL on the smallest first exact blocker. This review may not repair the candidate after freeze.
