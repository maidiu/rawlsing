import json
import shutil
from pathlib import Path

import pytest

from joined.session import JoinedSession
from support import (
    SessionRefusal,
    gm01_episode_source,
    r29p_donor,
    read_meta,
    start,
    write_meta,
)


def _open_or_fail(root, *, expected="refuse"):
    try:
        return JoinedSession.open(root)
    except (SessionRefusal, ValueError):
        return None
    except Exception as exc:
        pytest.fail(
            f"expected {expected}, got raw {type(exc).__name__}: {exc}"
        )


def test_different_product_root_is_refused(tmp_path):
    root_a = tmp_path / "a"
    root_b = tmp_path / "b"
    left = start(root_a, perform="omit")
    right = start(root_b, perform="e2")
    left.close()
    right.close()

    meta = read_meta(root_a)
    meta["product_root"] = str((root_b / "product").resolve())
    write_meta(root_a, meta)

    session = _open_or_fail(root_a, expected="refusal of a foreign product root")
    if session is None:
        return
    try:
        pytest.fail(json.dumps({
            "case": "different_product_root",
            "opened": True,
            "product_root": str(session.product.root),
            "session_root": str(root_a.resolve()),
            "expected_product_root": str((root_a / "product").resolve()),
            "meta_material_performance": session.meta.get("material_performance"),
            "source_a_e2_performed": session.product.source.get("a_e2_performed"),
            "source_b_operation": session.product.source.get("b_operation"),
            "tools": session.world().actor_state["A"].get("tools_remaining"),
            "verify": session.verify().get("ok"),
            "accepted": session.do_help().get("accepted"),
        }, sort_keys=True))
    finally:
        session.close()


def test_r29p_product_root_is_refused_without_mutating_donor(tmp_path):
    donor_product_root = r29p_donor(tmp_path / "r29p")
    donor_binding = donor_product_root / "bp2_join.json"
    before = donor_binding.read_bytes()

    root_a = tmp_path / "joint"
    session = start(root_a, perform="omit")
    session.close()
    meta = read_meta(root_a)
    meta["product_root"] = str(donor_product_root.resolve())
    meta["branch_id"] = "first_session"
    write_meta(root_a, meta)

    opened = None
    try:
        try:
            opened = JoinedSession.open(root_a)
        except (SessionRefusal, ValueError):
            after = donor_binding.read_bytes()
            assert after == before, "refusal path mutated the R29P donor binding"
            return
        except Exception as exc:
            pytest.fail(
                f"expected refusal of R29P product root, got raw "
                f"{type(exc).__name__}: {exc}"
            )
        after = donor_binding.read_bytes()
        pytest.fail(json.dumps({
            "case": "r29p_product_root",
            "opened": True,
            "source": opened.product.source,
            "pre_c9_binding": getattr(opened.product, "pre_c9_binding", None),
            "verify": opened.verify().get("ok"),
            "accepted": opened.do_help().get("accepted"),
            "donor_binding_mutated": after != before,
            "donor_r31j_keys": sorted(
                k for k in json.loads(after).keys() if k.startswith("r31j")
            ),
        }, sort_keys=True))
    finally:
        if opened is not None:
            opened.close()


def test_tampered_branch_id_is_refused(tmp_path):
    root = tmp_path / "branch"
    session = start(root, perform="omit")
    fork = session.product.fork("alt")
    assert fork["status"] == "OK"
    session.close()

    meta = read_meta(root)
    meta["branch_id"] = "alt"
    write_meta(root, meta)

    opened = _open_or_fail(root, expected="refusal of a non-recorded branch")
    if opened is None:
        return
    try:
        pytest.fail(json.dumps({
            "case": "tampered_branch_id",
            "opened": True,
            "branch_id": opened.branch_id,
            "recorded_branch_id": "first_session",
            "verify": opened.verify().get("ok"),
            "accepted": opened.do_help().get("accepted"),
        }, sort_keys=True))
    finally:
        opened.close()


def test_tampered_r31j_source_is_refused_or_bound_to_c12_episode(tmp_path):
    root = tmp_path / "source"
    session = start(root, perform="omit")
    session.close()

    binding_path = root / "product" / "bp2_join.json"
    binding = json.loads(binding_path.read_text())
    assert binding["r31j_source"]["b_operation"] == "SHARE_TOOL"
    binding["r31j_source"]["b_operation"] = "REFUSE_TOOL"
    binding["r31j_source"]["b_quantity"] = 0
    binding["r31j_source"]["b_to_actor"] = "TEST_ONLY_FOREIGN_ACTOR_A"
    binding["r31j_source"]["b_actor"] = "TEST_ONLY_FOREIGN_ACTOR_B"
    binding_path.write_text(json.dumps(binding, indent=2, sort_keys=True) + "\n")

    opened = _open_or_fail(root, expected="refusal or C12-bound source")
    if opened is None:
        return
    try:
        episode_source = gm01_episode_source(opened)
        loaded_source = opened.product.source
        if loaded_source == episode_source:
            return
        pytest.fail(json.dumps({
            "case": "tampered_r31j_source",
            "opened": True,
            "loaded_b_operation": loaded_source.get("b_operation"),
            "loaded_b_quantity": loaded_source.get("b_quantity"),
            "loaded_b_to_actor": loaded_source.get("b_to_actor"),
            "loaded_b_actor": loaded_source.get("b_actor"),
            "episode_b_operation": episode_source.get("b_operation"),
            "episode_b_quantity": episode_source.get("b_quantity"),
            "episode_b_to_actor": episode_source.get("b_to_actor"),
            "episode_b_actor": episode_source.get("b_actor"),
            "verify": opened.verify().get("ok"),
            "accepted": opened.do_help().get("accepted"),
        }, sort_keys=True))
    finally:
        opened.close()


def test_missing_session_is_typed_refusal(tmp_path):
    root = tmp_path / "missing"
    try:
        JoinedSession.open(root)
    except SessionRefusal as exc:
        assert exc.code == "SESSION_NOT_FOUND"
        return
    except Exception as exc:
        pytest.fail(
            f"expected SessionRefusal(SESSION_NOT_FOUND), got raw "
            f"{type(exc).__name__}: {exc}"
        )
    pytest.fail("open returned a session for a directory with no session.json")


def test_orphan_product_root_start_is_typed_refusal(tmp_path):
    root = tmp_path / "orphan"
    session = start(root, perform="omit")
    session.close()
    (root / "session.json").unlink()

    try:
        retried = JoinedSession.start(root, perform="omit")
    except SessionRefusal as exc:
        assert exc.code in {
            "SESSION_EXISTS__NO_AUTOMATIC_REROLL",
            "ORPHAN_PRODUCT_ROOT",
        }
        return
    except Exception as exc:
        pytest.fail(
            f"expected typed SESSION/ORPHAN refusal, got raw "
            f"{type(exc).__name__}: {exc}"
        )
    else:
        try:
            pytest.fail(json.dumps({
                "case": "orphan_product_root_start",
                "opened": True,
                "product_root": str(retried.product.root),
                "counts": retried.verify().get("counts"),
            }, sort_keys=True))
        finally:
            retried.close()


def test_relocated_session_root_is_refused_or_rebound(tmp_path):
    root = tmp_path / "relocated"
    session = start(root, perform="omit")
    session.close()
    moved = root.with_name(root.name + "_moved")
    shutil.move(str(root), str(moved))

    try:
        opened = JoinedSession.open(moved)
    except SessionRefusal:
        return
    except Exception as exc:
        pytest.fail(
            f"expected SessionRefusal or rebinding after directory move, got raw "
            f"{type(exc).__name__}: {exc}"
        )
    try:
        product_root = Path(opened.product.root).resolve()
        assert product_root.is_relative_to(moved.resolve()), (
            f"opened product root outside moved session: {product_root}"
        )
    finally:
        opened.close()
