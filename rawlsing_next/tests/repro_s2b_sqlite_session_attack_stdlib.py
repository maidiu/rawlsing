"""Standalone SQLite/OS falsifiers for PYAT S2-B; no native I03 claims.

The accompanying repository tests exercise the actual native consumer.
This script isolates the SQLite and atomic-publication primitive behavior.
"""
from pathlib import Path
import os
import sqlite3
import tempfile

with tempfile.TemporaryDirectory(prefix="pyat-s2b-g3g4-") as directory:
    base = Path(directory)
    path = base / "certificate.sqlite"
    with sqlite3.connect(path) as db:
        db.execute("CREATE TABLE selectors(respondent TEXT, kind TEXT, target TEXT, event_ref TEXT)")
        db.executemany("INSERT INTO selectors VALUES(?,?,?,?)", [
            ("R1", "native", "Y", "EVT-1"),
            ("R2", "native", "Y", "EVT-2"),
        ])
    uri = path.as_uri() + "?mode=ro"
    with sqlite3.connect(uri, uri=True) as db:
        db.execute("PRAGMA query_only=ON")
        db.execute("BEGIN")
        before = db.execute("SELECT COUNT(*) FROM selectors").fetchone()[0]
        db.execute("PRAGMA query_only=OFF")
        db.execute("CREATE TEMP TABLE selectors(respondent TEXT,kind TEXT,target TEXT,event_ref TEXT)")
        unqualified = db.execute("SELECT COUNT(*) FROM selectors").fetchone()[0]
        qualified = db.execute("SELECT COUNT(*) FROM main.selectors").fetchone()[0]
        assert (before, unqualified, qualified) == (2, 0, 2)
        print("SQL_TEMP_SHADOW: RED unqualified=0; GREEN main=2; held disk unchanged")
    with sqlite3.connect(uri, uri=True) as db:
        db.execute("BEGIN")
        query = "SELECT event_ref FROM main.selectors WHERE respondent=? ORDER BY event_ref"
        baseline = db.execute(query, ("R1",)).fetchall()
        db.create_collation("BINARY", lambda left, right: 0)
        poisoned = db.execute(query, ("R1",)).fetchall()
        assert baseline == [("EVT-1",)] and len(poisoned) == 2
        print("BINARY_COLLATION: RED main-qualified WHERE gained unrelated event")
    stage = base / "stage.tmp"
    destination = base / "final.sqlite"
    stage.write_bytes(b"verified-stage")
    destination.write_bytes(b"rival-owner")
    try:
        os.link(stage, destination, follow_symlinks=False)
    except FileExistsError:
        pass
    else:
        raise AssertionError("no-clobber publication unexpectedly replaced rival")
    assert destination.read_bytes() == b"rival-owner"
    print("ATOMIC_LINK: GREEN existing destination retained without clobber")
print("STANDALONE_G3_G4_PRIMITIVE_REPRODUCTION_PASS")
