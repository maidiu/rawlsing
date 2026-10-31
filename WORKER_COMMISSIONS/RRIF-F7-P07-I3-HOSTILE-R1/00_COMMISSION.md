# RRIF HQ DISPATCH CORRECTION — SELF-PROVISIONED, EXCLUSIVE GIT WORKTREE (REQUIRED)

**This is the operative 2026-10-31 self-provisioning amendment.** Earlier seal remains evidence, but an older prompt without this section is superseded for dispatch. This is PHASE-ONE RRIF only. The AI receiving this commission (not the user) MUST perform and verify all worktree provisioning itself with the local shell before inspecting/altering working files or running tests. Merely requesting a separate worktree is NOT compliance.

**Not an existing author's worktree. Not PRE-MAIN. Not another worker's branch.** Do not run in the checkout from which the agent was invoked, even if that checkout is clean. Never move/reset/delete/prune/rebase/force-push anybody else's worktree or branch. If the named path or local branch is already occupied, inspect registration and lease/process; if truly your own verified pre-existing session, continue that session safely without reset; otherwise STOP with `WORKTREE_COLLISION_OR_ACTIVE_LEASE` and report the exact blockage rather than selecting another worker's path. Never silently start a duplicate worker.

**Immutable dispatch gate:** the user-facing issue #571 supplies this commission's CURRENT 40-hex revised dispatch SHA. Verify it before Git work. Do not use any older pre-amendment SHA from prior messages or earlier issue versions. The worker MUST copy the verified SHA into `RRIF_DISPATCH_SHA` below; no guess/HEAD/latest substitution and no automatic branch-rebase. The branch being inspected has a unique per-issue name, but the input repository may have multiple worktrees and owners.

Execute in the **existing authenticated local `maidiu/rawlsing` Git clone** (a legitimate clone location must be verified, not invented):

```bash
set -euo pipefail
# Start inside any authenticated local clone/worktree of maidiu/rawlsing.
test "$(git remote get-url origin | sed 's/\\.git$//')" != "" || exit 1
git rev-parse --is-inside-work-tree | grep -qx true
TARGET_BRANCH='review/pyat-rrif-f7-p07-temporal-hostile-20261031-r1'
RRIF_DISPATCH_SHA="${RRIF_DISPATCH_SHA:?Set to exact 40-hex revision from GitHub issue #571}"
[[ "$RRIF_DISPATCH_SHA" =~ ^[0-9a-f]{40}$ ]] || { echo DISPATCH_SHA_INVALID; exit 2; }
WORKTREE_DIR="$HOME/Desktop/Rawlsing_Worktrees/rrif-571-exclusive-20261031"
LOCAL_SESSION_BRANCH='rrif-session-571-20261031'
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
printf 'ISSUE=571 BRANCH=%s SESSION_BRANCH=%s WORKTREE=%s START_SHA=%s\\n' "$TARGET_BRANCH" "$LOCAL_SESSION_BRANCH" "$PWD" "$(git rev-parse HEAD)"
```

The user must have explicitly selected the local editor/model/effort and the agent must verify its actual harness identity; this shell check DOES NOT grant source/science/actor authority. If the authenticated local clone or shell is not accessible, report `S2_NOT_AVAILABLE`, do **not** claim a created worktree or successful execution. If a previously active worker exists at this assignment, do not rerun it automatically. After satisfying this gate, execute ALL remaining original mission instructions below **within the new worktree**. Read-only external historical Git objects may be inspected without checking out their live branches.

**Return and publishing gate:** commit only the expressly assigned files, confirm the original issue branch is STILL the pinned initial SHA (compare `git ls-remote origin refs/heads/$TARGET_BRANCH` to `RRIF_DISPATCH_SHA` before push), and perform only a normal fast-forward push: `git push origin HEAD:refs/heads/$TARGET_BRANCH` (NO --force, NO --force-with-lease). If remote moved, STOP and reconcile; do not overwrite new work. Verify resulting remote 40-hex SHA and actual return files by cold readback. Do not use another worker's review/producer objects or mutate PRE-MAIN. This commission is NOT permission to merge into PRE-MAIN or to grade one's own scientific or engineering result as independently accepted.

---

# LAUNCH — RRIF F7/P07 I3+ — INDEPENDENT TEMPORAL METHOD, OWNER-SECURITY AND CONSUMER COURT

REPOSITORY: maidiu/rawlsing (PRIVATE).
AGENT_TYPE: Fresh independent I3+ scientific-temporal and sourcefree issuer/ABI hostile reviewer, NOT original F7/P07 issuer, return author, S7FIX author/reviewer, PRE-MAIN HQ, native C engineer, or own reviewer.
INTELLIGENCE_LEVEL: I3+ / MAX requested, full-task selected editor/model local OpenCode / DeepSeek V4.1-Flash MAX proposed; user must explicitly choose/verify supported MAX and distinct actual session; no model/editor switch. Browser documentary insufficient for original sourcefree 49/163 + fault-mutation execution, S2 local authorized sourcefree pytest; fallback only if accurately S0/S1.
BRANCH: review/pyat-rrif-f7-p07-temporal-hostile-20261031-r1
STARTUP_SHA: 8e44ca9c751049d65e6def47600b5c073ee04b29. Inspect currently active worktrees first, do not disturb/force push; separate clean worktree, no direct PRE-MAIN mutation.
AUTHOR_RETURN_BRANCH: agent/pyat-recover-f7-temporal-p07-hostile-successor-20261030-r1
AUTHOR_RETURN_SHA: f8fe03cc6e6a482f428bed9e03c08e50ce1e6479
ARTIFACTS: WORKER_RETURNS/PYAT-F7-P07-RECOVERY/{00_RETURN.md,ORIGINAL_METHODS_AND_ANTI_REBUILD.md,RED_VARIANTS_AND_TRUST_BOUNDARY.md,COMPATIBILITY_AND_CONSUMER_MAP.json,candidate/{temporal_method_candidate.py,test_temporal_method_candidate.py,mutation_check.py},test_receipts/**}.
EXACT SOURCE: historical F7 pure method blob 6f6b462b1cdef54d7989f15452473383c1661594; historic tests blob 8a82bd5905d266c1d500b1bf2bdcb01ea948efd6; current outer pre553_source_relations.py@5b67e3f98a5faf95a6c82700af2346fef6e306a5 TEST_ONLY; historical nested source owner absent from current. Independent S7FIX I3@1b89fd49c330e4a2c976e6af8d6c1a5e6dbfb088 finds current owner map RED (outer AST nonidentical, historical emit != PR526). Related separate correction commission #565; do not duplicate it. Current authority-registry 18 kinds, TEMPORAL_COMPARABILITY proposed but unissued; TEMPORAL_EVIDENCE exists. Historical native HQ240-HQ248 alias TCB, ledger-cell forgery, constructor OOB, PyObject_Call/PyErr_Fetch crash, Stage B leak, trusted callback and decide leaks: all adverse, no native import/compile/execute here.
MISSION:
1. Independently reproduce historical paired F7 HQ211 49/49, HQ235 163/163, intermediate HQ227 134/141 failure as recorded; current source-relations 24, decoder/custody 73+1 skipped, author test-only candidate 24/24 and two fail-capability mutations 2/2. Verify exact historical source pairs/receipts, no unsafe old native.
2. Hostile science audit: is original F7 truly only a two-anchor relation with caller-supplied hash-bound requirements, no sovereign EE12 construct/item/route/population/weight/time comparability? Verify exact numeric delta with Decimal/Fraction/int, no deadband/nearest/midpoint/interpolation, strong no direction when order unknown or partial; noncomparable != zero. Independently search existing current temporal, Field Forge, B5 lifecycle, source-relation, N9/N10W/as-of replacements, distinguish same semantic capability from name absence.
3. Inspect new ~972-line temporal_method_candidate.py for hidden self-issued comparability, caller-minted source identity, forged as-of eligibility, currentness mistaken for scientific validity, source cross-universe alias, hash/receipt laundering, authority fallback to labels/epochs/first/nearest, optional role bypass, infinite/unbounded resource pressure and tamper restoration loopholes. Attack candidate independently with defect-specific mutation and negative positive comparator. No acceptance from 24 green alone.
4. Verify that proposal TEMPORAL_COMPARABILITY has not been adopted, that current source-relations has no authenticated nested owner or production consumer, and that there is no original source-authorized EE12 pair or actual N9 historical/as-of consumer. Could ANY safe pure method be adopted as explicitly test-only bounded relation now without unsafe current nested P07? Keep authority and future consumer decoupled.
5. Evaluate whether a real sourcefree N9/as-of receiver can be built from current E03/P41 candidate, and distinguish physical as-of/time-window bookkeeping from authorization of scientific comparability. Produce concrete receiving-contract gap/owner spec and next method-issuer commission only where necessary; do not invent original permission.
6. Retain every actual adverse native/P07 failure, including the accepted historical source and S7FIX mapping RED. Do not resurrect native Stage A/B or transplant historical nested owner. No raw source, N9 operative world, Sorok actor, N11/N12 model rights or PRE-MAIN write.
ENGINEERING court: independent sourcefree evidence ACCEPT bounded or RED with code-specific oracle, receiver HOLD exact, candidate uptake conditional upon separate review. SCIENCE: distinguish relation calculation vs crosswave construct/sample comparability and original EE12 issuance. AUTHORITY: no self grants and no own review.
RETURN on named branch: PYAT_CONTROL_ROOM/BRANCH_RECOVERY_R1/INVESTIGATIONS/RRIF_F7_P07_I3/{00_RETURN.md,INDEPENDENT_ORACLE_AND_MUTATIONS.md,TEMPORAL_SCIENCE_ISSUER_GAP.md,CURRENT_RECEIVER_AND_P07_OWNER_COURT.md,ADVERSARIAL_NEGATIVES.md,INTEGRATION_OR_NONADOPTION_PLAN.md}. Include exact source files/bounds, commands/exits, separate six-axis engineering/science/authority verdict, FINDING/INTERPRETATION/ACTION/OWNER and DONE/REMAINING/BLOCKERS/LARGEST_MOVE/FLIGHT/DELTA. Push exact SHA and request separate appointed HQ adoption; reviewer cannot self-integrate.
