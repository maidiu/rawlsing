# FIABC-W3-I07 — Hostile Fixture Coverage

The executable fixture set is `rawlsing_next/tests/fixtures/fiabc_succession_preflight_hostile_cases.json`. Tests load this file and require every listed expected failure code to appear in a BLOCK result.

## Wave-2 B05 known blocker replays

| ID | Fixture mutation | Required rejection |
|---|---|---|
| KB01 | adopted owner but missing binding / LIVE receipt | `PF_EXECUTABLE_BINDING_MISSING`, `PF_LIVE_RECEIPT_MISSING` |
| KB02 | stale exact binding ref | `PF_BINDING_REF_STALE`, `PF_REF_UNRESOLVED` |
| KB03 | wrapper points at wrong owner | `PF_BINDING_OWNER_MISMATCH`, `PF_WRAPPER_SHADOWS_CURRENT_OWNER` |
| KB04 | receipt does not prove current post-repair live consumption | `PF_LIVE_RECEIPT_MISSING`, `PF_LIVE_RECEIPT_PREDATES_REQUIRED_REPAIR` |
| KB05 | candidate output/self replay used as expected parity truth | `PF_ORACLE_NOT_PREOUTPUT_FROZEN`, `PF_ORACLE_DERIVED_FROM_CANDIDATE_OUTPUT`, `PF_SELF_REPLAY_USED_AS_PARITY` |
| KB06 | unresolved/asymmetric/nonlocal/overwritten/documentary accounting | `PF_EQUAL_WORK_ACCOUNTING_UNRESOLVED`, `PF_METRIC_NOT_CANDIDATE_LOCAL`, `PF_METRIC_OVERWRITTEN`, `PF_DOCUMENTARY_VALUE_MISLABELED_OBSERVED` |
| KB07 | LiTS-C partial/synthetic production preimages | `PF_SOURCE_CANDIDATE_CAPABILITY_MISSING`, `PF_PARTIAL_PREIMAGE_SET`, `PF_SYNTHETIC_FIXTURE_SUBSTITUTION` |
| KB08 | WVS-C portability relabeled not-applicable | `PF_SOURCE_CANDIDATE_CAPABILITY_MISSING`, `PF_SOURCE_PORTABILITY_UNPROVED`, `PF_UNAUTHORIZED_NOT_APPLICABLE_ESCAPE` |
| KB09 | missing semantic authority replaced by implementation/binder evidence | `PF_AUTHORITY_MISSING`, `PF_SEMANTIC_INFERENCE_SUBSTITUTION` |
| KB10 | common failure misclassified and retry lifecycle stale/out-of-order | `PF_FAILURE_SCOPE_MISCLASSIFIED`, `PF_LIFECYCLE_ORDER_MISMATCH`, `PF_TERMINAL_HISTORY_STALE_FOR_RETRY` |
| KB11 | producer-to-consumer contract mismatch | `PF_PRODUCER_CONSUMER_CONTRACT_MISMATCH` |
| KB12 | stale verifier contract plus unclosed replay provenance | `PF_PRODUCER_CONSUMER_CONTRACT_MISMATCH`, `PF_REPLAY_PROVENANCE_UNCLOSED` |

## Wave-2 B05 false-PASS challenges

| ID | False-PASS attempt | Required rejection |
|---|---|---|
| FP01 | floating `HEAD` evidence | `PF_FLOATING_OR_FUZZY_REF` |
| FP02 | historical owner presented as current | `PF_OWNER_SUPERSEDED_OR_HISTORICAL` |
| FP03 | repository presence without live binding/consumer | `PF_EXECUTABLE_BINDING_MISSING`, `PF_LIVE_RECEIPT_MISSING` |
| FP04 | stale binding path/ref | `PF_BINDING_REF_STALE` |
| FP05 | wrapper shadows accepted owner | `PF_BINDING_OWNER_MISMATCH`, `PF_WRAPPER_SHADOWS_CURRENT_OWNER` |
| FP06 | candidate self-replay as oracle | `PF_SELF_REPLAY_USED_AS_PARITY` |
| FP07 | UNKNOWN/BLOCKED/valid-empty collapse | `PF_NEGATIVE_STATE_COLLAPSE` |
| FP08 | missing Candidate-C capability called not-applicable | `PF_UNAUTHORIZED_NOT_APPLICABLE_ESCAPE` |
| FP09 | synthetic/partial preimage set used as production realization | `PF_SYNTHETIC_FIXTURE_SUBSTITUTION`, `PF_PARTIAL_PREIMAGE_SET` |
| FP10 | current implementation ref used to infer semantics | `PF_SEMANTIC_INFERENCE_SUBSTITUTION` |
| FP11 | same metric label with different method identity | `PF_METRIC_METHOD_MISMATCH` |
| FP12 | pre-repair/stale LIVE receipt | `PF_LIVE_RECEIPT_CODE_REF_MISMATCH`, `PF_LIVE_RECEIPT_PREDATES_REQUIRED_REPAIR` |
| FP13 | required preterminal function deferred | `PF_DEFERMENT_UNPROVED` |
| FP14 | `GENUINELY_MISSING` asserted before exhaustive missingness search | `PF_MISSINGNESS_NOT_FALSIFIED_FIRST` |
| FP15 | semantic owner reused as candidate cost owner | `PF_SEMANTIC_COST_OWNERSHIP_CONFLATED` |
| FP16 | common failure treated candidate-local / lifecycle order wrong | `PF_FAILURE_SCOPE_MISCLASSIFIED`, `PF_LIFECYCLE_ORDER_MISMATCH` |

## Additional focused gates

The unit file also tests:

- a complete six-cell/succession fixture reaches PASS;
- a missing P10 governed context blocks;
- post-freeze manifest mutation is detected by identity mismatch;
- lawful historical evidence remains usable as genealogy/provenance, while historical-only owner substitution blocks;
- `run_only_after_preflight_pass` does not call the execution callback on BLOCK and does call it after PASS.

No fixture outcome is represented here as executed in this worker session. Execution is deferred to the integrated/local test surface described in `02_TEST_AND_EXECUTION_PROTOCOL.md`.
