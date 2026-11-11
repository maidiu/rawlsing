# CC-F01 cold respondent-order recheck

**Review:** focused independent nonauthor recheck of CC-F01 only.
**Exact worktree:** `/Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat-w03-w04-mcr-combined-code-review-r1`
**Branch/head:** `review/pyat-w03-w04-cold-order-recheck-r1` at `bcc176d7719e57d1e88b7f395f0280f72b0a74c5`; source tree 406 files, clean.
**Verdict:** **`ACCEPT_AT_CC_F01_SCOPE`**.

The production repair is the exact one-line ordering change requested by the prior review. It sorts only integer row indices inside each respondent group by the already-frozen exact event ref key. The new three-case test compares real `events_by_respondent` sequences, actual `_select_respondent_events` yields, and full typed I03/I05 consumer material against eager. Current focused tests pass; a temporary restoration of the pre-repair unsorted expression makes the new test fail by assertion, and restoring the exact candidate source makes it pass again. No lost topology, mutable ref, lazy-representation change, new avoidable materialization, or second engine was found.

This is **not** whole W03/W04, 12-ID MCR, economic, source/native/science/actor or protected acceptance. CC-F02/CC-F05 are active elsewhere; CC-F03/CC-F04 remain queued; none was reopened here.

## 1. Exact source identity and diff

- Prior independent review: `07c172683c4a720b8d1c37599c3e09a5357e56d8` at `2959dda3c95b05db40a399d6d746401f434f5a38`.
- Repair intake: `26f70635e8493c7759fa087b17da269104bd8922`.
- Author production/test commit: `f9aedf8e2b570174881cef627dc6a24b78031ed7`; return: `8f36fceb8fc518a8be03dfef6c32b4124f1d8867`.
- Integrated commits: `0dc8ee923dddf75716c0e5ac227d90ca8cd1ab89`, `bcc176d7719e57d1e88b7f395f0280f72b0a74c5`.
- Current production/test blobs match the author commit and return:
```text
06eefd8fe8c1839854a783c78045b170627806f2  rawlsing_next/_pre553_w03_cold_compact.py
75314ade650f87c3e5aec0e17c9e31b9fe22b07c  rawlsing_next/tests/test_pre553_w03_w04_cold.py
```
- SHA-256:
```text
bb0093fa0ad8f19e324f2ecd01cc1faad4e690f2152f6cb7316ee91b5a033e93  rawlsing_next/_pre553_w03_cold_compact.py
675ad4d5e014e81ab3db19ab45b30d62adfc4e2b4c356630cdb8883ebe88aeaa  rawlsing_next/tests/test_pre553_w03_w04_cold.py
```
- Production diff is only:
```diff
- key: _RespondentEvents(lane, tuple(rows))
+ key: _RespondentEvents(
+     lane,
+     tuple(sorted(rows, key=lambda row: self.event_keys[row])),
+ )
```
- Test diff adds the imported real selector/repository/executor and `test_cold_selector_sequence_and_yield_match_eager` with three sourcefree fixtures. No other production/test file changed in the repair range.

The frozen 12-ID contract and TSV were read; this recheck does not alter their status. Original 43-pass and prior compact blobs remain bounded prior capital.

## 2. Independent current GREEN evidence

Current parity probe (copied into this review lease; sourcefree S2):

```text
event_sequence_parity = true
selector_yield_parity = true
selector_yield_differences = 0
consumer_material_parity = true
release_equal/replay_equal/public_object_material_equal = true for all three fixtures
```

The probe covers `routed-ordered-repeated`, `missing-optional-weight`, and `valid-empty`. The new three-case test:

```sh
pytest ... test_pre553_w03_w04_cold.py::test_cold_selector_sequence_and_yield_match_eager
# 3 passed
```

Full focused cold file (no full 73 matrix):

```sh
pytest ... test_pre553_w03_w04_cold.py
# 18 passed
```

The test iterates every universe/respondent, compares exact event-ref sequences, compares `_select_respondent_events` for every native-question target present, and compares full typed consumer material via real `CarrierNeutralResearchExecutor` I03/I05. It does not use a hand-built statistical oracle.

Author RED/GREEN receipts were read from `lanes/cold/ORDER_R3/probes/`: RED `event_sequence_parity=false`, `selector_yield_parity=false`, `selector_yield_differences=3`, consumer parity true; GREEN true/true/0/true. The author 73-test receipt was read (`73 passed`); it was not independently rerun in full because the focused 18-case cold court plus the three-case new test is proportionate for this one-line repair.

## 3. Meaning, topology, refs and materialization

- The sort key is `self.event_keys[row]`, an already-frozen exact event ref key string. No ref is reconstructed or mutated.
- Only integer row indices are sorted; `_EventLane`, selectors, compressed bodies, `entries`, `non_events`, event states and release/replay/coverage are untouched.
- `_RespondentEvents` remains the same lazy `(lane, rows)` representation; the repair does not materialize event bodies or a full event graph.
- The selector still returns the same events; only the group sequence now matches eager. The ordered/repeated, missing-weight and valid-empty fixtures preserve full typed consumer material.
- No second C11 store, query engine, semantic rule, cache format or authority was added.

## 4. Assertion-level severance and restoration

Temporary source mutation in the review checkout only: replace the candidate expression with the exact pre-repair defect:

```diff
- tuple(sorted(rows, key=lambda row: self.event_keys[row]))
+ tuple(rows)
```

Under that mutation:
- `test_cold_selector_sequence_and_yield_match_eager`: **3 failed by assertion** (`cold_refs == eager_refs`).
- Parity probe: `event_sequence_parity=false`, `selector_yield_parity=false`, `selector_yield_differences=3`, consumer parity true.

Restored with `git checkout -- rawlsing_next/_pre553_w03_cold_compact.py`:
- production blob returned to `06eefd8fe8c1839854a783c78045b170627806f2`;
- source status clean (only this review lease untracked);
- post-restore new three-case test **3 passed**; full cold file **18 passed**; post-restore parity probe true/true/0/true.

This demonstrates the new test is assertion-meaningful and the production repair is the active cause of GREEN.

## 5. Proof gate and residuals

`CROSS_HQ_CONTROL_ROOM/proof_integrity_gate_r1.py lint rawlsing_next/tests/test_pre553_w03_w04_cold.py` passes AST lint. `changed --base 26f70635e... --head bcc176d77... --root .` examines the new cold test only and returns `MECHANICAL_PROOF_GATE_PASS_NOT_SCIENTIFIC_ADOPTION` with zero witness contracts. The new test does **not** independently require a sidecar record once it is named/classified as it is; no sidecar was quietly waived. The existing benchmark-integration proof residual (CC-F04) remains queued and outside this lease; it was not reopened or waived.

Boundary:
- No W04 F01/F02/F03 reopening; no old coupling bypass/caller-path investigation.
- No CC-F02/CC-F05 work; no CC-F03/CC-F04 repair.
- No 100k benchmark, no final 12-ID or economic receiving, no original35/SAV/DTA/DB/source bytes, no native/S3/science/actor effect, no installs, no protected merge, no CI waiver, no new engine/worker, no model/provider/account/effort change.
- Final same-SHA code/economic receiving with all 12 proof records remains pending.

## 6. Review output and commit

Writes are confined to `WORKER_RETURNS/PYAT_W03_W04_MCR_COMPLETION_R1/reviews/cold-order-recheck/`. Production/test/contract/HQ files are read-only after restore. Actual model is the existing OpenCode Go DeepSeek V4.1 Flash MAX; no change.

**Final:** `ACCEPT_AT_CC_F01_SCOPE` at `bcc176d7719e57d1e88b7f395f0280f72b0a74c5`; exact production sort, real selector/yield parity, full typed consumer parity, and assertion-level severance/restoration all verified. No whole MCR/economic acceptance.
