# R56-R04BYTEV r2 — frozen requalification expectations

Written BEFORE executing the repaired candidate tests or generating candidate
outputs in this session. Derived from the r1 frozen semantics (preserved at
`afbe6dd5f`), the pre-existing fixtures/facade/I03 contract, and the review
defect. Candidate-produced receipts are not the oracle.

## 1. Unchanged semantic expectations (same as r1)

- Real generated SAV and DTA from `_ROWS`; 21 physical cells; Y values
  1,0,1; X row 3 system missing.
- I03 fact for target Y, branch cohort all 3 respondents, risk set R with Y
  members {R1,R2}: `SUPPORTED`, denominator 2, cells `{"0": 1, "1": 1}`,
  numerator support 2; same release/fact identities for identical bytes.
- 21 C11 `RespondentEvent`s expected (fixture occurrence counts).

## 2. New binding expectations (repair interface)

1. After acquisition, the snapshot pathname must not exist
   (`snapshot_path_unlinked == True`) and `reader_path` must be
   `/dev/fd/{fd}`; `source_custody["reader_binding"] == OPEN_FD_VIA_POSIX_DEV_FD`.
2. Metadata, compatibility full read and SAV lazy chunk reads must pass the
   `/dev/fd/{fd}` string to pyreadstat (capture the actual `source` argument).
3. Replacing a file at the old private snapshot pathname after acquisition,
   before metadata or before lazy reads, must not change variables, metadata,
   or C11/I03 facts; original source/snapshot/release/fact identities must
   remain. The replacement pathname must not be consumed.
4. In-place change to the bound inode before metadata/lazy/full reads must
   raise typed `DecoderError` before any differently sourced metadata/events/
   facts are released.
5. In-place change to the bound inode between SAV lazy batches must raise
   typed `DecoderError` before any altered cell is yielded; only pre-change
   cells may have been released.
6. DTA value reads must use the bound fd; the installed chunk reader cannot
   consume `/dev/fd` DTA (verify the exact failure directly). DTA is full-frame
   per value pass: O(rows) memory; not a chunked claim.
7. Truncation and closed-fd reads must typed-refuse before facts.
8. Fresh-process old-digest cold replay with changed bytes must fail with no
   fact output; restoring exact bytes must reproduce the same fact payload.
   Genuinely changed same-path bytes acquired anew get a new identity.
9. Coverage distinction to report: full SHA-256 digest is re-verified after
   metadata, after compatibility full read, before returning the incidence,
   and at the start of each lazy pass; SAV per-batch coverage is the
   `fstat` (dev, ino, size, mtime_ns, ctime_ns) signature, NOT a per-batch
   full digest.
10. POSIX `/dev/fd` availability is part of the interface: on a runtime
    without it, acquisition must typed-refuse (`DecoderError`) before any
    reader call. Platform assumption: macOS/Linux POSIX.
11. Close semantics: `close()` must not unlink a replacement file that no
    longer names the bound inode; it must close the fd and remove the private
    directory when possible. Reads after close typed-refuse.
12. A synthetic monkeypatched compatibility-allowlist entry exercises the
    compatibility reader binding as native TEST_ONLY coverage; it does not
    issue installed encoding authority or retained original encoding coverage.

## 3. Threat model to state explicitly

- Trust boundary is the same-process address space plus anyone holding the
  bound descriptor; no ptrace/root-level claim.
- fstat-signature coverage is not full-digest coverage: any write that updates
  size/mtime/ctime is caught; a mechanism that changes bytes without updating
  those fields (e.g. dirty `mmap` pages if the OS defers timestamps) is a
  residual to probe and report honestly.
- `/dev/fd` semantics: reader opens a duplicate of the bound descriptor; the
  verified inode is the consumed inode.
