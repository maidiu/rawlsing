# Rawlsing Source/Wave Identity Repair — Rabochii Guide

## Terrain discipline

The defining discipline of this campaign is **containment**.

A phase prompt gives each rabochii:

1. primary issue IDs;
2. hook issue IDs, if any;
3. exact writable files;
4. behavior-level limits inside mixed-purpose files;
5. explicit forbidden terrain.

All five are binding. Passing tests do not excuse terrain breach.

### What to do when a neighboring defect appears

Do not patch it. Return a `CROSS_TERRAIN_FINDING` record containing:

- observed file/function;
- minimal reproduction/evidence;
- why it is outside your current terrain;
- likely owner if obvious;
- whether your assigned work can continue safely.

Vozhd decides whether to promote/reassign it.

## Phase startup

Before editing:

- verify branch name and base integration commit;
- read the full register load order;
- enumerate your allowed files and confirm the working diff is empty;
- inspect current code rather than assuming the audit's line-level state remains unchanged;
- classify each intended edit as `ADD_UID`, `ADAPT_AT_INGRESS`, `CHANGE_JOIN_KEY`, `CHANGE_GROUP_KEY`, `VERSION_ID`, `PRESERVE_LEGACY_COMPAT`, `VALIDATION_ONLY`, or `TEST_ONLY`.

## Semantic non-interference

Identity repairs are not permission to redesign measurement semantics.

Particularly:

- W03-B may not change V551 directionality, projection, neutral handling, support, promotability or adjudication policy.
- W04 may not loosen V550J/V551J registry/certification semantics.
- W06 may not change V552 pressure/measurement semantics or fabricate V552J evidence.
- W05 may not alter stage semantics at all.
- W02-B may not convert review-only overlay output into certified authority.

If an identity change appears to require a semantic change, stop and report it.

## Cross-hook law

One architectural defect may require stage-local changes from multiple owners. The issue still has exactly one primary owner.

Primary owner result may be:

- `RESOLVED`
- `PARTIAL_AWAITING_CROSS_HOOK`
- `BLOCKED_BY_AUTHORITY`
- `NO_LONGER_REPRODUCES_WITH_EVIDENCE`

Hook owner reports `HOOK_COMPLETE` or `HOOK_BLOCKED` keyed to the same SWID. Only Vozhd marks the issue terminal in the central resolution ledger.

## Required worker return

Return one machine-readable JSON object followed by a concise terminal summary.

Required fields:

```json
{
  "worker_id": "W03",
  "phase_id": "W03-A",
  "base_commit": "...",
  "branch": "agent/swid-w03-v550-a",
  "primary_issue_ids": [],
  "hook_issue_ids": [],
  "issue_results": [{"issue_id":"SWID-...","status":"RESOLVED","evidence":"..."}],
  "hook_results": [],
  "files_allowed": [],
  "files_changed": [],
  "files_changed_before_after_sha256": [],
  "edit_classifications": [],
  "contract_changes": [],
  "legacy_identity_compatibility": [],
  "tests": [{"command":"...","result":"PASS","detail":"..."}],
  "cross_terrain_findings": [],
  "cross_worker_dependencies": [],
  "commit_sha": "...",
  "draft_pr": "...",
  "no_unowned_files_changed": true
}
```

## PR discipline

- branch from the exact post-gate integration commit;
- one phase per branch/PR;
- draft PR targets `agent/source-wave-identity-repair-integration`;
- never merge your own PR;
- do not start the next phase on the same branch;
- no `git add -A` equivalent over unrelated files;
- tests must include neighboring regression tests for any mixed-purpose file touched;
- explain every intentional legacy/new ID difference in the PR body.
