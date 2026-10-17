# Exact operators, imports and physical tests

All 33 staged input files are exact preimages from `eede2b8bdb9fcdcc1d4187912f8e00773869c22c` and unchanged from startup. `SOURCE_INPUTS.json` records Git blob SHA-1, SHA-256 and size for each. `COURT_CODE_PIN.json` fixes the experiment code and inputs before final cold runs. The original preregistration, source pin and metadata-root files remain byte-identical to commit `8f6e14ce5`.

The test worker verifies preimages before imports, removes checkout import fallback, disables external pytest plugins, rejects network connections and SAV/DTA/POR/ZSAV opens, and records every imported project module's actual file under the verified stage root and its hash. Published `__file__` values use `$RETURN/runtime/pinned` in place of the personal worktree prefix. `actual_path_under_verified_pin=true` is checked on the resolved physical path, not inferred from the module name.

The actual call chain is:

`ExactPhysicalCellStream -> GovernedC11Projection -> build_source_backed_c11_repository -> C11Repository + C11LogicalRelease -> CarrierNeutralResearchExecutor.execute_i03 / execute_i05 -> BatchExecutionRunner actual callbacks -> exact result-ref outer join -> evaluate_oc01_pre553_source_local`.

Route-B direct composition and parity are also executed in the retained author suite. No accepted native owner was copied into an experimental replacement implementation. The source-free fixture's source SHA is a declared test identity, not a verified original survey checksum; the physical SAV/DTA decoder is not invoked.

## Observed quantitative positive

There are three test respondents; Y for R3 is NOT_ELIGIBLE. The raw Y denominator is **2**, with Y=0 count 1 and Y=1 count 1. The governed weighted denominator is **3**, with Y=0 weight 1 and Y=1 weight 2. The exact fractions are 1/2, 1/2 and 1/3, 2/3 respectively. The two actual I03 fact objects retain their full cell distributions, member refs, risk ref, query/ref lineage, weighted/raw distinction and `UNCERTAINTY_UNQUANTIFIED` state. The third Batch job actually invokes exact bounded I05 and retains its genuine discovery receipt/frontier provenance.

The actual OC01 receipt selects those exact two fact refs at the TEST_ONLY source-local ceiling. Full fact payloads and consumer receipt are in `observations/native_positive.json`. The consumer policy does not itself numerically recompute or authenticate the source; this return verifies its selected refs against the preceding facts and retains the values. This is not a source-original publication or N9 world consumer.

With a missing weight, native I03 returns UNAVAILABLE and the real OC01 consumer refuses required missing evidence. With an empty discovery, VALID_EMPTY survives in the exact I05 receipt. A native source/projection hash mismatch is rejected before reading the supplied cell stream. Removed projection authority is rejected by the real Route-B gateway; this is authority availability withdrawal, not proof of a signed source-artifact revocation protocol.

## No-drop finding

`BatchExecutionRunner.summary().full_coverage` means full coverage of the supplied **BatchManifest**. A deliberately incomplete, unguarded two-unit native subset actually executes and reports FULL_MANIFEST_COVERAGE while missing the third independently expected job. `observations/native_subset_characterization.json` preserves this result, with no consumer call. This is consistent with Batch's nonsemantic scheduling contract; it is not an original-estate completeness guarantee or a demonstrated Batch defect.

The experimental independent multiset outer join checks expected job identities before execution, exact unit/result refs after execution, and expected-work coverage again before consumption. Missing raw, weighted or discovery requests produce HOLD with independently instrumented **zero I03, zero I05 and zero consumer calls**. Duplicate/extra and same-count replacements cannot satisfy the join. This return code is not installed original E_pre governance; a requester controlling both expected root and candidate cannot confer source competence.

## Reproduction

From the assigned checkout, define `O35E=WORKER_RETURNS/PYAT-R28-O35E-ORIGINAL-35-ELIGIBILITY-NATIVE-R1`, then run:

```sh
python3 "$O35E/repro/stage_inputs.py"
"$METADATA_PYTHON" "$O35E/repro/build_inventory.py"
python3 "$O35E/repro/capture_source_authority.py"
python3 "$O35E/repro/run_courts.py"
```

`METADATA_PYTHON` is the already-established Python with pandas; recorded execution used Python 3.12.14 / pandas 2.2.3. Native courts use the existing Python 3.11.3 / pytest 9.1.1, with no package installation. Do not rerun `freeze_expectations.py` over the sealed files. Reproduction reuses the existing exact freeze; it cannot issue original rights.

`observations/process_receipts.json` gives exact subprocess arguments, exits, stdout and JUnit paths. `o35e_final.xml` and `o35e_cold.xml` each contain 26 PASS; `native_c11_route_batch.xml` contains 27 PASS. These are **53 unique passing tests**, with the cold 26 a repetition, not 79 unique scientific cases. `native_d07_missing_fixture.xml` is a real collection error, exit 2, for the missing retained helper. It is not a PASS or a native consumer scientific failure. The executable orchestrator expects and exposes that known fixture limitation.

Earlier `o35e_combined.xml` records 25 PASS/1 return-test transport FAIL; `native_owners.xml` records the initial collection error. Neither is deleted or retrospectively greened. `STAGING_LIMITATIONS.json` and the environment passport preserve the partial optional-suite closure. The actual final core imports are in the corresponding `*_imports.json` files.
