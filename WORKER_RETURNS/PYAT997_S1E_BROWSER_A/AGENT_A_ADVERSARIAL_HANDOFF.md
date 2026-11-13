# PYAT #997 — Browser A adversarial handoff

**Status:** AUTHOR_CANDIDATE_UNRECEIVED; ALL NEW TESTS UNEXECUTED; P0 / P1 G5 NOT_RUN. Original35 and protected merge untouched.

## 1 — Exact artifact and commands

Draft PR: https://github.com/maidiu/rawlsing/pull/1014
Author branch: agent/pyat997-s1e-browser-a-20261113-r1
Frozen code/test candidate before this handoff: 2346f313c589a8f8f5426735ea98ce9f8ca19060
Base accepted S2-D source: 9d96a9cac7d10f59f2c30d8045dd1696fa3ab969; inherited S2-C accepted code b7b697b69f0acea12174937ee824c19ac34ac284.
Transplanted accepted Q2 producer and original tests from 8b51dc8f1dd5bb622dda8bad3b11f6c5d703da94, Git blobs preserved exactly; no frozen S2-C/D writer or reader code edited.

New source:
- rawlsing_next/pre553_source_saved_body_bridge.py (P0)
- rawlsing_next/pre553_source_postconsumer_receipts.py (P1)

New tests:
- rawlsing_next/tests/test_pyat997_s1e_source_saved_body_bridge.py
- rawlsing_next/tests/test_pyat997_s1e_saved_native_first_consumer.py

Runnable workflow: .github/workflows/pyat997-s1e-browser-a.yml.

Install Python 3.11+, pytest, pyarrow, duckdb, pandas, pyreadstat. Run:

    python -m py_compile rawlsing_next/pre553_source_saved_body_bridge.py rawlsing_next/pre553_source_postconsumer_receipts.py

    python -B -m pytest -q -o addopts='' -p no:cacheprovider rawlsing_next/tests/test_pyat997_s1e_source_saved_body_bridge.py rawlsing_next/tests/test_pyat997_s1e_saved_native_first_consumer.py rawlsing_next/tests/test_pyat960_s1e_source_i02.py rawlsing_next/tests/test_pyat960_s1e_body_transport.py rawlsing_next/tests/test_pre553_source_direct_parquet_estate.py rawlsing_next/tests/test_pre553_direct_estate_i03.py

Run other inherited Q2 and S2-D hostile tests also, not as substitutes for above native joined test.

## 2 — Governing contract

#997 current November 13 phased P0 then P1, #918 S1-E, #909 R3C/R3S, PROGRAMMA PYAT, Oct28 source-direct selected architecture and MCR-lite. P0: real Q2 one physical source SAV/DTA snapshot/decode/cellpass, ALL 13 original typed family bodies into unchanged S2-C physical C11, source/I02/replay/manifest roots intact, cold true native first readers and changed source value/restore. Counts-only are not bodies. P1: authentic S1-C source/science operation dispositions joined to independently issued S1-D and real saved native Batch/I03/I05 output receipts. All HELD/UNKNOWN/DEFERRED/INAPPLICABLE/unavailable/pending/optional weight RAW axes retained. Original35 source/right/issuer holds separate, no 100k/6GiB from tiny fixtures, no new owner/engine.

## 3 — Strongest implemented candidate (not claimed executed)

P0: SourceSavedBodySink implements existing Q2 SourceI02BodySink. The existing source tee sends each original canonical object to this sink and direct I02 on ONE projection pass. This new module serializes exact 13 typed objects to 0700 private family JSONL via the accepted carrier object serializer; after Q2 physical I02 and complete source/fate transport, verifies certified Q2 physical digest/headers/replay/source/universe/census/typed absences, replays the 13 original body iterators into unchanged accepted write_direct_estate(expected_i02=Q2 roots), and destroys temporary journal after atomic success/failure. S2-C necessarily re-certifies I02 a second time on the bodies. This is a second BODY journal pass, not a second source decode or a competing saved corpus.

P1: join_saved_source_operation_fates is read-only to Q2. It requires accepted S2-D SavedC11Admission, exact current sourcefree issued workload/decision, exact Batch manifest, real typed executed receipts and actual native I03/I05 reexecution parity. For discovery, uses ORIGINAL R03 native_receipt_anti_join and candidate IDs to map distinct native discovery receipt refs to S1-C operation expected-candidate identities; separately retains the actual Batch receipt ref. Batch COMPLETED alone never marks all operations. Unexecuted/HELD/UNKNOWN remain pending/nonpositive.

Tests authored for SAV/DTA full 13 families, one-source snapshot, exact I02, cold event body, changed/restore, body missing, root/current refusal; native S1-C I03/I05/Batch/issued normal, authentic fate join, receipt pending and mixed-source refusal. These tests are NOT yet a successful execution.

## 4 — Self-hostile findings and repairs

- Q2 family statistics cannot be replayed as S2-C bodies. Added a true body transport, no second decoder.
- P0 one-source-pass must not be misrepresented as one I02 proof pass. Frozen S2-C performs a second verification and private journal costs disk.
- First P1 draft naively assumed per-operation QUERY jobs. Actual S1-C issues shared DISCOVERY: repaired by deriving per-operation receipt from R03 original candidate no-drop anti-join and exact native I05 receipts, not from shared Batch completion.
- Generic sourcefree fixture inventory_id depended on Python object address and could defeat exact cross-run restore. Native test stabilizes that inventory id for baseline/change/restore.
- Hosted CI fails with zero executed job steps and no test log; DO NOT claim green or failed Python assertions. Example latest https://github.com/maidiu/rawlsing/actions/runs/43505215337.

## 5 — Unresolved challenges

No authorized Python+PyArrow repository runner available in this session; GitHub Actions kills jobs before any steps. Therefore no newly executed positive, hostile, changed/restore or resource proof at candidate SHA, no independent G5. Most urgent real proof: does the journal roundtrip match ALL Q2 logical and physical I02 roots at actual cold source and actual native I03/I05/Batch? If not, repair precise ABI/root mismatch without rewriting S2-C. Actual process-tree RSS, peak scratch/temp bytes, source-open counts, physical retained bytes, native outputs and complete postconsumer anti-join have not been *measured*. The source code carries counters and tests, which do not count as results. No 100k DISTINCT respondents/6GiB run. Original35 rights/host/QSM/Epre and integrated source-native psychology remain OPEN.

## 6 — Highest-value Browser B attacks

1. Actual Q2→journal→S2-C second direct-I02 physical SHA and replay hash determinism under SAV, DTA, typed absence, repeated occurrence, optional-weight RAW, corpus bounds.
2. Truncate or corrupt body journal, drop/duplicate one member with equal-count manipulation or self-rehash; force wrong source/release/current pin and test refusal before any fact.
3. Test Q2 rollback after certificate published but S2-C write fails; ensure no valid-looking partially persisted release.
4. Run actual native S1-C / S2-D I03, I05, Batch and issued/resumed normal/COMPLETED/PARTIAL/ABSENT with current recheck, denominator/counterpattern conservation.
5. Attack source-operation-issuer anti-join: duplicate operations, fake HELD, missing native candidate or issued receipt, forged Batch completion, mixed released source, stale/revoked current; never promote invalid row.
6. Measure 13 family yields, temp journal/spool bytes, source read opens, process-tree RSS/peak staging, cold latency and duplicate I02 certification cost.
7. Check per-operation discovery candidate semantic mapping and any overlap across operations; correct real overissuance without suppressing legitimate shared candidate evidence.
8. Confirm exact inherited Q2 and S2-C/D blob preservation. PR against protected contains accepted previously unmerged S2-C/D ancestry; no automatic merge.

## 7 — Rejected alternatives

Counts-only handoff (no bodies); re-decoding SAV/DTA or constructing a full resident C11 graph (one-source requirement/resource violation); second physical Parquet/SQL authority corpus or new writer/issuer (owner violation); universal completion from one Batch receipt (scientific lie); using test-only fixture as original35 scientific grant (authority lie); treating zero-step red CI as an in-code assertion failure or as a green execution (proof lie).

## 8 — Proof boundary and next action

STATUS: AUTHOR_CANDIDATE_CODE_COMMITTED; P0_NATIVE_POSITIVE_NOT_EXECUTED; P1_OPERATION_JOIN_NOT_EXECUTED; INDEPENDENT_G5_NOT_RUN; ORIGINAL35_SOURCE_RIGHTS_HELD; PROTECTED_UNMERGED.

Browser B: FIRST obtain an actual authorized runner and execute the above focused/inherited tests, including true native first consumers. Independently inspect/repair a concrete defect in the same source descendant. Then submit a frozen tested SHA for separate nonauthor G5. Do not add a new architecture or checklist campaign, and do not count code/green author assertions as scientific acceptance.
