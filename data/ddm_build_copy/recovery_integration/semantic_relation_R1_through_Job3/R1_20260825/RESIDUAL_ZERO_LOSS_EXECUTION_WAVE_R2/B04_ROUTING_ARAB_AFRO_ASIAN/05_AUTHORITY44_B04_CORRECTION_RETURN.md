# B04 — AUTHORITY 44 CORRECTION RETURN

## Governing correction

Read and obeyed:

`data/ddm_build_copy/recovery_integration/semantic_relation_R1_through_Job3/R1_20260825/44_PROVISIONAL_700_TRIAL_SET_NONAUTHORITY_AND_ROUTING_DENOMINATOR_CORRECTION.md`

Exact authority commit: `9d845a71c767addd45a106c00f13ff523ca3676c`.

Authority 44 demotes the historical 700-row trial set and every partition derived from it (`99`, `320`, `280`, `600`, `699`) to **forensic history only**. They do not define the modern routing denominator, completeness universe, zero-loss gate, or current routing debt.

This correction is additive. The original B04 artifacts at worker commit `d0388feb0390f4bdfb0f0e7bb0f44e8b4031a88e` remain preserved as historical execution/provenance. They are not rewritten or erased.

## Revoked B04 modern framing

The following claims from the pre-Authority-44 B04 return are superseded as modern claims:

- `127` is **not** a current B04 routing denominator;
- `4 + 7 + 116` is **not** a complete modern routing disposition partition;
- `116` is **not** a current unresolved-routing debt count;
- the 11 useful source-native findings are **not** a completeness delta against a current denominator merely because they occurred in the historical trial slice.

The 127-row slice remains usable only as a forensic/regression witness set.

## Lawful current substrate

Authority 44 requires current routing completeness to begin from the full governed active implementation universe.

Validated active catalog:

- artifact: `Rawlsing_P2_Phase0_Governed_Question_Node_Catalog_v1.json`
- SHA-256: `2a13ca0551f812e71ad254ab65e3f1ccf99ccfa789eeac4ade708cdbfaa568b8`
- closure payload SHA-256: `cfab0692c5a6f66d7f4038d998af3ec3db5898aa1ca473ba61c9ad56c744ae9d`
- expected active implementations: **18,276**
- cataloged active implementations: **18,276**
- active waves: **35**
- source families: **9**

B04 does **not** recompute the modern full routing/applicability court here. That requires disposition accounting over all 18,276 exact current implementations under Authority 44.

## Salvaged source-native evidence rebound to current implementations

The useful B04 findings survive only as exact current-implementation evidence bindings. `06_AUTHORITY44_CURRENT_18276_IMPLEMENTATION_REBINDINGS.csv` records the full binding surface, including the current question-authority ref, the catalog's pre-install routing/universe refs, and the source-native evidence type.

All 11 retained findings pass both identity checks:

1. the exact `question_implementation_id` exists in the 18,276-row catalog;
2. the exact `(source_family, wave, source_variable_code)` key resolves to **one and only one** current implementation.

### Executable routing evidence — 4 exact current implementations

- `question_impl.phase0.b45336f05b20fdc96b27` — Arab Barometer II `q408` — recovered predicate `Q407 IN {1,2,3,4,5}`.
- `question_impl.phase0.6fd4afa9020defb0185d` — Arab Barometer V `Q412A4` — recovered predicate `Q409 IN {1,2,3,4,5}`.
- `question_impl.phase0.09784157d9d0405db073` — Arab Barometer V `Q412A9` — recovered predicate `Q409 IN {1,2,3,4,5}`.
- `question_impl.phase0.4058750de342b45b0ca3` — Arab Barometer V `Q104B_OTHER` — recovered predicate `Q104A == 1 AND 24 IN Q104B_SELECTIONS`.

The prior hostile-positive, hostile-negative, and deterministic replay evidence remains valid forensic execution evidence for these exact current identities. This correction does not claim that four rows exhaust modern executable-routing obligations.

### Country-specific nonapplicability evidence — 7 exact current implementations

- `question_impl.phase0.59f15be71a6f92ad9394` — Afrobarometer R1 `sapknw`: source authority affirmatively excludes Lesotho.
- `question_impl.phase0.2803d0306db87d5e9f30` — Arab Barometer II `ir52010`: Iraq-only source item; Jordan exclusion evidence.
- `question_impl.phase0.48656478051f6b3df181` — Arab Barometer II `eg8117`: Egypt-scoped source item; Jordan exclusion evidence.
- `question_impl.phase0.4641a9815eae66664458` — Arab Barometer II `eg8033`: Egypt-scoped source item; Jordan exclusion evidence.
- `question_impl.phase0.b56695341d4bb93d33d3` — Arab Barometer II `t50111`: Tunisia-only source item; Jordan exclusion evidence.
- `question_impl.phase0.5b31db6a2b9fae455d32` — Arab Barometer II `t3046`: Tunisia-only source battery member; Jordan exclusion evidence.
- `question_impl.phase0.491e37056081b6c2cbe0` — Asian Barometer W5 `Q106e`: India-only source item; Singapore exclusion evidence.

These are **country-scope evidence bindings**, not declarations that the entire wave-level implementation is globally absent/nonapplicable. The current P2 catalog still carries pending deep-review routing/universe contracts for these implementations; this B04 correction supplies sidecar source authority for a later full modern routing court rather than silently mutating that catalog.

## What does not survive as current authority

The old B04 rows that received `STILL_UNRESOLVED__SOURCE_AUTHORITY_INSUFFICIENT` do not become 116 current unresolved obligations. Their historical state remains preserved, but old sample membership has no authority to say those are the modern debt rows—or that rows outside the sample are not debt rows.

Likewise, historical `FAIL_CLOSED_UNRESOLVED` / `FAIL_CLOSED_NO_SOURCE_ROW_MATCH` labels remain forensic facts about the old trial set only. They are not current denominator membership classes.

## Validation

- Authority 44 read at exact commit: **PASS**
- 18,276 expected = 18,276 cataloged: **PASS**
- retained current implementation IDs present: **11 / 11 PASS**
- exact family/wave/variable current-key uniqueness: **11 / 11 PASS**
- retained executable-routing evidence bindings: **4**
- retained country-nonapplicability evidence bindings: **7**
- historical B04 artifacts deleted or rewritten: **0**
- old 116-row unresolved count promoted to current debt: **0**
- `99` or `600` used as current routing universe: **NO**
- modern routing completeness claimed by B04: **NO**

## HQ disposition

B04 is salvaged under Authority 44 as a bounded **source-authority acquisition and exact-current-implementation rebinding return**. It is no longer a modern completeness court.

The next lawful completeness court must derive its denominator from the entire 18,276-row governed active surface and may consume these 11 rebound evidence records at their exact implementation/country-routing grain.

`B04_AUTHORITY44_CORRECTION_COMPLETE`
