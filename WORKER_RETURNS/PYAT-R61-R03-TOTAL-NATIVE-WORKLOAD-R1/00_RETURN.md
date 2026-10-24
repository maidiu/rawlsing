# R61 R03 — governed frontier to native issued workload

**Disposition:** CANDIDATE_FOR_INDEPENDENT_REVIEW. Not self-adopted.

**Scope:** sourcefree TEST_ONLY only. No original source, original science,
R04/R05 custody, CI/prod, N11/N12, Sorok or J52/W52 is claimed.

## Identity

- Branch: `agent/opencode-pyat-r61-r03-total-native-workload-r1`
- Startup: `813775c07f0831605b6484a1d82afada30d85968`
- Predecessor candidate: `5f3cee7cb7a9b53af266b05a4c8db01a53a13add`
- Code commits: `d22319f2d6031a9766d7afe8bed205d9219f5b2a`,
  `db79e3913050039ddb55ba62b08bd764c79f1035`,
  `54a2c427c94767b29653426f7cfb55db9cf22aac`
- Recovered U43 transport blob: `31e84f49d624f5524906e9e7839d2873106f8249`
  (unchanged)

## Delivered

1. `compile_governed_frontier` consumes the caller-frozen R01
   `SourceInventory` / `GrammarPolicy` / `ScientificFrontier` and lowers every
   operation through `lower_frontier`. No operation-list or easier subset is
   supplied. Construction refusals remain explicit `UNSUPPORTED_RUNTIME`.
2. `execute_governed_frontier` issues one TEST_ONLY `NativeWorkload`, admits the
   exact envelope, and runs the actual C11 -> Batch -> I05 path once. It does
   not call U43's unbounded Route B discovery path, avoiding duplicate I05
   execution. Results are anti-joined at exact candidate and operation IDs.
3. The complete operation ledger preserves `NOT_ELIGIBLE`, `UNSUPPORTED`,
   `PENDING`, `SUPPORTED`, `VALID_EMPTY`, and `UNKNOWN` states, exact
   receipt/fact refs, native families, and all issued/expected IDs. Budget
   truncation is `PENDING` and is not executed.
4. `bind_recursive_workload` verifies an R01 retained campaign issuance plan,
   receipt refs and handoff refs, then binds every expected D=3 operation to its
   exact receipt/fact. It exposes root and immediate-parent contrasts, parent
   lineage, unissued work, activation waiting/stopped/nonwinning entries, and
   cold-restored campaign material without issuing or rerunning discovery.
5. Existing unary `compile_universal_workload` / `execute_universal_workload`
   and U43 exact custody remain intact.

## Actual proof

Command:

```text
/usr/local/bin/python3 -m pytest \
  rawlsing_next/tests/test_universal_workload.py \
  rawlsing_next/tests/test_universal_grammar.py \
  rawlsing_next/tests/test_universal_source_projection.py \
  rawlsing_next/tests/test_pre553_recursive_handoff.py \
  rawlsing_next/tests/test_pre553_discovery_exact.py \
  rawlsing_next/tests/test_pre553_batch_runner.py \
  rawlsing_next/tests/test_pre553_carrier_execution.py \
  rawlsing_next/tests/test_pre553_route_b_production.py \
  -q -o addopts=''
```

Result: **120 passed**, 0 failed/errors/skips. `junit.xml`, `pytest.log` and
`proof_witness.json` are attached.

Observed sourcefree run (`proof_witness.json`):

- 150 eligible operations -> 147 supported -> 150 exact native candidates.
- 3 eligible operations retained as `UNSUPPORTED_RUNTIME`.
- 150 native I05 receipts, 1 Batch receipt, 330 exact fact refs.
- Candidate anti-join, operation anti-join, and total eligible accounting all
  `no_drop_ok` / `accounting_ok`.
- A budget-limited run leaves exact operation IDs in `PENDING` with no receipts.
- Mutating one observed source value while preserving the declared edition
  changes **147 operation fact sets / 660 fact refs** through the same
  compilation; restoring the value restores the same fact refs.
- D=3 campaign: generations 1/2/3 each issue 4 operations, with 2 root and 2
  parent contrasts. Generation 2 independently shows
  `ROOT_RELATIVE=DISCOVERED_RESULT_SUPPORTED` versus
  `IMMEDIATE_PARENT_RELATIVE=VALID_EMPTY`, plus minority activation entries.
  Cold restore preserves operation material and leaves execution count 3 -> 3.

## Limits

The static governed-frontier proof is limited to scalar source topology;
repeated/qualified occurrences remain typed lowering refusals rather than being
silently flattened. Existing R03 repeated SAV/DTA tests remain green. R04 cold
durable custody and R05 grades are not claimed. Independent R03V review is
required; this return is not an acceptance.
