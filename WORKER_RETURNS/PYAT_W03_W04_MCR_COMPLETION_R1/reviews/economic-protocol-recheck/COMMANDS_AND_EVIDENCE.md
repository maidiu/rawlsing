# COMMANDS AND EVIDENCE — W03/W04 economic protocol recheck R2

All local commands were run with an explicit:

```text
cd /Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat-w03-w04-mcr-economics-review-r1
```

or with an exact `git -C /Users/matthewsmith/Desktop/Rawlsing_Worktrees/...` for read-only ref inspection. No production, test, workflow, author, peer, HQ, or protected file was edited. `.DS_Store` at the worktree root was left untouched and uncommitted.

## 1. Exact refs and frozen inputs

```text
git rev-parse --abbrev-ref HEAD
git rev-parse HEAD
git rev-parse 9a71d0a0825c142372e56ac5d6bd34847ce6f227
git rev-parse 58a8c56c98058bd4606a3195e2a0ae955343f218
git rev-parse 46b7325637e68f78ccc7487d4b1abc7009c5ac0b
git rev-parse 4f3413fc5c37b589be3412f826bf8f68ee617d4a
git rev-parse 5a891a311c70f4cb8c09864008b33405362f7c7c
git rev-parse HEAD:rawlsing_next/bench_w03_w04_physical.py
git rev-parse HEAD:rawlsing_next/tests/test_bench_w03_w04_physical.py
shasum -a 256 rawlsing_next/bench_w03_w04_physical.py rawlsing_next/tests/test_bench_w03_w04_physical.py
shasum -a 256 PYAT_W03_W04_MCR_C_Commission.md WORKER_COMMISSIONS/PYAT_W03_W04_MCR_COMPLETION_R1/REQUIRED_OBLIGATIONS.tsv CROSS_HQ_CONTROL_ROOM/verify_copy_paste_commission_r1.py WORKER_COMMISSIONS/PYAT_W03_W04_MCR_COMPLETION_R1/MCR_EXECUTABLE_LAUNCH.md
```

Recorded in `PROBE/source_and_evidence_hashes.txt` and `EVIDENCE_AUTHOR_R4/refs.txt`.

Exact source/return current state:

```text
review HEAD: 1c428d59dc53cb76a19c1502a74cfd3bba00a899
repair code/test: 9a71d0a0825c142372e56ac5d6bd34847ce6f227
return/evidence: 58a8c56c98058bd4606a3195e2a0ae955343f218
bench blob: 6c72f7d67c16fe79b9260032f6ace4085c6f1f3d
test blob: f2573109d032cd306b4790b009d5dcaaa9094b00
bench sha256: d4fbce68af10f8cfa7b84f513322053cfa4e4e83e070d8358c05cf7ad55ad4cc
test sha256: c6dd3aa11a25743b5a6489b79a2665443b749fbd6a03275cb53770a2ffe0cdd2
```

I read the full frozen commission, exact 12-ID TSV, MCR wrapper and launch presentation, latest `PROTOCOL_R4` return/correction matrix/evidence/commands, all six `RED_GREEN` groups, the tiny 8-row 3-repeat pair, actual code/test diff, and the prior `economic-method-recheck` counterexamples. The wrapper is documentary/source-blob format validation only; it does not self-certify completion.

## 2. Focused test suite

```text
cd /Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat-w03-w04-mcr-economics-review-r1
TMPDIR="$PWD/WORKER_RETURNS/PYAT_W03_W04_MCR_COMPLETION_R1/reviews/economic-protocol-recheck/PROBE/TMP" \
PYTHONDONTWRITEBYTECODE=1 \
python3 -m pytest -q -o addopts='' -p no:cacheprovider \
  rawlsing_next/tests/test_bench_w03_w04_physical.py
```

Observed: `21 passed in 26.11s` (`PROBE/bench_21.log`). The original 13 names are preserved; the new tests cover the six repaired groups.

## 3. Independent inherited-policy cold probe

A valid foreign policy was created under the review lease, then used for a 16-row cold run:

```text
RAWLSING_C11_ACCELERATOR_POLICY="$L/env_policy/accelerator-policy.json" \
  PYTHONDONTWRITEBYTECODE=1 \
  python3 -m rawlsing_next.bench_w03_w04_physical \
  --scenario cold --profiles narrow --rows 16 --repetitions 1 \
  --source-root . --root "$L/env_cold_root" \
  --jsonpath "$L/env_cold_16.json"
```

Observed `PROBE/env_cold_16.json`:

```text
env_isolation: parent_policy_env_present_before_strip=true,
               parent_policy_env_stripped=true,
               policy_env_present_after_isolation=false
derived_cache_files=0
derived_status=NO_GOVERNED_DERIVED_CACHE_WRITE
derived_cache_hit=false
foreign_files=[]
```

The prior hidden-policy cache was not written.

## 4. Tiny 8-row pair gate audit

Read-only Python audit of:

```text
EVIDENCE_AUTHOR_R4/baseline_protected_4f_8_full_matrix.json
EVIDENCE_AUTHOR_R4/current_r4_8_full_matrix.json
```

calling `bench_w03_w04_physical._acceptance_gate` with the current invocation/command, `rows=8`, `repetitions=3`, profiles narrow/wide/repeat, scenarios cold/full-matrix, cap 6 GiB, and the external baseline sha256.

Output `PROBE/gate_tiny_audit.txt`:

```text
status=FAIL_OR_INCOMPLETE
pass=false
final_shape=false
cap_pass=true
cold_pass=true
warm_pass=true
regression_pass=true
identity=all true
event_fingerprint_parity=true (6 comparisons)
repeat_wall_ratio=0.7904743171961152
retention_decision=RETAIN_FOR_REPEAT
```

The `pass=false` is only `final_shape=false` for 8 rows; no tiny PASS is claimed. The current warm launch-to-firstconsumer is `0.736052836 s`; baseline protected cold is `0.969928935 s`; current whole parent `1.566364076 s` and canonical reopen `0.435092948 s` are not used by the gate.

The tiny pair also records external baseline sha256 `b35d5bf2842ebe2f971bcdbdb17b453bc9069a19f31af19ab33fe7ffe4b8e7f1`. The gate's own `baseline_file_sha256_matches` is self-consistency; final receiving must independently pin that external b35. In the audit, a same-source/event baseline with one changed metric and its own self-hash still passed the gate's identity fields (only `final_shape=false` kept it from a pass), so the external b35 pin is a final-receiving condition, not merely a gate self-check.

## 5. Exact prior negative probes against the new code

`PROBE/negative_probe_audit.txt`:

```text
NO_CAP_PROBE: cap_pass=false, pass=false, cap gate present
UNRESOLVED_REGRESSION: pass=false, regression_pass=false,
                       unresolved record ratio=1.2
RESOLVED_REGRESSION: regression_pass=true, resolved record present,
                     pass=false only because final_shape=false
MISSING_IDENTITY: pass=false; command/event/fingerprint/hash fields fail
BODY_CORRUPTION: derived_hit=false, derived_write=true,
                 status=MISS_WRITE_VALIDATED_BY_EXISTING_WRITE_BOUNDARY,
                 read_valid=[false]
```

The 8 MiB author probe (`EVIDENCE_AUTHOR_R4/cap_probe.json`) is:

```text
status=BLOCKED_EXACT_DEPENDENCY
cap_bytes=8388608
cap_enforced=true
cap_monitor_active=true
cap_peak_sampled_bytes=15245312
acceptance_cap_pass=false
cap_method=PARENT_SAMPLED_RSS_KILL_NOT_HARD_MEMORY_GUARANTEE
```

The same-size/same-mtime body corruption probe (`EVIDENCE_AUTHOR_R4/derived_corruption_probe.json`) records a miss/write and invalid read. I accept the R4 non-body-parquet-byte caveat as legitimate logical cache identity at the existing read owner; actual body/envelope content corruption does not count as HIT.

## 6. Amortization / retention audit

From `EVIDENCE_AUTHOR_R4/tiny_pair_summary.json` / current receipts:

```text
narrow: derived_write_wall=1.041248655 s, bytes=60117,
        break_even_warm_restarts=4.993116228
repeat: derived_write_wall=0.982727714 s, bytes=77208,
        break_even_warm_restarts=3.792296093
wide:   derived_write_wall=1.302380194 s, bytes=77484,
        break_even_warm_restarts=10.645039574
tiny retention field: RETAIN_FOR_REPEAT
```

This is a diagnostic 8-row receipt, not a final retention or economic result. The tiny pair is `final_shape=false`/`pass=false`. The old 64-row RED (`38.99%` / warm `1.447` / `DO_NOT_RETAIN`) remains preserved in the prior review and is not substituted by this tiny pair. No optimization at 8 rows.

## 7. Source/test/workflow integrity

```text
git status --porcelain=v1
```

showed only `.DS_Store` and the new `reviews/economic-protocol-recheck/` lease. `git diff -- rawlsing_next/bench_w03_w04_physical.py rawlsing_next/tests/test_bench_w03_w04_physical.py .github/workflows/pyat-w03-w04-physical-economy.yml` was empty after probes; no source/test/workflow edits. The current HEAD bench/test blobs equal `9a71d0a`; the 1c CI-trigger fix did not change the bench.

## 8. Not run

No 100k matrix, no final three-profile three-repetition matrix, no original source/respondent/SAV/DTA/DB/native workload, no installs, subworkers, merge, protected adoption, or model/provider/account/effort/region change. The proof/CC-F04 and 1c trigger work are independent and not reopened.

Final receiving must occur at the same immutable SHA for both code and economic receivers, with full 12-ID coverage and external SHA-bound MCR evidence. This review qualifies the method only.
