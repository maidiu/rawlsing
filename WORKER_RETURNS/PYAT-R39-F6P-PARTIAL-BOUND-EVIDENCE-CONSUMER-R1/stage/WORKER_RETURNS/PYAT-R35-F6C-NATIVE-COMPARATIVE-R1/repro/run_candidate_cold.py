"""R35 F6C cold candidate runner.

Loads ONE candidate by absolute file path from the verified pinned blob, builds
the frozen worlds, executes synthesize + conditional, and writes one JSON
result. Invoked once per candidate in a separate COLD process so no candidate
can observe another's module state, and never twice in one interpreter.

Usage: python3 run_candidate_cold.py --candidate A --out result.json

Nothing here writes outside the given --out path. No source, actor, model,
Field Forge, N11/N12, V3 or route quantity is created.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
import platform
import socket
import sys
from fractions import Fraction as F
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STAGING = ROOT / "staging"
SHARED = STAGING / "shared"

# Candidate -> pinned blob recorded by this court. Asserted at load time so a
# substituted or drifted module cannot pass as the pinned owner.
CANDIDATES = {
    "A": (STAGING / "cand_A" / "rawlsing_next" / "pre553_heterogeneous_synthesis.py",
          "fc5e37fa5b2f0eb689593b42d95479d1327cb94c",
          "CORRECTED_NATIVE_S03FO_COMPARISON_A"),
    "A0": (STAGING / "cand_A0_historical" / "rawlsing_next" / "pre553_heterogeneous_synthesis.py",
           "182cc7970d7624f6614015f5a51d0602e1630d52",
           "HISTORICAL_CUSTODY_CONTROL_SUPERSEDED_NOT_COMPARISON_A"),
    "B": (STAGING / "cand_B" / "rawlsing_next" / "pre553_heterogeneous_synthesis.py",
          "2df811d76db258d98d89ffb43c830cb221ff9a7d",
          "REPAIRED_F6M_COMPARISON_B"),
}


def blob_sha(path):
    b = Path(path).read_bytes()
    return hashlib.sha1(b"blob " + str(len(b)).encode() + b"\0" + b).hexdigest()


def load_candidate(key):
    path, expected, role = CANDIDATES[key]
    got = blob_sha(path)
    if got != expected:
        raise SystemExit(f"ABORT candidate {key} blob {got} != pinned {expected}")
    sys.path.insert(0, str(SHARED))
    spec = importlib.util.spec_from_file_location(f"r35f6c_candidate_{key}", path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod, {"role": role, "pinned_blob": expected, "observed_blob": got,
                 "physical_path": str(path), "module_name": mod.__name__,
                 "module_file": os.path.realpath(mod.__file__)}


def q(x):
    return str(x) if isinstance(x, F) else x


def summarize_bundle(bundle):
    cand = bundle.get("candidate")
    out = {
        "decision": bundle.get("decision"),
        "target_joint_status": bundle.get("target_joint_status", "NOT_EMITTED"),
        "real_source_qualification": bundle.get("real_source_qualification"),
        "real_use_authorized": bundle.get("real_use_authorized", "NOT_EMITTED"),
        "use_scope": bundle.get("use_scope", "NOT_EMITTED"),
        "owner_admission_status": bundle.get("owner_admission_status", "NOT_EMITTED"),
        "origin_classification": bundle.get("origin_classification", "NOT_EMITTED"),
        "support_gate_semantics": bundle.get("support_gate_semantics", "NOT_EMITTED"),
        "content_hash": bundle.get("content_hash"),
        "refusals": bundle.get("refusals"),
        "overlap_diagnostics": bundle.get("overlap_diagnostics"),
    }
    if cand is None:
        out["candidate_is_none"] = True
        return out
    out["candidate_is_none"] = False
    out["uncovered_target_mass"] = cand["uncovered_target_mass"]
    out["distribution_is_none"] = cand["distribution"] is None
    out["distribution"] = cand["distribution"]
    out["covered_subprobability"] = cand.get("covered_subprobability")
    out["ordered_categories"] = cand.get("ordered_categories", "NOT_EMITTED")
    out["dependence"] = cand.get("dependence")
    out["coverage_detail"] = {
        z: {"target_share": v.get("target_share"),
            "sources": [{"source_id": s.get("source_id"),
                         "coefficient": s.get("coefficient"),
                         "conditional_source_weight": s.get("conditional_source_weight"),
                         "raw_support": s.get("raw_support")}
                        for s in v.get("sources", [])],
            "excluded_sources": v.get("excluded_sources", []),
            "uncovered_target_share": v.get("uncovered_target_share", "NOT_EMITTED"),
            "exclusion_reasons": v.get("exclusion_reasons", "NOT_EMITTED"),
            "minority_cell_protection": v.get("minority_cell_protection", "NOT_EMITTED")}
        for z, v in (cand.get("support") or {}).items()}
    unc = cand.get("uncertainty") or {}
    out["sampling_status"] = unc.get("sampling_status")
    out["source_disagreement_bounds"] = unc.get("source_disagreement_and_uncovered_bounds")
    out["bias_sensitivity_bounds"] = unc.get("bias_sensitivity_bounds")
    out["radii"] = unc.get("radii")
    return out


def run_conditional(mod, bundle, conditions, outcome, use=None):
    try:
        if use is None:
            res = mod.conditional(bundle, conditions, outcome)
        else:
            res = mod.conditional(bundle, conditions, outcome, use=use)
        return {"ok": True, "result": res}
    except Exception as exc:
        return {"ok": False, "error_type": type(exc).__name__, "error": str(exc)}


def run_candidate(key):
    mod, ident = load_candidate(key)
    sys.path.insert(0, str(ROOT / "repro"))
    import f6c_oracle_worlds as OW

    # `use` is keyword-only on B, so it never appears in co_argcount.
    supports_use_kw = "use" in mod.conditional.__code__.co_varnames

    results = {}
    for world_name, builder in OW.WORLD_BUILDERS.items():
        conditions, outcome = OW.CONSUMER_REQUEST[world_name]
        entry = {"consumer_request": {"conditions": conditions, "outcome": outcome},
                 "conditional_accepts_use_kwarg": supports_use_kw}
        target, sources, policy = builder()
        entry["target_strata"] = target["strata"]
        entry["source_strata_coverage"] = {
            s["source_id"]: {z: sum(c["n"] for c in t["cells"])
                             for z, t in s["strata"].items()} for s in sources}
        entry["minimum_raw_support"] = policy["minimum_raw_support"]
        try:
            bundle = mod.synthesize(target, sources, policy)
            entry["synthesize"] = {"ok": True, "bundle": summarize_bundle(bundle)}
            entry["conditional"] = run_conditional(mod, bundle, conditions, outcome)
            entry["conditional_standard_request"] = run_conditional(
                mod, bundle, {"material_security": "secure"}, "employment_position")
            if supports_use_kw:
                entry["conditional_real_use"] = run_conditional(
                    mod, bundle, {"material_security": "secure"}, "employment_position",
                    use="REAL_USE")
        except Exception as exc:
            entry["synthesize"] = {"ok": False, "error_type": type(exc).__name__,
                                   "error": str(exc)}
        results[world_name] = entry

    return {"candidate": key, "identity": ident, "results": results}


def run_c():
    sys.path.insert(0, str(SHARED))
    sys.path.insert(0, str(ROOT / "repro"))
    import f6c_method_c as MC
    import f6c_oracle_worlds as OW

    results = {}
    for world_name, builder in OW.WORLD_BUILDERS.items():
        conditions, outcome = OW.CONSUMER_REQUEST[world_name]
        entry = {"consumer_request": {"conditions": conditions, "outcome": outcome}}
        target, sources, policy = builder()
        entry["target_strata"] = target["strata"]
        entry["source_strata_coverage"] = {
            s["source_id"]: {z: sum(c["n"] for c in t["cells"])
                             for z, t in s["strata"].items()} for s in sources}
        entry["minimum_raw_support"] = policy["minimum_raw_support"]
        try:
            b = MC.nopooling_bounds(target, sources, policy)
            entry["bounds"] = {k: b[k] for k in (
                "method", "authority", "pooling", "positivity", "distinct_respondents",
                "strata", "per_source_native_descriptives",
                "target_marginal_bounds_employment_position",
                "target_marginal_bounds_material_security",
                "identified_point_component", "total_unknown_mass", "joint_status",
                "unidentified_cross_channel", "refusals", "claims_not_made")}
            entry["conditional"] = {"ok": True, "result": MC.condition_status(b, conditions, outcome)}
            entry["conditional_standard_request"] = MC.condition_status(
                b, {"material_security": "secure"}, "employment_position")
            # Control: with exactly one source's transport admitted for the
            # majority stratum, C should point-identify that stratum only.
            perm = {"majority": {sources[0]["source_id"]}}
            try:
                b2 = MC.nopooling_bounds(target, sources, policy, transport_permission=perm)
                entry["bounds_with_single_stratum_transport_admitted"] = {
                    "strata": b2["strata"],
                    "target_marginal_bounds_employment_position":
                        b2["target_marginal_bounds_employment_position"],
                    "total_unknown_mass": b2["total_unknown_mass"],
                    "joint_status": b2["joint_status"],
                }
            except Exception as exc:
                entry["bounds_with_single_stratum_transport_admitted"] = {
                    "ok": False, "error_type": type(exc).__name__, "error": str(exc)}
        except Exception as exc:
            entry["bounds"] = {"ok": False, "error_type": type(exc).__name__, "error": str(exc)}
        results[world_name] = entry

    return {"candidate": "C", "identity": {
        "role": "NO_POOLING_CONSERVATIVE_BOUNDS_COMPARISON_C",
        "pinned_blob": None, "observed_blob": None,
        "physical_path": str(ROOT / "repro" / "f6c_method_c.py"),
        "module_name": "f6c_method_c",
        "module_file": os.path.realpath(MC.__file__),
        "authority": MC.AUTHORITY,
        "native_primitive_reused": "complementary_binary_bounds from pinned blob "
                                   "fc5e37fa5b2f0eb689593b42d95479d1327cb94c"},
        "results": results}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--candidate", required=True, choices=sorted(CANDIDATES) + ["C"])
    ap.add_argument("--out", required=True)
    ap.add_argument("--round", default="1")
    a = ap.parse_args()
    payload = run_c() if a.candidate == "C" else run_candidate(a.candidate)
    payload["environment"] = {
        "python": sys.version.split()[0],
        "executable": sys.executable,
        "pid": os.getpid(),
        "hostname": socket.gethostname(),
        "platform": platform.platform(),
        "cold_round": a.round,
        "cwd": os.getcwd(),
        "PYTHONDONTWRITEBYTECODE": os.environ.get("PYTHONDONTWRITEBYTECODE"),
    }
    Path(a.out).write_text(json.dumps(payload, indent=2, default=q))
    print(f"wrote {a.out}")


if __name__ == "__main__":
    main()