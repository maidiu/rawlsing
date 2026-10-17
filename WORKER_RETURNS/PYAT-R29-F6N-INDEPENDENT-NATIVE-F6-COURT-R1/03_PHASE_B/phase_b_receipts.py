"""Independent F6N Phase-B receipts on the repaired producer.

Sourcefree only.  Uses the frozen F6L/F6N worlds and actual consumer calls.
"""
from __future__ import annotations

import copy
import hashlib
import json
import sys
from fractions import Fraction as F
from pathlib import Path

RET = Path(__file__).resolve().parents[1]
STAGE = RET / "03_PHASE_B/F6M_STAGE"
F6L = RET / "01_INHERITED_F6L"
sys.dont_write_bytecode = True
sys.path.insert(0, str(STAGE))
sys.path.insert(0, str(F6L / "02_PHASE_A/03_SCRIPTS"))
sys.path.insert(0, str(RET / "02_PHASE_A/03_SCRIPTS"))

from rawlsing_next.pre553_heterogeneous_synthesis import (  # noqa: E402
    synthesize, conditional, semantic_hash)
import rawlsing_next.pre553_heterogeneous_synthesis as P  # noqa: E402
import f6l_worlds as W  # noqa: E402
import f6n_worlds as N  # noqa: E402


def run(world, admit=lambda *_: True):
    return synthesize(world["target"], world["sources"], world["policy"], admit=admit)


def cells(c):
    return {"|".join(x["categories"]): str(F(x["probability"])) for x in c["distribution"]}


def ceilings(out):
    return sorted({n.get("authority_ceiling") for n in out["evidence_graph"]})


def main():
    out = {}
    # Null full-target distribution.
    null = run(W.novel_2x2_no_positivity())
    out["null_full_target"] = {
        "decision": null["decision"],
        "distribution": null["candidate"]["distribution"],
        "covered_subprobability": null["candidate"]["covered_subprobability"],
        "uncovered_target_mass": null["candidate"]["uncovered_target_mass"],
        "target_joint_status": null["target_joint_status"],
        "conditional_default": conditional(null, {"F6L_MATERIAL": "LOW"}, "F6L_ACTION"),
        "conditional_real_use": conditional(null, {"F6L_MATERIAL": "LOW"}, "F6L_ACTION", use="REAL_USE"),
        "ceilings": ceilings(null),
        "real_use_authorized": null["real_use_authorized"],
    }
    # Genuine positive.
    pos = run(W.positive_2x2())
    out["positive_complete"] = {
        "decision": pos["decision"],
        "joint": cells(pos["candidate"]),
        "uncovered_target_mass": pos["candidate"]["uncovered_target_mass"],
        "target_joint_status": pos["target_joint_status"],
        "conditional": conditional(pos, {"F6L_MATERIAL": "LOW"}, "F6L_ACTION"),
        "conditional_real_use": conditional(pos, {"F6L_MATERIAL": "LOW"}, "F6L_ACTION", use="REAL_USE"),
        "ceilings": ceilings(pos),
        "real_use_authorized": pos["real_use_authorized"],
    }
    # Rare/minority source excluded by aggregate support.
    rare = run(N.rare_renormalization(150))
    out["rare_excluded_source"] = {
        "decision": rare["decision"],
        "distribution": rare["candidate"]["distribution"],
        "covered_subprobability": rare["candidate"]["covered_subprobability"],
        "uncovered_target_mass": rare["candidate"]["uncovered_target_mass"],
        "target_joint_status": rare["target_joint_status"],
        "support": rare["candidate"]["support"],
        "conditional_default": conditional(rare, {"F6L_MATERIAL3": "HIGH"}, "F6L_ACTION3"),
        "conditional_real_use": conditional(rare, {"F6L_MATERIAL3": "HIGH"}, "F6L_ACTION3", use="REAL_USE"),
    }
    # Mixed declared-test + unverified source, forged admit=True.
    calls = []
    mixed = W.mixed_origin(W.positive_2x2())
    def mixed_admit(source, target, phase):
        calls.append({"source_id": source["source_id"], "phase": phase})
        return True
    mo = run(mixed, mixed_admit)
    out["mixed_origin_forged_admit"] = {
        "decision": mo["decision"],
        "test_origin": mo["test_origin"],
        "origin_classification": mo["origin_classification"],
        "real_source_qualification": mo["real_source_qualification"],
        "real_use_authorized": mo["real_use_authorized"],
        "owner_admission_status": mo["owner_admission_status"],
        "ceilings": ceilings(mo),
        "admission_calls": calls,
        "candidate_present": mo["candidate"] is not None,
        "conditional_default": conditional(mo, {"F6L_MATERIAL": "LOW"}, "F6L_ACTION"),
        "conditional_real_use": conditional(mo, {"F6L_MATERIAL": "LOW"}, "F6L_ACTION", use="REAL_USE"),
    }
    # All-declared-real forged admit.
    allreal = W.with_origin(W.positive_2x2(), False)
    ar = run(allreal)
    out["all_declared_real_forged_admit"] = {
        "decision": ar["decision"],
        "test_origin": ar["test_origin"],
        "origin_classification": ar["origin_classification"],
        "real_source_qualification": ar["real_source_qualification"],
        "real_use_authorized": ar["real_use_authorized"],
        "ceilings": ceilings(ar),
        "conditional_real_use": conditional(ar, {"F6L_MATERIAL": "LOW"}, "F6L_ACTION", use="REAL_USE"),
    }
    # Product-ref identity rebinding.
    sw = N.product_ref_substitution()
    so = run(sw)
    out["product_ref_substitution"] = {
        "decision": so["decision"],
        "measured_parent_refs": [b["measured_parent_ref"] for b in so["baseline"]],
        "input_hashes_match": [b["input_hash"] for b in so["baseline"]] == [semantic_hash(s) for s in sw["sources"]],
    }
    payload = {
        "schema": "PYAT_R29_F6N_PHASE_B_RECEIPTS@1",
        "producer": {
            "file": str(STAGE / "rawlsing_next/pre553_heterogeneous_synthesis.py"),
            "implementation_version": P.IMPLEMENTATION_VERSION,
            "method": P.METHOD,
            "sha256": hashlib.sha256(Path(P.__file__).read_bytes()).hexdigest(),
            "git_blob": hashlib.sha1(b"blob " + str(len(Path(P.__file__).read_bytes())).encode() + b"\0" + Path(P.__file__).read_bytes()).hexdigest(),
        },
        "receipts": out,
    }
    path = RET / "05_PHASE_B/02_CHANGED_UNCHANGED_RECEIPTS.json"
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps(payload, indent=2, sort_keys=True)[:8000])


if __name__ == "__main__":
    main()
