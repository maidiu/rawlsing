# PYAT #997 S1-E — actual P0/P1 execution, repair and native witness

**Disposition:** `P0 PASS`, `P1 PASS`, `G5 PENDING_INDEPENDENT_RECEIVING`.

This is the missing execution the A/B exchange could not produce. The frozen
sourcefree Q2 → S2-C → S2-D chain and the P1 receipt/fate join were run on real
repository Python with real SAV/DTA TEST_ONLY fixtures. No original35 source,
issuer, science, production or G5 authority is claimed.

## Immutable starting point and final code

- Mandatory frozen start:
  `2c476e739a263dd0069b54706c6cfa63b07190c1`
  (PR #1024 head, Agent B R5).
- Isolated branch:
  `agent/pyat997-s1e-exec-repair-20261113`.
- Code/test commit:
  `7b1795981ccc79c9c4700c5ec7e39507d6c88b0b`.
- Protected PRE-MAIN `integration/pre-main-reconciliation-r1` was not touched.
- Evidence commit SHA is the commit containing this directory; it is reported
  with the draft PR and final handoff message.

Changed blobs at the code/test commit:

| file | blob |
|---|---|
| `rawlsing_next/pre553_source_postconsumer_receipts.py` | `9293370a6022d622daeaff7cefb6d31cbeadff8c` |
| `rawlsing_next/tests/test_pyat960_s1e_native_fact.py` | `ee6434d78dd9ceef77ea074f1f6c69b12e177613` |
| `rawlsing_next/tests/test_pyat997_s1e_saved_native_first_consumer.py` | `4435fa5ec84114576dcd60469084605376b22680` |
| `rawlsing_next/tests/test_pyat997_s1e_saved_source_bridge.py` | `135a0e32021b839a753d81f16a771ef17cfca2ed` |
| `rawlsing_next/tests/test_pyat997_s1e_source_saved_body_bridge.py` | `beae72cd428ba8d67fe58c5d2eebf918659c07a9` |

The accepted S2-C writer, S2-D saved reader, Q2 producer and native engine were
not edited.

## Environment actually used

| | macOS host | Linux host |
|---|---|---|
| OS | Darwin 22.3.0 x86_64 (macOS 13.2.1) | Ubuntu kernel 7.3.0 x86_64 VM |
| Python | 3.11.3 | 3.12.16 |
| pytest | 9.0.2 | 9.2.0 |
| PyArrow | 22.0.0 | 26.0.1 |
| DuckDB | 1.5.2 | 2.0.0 |
| pyreadstat | 1.3.2 | 1.3.7 |
| pandas / numpy | 2.3.1 / 2.3.2 | 3.1.1 / 2.5.4 |
| `/proc/self/fd` | absent | present |

Machine-readable manifests and witness hashes are in
`evidence/p0p1_runtime_darwin.json` and
`evidence/p0p1_runtime_linux.json`. Every SAV write embeds a writer timestamp,
so separately emitted fixtures are run-local; **within one witness run**, exact
source replay reproduces the baseline roots, fact and P1 result, and a changed
valid cell changes them. The Linux JSON is from the final re-run; earlier Linux
runs had different fixture timestamps and therefore different root/fact hashes,
with the same SUPPORTED 5/5 result.

## Commands and raw outputs

Primary P0/P1 court (exit 0 on both hosts):

```bash
python -B -m pytest -q -o addopts='' -p no:cacheprovider \
  rawlsing_next/tests/test_pyat997_s1e_saved_native_first_consumer.py \
  rawlsing_next/tests/test_pyat997_s1e_saved_source_bridge.py \
  rawlsing_next/tests/test_pyat997_s1e_source_saved_body_bridge.py
```

- `evidence/test_p0p1_primary_darwin.txt` — **32 passed**, exit 0.
- `evidence/test_p0p1_primary_linux.txt` — **32 passed**, exit 0.
- No skips in either run.

Inherited suites:

| evidence file | result |
|---|---|
| `test_inherited_core_darwin.txt` (Q2 source-I02, transport, counter-attack, native bridge/fact, operation anti-join, S1-C frozen census, S2-B direct I02, S2-B external certificate, S2-C estate) | **102 passed, 32 failed** |
| `test_inherited_s2b_linux.txt` (same S2-B direct I02 + external certificate files) | **55 passed, exit 0** |
| `test_inherited_s2d_darwin.txt` (S2-D saved admission, five readers incl. completed/partial/absent/resume, G5 scope, Batch runner, direct estate I03, universal workload/grammar) | **102 passed, exit 0** |
| `test_inherited_regression_darwin.txt` (empirical query, source-backed facade, source projection, GT34 Q2 materialization, source-local admission) | **100 passed, 3 setup errors** |
| `test_gt34_pre_existing_base.txt` (same GT34 file at frozen `2c476e739`) | **2 passed, same 3 setup errors** |

The 32 Darwin core failures are the explicit Linux-only descriptor-pinned
`VerifiedExternalI02` gate (`descriptor-pinned SQLite cold verification requires
Linux /proc/self/fd`). All 55 tests in those two files pass on the Linux host.
They are not part of the accepted sourcefree S2-C/S2-D P0 path and are not
hidden as a green result.

The 3 GT34 setup errors are pre-existing at the frozen starting commit
(`accepted Q86 producer path did not reproduce accepted release identity`) and
are unchanged by this branch. They are outside this S1-E scope.

Runtime witness producer (exit 0 on both hosts):

```bash
python -B \
  WORKER_RETURNS/PYAT997_S1E_EXEC_REPAIR_20261113/evidence/run_p0p1_evidence.py
```

## P0 — actual result: PASS

One source snapshot/decode/cell pass, then exact 13-family bodies into the
unchanged S2-C Parquet/Zstd estate, producer termination, and cold S2-D native
first reader:

- source snapshot opens: **1**; declared source reads: **1**; decode calls:
  **1**; cell passes: **1**; legacy full C11 builds: **0**.
- source rows: **5** (tiny TEST_ONLY fixture; not production size).
- 13 family bodies transported and cold-retrievable:
  `EmpiricalUniverse 1`, `RespondentIdentity 5`, `QuestionVariableBinding 1`,
  `RespondentEvent 5`, `RoutingEligibilityFact 5`,
  `EmpiricalCoordinateFact 5`, `WeightMeasureFact 0`,
  `AuthoritySnapshot 7`, `SourceUniverseRelation 0`,
  `EmpiricalPredicateReplayBinding 0`, `ComparatorReplayBinding 0`,
  `DiscoveryBranchReplayBinding 0`,
  `StructuralAdmissionReplayBinding 0`.
- typed absences preserved: `WeightMeasureFact NOT_APPLICABLE`,
  `EmpiricalPredicateReplayBinding NOT_APPLICABLE`,
  `StructuralAdmissionReplayBinding NOT_APPLICABLE`,
  `ComparatorReplayBinding DEFERRED`,
  `DiscoveryBranchReplayBinding DEFERRED`,
  `SourceUniverseRelation DISTINCT_BY_DEFAULT`.
- 14 Parquet/Zstd files in the estate (13 logical families + ReplayManifest),
  no competing SQLite body corpus, no `.s1e-body-journal-*` or `.s2c-stage-*`
  leftovers. Retained estate = **356,591 bytes** on both final witness runs.
- external I02 roots: `handoff.roots == estate_receipt.i02` exactly; the
  manifest and release/replay/source/universe refs are recorded in the JSON.
- cold native I03 from the saved source: `SUPPORTED`,
  denominator **5**, numerator **5**, cells `0:3`, `1:2` on both hosts.
  Darwin final fact `...:1daf2808653c13d7...`; Linux fact hashes are run-local
  because of the fixture timestamp (final re-run `...:6235fe9084fe388e...`).
- real I05 discovery receipts executed; issued Batch unit(s) complete; the
  normal `execute_issued_workload` saved path completed with no source factory.
- changed valid source cell → changed native fact:
  Darwin baseline `...:3b1b516d9e62...` vs changed `...:0c5233893602...`;
  bridge cells baseline `[("0",2),("1",2),("2.0",1)]` vs changed
  `[("0",2),("1",3)]`.
- exact source replay → exact baseline fact and exact P1 result hash;
  roots and fact refs restore exactly within the host.
- negative controls preserved and passing: missing emitted body, concealed
  unresolved routing, zero eligible routing denominator, routing census drift,
  altered measure preimage, Q2↔R03 original-frontier drift, frozen source/
  science census drift, forged held root, mixed-source release identity, and
  CURRENT revocation.

## P1 — actual result: PASS

Original frozen S1-C source/scientific census → Q2 source realization →
qualified saved C11 → compiled/issued R03 workload → native I03/I05/Batch
receipts → postconsumer operation fate join:

- 22 original operations = 22 issued dispositions = 22 joined rows;
  anti-join missing **0**, extra **0**.
- original/issued fate census: `ELIGIBLE 8`, `HELD 14` (identical).
- postconsumer states: 6 `TEST_ONLY_SAVED_NATIVE_DISCOVERY_RECEIPTED`,
  2 `ELIGIBLE_PENDING_VERIFIED_NATIVE_RECEIPT`,
  14 `NONELIGIBLE_FATE_PRESERVED`.
- `positive_native_linked_operations = 6`;
  `pending_eligible_operations = 2`;
  held/unknown rows with receipt refs = **0**; issue grants created = 0.
- no fabricated completed receipt: the two pending eligible rows have zero
  receipt refs; the absent-Batch test confirms they stay pending.
- no held promotion: all 14 HELD rows are preserved verbatim with zero
  postconsumer receipts; the forged HELD→ELIGIBLE case refuses before any
  receipt promotion.
- issuer decision, envelope hash, saved release ref, estate manifest SHA,
  operation lineage and CURRENT status are recorded in the evidence JSON.
- completed vs partial/absent/resume behavior is covered by the 102-passing
  S2-D suite (`test_saved_completed_partial_absent_use_existing_resume` and
  the Batch resume courts), using the existing native machinery.

## Repairs actually committed

1. **P1 refusal ordering (implementation).**
   `join_saved_source_operation_fates` now checks the compiled frontier's
   per-operation disposition and claim class *before* the aggregate census
   comparison. A HELD/UNKNOWN row forged to ELIGIBLE now raises the documented
   `Q2_OPERATION_FATE_OR_CLAIM_PROMOTED`, not a masked generic census drift.
   The aggregate census check remains and still refuses census-only forgery.
2. **Exact-restoration witness (tests).**
   Re-emitting a SAV fixture embeds a new writer timestamp, so a second
   separately written "restored" file was not an exact source restoration.
   The three restoration tests now replay the baseline source bytes while
   still performing a fresh source open, Q2 projection, S2-C write and cold
   S2-D read.
3. **Real native I03 / canonical domain (tests).**
   The native saved-source tests now use the repository's accepted
   native-corrected fixture (routing authority and canonical values) and derive
   the issued TEST_ONLY target domain from the canonical values actually
   carried by the saved bodies. The first-consumer helper now selects a
   `SUPPORTED` cold I03 fact rather than returning the first typed negative
   fact.
4. **Stale refusal-code expectation (test).**
   The `unresolved_routing` hostile case now expects Agent A's preserved,
   more precise `Q2_REALIZATION_ROUTING_CENSUS_DRIFT`, which is the documented
   result of the flag/census consistency repair. The case still refuses; no
   negative test was weakened or deleted.

## Runtime economics (measured, not estimated)

Tiny five-row fixture only; **no 100,000-respondent or 6 GiB claim is made**.
Peak process RSS: **145.3 MiB** Darwin, **179.0 MiB** Linux. Journal staging:
78,149 bytes; Q2 spool: 31,090 bytes. Cold saved-native I03 first reader:
~0.039 s Darwin / ~0.019 s Linux (final re-run). I05 ~0.12/0.11 s;
Batch ~0.13/0.10 s; P1 join ~0.15/0.20 s. Whole evidence script ~5 s / ~6 s.
These are witness costs, not production throughput. Physical engine performance
remains #1006.

## Exact remaining boundaries

- `G5 = PENDING_INDEPENDENT_RECEIVING`. This execution cannot accept itself.
- No original35 source/science/issuer/production authority is claimed or
  created.
- The Linux-only S2-B `/proc/self/fd` courts pass on Linux but cannot run on
  the macOS host; this is an explicit host dependency, not a fabricated skip.
- The 3 GT34 Q86 setup errors are pre-existing at the frozen start and remain
  owned outside this S1-E branch.
- No protected merge, no S3, no PRE-MAIN change.

## Frozen packet for a distinct nonauthor G5

Provide the receiver with:

- this directory and `evidence/p0p1_runtime_{darwin,linux}.json`;
- all raw `evidence/test_*.txt` outputs and exit codes;
- code/test head `7b1795981ccc79c9c4700c5ec7e39507d6c88b0b`
  (plus the evidence commit SHA from the draft PR);
- starting head `2c476e739a263dd0069b54706c6cfa63b07190c1`;
- the five changed blob IDs above.

The receiver should re-run the three primary files, compare the P0 roots/fact
refs and P1 census/anti-join on an independently controlled host, and verify
that the Linux-only inherited S2-B courts pass there.
