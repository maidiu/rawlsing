# R9 — G adverse validation repairs

**VERDICT:** C repairs the two exact G `e05ff071…` defects. Code head `68980922c2748066e4481b0d222cc313256f3502`; prior candidate `8c5e8236…`; G review target `6f9e41f3…`.

## Release reuse repair

An attached `C11LogicalRelease` is no longer accepted from caller hashes alone. Before reuse, C now rechecks the existing binding material:

- release id, source artifact object/hash, and projection source SHA;
- `semantic_release_hash` recomputed from the release replay projection hash, replay manifest ref, and M01–M18 coverage;
- replay manifest authority-snapshot-set hash against actual authority snapshots;
- source substrate binding to the release artifact;
- replay closure refs against source snapshot, public objects, and internal records.

A `dataclasses.replace(prebuilt_release, semantic_release_hash="0"*64)` is now RED/refused. Valid prebuilt release reuse and exact release/replay refs remain PASS. This is existing binding validation, not a new signature framework; full SRC10 reuse timing was not rerun, so no performance claim.

## Coordinate rule repair

Caller-provided coordinate rules are selected by exact name/ordinal and now require source-qualified native-coordinate and unit-taxonomy references using existing authority/provenance tokens; a rule with correct slot/ordinal but `urn:wrong:source` is RED/refused. Valid explicit rules preserve A's typed `UNKNOWN`/`MISSING`/DEFER states. The legacy fallback remains for backward compatibility; actual SRC15 join is still **NOT_RUN** and no age meaning is inferred.

## Evidence

- `results/g_repair_tests.log`: 28 scale/facade/universal tests PASS, including adverse tampered-release and foreign-coordinate RED cases.
- Release valid reuse still exact; wrong source/projection still refused; coordinate UNKNOWN test still exact.
- Prior scale limits remain: SRC10 materialize 169.3 s, compile >425.9 s at 601.8 s / 2.07 GB, 0 facts; SRC09 materialize >347 s / 1.64 GB. No full-scale improvement is claimed.
- No original 600 s rerun, no native/all35/science/16-GiB claim, no protected adoption/self-review.

## PROGRAMMA_DELTA

`C_RELEASE_REUSE_VALIDATION = REPAIRED_SCOPED; COORDINATE_RULE_SOURCE = REPAIRED_SCOPED; FULL_PLAN = HOLD`: exact G adverse probes now RED->PASS for valid repair; final compile-stage sharing remains a separate D/universal-workload dependency.
