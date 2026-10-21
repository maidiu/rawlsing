"""UR-B native composition characterization tests."""
from __future__ import annotations

import json
import os
import subprocess
import sys
from collections import Counter
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[2]
FIXTURES = ROOT / "fixtures"
PYTHONPATH = os.pathsep.join(str(p) for p in (
    ROOT, REPO,
    Path.home() / ".cache/uv/archive-v0/sFE7VO7nHEpr328Z",
    Path.home() / ".cache/uv/archive-v0/quC1M_vhOV9lE6BI",
))


def _cell_map(fact):
    return {row["cell"]: row for row in
            fact.target_topology.get("complete_cell_semantic_projection", [])}


def _run(cmd):
    env = dict(os.environ, PYTHONPATH=PYTHONPATH, PYTHONDONTWRITEBYTECODE="1")
    completed = subprocess.run(cmd, cwd=str(ROOT), env=env,
                               capture_output=True, text=True, timeout=300)
    assert completed.returncode == 0, completed.stderr[-3000:]
    return completed.stdout


def test_s1_decode_projection_i03_i05_and_batch_reach_real_consumers():
    from ur_b.s1 import build
    from ur_b.s1_queries import run
    from ur_b.s1_route_b import execute
    from ur_b.s1_batch import run as run_batch

    fx = build(FIXTURES / "ur_b_s1_xor.sav")
    setup, route = execute(fx)
    assert route.i03_results and len(route.i03_results) == 10
    assert route.i05_result.receipts
    assert route.learned_empirical_execution_receipt["claim_kind"] == "LEARNED_EMPIRICAL_EXECUTION_ONLY"
    assert route.object_graph.empirical_facts

    queries = run(fx)
    cells = _cell_map(queries["results"]["DIST_Y_WEIGHTED"].facts[0])
    assert cells["0"]["weighted_numerator_support_if_authorized"]["$exact_fraction"] == [12, 1]
    assert cells["1"]["weighted_numerator_support_if_authorized"]["$exact_fraction"] == [12, 1]
    joint = queries["results"]["JOINT_A_B_Y"].facts[0]
    assert joint.raw_denominator_support == 16
    assert len(joint.target_topology["complete_cell_semantic_projection"]) == 8
    assert queries["results"]["ZERO_SUPPORT_Z"].facts[0].typed_state == "UNRESOLVED"
    assert queries["results"]["ZERO_SUPPORT_Z"].facts[0].raw_denominator_support == 16

    batch = run_batch(fx)
    assert len(batch["manifest"].units) == 4
    assert len(batch["receipts"]) == 4
    assert all(r.state == "COMPLETED" for r in batch["receipts"])
    assert all(r.execution_performed for r in batch["receipts"])


def test_s1_batch_cold_resume_reconstructs_exact_receipts(tmp_path):
    script = (
        "import sys,json;"
        "from ur_b.s1 import build;"
        "from ur_b.batch_resume import dump,resume;"
        "fx=build('fixtures/ur_b_s1_xor.sav');"
        "mode=sys.argv[1];path=sys.argv[2];"
        "d=dump(fx,path) if mode=='dump' else None;"
        "r=resume(fx,path) if mode=='resume' else None;"
        "print(json.dumps({'pending':len(r['pending']) if r else None,"
        "'receipts':len(r['receipts']) if r else None,"
        "'manifest_hash':r['manifest_hash'] if r else None}))"
    )
    path = tmp_path / "s1_batch.json"
    first = json.loads(_run([sys.executable, "-B", "-c", script, "dump", str(path)]).strip().splitlines()[-1])
    second = json.loads(_run([sys.executable, "-B", "-c", script, "resume", str(path)]).strip().splitlines()[-1])
    assert first["receipts"] is None
    assert second["pending"] == 0
    assert second["receipts"] == 4


def test_s1_caller_byte_custody_changes_values_under_old_source_identity():
    from ur_b.custody import compare

    receipt = compare(FIXTURES / "ur_b_s1_xor.sav")
    assert receipt["same_source_identity"] is True
    assert receipt["row1_a_before"] == [(1, "A", 0.0)]
    assert receipt["row1_a_after"] == [(1, "A", 1.0)]
    assert receipt["fact_before"] != receipt["fact_after"]
    assert receipt["cells_before"] != receipt["cells_after"]
    assert receipt["changed_values_under_old_identity"] is True


def test_s2_person_weights_household_and_cross_unit_refusal():
    from ur_b.s2 import build_person, build_household
    from ur_b.s2_queries import run_person, run_household, cross_unit_attempt

    person = build_person(FIXTURES / "ur_b_s2_person.dta")
    house = build_household(FIXTURES / "ur_b_s2_household.dta")
    person_out = run_person(person)
    out = _cell_map(person_out["results"]["OUTCOME_WEIGHTED"].facts[0])
    assert [out[k]["weighted_numerator_support_if_authorized"]["$exact_fraction"][0]
            for k in ("0", "1", "2")] == [21, 27, 24]
    pitem = _cell_map(person_out["results"]["PITEM_P1_WEIGHTED"].facts[0])
    assert [pitem[k]["weighted_numerator_support_if_authorized"]["$exact_fraction"][0]
            for k in ("0", "1", "2")] == [9, 12, 15]
    pitemb = _cell_map(person_out["results"]["PITEM_B_P1_WEIGHTED"].facts[0])
    assert [pitemb[k]["weighted_numerator_support_if_authorized"]["$exact_fraction"][0]
            for k in ("0", "1", "2")] == [15, 9, 12]
    half = _cell_map(person_out["results"]["OUTCOME_HOUSEHOLD_HALF"].facts[0])
    assert [half[k]["weighted_numerator_support_if_authorized"]["$exact_fraction"][0]
            for k in ("0", "1", "2")] == [8, 7, 5]
    house_out = run_household(house)
    hcells = _cell_map(house_out["result"].facts[0])
    assert [hcells[k]["raw_numerator_support"] for k in ("0", "1")] == [4, 4]
    cross = cross_unit_attempt(person, house)
    assert cross["accepted"] is True
    assert cross["typed_state"] == "UNAVAILABLE"


def test_s3_long_repeated_occurrences_are_duplicated_by_physical_projection():
    from ur_b.s3 import release
    from ur_b.s3_repeated_query import run

    fx, rel = release(FIXTURES / "ur_b_s3_repeated.sav",
                      respondents_count=12, repeated=True)
    from rawlsing_next.pre553_empirical_objects import RespondentEvent
    events = [obj for obj in rel.public_objects if isinstance(obj, RespondentEvent)]
    def oid(value):
        try:
            return value["object_id"]
        except Exception:
            return value.object_id

    by_question = Counter()
    qnames = {oid(q.native_question_ref): oid(q.native_question_ref)
              for q in fx["projection"].questions}
    for event in events:
        by_question[qnames[oid(event.native_question_ref)]] += 1
    score_question = next(key for key in qnames.values() if "SCORE" in key)
    assert by_question[score_question] == 48
    assert len(events) == 168
    repeated = run(fx)
    assert repeated["result"].facts[0].typed_state == "INTEGRITY_FAILURE"


def test_native_imports_and_fixture_hashes_are_exact():
    import hashlib
    import pyreadstat
    from rawlsing_next.pre553_physical_decoder import decode_sav

    paths = {
        "rawlsing_next/pre553_physical_decoder.py": "d2a074a41fb556a1cd5928a5fe1421ef3672a4e5",
        "rawlsing_next/pre553_source_backed_c11_facade.py": "8a761119e4a8d68eb291fc4edfadb52e027f8284",
        "rawlsing_next/pre553_route_b_production.py": "2385cd327dced3c5b887b59085aa0d21b04d78c3",
        "rawlsing_next/pre553_batch_runner.py": "2d291600b9a10c56d9c6f6de7f7d619f6c52e829",
    }
    for relative, blob in paths.items():
        assert hashlib.sha1(b"blob %d\0" % (REPO / relative).stat().st_size
                            + (REPO / relative).read_bytes()).hexdigest() == blob
    assert pyreadstat.__version__ == "1.3.6"
    incidence = decode_sav(FIXTURES / "ur_b_s1_xor.sav")
    assert incidence.row_count == 16
    assert incidence.source_sha256 == "3d69458668c66ee8a14fa70b3b4c6420aeb22c557c8a2ababae7388b819a3921"
