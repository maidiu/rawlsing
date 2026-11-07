# Proposed receiving PR draft — do not publish before acceptance

**Status:** DRAFT ONLY. No PR was created, no protected ref changed, no merge performed. The distinct nonauthor focused recheck of exact `16275d03` remains PENDING and gates acceptance and PR publication.

## Title

`SOROK P3: selective receiving of sourcefree compressed developmental state and actual P2-root proof`

## Body

```text
Selective receiving candidate for the P3 sourcefree developmental-state line.

Base: integration/pre-main-reconciliation-r1 @ c852d7516e23fcb6cf2215e9be7c5fa268503516
Source candidate: agent/sorok-p3-compressed-developmental-state-20261106-r1 @ 16275d03fc4724a694c48ed9d447c4eeadbe25f2
Implementation cut: 486d42a4aa5dcd449564b95567ae93b59c4679a4

This is a selective checkout of 157 files, not a bulk merge of the source branch. It adds the P3 runtime, tests, two frozen contracts, exact required E1 B1 source dependency, and the retained final/negative component evidence. It excludes PROGRAMMA/CURRENT_PROGRESS changes, commission/coordination files, dispositions/intake logs, superseded pre-repair matrix logs, and the E1/S1 candidate-review returns that are cited by exact commit but are not runtime dependencies.

What lands:
- p3/P3Owner composing unchanged accepted #704 P2Owner; normalized PsycheStore sidecar; sourcefree TEST_ONLY rules; compression evidence sidecar; activation/opacity projections; vertical-slice runner and tests.
- p3/state_store.py exact frozen SOURCEFREE_TEST_ONLY provenance and lossless V3MS kind/hash behavior.
- Exact E1 vendored B1 source dependency at WORKER_RETURNS/SOROK-P3-E1-DEVELOPMENTAL-ABI-RECONNAISSANCE-R1/probe/vendor/B1/bfirst.py, SHA-256 478b989730f49a5def41a367b6f53e4aae9c80961f7f466fe669c7dbd92201a3, plus source pin.

Published evidence at the candidate cut (author/HQ proof, not a new independent acceptance in this PR):
- 13/13 combined PRIMARY/A-H/resource matrix PASS at implementation 486d42a4a; no failed cases.
- 71/71 inherited engine regressions and cold-process compatibility preserved.
- Store/owner M1/M2 repair evidence: 61 passed, 1 skipped; units 37 passed; M3 resource metric repaired and matrix-green.
- Final independent review 1686c0b01e6b0b80738eaca89f31bab163fab36a was REVISE_CONDITIONAL_FULL_P3 with M1-M3; its negative findings and reproductions are retained.
- Combined resource receipt: 2 batches of 3 events, 1.5 calls/batch, two retrospectives, DB 4,096 B + WAL 1,537,792 B = 1,540,888 B; per-record 741,600 B, per-event 247,200 B.

Acceptance remains PENDING:
- The separate nonauthor focused recheck is live against exact 16275d03fc4724a694c48ed9d447c4eeadbe25f2 and has not been ingested as accepted here.
- Do not publish, receive or merge this PR until that review accepts the exact cut.

Preserved limits:
- Sourcefree TEST_ONLY engineering only.
- No native CAN/ADP science, original human validity, independently owned B behavior, ADP016/017 memory or claim issuance, production positive rule, protected CAS or merge authority.
- All original negative findings and inherited functionality remain preserved. No source/test/evidence file is deleted or rewritten by the selective checkout.

Selective exclusions are enumerated in WORKER_RETURNS/SOROK-P3-COMPRESSED-DEVELOPMENTAL-STATE-R1/evidence/selective-receiving-prep/SELECTIVE_INVENTORY.json. Excluded paths remain byte-identical on the candidate cut.
```

## Proposed branch construction

See `COMMANDS.md` and `SELECTIVE_PATHS.txt`. The proposed branch name is only a label:

```text
codex/sorok-p3-selective-receiving-20261107-r1
```

No branch was created by this preparation.
