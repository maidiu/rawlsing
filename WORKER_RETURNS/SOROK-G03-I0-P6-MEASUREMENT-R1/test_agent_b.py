"""Agent B: frozen G03-I0 custody/state attacks, not substitute P6 observations."""
import sqlite3
import tempfile
import unittest
from pathlib import Path
import test_measure as a
import read_receipts as reader

class StateAndCustodyAttacks(unittest.TestCase):
    def setUp(self):
        self.fixture = a.Attacks("test_valid_synthetic_format_only")
        self.fixture.setUp()
        self.addCleanup(self.fixture.doCleanups)
        self.root = self.fixture.p

    def test_same_byte_count_state_rewrite_cannot_hide(self):
        """Equal byte totals do NOT establish the failed P6 action was nonmutating."""
        state = self.root / "state"
        state.mkdir(exist_ok=True)
        file = state / "payload.bin"
        if not file.exists():
            file.write_bytes(b"A" * 40)
        before = file.read_bytes()
        self.assertTrue(reader.consume(self.root)["expected_scenario_pass"])
        file.write_bytes(b"Z" * len(before))
        try:
            with self.assertRaisesRegex(reader.Reject, "STATE_FINAL_CONTENT_MISMATCH"):
                reader.consume(self.root)
        finally:
            file.write_bytes(before)
        self.assertTrue(reader.consume(self.root)["expected_scenario_pass"])

    def test_logical_sqlite_witness_does_not_hide_real_row_change(self):
        """A stable SQLite page format is not permission to ignore changed P3 rows."""
        import measure as writer
        with tempfile.TemporaryDirectory() as tmp:
            state = Path(tmp) / "state"
            dbpath = state / "actual-p2" / "p3_psyche.sqlite3"
            dbpath.parent.mkdir(parents=True)
            with sqlite3.connect(dbpath) as db:
                db.execute("CREATE TABLE p3_records (id INTEGER, target TEXT)")
                db.execute("INSERT INTO p3_records VALUES (1, 'before')")
            first_writer = writer.state_snapshot(state, logical=True)["sha256"]
            first_reader = reader.state_snapshot(state, logical=True)["sha256"]
            self.assertEqual(first_writer, first_reader)
            with sqlite3.connect(dbpath) as db:
                db.execute("UPDATE p3_records SET target='after' WHERE id=1")
            last_writer = writer.state_snapshot(state, logical=True)["sha256"]
            last_reader = reader.state_snapshot(state, logical=True)["sha256"]
            self.assertNotEqual(first_writer, last_writer)
            self.assertEqual(last_writer, last_reader)

    def test_manifest_rewrite_cannot_survive_pinned_raw_index(self):
        """An external anchor for attempts must bind the runner/interpreter metadata."""
        manifest = self.fixture.man
        manifest["runner_sha256"] = "f" * 64
        self.fixture.save(self.root / "manifest.json", manifest)
        with self.assertRaisesRegex(reader.Reject, "MANIFEST_NOT_INDEXED"):
            reader.consume(self.root)

if __name__ == "__main__":
    unittest.main()
