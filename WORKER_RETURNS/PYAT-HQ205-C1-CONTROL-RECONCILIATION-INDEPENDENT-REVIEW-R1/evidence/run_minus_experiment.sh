#!/usr/bin/env bash
# HQ205 decisive over-import experiment.
#
# A scratch sparse worktree at the candidate commit, with every never-opened
# authority-material file REMOVED. If the accepted court still passes 454/454,
# those files are not dependencies of the accepted qualification.
#
# The candidate worktree itself is never modified.
set -u
REPO=/Users/matthewsmith/Desktop/Rawlsing
SCRATCH=/Users/matthewsmith/Desktop/Rawlsing_Worktrees/hq205-c1-minus
STAGE=/Users/matthewsmith/Desktop/Rawlsing_Worktrees/hq205-pyat-stage
VENV=/Users/matthewsmith/Desktop/Rawlsing/LOCAL_COURTS/qualification/r7-c4-source-free-venv/bin/python
CAND=88f262b94bbe94cd3e2a8113c8b17d0872c5089c

cd "$REPO"
git worktree remove --force "$SCRATCH" 2>/dev/null
rm -rf "$SCRATCH"
git worktree add --no-checkout --detach "$SCRATCH" "$CAND" >/dev/null 2>&1
cd "$SCRATCH"
git sparse-checkout init --no-cone >/dev/null 2>&1
git sparse-checkout set \
  '/rawlsing_next/' \
  '/WORKER_RETURNS/PYAT-AT07-SUCCESSOR-SPINE-INDEPENDENT-FREEZE-R1/' \
  '/WORKER_RETURNS/PYAT-C1-00-CONTRACT-CORRECTION-R2/' \
  '/WORKER_RETURNS/PYAT-C1-00-CONTRACT-CORRECTION-R3/' \
  '/WORKER_RETURNS/PYAT-C1-00-CONTRACT-CORRECTION-R8/' >/dev/null 2>&1
git checkout --detach "$CAND" >/dev/null 2>&1
echo "scratch HEAD: $(git rev-parse HEAD)"

removed=0
while read -r p; do
  [ -z "$p" ] && continue
  if [ -f "$SCRATCH/$p" ]; then
    case "$p" in
      "$SCRATCH"/*) echo "REFUSING absolute path $p" >&2; exit 1 ;;
    esac
    rm -f "$SCRATCH/$p" && removed=$((removed+1))
  fi
done < "$STAGE/logs/never_opened_authority.txt"
echo "removed $removed never-opened authority files"

echo "--- remaining authority files in scratch ---"
find "$SCRATCH/WORKER_RETURNS" -type f 2>/dev/null | wc -l

COURT="test_pre553_analytical_state_and_route test_pre553_authority_maintenance test_pre553_replay_audit test_pre553_analytical_replay_dependency test_pre553_empirical_possibility_provider test_pre553_analytical_composition_higher_order test_pre553_empirical_query test_pre553_c1_03_join test_pre553_structural_admission test_pre553_discovery_exact test_pre553_analytical_composition test_source_backed_positioned_subject_possibility test_pre553_discovery_adaptive test_pre553_discovery_adaptive_admission test_pre553_recursive_handoff"
FILES=""
for t in $COURT; do FILES="$FILES rawlsing_next/tests/$t.py"; done

( cd "$SCRATCH" && PYTHONHASHSEED=0 PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 PYTHONPATH="$SCRATCH" \
  "$VENV" -m pytest -p no:cacheprovider -q --tb=short -rfE $FILES ) \
  > "$STAGE/logs/court_minus.txt" 2>&1
echo "MINUS_COURT_EXIT=$?" >> "$STAGE/logs/court_minus.txt"
tail -4 "$STAGE/logs/court_minus.txt"
