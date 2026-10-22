# R56-R04BYTEV revision r3 — targeted read-only custody acceptance return

Verdict: **ACCEPT_SCOPED_LOCAL**. The R3 read-only capability handoff closes the
R2 mmap/writable-fd defect at the declared threat boundary: the retained reader
is genuinely `O_RDONLY`, the construction writer is closed before handoff, and
ordinary `write`/`pwrite`/`ftruncate`/shared-writable-`mmap`/`/dev/fd`-reopen
attempts through the supplied capability are denied before any modification with
the same independently frozen C11/I03 facts. Limits are listed explicitly below.

- Engineering: ACCEPT_SCOPED_LOCAL for local consumed-byte custody on POSIX
  `/dev/fd` with the R3 handoff, on this host and tested synthetic data.
- Science: no science acceptance; synthetic generated data only; no original
  source, original35 or N11 measurement.
- Authority: no production promotion, no R03/R04.joined, no joined issued
  workload, no partial Batch/revocation/dedup lifecycle, no protected R09 CI,
  no adoption/N11/N12.

## Continuity, session and exact identities

- Same independent `R56-R04BYTEV` reviewer role continues; this is a fresh
  agent context. R3 was authored and pushed by the R04BYTE author session, not
  this reviewer. R1 (`afbe6dd5f`) and R2 (`228387c59`) reviewer branches and
  returns are preserved and were not merged or edited; the R2 mmap
  counterexample is the immutable negative baseline copied into `evidence/`.
- Session: OpenCode CLI; model `opencode-go/deepseek-v4.1-flash`; effort
  `UNKNOWN_NOT_EXPOSED`; provider `UNKNOWN_NOT_EXPOSED`; host
  `MacBook-Pro.lan`, macOS 13.2.1 (22D68), x86_64; Python 3.11.3, pytest
  9.0.2, pyreadstat 1.3.2, pandas 2.3.1. Session ID `UNKNOWN_NOT_EXPOSED`;
  independence basis in `00_STARTUP_SESSION_RECORD.md`.
- Candidate `31a39c50cb5e8487968ab7b00386912fc5f1d6ca`; parent
  `ea0d6f0f9840db0e33645b40ceda54456612709e`; original startup
  `6d95a78bf6b7bcf70022e303a151255e65edc38a` (ancestor). Remote author branch
  equals the candidate.
- Decision/contract read at `1ac432d95ad9b6ca9da94828cc5f2aed8d10b5d7`
  (`22_R04_BYTE_BOUNDED_ENGINEERING_DECISION_AND_IMPLEMENTATION.md`) and the OS
  discriminator `23_R04_READONLY_CAPABILITY_PROBE.json` (primitive evidence,
  not pyreadstat acceptance). Shared review contract `485f31e52`; native
  contract `eb28fdcc3`; R56/R57 unchanged; frozen R2 policy `6d95a78b`
  read-only.
- Successor branch/worktree were verified absent before creation; no duplicate
  active reviewer. Author worktree at `31a39c50c` was not reset or reused.
- Candidate-side hashes before reviewer edits: decoder
  `1ed8a8ae01f90bba297d708a0926fe9911d9b186eb858d99aec616e23991d320`;
  test file `8a4efe40b939379c3b28e7455214370baec459d9a1f410e2548ffb6d0964848b`;
  proof sidecar `f4ff0cd8bf509c106f14d03812401fd2edc8581cf5e971dc1f17041d74363f51`
  (unchanged from R2). Actual imported production hashes: facade
  `03b88d25...`, I03 query `d45ad313...`, C11 repository `84a71fe4...`
  (unchanged by R3).
- Author r3 manifest (13 files) independently verified against the commit:
  0 hash/blob mismatches.

## Reproduced author result

- Focused module: **26 passed** (reviewer run).
- Core command (8 modules): **90 passed, 1 skipped**.
- Skip identified honestly: `test_pre553_sr06_decoder_carrier.py:268` — the
  installed pyreadstat writer/readback does not expose `missing_user_values`;
  DTA extended-missing remains unexercised/unqualified. The file is unchanged.
- The inherited 10 R1E/R1I/R1J failures were established baseline-identical at
  R1 and were not rerun; the R3 change touches only the decoder acquisition
  capability, and no concrete regression is indicated.

## Read-only handoff verified (actual values)

`evidence/probe_r3_handoff.json` (SAV and DTA):

- Retained fd is the distinct reader open (`retained_fd_matches_reader_open
  = true`), `fcntl(F_GETFL)` access mode `O_RDONLY`,
  `source_custody["reader_access_mode"] == "O_RDONLY"`.
- Construction writer (captured fd 4 in the probe) is closed at decode return,
  absent from `/dev/fd`; the reader fd is present. Decoder state retains a
  single fd field; the source fd is opened read-only and closed; no production
  mmap.
- Bound checks are real: reader/construction dev/ino/size equality enforced in
  code; `st_nlink == 0`; snapshot pathname unlinked (`snapshot_path_exists
  = false`); reader digest equals the acquisition/source digest; custody
  `snapshot_sha256 == source_sha256 == sha256(file bytes)`.

## Write-capability denial (declared contract, supplied fd only)

Through the supplied reader fd, with no new permission grant or private-state
substitution (SAV and DTA; `evidence/probe_r3_handoff.json`):

| attempt | result |
|---|---|
| `os.write(fd, b"x")` | denied `OSError` EBADF (9) |
| `os.pwrite(fd, alt_bytes, 0)` | denied `OSError` EBADF (9) |
| `os.ftruncate(fd, n)` | denied `OSError` EINVAL (22) |
| `mmap(fd, ACCESS_WRITE)` | denied `PermissionError` EACCES (13) |
| `mmap(dup(fd), ACCESS_WRITE)` | denied `PermissionError` EACCES (13) |
| `os.open("/dev/fd/N", O_RDWR)` | denied `PermissionError` EACCES (13) |
| `os.open("/dev/fd/N", O_WRONLY)` | denied `PermissionError` EACCES (13) |
| `fcntl(F_SETFL, O_RDWR)` | returns 0 but access mode remains `O_RDONLY` |
| `os.open("/dev/fd/N", O_RDONLY)` | ordinary read open allowed |

After every attempt the reader-fd full digest equals the acquisition digest and
the actual C11/I03 facts equal the frozen positive baseline (`i03_y_cells
{"0":1,"1":1}`, same fact/release identity). The ported R2 mmap counterexample
now denies write-capability acquisition and reproduces the same baseline facts.

## Windows, lifetime and cold replay

- Original-path replacement after acquisition and between phases: frozen facts
  and original source/snapshot identity.
- Foreign file created at the old private snapshot pathname: not consumed;
  facts frozen; `close()` does not delete the foreign replacement (verified
  for SAV and DTA).
- Metadata, compatibility full read, SAV lazy chunk and DTA full value paths all
  use the bound read-only `/dev/fd` reader.
- Repeated facts/cells stable; normal `close()` typed-refuses later reads;
  genuinely changed same-path bytes acquired anew get a new digest/new facts,
  while the old incidence keeps the original facts; old-digest decode of the
  changed path is typed-refused.
- Fresh-process old-digest cold replay: changed bytes rc=1, empty stdout,
  typed mismatch; restoring exact bytes rc=0 and the identical fact payload.
- Handoff failure probes: inode mismatch and pre-unlink pathname replacement are
  typed `DecoderError` and clean up; the foreign replacement is preserved in
  the acquisition directory (verified content), construction/reader fds close.
- POSIX `/dev/fd` unavailable is a typed `DecoderError` (author test, module
  run); non-POSIX platform is out of scope.

## Read shape / limits (not promoted)

- SAV keeps `read_file_in_chunks` streaming; one full-digest check per value
  pass (`sha_fd_calls_in_one_pass == 1`), not per chunk. Synthetic maxrss deltas
  ~0.64/0.72/1.11 MB at 1k/10k/50k rows.
- DTA normal value pass is one full `read_dta` frame per pass (`chunks == 0`,
  `full == 1`); direct chunking on `/dev/fd` DTA fails exactly
  `ReadstatError: This version of the file format is not supported`. Synthetic
  maxrss deltas ~0.24/1.58/12.53 MB at 1k/10k/50k rows: O(rows x cols).
  No original35-scale or unchanged-DTA-chunking claim.
- Extended-missing DTA writer/readback remains skipped/unqualified. Compatibility
  full-read coverage is a synthetic monkeypatched allowlist (TEST_ONLY), not
  installed encoding authority or retained original-encoding coverage.

## Failure-path typing limit (reported, not hidden)

Supported/wrong descriptor states are domain-typed: normal `close()` and
post-close reads raise `DecoderError`; substituted non-read-only and non-regular
read-only fds raise `DecoderError`; inode mismatch and pre-unlink pathname
replacement raise `DecoderError`.

Two fail-closed paths are **not** domain-typed and are listed as limits:
- an externally OS-closed or invalid retained fd (requires private-state
  substitution/`os.close` of decoder state, excluded by packet 22) raises
  `OSError` EBADF; `close()` on that state also raises `OSError` EBADF;
- an environmental reader-open failure during acquisition (forced EACCES in the
  probe) raises `PermissionError` and cleans up (construction writer closed, no
  leftover acquisition directory, no facts) rather than `DecoderError`.

Neither path releases facts, yields a writable capability, or leaves a temp
artifact. If the director requires domain-typed `DecoderError` for those exact
excluded/environmental paths, that is a small typed-wrapper follow-up, not a
failure of the read-only capability handoff. The ordinary declared reader
contract (no retained write capability) is satisfied.

## Proof integrity and negative baseline

- `proof_integrity_gate_r1.py lint` -> `AST_LINT_PASS`.
- Witness over the three sidecar claims (author lazy readset + two R04BYTEV
  independent path/replacement claims): 3/3 baseline PASS, 3/3 exact mutation
  `TARGET_ASSERTION_FAILED`, decoder restored byte-exact `1ed8a8ae...`.
- R2 negative evidence preserved read-only in `evidence/`
  (`r2_negative_baseline_00_RETURN.md`,
  `r2_negative_baseline_mmap_test_excerpt.py`,
  `r2_negative_baseline_probe_mmap_fact_bypass.{py,json}`); R2 branches were not
  merged or edited.

## Threat boundary and scope limits

- Guarantee is local byte custody after handoff on POSIX `/dev/fd`: the supplied
  reader capability is read-only; ordinary write/truncate/shared-writable-mmap
  and writable `/dev/fd` reopen are denied before modification.
- Trusted operator/process can still deliberately manufacture new privileges or
  corrupt private decoder state (fchmod + new write fd, dup2 substitution,
  ptrace/root, object/code replacement); packet 22 excludes that supervisor
  fault. No hostile same-UID supervisor isolation is claimed. The construction
  window and exotic syscalls of the same access-check class are not separately
  certified.
- Local synthetic qualification only; no original data, R09 CI, production,
  N11/N12 or combined-candidate proof. Combined-candidate proof remains a later
  bounded task.
