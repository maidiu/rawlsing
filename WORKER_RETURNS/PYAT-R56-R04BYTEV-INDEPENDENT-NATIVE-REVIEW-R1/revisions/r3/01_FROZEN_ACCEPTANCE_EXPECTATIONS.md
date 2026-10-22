# R56-R04BYTEV r3 — frozen acceptance expectations

Written BEFORE executing the R3 candidate tests or generating R3 candidate
outputs. Derived from the frozen R1/R2 semantics, decision packet 22, and the
immutable R2 negative baseline (`228387c59`), not from R3 receipts.

## 1. Unchanged facts (same oracle as R1/R2)

- Generated SAV/DTA from `_ROWS`: 21 physical cells; Y values 1,0,1.
- C11 `RespondentEvent` count 21; I03 fact for Y over the all-respondent branch
  cohort with risk set R (Y members R1,R2): `SUPPORTED`, denominator 2,
  cells `{"0": 1, "1": 1}`, numerator support 2.
- Identical bytes -> identical release/fact identities; different bytes ->
  different identity. Baseline facts must remain byte-for-byte identical in
  every denied-write attack.

## 2. Read-only handoff expectations

1. Retained reader `snapshot.fd` is `O_RDONLY` by `fcntl(F_GETFL)`; reported
   `access_mode == "O_RDONLY"`, `source_custody["reader_access_mode"] ==
   "O_RDONLY"`.
2. A distinct construction writer exists only during acquisition; it is closed
   before the incidence escapes, and no decoder state retains it or any
   writable alias/map. A `/dev/fd` listing must not show the construction fd;
   the reader fd must be present and read-only.
3. Bound checks are real: reader and construction dev/ino match; size matches;
   `snapshot_sha256 == source digest == sha256(file bytes)`; accepted inode has
   `st_nlink == 0` and the construction pathname is unlinked.
4. Snapshot pathname is unlinked; `source_custody["snapshot_path_unlinked"]`.
5. `reader_path` is `/dev/fd/{reader_fd}`.

## 3. Denied ordinary write capability (declared threat contract)

Through the supplied reader fd only (no fchmod/new-permission grant, no private
state substitution), each of these must be denied BEFORE modification and the
same frozen facts must survive and be served:
- `os.write(fd, ...)`;
- `os.pwrite(fd, bytes, 0)`;
- `os.ftruncate(fd, n)`;
- `mmap(fd, ACCESS_WRITE)` and `mmap(dup(fd), ACCESS_WRITE)`;
- `os.open("/dev/fd/{fd}", O_RDWR)` and `O_WRONLY`;
- `fcntl(fd, F_SETFL, ...)` must not change the access mode.
After each denial: full digest via the reader fd equals the acquisition digest,
and actual C11/I03 facts equal the frozen positive baseline.
Mere raw exception without unchanged-fact control is insufficient.

## 4. Wrong/closed/non-read-only fd diagnostics

- Normal `close()` -> methods typed-refuse (`DecoderError`), access mode
  `CLOSED`, snapshot path/dir removed, no facts.
- A substituted non-read-only fd or a read-only non-regular fd must typed-refuse
  (`DecoderError`) rather than serve bytes.
- An OS-closed descriptor with `_closed` unset is an item-1 robustness check;
  record the actual exception type honestly (expected typed `DecoderError`).
- Handoff failure paths (reader-open failure, pathname replacement before
  unlink) must fail closed/typed, close both descriptors, remove the temporary
  acquisition path when safe, and must not delete a foreign replacement.

## 5. Window/lifetime requalification

- Original-path replacement after acquisition and between metadata/lazy phases:
  frozen facts, original source/snapshot/release/fact identity.
- Private-path re-creation at the old snapshot pathname before metadata,
  between verify and reader, and after acquisition: not consumed; facts frozen.
- Metadata, compatibility full read, SAV lazy, DTA full value path all read the
  bound read-only fd.
- Repeated `iter_cells`/`iter_batches` calls stable; `close()` lifetime;
  genuinely changed same-path bytes acquired anew get a new identity; old
  incidence keeps original facts.
- Fresh-process old-digest cold replay: changed bytes refused with no fact
  output; restoring exact bytes reproduces the identical fact payload.

## 6. Read shape / limits

- SAV keeps `read_file_in_chunks` streaming; no whole-SAV buffering and no
  per-chunk full-file rehash.
- DTA normal value pass is one full `read_dta` frame per pass (installed chunk
  reader cannot consume `/dev/fd` DTA), O(rows x cols); no original35-scale
  claim.
- POSIX `/dev/fd` required; unavailable -> typed `DecoderError`.
- DTA extended-missing writer skip remains unqualified; compatibility
  full-read tests are TEST_ONLY synthetic allowlist, not installed encoding
  authority.

## 7. Author result to reproduce

- Focused module: 26 passed; core: 90 passed, 1 skipped (the known
  `test_pre553_sr06_decoder_carrier.py:268` writer/readback skip).
- Proof-integrity lint and three-claim witness; decoder restored byte-exact.
- Inherited 10 R1E/R1I/R1J failures were established baseline-identical at R1;
  no new sweep unless R3 shows a concrete regression.

Threat boundary: after handoff ordinary writes through the supplied reader
capability are denied. Deliberate new permission grants (e.g. fchmod + new
write open), private-state/code substitution, dup2, ptrace/root are excluded
by packet 22 and are not ordinary-reader-contract evidence.
