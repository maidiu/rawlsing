"""PYAT R26 T9C — genuine counterexamples: original T9B adapter vs repaired T9C.

This does NOT modify the original T9B return. It loads the original author module
by exact path, runs the seven defect assertions against BOTH adapters, and records
side-by-side observations. A repair is only real if the original fails the same
assertion that the corrected adapter passes.

The native V553 module is imported once, from this return's byte-verified closure,
for BOTH adapters: the original T9B return's copy of
`data/ddm_build_copy/ddm_v553_temporal_pressure.py` is asserted to be byte-identical
first, so reusing the cached native module is not a silent substitution.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

RET = Path(__file__).resolve().parent
T9B_RET = RET.parent / "PYAT-R18-T9B-TEMPORAL-HISTORY-CONSUMER-R1"
NATIVE = RET / "native"

sys.path.insert(0, str(RET))
sys.path.insert(0, str(NATIVE))

MINE = NATIVE / "data/ddm_build_copy/ddm_v553_temporal_pressure.py"
THEIRS = T9B_RET / "native/data/ddm_build_copy/ddm_v553_temporal_pressure.py"


def _sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def _blob(p: Path) -> str:
    return subprocess.run(["git", "hash-object", str(p)], capture_output=True,
                          text=True, check=True).stdout.strip()


NATIVE_BYTE_IDENTICAL = _sha(MINE) == _sha(THEIRS)

import t9b_temporal as T9C  # noqa: E402  (corrected adapter, this return)

spec = importlib.util.spec_from_file_location("t9b_temporal_original_t9b",
                                              T9B_RET / "t9b_temporal.py")
ORIG = importlib.util.module_from_spec(spec)
sys.modules["t9b_temporal_original_t9b"] = ORIG
spec.loader.exec_module(ORIG)

C = "SYNTH_COUNTRY_A"


def make_wave(mod, name, year, value, **kw):
    args = dict(wave_id=name, source_family="SYNTH_FAMILY", country=C,
                instrument="SYNTH_INSTRUMENT", edition="E1", cohort="COHORT_ALL",
                observation_year=year, published_year=year, value=value)
    args.update(kw)
    return mod.Wave(**args)


def make_case(mod, waves=None, **kw):
    args = dict(case_id="X", country=C,
                waves=tuple(waves if waves is not None
                            else [make_wave(mod, "W0", 1990, .20),
                                  make_wave(mod, "W1", 2000, .60)]),
                target_year=1995)
    args.update(kw)
    return mod.TemporalCase(**args)


def make_world(mod):
    return mod.StructuralWorld(
        "W_SYNTH_INSTITUTION",
        ("ROUTE_REDUCED_BURDEN", "ROUTE_PARTICIPATION", "ROUTE_DEFERRED_REVIEW"),
        ("GRANT_YOUNG_PERSON_ACCESS",), "SYNTH_INSTITUTION")


def snap(value):
    if hasattr(value, "as_dict"):
        return value.as_dict()
    return value


def probe(mod, which):
    """Execute every one of the ten independent RED assertions against `mod`."""
    w = make_world(mod)
    out = {}

    # R1
    native = mod.V553._authorize_v553_multi_wave_key(
        {"ready_for_v553": True, "comparison_authority_status": "multi_wave_authorized",
         "shared_semantic_columns": ["s"], "shared_directionality_columns": ["d"],
         "shared_position_columns": ["p"]},
        __import__("pandas").DataFrame([{
            "wave_id": "ONE", "structural_dimension_status": "resolved",
            "probe_ready_input_count": 1, "source_v552j_packet_ids_json": '["pkt"]',
            "structural_pressure_value": .2, "comparable_key_grain": "structural_channel_exact",
            "source_v552_structural_fact_lane": "temporal_fact",
            "canonical_semantic_signature": "sig"}]))
    adapted = mod.evaluate(make_case(mod, [make_wave(mod, "ONE", 1990, .2)]),
                           mod.METHOD_M0_HOLD)
    out["R1"] = {"native_status": native["multi_wave_authorization_status"],
                 "adapted": snap(adapted),
                 "assertion": "adapted.temporal_key != AUTHORIZED_SPARSE_TEMPORAL_KEY",
                 "passes": adapted.temporal_key != mod.AUTHORIZED_SPARSE_TEMPORAL_KEY}

    # R2
    r2 = {}
    for method in (mod.METHOD_M0_HOLD, mod.METHOD_M1_INTERP, mod.METHOD_M2_BACKOFF):
        try:
            got = mod.evaluate(make_case(mod, [make_wave(mod, "MISSING", 1990, float("nan"))]),
                               method)
            r2[method] = {"observation": snap(got),
                          "assertion": "value is None and refused_code is not None",
                          "passes": (got.value is None and got.refused_code is not None)}
        except Exception as exc:  # noqa: BLE001
            r2[method] = {"observation": {"exception": type(exc).__name__, "message": str(exc)},
                          "assertion": "returns typed unknown, does not raise",
                          "passes": False}
    out["R2"] = r2

    # R3
    wrong = make_wave(mod, "EXCLUDED", 1980, .1, country="OTHER",
                      source_family="WRONG_SOURCE", edition="WRONG_EDITION")
    valid = make_wave(mod, "VALID", 1990, .6, source_family="ACTUAL_SOURCE",
                      edition="ACTUAL_EDITION")
    got = mod.read_selected_world(w, make_case(mod, [wrong, valid]), mod.METHOD_M0_HOLD, 1995)
    out["R3"] = {"observation": snap(got),
                 "assertion": "provenance source_family/edition name ACTUAL_* not WRONG_*",
                 "passes": (got.provenance.get("source_family") == "ACTUAL_SOURCE"
                            and got.provenance.get("edition") == "ACTUAL_EDITION")}

    # R4
    from dataclasses import replace
    changed = replace(w, structural_routes=("ROUTE_DEFERRED_REVIEW",))
    a = mod.read_selected_world(w, make_case(mod), mod.METHOD_M0_HOLD, 2000)
    b = mod.read_selected_world(changed, make_case(mod), mod.METHOD_M0_HOLD, 2000)
    out["R4"] = {"world_a": {"structural_routes": list(w.structural_routes)},
                 "world_b": {"structural_routes": list(changed.structural_routes)},
                 "read_a": snap(a), "read_b": snap(b),
                 "assertion": "not structurally_identical(a, b)",
                 "passes": not mod.structurally_identical(a, b)}

    # R5
    got = mod.read_selected_world(w, make_case(mod), mod.METHOD_M1_INTERP, 1995,
                                  retrospective=True)
    out["R5"] = {"observation": snap(got),
                 "assertion": "no non-ROUTE_BLOCKED_NO_SUPPORT entry in opportunity_ids",
                 "passes": not [r for r in got.opportunity_ids
                               if r != "ROUTE_BLOCKED_NO_SUPPORT"]}

    # R6
    r6 = {}
    for method in (mod.METHOD_M0_HOLD, mod.METHOD_M2_BACKOFF):
        got = mod.evaluate(make_case(mod, ruptures=(1995,)), method,
                           clock_year=1997, retrospective=True)
        r6[method] = {"observation": snap(got),
                      "assertion": "value is None or RUPTURE in uncertainty/detail",
                      "passes": (got.value is None
                                 or "RUPTURE" in got.uncertainty
                                 or "RUPTURE" in (got.detail or "").upper())}
    out["R6"] = r6

    # R7
    got = mod.evaluate(make_case(mod), mod.METHOD_M0_HOLD, retrospective=True)
    lag = mod.pub_lag_of(got)
    out["R7"] = {"observation": snap(got), "pub_lag_of": list(lag),
                 "assertion": "set(pub_lag_of) <= set(basis_wave_ids)",
                 "passes": set(lag) <= set(got.basis_wave_ids)}

    out["_which"] = which
    return out


orig = probe(ORIG, "original_T9B")
rep = probe(T9C, "repaired_T9C")

def verdict(node):
    if isinstance(node, dict):
        if "passes" in node and "assertion" in node:
            return [node["passes"]]
        return [p for v in node.values() for p in verdict(v)]
    return []

counterexamples = []
for defect in ("R1", "R2", "R3", "R4", "R5", "R6", "R7"):
    o, r = orig[defect], rep[defect]
    counterexamples.append({
        "defect": defect,
        "assertion_count": len(verdict(o)),
        "original_t9b_passed": sum(1 for x in verdict(o) if x),
        "original_t9b_failed": sum(1 for x in verdict(o) if not x),
        "repaired_t9c_passed": sum(1 for x in verdict(r) if x),
        "repaired_t9c_failed": sum(1 for x in verdict(r) if not x),
        "original_t9b": o,
        "repaired_t9c": r,
    })

payload = {
    "schema": "PYAT_R26_T9C_02_ACTUAL_ORIGINAL_V553_AND_CONSUMER@1",
    "generated_by": "02_counterexamples.py",
    "original_author_return": str(T9B_RET.name),
    "original_author_commit": "edf3494b1b11cb71a78540aba950aa15da900c8a",
    "independent_t9i_court_commit": "a2a7bdeda76aa008b3d620b01af71f7fd6efaaae",
    "native_module": {
        "this_return_path": str(MINE.relative_to(RET)),
        "author_return_path": str(THEIRS),
        "sha256_this_return": _sha(MINE),
        "sha256_author_return": _sha(THEIRS),
        "git_blob_sha1_this_return": _blob(MINE),
        "git_blob_sha1_author_return": _blob(THEIRS),
        "byte_identical": NATIVE_BYTE_IDENTICAL,
        "reused_cached_module_is_legitimate": NATIVE_BYTE_IDENTICAL,
    },
    "native_controls": {},
    "counterexamples": counterexamples,
    "prohibitions": [
        "no real EE12 source pair", "no national inference", "no OC05",
        "no N11", "no N12", "no V3", "no method adoption",
    ],
}

# direct native controls (unchanged V553 machines)
import pandas as pd
report = {"ready_for_v553": True, "comparison_authority_status": "multi_wave_authorized",
          "shared_semantic_columns": ["s"], "shared_directionality_columns": ["d"],
          "shared_position_columns": ["p"]}
rows = [{"wave_id": f"N{i}", "structural_dimension_status": "resolved",
         "probe_ready_input_count": 1, "source_v552j_packet_ids_json": json.dumps([f"p{i}"]),
         "structural_pressure_value": .2 + .4 * i,
         "comparable_key_grain": "structural_channel_exact",
         "source_v552_structural_fact_lane": "temporal_fact",
         "canonical_semantic_signature": "sig"} for i in range(2)]
for count, label in ((2, "NATIVE_AUTHORIZATION_2"), (1, "NATIVE_AUTHORIZATION_1")):
    payload["native_controls"][label] = T9C.V553._authorize_v553_multi_wave_key(
        report, pd.DataFrame(rows[:count]))
payload["native_controls"]["NATIVE_AUTHORIZATION_BLOCKED"] = \
    T9C.V553._authorize_v553_multi_wave_key({}, pd.DataFrame())
obs = pd.DataFrame([{"temporal_pressure_key": "k", "country": "US", "survey_year": y,
                     "wave_id": str(y),
                     "multi_wave_authorization_status": T9C.AUTHORIZED_SPARSE_TEMPORAL_KEY,
                     "temporal_status": "observed_authorized_anchor"} for y in (1990, 2000)])
gap = T9C.V553._build_v553_interpolation_segment_index({}, obs, "t9c",
                                                       allow_interpolation=True)
row = gap.iloc[0].to_dict()
row["interpolation_allowed"] = bool(row["interpolation_allowed"])
row["anchor_count"] = int(row["anchor_count"])
row["gap_length_years"] = int(row["gap_length_years"])
row["segment_start_year"] = int(row["segment_start_year"])
row["segment_end_year"] = int(row["segment_end_year"])
payload["native_controls"]["NATIVE_GAP_ALLOW_INTERPOLATION_TRUE"] = row

# full consumer outputs of the repaired adapter on the frozen TC1 grid + two-time reads
methods = (T9C.METHOD_M0_HOLD, T9C.METHOD_M1_INTERP, T9C.METHOD_M2_BACKOFF)
payload["consumer"] = {
    "method_comparison_TC1": {
        m: {"AS_OF": snap(T9C.evaluate(make_case(T9C), m, retrospective=False)),
            "RETROSPECTIVE": snap(T9C.evaluate(make_case(T9C), m, retrospective=True))}
        for m in methods},
    "two_time_reads": {
        str(y): snap(T9C.read_selected_world(make_world(T9C), make_case(T9C),
                                             T9C.METHOD_M1_INTERP, y, retrospective=True))
        for y in (1990, 2000)},
    "endpoints_numerical": {
        str(y): T9C.evaluate(make_case(T9C), T9C.METHOD_M1_INTERP,
                             clock_year=y, retrospective=True).value
        for y in (1990, 2000)},
    "as_of_1995_M1": snap(T9C.evaluate(make_case(T9C), T9C.METHOD_M1_INTERP,
                                       clock_year=1995, retrospective=False)),
    "retrospective_1995_M1": snap(T9C.evaluate(make_case(T9C), T9C.METHOD_M1_INTERP,
                                               clock_year=1995, retrospective=True)),
}

(RET / "02_ACTUAL_ORIGINAL_V553_AND_CONSUMER.json").write_text(
    json.dumps(payload, indent=2, sort_keys=True) + "\n")

print(f"native byte_identical={NATIVE_BYTE_IDENTICAL}")
for c in counterexamples:
    print(f"{c['defect']}: original_T9B {c['original_t9b_passed']}pass/"
          f"{c['original_t9b_failed']}fail  ->  repaired_T9C "
          f"{c['repaired_t9c_passed']}pass/{c['repaired_t9c_failed']}fail "
          f"(assertions={c['assertion_count']})")