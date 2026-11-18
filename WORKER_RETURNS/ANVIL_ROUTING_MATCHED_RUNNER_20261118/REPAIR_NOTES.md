# RUNNER REPAIR NOTES

Original commit `c79d1a33...` preserved. Corrections in this revision:

- explicit `MEASUREMENT_PREP = HERE.parents[2]` and shared Git path; no engineering-parent inference;
- supervisor imports `process_tree_rss_bytes`/`directory_bytes` inside its own scope;
- `RUN_RESULT.json` is a file under the output directory, not a write to the directory;
- cumulative total cap enforced after each child; baseline overrun also refused;
- nonzero/abort child is gated before the next variant or comparison, with partial `RUN_RESULT.json`;
- estate scratch sampled as `directory_bytes(estate_root) - retained_bytes`, excluding the retained estate baseline; owned output bytes tracked separately;
- routing reconstruction counted in S and Q via a transparent `_object_from_row` wrapper for `RoutingEligibilityFact`, in addition to `_routing_fact_for` calls;
- exact expected operation set `{f2_forward, f2_reverse}` checked on both variants before comparison;
- runtime API/path check against the frozen baseline snapshot passed (class, instrumentation, catalog query names/refs); no native query/build executed;
- logs/timers/abort details retained in per-variant/partial results.

No product, raw-source, science, actor, CURRENT or protected edit. No heavy run. Candidate pin remains the exact frozen repaired routing commit, not the rejected `73b480...`.
