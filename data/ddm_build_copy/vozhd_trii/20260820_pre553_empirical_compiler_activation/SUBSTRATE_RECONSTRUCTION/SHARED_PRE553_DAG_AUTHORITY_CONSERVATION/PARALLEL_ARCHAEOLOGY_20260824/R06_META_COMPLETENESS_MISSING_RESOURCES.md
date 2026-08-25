# R06 — CROSS-CORPUS META-COMPLETENESS, AUTHORITY-LOSS & MISSING-RESOURCE ARCHAEOLOGY

Read `00_COMMON_WORKER_CONTRACT.md` first.

Mission: act as the anti-unknown-unknowns cell. Do not duplicate the semantic deep audit of R01–R05. Instead, exhaustively trace references, names, hashes, package chronology, duplicate/successor relations, stale handoffs, missing/unpackaged dependencies, absent authority roles, and unexplained producer/consumer edges across the entire historical corpus.

Primary territory:
- 72k-line `Rawlsing_repo_tree_dates_sizes_sha256(1).txt`;
- `TRAWLSING_DATE_SIZE_SHA256_TREE.tsv`;
- all three authority-document archives;
- `authority_role_loss_diagnostic(1).zip`;
- current HQ census/audit ledgers;
- package manifests, README/current-state/EXACT_CONTINUATION/MISSING_OR_UNPACKAGED_DEPENDENCIES files across all supplied packages;
- old Pax Marxica vision packs only to detect named capabilities that later disappear;
- J v23→v40 chronology as a stale-cumulative-package test case.

Critical questions:
1. Build a reference graph of named resources/capabilities not physically present in the indicating package.
2. Check each against the sealed tree and other supplied packages before calling it absent.
3. Detect packages whose root README/current-state is stale relative to later internal sections.
4. Detect same-name/different-hash and different-name/same-hash succession.
5. Detect explicit `missing`, `unpackaged`, `blocked`, `next step`, `must later`, `not installed`, `external`, `uploaded artifact`, `TODO`, `reconstruct`, `repair`, `supersedes`, and `replaces` signals.
6. Produce the retrieval hit list HQ can hand to the user after archaeology.
7. Flag conceptual capabilities whose names disappear entirely even if no exact filename is given.
8. Keep `ABSENT_FROM_SEALED_TREE` distinct from `EXTERNAL_PAYLOAD_RECOVERED`; `harmonized.zip` is the canonical example.

R06 must not decide that a concept is safely covered by Trii/Chetiri. It may identify candidate checked-in successors for HQ to adjudicate later.

Required return directory:
`PARALLEL_ARCHAEOLOGY_20260824/RETURNS/R06_META_COMPLETENESS_MISSING_RESOURCES/`

Produce all six common-contract outputs and commit them only to the assigned worker branch.