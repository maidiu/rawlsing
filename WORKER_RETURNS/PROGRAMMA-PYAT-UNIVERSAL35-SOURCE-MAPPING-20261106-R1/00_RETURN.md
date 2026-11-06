# A — SRC31 source/config unbound-response boundary — return

**Job:** `PROGRAMMA-PYAT-UNIVERSAL35-SOURCE-MAPPING-20261106-R1`
**Branch:** `codex/pyat-universal35-source-mapping-20261106-r1`
**Start/D repro:** `115fe70e660fb19a65ca49b4a12ffc8876be065c`
**Source-pack branch preserved:** `9eaf9dd145409d8aedf583226c7c99d663c43abc`
**Guide branch preserved:** `6c243ffee042187092fead1e7a25f0f838578b9e`
**Status:** `AUTHOR_TESTED__SOURCE_MAPPING_BOUNDARY_REPAIRED__INDEPENDENT_REVIEW_REQUESTED`
**Implementation/evidence SHA:** reported by terminal push readback.

## Finding — exact cause

The current original SRC31 SAV reaches the current C11 factory and refuses:

`SourceBackedC11FacadeError: unbound response value/state; no label/frequency/missingness inference`

The exact cause is a source-config factual binding gap, not source absence:

- 11 SRC31 response slots have physical decoder keys not bound by the pinned R157 config.
- 14 config values are declared user-missing by the SAV metadata but were bound as
  `OBSERVED_STORAGE_VALUE / SUBSTANTIVE_RESPONSE`:
  `c10ai` 98/99; `c12`, `c17`, `c18a/b/d/e` 0/8; `d3` 9; `d13` 9.
- 17 observed codes in `d7`/`d12` are not declared in the SAV value labels or the
  pinned config. They are **not** mapped by label/frequency. They remain typed
  `INVALID_UNRESOLVED` physical response facts.
- The old config has 14,933 unbound cells across those 11 slots. The D prescan
  count `SRC31=325` is exactly the `d7`/`d12` unlabelled-code cells, not the
  user-missing-code cells.

## Interpretation

This is response/config compatibility, not `SOURCE_NOT_PRESENT_HERE`, not a
missing weight, and not a reason to invent response meaning. The correction uses
the exact SAV-declared value labels and missing declarations and the exact pinned
R157 config lineage. No source/native/science/actor authority is minted.

## Action — smallest resource patch

Added `rawlsing_next/source_configuration/corrections/SOURCE_CONFIGURATION_CORRECTIONS.json`
and `corrections.py`:

- Correction is versioned resource data, bound to `source_id`, exact original
  source SHA-256, base R157 commit, exact base config path and base canonical hash.
- Applied only to `ORIGINAL_SOURCE / SOURCE_PREPARATION`; fixtures and unrelated
  sources are unchanged.
- 31 changes: 14 exact user-missing replacements and 17 typed
  `INVALID_UNRESOLVED` additions.
- Exact response states from declared labels: 7 DK, 3 NOT_ASKED, 4
  SOURCE_SPECIFIC_SPECIAL, 17 INVALID_UNRESOLVED.
- `SourceConfig.corrections_applied` and `SourceConfigLibrary.select/validate_source`
  expose the applied correction list. `ABI.json` documents the correction ABI.
- No survey-name branch was added to the factory/facade/kernel; no pinned R157
  object was rewritten.

## Proof — RED / PASS

`evidence_src31_boundary.json` (reproducible via `probe_src31_boundary.py`):

| Case | Result |
|---|---|
| Old pinned config + current decoder, selected affected original columns | **RED** `SourceBackedC11FacadeError: unbound response value/state` |
| Corrected same-source config + same decoder/current facade consumer | **PASS** 92,862 response events |
| Corrected states | DK 13,497; MISSING 6,387; NOT_ASKED 1,111; INVALID_UNRESOLVED 325; SUBSTANTIVE_RESPONSE 71,542 |
| `c10ai` 98/99 | `DK` / `NOT_ASKED`, exact user-missing declarations |
| SRC31 fixture release | receipt match `85fc1d3ca2acffcf41244ac9e4f41a2664dd7d86fd6a4b53194baa8bf7702189` |

The proof reads only selected affected original response columns plus routing, not
the full eager release. Full release validation is **NOT_RUN** because the next
gate is a separate positive-authority `DEFER`; that is not a mapping failure and
is not claimed as PASS.

## Tests

`evidence_pytest.txt`: **43 passed** across the source-configuration foundation,
library, source-read admission, current-port and correction tests. `evidence_pytest` includes:

- correction source/base-hash binding;
- old config user-missing values become typed missing;
- undeclared observed codes become typed unresolved, not substantive;
- fixture config is not corrected;
- SRC31 item/slot/response denominators remain 68/68/64;
- all35 estate denominators remain 35 sources / 18,276 items / 18,413 slots /
  18,250 joins / 26 unmatched.

## FINDING | INTERPRETATION | ACTION | OWNER

| FINDING | INTERPRETATION | ACTION | OWNER |
|---|---|---|---|
| SRC31 config bound declared user-missing codes as substantive and omitted 17 observed undeclared codes. | This is an exact source/config mapping gap, not source absence or a global stop. | Versioned source/hash-bound correction: exact missing states + typed unresolved unknown codes. | A source-pack owner; HQ review |
| Old config refuses the whole release on the first unbound value. | The facade correctly refuses inferred semantics. | Bind exact facts; do not coerce or infer labels/frequencies. | Current facade owner (read-only) |
| Full release then hits positive-authority DEFER. | Mapping boundary is repaired; native/authority is separate. | Preserve HOLD; no source/native grant. | Original source/authority owner |

## PROGRAMMA_DELTA

- **Identity:** SRC31 original source `de7b51f9…`, base R157
  `1924499e…`, correction registry
  `rawlsing_next/source_configuration/corrections/SOURCE_CONFIGURATION_CORRECTIONS.json`.
- **Function:** source/hash-bound response-value/missingness binding correction.
- **Input → typed output:** pinned SRC31 config + exact SAV physical keys → corrected
  `SourceConfig` with 31 applied corrections → typed `RespondentEvent` states.
- **Root/schema/clock/permission:** no source root or schema change; no clock,
  native grant, actor right, or raw source byte publication.
- **Actual first consumer:** current source-config factory/facade physical-cell
  projection over selected original SRC31 columns.
- **Evidence:** `evidence_src31_boundary.json`, `evidence_src31_correction_summary.json`,
  `evidence_src31_fixture_identity.json`, `evidence_pytest.txt`.
- **Affected IDs:** SRC31 response slots `c10ai`, `c12`, `c17`, `c18a/b/d/e`,
  `d3`, `d7`, `d12`, `d13`; no item/slot/join denominator change.
- **Conditional unlocks:** D can consume corrected original SRC31 selected columns;
  full release still awaits positive authority and C stream adapter.
- **Next action:** independent review of this exact head; then D integration.

## Independent review request

Review this exact branch head as a nonauthor source-mapping patch: verify the
correction is source/base-hash bound, that user-missing codes are not substantive,
that undeclared observed codes remain typed unresolved rather than label-mapped,
that fixtures/other sources are unchanged, and that the old-config RED plus
corrected original-column PASS reproduce.

## Limits

- Selected-column genuine original proof, not full all35 native execution.
- Full C11 release remains behind positive-authority DEFER; no facts or native
  acceptance claimed.
- No respondent rows, native keys or raw source bytes were printed or committed.
- This patch is unadopted until independent review and qualified protected
  receiving.
