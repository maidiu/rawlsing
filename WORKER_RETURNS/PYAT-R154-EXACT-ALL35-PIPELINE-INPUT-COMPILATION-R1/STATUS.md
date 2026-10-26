# R154 status

- Sources: 35/35.
- Physical metadata receipts: 35/35, including exact metadata-only Latin-1 retries for SRC13/SRC14.
- Codebook rows: 18,276; physical columns: 18,413.
- Reconciliation: 538 physical-only columns; 401 codebook-only columns; explicit in store/exports.
- B49/typed evidence rows: 4,493; typed surfaces: 38; context: 3,804; unmatched relation holds: 26.
- Native loader: 35 `NativeSourceIdentity`, 35 `OriginalWaveIdentity`, 35 `SelectedSourceRulePackage`.
- Task ledger: 108 DONE, 35 DONE_WITH_EXACT_UNRESOLVED_FIELDS, 70 BLOCKED (35 WORKLOAD + 35 PACKAGE), 0 RUNNING.
- Exact external blockers: current source-read grant/resolver and source-specific occurrence/frontier/learned/FF authority. See `HQ_ACQUISITION_AND_DECISION_REQUESTS.json`.
- Response rows decoded/exported: 0. Empirical/learned/FF execution: 0.
