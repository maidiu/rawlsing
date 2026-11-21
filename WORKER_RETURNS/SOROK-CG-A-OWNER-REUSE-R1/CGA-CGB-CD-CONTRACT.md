# CGA-CGB-CD-CONTRACT — minimal future material/period/actor/root ABI

**Obligation:** `CGA-CGB-CD-CONTRACT`
**Result:** `PASS_CONTRACT__NO_NEW_SCHEDULER__CG_BCD_MULTI_ACTOR_MATERIAL_ADAPTER_BUILD_HOLD`
**Canonical detail:** `02_SELECTED_ABI_AND_CG_BCD_CONTRACT.md`
**Pinned P6 source:** `WORKER_RETURNS/SOROK-P6-ONE-LIVING-HOUSE-R1/house.py` at `2be0cf25`, blob `af556c14...`, SHA-256 `7d78d48d...` (exact for the declared `af556c14`).

## 1. Frozen choice

CG-B/C/D must share **one** writer/readset, not a new life engine:

```text
writer   = P3Owner -> P2Owner + PsycheStore
readset  = PsycheStore.query(project, counterpart, as_of)
           + P2Owner.snapshot()
           + house.read_house(session)
scheduler= BatchEngine + RecursionCycle (unchanged)
```

The current `P3Owner`/`PsycheStore` already enforce root/actor/branch/clock, source/registry/rule/version, exact event binding, effective-time query, immutable records, rollback, cold reopen, and exact replay. The current `house.py` already enforces the material root/branch/source/epoch/object-history readset. No parallel person/world ledger is required.

## 2. Exact current surface

```text
P3Owner(base_owner, *, source, history, plans, catalog=None,
        compression_specs=None, standpoints=None, mode="TEST_ONLY")

PsycheStore(path, *, binding={root, actor, branch}, registry_hash, source_hash)
PsycheStore.query(*, project, counterpart, as_of) -> list[record]
PsycheStore.reserve(operation_id, *, proposal_hash, expected, plan_hash,
                    base_before, psyche_before, plan) -> dict
PsycheStore.save_world(operation_id, base_result) -> dict
PsycheStore.commit_effects(operation_id, *, records, response, event_binding,
                           compression=None, projection=None) -> dict
PsycheStore.finish(operation_id, result) -> dict

house.establish(session) -> writes world.resources["p6_house"]
house.read_house(session) -> (world, house)
house.facts_for(history, objects, epoch) -> dict

situated.reconsider(session, receipt, interpret, realize=None, *,
                    actor_context=None, provider_mode="INJECTED") -> dict
situated.recent_speech(session) -> list[{event_id, clock, speaker, text}]
```

The P3 sidecar's later read is `P3Owner._effect` (`p3_owner.py:548-604`). The P6 situated later read is `situated.reconsider` (`situated.py:134-230`); it currently does not query `PsycheStore`.

## 3. Minimal extension points

### A. RootActorSet (multi-actor, same root)

- `participants(root)` reads the actual root roster.
- The proposal's `participants` must be a subset of that roster; the focal actor must be selected by the frozen plan, never by model prose.
- One `PsycheStore` per actor, same root/branch, `binding.actor` set to that actor.
- A composite snapshot binds the P2 state hash, each actor store head, the house hash and the home-period hash.
- This adapter is the only missing multi-actor piece. It must not change `BatchEngine`/`RecursionCycle` and must not silently turn the P2 fixed tuple into universal policy.

### B. HomePeriodResource (dated material home/period)

- World resource `home_period` with `{root, branch, source_hash, home_ref, from_clock, to_clock, actors, history_refs, hash}`.
- Writer: `establish_home_period(session, ...)` using the existing P6 checkpoint path.
- Reader: `read_home_period(session, as_of)` in the same owner; it must be included in the P2 `world` material hash.
- `from_clock`/`to_clock` are inputs, not automatic trait deltas. They do not authorize a change, memory, or native action by themselves.
- S46 interval state remains the actual interval source; the S46 span is not a historical calendar.

### C. MotherSpeech (independent speaker and qualified child access)

- A real `SPEAK` event with `speaker` and `recipient` in the root roster; the speaker must not be a counterpart-only string.
- Use the existing P6/P2 event/perception writer; the child's `read_qualified_speech` returns only perceived speech fields, never the mother's private ledger, objective history, or unadmitted prose.
- `situated.recent_speech` already demonstrates the recipient-filtered read pattern for actor A; generalize the speaker parameter rather than inventing a second speech store.

### D. SidecarDecisionReadset (later bridge)

- Before a situated decision, call `PsycheStore.query` and attach the exact record hashes, store head and `as_of` to the decision packet as a read-only readset.
- After a grounded decision, any durable actor record must go through `P3Owner.realize` so source/plan/rule/refusal and phase recovery still apply.
- No provider or model callback may write the store directly.

## 4. Why this is not a new scheduler

- `P3Owner` is a `DevelopmentOwner`; `BatchEngine` already sequences 3–5 events; `RecursionCycle` already owns the provider halves.
- The extension adds a root participant selector and material/speech resources around the existing writer.
- It does not add a second journal, a parallel clock, a habitus store, a new gate ID, or a universal economic/world simulator.
- The P2 fixed tuple and P6 house are local adapters; the generic engine remains actor/source/operation agnostic.

## 5. Refusals the extension must preserve

```text
wrong root/actor/branch/clock          refuse before effect
non-participant or spoofed participant refuse before effect
source/registry/rule/version mismatch  refuse before effect
stale head or changed plan             refuse before effect
bad target in a record batch           rollback all records
interrupted write                      durable pending/HOLD; no blind reissue
missing rule                           MISSING_RULE, never NO_CHANGE
model prose or provider mutation       no canonical write
```

## 6. Acceptance owed by CG-B/C/D

See `02_SELECTED_ABI_AND_CG_BCD_CONTRACT.md` section 5. The minimum is a cold, later, actor-local decision that consumes an exact sourcefree home/actor record, a control that does not, a second-actor speech whose private state never reaches the child, and source/identity/refusal tests. CG-A does not implement those; it provides the selected writer and the exact missing edge.

## 7. PW note

`PW-01..PW-12` definitions are not present in the repository. The twelve explicit mission functions are mapped in `02_SELECTED_ABI_AND_CG_BCD_CONTRACT.md` section 4. This return does not invent the named PW set.
