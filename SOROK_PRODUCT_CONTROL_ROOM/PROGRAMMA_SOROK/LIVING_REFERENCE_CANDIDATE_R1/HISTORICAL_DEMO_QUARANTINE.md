# Historical demonstration evidence — not operating state

`r2_live_transaction.json` at this directory root is the original R2 author receipt.
It reports a self-declared `SOURCEFREE_REVIEW`/`PASS`, a synthetic
`SOROK_R2_NEW_REQUIREMENT` and a repeated-`a` return SHA. It is not independent
review, not a real returned artifact and not operating acceptance.

Exact historical bytes are preserved under:

`quarantine/historical_demo_contamination/`

with `MANIFEST.json` containing SHA-256 values and an inventory of excluded
history identities. The clean operating state is rebuilt from frozen
source-backed seeds plus the append-only `evidence/journal.jsonl`; none of the
excluded demo/self-review events are replayed.

The current `r2_live_transaction.py` is disposable by default: it writes only to a
temporary directory and proves the operating state, snapshot, journal and this
historical receipt are byte-identical before and after.
