"""WG0P7 — drive the exact 14 frozen WG0O authority-API controls unchanged.

Uses the WG0O's own frozen oracle and unchanged adapter; only the reviewer
transport points at the repaired WG0P6 runtime.  Records raw per-case outcomes
plus the actual imported module identity.
"""
import hashlib
import json
import pathlib
import sys

RET = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RET / "repro"))

import phase_b_support_v1 as S  # noqa: E402
import authority_seam_adapter_v1 as A  # noqa: E402

cases = json.loads((RET / "repro" / "01_FROZEN_ACTUAL_AUTHORITY_API_CASES.json").read_text())["controls"]
court = A.AuthoritySeamCourt()
rows = []
for c in cases:
    try:
        out = court.execute_case(c["group"], c["case"])
    except Exception as exc:  # noqa: BLE001
        out = {"case": c["case"], "exception_type": type(exc).__name__,
               "exception_reason": str(exc), "served_supported_original_fact": False,
               "supported_fact_cells_served": 0, "new_I03_calls": 0, "runner_error": True}
    rows.append(out)
    print("%-55s exc=%-32s typed=%-8s served=%-5s cells=%-3s i03=%s" % (
        c["case"], out.get("exception_type"), out.get("typed_refusal"),
        out.get("served_supported_original_fact"), out.get("supported_fact_cells_served"),
        out.get("new_I03_calls")))

module = pathlib.Path(S.w.__file__).resolve()
data = module.read_bytes()
record = dict(schema="WG0P7_14_CASE_EXECUTION@1", cases=rows,
              candidate_module=str(module),
              candidate_module_sha256=hashlib.sha256(data).hexdigest(),
              candidate_module_git_blob_sha1=hashlib.sha1(
                  b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest())
(RET / "observations" / "frozen14_execution.json").write_text(
    json.dumps(record, indent=1, sort_keys=True, default=str) + "\n")
print("module", record["candidate_module_sha256"])
