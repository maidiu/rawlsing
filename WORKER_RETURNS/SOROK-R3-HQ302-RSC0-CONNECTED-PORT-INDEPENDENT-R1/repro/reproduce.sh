#!/usr/bin/env bash
set -eu
RET="$(cd "$(dirname "$0")/.." && pwd)"
if [ ! -d "$RET/runtime_root" ]; then
  python3 "$RET/repro/stage.py"
fi
cp "$RET/repro/sitecustomize.py" "$RET/runtime_root/sitecustomize.py"
python3 "$RET/repro/run.py" probe
python3 - "$RET" <<'PY'
import pathlib,subprocess,sys
ret=pathlib.Path(sys.argv[1])
for suite,expected_exit in [('smoke',0),('baseline_rc0',1),('rc0',0),('k9_k10',0),('original_k9_k10',1),('connection',0),('n10e_c1',0),('pe',0),('hostile',1),('reverse_probe',0)]:
    p=subprocess.run([sys.executable,str(ret/'repro/run.py'),suite])
    print('ACTUAL_SUITE_EXIT',suite,p.returncode,flush=True)
    assert p.returncode==expected_exit,(suite,p.returncode,expected_exit)
PY
python3 "$RET/repro/build_results.py"
python3 "$RET/repro/run.py" probe
echo 'COURT_REPLAY_FINISHED_WITH_REVIEW_REVISE; KNOWN_RED_EXIT_STATUSES_RETAINED'
