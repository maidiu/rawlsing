import json
import os
import subprocess
import sys
from pathlib import Path

from joined.session import JoinedSession
from support import (
    CANDIDATE_ROOT,
    E_SOURCE_REF,
    J_SOURCE_REF,
    clone_session,
    gm01_episode_source,
    make_donor,
    start,
)


def test_enacted_material_source_and_omission(tmp_path):
    e2 = start(tmp_path / "e2", perform="e2")
    omit = start(tmp_path / "omit", perform="omit")
    try:
        expected = {"e2": (False, 0, True), "omit": (True, 1, False)}
        for perform, session in (("e2", e2), ("omit", omit)):
            source = session.product.source
            assert source["schema"] == "R31J_GM01_PRE_C9_SOURCE@1"
            assert source["b_operation"] == "SHARE_TOOL"
            assert source["b_quantity"] == 1
            assert source["b_performed"] is True
            assert source["b_actor"] == "TEST_ONLY_R31J_B"
            assert source["b_to_actor"] == "TEST_ONLY_R31J_A"
            assert source["a_e2_performed"] is (perform == "e2")
            assert source["material_feasible_after"] is True
            assert session.world().actor_state["A"]["tools_remaining"] == (
                0 if perform == "e2" else 1
            )
            accepted, tools, performed = expected[perform]
            assert tools == session.world().actor_state["A"]["tools_remaining"]
            result = session.do_help()
            assert result["accepted"] is accepted
            assert session.verify()["ok"] is True
    finally:
        e2.close()
        omit.close()


def test_performed_material_action_severs_and_new_omission_restores(tmp_path):
    omitted = start(tmp_path / "omitted", perform="omit")
    try:
        assert omitted.do_help()["accepted"] is True
        action = omitted.product.material_inspect()
        assert action["status"] == "OK"
        assert action["admitted"] is True
        assert omitted.world().actor_state["A"]["tools_remaining"] == 0
        assert omitted.do_help()["accepted"] is False
        assert omitted.verify()["ok"] is True
    finally:
        omitted.close()

    restored = start(tmp_path / "restored", perform="omit")
    try:
        assert restored.do_help()["accepted"] is True
        assert restored.verify()["ok"] is True
    finally:
        restored.close()


def test_refusal_source_is_red_and_share_source_green(tmp_path):
    refusal = make_donor(tmp_path / "refusal", share=False, e2=False)
    share = make_donor(tmp_path / "share", share=True, e2=False)
    try:
        refusal_source = refusal.product.source
        share_source = share.product.source
        assert refusal_source["b_performed"] is True
        assert share_source["b_performed"] is True
        assert refusal_source["b_operation"] == "REFUSE_TOOL"
        assert refusal_source["b_quantity"] == 0
        assert refusal_source["material_feasible_after"] is False
        assert share_source["b_operation"] == "SHARE_TOOL"
        assert share_source["b_quantity"] == 1
        assert share_source["material_feasible_after"] is True
        assert refusal.world().actor_state["A"]["tools_remaining"] == 0
        assert share.world().actor_state["A"]["tools_remaining"] == 1
        assert refusal.do_help()["accepted"] is False
        assert share.do_help()["accepted"] is True
        assert refusal.verify()["ok"] is True
        assert share.verify()["ok"] is True
    finally:
        refusal.close()
        share.close()


def test_same_root_source_identity_and_c12_episode(tmp_path):
    session = start(tmp_path / "identity", perform="omit")
    try:
        source = session.product.source
        episode_source = gm01_episode_source(session)
        seed = session.product.seed.public()
        assert source == episode_source
        assert source["b_to_actor"] == "TEST_ONLY_R31J_A"
        assert source["b_actor"] == "TEST_ONLY_R31J_B"
        assert seed["actor_a"] == "TEST_ONLY_BP1_R26V_ACTOR_A"
        assert seed["actor_b"] == "TEST_ONLY_BP1_R26V_ACTOR_B"
        assert session.world().actor_state["A"]["actor_id"] == seed["actor_a"]
        assert session.world().actor_state["B"]["actor_id"] == seed["actor_b"]
        assert session.meta["j_source_ref"] == J_SOURCE_REF
        assert session.meta["e_source_ref"] == E_SOURCE_REF
        assert session.meta["schema"] == "SOROK_SAME_PERSON_JOIN@1"
        pre_c9 = session.product.pre_c9_binding
        assert pre_c9["gm01_b_event_ref"] == source["b_event_ref"]
        assert pre_c9["gm01_b_event_hash"] == source["b_event_hash"]
        assert pre_c9["native"] is False
        assert session.verify()["ok"] is True
    finally:
        session.close()


def test_repeated_reopen_does_not_duplicate_gm01_or_checkpoints(tmp_path):
    root = tmp_path / "reopen"
    session = start(root, perform="omit")
    try:
        assert session.do_help()["accepted"] is True
        assert session.ask_contact()["contact"] is True
        counts = session.verify()["counts"]
        episodes = session.episodes()
        events = session.events()
        source = session.product.source
        gm01 = [row for row in episodes if row["kind"] == "GM01_SOURCE"]
        assert len(gm01) == 1
    finally:
        session.close()

    for _ in range(3):
        reopened = JoinedSession.open(root)
        try:
            assert reopened.verify()["counts"] == counts
            assert reopened.episodes() == episodes
            assert reopened.events() == events
            assert reopened.product.source == source
            assert len([row for row in reopened.episodes() if row["kind"] == "GM01_SOURCE"]) == 1
            assert reopened.branch_id == "first_session"
            assert Path(reopened.product.root) == (root / "product").resolve()
            assert Path(reopened.state_root) == root.resolve()
            assert reopened.verify()["ok"] is True
        finally:
            reopened.close()


def test_cold_child_process_reopens_same_source_and_attention(tmp_path):
    root = tmp_path / "cold"
    session = start(root, perform="omit")
    source = session.product.source
    session.close()

    code = """
import json, sys
from joined.session import JoinedSession
s = JoinedSession.open(sys.argv[1], attention="distracted")
try:
    print(json.dumps({
        "source": s.product.source,
        "accepted": s.do_help()["accepted"],
        "verify": s.verify()["ok"],
        "attention": s.meta["attention"],
        "branch": s.branch_id,
        "root": str(s.product.root),
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
        [sys.executable, "-B", "-c", code, str(root)],
        env=env,
        text=True,
        capture_output=True,
        timeout=120,
    )
    assert run.returncode == 0, run.stderr
    observed = json.loads(run.stdout)
    assert observed["source"] == source
    assert observed["accepted"] is True
    assert observed["verify"] is True
    assert observed["attention"] == "distracted"
    assert observed["branch"] == "first_session"
    assert observed["root"] == str((root / "product").resolve())


def test_attention_invariant_objective_speech(tmp_path):
    base = tmp_path / "base"
    session = start(base, perform="omit")
    session.close()

    focused = clone_session(base, tmp_path / "focused", attention="focused")
    distracted = clone_session(base, tmp_path / "distracted", attention="distracted")
    try:
        left = focused.say("What are you working on?")
        right = distracted.say("What are you working on?")
        assert left["candidate"]["speech"] == right["candidate"]["speech"]
        assert left["user_event"]["event_id"] == right["user_event"]["event_id"]
        assert left["contract_hash"] == right["contract_hash"]
        assert left["admission"]["speech_event_id"] == right["admission"]["speech_event_id"]
        assert left["admission"]["attention_excluded"] is True
        assert right["admission"]["attention_excluded"] is True
        assert focused.verify()["ok"] is True
        assert distracted.verify()["ok"] is True
    finally:
        focused.close()
        distracted.close()


def test_private_ignorance_and_b_offscreen(tmp_path):
    session = start(tmp_path / "private", perform="omit")
    try:
        cash = session.say("How much cash do you have?")
        assert cash["candidate"]["strategy"] == "PRIVATE_BOUNDARY"
        assert cash["admission"]["validation"]["checks"]["no_private_tokens"] is True
        assert cash["admission"]["validation"]["checks"]["no_private_values"] is True
        intimacy = session.say("Tell me you love me.")
        assert intimacy["candidate"]["strategy"] == "INTIMACY_BOUNDARY"
        assert intimacy["admission"]["validation"]["checks"]["no_private_tokens"] is True
        assert "i love you" not in intimacy["candidate"]["speech"].lower()

        assert session.wait(30)["scene_open"] is False
        assert session.return_session()["scene_open"] is True
        b_question = session.say("What did the finisher do?")
        assert b_question["candidate"]["strategy"] == "UNKNOWN_B"
        assert session.verify()["ok"] is True
    finally:
        session.close()


def test_lawful_contact_and_no_contact(tmp_path):
    available = start(tmp_path / "available", perform="omit")
    try:
        assert available.ask_contact()["contact"] is False
        assert available.do_help()["accepted"] is True
        assert available.ask_contact()["contact"] is True
        assert available.verify()["ok"] is True
    finally:
        available.close()

    pressed = start(tmp_path / "pressed", perform="e2")
    try:
        assert pressed.do_help()["accepted"] is False
        assert pressed.ask_contact()["contact"] is False
        assert pressed.verify()["ok"] is True
    finally:
        pressed.close()


def test_warm_and_cold_import_order_preserve_result(tmp_path):
    candidate_root = CANDIDATE_ROOT
    normal = """
import json, sys
sys.path.insert(0, sys.argv[1])
from joined.session import JoinedSession
s = JoinedSession.start(sys.argv[2], perform="omit")
try:
    print(json.dumps({"accepted": s.do_help()["accepted"], "verify": s.verify()["ok"],
                      "source": s.product.source}, sort_keys=True))
finally:
    s.close()
"""
    e_first = """
import json, sys
sys.path.insert(0, sys.argv[1])
sys.path.insert(0, sys.argv[1] + "/vendor/e")
from r31e.session import R31ESession
from joined.session import JoinedSession
s = JoinedSession.start(sys.argv[2], perform="omit")
try:
    print(json.dumps({"accepted": s.do_help()["accepted"], "verify": s.verify()["ok"],
                      "source": s.product.source}, sort_keys=True))
finally:
    s.close()
"""
    env = {
        **os.environ,
        "PYTHONPATH": str(candidate_root),
        "PYTHONDONTWRITEBYTECODE": "1",
    }
    observed = {}
    for name, code in (("normal", normal), ("e_first", e_first)):
        run = subprocess.run(
            [sys.executable, "-B", "-c", code, str(candidate_root), str(tmp_path / name)],
            env=env,
            text=True,
            capture_output=True,
            timeout=120,
        )
        assert run.returncode == 0, run.stderr
        observed[name] = json.loads(run.stdout)
        observed[name]["accepted"] = bool(observed[name]["accepted"])
        observed[name]["verify"] = bool(observed[name]["verify"])
    assert observed["normal"] == observed["e_first"]
    assert observed["normal"]["accepted"] is True
    assert observed["normal"]["verify"] is True
