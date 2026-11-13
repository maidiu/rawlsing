# PYAT960 Q2 S1-E — G5 independent nonauthor receiving

**Role:** G5_INDEPENDENT_NONAUTHOR_RECEIVER · **session:** `ses_e30a442d8ffeYBbXi7rPUpPxoc`
**Decision:** `REVISE_EXACT_DEFECT` · **G5:** `FAIL` · **Integration:** `UNMERGED`
**Original task:** Q2 S1-E/P1-06/P1-07 — bounded source-direct handoff.

## 1. Exact artifact and refs

| Item | Value |
|---|---|
| Base composition | `591056a948fb0fdd68adbd581301dd903485adc8` |
| Delivery | `24e6bc02536a0714b0ab94a225f8eef1d84d8127` |
| Code/test cut | `f6fcd708f8cb8b8fc32bb7f6b9745b3676910be7` |
| Contract v1 SHA-256 | `0ed0384411441b2f647dc5ea3369931c88d408c71802ec8cd7eaff00c3052a40` |
| Provisional ABI SHA-256 | `cbc8988b6f38fc354311d7db7afe02a5bd66c8e53ab2c6f9cca2b5134d383f54` |
| A implementation | `75d09e87dbaf8273fab3a5ece2bb7981328113ce` |
| B delivery / code cut | `ed9bda50ec1c1cbbc0ced56262a696b65fb14dad` / `9987a00e10dbb4e2dca7032b7d66a90e2303c780` |
| A counter | `f6fcd708f8cb8b8fc32bb7f6b9745b3676910be7` |
| Review branch | `agent/pyat960-s1e-g5-r1` |

`delivery` changes only `WORKER_RETURNS/PYAT960_S1E_A_COUNTER/` after the code cut. I wrote only `WORKER_RETURNS/PYAT960_S1E_G5/`; no candidate code, tests, upstream owners, earlier returns, controller or protected path was edited. Q3/S2-C was not launched or resumed.

## 2. What is real

- **Direct I02 positive/change/restore PASS.** Real generated SAV/DTA → bounded decoder → R157 projection → one bounded cell pass/spool → existing `build_sourcefree_direct_i02` → `ExternalI02Roots`; changed response meaning changes roots/event refs; restore reproduces them. Q2 handoff performs zero full C11 builds.
- **13-family body tee PASS.** `SourceI02BodySink/Tee` delivers the exact 13 families during the same one-shot builder consumption; no second source read; typed absences/finish/abort/failure cleanup tested.
- **Operation/fate anti-join largely PASS.** 22 operations, 8 ELIGIBLE/14 HELD; multiowner response+coordinate routing now fails closed when routing is unknown; partial routing preserves typed HOLD; source/operation/occurrence/target/duplicate negatives refuse before source; wrong source bytes refuse with no output; missing output receipts are typed HOLD.
- **Native selector PASS.** Q2 certificate selectors drive 5/5 exact native event refs on the existing Linux `s2b` runner; S2-B external/direct/verified native suites 81 passed.
- **G4 Q2-handoff fixture grade PASS.** 1,200 rows/events/coordinates; one fixture source snapshot, one decode, one cell pass, one direct builder, zero full C11; spool 7,464,000B cleaned; certificate 19,353,600B; peak disk 46,190,901B; peak process RSS 133,267,456B; cold 5.616829s/repeat 5.718084s; denied-read source opens 0; body transport 4,809 objects/13 families. 100k/6GiB NOT_RUN.
- **All35 ledger exact:** 35 sources / 18,276 original items / 18,413 physical slots / 26 unjoined preparation-held; sha256 `b9a83189e41800618d76ad191e33b2c97b754c45cd01df11286a5ba91a11ca89`.
- Tests: Q2 33 passed/1 skipped Darwin, 34 passed Linux; S2-B native 81; S1-C 18; S1-B 33; decoder/custody 56/1; G3 focused 21; G2 focused 11.

## 3. Material G2 defect — the claimed Q2 native fact is a legacy-body comparator

**Command:** `PYTHONPATH=$PWD python3 WORKER_RETURNS/PYAT960_S1E_G5/g5_lineage_measure_probe.py` and the Linux body-independence probe.

**Input:** sourcefree q101 nonrespondent SAV; `test_pyat960_s1e_native_fact._build_native` / `native_fact_probe.py`.

**Expected:** native I03/Batch fact driven by the Q2 direct I02 body/body tee and an actual issued S1-C operation/fate, with one Q2 source read; or an explicit `G2_NATIVE_I03_BATCH_CONSUMER=HOLD_DEPENDENCY`.

**Observed:**
- The test helper calls `decode_fixture_config` a second time and `build_validated_c11_release_from_config` to create a **legacy full `C11LogicalRelease`**, then uses it as the native repository. Counts: `snapshot=2`, `decode_fixture=1`, `legacy_build=1`; Q2 handoff reports `source_reads=1`, `full_c11_builds=0`, `body_transport=None`.
- The Q2 body tee is not consumed by the native reader. Running the same native fact with and without a `body_sink` produces the **identical** fact ref and raw 5/5; the body sink had 5 events but did not affect the fact.
- All 22 Q2 `operation_fates` have `issued_receipt_refs=()` and `native_first_reader_state=HOLD_DEPENDENCY_LINUX_PROC_SELF_FD_AND_SEALED_BODY_RELEASE`; the native query is `BRANCH-q2-native`, not a frontier operation ID.
- The Linux fact result 5/5 → 3/3 → exact 5/5 is real, but it is a **legacy-body comparator** with Q2 selectors, not the Q2 body/issued-operation native fact.

**First-reader consequence:** a SUPPORTED fact can be produced even if the Q2 body tee is absent/wrong; the fact does not prove the Q2 direct-body/issued-operation handoff. This is a false green at G2, not merely a claim nuance.

**Owner:** `test_pyat960_s1e_native_fact.py::_build_native`, `native_fact_probe.py`, `_pre553_external_i02_certificate.py::install_direct_sourcefree_i02_i03/_DiskSelectedRespondent`.

**Minimal correction:** either build a real Q2 body repository from the body tee/Q3 producer and execute the native fact from an actual issued S1-C operation/fate (changed Q2 body changes fact; restore exact), or mark `Q2_G2_NATIVE_I03_BATCH_CONSUMER=HOLD_DEPENDENCY`, relabel the current result as a legacy comparator, and count its second source snapshot and one legacy full build in G4. Do not claim actual Q2 native fact from the comparator.

## 4. Material G1/G3 defect — optional-weight RAW fate loss

**Command:** `PYTHONPATH=$PWD python3 WORKER_RETURNS/PYAT960_S1E_G5/g5_lineage_measure_probe.py`.

**Input:** sourcefree q101 fixture frontier: 16 `SAMPLE`, 6 `POPULATION` operations.

**Expected:** every operation/fate row preserves `measure_kind`/`measure_id` (and `weight_ref`/`estimand`/design where applicable), so SAMPLE RAW vs population/weighted fates survive the no-drop ledger.

**Observed:** `handoff.operation_fates` rows expose only `claim_class`, disposition, execution/result state, `source_preimage`, `source_realization`, `source_realized`, `issued_receipt_refs`, `native_first_reader_state`, `routing_unresolved_keys`, `unrealized_keys`; `measure_kind`, `measure_id`, `weight_ref`, `estimand`, `design_ref` are absent. The authored `test_s1e_output_collision_and_optional_weight_raw_conservation` checks only `frontier.operations`, not the handoff, so it does not prove optional-weight RAW nonloss.

**First-reader consequence:** a Q3/S2-D consumer cannot distinguish SAMPLE RAW from population/weighted operations from the handoff and may apply the wrong estimator/denominator.

**Owner:** `rawlsing_next/pre553_source_i02_handoff.py::_operation_source_antijoin` row/source_preimage.

**Minimal correction:** carry the measure/weight/estimand determinants in the fate row or source preimage and add a test asserting the 16 SAMPLE / 6 POPULATION distinction in `handoff.operation_fates`.

## 5. G1 reuse-matrix defect

`WORKER_RETURNS/PYAT960_S1E_B/reuse_matrix.json` has 14 entries but omits four owners imported by the Q2 handoff:

- `rawlsing_next/pre553_c11_ingest.py` blob `37cd35fa2e3420a3eea272a2902e96ab9ba38aba` (`SourceReleaseManifest`, `INGEST_CONTRACT_VERSION`);
- `rawlsing_next/pre553_c11_integrity.py` blob `7c59aa13a2b7c8e3ab0dc90a1400df645b0b4bbd` (`TypedAbsence`);
- `rawlsing_next/pre553_empirical_objects.py` blob `a61365b994e5c3c50de0f598fcf40e90abf757b6` (canonical objects);
- `rawlsing_next/universal_grammar/types.py` blob `e7b196efe5b1f86134c27a80bfdd8f472be76e5d` (`SourceInventory`, `ScientificFrontier`, `GrammarPolicy`).

The G1 reuse court is not complete until each has a function-level path/blob/disposition/first-consumer/no-loss/reason entry. This is a return/ABI documentation correction, not optional hardening.

## 6. Passed G3 negatives and G4 disclosure

- Multiowner response+coordinate with all `ROUTING_UNKNOWN` refuses pre-source; eligible multiowner retained.
- Partial routing: 6 operation HOLD rows; corrected TEST_ONLY fixture native query returns `UNAVAILABLE/RISK_SET_UNAVAILABLE`, no false SUPPORTED fact.
- Wrong source bytes → `SourceI02Refusal DECODED_SOURCE_SHA_MISMATCH`, no output.
- Duplicate operation/census omission/occurrence/slot/target/authority negatives refuse; missing output receipt is typed HOLD.
- Body tee exact 13 families/4,809 objects at 1,200 rows; no second source read; finish/abort/error cleanup tests pass.
- Original path prehash+snapshot=2; keyed path external key-witness read; disclosed. Sourcefree fixture path one pass.
- Native comparator extra resource: 2 source snapshots and 1 legacy full C11 build; must be counted/labelled (G2 defect).

## 7. Upstream, science, authority holds

- S1-C `dae66cdf...` and S2-B `155cd1b...` independent G5 remain pending; #980 combined receiving pending. Q2 does not self-accept upstream.
- S1-B accepted prior at `dedd2fb8...`.
- Original35 source/science/respondent/source-read entitlement HOLD; only generated nonrespondent SAV/DTA and TEST_ONLY operation/source-decision/U/Epre preimages used.
- Production S1-D CURRENT issuer HOLD; no production permission minted.
- Q3 S2-C remains **USER_PAUSED**; no writer, resume or Q2 body estate. S2-D all-consumer/resume outside this canary.
- Protected merge HOLD; integration UNMERGED; 100k/6GiB NOT_RUN; W03/W04 paused.

## 8. Three courts

- **Engineering:** direct I02/body tee/selector comparator and hostile repairs are substantive, but native fact lineage, optional-weight fate retention, and the G1 reuse matrix fail.
- **Science:** sourcefree TEST_ONLY q101 nonrespondent canary; routing-authority-kind/canonical-spelling corrections are disclosed engineering preimages; no original35 science or source execution.
- **Authority:** upstream S1-C/S2-B/#980 G5, original35/source, production CURRENT, protected merge, Q3/S2-D and integrated resource holds remain separate.

## 9. Decision

`REVISE_EXACT_DEFECT` at delivery `24e6bc02536a0714b0ab94a225f8eef1d84d8127` / code cut `f6fcd708f8cb8b8fc32bb7f6b9745b3676910be7`. G5 is **FAIL**. Direct I02/body tee/selector comparator are not accepted as full original Q2 S1-E because G2 native lineage and G3 optional-weight conservation are materially incomplete and the G1 reuse court is incomplete. No `ACCEPT_SCOPED`, no protected merge, no Q3/S2-C resume, no original35 claim.

One bounded correction under HQ should address the three exact cases above, then submit the new immutable SHA for fresh nonauthor G5. Stop finite; no new A/B duel, optional hardening, Q3 writer or 100k matrix.

Evidence: `WORKER_RETURNS/PYAT960_S1E_G5/evidence/` including `lineage-measure.json`, `lineage-measure-linux.txt`, `native-body-independence.txt`, `native-fact-linux.txt`, `native-selector-linux.txt`, `partial-routing-native.txt`, `wrong-source-bytes.txt`, test logs, `resource.json`, `all35_ledger.json`, `reuse_matrix_gap.json`, `refs.json`.
