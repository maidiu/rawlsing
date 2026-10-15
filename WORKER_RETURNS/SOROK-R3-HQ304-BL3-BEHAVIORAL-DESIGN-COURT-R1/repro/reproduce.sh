#!/usr/bin/env bash
set -eu
RET="$(cd "$(dirname "$0")/.." && pwd)"
if [ ! -f "$RET/runtime_root/runtime_marker.json" ]; then
  python3 "$RET/repro/stage.py"
fi
python3 "$RET/repro/stage_archived_evidence.py"
cp "$RET/repro/sitecustomize.py" "$RET/runtime_root/sitecustomize.py"
python3 "$RET/repro/run.py" probe
python3 - "$RET" <<'PY'
import pathlib,subprocess,sys
ret=pathlib.Path(sys.argv[1])
for suite,wanted in [('r2',0),('rba',0),('lab1',0),('lab2',0),('rmb',1),('r3',0),('r2_archive_audit',0),('rba_recompute',0),('mock',0),('r3_audit',0)]:
    result=subprocess.run([sys.executable,str(ret/'repro/run.py'),suite])
    print('ACTUAL_SUITE_EXIT',suite,result.returncode,flush=True)
    assert result.returncode==wanted,(suite,result.returncode,wanted)
PY
cp "$RET/runtime_root/rba/exec/r2/receipts/rba_review_run1/raw_capture_audit.json" "$RET/outputs/original_R2_reaudited_raw_capture_audit.json"
cp "$RET/runtime_root/rba/outputs/paired_recompute.json" "$RET/outputs/original_RBA_paired_recompute.json"
python3 "$RET/repro/run.py" evidence
python3 "$RET/repro/run.py" probe
echo 'SOURCEFREE_R3_SENSITIVITY_REPLAY_COMPLETE; REAL_EXPERIMENT_AND_CUSTODY_HOLDS_REMAIN'
