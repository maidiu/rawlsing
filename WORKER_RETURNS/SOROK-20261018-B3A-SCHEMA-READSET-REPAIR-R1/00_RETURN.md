# B3A schema/readset repair — author return

**Fixed locally: the two unchanged schema falsifiers now PASS.** Schema-only public changes cause immediate refusal; no_mutation accounts for schema and version metadata as well as rows. No frozen test or prior independent return was edited.

The user explicitly requested this repair after the completed B3A-I2 court. This is a new bounded author task, not a continuation claiming the prior reviewer's independence. Local branch: `codex/sorok-b3a-schema-readset-repair-r1`, based on exact author candidate `8bd4d6b01fd402e7e6a8d07903f2c3cada837f55`. Prior independent review: `528e8cde0cff9e28f3c55d5d54a66e820d7401fa`. No new HQ seal/commission was invented, and no remote push, production change or canonical integration was attempted. The containing local commit identifies this runnable candidate.

## Change

Only inherited `candidate/integration.py` changes. Its content SHA-256 is `6b0187c5dfa0a48928f78fb0c3979de6c35e49aa770c9d10f644f57eaed6a679`; Git blob SHA-1 is `d3a324bb93c17fdaf12670dd153aeb138d9c426a`. `input_manifest.json` binds all copied inputs; all other inherited Python files and frozen review/atomic/X3 tests retain their exact input blobs. Runtime materialization verifies the same pinned B2/M2/F2 closure; no newer M2 implementation is included.

The new consistent logical snapshot contains schema definitions for tables/indexes/triggers/views, all table rows, and SQLite schema/user/application version metadata. It uses a read transaction when needed and preserves an existing caller transaction. The existing row-only snapshot API stays compatible, with table identifiers safely quoted. The public snapshot is rechecked under BEGIN IMMEDIATE; scratch schema/metadata drift is refused. Domain-refusal receipts compare the same logical state, preserving external changes rather than removing them.

SQLite backup can advance the destination schema cookie. Scratch version is therefore checked against its own immediate post-backup baseline, while public version remains bound to the original public readset. Schema definitions and user/application metadata still agree across both copies. The first development patch compared cookies across files and falsely refused ordinary success; the rollback-acceptance control caught this. Its 14 PASS /1 RED development output is preserved, not counted as final qualification.

## Actual execution

| Court | PASS | RED |
|---|---:|---:|
| Two unchanged schema falsifiers, before fix | 0 | 2 |
| Same two falsifiers after fix | 2 | 0 |
| Full frozen reviewer court plus 13 new repair controls | 33 | 0 |
| Clean/seeded bad-origin/future-event refusal controls | 4 | 0 |
| Unchanged B3 suite | 71 | 0 |
| Unchanged B3A atomicity suite | 63 | 0 |
| Unchanged F2 | 42 | 0 |
| Blinded F2 IDs/expectations | 42 | 0 |
| Unchanged X3 | 24 | 4 |

Zero final errors/skips. The two repaired falsifiers are included in the 33, not an additional population. That court includes ten real SIGKILL controls; the atomic suite separately includes twelve. Both positive and permission-absent loops matched every receipt and complete SQL schema/table snapshot on cold reconstruction; integrity checks returned ok. Blinded F2 retained 20 eligible /22 refusal-or-deferral, with no oracle routing inside the engine. Raw logs/JUnit, full SQL receipts, commands, actual imports and verification are under evidence/.

New controls cover index/view/trigger changes; schema/user/application version changes; create/drop schema ABA; quoted table names; truthful external-change flags after domain refusal; private scratch schema drift; rolled-back external DDL acceptance; and an existing write transaction remaining uncommitted while snapshotted. Independent B2 facts remain intact and no proposed occurrence/target effect leaks on refusal.

The four X3 REDs remain the same: duplicate physical-check IDs, the stronger pre-loss expectation, standalone helper missing-readset expectation, and the obsolete delayed-detection race assertion. No target/practice rule was changed to turn them green. Older B2/E3/inherited courts, native F1 and M3 were NOT rerun for this B3-only patch; their prior results remain historical evidence, not new PASS claims. Their unchanged source/grant limitations remain in force.

## Limits and custody

This repair is an author-tested sourcefree candidate, requiring a distinct independent reviewer for acceptance. The original independent review remains immutable and applicable to its old target. No self-acceptance, CAN008/CAN011 law, selected belief/affect, habit-acquisition calibration, actor/source grant, memory/access permission, native F1 closure, M3 closure or production integration follows.

The readset is logical database state; physical file layout, connection-local settings and arbitrary privileged SQL forgery are outside it. Whole-store staging remains O(database size). SIGKILL recovery is not power-loss/fsync proof. No unrelated developmental threshold or psychologically predetermined outcome was introduced.

All new tracked files are confined to this repair return subtree in a separate managed worktree. The prior review/author worktrees and shared canonical files were left unchanged. Pinned source and test bytes remain exact; only new receipts are sanitized for local paths/hostnames. Local Python/pytest/SQLite/Node, unchanged source closure and actual imports were verified. No package installation, model/provider switch, delegation, paid external model or original-source execution occurred.

AUTHOR_REPAIR_COMPLETE_PENDING_DISTINCT_REVIEW. No background execution remains.
