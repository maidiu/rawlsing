# PYAT HQ184 — PYTHON3 REPAIRED, PACKET VERIFIER RUNS NATIVELY

Status:
`ENVIRONMENT_DEFECT_RESOLVED__PACKET_VERIFIER_EXECUTED_AND_PASS__OPS03_REQUALIFIED__HQ182_HOLD_UNLIFTED__RAW_SOURCE_EXECUTION_HELD`

Decision: `HQD-2026-10-02-184`
Base: `54d0dec2a56f680250c066194c4a77d9f0116160`

HQ183 is preserved unmodified. This is a successor decision.

## What changed

`python3` was non-functional during OPS-01..04: silent no-op via shell,
`Unknown system error -8` via `execFileSync`. It is now Python 3.11.3 at
`/usr/local/bin/python3`, repaired at the user's direction.

## What was re-verified natively

- `PYAT_CONTROL_ROOM/SPACE_BUNNY_OPENCODE_R1/scripts/verify_packet.py`
  **EXECUTES**: `PASS: 19 delivery files verified`, exit 0.
- **Negative control**: a deliberately corrupted `README.md` sha256 in
  MANIFEST.json produced `FAIL: integrity mismatch: README.md`, exit 1. The
  verifier genuinely detects tampering rather than always passing.
  MANIFEST.json was restored and re-verified clean.
- **Cross-implementation agreement**: the shipped python verifier and HQ's
  earlier node substitute agree on all 19 files, sha256 and git blob sha1,
  with **zero disagreements**.

## OPS-03 re-qualification

Re-run with functional python: **23 pass / 0 fail / 1 declared skip**,
level `PASS_WITH_DECLARED_SKIP`. Q11 now reports
`python3 FUNCTIONAL (wrote file; exit-0)`.

The single skip is unchanged and deliberate: **Q12 OS-level raw-directory
denial remains unqualified.** Role isolation is procedural only.

## Unchanged

The dispatcher stays node by design; python3 is now additionally available
to workers. HQ183's checkpoint bytes are untouched. The C4 reconciliation,
all holds, and the pending Astra adjudication are unchanged.

Terminal: `ENVIRONMENT_DEFECT_RESOLVED__PACKET_VERIFIER_NATIVE_PASS__HQ182_HOLD_UNLIFTED`
