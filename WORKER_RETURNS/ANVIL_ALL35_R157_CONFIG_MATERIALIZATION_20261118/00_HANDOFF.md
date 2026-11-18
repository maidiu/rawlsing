# All-35 R157 SourceConfig materialization

## Verdict

**PASS — 35/35 parsed and qualified metadata configurations; 0 authorized executable Q2 bundles.**

- Historical R157 accepted config revision: `1924499ef52403a0f331b8aff9b7c7eff99bf1e2`
- SRC04 repaired accepted config: `da23c65d1e211cb7e8ce416e98757f321b78d25e:rawlsing_next/source_configuration/data/SRC04/source.config.repaired.v2.json`
- Current parser: `aee95429609c372564e996c2d3d3eb30e9253cbf`, `load_source_config` / `canonical_config_hash`
- Canonical 35 locator matrix: `d4f0a6499432aa3186c0d92174fa228211759e44`; locator source: `OWNER/WORKER_RETURNS/ANVIL_ALL35_ORIGINAL_INPUT_REUSE_20261118/REUSE_RESULT.json`
- Start OWNER: `88cc067534f2fc7e6d3f0705a6915be5cdb9a5eb`

This is metadata qualification only. No respondent file was opened, hashed, or decoded; no source body was read; no config was rewritten; no grant, scientific decision, census, inventory, frontier, product, or Q2 executable was created.

## Exact materialization

`materialize_validate_all35.py` stages each exact config blob from its immutable Git revision into a private temporary directory, loads it through the current parser, and compares against the matching all-35 bundle pin:

- exact file SHA-256 and canonical config SHA-256;
- source ID and `ORIGINAL_SOURCE` identity class;
- expected source SHA-256 from the config and bundle;
- declared rows, columns, original items, physical slots, questions, response/coordinate/weight slots, and routing count;
- source preparation purpose and schema;
- explicit Q2 holds conserved from the bundle.

No config blobs are committed. `CONFIG_INDEX.json` retains only immutable Git refs, hashes, parsed metadata, declared shape, and holds.

## Result

- **34/35 exact historical configs** match the existing locator file hashes at `1924499...`.
- **SRC04** correctly uses the repaired accepted blob at `da23c65d...`; the stale `1924499` sibling is rejected.
- **35/35 qualify as parsed `SourceConfig` metadata** with exact shape/source identity.
- **0/35 are authorized executable original Q2 bundles**; every row remains Q2 HELD with the original missing-input list.
- **Negative evidence passes:** stale SRC04 sibling rejected; mismatched expected source SHA rejected.
- **No duplicate config blobs** were committed.

## Evidence

- `CONFIG_INDEX.json` — 35-row machine index with exact revision refs and metadata comparisons.
- `VALIDATION.json` — actual clean run, 35 qualified, 0 failures, 0 Q2 executable.
- `NEGATIVE_EVIDENCE.json` — stale SRC04 and mismatched source SHA witnesses.
- `materialize_validate_all35.py` — executable Git materializer/parser validator.
- `run.stdout.txt`, `MANIFEST.json`.

The implementer-owned TEST_ONLY Q2 producer proof is separate and not overlapped here.
