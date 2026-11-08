# C11 — independent nonauthor review of Q3/F08 historical consumer effect

**Reviewer:** independent nonauthor issue777 review; same existing OpenCode session and `opencode-go/deepseek-v4.1-flash#max`; no new worker, model/provider/effort change or delegation.
**Author target:** `76392135cea16afc0ff07da97843837bd33fc9b7`, `/Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat777-source-consumer`, `WORKER_RETURNS/PROGRAMMA_PYAT_FUNCTION_AUTHORITY_SEVERANCE_AND_ADEQUACY_20261107_R1/C11_Q3_F08_FIRST_CONSUMER_EFFECT/`.
**C6 cut:** `0d548b033a0a20c9738fa4a3412ba5acd01217c5`; **archive source:** `9ba4764bef551b1ce498e5772d60b73d69337d4b`.
**HQ checkpoint:** `/Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat777-authority-severance-hq` HEAD `9f578483839091b7215d73ad96041deb3ded79bd`; exact output head `55fca441d1c674c256473c264cabda48f2df0e52`; stage `C9_SCOPED_RECONCILIATION_ACCEPTED__Q3_F03_F08_CONSUMER_CHECKS_DISPATCHED__GOAL_FALSE`.

## Verdict: `REVISE_SCOPED`

**Q3 historical replay is accepted** at the exact test-time/S2 scope: authority bytes, unchanged historical consumer, selected GSS/1973/`uswar` row, positive/removal/duplication/missing-register/restore effects and recorded hashes check. **Q4 current succession remains `UNPROVED`**; the author's “no QUC reader”/“would need QUC reader” wording is a name/path hypothesis, not an established current functional-responsibility or absence/equivalence result. The required revision is Q4 reporting/owner-check only; no repair, new reader, engine or issuer gate.

## Exact pins independently checked

| Item | Exact value |
|---|---|
| AR-0047 itinerary | `data/ddm_build_copy/manifests/question_wave_itinerary.csv` @9ba; 11,059 bytes; SHA-256 `866eb3ab25fbd9479781c15a0aecbb00a9d547fdc947cc443e8b904262b86eb3`; 35 rows |
| AR-0048 override | `data/ddm_build_copy/manifests/question_use_overrides.csv` @9ba; 1,702 bytes; SHA-256 `29e7706b7467f9435e57e78a7c8cf1314d9760f03d4d14d2bcf0d54f51809479`; 7 rows |
| AR-0049 QSR baseline | archive `question_structure_register.csv`; 26,582,348 bytes; SHA-256 `15f7b5613b7cb106c2d2db233925891d5392917b66eee19c1a5eff8e0655585b`; 18,792 rows |
| AR-0050 taxonomy | `data/ddm_build_copy/manifests/question_type_taxonomy.yaml` @9ba; 3,487 bytes; SHA-256 `3612c6b400008467471b71cc38d811b8c5349bac0617e974a72e76e584e86b27`; 8 question types |
| Historical QUC module | `data/ddm_build_copy/ddm_v550_question_use.py` @9ba; SHA-256 `254542f96dcb8f07c9ff8fa136d6d13f5923b43ec04c7d2bb1d8a14f46955f31`; 115,511 bytes |
| Source-structure module | `data/ddm_build_copy/ddm_v550_source_structure.py` @9ba; SHA-256 `609a02e1615ba3c028d284b5f11e198df1eda26e53bae2a0b50d6609d749a0e0`; 25,491 bytes |

The exact `GSS / 1973 / uswar` row is present once in AR-0047, AR-0048 and AR-0049:

- AR-0047: `review_priority=high`, `manual_designation_required=false`.
- AR-0048: `semantic_role=RELATION_EVIDENCE`, reason `promote_memory_of_catastrophe_direct_evidence`, `allowed_as_v551_relation_evidence=true` at the override row.
- AR-0049: `question_id=GSS:1973:uswar`, `classification=substantive_single_choice`, `structural_role=answer`, exact join `source+wave+question_id`.
- AR-0050: `single_choice`, structural role `answer`, loaded only by the separate `build_question_structure_register.load_taxonomy` register-builder path; the QUC module does not load taxonomy directly. **Do not accept AR-0050 as QUC runtime/effect proof.**

## Q3 accepted checks

The author's replay imports the exact staged historical QUC module unchanged; the module SHA-256 is asserted at runtime, and the only harness inputs are `sys.path` and explicit authority-path/dataframe arguments. No substantive monkeypatch, `setattr`, `__dict__` patch or function replacement is present. The author's `probes/q3_f08_replay.json` and `logs/q3_f08_replay.log` both hash `ecf97894d50ae0e11caf5f4d8717b42669fd6b9d22f6ea80ad6ea99fe4333a4c`; no replay rerun was necessary, and no full matrix was run.

Observed positive contract summary:

```text
manual_override_used=true
manual_override_basis=source_wave_var_code
manual_override_reason=promote_memory_of_catastrophe_direct_evidence
semantic_role=RELATION_EVIDENCE
itinerary_review_priority=high
source_structure_classification=substantive_single_choice
source_structure_fields_joined=true
review_required=true
allowed_as_v551_relation_evidence=false
question_use_contract_hash=6c94c7a8bbbf4dbae511dece64a312a1ee7fd5fa3a8e4008f004783057288cb1
positive output hash=1c78a386f0b433dd4ffb97768314f92b09e7476d1c31f4a92f8343cb26f253b1
```

Recomputed stable summary hash equals `1c78a386...`; the contract remains `review_required=true` and `allowed_as_v551_relation_evidence=false` with the declared missing semantic/directional/structural authorities. This is **not** a full operational pass; preserve it.

Negative/restore:

```text
AR-0048 selected row removed: manual_override_used=false; basis/reason empty; contract hash 6dd4fa85be5c2640e8f810a64b8cf0b79fbf5637930f3730bf05cbfbaab4acf7
AR-0048 selected row duplicated: RuntimeError ambiguous manual override match ... source_wave_var_code: 2 rows
AR-0049 register absent: fallback missing_register; fields_joined=false; contract hash 919df24c41cd47d5a0e1edf1565887538e75262753ae44931d56f577e1911227; output a8010c5bb11f21936ca3796ab358abe069b27b7d41f11ced254f3259e1f5ac3b
AR-0047 GSS 1973 itinerary removed: review_priority=normal; contract hash 57cf755dde1d2a117eefc3565ed494b5f83cc578fb4c9a8c7c244d71ab7b994c
Restore exact bytes: output hash 1c78a386... equals positive
```

The positive/removal/duplication/missing-register/restore observations match the recorded JSON/log; no source, respondent, SAV/DTA/DB or native data was read.

## Accepted findings

- **C11A-01 — ACCEPT.** Authority byteidentity and exact historical consumer loading are verified: all four authority pins, QUC/source-structure module hashes, selected row and unchanged module import; no substantive monkeypatch.
- **C11A-02 — ACCEPT.** The selected GSS/1973/`uswar` row is real and the positive/negative/restore effects and hashes check. The contract remains `review_required=true`/`allowed_as_v551_relation_evidence=false`; no promotion.
- **C11A-03 — ACCEPT.** This is S2 test-time replay on **one** selected nonrespondent authority row, not an original historical run; one row does not prove all35 or actual original35 estate. AR-0050 is register-builder metadata only, not QUC runtime effect.

## Q4 — revise, do not manufacture repair or issuer gate

The author's Q4 says the current installed successor is not a QUC reader, no installed non-test `question_use`/itinerary/taxonomy reader was found, and a selected operation “would need a QUC reader.” That is a **name/path hypothesis**, not actual functional-responsibility proof. The current whole PRE-V3 may carry the responsibility outside `EmpiricalQuerySpec`/I03:

- C6-F08_Q_USE: historical QUC function; current owner/first consumer `UNKNOWN_NOT_PROVED`; current selected operation `NOT_RUN`/`UNPROVED_CURRENT_SELECTION`; no selected current QUC operation.
- C6-F06_RESP_CONTRACT: exact current generic refs `pre553_c11_ingest.py:644-659`, `pre553_source_backed_c11_facade.py:502-553`; response-contract responsibility, not QUC override/itinerary.
- C6-F09_ROUTING: exact current generic refs `pre553_c11_ingest.py:601-620`, `pre553_empirical_query.py:725-731`; routing/risk responsibility, not QUC.
- C4-O14_J_ROLE: `pre553_j_role_certification.py:356-388,1018-1027`; J role/component certification, a different responsibility.
- C3-FF: Q86/GT12 bounded canaries and GF1 test-only; no QUC responsibility.
- Current `EmpiricalQuerySpec`/I03 optional `TARGET_USE_PERMISSION` and governed frontier are valid current owners, but target-use alone neither proves a QUC equivalent nor a missing function.

**Result:** current QUC succession remains **`FUNCTION_CURRENT_BUT_AUTHORITY_PROVENANCE_UNPROVED`**. The author's `__NO_QUC_READER_IN_CURRENT_OWNER` suffix and “would need QUC reader” should be removed/qualified until an actual selected current operation and successor contract are established. No repair, QUC reader, engine or issuer gate is manufactured. This is a Q4 reporting/owner-check revision, not a rejection of Q3.

## Smallest necessary existing-owner action

The current C6 F08/Q_USE owner, together with the current C11/I03/frontier owners, should perform a focused read-only responsibility comparison against C6 F06/F09, C4 O14 J role, C3 FF and current owner implementations for exact semantic-role/routing/review/override responsibility. Record whether any actual selected current operation demands the exact historical QUC semantics:

- If none, preserve `FUNCTION_CURRENT_BUT_AUTHORITY_PROVENANCE_UNPROVED` / `NOT_RUN` and the existing holds.
- If a selected operation exists, route at the existing query/authority owner with the exact selected input.

No new QUC reader, engine, repair, issuer gate or architecture change.

## Limits and holds

- **Engineering:** exact historical code/authority replay on one nonrespondent authority row; no monkeypatch; effects/hashes check.
- **History:** selected bytes/row and historical code are real; actual original historical invocation remains `NOT_RUN`; one row does not prove all35.
- **Current authority:** Q4 current succession `UNPROVED`; current adoption not proved; contract remains `review_required=true`/`allowed_as_v551_relation_evidence=false`; AR-0050 is not QUC runtime proof.
- No source/respondent/SAV/DTA/DB read, source-byte copy, native/S3/science/actor effect, installation, production/existing-test/HQ/peer/protected write, CI, merge, delegation or environment/model change.
- Whole #777 remains incomplete; `goal_complete=false`; 17 agenda gates and all holds preserved; quota `UNKNOWN`.

**Checks performed (read-only):** `git -C source show 9ba…` for the four authority files and historical modules; `git -C source show 7639…` for the author return/TRACE/probe JSON/log; focused CSV row checks for GSS/1973/`uswar`; recomputation of the positive/negative/restore stable hashes; C6/C4/C3 pin inspection. No replay rerun and no full matrix.

**Review commit/remote readback:** reported in the terminal return after push; this file is in the same review-only commit.
