# PYAT C11: four permanent physical stores, one command

Status: ISOLATED TEST-ONLY AUTHOR CANDIDATE. Not native-source science, accepted S2-D cold reader, production schema cutover, original-issuer grant, independent G5, or protected PROGRAMMA receipt.

## What runs

One frozen and independently verified ANVIL saved C11 stream is read four times, once per persistent destination. These are physical *experiments* on the same already-saved source, never another SAV/DTA decode.

| Arm | Primary body storage | Persistent query index |
| --- | --- | --- |
| H | Existing 13 family Parquet files and event locator | Compact INTEGER/SHA256 SQLite sidecar, all refs recoverable |
| S1 | Complete SQLite canonical bodies (zlib-6), full TEXT keys | Indexed TEXT questions/person/events |
| S2 | Same complete SQLite bodies | Release-local INTEGER join keys, exact full-reference dictionary |
| S3 | Same complete SQLite bodies | INTEGER join keys plus SHA256 fingerprints, exact full-reference recovery |

All retain complete original body_json objects and source/typed metadata, all thirteen source families, exact refs, authority and replay bodies, event occurrence fields, risk/eligible/routing/weight/coordinate objects and original source roots. Every source row is checked by the existing Rawlsing object reader and exact typed projection; every event locator position is checked, followed by a full family-level post-build digest audit. H retains the original Parquet source as a required part of its durable query service; S1/S2/S3 read their physical bodies from their own SQLite after initial construction. Each SQLite also contains versioned query specs, result records, and receipts. Fingerprints accelerate lookup and **never** replace the original full text reference.

## Original R2 MainMac no-handwritten-hook launch

The supplied bundle.example.json now directly names the EXISTING original R2 custody decision and its separately retained Q006 Q103 operation/universe-use JSON. Place the original unpacked P0_TWO_SAVED_WAVES_PRIVATE directory beside run_all.sh or set PYAT_BENCH_CONFIG to an equivalent one-time configured JSON. The R2 decision retains the original absolute ANVIL saved-estate path; that path must still exist on MainMac and match the externally held roots.

For this direct R2 mode, the code reads and rechecks the original user-scoped host/purpose, source/release/manifest/root/decision references, original Q103 document SHA, historical DEFER and positive source-interpretation authority and exact ALLOW_EXACT_OPERATION_ONLY universe-use decision. It makes no new query authority. It constructs Q103 once and executes that SAME already-issued operation through each four physical store adapter; other 1/10/100 per-question probes remain expressly PHYSICAL_ONLY until original source-authorized operations exist.

Simplest launch from the Rawlsing repo checkout after placing the private R2 bundle beside this package:

    PYAT_BENCH_OUTPUT_DIR=/Volumes/YourLargeLocalDrive/pyat-four-store sh tools/pyat_c11_four_store/run_all.sh

The output environment variable is optional if enough space remains on the configured output volume. The script uses bundle.json if present, otherwise automatically uses bundled bundle.example.json. No handwritten Python providers are required in this R2/Q103 mode. No private keys, respondent values, decisions or proof payloads are committed by the package.

The original R2 decision check is scoped to its user-declared host/purpose and is re-read every time the source CURRENT guard is invoked. Its use does not grant scientific use beyond the recorded decision. Missing original source, moved/stale paths or revoked decision cause a typed failure or hold—not a synthetic recreated grant.

## One Mac invocation

Put this package inside a clone of Rawlsing. Arrange one private working folder containing access to the already-saved ANVIL C11 release and its actual existing held source/authority information. The bundled R2 example will work as-is when its original private folder is co-located and the original absolute estate path still exists; override once through bundle.json only if paths differ. Provide the two small adapter modules pointing to existing authorized local code (not fabricated authority):

- current_authorizer.py exports check_current(held_pins) -> bool, actually consulting the current authoritative saved source/host grants;
- issued_operations.py exports provide_operations(verified_estate), yielding already issued Python dictionaries containing query, predicate, authority_registry and optionally recorded_plan; it is optional for *physical* benchmarking but required to claim any native empirical comparison.

The included TEMPLATE files refuse permission and cannot be used as current authorizers. These separate modules are for non-R2 sources; the included R2 pathway reads original JSON directly.

Execute once from anywhere:

    PYAT_BENCH_PYTHON=/path/to/your/rawlsing/python sh tools/pyat_c11_four_store/run_all.sh

Use the existing Python environment with rawlsing_next imports, pyarrow and psutil. The script will not run pip, fetch anything, or install anything. The bundle.json schema is PYAT_FOUR_PERMANENT_STORE_BUNDLE@1, pointing to original estate_root, estate_path, held_pins, authority_provider, operations_provider and output_dir. Run an individual arm via run_all.sh --only H, --only S1, --only S2 or --only S3. A successful single arm returns success with a clearly marked SINGLE_ARM status; it cannot be used to claim four-way parity. The self-test command runs physical-store, sourcefree end-to-end and recorded-R2 guard tests: python -m tools.pyat_c11_four_store.runner --self-test.

The four-arm launcher refuses missing original held pins/current rights, altered saved files or manifest, incomplete families, wrong event locators, corrupt compressed canonical bodies, lost exact refs, SHA256 identity collisions, an exhausted resource ceiling, or insufficient free disk. It does NOT silently reuse a fabricated new source/operation grant.

## Emissions and persisted results

Each run goes to OUTPUT_DIR/RUN_ID. The common progress.jsonl is flushed while scanning original files; each of H/S1/S2/S3 independently writes:

- progress.jsonl, streaming and flushed JSON stage/row/family/timing/RSS/disk events plus unbuffered terminal output.
- permanent.sqlite, with source metadata, indexed records and result tables (H still requires original Parquet).
- report.json, with full thirteen-family body hashes/counts, physical query timings, SQL three-question co-presence, evidence-reference retrieval, native original I03 result references if issued, retained disk, scratch/RSS sampling, failure reasons, and exact source roots.

Overall comparison.json and summary.csv compare completed arms. Construction, source admission, post-build complete-corpus audit, fresh connection, physical queries and native issuing are timed separately. 1..100 physical question probes are distinct source questions, NOT invented scientific I03 queries. Native results are generated by existing execute_empirical_query using an exact-type test-only DirectEstateI03Session-shaped reader. The reader uses the original verified ANVIL source object to check CURRENT and a committed audited SQLite to supply bodies. This is a TEST-ONLY in-memory adapter because the production evaluator rejects arbitrary repository types; it is *not* an accredited production substitute. The original source-free SQL probe output and native results are distinctly labeled.

A completed physical-only test is **not** an answer to the scientific/consumer test. The current package does not execute I05/Batch or S2-F/S05, though it invokes the existing S04 projection after an issued I03 operation and optionally FF01 when the issuer supplies its exact permission-ceiling inputs; downstream code is left unmodified and their receiving tests remain an additional necessary part of any storage cutover. A later owner can supply additional original issued operations and the existing I05/Batch and S2-F/S05 consumers without recreating a numerical evaluator. The measured economics and break-even analysis in comparison.json are PHYSICAL profiles, not a scientific winner.

## Resource and privacy discipline

Output must be on a large local volume: preflight reserves at least 12 GiB free or 5× original estate retained bytes, whichever is greater. The process-tree RSS cap is 6 GiB; arms run sequentially. The live sampler records maximum output directory size (not a complete total of separately retained original source or filesystem-level temporary space), so report that distinction honestly. Existing original saved files are never modified or deleted. Any FAILED/HELD variant retains a trace and an unfinished SQLite marked BUILDING, which will not be considered a committed valid store. A fully constructed store remains AUDIT_PENDING until all thirteen complete canonical body digests, event/identity posting counts and SQL integrity checks pass; a killed build cannot be cold-opened as COMMITTED. The original R2 decision document is pinned byte-exact for each run, and any file edit requires new admission. SQLite databases should be copied while closed, by SQLite backup API, or with a correct WAL checkpoint; the script checkpoints before readback. Do not run WAL over NFS. Do NOT commit bundle.json, original survey bytes, authority credentials, private result SQLite files or progress logs to GitHub.

## Evidentiary limits and exact next milestone

- S1/S2/S3 use complete compressed canonical body_json, preserving all R5 typed lane data from the original; the compression codec itself is zlib-6 rather than the Parquet Zstd body compression. This is a concrete comparison, not evidence that no alternate SQL compression can be better.
- The physical marginal GROUP BY is not native I03 population inference. If no original issuance hook exists, its absence is reported as HELD.
- Full original Q103 construction currently has its own unoptimized all-event scan outside the saved reader; this code does not pretend it has eliminated that stage.
- Same-format independent integrity, source/current approvals, I03 typed negatives, I05/Batch and real downstream first-consumer receiving are required before making a canonical store replacement claim. Bench figures are not scientific acceptance.
- Internal INTEGER ids are scoped to this physical release and must never enter original fact identities.
- No test data, fixture or individual-level sources are copied to GitHub by these harness scripts.

Controlling existing owner: #1006 and #1097. G4/KUDA source-grade record is documentary only. This experimental branch does not modify existing protected S2-B/C/D scientific or physical modules.
