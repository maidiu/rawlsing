# SUB-VOZHD D — OBL009 J01-B WVS + EVS HISTORICAL SUCCESSION R1 — RETURN

Status:

`PASS__SUBV_D_OBL009_J01B_WVS_EVS_SUCCESSION_CURRENT_GRAIN_R1`

Worker branch:

`agent/rabochii-subv-d-obl009-j01b-wvs-evs-succession-r1`

Exact worker starting HEAD:

`ea6ab0368326041f8ad267cfca74b834619d41cb`

This return is lane-local succession classification only. It does not alter the frozen J01-A denominator, close global J01-B, grant project-current authority, or consume any sibling J01-B lane result.

## 1. Exact material gate

The frozen J01-A current-candidate carrier was materially recovered and verified:

- Library: `libfile_3f6b0d93bb74819195702d808e3093ec`
- global rows: **1,411**
- bytes: **1,641,446**
- SHA-256: `b21a79947f19f4c520ea493480a38ef8b23cb6797444eeb913bc8575b6cafb64`

Mechanical family filtering yields exactly:

- WVS: **109** current candidates
- EVS: **130** current candidates
- lane total: **239**

The admitted C07 historical carrier was materially recovered and verified from `277d1a88e720ab5b5dbedf3daf41821656435b3f`:

- archive SHA-256: `1687b4fea789aabf90e3906f104250f4d7bfa0055586a71066598fd9541f0286`
- exact normalized registry: **2,499** rows, SHA-256 `d75d6e30373d1fd45d29ffb34fc14d135c6addf0bbb7aa64d7aed57cf45cd8dd`
- exact memberships: **15,990** rows, SHA-256 `52f10099ce98f9fe9bcf161b80d50b05dfd2f584bb78c3bed007d5055f38980c`

Mechanical WVS/EVS filtering yields:

- WVS: **115** historical structures / **697** memberships
- EVS: **182** historical structures / **1,237** memberships
- lane total: **297** historical structures / **1,934** memberships

C08 `f24a90be78e11c0a234fdc4a14cbafe60390c1f8` independently corroborates those exact WVS/EVS serialized partitions and binds their Git blobs. No historical row was generated from a count.

## 2. Current succession disposition

Exactly one succession state is emitted for every one of the 239 frozen current candidates.

Aggregate state counts:

- `EXACT_CURRENT_SUCCESSOR`: **71**
- `CURRENT_SUCCESSOR_CHANGED_SCOPE`: **6**
- `CURRENT_SUCCESSOR_CHANGED_MEMBERSHIP`: **32**
- `CURRENT_SUCCESSOR_CHANGED_MEMBERSHIP_AND_SCOPE`: **1**
- `CURRENT_NEW_STRUCTURE`: **61**
- `AMBIGUOUS_SUCCESSION`: **2**
- `UNRESOLVED_IDENTITY`: **66**

WVS:

- exact: **17**
- changed scope: **6**
- current new: **34**
- ambiguous: **2**
- unresolved: **50**

EVS:

- exact: **54**
- changed membership: **32**
- changed membership + scope: **1**
- current new: **27**
- unresolved: **16**

No WVS/EVS current candidate was added, deleted, merged, split, or rebound.

## 3. WVS terminal ceilings preserved

Historical membership was not allowed to repair current J01-A gaps.

All **27 WVS W1** candidates remain `UNRESOLVED_IDENTITY` because their frozen current status is:

`SAFE_NATIVE_TO_CURRENT_MEMBER_CROSSWALK_UNAVAILABLE__POSITIVE_V111_NUMBERING_CONFLICT`

The W4 `V68-V77 undesirable neighbors` candidate remains nonbinding at the V77 slot. History corroborates a split-slot structure containing `V68-V76` plus `V77_01..V77_27`, but that evidence cannot lawfully collapse the current country/form split into a single V77 identity. Its succession state is therefore `AMBIGUOUS_SUCCESSION`, and the frozen current gap remains untouched:

`V77_COUNTRY_FORM_SUBSTITUTION_SLOT__CURRENT_CATALOG_SPLITS_V77_01_TO_V77_27_WITHOUT_SAFE_COUNTRY_FORM_COLLAPSE`

All **4 WVS W7** Middle East regional-module structures whose current native MN codes are absent from the governed current catalog remain `UNRESOLVED_IDENTITY`.

Across WVS, all **32** current typed member-binding gaps remain nonbinding: 31 unresolved and the V77 case ambiguous.

## 4. Identity law actually used

Exact succession requires the same source family and wave plus an exact native-member set and exact current question-implementation set. Where more than one historical structure carries the same exact fingerprint, the row is typed ambiguous rather than guessed.

Changed-membership succession is promoted only where admitted history supplies structure identity beyond raw overlap: exact family/wave, exact member/QID relation, and source-parent label corroboration. One important lawful many-to-one pattern is preserved in EVS: where two disjoint historical child structures exactly partition one current parent structure's complete native-member and current-QID sets, both historical IDs are retained as the predecessor relation rather than forcing a false 1:1 identity.

Mere same-label, variable-number, adjacency, same-file, count similarity, or member overlap without structure identity never promotes a relation.

## 5. Historical conservation

Of the **297** admitted WVS/EVS historical structures:

- **115** unique historical structures are referenced by at least one current succession relation;
- **182** are residual-disposed exactly once.

Residual states:

- `HISTORICAL_ONLY`: **139**
- `AMBIGUOUS_HISTORICAL_RESIDUAL`: **43**

Thus every admitted historical structure is conserved exactly once as matched capital or residual capital. None is used to create current candidacy.

## 6. Ambiguity and current-freeze review

`AMBIGUITIES.csv` types every current ambiguous/unresolved case and every materially signaled historical residual.

`CURRENT_FREEZE_REVIEW_REQUESTS.csv` contains **0** requests. The WVS W1/W4/W7 conditions are already frozen terminal current states, not newly discovered defects to be rewritten from history.

## 7. Validation

`VALIDATION.json` passes all required lane invariants, including:

- exact 239-row current lane denominator derived mechanically from the frozen J01-A carrier;
- every current candidate exactly once;
- no duplicate or out-of-lane current IDs;
- every historical structure matched or residual-disposed exactly once;
- admitted evidence restricted to C07 `277d1a88e720ab5b5dbedf3daf41821656435b3f` and C08 `f24a90be78e11c0a234fdc4a14cbafe60390c1f8`;
- no sibling J01-B result consumption;
- no count-to-identity inference;
- no historical mutation of current candidacy;
- full preservation of WVS W1, W4 V77, and W7 current-member ceilings.

Terminal:

`PASS__SUBV_D_OBL009_J01B_WVS_EVS_SUCCESSION_CURRENT_GRAIN_R1`

Lane PASS does not close global J01-B. A separate sibling-consuming global join/collision/completeness court remains required after all five family lanes return.
