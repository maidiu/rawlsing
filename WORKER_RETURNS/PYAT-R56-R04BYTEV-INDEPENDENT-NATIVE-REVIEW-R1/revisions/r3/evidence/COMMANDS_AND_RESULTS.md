# R56-R04BYTEV r3 — exact commands, exits and observed results

All runs in `/Users/matthewsmith/Desktop/Rawlsing/R56-R04BYTEV-r3-custody-requalification-wt`.
Host macOS 13.2.1; Python 3.11.3; pytest 9.0.2; pyreadstat 1.3.2; pandas 2.3.1.

## Startup / identity

- Candidate `31a39c50c`; parent `ea0d6f0f9`; startup `6d95a78bf` ancestor.
- Remote author branch = `31a39c50cb5e8487968ab7b00386912fc5f1d6ca`.
- Successor branch/worktree absent before creation; no duplicate reviewer;
  author worktree untouched.
- Decision/contract read at `1ac432d95...` (packet 22) and OS discriminator 23.
- Candidate-side decoder `1ed8a8ae...`, test `8a4efe40...`, sidecar
  `f4ff0cd8...`. Author r3 manifest verified: 13 files, 0 mismatches.

## Reproduced author result

```
python3 -m pytest rawlsing_next/tests/test_universal_source_byte_custody.py -q -rs
26 passed in 7.42s                        exit 0

python3 -m pytest <8 core modules> -q -rs
SKIPPED [1] rawlsing_next/tests/test_pre553_sr06_decoder_carrier.py:268: installed pyreadstat writer/readback does not expose missing_user_values in metadata
90 passed, 1 skipped in 22.98s            exit 0
```

## Proof integrity

```
python3 CROSS_HQ_CONTROL_ROOM/proof_integrity_gate_r1.py lint <module>
{"state": "AST_LINT_PASS", ...}           exit 0

python3 CROSS_HQ_CONTROL_ROOM/proof_integrity_gate_r1.py witness \
  <module>.proof.json --root . --receipt .../evidence/proof_witness.json
3/3 baseline PASS, 3/3 TARGET_ASSERTION_FAILED, BOUNDED_MUTATION_DETECTED
exit 0; decoder restored 1ed8a8ae...
```

## Independent probes (evidence/)

`probe_r3_handoff.json` (SAV+DTA):
- retained fd == reader open; access mode O_RDONLY; construction fd closed and
  absent from `/dev/fd`; reader fd present; nlink 0; path unlinked; digest and
  facts unchanged after all denial attempts.
- denied: write EBADF 9, pwrite EBADF 9, ftruncate EINVAL 22, mmap EACCES 13,
  mmap(dup) EACCES 13, `/dev/fd` reopen O_RDWR/O_WRONLY EACCES 13;
  `fcntl(F_SETFL,O_RDWR)` leaves access mode O_RDONLY; O_RDONLY reopen allowed.
- after denials: reader digest == source digest, C11/I03 facts == frozen
  baseline (`i03_y_cells {"0":1,"1":1}`).
- wrong/closed diagnostics: substituted O_RDWR -> DecoderError not read-only;
  substituted O_RDONLY non-regular -> DecoderError not regular; normal close ->
  DecoderError closed; externally OS-closed/invalid fd -> OSError EBADF;
  `close()` on OS-closed state -> OSError EBADF.
- handoff failures: inode mismatch -> DecoderError, no leftovers; pathname
  replacement before unlink -> DecoderError, foreign content preserved in the
  acquisition directory; reader-open failure -> PermissionError, construction fd
  closed, no leftover directory.
- windows/lifetime: original-path and private-path replacement facts frozen;
  foreign survives close; repeated facts equal; new acquisition new identity;
  old digest on changed path refused; cold changed rc=1 empty stdout, restore
  rc=0 identical payload (SAV+DTA).
- SAV shape: 21 cells, 1 chunk generator, 1 full-digest call per pass.

`probe_r3_read_shape.json` (child-process maxrss deltas):
- SAV ~0.64/0.72/1.11 MB at 1k/10k/50k; DTA ~0.24/1.58/12.53 MB -> O(rows)
  full-frame. No original35-scale claim.

`probe_r3_dta_chunk_and_reader_calls.json`:
- SAV value pass: `read_file_in_chunks` used; DTA value pass: one full
  `read_dta`, zero chunk calls; direct `/dev/fd` DTA chunking fails
  `ReadstatError: This version of the file format is not supported`.

## Negative baseline

R2 failing evidence copied read-only from `228387c59`:
`r2_negative_baseline_00_RETURN.md`,
`r2_negative_baseline_mmap_test_excerpt.py`,
`r2_negative_baseline_probe_mmap_fact_bypass.py` / `.json`. The R2 mmap attack
is ported by the author as denial-plus-unchanged-fact regression and is
independently reproduced by `probe_r3_handoff.json`.
