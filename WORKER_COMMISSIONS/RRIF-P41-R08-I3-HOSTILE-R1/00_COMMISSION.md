# RRIF HQ DISPATCH CORRECTION — SELF-PROVISIONED, EXCLUSIVE GIT WORKTREE (REQUIRED)

**This is the operative 2026-10-31 self-provisioning amendment.** Earlier seal remains evidence, but an older prompt without this section is superseded for dispatch. This is PHASE-ONE RRIF only. The AI receiving this commission (not the user) MUST perform and verify all worktree provisioning itself with the local shell before inspecting/altering working files or running tests. Merely requesting a separate worktree is NOT compliance.

**Not an existing author's worktree. Not PRE-MAIN. Not another worker's branch.** Do not run in the checkout from which the agent was invoked, even if that checkout is clean. Never move/reset/delete/prune/rebase/force-push anybody else's worktree or branch. If the named path or local branch is already occupied, inspect registration and lease/process; if truly your own verified pre-existing session, continue that session safely without reset; otherwise STOP with `WORKTREE_COLLISION_OR_ACTIVE_LEASE` and report the exact blockage rather than selecting another worker's path. Never silently start a duplicate worker.

**Immutable dispatch gate:** the user-facing issue #570 supplies this commission's CURRENT 40-hex revised dispatch SHA. Verify it before Git work. Do not use any older pre-amendment SHA from prior messages or earlier issue versions. The worker MUST copy the verified SHA into `RRIF_DISPATCH_SHA` below; no guess/HEAD/latest substitution and no automatic branch-rebase. The branch being inspected has a unique per-issue name, but the input repository may have multiple worktrees and owners.

Execute in the **existing authenticated local `maidiu/rawlsing` Git clone** (a legitimate clone location must be verified, not invented):

```bash
set -euo pipefail
# Start inside any authenticated local clone/worktree of maidiu/rawlsing.
test "$(git remote get-url origin | sed 's/\\.git$//')" != "" || exit 1
git rev-parse --is-inside-work-tree | grep -qx true
TARGET_BRANCH='review/pyat-rrif-p41-r08-sourcefree-world-hostile-20261031-r1'
RRIF_DISPATCH_SHA="${RRIF_DISPATCH_SHA:?Set to exact 40-hex revision from GitHub issue #570}"
[[ "$RRIF_DISPATCH_SHA" =~ ^[0-9a-f]{40}$ ]] || { echo DISPATCH_SHA_INVALID; exit 2; }
WORKTREE_DIR="$HOME/Desktop/Rawlsing_Worktrees/rrif-570-exclusive-20261031"
LOCAL_SESSION_BRANCH='rrif-session-570-20261031'
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
printf 'ISSUE=570 BRANCH=%s SESSION_BRANCH=%s WORKTREE=%s START_SHA=%s\\n' "$TARGET_BRANCH" "$LOCAL_SESSION_BRANCH" "$PWD" "$(git rev-parse HEAD)"
```

The user must have explicitly selected the local editor/model/effort and the agent must verify its actual harness identity; this shell check DOES NOT grant source/science/actor authority. If the authenticated local clone or shell is not accessible, report `S2_NOT_AVAILABLE`, do **not** claim a created worktree or successful execution. If a previously active worker exists at this assignment, do not rerun it automatically. After satisfying this gate, execute ALL remaining original mission instructions below **within the new worktree**. Read-only external historical Git objects may be inspected without checking out their live branches.

**Return and publishing gate:** commit only the expressly assigned files, confirm the original issue branch is STILL the pinned initial SHA (compare `git ls-remote origin refs/heads/$TARGET_BRANCH` to `RRIF_DISPATCH_SHA` before push), and perform only a normal fast-forward push: `git push origin HEAD:refs/heads/$TARGET_BRANCH` (NO --force, NO --force-with-lease). If remote moved, STOP and reconcile; do not overwrite new work. Verify resulting remote 40-hex SHA and actual return files by cold readback. Do not use another worker's review/producer objects or mutate PRE-MAIN. This commission is NOT permission to merge into PRE-MAIN or to grade one's own scientific or engineering result as independently accepted.

---

# LAUNCH — RRIF P41/R08 I3+ — HOSTILE SOURCEFREE WORLD/CONSUMER AND R08 BINDER COURT

REPOSITORY: maidiu/rawlsing (PRIVATE).
AGENT_TYPE: Fresh independent I3+ scientific/engineering and issuer-boundary hostile reviewer, NOT P41/R08 author, selected-world repair author, E03 author, original owner/issuer, HQ integrator, Sorok actor owner or own reviewer.
INTELLIGENCE_LEVEL: I3+ / MAX requested; SINGLE_AGENT_FULL_DELIVERABLE: YES.
PROPOSED_EDITOR_MODEL: local OpenCode / DeepSeek V4.1-Flash MAX, user-selected verified editor/model/effort and separate actual session. Do not autonomously switch model. WHY_NOT_BROWSER: exact local historical Git/current sourcefree executor and fault mutation needed. S2 qualified local worktree or accurately scoped S0/S1 fallback. No original raw respondent/source or native execution.
BRANCH: review/pyat-rrif-p41-r08-sourcefree-world-hostile-20261031-r1
STARTUP_SHA: 8e44ca9c751049d65e6def47600b5c073ee04b29. Recheck PRE-MAIN, existing worktrees/leases, separate author session, no force push. Do not merge to PRE-MAIN, no production code edits.
EXACT AUTHOR_RETURN_BRANCH: agent/pyat-recover-p41-r08-world-evidence-consumer-20261030-r1
EXACT AUTHOR_RETURN_SHA: aa6ca0d700f10bc349a98d98c4239c554ca221f8
AUTHOR_FILES: WORKER_RETURNS/PYAT-P41-R08-RECOVERY/{00_RETURN.md,sourcefree_adapter/{selected_world_repair.py,p41_current_service.py},tests/test_selected_world_repair.py,tests/test_p41_current_service.py,repro/{run_sourcefree_adapters.sh,run_r08_current_binder.sh},SELECTED_WORLD_DEFECT_READBACK.md,EVIDENCE_BINDER_INGRESS_MAP.md,FUNCTION_AND_CONSUMER_MAP.md,TEST_RECEIPTS_AND_FAULT_NEGATIVES.md,REVIEWER_REQUEST.md}.
CURRENT_RECEIVER: integration/pre-main-reconciliation-r1@8e44ca9c751049d65e6def47600b5c073ee04b29. Existing E03 blob 84d404147547767be8ecd4b6e1541f5fa3a8c8a2, C1/N10E/F8 sourcefree owners; historic P41 service 7d428106c79bcc56973f7c0044fc273a2b354554; historic R61-R08 evidence-binding blob 3ca860e409f1d063da4cd03dd1691a89c67333f6. S3 original selected-world source cut ed34944e253b78714a28d72b8ca2a6521ce15930, seam court 26 pass / 1 fail KeyError exact_probabilities. PE ownerbound successor@a48c6acb7e0d3e0610dd0bc0e7b4ba2c09250253 author-only 33 pass awaiting separate independent court #564; do not use as adopted receiver.
MISSION:
1. Independently prove source/execution provenance and rerun P41 19, P41 W1/W2/W3 mutation, E03 18, selected-world 24 and original seam 26/1, current C1/N10E/F8 69, learned-world 30, bounded repair 5, P41 adapter 5, staged R08 binder 113 and targeted R8 8. Record exact tests/exits and whether R08 external library was supplied from correct exact historical blob. Reproduction is NOT sole ground for accepting safety or meaning.
2. Hostile court of selected-world rebinding. Check original failure is contract/value mismatch, not concealed numeric error or test coding artifact. Use changed cells (3,1,1,3)→(3,1,2,2), exact 3/4→1/2 only with fresh contract, old contract refused. Attack stale clock, swapped source identity, altered denominator, fake hash, zero-vs-missing, reconstructed forbidden world, cold restore and mutation bypass. Does the candidate permit caller to mint source-owned contract authority by hashing supplied cells? If yes distinguish TEST_ONLY demonstration from legitimate producer-bound source ownership; no false source-owner acceptance.
3. P41 current-style adapter over actual E03→N10E/C1/F8. Verify the direct function calls through current modules are real, that the "F8 consumed" field cannot be self-minted, and rule/as-of/publication/revocation are not purely decorative caller-controlled metadata. Attack wrong conditioner, forged rule clock, stale cache, cold payload, wrong issuer, missing upstream producer, replay and incompatible world.
4. R08 staged 118KB binder: inspect all privilege/issuer/HMAC/test fixture boundaries. Does test-only ephemeral HMAC server create hidden authority? Are current C1 fixtures and real provider actually in the same executed route? Rerun negative binder/foreign source/altered/held-row admission and prove a missing binder fails closed. Never treat 113+8 isolated tests as a production receiver.
5. Separate meaningful technical capability from original N9/SC0/P41/R08 scientific claims and actual production receiver. Locate any legitimate current import/caller; if absent, issue exact receiver-gap specification, not magic acceptance or wholesale binder transplant.
6. Crosscheck related PE #564 court / F7 temporal no crosswave claims; no competing ownership. Distinguish original selected-world RED receipt from sourcefree candidate repair success.
GRADE per element: scoped sourcefree ACCEPT, engineering RED, HOLD current receiver, science HOLD, authority HOLD, with exact falsifier and next implementable minimal bridge. Require independent positives/fault negatives, not descriptive reassurance.
NO grants: raw U/E/source, CAN/ADP/SCI, model world N9/N10W/N11/N12, Sorok actor. No PRE-MAIN modification; no self-review. Broken historical assertion retained exact, no test patch to delete failure.
OUTPUT on isolated branch: PYAT_CONTROL_ROOM/BRANCH_RECOVERY_R1/INVESTIGATIONS/RRIF_P41_R08_I3/00_RETURN.md, SELECTED_WORLD_MUTATION_AND_SOURCE_OWNERSHIP.md, CURRENT_E03_P41_CALLGRAPH_AND_FAULTS.md, R08_BINDER_ISSUER_ATTACKS.md, REAL_CONSUMER_GAP_SPEC.md, SOURCEFREE_TEST_RECEIPTS_AND_NEGATIVES.md. FINDING/INTERPRETATION/ACTION/OWNER and DONE/REMAINING/BLOCKERS/LARGEST_MOVE/FLIGHT/DELTA; exact SHA and separate HQ adoption, no worker self-merging.
