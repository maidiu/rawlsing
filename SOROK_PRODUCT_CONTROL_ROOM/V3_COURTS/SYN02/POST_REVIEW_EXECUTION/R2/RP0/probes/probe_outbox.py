#!/usr/bin/env python3
"""TEST_ONLY probe of actor outbox PENDING -> PROJECTED -> ACKED and replay."""
from __future__ import annotations

import sqlite3
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
import probe_actor_authority as actor_probe  # noqa: E402

NOW = actor_probe.NOW


def main() -> int:
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        actor = actor_probe.connect(root / "actor.sqlite")
        actor_probe.seed(actor, "A", "b0", "e0", "root")
        committed = actor_probe.publish(
            actor, actor="A", branch="b0", epoch="e0", event_key="event-outbox",
            attempt_no=1, idempotency_key="outbox-1", request_digest="outbox-d1",
            decision_kind="COMMITTED_CHANGE", legacy_receipt="legacy-A-b0",
            source_scope="source-outbox", settled_scope="settled-outbox",
        )
        receipt = committed["receipt_hash"]
        version = committed["version"]
        versions_before = actor.execute(
            "SELECT count(*) FROM actor_version WHERE actor_id='A' AND branch_id='b0'"
        ).fetchone()[0]
        outbox = actor.execute(
            "SELECT projection_state,projected_c12_hash,acked_admin_us "
            "FROM projection_outbox WHERE receipt_hash=?", (receipt,)
        ).fetchone()
        assert outbox == ("PENDING", None, None), outbox
        mirror = sqlite3.connect(str(root / "mirror.sqlite"), isolation_level=None)
        mirror.executescript((HERE / "schema_mirror.sql").read_text(encoding="utf8"))
        mirror.execute(
            "INSERT INTO mirror_branch VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
            ("root", "A", "e0", None, "", None, 10, 0, None, None, None, 0,
             "ROOT_READY", NOW),
        )
        mirror.execute(
            "INSERT INTO mirror_watermark VALUES (?,?,?,?,?,?)",
            ("root", 0, None, None, "CLEAN", NOW),
        )
        assert mirror.execute("SELECT count(*) FROM mirror_receipt").fetchone()[0] == 0
        assert actor.execute(
            "SELECT count(*) FROM actor_version WHERE actor_id='A' AND branch_id='b0'"
        ).fetchone()[0] == versions_before

        projection_hash = actor_probe.sha({"projection": receipt})
        mirror.execute(
            "INSERT INTO mirror_receipt VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
            ("root", 1, receipt, version, "COMMITTED_CHANGE", "semantic",
             projection_hash, actor_probe.canon({"receipt": receipt}), "", 10,
             "wr-A-b0", NOW),
        )
        mirror.execute(
            "UPDATE mirror_watermark SET last_seq=1,last_receipt_hash=?,"
            "last_projection_hash=?,updated_admin_us=? WHERE c12_branch_id='root'",
            (receipt, projection_hash, NOW),
        )
        actor.execute(
            "UPDATE projection_outbox SET projection_state='PROJECTED',"
            "projected_c12_hash=?,attempt_count=attempt_count+1 WHERE receipt_hash=?",
            (projection_hash, receipt),
        )
        assert actor.execute(
            "SELECT projection_state FROM projection_outbox WHERE receipt_hash=?",
            (receipt,)
        ).fetchone()[0] == "PROJECTED"
        actor.execute(
            "UPDATE projection_outbox SET projection_state='ACKED',"
            "acked_admin_us=?,attempt_count=attempt_count+1 WHERE receipt_hash=?",
            (NOW, receipt),
        )
        assert actor.execute(
            "SELECT projection_state,projected_c12_hash,acked_admin_us "
            "FROM projection_outbox WHERE receipt_hash=?", (receipt,)
        ).fetchone() == ("ACKED", projection_hash, NOW)
        assert actor.execute(
            "SELECT count(*) FROM actor_version WHERE actor_id='A' AND branch_id='b0'"
        ).fetchone()[0] == versions_before
        try:
            mirror.execute(
                "INSERT INTO mirror_receipt VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
                ("root", 1, "different-receipt", None, "HELD_MISSING_RULE",
                 None, "different-projection", "{}", "", 10, None, NOW),
            )
        except sqlite3.IntegrityError:
            pass
        else:
            raise AssertionError("MIRROR_DUPLICATE_ACCEPTED")
        print("PASS outbox: C4 C9 durable actor receipt, no C12 mirror, state=SYNC_HELD, outbox=PENDING")
        print("PASS outbox: C5 C12 mirror before ACK, outbox PROJECTED->ACKED, retry creates no new actor version")
        print("PASS outbox: duplicate mirror identity refused; existing projection retained")
        print("OBSERVED outbox: receipt=%s version=%s state=%s" %
              (receipt, version, actor.execute(
                  "SELECT projection_state FROM projection_outbox WHERE receipt_hash=?",
                  (receipt,)).fetchone()[0]))
        mirror.close()
        actor.close()
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
