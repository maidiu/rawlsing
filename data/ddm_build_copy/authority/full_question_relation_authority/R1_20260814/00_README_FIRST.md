# Rawlsing Full Question Relation Authority — Final R1

This package completes the July-19 QSM full-universe authority reconciliation requested for the four appended authority fields and the structural coordinates needed to make governed relation status truthful.

## Final target surface
- 18,518 / 18,518 July-19 QSM rows retained in original order.
- `question_structural_mapping_live_PLUS4_FINAL_APPLIED_R1.csv` has the original 23-column schema plus exactly four appended authority fields: `canonical_wave`, `country_code_scope`, `authority_status`, `authority_rule_id`.
- The six structural coordinate columns in that applied surface are the final governed/fail-closed coordinates, not the stale July-19 legacy values.

## Structural completion
- 3,196 / 3,196 relational semantic units integrated.
- 4,438 / 4,438 source implementations structurally adjudicated and block-bound.
- 4,397 formerly blocked structural rows promoted to `GOVERNED_QSMV2_RELATION_AUTHORITY`.
- 41 implementations across 21 units remain `BLOCKED_STRUCTURAL_MAPPING_AUTHORITY`; their explicitly unblocked coordinates are preserved and blocked coordinates remain blank.
- Together with the 225 previously frozen/manual directional rows, the target now contains 4,622 fully governed relation rows.

## Final status counts
{
  "GOVERNED_NON_DIRECTIONAL_DISPOSITION": 12611,
  "GOVERNED_QSMV2_RELATION_AUTHORITY": 4397,
  "GOVERNED_ADMINISTRATIVE_DISPOSITION": 966,
  "EXCLUDED_INACTIVE_WAVE": 259,
  "GOVERNED_MANUAL_RELATION_AUTHORITY": 173,
  "FROZEN_ACCEPTED_GSS": 52,
  "BLOCKED_STRUCTURAL_MAPPING_AUTHORITY": 41,
  "BLOCKED_SOURCE_AUTHORITY": 10,
  "BLOCKED_IDENTITY_OR_AUTHORITY_JOIN": 9
}

## Governance invariants
- 259 Asian Barometer W6 rows remain excluded.
- 10 source-authority blockers and 9 identity/join blockers remain fail-closed.
- 236-row frozen QRA regression remains PASS; 225 of those directional calibration rows physically present in the July-19 target are unchanged.
- No worker namespace survives in active structural authority. New QSMv2 adjudication introduces no novel `infer_*` placeholder IDs. Exact reuse of a registered `FROZEN_QRA236_COORDINATE` is permitted under higher-authority precedent; the 52 `FROZEN_ACCEPTED_GSS` rows themselves remain unchanged.
- Canonical facet-parent law is enforced except the explicitly frozen `civil_liberties_target_tolerance` exception.

Final hostile QA: **PASS** (4886 checks; 0 failures).
