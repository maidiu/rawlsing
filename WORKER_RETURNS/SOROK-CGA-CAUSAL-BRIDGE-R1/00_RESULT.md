# CG-A substantive repair: actual P3→P6 first consumer (sourcefree)

**Author baseline:** PR #915, `8248711fb8ba4ac07c0b0e6e7dfc4decce9352b7`.
**Repair PR:** #917 (isolated reviewer branch, based on frozen author; not protected-merged).
**Proof custody:** prior early-version [PR CI #43157155117](https://github.com/maidiu/rawlsing/actions/runs/43157155117) passed at `10f948c84f3fbef7a51b9560a57084aaba6a6c05`, but that earlier bridge was semantically overpermissive. The **activation-hardened** sourcefree code cut `ddccba7634784912a65d32ec26e532a5c1d3a19e` passed 4 new tests + 1 inherited P6 test at [PR CI #43159856355](https://github.com/maidiu/rawlsing/actions/runs/43159856355). Later source-qualified P6 test and expanded inherited-P3/P4/P6 suites must be checked at the final immutable PR HEAD, not inferred from earlier green. See `AGENT_A_ADVERSARIAL_HANDOFF.md` for commands, failure record, remaining attacks and explicit proof boundaries.

## Actual causal path

`P4.new` (actual P2 root, P3 formation) → cold close/reopen → `P3Owner.store.query` → `qualified_p3_read` (same root, actor, branch, clock, original B1 source and frozen rule registry, plus `projections.activate` role/relation/current actor access) → P6 `situated.reconsider` packet → injected sourcefree `interpret` → existing P6 `session.product.say(actor="A")` if sourcefree chosen → committed actor speech event and P4 receipt.

The primary multi-oracle suite includes (1) actual prior-history vs no-mediator history using the same P6 interpreter; (2) source-hash mismatch and invalid clock refuse without changing stored state, exact restore recovers the identical read; (3) byte-identical copied P2/P3/P6 checkpoint: read edge enabled = actor speech; same frozen checkpoint with read edge omitted = no additional speech; restored read edge = actor speech again. The inherited `test_silent_interval_reconsiders_and_commits_only_admitted_speech` also passes. The P3 store head remains unchanged by read-only P6 consumption.

## What was wrong and what changed

The author's isolated `MEDIATOR{room=kitchen}` test used an independent synthetic source/registry and a local `later_decision`; it was not a real common P3/P6 writer. The reviewer's first bridge also handed historical record modes to the model without P3 activation: **unearned**. That defect was repaired by reusing `test_rules._check_sources` and `projections.activate`. The primary positive now uses a committed P6 outward cue, not a fabricated actor memory. `actor_observed` derives from actor-local actually available self-actions, speech or cues. We keep material world and speech under P2/P6, keep psychological sourcefree B1 records under P3, and connect them with an optional strictly bound read-only first-consumer bridge. No new world ledger, scheduler, universal psyche registry or retrospective invented mother speech.

The 23-row exact-code matrix has 21 inspectable source tuples and two historic/unlocated records. Every one of the **21 commit/path/Git-blob identities** now matches directly retrieved GitHub source bytes. Corrected rows: 05 and 06 held SHA-256 values in a `git_blob` field rather than the actual 40hex Git object IDs; 21 used the abbreviated historical S47 commit `765a441f`, now resolved to `765a441f87292aa4c17794745b65cb54e6aaa83f`. Correctness of these source tuples is **not** acceptance of current native science, complete transitive source identity, or every historical candidate's functional suitability.

## Disposition

**Engineering:** candidate **ACCEPT_SCOPED_SOURCEFREE_PENDING_FINAL_EXECUTION_AND_RECEIVING** for this bounded P3→P6 consumer seam; do not confer independent review or exact-final-head pass before checking GitHub Actions at the ultimate commit. The conditional actor speech is driven by the **test interpreter**, not by a scientifically validated native developmental rule or real mother.

**Science and actor/human authority:** **HELD**. No CAN/ADP/Pyat positive rule issuance, native actor memory or authority, independent mother actor, world-owned dated home-period, full multi-actor transaction, C12 person, or operated human rights.

**Next actual work:** CG-B must write a dated home/period via world owner; CG-C must constitute an independent second actor and qualified event/perception; CG-D must bind those to the P3/P6 sourcefree reader, with negative and rollback. No meta-review chain is required to preserve this scoped evidence.
