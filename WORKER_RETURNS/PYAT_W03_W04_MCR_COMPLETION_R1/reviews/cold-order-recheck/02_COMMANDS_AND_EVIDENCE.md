# CC-F01 cold-order recheck — commands and evidence

**Worktree:** `/Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat-w03-w04-mcr-combined-code-review-r1`
**Branch:** `review/pyat-w03-w04-cold-order-recheck-r1`
**Reviewed head:** `bcc176d7719e57d1e88b7f395f0280f72b0a74c5`
**Verdict:** `ACCEPT_AT_CC_F01_SCOPE`

All commands used an explicit `cd` into this worktree. Writes are confined to `WORKER_RETURNS/PYAT_W03_W04_MCR_COMPLETION_R1/reviews/cold-order-recheck/`; production/test/contract/HQ were read-only after the restored transient mutation.

## 1. Worktree and source

```sh
cd /Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat-w03-w04-mcr-combined-code-review-r1
git branch --show-current
git rev-parse HEAD
git status --short
git ls-tree -r --name-only HEAD rawlsing_next | wc -l
find rawlsing_next -type f | wc -l
```

Result:

```text
review/pyat-w03-w04-cold-order-recheck-r1
bcc176d7719e57d1e88b7f395f0280f72b0a74c5
clean before this review lease
406
406
```

Read: original review `07c172683c4a720b8d1c37599c3e09a5357e56d8`, frozen `PYAT_W03_W04_MCR_C_Commission.md`, and the 12-ID `REQUIRED_OBLIGATIONS.tsv` (12 unique IDs). This recheck changes none of their statuses.

## 2. Exact repair and blobs

```sh
git diff --name-status 26f70635e8493c7759fa087b17da269104bd8922..bcc176d7719e57d1e88b7f395f0280f72b0a74c5
git diff 26f70635e8493c7759fa087b17da269104bd8922..bcc176d7719e57d1e88b7f395f0280f72b0a74c5 -- rawlsing_next/_pre553_w03_cold_compact.py rawlsing_next/tests/test_pre553_w03_w04_cold.py
git hash-object rawlsing_next/_pre553_w03_cold_compact.py rawlsing_next/tests/test_pre553_w03_w04_cold.py
shasum -a 256 rawlsing_next/_pre553_w03_cold_compact.py rawlsing_next/tests/test_pre553_w03_w04_cold.py
```

Production change only:

```diff
- key: _RespondentEvents(lane, tuple(rows))
+ key: _RespondentEvents(
+     lane,
+     tuple(sorted(rows, key=lambda row: self.event_keys[row])),
+ )
```

Test change: adds real `_ReleaseIndex`/`_select_respondent_events`/`CarrierNeutralResearchExecutor` imports and `test_cold_selector_sequence_and_yield_match_eager` for the three fixtures.

Blobs/SHA-256:

```text
06eefd8fe8c1839854a783c78045b170627806f2  rawlsing_next/_pre553_w03_cold_compact.py
75314ade650f87c3e5aec0e17c9e31b9fe22b07c  rawlsing_next/tests/test_pre553_w03_w04_cold.py

bb0093fa0ad8f19e324f2ecd01cc1faad4e690f2152f6cb7316ee91b5a033e93  rawlsing_next/_pre553_w03_cold_compact.py
675ad4d5e014e81ab3db19ab45b30d62adfc4e2b4c356630cdb8883ebe88aeaa  rawlsing_next/tests/test_pre553_w03_w04_cold.py
```

Current blobs equal author commit `f9aedf8e2b570174881cef627dc6a24b78031ed7` and return `8f36fceb8fc518a8be03dfef6c32b4124f1d8867`; integrated at `0dc8ee923dddf75716c0e5ac227d90ca8cd1ab89` / `bcc176d7719e57d1e88b7f395f0280f72b0a74c5`.

## 3. Author ORDER_R3 receipts read

```sh
cat WORKER_RETURNS/PYAT_W03_W04_MCR_COMPLETION_R1/lanes/cold/ORDER_R3/00_REPAIR.md
cat WORKER_RETURNS/PYAT_W03_W04_MCR_COMPLETION_R1/lanes/cold/ORDER_R3/02_COMMANDS_AND_RESULTS.md
cat WORKER_RETURNS/PYAT_W03_W04_MCR_COMPLETION_R1/lanes/cold/ORDER_R3/03_HANDOFF.md
cat WORKER_RETURNS/PYAT_W03_W04_MCR_COMPLETION_R1/lanes/cold/ORDER_R3/proof_73_focused.txt
```

Read results:

- RED at intake: `event_sequence_parity=false`, `selector_yield_parity=false`, `selector_yield_differences=3`, `consumer_material_parity=true`.
- GREEN at candidate: true/true/0/true.
- Author focused receipts: 18 cold tests passed, 43 selected passed, 73 focused passed in 15.97s.
- The 73-test receipt was read, not independently rerun in full. Independent focused work below is proportionate for this one-line repair.

## 4. Current parity probe

```sh
cp WORKER_RETURNS/PYAT_W03_W04_MCR_COMPLETION_R1/reviews/combined-code/probes/cold_parity_probe.py \
  WORKER_RETURNS/PYAT_W03_W04_MCR_COMPLETION_R1/reviews/cold-order-recheck/probes/
TMPDIR="$PWD/$OUT/tmp" PYTHONPATH="$PWD" PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=0 \
python3 -B "$OUT/probes/cold_parity_probe.py"
```

Result (`logs/cold_parity_probe.stdout.json`, `probes/cold_parity_probe.json`):

```text
event_sequence_parity = true
selector_yield_parity = true
selector_yield_differences = 0
consumer_material_parity = true
release_equal/replay_equal/public_object_material_equal = true for all three fixtures
```

All three sourcefree fixtures: `routed-ordered-repeated`, `missing-optional-weight`, `valid-empty`.

## 5. Focused three-case new test and cold file

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=0 TMPDIR="$PWD/$OUT/tmp" \
python3 -B -m pytest -q -o addopts='' -p no:cacheprovider \
  rawlsing_next/tests/test_pre553_w03_w04_cold.py::test_cold_selector_sequence_and_yield_match_eager
```

Result: **3 passed in 1.23s** (`logs/new_three_case_post_restore.log`; initial run also 3 passed in `logs/new_three_case.log`).

```sh
python3 -B -m pytest -q -o addopts='' -p no:cacheprovider \
  rawlsing_next/tests/test_pre553_w03_w04_cold.py
```

Result: **18 passed in 3.64s** after restore (`logs/cold_file_post_restore.log`; initial run `logs/cold_file.log`, 18 passed).

The new test compares every respondent's exact event-ref sequence, actual `_select_respondent_events` yields for every native-question target, and full typed I03/I05 consumer material through the real executor. It is not a hand-built oracle.

## 6. Assertion-level severance and restoration

Temporary mutation in the review checkout only (never committed):

```diff
- tuple(sorted(rows, key=lambda row: self.event_keys[row]))
+ tuple(rows)
```

Commands/result:

```sh
python3 -B -m pytest ... test_pre553_w03_w04_cold.py::test_cold_selector_sequence_and_yield_match_eager
# 3 failed by assertion: cold_refs == eager_refs

python3 -B "$OUT/probes/cold_parity_probe.py"
# event_sequence_parity=false, selector_yield_parity=false,
# selector_yield_differences=3, consumer_material_parity=true
```

Then:

```sh
git checkout -- rawlsing_next/_pre553_w03_cold_compact.py
git hash-object rawlsing_next/_pre553_w03_cold_compact.py
# 06eefd8fe8c1839854a783c78045b170627806f2
git status --short -- rawlsing_next
# empty
```

Post-restore: new test **3 passed**, cold file **18 passed**, parity probe true/true/0/true. See `logs/severance_mutation.txt`, `logs/severance_new_test.log`, `logs/severance_parity_probe.stdout.json`, `logs/source_identity_after_restore.log`.

## 7. Meaning, topology, refs and materialization

- Sort key is the already-frozen exact event ref key string in `self.event_keys`; no ref reconstruction or mutation.
- Only integer row indices are sorted; selectors, compressed bodies, `entries`, `non_events`, event states, release/replay/coverage are unchanged.
- `_RespondentEvents` remains `(lane, rows)`; no event body/event graph materialization added.
- Ordered/repeated, missing-weight and empty fixtures preserve full typed I03/I05 consumer material.
- No second store, query engine, semantic rule, cache format or authority introduced.

## 8. Existing proof-integrity gate

```sh
python3 CROSS_HQ_CONTROL_ROOM/proof_integrity_gate_r1.py lint rawlsing_next/tests/test_pre553_w03_w04_cold.py
# AST_LINT_PASS

python3 CROSS_HQ_CONTROL_ROOM/proof_integrity_gate_r1.py changed \
  --base 26f70635e8493c7759fa087b17da269104bd8922 \
  --head bcc176d7719e57d1e88b7f395f0280f72b0a74c5 --root .
# MECHANICAL_PROOF_GATE_PASS_NOT_SCIENTIFIC_ADOPTION; 0 witness contracts
```

The new test does not independently require a `.proof.json` sidecar under the existing gate. No sidecar was quietly waived. Existing CC-F04 benchmark-sidecar work remains queued outside this lease.

## 9. Boundary and hashes

- No W04 F01/F02/F03 reopening; no old coupling bypass/caller-path investigation; no CC-F02/CC-F05 work; no CC-F03/CC-F04 repair.
- No 100k benchmark, no final 12-ID/economic receiving, no original35/SAV/DTA/DB/source bytes, native/S3/science/actor effect, install, protected merge, CI waiver, new engine/worker, model/provider/account/effort change.
- Final same-SHA code/economic receiving with all 12 proof records remains pending.
- `logs/review_hashes.log` records SHA-256 of this review, findings, logs/probes and exact source/test blobs.

**Final:** `ACCEPT_AT_CC_F01_SCOPE` at `bcc176d7719e57d1e88b7f395f0280f72b0a74c5`; exact sort, real selector/yield parity, full typed consumer parity and assertion-level severance/restoration verified. No whole MCR/economic acceptance.
