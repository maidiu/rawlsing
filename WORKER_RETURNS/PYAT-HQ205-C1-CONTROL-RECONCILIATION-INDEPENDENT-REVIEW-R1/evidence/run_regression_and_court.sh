#!/usr/bin/env bash
# HQ205: regression before/after + 454-court open audit.
set -u
VENV=/Users/matthewsmith/Desktop/Rawlsing/LOCAL_COURTS/qualification/r7-c4-source-free-venv/bin/python
CTRL=/Users/matthewsmith/Desktop/Rawlsing_Worktrees/hq205-c1-review
CAND=/Users/matthewsmith/Desktop/Rawlsing_Worktrees/hq205-c1-candidate
STAGE=/Users/matthewsmith/Desktop/Rawlsing_Worktrees/hq205-pyat-stage
mkdir -p "$STAGE/logs"

run_suite () {
  local tree="$1" out="$2"
  ( cd "$tree" && \
    PYTHONHASHSEED=0 PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 PYTHONPATH="$tree" \
    "$VENV" -m pytest -p no:cacheprovider -q --tb=no -rfE \
      --continue-on-collection-errors rawlsing_next/tests ) > "$out" 2>&1
  echo "exit=$?" >> "$out"
}

echo "### BEFORE (control, rawlsing_next == candidate base) ###"
date
run_suite "$CTRL" "$STAGE/logs/suite_before.txt"
echo "### AFTER (candidate) ###"
date
run_suite "$CAND" "$STAGE/logs/suite_after.txt"
echo "### 454 COURT with open audit ###"
date
COURT="test_pre553_analytical_state_and_route test_pre553_authority_maintenance test_pre553_replay_audit test_pre553_analytical_replay_dependency test_pre553_empirical_possibility_provider test_pre553_analytical_composition_higher_order test_pre553_empirical_query test_pre553_c1_03_join test_pre553_structural_admission test_pre553_discovery_exact test_pre553_analytical_composition test_source_backed_positioned_subject_possibility test_pre553_discovery_adaptive test_pre553_discovery_adaptive_admission test_pre553_recursive_handoff"
FILES=""
for t in $COURT; do FILES="$FILES rawlsing_next/tests/$t.py"; done
: > "$STAGE/logs/court_opened.txt"
( cd "$CAND" && \
  HQ205_AUDIT_LOG="$STAGE/logs/court_opened.txt" \
  PYTHONHASHSEED=0 PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
  PYTHONPATH="$CAND:$STAGE/audit" \
  "$VENV" -m pytest -p no:cacheprovider -q --tb=short -rfE $FILES ) \
  > "$STAGE/logs/court_run.txt" 2>&1
echo "court_exit=$?" >> "$STAGE/logs/court_run.txt"
date
echo "### DONE ###"
