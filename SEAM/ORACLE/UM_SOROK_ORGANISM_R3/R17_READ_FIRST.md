# SOROK REMONTATHON R17 — full source preflight after R16

**Frozen parent:** R16 draft #1222 `7a8a18c153ee5a36e1c52eca15f4e5e8862296be`.
**Scope:** repair the inherited R15 P018 defect: source reads and appends must use the same full source/chain validity required by `verify_chain()`, not only the limited auxiliary fast check. No new psychology, native authority, protected merge, or canonical PROGRAMMA write.

From this extracted archive root:

```bash
python -m unittest discover -s tests -q
python -O -m unittest discover -s tests -q
python -m pytest -q
python -m unittest tests.test_r17_source_preflight -v
python -m um_sorok_organism demo --db /tmp/remont_r17_fresh.sqlite3
```

**Executed locally on Python 3.11.3:** 289/289 unittest normal, 289/289 `-O`, pytest 289 passed + 32 subtests. Fresh demo outputs are byte-identical across `PYTHONHASHSEED` values, 9 events, last hash `bc47d610…`, cold reopen and `PRAGMA integrity_check` valid.

The repair adds full `verify_chain()` preflight to `source()`, `commit()` and `seal_source()`, maps malformed envelopes to typed `EVENT_ENVELOPE_MALFORMED` / `Conflict(SOURCE_HISTORY_INVALID: …)`, preserves the existing specific conflict diagnostics, and updates two inherited R4 source-seal assertions to inspect the source table directly because `source()` now correctly refuses an already-invalid ledger. See `REMONT/SOROK/REPAIRS/REMONTATHON_R3_R17_20261120/REPAIR_RECEIPT.md`.

R17 is sourcefree author-tested, not independently accepted. The 73 P records and six E holds remain unchanged; P070–P073 and all prior receiving histories remain separately attributed.
