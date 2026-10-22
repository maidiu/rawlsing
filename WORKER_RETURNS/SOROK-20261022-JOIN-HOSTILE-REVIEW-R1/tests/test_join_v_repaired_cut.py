"""Independent coverage added for JOIN-E cc0ff7d.

Covers the new targetless refusal adapter, refusal-path persistence/lineage,
the cc0ff7d import adaptation, and the authorized-fork/private/attention claims.
"""
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import pytest

from joined.refusal import RefusalSession
from joined.session import JoinedSession
from r30a.first_session import SessionRefusal
from support import CANDIDATE_ROOT


def _snapshot(root):
    root = Path(root)
    return {
        str(path.relative_to(root)): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in sorted(root.rglob("*"))
        if path.is_file()
    }


def _copy_refusal(root, target):
    source = Path(root)
    target = Path(target)
    shutil.copytree(source, target)
    meta = json.loads((target / "session.json").read_text())
    meta["product_root"] = str((target / "product").resolve())
    meta["state_root"] = str(target.resolve())
    (target / "session.json").write_text(
        json.dumps(meta, indent=2, sort_keys=True) + "\n"
    )
    return meta


def _open_refusal_or_error(root):
    try:
        return RefusalSession.open(root)
    except SessionRefusal as exc:
        return exc


def _refusal_episode_source(session):
    rows = [
        row for row in session.episodes()
        if row["kind"] == "GM01_REFUSAL"
    ]
    return rows[-1]["body"]["gm01_source"]


def test_e_first_import_adaptation_uses_j_closure(tmp_path):
    code = """
import json, sys
sys.path.insert(0, sys.argv[1])
sys.path.insert(0, sys.argv[1] + "/vendor/e")
from r31e.session import R31ESession
from joined.session import JoinedSession
from joined.closure import audit_loaded
s = JoinedSession.start(sys.argv[2], perform="omit")
try:
    audit = audit_loaded()
    print(json.dumps({
        "accepted": s.do_help()["accepted"],
        "verify": s.verify()["ok"],
        "closure": audit["ok"],
        "origins": {row["module"]: row["actual_closure"]
                    for row in audit["rows"]
                    if row["module"] in {"bp4", "bp2p4", "r29p.product",
                                         "r30a.first_session", "r31e.session"}},
    }, sort_keys=True))
finally:
    s.close()
"""
    env = {
        **os.environ,
        "PYTHONPATH": str(CANDIDATE_ROOT),
        "PYTHONDONTWRITEBYTECODE": "1",
    }
    run = subprocess.run(
        [sys.executable, "-B", "-c", code, str(CANDIDATE_ROOT), str(tmp_path / "e_first")],
        env=env,
        text=True,
        capture_output=True,
        timeout=120,
    )
    assert run.returncode == 0, run.stderr
    observed = json.loads(run.stdout)
    assert observed["accepted"] is True
    assert observed["verify"] is True
    assert observed["closure"] is True
    assert observed["origins"]["bp4"] == "J"
    assert observed["origins"]["bp2p4"] == "J"
    assert observed["origins"]["r30a.first_session"] == "E"
    assert observed["origins"]["r31e.session"] == "E"


def test_refusal_actual_b_source_no_target_and_same_consumer(tmp_path):
    share = JoinedSession.start(tmp_path / "share", perform="omit")
    refusal = RefusalSession.start(tmp_path / "refusal")
    try:
        share_source = share.product.source
        refusal_source = refusal.product.source
        assert share_source["b_operation"] == "SHARE_TOOL"
        assert refusal_source["b_operation"] == "REFUSE_TOOL"
        assert refusal_source["b_performed"] is True
        assert refusal_source["a_e2_performed"] is False
        assert refusal_source["material_feasible_after"] is False
        assert refusal.world().actor_state["A"]["tools_remaining"] == 0
        assert share.world().actor_state["A"]["tools_remaining"] == 1
        assert refusal.world().actor_state["A"]["material_remaining"] == 4
        assert refusal.world().actor_state["A"]["completed_units"] == 4
        assert refusal.world().actor_state["A"]["free_hours"] == 12
        assert not any(event.get("kind") == "INSPECT" for event in refusal.events())

        episodes = refusal.episodes()
        assert len([row for row in episodes if row["kind"] == "GM01_REFUSAL"]) == 1
        assert not any(row["kind"] == "GM01_SOURCE" for row in episodes)
        c9 = refusal.meta["c9"]
        assert c9["target_branch"] == "NO_CHANGE"
        assert c9["target_reason"] == "NO_PROPOSAL"
        assert c9["target_id"] == ""
        assert c9["material_reason"] == "NO_ELIGIBLE_MATERIAL_SOURCE"
        assert c9["response_status"] == "RESPONSE_EFFECTS_VALID_EMPTY"
        assert c9["later_read_status"] == "STATE_ABSENT"
        assert refusal.meta["j_c8_state_digest"] == c9["c8_state_digest"]
        assert refusal.meta["j_e1_event_hash"] == c9["event_hash"]
        assert refusal.meta["target_id"] == ""
        assert refusal.status()["targetless"] is True
        assert refusal.status()["target_id"] == ""
        assert refusal.verify()["targetless"] is True
        assert refusal.verify()["ok"] is True
        assert all(
            value is False
            for value in refusal.product.seed.custody()["native_grants"].values()
        )

        refused = refusal.do_help()
        accepted = share.do_help()
        assert refused["accepted"] is False
        assert refused["strategy"] == "HELP_REFUSE"
        assert refused["admission"]["schema"] == "R31E_EXPRESSION_ADMISSION@1"
        assert refused["admission"]["target_id"] == ""
        assert refused["admission"]["action_event_id"] == ""
        assert accepted["accepted"] is True
        assert accepted["strategy"] == "HELP_ACCEPT"
        assert accepted["admission"]["schema"] == "R31E_EXPRESSION_ADMISSION@1"
        assert refusal.verify()["ok"] is True
        assert share.verify()["ok"] is True
    finally:
        share.close()
        refusal.close()


def test_refusal_cold_open_targetless_nonmutating(tmp_path):
    state = tmp_path / "refusal_cold"
    session = RefusalSession.start(state)
    source = session.product.source
    before = _snapshot(state)
    before_counts = session.verify()["counts"]
    session.close()

    cold = RefusalSession.open(state)
    try:
        assert cold.product.source == source
        assert cold.world().actor_state["A"]["tools_remaining"] == 0
        assert cold.world().actor_state["A"]["material_remaining"] == 4
        assert cold.status()["targetless"] is True
        assert cold.status()["target_id"] == ""
        assert cold.verify()["ok"] is True
        assert cold.verify()["targetless"] is True
        assert cold.verify()["counts"] == before_counts
        assert _snapshot(state) == before
        assert cold.do_help()["accepted"] is False
    finally:
        cold.close()

    code = """
import json, sys
from joined.refusal import RefusalSession
s = RefusalSession.open(sys.argv[1])
try:
    print(json.dumps({"source": s.product.source, "tools": s.world().actor_state["A"]["tools_remaining"],
                      "targetless": s.status()["targetless"], "verify": s.verify()["ok"],
                      "accepted": s.do_help()["accepted"]}, sort_keys=True))
finally:
    s.close()
"""
    env = {
        **os.environ,
        "PYTHONPATH": str(CANDIDATE_ROOT),
        "PYTHONDONTWRITEBYTECODE": "1",
    }
    run = subprocess.run(
        [sys.executable, "-B", "-c", code, str(state)],
        env=env,
        text=True,
        capture_output=True,
        timeout=120,
    )
    assert run.returncode == 0, run.stderr
    observed = json.loads(run.stdout)
    assert observed["source"] == source
    assert observed["tools"] == 0
    assert observed["targetless"] is True
    assert observed["verify"] is True
    assert observed["accepted"] is False


def test_refusal_coordinated_meta_sidecar_source_tamper_refused_or_c12_bound(tmp_path):
    state = tmp_path / "refusal_tamper"
    session = RefusalSession.start(state)
    session.close()
    copy = tmp_path / "copy"
    meta = _copy_refusal(state, copy)
    sidecar_path = copy / "product" / "refusal.json"
    sidecar = json.loads(sidecar_path.read_text())
    foreign = dict(meta["j_source"])
    foreign["b_actor"] = "FOREIGN_B"
    foreign["b_to_actor"] = "FOREIGN_A"
    foreign["b_event_hash"] = "FOREIGN_HASH"
    meta["j_source"] = foreign
    meta["j_c8_state_digest"] = "FOREIGN_C8"
    meta["j_e1_event_hash"] = "FOREIGN_E1"
    sidecar["j_source"] = foreign
    (copy / "session.json").write_text(
        json.dumps(meta, indent=2, sort_keys=True) + "\n"
    )
    sidecar_path.write_text(json.dumps(sidecar, indent=2, sort_keys=True) + "\n")

    opened = _open_refusal_or_error(copy)
    if isinstance(opened, SessionRefusal):
        return
    try:
        episode = _refusal_episode_source(opened)
        if opened.product.source == episode:
            return
        pytest.fail(json.dumps({
            "case": "refusal_coordinated_source_tamper",
            "opened": True,
            "meta_matches_sidecar": opened.product.source == opened.meta.get("j_source"),
            "loaded_b_actor": opened.product.source.get("b_actor"),
            "loaded_b_to_actor": opened.product.source.get("b_to_actor"),
            "loaded_b_event_hash": opened.product.source.get("b_event_hash"),
            "episode_b_actor": episode.get("b_actor"),
            "episode_b_to_actor": episode.get("b_to_actor"),
            "episode_b_event_hash": episode.get("b_event_hash"),
            "verify": opened.verify().get("ok"),
            "targetless": opened.status().get("targetless"),
        }, sort_keys=True))
    finally:
        opened.close()


def test_refusal_metadata_only_branch_substitution_refused(tmp_path):
    state = tmp_path / "refusal_branch"
    session = RefusalSession.start(state)
    session.close()
    copy = tmp_path / "copy"
    meta = _copy_refusal(state, copy)
    meta["branch_id"] = "root"
    (copy / "session.json").write_text(
        json.dumps(meta, indent=2, sort_keys=True) + "\n"
    )
    opened = _open_refusal_or_error(copy)
    if isinstance(opened, SessionRefusal):
        return
    try:
        pytest.fail(json.dumps({
            "case": "refusal_metadata_branch",
            "opened": True,
            "branch_id": opened.branch_id,
            "recorded_branch_id": "first_session",
            "verify": opened.verify().get("ok"),
        }, sort_keys=True))
    finally:
        opened.close()


def test_refusal_fork_continuation_or_typed_refusal(tmp_path):
    state = tmp_path / "refusal_fork"
    session = RefusalSession.start(state)
    try:
        try:
            forked = session.fork_alt()
        except SessionRefusal:
            return
        if forked.get("status") != "OK":
            pytest.fail(f"refusal fork returned non-OK result: {forked!r}")
        assert session.branch_id == "alt"
        assert session.meta["branch_id"] == "alt"
        assert session.meta.get("branch_lineage")
        assert session.verify()["ok"] is True
    finally:
        session.close()
    cold = RefusalSession.open(state)
    try:
        assert cold.branch_id == "alt"
        assert cold.verify()["ok"] is True
    finally:
        cold.close()


def test_refusal_receiving_edge_fault_restore_is_bounded(tmp_path):
    session = RefusalSession.start(tmp_path / "refusal_fault")
    try:
        assert session.world().actor_state["A"]["tools_remaining"] == 0
        assert session.do_help()["accepted"] is False
        world = session.world()
        world.actor_state["A"]["tools_remaining"] = 1
        world.resources["workshop"]["tool_available"] = True
        session.product._checkpoint(session.branch_id, world.clock, world)
        faulted = session.do_help()
        assert faulted["accepted"] is True
        assert faulted["strategy"] == "HELP_ACCEPT"
        assert session.product.source["b_operation"] == "REFUSE_TOOL"
        assert session.verify()["ok"] is True
        assert session.status()["targetless"] is True
    finally:
        session.close()

    restored = RefusalSession.start(tmp_path / "refusal_restore")
    try:
        assert restored.world().actor_state["A"]["tools_remaining"] == 0
        assert restored.do_help()["accepted"] is False
    finally:
        restored.close()


def test_refusal_attention_private_and_actor_ignorance(tmp_path):
    session = RefusalSession.start(tmp_path / "refusal_expr")
    try:
        said = session.say("Hello. I just moved in.")
        event_ids = [
            said["user_event"]["event_id"],
            said["admission"]["speech_event_id"],
        ]
        session.meta["attention"] = "focused"
        focused = session._surface(event_ids)
        session.meta["attention"] = "distracted"
        distracted = session._surface(event_ids)
        assert focused != distracted
        assert [
            row["event_id"] for row in session.events()
            if row["event_id"] in event_ids
        ] == event_ids

        private = session.say("How much cash do you have?")
        assert private["strategy"] == "PRIVATE_BOUNDARY"
        assert "cash" not in private["candidate"]["speech"].lower()
        assert private["admission"]["validation"]["checks"]["no_private_tokens"] is True

        assert session.wait(30)["scene_open"] is False
        assert session.return_session()["scene_open"] is True
        unknown = session.say("What did the finisher do?")
        assert unknown["strategy"] == "UNKNOWN_B"
        assert "took the pieces" not in unknown["candidate"]["speech"].lower()
        assert session.do_help()["accepted"] is False
        assert session.verify()["ok"] is True
    finally:
        session.close()


def test_refusal_typed_missing_orphan_moved_and_donor(tmp_path):
    with pytest.raises(SessionRefusal) as exc:
        RefusalSession.open(tmp_path / "missing")
    assert exc.value.code == "SESSION_NOT_FOUND"

    orphan = tmp_path / "orphan"
    session = RefusalSession.start(orphan)
    session.close()
    (orphan / "session.json").unlink()
    with pytest.raises(SessionRefusal) as exc:
        RefusalSession.start(orphan)
    assert exc.value.code == "ORPHAN_PRODUCT_ROOT"

    moved = tmp_path / "moved"
    session = RefusalSession.start(moved)
    session.close()
    relocated = tmp_path / "relocated"
    moved.rename(relocated)
    with pytest.raises(SessionRefusal) as exc:
        RefusalSession.open(relocated)
    assert exc.value.code in {"FOREIGN_PRODUCT_ROOT", "SESSION_ROOT_MOVED"}

    state = tmp_path / "donor_state"
    session = RefusalSession.start(state)
    session.close()
    copy = tmp_path / "donor_copy"
    meta = _copy_refusal(state, copy)
    donor = tmp_path / "donor_product"
    shutil.copytree(copy / "product", donor)
    meta["product_root"] = str(donor.resolve())
    (copy / "session.json").write_text(
        json.dumps(meta, indent=2, sort_keys=True) + "\n"
    )
    with pytest.raises(SessionRefusal) as exc:
        RefusalSession.open(copy)
    assert exc.value.code == "FOREIGN_PRODUCT_ROOT"
