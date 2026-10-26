# R153 — repair R152 native-evidence promotion defects

**Status:** `R152_WVS_PROMOTION_REPAIRED__UNKNOWN_ADMINISTRATION_HELD__SUPPORTED_FIELDS_PRESERVED`
**Base:** `e3a95fef6eecfbac56341553cf3482ccd750a351` (R151 preserved/read-only)
**Scope:** metadata/authority only. No survey file was opened, stat'ed, hashed or decoded; no current source/science/access grant.

## Exact R152 RED repaired

R152 found WVS7 `NativeSourceRule.administered=true` alongside an Occurrence with
`administration=UNKNOWN`, plus hardcoded unit/topology and `DEFAULT_FORM`. R153
consumes the exact WVS7 source-specific runtime package and finds:

- exact source SHA, response topology (`SCALAR_SINGULAR`), risk-set binding,
  source/routing authority IDs — all preserved with package hash;
- **no exact WVS7 source unit, form or administration field** in that package;
- therefore no `Occurrence`, `NativeSourceRule` or `SourceInventory` is
  constructed for WVS7. The dependent objects are held rather than promoted;
- no `administered` boolean and no `DEFAULT_FORM` is emitted for WVS7.
- Held dependent objects are counted explicitly: 2 WVS occurrences, 2 WVS
  NativeSourceRules, 1 WVS SourceInventory; none is claimed constructed.

The two WVS7 item records retain their exact typed domain/topology/risk fields
and now expose exact missing owners:
`WVS7_SOURCE_UNIT_AUTHORITY_OWNER`, `WVS7_SOURCE_FORM_AUTHORITY_OWNER`,
`WVS7_SOURCE_ADMINISTRATION_AUTHORITY_OWNER`. This is an honest dependent-object
hold, not a blanket source unknown.

## Preserved evidence

- B49 records: **4,460**; typed-surface-only items: **33**; preparation items: **4,493**.
- 38/38 typed surfaces consumed; 3,804 conditioner/context items; 26 unmatched relation holds; 35 source cells.
- R148 current codebook denominator: **18,276** rows retained by reference.
- LiTS-I q301_2/q301_7 domain, D03 risk set and selected-respondent unit remain
  resolved; topology remains an exact item-level gap and no fake Occurrence is
  created.
- Current source access/edition/U/Epre/response grants remain null; planner/lowerer
  is not invoked; no empirical/learned/FF claim.

## Next dependency

The WVS7 dependent native objects require an exact source-specific authority for
form, unit and administration. The next call remains
`rawlsing_next.pre553_source_read_admission.decode_with_source_read_permission`
but is blocked on current source identity/edition plus an exact response-read
grant; metadata and the WVS7 runtime package do not authorize decode.

## Verification

- Focused R153 checks: **5 passed** (`evidence/focused.log`).
- Proved: no WVS rule/admin bool, no default form, exact WVS topology/risk/domain
  preserved, honest holds, LiTS partial fields preserved, 4460/4493/3804/26/38/18276
  conservation, foreign WVS source refusal, no decoder/survey call.
- CLI probes: SRC27, SRC35.
- Receipt: `evidence/PROOF_RECEIPT.json`.

## Limits

No source/respondent access, current U/Epre, source grant, empirical/learned/FF
execution or adoption. Full35/1890/F1–F8/global/LongMemory/C5 and all
R09/CI/prod/N11/N12/Sorok/J52/W52/actor holds remain. Native core read-only at
`44e7ace44d9e1b023a15d14ee1ead9b176d0e522`.
