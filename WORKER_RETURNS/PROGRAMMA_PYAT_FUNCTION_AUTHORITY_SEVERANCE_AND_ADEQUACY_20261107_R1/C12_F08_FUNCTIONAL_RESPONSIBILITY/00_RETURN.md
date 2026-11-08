# C12 — F08/Q_USE functional-responsibility comparison (C11R-01)

**Lane:** issue #777 C11R-01 finite continuation; same existing OpenCode session/model.
**Worktree:** `/Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat777-source-consumer`
**Branch:** `agent/pyat777-source-consumer-20261107-r1`
**Starting HEAD:** `76392135cea16afc0ff07da97843837bd33fc9b7`
**Accepted Q3 input:** C11 commit `76392135c`; C6 corrected cut `0d548b033a0a20c9738fa4a3412ba5acd01217c5`; archive source `9ba4764bef551b1ce498e5772d60b73d69337d4b`.
**Review read:** `b939c51a21359efc556c3f58860789e247b011aa`; verdict `REVISE_SCOPED`, Q3 accepted, Q4 `UNPROVED`.

No replay, test, source/respondent/SAV/DTA/DB read, native/science/actor run, production/test/HQ/peer/protected write, environment install, new worker, model/provider/effort change or repair was performed.

## Result

The historical QUC output decomposes into five exact obligations. The current whole PRE-V3 has **different or partial responsibilities** in existing owners, but no proved QUC-equivalent producer→selector→consumer contract. No selected current operation in the existing C6/C4/C3/current traces demands the exact historical QUC semantics.

| Obligation | Historical responsibility | Current existing owner / contract | Current status |
|---|---|---|---|
| Role designation / inference / override | QUC infer role, authority designation and manual override; AR-0048 selected `RELATION_EVIDENCE` override | C4 O14 `pre553_j_role_certification.py:356-388/1018-1027/1257-1329`: caller role assignment → J role vector → M1 validator; non-test invocation `NONE_FOUND_IN_STATIC_SOURCE` (not absence) | Implemented different responsibility; QUC role/override **UNPROVED** |
| Relation-evidence admission / review required | QUC `review_required=true`, `allowed_as_v551_relation_evidence=false`, four disallowed gates | C3 FF/GT12 bounded Q86 canary; generic GF1 is test-only/unmerged PR #691; C3-FF-04 says no generic first reader | Bounded canary/unmerged candidate, different responsibility; QUC admission/review **UNPROVED** |
| Source-structure classification | AR-0049 exact join `source+wave+question_id` → `substantive_single_choice`, fields joined | C11 `QuestionVariableBinding` semantic/topology authority refs and ingest validation; C6 F06 response-contract and F09 routing are separate generic responsibilities | Implemented generic authority refs, not QUC classification; **UNPROVED** |
| Itinerary / review priority / manual designation | AR-0047 selected GSS/1973 `review_priority=high`, no manual designation | No exact current QUC itinerary owner observed in the checked C6/C4/C3/current surfaces; current `EmpiricalQuerySpec`/`TARGET_USE_PERMISSION` is a different authority | **NOT_RUN / UNPROVED**; target-use is not equivalence |
| Taxonomy provenance | AR-0050 `single_choice`/`answer` loaded by historical register builder | Historical `build_question_structure_register.load_taxonomy` only; no current QUC runtime consumer observed | Historical register-builder only; **UNPROVED** |

Full machine-readable row-level producer/selector/consumer contracts, pins and limits are in `RESPONSIBILITY_MAP.jsonl`.

## Current Q4 location and classification

- C6 F08/Q_USE current owner/first consumer remains **`UNKNOWN_NOT_PROVED`**; selected current operation is `NOT_RUN`/`UNPROVED_CURRENT_SELECTION`.
- C4 O14 J role certification is a **different responsibility** from QUC semantic role/override.
- C3 FF covers Q86/GT12 bounded canary and GF1 test-only candidate, not QUC obligation. C3-FF-04/07 preserve generic FF unmerged/unproved and post-FF separation.
- C6 F06 `pre553_c11_ingest.py:644-659` / `pre553_source_backed_c11_facade.py:502-553` and F09 `pre553_c11_ingest.py:601-620` / `pre553_empirical_query.py:725-731` are real generic response/routing owners, not QUC alternatives.
- C11 `EmpiricalQuerySpec` / optional `TARGET_USE_PERMISSION` (`pre553_empirical_query.py:403-438`) and `compile_governed_frontier` are valid current owners, but **target-use permission alone is not QUC equivalence**.

Q4 classification:

```text
FUNCTION_CURRENT_BUT_AUTHORITY_PROVENANCE_UNPROVED
__NO_SELECTED_CURRENT_OPERATION
```

The previous absence/read-requirement wording is removed/qualified: the focused comparison found different existing responsibilities, not a proved absence or a new-reader requirement. No repair, QUC reader, resolver or issuer gate is manufactured.

## Smallest actual unresolved choice / input

The only unresolved choice is whether an actual selected current operation demands the exact historical QUC semantic-role/itinerary/taxonomy responsibility:

- If none, preserve `FUNCTION_CURRENT_BUT_AUTHORITY_PROVENANCE_UNPROVED` / `NOT_RUN` and the existing holds.
- If one exists, the current C6 F08/Q_USE owner plus the existing C11/I03/frontier owners must name the exact selected input and route it at the true metadata/FF/role-preparation owner. Do not force QUC semantics into I03.

## Proof limits and coverage

- Historical Q3 evidence remains accepted at one-row test-time replay: AR-0047 35 rows, AR-0048 7 overrides, AR-0049 18,792 rows, AR-0050 8 question types; one row does not prove all35.
- Historical original runtime remains `NOT_RUN`; current adoption remains unproved.
- The historical contract remains `review_required=true` / `allowed_as_v551_relation_evidence=false`; no full operational pass is claimed.
- No source/respondent/SAV/DTA/DB read, source-byte copy, native/science/actor effect, production/existing-test/HQ/peer/protected write, CI/merge, install, new worker or model change.
- Whole #777 remains incomplete; quota `UNKNOWN`.

## Evidence

`RESPONSIBILITY_MAP.jsonl` — exact obligation, historical owner/effect, current owner/calls, covered/not-covered obligation, selected-operation status, pins and proof limits.
