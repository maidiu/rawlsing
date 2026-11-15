# EE-R2D — ROUTING AUTHORITY BATCH REGISTRY

Repository: `maidiu/rawlsing`

Exact branch: `agent/rabochii-prev3-ee-r2d-routing-authority-batch-registry-r1`

Read current canonical HQ authority from `HQ_HANDOFF/LATEST.json`, EE-W3 return head `cf609f6447d0bb8d07de14c5116e6b6dfdf4f943`, N04-R4B return head `f1f977910e5f0f40da4ddb0d0f329be556e7b718`, and `WORKER_RETURNS/EE-W3/05_SCALE_AND_FINISH_PLAN.md`.

Exact grain:
`PARTITION_EXACT_159_CLASS_D_ROUTING_RESIDUALS_INTO_FINITE_SOURCE_RULE_AUTHORITY_UNITS_AND_FREEZE_DISPATCH_REGISTRY_ONLY`

Library permission: `NO`.

Start from the exact 159-ID residual. Partition only where exact source routing-document/rule authority itself establishes common coverage. Preserve rows without a recoverable owner or with conflicted authority as exact true residuals.

Required outputs:
- exact 159-row accounting with zero missing/duplicate rows;
- finite source-rule batch registry;
- exact source/routing owner refs and coverage basis per batch;
- per-batch state READY_FOR_ROUTING_AUTHORITY_COURT, TRUE_UNRESOLVED_NO_OWNER, CONFLICTED_OWNER, OUTSIDE_ROUTING_JURISDICTION if already positively proved, or other explicit typed state;
- parallel dispatch graph and anti-expansion boundary.

Do not infer routing from question numbering, labels, missingness, adjacency, data patterns, statistics, or family resemblance. Grouping is not authority. Do not coerce unresolved to applicable/inapplicable/outside jurisdiction.

No replacement branch. No rebase. No MAIN or semantic PRE-MAIN mutation.

Commit the governed return and report PASS or the smallest exact blocker and final branch tip.
