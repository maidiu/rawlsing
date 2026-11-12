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

## Agent B FOLLOW-UPPER — versioned V2 correction (Commission #949)

**This directory now contains the B descendant** of A's frozen `b4f26fec056f5cb481a0b4e417e7a29bae833546`. A's branch, existing P6/P3 and source owners remain untouched. The v1 evidence remains independently readable with the frozen v1 reader at A's commit; v2 does not regrade or rewrite earlier archives.

The original receiver treated equal **state-root byte totals** as proof of an untouched refused P6 operation. That oracle is false. On an actual P6 `wait 0` refusal, `actual-p2/p3_psyche.sqlite3` changes physical content while preserving its file byte count. A dedicated read-only SQLite comparison established unchanged table records and schema for that observed case; the source P3 store initializes a SQLite immediate transaction when an owner opens. Do **not** infer that all possible physical changes are harmless.

V2 writes separate path-sensitive physical and logical state snapshots before and after **every actual attempt**, chains them across attempts and cold reopening, and has the independently implemented reader recompute the final state. The logical view substitutes validated read-only SQLite schema/table/PRAGMA-user-version content for the database's physical page layout, but still hashes every other file's bytes and paths. Real SQLite row changes alter the logical digest. The receiver reports `refused_state.physical_content_changed` and `refused_state.logical_content_changed` independently; `expected_scenario_pass` requires a source-exact refusal with **unchanged logical state**, not a fictitious claim that SQLite's physical bytes were untouched. This is a bounded P3 sourcefree state witness, not a universal database or actor-science oracle.

V2's externally anchored index now covers `manifest.json` **and** the 20 per-attempt raw files. A modified runner or interpreter digest in the manifest can no longer survive unchanged external index custody. The meter refuses dirty **or untracked** checked-out source and verifies unchanged HEAD and relevant hashes after execution; output must reside outside the repo. The receiver accepts optional `--repo` for an independently checked matching live checkout and `--index-sha256` for externally pinned evidence.

### Exact B commands

From the candidate's clean isolated checkout at its immutable SHA:

```bash
python3 -B WORKER_RETURNS/SOROK-G03-I0-P6-MEASUREMENT-R1/measure.py --repo "$PWD" --out /tmp/g03-b-FRESH
INDEX_SHA=$(sha256sum /tmp/g03-b-FRESH/index.json)
INDEX_SHA="${INDEX_SHA%% *}"
python3 -B WORKER_RETURNS/SOROK-G03-I0-P6-MEASUREMENT-R1/read_receipts.py /tmp/g03-b-FRESH --index-sha256 "$INDEX_SHA" --repo "$PWD" --require-expected
(cd WORKER_RETURNS/SOROK-G03-I0-P6-MEASUREMENT-R1 && python3 -B -m unittest -v test_measure test_agent_b)
```

**Evidence boundary:** the true measured subprocess wall time, direct-child wait4 CPU/RSS, sourcefree command outcomes, SQLite readback, state bytes and cold **process** proof survive. Process-tree resource use, true cold kernel cache, provider calls/tokens/retries/spend, live network activity, generated-root cohort and Mac-host performance are **UNOBSERVED**, not zero. Physical SQLite header/page writes remain observable and are not denied. Immutable GitHub Actions results and downloadable raw artifacts are cut-specific. Final independent G5 receiving and any protected/native/human grant remain separate.
