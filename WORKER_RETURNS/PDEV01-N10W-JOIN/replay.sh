#!/usr/bin/env bash
# Replay the actual J42 W41/E41/P41 two-input N10W receipt and controls.
# Writes only to WORKER_RETURNS/PDEV01-N10W-JOIN/replay/ plus a temp directory.
set -euo pipefail

ROOT="$(git rev-parse --show-toplevel)"
OUT="$ROOT/WORKER_RETURNS/PDEV01-N10W-JOIN/replay"
J42=f53cb0d2bce52640268c844c398bbd8007d28edc
J42_PACKET="WORKER_RETURNS/PYAT-R42-J42-COMPLETE-E41-W41-P41-ACTUAL-JOINT-PREV3-CONSUMER-R1"
TMPROOT="${TMPDIR:-/private/var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T/opencode}"
mkdir -p "$OUT" "$TMPROOT"
BASE="$(mktemp -d "$TMPROOT/pdev01-n10w-replay.XXXXXX")"
trap 'rm -rf "$BASE"' EXIT

git -C "$ROOT" archive "$J42" "$J42_PACKET" -o "$BASE/j42.tar"
tar -xf "$BASE/j42.tar" -C "$BASE"
ln -s "$ROOT/rawlsing_next" "$BASE/rawlsing_next"
printf 'gitdir: %s\n' "$(git -C "$ROOT" rev-parse --absolute-git-dir)" > "$BASE/.git"

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$ROOT" \
  python3 "$BASE/$J42_PACKET/runtime/j42_build.py" --outdir "$BASE/out" \
  > "$OUT/j42_build.stdout.log" 2> "$OUT/j42_build.stderr.log"
cp "$BASE/$J42_PACKET/n9_n10e_n10w_real_joined_consumer_receipts.json" \
  "$OUT/J42_RECEIPTS.json"

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$ROOT" python3 - "$OUT" <<'PY'
from copy import deepcopy
from pathlib import Path
import json
import sys

from rawlsing_next.tests.test_universal_world_binding import _joined_request
from rawlsing_next.pre553_universal_world_binding import (
    JoinedWorldField, select_joined_world_view,
)

out = Path(sys.argv[1])
receipts = json.loads((out / "J42_RECEIPTS.json").read_text())
key = "base/TEST_CURRENT/budget5"
source_rows = receipts["p41_joined_receipts"][key]["j42_bindings"]["e41_rows_hash"]
request = _joined_request(receipts, key, source_rows_hash=source_rows)
view = select_joined_world_view(request)

missing_n9 = deepcopy(receipts)
missing_n9["p41_joined_receipts"][key]["providers"].pop("n9_world", None)
missing_n10e = deepcopy(receipts)
missing_n10e["p41_joined_receipts"][key]["n10e_steps"] = []

negatives = {
    "missing_n9": select_joined_world_view(_joined_request(missing_n9, key)),
    "missing_n10e": select_joined_world_view(_joined_request(missing_n10e, key)),
    "wrong_source_rows": select_joined_world_view(
        _joined_request(receipts, key, source_rows_hash="f" * 64)
    ),
    "wrong_as_of": select_joined_world_view(
        _joined_request(receipts, key, as_of_ref="2099-01-01")
    ),
    "one_field": select_joined_world_view(
        _joined_request(receipts, key, fields=(JoinedWorldField("training_access", True),))
    ),
}
result = {
    "schema": "PDEV01_N10W_REPLAY_WITNESS@1",
    "positive": {
        "state": view.state,
        "reason_code": view.reason_code,
        "view_hash": view.view_hash,
        "families": view.consumer_values_read.get("families"),
        "n9_clock": view.consumer_values_read.get("n9_clock"),
        "n9_currentness": view.consumer_values_read.get("n9_currentness"),
        "n10e_steps": len(view.consumer_values_read.get("n10e_steps", [])),
        "n10w": view.consumer_values_read.get("n10w"),
    },
    "negatives": {
        name: {"state": value.state, "reason_code": value.reason_code}
        for name, value in negatives.items()
    },
}
(out / "REPLAY_WITNESS.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
print(json.dumps(result, indent=2, sort_keys=True))
PY

echo "replay complete: $OUT"
