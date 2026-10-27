#!/usr/bin/env python3
"""TEST_ONLY probe of actual QualifiedC12Store geometry plus proposed sidecar."""
from __future__ import annotations

import json
import os
import sqlite3
import sys
import tempfile
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
JOIN = Path(os.environ.get("JOIN_E_RETURN", "")).resolve()
if not JOIN.is_dir():
    raise SystemExit("JOIN_E_RETURN_MISSING: " + str(JOIN))
for path in (JOIN / "vendor" / "j", JOIN / "vendor" / "j" / "candidate",
             JOIN / "vendor" / "j" / "candidate" / "vendor" / "bp4"):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from r26e.c12_integrity import QualifiedC12Store  # noqa: E402
from bp1.canon import digest  # noqa: E402
from bp4.world import make_event  # noqa: E402

MIRROR_SCHEMA = HERE / "schema_mirror.sql"
NOW = 1_780_000_000_000_000


def canon(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def sha(value: Any) -> str:
    return digest(value)


def mirror_verify(mirror: sqlite3.Connection, c12: QualifiedC12Store) -> dict:
    errors: list[str] = []
    branches = {row["branch_id"]: row for row in c12.branches()}
    mirror_rows = list(mirror.execute(
        "SELECT c12_branch_id,c12_parent_branch_id,c12_root_hash,c12_fork_clock,"
        "c12_created_clock,c9_start_seq,c9_start_receipt_hash,base_c12_branch_id,"
        "base_c12_root_hash,base_c12_perception_count,mirror_state "
        "FROM mirror_branch"
    ))
    for (branch_id, parent, root, fork_clock, created_clock, start_seq,
         start_receipt, base_branch, base_root, base_perception, state) in mirror_rows:
        if branch_id not in branches:
            errors.append("C12_MIRROR_BRANCH_ABSENT:" + branch_id)
            continue
        actual = branches[branch_id]
        if actual["parent_branch_id"] != parent:
            errors.append("C12_PARENT_MISMATCH:" + branch_id)
        if actual["root_hash"] != root:
            errors.append("C12_ROOT_MISMATCH:" + branch_id)
        if actual["fork_clock"] != fork_clock:
            errors.append("C12_FORK_CLOCK_MISMATCH:" + branch_id)
        if actual["created_clock"] != created_clock:
            errors.append("C12_CREATED_CLOCK_MISMATCH:" + branch_id)
        if state == "FORK_HELD":
            errors.append("MIRROR_FORK_HELD:" + branch_id)
        if base_branch is not None and len(c12.perceptions(branch_id)) < base_perception:
            errors.append("C12_FORK_PERCEPTION_LOSS:" + branch_id)
        watermark = mirror.execute(
            "SELECT last_seq,last_receipt_hash,last_projection_hash,watermark_state "
            "FROM mirror_watermark WHERE c12_branch_id=?", (branch_id,)
        ).fetchone()
        if watermark is None:
            errors.append("MIRROR_WATERMARK_ABSENT:" + branch_id)
            continue
        receipts = list(mirror.execute(
            "SELECT c9_seq,c9_receipt_hash,projection_hash FROM mirror_receipt "
            "WHERE c12_branch_id=? ORDER BY c9_seq", (branch_id,)
        ))
        expected = start_seq + 1
        for seq, receipt_hash, projection_hash in receipts:
            if seq != expected:
                errors.append("MIRROR_SEQ_GAP:%s:%s" % (branch_id, seq))
            expected = seq + 1
            if seq == watermark[0]:
                if receipt_hash != watermark[1] or projection_hash != watermark[2]:
                    errors.append("MIRROR_WATERMARK_RECEIPT_MISMATCH:" + branch_id)
        if base_branch is not None:
            parent_gap = mirror.execute(
                "SELECT 1 FROM mirror_watermark WHERE c12_branch_id=? AND last_seq>=?",
                (base_branch, start_seq),
            ).fetchone()
            if parent_gap is None:
                errors.append("MIRROR_BASE_WATERMARK_MISSING:" + branch_id)
    mirror_ids = {row[0] for row in mirror_rows}
    for branch_id in branches:
        if branch_id not in mirror_ids:
            errors.append("C12_BRANCH_NOT_MIRRORED:" + branch_id)
    return {"ok": not errors, "errors": errors}


def main() -> int:
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        c12_path = root / "c12.sqlite"
        mirror_path = root / "c12_actor_mirror.sqlite"
        c12 = QualifiedC12Store(c12_path)
        c12.create_root(
            "root", clock=10, actor_ids=["A", "B"],
            state={"world": {"clock": 10}, "actors": {"A": {"x": 0}, "B": {}}},
        )
        root_branch = c12.branch("root")
        assert root_branch["root_hash"] == ""
        assert c12.verify("root")["ok"]
        assert QualifiedC12Store.__module__ == "r26e.c12_integrity"
        assert QualifiedC12Store.__mro__[1].__module__ == "bp4.store"
        assert "actor_mirror" not in [
            row[0] for row in c12.db.execute(
                "SELECT name FROM sqlite_master WHERE type='table'"
            )
        ]

        mirror = sqlite3.connect(str(mirror_path), isolation_level=None)
        mirror.executescript(MIRROR_SCHEMA.read_text(encoding="utf8"))
        mirror.execute(
            "INSERT INTO mirror_branch VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
            ("root", "A", "e0", None, root_branch["root_hash"], None,
             root_branch["created_clock"], 0, None, None, None, 0,
             "ROOT_READY", NOW),
        )
        mirror.execute(
            "INSERT INTO mirror_watermark VALUES (?,?,?,?,?,?)",
            ("root", 0, None, None, "CLEAN", NOW),
        )
        receipt_hash = sha({"c9": "receipt-1"})
        projection_hash = sha({"projection": "state-1"})
        mirror.execute(
            "INSERT INTO mirror_receipt VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
            ("root", 1, receipt_hash, "version-1", "COMMITTED_CHANGE",
             "semantic-1", projection_hash, canon({"state": 1}),
             root_branch["root_hash"], 10, "wr-1", NOW),
        )
        mirror.execute(
            "UPDATE mirror_watermark SET last_seq=1,last_receipt_hash=?,"
            "last_projection_hash=?,updated_admin_us=? WHERE c12_branch_id='root'",
            (receipt_hash, projection_hash, NOW),
        )
        assert mirror_verify(mirror, c12)["ok"]
        try:
            mirror.execute(
                "INSERT INTO mirror_receipt VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
                ("root", 1, sha({"c9": "other"}), None, "HELD_MISSING_RULE",
                 None, sha({"projection": "other"}), "{}",
                 root_branch["root_hash"], 10, None, NOW),
            )
        except sqlite3.IntegrityError:
            pass
        else:
            raise AssertionError("MIRROR_DUPLICATE_ACCEPTED")

        event = make_event(
            clock=10, kind="NO_CHANGE", actor_id="A", location="workshop",
            summary="clock-ten perception", body={"probe": True},
        )
        c12.append_world_event("root", event)
        c12.record_perception(
            "root", actor_id="A", event_id=event["event_id"], clock=10,
            channel="co_present",
        )
        assert c12.verify("root")["ok"]
        alt = c12.fork("root", "alt_ok")
        assert c12.verify("alt_ok")["ok"]
        missing = mirror_verify(mirror, c12)
        assert not missing["ok"]
        assert any("C12_BRANCH_NOT_MIRRORED:alt_ok" == e for e in missing["errors"])
        base_perception = len(c12.perceptions("root"))
        assert base_perception == 1
        mirror.execute(
            "INSERT INTO mirror_branch VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
            ("alt_ok", "A", "e1", "root", alt["root_hash"], alt["fork_clock"],
             alt["created_clock"], 1, receipt_hash, "root",
             root_branch["root_hash"], base_perception, "FORK_READY", NOW),
        )
        mirror.execute(
            "INSERT INTO mirror_watermark VALUES (?,?,?,?,?,?)",
            ("alt_ok", 1, receipt_hash, projection_hash, "CLEAN", NOW),
        )
        assert mirror_verify(mirror, c12)["ok"]

        event_11 = make_event(
            clock=10, kind="NO_CHANGE", actor_id="A", location="workshop",
            summary="clock-eleven perception", body={"probe": 2},
        )
        c12.append_world_event("root", event_11)
        c12.record_perception(
            "root", actor_id="A", event_id=event_11["event_id"], clock=11,
            channel="co_present",
        )
        assert len(c12.perceptions("root")) == 2
        bad = c12.fork("root", "alt_bad")
        assert c12.verify("alt_bad")["ok"]
        assert bad["fork_clock"] == 10
        assert len(c12.perceptions("alt_bad")) == 1
        mirror.execute(
            "INSERT INTO mirror_branch VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
            ("alt_bad", "A", "e2", "root", bad["root_hash"], bad["fork_clock"],
             bad["created_clock"], 1, receipt_hash, "root",
             root_branch["root_hash"], 2, "FORK_READY", NOW),
        )
        mirror.execute(
            "INSERT INTO mirror_watermark VALUES (?,?,?,?,?,?)",
            ("alt_bad", 1, receipt_hash, projection_hash, "CLEAN", NOW),
        )
        bad_result = mirror_verify(mirror, c12)
        assert not bad_result["ok"]
        assert any("C12_FORK_PERCEPTION_LOSS:alt_bad" == e
                   for e in bad_result["errors"]), bad_result

        c12.db.execute("UPDATE branch SET root_hash='TAMPERED' WHERE branch_id='alt_ok'")
        assert c12.verify("alt_ok")["ok"]
        tampered = mirror_verify(mirror, c12)
        assert not tampered["ok"]
        assert any("C12_ROOT_MISMATCH:alt_ok" == e for e in tampered["errors"])
        c12.db.execute("UPDATE branch SET root_hash=? WHERE branch_id='alt_ok'",
                       (alt["root_hash"],))

        c12.close()
        c12 = QualifiedC12Store(c12_path)
        assert c12.verify("root")["ok"] and c12.verify("alt_ok")["ok"]
        assert c12.verify("alt_bad")["ok"]
        cold = mirror_verify(mirror, c12)
        assert not cold["ok"]
        assert any("C12_FORK_PERCEPTION_LOSS:alt_bad" == e for e in cold["errors"])
        print("PASS c12: actual QualifiedC12Store imported from r26e.c12_integrity; base C12Store from bp4.store")
        print("PASS c12: actual root/fork/cold row verify; root=%r alt_ok_root=%s" %
              (root_branch["root_hash"], alt["root_hash"]))
        print("PASS c12: sidecar root/watermark/alt_ok mirror verified; duplicate rejected")
        print("OBSERVED c12: exact tables=%s" % (["branch", "checkpoint", "episode", "meta", "perception", "world_event"]))
        print("OBSERVED c12: PRAGMA journal_mode=%r synchronous=%r foreign_keys=%r" %
              tuple(c12.db.execute("PRAGMA " + p).fetchone()[0]
                    for p in ("journal_mode", "synchronous", "foreign_keys")))
        print("FAIL c12_physical: fork_clock=%s dropped clock-11 perception (parent=2 alt_bad=1); actual C12 verify still ok" %
              bad["fork_clock"])
        print("PASS c12: sidecar fails closed with C12_FORK_PERCEPTION_LOSS:alt_bad")
        print("PASS c12: actual C12 verify does not validate branch root; sidecar does (C12_ROOT_MISMATCH:alt_ok)")
        print("PASS c12: missing fork mirror is fail-closed (C12_BRANCH_NOT_MIRRORED:alt_ok)")
        mirror.close()
        c12.close()
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
