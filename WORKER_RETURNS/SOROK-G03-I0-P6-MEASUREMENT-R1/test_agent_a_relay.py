"""Agent A relay: invalidate B's BLOB/TEXT type-collision logical witness.

Both falsifiers use genuine SQLite transactions. The second uses a P3 store
created by the original unmodified P6 CLI, not an invented replacement owner.
"""
import sqlite3
from contextlib import closing
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import measure as writer
import read_receipts as reader


class TypedPsycheWitness(unittest.TestCase):
    def setUp(self):
        td = tempfile.TemporaryDirectory()
        self.addCleanup(td.cleanup)
        self.root = Path(td.name) / "state"
        self.dbpath = self.root / writer.SQLITE_REL
        self.dbpath.parent.mkdir(parents=True)

    def update_and_checkpoint(self, sql, parameters):
        with closing(sqlite3.connect(self.dbpath)) as db:
            db.execute(sql, parameters)
            db.commit()
            if db.execute("PRAGMA journal_mode").fetchone()[0] == "wal":
                result=db.execute("PRAGMA wal_checkpoint(TRUNCATE)").fetchone()
                self.assertEqual(result[0],0,"SQLite WAL checkpoint blocked")

    def readings(self):
        w = writer.state_snapshot(self.root, logical=True)["sha256"]
        r = reader.state_snapshot(self.root, logical=True)["sha256"]
        self.assertEqual(w, r, "writer and receiver must independently agree")
        return w

    def test_blob_vs_text_must_not_collapse_in_logical_record(self):
        with closing(sqlite3.connect(self.dbpath)) as db:
            db.execute("CREATE TABLE p3_records(id INTEGER PRIMARY KEY, payload_json TEXT NOT NULL)")
            db.execute("INSERT INTO p3_records VALUES (1, ?)",
                       (sqlite3.Binary(bytes.fromhex("4142")),))
            db.commit()
        with closing(sqlite3.connect(self.dbpath)) as db:
            self.assertEqual(db.execute(
                "SELECT typeof(payload_json) FROM p3_records").fetchone()[0], "blob")
        before = self.readings()
        self.update_and_checkpoint("UPDATE p3_records SET payload_json=? WHERE id=1", ("4142",))
        with closing(sqlite3.connect(self.dbpath)) as db:
            self.assertEqual(db.execute(
                "SELECT typeof(payload_json) FROM p3_records").fetchone()[0], "text")
        after = self.readings()
        self.assertNotEqual(before, after,
                            "REAL SQL ROW CHANGED TYPE AND CONTENT BUT B'S LOGICAL HASH COLLIDED")

    def test_original_p6_p3_table_blob_text_collision(self):
        repo = Path(__file__).resolve().parents[2]
        cmd = [sys.executable, str(repo / writer.P6),
               "--state", str(self.root), "new"]
        result = subprocess.run(cmd, cwd=repo, env=writer.env_offline(),
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                timeout=120)
        self.assertEqual(result.returncode, 0,
                         "Original P6 new failed: " + result.stderr.decode(errors="replace")[:500])
        self.assertTrue(self.dbpath.is_file(), "Actual P3 psyche store missing")
        with closing(sqlite3.connect(self.dbpath)) as db:
            existing = db.execute("SELECT seq FROM p3_records ORDER BY seq LIMIT 1").fetchone()
            self.assertIsNotNone(existing, "Real P6 P3 record absent")
        self.update_and_checkpoint("UPDATE p3_records SET payload_json=? WHERE seq=?",
                                   (sqlite3.Binary(bytes.fromhex("4142")), existing[0]))
        before = self.readings()
        self.update_and_checkpoint("UPDATE p3_records SET payload_json=? WHERE seq=?",
                                   ("4142", existing[0]))
        after = self.readings()
        self.assertNotEqual(before, after,
                            "Genuine P6-generated P3 database changed logical row undetected")

    def test_uncheckpointed_wal_must_be_refused_not_misreported_logical(self):
        with closing(sqlite3.connect(self.dbpath)) as db:
            db.execute("PRAGMA journal_mode=WAL")
            db.execute("CREATE TABLE p3_records(id INTEGER PRIMARY KEY, payload_json TEXT)")
            db.execute("INSERT INTO p3_records VALUES (1, 'old')")
            db.commit()
            # Keep the writer open, so a committed WAL remains uncheckpointed.
            db.execute("UPDATE p3_records SET payload_json='new' WHERE id=1")
            db.commit()
            wal=Path(str(self.dbpath)+"-wal")
            self.assertTrue(wal.is_file() and wal.stat().st_size>0,
                            "Test requires real committed, uncheckpointed WAL")
            observed=writer.sqlite_logical_digest(self.root)
            self.assertEqual(observed.get("status"),"UNOBSERVED")
            self.assertEqual(observed.get("reason"),"sqlite_uncheckpointed_wal")
            with self.assertRaisesRegex(reader.Reject,"SQLITE_UNCHECKPOINTED_WAL"):
                reader.sqlite_logical_digest(self.root)


if __name__ == "__main__":
    unittest.main()
