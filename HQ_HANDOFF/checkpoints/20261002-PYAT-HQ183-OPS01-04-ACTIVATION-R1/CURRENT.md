# PYAT HQ183 — OPS-01..04 ACTIVATION, C4 RECONCILIATION PREPARED

Status:
`OPS01_04_COMPLETE__C4_RECONSOLIDATED__DISPUTED_CLAIMS_RECHECK_BOUND__HQ182_HOLD_UNLIFTED__RAW_SOURCE_EXECUTION_HELD`

Decision: `HQD-2026-10-02-183`

Base: `55ba382dccb88494d219a945c17efc166e456bd2`
Activation branch: `agent/opencode-pyat-hq183-ops01-ops04-activation-r1`

## What this decision does

Records the Space Bunny OpenCode HQ activation: OPS-01 frontier
reconciliation, OPS-02 minimal orchestration setup, OPS-03 independent
qualification, and OPS-04 consolidated C4 decision claims.

It does **not** adopt the C4 freeze. It does **not** lift HQ182's hold. It
does **not** issue a warrant, discover a locator, or access any raw source.

## Material corrections this run

Against the governing evidence, three claims did not survive, and two of
them originated in HQ182 — my own prior adjudication.

1. **Sol shadow HQ's byte-identity justification is false.** The producer
   blob at the freeze is `2385cd32`; at M01 bounded-court time it was
   `6560d7a9`, changed by `903c262e4`. The *conclusion* survives on a
   stronger and correct basis that neither lane stated: C4A's combined
   court exercised the producer's current bytes. Its 11 tests are among
   the 76 passed; all 3 failures are `test_fiabc_*`, triaged INHERITED.

2. **HQ182's R7 wording was inaccurate.** The record says "NOT reproducible
   from this path alone", not "from the repository", and continues "The
   reproducible content is the freeze below, not the path", with a pinned
   13-package `reproduce_command`. R7 is reclassified from environment
   irreproducibility to **fingerprint incompleteness**.

3. **The hash census was wrong on both count and character.** Correct
   figure: 38 SHA-256 prefixes (32 of 16 hex, 6 of 32 hex) plus 2 *complete*
   40-hex Git SHA-1 tree identities. HQ182 said "40 truncated SHA-256
   identity literals".

R9 was also narrowed: per-source constraints are **not** lost; only explicit
per-source read-limit counters are absent from the warrant instrument.
R10's full digest was recovered from C4B, not guessed.

## Stage-separated blockers

- Freeze acceptance: **0**
- Warrant issuance: **1** (R9, narrowly restated)
- Live execution: **1** (R7, reclassified as fingerprint incompleteness)
- Advisory: 9
- Counterexamples: **0**

## OPS-03 result

23 pass / 0 fail / 1 declared skip. Level `PASS_WITH_DECLARED_SKIP`.
The skip is Q12 raw-directory denial, left deliberately unqualified: role
isolation is **procedural**, not process-enforced, and closing it needs host
administration permission not granted.

Qualification found and fixed two real defects in my own dispatcher: the
slot cap was not enforced at submission, and terrain globs were treated as
literal prefixes.

## Environment defect

`python3` is non-functional on this host: silent no-op via shell, and
`Unknown system error -8` via `execFileSync`. The packet's own
`scripts/verify_packet.py` **cannot be executed**. Packet integrity was
confirmed by an independent node reimplementation of its exact algorithm
(19/19 files). Any agent reporting that script as passed here is wrong.

## Pending

External Astra adjudication of the C4 reconciliation. A fresh independent
re-check of the four disputed claims is bound at
`agent/opencode-pyat-hq183-c4-disputed-claims-recheck-r1 @ dd00896848c98de5e6ff124fd50f8508431fc0ff`.

Terminal: `OPS01_04_COMPLETE__C4_RECONSOLIDATED__RECHECK_BOUND__HQ182_HOLD_UNLIFTED`
