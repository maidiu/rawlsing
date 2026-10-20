# Validation receipts

## Executed checks

| Check | Result | Evidence |
|---|---|---|
| Current C11/Route B/carrier/I05/Batch owner suite, exact sealed startup | 55 passed in 6.14s | `evidence/runtime_owner_tests.txt` |
| Exact U43 returned branch `98877a1755cab9f8afd453c450f3d1e15001eede` | 64 passed in 32.80s | `evidence/u43_native_transport_tests.txt` |
| Original35/item/evidence/field/authority integrity | PASS: 35 waves, 18,276 exact IDs, 357 input rows, 681 locator rows, 140 hash-bound stages, 446 evidence entries | `evidence/atlas_validation.json` |
| Seven commission hostile examples | 7 PASS, sourcefree/static at stated scope | `validate_atlas.py --native`; observations in `evidence/atlas_validation.json` |
| Fresh preimage SHA-256 / byte size and Git blob identity | 446 PASS, 0 unavailable/mismatch | `verify_preimages.py`; `evidence/preimage_validation.json` |
| Query navigation | Input `GovernedC11Projection.response_slots`, exact item `LiTS|2006/q301_2`, and `WVS|W7` routes resolve | `query_atlas.py` |
| Privacy / independence | No raw SAV/DTA/Parquet/Arrow/database opened, copied or published; local identity locators use logical root aliases; no A48/M48 later draft/return inspected | Bounded search/reuse receipt and manifest |

## Reproduction

From the exact qualified H48 worktree, with `RETURN` set to this return's repository-relative directory:

```bash
PYTHONPATH=. PYTHONDONTWRITEBYTECODE=1 python3 "$RETURN/validate_atlas.py" --native
python3 "$RETURN/query_atlas.py" --input GovernedC11Projection.response_slots --wave 'LiTS|2006'
python3 "$RETURN/query_atlas.py" --wave 'LiTS|2006' --item q301_2
python3 "$RETURN/query_atlas.py" --evidence E1cf3cf939ef4
```

For fresh preimage verification, pass the qualified local metadata roots explicitly:

```bash
python3 "$RETURN/verify_preimages.py" --repo "$H48_WORKTREE" \
  --local-root "$RAWLSING_LOCAL" --trawlsing-root "$TRAWLSING_LOCAL" \
  --harvest-root "$HARVEST_ROOT"
```

This verifier refuses raw source/database suffixes, does not fetch missing objects and does not reconstruct or run survey producers. Historical source digests inside documents are declarations, not original-source files to be opened. Missing local roots limit independent byte reproduction on another host; Git pointers and hashes remain usable.

The runtime-owner command was `python3 -m pytest -q -p no:cacheprovider` over `rawlsing_next/tests/test_pre553_{route_b_production,carrier_execution,discovery_exact,batch_runner,source_backed_c11_facade}.py`, with bytecode writes disabled. U43's command targeted its returned `WORKER_RETURNS/PYAT-R43-U43-ORIGINAL35-PROSPECTIVE-WORKLOAD-R1/tests` in that exact worker checkout, also with bytecode/cache writes disabled. Neither suite is an original35 source-positive qualification.

## Hostile witness meaning

1. A synthetically superseded snapshot is rejected by the actual current positive-authority validator. This demonstrates the firewall, not that a particular real predecessor has a new successor.
2. The real I05 finite compiler accepts an expressly empty declared grammar; the coverage label remains exact-declared-frontier only. Original-U completeness requires independent source evidence.
3. The retained PREP71 source rows total 34 and exclude WVS7; the independently bound original roster totals 35. No inferred 35th permission.
4. Exact B43 guard definitions extracted from its immutable returned blob reject a dummy source path with no grant. No file is opened and no deployment-rights claim follows.
5. Actual positive-authority validation rejects an operation not named by a synthetic exact snapshot. P2/P3C source/relationship authority cannot silently supply every E_pre operation.
6. LiTS-I P2 has 1,198 implementations; the inspected AS2B producer and aggregate receipts cover two response questions. R47 separately identifies the old four-question snapshot. Neither proves whole-source completion or imposes that physical snapshot on current B.
7. Actual Route B requires supplied source/projection/catalog/request/discovery inputs; an empty call raises before work. Its real execution chain composes supplied science rather than issuing it.

## Limits and final grade

The static search covered 140 canonical non-test/non-runtime Python modules plus named exact historical/returned/local producers. AST call existence is not actual production invocation; runtime tests prove only their synthetic fixtures. Closed source identity/current selection, source legal use and scientific eligibility remain separate. The missing old repair-bundle prerequisite and inaccessible other-machine/Library scope are recorded, not erased.

`H48_FORENSIC_ATLAS_RETURNED__EXISTING_PRODUCERS_IDENTIFIED__FINITE_RECOVER_WIRE_TARGETS__NO_ORIGINAL_SOURCE_EXECUTION__NO_SCIENTIFIC_OR_N11_ADOPTION`
