"""C8O hostile court F: source/import custody and inherited-execution ledger verification.

Verifies the reconstructed local dependency closure against pinned Git blob
SHA-1 values, the actual imported module file paths, and the JUnit counts of
the inherited courts executed in this return.
"""
from __future__ import annotations

import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))

from c8o_court_support import ACCEPTED_STAGE, CANDIDATE, CONSUMER, RET  # noqa: E402

PINNED = {
    "runtime/stage_out12/outbox_prototype.py": "331840768ce0b5f6f73e5e93094ca0d217ddaebf",
    "runtime/stage_out12/multiwriter_journal.py": "99217d390a452f22fc1a470abc411c6ca84b86ba",
    "runtime/stage_out14/outbox_prototype.py": "331840768ce0b5f6f73e5e93094ca0d217ddaebf",
    "runtime/stage_out14/multiwriter_journal.py": "7488353f492cccac86a5d6a02937d3f2bf052341",
    "runtime/stage_out14/test_out14_integrity.py": "1cc37c428a995e89419b4b4ceb8e95995c4ff7f6",
    "runtime/out13_return/runtime/candidate/outbox_prototype.py": "331840768ce0b5f6f73e5e93094ca0d217ddaebf",
    "runtime/out13_return/runtime/candidate/multiwriter_journal.py": "99217d390a452f22fc1a470abc411c6ca84b86ba",
    "severance/proof_integrity_gate_r1.py": "774d338cdbeea68ab09006807431cc8d17a22345",
}

INHERITED_SUITES = {
    "junit/original_272.xml": (272, 270, 2),
    "junit/out12_author_9.xml": (9, 9, 0),
    "junit/out13_hostile_23.xml": (23, 23, 0),
    "junit/out14_new_court.xml": (27, 27, 0),
}


def _blob_sha1(path: Path) -> str:
    out = subprocess.run(
        ["git", "hash-object", str(path)],
        capture_output=True,
        text=True,
        check=True,
        cwd=str(RET),
    )
    return out.stdout.strip()


def test_staged_inherited_sources_match_pinned_git_blob_sha1():
    for rel, expected in PINNED.items():
        path = RET / rel
        assert path.is_file(), rel
        assert _blob_sha1(path) == expected, rel


def test_imported_modules_resolve_inside_this_return():
    import c8_readonly_consumer
    import c8o_trusted_outbox
    import multiwriter_journal
    import outbox_prototype

    assert str(RET) in outbox_prototype.__file__
    assert str(RET) in multiwriter_journal.__file__
    assert str(CANDIDATE) in c8o_trusted_outbox.__file__
    assert str(CONSUMER) in c8_readonly_consumer.__file__
    assert outbox_prototype.__file__.endswith("outbox_prototype.py")
    accepted = Path(outbox_prototype.__file__).read_bytes()
    assert _blob_sha1(Path(outbox_prototype.__file__)) == PINNED["runtime/stage_out12/outbox_prototype.py"]
    assert accepted == (ACCEPTED_STAGE / "outbox_prototype.py").read_bytes()


def test_accepted_legacy_writer_api_is_the_original_unmodified_one():
    import inspect

    import outbox_prototype

    assert str(inspect.signature(outbox_prototype.Journal.commit)) == "(self, p, crash_boundary=None)"
    assert outbox_prototype.Journal.__doc__.startswith("Single-writer source-free durability experiment")


def test_inherited_junit_counts_match_executed_courts():
    for rel, (tests, passed, failures) in INHERITED_SUITES.items():
        xml = RET / rel
        assert xml.is_file(), rel
        root = ET.parse(xml).getroot()
        suites = [root] if root.tag == "testsuite" else list(root)
        total = sum(int(s.attrib.get("tests", 0)) for s in suites)
        fail = sum(int(s.attrib.get("failures", 0)) for s in suites)
        err = sum(int(s.attrib.get("errors", 0)) for s in suites)
        assert total == tests, rel
        assert fail + err == failures, rel
        assert total - fail - err == passed, rel


def test_historical_reds_are_preserved_and_identified():
    xml = RET / "junit/original_272.xml"
    root = ET.parse(xml).getroot()
    names = sorted(
        c.attrib["name"]
        for c in root.iter("testcase")
        if c.find("failure") is not None or c.find("error") is not None
    )
    assert names == [
        "test_replay_manual_two_writers_can_lose_first_committed_event",
        "test_s27_material_move_needs_world_owner",
    ]


def test_out14_under_out14_repair_divergence_is_recorded():
    xml = RET / "junit/regression_out13_23_under_out14.xml"
    root = ET.parse(xml).getroot()
    failed = [
        c.attrib["name"]
        for c in root.iter("testcase")
        if c.find("failure") is not None or c.find("error") is not None
    ]
    assert failed == ["test_hp8_corrupting_writer_version_resets_to_zero_and_defeats_the_CAS"]
