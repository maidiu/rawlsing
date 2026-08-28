# G02 — V550 SHARD-BUILDER EXHAUSTIVE FUNCTIONAL ARCHAEOLOGY R1

Role: VOZHD TRII
Repository: `maidiu/rawlsing`
Branch: `agent/verkhovod-finalconserve-g02-v550-shardbuilder-r1`
Starting authority: Authority 38.

AUDIT ONLY. GitHub-ground every claim.

## Mission

Audit the entire historical V550 shard-builder family as an engineering system, not merely the final V550 row schema.

Search all accessible history/branches for filenames, commits, builders, assessors, backfills, shard manifests, completion sentinels, tests, receipts, and helper utilities associated with V550, V550 shards, question-completes, shard completion, source partitioning, or publication.

The current tree visibly contains examples such as `assess_v550_shard_completion.py` and `backfill_v550_question_completes.py`; do not assume these are exhaustive.

Recover every independently valuable function, including but not limited to:
- shard partition key and why that grain was chosen;
- source/question/component identity conservation;
- completeness detection;
- restartability/resume semantics;
- idempotence and duplicate prevention;
- atomicity/partial-shard handling;
- manifests/checksums/content identity;
- backfill/repair law;
- ordering/determinism;
- authority joins and source-native structure;
- denominator/weight/state preservation;
- failure detection and fail-closed behavior;
- reopen/audit/replay;
- publication/consumer contract;
- memory/streaming/boundedness or other operational safeguards;
- any explicit reason a simpler monolith or overwrite strategy was rejected.

## Critical distinction

`OLD_SHARD_FILE_FORMAT != VALUABLE_SHARD_BUILDER_FUNCTION`

A modern DAG may lawfully remove shards while still needing the old functions of resumability, completeness, auditability, deterministic identity, selective repair, etc. Recover the function separately from the mechanism.

## Required outputs

- `V550_SHARDBUILDER_FUNCTION_LEDGER.csv`
- `V550_OPERATIONAL_GUARANTEES.csv`
- `V550_FAILURE_AND_RECOVERY_LAWS.csv`
- `V550_MECHANISM_VS_FUNCTION.csv`
- `V550_PRIOR_RECOVERY_CROSSWALK.csv`
- `POSSIBLE_UNRECOVERED_V550_FUNCTIONS.csv`
- `RESULT.md`
- `CHANGED_FILES.txt`

Each row requires exact historical ref/file and implementation/test evidence or an explicit planned-only classification.
Do not modify production. Do not select architecture. Remain sibling-blind.

Success token: `G02_V550_SHARDBUILDER_EXHAUSTIVE_FUNCTIONAL_ARCHAEOLOGY_R1_COMPLETE`
