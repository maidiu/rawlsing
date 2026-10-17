"""Run separate physical courts with literal exits, never synthesize test results."""
import json
from pathlib import Path
import subprocess
import sys
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parent
rows = []
for suite in ['legacy', 'author', 'independent', 'delta', 'candidate_own', 'postinspection']:
    cmd = [sys.executable, '-B', str(ROOT/'guarded_runner.py'), suite]
    result = subprocess.run(cmd, cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    (ROOT/'logs'/f'{suite}.log').write_bytes(result.stdout)
    rows.append(dict(suite=suite, command=cmd, cwd=str(ROOT), exit=result.returncode))
    print(suite, 'exit', result.returncode, flush=True)
(ROOT/'evidence/process_exits.json').write_text(json.dumps(dict(at_utc=datetime.now(timezone.utc).isoformat(),
    runs=rows, runtime='bundled Python 3.12; pandas/numpy from bundled runtime; locally pinned pytest8.4.2',
    differs_from_phase_a_runtime=True),indent=2)+'\n')
sys.exit(int(any(r['exit'] for r in rows)))
