# CG-A substantive repair: actual P3→P6 first consumer (sourcefree)

**Author baseline:** PR #915, `8248711fb8ba4ac07c0b0e6e7dfc4decce9352b7`.
**Repair PR:** #917 (isolated reviewer branch, based on frozen author; not protected-merged).
**Verified CI:** [push run #43157077711](https://github.com/maidiu/rawlsing/actions/runs/43157077711) and [PR run #43157155117](https://github.com/maidiu/rawlsing/actions/runs/43157155117), both SUCCESS at `10f948c84f3fbef7a51b9560a57084aaba6a6c05`. Tests ran with GitHub-hosted Python 3.11 and pytest. Initial CI failures were **test oracle errors**, not suppressed: P4 opening has one mediator instead of the separate P3 fixture's two; separately generated source histories have different provenance hashes. Both were corrected, then the actual tests passed.

## Actual causal path

`P4.new` (actual P2 root, P3 formation) → cold close/reopen → `P3Owner.store.query` → `qualified_p3_read` (same root, actor, branch, clock, source and frozen B1 registry) → P6 `situated.reconsider` packet → injected sourcefree `interpret` → existing P6 `session.product.say(actor="A")` if sourcefree chosen → committed actor speech event and P4 receipt.

The **three-case** test includes (1) actual prior-history vs no-mediator history using the same P6 interpreter; (2) source-hash mismatch and invalid clock refuse without changing stored state, exact restore recovers the identical read; (3) byte-identical copied P2/P3/P6 checkpoint: read edge enabled = actor speech; same frozen checkpoint with read edge omitted = no additional speech; restored read edge = actor speech again. The inherited `test_silent_interval_reconsiders_and_commits_only_admitted_speech` also passes. The P3 store head remains unchanged by read-only P6 consumption.

## What was wrong and what changed

The author's isolated `MEDIATOR{room=kitchen}` test used an independent fake source/registry and a local `later_decision`; it was not a real common P3/P6 writer. We keep material world and speech under P2/P6, keep psychological sourcefree B1 records under P3, and connect them with an optional strictly bound read-only first-consumer bridge. No new world ledger, scheduler, universal psyche registry or retrospective invented mother speech.

The 23-row exact-code matrix has 21 inspectable source tuples and two historic/unlocated records. Every one of the **21 commit/path/Git-blob identities** now matches directly retrieved GitHub source bytes. Corrected rows: 05 and 06 held SHA-256 values in a `git_blob` field rather than the actual 40hex Git object IDs; 21 used the abbreviated historical S47 commit `765a441f`, now resolved to `765a441f87292aa4c17794745b65cb54e6aaa83f`. Correctness of these source tuples is **not** acceptance of current native science, complete transitive source identity, or every historical candidate's functional suitability.

## Disposition

**Engineering:** proposed **ACCEPT_SCOPED_SOURCEFREE** for this demonstrable P3→P6 bounded consumer seam; code and tests complete on frozen author descendant. The conditional actor speech is driven by the **test interpreter**, not by a scientifically validated native developmental rule or real mother.

**Science and actor/human authority:** **HELD**. No CAN/ADP/Pyat positive rule issuance, native actor memory or authority, independent mother actor, world-owned dated home-period, full multi-actor transaction, C12 person, or operated human rights.

**Next actual work:** CG-B must write a dated home/period via world owner; CG-C must constitute an independent second actor and qualified event/perception; CG-D must bind those to the P3/P6 sourcefree reader, with negative and rollback. No meta-review chain is required to preserve this scoped evidence.
