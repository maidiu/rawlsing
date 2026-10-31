# RRIF HQ DISPATCH CORRECTION — SELF-PROVISIONED, EXCLUSIVE GIT WORKTREE (REQUIRED)

**This is the operative 2026-10-31 self-provisioning amendment.** Earlier seal remains evidence, but an older prompt without this section is superseded for dispatch. This is PHASE-ONE RRIF only. The AI receiving this commission (not the user) MUST perform and verify all worktree provisioning itself with the local shell before inspecting/altering working files or running tests. Merely requesting a separate worktree is NOT compliance.

**Not an existing author's worktree. Not PRE-MAIN. Not another worker's branch.** Do not run in the checkout from which the agent was invoked, even if that checkout is clean. Never move/reset/delete/prune/rebase/force-push anybody else's worktree or branch. If the named path or local branch is already occupied, inspect registration and lease/process; if truly your own verified pre-existing session, continue that session safely without reset; otherwise STOP with `WORKTREE_COLLISION_OR_ACTIVE_LEASE` and report the exact blockage rather than selecting another worker's path. Never silently start a duplicate worker.

**Immutable dispatch gate:** the user-facing issue #574 supplies this commission's CURRENT 40-hex revised dispatch SHA. Verify it before Git work. Do not use any older pre-amendment SHA from prior messages or earlier issue versions. The worker MUST copy the verified SHA into `RRIF_DISPATCH_SHA` below; no guess/HEAD/latest substitution and no automatic branch-rebase. The branch being inspected has a unique per-issue name, but the input repository may have multiple worktrees and owners.

Execute in the **existing authenticated local `maidiu/rawlsing` Git clone** (a legitimate clone location must be verified, not invented):

```bash
set -euo pipefail
# Start inside any authenticated local clone/worktree of maidiu/rawlsing.
test "$(git remote get-url origin | sed 's/\\.git$//')" != "" || exit 1
git rev-parse --is-inside-work-tree | grep -qx true
TARGET_BRANCH='review/pre-main-rrif-f0r3-control-gate-independent-20261031-r1'
RRIF_DISPATCH_SHA="${RRIF_DISPATCH_SHA:?Set to exact 40-hex revision from GitHub issue #574}"
[[ "$RRIF_DISPATCH_SHA" =~ ^[0-9a-f]{40}$ ]] || { echo DISPATCH_SHA_INVALID; exit 2; }
WORKTREE_DIR="$HOME/Desktop/Rawlsing_Worktrees/rrif-574-exclusive-20261031"
LOCAL_SESSION_BRANCH='rrif-session-574-20261031'
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
printf 'ISSUE=574 BRANCH=%s SESSION_BRANCH=%s WORKTREE=%s START_SHA=%s\\n' "$TARGET_BRANCH" "$LOCAL_SESSION_BRANCH" "$PWD" "$(git rev-parse HEAD)"
```

The user must have explicitly selected the local editor/model/effort and the agent must verify its actual harness identity; this shell check DOES NOT grant source/science/actor authority. If the authenticated local clone or shell is not accessible, report `S2_NOT_AVAILABLE`, do **not** claim a created worktree or successful execution. If a previously active worker exists at this assignment, do not rerun it automatically. After satisfying this gate, execute ALL remaining original mission instructions below **within the new worktree**. Read-only external historical Git objects may be inspected without checking out their live branches.

**Return and publishing gate:** commit only the expressly assigned files, confirm the original issue branch is STILL the pinned initial SHA (compare `git ls-remote origin refs/heads/$TARGET_BRANCH` to `RRIF_DISPATCH_SHA` before push), and perform only a normal fast-forward push: `git push origin HEAD:refs/heads/$TARGET_BRANCH` (NO --force, NO --force-with-lease). If remote moved, STOP and reconcile; do not overwrite new work. Verify resulting remote 40-hex SHA and actual return files by cold readback. Do not use another worker's review/producer objects or mutate PRE-MAIN. This commission is NOT permission to merge into PRE-MAIN or to grade one's own scientific or engineering result as independently accepted.

---

LAUNCH — RRIF F0R3 — FRESH INDEPENDENT PRE-MAIN FANIN CONTROL READINESS REVIEW

REPOSITORY: maidiu/rawlsing PRIVATE. PHASE: RRIF only, not PROGRAMMA or new scientific/person product construction.
ROLE: Fresh independent I3 sourcefree PRE-MAIN fan-in security/currentness reviewer. NOT prior F0/F0R2 reviewer, F0R3 code author, PR519 controller, original source/science issuer, repo administrator, PRE-MAIN integrator or own reviewer.
INTELLIGENCE: I3/MAX; proposed local OpenCode / DeepSeek V4.1-Flash MAX subject to user actual editor/model/variant/host selection and independent session verification, no autonomous pair switch.
EXECUTION: qualified local S2 full Git, sourcefree Python adversarial tests; if unavailable S0/S1 with truthful NOT_RUN. Do not execute native original source, survey/respondents, Sorok actors or untrusted scripts from arbitrary branches.
BRANCH: review/pre-main-rrif-f0r3-control-gate-independent-20261031-r1
STARTUP_SHA: 8e44ca9c751049d65e6def47600b5c073ee04b29
WORK ONLY: WORKER_RETURNS/RRIF-PREMAIN-F0R3-CONTROL-INDEPENDENT-R1/**. Check live branch/worktree/session collision and current PR519/SHA. No edits to PR519, canonical PRE-MAIN, required-check/branch protection settings, Sorok/Pyat CURRENT_PROGRESS, F4 or source owner.
SOURCE CUTS: PR519 current verified HEAD 59c9a7a4a4fae60d809c1ef545ff4e48906d0dd0, re-resolve at runtime. Prior F0 verdict e5089b7da29d3c290ad1447f7b7a45cc81f0eb6e; F0R2 hostile 53c4e16f5e402f452efb036878a58cd4258cd14a; F0R3 candidate repair return 3057b2f5b87f04ff1737d88356edfe3568e1745f, proposed patched validator source Git blob 2fc1c3c7ae6113d12b70abb655ff123a6ae9c895. Original PR519 validator blob 6fa0ce132e68f1fea7d67321129a2af2627a5d94. Initial-seed blob 4ffe5f95b84505431a928f7ef6d0e7b5931f63d8 owner status PENDING. Current PRE-MAIN 8e44ca9c751049d65e6def47600b5c073ee04b29. PRE-MAIN API presently protected=false, required_status_checks off, repo rulesets []; revalidate during work. Separate F4 early branch 9fb7caebc266f1e3a8315d87ff446d5db1634cc5 divergent and HELD.
MISSION:
1. Fetch exact PR519 live HEAD and F0R3 candidate, replay current live event+flight corpus and actual sourcefree Python 20 adversarial mutation witnesses + legal nonadopted candidate. Independently verify old 13 and new N1-N7: false source_authority, science ACCEPT by nonissuer, reviewer-of-commission, fake merged PR, edited appended event/flight after immutable seed, forged CAS/current owner, replay and fake first consumer. A legitimate nonadopting event must remain accepted at scoped offline integrity. Do not transfer old head test pass to new bytes.
2. Recompute patch applicability on live PR519 and exact SHA; distinguish sourcefree engineering PASS from proof of reviewer identity/source grant or admin/CAS. Any regression is REVIEW RED with precise repair. Reviewer cannot implement patch; direct current PR519 owner separately.
3. Fetch actual live branch protection and rulesets for integration/pre-main-reconciliation-r1 and identify required check name from exact CI status. Prove real required-PR/check/independent-approval/no bypass if it exists; otherwise state ENFORCEMENT_NOT_INSTALLED. Repository ADMIN alone may install/readback verified settings; sourcefree validator alone cannot create authority.
4. Examine incumbent owner approval of initial seed and real privileged verifier for signed source/science ownership, merged commit, paired CURRENT_PROGRESS MD+JSON and importing consumer. If absent state hard gate. Explicitly separate FIABC 144/3 failures and Sorok MD/JSON revision divergence from this sourcefree control code; no unrelated wave or person source grant.
5. Determine exactly what must be done for existing PR519 + F0R3 to become admissible fan-in gate under authorized maintainer and administrator, and whether F4 must be reconciled or abandoned in favor of the current reviewed head. No second competing control law/system or shadow HQ.
6. Strictly RRIF historical recovery/fan-in gate, not future PROGRAMMA #566. No merge, CAS, new model, new original science/wave/actor grants.
RETURN: WORKER_RETURNS/RRIF-PREMAIN-F0R3-CONTROL-INDEPENDENT-R1/{00_RETURN.md,PR519_HEAD_AND_CANDIDATE_PATCH.md,INDEPENDENT_NEGATIVE_WITNESSES.md,ADMIN_PROTECTION_AND_OWNER_CAS_GATES.md,EXACT_REMAINING_OWNER_ACTIONS.md,COMMANDS_AND_READBACK.md}. Separate engineering/science/authority conclusions. FINDING/INTERPRETATION/ACTION/OWNER, DONE/REMAINING/BLOCKERS/LARGEST_MOVE/FLIGHT/DELTA, exact return SHA and tests, no self-adoption or user-selected model change.