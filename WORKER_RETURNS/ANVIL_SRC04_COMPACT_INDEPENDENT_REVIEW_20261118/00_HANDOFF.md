# SRC04 compact staging — independent review

## Disposition

**SCOPED_ACCEPT_COMPACT_SOURCEFREE_PARITY** with exact caller/packaging defects.

The compact typed/gzip spool and checkpoint resume are correct on the
sourcefree matched fixture: no re-decode, cold reader, exact roots/counts,
full ordered object equality and replay equality all pass. The actual shared
witness caller can reach the path with the exact overlay candidate tree, but
its current startup disk gate and two caller defects prevent a clean real
launch story:
- the compact worktree's raw `rawlsing_next` tree is rejected by the candidate
  hash pin;
- direct producer resume without `--source-path` raises `TypeError`;
- the compact implementation is not runtime hash-pinned;
- direct `resume_single_pass` lacks its own current/revocation check;
- current free space is below the caller's startup floor.

## Matched rehearsal (independent rerun)

Source cut: `e35a9c79ea02035d9345d70205a3373ffeded913`
Manifest SHA-256: `05b648a5ee61a5e5a968f6c264635569d4c9bfc67d7810b0afd05e776b9d54c6`

Commands, from a fresh sourcefree root:

```text
compact_rehearsal.py baseline-stop
compact_rehearsal.py compact-stop
compact_rehearsal.py baseline-resume
compact_rehearsal.py compact-resume
compact_rehearsal.py reader
```

Results:

- Spool: baseline 551,124 bytes / 3 files; compact 38,851 bytes / 2 files.
- Both resumes report `decode_called=false`.
- Fresh `VerifiedDirectEstate` reader opened both outputs.
- Exact roots, manifest, all family counts, full ordered family payloads,
  `RespondentIdentity`, `RoutingEligibilityFact` and replay equal.
- Manifest: `733beddd3b3b6b82339666e5adab4ed6360a2e90ee0f3efe250e7225a0ce3346`.
- Counts: 90 events, 90 identities, 90 routing, 90 coordinates, 1 universe,
  1 question, 7 authority, 0 weights, 0 relation/replay families.
- Typed edge evidence: 45 substantive, 18 missing, 18 not-asked, 9 DK;
  9 exact zero values, 18 missing tokens, 18 negative tokens, 84 repeated
  occurrences; full compact event payloads equal.
- Zero-weight family is persisted as bytes=0/records=0/sha=null in the
  checkpoint and reconstructed as empty; reader count is 0.
- One-byte corruption of the compact `EmpiricalCoordinateFact.jsonl.gz` after
  checkpoint refused before decode/publication with
  `CHECKPOINT_SPOOL_MISMATCH` / `EmpiricalCoordinateFact`.

## Caller and config/CLI

- Exact overlay candidate tree:
  `MEASUREMENT_PREP/private-runtime/SRC04_OVERLAY_REPLAY_1795040438/tree`
  has `pre553_source_i02_handoff.py = 6ab7cb50…` and passes
  `--mode preflight` with `RUNTIME_OVERLAY_QUALIFIED`; q217 held at 38;
  177/3/181 scoped counts; source path not opened, statted, hashed or decoded.
- Raw `MEASUREMENT_PREP` worktree handoff hash is `801ff416…`, so the same
  preflight refuses with `CANDIDATE_SOURCE_HASH_MISMATCH`.
- Direct `--mode producer --resume-checkpoint ...` without `--source-path`
  raises `TypeError: expected str, bytes or os.PathLike object, not NoneType`
  at `witness_caller.py:207`. The shared `run` wrapper supplies source path
  from the grant, so this is a direct-subcommand defect, not a run-path
  source read.
- Current caller startup floor: 26,907,826,727 B; manifest available:
  15,569,469,440 B; run blocker `CURRENT_FREE_SPACE_BELOW_SINGLE_PASS_FLOOR`.
  The compact spool itself does not remove this startup gate.
- `witness_caller.verify_candidate` pins only
  `pre553_source_i02_handoff.py` and `candidate.patch`; the compact
  implementation `single_pass_handoff.py` is imported from the runner
  directory and is not runtime hash-checked (manifest hash `c87ad499…`).
- `resume_single_pass` validates checkpoint HMAC/config/request/grant/decision
  and does not decode, but it does not call the resolver/current check itself.
  The actual caller's `_grant` performs a pre-resume current check; direct API
  resume does not.

## Boundary

Read-only MEASUREMENT_PREP. Fresh sourcefree temp roots only. No original
source `.sav` read/open/stat/hash/decode, no real run, no product edit, no
prior scratch access, no wider review. The interrupted R3 original artifacts
were not accessed or modified.

Immutable source cut: `e35a9c79ea02035d9345d70205a3373ffeded913` on
MEASUREMENT_PREP. OWNER review return is the commit containing this directory.
