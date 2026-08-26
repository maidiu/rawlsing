# CODEX — INSTALL G1A GITHUB PORTABILITY CORPUS R1

Repository: `maidiu/rawlsing`
Base commit: `9b65e0232916f660d9a0bc343b01e94e438e2cbb`
Create/use branch: `agent/g1a-github-portability-r1`

You are performing evidence portability only. Do not mutate main, live Trii, authority registries, C1–C6 conclusions, P1–P10 law, or downstream semantics.

Read first:
- `G1A_GITHUB_PORTABILITY_MANIFEST_R1_20260826.md`
- `G1A_GITHUB_PORTABILITY_MANIFEST_R1_20260826.tsv`
- `SHA256SUMS.txt`

Goal: make the active G1A closure campaign reproducible from repository checkout without dependence on one ChatGPT Library.

1. Verify every supplied transfer file against `SHA256SUMS.txt` before extraction.
2. Create `data/ddm_build_copy/recovery_integration/portable_evidence/G1A_CLOSURE_R1_20260826/` and the manifest's subtrees.
3. Install/extract the READY files exactly as directed by the manifest. Preserve original transfer archives in `_transfer_archives/` or `_raw_archives/` as directed.
4. Preserve all `PORTABILITY_PROVENANCE.json` files. Do not normalize source bytes.
5. Locate every `REQUIRED_SHA_LOCATE` object from the manifest in available historical Rawlsing/RawlsingsExcess workspaces, archives, backups, or local handoffs by exact SHA-256. Filename/mtime/recency is not sufficient.
6. For each located object record original path, archive SHA if applicable, member path, byte size, SHA-256, target repo path, evidence/authority status, and which C-lane needs it in `99_PROVENANCE/SOURCE_PROVENANCE.tsv`.
7. Do not commit a normal Git object >=95 MiB. Split large text deterministically into readable chunks plus a reassembly manifest that recreates the exact original SHA. Keep the original transfer archive when useful.
8. For Parquet or other binary analytical evidence needed for inspection, retain original bytes and add deterministic CSV/JSON companions with source SHA, schema, row count and conversion recipe. Companions are evidence projections, not authority replacements.
9. The historical 9-family archive SHA `266d82216bcd6351de19ada84377d56fcf8b48fba1d29eb208a399fda012e816` is a critical C1 target. Use the supplied `EXCLUDED_LARGE_ARCHIVE_COMPLETE_MEMBER_INDEX.csv` to select manual/provider-relevant members; do not import unrelated raw microdata.
10. C2 must mirror the exact SWID/current-35 identity objects named in the manifest. C3 must mirror the exact V525b/d62 raw carriers named by SHA. C4 should install all three supplied J-family packs and SHA-locate the named historical specs when available. C5 should install both function packs and, where available, mirror the R184 bundle/dump named by SHA.
11. Generate `99_PROVENANCE/SHA256SUMS.txt` and `PORTABILITY_VALIDATION_RETURN.json`. Validation must cover every ready transfer SHA, every mirrored exact source SHA, all split/reassembly hashes, and every internal `PORTABILITY_PROVENANCE.json` member hash.
12. Return a ledger for every manifest object with exactly one status: `PRESENT_EXACT`, `NOT_FOUND`, or `EXCLUDED_BY_GOVERNING_SEARCH_LAW`. Do not silently omit unresolved objects.
13. Do not claim full portability if any required object remains `NOT_FOUND` or if C1's provider universe still depends on an unmirrored Library-only packet.

Expected provisional result after installing the supplied files but before all SHA-located legacy objects are found:
`G1A_GITHUB_PORTABILITY = PARTIAL__SHA_PINNED__CODEX_MIRROR_REQUIRED`

Only claim `G1A_GITHUB_PORTABILITY_COMPLETE` after the manifest certification rule is satisfied.
