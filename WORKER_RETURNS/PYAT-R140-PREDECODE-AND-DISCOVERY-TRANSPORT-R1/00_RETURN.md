# R140 — predecode source-read + native discovery transport

**Status:** `TWO_SOURCEFREE_TRANSPORT_EXTENSIONS_IMPLEMENTED__SYNTHETIC_ONLY__NOT_SOURCE`
**Base:** `98612c6d511d54acdf304ab4086547192573f403`
**Contract:** `PYAT_CONTROL_ROOM/CONTINUOUS_DEVELOPMENT/R139_PRODUCTION_INGRESS_CONTRACT.json` at `8a6760daeccfc09eade88fa4365d06a86509af1a`
**Commission:** `WORKER_COMMISSIONS/PYAT-R140-PREDECODE-AND-DISCOVERY-TRANSPORT-R1/00_COMMISSION.md`
**Source reads:** 0. No source, host, scientific, or current grant is issued.

## 1. Externally authenticated predecode source-read transport

New `rawlsing_next/pre553_source_read_admission.py` is a transport over the
unchanged R04 `decode_sav`/`decode_dta` owner. It does not issue rights and does
not create a grant.

- `SourceReadRequest` is metadata-only: source id, edition SHA, format, custody
  locator binding, host, purpose, consumer use, `SOURCE_RESPONSE_DECODE`,
  `EXACT_FILE`, metadata/use freeze refs, and semantic-use scope.
- `IssuedSourceReadDecision` is supplied by an external trusted resolver. It
  carries exact decision/source-permission refs, all source/host/purpose/use and
  freeze fields, currentness, revocation, effective interval and retention/
  export limits.
- `decode_with_source_read_permission` resolves the exact current decision
  **before** touching `source_path`; only then calls the unchanged decoder with
  the decision's independently granted expected SHA and whole-file extent.
- It re-resolves the same exact decision after decode. On revocation, changed
  decision, decoded edition/format mismatch, or other failure it closes the R04
  incidence and releases nothing.
- Selected-columns or any non-`EXACT_FILE` extent is refused. No final
  projection/universe hash is required, so source access is not circular.
- The trusted resolver is external deployment infrastructure. The test resolver
  is a fixture and is not source permission.

Proved: authorized synthetic whole file uses the unchanged R04 path (2 rows, 6
cells, matching source SHA, physical metadata digest and custody snapshot); 14
malformed/foreign/stale/revoked cases produced zero decoder calls and zero
`open`/`stat`/`read_bytes` source touches; post-decode revocation closed the
incidence and returned no capability.

## 2. External-authority full-frontier discovery transport

`pre553_native_workload_binding.py` and `pre553_universal_workload.py` now accept
already-exact external query and discovery `AuthoritySnapshot`s; they do not
generate ALLOW authority on this path. Existing `lower_frontier`/native grammar,
candidate accounting, `RuntimeObjectCatalog`, `DiscoveryAuthority`, `admit`, and
I05 are reused.

- `prepare_production_discovery` accepts full inventory/policy/frontier and
  external query/discovery authorities, prepares the complete unsigned
  `NativeWorkload` with full declared discovery plan, exact descriptor, root
  inputs and external record left separate.
- `execute_production_workload` now transports discovery-only workloads through
  the existing Batch/C11/I05 owners after unchanged
  `admit(...allow_test_only=False)`, using actual native receipts, not a second
  discovery loop or a scalar wrapper.
- Source/grammar/risk/measure/operation/frontier/descriptor/currentness
  mismatches refuse; the record is externally constructed in the test only.
- The explicit TEST_ONLY helpers and their scope remain unchanged.

Proved synthetic native discovery: 9 catalog queries, 147 expected operations,
150 declared candidates, 150 covered candidates, 150 native receipts, 98
`DISCOVERED_RESULT_SUPPORTED` and 52 honest `VALID_EMPTY`; 330 native facts (314
supported, 16 zero-support); one supported fact has arity 2, four observed cells,
raw numerator 6 / denominator 6. No-drop ledger has zero missing/unexpected/
duplicate/semantic mismatches. Repeat execution restored identical receipt refs,
fact refs, evaluated frontier and replay.

## Actual focused counts

- Production + source-read focused tests: **18 passed** (13 production, 5 source-read).
- Listed repeated-positive/test-only regressions: **4 passed**.
- No skip is counted as pass.

## Refusals actually exercised

- Predecode: non-current/expired/revoked, foreign source/edition/format/custody/
  host/purpose/consumer/operation/extent/freeze/semantic scope, external resolver
  failure, post-decode revocation.
- Discovery: foreign query source/universe/risk, foreign discovery source/universe/
  risk, wrong discovery operation, policy/frontier hash mismatch, foreign
  descriptor carrier/measure, non-current record before native execution.

## Limits

Synthetic fixtures and fixture resolvers/authorities only. `ORIGINAL_SOURCE_GRANTED`
is a transport label, not actual source/scientific issuance. No all35,
representative milestone, F1–F8/global, learned/FF/V553, actor, M1-for-all,
R09/CI/prod, N11/N12, Sorok, J52/W52 or source-access claim. R138 independent
review and R131 stopped status are untouched. Core decoder/issued/admit/I05/
grammar/learned/FF/CI/prod owners were read-only.

Detailed receipt: `evidence/PROOF_RECEIPT.json`.

## Code pins

- `rawlsing_next/pre553_source_read_admission.py`: `652ea3cdf0f53cd9ce14c4419486f6c1a81f3584`
- `rawlsing_next/pre553_production_binding.py`: `ad5abfe7d71b76eb421f729c1b88e4ac56a59591`
- `rawlsing_next/pre553_native_workload_binding.py`: `b7ffe2f69f34f665158d9dfa267096fad2151444`
- `rawlsing_next/pre553_universal_workload.py`: `95d19e9fa7a8d222e8b429578a8fd3efdc79f8bd`
- `rawlsing_next/tests/test_pre553_production_binding.py`: `41d4a40a1c8ab853cf5c912cee36fa8e66f1bc86`
- `rawlsing_next/tests/test_pre553_source_read_admission.py`: `b48641813eea1fc78778c65379505d7c46d641b3`
