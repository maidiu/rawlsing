# W03/W04 one-pass pilot

**Status:** `LAUNCH_PREPARED_PENDING_DURABLE_HANDOFF`
**Branch:** `agent/pyat-w03-w04-one-pass-pilot-r1`
**Implementation cut:** `c59c40f9988ec869953a4865c09d8380352db4ab`
**Runtime benchmark blob:** `6c72f7d67c16fe79b9260032f6ace4085c6f1f3d`
**Protected baseline:** `4f3413fc5c37b589be3412f826bf8f68ee617d4a`
**First pair:** `cold/narrow`, 100000 rows, actual event count expected 200000, one repetition, same 6 GiB sampled cap.

## Baseline receipt decision

Six nonempty old `NATIVE_W03_W04_FULLSCALE` worker JSONs were preserved losslessly in
`archive/old_baseline_worker_json.tar.zst` with a SHA-256 manifest. They are complete
worker payloads, but they lack parent-level cap enforcement, method, and source-head
provenance. They are therefore retained as historical raw evidence, not mislabeled
as a fully qualified baseline. The first pair runs a fresh baseline narrow cold case
then the matching candidate, in that order.

## First-pair driver

`run_pair.py` uses the existing CLI, existing `_run_child`/worker and existing
metrics/comparison output. It does not add benchmark logic.

```text
baseline:  python -B -m rawlsing_next.bench_w03_w04_physical \
  --scenario cold --profiles narrow --rows 100000 --repetitions 1 \
  --source-root <protected-4f> --root <native-run>/cache/baseline-narrow-cold \
  --jsonpath <ONE_PASS_PILOT_R1>/raw/baseline_narrow_cold_n1.json \
  --cap-bytes 6442450944

candidate: python -B -m rawlsing_next.bench_w03_w04_physical \
  --scenario cold --profiles narrow --rows 100000 --repetitions 1 \
  --source-root <candidate> --root <native-run>/cache/candidate-narrow-cold \
  --jsonpath <ONE_PASS_PILOT_R1>/raw/candidate_narrow_cold_n1.json \
  --baseline-json <ONE_PASS_PILOT_R1>/raw/baseline_narrow_cold_n1.json \
  --cap-bytes 6442450944 --acceptance-gate
```

The candidate `--acceptance-gate` is expected to have `final_shape=false` at one
repetition; that is recorded, not repaired or treated as a final PASS.

## Remaining queue

`queue.json` lists seven remaining operation/profile pairs. Only the first pair is
launched now. No full queue is started before this handoff.

## Native launch

The finite native job/session is `NATIVE_W03_W04_ONE_PASS_PILOT`, same HQ recipient
`01a15c1e-5446-7ef3-80bb-9ff5c2cb27da`, notify true. No recurring model poll,
goal wakeup, subworker, or daemon.

## Limits

No original35/source/native/science/actor/protected merge. No 3-run confidence or
economic final PASS. Raw receipts are the only comparison source; no manually
computed analytical oracle.
