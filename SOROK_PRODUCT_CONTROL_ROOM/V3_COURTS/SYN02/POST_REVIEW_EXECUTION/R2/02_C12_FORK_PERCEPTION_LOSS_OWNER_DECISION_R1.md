# C12 fork perception-loss — original-source owner decision docket (critical path)

**Status: ORIGINAL C12 SOURCE OWNER DECISION REQUIRED; NOT A SOURCE PATCH AUTHORIZATION.**

Source of finding: SYN02-RP0-R2 `f13f74d3f92ef0732dc33e5d3ebc314b6d0c70df`, `01_REAL_S36_C9_AND_IMPORTED_C12_DDL_FORENSICS.md` + `04_SOURCEFREE_SQL_FAULT_PROBES_AND_OWNER_DOCKET.md` + `probes/probe_c12_mirror.py`. Actual source: imported `r26e.c12_integrity.QualifiedC12Store` and base `bp4.store.C12Store` at JOIN-E `7bf2da302996491ddf34b9a039fea47ac982d135`. The worker reported original source/SQL executed; a separate RRP0-R2 must confirm, not infer execution.

## Contradiction

Root branch had perception rows at clocks 10 and 11. Existing fork cut computed from episode/world_event/checkpoint but not perception and chose `fork_clock=10`, child fork carried only one perception. Actual existing `QualifiedC12Store.verify` returned `ok` for both parent/child. A newly designed mirror sidecar detected `C12_FORK_PERCEPTION_LOSS`; that sidecar is a sourcefree *proposal/probe*, not production.

A historically constituted person cannot safely have a supposedly clean branch that silently drops a received impression. This threatens actor-access memory, conditional developmental continuity and the N/N+1 real event ledger. Later sourcefree actor CAS correctness does not cure a corrupt fork in independent C12 world/perception history.

## Owner must choose, freeze and test

**Option A — Patch actual fork/readiness (preferred if compatible with original BP4/C12 invariants).** Include perception in the fork cut/actual-causal source bounds; copy exactly corresponding perception rows along with episode/world/checkpoint under one transaction; include perception count/identity in relevant branch roots or verification; recompute parent/child hashes, fork clock/cold reopen deterministically; test no phantom future, no partial fork after crash, no doubled views. Check original append-only triggers and mutable `branch.root_hash`; do not silently mutate accepted legacy receipts.

**Option B — Non-destructive hard guard if patch cannot yet be source-qualified.** Refuse `fork` whenever any perception lies beyond the actual last fork clock or parent/child counts/root integrity cannot be proved; emit `FORK_HELD`, NEVER `CLEAN`. A guard is a protective integrity invariant, not a developmental rule. This blocks unsafe native fork until full repair.

**Option C — HOLD** for missing original-owner capability/authority, with no source edit and product fork path disabled; source/actor memory remains uncertain.

The original C12/BP4 source owner, not Sorok architectural reviewer or independent RP0-R2 author, must select the exact code/branch and grant bounded sourcefree repair/guard scope. No autonomous Mac/code editor/subscription switch. Independently reproduce the defect before accepting any patch. Follow with separate hostile code review of sourcefree tests and cold forks.

## F1.1 prerequisite

C9 actor source custody and C12 world projection can be implemented only after independent RP0-R2 source review, C9/C12 owner freezes schema/readset/receipt roots and fork repair/guard. None of these is a native C11/C12 person release. C8 independent world and SCI05/Rule A/T originally issued science remain separate gate processes.