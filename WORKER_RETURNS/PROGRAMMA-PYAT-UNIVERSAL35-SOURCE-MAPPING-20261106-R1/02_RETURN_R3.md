# A — exact reviewed composite-state and fail-open repair — R3 return

**Job:** `PROGRAMMA-PYAT-UNIVERSAL35-SOURCE-MAPPING-20261106-R1`
**Branch:** `codex/pyat-universal35-source-mapping-20261106-r1`
**Continues:** `7f3931607d1309e84ad068c353946831248184b3`
**C review:** `d731f0a15a54d6e664ac181c5e1be691f5be9f51`
**Status:** `AUTHOR_TESTED__COMPOSITE_STATES_CONSERVATIVE__FAIL_CLOSED__INDEPENDENT_REVIEW_REQUESTED`

## C findings repaired

- **362 composite/ambiguous labels** previously mapped to precise
  `DK`/`NOT_ASKED`/`REFUSAL` are now `SOURCE_SPECIFIC_SPECIAL`.
  - SRC16 `dk, na, iap`: 154
  - SRC24 `No answer/Refused`: 182
  - SRC25 composites: 24
  - SRC26 composites: 2
  - remaining precise composite mappings: **0**
- **Fail-open default removed.** An `add_if_absent` change without explicit
  `response_state` now defaults to `INVALID_UNRESOLVED`, never substantive.
- **95 existing substantive→missing transitions accounted**: SRC24 4, SRC25 91.
  All 95 carry exact declared missing metadata and are warranted; unwarranted = 0.
  No claim of unbound-only additions.
- SRC31 correction remains frozen and unchanged. No substantive additions exist
  in the registry.

## Preserved

- trusted source SHA/base canonical hash/base commit/base path enforcement;
- R157 pinned objects and SRC31 `ef43bbbbb` correction;
- fixture identity and 35 / 18,276 / 18,413 / 18,250 / 26 denominators;
- zero corrected unbound keys for the seven remaining sources;
- no D/C/E/guide/controller/protected edits.

## Evidence

- `evidence_composite_state_repair.json` — 362 exact replacements, 0 remaining.
- `evidence_state_authority_repair.json` — 0 substantive additions, 95 warranted
  substantive→missing transitions, 0 unwarranted.
- `evidence_binding_contract.json` — provenance refusal/restore still passes.
- `evidence_remaining7_boundary.json` — old unbound > 0, corrected = 0.
- `evidence_pytest.txt` — **49 passed**.

## PROGRAMMA_DELTA

- **Identity:** same registry/loader; SRC31 frozen; C-reviewed R2 delta corrected.
- **Function:** conservative composite-state handling + fail-closed add default.
- **Input → typed output:** exact declared missing metadata → missing state +
  `SOURCE_SPECIFIC_SPECIAL`/`INVALID_UNRESOLVED`, not precise label inference.
- **Root/schema/clock/permission:** no change; no source/native/science authority.
- **Actual first consumer:** corrected `SourceConfig` → current physical response
  projection; full release still NOT_RUN behind positive-authority DEFER.
- **Affected IDs:** SRC16/24/25/26 composite-label values; SRC31 untouched.
- **Next action:** independent review of this R3 delta only; then D integration.

## Limits

- Mapping/state boundary only; full C11/native facts NOT_RUN.
- No respondent rows, native keys or raw source bytes published.
- Unadopted until independent review and qualified protected receiving.
