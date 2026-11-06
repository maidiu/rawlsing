# A — observed original SRC15 coordinate boundary — R4 return

**Job:** `PROGRAMMA-PYAT-UNIVERSAL35-SOURCE-MAPPING-20261106-R1`
**Branch:** `codex/pyat-universal35-src15-coordinate-20261106-r1`
**Start/D r7:** `f295f90f2dc2202055ddf21b575776621260b118`
**Accepted A state:** `cf44c5df67863c040ac2424e27413d0101917c40`
**C state review:** `061d1dd71591863375110e451ddc49c1ee8cf6aa`
**Status:** `AUTHOR_TESTED__SRC15_COORDINATE_BOUNDARY_BOUND__C_ADAPTER_HANDOFF__INDEPENDENT_REVIEW_REQUESTED`

## Exact finding

D r7 selected coordinate `age_r2` (physical ordinal 313, `double`) for SRC15.
The exact SAV metadata declares a missing range `-10..-1` and substantive age
codes `1`, `2`, `3`. The pinned R157 coordinate slot contained only negative
codes, all with `missing_state=OBSERVED_STORAGE_VALUE`, and omitted `1/2/3`.

Observed old boundary:

- `old_unbound_cells = 59,438`
- missing-code cells: `-1` 13, `-2` 312 (325 cells)
- observed age-code cells: `1` 9,840; `2` 19,342; `3` 29,931
- exact old refusal:
  `SourceBackedC11FacadeError: unbound/missing coordinate cannot acquire semantics`

This is a source/config coordinate binding gap, not source absence, not a missing
respondent key, and not a new coordinate-science claim.

## Smallest lawful correction

Added source/hash/base-commit/base-path-bound SRC15 coordinate correction:

- 8 negative codes `-10..-1` → `FORMAT_USER_MISSING_RANGE` with the exact declared
  range `{'kind':'range','lo':-10.0,'hi':-1.0}`; existing coordinate states
  (`UNKNOWN`, `MISSING`, `NOT_LAWFULLY_CONDITIONABLE`) preserved.
- 3 observed age codes `1/2/3` → `OBSERVED_STORAGE_VALUE` with
  `coordinate_state=UNKNOWN`, not a valid semantic coordinate, under the existing
  `R157-EVS-SRC15-COORDINATE-DEFER` authority.
- No label/frequency meaning inference, no canonical coordinate value, no new
  authority, no source-specific code branch.
- Public `build_coordinate_slot_rules(config)` added for the existing
  materialization owner. The C-owned `materialize_native_preimages` adapter still
  constructs an empty coordinate rule list; it must consume these rules or
  equivalent exact config values. That is a named C-owner dependency, not a
  competing A edit.

## Proof

`evidence_src15_coordinate_boundary.json`:

| Check | Result |
|---|---|
| Old `age_r2` binding | **RED** exact unbound/missing coordinate refusal |
| Corrected binding | **PASS**, 0 untyped, 0 unbound cells |
| Corrected typed states | `-1 UNKNOWN`, `-2 MISSING`, `1/2/3 UNKNOWN` |
| Proof wall / peak RSS | 143.93 s / 604 MB |
| SRC15 identity | 474 items, 474 slots, 337 response, 86 coordinate slots |
| Fixture receipt | unchanged and matching |

`evidence_pytest.txt`: **43 passed**. SRC31 correction remains 31 changes;
remaining-seven/composite/provenance accepted state remains unchanged; 35-source
and 18,276/18,413/18,250/26 denominators remain unchanged.

## PROGRAMMA_DELTA

- **Identity:** SRC15 source `95096c24…`; correction bound to R157
  `1924499e…` and exact base config hash/path.
- **Function:** exact coordinate missing-range binding plus typed unknown observed
  age codes; no semantic coordinate issuance.
- **Input → typed output:** exact SAV coordinate cell → typed coordinate fact
  (`UNKNOWN`/`MISSING`/`NOT_LAWFULLY_CONDITIONABLE`).
- **Root/schema/clock/permission:** no change; no source/native/science/actor grant.
- **Actual first consumer:** `build_coordinate_slot_rules` → existing
  materialization owner; full C11/native remains NOT_RUN.
- **Affected IDs:** SRC15 `age_r2` only.
- **Next action:** C consumes exact coordinate rules; independent review of this
  R4 delta; no full release claim.

## Limits

- Actual original native/full release remains NOT_RUN; D r7 native facts were not
  emitted and are not claimed here.
- No respondent rows, native keys or raw source bytes were printed or committed.
- C-owned adapter remains the exact remaining consumer dependency.
- Unadopted until independent review and qualified protected receiving.
