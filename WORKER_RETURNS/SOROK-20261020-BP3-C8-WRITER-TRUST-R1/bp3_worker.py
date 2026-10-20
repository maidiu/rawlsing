"""BP3 OS-process append worker; TEST_ONLY, no native authority."""
from __future__ import annotations
import json, os, sys, time
from pathlib import Path
ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
import c8_exclusive_writer as X
journal_path, key_path, key_id, rows, watermark, writer, label = sys.argv[1:8]
store = X.WriterKeyStore.load(key_path, key_id)
anchor = X.KeyedMonotonicAnchor(Path(rows), Path(watermark), store)
journal = X.ExclusiveJournal(journal_path, store=store, anchor=anchor)
cap = X.KeyedCapability.issue(store, journal.journal_id, writer, ttl_seconds=3600)
candidate = {"candidate_id": label, "payload": {"utterance": "worker"}}
for _ in range(200):
    try:
        p, version = journal.recover()
        event, err, receipt = journal.append_occurrence(
            candidate, capability=cap, expected_version=version)
        if event is not None:
            print(json.dumps({"writer": writer, "version": receipt.c8o["writer_version"],
                              "receipt": receipt.c8o["receipt_id"]}))
            raise SystemExit(0)
        print(json.dumps({"writer": writer, "refused": err}))
        raise SystemExit(2)
    except X.c8o.StaleJournalConflict:
        time.sleep(0.002 * (1 + os.getpid() % 7))
print(json.dumps({"writer": writer, "status": "RETRY_EXHAUSTED"}))
raise SystemExit(3)
