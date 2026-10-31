# RRIF HQ DISPATCH CORRECTION — SELF-PROVISIONED, EXCLUSIVE GIT WORKTREE (REQUIRED)

**This is the operative 2026-10-31 self-provisioning amendment.** Earlier seal remains evidence, but an older prompt without this section is superseded for dispatch. This is PHASE-ONE RRIF only. The AI receiving this commission (not the user) MUST perform and verify all worktree provisioning itself with the local shell before inspecting/altering working files or running tests. Merely requesting a separate worktree is NOT compliance.

**Not an existing author's worktree. Not PRE-MAIN. Not another worker's branch.** Do not run in the checkout from which the agent was invoked, even if that checkout is clean. Never move/reset/delete/prune/rebase/force-push anybody else's worktree or branch. If the named path or local branch is already occupied, inspect registration and lease/process; if truly your own verified pre-existing session, continue that session safely without reset; otherwise STOP with `WORKTREE_COLLISION_OR_ACTIVE_LEASE` and report the exact blockage rather than selecting another worker's path. Never silently start a duplicate worker.

**Immutable dispatch gate:** the user-facing issue #565 supplies this commission's CURRENT 40-hex revised dispatch SHA. Verify it before Git work. Do not use any older pre-amendment SHA from prior messages or earlier issue versions. The worker MUST copy the verified SHA into `RRIF_DISPATCH_SHA` below; no guess/HEAD/latest substitution and no automatic branch-rebase. The branch being inspected has a unique per-issue name, but the input repository may have multiple worktrees and owners.

Execute in the **existing authenticated local `maidiu/rawlsing` Git clone** (a legitimate clone location must be verified, not invented):

```bash
set -euo pipefail
# Start inside any authenticated local clone/worktree of maidiu/rawlsing.
test "$(git remote get-url origin | sed 's/\\.git$//')" != "" || exit 1
git rev-parse --is-inside-work-tree | grep -qx true
TARGET_BRANCH='agent/pyat-s7fix-current-owner-map-correction-20261031-r1'
RRIF_DISPATCH_SHA="${RRIF_DISPATCH_SHA:?Set to exact 40-hex revision from GitHub issue #565}"
[[ "$RRIF_DISPATCH_SHA" =~ ^[0-9a-f]{40}$ ]] || { echo DISPATCH_SHA_INVALID; exit 2; }
WORKTREE_DIR="$HOME/Desktop/Rawlsing_Worktrees/rrif-565-exclusive-20261031"
LOCAL_SESSION_BRANCH='rrif-session-565-20261031'
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
printf 'ISSUE=565 BRANCH=%s SESSION_BRANCH=%s WORKTREE=%s START_SHA=%s\\n' "$TARGET_BRANCH" "$LOCAL_SESSION_BRANCH" "$PWD" "$(git rev-parse HEAD)"
```

The user must have explicitly selected the local editor/model/effort and the agent must verify its actual harness identity; this shell check DOES NOT grant source/science/actor authority. If the authenticated local clone or shell is not accessible, report `S2_NOT_AVAILABLE`, do **not** claim a created worktree or successful execution. If a previously active worker exists at this assignment, do not rerun it automatically. After satisfying this gate, execute ALL remaining original mission instructions below **within the new worktree**. Read-only external historical Git objects may be inspected without checking out their live branches.

**Return and publishing gate:** commit only the expressly assigned files, confirm the original issue branch is STILL the pinned initial SHA (compare `git ls-remote origin refs/heads/$TARGET_BRANCH` to `RRIF_DISPATCH_SHA` before push), and perform only a normal fast-forward push: `git push origin HEAD:refs/heads/$TARGET_BRANCH` (NO --force, NO --force-with-lease). If remote moved, STOP and reconcile; do not overwrite new work. Verify resulting remote 40-hex SHA and actual return files by cold readback. Do not use another worker's review/producer objects or mutate PRE-MAIN. This commission is NOT permission to merge into PRE-MAIN or to grade one's own scientific or engineering result as independently accepted.

---

# PYAT R-S7MAP — correct S7FIX present-owner/source-consumer claims without remapping historical science

**SEALED USER-DISPATCHABLE COMMISSION — NOT AUTOMATICALLY LAUNCHED.**

AGENT TYPE: Independent bounded I2 sourcefree function-lineage and receiver-map repair engineer
INTELLIGENCE LEVEL: I2 / MAX

```text
LAUNCH — PYAT R-S7MAP — FIX CURRENT OWNER/CONSUMER CLAIMS AFTER INDEPENDENT S7FIX HOSTILE RED
REPOSITORY: maidiu/rawlsing (PRIVATE)
AGENT_TYPE: Independent bounded I2 sourcefree function-lineage/receiver-map repair engineer. NOT S6/S7/S7FIX original author, S7FIX hostile reviewer, PRE-MAIN integrator or own reviewer.
INTELLIGENCE_LEVEL: I2
SINGLE_AGENT_FULL_DELIVERABLE: YES
USER_SELECTED_EDITOR_MODEL_PAIR: Proposed local OpenCode / DeepSeek V4.1-Flash at verified MAX. User selects; no switch.
EXECUTION: S2 qualified isolated local full Git + bounded Python sourcefree validator/tests. S0/S1 fallback must report NOT_RUN rather than pass.
MODEL: DeepSeek V4.1-Flash proposed, not auto-selected.
REASONING: MAX requested; actual harness, process, host, quota, selected account and availability UNKNOWN until verified.
WHY_NOT_BROWSER: 47MB Git source artifact and focused current Python tests require S2.
WHY_NOT_FLASH: Flash MAX is proposed for the whole bounded I2 task; cannot assume inadequate.
WHY_NOT_CODEX_HIGH: Not established necessary for specific static/owner rekey; escalate only on demonstrated need and user approval.
WHY_NOT_MIDDLE: No autonomous downgrade; user selection necessary.
ACTIVE_WORKER_NO_DISTURBANCE: YES. Do not reset or edit older worker worktrees.
EXACT_BRANCH: agent/pyat-s7fix-current-owner-map-correction-20261031-r1
STARTUP_SHA: 80bc5d9bf6624c2ea04027322947a41c347330aa
COMMISSION_PATH: WORKER_COMMISSIONS/PYAT-R-S7FIX-CURRENT-OWNER-MAP-R1/00_COMMISSION.md
REVIEW_SUBJECT: review/pyat-s7fix-boundary-source-abi-hostile-20261031-r1@1b89fd49c330e4a2c976e6af8d6c1a5e6dbfb088
CURRENT_PREMAIN_BASELINE: 8e44ca9c751049d65e6def47600b5c073ee04b29; recheck live head/receiver before tests.
WRITE_SCOPE: only S7_BOUNDARY_REPAIR sourcefree mapping/validator-focused tests and WORKER_RETURNS/PYAT-R-S7MAP-CORRECTION-R1/**. Never edit current rawlsing_next production, PRE-MAIN, canonical owner decisions, scientific semantics or hidden worker files.
NO_SOURCE_NATIVE_SURVEY, NO_ORIGINAL_U_E_ISSUER, NO_F7_P07_RULE, NO_N9_N11_N12, NO_SOROK_ACTOR_GRANT, NO_MERGE_OR_SELF_ACCEPTANCE.

FROZEN FACTS: Historical 5 splits + 1 join PASS; 845 branches; 3135 exact-once function IDs; corrected families 1885; 2595 negative records retained. Independent reviewer specifically found current-owner mapping RED: nested historical resolver methods mapped to outer present resolver, five S5 outer EXACT_AST_SAME_PATH labels false, absent pre553_temporal_comparability.py falsely named as current consumer, historical PhysicalSourceIncidence.iter_batches.emit AST differs from current decoder.

MISSION (finite bounded repair, not 845 reinventory):
1. Compare exact original six family maps, reviewer-return JSON and current PRE-MAIN blobs before edits.
2. Mark all historical nested _make_sealed_source_relation_owner.SourceRelationResolver members with null current implementation and NO_CURRENT_NESTED_OWNER__HISTORICAL_ONLY; keep historical defects with their nested families, no false reattribution.
3. Mark five outer S5 current path matches as CURRENT_PATH_SYMBOL_ONLY__AST_DIFFERENT__BEHAVIORAL_EQUIVALENCE_NOT_CLAIMED. Preserve historical AST/negative reviewer provenance.
4. Replace absent temporal-comparability consumer with HISTORICAL_FIRST_CONSUMER_ONLY__CURRENT_PATH_ABSENT and CURRENT_EXECUTED_CONSUMER=TEST_ONLY. Physical decoder current import/call sites remain current static owner candidates but no historical behavioral equivalence.
5. Mark historical emit join source exact at historical scope and current PR526 emit as DIFFERENT_AST__TEST_ONLY_GREEN; do not copy or merge historical 47 MB artifact into PRE-MAIN.
6. Update focused sourcefree verifier/tests so a forged current nested owner, absent consumer, false AST or lost negative cannot pass. Preserve all 3135 exact-once, 1885 family counts, 2595 original negatives; include adversarial fault for the named map claim.
7. Run actual commands and record SHA/test/exit; sourcefree current tests (24/26/31/16 pass +1 skip) only if qualified and relevant. Do not claim production consumer execution. Preserve historical F7/P07 and HQ240/HQ245–248 security REDs.
8. Produce explicit OWNER_DECISION: historical nested owner RETIRE/HOLD requires an actual competent current owner; do NOT invent new nested production class just to satisfy map. State missing current product consumer as function card.

ACCEPT_ENGINEERING: exact current owner truth + original IDs/negative custody preserved + validator and claim-specific fault-negative green + versioned source/consumer readback.
RED_ENGINEERING: current nested→outer conflation, fake equality, fake current importer, lost negative, forbidden code import or false behavioral equivalence.
HOLD_ENGINEERING: original AST/Git or current test runtime not available; give exact NOT_RUN.
SCIENTIFIC: preserve alternatives and original negative findings; no Rule/issuer promotion.
AUTHORITY: separate original permission/semantic and owner CAS; no self-review.
FIRST_CONSUMER: Programma Pyat R/O source-function reference shall ingest correction as RETURNED_UNADOPTED pending separate qualified review/owner.
DELIVER 00_RETURN.md (FINDING/INTERPRETATION/ACTION/OWNER; DONE/REMAINING/BLOCKERS/LARGEST_MOVE/FLIGHT/DELTA), corrected source maps, test+fault receipt, exact old/new family and owner links, independent-review request and rollback. Commit/push only exact isolated branch, report final 40hex SHA; do not launch next worker or declare canonical adoption.
```
