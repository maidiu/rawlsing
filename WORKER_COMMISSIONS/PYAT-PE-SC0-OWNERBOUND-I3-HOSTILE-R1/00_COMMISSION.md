# RRIF HQ DISPATCH CORRECTION — SELF-PROVISIONED, EXCLUSIVE GIT WORKTREE (REQUIRED)

**This is the operative 2026-10-31 self-provisioning amendment.** Earlier seal remains evidence, but an older prompt without this section is superseded for dispatch. This is PHASE-ONE RRIF only. The AI receiving this commission (not the user) MUST perform and verify all worktree provisioning itself with the local shell before inspecting/altering working files or running tests. Merely requesting a separate worktree is NOT compliance.

**Not an existing author's worktree. Not PRE-MAIN. Not another worker's branch.** Do not run in the checkout from which the agent was invoked, even if that checkout is clean. Never move/reset/delete/prune/rebase/force-push anybody else's worktree or branch. If the named path or local branch is already occupied, inspect registration and lease/process; if truly your own verified pre-existing session, continue that session safely without reset; otherwise STOP with `WORKTREE_COLLISION_OR_ACTIVE_LEASE` and report the exact blockage rather than selecting another worker's path. Never silently start a duplicate worker.

**Immutable dispatch gate:** the user-facing issue #564 supplies this commission's CURRENT 40-hex revised dispatch SHA. Verify it before Git work. Do not use any older pre-amendment SHA from prior messages or earlier issue versions. The worker MUST copy the verified SHA into `RRIF_DISPATCH_SHA` below; no guess/HEAD/latest substitution and no automatic branch-rebase. The branch being inspected has a unique per-issue name, but the input repository may have multiple worktrees and owners.

Execute in the **existing authenticated local `maidiu/rawlsing` Git clone** (a legitimate clone location must be verified, not invented):

```bash
set -euo pipefail
# Start inside any authenticated local clone/worktree of maidiu/rawlsing.
test "$(git remote get-url origin | sed 's/\\.git$//')" != "" || exit 1
git rev-parse --is-inside-work-tree | grep -qx true
TARGET_BRANCH='review/pyat-pe-sc0-ownerbound-successor-hostile-20261031-r1'
RRIF_DISPATCH_SHA="${RRIF_DISPATCH_SHA:?Set to exact 40-hex revision from GitHub issue #564}"
[[ "$RRIF_DISPATCH_SHA" =~ ^[0-9a-f]{40}$ ]] || { echo DISPATCH_SHA_INVALID; exit 2; }
WORKTREE_DIR="$HOME/Desktop/Rawlsing_Worktrees/rrif-564-exclusive-20261031"
LOCAL_SESSION_BRANCH='rrif-session-564-20261031'
# Only read origin; do not check out or modify any existing worker's branch.
git fetch --no-tags origin "refs/heads/$TARGET_BRANCH"
ACTUAL_REMOTE_SHA="$(git rev-parse --verify FETCH_HEAD)"
[[ "$ACTUAL_REMOTE_SHA" == "$RRIF_DISPATCH_SHA" ]] || { echo DISPATCH_HEAD_MOVED_STOP; exit 3; }
git worktree list --porcelain
if [[ -e "$WORKTREE_DIR" ]] || git show-ref --verify --quiet "refs/heads/$LOCAL_SESSION_BRANCH"; then
  echo WORKTREE_COLLISION_OR_EXISTING_SESSION_STOP
  exit 4
fi
mkdir -p "$(dirname "$WORKTREE_DIR")"
git worktree add -b "$LOCAL_SESSION_BRANCH" "$WORKTREE_DIR" "$RRIF_DISPATCH_SHA"
cd "$WORKTREE_DIR"
[[ "$(git rev-parse --verify HEAD)" == "$RRIF_DISPATCH_SHA" ]] || exit 5
[[ -z "$(git status --porcelain)" ]] || { echo WORKTREE_NOT_CLEAN; exit 6; }
printf 'ISSUE=564 BRANCH=%s SESSION_BRANCH=%s WORKTREE=%s START_SHA=%s\\n' "$TARGET_BRANCH" "$LOCAL_SESSION_BRANCH" "$PWD" "$(git rev-parse HEAD)"
```

The user must have explicitly selected the local editor/model/effort and the agent must verify its actual harness identity; this shell check DOES NOT grant source/science/actor authority. If the authenticated local clone or shell is not accessible, report `S2_NOT_AVAILABLE`, do **not** claim a created worktree or successful execution. If a previously active worker exists at this assignment, do not rerun it automatically. After satisfying this gate, execute ALL remaining original mission instructions below **within the new worktree**. Read-only external historical Git objects may be inspected without checking out their live branches.

**Return and publishing gate:** commit only the expressly assigned files, confirm the original issue branch is STILL the pinned initial SHA (compare `git ls-remote origin refs/heads/$TARGET_BRANCH` to `RRIF_DISPATCH_SHA` before push), and perform only a normal fast-forward push: `git push origin HEAD:refs/heads/$TARGET_BRANCH` (NO --force, NO --force-with-lease). If remote moved, STOP and reconcile; do not overwrite new work. Verify resulting remote 40-hex SHA and actual return files by cold readback. Do not use another worker's review/producer objects or mutate PRE-MAIN. This commission is NOT permission to merge into PRE-MAIN or to grade one's own scientific or engineering result as independently accepted.

---

# PYAT PE/SC0 I3+ — independent hostile review of 33-test owner-bound successor and actual consumer boundary

**SEALED USER-DISPATCHABLE COMMISSION — NOT AUTOMATICALLY LAUNCHED.**

AGENT TYPE: Fresh independent I3+ secure scientific-contract and current-consumer hostile reviewer
INTELLIGENCE LEVEL: I3+ / MAX

```text
LAUNCH — PYAT PE-OWNER-IR — INDEPENDENT HOSTILE SCIENTIFIC-CODE AND CONSUMER COURT
REPOSITORY: maidiu/rawlsing (PRIVATE)
AGENT_TYPE: Fresh independent I3+ secure scientific-contract/issuer/source/consumer hostile reviewer. NOT original PE, fixture-overlay, successor author, earlier PE/V2K hostile reviewer, PRE-MAIN integrator, science issuer or own adopting reviewer.
INTELLIGENCE_LEVEL: I3+
SINGLE_AGENT_FULL_DELIVERABLE: YES
USER_SELECTED_EDITOR_MODEL_PAIR: Proposed local OpenCode / DeepSeek V4.1-Flash MAX. User selects exact editor/model/host; verify actual independent session.
EXECUTION: S2 qualified isolated Git/Python sourcefree real executions and fault restorations; documentary S0/S1 only if not qualified, accurately held.
MODEL: DeepSeek V4.1-Flash proposed; REASONING: MAX requested, actual provider/account/quota/cost/availability UNKNOWN until verified.
WHY_NOT_BROWSER: original 21/13 and hostile 12 current real Python execution required.
WHY_NOT_FLASH: proposed whole I3+ MAX task; insufficiency not established.
WHY_NOT_CODEX_HIGH: necessity not positively demonstrated; user approves escalation only if actual selected model fails.
WHY_NOT_MIDDLE: no automatic downgrade.
ACTIVE_WORKER_NO_DISTURBANCE: YES; do not modify production or authors' worktrees.
EXACT_BRANCH: review/pyat-pe-sc0-ownerbound-successor-hostile-20261031-r1
STARTUP_SHA: a48c6acb7e0d3e0610dd0bc0e7b4ba2c09250253
REVIEW_SUBJECT: agent/pyat-pe-sc0-owner-bound-secure-successor-20261031-r1@a48c6acb7e0d3e0610dd0bc0e7b4ba2c09250253
CURRENT_PREMAIN_BASELINE: 8e44ca9c751049d65e6def47600b5c073ee04b29; recheck.
WRITE_SCOPE: only WORKER_RETURNS/PYAT-PE-SC0-OWNERBOUND-I3-HOSTILE-R1/**. Read subject code/test evidence; do NOT modify candidate, historical PE/fixture, rawlsing_next, canonical PRE-MAIN or actual original source.
NO_SOURCE_NATIVE_RESPONDENT, NO_ORIGINAL_SC0/N9/MODEL_ISSUANCE, NO_N11_N12, NO_SOROK_ACTOR, NO_PRODUCTION_GRANT_OR_SELF_ACCEPTANCE.

PRIMARY SOURCE: WORKER_RETURNS/PYAT-PE-SC0-OWNER-BOUND-SUCCESSOR/** on exact subject. Original PE @e61a26ce24f023a53d6b116bb9eca2fb7b6f8e65 (original 21 PASS, strict 4 PASS / 9 FAIL); overlay @9c030bf4c239d2e14f2b5a8a02ff7b44906cd0c7 (fixture 21/13/9 GREEN only); hostile PE review @33b5363a20d44cfb42b3d1e86fdb9615710adb23 (12 attacks prove overlay vulnerability). New candidate author: 33 green (19 positive + 14 hostile) at sourcefree and current PRE-MAIN, explicit current N10E/C1 adapter and IN-CANDIDATE first consumer; no actual production reader.
MISSION:
A. Verify exact source tree/objects, import hygiene, session independence, TEST_ONLY markings, result/receipt schemas and no accidental sitecustomize auto-patch or arbitrary fixture authority.
B. Rerun independent current 33 tests with sourcefree qualified host; independently challenge source changes, selected-world digest/value binding, actual refresh invocation versus fabricated receipt, denominator/cell geometry, four-clock revocation, duplicate publication, result_hash field omissions, negative scope, issuer identity, unrestricted reversal, cross-user/cross-source replay, transport tamper, missing producer and first-consumer bypass. Run new claim-specific faults that FAIL in named consumer assertion and restore baseline GREEN; merely raising unrelated exception does not prove edge.
C. Trace exact actual current pre553_empirical_possibility_provider and compose_positioned_subject_possibility call through n10e_adapter to first_consumer. Establish whether purported real current owner is truly called and whether the consumer is still candidate-only. Do not promote candidate success to current N9 N10W or E04L/P41 service.
D. Compare original 4/13 RED and overlay 13/13 with fresh actual tests; keep negative historical witnesses. Check candidate secure method alternatives including legitimate absence/no-change versus withheld source permission.
E. Determine minimal safe integration target: if only standalone sourcefree, identify named current receiver and exact missing owner-bound inputs as a GAP CARD. #536 P41/R08 branch still at startup remotely at prior check; if locally returned now, ingest exact SHA only after verification, no duplicate.
F. Give independent three court verdicts ENGINEERING / SCIENCE / AUTHORITY: ACCEPT_SOURCEFREE_SCOPED / REVISE_PRECISE_DEFECTS / HOLD, with exact positive/negative and no auto-merge. No new issuer, N9/world law or original survey access.

DELIVER 00_RETURN.md four-column FINDING/INTERPRETATION/ACTION/OWNER and DONE/REMAINING/BLOCKERS/LARGEST_MOVE/FLIGHT/DELTA; 01_ACTUAL_GIT_AND_TESTS.json; 02_TWELVE_PLUS_HOSTILE_MUTATIONS.md; 03_REAL_N10E_FIRST_CONSUMER_AND_CURRENT_OWNER_MAP.md; 04_SCOPED_VERDICT_AND_NEXT_WELD.md; 05_NOT_RUN_PERMISSION_ROLLBACK.json. Push exact review SHA. Incumbent authorized HQ independently adjudicates adoption; no self-acceptance and no new agent automatically dispatched.
```
