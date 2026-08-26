# Rawlsing retrieval-only semantic-authority package

Created 2026-08-08 from the current Rawlsing worktree. This is a retrieval
package only. No source, authority, ontology, runtime, or survey file was
modified or regenerated.

## Package layout

The `zips/` directory contains logically split packages. Each ZIP contains a
`SHA256SUMS.txt` manifest for its packaged files. All deliverable ZIPs are
below 100 MB.

- `data.zip`: native instrument/codebook/data evidence selected for Asian Barometer, WVS, and Latinobarometro.
- `07_P2_...zip` through `42_P2_...zip` (including `31_INDEPENDENT_INTEGRITY_AND_CONTINUITY_AUDIT.zip` and `35_V552J_COMPONENT_AWARE_STRATA_HORIZON_RUNTIME_BRIDGE.zip`): the full current v40 P2/source-authority chain, including source-local surfaces, cross-source refreshes, global adjudication tranches, audits, unresolved/negative ledgers, and the runtime bridge.
- `43_...` through `60_...` ZIPs: current P3/P3A working authority, contracts, schemas, validation, candidate, exclusion, and release surfaces from the v40 working handoff.
- `Rawlsing_GSS_P3C_Joint_Authority_07_FULL_GSS_SEMANTIC_AUTHORITY_R1.zip`: immutable P3C GSS authority.
- `R4_V3_*.zip`: split R4 V3 semantic-review components.
- `04_QSM_ONTOLOGY_AUTHORITY.zip`: current codebooks, registries, QSM/ontology substrate.
- `05_V550_RUNTIME_CONTRACTS_CURRENT.zip`: current V550–V552J source modules, schemas, and tests selected from `data/ddm_build_copy`.
- `07_REPO_METADATA.zip`: branch/HEAD/status and relevant-tree metadata.

## Important provenance finding

The current semantic-authority work is materially present inside:

`rawlsing_p3a_v31_execution/work/Rawlsing_J_Family_Authority_Strategy_Handoff_v40_WORKING`

That tree is therefore protected from cleanup. It contains current P2/P3/P3A
authority, the Latinobarometro deep-pass/source packages, and current release
work. The older-looking `p3a_v31_execution` name is not evidence that the
contents are stale.

## Found

- Asian Barometer W1, W4, and W5 questionnaire/codebook/SAV evidence available in the repository.
- WVS W1, W4, and W7 data/codebook evidence and retained WVS questionnaire PDFs.
- Latinobarometro 1995 data and current 1995/2011/2024 derived authority; current v40 P2 source/deep-pass material is included.
- Current P2 source structure, routing/variant, provenance, calibre, unresolved, and negative ledgers where present.
- Current P3/P3C authority, immutable GSS authority, R4 review material, QSM/ontology registries, and V550–V552J runtime contracts.
- Current 35-wave authority and manual authority surfaces included from the available current trees.

## Not found or not independently verified

- Native Latinobarometro 2005 questionnaire/source package was not found as a standalone current native instrument.
- Native Latinobarometro 2023 questionnaire/source package was not found as a standalone current native instrument.
- The request names R14/R15; the repository exposes current v40 P2/P3 authority and R4/R5-style successor surfaces, but no single directory explicitly named `R14` or `R15` was found. The package preserves the current successor surfaces rather than relabeling them.
- A live PostgreSQL connection was not available for read-only export: `psql` reached the local socket but required an unavailable password. No DB-only CSV exports were fabricated. DB-only relations therefore remain reported as unavailable in this retrieval run.
- The package does not claim that derived authority replaces missing native instruments. Missing source evidence remains missing.

## Authority status

Files copied from `data/ddm_build_copy`, current v40 P2/P3 work, current P3C,
R4 V3, and current 35-wave authority trees are packaged as current or
successor authority surfaces according to their source paths. Historical
predecessors are retained only where they are part of the current handoff or
needed to explain provenance. Negative, unresolved, blocked, and fail-closed
rows were not filtered deliberately.

The `staging/` directory is retained beside the ZIPs as an audit workspace;
the ZIPs are the transfer artifacts. The `oversize_source_archives/` directory
contains an unshipped aggregate R4 archive only as a local convenience; it is
not part of the under-100-MB deliverable set.
