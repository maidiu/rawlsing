"""S44 deployable qualified source-runtime handoff.

Binds the accepted original source/semantic authorities (HARVEST/P10/V525b,
AS2B LiTS-I) and the U43 authenticated ingress to the B43 issuer-bound feeder
and the E41/J42 consumers. No grant is invented; a missing grant yields a finite
single owner decision plus the all35 deferred ledger.
"""
from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

RETURN_ROOT = Path(__file__).resolve().parent.parent
REPO = RETURN_ROOT.parents[1]
for p in (RETURN_ROOT, REPO):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

U43_COMMIT = "dcf71f1afbfdbe8a084844cea5fffbc73d9d91ef"
B43_COMMIT = "0fa15c1eda1ca36d89b0bbd948b655aa68f17370"
J42_COMMIT = "f53cb0d2bce52640268c844c398bbd8007d28edc"
F43_COMMIT = "c0271e2b8d59018d3cf2af7b366258ea503295a6"
A42_COMMIT = "843175b0587b54db3df1f461ad9f7f1314894372"
U43_MODULE_BLOB = "07e6f419f7fb5e588d041ce9993fa17b935d3626"

RUNTIME_MEMBERS = ("resolver", "workloads", "source_factory", "host", "purpose")


class S44RuntimeRefused(PermissionError):
    def __init__(self, code, detail=""):
        self.code = code
        super().__init__(code + (":" + detail if detail else ""))


def _u43(path):
    return json.loads((RETURN_ROOT / "frozen_u43" / "evidence" / path).read_text())


def verify_u43_entrypoint(gp) -> dict:
    gp.verify(U43_COMMIT, "rawlsing_next/pre553_issued_workload.py",
              expect_blob_sha1=U43_MODULE_BLOB)
    path = RETURN_ROOT / "frozen_u43" / "rawlsing_next" / "pre553_issued_workload.py"
    name = "rawlsing_next.pre553_issued_workload"
    if name not in sys.modules:
        spec = importlib.util.spec_from_file_location(name, path)
        mod = importlib.util.module_from_spec(spec)
        sys.modules[name] = mod
        spec.loader.exec_module(mod)
    mod = sys.modules[name]
    for sym in ("execute_issued_workload", "WorkloadAdmissionError"):
        if not hasattr(mod, sym):
            raise S44RuntimeRefused("S44_U43_ENTRYPOINT_MISSING_SYMBOL", sym)
    return {"module": name, "blob_sha1": U43_MODULE_BLOB,
            "symbols": ["execute_issued_workload", "WorkloadAdmissionError"]}


def validate_runtime(runtime) -> dict:
    missing = [m for m in RUNTIME_MEMBERS if not hasattr(runtime, m)]
    if missing:
        raise S44RuntimeRefused("S44_RUNTIME_INCOMPLETE", ",".join(missing))
    if not getattr(runtime, "host") or not getattr(runtime, "purpose"):
        raise S44RuntimeRefused("S44_RUNTIME_MISSING_AUTHENTICATED_HOST_OR_PURPOSE")
    return {"state": "S44_RUNTIME_CONTRACT_SATISFIED",
            "members": list(RUNTIME_MEMBERS),
            "host": getattr(runtime, "host"), "purpose": getattr(runtime, "purpose")}


def all35_deferred_ledger() -> dict:
    permitted = _u43("currently_permitted_native_manifests.json")
    packets = {p["atlas_id"]: p for p in _u43("original35_issuer_decision_packets.json")}
    rows = []
    for w in permitted["waves"]:
        sid = w["atlas_id"]
        pkt = packets.get(sid, {})
        rows.append({
            "source_id": sid,
            "native_manifest": w.get("native_manifest"),
            "state": w.get("state"),
            "owner_decisions": w.get("owner_decisions"),
            "recorded_missing_materials": pkt.get("recorded_missing_materials"),
            "source_edition_or_hash": pkt.get("source_edition_or_hash"),
        })
    return {"schema": "S44_ALL35_DEFERRED_LEDGER@1", "wave_count": len(rows),
            "waves": rows,
            "original_measured_wave_count": permitted.get("original_measured_wave_count", 0),
            "U_E_pre_count": permitted.get("U_E_pre_count"),
            "counts_as_operations": False}


def single_highest_yield_decision(historical: dict) -> dict:
    packets = {p["atlas_id"]: p for p in _u43("original35_issuer_decision_packets.json")}
    pkt = packets["SRC27"]
    a = historical["as2b"]
    return {
        "schema": "S44_SINGLE_COMPETENT_OWNER_DECISION@1",
        "selected_wave": "SRC27",
        "selected_source": "LiTS-I",
        "why_highest_yield": (
            "strongest verified historical original-source positive (AS2B: 29,002 respondents, "
            "58,004 events, 8/8 I03 executed, one SUPPORTED fact 516c1a8b... 5155/5155); "
            "unblocks the first current selected-B measured product with the least new grant"),
        "exact_source_identity": {
            "source_sha256": a["source_sha256"],
            "historical_host": a["historical_host"],
            "historical_commit": a["commit"],
        },
        "exact_missing_competent_decisions": [d["demand_id"] for d in pkt["demands"]],
        "owner_actions": [{"demand_id": d["demand_id"], "owner": d["owner"],
                           "exact_next_actions": d["exact_next_actions"]}
                          for d in pkt["demands"]],
        "liTS_c11_prerequisite": {
            "source_release_ref": "LITS1-I02-F02-SUCCESSOR-7cac43e2ca5b31cb-bf305bf3f169d669",
            "semantic_hash": "192926fabd9c9c3d40e43b1d7705ca2bcfe7f8d06e286be26d4b886d436df43f",
            "missing": "complete 15-section C11SourceReleaseCandidate preimages OR exact current source+host+purpose reconstruction warrant",
        },
        "grant_present": False,
        "worker_can_self_issue": False,
        "on_grant": ("B43 issuer-bound admission + U43 execute_issued_workload -> selected Route B "
                     "C11/I03/I05/Batch -> M1/M2/B5/I4 -> E41/N10E -> original E04 consumer -> A42"),
    }


def handoff(gp, historical: dict) -> dict:
    entry = verify_u43_entrypoint(gp)
    ledger = all35_deferred_ledger()
    decision = single_highest_yield_decision(historical)
    return {
        "schema": "S44_SOURCE_RUNTIME_HANDOFF@1",
        "grade": "FIRST_ORIGINAL_CURRENT_B_MEASURED_NOT_YET_EARNED",
        "return_heads": {"U43": U43_COMMIT, "B43": B43_COMMIT, "J42": J42_COMMIT,
                         "F43": F43_COMMIT, "A42": A42_COMMIT},
        "u43_entrypoint": entry,
        "runtime_contract": {"members": list(RUNTIME_MEMBERS),
                             "trusted_infrastructure": True,
                             "caller_supplied_checkpoint_receipts": "REFUSED"},
        "grant_present": False,
        "raw_source_read": False,
        "deferred_ledger": ledger,
        "single_decision": decision,
        "historical_positive": historical["as2b"],
    }
