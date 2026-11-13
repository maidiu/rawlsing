#!/bin/bash
# Exact execution command record for SOROK #1008 C03/C04 final execution.
# Worktree: /Users/matthewsmith/s2b-work/pyat1008-c03c04-exec
# Each suite run redirects to EXECUTION_1008/logs/<name>.log and appends EXIT=<code>.
set -o pipefail

# --- custody ---------------------------------------------------------------
git fetch origin 4e1cd301b994e4df58e89052642fde5c16fa3542
git worktree add /Users/matthewsmith/s2b-work/pyat1008-c03c04-exec 4e1cd301b994e4df58e89052642fde5c16fa3542
git switch -c sorok-c03-c04-exec-1008
git rev-parse HEAD
git merge-base --is-ancestor 6a5c12f04323d74001f9632063ec907f4fc4468e 4e1cd301b994e4df58e89052642fde5c16fa3542

# --- mandated suites at starting SHA --------------------------------------
/usr/bin/time -l python3 -m pytest -q WORKER_RETURNS/SOROK-C03-C04-A-FINAL-R1/test_c04_first_consumer_identity.py > EXECUTION_1008/logs/01_test_c04_first_consumer_identity.log 2>&1; echo "EXIT=$?" >> EXECUTION_1008/logs/01_test_c04_first_consumer_identity.log
/usr/bin/time -l python3 -m pytest -q WORKER_RETURNS/SOROK-C03-C04-GOFIRST-A-R1/test_c04_custody.py > EXECUTION_1008/logs/02_test_c04_custody.log 2>&1; echo "EXIT=$?" >> EXECUTION_1008/logs/02_test_c04_custody.log
/usr/bin/time -l python3 -m pytest -q WORKER_RETURNS/SOROK-C03-C04-GOFIRST-A-R1/test_c03_prospectives.py > EXECUTION_1008/logs/03_test_c03_prospectives.log 2>&1; echo "EXIT=$?" >> EXECUTION_1008/logs/03_test_c03_prospectives.log
/usr/bin/time -l python3 -m pytest -q WORKER_RETURNS/SOROK-E01-J1-995-R1/test_j1_three_head_join.py > EXECUTION_1008/logs/04_test_j1_three_head_join.log 2>&1; echo "EXIT=$?" >> EXECUTION_1008/logs/04_test_j1_three_head_join.log
/usr/bin/time -l python3 -m pytest -q WORKER_RETURNS/SOROK-DUEL-C02-C03-R2/A_RETURN_R3/test_c03_c04_consumer.py > EXECUTION_1008/logs/05_test_c03_c04_consumer.log 2>&1; echo "EXIT=$?" >> EXECUTION_1008/logs/05_test_c03_c04_consumer.log

# --- C01/C02 regression (one file per source-owned entry point) -----------
for f in \
  WORKER_RETURNS/SOROK-DUEL-C01-R1/test_c01_supporting_actor.py \
  WORKER_RETURNS/SOROK-DUEL-C01-R1/B_RETURN_R1/test_c01_b_supporting_actor.py \
  WORKER_RETURNS/SOROK-DUEL-C01-R1/C02/test_c02_parent_activity.py; do
  n=$(basename "$f" .py)
  /usr/bin/time -l python3 -m pytest -q "$f" > "EXECUTION_1008/logs/10_$n.log" 2>&1
  echo "EXIT=$? FILE=$f" >> "EXECUTION_1008/logs/10_$n.log"
done
for f in \
  WORKER_RETURNS/SOROK-DUEL-C02-R1/test_c02_b_parent_activity.py \
  WORKER_RETURNS/SOROK-DUEL-C02-R1/A_RETURN_R2/test_c02_live_root_b02.py \
  WORKER_RETURNS/SOROK-DUEL-C02-C03-R2/test_c02_c03_b_period_decision.py; do
  n=$(basename "$f" .py)
  /usr/bin/time -l python3 -m pytest -q "$f" > "EXECUTION_1008/logs/11_$n.log" 2>&1
  echo "EXIT=$? FILE=$f" >> "EXECUTION_1008/logs/11_$n.log"
done

# --- B04/B05 regression ----------------------------------------------------
for f in WORKER_RETURNS/SOROK-DUEL-B04-R1/test_b04_composition.py \
         WORKER_RETURNS/SOROK-DUEL-B04-R1/test_b04_operations.py; do
  n=$(basename "$f" .py)
  /usr/bin/time -l python3 -m pytest -q "$f" > "EXECUTION_1008/logs/12_$n.log" 2>&1
  echo "EXIT=$? FILE=$f" >> "EXECUTION_1008/logs/12_$n.log"
done
for f in WORKER_RETURNS/SOROK-DUEL-B05-R1/test_b05_*.py; do
  n=$(basename "$f" .py)
  /usr/bin/time -l python3 -m pytest -q "$f" > "EXECUTION_1008/logs/13_$n.log" 2>&1
  echo "EXIT=$? FILE=$f" >> "EXECUTION_1008/logs/13_$n.log"
done

# --- P6 and D03 regression -------------------------------------------------
for f in WORKER_RETURNS/SOROK-P6-ONE-LIVING-HOUSE-R1/test_*.py; do
  n=$(basename "$f" .py)
  /usr/bin/time -l python3 -m pytest -q "$f" > "EXECUTION_1008/logs/14_$n.log" 2>&1
  echo "EXIT=$? FILE=$f" >> "EXECUTION_1008/logs/14_$n.log"
done
/usr/bin/time -l python3 -m pytest -q WORKER_RETURNS/SOROK-DUEL-D03-R1/tests/test_d03_immediate_uptake.py > EXECUTION_1008/logs/15_test_d03_immediate_uptake.log 2>&1; echo "EXIT=$?" >> EXECUTION_1008/logs/15_test_d03_immediate_uptake.log

# --- hostile probe and new controls ---------------------------------------
/usr/bin/time -l python3 EXECUTION_1008/probe_hostile.py > EXECUTION_1008/logs/20_probe_hostile.log 2>&1; echo "EXIT=$?" >> EXECUTION_1008/logs/20_probe_hostile.log
python3 -m pytest -q WORKER_RETURNS/SOROK-C03-C04-A-FINAL-R1/test_c04_hostile_execution_r1.py > EXECUTION_1008/logs/21_hostile_execution_RED.log 2>&1; echo "EXIT=$?" >> EXECUTION_1008/logs/21_hostile_execution_RED.log
python3 -m pytest -q WORKER_RETURNS/SOROK-C03-C04-A-FINAL-R1/test_c04_hostile_execution_r1.py > EXECUTION_1008/logs/22_hostile_execution_GREEN.log 2>&1; echo "EXIT=$?" >> EXECUTION_1008/logs/22_hostile_execution_GREEN.log
/usr/bin/time -l python3 -m pytest -q WORKER_RETURNS/SOROK-C03-C04-A-FINAL-R1/test_c04_hostile_execution_r1.py > EXECUTION_1008/logs/23_hostile_execution_GREEN2.log 2>&1; echo "EXIT=$?" >> EXECUTION_1008/logs/23_hostile_execution_GREEN2.log
python3 EXECUTION_1008/probe_hostile.py > EXECUTION_1008/logs/24_probe_hostile_after_fix.log 2>&1; echo "EXIT=$?" >> EXECUTION_1008/logs/24_probe_hostile_after_fix.log

# --- post-repair reruns of every suite importing parent_speech ------------
for f in WORKER_RETURNS/SOROK-C03-C04-A-FINAL-R1/test_c04_first_consumer_identity.py \
         WORKER_RETURNS/SOROK-C03-C04-GOFIRST-A-R1/test_c04_custody.py; do
  n=$(basename "$f" .py)
  /usr/bin/time -l python3 -m pytest -q "$f" > "EXECUTION_1008/logs/30_rerun_$n.log" 2>&1
  echo "EXIT=$? FILE=$f" >> "EXECUTION_1008/logs/30_rerun_$n.log"
done
for f in WORKER_RETURNS/SOROK-E01-J1-995-R1/test_j1_three_head_join.py \
         WORKER_RETURNS/SOROK-DUEL-D03-R1/tests/test_d03_immediate_uptake.py; do
  n=$(basename "$f" .py)
  /usr/bin/time -l python3 -m pytest -q "$f" > "EXECUTION_1008/logs/31_rerun_$n.log" 2>&1
  echo "EXIT=$? FILE=$f" >> "EXECUTION_1008/logs/31_rerun_$n.log"
done
for f in WORKER_RETURNS/SOROK-DUEL-C02-C03-R2/A_RETURN_R3/test_c03_c04_consumer.py \
         WORKER_RETURNS/SOROK-DUEL-C02-C03-R2/test_c02_c03_b_period_decision.py \
         WORKER_RETURNS/SOROK-DUEL-D02-R1/tests/test_d02_b_two_event_uptake.py \
         WORKER_RETURNS/SOROK-C03-C04-GOFIRST-A-R1/test_c03_prospectives.py; do
  n=$(basename "$f" .py)
  /usr/bin/time -l python3 -m pytest -q "$f" > "EXECUTION_1008/logs/32_rerun_$n.log" 2>&1
  echo "EXIT=$? FILE=$f" >> "EXECUTION_1008/logs/32_rerun_$n.log"
done

# --- static compile --------------------------------------------------------
python3 -m py_compile WORKER_RETURNS/SOROK-DEVELOPMENTAL-RECURSION-ENGINE-R1/developmental_recursion/parent_speech.py WORKER_RETURNS/SOROK-C03-C04-A-FINAL-R1/test_c04_hostile_execution_r1.py
