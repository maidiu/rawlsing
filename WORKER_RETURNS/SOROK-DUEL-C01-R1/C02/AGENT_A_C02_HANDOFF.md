# SOROK C02 AGENT A — constructive handoff

**Packet:** C02, `Independent mother antecedent and continuing materially conditioned activity`, CG-C.
**Status:** current-clock lawful portion constructed; **B02 calendar/period prerequisite explicitly HELD**. C02 is not complete.
**Grade:** `SOURCEFREE_S2_ONLY`.
**Branch:** `codex/sorok-duel-c01-a-relay-c02-20261112-r1`.
**Implementation SHA:** `ace64f7794a4dd9324bc67768835083b452c49b2`.
**Composition start:** `5932a509095f92f2d2b463b0899b27ac851741f6`.
**B frozen return:** `0fd303e2af23d71b51b068393cfaa6f62d40fe38`; B implementation `0e526f043027e4256b353d42240e80d85ad39265`.
**Contract SHA:** `08a323b490df4e2ddd0dca7f8b3cd394dfe17e0a`.
**Protected baseline:** `6a5c12f04323d74001f9632063ec907f4fc4468e`.

## 1. Exact artifact

New product code:

| Path | Change |
|---|---|
| `WORKER_RETURNS/SOROK-DEVELOPMENTAL-RECURSION-ENGINE-R1/developmental_recursion/parent_activity.py` | Parent-local material antecedent, circumstance change, actual parent-authored current-clock activity, self-only feasible-options/material/activity/history readers. |

Tests/evidence:

| Path | Result |
|---|---|
| `WORKER_RETURNS/SOROK-DUEL-C01-R1/C02/test_c02_parent_activity.py` | 4 passed in 10.50 s |
| `WORKER_RETURNS/SOROK-DUEL-C01-R1/C02/evidence/c02_parent_activity.log` | C02 packet |
| `WORKER_RETURNS/SOROK-DUEL-C01-R1/C02/evidence/b_c01_moved_regression.log` | B C01 moved: 8 passed |
| `WORKER_RETURNS/SOROK-DUEL-C01-R1/C02/evidence/a_c01_p2_p3_regression.log` | A C01 + P2 owner + P3 owner: 20 passed, 1 skipped |
| `WORKER_RETURNS/SOROK-DUEL-C01-R1/C02/evidence/b01_current_cut.log` | B01 current cut: 7 passed |
| `WORKER_RETURNS/SOROK-DUEL-C01-R1/C02/evidence/b03_current_cut.log` | B03 current cut: 8 passed |

No edit was made to Pair1 `house.py`, Pair1 module-level P2 material functions/`material_fact`, P3, `model_cycle`, or Pair2 files.

## 2. Governing contract

C02 requires an independently changing parent antecedent and materially conditioned continuing activity before a child request; the terminal consumer is the parent's own later choice. Positive: change employment/debt/care before the request and independently change feasible alternatives. Negative: future-tailored parent or private state copied into Nadia. Restoration: two chronological parent periods reopen; source severance changes private choice, not past fact. Dependencies: C01, B02, B03. PW-05/06. Grade `SOURCEFREE_S2_ONLY`.

Governing sources read: frozen programme `01`–`05`, the 20261111 rolling person–world requirement, owner reconciliation `32`, B01 A handoff/ABI at `edbb4b344`, B C01 handoff/ABI at `0fd303e2`, and the actual current P2/C12/S47/S45/B01/B03 code. The two full Library architecture records remain **NOT_INSPECTED locally**; no contents are claimed.

## 3. Strongest achieved result

A registered parent now has source-qualified actor-local material state in the actual P2 world:

```text
world.actor_state[parent_alias]["material"] = {
    schema, grade, actor_id, source_ref,
    employment_status, wage_units_per_hour, debt_units,
    care_hours_due, cash_units, free_hours,
    root, branch, epoch, source
}
```

Writers:

- `establish_parent_material` records a C12 `P2_PARENT_MATERIAL_ANTECEDENT` episode + material state + P2 checkpoint. Exact recovery after world-material severance; later-history recovery refuses stale.
- `commit_parent_circumstances` changes employment/wage/debt/care/free-hours antecedent fields with a required `source_ref`, `event_effect=NONE`, no cash creation. Cash is refused (`PARENT_CASH_REQUIRES_ACTIVITY`).
- `record_parent_activity` admits `PAID_WORK`, `CARE_DEPENDENT`, `PAY_DEBT` only when actual material conditions allow. It atomically writes an actual parent-authored P2 world event (parent alias, owner receipt, current clock/position), a parent `own_action` C12 perception, a `P2_PARENT_ACTIVITY` C12 episode and the updated material state. It does **not** record a focal/Nadia perception.

Reads (self-only):

- `read_parent_material` — material source/binding and fields.
- `parent_feasible_actions` — PAID_WORK/CARE_DEPENDENT/PAY_DEBT ADMISSIBLE/REFUSED reasons and prospective after-state.
- `read_parent_activity` — public projected actual event + receipt.
- `read_parent_history` — ordered C12 antecedent/activity/circumstance rows.

Demonstrated:

- Baseline employed parent with debt=4, care=2, cash=20, free_hours=8 has all three options ADMISSIBLE.
- `PAY_DEBT` payment=4 changes debt to 0; PAY_DEBT then refuses `NO_DEBT`.
- `CARE_DEPENDENT` hours=2 changes care to 0; CARE then refuses `NO_CARE_OBLIGATION`.
- `PAID_WORK` hours=6 consumes free hours; PAID_WORK then refuses `NO_FREE_HOURS`.
- `commit_parent_circumstances` job loss changes PAID_WORK to `EMPLOYMENT_NOT_AVAILABLE`.
- Parent activity events are authored by the parent alias, not Nadia; focal access is `NOT_PERCEIVED`; the private motive is absent from material/activity/history reads and event/body.
- Replay by operation ID returns `REPLAY` with unchanged counts; later-state replay refuses `REPLAY_STALE`; cold reopen and a fresh Python subprocess read the same material/options/history.
- Fresh final-cut P6/B01/B03 composition: household and dwelling sources remain unchanged after a parent activity; B03 material feasibility still runs.

## 4. Own hostile findings

1. **My first C02 option evaluator crashed on zero debt/care.** A refused option must still be returnable. I split zero-obligation options into explicit refused rows and re-ran.
2. **My first antecedent recovery appended a duplicate episode after material severance.** I made establishment recover from the exact antecedent episode and refuse `PARENT_MATERIAL_RECOVERY_STALE` when later parent history exists.
3. **An antecedent change could originally conjure cash.** I removed `cash_units` from circumstance changes and added `PARENT_CASH_REQUIRES_ACTIVITY`; cash changes only through admitted work/debt activity.
4. **Parent activity must not become a Nadia percept.** The writer records only the parent `own_action` perception; focal access is `NOT_PERCEIVED`.
5. **A naked material dict is not enough.** Part 1 requires a schema/source/binding and C12 episode; performed activity is an actual world event with owner receipt, not a stored dict.
6. **I did not fake B02.** Every read/receipt carries `period_qualification=HELD_B02_CALENDAR_ABSENT`; no dates or years are fabricated.

## 5. Unresolved challenges

- **B02 is still absent.** No calendar/as-of, dated period, split period or two-dated-period replay. C02 is partial and must not be marked complete.
- **No parent decision/utterance/uptake.** C03 and C04 remain future. `parent_feasible_actions` is an input, not a choice.
- **No relation/dyad or variable supporting roles.** C05 remains future.
- **No fork/copy of parent registration/material/activity.** C01 origin-branch refusal remains.
- **No structured private-state confidentiality proof.** Private motive remains C12-developer-visible; C02 material state is objective actor-local material.
- **`OFFSCREEN_REPAIR` is a carrier kind**, not a repair claim.
- **No full-estate run.** P3 full vertical suite timeout remains inherited.
- **Controller/provider cost unknown.**

## 6. Likely attack surfaces for SAME B

- Integrate exact B02 calendar/period and make two dated parent periods reopen without retconning past material facts; this is the real C02 completion.
- Replace `commit_parent_circumstances` with a stronger source-qualified antecedent-event writer if arbitrary debt/care changes are judged too loose; preserve cash conservation and idempotence.
- Make C03 consume `parent_feasible_actions` and produce an actual parent decision/utterance with hidden reason separate from outward speech and Nadia-uptake; no second owner/scheduler.
- Attack `record_parent_activity` carrier semantics, clock/position, parent-only perception, and replay-after-later-state.
- Attack the event/body and self-only reads for private material leakage into a child/user projection.
- Test parent material/activity on a real P6/B01/B03 composition and then a fork; keep branch provenance precise.
- Test whether P3 source closure needs `parent_activity.py`; do not silently weaken pins.

**Hardest concrete challenge for SAME B:** use this parent material/activity boundary to implement the C03 parent decision and performed utterance before any Nadia request, then prove with actual consumers that changed employment/debt/care independently changes the admitted parent decision/utterance while Nadia receives only qualified speech and never the parent's private material/motive state. A C02-only reader improvement will not surpass this.

## 7. Rejected alternatives

- **Set cash in an antecedent change.** Rejected: conjures resources without activity. Cash changes only via PAID_WORK/PAY_DEBT.
- **Store parent material in a new resource slot/ledger.** Rejected: existing P2 world actor state is the actor-local owner; no second ledger.
- **Use a new scheduler/actor owner.** Rejected: C01 supporting identity + P2 world/C12 suffice.
- **Fabricate B02 dates to satisfy the packet.** Rejected: explicit hold; no fake years.
- **Treat parent activity as a Nadia percept.** Rejected: only parent own_action receipt; C04 owns qualified uptake.
- **Use LLM prose as parent activity.** Rejected: actual state/event/C12 writer only.
- **Let `OFFSCREEN_REPAIR` semantics imply a repair.** Rejected: carrier-kind limitation disclosed.
- **Edit `house.py`/P2 material functions or P3 to integrate.** Rejected: outside C02 lease; precise dependencies recorded.

## 8. Proof boundaries

- `SOURCEFREE_S2_ONLY`; no native C4/ADP-015, CAN/ADP/Pyat, actor/human/right, or protected merge.
- C02 full packet incomplete due B02 hold; no dated period/two-period claim.
- No parent decision, utterance, child request, Nadia uptake, relation, J1/J2.
- No automatic elapsed-time effect, trait, memory, motive or private-state transfer.
- No fork/cold parent lineage claim.
- Raw C12/world developer access is not a confidentiality proof.
- P3 source closure for `parent_activity.py` is not established; P3 owner must decide.
- Full estate not run.
