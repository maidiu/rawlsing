#!/usr/bin/env bash
# RA-C sourcefree-only reproduction handoff. UNEXECUTED by RA-C.
set -euo pipefail
REPO="${RAWLSING_REPO:?Set RAWLSING_REPO to an authenticated existing local Rawlsing checkout}"
SHA="c821b488b3a9a3f0fa01b1981989cc17af637dc1"
RET="WORKER_RETURNS/SOROK-20261026-RA-C-EXECUTABLE-CAUSAL-PROBE-R1"
S52="WORKER_RETURNS/SOROK-20261025-S52-PAID-ACTIVITY-REPERTOIRE-R1"
G18="/Users/matthewsmith/Desktop/Rawlsing/rawlsing-r31j/WORKER_RETURNS/SOROK-20261021-R31J-GM01-PREC9-SOURCE-PERSON-R1/candidate/vendor/bp2/vendor/g18"
[[ -d "$REPO/.git" || -f "$REPO/.git" ]] || { echo "BLOCK:NO_AUTHENTICATED_GIT_CHECKOUT"; exit 40; }
git -C "$REPO" cat-file -e "${SHA}^{commit}" || { echo "BLOCK:SOURCE_COMMIT_MISSING"; exit 41; }
[[ -f "$G18/lab_sgi1/history.py" ]] || { echo "BLOCK:G18_EXTERNAL_SOURCE_MISSING"; exit 42; }
mkdir -p "$REPO/$RET/TEST_SOURCE_AND_LOGS"
BASE="$REPO/$RET/TEST_SOURCE_AND_LOGS"
SCRATCH="$BASE/isolated_archive"
[[ ! -e "$SCRATCH" ]] || { echo "BLOCK:SCRATCH_ALREADY_EXISTS (protect other runs)"; exit 43; }
mkdir -p "$SCRATCH" "$BASE/tmp"
# Archive ONLY Sorok S39–S52 code/return subtrees at exactly one commit.
PATHS=()
while IFS= read -r name; do
  case "$name" in
    SOROK-20261024-S3*|SOROK-20261024-S4*|SOROK-20261025-S4*|SOROK-20261025-S5*)
      PATHS+=("WORKER_RETURNS/$name");;
  esac
done < <(git -C "$REPO" ls-tree --name-only "${SHA}:WORKER_RETURNS")
[[ ${#PATHS[@]} -gt 0 ]] || { echo "BLOCK:NO_SOROK_SOURCE_SUBTREES"; exit 44; }
git -C "$REPO" archive --format=tar "$SHA" "${PATHS[@]}" | tar -xf - -C "$SCRATCH"
export TMPDIR="$BASE/tmp" PYTHONDONTWRITEBYTECODE=1
command -v python3; python3 --version; python3 -m pytest --version
(
 cd "$SCRATCH"
 echo "SOURCE_CUT=$SHA"
 shasum -a 256 "$S52/run_s52.py" "$S52/s52/session.py" "$S52/s52/bootstrap.py"
 python3 -B -m pytest -q "$S52/tests/test_s52.py" -p no:cacheprovider
 python3 -B "$S52/run_s52.py"
 # Prepare same-source hostile probe; NO accepted source edits.
 PYTHONPATH="$SCRATCH/$S52" python3 -B "$REPO/$RET/TEST_SOURCE_AND_LOGS/test_s52_postcondition_fault.py"
) > "$BASE/local_mac_run.stdout.log" 2> "$BASE/local_mac_run.stderr.log"
echo "ALL_INVOCATIONS_COMPLETED_INSPECT_LOGS" # Does NOT mean K1/K2/K4/K8 pass
