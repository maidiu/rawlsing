# Exact Preservation Disposition Ledger

Status: `ALL_CENSUS_UNITS_HAVE_LAWFUL_NON_GAP_DISPOSITION`

Canonical census accounting units: **65,354** across 45 non-overlapping census rows.  
This count deliberately excludes C3 provenance-only/defective-shadow records from authority-bearing census count and does not double-count P5/P6's 712 objects again under P8; P8 contributes 38 shared-policy authority objects while its 10,746 policy-membership links remain crosswalk edges.

## Disposition counts
- `CURRENT_LIVE_AUTHORITY_PROVED`: **1**
- `CURRENT_LIVE_AUTHORITY_JURISDICTION_PROVED__POSITIVE_LOAD_UNPROVED`: **1**
- `PRESERVED_BY_EXACT_GOVERNED_REFERENCE_TO_FROZEN_AUTHORITY`: **40,576**
- `PRESERVED_BY_TYPED_LIFECYCLE/SUCCESSION_TO_CURRENT_AUTHORITY`: **24,643**
- `PRESERVED_AS_EXACT_UNRESOLVED/BLOCKED_AUTHORITY`: **76**
- `PRESERVED_AS_CONSTRAINT/NONINFERENCE_LAW`: **49**
- `PRESERVED_AS_PROVENANCE/REPLAY_REQUIRED_FOR_AUTHORITY_INTERPRETATION`: **7**
- `FUNCTION_PRESERVED__HISTORICAL_MECHANISM_COMPOSTABLE_AFTER_BROADER_RELEASE`: **1**
- `OUTSIDE_P10_JURISDICTION__GOVERNED_OWNER_PROVED`: **0**
- `UNRESOLVED_AUTHORITY_PRESERVATION_GAP`: **0**

The 76 explicitly unresolved units are preservation-complete governed states, not hidden omissions:
15 P6 BLOCKED + 42 B04 + 4 B06 + 7 B07 functions + 8 B08 functions.

No unresolved item is widened into FALSE, REJECT, current selection, or absence.
