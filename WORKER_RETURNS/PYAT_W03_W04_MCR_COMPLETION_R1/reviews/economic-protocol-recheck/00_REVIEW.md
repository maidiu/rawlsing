# 00_REVIEW — W03/W04 economic protocol recheck R2 at `9a71d0a`

**Method verdict:** `METHOD_READY_FOR_PINNED_FULL_SCALE` — scoped to the benchmark method only. This is **not** whole-economic or 12-ID acceptance, and no 100k matrix was run.

**Reviewer:** original independent economics/memory receiver; not the implementation author.
**Review turn:** `opencode-go/deepseek-v4.1-flash#max` (unchanged).
**Review branch / exact checkout:** `review/pyat-w03-w04-economic-protocol-recheck-r2` at `1c428d59dc53cb76a19c1502a74cfd3bba00a899`.
**Review lease:** `WORKER_RETURNS/PYAT_W03_W04_MCR_COMPLETION_R1/reviews/economic-protocol-recheck/`.

## 1. Exact refs and read evidence

- Input economic review: `5c963bfee0c31f0d1e2794978296f101e804f395` (original `REVISE_METHOD`; preserved, not rewritten).
- Repair code/test: `9a71d0a0825c142372e56ac5d6bd34847ce6f227`; return/evidence: `58a8c56c98058bd4606a3195e2a0ae955343f218`.
- Current integrated checkout: `1c428d59dc53cb76a19c1502a74cfd3bba00a899`.
- Current bench/test blobs are unchanged from `9a71d0a`: `6c72f7d67c16fe79b9260032f6ace4085c6f1f3d` and `f2573109d032cd306b4790b009d5dcaaa9094b00`.
- Bench/test sha256: `d4fbce68af10f8cfa7b84f513322053cfa4e4e83e070d8358c05cf7ad55ad4cc` and `c6dd3aa11a25743b5a6489b79a2665443b749fbd6a03275cb53770a2ffe0cdd2`.
- Frozen PR895 `46b7325637e68f78ccc7487d4b1abc7009c5ac0b`; protected baseline `4f3413fc5c37b589be3412f826bf8f68ee617d4a`.
- Frozen commission sha256 `ddc6273adcc9aeb1b7e75c7d82897dde929adffea152e7f57dc5254fa32f0166`; exact 12-ID TSV source `5a891a311c70f4cb8c09864008b33405362f7c7c`, sha256 `5de8d68207de353926bd2d42095a8c8c44a36b06ac4038a7c9b16a1b6173428e`.
- MCR wrapper `CROSS_HQ_CONTROL_ROOM/verify_copy_paste_commission_r1.py` sha256 `ea1edef49b0f11bcc36e45d6cf9f59fdfc1d2fac9684b920df6aa6d9dcb7218a`; launch presentation `MCR_EXECUTABLE_LAUNCH.md` sha256 `c25dbb96259971a8f623179dd1435bcdc2d684edb2b02a4970565bbb0c5c25e7`. The wrapper is documentary/format/source-blob validation only; it does not self-certify completion.
- Actual source/test diff from prior review to `9a71d0a` is `EVIDENCE_AUTHOR_R4/actual_code_and_test.diff` (sha256 `ca41416f208728425db444c971c8a3eb11b0fd0eba38d43439dbc27e3d5c78f8`).
- `PROTOCOL_R4` return, correction matrix, evidence, commands, `RED_GREEN.json`, tiny pair summary, and the three core probes are copied under `EVIDENCE_AUTHOR_R4/` with exact hashes. The raw 8-row pair receipts remain at `baseline_protected_4f_8_full_matrix.json` (sha256 `b35d5bf2842ebe2f971bcdbdb17b453bc9069a19f31af19ab33fe7ffe4b8e7f1`) and `current_r4_8_full_matrix.json` (sha256 `946d722744c5c9862acbd29f75e68c62b44d9d7a227aa4f1d610ec7d00c06617`).

I read the full frozen commission, exact TSV, MCR wrapper/launch, latest `PROTOCOL_R4` return/matrix/evidence/commands, all six `RED_GREEN` groups, the tiny 8-row 3-repeat pair, the actual code/test diff, and the prior `economic-method-recheck` counterexamples. I did **not** reopen ECON-M2.

## 2. Six-group disposition

### ECON-M1 — inherited-policy isolation: `CORRECTED / GREEN`

The cold/cells child path clears `RAWLSING_C11_ACCELERATOR_POLICY` and `RAWLSING_C11_ACCELERATOR_DIR` in both the launcher and worker (`bench_w03_w04_physical.py:663-698, 837-845`). The author's `env_isolation_probe.json` has parent policy present, stripped, foreign file count 0, derived status `NO_GOVERNED_DERIVED_CACHE_WRITE`; the full-matrix test uses its own qualified root and leaves the foreign root untouched.

My independent 16-row inherited-policy probe reproduced: parent policy stripped, `policy_env_present_after_isolation=false`, `derived_cache_files=0`, `derived_status=NO_GOVERNED_DERIVED_CACHE_WRITE`, no foreign derived file. Evidence: `PROBE/env_cold_16.json`, `EVIDENCE_AUTHOR_R4/env_isolation_probe.json`.

### ECON-M2 — stage RSS separation: `PRESERVED / GREEN`; not reopened

The repaired sampled current-RSS stage peaks, separate process `ru_maxrss`, combined-boundary labelling, and aliases remain unchanged. I did not re-open this item; the focused suite is 21/21.

### ECON-M3 — active sampled cap monitor: `CORRECTED / GREEN`

The 21-test file includes `test_acceptance_gate_requires_active_cap_evidence`. The gate now requires all runs to have `cap_enforced=true`, `cap_monitor_active=true`, the declared `cap_bytes`, a sampled peak `<= cap_bytes`, and no blocked run (`bench_w03_w04_physical.py:1219-1261, 1341-1349, 1424-1429`). The 8 MiB `cap_probe.json` is `BLOCKED_EXACT_DEPENDENCY`, `cap_enforced=true`, `cap_peak_sampled_bytes=15,245,312`, `acceptance_cap_pass=false`; the tiny 8×3 pair is `cap_pass=true` with peaks below 6 GiB. The method is explicitly `PARENT_SAMPLED_RSS_KILL_NOT_HARD_MEMORY_GUARANTEE`, not a hard-memory claim. This is the truthful sampled bound requested; final 100k must still demonstrate no overshoot and 6 GiB behavior.

### ECON-M4 regressions — `CORRECTED / GREEN`

The gate now records all >10% cold/full-matrix profile RSS/wall regressions and distinguishes resolved from unresolved (`bench_w03_w04_physical.py:1406-1429, 1295-1321`). A synthetic 20% other-profile regression fails unresolved; an explicit `JUSTIFIED_CORRECTION` record with justification/correction makes `regression_pass=true` and retains `receiving_required=true`. The frozen 15% cold / 90% repeat thresholds remain; the tiny pair has no unresolved regressions.

My independent probe (`PROBE/negative_probe_audit.txt`) reproduced: unresolved case `regression_pass=false`, explicit resolution `regression_pass=true` (overall gate still false only because `final_shape=false`). No universal regression ban remains; no tiny PASS.

### ECON-M4 clock — `CORRECTED / GREEN`

The child records `firstconsumer_completed_monotonic_ns` after the normal derived first consumer; the parent records launch monotonic before `Popen` and derives `launch_to_firstconsumer_seconds` (`bench_w03_w04_physical.py:618-647, 837-946`). Canonical reopen/consumer is after that marker. The gate uses `median_launch_to_firstconsumer_seconds`, not whole-parent wall (`:1399-1404`).

Tiny pair audit: current warm launch `0.736052836 s`, baseline protected cold `0.969928935 s`, gate ratio `0.7904743171961152`; current whole parent is `1.566364076 s` with canonical reopen `0.435092948 s`, which is **not** used for the gate. `EVIDENCE_AUTHOR_R4/tiny_pair_summary.json` and `PROBE/gate_tiny_audit.txt` confirm.

### ECON-M4 identity — `CORRECTED / GREEN` with an explicit final-receiving condition

The tiny pair identity has all fields true: protected 4f source, method sha256, command parameter identity, actual event counts, full consumer fingerprints (6 comparisons), host, rows, profiles, repetitions, and the external baseline file sha256 `b35d5bf2842ebe2f971bcdbdb17b453bc9069a19f31af19ab33fe7ffe4b8e7f1`. Missing events/commands/hash fail; a wrong external hash fails; a same-source/event baseline with a modified metric and its own self-hash still passes the gate's **self-consistency** but is not an independently pinned external hash.

That last point is a **final-receiving condition, not a method blocker**: the tiny pair summary records the external `b35...` hash and the final receiver must independently compare it. The gate's `baseline_file_sha256_matches` alone is only self-consistency; final receiving must pin the external b35 in the same immutable SHA/lockstep as engineering receiving. No new architecture or production change is requested. Events/fingerprint/method/command identity itself is green.

### ECON-M5 write cost and hit truth — `CORRECTED / GREEN`

- Actual existing `_read_bodies`/`_write_compact_bodies` boundaries are observed without semantic replacement (`bench_w03_w04_physical.py:451-615`); derived-write wall, CPU, bytes and read-validation wall are measured.
- Tiny pair: derived writes are actual (`narrow 1.041248655 s / 60,117 B`, `wide 1.302380194 s / 77,484 B`, `repeat 0.982727714 s / 77,208 B`); canonical persistence is separate; `derived_write_amortization_receipt` uses measured restart savings and actual write cost, not `canonical_persist/repeat_count`.
- Hit truth: `derived_hit` is `read_observations` validity, not filename/size/mtime. The body-page same-size/same-mtime corruption probe returns `derived_hit=false`, `derived_write=true`, `MISS_WRITE_VALIDATED_BY_EXISTING_WRITE_BOUNDARY`; valid warm hits return `HIT_VALIDATED_BY_EXISTING_READ_BOUNDARY`. I accept the R4 non-body-parquet-byte caveat as legitimate logical cache identity at the existing read owner; I do **not** require an opaque full-file byte canon where the validated bodies/envelope are unchanged.
- At 8 rows the reported break-evens are narrow `4.993`, repeat `3.792`, wide `10.645` warm restarts, all above the three tiny repeats, while the tiny retention field is `RETAIN_FOR_REPEAT`. This is a **diagnostic tiny receipt**, not a final retention decision. The final 100k economic receiver must apply benefit-aware retention using the measured savings/break-even; do not optimize production or convert 8 rows into a PASS.

## 3. Focused tests and original names

`21 passed in 26.11s` (`PROBE/bench_21.log`). All original 13 collected test names are preserved; the additional tests add cap, clock, identity, regression, amortization, same-size/same-mtime corruption, cold policy isolation, and full-matrix own-policy coverage. No original assertion was removed or relaxed in the reviewed delta.

## 4. Why this is method-ready, not whole-acceptance

The six method groups are corrected at the current method boundary, with the following final-receiving conditions:

1. Run the exact 100k × 3-repetition × narrow/wide/repeat matrix on the pinned final immutable SHA, 16 GiB host / 6 GiB sampled monitor, all limits and process isolation reported.
2. Independently pin/verify the external baseline file sha256 `b35...` in final receiving; do not rely only on the gate's self-hash.
3. Treat the tiny 8-row pair as diagnostic only. It is `final_shape=false` and `pass=false`; cold wide improvement `0.3359685448`, repeat launch-to-firstconsumer `0.7904743172`, no tiny PASS.
4. Apply benefit-aware retention at full scale from the measured write/restart savings; the 8-row break-evens above 3 are not a final retention result.
5. Keep the sampled-kill cap method truthful; if the pinned run cannot enforce the 6 GiB bound, mark exact `BLOCKED_EXACT_DEPENDENCY`, never downsize or claim a whole PASS.
6. Final code and economic receivers must share the same final immutable SHA, full 12-ID coverage, external SHA-bound MCR evidence, and separate source/science/authority courts.

The old64-row RED `38.99%` / warm `1.447` / `DO_NOT_RETAIN` remains historical and preserved; the new 8-row tiny pair is a different diagnostic and is not substituted for it.

**No whole-economic or 12-ID acceptance is claimed. No 100k matrix, original source/respondent/native/science/actor execution, production/test/workflow edit, install, subworker, model/provider/account/effort/region change, or protected merge was performed. The `.DS_Store` is untouched/uncommitted.**
