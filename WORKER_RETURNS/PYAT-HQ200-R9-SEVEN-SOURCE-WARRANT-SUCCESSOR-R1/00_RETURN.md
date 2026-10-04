# HQ200-R1 Return — seven-source unsigned warrant/accounting successor

**Disposition:** `SEVEN_SOURCE_WARRANT_SUCCESSOR_READY__RUNTIME_ACCEPTANCE_AND_SOURCE_DEPENDENT_VALUES_PENDING`
**Branch:** `agent/rabochii-pyat-hq200-r2`
**Startup SHA (verified exact):** `e15d3647fbc1e149786a3f33e660ac2e16e0f78f`
**Base technical-value successor:** `ea51c409462b3bfe0a88a4b7e7326e117b76877e`
**Checkout mode:** `SPARSE_REQUIRED` — sufficient. No clone, no full checkout.

Documentary binding only. Nothing issued, no locators filled, no invented numbers. **R9 is not closed.**

---

## The seven plans, as carried

| source | row_data_mode | encoding | selected_reads | full_reads | header prefix | route pass |
|---|---|---|---|---|---|---|
| SRC02 | SELECTED Q10B@58 | null | **1 exact** | **0** | none | 0 |
| SRC06 | SELECTED Q101@20, Q2061B@19 | null | **1 exact** | **0** | none | 0 |
| SRC08 | METADATA_ONLY | BIG5 | 0 | 0 | none | 0 |
| SRC12 | METADATA_ONLY | WINDOWS-1252 | 0 | 0 | none | 0 |
| SRC14 | SELECTED v372@466 | null | **1 exact** | **0** | none | 0 |
| SRC26 | METADATA_ONLY + prefix | null | 0 | 0 | **176 bytes exact** | 0 |
| SRC27 | FULL | latin1 | *UNBOUND* | **FLOOR 1** | none | **1 / max 1** |

`retries = 0` for all seven. Every account carries **expected / floor / maximum / observed** as four distinct
fields, and every numeric/policy field carries an authority status.

| classification | fields |
|---|---|
| `FROZEN_AUTHORITY` | 157 |
| `IMPLEMENTATION_POLICY` | 29 |
| `PENDING_TECHNICAL_ACCEPTANCE` | 66 |
| `UNBOUND_SOURCE_DEPENDENT` | 21 |
| *of which candidate maxima pending runtime acceptance* | *29* |

---

## SRC27: all three corrections encoded

| forbidden encoding | what the instrument actually carries |
|---|---|
| `path_opens >= 2` | `expected` **null / PENDING**; the only number is a candidate **MAXIMUM 1**, typed `PENDING_HQ200_RUNTIME_ACCEPTANCE` |
| `full_reads` EXACT 1 | `expected` **null / PENDING**; **floor 1 `FROZEN_AUTHORITY`**; candidate maximum 1 |
| `decoder_invocations` EXACT 1 | `expected` **null / PENDING**; candidate maximum 1 |

`selected_reads` stays **null/PENDING** — mapping SRC27 into a selected-read slot would be a fabrication.

And a new **outer account** was added, structurally separate:

```
governed_full_route_passes   expected 1 / floor 1 / maximum 1   FROZEN_AUTHORITY   is_outer_account = true
```

with a non-substitution law forbidding the route-pass count from ever becoming the value of
`decoder_invocations`, `full_reads`, `chunk_reads`, `reader_invocations` or `path_level_opens`. The other six
sources carry it as **EXACT 0**, since no full-route pass is admitted for their operation classes.

## Policy ceilings are quarantined

All **29** candidate maxima sit in **MAXIMUM** fields only, typed `IMPLEMENTATION_POLICY` or
`PENDING_HQ200_RUNTIME_ACCEPTANCE` — never `FROZEN_AUTHORITY`. This is enforced mechanically by
**H-08-NO-POLICY-IN-EXPECTED**, which scans every `expected` field across all seven plans and found zero
offenders.

## Byte accounts

`UNBOUND_SOURCE_DEPENDENT__MUST_BE_BOUND_BEFORE_LAUNCH` on all seven. Measurability and budget-availability are
recorded as **two separate booleans**; no synthetic total appears; no derivation rule exists in frozen authority,
so the requirement is preserved as issuance-blocking rather than filled. **H-11-BYTES-TOKEN-ONLY** verifies that
no byte field anywhere carries a number.

---

## One runtime gap this lane found

**The frozen SRC27 route-pass ceiling has no owner in code.** At the session candidate
(`90ccbd54`), `full_route_passes` has **zero occurrences** — the plan carries only an `outer_account_token`. So a
frozen `expected 1 / max 1` constraint is currently **unenforceable**, which means **TAC-05 cannot be satisfied by
the present candidate**.

This is a gap in the *runtime*, not in the instrument, so I carried it as a technical acceptance dependency rather
than as an instrument defect — but it should be built first among the runtime items, because it is frozen yet
unowned.

---

## Verification: 20 invariants, 20 passing

Including `H-05-SRC27-NO-2-OPENS` (no numeric field implies ≥2), `H-06/H-07` (SRC27 `full_reads` and
`decoder_invocations` not encoded as EXACT 1), `H-10-OUTER-PASS-SEPARATE`, `H-12-NO-INVENTED-DTA-PREFIX`
(no 512 invented), `H-13-176-ONLY-SRC26`, `H-14-PRQ-07-NOT-OPEN`, `H-15-R9-NOT-CLOSED`, and
`H-18-SRC08-12-HARD-ZEROS`.

**PRQ-07** is recorded in `discharged_and_must_not_reappear` and is **absent** from `open_blockers` — alongside
`R9-SEL-PHYSICAL-SEMANTICS-003`, `R9-SEL-03` and the three broker items.

## One judgement call

I rejected `SOURCE_DEPENDENT_VALUES_PREVENT_SOURCE_FREE_COMPLETION`, which is *true* of the byte ceilings. But
characterising the whole instrument as source-free-incomplete would misdescribe it: the byte requirement is one
accounted family among many, and it is fully and correctly typed. The selected disposition names the pendency
precisely instead. I also rejected `WARRANT_SUCCESSOR_PARTIAL__SPECIFIC_STRUCTURE_GAP`, since the instrument has
no structural gap — the one real gap is in the runtime.

## Status

`signed=false`, `issued=false`, `authorizes_access=false`, `execution_authorized=false`. Both approvals `UNSET`.
All seven locator placeholders unfilled. No locator search, no source access, no production mutation.

**Nine open issuance blockers**, including all TAC-01..TAC-07 dependencies, the byte ceilings, and the SRC27
route-pass owner.

## Artifacts

`00_RETURN.md` · `01_SEVEN_SOURCE_PLAN_BINDING.json` · `02_AUTHORITY_POLICY_OBSERVED_MATRIX.json` ·
`03_SRC27_OUTER_AND_LOWER_ACCOUNTING.json` · `04_TECHNICAL_ACCEPTANCE_DEPENDENCIES.json` ·
`05_ISSUANCE_BLOCKER_MATRIX.json` · `06_UNSIGNED_SEVEN_SOURCE_WARRANT_SUCCESSOR.json` · `07_FINAL_DISPOSITION.json`

## Recommended next step for HQ

Independent acceptance review of the session candidate is the gating item — all 29 candidate maxima and six of the
seven TAC dependencies depend on it. Build **TAC-05** first among the runtime items, since the SRC27 route-pass
ceiling is frozen yet unowned. The byte ceilings need a governing numeric rule or an exact later derivation rule;
they cannot be resolved by measurement.

`HQ200_R9_SEVEN_SOURCE_WARRANT_SUCCESSOR_RETURNED__HQ_REVIEW_REQUIRED`
