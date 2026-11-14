# ZAK-03S — adversarial author handoff / exact runtime hold

**Terminal grade:** `ZAK03S_EXACT_MISSING_EDGE_WITH_RUNTIME_HOLD`. **NOT S2 PASS.**  
**Protected base (live verified):** `integration/pre-main-reconciliation-r1@6a5c12f04323d74001f9632063ec907f4fc4468e`. No protected edit.  
**Isolated branch:** `agent/zak03s-current-rule-effect-20261114`; draft PR #1042.  
**Exact last code/test candidate:** `813e623845afcf2e9d9dfa201b55ffc0dfc03079`. Read the final PR HEAD for report-only successor SHA.

## 1 — Exact artifact

Added, and did not replace shared current producers:

| Path | Git blob at exact code/test candidate |
|---|---|
| `rawlsing_next/pre553_zak03s_selected_qsm_reader.py` | `07bd2b2c88787e8b2091e652c677864be2ba5244` |
| `rawlsing_next/tests/test_pre553_zak03s_selected_qsm_reader.py` | `b1223ce1f0e7b3da700e51428e79767ef60058fe` |
| `.github/workflows/zak03s-selected-qsm-sourcefree.yml` | `14c38a9ff4dd9781757d157c0d0594c17963cdd9` |

Actual intended runner commands (from repository root, Python 3.11 with `pytest pandas pyreadstat pyarrow duckdb`):

```bash
PYTHONPATH=. python -m pytest rawlsing_next/tests/test_pre553_zak03s_selected_qsm_reader.py -q -o addopts=''
PYTHONPATH=. python -m pytest rawlsing_next/tests/test_pre553_route_b_production.py data/ddm_build_copy/tests/test_r1_question_relation_authority.py -q -o addopts=''
```

## 2 — Governing contract and boundaries

New commission ZAK-03S directs **selected historical QSM/F03 resource/version/row → source + permission → governed C11 → actual I03/I05/Batch → real first reader**, positive/wrong-source/permission/restore, at authorized sourcefree grade. The ZAK-00 flight matrix at `e725ec39d021f4f7d8080298a95ea519ada2de01` assigns current Pyat authority application to ZAK-03; existing #903 at `7451042624a789ba4a93de2f3137a03305905373` remains the nine-obligation predecessor, not a waived contract. No claims of TASK-03/TASK-04/HOSTILE S2 or whole original35 conservation are inherited from #903.

Actual protected component sources inspected: legacy `data/ddm_build_copy/ddm_v550_question_relation_authority.py` Git blob `62084cbed10a5975f79bd504bf4fb99025e4e64e`; `rawlsing_next/pre553_route_b_production.py` blob `5b28d6c0c4f9bc032088cf660834ad574b8c8446`; `rawlsing_next/pre553_empirical_query.py` blob `b72b469e6646b88e4e2ed4dbbf0f3c209557fd69`. PYAT #909 R3/997/998/999 ongoing writer and native-source work remains separate.

## 3 — Strongest achieved and exact evidence grade

**Engineering implementation authored, NOT runtime demonstrated:** The optional `execute_selected_qsm_route_b` selects a caller-explicit QSM file (SHA-256 checked against index and again after operation), resolves one exact row/version/rule, rejects blocked dispositions, matches source/wave/country and native *same-code* response slot in the already governed C11 projection. It requires a separately positive **current** `TARGET_USE_PERMISSION` for each requested I03 query, including the exact triple in the original query's own dependency/authority closure; then it actually calls the existing `execute_route_b_production` in source, which calls C11 repository construction, I03 and I05, and ties the selected QSM file+row to its returned C11/I03/I05 receipt references. Existing direct-source and conditional paths remain intact.

The intended test creates two independent 700-row synthetic derivatives of the legacy calibration registry, checks A positive, B wrong-file/changed row and separately selected B identity, QSM blocked status, contradictory historical status, modern DENY, absent I03 target-use triple, exact physical variable mismatch and byte-equal restored outcome. These are **authored discriminatory tests, NOT executed successful tests**.

**Attempted hosted execution:** [ZAK03S run #43632091614](https://github.com/maidiu/rawlsing/actions/runs/43632091614) at code/test candidate `813e6238...`, initial failure and a genuine one-job rerun accepted as attempt 2. Latest attempt job `132561073903` completed FAILURE with `runner_id=0`, `steps=[]`. Initial job `132560736908` also FAILED with no assigned runner / zero steps. No pytest, compile, C11, I03, I05 or JUnit artifact ran. Independent [canonical-tree run #43632091622](https://github.com/maidiu/rawlsing/actions/runs/43632091622) at same SHA likewise failed before step 1 with runner_id 0, steps 0. Job log download returned `404 BlobNotFound` and no workflow artifacts exist. This is **runner-availability hold**, not evidence that any test passed or failed.

## 4 — Author's hostile findings and repairs

- A modern positive authority snapshot does not encode an actually selected historical QSM source: implemented explicit byte/row/version selection rather than snapshot-only acceptance.
- QSM question relation is not an I03 grammar or target-use permission: require a distinct existing current snapshot, do not translate the historical disposition into an ALLOW grant.
- Native C11 question refs are frozen semantic dictionaries in `EmpiricalQuerySpec`, not `ExactRef` objects: corrected exact conversion rather than incorrectly testing dict-vs-object membership.
- Caller-invented historical-to-native link risk: added exact match to source-native physical `ResponseSlotRule.slot.name` and the response QVB/universe, denying guessed aliases.
- Contradictory `relation_use_status` and negative `authority_status`: now checks *both* the resolution class and positively qualified historical disposition.
- Implicit `None`/blank historical selection could invoke the legacy default/environment path: forbidden explicitly.
- Cached historical index can be stale: requires its recorded file SHA to equal the selected bytes, and the selected file SHA remains unchanged after the real reader returns.

## 5 — Remaining exact challenges / necessary competent owners

1. **Runner:** obtain an actually working authorized execution surface and run the above commands. First inspect failed node(s), repair only reproduced defects, then record positive/wrong-source/permission/restore receipts at immutable HEAD. No claim may precede this.
2. **Source selection and rights:** fixture source is deliberately synthetic, derived from the 700-row legacy calibration register, not the live 18,518-row QSM production file or a historical operating process. The declared historical variable-to-native-ref is still only *same-code* evidence; non-identical historical aliases need a qualified source owner-issued exact mapping, not a heuristic.
3. **I05 and Batch:** Route-B executes I05 in source, but the selected QSM rule has **not** been inserted into I05's independently authorized grammar/frontier, nor Batch's actual issued-workload first consumer. A complete `I03/I05/Batch` selected-source production dependency is unproved. The receipt deliberately says `i05_historical_qsm_authority_established=False`.
4. **Currentness:** adapter is opt-in; existing direct legacy callers and the live R3 joined production path are not globally guarded. Their owner must decide the smallest noncolliding adoption point. Do not alter active S01–S05/997/998/999 writer modules from this branch.
5. **Claim levels:** original35/native selected production, full empirical/scientific source interpretation, SOROK/actor rights, native effects, independent ZAK receiving, protected branch CAS, and the nine original ZAK03 MCR-C obligation PASS statuses are separately held.

The old #903 architecture tuple question was **not used as a proxy for C11 failure**: the contents API presently cannot resolve commit `315251451a6d112fb312a6e80b096d345c5de6` while another reviewer reported a successful direct Git tree/blob check. Competent source-identity reconcilers should settle that separately, not redefine an actual runtime issue.

## 6 — Best independent attack surfaces

- Prove a forged selected file with syntactically valid 700/18,518 rows cannot manufacture a source grant; file SHA is integrity, **not source authority or external signature**.
- Challenge the QSM var-code → physical slot → QVB → I03 target relation in genuinely different source naming conventions; insist on an issuer instead of expanding an alias heuristic.
- Verify that the I03 target-use snapshot is genuinely effective/revocation-checked at the real reader; test a modern otherwise-plausible authority catalog without the required triple.
- Directly run the negative court against actual route and verify received fact/replay identities, not just the adapter sidecar; independently inspect I05 and Batch issuing/reading.
- Test mutable file/cache TOCTOU, same-mtime/same-size changes, source scope, negative state, domain zeros, weighted risk and original reader regression.

## 7 — Rejected alternatives

- **Modify I03 / source-backed C11 / Batch shared engine on a conflicting PYAT R3 lease**: violates writer ownership and risks working current semantics.
- **Treat old QSM row as new `TARGET_USE_PERMISSION` or `PREDICATE_GRAMMAR`**: illegitimate scientific/authority promotion.
- **Produce another 17-row atlas / ten unexecuted design-only negatives**: would repeat #903 and fail ZAK-03S's operational remit.
- **Make Field Forge, N9/N10W, Sorok or a mandatory physical serial C11 chain a prerequisite**: wrong DAG and outside the sourcefree edge.
- **Mark CI red as a failing test or CI invocation as S2 PASS**: jobs never acquired runners, so both claims are false.

## 8 — Proof boundaries and receiving request

**Actual currently proven:** authenticated GitHub source verification, a committed optional adapter/test/workflow source candidate, precise current-path static code linkage, actual GitHub Actions runner-unavailability receipt. **Not proven:** Python runtime compilation, four-case executions, real first-reader effect, Batch selected dependency, full semantic conservation, original historical source selection or independent receiving. The next agent should begin with a real executable host and direct test failures—not with another architecture atlas—and either graduate this exact adapter with observed evidence or supersede it with a demonstrably better owner-compatible connection.

**Terminal:** `ZAK03S_EXACT_MISSING_EDGE_WITH_RUNTIME_HOLD`.
