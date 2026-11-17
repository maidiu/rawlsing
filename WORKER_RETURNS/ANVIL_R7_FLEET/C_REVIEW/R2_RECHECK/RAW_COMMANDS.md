# R2 RAW COMMANDS AND EXITS

All R2 paths are under `WORKER_RETURNS/ANVIL_R7_FLEET/C_REVIEW/R2_RECHECK/`. R1 files are untouched.

## Target and archive

```text
git -C /Users/matthewsmith/Desktop/ANVIL_RABOCHII_EXECUTION_20261117/INTEGRATION rev-parse HEAD
e919cd6e637270951ab57c06c97a8fb7bf98107d
shasum -a 256 INTEGRATION/WORKER_RETURNS/ANVIL_R7_FLEET/INTEGRATION/REPAIRED_PACKAGE.zip
49750ae7a80cdeb84eefc8ec4b84fa7c8edefcbb10f5d29867a6d506cc71dae3  (1,812,248 bytes)
cp .../REPAIRED_PACKAGE.zip R2_RECHECK/INPUT/REPAIRED_PACKAGE_R2.zip
unzip -q R2_RECHECK/INPUT/REPAIRED_PACKAGE_R2.zip -d R2_RECHECK/COLD/FRESH_<stamp>
```

- Target worktree HEAD = `e919cd6`; target ZIP hash = Git blob hash = `49750a…`.
- Manifest rehash against the exact target root: **734/734**, 0 missing, 0 bad.
- Extracted fresh package has 336 files under `ANVIL_R7/`, including package-resident `EVIDENCE/` and `BUILT/`.

## Literal cold commands (from `COLD/FRESH_<stamp>/ANVIL_R7/tools`)

```text
python3 r7_inventory.py verify --source-root ../EVIDENCE/SOURCE_118 \
  --repo /Users/matthewsmith/s2b-work/rawlsing \
  --zip /Users/matthewsmith/Desktop/ANVIL_R7_INTEGRATED_WORKFLOW_FIX_20261117.zip \
  --inventory ../EVIDENCE/SOURCE_IDENTITY_INVENTORY.json
```
exit 0; `PASS_SOURCE_IDENTITY_INVENTORY_S1_DOCUMENTARY`; `GIT_AND_ZIP_PINS_VERIFIED`; 118; zero errors. Log `LOGS/literal_inventory.log`.

```text
python3 -m unittest test_r7_integrated -q
```
exit 0; `Ran 29 tests ... OK`. Log `LOGS/literal_29.log`.

```text
python3 test_integrated_strict.py
```
exit 0; `Ran 11 tests ... OK`. Log `LOGS/literal_11.log`.

```text
python3 r7_integrated.py FRAME ../EVIDENCE/FRAME.json --evidence-root ../EVIDENCE \
  --source-root ../EVIDENCE/SOURCE_118 --repo ... --zip ...
python3 r7_integrated.py DECISION ../EVIDENCE/DECISION.json ...
python3 r7_integrated.py C_INTEGRATED ../EVIDENCE/C.json ...
```
exit 0 for all three; statuses `PASS_LOCAL_COMMON_REQUIREMENTS_SOURCE_IDENTITY_NOT_NATIVE_AUTHENTICATED`, `PASS_LOCAL_INTEGRATED_DECISION_PENDING_C`, `PASS_LOCAL_C_PACKET_ONLY_INDEPENDENCE_UNVERIFIED`. Logs `LOGS/literal_{FRAME,DECISION,C_INTEGRATED}.log`.

```text
python3 r7_build.py verify ../EVIDENCE/DECISION.json --evidence-root ../EVIDENCE \
  --source-root ../EVIDENCE/SOURCE_118 --repo ... --zip ... --out ../BUILT
```
exit 0; `PASS_SIX_PROJECTIONS_BYTE_IDENTICAL`. Log `LOGS/literal_build.log`.

## R2 adversarial witnesses

All scripts use `R2_RECHECK/COLD/FRESH_<stamp>` and copy evidence into their own `R2_RECHECK/WITNESS/...` temp directory; they do not write R1.

```text
python3 WITNESS/w1_paraphrase.py
```
exit 0; `FRAME PASS`, `DECISION PASS` after alternative pairwise-only F4 and F6 guard-as-numeric text. `WITNESS/W1_PARAPHRASE/w1_result.json`; log `LOGS/w1_paraphrase.log`.

```text
python3 WITNESS/w2_paraphrase.py
```
exit 0; `C_INTEGRATED PASS` with alternative false T4/T6/T7 `SOURCE_STATIC_CONSERVED` prose. `WITNESS/W2_PARAPHRASE/w2_result.json`; log `LOGS/w2_paraphrase.log`.

```text
python3 WITNESS/w3_external_flag.py
```
exit 0; `C_INTEGRATED PASS` with self-asserted `EXTERNAL_RUNNER_VERIFIED` and fabricated receipt. `WITNESS/W3_EXTERNAL_FLAG/w3_result.json`; log `LOGS/w3_external_flag.log`.

```text
python3 WITNESS/w4_freeze_control.py
```
exit 0; FRAME RED `AUTHORED_SEMANTIC_SUMMARY_FREEZE_MISMATCH`; DECISION RED. `WITNESS/W4_FREEZE_CONTROL/w4_result.json`; log `LOGS/w4_freeze_control.log`.

```text
python3 WITNESS/w5_terminal_relabel.py
```
exit 0; F5 exact hold relabelled to generic consumer, C audit still exact hold; DECISION and C PASS. `WITNESS/W5_TERMINAL_RELABEL/w5_result.json`; log `LOGS/w5_terminal_relabel.log`.

```text
python3 WITNESS/w5b_disconnect.py
```
exit 0; F5 disconnected (0 incident edges), 2 filler edges added, counts still 43/58; DECISION and C PASS. `WITNESS/W5_DISCONNECT/w5b_result.json`; log `LOGS/w5b_disconnect.log`.

```text
python3 WITNESS/w6_projections.py
```
exit 0; 118 distinct identity meanings/negatives/effects/consumers/witnesses; 16 distinct requirements; 43/58 graph; full T fields; evidence/falsifier index; JSONL handoff with ABI/status/deps. `WITNESS/W6_PROJECTIONS/w6_result.json`; log `LOGS/w6_projections.log`.

## R1 custody

`git status` in the C_REVIEW worktree shows no modified/staged R1 files; the tracked R1 review content remains at frozen `6c70839a…`. The author’s `CUSTODY_INCIDENT.md` is read as an admission, not as technical evidence. R2 was reconstructed from the new ZIP, not from the incident or any dirty R1 timestamp.
