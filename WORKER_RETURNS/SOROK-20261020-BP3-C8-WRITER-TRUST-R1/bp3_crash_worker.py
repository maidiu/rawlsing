"""BP3 crash boundary worker; TEST_ONLY."""
from __future__ import annotations
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
import c8_exclusive_writer as X
journal_path, key_path, key_id, rows, watermark, writer, label, boundary = sys.argv[1:9]
store = X.WriterKeyStore.load(key_path, key_id)
anchor = X.KeyedMonotonicAnchor(Path(rows), Path(watermark), store)
journal = X.ExclusiveJournal(journal_path, store=store, anchor=anchor)
cap = X.KeyedCapability.issue(store, journal.journal_id, writer, ttl_seconds=3600)
p, version = journal.recover()
event = p.ledger.admit({"candidate_id": label, "payload": {"utterance": "crash"}})
assert event is not None
journal.commit(p, version, capability=cap, crash_boundary=boundary)
