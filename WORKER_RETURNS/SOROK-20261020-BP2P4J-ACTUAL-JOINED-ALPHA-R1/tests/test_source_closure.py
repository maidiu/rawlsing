"""Exact source closure: staged bytes, imported modules and no upstream edits."""
from __future__ import annotations

import hashlib
from pathlib import Path

import bp2p4
from bp2p4 import bootstrap

RETURN = bootstrap.RETURN
VENDOR = bootstrap.VENDOR


def test_manifest_verifies_against_origin_commits():
    manifest = bp2p4.verify_sources()
    assert manifest["file_count"] == 150
    assert manifest["origin_commits"]["BP2"] == (
        "5065e2e6934e9d5bca800cbf88c79e461bcf2393")
    assert manifest["origin_commits"]["BP4"] == (
        "d868e82c7c83def2df18295244d93af9706e647f")
    bp2 = [row for row in manifest["files"] if row["staged_path"].startswith("bp2/")]
    bp4 = [row for row in manifest["files"] if row["staged_path"].startswith("bp4/")]
    assert len(bp2) == 74
    assert len(bp4) == 76


def test_loaded_upstream_modules_are_pinned():
    # Import the modules under test first, then verify the loaded bytes.
    import bp2_joined.producer  # noqa: F401
    import candidate.pipeline  # noqa: F401
    import lab_sgi1  # noqa: F401
    import lab_sgi1.core  # noqa: F401
    import lab_sgi1.history  # noqa: F401
    import lab_sgi1.joint  # noqa: F401
    import lab_sgi1.proposal  # noqa: F401
    import bp4.bp2_compat  # noqa: F401
    import bp4.c10  # noqa: F401
    import bp4.product  # noqa: F401
    import bp4.perception  # noqa: F401
    import rawlsing_next.m6_actor_safe_expression  # noqa: F401
    import rawlsing_next.v3_psepf_zero_positive_guard  # noqa: F401

    report = bp2p4.verify_loaded_modules()
    assert report["ok"] is True, report["problems"]
    by_name = {row["module"]: row for row in report["modules"]}
    for name in ("bp1.c9_bridge", "candidate.pipeline", "c8_exclusive_writer",
                 "c9_event_ingress", "bp2_joined.producer", "bp4.c10",
                 "bp4.product", "bp4.perception"):
        assert by_name[name]["origin"] == "STAGED_RETURN", name
        assert by_name[name]["ok"] is True, name
    m6 = by_name["rawlsing_next.m6_actor_safe_expression"]
    assert m6["origin"] == "LIVE_REPO_PINNED"
    assert m6["pinned"] == "74d9701cdc7dabccf61eb5089498db290c1efd9c"


def test_upstream_test_files_are_byte_identical():
    manifest = bp2p4.verify_sources()
    by_path = {row["staged_path"]: row for row in manifest["files"]}
    for staged in ("bp2/tests/test_joined_positive.py",
                   "bp2/tests/test_joined_severance.py",
                   "bp4/tests/test_bp4_product.py",
                   "bp4/tests/test_bp4_severance.py"):
        assert staged in by_path
        path = VENDOR / staged
        assert hashlib.sha256(path.read_bytes()).hexdigest() == by_path[staged]["sha256"]


def test_no_upstream_file_was_written_in_place():
    # The staged copies live only under this return's vendor/ tree.
    for prefix in ("bp2", "bp4"):
        for path in (VENDOR / prefix).rglob("*.py"):
            assert RETURN in path.parents
    assert bootstrap.REPO != RETURN
