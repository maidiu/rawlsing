# Build and replay

Publication branch: `agent/programma-pyat-w1-h-master-map-fanin-p0p1-20261101-r1`, private repository `maidiu/rawlsing`. Use the exact published 40-hex commit in the handback; do not substitute a later branch head. The implementation is `rawlsing_next/programma_pyat_reference/`.

Dependencies: Python 3.10+ standard library and Git; no pip packages, server, credentials in files, survey files, controller or UI. Run at the repository root. The fresh checkout must retain the historical Git commit/blob objects listed in `SOURCE_LOCK_AND_NORMALIZATION.json` (`input_lock[].cut` and `source_pins.*.cut`). An ordinary complete clone with the referenced branches contains these objects. For a shallow or partial checkout, fetch the listed exact commit SHAs from authenticated `origin` before replay. A missing object cannot be replaced by a newer file. Non-Git URLs, absent paths and unavailable Library pointers remain explicitly unresolved.

```sh
python3 -m rawlsing_next.programma_pyat_reference --store /tmp/pyat-map ingest --cut 9809203fd915a84bae056a67210e9213879840db
python3 -m rawlsing_next.programma_pyat_reference --store /tmp/pyat-map verify
python3 -m rawlsing_next.programma_pyat_reference --store /tmp/pyat-map whole
python3 -m rawlsing_next.programma_pyat_reference --store /tmp/pyat-map focus N11 --brief
python3 -m rawlsing_next.programma_pyat_reference --store /tmp/pyat-map reverse N10W --brief
python3 -m rawlsing_next.programma_pyat_reference --store /tmp/pyat-map code N2 --brief
python3 -m rawlsing_next.programma_pyat_reference --store /tmp/pyat-map seams F6 --brief
python3 -m rawlsing_next.programma_pyat_reference --store /tmp/pyat-map gaps WG0 --brief
python3 -m rawlsing_next.programma_pyat_reference --store /tmp/pyat-map alternatives F7
python3 -m rawlsing_next.programma_pyat_reference --store /tmp/pyat-map source SRC35
python3 -m rawlsing_next.programma_pyat_reference --store /tmp/pyat-map work-now
python3 -m rawlsing_next.programma_pyat_reference --store /tmp/pyat-map ingest --cut acbe2326c8f52dfe8bfa200e87c5c07a62a5c93a
python3 -m rawlsing_next.programma_pyat_reference --store /tmp/pyat-map changes acbe2326c8f52dfe8bfa200e87c5c07a62a5c93a 9809203fd915a84bae056a67210e9213879840db
python3 -m unittest rawlsing_next.programma_pyat_reference.test_reference -v
python3 -m rawlsing_next.programma_pyat_reference.replay
```

The final replay command regenerates the required receipts, coverage, lock and traversal file using fresh CLI processes and two independent temporary stores. It checks identical cold snapshot bytes and hashes, inverse edge identity, targeted evidence withdrawal/restore, an unaffected independent N9C RED and all hostile tests. Temporary paths in the emitted commands identify the actual executed process stores; substitute your own `--store` path for manual queries. No source-native pilot is run.

`ingest --cut` selects a read comparison context. The seven lane inputs always retain their frozen source cuts. `changes` compares the same frozen evidence set against actual path/blob identities at both selected contexts; it does not silently refresh lanes or infer adoption. `--route` requires an actual graph edge at every hop and errors if absent; MISSING edge types show a broken functional connection. `reverse` derives inverse navigation over those same edge IDs. Associations and partial function matches never roll up to completion.

Full raw assertions are in every default query; `--brief` reduces output while retaining exact return evidence, pins, maturity axes and negative scope. `ROW:<lane>:<table>:<original-id>` disambiguates raw records. Stable entity shorthand such as `SRC35` selects the source entity; `M2` returns explicit ambiguity. All proposed F schema content and all 39 input/support files are retained unchanged under `inputs/` and verified against Git.

Expected failures: input-byte or snapshot tampering, a manifest duplicate, wrong content pin, fake immutable cut, unknown route endpoint/edge, self-review promotion or synthetic-to-native promotion. These failures are not original-source refusals or scientific null results. The reference has no authority-issuance, owner-adoption or protected CAS endpoint.
