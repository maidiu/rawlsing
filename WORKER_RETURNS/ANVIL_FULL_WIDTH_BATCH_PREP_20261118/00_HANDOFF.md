# Full-width prepared Batch receiving path

## Status

**PREPARED_TEMPLATE_ONLY — waiting for the sealed combined fixture contract after the 10,000 × 600 build.** No Batch, native query, source read, fixture build, benchmark, or product edit was executed here.

The existing `ANVIL_ROUTING_MATCHED_RUNNER_20261118` is not sufficient for this task: it exercises direct prepared I03 with two operations and does not construct an actual `BatchExecutionRunner`/`BatchManifest` or emit per-unit Batch receipts. The new driver is a thin receiving wrapper over the already-accepted prepared Saved Batch path, not a second matcher and not a fake Batch.

## Driver

`full_width_batch_driver.py`:

- imports one read-only code snapshot, exact candidate `aee95429609c372564e996c2d3d3eb30e9253cbf`;
- accepts the sealed combined contract after build;
- requires explicit runtime catalog materialization and an explicit current-authorizer callable (no default allow);
- constructs exactly two distinct QUERY units (`f2_forward_raw`, `f2_reverse_raw`) on the exact reconstructed release;
- calls the accepted `execute_saved_batch` helper, which opens exactly one `PreparedSavedC11Admission.prepared_i03()` context;
- counts `DirectEstateI03Session._build` as a one-session assertion;
- emits exact unit/receipt refs, receipt hashes, result refs, states and provenance refs per operation;
- optionally compares each Batch result ref to a qualified baseline JSON when supplied;
- reports full fact payload and denominator/cell payload as **not carried by Batch receipts**, with the existing direct artifact/I03 API named as the separate source;
- enforces one synthetic `source_wave_country_context` scalar and reports `multi_country_execution: false`.

### Contract

`contract_template.json` is the exact input shape to replace after the combined build:

- sealed estate: `root`, `exact_path`, `manifest_sha256`, `i02`, reconstructed release ref;
- one synthetic source-wave-country context;
- exact forward/reverse query and predicate refs;
- runtime catalog public documents (authorities/predicates/queries/discovery authorities).

The actual catalog must be supplied either in the sealed contract or via `--runtime-catalog`; the template's empty catalog is not executable.

### Run

After the combined fixture is sealed:

```bash
python3 full_width_batch_driver.py \
  --snapshot /path/to/read-only/aee95429609c code \
  --contract /path/to/sealed_combined_contract.json \
  --runtime-catalog /path/to/runtime_catalog.json \
  --current-authorizer package.module:function \
  --baseline /path/to/qualified_baseline.json \
  --out BATCH_RESULT.json
```

Dry validation only (no product import and no Batch):

```bash
python3 full_width_batch_driver.py \
  --contract contract_template.json --validate-only
```

`template_validate.txt` records `VALID_CONTRACT_NO_EXECUTION` for the schema/template.

## Semantic boundary

- Release, query, predicate and unit identities are exact; no latest/default/fuzzy fallback.
- `execute_saved_batch` preserves the existing accepted prepared Session, I03 evaluator, current checks, replay provenance and receipt semantics.
- Batch receipts contain result refs, not full fact payloads. Full cells, risk/denominator member arrays, weighted semantics and full provenance remain in the existing direct fact/artifact path; this driver does not claim they are in Batch receipts.
- A baseline comparison, when supplied, checks exact Batch result refs and any exact query/predicate identity available. A missing baseline is `BASELINE_NOT_AVAILABLE`, not a pass or mismatch. Full payload/denominator parity is explicitly marked unavailable from Batch.
- One synthetic source-wave-country context only; multi-country execution is outside this template.

## Sources

- Code snapshot: `aee95429609c372564e996c2d3d3eb30e9253cbf`.
- Accepted prepared Batch helpers: `pre553_saved_workload_integration.execute_saved_batch`, `pre553_prepared_saved_i03.PreparedSavedC11Admission`, `pre553_batch_runner.BatchExecutionRunner/BatchManifest/BatchUnitSpec`.
- Prior evidence: WIDTH128 and 10k fixture contracts, accepted Cut1 prepared Batch tests, postconsumer prepared-Batch join tests, and the routing exact-repair recheck at `bbc3114f`.

No raw/original source, production/protected/science claims, product edits, build, native run, or heavy child was used.

## Exact input repair

The prior template exposed exact refs as strings. The accepted API's `exact_ref`
requires an `ExactRef` or a three-field mapping; it rejects strings. The driver
now normalizes every contract/baseline ref to a strict
`kind/object_id/content_hash` document, verifies its canonical round-trip, and
passes the document to `exact_ref`. Bare strings and non-sha256 placeholders are
rejected by the same path used by `--validate-only`; `template_validate.txt`
records the valid synthetic template validation and `placeholder-reject.txt`
records the rejection.

`load_catalog` now gives explicit `--runtime-catalog` precedence over an empty
contract-template catalog. It requires nonempty authorities/predicates/queries,
materializes the catalog, and resolves every forward/reverse query and predicate
exactly before opening the estate.

Baseline use now requires an exact manifest and exact query/predicate/fact
identities. Any available-baseline mismatch fails; absent baseline remains
`BASELINE_NOT_AVAILABLE`. Full Batch payload/denominator comparison remains
explicitly separated.

`exact-ref-smoke.txt` is a light no-native smoke against the exact `aee954`
snapshot using existing 10k release/query/predicate documents: normalization
round-trips and the bare string form is rejected by `exact_ref`. No estate was
opened, no query/build/benchmark ran, and construction was untouched.
