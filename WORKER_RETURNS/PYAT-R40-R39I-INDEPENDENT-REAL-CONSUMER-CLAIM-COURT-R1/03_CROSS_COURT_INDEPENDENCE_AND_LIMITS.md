# Cross-court independence, methodology and limits

## Independence of this court

- Fresh arm's-length reviewer: not E04L/F6P author, not HQ, not the new adapter author, not source/semantic issuer, not actor. No author process state was reused.
- Separate governed sparse worktree `R40-R39I-reviewer-wt` sharing the object store, created by this reviewer from the sealed startup `1150e836e`, distinct from the E04L, F6P, EE1 and all other live author worktrees. No colleague worktree was reset.
- The two courts did not commission a further reviewer and did not block O35B/WV1/EE1.
- The author returns are self-contained under their own `WORKER_RETURNS/` directories; no shared production file was modified by either author, and the reviewer touched no shared production file.

## Independent oracle vs author expectation

For both courts the reviewer froze the expected values **before** reading the author's asserted outputs as an oracle:

- Court A: values recomputed from `synthetic_world_rows()` and the producer fact objects. The author's hard-coded `14/18`, `6/10`, `2/6` are consistent with, but not used as, the reviewer oracle.
- Court B: all W1/W2/W3/W7 exact rationals recomputed from the frozen world builders' counts with reviewer arithmetic; the author's `01_FROZEN_ESTIMANDS…json`, `f6c_method_c` and candidate outputs are not used as the reviewer expectation.

## Fault efficacy is claim-specific, not incidental

Each injected fault targets the genuine commissioned edge and the named test fails **by its own assertion** (gate reports `TARGET_ASSERTION_FAILED`, `errors=0`, `skips=0`), not by import error or an unrelated test:

- E04L severed selected release → original consumer productive assertion RED.
- E04L stale B5 selection → stale-selection refusal assertion RED.
- F6P consumer uncovered-mass read → partial-preservation assertion RED.
- F6P actual F6M producer decision corruption → consumer-follows-producer assertion RED.

In all four cases the exact source was restored (blob-verified) and the named test returned green.

## Claim grain

- E04L "read-through" = live B5/M2/I4 gating over producer-owned fact objects; not release-inlined payloads.
- F6P = a bounded TEST_ONLY read-only F6 evidence client; not an E04 join, not a route model, not a transport permission.
- Both positives are `EXECUTED_GREEN` and `ASSERTION_EFFICACY_PROVED`; the wider integration/realsource claims remain `NOT_PROVED`/`NOT_RUN` and are explicitly preserved as holds.

## What this court does NOT do

- No production promotion, no source/model/actor/N11/N12/V3 issuance, no HQ succession, no re-sealing of any commission.
- No global completeness audit of unrelated historical suites; inherited/unrelated REDs (none encountered here) would be recorded separately.
- No claim that arbitrary test quality is mathematically guaranteed.
