# WG0R current35 return — disposition carrier repaired

**The disposition-carrier RED is closed by recovery of the exact frozen payload. Full current35 operation execution remains unverified.**

The recovered payload is exactly **18,276 bytes**, with the original SHA-256 `64a43ba2d7564d7681770065b843273330dc368b8d01bf328a8af7b19878bd98`. The expected hash, P2 identity master and code meanings are unchanged. Every recovered byte agrees with the surviving 1,000-row shard where independently comparable; all reserved bits are zero.

The malformed file was already malformed in its original Git publication `b44596d880425f6984f208bfa14daee2f15d3f90` (blob `c93945d158198871f5cc6692a6bed25aeef44028`), not damaged by the local documentary copy. It remains unmodified as historical RED evidence. The separately versioned repaired carrier is `sources/recovered_disposition/CURRENT35_IMPLEMENTATION_DISPOSITION_LEDGER.csv`.

`recover_disposition_payload.py` reproduces the exact bytes from retained per-implementation S00 workstreams, central O06 routing, O08/O09 conditioner records, accepted O04 endpoint identities and immutable worker ancestry plus the explicit central feelevel ruling. A diagnostic O07 recall projection is used solely to construct candidate bytes; it has no semantic issuance authority. The candidate is usable only after matching the independently frozen original payload SHA and exact P2 master. No aggregate-count reconstruction or new semantic decision is accepted. Input hashes, archive/member provenance and the minimal replay projections are in `evidence/disposition_recovery_input_custody.json` and `sources/recovered_disposition/`.

The accounting reader now consumes the repaired carrier and checks payload/hash/P2 identity, format, declared length, code map and reserved bits. The regenerated ledger accounts for **18,276 unique implementations / 35 waves / nine families**, with **10,418 hard-fail flags** and **4,447 route-predicate-required flags** preserved. These implementation flags are separate from the **76 P10/G1A held accounting states**, which remain unchanged within the 65,354-unit census. Full per-row and per-wave outputs are in `evidence/current35_implementation_accounting.csv` and `evidence/all35_wave_conservation.csv`.

The repair court includes exact byte recovery, all 1,000 surviving shard rows, original class counts, and payload/header/P2/code-map/length/duplicate corruption refusals. Fresh native and relocated cold results are in `evidence/repair_court.xml` and `evidence/repair_cold_court.xml`. Prior 82-test native-fixture and cold evidence is preserved. No native empirical owner or original semantic source is modified.

The independent WG0I review at `44eac9021db23267448a6fc151e6bbe8374a868f` accepted the earlier bounded fixture and identity-accounting results, required this carrier repair, and retained the full original-item/operation HOLD. It has not reviewed this repair. Its separate P2/O35E crosswalk obligation and full authority-to-operation execution witness remain pending; this byte repair does not issue source rights, operation permission, psychological coefficients, CAN/ADP semantics, N11/N12 or V3 adoption.

Replay from this return directory:

```sh
python3 -B recover_disposition_payload.py
python3 -B account_current35.py
PYTHONPATH=sources/native PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python3 -B -m pytest test_wg0r.py test_disposition_repair.py -q
```

The original research report is retained as `01_PRE_REPAIR_RESULT.md`. `02_OWNER_SUCCESSION_GRAPH.json`, `03_AUTHORITY_OPERATION_CROSSWALK.csv`, `04_TYPED_PENDING.json`, source manifests and the sanitized environment passport retain the broader proof boundaries.
