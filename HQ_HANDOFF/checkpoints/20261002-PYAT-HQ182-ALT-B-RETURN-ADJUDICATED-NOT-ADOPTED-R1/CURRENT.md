# PYAT HQ182 — ALT-B RETURN ADJUDICATED (NOT ADOPTED INTO BUILD)

Status:
`C4_FINAL_REVIEW_ALT_B_RETURN_ADJUDICATED__FREEZE_ACCEPTED_AT_SOURCE_FREE_GRAIN__NOT_ADOPTED_INTO_BUILD__HELD_FOR_EXTERNAL_ASTRA_COMPARISON__RAW_SOURCE_EXECUTION_HELD`

Decision:
`HQD-2026-10-02-182`

Adjudicator:
HQ/Vozhd on OpenCode — Space Bunny Free

Subject return:
`3a5b2cbc7f1978384268376f3ee493c7c095780b`
on `agent/reviewer-pyat-hq181-c4-executable-freeze-final-integration-review-alt-b-r1`

Subject disposition:
`APPROVE_AT_DECLARED_GRAIN`

## Adoption status

`NOT_ADOPTED_INTO_BUILD`

This decision adjudicates the alt-B return and records HQ's findings. It
does **not** adopt the C4 executable freeze into the build, does not advance
the build toward warrant issuance, and does not bank the residual register
as governing program state. Adoption is withheld pending external
cross-model adjudication by Astra on a separate machine.

Lane A remains unadjudicated and unread by this HQ instance.

## Branch reconciliation

- Exactly one commit over commission tip `2836f6259`.
- Parent of `3a5b2cbc7` is `2836f6259` exactly.
- 8 files added, 0 modified, 0 deleted, 1891 insertions.
- All 8 paths under `WORKER_RETURNS/PYAT-C4-EXECUTABLE-FREEZE-FINAL-INTEGRATION-REVIEW-ALT-B-R1/`.
- Zero `rawlsing_next/**` movement.
- No lane A content imported: single commit, additions only.

## HQ independent re-derivation

HQ re-derived the load-bearing claims from git objects rather than accepting
the return's assertions.

Verified exact:

- `rawlsing_next` tree `b0c1ab472cde033e21f1c2f63fbcbea2f0cccef0` is
  identical at all seven points the return names: `9a5752a8`, `8f7efe690`,
  `01256977`, `39015a90`, `f8c8e2e4`, `8ff40d37`, `2836f625`.
- First-parent count of `01256977..8ff40d37` is 3; total reachable is 5.
  The two extra reachable commits are exactly `1df64cc59` (C4C3 return) and
  `eba2f4249` (its HQ bind) — the declared merge side. Count discrepancy is
  resolved as a pure counting-basis difference with nothing unreviewed.
- Fan-in lineage `01256977..8ff40d37` is 47 files added, 0 modified,
  0 deleted, all confined to `WORKER_RETURNS/`.
- Warrant candidate SHA-256 recomputes to
  `d57420f8016bf49cc0353f39dcd2271e6f370c3bd9b7e81f08466c0a1f574e0a`.
- Route-B producer blob at C4A is `2385cd327dced3c5b887b59085aa0d21b04d78c3`.
  The contract `PYAT_M01_ROUTE_B_PRODUCTION_COMPOSITOR` is declared in
  exactly 1 of 330 `rawlsing_next` files, and `def execute_route_b_production`
  is defined in exactly 1. The binding is correct and unique, established by
  uniqueness search rather than by the fan-in's naming of it.

Verified as claimed, and material:

- **R9 confirmed and correctly scoped.** C4B's warrant template carries
  `source_access_accounting` on every source with 7 named slots
  (`full_file_sha256_passes`, `path_opens`, `decoder_invocations`,
  `metadata_header_reads`, `selected_reads`, `full_reads`, `retries`) across
  7 sources. The fan-in warrant candidate's `per_source` entries carry no
  `source_access_accounting` at all. The candidate's replacement
  `access_accounting_instrumentation_bound` lists 10 account types globally —
  a richer taxonomy than C4B's 7, but instantiated zero times per source.
  The loss is therefore the per-source binding, not the taxonomy. Correctly
  classified as blocking warrant issuance and not blocking the freeze.
- **R10 confirmed exactly.** `05_ORACLE_AND_COMPARISON_LAW.json` line 44
  carries `"T3_freeze_sha256": "7dfb6..."` — a truncated literal in a
  machine-readable identity field, sitting beside two full 64-character
  digests in the same object.

Corrected as to weight — the return **understated** R7:

- C4C3's `01_ENVIRONMENT_LOCK.json` states in its own words that the venv
  lives in a per-session temporary directory and is NOT durable and NOT
  reproducible from the repository. This is C4C3's own self-declaration, not
  the reviewer's inference.
- The qualified interpreter resolves under
  `LOCAL_COURTS/tooling/python/cpython-3.11.3-macos-x86_64-none/bin/`, and
  `LOCAL_COURTS/` is untracked in this repository. The interpreter is
  genuinely uncommitted.
- C4C3's environment lock contains **40 truncated hex identity literals**,
  e.g. `11d6f541a870a141249ce98d45834a67`. The return cited a single
  16-byte prefix; the actual scale is 40 fields.
- `repository_dependency_lock_exists` is the only lock reference in the
  fan-in runtime law, confirming the no-lock ground.

HQ therefore upgrades R7's severity: it is not merely a precondition but a
self-declared non-durability in the qualified surface, and it must be
resolved before any governed run.

## Residual register as adjudicated

| Class | Count |
|---|---|
| blocking executable-freeze acceptance | 0 |
| blocking warrant issuance | 1 (R9) |
| blocking live execution | 1 (R7, upgraded) |
| advisory / nonblocking | 9 |
| counterexamples requiring escalation | 0 |

## HQ disposition

`UPHELD_AT_DECLARED_GRAIN__NOT_ADOPTED_INTO_BUILD`

The alt-B disposition `APPROVE_AT_DECLARED_GRAIN` is upheld on its declared
grain. HQ independently reproduced its load-bearing determinations and found
no contradiction. HQ records that the return's R7 was materially understated
in scope and upgrades it accordingly.

Approval semantics are unchanged and expressly limited: acceptance of the
source-free freeze at declared grain only. It authorises nothing. No raw
survey file may be opened, stat-ed, hashed, metadata-read, decoded or
materialised. No locator may be discovered. No warrant is issued.

## Held

- adoption of the C4 freeze into the build
- source locator discovery and fill
- warrant issuance
- raw-source access and live C4 execution
- lane A adjudication
- C7
- actor/person work

External comparator:
Astra, separate machine, retrieving from `origin`.