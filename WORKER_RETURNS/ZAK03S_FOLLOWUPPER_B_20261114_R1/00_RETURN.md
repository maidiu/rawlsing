# ZAK-03S — Agent B independent correction and challenge

**Terminal engineering grade:** `ZAK03S_EXACT_MISSING_EDGE_WITH_RUNTIME_HOLD`. This is a committed, inspectable correction to Agent A's optional sourcefree adapter, **not** S2 PASS, operational acceptance, a new selected source/science issuance, native original35 evidence, or protected integration.

**Protected branch verified:** `integration/pre-main-reconciliation-r1@6a5c12f04323d74001f9632063ec907f4fc4468e` (no change).
**Inherited Agent A:** draft PR [#1042](https://github.com/maidiu/rawlsing/pull/1042) at `ad17076cc95b9383ab3b28879f471026bcba9ff7`.
**Independent B branch:** `agent/zak03s-followupper-b-20261114-r1`; the immutable final head is the PR's exact `head_sha`, after this report commit.
**Pre-report B code/test head:** `7164b51239ebd7080b3a07470253e5ae51c7e870`; 5 fast-forward commits beyond A, 0 behind.
**Revised code/test Git blobs:** adapter `d3c6c4e8a32398a3c4977ed287684bd95d058df3`; tests `5ef5ae473420dd314256898e44c10cb3b9821741`; workflow `1a1bde8d5c3860d2c9441abb2bcd005309db53b8`.

## 1. Reconstructed commission, independent of A

The user-issued ZAK-03S commission requires **selected historical QSM/F03 artifact + exact row/version -> applicable historical rule and source/use permission -> actual governed C11 -> I03/I05/Batch -> real importing current reader -> observed changed outcome/refusal**, with positive, genuinely different resource, permission denial, and exact restoration on a functioning runner. Historical and current authority are separate owners. A candidate file, plausible snapshot, test design, sidecar hash or C11 builder body cannot substitute for an executed end-to-end edge.

ZAK-00's exact flight-owner matrix at `e725ec39d021f4f7d8080298a95ea519ada2de01`, `WORKER_RETURNS/VMESTYE_ZAK00_V2_MCR_AUTHOR_EXECUTION_20261110_R1/03_FULL_FLIGHT_DEPENDENCY_AND_OWNER_MAP.md` assigns current authority application to ZAK-03 and distinguishes separate first-reader/functional-conservation closure. Required predecessor `WORKER_RETURNS/VMESTYE_ZAK03_MCR_R1/00_RETURN.md@7451042624a789ba4a93de2f3137a03305905373` preserves nine frozen obligations and marks S2 first-reader and negative executions NOT_RUN; it is S0–S1 author testimony, not a terminal claim.

Protected actual owners: historical `data/ddm_build_copy/ddm_v550_question_relation_authority.py` blob `62084cbed10a5975f79bd504bf4fb99025e4e64e`; current Route-B `rawlsing_next/pre553_route_b_production.py` blob `5b28d6c0c4f9bc032088cf660834ad574b8c8446`; current empirical I03 `rawlsing_next/pre553_empirical_query.py` blob `b72b469e6646b88e4e2ed4dbbf0f3c209557fd69`; actual issued-workload/Batch caller `rawlsing_next/pre553_issued_workload.py` blob `28174766f61a15f7296f575d615462d6410cfcb6`, particularly `execute_issued_workload` around lines 280–367. The issued-workload caller invokes Route-B, separately builds C11, executes I03/I05 with Batch and rechecks current issuance. It **does not consume Agent A's new selected QSM binding**, and no sourcefree execution or production adoption has proved otherwise.

## 2. Agent A strengths independently verified

- Explicit selected-path + exact historical file SHA, exact resolved QSM row hash/rule/version and source/wave/country checks; no environment/default fallback.
- Distinct separately positive modern `TARGET_USE_PERMISSION` in the current I03 query's declared target-use triple and authority/dependency closures. No attempt to convert historical QSM relation status to an I03 permission or discovery grammar.
- Unchanged Route-B/source-backed C11/I03/I05 owners; no overwrite of active PYAT R3 S01–S05 writers. Sourcefree candidate is **opt-in**, not a global guard.
- Original A test suite has real Route-B fixtures and meaningful proposed wrong-file, blocked disposition, modern permission DENY, restore and I05 checks. They were authored but **never executed** at S2.

## 3. Consequential B defects established and fixes

**B-01 — Single-row authority laundering into multi-target requests.** A's `_exact_selection` matched one historical row and then checked merely `selection.native_question_ref in query.target_refs`. A valid I03 F4 `(X, Y)` request could therefore pass the Y-only preflight even though no selected QSM row had qualified X. It similarly checked universe membership rather than the entire queried universe set. **Correction:** this explicit one-row adapter requires the exact singleton target and exact singleton universe, leaving the independent Route-B/fully qualified joint engine untouched. A different joint target requires separately qualified selected rows/issued mapping, not a fabricated one-row authority.

**B-02 — Historical question identity was not bound.** A checked `row.var_code == physical_slot.name` and a caller-provided native QVB ref, but did not constrain `row.question_id`: two different historical questions sharing physical `var_code=Y` could inherit the same I03 Y execution and a purported historical lineage. **Correction:** require a separate exact `historical_question_id` in `SelectedQsmRequest`, verify against the selected row, and refuse `question_id != var_code` within this *same-code-only* adapter unless a competent separate question-to-variable mapping is supplied elsewhere. This may refuse legitimate mismatched-code sources; that is an explicit source-mapping hold, not an assertion the historical registry is invalid.

**B-03 — Producer misrepresented as a first importing reader.** A's binding receipt labeled `execute_route_b_production` as `reader`. In fact that function builds C11/I03/I05 while `execute_issued_workload` is the separately current issued-workload/Batch operation; it does not import or bind the new QSM wrapper. **Correction:** rename receipt field to `invoked_current_producer`; explicitly set `selected_binding_first_importing_reader=NOT_PROVED` and `issued_batch_consumption_of_selected_qsm=False`. No fake successful first consumer.

These are precise source-level implementation deltas, not proof of runtime effectiveness. All existing accepted Route-B, I03, I05, Batch code and scientific/rights semantics are unmodified.

## 4. Tests and evidence — exact grade

**Original A authored tests, not executed:** 700-row synthetic selected A/B identity, wrong file hash, wrong row/version/rule, historical denial, current permission denial, exact restore and real-route sourcefree fixture.

**New B authored tests, not executed:**
- `test_same_variable_but_different_historical_question_id_cannot_be_laundered`: synthetic history uses `question_id=OTHER-QUESTION, var_code=Y`; first the unchanged historical-question request must refuse, then changing the caller's asserted historical ID must still refuse the absent issuer-supplied mapping.
- `test_one_historical_row_cannot_authorize_unselected_joint_question`: a valid constructed I03 `(X,Y)` request under the modern catalog must refuse at the one-row historical Y gate; baseline single-target request remains a positive fixture.
- Existing positive fixture now checks explicit first-reader and issued-Batch nonpromotion in the binding receipt.

**Runnable intended commands** from the repository root with Python 3.11 and `pytest pandas pyreadstat pyarrow duckdb` installed:

```bash
PYTHONPATH=. python -m pytest rawlsing_next/tests/test_pre553_zak03s_selected_qsm_reader.py -q -o addopts=''
PYTHONPATH=. python -m pytest rawlsing_next/tests/test_pre553_route_b_production.py data/ddm_build_copy/tests/test_r1_question_relation_authority.py -q -o addopts=''
```

**Attempted actual execution:** [Agent B hosted run #43634055876](https://github.com/maidiu/rawlsing/actions/runs/43634055876), branch commit `c2a4d8ace1868aa618f846fea3afd06d653bcc02`, completed FAILURE with `steps=[]` and **zero artifacts**. It never executed Python or pytest; no GREEN or test-specific RED can be claimed. Additional B branch pushes invoke the same workflow but are not proof unless a job executes. Agent A's original hosted run #43632091614 likewise returned failure without steps, including its third rerun. A runner/unavailable-execution hold remains, not a Python result.

## 5. Self-hostile check, rejected attacks, and regressions

- **Conceded:** A correctly separated QSM relation use from modern permission, and rejected a duplicate C11 engine. B preserves those decisions.
- **Not a defect:** a different QSM file with a separately qualified positive row can yield the same RAW I03 fact while having a different historical binding receipt. Identical measured facts are not alone a false source provenance claim; the *real importer* and actual causal dependence are the missing proof.
- **Not an invented architecture failure:** the ZAK-03 historical source-pointer dispute from #903 is distinct from actual execution; it does not authorize changing source law or replacing the C11 engine.
- **New B limitation:** `question_id != var_code` now refuses rather than guesses. If a legitimate native source uses different labels, an exact issued mapping and a separately exercised test must be supplied by the appropriate source owner.
- **New B limitation:** a one-row QSM adapter cannot carry an F4 multi-question historical-qualification chain. A separately selected complete set of historical question relations is required for that claim. Existing independent I03 joint query behavior is not changed.
- **Potential execution unknown:** new tests could expose API/schema mistakes when a genuine runner starts. This report does not claim syntactic compilation or test PASS from static inspection. Any resulting error should be repaired at this branch's exact frozen code scope, not by broad changes to active PYAT R3.

## 6. Real remaining gates and strongest challenge to Agent A

1. **Genuine execution:** run the original A + new B sourcefree positive, different historical source, wrong authorization and restoration cases, and the inherited Route-B tests on a working authorized runner; record exact log, output and executable SHA. Repair any observed test failure.
2. **Real consumer:** demonstrate a normal, externally admissible `execute_issued_workload`/Batch run that **consumes the selected QSM source/row/version and can be severed by changing that selection while holding other relevant inputs fixed**. B's wrapper by itself does not prove this. Preserve current external `CurrentDecisionResolver` source/host/purpose/currentness checks.
3. **Real source semantics:** secure issuer-qualified historical question ID → actual native QVB mapping and source rights when same-code synthetic coverage is not the proper scope. Do not forge a QSM-to-I03 authority grant from checksum consistency.
4. **I05 authority:** if claimed, prove the separate selected-source rule is valid for the actual discovery grammar/frontier; do not silently infer I05 lineage merely because Route-B executes I05.
5. **Independent acceptance:** exact-HEAD nonauthor receiving, preserved nine frozen predecessor obligations, separate engineering/science/authority grades and no protected branch merge by this B return.

## 7. Return and stop

Engineering: improved **static, sourcefree, unexecuted** adapter/test candidate; no S2 runtime PASS. Science: no new issuance. Authority: no historical source/actor/reviewer/integration grant. Native-original35 and whole-machine-zero-loss: not claimed. ZAK-01's user-admitted scoped evidence preserved, not recommissioned.

**Terminal:** `ZAK03S_EXACT_MISSING_EDGE_WITH_RUNTIME_HOLD`.
