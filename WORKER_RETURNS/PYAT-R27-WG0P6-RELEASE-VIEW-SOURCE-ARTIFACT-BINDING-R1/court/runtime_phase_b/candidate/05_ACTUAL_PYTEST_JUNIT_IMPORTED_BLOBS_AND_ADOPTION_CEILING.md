# Execution ledger, immutable imports and independent-review handoff

Expectation freeze `263ec61bd5bc6c12d121286bcd7a1734ae8c276d`; implementation/evidence commit `a847e39fe4576a5b6213d121d6ed8989770c0178`. Actual final candidate SHA256 `c74b34d14c5a79993e7b56908ac017b2e35a97df422460f4d62beb30b63821f8`. Each final candidate court records this same source digest. Python3.11.3 / pytest9.1.1, shared Git object store and isolated sparse commissioned branch; no helper/model switches, new clone, protected code change or external model call.

| Court | Tests | Pass | RED | Error | Skip | Exit |
|---|---:|---:|---:|---:|---:|---:|
| historical_p2 | 29 | 29 | 0 | 0 | 0 | 0 |
| historical_p3 | 36 | 36 | 0 | 0 | 0 | 0 |
| historical_j | 44 | 24 | 20 | 0 | 0 | 1 |
| historical_k_on_p3 | 11 | 1 | 10 | 0 | 0 | 1 |
| ported_j | 44 | 44 | 0 | 0 | 0 | 0 |
| ported_k | 11 | 11 | 0 | 0 | 0 | 0 |
| wg0p4 | 69 | 69 | 0 | 0 | 0 | 0 |

Each name maps to `observations/<name>.stdout`, `.xml` and `.terminal.json`; full command/cwd aliases, return code, counts and source hashes are retained. Personal filesystem root aliases are the only log redaction. Original imported native Git blobs and actual module.__file__ aliases are in baseline/source_custody and selector. All27 immutable preimages were independently hashed with actual Git object format and git hash-object. No mock native C11/I03/Batch consumer or package-substitute stubs are used. Owner's populated_data_execution_claim remains false.

Historical controls are truthful prospective failures, not xfails. WG0J exact44 on originalP2 reproduces24 PASS/20 RED; WG0K exact11 full-module tests on originalP3 reproduce1 PASS/10 RED. These11 full-source cases are not its historical extracted15+4 court. The original36 P3 and29 P2 suites are unchanged historical runs, not automatic WG0P4 interface acceptance. Candidate ports44/11 retain their old files byte-identical and add separately versioned adapters. Admission refusals preserve no-stale-product expectations; immutable binding/read APIs replace attempts to corrupt mutable objects. One K foreign-grant expectation now tests explicit rejection rather than silent normalization. All case mappings and original RED text are in01.

The69 additional author cases are newly written after the independently frozen input/output expectations; they are not the separately precommitted WG0L65. All final candidate cases pass with no error, skip or xfail. Initial failed runs remain in `*.attempt1.*`: real inherited invalid MISSING_CODE producer fixed only in WG0P4-owned fixture code, and a test's wrong denominator-member field spelling fixed without changing expected R2/R3. No historical source/oracle was edited. Original-source and independent-adoption holds persist.

Reproduce from repository root (the `<RETURN>` alias denotes this owned return directory):

```sh
python3 <RETURN>/repro/reconstruct_sources.py
python3 <RETURN>/repro/run_suites.py historical_p2 historical_p3 historical_k_on_p3 prepare_historical_j historical_j
python3 <RETURN>/repro/run_suites.py prepare_native ported_j ported_k wg0p4
```

The runner fixes pytest configuration, disables external plugin autoload, uses only pinned native closure and the declared per-court module path, and stores genuine subprocess output/JUnit. Generated sourcefree runtime/keys stay ignored. Historical suites intentionally exit1 within recorded subprocesses; inspect terminal JSON rather than treating their expected failures as command success.

Existing Pyat HQ should resolve the final pushed branch SHA, verify startup ancestry/owned-directory-only diff and this packet manifest, then send the exact candidate to existing independent WG0L PhaseB. WG0L must use its own frozen65 and genuine imports/processes, not rubber-stamp author69. Only a separate competent reviewer and Pyat HQ can adjudicate a sourcefree method. No self-acceptance, original35/N11/N12 or V3 claim.

Import accounting:14 native modules are statically staged and Git-blob verified;12 are actually imported in the native baseline, including all required C11/I02/I03/Batch/objects/integrity owners. Discovery_exact and runtime_composition are staged optional dependencies, not claimed imported or executed. The final structural verifier initially conflated staging with imports; this was corrected without changing the candidate or scientific test results.
