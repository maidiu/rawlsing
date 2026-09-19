# FIABC-B04 — Evidence index

All Git refs below are immutable commit identities or the exact commission-branch snapshot used for this return.

- **E01 — Sealed HQ pointer/current state.** `HQ_HANDOFF/LATEST.json` on commission start `d474f8e3c9630c4bcbb10d6e8359b71ba5b3060d` points to checkpoint `20260919T1207-0400`, sealed handoff commit `3692aa093e26252c2f94678b3d456dc37cf7144e`. `HQ_HANDOFF/checkpoints/20260919T1207-0400/CURRENT.md@3692aa093e26252c2f94678b3d456dc37cf7144e` records measured P2X held pending exact local reconciliation.

- **E02 — Frozen ChETIRI final P2 court manifest.** `HQ_HANDOFF/CHETIRI_FINAL_P2_COURT_MANIFEST_R1.json@d474f8e3c9630c4bcbb10d6e8359b71ba5b3060d`. It freezes A/B/C owner definitions at owner commit `0b96b8de9aac774566f872cf0630ebd4ddeb70e6`; requires semantic, ExactRef/identity, replay, integrity/fail-closed, complete-frontier and typed-negative parity before performance is admissible; and freezes deletion/rebuild law.

- **E03 — Canonical semantic states, exact refs, canonical identity.** `rawlsing_next/pre553_empirical_objects.py@d474f8e3c9630c4bcbb10d6e8359b71ba5b3060d`, blob `a61365b994e5c3c50de0f598fcf40e90abf757b6`. Relevant surfaces: `STATE_FAMILIES`, `ExactRef`, `AuthorityRef`, `canonicalize`, `semantic_hash`, `CanonicalSemanticObject`, `AuthoritySnapshot` fuzzy-selector prohibition.

- **E04 — Frozen candidate B semantic core.** `rawlsing_next/pre553_source_backed_c11_facade.py@0b96b8de9aac774566f872cf0630ebd4ddeb70e6`, blob `7c509c2098d0030f253344eb3f682471378812a8`. Relevant surfaces: `physical_value_binding_key`, `GovernedC11Projection`, `_event`, `_coordinate`, `_weight`, `project_c11_candidate_from_physical_cells`, replay-manifest construction, `build_source_backed_c11_repository`.

- **E05 — Frozen candidate A adapter.** `rawlsing_next/pre553_r5_source_backed_adapter.py@0b96b8de9aac774566f872cf0630ebd4ddeb70e6`, blob `d4915e7e6755ba1850756aebff72f982f73a332b`. It validates/reconstructs exact `PhysicalCell` state, preserves source missing declarations and raw labels, binds source SHA/geometry, then calls B with `cache=None`.

- **E06 — Frozen candidate C accelerator path.** `rawlsing_next/pre553_route_c_accelerators.py@0b96b8de9aac774566f872cf0630ebd4ddeb70e6`, blob `abfdc91a71ef5e18c4a8a6bf62fa65750d8d9889`. Relevant surfaces: module authority boundary; `RouteCDeterminants`; `_state_envelope`; `_coordinate_envelope`; exact-stream reconstruction; `delete_cacc1`; `delete_cacc2`; query/discovery identity parity assertions; `build_route_c_repository`. Unsupported source-missing declarations require cacheless exact-source fallback rather than semantic widening.

- **E07 — I03 fail-closed query and negative replay.** `rawlsing_next/pre553_empirical_query.py@0b96b8de9aac774566f872cf0630ebd4ddeb70e6` plus `rawlsing_next/_pre553_query_eval.py@0b96b8de9aac774566f872cf0630ebd4ddeb70e6`. Relevant surfaces: exact release resolution; `_failure_code`; `_negative_result`; `_routing_fact_for`; `_risk_membership`; topology compatibility; `_build_negative_fact` deterministic replay ref and dependency closure.

- **E08 — Source-plurality law.** `rawlsing_next/pre553_source_relations.py@0b96b8de9aac774566f872cf0630ebd4ddeb70e6`, blob `5b67e3f98a5faf95a6c82700af2346fef6e306a5`. Relevant surfaces: `DEFAULT_RELATION_STATE = DISTINCT_BY_DEFAULT`, relation decision matrix, nonauthorizing provenance/alias relation kinds, exact positive-authority guards, `RelationDecision.replay_identity`.

- **E09 — Component negative-state scalarization guard.** `rawlsing_next/pre553_component_authority_vector.py@d474f8e3c9630c4bcbb10d6e8359b71ba5b3060d`, blob `7c5993540e3dcfde5110f882fd1e26a298f47ac6`. `DENIED`/`NONCOMPARABLE` require exact negative refs; incomplete/governed-empty/denied/noncomparable vectors do not scalarize as ordinary values.

- **E10 — Current P2X selective fan-in/hold record.** `HQ_HANDOFF/EE_P2X_PARALLEL_REPAIR_FANIN_20260919.md@3692aa093e26252c2f94678b3d456dc37cf7144e`. It records exact current P2X head `617c9c9426db12a3c0f7fea6b68a582c10759553`, the adopted 18-file fan-in, and that measured execution remains held until the exact R6X stopped-ledger reconciliation receipt is returned.

## Court interpretation rule

Evidence that a candidate shares the same semantic owner is not treated as proof that a later measured benchmark has passed. Conversely, the absence of a measured benchmark while HQ has explicitly held execution is not treated as semantic failure. This return audits succession law and code paths only.
