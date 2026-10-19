"""Independent I2 Court B (F6P) claim-edge test module.

Authored by the independent reviewer (DeepSeek Harness / DeepSeek V4.1 Flash),
NOT by the F6P author. It re-derives the W1/W2/W3/W7 exact-rational oracles from
the frozen world inputs with reviewer arithmetic (no candidate output is used as
the oracle), and it independently severs the actual F6M producer and the
consumer's uncovered-mass read. Named fault-witness positives:

  test_uncovered_mass_preserved_independently            (consumer-side defect)
  test_consumer_responds_to_actual_producer_decision     (producer-side defect)
"""
from __future__ import annotations

import hashlib
from fractions import Fraction as F
from pathlib import Path
import sys

import pytest


def _repo_root() -> Path:
    p = Path(__file__).resolve()
    for cand in p.parents:
        if (cand / "rawlsing_next").is_dir() and (cand / "WORKER_RETURNS").is_dir():
            return cand
    raise RuntimeError("repo root not found")


ROOT = _repo_root()
F6P = ROOT / "WORKER_RETURNS/PYAT-R39-F6P-PARTIAL-BOUND-EVIDENCE-CONSUMER-R1"
for _p in (str(F6P), str(F6P / "native"), str(F6P / "oracle"), str(F6P / "tests"), str(ROOT)):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from f6p_fixtures import MODULES, build, request  # noqa: E402
import f6p_partial_bound_evidence_consumer as C  # noqa: E402
import f6c_oracle_worlds as OW  # noqa: E402
from rawlsing_next.pre553_empirical_objects import semantic_hash  # noqa: E402

LABELS = OW.LABELS
CELLS = OW.CELLS


def _mapped_cells(source, stratum):
    table = {}
    for cell in source["strata"][stratum]["cells"]:
        cats = tuple(cell["categories"])
        lab = tuple(source["axes"][i]["category_map"][c] for i, c in enumerate(cats))
        table[lab] = table.get(lab, F(0)) + F(cell["mass"])
    return table


def independent_oracle(builder):
    """Reviewer arithmetic over frozen inputs: joint mass, uncovered, exclusions."""
    target, sources, policy = builder()
    strata = {z: F(share) for z, share in target["strata"].items()}
    min_support = policy["minimum_raw_support"]
    weights = policy["source_weights"]
    joint = {k: F(0) for k in CELLS}
    uncovered = F(0)
    exclusions = []
    for z, share in strata.items():
        present = [s for s in sources if z in s["strata"]]
        eligible = [s for s in present
                    if sum(c["n"] for c in s["strata"][z]["cells"]) >= min_support
                    and sum(_mapped_cells(s, z).values()) > 0]
        denom = sum(weights[s["source_id"]] for s in present)
        eligible_weight = sum(weights[s["source_id"]] for s in eligible)
        missing = share * (1 - F(eligible_weight, denom)) if denom else share
        uncovered += missing
        for s in sources:
            if s not in eligible:
                exclusions.append({
                    "stratum": z, "source_id": s["source_id"],
                    "reason": ("NO_SOURCE_STRATUM" if z not in s["strata"]
                               else "AGGREGATE_SUPPORT_OR_MASS_INSUFFICIENT")})
        if not eligible_weight:
            continue
        for s in eligible:
            alpha = F(weights[s["source_id"]], denom)
            table = _mapped_cells(s, z)
            mass = sum(table.values())
            for k in CELLS:
                joint[k] += share * alpha * (table.get(k, F(0)) / mass)
    return joint, uncovered, exclusions


def _point_from_joint(joint, condition):
    (ck, cv), = condition.items()
    i = tuple(LABELS).index(ck)
    selected = {k: v for k, v in joint.items() if k[i] == cv}
    denom = sum(selected.values())
    out = {}
    oi = 1 - i
    for k, v in selected.items():
        out[k[oi]] = out.get(k[oi], F(0)) + v / denom
    return out


def _cand_covered(bundle):
    return {tuple(c["categories"]): F(c["probability"])
            for c in bundle["candidate"]["covered_subprobability"]}


def _consumer_covered(result):
    return {tuple(k.split("|")): F(v) for k, v in result["covered_subprobability"].items()}


def test_independent_oracle_matches_f6m_and_consumer_W1_W2_W3_W7():
    expected = {
        "W1_full_coverage_disjoint": (
            {(("secure", "formal")): F(5, 16), ("secure", "informal"): F(3, 16),
             ("insecure", "formal"): F(17, 80), ("insecure", "informal"): F(23, 80)},
            F(0)),
        "W2_mixed_eligibility_trap": (
            {(("secure", "formal")): F(1, 4), ("secure", "informal"): F(1, 8),
             ("insecure", "formal"): F(3, 16), ("insecure", "informal"): F(3, 16)},
            F(1, 4)),
        "W7_source_excluded_all_strata": (
            {(("secure", "formal")): F(3, 20), ("secure", "informal"): F(1, 10),
             ("insecure", "formal"): F(1, 8), ("insecure", "informal"): F(1, 8)},
            F(1, 2)),
        "W3_minority_whole_stratum_absent": (
            {(("secure", "formal")): F(6, 25), ("secure", "informal"): F(4, 25),
             ("insecure", "formal"): F(1, 5), ("insecure", "informal"): F(1, 5)},
            F(1, 5)),
    }
    for world, (cells, uncovered) in expected.items():
        joint, unc, _ = independent_oracle(OW.WORLD_BUILDERS[world])
        assert joint == cells, world
        assert unc == uncovered, world
        bundle = build("B", world)
        assert _cand_covered(bundle) == cells, world
        assert F(bundle["candidate"]["uncovered_target_mass"]) == uncovered, world
        result = C.consume_f6m_evidence(bundle, request(world))
        assert _consumer_covered(result) == cells, world
        assert F(result["uncovered_target_mass"]) == uncovered, world
        assert sum(cells.values()) + uncovered == 1
        if uncovered == 0:
            assert result["evidence_state"] == C.SUPPORTED
            point = _point_from_joint(joint, request(world)["conditions"])
            assert {k: str(v) for k, v in point.items()} == result["supported_point"]
            assert result["supported_point"] == {"formal": "5/8", "informal": "3/8"}
        else:
            assert result["evidence_state"] == C.PARTIAL
            assert result["supported_point"] is None
            assert bundle["decision"] == "PARTIAL_IDENTIFICATION_ONLY"
            assert bundle["target_joint_status"] == "NO_COMPLETE_TARGET_JOINT"


def test_minority_and_exclusions_recomputed_independently():
    _, unc2, exc2 = independent_oracle(OW.WORLD_BUILDERS["W2_mixed_eligibility_trap"])
    assert unc2 == F(1, 4)
    assert {"S_A"} == {e["source_id"] for e in exc2 if e["stratum"] == "minority"}
    assert all(e["reason"] == "AGGREGATE_SUPPORT_OR_MASS_INSUFFICIENT" for e in exc2)
    _, unc7, exc7 = independent_oracle(OW.WORLD_BUILDERS["W7_source_excluded_all_strata"])
    assert unc7 == F(1, 2)
    sa = {e["stratum"] for e in exc7 if e["source_id"] == "S_A"}
    assert sa == {"majority", "minority"}
    _, unc3, exc3 = independent_oracle(OW.WORLD_BUILDERS["W3_minority_whole_stratum_absent"])
    assert unc3 == F(1, 5)
    assert {e["source_id"] for e in exc3} == {"S_A", "S_B"}
    assert {e["reason"] for e in exc3} == {"NO_SOURCE_STRATUM"}

    r2 = C.consume_f6m_evidence(build("B", "W2_mixed_eligibility_trap"),
                                request("W2_mixed_eligibility_trap"))
    assert any(e["source_id"] == "S_A" and e["stratum"] == "minority" for e in r2["exclusions"])
    assert set(r2["covered_subprobability"]) == {
        "secure|formal", "secure|informal", "insecure|formal", "insecure|informal"}
    r7 = C.consume_f6m_evidence(build("B", "W7_source_excluded_all_strata"),
                                request("W7_source_excluded_all_strata"))
    assert {e["stratum"] for e in r7["exclusions"] if e["source_id"] == "S_A"} == {"majority", "minority"}
    r3 = C.consume_f6m_evidence(build("B", "W3_minority_whole_stratum_absent"),
                                request("W3_minority_whole_stratum_absent"))
    assert {e["source_id"] for e in r3["exclusions"]} == {"S_A", "S_B"}
    assert {e["reason"] for e in r3["exclusions"]} == {"NO_SOURCE_STRATUM"}


def test_corrected_A_is_comparison_and_A0_is_only_control():
    a_blob = hashlib.sha1(b"blob " + str(len(Path(MODULES["A"].__file__).read_bytes())).encode()
                          + b"\0" + Path(MODULES["A"].__file__).read_bytes()).hexdigest()
    a0_blob = hashlib.sha1(b"blob " + str(len(Path(MODULES["A0"].__file__).read_bytes())).encode()
                           + b"\0" + Path(MODULES["A0"].__file__).read_bytes()).hexdigest()
    assert a_blob == "fc5e37fa5b2f0eb689593b42d95479d1327cb94c"
    assert a0_blob == "182cc7970d7624f6614015f5a51d0602e1630d52"
    assert MODULES["B"].__file__.endswith("pre553_heterogeneous_synthesis.py")
    for world in ("W2_mixed_eligibility_trap", "W7_source_excluded_all_strata"):
        ba = build("A", world)
        r = C.consume_f6m_evidence(ba, request(world))
        assert ba["candidate"]["uncovered_target_mass"] == "0"
        assert r["evidence_state"] == C.FALSE_FULL
        assert r["supported_point"] is None
    ba3 = build("A", "W3_minority_whole_stratum_absent")
    assert C.consume_f6m_evidence(ba3, request("W3_minority_whole_stratum_absent"))["evidence_state"] == C.INCONSISTENT


def test_transport_and_model_use_refused_independently():
    bundle = build("B", "W2_mixed_eligibility_trap")
    req = request("W2_mixed_eligibility_trap")
    req["transport_permission"] = "OWNER_APPROVED"
    r = C.consume_f6m_evidence(bundle, req)
    assert r["evidence_state"] == C.PROHIBITED
    assert r["supported_point"] is None
    req2 = request("W2_mixed_eligibility_trap")
    req2["use"] = "REAL_USE"
    assert C.consume_f6m_evidence(bundle, req2)["evidence_state"] == C.PROHIBITED
    complete = build("B", "W1_full_coverage_disjoint")
    cond = MODULES["B"].conditional(complete, {"material_security": "secure"},
                                    "employment_position", use="REAL_USE")
    assert cond["state"] == "UNAVAILABLE" and cond["reason"] == "UNVERIFIED_OWNER_ADMISSION"


def test_no_fabricated_behavioral_probability():
    for world in ("W1_full_coverage_disjoint", "W2_mixed_eligibility_trap",
                  "W7_source_excluded_all_strata", "W3_minority_whole_stratum_absent"):
        result = C.consume_f6m_evidence(build("B", world), request(world))
        text = str(result)
        assert '"route_probability"' not in text and '"selection_weight"' not in text
        assert result["no_route_probability"] is True and result["no_selection_weight"] is True
        if F(result["uncovered_target_mass"]) > 0:
            assert result["supported_point"] is None
        for bound in result["bounds"]:
            assert F(bound["lower"]) <= F(bound["upper"])


def test_uncovered_mass_preserved_independently():
    for world, unc in (("W2_mixed_eligibility_trap", "1/4"),
                       ("W7_source_excluded_all_strata", "1/2"),
                       ("W3_minority_whole_stratum_absent", "1/5")):
        bundle = build("B", world)
        result = C.consume_f6m_evidence(bundle, request(world))
        assert result["evidence_state"] == C.PARTIAL, world
        assert F(result["uncovered_target_mass"]) == F(unc), world
        assert F(bundle["candidate"]["uncovered_target_mass"]) == F(unc), world
        assert result["supported_point"] is None, world


def test_consumer_responds_to_actual_producer_decision():
    bundle = build("B", "W2_mixed_eligibility_trap")
    assert bundle["decision"] == "PARTIAL_IDENTIFICATION_ONLY"
    assert bundle["target_joint_status"] == "NO_COMPLETE_TARGET_JOINT"
    assert F(bundle["candidate"]["uncovered_target_mass"]) == F(1, 4)
    result = C.consume_f6m_evidence(bundle, request("W2_mixed_eligibility_trap"))
    assert result["evidence_state"] == C.PARTIAL


def test_consumer_requires_real_f6m_bundle_identity():
    bundle = build("B", "W2_mixed_eligibility_trap")
    tampered = dict(bundle)
    tampered["candidate"] = dict(bundle["candidate"])
    tampered["candidate"]["uncovered_target_mass"] = "0"
    with pytest.raises(C.ConsumerRefusal, match="BUNDLE_REPLAY_MISMATCH"):
        C.consume_f6m_evidence(tampered, request("W2_mixed_eligibility_trap"))
    rehashed = dict(tampered)
    rehashed["content_hash"] = semantic_hash({k: v for k, v in rehashed.items() if k != "content_hash"})
    result = C.consume_f6m_evidence(rehashed, request("W2_mixed_eligibility_trap"))
    assert result["evidence_state"] != C.PARTIAL
    assert result["supported_point"] is None
