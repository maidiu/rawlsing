"""R51 joined B49 → G50 → B49 native U43/C11/I03/Batch consumer court."""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
CAND = ROOT / "candidate"
sys.path.insert(0, str(CAND))
sys.path.insert(0, str(ROOT.parents[1]))
import r51_joined_source_producer as J


def test_b49_corpus_package_and_administered_pair_are_exact():
    corpus = J.corpus()
    package = J.selected_package()
    assert corpus.source_count == 35
    assert len(corpus.unmatched_ids) == 26
    assert corpus.total_authority_items == 18276
    assert len(package.accounted_item_ids) == 1198
    assert len(package.selected) == 50
    assert len(package.held) == 7
    assert len(package.excluded) == 1141
    b = J.b49_bundle()
    assert b.administered_ids
    assert {x.source_variable_code for x in b.administered} >= {"q301_2", "q301_7"}
    assert all(x.classification == "ADMINISTERED_MEASUREMENT_U" for x in b.administered)


def test_g50_bundle_keeps_b49_source_identity_and_not_g50_toy():
    b49 = J.b49_bundle()
    bundle = J.g50_bundle(b49)
    assert bundle.source_id == J.selected_package().source.source_id
    assert bundle.source_id != "SYNTH-SRC-A"
    assert bundle.source_sha256 == b49.source_sha256
    assert bundle.schema == "SourceDecisionBundle@candidate1"
    assert bundle.held == ("CURRENT_SOURCE_HOST_PURPOSE_NOT_GRANTED",)
    assert bundle.current_selection is None
    f = J.frontier(bundle)
    assert f.policy_grade == "PROPOSED_TEST_ONLY"
    assert f.e_pre_count != 432
    assert f.original_science_grade.startswith("SOURCEFREE_PROPOSAL")
    assert {op.targets for op in f.eligible() if op.claim_class == "DIST"} >= {("q301_2",), ("q301_7",)}
    assert any(op.claim_class == "JOINT" and op.targets == ("q301_2", "q301_7") for op in f.eligible())


def test_joined_g50_operation_executes_real_b49_native_consumer():
    op = J.find_eligible(J.frontier())
    result, receipt = J.execute_joined(op)
    assert result.summary.batch_state == "COMPLETED"
    assert receipt["schema"] == "R51_JOINED_SOURCE_TO_NATIVE_CONSUMER@1"
    assert receipt["source_id"] == J.selected_package().source.source_id
    assert receipt["g50_operation_id"] == op.op_id
    assert receipt["b49_target_variable_code"] == "q301_2"
    assert receipt["g50_claim_class"] == "DIST"
    assert receipt["b49_native_numerator"] == 1
    assert receipt["b49_native_denominator"] == 1
    assert receipt["consumer"] == "PRE553_I03_EXACT_EMPIRICAL_QUERY@1.0.0"
    assert receipt["adp019_admission_receipt"] == "ADP019_ADMISSION_RECEIPT_ABSENT"
    assert receipt["e2_performed"] is False
    assert receipt["native_actor_admitted"] is False
    assert receipt["original_e_pre"] is None
    assert receipt["current_source_host_purpose_grant"] is None


def test_source_value_mutation_changes_same_downstream_fact_but_not_epre():
    op = J.find_eligible(J.frontier())
    good, good_receipt = J.execute_joined(op)
    bad, bad_receipt = J.execute_joined(op, rows=J.MUTATED_ROWS)
    assert good_receipt["b49_native_fact_ref"] != bad_receipt["b49_native_fact_ref"]
    assert good_receipt["b49_native_numerator"] == 1
    assert bad_receipt["b49_native_numerator"] == 2
    assert good_receipt["b49_native_denominator"] == 1
    assert bad_receipt["b49_native_denominator"] == 2
    assert good_receipt["g50_operation_id"] == bad_receipt["g50_operation_id"]
    assert good_receipt["consumer"] == bad_receipt["consumer"]
    assert good_receipt["frontier_e_pre_root"] == bad_receipt["frontier_e_pre_root"]


def test_policy_mutation_removes_the_eligible_native_operation_and_restores():
    baseline = J.find_eligible(J.frontier())
    op, remaining = J.policy_mutation_removes_operation()
    assert baseline.op_id == op.op_id
    assert remaining == []
    with pytest.raises(J.JoinRefusal):
        J.find_eligible(J.frontier(pol=J.policy(target_roles=("q301_7",))))
    restored = J.find_eligible(J.frontier())
    result, receipt = J.execute_joined(restored)
    assert result.summary.batch_state == "COMPLETED"
    assert receipt["b49_target_variable_code"] == "q301_2"


def test_joint_operation_is_not_flattened_to_one_target():
    joint = next(op for op in J.frontier().eligible()
                 if op.claim_class == "JOINT" and op.targets == ("q301_2", "q301_7"))
    with pytest.raises(J.JoinRefusal, match="B49_ONE_TARGET_ADAPTER_UNSUPPORTED"):
        J.lower_to_b49(joint)


def test_wrong_source_edition_and_native_fact_refusal_are_typed():
    from rawlsing_next.pre553_source_native_preimage_adapter import NativePreimageRefusal
    from rawlsing_next.pre553_inherited_source_rules import SourceRuleRefusal
    with pytest.raises(SourceRuleRefusal):
        J.select_source_rules(J.corpus(), family="LiTS", wave="I",
                              as_of=J.AS_OF, expected_source_sha256="0" * 64)
    with pytest.raises(NativePreimageRefusal):
        J.materialize_native_preimages(
            package=J.selected_package(), inventory=J.inventory("0" * 64),
            incidence=J.incidence(J.SOURCE_ROWS, "0" * 64),
            authorities=J.build_authority_set(source=J.selected_package().source, as_of=J.AS_OF),
            as_of=J.AS_OF,
        )


def test_original35_accounting_and_null_original_science_are_preserved():
    rows = J.coverage()
    assert len(rows) == 35
    assert len({r["source_id"] for r in rows}) == 35
    assert len({(r["family"], r["wave"]) for r in rows}) == 35
    for row in rows:
        assert row["declared_sha256"]
        assert row["original_administered_measurement_u"] is None


def test_m48_canary_matrix_is_complete_and_explicit():
    rows = J.canary_rows()
    assert len(rows) == 28
    assert {r["id"] for r in rows} == {f"C{i:02d}" for i in range(1, 29)}
    assert {r["disposition"] for r in rows} <= {
        "NATIVE_EXECUTED", "TYPED_REFUSAL", "POLICY_HOLD", "SPEC_ONLY_NATIVE_UNSUPPORTED"
    }


def test_cold_joined_consumer_replays_exactly(tmp_path):
    code = (
        "import json,sys;"
        f"sys.path.insert(0,{str(CAND)!r});"
        f"sys.path.insert(0,{str(ROOT.parents[1])!r});"
        "import r51_joined_source_producer as J;"
        "op=J.find_eligible(J.frontier());"
        "res,rec=J.execute_joined(op);"
        "print(json.dumps({'rec':rec,'batch':res.summary.batch_state,'envelope':None},sort_keys=True))"
    )
    env = dict(os.environ, PYTHONPATH=str(CAND) + os.pathsep + str(ROOT.parents[1]))
    outs = []
    for _ in range(2):
        proc = subprocess.run([sys.executable, "-B", "-c", code], capture_output=True,
                              text=True, env=env, cwd=str(ROOT.parents[1]), timeout=180)
        assert proc.returncode == 0, proc.stderr
        outs.append(json.loads(proc.stdout.strip().splitlines()[-1]))
    assert outs[0] == outs[1]
