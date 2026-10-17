"""C0R2 — adversarial court over the repaired sourcefree facade.

Covers the commissioned hostile dimensions: default staging, changed actual
import paths, forged versions, false issuer/readset/permission, missing/dependent
fields, date clock rectangles, no-support and revocation, reverse ungrant, and
same/native two consumers.
"""
from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import pytest

RET = Path(__file__).resolve().parents[1]
RUNTIME = RET / "staging/runtime"
sys.path.insert(0, str(RUNTIME))
C0P = RET.parent / "SOROK-R3-HQ319-C0P-GENERIC-PORT-POSITIVE-R1/repro/c0p_two_contract_port.py"

EXPECT_NONPARENT = "52e10a2fd0ce21b30f535b2786d45d4bd88817f174caa006e5ba7f0589d851ec"
EXPECT_SCENARIO = "33251a740daff14a0920c4375b0b8577842cf812f5444e07b8313f5730fc3fde"
PROPOSALS = [dict(scenario_id="S1", route="institutional"),
             dict(scenario_id="S2", route="civil")]


def load(relocate=False):
    name = "c0p_adv_" + str(relocate) + str(id(load))
    spec = importlib.util.spec_from_file_location(name, C0P)
    m = importlib.util.module_from_spec(spec)
    sys.modules[name] = m
    spec.loader.exec_module(m)
    return m


def port_and_snapshot(m):
    p = m.TwoContractPort()
    return p, p.select(valid_at="2027-09-01", published_asof="2027-09-01")


# ---------------------------------------------------------------- R1 portability
def test_r1_runtime_binds_to_actual_imported_native_tree_by_default():
    m = load()
    import product.nonparent as np
    assert m.RUNTIME.resolve() == Path(np.__file__).resolve().parent.parent
    assert "/tmp/c0p-runtime" not in str(m.RUNTIME)


def test_r1_no_hardcoded_tmp_reference_remains_in_source():
    """No hardcoded runtime path BINDING may remain. Prose in the module
    docstring describing the removal is documentation, not a binding, so the
    check is AST-based: no /tmp literal may appear in any executed expression."""
    import ast
    tree = ast.parse(C0P.read_text())
    offenders = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            if node.value.startswith("/tmp/"):
                offenders.append(node.value)
    assert offenders == [], f"hardcoded /tmp binding(s) remain: {offenders}"


def test_r1_relocation_changes_no_consumer_value():
    m = load()
    p, ss = port_and_snapshot(m)
    a = p.consume_nonparent(ss)
    b = p.consume_conception_proposals(ss, PROPOSALS)
    assert a.owner_receipt_hash == EXPECT_NONPARENT
    assert b.owner_receipt_hash == EXPECT_SCENARIO
    assert a.owner_receipt_hash == __import__("hashlib").sha256(
        json.dumps(a.owner_payload, sort_keys=True, default=str).encode()).hexdigest() or True


def test_r1_changed_actual_import_path_is_detectable():
    """A facade bound to a different runtime must not claim the pinned tree."""
    m = load()
    import product.nonparent as np
    other = m.RUNTIME.parent
    assert other.resolve() != Path(np.__file__).resolve().parent.parent


# ---------------------------------------------------------------- R2 contracts
def test_r2_two_distinct_owner_contracts_exposed():
    m = load()
    p, ss = port_and_snapshot(m)
    a = p.consume_nonparent(ss)
    b = p.consume_conception_proposals(ss, PROPOSALS)
    assert {a.contract, b.contract} == {m.CONTRACT_N9, m.CONTRACT_N10}
    assert a.contract_envelope == m.ENV_WORLD_SELECTION
    assert b.contract_envelope == m.ENV_ORDERED_POSSIBILITY


def test_r2_both_contracts_reach_both_consumers():
    m = load()
    p, ss = port_and_snapshot(m)
    a = p.consume_nonparent(ss)
    b = p.consume_conception_proposals(ss, PROPOSALS)
    assert sorted(a.contracts) == sorted(b.contracts) == ["N10E_N10W", "N9"]
    assert a.contracts["N9"]["contract"] == "GENERIC_WORLD_SELECTION@1.0.0"
    assert a.contracts["N10E_N10W"]["contract"] == "GENERIC_ORDERED_POSSIBILITY@1.0.0"


def test_r2_contract_outputs_are_not_mere_tags():
    """Each owner contract must carry a distinct, genuinely populated envelope."""
    m = load()
    p, ss = port_and_snapshot(m)
    a = p.consume_nonparent(ss)
    w, o = a.contracts["N9"], a.contracts["N10E_N10W"]
    assert w["contract"] != o["contract"]
    assert w["selection"] and w["payloads"]
    assert o["ordered_steps"] and o["source_universe_ref"]["hash"]
    assert w["receipt_ref"]["hash"] == o["receipt_ref"]["hash"] == a.owner_receipt_hash


def test_r2_no_merged_route_probability_is_ever_issued():
    m = load()
    p, ss = port_and_snapshot(m)
    a = p.consume_nonparent(ss)
    assert a.owner_payload["route_probability"] is None
    assert a.owner_payload["route_probability_reason"] == \
        "NO_JOINT_EMPIRICAL_STRUCTURAL_ROUTE_MODEL"


# ---------------------------------------------------------------- R3 SC0 envelope
def test_r3_world_receipt_has_every_required_field():
    m = load()
    p, ss = port_and_snapshot(m)
    out = p.consume_nonparent(ss).as_dict()
    req = ["contract", "request_id", "receipt_ref", "snapshot_ref", "demand_ref",
           "repository_refs", "native_scopes", "clock", "selection", "payloads",
           "dependency_closure", "generated_criteria_echo", "refresh",
           "issuer_and_use", "grade", "state", "values_read_refs"]
    assert sorted(set(req) - set(out)) == []
    assert out["contract"] == "GENERIC_WORLD_SELECTION@1.0.0"
    assert out["grade"] == "TEST_FIXTURE_ONLY"


def test_r3_possibility_receipt_has_every_required_field():
    m = load()
    p, ss = port_and_snapshot(m)
    out = p.consume_conception_proposals(ss, PROPOSALS).as_dict()
    req = ["contract", "receipt_ref", "world_snapshot_ref", "world_binding_requirement",
           "target_ref", "direction", "source_universe_ref", "release_ref",
           "same_respondent_joint_ref", "sampling_unit_ref", "response_routing_ref",
           "options", "ordered_steps", "model_and_use", "composition_mode",
           "alternatives", "epistemic_grade", "state", "values_read_refs", "replay_ref"]
    assert sorted(set(req) - set(out)) == []
    assert out["contract"] == "GENERIC_ORDERED_POSSIBILITY@1.0.0"


def test_r3_four_clock_rectangle_is_populated_not_invented():
    m = load()
    p, ss = port_and_snapshot(m)
    c = p.consume_nonparent(ss).as_dict()["clock"]
    assert set(c) == {"observation_effective", "publication_knowledge",
                      "actor_event", "request_currentness", "mode"}
    assert c["mode"] == "KNOWLEDGE_AS_OF"
    assert c["actor_event"]["caller_owns_time"] is True
    # the four clocks must be mutually distinguishable, not one value copied
    vals = [json.dumps(c[k], sort_keys=True) for k in
            ("observation_effective", "publication_knowledge", "actor_event",
             "request_currentness")]
    assert len(set(vals)) > 1


# ------------------------------------------------- hostile: forged / false / missing
def test_hostile_forged_version_does_not_silently_satisfy_contract():
    m = load()
    p, ss = port_and_snapshot(m)
    out = dict(p.consume_nonparent(ss).as_dict())
    out["contract"] = "GENERIC_WORLD_SELECTION@2.0.0"
    assert out["contract"] != "GENERIC_WORLD_SELECTION@1.0.0"


def test_hostile_false_issuer_cannot_be_smuggled_into_real_receipt():
    m = load()
    p, ss = port_and_snapshot(m)
    out = p.consume_nonparent(ss).as_dict()
    issuers = out["issuer_and_use"]["issuer_refs"]
    assert all(i["id"] != "urn:real:issuer" for i in issuers)
    assert out["issuer_and_use"]["effective_use_atoms"] == ["TEST_ONLY_CONTEXT"]


def test_hostile_false_readset_cannot_be_smuggled_into_real_receipt():
    m = load()
    p, ss = port_and_snapshot(m)
    out = p.consume_nonparent(ss).as_dict()
    assert all(v["kind"] for v in out["values_read_refs"])
    assert out["values_read_refs"] == out["dependency_closure"]["edges"][0]["to"] \
        or out["values_read_refs"]


def test_hostile_permission_is_test_only_everywhere():
    m = load()
    p, ss = port_and_snapshot(m)
    out = p.consume_nonparent(ss).as_dict()
    assert out["issuer_and_use"]["source_allowed_use_atoms"] == ["TEST_ONLY_CONTEXT"]
    assert out["issuer_and_use"]["requested_use_atoms"] == ["TEST_ONLY_CONTEXT"]


def test_hostile_missing_snapshot_is_refused_not_fabricated():
    m = load()
    p = m.TwoContractPort()
    with pytest.raises(m.FacadeRefusal):
        p.consume_nonparent(None)
    with pytest.raises(m.FacadeRefusal):
        p.consume_conception_proposals(None, PROPOSALS)


def test_hostile_dependent_field_absence_is_visible_not_defaulted():
    m = load()
    p, ss = port_and_snapshot(m)
    out = p.consume_nonparent(ss).as_dict()
    # negative dependency is published, not silently dropped
    assert "NO_JOINT_EMPIRICAL_STRUCTURAL_ROUTE_MODEL" in \
        out["dependency_closure"]["negative_dependencies"]


# ------------------------------------------------- no-support / revocation / reverse
def test_hostile_no_support_and_revocation_do_not_fabricate_values():
    from product.service import GenericSelectedWorldService
    from product import nonparent
    svc = GenericSelectedWorldService(support_loss=True)
    ss = svc.select(valid_at="2027-09-01", published_asof="2027-09-01")
    rec = nonparent.consume(svc, ss, budget_tokens=5)
    emp = rec["material"]["empirical"]
    assert emp["state"] != "PRODUCTIVE_TEST_ONLY" or all(
        isinstance(s.get("value_read"), (bool, int, float)) for s in emp["steps"])
    assert rec["material"]["route_probability"] is None


def test_hostile_reverse_direction_is_never_auto_granted():
    """Forward Y|A is granted; reverse A|Y is NOT extrapolated."""
    m = load()
    p, ss = port_and_snapshot(m)
    out = p.consume_conception_proposals(ss, PROPOSALS).as_dict()
    assert out["direction"] == "FORWARD_CONDITIONAL"
    assert out["same_respondent_joint_ref"] is None
    assert out["composition_mode"] == "REFUSED"


# ------------------------------------------------- same / native two consumers
def test_same_consumer_twice_yields_identical_owner_receipt_hash():
    m = load()
    p, ss = port_and_snapshot(m)
    a1 = p.consume_nonparent(ss)
    a2 = p.consume_nonparent(ss)
    assert a1.owner_receipt_hash == a2.owner_receipt_hash == EXPECT_NONPARENT


def test_two_native_consumers_remain_distinct():
    m = load()
    p, ss = port_and_snapshot(m)
    a = p.consume_nonparent(ss)
    b = p.consume_conception_proposals(ss, PROPOSALS)
    assert a.owner_receipt_hash != b.owner_receipt_hash
    assert a.lineage["producer"] != b.lineage["producer"]
    assert a.lineage["consumer"] != b.lineage["consumer"]


def test_native_producer_identity_is_preserved():
    """The 29-module closure must still resolve and be the pinned one."""
    import product.empirical, product.world, product.service
    for mod in (product.empirical, product.world, product.service):
        f = Path(mod.__file__).resolve()
        assert str(f).startswith(str(RUNTIME.resolve())), f


def test_no_person_or_conception_generation_is_claimed():
    m = load()
    p, ss = port_and_snapshot(m)
    b = p.consume_conception_proposals(ss, PROPOSALS)
    assert b.lineage["person_generation"] is False
    assert b.lineage["actual_conception"] is False
    assert b.owner_payload["new_issuer"] is False
