# G04 FIXTURE SPEC — FULL ORIGINARY FRACTURE-MAP HOSTILE ORACLE R1

Authority: `35_ORIGINARY_EMPIRICAL_FRACTURE_MAP_CONSERVATION_AND_10_LANE_COURT_AUTHORITY.md`

This fixture is an experiment-only semantic oracle. It does not import or adapt to production I05 behavior.

## Frozen population

- 52 deterministic respondent rows.
- 48 substantive `TARGET_MULTISELECT` responses.
- Four separate nonresponse/authority states: `MISSING`, `REFUSED`, `NOT_APPLICABLE`, `UNKNOWN`.
- Exact CSV SHA-256: `83c496c9482c2e9736a6797e243965110899c1aa97436d752795b15d483a8215`.
- Canonical logical digest: `e4ef71ccf3815b0734013a5ebf1c85f9f3ac94720b30f2c5cf6285aa784a0017`.
- Exact raw stop threshold: `minimum_raw_support = 3`.
- Integer fixture weight: 2 when the numeric respondent id is divisible by four; otherwise 1.

Replay identity is `FRACTUREMAP-R1:<respondent_id>`; all 52 are unique.

## Target response morphology

The target is multi-label. Exact pattern counts across the 48 substantive rows:

- `A+B = 24` — modal response M.
- `A_ONLY = 14`.
- `B_ONLY = 6`.
- `NONE = 4` — a substantive residual/category-failure pattern, not missing/refused/not-applicable.

Presence marginals are `A_present=38`, `B_present=30`. Those marginals are insufficient: `A+B=22, A_ONLY=16, B_ONLY=8, NONE=2` has the same two presence marginals but a different morphology.

## Positional fracture

`P` is the primary positional determinant.

- P=1: 28 rows, 20 modal A+B.
- P=0: 20 rows, 4 modal A+B.
- Raw modal-rate contrast: `20/28 - 4/20 = 18/35`.

Required four-way fracture:

1. P+M conformers: 20.
2. P+not-M deviants: 8.
3. not-P+M alternative-route convergers: 4.
4. not-P+not-M minority/alternative branch: 16.

## Secondary determinants and recursion

`Q` is evaluated inside the discovered P+not-M branch:

- Q=1: 6, all A_ONLY.
- Q=0: 2, all NONE; typed underpowered for further recursion.

The Q=1 child is itself a discovered parent. `S` then fractures it:

- S=1: 4, all `FOLLOWUP=F_HIGH` — supported depth>1 child.
- S=0: 2, all `FOLLOWUP=F_LOW` — underpowered stop.

`R` is evaluated inside not-P:

- R=1: 6 rows, 4 modal A+B.
- R=0: 14 rows, 0 modal A+B.

Thus R supplies a distinct alternative route to the same modal outcome.

## Same-respondent branch co-signature

Questions `C1` and `C2` are globally reversed but perfectly positive inside the discovered Q=1 deviant branch.

Global 48-row table: `00=3, 01=21, 10=21, 11=3`, phi = `-0.75`.

Conditioned P+not-M -> Q=1 table: `00=3, 01=0, 10=0, 11=3`, phi = `+1.0`.

A global association summary therefore gives the wrong topology for the branch.

## Higher-order failure fixture

Across all 48 substantive rows:

`XOR_C = XOR_A XOR XOR_B`.

Only triple cells `000,011,101,110` occur, each 12 times. Every pairwise 2x2 table is exactly uniform `12/12/12/12`, so every pairwise phi is zero. The K-way structure is exact and invisible to naive pairwise analysis.

## Minority, stops, residual

- Stable supported minority: `P=0 AND B_ONLY`, n=6.
- Underpowered branch: that minority with `U=1`, n=2; must stop.
- Valid-empty branch: `P=1 AND B_ONLY`, n=0; must remain valid-empty.
- Residual/category-failure: `NONE`, n=4 and weighted n=6; it remains distinct from nonresponse states.

## Perturbation

The only permitted perturbation changes `SYN-R035.R` from 0 to 1.

Before: P0/R1 = 6 rows with 4 modal; P0/R0 = 14 rows with 0 modal.

After: P0/R1 = 7 rows with 4 modal; P0/R0 = 13 rows with 0 modal.

No response value, P/Q/S branch, co-signature, XOR structure, or replay identity changes. The only lawful topology change is R-dependent membership/metrics.
