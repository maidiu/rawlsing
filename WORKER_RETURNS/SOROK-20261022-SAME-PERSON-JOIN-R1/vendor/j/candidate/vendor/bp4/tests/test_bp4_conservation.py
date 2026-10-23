"""Conservation, actor identity, branch isolation and BP2 compatibility."""
from __future__ import annotations

import pytest

from bp4.bp2_compat import BP2Refusal, from_c10, native_slot_template, receiving_requirements, validate_envelope
from bp4.c10 import receive
from bp4.product import BP4Product
from bp4.store import StoreRefusal


def test_future_child_and_retroactive_episode_refused(tmp_path):
    p = BP4Product(tmp_path / "state")
    try:
        with pytest.raises(ValueError):
            p.store.append_episode("root", actor_id="A", kind="DO", clock=11,
                                   body={"future_child_outcome": "forged"})
        with pytest.raises(StoreRefusal) as err:
            p.store.append_episode("root", actor_id="A", kind="DO", clock=1, body={})
        assert err.value.code == "RETROACTIVE_EPISODE"
        with pytest.raises(StoreRefusal) as err:
            p.store.append_episode("root", actor_id="C", kind="DO", clock=11, body={})
        assert err.value.code == "ACTOR_NOT_IN_BRANCH"
    finally:
        p.close()


def test_no_actor_alias_and_shared_objective_identity(tmp_path):
    p = BP4Product(tmp_path / "state")
    try:
        public = p.seed.public()
        assert len(set(public["actor_a"] + public["actor_b"])) > 0
        assert public["actor_a"] != public["actor_b"]
        assert public["source_refs"][0] != public["source_refs"][1]
        assert public["snapshot_hashes"][0] != public["snapshot_hashes"][1]
        assert p.observe()["native_claims"]["actor"] is False
    finally:
        p.close()


def test_branch_isolation_after_fork(tmp_path):
    p = BP4Product(tmp_path / "state")
    try:
        p.fork("branch_x")
        p.use("branch_x")
        p.say("only in branch x")
        x_claims = [c["event_id"] for c in p.observe()["claims"]]
        p.use("root")
        root_claims = [c["event_id"] for c in p.observe()["claims"]]
        assert len(x_claims) == len(root_claims) + 1
        assert set(root_claims).issubset(set(x_claims))
        shared = p.store.shared_root_equal("branch_x", "root")
        assert shared["equal"] is True
    finally:
        p.close()


def test_c12_append_only_triggers(tmp_path):
    p = BP4Product(tmp_path / "state")
    try:
        with pytest.raises(Exception):
            p.store.db.execute("UPDATE checkpoint SET clock=1 WHERE branch_id='root'")
        p.say("trigger probe")
        with pytest.raises(Exception):
            p.store.db.execute("DELETE FROM episode WHERE branch_id='root'")
    finally:
        p.close()


def test_bp2_receiving_contract_is_typed_not_emitted(tmp_path):
    p = BP4Product(tmp_path / "state")
    try:
        c10 = receive(p.seed, p.store, "root", actor_id="A")
        envelope = from_c10(c10)
        checked = validate_envelope(envelope)
        assert checked["ok"] is True
        assert checked["status"] == "AWAITING_ACTUAL_BP2_PRODUCER__COMPAT_CONTRACT_NOT_EMITTED"
        bad = dict(envelope)
        del bad["c8_occurrence_refs"]
        with pytest.raises(BP2Refusal):
            validate_envelope(bad)
        self_granted = dict(envelope)
        self_granted["native_grants"] = {"actor": True}
        self_granted["authority_grades"] = {}
        with pytest.raises(BP2Refusal):
            validate_envelope(self_granted)
        slots = native_slot_template()
        assert all(v["status"] == "UNISSUED" for v in slots["slots"].values())
        assert receiving_requirements()["status"].startswith("AWAITING_ACTUAL_BP2")
    finally:
        p.close()
