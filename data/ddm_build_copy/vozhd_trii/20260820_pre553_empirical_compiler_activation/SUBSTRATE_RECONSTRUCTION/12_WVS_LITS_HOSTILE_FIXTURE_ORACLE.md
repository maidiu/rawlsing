# PRE553 SUBSTRATE RECONSTRUCTION — WVS7 + LiTS I HOSTILE FIXTURE ORACLE

Status: `FROZEN_PARTIAL_ORACLE__AWAITING_SR03_FULL_NATIVE_COUNTS`

This oracle defines the first two source families that every decoder/carrier candidate must survive before the 35-source campaign may advance to implementation scale.

## 1. WVS Wave 7 SAV — known frozen evidence

Exact uploaded/source file SHA-256 established by HQ:

`2bd2a20fc565e7e7b4b2030fd8457db4d0d88160c5ee5186e9ea6c267209af7d`

Known physical/source facts already established:

- 97,220 cases;
- source header dated 31 May 2024;
- source declares SPSS user-missing states on Q152-Q157;
- source-native user-missing states were dropped from the historical generic response carrier;
- D_INTERVIEW is not injective: a Uruguay value occurs for 1,000 source rows;
- Q152/153, Q154/155, Q156/157 are distinct ordered slots;
- I_PSU contains source-declared missing/design states;
- W_WEIGHT and S018 are distinct source variables.

### WVS mandatory count equalities already proven

For each variable below, the count of source typed-missing states equals the count of absent legacy Postgres response rows discovered by PD01-PG01:

| variable | source typed-missing count |
|---|---:|
| Q152 | 2,557 |
| Q153 | 4,877 |
| Q154 | 1,802 |
| Q155 | 3,777 |
| Q156 | 1,745 |
| Q157 | 3,626 |
| I_PSU `-4` | 31,137 |

A compliant source decoder/C11 ingest must preserve these source rows as typed source incidence rather than erase them.

### WVS hostile requirements

1. All 97,220 source rows retain deterministic source-row identity.
2. D_INTERVIEW duplication cannot create respondent collision or reassignment.
3. Q152-Q157 positive values and all declared user-missing states remain tied to the correct row ordinal.
4. Q154 and Q155 remain distinct first/second rank slots; likewise Q152/153 and Q156/157.
5. Q223 country-local raw codes remain source-scoped and are never globally interpreted without country/source authority.
6. I_PSU physical missing/design state is retained and not converted to simple row absence.
7. W_WEIGHT and S018 remain separate raw candidates until weight authority binds them.
8. Exact same-respondent 5-way reconstruction remains possible for the Q177-Q181 battery.
9. Legacy positive-value parity is tested, but legacy row absence is not treated as negative source evidence.

## 2. LiTS I DTA — known frozen evidence

Known source facts established by HQ direct inspection:

- 29,002 cases;
- 1,198 variables;
- Stata format 113;
- 29 countries;
- native `id` populated and unique across the 29,002 inspected rows;
- three distinct candidate weight variables: `weight_0`, `weight_1`, `weight_2`;
- source uses ordinary labeled numeric values for many semantic absence states;
- source contains ordinary Stata system missing `.` cells;
- no Stata `.a`-`.z` extended-missing values were observed in the initial inspection.

Examples of ordinary observed codes whose semantic meaning comes from source labels rather than Stata missing machinery include:

- q301 family: `6 = not applicable`, `7 = don't know`;
- some education variables: `99 = don't know`;
- q201: `98 = don't know`;
- q204: `99 = refused`;
- occupation variables: `12 = don't know`, `98 = refused`;
- q707: `99 = refused`.

Initial HQ inspection found, across eleven q301 variables:

- 18,509 ordinary observed `not applicable` cells;
- 22,716 ordinary observed `don't know` cells.

SR03 must independently freeze the full physical counts before these become final certification oracle values.

### LiTS hostile requirements

1. All 29,002 rows retain source-row replay identity.
2. Native `id` is retained separately from source-row identity even if injectivity is confirmed.
3. Stata system missing `.` remains physically distinct from ordinary numeric values.
4. Ordinary codes such as q301 `6` and `7` remain `OBSERVED_STORAGE_VALUE` at decoder layer; semantic classification occurs only under LiTS source authority.
5. Value-label dictionaries survive extraction so those meanings remain recoverable.
6. `weight_0`, `weight_1`, `weight_2` remain separate raw source variables; no default weight is selected by decoder/carrier.
7. Absence of observed `.a`-`.z` in this source does not permit the DTA decoder to omit support for extended missings generally.

## 3. Cross-format invariants

The same C11 logical representation must be able to express both of these without claiming that their physical encoding is equivalent:

- WVS: semantic absence often encoded through SPSS user-missing declarations;
- LiTS: semantic absence often encoded as ordinary labeled numeric values while `.` represents physical system missing.

Therefore the following equivalence is prohibited:

`physical_missing == semantic_absence`

and the following normalized representation is insufficient:

`value OR NULL`

The required representation must retain both raw physical state and separately governed semantic interpretation.

## 4. SR03 completion amendments

When SR03 returns, HQ must amend this oracle only by adding mechanically established physical facts/counts for all 35 sources. Any change to the constitutional rules above requires an explicit contradiction finding, not merely new convenience.
