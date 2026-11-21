# G03-I0 — Actual P6 process measurement (SOURCEFREE_S2_INSTRUMENTATION)

Governing commission: https://github.com/maidiu/rawlsing/issues/949
Original GO-FIRSTER persona: https://github.com/maidiu/rawlsing/blob/08a323b490df4e2ddd0dca7f8b3cd394dfe17e0a/SOROK_PRODUCT_CONTROL_ROOM/ADVERSARIAL_IMPLEMENTATION_20261112_R1/01_USER_ORIGINAL_DUEL_PERSONAS_UNABRIDGED.md

## Execute

From an isolated clone/worktree at a selected immutable commit:

    python3 -B WORKER_RETURNS/SOROK-G03-I0-P6-MEASUREMENT-R1/measure.py --repo "$PWD" --out /tmp/unique-g03-i0
    python3 -B WORKER_RETURNS/SOROK-G03-I0-P6-MEASUREMENT-R1/read_receipts.py /tmp/unique-g03-i0 --require-expected
    (cd WORKER_RETURNS/SOROK-G03-I0-P6-MEASUREMENT-R1 && python3 -B -m unittest -v test_measure)

The output directory must NOT exist beforehand. GitHub Actions provides a real Ubuntu/Python 3.11 clean checkout and a standalone raw-artifact ZIP. The same run can be repeated at another frozen source commit with different wall-time and RSS observations.

## Physical execution and evidence

Genuine unmodified P6 CLI: new -> view -> wait 1 -> fresh-process cold view -> deliberately refused wait 0. All five use the same disposable state and each runs through a distinct Python child process. No mock world or synthetic timing. One source-graded manifest; durable per-attempt start.json written before process spawn; per-attempt receipt.json, stdout.bin, stderr.bin; index.json with exact hashes; summary.json recomputed and independently checked by read_receipts.py. The reader checks the frozen five-run plan, failed-run denominator, source SHA and six source-file hashes, units and scope of wait4 resources, output bytes and JSON claims, true +1 P6 clock and cold preservation, refusal reason and no state mutation, and falsified counters. External index SHA-256 should be retained separately; the index is NOT a signature or trusted OS attestation.

The child environment is an explicit five-key allowlist and excludes all SOROK_SITUATED_MODEL_* configuration and credentials. This proves provider-unconfigured subprocesses, NOT independently observed zero provider transport calls, tokens, retries, billing or network use. Those fields are UNOBSERVED, not numeric zero. OS wait4 gives direct-child CPU and max RSS (Linux native KiB / macOS bytes, both normalized to bytes), NOT summed process-tree memory. Descendant count and external cache warmth are UNOBSERVED. Distinct cold *process* is demonstrated; cold kernel page cache is NOT.

No change to P6/P3/source/actor owners, no model API spending, no native psychology, human usability or production. Full G03 five-root cohort is NOT_EVALUATED_G02_MISSING. Test_measure.py deliberately fabricates format fixtures solely to try to break the independent reader; those tests are not P6 measurements.

## Provenance and reproducibility

Run manifest records repo HEAD, Python binary digest, reader/runner version via committed HEAD, the runner SHA-256, the six directly relevant source-file SHA-256 digests, OS and Python versions, child environment allowlist and fingerprint, and five immutable invocations. The Git HEAD pins the full tracked code tree; it is not an external binary attestation. Check the separate GitHub Actions raw evidence ZIP and matching job logs for real observed metrics. The sample receipts are source-specific, not a universal performance forecast. Every retry must be a new fresh sample, not an overwrite of earlier raw evidence.

Writer custody: dedicated Agent A branch and independent GitHub-hosted execution checkout; no Codex/OpenCode controller or shared worktree touched. GitHub branch creation and SHA/blob-conditional writes are observed, but a separate local-host exclusive worker lease was NOT independently observable through this connector and must not be invented.
