# R152 coverage and limits

## Scoped result

- Partial documentary native typed binding: **PARTIAL PASS**.
- Exact joins/conservation/context/unmatched/source cells: PASS.
- Typed surfaces/domains and LiTS partial resolution: PASS.
- Actual WVS Occurrence + incomplete SourceInventory: PASS at object/type level.
- WVS unknown administration/source-specific defaults: **FAIL**; `NativeSourceRule`
  administered=true while Occurrence administration=UNKNOWN, and form/unit/
  topology are hardcoded/default.
- No current source/grant/U/Epre/planner invocation: correctly retained.
- No raw source or decoder access: verified.

## Demonstrated values

- B49 records 4,460; preparation 4,493; context 3,804; unmatched 26; sources 35.
- 38 typed surfaces; 18 exact typed domains; 17 raw codebook domains; 4 units;
  2 topologies; 4 risk sets.
- WVS Q291G5/Q291P5 domain `[1,2,3,4,5,-1,-2,-4,-5]`; exact WVS7 risk set;
  incomplete inventory with 2 occurrences and explicit gaps.
- LiTS q301_2/q301_7 domain/unit/risk resolved; topology unresolved; no fake
  occurrence.
- Current source identity/permission/U/Epre null; native execution unauthorized.

## Blocking defect

WVS rules assert `administered=true` despite the same occurrences carrying
`administration=UNKNOWN`; forms default to `DEFAULT_FORM`; WVS unit/topology are
hardcoded literals rather than extracted from the exact source package. This is
a false typed administration/default promotion and not an exact evidence-bound
native input.

Exact owner: `WORKER_RETURNS/PYAT-R151-GROUNDED-NATIVE-OCCURRENCES-R1/runtime/grounded_occurrences.py`,
`_wvs_package`/`_wvs_surfaces` (unit/topology constants, `administered=True`,
`forms=("DEFAULT_FORM",)`). Minimal fix: bind exact WVS admin/unit/topology/form
evidence or leave them pending and do not construct the rule; retain partial
occurrences/inventory with honest counts.

## Limits

No actual source/respondent, current edition/grant, U/Epre, scientific frontier,
empirical/learned/FF execution or current adoption. No all35/1890/F1–F8/global
F6/F7/F8/LongMemory/C5, R09/CI/prod, N11/N12, Sorok/J52/W52, actor or source/
science claim. No candidate edit, source fixture as original positive, new
worker/engine or broader court.
