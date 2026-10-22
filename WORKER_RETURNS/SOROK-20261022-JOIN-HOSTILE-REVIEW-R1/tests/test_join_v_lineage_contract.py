"""Targeted shared-lineage transition attacks for JOIN-E 49022f6."""
import hashlib
import json
import shutil
from pathlib import Path

import pytest

from joined.refusal import RefusalSession
from joined.session import JoinedSession
from r30a.first_session import SessionRefusal
from support import read_meta, start, write_meta


CASES = (
    ("joined", lambda path: JoinedSession.start(path, perform="omit"), JoinedSession.open),
    ("refusal", RefusalSession.start, RefusalSession.open),
)


def _branch_ids(session):
    return sorted(row["branch_id"] for row in session.product.store.branches())


def _products(root):
    root = Path(root) / "product"
    return {
        str(path.relative_to(root)): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in sorted(root.rglob("*"))
        if path.is_file()
    }


def _copy_state(source, target):
    shutil.copytree(source, target)
    meta = read_meta(target)
    meta["product_root"] = str((Path(target) / "product").resolve())
    meta["state_root"] = str(Path(target).resolve())
    write_meta(target, meta)
    return meta


def test_nested_forks_receipts_and_cold_parent_isolation(tmp_path):
    for name, start_session, open_session in CASES:
        state = tmp_path / name
        session = start_session(state)
        parent_counts = session.product.store.verify("first_session")["counts"]
        try:
            first = session.fork_alt("alt")
            second = session.fork_alt("alt2")
            assert first["status"] == "OK"
            assert second["status"] == "OK"
            assert session.branch_id == "alt2"
            lineage = session.meta["branch_lineage"]
            assert lineage["current_branch"] == "alt2"
            assert [r["new_branch"] for r in lineage["fork_receipts"]] == ["alt", "alt2"]
            for receipt in lineage["fork_receipts"]:
                row = session.product.store.branch(receipt["new_branch"])
                assert receipt["parent_branch"] == row["parent_branch_id"]
                assert receipt["fork_clock"] == row["fork_clock"]
                assert receipt["root_hash"] == row["root_hash"]
                assert receipt["created_clock"] == row["created_clock"]
                assert receipt["fork_clock"] is not None
                assert receipt["root_hash"]
            assert session.product.store.verify("first_session")["counts"] == parent_counts
            assert session.verify()["ok"] is True
        finally:
            session.close()

        cold = open_session(state)
        try:
            assert cold.branch_id == "alt2"
            assert cold.verify()["ok"] is True
            assert cold.product.store.verify("first_session")["counts"] == parent_counts
        finally:
            cold.close()


def test_parent_sibling_and_root_metadata_switches_refused_without_mutation(tmp_path):
    for name, start_session, open_session in CASES:
        state = tmp_path / f"{name}_base"
        session = start_session(state)
        session.fork_alt("alt")
        session.fork_alt("alt2")
        session.close()
        for requested in ("first_session", "alt", "root"):
            copy = tmp_path / f"{name}_{requested}"
            meta = _copy_state(state, copy)
            meta["branch_id"] = requested
            write_meta(copy, meta)
            before = _products(copy)
            with pytest.raises(SessionRefusal) as exc:
                opened = open_session(copy)
                opened.close()
            assert exc.value.code in {"UNAUTHORIZED_BRANCH", "BRANCH_LINEAGE_MISMATCH"}
            assert _products(copy) == before


def test_missing_and_tampered_receipts_refused_without_mutation(tmp_path):
    for name, start_session, open_session in CASES:
        state = tmp_path / f"{name}_base"
        session = start_session(state)
        session.fork_alt("alt")
        session.fork_alt("alt2")
        session.close()
        mutations = {
            "missing_receipts": lambda meta: meta["branch_lineage"].pop("fork_receipts", None),
            "missing_first_receipt": lambda meta: meta["branch_lineage"]["fork_receipts"].pop(0),
            "tampered_clock": lambda meta: meta["branch_lineage"]["fork_receipts"][0].update({"fork_clock": 999}),
            "tampered_root": lambda meta: meta["branch_lineage"]["fork_receipts"][0].update({"root_hash": "FOREIGN"}),
            "broken_chain": lambda meta: meta["branch_lineage"]["fork_receipts"][1].update({"parent_branch": "first_session"}),
        }
        for label, mutate in mutations.items():
            copy = tmp_path / f"{name}_{label}"
            shutil.copytree(state, copy)
            meta = read_meta(copy)
            meta["product_root"] = str((copy / "product").resolve())
            meta["state_root"] = str(copy.resolve())
            mutate(meta)
            write_meta(copy, meta)
            before = _products(copy)
            with pytest.raises(SessionRefusal) as exc:
                opened = open_session(copy)
                opened.close()
            assert exc.value.code in {"UNAUTHORIZED_BRANCH", "BRANCH_LINEAGE_MISMATCH"}
            assert _products(copy) == before


def test_duplicate_fork_refused_without_mutation(tmp_path):
    for name, start_session, open_session in CASES:
        state = tmp_path / f"{name}_duplicate"
        session = start_session(state)
        try:
            session.fork_alt("alt")
            branches = _branch_ids(session)
            meta = json.dumps(session.meta.get("branch_lineage"), sort_keys=True)
            with pytest.raises(SessionRefusal) as exc:
                session.fork_alt("alt")
            assert exc.value.code == "FORK_REFUSED"
            assert _branch_ids(session) == branches
            assert json.dumps(session.meta.get("branch_lineage"), sort_keys=True) == meta
            assert session.branch_id == "alt"
        finally:
            session.close()


def test_invalid_empty_fork_is_atomic(tmp_path):
    for name, start_session, open_session in CASES:
        state = tmp_path / f"{name}_invalid"
        session = start_session(state)
        try:
            branches = _branch_ids(session)
            meta = json.dumps(session.meta.get("branch_lineage"), sort_keys=True)
            with pytest.raises(SessionRefusal) as exc:
                session.fork_alt("")
            assert exc.value.code == "FORK_REFUSED"
            assert _branch_ids(session) == branches, (
                f"{name}: invalid fork left branch(es) "
                f"{sorted(set(_branch_ids(session)) - set(branches))}"
            )
            assert json.dumps(session.meta.get("branch_lineage"), sort_keys=True) == meta
            assert session.branch_id == "first_session"
        finally:
            session.close()
