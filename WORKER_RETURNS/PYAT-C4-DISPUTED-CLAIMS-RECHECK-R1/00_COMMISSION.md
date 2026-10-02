# LAUNCH IN: OpenCode — Space Bunny Free
# ROLE: PYAT C4 — DISPUTED-CLAIMS INDEPENDENT RE-CHECK — R1
# REPOSITORY: maidiu/rawlsing

Branch:
`agent/opencode-pyat-hq183-c4-disputed-claims-recheck-r1`

Exact review base:
`8ff40d37de69db2d8a6053a7c2242f481677f1a4`

This is a **narrow re-check of four disputed claims only**. It is not a
rereview of the C4 freeze. Do not re-adjudicate O1-C01 through O1-C11.

## Hard prohibitions

- Do not execute C4.
- Do not access, hash, stat, inspect, decode or materialize any raw survey source.
- Do not discover or fill source locators.
- Do not issue or alter any warrant.
- Do not mutate production code.
- Do not adopt the freeze, lift HQ182's hold, or self-adopt.
- Do not "fix" the freeze. You are checking claims, not repairing artifacts.

Note on tooling: `python3` on this host is a **silent no-op** (exit 0, no
output, no writes). Any verification you attempt with `python3` will
false-pass. Use `node`, or `git` plumbing, and state which you used.

## Claims to check

### D1 — Route-B producer adopted authority, and the 21→23 correction

Two claims are in tension and both may be wrong.

Claim X (Space Bunny HQ182): the producer binding is established, because
the contract is declared in exactly 1 of 330 `rawlsing_next` files and
`execute_route_b_production` is defined in exactly 1.

Claim Y (Sol shadow HQ at `d0fc810d`): the freeze survives because the
producer "is byte-identical to the already-qualified M01 candidate."

The reconciliation asserts that Claim Y is **false**: the producer blob at
the freeze is `2385cd327dced3c5b887b59085aa0d21b04d78c3`, while at M01
bounded-court time it was `6560d7a9472600330be721ba0c3c82d0b04b621f`, changed
by commit `903c262e4` "Fix M01 authority preimage canonical verification"
(+7/-2 inside `verify_route_b_replay_receipt`).

The reconciliation further asserts a replacement basis: C4A's combined
court at `8f7efe690` included `rawlsing_next/tests/test_pre553_route_b_production.py`
with count 11, and the consolidated result was 533 collected / 530 passed /
3 failed, with all 3 failures being `test_fiabc_*` tests triaged INHERITED at
both accepted parents.

Verify or refute each of these. Specifically:
- Is Claim X sufficient to establish adoption, or does uniqueness fail to
  distinguish an adopted owner from an incidental module?
- Is Claim Y true or false? Check the blob history yourself.
- Does C4A's combined court actually exercise the producer's current bytes?
  Confirm the 11 tests are in the passing set and not among the 3 failures.
- Is the producer-inclusive closure exactly 23 modules, and are both delta
  modules free of P2X / DuckDB / subprocess / ctypes / dynamic-import edges?

### D2 — R7 actual wording and reproduction provisions

Read `WORKER_RETURNS/PYAT-C4C3-DARWIN-ANCHOR-RUNTIME-R1/01_ENVIRONMENT_LOCK.json`
at commit `1df64cc59` in full.

HQ182 asserted the record says the venv is "NOT durable and NOT reproducible
from the repository" and characterised that as self-declared
non-reproducibility. The reconciliation asserts that is **inaccurate**: the
actual text ends the sentence with "from this path alone", continues "The
reproducible content is the freeze below, not the path", and the record
supplies a `reproduce_command` pinning all 13 packages.

Verify the exact wording character for character. Then determine:
- What is genuinely required before a governed run — durable preservation,
  re-creation and re-qualification, or something else?
- Is the environment actually non-reproducible, or is the fingerprint merely
  incomplete?
- Is `reproducibility_caveat` (narwhals re-resolve) material to the C4 path?

State the residual class precisely: environment irreproducibility, or
fingerprint incompleteness, or both.

### D3 — 38 SHA-256 prefixes versus two complete Git tree identities

Census every hex-valued string in that same environment lock and classify by
length and by field name.

The reconciliation asserts: 32 values of 16 hex, all field-named
`*_prefix16`; 6 values of 32 hex, being 1 `base_interpreter_sha256_prefix32`
and 5 `distribution_hashes.compiled_extensions.*.cpython-311-darwin.so`
values that carry **no** prefix marker in the field name; and 2 values of 40
hex which are `no_repo_mutation.rawlsing_next_tree_before` and `_after`, both
`b0c1ab472cde033e21f1c2f63fbcbea2f0cccef0`, which are **complete Git SHA-1
tree identities**, not truncated SHA-256. Total 38 + 2 = 40 short hex values.
Three further values are complete 64-hex SHA-256, all equal to
`9cde8e5ab9abba46a9e98826100ed084a0943a77fee7bc232a3c7643334da2eb`.

Confirm or correct the census. Then state whether the 38 prefixes are
sufficient for their declared purpose, distinguishing the base interpreter
fingerprint from the distribution fingerprints.

### D4 — R9 precise gap and R10 recoverable digest

R9: compare C4B's warrant template
(`WORKER_RETURNS/PYAT-C4B-WORKLOAD-ORACLE-FREEZE-R1/07_UNSIGNED_SOURCE_WARRANT_TEMPLATE.json`
at `c2af4f61`) against the fan-in candidate
(`WORKER_RETURNS/PYAT-C4-EXECUTABLE-FREEZE-FANIN-R1/04_SOURCE_EXECUTION_WARRANT_CANDIDATE.json`
at `8ff40d37d`) and the fan-in accounting law
(`07_EXECUTION_ACCOUNTING_AND_FAILURE_LAW.json`).

Determine precisely what per-source accounting survives and what does not.
The reconciliation asserts that per-source constraints are **not** lost —
artifact 07 retains 8 sources with `expected_full_reads`,
`expected_selected_reads`, `max_retry_budget` and `retry_law`, and the
candidate retains `max_retry_budget`, `expected_operation_class`,
`reader_lane` and detailed `allowed_operations` — and that the only missing
element is explicit per-source read-limit counters inside the warrant
instrument. Confirm or refute. Do not manufacture a freeze blocker.

R10: the candidate's oracle law carries
`"T3_freeze_sha256": "7dfb6..."`. The reconciliation asserts the full digest
is recoverable from C4B `04_WVS_ORACLE_CUSTODY.json` as
`7dfb62362b983b92dee2774d862a46c0c0ce3ca2c3bb48850e0f400346936908`. Recover
it yourself from governing evidence. Do not guess a digest.

## Required output

Write only:

`WORKER_RETURNS/PYAT-C4-DISPUTED-CLAIMS-RECHECK-R1/**`

- `00_RECHECK.md`
- `01_D1_ROUTE_B_ADOPTED_AUTHORITY.json`
- `02_D2_R7_ENVIRONMENT_WORDING.json`
- `03_D3_HASH_CENSUS.json`
- `04_D4_R9_R10.json`
- `05_FINAL_DISPOSITION.json`

For each of D1..D4 return one of: `UPHELD`, `CORRECTED`, `REFUTED`,
`INSUFFICIENT_EVIDENCE`, with the exact command output or file path/line
that supports it, and the tooling you used.

Stage-separate your conclusions: freeze-acceptance blockers, warrant-issuance
blockers, live-execution blockers, advisory.

## Allowed dispositions

- `ALL_FOUR_CLAIMS_UPHELD`
- `UPHELD_WITH_CORRECTIONS`
- `MATERIAL_CORRECTION_REQUIRED`
- `INSUFFICIENT_EVIDENCE_TO_ADJUDICATE`

Terminal:

`C4_DISPUTED_CLAIMS_RECHECK_RETURNED__HQ_ADJUDICATION_REQUIRED`