"""JOIN-V targeted attacks added after JOIN-E's c367777 repair.

These are new tests. The original frozen test files remain untouched.
"""
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

from joined.session import JoinedSession
from support import (
    CANDIDATE_ROOT,
    SessionRefusal,
    gm01_episode_source,
    make_donor,
    read_meta,
    start,
    write_meta,
)


def _open_or_refusal(root):
    try:
        return JoinedSession.open(root)
    except (SessionRefusal, ValueError) as exc:
        return exc


def test_lawful_fork_alt_continuation_is_supported(tmp_path):
    state = tmp_path / "lawful_fork"
    session = start(state, perform="omit")
    try:
        forked = session.fork_alt("alt")
        assert forked["status"] == "OK"
        assert session.branch_id == "alt"
        assert session.meta["branch_id"] == "alt"
        said = session.say("Hello. I came back to the bench.")
        assert said["status"] == "OK"
        assert session.product.store.verify("first_session")["ok"] is True
        assert session.product.store.verify("alt")["ok"] is True
        assert session.product.store.shared_root_equal("first_session", "alt")["equal"] is True
        assert len(session.product.store.episodes("alt")) > len(
            session.product.store.episodes("first_session")
        )
        assert session.verify()["ok"] is True
    finally:
        session.close()

    cold = JoinedSession.open(state)
    try:
        assert cold.branch_id == "alt"
        assert cold.verify()["ok"] is True
        assert cold.say("Back at the bench.")["status"] == "OK"
        assert cold.verify()["ok"] is True
    finally:
        cold.close()


def test_metadata_only_branch_substitution_to_root_is_refused(tmp_path):
    state = tmp_path / "branch_root"
    session = start(state, perform="omit")
    session.fork_alt("alt")
    session.close()

    meta = read_meta(state)
    assert meta["branch_id"] == "alt"
    meta["branch_id"] = "root"
    write_meta(state, meta)

    opened = _open_or_refusal(state)
    if isinstance(opened, (SessionRefusal, ValueError)):
        return
    try:
        pytest.fail(json.dumps({
            "case": "metadata_only_branch_root",
            "opened": True,
            "branch_id": opened.branch_id,
            "verify": opened.verify().get("ok"),
            "root_branch_id": opened.meta.get("root_branch_id"),
        }, sort_keys=True))
    finally:
        opened.close()


def test_foreign_product_root_with_same_source_is_refused(tmp_path):
    state = tmp_path / "root_source"
    session = start(state, perform="omit")
    session.close()

    donor = tmp_path / "donor"
    donor.mkdir()
    shutil.copytree(state / "product", donor / "product")
    meta = read_meta(state)
    meta["product_root"] = str((donor / "product").resolve())
    write_meta(state, meta)

    opened = _open_or_refusal(state)
    if isinstance(opened, (SessionRefusal, ValueError)):
        return
    try:
        pytest.fail(json.dumps({
            "case": "same_source_foreign_root",
            "opened": True,
            "product_root": str(opened.product.root),
            "state_root": str(state.resolve()),
            "canonical_product_root": str((state / "product").resolve()),
            "source_equal": opened.product.source == opened.meta.get("j_source"),
            "verify": opened.verify().get("ok"),
        }, sort_keys=True))
    finally:
        opened.close()


def test_double_sidecar_and_meta_source_tamper_is_refused_or_c12_bound(tmp_path):
    state = tmp_path / "double_source"
    session = start(state, perform="omit")
    session.close()

    meta = read_meta(state)
    binding_path = state / "product" / "bp2_join.json"
    binding = json.loads(binding_path.read_text())
    foreign = dict(meta["j_source"])
    foreign["b_operation"] = "REFUSE_TOOL"
    foreign["b_quantity"] = 0
    foreign["b_to_actor"] = "TEST_ONLY_FOREIGN_ACTOR_A"
    foreign["b_actor"] = "TEST_ONLY_FOREIGN_ACTOR_B"
    meta["j_source"] = foreign
    binding["r31j_source"] = foreign
    write_meta(state, meta)
    binding_path.write_text(json.dumps(binding, indent=2, sort_keys=True) + "\n")

    opened = _open_or_refusal(state)
    if isinstance(opened, (SessionRefusal, ValueError)):
        return
    try:
        episode = gm01_episode_source(opened)
        if opened.product.source == episode:
            return
        pytest.fail(json.dumps({
            "case": "double_source_tamper",
            "opened": True,
            "meta_equal_sidecar": opened.product.source == opened.meta.get("j_source"),
            "loaded_b_operation": opened.product.source.get("b_operation"),
            "loaded_b_quantity": opened.product.source.get("b_quantity"),
            "episode_b_operation": episode.get("b_operation"),
            "episode_b_quantity": episode.get("b_quantity"),
            "verify": opened.verify().get("ok"),
            "accepted": opened.do_help().get("accepted"),
        }, sort_keys=True))
    finally:
        opened.close()


def test_b_refusal_and_b_share_with_same_a_omission(tmp_path):
    refusal = make_donor(tmp_path / "b_refusal", share=False, e2=False)
    share = make_donor(tmp_path / "b_share", share=True, e2=False)
    restored = make_donor(tmp_path / "b_restored", share=True, e2=False)
    try:
        assert refusal.product.source["b_operation"] == "REFUSE_TOOL"
        assert refusal.product.source["b_performed"] is True
        assert refusal.product.source["material_feasible_after"] is False
        assert share.product.source["b_operation"] == "SHARE_TOOL"
        assert share.product.source["b_quantity"] == 1
        assert share.product.source["material_feasible_after"] is True
        assert refusal.product.source["a_e2_performed"] is False
        assert share.product.source["a_e2_performed"] is False
        assert refusal.world().actor_state["A"]["tools_remaining"] == 0
        assert share.world().actor_state["A"]["tools_remaining"] == 1
        assert refusal.do_help()["accepted"] is False
        assert share.do_help()["accepted"] is True
        assert restored.do_help()["accepted"] is True
        assert refusal.verify()["ok"] is True
        assert share.verify()["ok"] is True
        assert restored.verify()["ok"] is True
    finally:
        refusal.close()
        share.close()
        restored.close()

    probe = JoinedSession.probe_refusal(tmp_path / "b_probe")
    assert probe["source"]["b_operation"] == "REFUSE_TOOL"
    assert probe["source"]["b_performed"] is True
    assert probe["target_id"] == ""
    assert probe["c9"]["target_branch"] == "NO_CHANGE"
    assert probe["c9"]["target_reason"] == "NO_PROPOSAL"


def test_import_closure_refuses_e_first_and_accepts_j_first(tmp_path):
    normal = """
import json, sys
sys.path.insert(0, sys.argv[1])
from joined.session import JoinedSession
s = JoinedSession.start(sys.argv[2], perform="omit")
try:
    print(json.dumps({"accepted": s.do_help()["accepted"], "verify": s.verify()["ok"]}))
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
print(json.dumps({"accepted": s.do_help()["accepted"], "verify": s.verify()["ok"]}))
"""
    env = {
        **os.environ,
        "PYTHONPATH": str(CANDIDATE_ROOT),
        "PYTHONDONTWRITEBYTECODE": "1",
    }
    accepted = subprocess.run(
        [sys.executable, "-B", "-c", normal, str(CANDIDATE_ROOT), str(tmp_path / "normal")],
        env=env, text=True, capture_output=True, timeout=120,
    )
    assert accepted.returncode == 0, accepted.stderr
    result = json.loads(accepted.stdout)
    assert result == {"accepted": True, "verify": True}

    refused = subprocess.run(
        [sys.executable, "-B", "-c", e_first, str(CANDIDATE_ROOT), str(tmp_path / "e_first")],
        env=env, text=True, capture_output=True, timeout=120,
    )
    assert refused.returncode != 0
    assert "IMPORT_CLOSURE_INVALID" in refused.stderr
    assert "WRONG_CLOSURE" in refused.stderr
