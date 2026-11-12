# C02 current-clock parent antecedent and independent activity ABI

**Status:** sourcefree `SOURCEFREE_S2_ONLY`; partial C02 construction. B02 dated calendar/history qualification is **HELD**.
**Task:** C02, `Independent mother antecedent and continuing materially conditioned activity`, CG-C.
**Implementation SHA:** `ace64f7794a4dd9324bc67768835083b452c49b2`.
**Composition start:** `5932a509095f92f2d2b463b0899b27ac851741f6` (C01 B + Pair1 A B01-counter/B03 at `5bc29474e769b928d9264f1607bab605e2b1c7e9`).
**B frozen return:** `0fd303e2af23d71b51b068393cfaa6f62d40fe38`; B implementation `0e526f043027e4256b353d42240e80d85ad39265`.
**Running contract SHA:** `08a323b490df4e2ddd0dca7f8b3cd394dfe17e0a`.
**Protected inspection baseline:** `6a5c12f04323d74001f9632063ec907f4fc4468e`.

## Actor-local material state

The parent is the stable supporting actor registered by C01. Its material state lives in the existing P2 world actor state, not in a separate owner/database/ledger:

```text
world.actor_state[parent_alias]["material"] = {
    schema, grade, actor_id, source_ref,
    employment_status: employed|unemployed|UNKNOWN,
    wage_units_per_hour, debt_units, care_hours_due, cash_units, free_hours,
    root, branch, epoch, source
}
```

`source` is the content address excluding root/branch/epoch/source. The state is bound to the actual root/branch/clock and the registered parent stable ID. Private motive state remains in the C01 C12 registration episode; it is not copied into this material document.

## Writers

```text
establish_parent_material(session, parent_id, *, fixture) -> PARENT_MATERIAL_READ
commit_parent_circumstances(session, parent_id, *, operation_id,
                            changes, source_ref, expected_clock=None)
record_parent_activity(session, parent_id, *, operation_id, activity,
                       hours=None, payment=None, expected_clock=None)
```

### Antecedent establishment

`establish_parent_material` accepts a bounded, source-qualified fixture (`parent_material_fixture`) and writes:

- one C12 `P2_PARENT_MATERIAL_ANTECEDENT` episode (source, source_ref, identity, material snapshot);
- the world actor-state material document;
- one P2 checkpoint.

It is one-shot for a different material source (`PARENT_MATERIAL_ALREADY_ESTABLISHED`), idempotent for the same document (`UNCHANGED`), and can recover an exactly matching antecedent episode after world material severance (`RECOVERED`). Recovery refuses `PARENT_MATERIAL_RECOVERY_STALE` if any later parent material/activity/circumstance episode exists, so a later material fact is not silently rolled back.

### Antecedent material change

`commit_parent_circumstances` is explicitly **not an enacted event**. It changes only antecedent material fields:

```text
employment_status, wage_units_per_hour, debt_units, care_hours_due, free_hours
```

`cash_units` is refused with `PARENT_CASH_REQUIRES_ACTIVITY`: cash can change only through an admitted parent activity. Every change requires an operation ID and a nonempty `source_ref`; it is recorded as a C12 `P2_PARENT_CIRCUMSTANCE` episode with before/after material sources and has `event_effect=NONE`, `operation_kind=ANTECEDENT_MATERIAL_CHANGE`. It is idempotent by operation ID and refuses stale replay after a later change.

### Performed parent activity

`record_parent_activity` admits one bounded parent-authored material activity:

```text
PAID_WORK      employed + wage>0 + free_hours>=hours -> cash += wage*hours, free_hours -= hours
CARE_DEPENDENT care_hours_due>=hours + free_hours>=hours -> care_hours_due -= hours, free_hours -= hours
PAY_DEBT       debt_units>=payment + cash_units>=payment -> debt_units -= payment, cash_units -= payment
```

Every pre-write condition is checked before mutation. On admission the writer atomically:

1. creates an actual world event with `actor_id=parent_alias`, an owner receipt, current world clock and parent position, carried by the existing `OFFSCREEN_REPAIR` ordinary-material event kind;
2. records the parent's own C12 `own_action` perception (no focal/Nadia perception);
3. appends a C12 `P2_PARENT_ACTIVITY` episode with operation ID, parameters, before/after material sources, event ref/hash and public receipt;
4. updates the parent material document;
5. checkpoints the P2 world.

The event body carries activity, parameters, parent identity, before/after material content addresses, activity source, B02 hold and `visibility=PARENT_ORDINARY_ACTIVITY`. It never carries the parent's private registration state.

A repeated operation ID returns the stored receipt (`REPLAY`) without writing; a different request under the same ID refuses `PARENT_OPERATION_REUSE_MISMATCH`; replay after a later material state refuses `PARENT_ACTIVITY_REPLAY_STALE`.

## Readers

```text
read_parent_material(session, parent_id, *, as_actor)
parent_feasible_actions(session, parent_id, *, as_actor)
read_parent_activity(session, parent_id, operation_id, *, as_actor)
read_parent_history(session, parent_id, *, as_actor)
```

All four are **self-only** (`PARENT_SELF_READ_REQUIRED` for any other actor ID). They return no private motive state, no Nadia state and no child-request evaluation.

`parent_feasible_actions` returns the three current-clock options with `ADMISSIBLE`/`REFUSED` status, reasons and prospective after-material state. This is the C02 first consumer and the input for a later parent decision; it is not a decision, utterance or action.

`read_parent_activity` returns the public projected event and stored receipt. `read_parent_history` returns ordered C12 antecedent/activity/circumstance rows with operation IDs, source refs, before/after sources and event refs.

All reads carry:

```text
period_qualification = HELD_B02_CALENDAR_ABSENT
historical_dates = NOT_AVAILABLE
child_request = NOT_EVALUATED
nadia_state = NOT_READ
```

## Explicit limits

- **B02 is held.** No dated year/period, calendar conversion, historical as-of or multi-year duration is implemented or claimed. The C02 packet is not fully closed.
- C03 parent decision/action/utterance, C04 hidden-reason/utterance/Nadia-qualified uptake, C05 relations and J1/J2 are not implemented.
- The `OFFSCREEN_REPAIR` event kind is reused as the existing ordinary-material carrier; it is not a claim that the parent performed a repair.
- Parent activity is not automatically perceived by Nadia; C04 owns qualified uptake. A future reader must not treat the objective event as a Nadia percept.
- Fork/copy of parent material/activity is not made lawful here; C01's origin-branch-bound registration refusal remains.
- `parent_activity.py` is a new actor-local module. P3 currently pins only `contracts.py` and `p2_owner.py`; if P3 integration is to include this module in source closure, the P3 owner must add that pin deliberately. This return does not edit or weaken P3.
- No native actor science, C4/ADP-015 issuance, rights, human validation or protected merge.
