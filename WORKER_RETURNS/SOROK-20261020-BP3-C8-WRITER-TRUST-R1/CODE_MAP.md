# BP3 old/new code map

## Old accepted writer paths

| Entrypoint | Exact source | Blob | Disposition |
|---|---|---|---|
| `outbox_prototype.Journal.commit` | `vendor/outbox_prototype.py` from accepted OUT9 | `331840768ce0b5f6f73e5e93094ca0d217ddaebf` | gated by `install_exclusive_gate` |
| `outbox_prototype.Journal.admit_and_queue` | same | same | gated |
| `c8o_trusted_outbox.C8OccurrenceJournal.commit` | C8O trusted wrapper | `7d785d35be09ab2ca5877a89a7880c70f2fe488c` | inherited CAS base; not old `Journal.commit` |
| `c8o_trusted_outbox.C8OccurrenceJournal.admit_and_queue` | same | same | inherited; BP3 `append_occurrence` preferred |

## New candidate paths

| Module/function | Role |
|---|---|
| `c8_exclusive_writer.install_exclusive_gate` | closes old class methods in-process |
| `c8_exclusive_writer.WriterKeyStore` | external test key loading + external-path check |
| `c8_exclusive_writer.KeyedCapability` | HMAC capability bound to journal/role/expiry |
| `c8_exclusive_writer.KeyedMonotonicAnchor` | keyed rows + separate watermark, observe/check |
| `c8_exclusive_writer.ExclusiveJournal.commit` | sole keyed CAS append with proof |
| `c8_exclusive_writer.ExclusiveJournal.append_occurrence` | occurrence/outbox append, duplicate no-op |
| `c8_exclusive_writer.ExclusiveJournal.verify_journal` | proof + anchor verification |
| `c9_event_ingress.receive_event` | sourcefree C9 event ingress over actual C8 readset |
| `bp3_worker.py` | 2/3/5 OS writer fixture |
| `bp3_crash_worker.py` | BEFORE_RENAME/AFTER_COMMIT crash fixture |

## Import/consumer graph

`outbox_prototype.Journal` → gated; `c8o_trusted_outbox.C8OccurrenceJournal` → inherited by `ExclusiveJournal` → writes C8O envelope → `c8_readonly_consumer.C8ReadOnlyConsumer` reads → `c9_event_ingress.receive_event` consumes (proof verifier required). No old `Journal.commit` call remains in the candidate positive path.
