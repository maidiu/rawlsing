# P3A v40 reporting seam repair

The executable v40 DDL and loader use the normalized tables:

- `p3_pair_projection_semantic_identity` + `p3_pair_projection_semantic_binding`
- `p3_candidate_component_semantic_identity` + `p3_candidate_component_semantic_binding`

The packaged report generator still queried two obsolete denormalized table names ending in `_semantic_fingerprint`. The repair changes only the two read-only report queries to join the actual identity and binding tables. No DDL, loader, candidate hash, evidence bundle, or authority table was changed.
