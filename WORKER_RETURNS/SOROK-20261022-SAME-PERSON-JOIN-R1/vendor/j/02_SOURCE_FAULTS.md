# R31J source faults and restoration

Frozen assertion: `R31J_PREC9_SOURCE_TO_C12_A0_P01` (`r31j.assertion.p01`).

## Positive

- `gm01_pre_c9_source` is inside the C8 occurrence payload with B owner, B performed event, operation `SHARE_TOOL`, quantity 1, and GM01 readset.
- C8 digest is `545922…`, not the inherited `cd5a12…`.
- C9 target `59ff0a…` has E1 `630d97…` and BP1 parents.
- Product tools 1→0, completed 4→5, material 4→3, B 4, `OFFSCREEN_NO_CHANGE`, C12 verifier true.

## Faults

| Fault | Actual result |
|---|---|
| B share → B refusal | C8 digest `22bc08…`; E1 `739113…`; C9 `NO_CHANGE` / `NO_PROPOSAL`; `RESPONSE_EFFECTS_VALID_EMPTY` / `NO_ELIGIBLE_MATERIAL_SOURCE`; no target |
| A E2 → A omit | C8 digest `b33f57…`; target CREATE remains but A performs no material action; tools 1; completed 4; B 5; `OFFSCREEN_REPAIR` |
| Missing E1 | GM01 `HOLD_E1_NOT_ADMITTED_TEST_ONLY`; no product positive |
| Label-only role/class change | GM01 result identical; `psyche_delta={}`, `v3ms_created=0`, `rule_t_grant=None` |
| Forged/revoked GM01 source | `DENY_E2_NOT_LATER` / `DENY_REVOKED`; no product action |
| B refusal vs user request | B refusal remains B-owned; no automatic share is authored |

## Restoration

Share+E2 → refusal → share+E2: P01 true → false/no target → true. The restored product is a fresh root with the same source case and the same assertion.
