# Reproduce M04

Use the assigned local sparse worktree and existing authenticated Git store with the pinned objects. Python 3.11 and pytest were already available. No install, source respondent material, remote model or production actor is required. Run from repository root.

The `repro/` M03 Python files and `candidate/` files are exact pinned M03 copies; they are retained for reproduction, not authored or repaired by this reviewer. `review/` contains the new reviewer code. Do not use the copied M03 `repro/audit.py` as this court's verdict: it describes its author return and expects its author seal. Use `review/audit_review.py`.

Bootstrap from absent/reconstructed `runtime/`:

```sh
python3 WORKER_RETURNS/SOROK-R3-HQ314-M04-M03-INDEPENDENT-R1/repro/stage_independent.py
python3 WORKER_RETURNS/SOROK-R3-HQ314-M04-M03-INDEPENDENT-R1/repro/run.py before original_413
python3 WORKER_RETURNS/SOROK-R3-HQ314-M04-M03-INDEPENDENT-R1/repro/run.py before independent_100
python3 WORKER_RETURNS/SOROK-R3-HQ314-M04-M03-INDEPENDENT-R1/repro/install_candidate.py
python3 WORKER_RETURNS/SOROK-R3-HQ314-M04-M03-INDEPENDENT-R1/repro/run.py after original_413
python3 WORKER_RETURNS/SOROK-R3-HQ314-M04-M03-INDEPENDENT-R1/repro/run.py after independent_100
python3 WORKER_RETURNS/SOROK-R3-HQ314-M04-M03-INDEPENDENT-R1/repro/run_author.py
python3 WORKER_RETURNS/SOROK-R3-HQ314-M04-M03-INDEPENDENT-R1/repro/run_historical.py
python3 WORKER_RETURNS/SOROK-R3-HQ314-M04-M03-INDEPENDENT-R1/review/run_fresh.py
python3 WORKER_RETURNS/SOROK-R3-HQ314-M04-M03-INDEPENDENT-R1/review/audit_review.py
```

Fresh pytest exits **1**, with 41 PASS / 10 FAIL; preserve that exit, and proceed to the independent evidence audit as a separate command. Historical child pytest also exits **1**, with exactly nine literal failures; its wrapper validates that identity/count rather than calling them passes. Baseline independent100 child exits **1** with two failures; its wrapper records the real child exit/count. Final published tests all exit zero. The audit checks exact expected recorded counts and byte custody; `M04_AUDIT_OK` means evidence consistency, never a successful implementation acceptance.

Two bootstrap attempts failed before tests because the inherited staging scripts assume a fixed directory depth for Git path filters. The reviewer wrapper adds `--full-tree` only to Git `ls-tree` in its generated local tool wrapper; it changes no Git objects, scientific source, test or oracle. Exact published staging and test source bytes remain unchanged. The first failure and correction are documented under evidence. Reconstruction uses only pinned Git source, not the earlier author sessions' files. The ignored generated `toolbin/` script contains host paths and is not portable evidence.

`run_fresh.py` checks the frozen test SHA-256 against the pre-execution commit manifest, disables pytest plugin autoload and cache, records exact child command and exit, and produces the same 51-case JUnit plus full stdout. Review evidence contains synthetic state only. Metadata sanitization preserves assertion/results while replacing local personal paths/hostname; raw metadata is retained in ignored runtime storage with raw/portable digest receipts. To recreate portable evidence after reruns, run `review/package_return.py` after the audit.

The return's source index, test preimages and import audit bind original source commits/blobs to actually executed module files. `candidate/` is an exact copy of the reviewed M03 candidate. No reviewer patch is proposed. Remote verification records a pushed content commit, followed by a receipt-only commit; the last direct remote check and final SHA are reported in the chat because a file cannot embed its own Git commit hash.
