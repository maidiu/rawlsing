# UNIVERSAL35 A mapping R3 independent closure review

**VERDICT: ACCEPT_SCOPED_ENGINEERING** at A head `cf44c5df67863c040ac2424e27413d0101917c40`, delta `7f3931607d1309e84ad068c353946831248184b3`.

- **Mechanism/fail-closed default: ACCEPT_SCOPED_ENGINEERING.**
- **Composite-state repair: ACCEPT_SCOPED_ENGINEERING.**
- **95 substantive→missing transitions: ACCEPT_SCOPED_ENGINEERING** for the checked source-declared metadata.
- **Actual projection state propagation: ACCEPT_SCOPED_ENGINEERING.**
- **Preserved provenance/freeze/denominators: ACCEPT_SCOPED_ENGINEERING.**
- **Full C11/native/empirical: NOT_RUN**, separate from mapping acceptance.

## FINDING

The exact R3 delta repairs the C R2 findings without changing any other correction field:

- Registry keys are unchanged (6,125 response-value changes, same key set).
- 362 changes differ, and only `response_state` differs; every one is the exact R2 composite precise-state set and is now `SOURCE_SPECIFIC_SPECIAL`.
- Remaining composite labels mapped to precise `DK`/`NOT_ASKED`/`REFUSAL`: **0**.
- Added substantive response values: **0**.
- Omitted `response_state` on `add_if_absent` now defaults to `INVALID_UNRESOLVED`; no substantive fallback.
- 95 existing substantive→missing transitions remain accounted: all have declared missing metadata, source labels match actual SAV metadata, and no unwarranted transition was found. One transition is among the 362 state replacements; only its response state changed, not its declaration.
- Actual factory projection on SRC16 (2,538 corrected values) and SRC31 (31 corrected values) found every corrected physical key with the declared typed state; zero projection misses.

No remaining C R2 factual-state defect was found in this delta.

## EVIDENCE

- Targeted suite: **49 passed** (`results/pytest_49.log`).
- Focused composite/default/transition tests: **3 passed** (`results/r3_repair_tests.log`).
- Repair-set audit: `results/repair_audit.json`.
  - old/new keys 6,125/6,125 and identical;
  - 362 changed entries, only `response_state`;
  - R2 composite set == changed set;
  - 0 remaining precise composite, 0 substantive additions;
  - 95 transitions all declared missing.
- Source metadata/state probe: `results/state_probe.json`.
  - all eight entries mismatch-free against actual declared missing metadata/labels;
  - no substantive additions;
  - SRC16/SRC31 actual projection states match, zero missing.
- Provenance/freeze/denominators are unchanged by the R3 delta (only `corrections.py`, the registry, and its test changed). Prior R2 independent probes remain valid: exact R157/SRC31 freeze, wrong commit/path/loaded-path/registry refusal and exact restore, fixture/unrelated identity, 35 / 18,276 / 18,413 / 18,250 / 26 baseline.

## LIMITS

- Mapping/state closure only; full C11/native facts, all35 fixture floor, genuine original facts, 600-second scans, and native/science/actor acceptance remain **NOT_RUN**.
- No code fix, self-review substitution, protected merge, or A/D/E/guide/controller edit.
- No respondent rows, native keys or raw source bytes are published.

## PROGRAMMA_DELTA

`MAPPING_R3_REVIEW = ACCEPT_SCOPED_ENGINEERING`: 362 composite precise states conservatively replaced, fail-open default removed, 95 transitions accounted, no remaining composite precise state or substantive addition; projection and provenance scopes retained. Full C11/native remains separate and NOT_RUN.
