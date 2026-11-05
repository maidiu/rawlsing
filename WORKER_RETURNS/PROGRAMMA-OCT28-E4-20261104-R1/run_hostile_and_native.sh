#!/usr/bin/env bash
set -eu
root=$1
packet=$(cd "$(dirname "$0")" && pwd)
export PYTHONPATH=. PYTHONHASHSEED=0 PYTHONDONTWRITEBYTECODE=1
export LC_ALL=C
for cut in base e1 e3; do
    (
        cd "$root/$cut"
        git rev-parse HEAD
        python3 - <<'PY'
from hashlib import sha256
import inspect
from pathlib import Path
from rawlsing_next import pre553_carrier_execution as carrier, pre553_empirical_query as query
assert carrier.CarrierNeutralResearchExecutor.execute_i03.__globals__["execute_empirical_query"] is query.execute_empirical_query
for module in (carrier, query):
    path = Path(inspect.getfile(module)).resolve()
    assert path.is_relative_to(Path.cwd())
    print(module.__name__, path, sha256(path.read_bytes()).hexdigest())
PY
    ) >>"$root/evidence/imports.log" 2>&1
done
(cd "$root/e3"; python3 "$packet/probe_cache.py" "$root/inputs/e1") >"$root/evidence/e4-cache.json" 2>"$root/evidence/e4-cache.stderr"
for cut in base e1 e3; do
    mkdir -p "$root/evidence/native-$cut"
    (cd "$root/$cut"; python3 "$packet/capture_native.py" "$root/inputs/e1/same-source.sav" "$root/evidence/native-$cut") >"$root/evidence/native-$cut.log" 2>&1
done
python3 "$packet/compare.py" "$root/evidence" >"$root/evidence/MEASUREMENTS.json"
