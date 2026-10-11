# HQ280 PV3 A01 — Native Topology Identity Gaps

**Documentary gap analysis only. No semantic, model, or operation-use grant. No canonical mutation.**

Scope: `RAWLSING_HQ280_LR_A_CROSSWALK@1.0.0` — 18,276 implementations across 35 waves / 9 families,
cross-checked against LR-A primary archive
`RAWLSING_HQ280_LR_A_SOURCE_SCIENCE_FORENSIC_RETURN_R1.zip`
(sha256 `e201e7923e1d34520dec7134a51e338b5204d55e39c3caa6a51b65888663600b`).

## G1 — Governed grain is "historical implementation", not "original measured item"

Every implementation carries
`grain = HISTORICAL_IMPLEMENTATION__NOT_AUTOMATICALLY_ORIGINAL_MEASURED_ITEM`.
An implementation is an *observed variable-in-wave binding asserted by historical carriers*,
not proof that the variable is a measured instrument question on that wave's physical form.
**No original-item count may be inferred from `implementation_count`.** This is a native
identity gap, not a defect: the crosswalk refuses to overclaim by construction.

- `implementation_count` = 18,276 (all rows).
- Non-measurement / context / administrative typed retained (never zero-filled):
  - `MEASUREMENT_CANDIDATE` 13,270
  - `CONTEXT_NONMEASURE` 4,272
  - `ADMINISTRATIVE_NONMEASURE` 490
  - `DERIVED_NONMEASURE_OR_CONTEXT` 29
  - `NONMEASURE_OR_ADMIN_HINT` 15
- 7 case-variant namespace collisions (same family+wave+casefold var, two exact spellings).

## G2 — Inner-join omission is structurally available

46 carriers exist; only 4 cover 100% of the 18,276 implementations
(`QSM_PROVENANCE`, `QSM_RAW`, `R10K_IMPLEMENTATION_SOURCE_CONTEXT_R1.csv`,
`R10K_O06_IMPLEMENTATION_ROUTING_CENTRAL.jsonl`). The other 42 are partial.

- Deep/Manual per-wave catalogs each cover only their own family/wave (e.g. GSS manual 6,021 = 32.9%).
- `QUESTIONS_MASTER` covers 15,158 (82.9%); `QSR_A` 18,073 (98.9%); `QSR_B`/`QSR_C` 18,235 (99.8%);
  `DRIVERS_D62`/`SEMANTIC_171D` 18,052 (98.8%); `V525B_*` 4,918 (26.9%); QSMV2 blocks 4,438 (24.3%);
  the two `BLOCKED_QSMV2_*` carriers only 41 (0.2%).

**Consequence:** any pipeline that inner-joins to a single carrier silently drops administered
items. The only omission-safe consumption of this crosswalk is a union-of-carriers outer join,
with carrier-presence recorded per implementation (this return does that).

## G3 — Identity evidence is carrier-asserted, adoption unproved

Every implementation carries
`current_adoption_and_operation_permission = UNPROVED_BY_THIS_INVESTIGATOR`.
Exact-coordinate joins (`EXPLICIT_IMPLEMENTATION_ID`,
`EXACT_COORDINATE_CANDIDATE__VARIABLE_CASE_PRESERVED`) are *documentary* bindings; casefold
candidates cannot confer identity; parsed-assertion hashes are not file-byte hashes.

## G4 — Alternative conflicts are mass-present, not edge cases

10,457 of 18,276 implementations (57.2%) carry ≥1 `alternative_conflicts` entry — genuine
disagreement between carriers about the same coordinate. These must be adjudicated by the
source-identity owners (A01 scope) before any downstream consumption treats a binding as settled.
They are retained verbatim, not resolved here.

## G5 — Anti-measurement and unknown cases are retained by design

No original item is silently dropped: administrative/context/derived rows, blockers
(`BLOCKED_QSMV2_*`), and provenance-only carriers are all preserved with typed role classes.
The exit criterion "nonmeasurement and unknown cases retained" is met structurally; semantic
adjudication of each remains with source owners.

## G6 — Exact byte identity is preserved, source-of-truth unavailable in-place

Carriers reference external archive paths; the crosswalk stores per-carrier
`byte_identity` (path + sha256 + bytes). Crosswalk's own `canonical_control_commit`
(`6a8c91d99dca1ae2fd3559ba3c11ee26649e3cd9`) is an LR-A stamp, **not** the operating-HQ
canonical baseline (`a70a069f…` on `integration/pre-main-reconciliation-r1`); no reconciliation
is asserted by this return.