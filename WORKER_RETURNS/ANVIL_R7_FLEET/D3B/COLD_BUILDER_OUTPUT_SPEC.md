# COLD_BUILDER_OUTPUT_SPEC — exact first-reader ABI and six projections

**Schema:** `ANVIL_R7_FIRST_READER_ABI@1`
**Scope:** local deterministic projection of a verified S1 inventory + S3 decision. Not native science, independent C, H1 or architecture adoption.

## 1. Inputs (read-only)

The cold builder receives exactly three paths:

```
--evidence-root  EVIDENCE/          # JSON packet pointers and source inventory
--source-root    EVIDENCE/SOURCE_118/  # exact pinned source bytes
--repo           /path/to/rawlsing     # optional Git object store; verifies commit:path:blob
```

It loads, in order:

1. `DECISION.json` (`ANVIL_R7_INTEGRATED`, stage `INTEGRATED_DECISION`);
2. `common_frame` pointer → `FRAME.json` (`ANVIL_R7_INTEGRATED`, stage `COMMON_FRAME`);
3. `frame.source_inventory` pointer → `SOURCE_IDENTITY_INVENTORY.json`
   (`ANVIL_R7_SOURCE_IDENTITY_INVENTORY`, 118 entries, counts 29/26/14/10/8/8/7/16).

Every pointer is `{path, sha256}` relative to `--evidence-root`; absolute paths, `..`, backslashes and symlinks are refused. Every source file is `{path, sha256, commit, git_path, git_blob}` or `{source_kind: SUPPLIED_ZIP, zip_sha256}`; bytes are rehashed, and with `--repo` the commit, path and Git blob are re-read.

## 2. Hard refusal conditions (exit 2, no output)

- wrong/missing schema, unsafe path, changed bytes, Git blob mismatch, missing commit;
- inventory total ≠ 118, wrong group count, missing/extra ID, K3 row hash drift, missing B/S/L excerpt, T/terminal ID absent;
- `PYAT_PC.adopted != false` or `P4R.closed != false`;
- decision missing any of the 118 identity dispositions, any origin hash drift, any `BLOCKING_LOSS` at author grade, any present-hard hold, any 53-row substitute claim;
- typed graph missing producer/authority/time/consumer, type mismatch, orphan edge, missing T1–T7 boundary edge, fictional/modeled → observed backflow;
- any local H1/protected claim.

A refusal is a typed RED with exact error codes, never a partial package.

## 3. Deterministic outputs

All outputs are written only after all checks pass. JSON is `sort_keys=True`, UTF-8, two-space indent, trailing LF. JSONL is one sorted object per line. TSV is header + rows sorted by `identity_id`, tabs are rejected in field values.

| File | Media | Exact content |
|---|---|---|
| `DESIGN_DECISION.md` | UTF-8 Markdown | frame digest, author grade, first consumer, candidate/strategy, cost reasoning, historical conservation, scientific boundary, strongest objection, next operation, authority ceiling |
| `IDENTITY_DISPOSITIONS.tsv` | TSV | header `identity_id,group,disposition,status_assertion,evidence_grade,design_effect,first_consumer_path,conservation_or_refusal_witness,origin_sha256`, 118 data rows |
| `BOUNDARY_CONTRACT_MAP.json` | JSON | `{schema, boundaries:{T1..T7}, note}`; T1–T7 are interrogations, not seven stages |
| `TYPED_GRAPH.json` | JSON | `{schema, graph:{nodes,edges}, note}` with producer, producer_authority, input_types, output_types, time_mode, first_consumer; edge data_type, authority_grade, temporal_mode, negative_or_refusal, invalidation_rule, boundary |
| `EVIDENCE_INDEX.jsonl` | JSONL | sorted `INV:*`, `DISP:*` and decision evidence refs; each has `id`, `kind`, origin/source anchor |
| `BUILDER_HANDOFF.json` | JSON | `{schema, first_real_consumer, handoff:{first_reader_abi,input,output,negative,restore,consumer}, authority_ceiling}` |

Plus `MANIFEST.json`: `{schema: ANVIL_R7_BUILT_MANIFEST, files: {name: sha256}, note}`. The six files are the contract; the manifest is the byte check.

## 4. First-reader sequence

1. Read `BUILDER_HANDOFF.json`; confirm `first_reader_abi == ANVIL_R7_FIRST_READER_ABI@1`, `first_real_consumer` matches the decision, and `authority_ceiling` is not native/protected.
2. Read `IDENTITY_DISPOSITIONS.tsv`; confirm 118 rows and the exact group counts; any missing/extra row stops.
3. Read `BOUNDARY_CONTRACT_MAP.json`; confirm T1–T7 names and no claim of adoption/science.
4. Read `TYPED_GRAPH.json`; confirm every edge has a T boundary, every node has producer/authority/time/consumer, and no fictional/modeled backflow into observed.
5. Read `EVIDENCE_INDEX.jsonl`; verify each `origin_sha256`/`source_anchor` against the inventory and decision.
6. Read `DESIGN_DECISION.md`; confirm the author grade is `AUTHOR_PROPOSED_PENDING_C` and the authority ceiling is present.

**Positive:** all six present and byte-identical to a fresh re-derivation.
**Negative:** mutate any projection or source byte; cold reader must refuse.
**Restore:** restore exact bytes; re-derive and require the same six hashes.

## 5. Commands

```bash
python3 tools/r7_integrated.py FRAME FRAME.json \
  --evidence-root EVIDENCE --source-root EVIDENCE/SOURCE_118 --repo /path/to/rawlsing

python3 tools/r7_integrated.py DECISION DECISION.json \
  --evidence-root EVIDENCE --source-root EVIDENCE/SOURCE_118 --repo /path/to/rawlsing

python3 tools/r7_build.py build DECISION.json \
  --evidence-root EVIDENCE --source-root EVIDENCE/SOURCE_118 --out BUILT

python3 tools/r7_build.py verify DECISION.json \
  --evidence-root EVIDENCE --source-root EVIDENCE/SOURCE_118 --out BUILT
```

Expected local statuses: `PASS_LOCAL_COMMON_REQUIREMENTS_SOURCE_IDENTITY_NOT_NATIVE_AUTHENTICATED`, `PASS_LOCAL_INTEGRATED_DECISION_PENDING_C`, `BUILT`, `PASS_SIX_PROJECTIONS_BYTE_IDENTICAL`. None is C or H1.

## 6. Non-custody

The builder never writes to the source root, never mutates the shared package, never pushes/merges, never creates an H1 receipt, and never edits PROGRAMMA or CURRENT_PROGRESS. Its output belongs in the private return directory only.
