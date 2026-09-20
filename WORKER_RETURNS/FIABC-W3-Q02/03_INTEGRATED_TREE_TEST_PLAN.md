# FIABC-W3-Q02 — integrated-tree test plan

No command in this file was executed by Q02. Browser/GitHub and local commands are deliberately separated.

## A. PRE-MAIN fan-in: source-independent qualification

Run from the root of the Wave-3 fan-in branch after I01-I08, Q01, Q02 are integrated.

### A1. Syntax/import gate

```bash
python -m compileall -q rawlsing_next
```

### A2. Existing PRE553 authority/query/discovery regression spine

```bash
python -m pytest -q \
  rawlsing_next/tests/test_pre553_empirical_objects_authority.py \
  rawlsing_next/tests/test_pre553_empirical_query.py \
  rawlsing_next/tests/test_pre553_discovery_exact.py
```

These guard the inherited semantic owner, exact empirical query surface, and the existing law that diagnostic score cannot become discovery truth/frontier authority.

### A3. Every Wave-3 focused test file, mechanically discovered by governed naming only

```bash
W3_TESTS="$(find rawlsing_next/tests tests -type f -name 'test_fiabc_w3_*.py' -print 2>/dev/null | sort)"
test -n "$W3_TESTS"
python -m pytest -q $W3_TESTS
```

The naming scan is not architecture discovery: it is only test-file collection under the commissioned Wave-3 prefix. If a worker return names an additional focused test outside that prefix, append that exact returned path to this command. Do not omit it.

### A4. I04 byte-preservation gate

After I04 is present, these exact Git-blob checks must pass:

```bash
test "$(git hash-object WORKER_RETURNS/EE-P2R6O/SUPPORT/01_NODE4A_PREDICATE_INPUTS.py)" = "504944f9533b7385d201076e2e834b8a9446dee8"
test "$(git hash-object rawlsing_next/runtime/ee_p2x/01_LITS_CURRENT_RUNTIME_MATERIALIZER.py)" = "9406bacfd928393f6a159a46216aa1f7ec129f34"
test "$(git hash-object rawlsing_next/runtime/ee_p2x/02_WVS7_P2F2_RUNTIME_PACKAGE.json)" = "e04e84b76f8b4eb53905276dd025938bf2e5f6fe"
test "$(git hash-object rawlsing_next/runtime/ee_p2x/05_WVS7_PROJECTION_MATERIALIZER.py)" = "11b28416aac5a4899706150721f2f8ac8bb6ee43"
```

If I04's final return proves a different stable path while preserving the same accepted bytes, substitute only the returned stable path; the expected blobs do not change without a new adjudication.

### A5. Frozen candidate-owner object gate

```bash
test "$(git rev-parse 0b96b8de9aac774566f872cf0630ebd4ddeb70e6:rawlsing_next/pre553_r5_source_backed_adapter.py)" = "d4915e7e6755ba1850756aebff72f982f73a332b"
test "$(git rev-parse 0b96b8de9aac774566f872cf0630ebd4ddeb70e6:rawlsing_next/pre553_source_backed_c11_facade.py)" = "7c509c2098d0030f253344eb3f682471378812a8"
test "$(git rev-parse 0b96b8de9aac774566f872cf0630ebd4ddeb70e6:rawlsing_next/pre553_route_c_accelerators.py)" = "abfdc91a71ef5e18c4a8a6bf62fa65750d8d9889"
```

Do not replace these identities with files at `HEAD` merely because names match.

### A6. Full source-independent suite

Once focused tests pass:

```bash
python -m pytest -q rawlsing_next/tests tests
```

If the repository's governed CI wrapper is required by HQ, run that wrapper as well; this broad pytest command does not supersede a required governed workflow receipt.

## B. P2X execution-rebinding branch: current runtime regression

After the accepted Wave-3 production deltas are transposed onto the HQ-authorized descendant of the existing P2X line, and before any real source is opened:

```bash
python -m pytest -q \
  tests/test_ee_p2x_darwin_court_driver.py \
  rawlsing_next/tests/test_ee_p2x_local_court_driver_integration.py \
  rawlsing_next/tests/test_ee_p2x_local_court_receipts.py \
  rawlsing_next/tests/test_pre553_carrier_execution.py
```

Then rerun the Wave-3 focused suite on this execution tree:

```bash
W3_TESTS="$(find rawlsing_next/tests tests -type f -name 'test_fiabc_w3_*.py' -print 2>/dev/null | sort)"
test -n "$W3_TESTS"
python -m pytest -q $W3_TESTS
```

## C. Browser/GitHub-eligible versus LOCAL-only

### Browser/GitHub-eligible

The following are source-independent and should be run in Browser/GitHub CI where the branch permits it:

- I01 diagnostic formulas, identity law, typed negative states, and non-authority hostile tests;
- I02 effective-N formula/authority/scope/invalid-weight hostile tests using synthetic governed fixtures;
- I03 Candidate-C binding unit tests with synthetic source/projection fixtures, including accelerator deletion and C identity preservation;
- I04 exact byte/hash/dependency tests;
- I05 oracle contract and hostile tests that do not require the real WVS SAV;
- I06 instrumentation tests for overwrite/leakage/RSS/fake-zero/endpoint-size substitution using synthetic subprocesses/fixtures;
- I07 succession schema/preflight hostile fixtures;
- I08 terminal-verifier hostile fixtures;
- Q01 hostile cross-implementation tests;
- existing PRE553 regressions listed above.

### LOCAL-only

Do **not** fabricate Browser results for:

- verification of the real LiTS-I source carrier SHA-256;
- verification of the real WVS7 source carrier SHA-256;
- WVS oracle materialization from exact SAV bytes;
- any LiTS oracle step that the I05 implementation explicitly requires to re-open the exact source bytes;
- R6X mutation of the real stopped P2X work root and ledger;
- any premeasurement six-cell capability check that opens real source bytes;
- actual fresh process source×candidate lifecycle execution;
- Darwin x86_64 process-local RSS/CPU/I/O measurements;
- measured P2X itself.

## D. Required sibling-return command reconciliation

Each implementation worker was commissioned to return the exact commands it expects to be run later. During fan-in, HQ must concatenate those exact command blocks and compare them against Sections A-C above.

Stop if a sibling return requires a materially different authority root, candidate owner, source hash, workload, or execution order. Do not choose one command arbitrarily. A path/name difference with identical semantics may be mechanically reconciled; an authority/identity difference requires adjudication.

For I05, I07, and I08 in particular, Q02 does not invent CLI flags before those implementations exist. The local operator must run the exact materializer/preflight/verifier command written in each final worker return. **If any of those returns omits a deterministic command for its local obligation, the fan-in is incomplete and measured P2X remains unlawful.**
