#!/usr/bin/env python3
"""HQ198 — independent exercises of the eight commissioned broker properties.

These are deliberately NOT the candidate's own courts. Each property is
exercised here directly against the repaired candidate, so a passing court that
had grown soft would still be caught.

Synthetic carriers only. No real survey source is opened.
"""
from __future__ import annotations

import io
import json
import os
import sys
import tempfile
import time
from pathlib import Path

import pandas as pd
import pyreadstat

sys.path.insert(0, "/Users/matthewsmith/Desktop/Rawlsing_Worktrees/hq198-r9-requal")

from rawlsing_next.pre553_physical_decoder import decode_dta, decode_sav  # noqa: E402
from rawlsing_next.pre553_source_access_broker import (  # noqa: E402
    GovernedSourceOpen,
    SourceAccessBroker,
    SourceAccessBudget,
    SourceAccessViolation,
)

TMP = Path(tempfile.mkdtemp(prefix="hq198-exercise-"))
results = []


def record(name: str, ok: bool, detail) -> None:
    results.append({"exercise": name, "pass": bool(ok), "detail": detail})
    print(f"  {'PASS' if ok else 'FAIL'}  {name}")
    print(f"        {detail}")


def carrier(fmt: str, name: str, rows: int = 60, cols: int = 3) -> str:
    data = {}
    for c in range(cols):
        data[f"V{c:02d}"] = [float(i) * (c + 1) for i in range(rows)]
    path = TMP / f"{name}.{fmt}"
    frame = pd.DataFrame(data)
    if fmt == "sav":
        pyreadstat.write_sav(frame, str(path))
    else:
        pyreadstat.write_dta(frame, str(path))
    return str(path)


def needed_bytes(path: str) -> int:
    b = SourceAccessBroker(path)
    b.bind_reader("SAV")
    b.existence_check(); b.hash_pass(); b.metadata_read()
    n = b.account_dict()["reader_bytes"]
    b.close()
    return n


def attempt(path: str, cap):
    b = SourceAccessBroker(path, budget=SourceAccessBudget(reader_bytes=cap))
    b.bind_reader("SAV")
    b.existence_check(); b.hash_pass()
    started = time.monotonic()
    refused, code, message = False, None, None
    try:
        b.metadata_read()
    except SourceAccessViolation as exc:
        refused, code, message = True, exc.code, str(exc)
    elapsed = time.monotonic() - started
    accounts = b.account_dict()
    b.close()
    return {"refused": refused, "code": code, "message": message,
            "elapsed_s": round(elapsed, 6), "accounts": accounts}


print("=== HQ198 independent broker exercises ===")

# 1 + 2 + 3 — exactly-enough, one-byte-short, never beyond cap
p = carrier("sav", "caps")
need = needed_bytes(p)
exact = attempt(p, need)
short = attempt(p, need - 1)
record("reader_bytes exactly-enough completes",
       exact["refused"] is False and exact["accounts"]["reader_bytes"] == need,
       f"cap={need} -> refused={exact['refused']} consumed={exact['accounts']['reader_bytes']} (needed {need})")
record("reader_bytes one-byte-short refuses",
       short["refused"] is True and short["code"] == "READER_BYTES_LIMIT_EXCEEDED"
       and short["accounts"]["reader_bytes"] == need - 1,
       f"cap={need-1} -> code={short['code']} consumed={short['accounts']['reader_bytes']}")
sweep = []
breach = None
for cap in (1, 7, 64, 199, need - 1, need, need + 1, need * 3):
    r = attempt(p, cap)
    within = r["accounts"]["reader_bytes"] <= cap
    sweep.append({"cap": cap, "consumed": r["accounts"]["reader_bytes"], "within_cap": within,
                  "refused": r["refused"]})
    if not within:
        breach = cap
record("no bytes beyond ceiling (8-ceiling sweep)", breach is None,
       f"consumed<=cap in every case; breach={breach}; sweep={json.dumps(sweep)}")

# 4 — the limiting mechanism is NOT a callback exception
gov = GovernedSourceOpen(p)
gov.arm_limit(24)
raised = False
served = []
try:
    view = gov.view()
    while True:
        chunk = view.read(8192)
        served.append(len(chunk))
        if chunk == b"":
            break
        if len(served) > 10000:
            break
except BaseException as exc:                      # noqa: BLE001
    raised = True
    served.append(f"EXC:{type(exc).__name__}")
total = gov.bytes_read
truncated_or_exhausted = gov.limit_truncated or gov.limit_exhausted
gov.disarm_limit(); gov.close()
record("no callback exception as the limiting mechanism",
       raised is False and total <= 24 and truncated_or_exhausted,
       f"raised_inside_read={raised} bytes_served={total} (cap 24) "
       f"chunk_sizes={served[:6]} truncated_or_exhausted={truncated_or_exhausted}")

# 5 — DTA view/reset behaviour
dp = carrier("dta", "dta60")
gov = GovernedSourceOpen(dp)
reuse_failed = False
try:
    shared = gov.view()
    pyreadstat.read_dta(shared, row_offset=0, row_limit=2)
    pyreadstat.read_dta(shared, row_offset=2, row_limit=2)
except Exception:
    reuse_failed = True
reset_ok = True
detail = ""
try:
    a = pyreadstat.read_dta(gov.view(), row_offset=0, row_limit=2)[0]
    b = pyreadstat.read_dta(gov.view(), row_offset=2, row_limit=2)[0]
    # V00 is built as float(i) * (c + 1) with c == 0, so its values are 0,1,2,3...
    # chunk0 must be rows 0-1 and chunk1 rows 2-3.
    reset_ok = list(a["V00"]) == [0.0, 1.0] and list(b["V00"]) == [2.0, 3.0]
    detail = f"chunk0={list(a['V00'])} chunk1={list(b['V00'])}"
except Exception as exc:
    reset_ok = False
    detail = f"{type(exc).__name__}: {exc}"
opens_dta = gov.physical_opens
views_dta = gov.views_issued
gov.close()
record("DTA view/reset behaviour", reuse_failed and reset_ok and opens_dta == 1,
       f"naive_single_view_reuse_failed={reuse_failed} reset_view_correct={reset_ok} "
       f"{detail} physical_opens={opens_dta} views={views_dta}")

# 6 — chunk_rows honoured on a carrier larger than one chunk
big = carrier("sav", "big200", rows=200)
inc = decode_sav(big)
cells = [c for batch in inc.iter_batches(batch_size=30) for c in batch]
acc = inc.source_access_receipt["accounts"]
rows_seen = sorted({c.row_ordinal for c in cells})
batch_sizes = [len(b) for b in inc.iter_batches(batch_size=30)]
vals = [c.raw_value for c in cells if c.variable_name == "V00"]
expected_chunks = -(-200 // (30 // 3))       # rows_per_chunk = batch//ncols
record("chunk_rows honoured on a carrier larger than one chunk",
       len(rows_seen) == 200 and max(batch_sizes) <= 30 and acc["chunk_reads"] >= expected_chunks
       and acc["path_opens"] == 1 and vals == [float(i) for i in range(200)],
       f"rows_covered={len(rows_seen)} max_batch={max(batch_sizes)} "
       f"chunk_reads={acc['chunk_reads']} (expected>={expected_chunks}) "
       f"path_opens={acc['path_opens']} V00_values_exact={vals == [float(i) for i in range(200)]}")
inc.close_source_access()

# 7 — selected / full counters kept separate
selp = carrier("sav", "sel")
sel = decode_sav(selp, selected_variables=("V01",))
sa = sel.source_access_receipt["accounts"]
record("selected/full counters separate",
       sa["selected_reads"] == 1 and sa["full_reads"] == 0 and sa["metadata_reads"] == 1
       and sa["reader_bytes"] > 0,
       f"selected_reads={sa['selected_reads']} full_reads={sa['full_reads']} "
       f"metadata_reads={sa['metadata_reads']} reader_bytes={sa['reader_bytes']} "
       f"bound_ordinals={sel.source_access_receipt['selected_read_configuration']['bound_ordinals']}")
sel.close_source_access()

# 8 — selected-mode non-suppression disclosure
full = decode_sav(selp)
fa = full.source_access_receipt["accounts"]
disc = full.source_access_receipt["selected_route_physical_column_suppression"]
full.close_source_access()
record("selected-mode non-suppression disclosure preserved",
       disc.startswith("NOT_ENFORCED_BY_READER") and "reads_full_stream_then_subsets" in disc,
       f"disclosure={disc[:96]}")
record("selected route does NOT claim byte suppression (physical bytes still full-stream)",
       sa["reader_bytes"] > 0,
       f"selected-route reader_bytes={sa['reader_bytes']} vs full-route reader_bytes={fa['reader_bytes']} "
       f"(comparable magnitude => no physical suppression is being claimed)")

summary = {
    "schema": "HQ198_INDEPENDENT_BROKER_EXERCISES@1.0.0",
    "CATEGORY": "C2_OBSERVED_SYNTHETIC",
    "category_law": "Synthetic carriers only. Not survey-semantic equivalence. Zero real sources opened.",
    "candidate_under_test": "4b6335ca5fc485108b0ffb1d682a29a02e1eee51 (repair a483cb6619a84c4785296e923a8571447041ffa5)",
    "bytes_required_reference": need,
    "exercises": results,
    "passed": sum(1 for r in results if r["pass"]),
    "total": len(results),
}
out = os.environ.get("HQ198_OUT", "/tmp/hq198_exercises.json")
Path(out).write_text(json.dumps(summary, indent=1), encoding="utf-8")
print(f"\n{summary['passed']}/{summary['total']} independent exercises passed")
print(f"written: {out}")
raise SystemExit(0 if summary["passed"] == summary["total"] else 1)
