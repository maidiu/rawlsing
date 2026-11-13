# G03-I0-G5 — independent executable final receiving

**Status:** `ACCEPT_SCOPED`
**Scope:** `SOURCEFREE_S2_INSTRUMENTATION_ONLY`
**Candidate:** PR #972 head `bfe420af96e401342b4d36b942532057a4871575`
**Runner evidence verified:** `41ac77670008e6d73f5d6a6bc4422e0c262aaf32`
**Prior runner SHA:** `5cc6595409d224f5331f367e36e4f8b283fe1959`
**Integration:** `UNMERGED`
**Full G03:** `NOT_EVALUATED_G02_MISSING`
**Reviewer:** opencode session `ses_e2de207ebffeB9ZV7kqTMQnz4s`, model `opencode-go/deepseek-v4.1-flash`, user `matthewsmith`
**Host:** `oldMac.lan`, macOS 13.7.8, Darwin 22.6.0, x86_64, Python 3.11.3
**Lease:** exclusive, created before checkout; see `LEASE.json`
**No native science, actor/human/production grant, or protected merge is issued.**

## 1. Custody and candidate identity

- Fresh detached checkout at `bfe420af96e401342b4d36b942532057a4871575`.
- Clean tree before and after the run: `git status --porcelain --untracked-files=all` empty.
- Exact diff from prior runner SHA `5cc6595…` to candidate `bfe420af…`:
  - only `WORKER_RETURNS/SOROK-G03-I0-P6-MEASUREMENT-R1/test_agent_a_relay.py`;
  - 5 insertions, 1 deletion;
  - no P3/P4/P5/P6 producer, actor/world owner, or protected source edit.
- The change repairs a test fixture that precreated the P6 state root. The original P6 test now asserts a wholly absent state root; the SQLite-only tests create their own fixture directories.
- Issue #949’s full body was not retrievable locally/current token. The corrected seven-case labels in the G5 issue were used, not the runner’s older frozen labels.
- The live PR head was not independently checked through the remote API; the local pinned ref `g03/pr972` equals `bfe420af…` and the commit object is exact.

## 2. R2 evidence verification

The committed R2 archive was checked against the pinned Git commit `41ac7767…`:

- Archive SHA-256 `334dfcff09b1e01c3994da51c18df52a569a46cd209d8f9af10e81bbda2c1375` matches `ARCHIVE_SHA256.txt`.
- `shasum -a 256 -c SHA256SUMS` reports every listed file `OK`.
- Raw index SHA-256 `dca3959d8b0876968bc4f6f4aa2eb0394133d1e002d62ac6d20f29cb0a2cdc73` matches `EVIDENCE_INDEX_SHA256.txt`.
- R2 reader output reports `expected_scenario_pass=true`; R2 test log records 26 tests passing.
- Minor metadata observation: `RUNNER_RESULT.json` has `archive` and `archive_sha256` as `null`, while the committed archive and `ARCHIVE_SHA256.txt` exist and match. This is evidence metadata only, not a material execution failure.
- The runner’s seven-case mapping used old labels for `I0-P02` and `I0-N02`; this receiving regrades with the corrected G5-issue labels.

## 3. Fresh independent execution

Commands actually run on the fresh checkout:

```bash
python3 -B -m unittest -v test_measure test_agent_b test_agent_a_relay
python3 -B WORKER_RETURNS/SOROK-G03-I0-P6-MEASUREMENT-R1/measure.py --repo "$PWD" --out "$EVIDENCE/measure2"
INDEX_SHA="$(python3 -B -c 'import sys,hashlib;print(hashlib.sha256(open(sys.argv[1],"rb").read()).hexdigest())' "$EVIDENCE/measure2/index.json")"
python3 -B WORKER_RETURNS/SOROK-G03-I0-P6-MEASUREMENT-R1/read_receipts.py \
  "$EVIDENCE/measure2" --index-sha256 "$INDEX_SHA" --repo "$PWD" --require-expected
```

Results:

- Tests: **26 passed, 0 failed, exit 0**, 23.653 s.
- Measure: exit 0, index SHA-256 `e35455ddd634f83de883ad82c44dcd3ba70e0368eaad14f7fc3ff5e584b37995`.
- Reader: exit 0, `expected_scenario_pass=true`.
- Attempts: 5; success 4; expected refusals 1; unexpected failed/refused 0; timed out 0; `cold_reopened=1`; 5 distinct child PIDs.
- Wall total 40.9885 s; direct-child CPU user 29.39015 s, system 2.604349 s.
- Max direct-child RSS 55,226,368 bytes.
- Refused `wait 0`: exit 2, `P6_WAIT_DURATION_OUT_OF_RANGE`; state bytes unchanged; physical content changed only `actual-p2/p3_psyche.sqlite3`; logical content unchanged.
- Provider calls/tokens/retries/billable cost: `UNOBSERVED`, not zero.
- Process-tree RSS/descendants: `UNOBSERVED`; only direct wait4 child metrics measured.
- Cold Python process demonstrated; cold kernel page cache `UNOBSERVED`.

Attempt detail:

| Attempt | Exit | Clock | State before | State after | Wall s | CPU user s | CPU sys s | Peak RSS bytes |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| new | 0 | 248 | 0 | 1,282,745 | 15.5323 | 10.4492 | 0.9922 | 54,239,232 |
| view | 0 | 248 | 1,282,745 | 1,285,673 | 6.3702 | 4.2907 | 0.4539 | 51,548,160 |
| wait 1 | 0 | 249 | 1,285,673 | 1,390,936 | 6.7148 | 5.7699 | 0.4441 | 53,125,120 |
| cold view | 0 | 249 | 1,390,936 | 1,393,526 | 5.8725 | 4.3005 | 0.3371 | 54,554,624 |
| wait 0 | 2 REFUSED | null | 1,393,526 | 1,393,526 | 6.4987 | 4.5798 | 0.3770 | 55,226,368 |

## 4. New independent hostile variation

On a copy of the fresh completed evidence+state:

1. The copied evidence passed the reader before tampering: exit 0, `expected_scenario_pass=true`.
2. An existing generated SQLite P3 `p3_records` row was changed from `TEXT` length 178 to `BLOB` length 2 (`X'4142'`).
3. The WAL was checkpointed (`wal_bytes=0`, no WAL file).
4. Receipts and index were left untouched; the original external index SHA remained `e35455…`.
5. The reader was rerun with the original external index.

Result: **exit 2, `REJECT STATE_FINAL_CONTENT_MISMATCH`**, not `expected_scenario_pass=true`.

The logical digest also changed independently:

- Before: `8d1c0329e92d40f9281da44def881bf1043c59c437d5f620a11288434f9fcc64`
- After: `07a2e6316852bf3226ac813aef55b0ad698a9030b6d368129d752ba5a453e6b3`

The reader’s final physical-state guard fired first; the expected logical-state mismatch is separately evidenced by the changed logical digest. This is a valid refusal, not a material defect.

## 5. Seven corrected case outcomes

| ID | Result | Independent evidence |
|---|---|---|
| `I0-P01` | PASS | Actual P6 `new`, `view`, `wait 1`, and cold `view` all exit 0; clock 248→249; `wait` admission `ADMITTED`; five distinct child PIDs. |
| `I0-P02` | PASS | Full raw start/receipt/stdout/stderr for all five attempts, manifest, 21-entry index; independent reader exit 0 with `expected_scenario_pass=true`. |
| `I0-N01` | PASS | Five attempts, four successes, one expected refusal; `fail_wait` exit 2 with `P6_WAIT_DURATION_OUT_OF_RANGE`; `unexpected_failed_or_refused=0`. |
| `I0-N02` | PASS | Provider calls/tokens/retries/billable cost are `UNOBSERVED`, not zero; five-key offline child allowlist; no provider transport independently observed. |
| `I0-N03` | PASS | 26/26 hostile suite covers source forgery, edited receipt, stdout mutation, forged summary, RSS units, provider zero, cold lie, WAL refusal, and BLOB/TEXT collision; new P3 row type/content tamper refused with exit 2. |
| `I0-R01` | PASS | Candidate diff from prior runner SHA changes only `test_agent_a_relay.py`; no P3/P4/P5/P6 owner or protected source edit; clean tree before and after; no commit or merge. |
| `I0-M01` | PASS | Five direct-child wait4 samples measured wall/CPU/RSS; max RSS 55,226,368 bytes; process-tree RSS and descendants remain `UNOBSERVED`. |

## 6. Gates

| Gate | State | Basis |
|---|---|---|
| G1 | `PASS_SOURCE_CUSTODY__CONTRACT_TEXT_NOT_ACCESSIBLE` | Exact candidate SHA, clean detached checkout, source hashes, exclusive lease, one-file test-only diff. #949 full body not retrievable; corrected labels from the G5 issue used. Live PR head not remotely checked; local pinned ref matches. |
| G2 | `PASS` | 26/26 tests; five actual P6 children; measure exit 0; independent reader exit 0 with `expected_scenario_pass=true`. |
| G3 | `PASS` | 26/26 hostile suite; new independent SQLite P3 tamper refused with exit 2. |
| G4 | `PASS` | Fresh raw receipts, manifest, 21-entry index, reader output, environment, source state, durable copies. R2 archive SHA and SHA256SUMS verified; raw index matches `dca3959d…`. One minor R2 metadata inconsistency noted. |
| G5 | `ACCEPT_SCOPED` | Independent execution completed; all seven corrected cases PASS; no substantive defect; integration remains `UNMERGED`; full G03 is `NOT_EVALUATED_G02_MISSING`. |

## 7. Decision and limits

**G5 decision:** `ACCEPT_SCOPED` at `SOURCEFREE_S2_INSTRUMENTATION_ONLY`.

This accepts the scoped sourcefree instrumentation execution only. It does not accept full G03, original source science, native psychology, actor/human authority, provider billing, process-tree resource use, or a protected merge.

Limits:

- Provider calls/tokens/retries/billable cost: `UNOBSERVED`, not zero.
- Process-tree RSS and descendant count: `UNOBSERVED`; only direct wait4 child metrics measured.
- Cold Python process demonstrated; cold kernel page cache `UNOBSERVED`.
- Mac host sample, not Linux/GitHub-hosted.
- G02 cohort missing; full G03 `NOT_EVALUATED_G02_MISSING`.
- No native science, actor/human/production grant, protected merge, or GitHub publication.
- Issue #949 full body and live PR head were not independently accessible through the current remote API.

## 8. Evidence paths

Durable review directory:

`/Users/matthewsmith/Desktop/rawlsing-g03-i0-g5-review-20261113T030841Z`

Key files:

- `G5_01_GATE_FINDINGS.json` — machine-readable finding.
- `evidence/tests.stderr` — 26-test output.
- `evidence/measure2.stdout` / `.stderr` — fresh P6 measurement.
- `evidence/reader2.stdout` — independent reader success.
- `evidence/tamper2_values.json` — before/after P3 row and logical digests.
- `evidence/tamper2_reader.stdout` — tamper refusal.
- `evidence/SOURCE_STATE.txt` — exact HEAD, clean tree, source hashes.
- `evidence/ENVIRONMENT.txt` — host, Python, lease, unobserved metrics.
- `r2/` — verified R2 archive, SHA256SUMS check, raw index pin, and independent R2 checks.
- `DIFF_5cc6595_to_bfe420af.txt` — exact candidate diff.
- `LEASE.json` — exclusive review lease.

No SEV-0, SEV-1, or SEV-2 defect was found.
