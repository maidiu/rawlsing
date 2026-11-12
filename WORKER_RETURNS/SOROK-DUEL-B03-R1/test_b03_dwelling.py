"""B03 sourcefree proof: committed dwelling conditions constrain drum-kit feasibility."""
from __future__ import annotations

from argparse import Namespace
import copy
import inspect
import json
from pathlib import Path
import subprocess
import sys

import pytest

RETURNS = Path(__file__).resolve().parents[1]
P6 = RETURNS / "SOROK-P6-ONE-LIVING-HOUSE-R1"
ENGINE = RETURNS / "SOROK-DEVELOPMENTAL-RECURSION-ENGINE-R1"
for _path in (P6, ENGINE):
    if str(_path) not in sys.path:
        sys.path.insert(0, str(_path))

import house  # noqa: E402
from developmental_recursion.contracts import RecursionRefusal  # noqa: E402
import run_p6  # noqa: E402
from house import (  # noqa: E402
    DWELLING_SLOT,
    DRUM_KIT_REQUESTS,
    commit_dwelling,
    establish_dwelling,
    material_feasibility,
    mother_material_input,
    read_dwelling,
    read_household,
    read_house,
    scene,
)


def run_cmd(state, command, **args):
    return run_p6.experience(
        state, Namespace(command=command, request_id=None, **args)
    )


def open_owner(state):
    return run_p6.open_owner(state / "actual-p2")


def counts(session):
    store = session.product.store
    return {
        "episodes": len(store.episodes(session.branch_id)),
        "checkpoints": len(store.checkpoints(session.branch_id)),
        "world_events": len(store.world_events(session.branch_id)),
        "perceptions": len(store.perceptions(session.branch_id)),
    }


def facts_for(session):
    return copy.deepcopy(house.dwelling_fixture(session))


def test_actual_root_dwelling_constrains_concrete_drum_kit_without_possession(tmp_path):
    state = tmp_path / "state"
    run_cmd(state, "new")
    owner = open_owner(state)
    try:
        session = owner.base_owner.fanin.session
        dwelling = read_dwelling(session)
        household = read_household(session)
        acoustic = material_feasibility(session, DRUM_KIT_REQUESTS["acoustic"])
        junior = material_feasibility(session, DRUM_KIT_REQUESTS["junior"])
        mother = mother_material_input(session, DRUM_KIT_REQUESTS["junior"])
        before = counts(session)
        _, before_house = read_house(session)
        before_scene = scene(session)

        assert dwelling["schema"] == "SOROK_DWELLING_MATERIAL_READ@1"
        assert dwelling["grade"] == "SOURCEFREE_FIXTURE"
        assert dwelling["root"] == household["root"]
        assert dwelling["branch"] == session.branch_id
        assert dwelling["epoch"] <= dwelling["clock"]
        assert len(dwelling["source"]) == 64
        int(dwelling["source"], 16)
        assert dwelling["home"]["dwelling_id"] == household["place"]["dwelling_id"]
        assert dwelling["home"]["rooms"] == household["place"]["rooms"]
        assert dwelling["home"]["tenancy"]["holder_actor_slot"] == "A"
        assert dwelling["home"]["tenancy"]["instrument_policy"] == (
            "acoustic_instruments_with_quiet_hours"
        )
        assert dwelling["space"]["usable_room"] == "living room"
        assert dwelling["space"]["floor_area_m2"] == 8.0
        assert dwelling["space"]["clearance_m2"] == 1.0
        assert dwelling["acoustics"]["max_indoor_loudness_db"] == 80
        assert dwelling["acoustics"]["neighbor_shared_walls"] == 2
        assert dwelling["costs"]["rent_due_now"] == 12
        assert dwelling["household_source"] == household["source"]
        assert dwelling["household_material_hash"] == household["material_hash"]
        assert dwelling["provenance"]["scope"] == "P6_MATERIAL_FACT_ONLY"
        assert dwelling["provenance"]["fork_state"] == "CURRENT_BRANCH"

        assert acoustic["status"] == "REFUSED"
        assert acoustic["reasons"] == ["REFUSED_NOISE", "REFUSED_AFFORDABILITY"]
        assert acoustic["unknowns"] == []
        assert acoustic["conditions"] == ["QUIET_HOURS=22:00-07:00"]
        assert junior["status"] == "ADMISSIBLE"
        assert junior["reasons"] == []
        assert junior["unknowns"] == []
        assert junior["request"]["kind"] == "junior_drum_kit"
        assert junior["dwelling"]["source"] == dwelling["source"]
        assert junior["household"]["source"] == household["source"]
        assert junior["material_reader"] == "house.material_feasibility"
        assert junior["mother_decision"] == "NOT_EVALUATED"
        assert junior["parent_action"] is None
        assert junior["possession_created"] is False

        assert mother["schema"] == "SOROK_MOTHER_MATERIAL_INPUT@1"
        assert mother["first_consumer"] == "NONE_VERIFIED"
        assert mother["material_reader"] == "house.material_feasibility"
        assert mother["mother_decision"] == "NOT_EVALUATED"
        assert mother["parent_action"] is None
        assert mother["request"] == junior["request"]
        assert mother["feasibility"] == junior
        assert mother["dwelling"] == dwelling
        assert mother["household"] == household
        assert mother["feasibility"]["dwelling"]["source"] == mother["dwelling"]["source"]
        assert mother["feasibility"]["household"]["source"] == mother["household"]["source"]

        assert counts(session) == before
        assert scene(session) == before_scene
        _, after_house = read_house(session)
        assert after_house["objects"] == before_house["objects"]
        assert "drum_kit" not in json.dumps(after_house["objects"])
        assert "drum_kit" not in json.dumps(scene(session))
        assert "possession" not in json.dumps(junior["status"])
        assert junior["read_boundary"]["class_to_trait"] == "NOT_APPLIED"
        assert '"trait"' not in json.dumps(junior)
        assert junior["read_boundary"]["psyche_store"] == "NOT_READ"
        assert '"psyche"' not in json.dumps(junior)
        assert "social_class" not in json.dumps(junior)
    finally:
        owner.close()


def test_bound_world_value_changes_feasibility_and_restores(tmp_path):
    state = tmp_path / "state"
    run_cmd(state, "new")
    owner = open_owner(state)
    try:
        session = owner.base_owner.fanin.session
        baseline = read_dwelling(session)
        baseline_household = read_household(session)
        baseline_junior = material_feasibility(session, DRUM_KIT_REQUESTS["junior"])
        baseline_mother = mother_material_input(session, DRUM_KIT_REQUESTS["junior"])
        original_cash = session.world().actor_state["A"]["cash"]
        assert baseline_junior["status"] == "ADMISSIBLE"

        world = session.world()
        world.actor_state["A"]["cash"] = 30
        session.product._checkpoint(session.branch_id, world.clock, world)
        changed = read_dwelling(session)
        changed_household = read_household(session)
        changed_junior = material_feasibility(session, DRUM_KIT_REQUESTS["junior"])
        assert changed["source"] == baseline["source"]
        assert changed["home"] == baseline["home"]
        assert changed_household["source"] == baseline_household["source"]
        assert changed_household["material_hash"] != baseline_household["material_hash"]
        assert changed_junior["status"] == "REFUSED"
        assert changed_junior["reasons"] == ["REFUSED_AFFORDABILITY"]
        assert changed_junior["household"]["material_hash"] != (
            baseline_junior["household"]["material_hash"]
        )
        assert changed_junior["dwelling"]["source"] == baseline["source"]

        world = session.world()
        world.actor_state["A"]["cash"] = original_cash
        session.product._checkpoint(session.branch_id, world.clock, world)
        assert read_dwelling(session) == baseline
        assert read_household(session) == baseline_household
        assert material_feasibility(session, DRUM_KIT_REQUESTS["junior"]) == baseline_junior
        assert mother_material_input(session, DRUM_KIT_REQUESTS["junior"]) == baseline_mother
    finally:
        owner.close()


def test_committed_tenancy_space_unknown_and_restore(tmp_path):
    state = tmp_path / "state"
    run_cmd(state, "new")
    owner = open_owner(state)
    try:
        session = owner.base_owner.fanin.session
        baseline = read_dwelling(session)
        baseline_junior = material_feasibility(session, DRUM_KIT_REQUESTS["junior"])

        prohibited = facts_for(session)
        prohibited["home"]["tenancy"]["instrument_policy"] = "prohibited"
        assert commit_dwelling(session, facts=prohibited)["source"] != baseline["source"]
        refused = material_feasibility(session, DRUM_KIT_REQUESTS["junior"])
        assert refused["status"] == "REFUSED"
        assert refused["reasons"] == ["REFUSED_TENANCY"]

        unknown = facts_for(session)
        unknown["acoustics"]["max_indoor_loudness_db"] = "UNKNOWN"
        commit_dwelling(session, facts=unknown)
        held = material_feasibility(session, DRUM_KIT_REQUESTS["junior"])
        assert held["status"] == "UNKNOWN"
        assert held["unknowns"] == ["UNKNOWN_ACOUSTICS"]
        assert held["reasons"] == []

        tight = facts_for(session)
        tight["space"]["floor_area_m2"] = 1.0
        tight["space"]["clearance_m2"] = 1.0
        commit_dwelling(session, facts=tight)
        squeezed = material_feasibility(session, DRUM_KIT_REQUESTS["junior"])
        assert squeezed["status"] == "REFUSED"
        assert squeezed["reasons"] == ["REFUSED_SPACE"]

        restored = commit_dwelling(session, facts=facts_for(session))
        assert restored["source"] == baseline["source"]
        assert restored == baseline
        assert material_feasibility(session, DRUM_KIT_REQUESTS["junior"]) == baseline_junior
    finally:
        owner.close()


def test_dwelling_severance_restore_and_cold_reopen(tmp_path):
    state = tmp_path / "state"
    run_cmd(state, "new")
    owner = open_owner(state)
    try:
        session = owner.base_owner.fanin.session
        baseline_dwelling = read_dwelling(session)
        baseline_household = read_household(session)
        baseline_feasibility = material_feasibility(session, DRUM_KIT_REQUESTS["junior"])
        baseline_mother = mother_material_input(session, DRUM_KIT_REQUESTS["junior"])
        world = session.world()
        world.resources.pop(DWELLING_SLOT)
        session.product._checkpoint(session.branch_id, world.clock, world)
    finally:
        owner.close()

    owner = open_owner(state)
    try:
        session = owner.base_owner.fanin.session
        with pytest.raises(RecursionRefusal, match="P6_DWELLING_ABSENT"):
            read_dwelling(session)
        with pytest.raises(RecursionRefusal, match="P6_DWELLING_ABSENT"):
            material_feasibility(session, DRUM_KIT_REQUESTS["junior"])
        with pytest.raises(RecursionRefusal, match="P6_DWELLING_ABSENT"):
            mother_material_input(session, DRUM_KIT_REQUESTS["junior"])
        with pytest.raises(RecursionRefusal, match="P2_MATERIAL_FACT_ABSENT"):
            owner.base_owner.material_fact(DWELLING_SLOT)
        restored = establish_dwelling(session)
        assert restored == baseline_dwelling
        assert read_household(session) == baseline_household
        assert material_feasibility(session, DRUM_KIT_REQUESTS["junior"]) == baseline_feasibility
        assert mother_material_input(session, DRUM_KIT_REQUESTS["junior"]) == baseline_mother
        restored_counts = counts(session)
    finally:
        owner.close()

    script = (
        "import json, sys\n"
        "from pathlib import Path\n"
        "sys.path.insert(0, sys.argv[1])\n"
        "import run_p6\n"
        "from house import (read_household, read_dwelling, material_feasibility,\n"
        "                   mother_material_input, DRUM_KIT_REQUESTS, DWELLING_SLOT)\n"
        "state = Path(sys.argv[2])\n"
        "owner = run_p6.open_owner(state / 'actual-p2')\n"
        "try:\n"
        "    session = owner.base_owner.fanin.session\n"
        "    store = session.product.store\n"
        "    print(json.dumps({\n"
        "        'household': read_household(session),\n"
        "        'dwelling': read_dwelling(session),\n"
        "        'feasibility': material_feasibility(session, DRUM_KIT_REQUESTS['junior']),\n"
        "        'mother': mother_material_input(session, DRUM_KIT_REQUESTS['junior']),\n"
        "        'p2': owner.base_owner.material_fact(DWELLING_SLOT),\n"
        "        'counts': {\n"
        "            'episodes': len(store.episodes(session.branch_id)),\n"
        "            'checkpoints': len(store.checkpoints(session.branch_id)),\n"
        "            'world_events': len(store.world_events(session.branch_id)),\n"
        "            'perceptions': len(store.perceptions(session.branch_id)),\n"
        "        },\n"
        "    }, sort_keys=True))\n"
        "finally:\n"
        "    owner.close()\n"
    )
    cold = subprocess.run(
        [sys.executable, "-B", "-c", script, str(P6), str(state)],
        capture_output=True, text=True, timeout=120,
    )
    assert cold.returncode == 0, cold.stdout + cold.stderr
    reopened = json.loads(cold.stdout)
    assert reopened["household"] == baseline_household
    assert reopened["dwelling"] == baseline_dwelling
    assert reopened["feasibility"] == baseline_feasibility
    assert reopened["mother"] == baseline_mother
    assert reopened["p2"]["source"] == baseline_dwelling["source"]
    assert reopened["p2"]["slot"] == DWELLING_SLOT
    assert reopened["counts"] == restored_counts


def test_dwelling_extra_class_or_trait_is_refused(tmp_path):
    state = tmp_path / "state"
    run_cmd(state, "new")
    owner = open_owner(state)
    try:
        session = owner.base_owner.fanin.session
        social = facts_for(session)
        social["social_class"] = "poor"
        with pytest.raises(RecursionRefusal, match="P6_DWELLING_SCHEMA"):
            commit_dwelling(session, facts=social)
        trait = facts_for(session)
        trait["home"]["trait"] = "anxious"
        with pytest.raises(RecursionRefusal, match="P6_DWELLING_SCHEMA"):
            commit_dwelling(session, facts=trait)
        policy = facts_for(session)
        policy["home"]["tenancy"]["instrument_policy"] = "class_entitlement"
        with pytest.raises(RecursionRefusal, match="P6_DWELLING_TENANCY"):
            commit_dwelling(session, facts=policy)
        request = copy.deepcopy(DRUM_KIT_REQUESTS["junior"])
        request["trait"] = "anxious"
        with pytest.raises(RecursionRefusal, match="P6_DRUM_KIT_REQUEST_SCHEMA"):
            material_feasibility(session, request)
    finally:
        owner.close()


def test_fork_dwelling_feasibility_preserves_provenance(tmp_path):
    state = tmp_path / "state"
    run_cmd(state, "new")
    owner = open_owner(state)
    try:
        session = owner.base_owner.fanin.session
        parent_branch = session.branch_id
        parent_dwelling = read_dwelling(session)
        parent_junior = material_feasibility(session, DRUM_KIT_REQUESTS["junior"])
        session.fork_alt("child")
        before = counts(session)
        child_dwelling = read_dwelling(session)
        child_junior = material_feasibility(session, DRUM_KIT_REQUESTS["junior"])
        child_mother = mother_material_input(session, DRUM_KIT_REQUESTS["junior"])
        p2 = owner.base_owner.material_fact(DWELLING_SLOT)
        assert child_dwelling["branch"] == "child"
        assert child_dwelling["source"] == parent_dwelling["source"]
        assert child_dwelling["provenance"] == {
            "stored_branch": parent_branch,
            "current_branch": "child",
            "inherited": True,
            "scope": "P6_MATERIAL_FACT_ONLY",
            "fork_state": "C12_FORK_WITHOUT_S46_INTERVAL_STATE",
        }
        assert child_junior["dwelling"]["provenance"] == child_dwelling["provenance"]
        assert child_junior["household"]["provenance"]["inherited"] is True
        assert child_junior["status"] == parent_junior["status"]
        assert child_mother["dwelling"]["provenance"] == child_dwelling["provenance"]
        assert child_mother["parent_action"] is None
        assert p2["document"]["branch"] == parent_branch
        assert p2["state_scope"] == "C12_FORK_WITHOUT_S46_INTERVAL_STATE"
        assert counts(session) == before
    finally:
        owner.close()


def test_child_can_commit_its_own_dwelling_without_mutating_parent(tmp_path):
    state = tmp_path / "state"
    run_cmd(state, "new")
    owner = open_owner(state)
    try:
        session = owner.base_owner.fanin.session
        parent_branch = session.branch_id
        parent_dwelling = read_dwelling(session)
        session.fork_alt("child")
        child_facts = facts_for(session)
        child_facts["home"]["tenancy"]["instrument_policy"] = "prohibited"
        child = commit_dwelling(session, facts=child_facts)
        assert child["branch"] == "child"
        assert child["source"] != parent_dwelling["source"]
        assert child["provenance"] == {
            "stored_branch": "child",
            "current_branch": "child",
            "inherited": False,
            "scope": "P6_MATERIAL_FACT_ONLY",
            "fork_state": "CURRENT_BRANCH",
        }
        assert child["home"]["tenancy"]["instrument_policy"] == "prohibited"
        refused = material_feasibility(session, DRUM_KIT_REQUESTS["junior"])
        assert refused["status"] == "REFUSED"
        assert refused["reasons"] == ["REFUSED_TENANCY"]
        parent_document = session.product.store.latest_state(parent_branch)["world"]["resources"]
        assert parent_document[DWELLING_SLOT]["source"] == parent_dwelling["source"]
        assert parent_document[DWELLING_SLOT]["home"] == parent_dwelling["home"]
    finally:
        owner.close()


def test_b03_source_has_no_psyche_or_parent_writer():
    source = inspect.getsource(house)
    assert "PsycheStore(" not in source
    assert "p3.state_store" not in source
    assert "MATERIAL_FEASIBILITY_SCHEMA" in source
    assert "possession_created" in source
