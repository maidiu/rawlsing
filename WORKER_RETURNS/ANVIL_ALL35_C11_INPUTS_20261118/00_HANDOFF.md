# ANVIL all-35 C11 input producer — first executable cut

## Status

**Executable metadata/input producer complete.**
**35 metadata bundles validated; 35/35 exact R157 config revisions bound; 0 Q2-executable bundles; 35 Q2 inputs held.**

- Branch: `agent/anvil-engineering-cut1-20261117-r1`
- Canonical source set: PYAT1002 R2 `d4f0a6499432aa3186c0d92174fa228211759e44`
- Accepted current code: `aee95429609c372564e996c2d3d3eb30e9253cbf`
- Own return: `WORKER_RETURNS/ANVIL_ALL35_C11_INPUTS_20261118/`
- No product files modified.
- No original respondent body opened, read, decoded or hashed.
- No new grant or science.

## Executable producer

```bash
PYTHONPATH=. PYTHONDONTWRITEBYTECODE=1 python3 -B \
  WORKER_RETURNS/ANVIL_ALL35_C11_INPUTS_20261118/producer.py
```

It produces:

- `bundles/SRC01.json` … `bundles/SRC35.json`
- `ALL35_RESULT.json`

Validation per source:

- canonical 35 IDs/order and uniqueness;
- exact local codebook SHA-256 match (35/35);
- metadata-only data path presence and declared size (35/35; no body hash/open);
- source config pins, sourcefree fixture pins, rights decision, counts;
- SRC04 exact historical repaired-v2 config loaded through the current
  `pre553_r157_projection_adapter.load_source_config` and canonical hash checked;
- no TEST_ONLY relabel of any original source.

## Actual counts

| Result | Count |
|---|---:|
| Canonical sources | 35 |
| Metadata bundles produced | **35** |
| Metadata bundles validated | **35** |
| Exact R157 config revisions bound | **35** |
| Config binding failures | **0** |
| Q2-executable input bundles | **0** |
| Q2-held bundles | **35** |
| Source-rights-held bundles | **33** |
| Typed Q2-held bundles | **35** |
| Actual test-only executable bundles | **1** |
| Witness configs loaded | **1** (SRC04) |
| Sourcefree transfer example | **SRC01** fixture pins only |

`ALL35_RESULT.json` SHA-256:
`c4bdc2a6e94fabd4e06a3616eb112be4d36759443df3a61ef7aed259d9b7fbdc`


## Exact R157 config binding

The frozen index is accepted only by immutable reference:

- commit `ad3386b718fd9ace234a00dab3b32ee51039b77f`
- path `WORKER_RETURNS/ANVIL_ALL35_R157_CONFIG_MATERIALIZATION_20261118/CONFIG_INDEX.json`
- SHA-256 `d6741f8e7d084f031d0b762f4f8b6465dc35eb73d7ab6ffc64598123174a1f27`

All 35 rows are materialized through the existing current
`load_source_config` / `canonical_config_hash` path and bound to the package
bundle's exact wave, expected source SHA-256, row/column counts, physical/
question/response/coordinate/weight/routing shape and Q2 hold. The bundles carry
only immutable revision refs and hashes; no config blobs are committed. The
resolver is `resolve_config.py --all`.

Negative checks all refuse: swapped config, swapped wave, source SHA mismatch,
and stale SRC04 (the stale `1924499` sibling is rejected; the repaired
`da23c65d` config is required). Permissions and hold fields are byte-identical
to `d8758a1b` for all 35 rows.

## SRC04 witness

The exact grant is preserved at:

`evidence/FULL_SOURCE_GRANT.json`
SHA-256 `d8f13c67af276175266168e9af1a91e28fd543fcecadc1e79112a9854b4a8139`

The exact repaired-v2 config is materialized at:

`inputs/SRC04/source.config.repaired.v2.json`
file SHA-256 `5e107de4baf43f11a2a3e739e05481d8008de6f90951e86a170fb4d804ef3ff5`
canonical SHA-256 `28630f26b491dcbce411667e3ad285ea42b40abf2d0176056a8a15d1ecad768d`

It loads as SRC04, source SHA `2a48ba4b…`, 181 physical slots, 178 configured
responses, 3 configured coordinates. The accepted C11 reference remains
`ba41253681212be14a0cde009afb99d77e14935e`: 7,337 rows, 177 selected responses,
3 coordinates, 1,298,649 response positions, q217 held at 38 unbound cells.

## SRC17 correction

SRC17 has **source-read/C11 construction permission at its exact scope**; I03/I05
are excluded. Its Q2 inputs remain held. The permission bytes are preserved and
the bundle status is corrected to
`SOURCE_READ_C11_AUTHORIZED__I03_I05_EXCLUDED__Q2_INPUTS_MISSING`.

## Second sourcefree example

`SRC01` is pinned as the existing R157 sourcefree fixture transfer witness from
the R2 matrix (`fixture_file_sha256`, `fixture_config_file_sha256`). It is
metadata-transfer evidence only; it is not an original source read and is not
Q2-executable without the same missing Q2 inputs.

## Actual executable TEST_ONLY bundle

`testonly_bundle/` contains actual typed `SourceConfig`, `SourceInventory`,
`GrammarPolicy`, `ScientificFrontier` and `FrozenInputCensus` pickled and
reloaded from one existing 5-row sourcefree fixture. It performs:

- one actual `SourceSavedBodySink` build into a 13-family saved estate;
- a fresh-process cold reopen with exact full-family counts;
- a pre-source census mismatch refusal (`SOURCE_CENSUS_SHA_MISMATCH`) against
  a nonexistent source path.

This is **separate** from the 35 original metadata bundles and is not counted
as an original-source executable input.

## Proof-harness repair

The frozen `d8758a1b` harness had two observed defects: unconditional
`current_authorizer=lambda _roots: True` on cold reopen, and pickle load before
checking its emitted digest. Both are repaired in `testonly_bundle/`:

- reopen now uses the existing exact-held manifest/roots callback pattern;
  revoked and wrong-root/scope cases both refuse;
- `build_bundle.py` validates the local TEST_ONLY manifest marker, relative
  pickle path, and SHA-256 digest **before** `pickle.loads`; arbitrary pickle
  packages are not accepted as original input;
- replay root is an explicit fresh empty directory, with relative source path;
  `run.py` refuses the canonical return and non-empty roots;
- canonical frozen proofs and all 35 original rows are unchanged.

Exact commands: `REPAIR_COMMANDS.md`.

Evidence: `evidence/reproduce_old_defect.json`,
`evidence/fresh_repair_proof/`, `evidence/fresh_repair.out`,
`evidence/tests_repair.txt`.

## Commands

```bash
PYTHONPATH=. PYTHONDONTWRITEBYTECODE=1 python3 -B \
  WORKER_RETURNS/ANVIL_ALL35_C11_INPUTS_20261118/producer.py

PYTHONPATH=. PYTHONDONTWRITEBYTECODE=1 python3 -B \
  WORKER_RETURNS/ANVIL_ALL35_C11_INPUTS_20261118/resolve_config.py --all
```

Evidence: `evidence/config_bindings.json` (35/35 resolver rows),
`evidence/config_binding_negatives.json`, `evidence/config_binding_summary.json`.

## Unresolved required Q2 fields

For every source, the following current Q2 inputs are still absent:

- `FrozenInputCensus`
- `SourceInventory`
- `GrammarPolicy`
- `ScientificFrontier`
- concrete current `SourceReadDecisionResolver` adapter

Additionally:

- All 35 sources now have an exact materialized metadata `SourceConfig` binding;
- 33 sources have no current source-use grant (`UNKNOWN_OWNER_DECISION`);
- SRC17 is source-read/C11-only and excludes I03/I05;
- SRC04 has the grant/config/C11 witness but not the Q2 census/frontier objects.

The producer does not force storage preparation to settle science. If current
Q2 requires an issued frontier, that is the exact code/authority dependency:
`build_source_i02_handoff` requires the four Q2 objects plus an admitted current
resolver.

## Tests

```text
6 passed in 5.14 s
```

- all-35 metadata positive and typed holds;
- codebook hash drift refusal;
- data path drift refusal;
- SRC04 config drift refusal.

Evidence: `evidence/tests.txt`.

## Limits

No raw source, no respondent values, no new grant, no original TEST_ONLY
relabel, no source science, no product edit, no large/real builds. Codebooks are
metadata descriptions only, not authority.

**STOP after publish.** SRC04 published intake and earlier evidence are preserved.
