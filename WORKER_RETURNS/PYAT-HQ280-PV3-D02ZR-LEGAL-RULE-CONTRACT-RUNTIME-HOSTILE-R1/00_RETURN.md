# PYAT HQ280 PV3 D02ZR — Independent documentary-rule candidate runtime review

**TERMINAL:** `HQ280_PV3_D02ZR_DOCUMENTARY_RULE_SOURCEFREE_RUNTIME_HOSTILE_RETURNED__NONISSUING__GITHUB_PUSHED`

**Role:** Independent documentary-rule source contract reviewer (not the D02Z author, not an adopter).
**Repository:** `maidiu/rawlsing`
**Branch:** `agent/reviewer-pyat-hq280-pv3-d02zr-legal-rule-runtime-hostile-r1`
**EXACT SEALED STARTUP (verified before mutation):** `ee66e2b8435d281399e8ce1f8feeeb6927971254`
**Inherited exact D02Z candidate:** `8fbcc84f3ec7664ef2ea565c6813d6e2c1723761`
**Authority:** HQD-2026-10-10-280 · canonical `a70a069fa948e0f3c041b389edcc732b6b948a4f` · semantic PRE-MAIN `1f47063c3205a45888b3c55e81e7485943ed1390` (unmutated).

No original survey source execution. No accepted-owner modifications. No claim that Ghana's statute has an authenticated current legal status. No canonical mutation. No self-adoption.

---

## 0. Verdict in one paragraph

D02Z's evidence is honest and faithfully reproducible: all 6 candidate tests pass and all 35 authored fixture cases execute with the exact expected states, `issued_fact_ref=None` and `candidate_only=True` in every outcome. The candidate never issues a legal fact, never mints a competent issuer, and never manufactures N5/N6/N9 operative states. Independently reproduced here: **27 additional hostile tests, all passing**, covering wrong clause/document/wording/dates/URL, unsigned issuer metadata, issued-fact masquerade, local-SHA-vs-PDF-custody separation, altered JSON identity, operative-state escalation attempts (N9/G0b/empirical/causal/enforcement/person), omitted/extra keys, non-dict inputs, and the as-enacted-text vs person-outcome boundary. **Total: 33 tests, 0 failures, 2 suites, exit code 0 on both.** Disposition: **bounded technical candidate — ACCEPTED as honest development-grade work; NOT an issued legal fact; NOT a competent issuer; NOT N5/N6/N9; NOT G0b; NOT current law.** No adoption.

---

## 1. What was actually executed (nothing here is a restatement)

Worktree: reviewer branch at the sealed startup `ee66e2b843`; inherited D02Z candidate at `8fbcc84f3e` in the same tree (no new clone).

| run | exact command | actual result |
|---|---|---|
| D02Z candidate suite | `python -m unittest -v test_d02z_documentary_rule_contract.py` in D02Z `repro/` | **6 passed, 0 failed** (0.005s), exit 0 |
| D02ZR independent hostile suite | `python -m unittest -v test_d02zr_hostiles.py` in D02Z `repro/` (execution copy of reviewer-authored test) | **27 passed, 0 failed** (0.006s), exit 0 |

Interpreter: Python 3.11.3 (see `repro/interpreter.txt`). Logs: `repro/d02z_candidate_suite.log`, `repro/d02zr_hostile_suite.log`. The hostile test file committed in this return is `repro/test_d02zr_hostiles.py` (byte-identical to the executed copy; the execution copy placed alongside the D02Z candidate module for import was removed after the run — D02Z's return directory is untouched).

**Tests vs fixture cases, distinguished as commissioned:** 6 + 27 = 33 *test methods*. 35 *fixture cases* (1 positive + 34 hostile/held vectors in `03_RULE_TEXT_ORIGINAL_POSITIVE_AND_NEGATIVE_FIXTURES.json`, `case_count: 35`, `len(cases) == 35` verified at runtime). Every fixture case was executed through `evaluate_requested_operation` with its declared operation, and every outcome carried `issued_fact_ref=None` and `candidate_only=True`.

---

## 2. Findings, by severity

### No defects found in the candidate's fail-closed behavior

Every hostile below was **refused or held exactly as the candidate's contract requires**:

- **Source identity substitution** (wrong clause `PART_II_SECTION_15`, wrong document, wrong source URL): `CLAUSE_OR_SOURCE_SEMANTIC_MISMATCH` on the exact field.
- **Wording substitution** (extra/altered ancestor roles): `CLAUSE_OR_SOURCE_SEMANTIC_MISMATCH:qualifying_ancestor_roles`.
- **Time-boundary substitution** (wrong cohort date, wrong assent date): `CLAUSE_OR_SOURCE_SEMANTIC_MISMATCH` on the exact date field.
- **Unsigned issuer metadata** (non-null `producer_issuer_ref`): `FORBIDDEN_UNPROVED_AUTHORITY_OR_OUTCOME`.
- **Issued-fact masquerade** (non-null `issued_fact_ref` smuggled as an extra key): `UNAUTHORIZED_EXTRA_KEYS`.
- **Operative-state escalation** (N9 current/historical, G0b/actor, empirical fact, causal, enforcement, person-citizenship): exact held/refused states from `HELD_OPERATIONS`, never an issued fact.
- **Omitted/extra keys, non-dict inputs**: refused with the exact reason code.

### Confirmed positives (no defect — recorded for symmetry and non-vacuity)

| behaviour | evidence |
|---|---|
| Valid preimage yields shape-positive, never issued | `LOCAL_PREIMAGE_SHAPE_POSITIVE__NOT_ISSUED`, `issued_fact_ref=None`, `competent_issuer_ref=None`, `permitted_externally_active_uses=()` |
| Canonical hash is deterministic local JSON identity | same input → same `canonical_input_sha256`; altered field → altered hash |
| Local SHA-256 is never PDF custody | `source_document_pdf_sha256=None` in every outcome; `original_pdf_byte_custody="NOT_CUSTODIED"` on the input |
| As-enacted text is not a person outcome | `documentary_assertion="SOURCE_TEXT_PREIMAGE_CANDIDATE_ONLY"`; no person-level inference path exists in the module |
| All 12 held/refused production operations | `test_production_operations_always_held_or_refused` (D02Z) + per-operation hostile tests (D02ZR) |

### One honest correction to D02Z's framing (not a defect)

D02Z's return describes "35 locally checkable positive/hostile/held fixtures" and the fixture file declares `case_count: 35` with 35 entries — verified. The 6-test unittest suite exercises them via `test_all_fixture_mutations_and_expected_states` with subTests. There is no missing 35th vector; the count is exact. What "35" does *not* mean is recorded here to prevent misreading: it is not 35 issued facts, not 35 authenticated source bytes, not 35 current-law findings.

---

## 3. Is the candidate certifiable?

**No — not as an issued legal fact, a competent issuer, or N5/N6/N9.** It is certifiable as: an honest, bounded, non-issuing **development candidate providing a shape-checked documentary preimage** with genuine positive and negative runtime behaviour and no accepted-owner mutation.

The gap between "the preimage shape is valid" (true, at this surface) and "Ghana Act 591 §7 has an authenticated current legal status" (false, unproved) is the whole boundary. The candidate itself never crosses it.

## 4. Exact holds (nonissuing)

1. **SOURCE-CUSTODY HOLD:** `original_pdf_byte_custody="NOT_CUSTODIED"`; `source_document_pdf_sha256=null` in every outcome. A local input SHA-256 is a repeatable specimen identity, never custody of the original government PDF.
2. **ISSUER HOLD:** `competent_issuer_ref=null` in every outcome; `ISSUE_RULE_TEXT_DOCUMENTED` is HELD pending a competent original source issuer and producer adoption.
3. **COMMENCEMENT/AMENDMENT HOLD:** `RULE_IN_FORCE_AT_TIME` is HELD pending act-commencement and amendment-asof authority; `amendment_version_chain="NOT_CERTIFIED"`.
4. **PERSON/ENFORCEMENT/SERVICE/CAUSAL HOLD:** person-citizenship, enforcement, service-access and causal operations are REFUSED — no person case facts, no administrative observation, no access measurement, no causal authority.
5. **STRUCTURAL/EMISSION HOLD:** empirical-fact emission, V554-root emission and V557/V558 binding are REFUSED/HELD — wrong object family, forged producer family, unapproved documentary root.
6. **N9/CURRENT HOLD:** N9 historical/current are HELD — no issued rule-source root, no N9 consumer, no current legal version, no selected world.
7. **G0b/V3 HOLD:** model/actor use is REFUSED — no grant.
8. **No G0b / no operative CURRENT / no N9 release / no V3 / no trust root.**

## 5. Return contents

- `00_RETURN.md` — this file
- `01_ACTUAL_RUNTIME_RESULTS.json` — exact interpreter, exit codes, test/fixture counts, per-suite logs digests
- `02_INDEPENDENT_HOSTILE_EVIDENCE.md` — hostile classes and what each proves
- `03_SCIENTIFIC_HOLDS.md` — exact holds (source/issuer/commencement/person/N9/G0b)
- `05_MANIFEST.json` — file manifest with SHA-256
- `repro/test_d02zr_hostiles.py` — reviewer-authored independent hostile suite (27 tests)
- `repro/d02z_candidate_suite.log` — captured D02Z 6-test verbose log
- `repro/d02zr_hostile_suite.log` — captured D02ZR 27-test verbose log
- `repro/interpreter.txt` — Python version
