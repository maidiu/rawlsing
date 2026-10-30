# QF1 — PRE-MAIN code fan-in: NOT_MERGED

Observed FINDING: PR #519 advanced to `59c9a7a4…`, but the independent control review still covers only `342164a09…` and still holds current-head CI, protection, progress CAS and F4. Causal INTERPRETATION: a newer draft head is not an accepted current-head control or owner CAS; canonical fan-in is unavailable. Proposed HQ ACTION: complete F0R3/current-head review, admin protection, owner seed approval, FIABC attribution, paired progress CAS and F4 reconciliation before any QF1 merge. Accountable OWNER: PRE-MAIN maintainer/repo admin, F0R3 author/reviewer, FIABC/Pyat and Sorok owners.

## Exact state

| Surface | Evidence | Status |
|---|---|---|
| PRE-MAIN canonical | `integration/pre-main-reconciliation-r1` = `299f41e97a43c67be9cc76a79fa49b48f4e12e54` | unchanged; unprotected per F0R2 |
| PR #519 head | `59c9a7a4a4fae60d809c1ef545ff4e48906d0dd0` (draft, unmerged) | source-only; not canonical |
| F0R2 independent review | `53c4e16f…`, reviewed `342164a09…` | `HOLD_CURRENT_HEAD_RECEIPT_CI…AUTHORITY_RED` |
| Current-head CI | F0R2: exact-head Python cancel; previous head only 13 witnesses | no accepted current-head run |
| Protection | F0R2: `protected=false`, rulesets `[]`, protection detail 403 | no enforced required checks/approvals |
| FIABC | 144 PASS / 3 FAIL on predecessor governed run | not all-green; owner attribution absent |
| Sorok progress | MD rev36 / JSON rev35 | paired owner CAS absent |
| Pyat progress | JSON preview empty in F0R2 | owner retrieval/CAS absent |
| F4 | `integration/pre-main-fanin-owner-cas-activation-20261029-r1@9fb7caeb…` | held/divergent; not reconciled to current head |
| Initial seed | F0R2: owner approval PENDING | not owner-signed |

PR519's own new dispatch document says: draft until approved/protected merge; F4 STOP; PRE-MAIN unprotected; FIABC 144/3; Sorok MD/JSON split. That is not a canonical receiving control.

## What QF1 did not do

No merge, code PR, branch protection change, force push, PRE-MAIN mutation, PR #514/#516/#519 edit, original author/reviewer mutation or owner adoption. No code was selected or staged. No owner CAS was fabricated.

## Ordered owner packet

1. F0R3/current-head control repair with exact Python witnesses, preserving original 13.
2. Separate hostile review of the new exact PR head.
3. Repository admin configures and independently reads required checks/approvals/no-bypass.
4. Original PRE-MAIN owner authenticates the initial seed.
5. FIABC/Pyat owner attributes the three failures and restores progress source.
6. Sorok owner reconciles paired MD/JSON via one truth-qualified CAS.
7. Authorized maintainer reconciles F4 to the exact approved head, merges only after currentness and grants, then performs post-merge first-consumer readback.

No step is undertaken by QF1.

DONE: exact current PR/F0R2/protection/CI/F4 state and no-merge decision. REMAINING: steps 1–7. CRITICAL BLOCKERS: current-head control, protection, progress CAS, FIABC, F4. LARGEST PRODUCTIVE MOVE: F0R3/current-head witness repair and protected exact-head CI. FLIGHT: read-only; no PR or canonical write. DELTA: PR head moved but control acceptance did not; QF1 remains NOT_MERGED.
