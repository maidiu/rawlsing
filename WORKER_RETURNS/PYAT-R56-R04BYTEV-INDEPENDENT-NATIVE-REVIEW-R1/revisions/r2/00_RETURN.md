# R56-R04BYTEV revision r2 — targeted custody requalification return

Verdict: **REVISE** — one minimal reproducible engineering counterexample remains
at the claimed in-place custody boundary. The repaired fd binding and pathname
replacement defense work, but a memory-mapped in-place write between SAV lazy
batches is not caught by the per-batch `fstat` signature on this platform; the
actual C11/I03 facts are then built from altered bytes while carrying the old
source identity.

- Engineering: REVISE with the minimal counterexample in
  `test_r2_mmap_between_batch_change_cannot_release_altered_c11_i03_under_old_identity`.
- Science: no science acceptance; synthetic generated data only; no original
  source, original35 or N11 measurement.
- Authority: no production promotion, no joined R04/R03, no partial Batch/
  revocation/dedup lifecycle, no protected R09 CI, no adoption/N11/N12.

## Continuity, session and exact identities

- Same independent `R56-R04BYTEV` reviewer role, fresh agent context; the
  repair was authored and pushed by the R04BYTE author session, not this
  reviewer. Original review preserved at `afbe6dd5f`; it was not merged, reset
  or edited, and its probes are the negative baseline copied into
  `evidence/` (`r1_probe_*`, `r1_negative_baseline_*`).
- Session: OpenCode CLI; model `opencode-go/deepseek-v4.1-flash`; effort
  `UNKNOWN_NOT_EXPOSED`; provider `UNKNOWN_NOT_EXPOSED`; host
  `MacBook-Pro.lan`, macOS 13.2.1 (22D68), x86_64; Python 3.11.3, pytest
  9.0.2, pyreadstat 1.3.2, pandas 2.3.1. Session ID `UNKNOWN_NOT_EXPOSED`;
  independence basis recorded in `00_STARTUP_SESSION_RECORD.md`.
- Candidate `ea0d6f0f9840db0e33645b40ceda54456612709e` (parent
  `c1b0abec563a91940ae2f505b53a4c7e16f8685a`; original startup
  `6d95a78bf6b7bcf70022e303a151255e65edc38a` is an ancestor). Remote author
  branch equals the candidate.
- Successor branch `agent/rabochii-pyat-r56-r04bytev-r2-custody-requalification-r1`
  and successor worktree were verified absent before creation; no duplicate
  active reviewer. Author worktree was not reset or reused.
- Actual imports: decoder sha256 `a767b653...`, test file `694dd2f8...` (after
  the reviewer addition), proof sidecar `f4ff0cd8...`; unchanged facade
  `03b88d25...`, I03 query `d45ad313...`, C11 repository `84a71fe4...`.
  Candidate-side git blobs and the repaired author manifest were verified.

## Repaired author result independently reproduced

- Focused module (author/repaired tests, reviewer counterexample deselected):
  **24 passed**.
- Core command (8 modules, counterexample deselected): **88 passed, 1 skipped**.
- Full module with the reviewer counterexample: **24 passed, 1 failed**.
- Full core with the counterexample: **88 passed, 1 failed, 1 skipped**.
- Skip identified honestly: `test_pre553_sr06_decoder_carrier.py:268` —
  installed pyreadstat writer/readback does not expose `missing_user_values`
  in metadata; DTA extended-missing readback remains unexercised/unqualified
  in this runtime. The file is unchanged by the repair.
- The original 10 R1E/R1I/R1J failures were already independently
  baseline-identical at r1. The author's repaired-code rerun (receipt read)
  shows the same 10 nodes/messages (`10 failed, 23 passed`); no new sweep was
  run because no concrete regression was indicated.

## What the repair now does correctly (independently verified)

- The private snapshot pathname is unlinked at acquisition; `reader_path` is
  `/dev/fd/{fd}`; `source_custody.reader_binding == OPEN_FD_VIA_POSIX_DEV_FD`,
  `snapshot_path_unlinked == true`. Captured pyreadstat reader arguments were
  `/dev/fd/N` for metadata, compatibility full read, SAV chunk and DTA full
  read. A direct `seek(0)` read of `/dev/fd/N` hashes equal to the source and
  to the bound fd (`evidence/probe_r2_attack_windows.json`).
- Replacing a file at the old private snapshot pathname after acquisition
  (before facts, and inside the reader-call window) does not change variables,
  metadata or C11/I03 facts; source/snapshot identity stays original; the
  replacement survives `close()` because `close()` only unlinks the recorded
  pathname when it still names the bound inode.
- `pwrite`/`ftruncate` in place before a lazy pass is typed-refused
  (`DecoderError`); truncation and closed-fd reads are typed-refused; an
  external between-batch `pwrite` is refused before altered cells (only the
  already-read frame prefix is yielded).
- DTA in-place change before the full value read is typed-refused by the
  post-read full digest. DTA direct `/dev/fd` chunking fails exactly as the
  author states (`ReadstatError: This version of the file format is not
  supported`); DTA uses one full `read_dta` frame per value pass.
- Shortest cold replay: changed bytes under the old digest fail before the
  reader with no fact output; restoring exact bytes reproduces the identical
  fact payload (SAV+DTA). Repeated lazy/full reads are stable, and the
  reader-call window replacement is covered.
- Synthetic monkeypatched compatibility-allowlist test passes for SAV/DTA and
  is TEST_ONLY: it exercises reader binding, not installed encoding authority
  or retained original encoding coverage.
- POSIX `/dev/fd` refusal exercised by making `/dev/fd` unavailable in the
  check: typed `DecoderError: content-bound reader path requires POSIX /dev/fd`.
- Proof-integrity lint passes; witness over the three sidecar claims (author
  lazy readset + the two R04BYTEV independent claims) shows baseline PASS and
  exact mutation `TARGET_ASSERTION_FAILED` for each; decoder restored
  byte-exact `a767b653...` (`evidence/proof_witness.json`).

## Remaining counterexample (minimal, reproducible)

`test_r2_mmap_between_batch_change_cannot_release_altered_c11_i03_under_old_identity`
(added to the allowed test file; author/repaired tests preserved verbatim).

Setup: generated SAV with the frozen rows; decode; bind the unchanged facade
projection; `mmap.mmap(incidence._source_snapshot.fd, PROT_WRITE)` (the same
descriptor the repaired between-batch test already uses); during the actual
C11 release build, after the first chunk, write the valid alternate SAV bytes
through the mapping (same 839-byte size); continue the reader; build the
release and execute the unchanged I03 query.

Observed on the exact candidate (deterministic, 3/3 test runs, 2/2 probe runs):

| quantity | baseline | after mmap write between SAV batches |
|---|---|---|
| `fstat` signature (dev/ino/size/mtime/ctime) | original | **unchanged** |
| `source_artifact_ref.content_hash` | original digest | original digest |
| `snapshot_sha256` / `source_sha256` | original digest | original digest |
| I03 `i03_y_cells` | `{"0": 1, "1": 1}` | `{"0": 0, "1": 2}` |
| I03 `i03_fact_ref` | baseline | changed |
| typed refusal before release | — | **none** (verify detects only after) |

So affected C11 `RespondentEvent`/I03 `EmpiricalFact` values are released under
the old source identity. The author's claim that a between-batch write is
refused is true for `write(2)`/`pwrite` but not for dirty `mmap` pages on this
APFS host, where mtime/ctime did not update synchronously. The same-uid process
address space and anyone holding the writable bound descriptor are inside the
author's stated trust boundary; the descriptor is opened `O_RDWR` and the
`mmap` is therefore permitted. This is exactly the fstat-signature vs
full-digest coverage distinction: per-batch coverage is a signature, not a
digest, and a full-digest check after the SAV pass (or a read-only reader fd)
would be needed to close it.

Counterexample evidence: `evidence/probe_r2_mmap_fact_bypass.json` and
`evidence/probe_r2_attack_windows.json` (`mmap_between_batch`); the failing
test receipt is in the module/core receipts.

## Read shape / scale limit (not certified beyond this)

- DTA: one full `read_dta` frame per value pass, no chunking, O(rows×cols)
  memory. Synthetic child-process maxrss deltas: 0.78 MB @1k rows, 1.9 MB
  @10k, 12.5 MB @50k (file 1.56 MB) — O(rows) growth, row-count-limited.
- SAV: chunked `read_file_in_chunks` with per-batch signature; synthetic
  maxrss deltas stayed ~0.7–1.2 MB from 1k to 50k rows when cells are consumed
  and discarded.
- No original35-scale memory, unchanged DTA chunking or memory-budget claim is
  made. POSIX `/dev/fd` is required; non-POSIX/non-/dev/fd runtime typed-refuses.

## Residual limits / notes

- The failing boundary is a same-process actor holding the writable descriptor;
  no ptrace/root-level immutability is claimed by either party.
- DTA extended-missing readback remains skipped/unqualified by the installed
  writer/readback capability.
- Compatibility full-read coverage here is synthetic TEST_ONLY, not installed
  original-encoding authority.
- After the owner repairs the mmap-signature gap, affected requalification
  should rerun the focused module, the two counterexample probes, the cold
  replay and the three-claim witness.
