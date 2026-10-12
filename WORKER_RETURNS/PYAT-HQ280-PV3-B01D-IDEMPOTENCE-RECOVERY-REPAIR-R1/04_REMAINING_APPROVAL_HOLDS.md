# B01D — Remaining approval holds

## 1. Custody

| Item | Value |
|---|---|
| Sealed startup (verified before mutation) | `d4bb1907dbb1e00fcb6526489d18ad3796c7013e` |
| Branch | `agent/rabochii-pyat-hq280-pv3-b01d-idempotence-recovery-repair-r1` |
| Repaired candidate | B01C `88a2b4c1916c73d30cae4c2ffe48d083eb2e0667` |
| Reviewer finding | B01CR `c7dab90ff7b853c62f6dd9778e7e002d0d1564d6` (W6) |
| Interpreter | Python 3.11.3 (`.pv3-venv`), macOS-13.7.8-x86_64 |
| Raw `.sav`/`.dta` in worktree | **0 files** |
| Source read / source-use grant | **none** |
| Canonical / semantic PRE-MAIN | **unmutated** |
| Self-adoption / merge | **none** |
| ZIP relay | **none** — all evidence is modest text/JSON pushed to the branch |

Changed files (only): `rawlsing_next/pre553_batch_durable_checkpoint_candidate.py`
(+85/−~18) and `rawlsing_next/tests/test_pre553_batch_durable_checkpoint_candidate.py`
(+303/−~10). Verified: `git diff --stat d4bb1907d… -- rawlsing_next/` lists
exactly these two files; every accepted owner (batch runner, protocol,
carrier, empirical objects, repository, discovery) is byte-identical.

## 2. Safe hosted bounded resource record

Measured recorder process, real subprocesses, bounded manifests:

| Measure | Value |
|---|---|
| Peak RSS | **15.9 MiB** |
| User CPU | **0.093 s** |
| System CPU | **0.084 s** |
| Recorder wall | **~1.1 s** |
| Crash worker wall | ~90 ms per real SIGKILL phase |

**Bounded development-scale numbers only — not a capacity forecast.**

## 3. Approval holds — what this repair does NOT establish

1. **`IDEMPOTENCE_ISSUER_HOLD` (new, explicit).** No accepted owner issues a
   verifiable idempotence credential, so `RERUN_SAFE` is unreachable and every
   unknown outcome stays HELD. A future competent issuer must supply exact
   unit/release/manifest/executor/side-effect fields plus a verifiable
   signature/schema (see `01_...md` §4). Until then, non-idempotent external
   work involved in a crash-window loss is **unrecoverable by rerun** — HELD
   is the terminal safe state, not a prelude to execution.
2. **No REAL_EXECUTION grant.** The protocol module is unmodified and still
   controlling; this packet neither requests nor constitutes approval.
3. **Exactly-once external execution is NOT proven** — only the safe HOLD and
   the tangibly demonstrated duplicate-under-old-rule are proven.
4. **Single-host `flock` only**; NFS/distributed semantics unsupported
   (inherited B01CR hold 4, unchanged).
5. **Crash-consistency is phase-bounded**: measured for START→side-effect→kill
   and COMMIT→kill windows, torn files, lock contention. Hardware/FS lies,
   disk exhaustion, and multi-host races are outside the envelope.
6. **Scale is bounded** (1–4 unit manifests). No large-manifest checkpoint
   cost or fsync-throughput characterisation.
7. **B01 F-04/F-05/F-06 and P17** inherited unchanged, out of scope.
8. **Full repository suite not run** per commission scope; no claim made about
   it either way.

## 4. Competent-owner decisions required

| Decision | Owner |
|---|---|
| Accept/reject this candidate-only repair | HQ / competent owner |
| Issue (or decline) a verified idempotence credential + issuer | execution/authority owner |
| Whether HELD-forever is acceptable for non-idempotent crash losses | runtime owner |
| REAL_EXECUTION approval, if ever sought | protocol owner |

**Terminal:** `HQ280_PV3_B01D_CALLER_IDEMPOTENCE_FORGERY_CLOSED_OR_TYPED_HOLD__SOURCEFREE__GITHUB_PUSHED`.