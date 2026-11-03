# PDEV01 exact commands

The replay script is `replay.sh`; it writes only to this returnroot and one temp directory.

## Actual J42 two-input build

```sh
cd /Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat-pdev01-n10w-join
BASE=$(mktemp -d /private/var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T/pdev01-n10w-j42.XXXXXX)
git archive f53cb0d2bce52640268c844c398bbd8007d28edc \
  WORKER_RETURNS/PYAT-R42-J42-COMPLETE-E41-W41-P41-ACTUAL-JOINT-PREV3-CONSUMER-R1 \
  -o "$BASE/j42.tar"
tar -xf "$BASE/j42.tar" -C "$BASE"
ln -s "$PWD/rawlsing_next" "$BASE/rawlsing_next"
printf 'gitdir: %s\n' "$(git rev-parse --absolute-git-dir)" > "$BASE/.git"
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" \
  python3 "$BASE/WORKER_RETURNS/PYAT-R42-J42-COMPLETE-E41-W41-P41-ACTUAL-JOINT-PREV3-CONSUMER-R1/runtime/j42_build.py" \
  --outdir "$BASE/out"
```

The referenced W41 artifact is accepted at
`b0a68e4ff5d5e2ca62b080376fda6b5f5431a6c2:WORKER_RETURNS/PYAT-R41-W41-OBJECTIVE-WORLD-R1/current_historical_asof_world_consumer_receipts.json`
with SHA-256
`09a92d6c00e867a44712b225cadd352b7d41a2038384de26de34f5c10a9185e7`.
It is read through the repository’s exact git objects; no new parent is created.

## Public receiver positives and negatives

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. python3 - <<'PY'
import json
from rawlsing_next.tests.test_universal_world_binding import _joined_request
from rawlsing_next.pre553_universal_world_binding import select_joined_world_view
r = json.load(open("WORKER_RETURNS/PDEV01-N10W-JOIN/J42_RECEIPTS.json"))
key = "base/TEST_CURRENT/budget5"
v = select_joined_world_view(_joined_request(r, key))
print(v.state, v.reason_code, v.view_hash)
PY
```

The version/currentness hostile command is the same receiver with the receipt copies mutated in
`VERSION_AND_IDENTITY_NEGATIVES.json`; it returned positive for each wrong provider version,
`REVOKED` N9 currentness, and a mutated N9 selection. The receiver also does not reject the stale
`p41.content_hash` left after those mutations.

## R05/P41 boundary trace

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. python3 - <<'PY'
from rawlsing_next.tests.test_universal_world_binding import (
    _build_r05_learned_inprocess, _build_r05_p41_receipts,
    _actual_execution_for, _r05_request)
from rawlsing_next.pre553_universal_world_binding import select_r05_world_view
runtime = "<extracted P41 runtime>"
data = _build_r05_learned_inprocess()
receipts = _build_r05_p41_receipts(runtime)
execution = _actual_execution_for(data, runtime)
view = select_r05_world_view(_r05_request(data, receipts, actual_execution=execution))
print(view.state, view.reason_code, view.view_hash)
PY
```

This returns `R05_WORLD_SELECTED_VIEW` for the R05 fixture, but the P41 N9 provider remains
`E04_TEST_ONLY_SELECTED_WORLD_M4_M5@1`; it is not W41 N9 or a `CURRENT` N9 world.

## Cold replay

The build was executed twice with the same J42 commit and the same accepted W41 artifact. Both
`n9_n10e_n10w_real_joined_consumer_receipts.json` files were byte equal
(`c54b215bb03bba391571b4c51357831b14f256b7c4c6eec98d85dd9bda30eebf`), and the receiver view hash
was identical (`062c4c5fc59c5618582d43f9e4c917ab97a32ecfd7249d5bfba2824fe0767287`).

`replay.sh` is the concise executable form of the J42 build and receiver checks.
