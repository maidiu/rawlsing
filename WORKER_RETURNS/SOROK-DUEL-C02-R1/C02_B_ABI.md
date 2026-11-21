# C02 Agent B revised ABI — truthful, history-bound parent material activity

**Status:** sourcefree `SOURCEFREE_S2_ONLY`; partial C02 construction. **B02 calendar/as-of/period is `HELD_B02_CALENDAR_ABSENT`; C03/C04 are not implemented.**
**Task:** C02, `Independent mother antecedent and continuing materially conditioned activity`, CG-C.
**B implementation commit:** `3f9d1079bc3b1f09a318afc80bd5aa63d7ccdecf`.
**Parent / attacked A HEAD:** `ff9b6d85d32b1529ea32b5488f1fd8a623786d26` (A C02 implementation `ace64f7794a4dd9324bc67768835083b452c49b2`).
**B C01 received implementation:** `0e526f043027e4256b353d42240e80d85ad39265`; return `0fd303e2af23d71b51b068393cfaa6f62d40fe38`.
**Running contract SHA:** `08a323b490df4e2ddd0dca7f8b3cd394dfe17e0a`.
**Protected baseline:** `6a5c12f04323d74001f9632063ec907f4fc4468e`.

## Actor-local material ABI

The parent is the stable supporting actor registered by C01. Its material state is in the existing P2 world actor row, not a new owner/database/ledger:

```text
world.actor_state[parent_alias]["material"] = {
    schema: SOROK_P2_PARENT_MATERIAL@1,
    grade: SOURCEFREE_S2_ONLY,
    actor_id: <C01 stable parent id>,
    source_ref: <required sourcefree antecedent label>,
    employment_status: employed | unemployed | UNKNOWN,
    wage_units_per_hour: int >= 0,
    debt_units: int >= 0,
    care_hours_due: int >= 0,
    cash_units: int >= 0,
    free_hours: int >= 0,
    currency_unit: <parent-local currency label>,   # new in B
    root, branch, epoch,
    source: content address excluding root/branch/epoch/source,
}
```

`currency_unit` defaults to `parent_sourcefree_currency_unit`, deliberately distinct from B03 household/dwelling `sourcefree_currency_unit`. It cannot be changed by a circumstance write. `material_boundary` on every relevant read states:

```text
owner = PARENT_ACTOR_LOCAL_P2_STATE
household_cash = NOT_READ
household_stock_shared = False
household_spend_permission = C03_B04_HELD
double_counting = NO_HOUSEHOLD_EFFECT_APPLIED
parent_currency_unit = <parent unit>
household_currency_unit = NOT_READ
currency_conversion = NOT_APPLIED
```

No parent cash/debt/wage is silently treated as B01 actor-A household cash. C03/B04 must reconcile explicitly.

## Writers

```text
establish_parent_material(session, parent_id, *, fixture) -> PARENT_MATERIAL_READ
commit_parent_circumstances(session, parent_id, *, operation_id, changes,
                            source_ref, expected_clock=None) -> PARENT_CIRCUMSTANCE_RECEIPT
record_parent_activity(session, parent_id, *, operation_id, activity,
                       hours=None, payment=None, expected_clock=None)
                       -> PARENT_ACTIVITY_RECEIPT
```

All three acquire a per-state-root `parent_activity.lock` around their read/evaluate/write unit (a serialization lock, not a scheduler), then use the existing `_StoreWrite` C12 transaction.

### Antecedent establishment

`establish_parent_material` validates the fixture including `currency_unit`, writes one `P2_PARENT_MATERIAL_ANTECEDENT` episode, the material document and a checkpoint. It is idempotent for the same document (`UNCHANGED`), refuses a different established document, can recover an exact antecedent episode after material severance (`RECOVERED`), and refuses `PARENT_MATERIAL_RECOVERY_STALE` if later parent history exists.

### Antecedent change

`commit_parent_circumstances` changes only:

```text
employment_status, wage_units_per_hour, debt_units, care_hours_due, free_hours
```

`cash_units` refuses with `PARENT_CASH_REQUIRES_ACTIVITY`; `currency_unit` refuses with `PARENT_CIRCUMSTANCE_SCHEMA`. It is not an enacted event (`event_effect=NONE`, `operation_kind=ANTECEDENT_MATERIAL_CHANGE`), requires a nonempty `source_ref`, records a `P2_PARENT_CIRCUMSTANCE` episode with before/after material sources, is idempotent by operation ID, and refuses stale replay.

### Performed activity

PAID_WORK/CARE_DEPENDENT/PAY_DEBT are evaluated against the actual parent material before mutation. Zero-obligation defaults now produce `NO_CARE_OBLIGATION`/`NO_DEBT`; positive obligations with zero hours/payment produce `NO_CARE_HOURS`/`NO_PAYMENT`.

On admission the writer atomically:

1. creates an actual world event with `kind = MATERIAL_ACTIVITY` and `owner_receipt.act = MATERIAL_ACTIVITY`, current clock, parent position, truthful summary and body containing activity/parameters/currency/parent identity/before-after sources/activity source/B02 hold/visibility/`household_effect=NONE_PARENT_LOCAL_ONLY`;
2. records the parent's own C12 `own_action` perception (no focal/Nadia perception);
3. appends a `P2_PARENT_ACTIVITY` episode with operation ID, parameters, `source_ref`, sources, event ID/hash and receipt;
4. updates the parent material document;
5. checkpoints the P2 world.

Replay by operation ID returns `REPLAY` without writing; a different request under the same ID refuses `PARENT_OPERATION_REUSE_MISMATCH`; later-state replay refuses `PARENT_ACTIVITY_REPLAY_STALE`; duplicate operation episodes refuse.

**Event vocabulary:** B adds exactly one kind, `MATERIAL_ACTIVITY`, to the imported `bp4.world.make_event` allowlist. `bp4.c10._verify_world` validates its owner receipt. No physical/material action engine, time/scheduler semantics or other vocabulary was added. MI historical-source kinds, P5 `CHANNELS`, P6 scene and `bp4.product.other` public-work lists still do not accept/render `MATERIAL_ACTIVITY`; C02's parent event is not user/child-perceived, so those consumers must deliberately extend if exposure becomes lawful.

## Readers (self-only)

```text
read_parent_material(session, parent_id, *, as_actor)
parent_feasible_actions(session, parent_id, *, as_actor)
read_parent_activity(session, parent_id, operation_id, *, as_actor)
read_parent_history(session, parent_id, *, as_actor)
```

All require `as_actor == parent_id`; any other actor ID refuses `PARENT_SELF_READ_REQUIRED`. They return no private motive, no Nadia state and no child-request evaluation.

- `read_parent_material` requires the current material `source` to equal the latest ordered parent antecedent/activity/circumstance source; otherwise `PARENT_MATERIAL_HISTORY_MISMATCH`. This binds the read to C12 owner history rather than a detached self-hash.
- `parent_feasible_actions` returns PAID_WORK/CARE_DEPENDENT/PAY_DEBT options with ADMISSIBLE/REFUSED, reasons, prospective after-material, material boundary and B02 ingress hold. It is input, not a decision.
- `read_parent_activity` validates the event author, kind, activity/parameters/currency, before/after sources, household/period/visibility fields, owner receipt (act/actor/clock/perform) and the parent's `own_action` perception. It returns the public projected event and truthful receipt.
- `read_parent_history` returns ordered C12 rows, current material source, latest history source and `material_consistent`.

Every read carries:

```text
period_qualification = HELD_B02_CALENDAR_ABSENT
historical_dates = NOT_AVAILABLE
historical_ingress = {status: HELD_B02_CALENDAR_ABSENT, dates_claimed: false,
                      required: [B02_PERIOD_BOUNDARY, B02_AS_OF_CLOCK_MAPPING,
                                 SOURCE_PERIOD_REF, MATERIAL_SOURCE_BINDING]}
child_request = NOT_EVALUATED
nadia_state = NOT_READ
private_state = NOT_READ
```

## Explicit limits

- **B02 held.** No dated year/period, calendar conversion, historical as-of, split period or multi-year duration. B02 must supply a material source binding that participates in `_parent_material_history`; otherwise history-bound reads fail closed.
- **C03/C04 held.** No parent decision, utterance, child request, Nadia-qualified uptake, relationship or J1/J2. `parent_feasible_actions` is an input.
- **P4/P6 live turn not proved.** Actual P6 view after direct C01 registration/C02 activity refuses `P4_COLD_STATE_MISMATCH`; static B01/B03/P6 house-read composition is the proven boundary. P4/F01/J3 owners must define lawful ledger integration.
- **Fork/copy** of parent material/activity is not lawful; C01 origin-branch refusal remains. No verified-lineage fork reader was copied.
- **P3 source closure** does not include `parent_activity.py`; the P3 owner must deliberately add it if required. No P3 edit/weakening.
- **Self-read authorization** is caller-asserted; raw C12 developer access remains visible. Stronger confidentiality is a C04/C09/C12 trust decision.
- **Sourcefree antecedent** `source_ref` is a required label, not a verified external source artifact. No native history/science is claimed.
- **Concurrency** is serialized by `parent_activity.lock`; no multi-process stress/SIGKILL test was run.
- No HTTP/controller cost measurement; no native/actor/human/source/protected authority.
