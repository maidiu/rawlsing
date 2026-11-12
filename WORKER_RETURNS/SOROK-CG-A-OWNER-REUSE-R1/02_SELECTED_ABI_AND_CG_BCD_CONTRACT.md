# Selected ABI and CG-B/C/D contract

**Status:** sourcefree TEST_ONLY engineering contract. No native science, actor right, production authority or protected merge.
**Source custody:** author executed at `2be0cf252662ad021571db6f0d38b12c205c56ae`, while PR #915 is based on protected `1f77f2036427a410429184780ef884ec4f253ad0`. Exact selected Git blobs, not claimed universal startup equivalence, govern. The three malformed source-matrix identities are corrected on this review repair branch; relevant P6 `run_p6.py` changed across these cuts.
**Selected owner-domain composition, not a common world writer:** P2/P6 world state owns material facts and speech events; P3/PsycheStore owns sourcefree actor-scoped mediator records. The existing BatchEngine/RecursionCycle remains the developmental scheduler. An explicitly qualified READ-ONLY bridge is needed from P3 state into the actual P6 situated consumer.
**No new scheduler:** the existing three-event-to-five-event cycle remains the only scheduler.

## 1. Exact current signatures

### 1.1 Engine contracts

`developmental_recursion/contracts.py` (`c4ce557c...`):

```text
StateIdentity(root: str, actor: str, branch: str, clock: int, state_hash: str)

EventProposal(event_id: str, event_time: int, operation: str,
              source_refs: tuple[str, ...], participants: tuple[str, ...],
              circumstances: Mapping[str, Any],
              interval: Mapping[str, Any] | None)

RealizedEvent(operation_id: str, proposal_hash: str, before: StateIdentity,
              after: StateIdentity, status: str, objective: Mapping[str, Any],
              accessible: Mapping[str, Any], consequences: Mapping[str, Any],
              readset: tuple[str, ...], receipt_ref: str)

DevelopmentOwner.snapshot() -> StateIdentity
DevelopmentOwner.validate_proposal(proposal) -> None
DevelopmentOwner.realize(operation_id, proposal, expected) -> RealizedEvent
```

`BatchEngine(owner, journal_path)` exposes `run_batch(batch_id, proposals) -> {batch_id, history_hash, records}`, `history(batch_id) -> same shape`, `verify() -> bool`, and `owner`. It accepts 3–5 proposals, rejects non-forward event times before the first reservation, validates all proposals before the first effect, binds the journal to the initial `(root, actor, branch)`, checks every owner `after` identity and current snapshot, and records a durable reservation before `owner.realize`.

`RecursionCycle(engine, provider, store_path)` exposes `bootstrap(context=None)`, `advance(context=None)`, `finish(context=None)`. It reserves a provider call before invoking it, refuses a provider that mutates owner state, validates retrospective `batch_id`/`history_hash`/ordered `event_ids`, completes the retrospective before realizing the next batch, and requires terminal `prospective=null`. There is no model call between events.

### 1.2 P2 base adapter

`P2Owner` (`3160eb15...`):

```text
P2Owner(fanin, *, case, source, participants)
snapshot() -> StateIdentity
validate_proposal(proposal) -> None
realize(operation_id, proposal, expected) -> RealizedEvent
actor_experience(event, *, after_clock) -> dict
```

Local limits, not generic root policy:

- `participants` must equal `tuple(root["actor_ids"])` (`p2_owner.py:45-46`).
- `self.actor = root["actor_ids"][0]` (`p2_owner.py:47`).
- operation must be `ADMIT_EVENT`; interval modes are `ACTUAL` or `SCHEDULED_ONLY`; span is a positive integer and must not cross the event clock.
- `snapshot.state_hash` hashes `world`, `events`, `intervals` and `encounters`; actor experience uses the developing actor's perception receipts, not the portal user view.
- Repeated operation IDs resolve from the owner receipt or raise `P2_AMBIGUOUS_PRIOR_OPERATION_HOLD`; native effects are never blindly reissued.

### 1.3 P3 sidecar owner and store

`P3Owner` (actual Git blob `233a89f2cf99c192717cb223a771af47efe3bbd2`):

```text
P3Owner(base_owner, *, source, history, plans, catalog=None,
        compression_specs=None, standpoints=None, mode="TEST_ONLY")
snapshot() -> StateIdentity
validate_proposal(proposal) -> None
realize(operation_id, proposal, expected) -> RealizedEvent
```

`P3Owner` requires the base owner's `snapshot`, `validate_proposal`, `realize`, `actor_experience` and `fanin`; binds `source.root/actor/branch` exactly to the base snapshot; freezes source hash, history, plans, catalog, compression specs, standpoints and code pins; and composes one `PsycheStore` at `<state_root>/p3_psyche.sqlite3` with `binding={root, actor, branch}`. A pending sidecar operation blocks an unrelated operation. The recovery phases are `PREPARED -> WORLD_COMMITTED -> PSYCH_COMMITTED -> COMPLETE`.

`PsycheStore` (actual Git blob `d38a67ce72ae40b44bd97705bb6837265804d071`):

```text
PsycheStore(path, *, binding={root, actor, branch}, registry_hash, source_hash)
head() -> {hash, count}
query(*, project, counterpart, as_of) -> list[record]
get_operation(operation_id) -> dict | None
pending() -> list[dict]
reserve(operation_id, *, proposal_hash, expected, plan_hash, base_before,
        psyche_before, plan) -> dict
save_world(operation_id, base_result) -> dict
commit_effects(operation_id, *, records, response, event_binding,
               compression=None, projection=None) -> dict
finish(operation_id, result) -> dict
verify() -> bool
```

`query` is exactly actor-local (`root=? AND actor=? AND branch=?`), effective time `effective_from <= as_of`, exact `project`/`counterpart` scope, deterministic `(effective_from, seq)` order. A record must bind the same root/actor/branch, source hash, registry hash, permitted rule version/hash, event clock, and an actual event hash in `causal_parents`; a bad target rolls back all records. `head` is a chained immutable record-state hash/count, not a whole-life rewrite.

### 1.4 P6 material and situated readers

`house.py` (`af556c14...`):

```text
establish(session) -> writes world.resources["p6_house"]
establish_gallery(session) / establish_symbolic(session)
read_house(session) -> (world, house)
facts_for(history, objects, epoch) -> dict
perform(session, action) -> event
scene(session) -> dict
```

`read_house` requires the current root, branch, exact source hash, exact rooms/objects, and valid object-history provenance. The house resource contains `root`, `branch`, `source`, `epoch`, `rooms`, `objects`, `presentation_conditions`, and `history`; it is part of `world.resources` and therefore part of the P2 `snapshot` material hash.

`situated.py`:

```text
actor_context_for(actor_id, context) -> dict | None
recent_speech(session) -> list[{event_id, clock, speaker, text}]
reconsider(session, receipt, interpret, realize=None, *,
           actor_context=None, provider_mode="INJECTED") -> dict
```

`recent_speech` filters only events perceived by actor `A`; `reconsider` builds an actor-local packet from world/house/actor state, validates a model decision against actual cues and actions, and commits speech through `session.product.say(text, actor="A")`. At the frozen author source cut it does not query `PsycheStore`; the separate repair branch now adds an opt-in TEST_ONLY read-only bridge from the real owner.

## 2. Owner, time, actor, version and edge

| Dimension | Selected current rule | Limit for CG-B/C/D |
|---|---|---|
| Owner | `P3Owner` composes `P2Owner` and `PsycheStore`; only the owner writes | One `P3Owner` per single `(root, actor, branch)`; no multi-actor owner |
| Root | exact `root` string checked by P2, P3 and store | one root can be reused, but stores are actor-bound |
| Branch | exact `branch` string checked at every layer | no branch switching inside a batch |
| Clock | integer; event times strictly forward; interval span; `effective_from <= as_of`; P6 `epoch` | P6 epoch is not a historical calendar; S46 span is not a calendar |
| Actor | focal actor is P2 `actor_ids[0]`; P3 store binds that actor | mother can only be a counterpart string, not an independent actor |
| Version | store binding, head, source hash, registry hash, plan hash, rule id/version/hash, causal parents, receipt hash | no native rule version is issued |
| Material | P2 world/interval snapshot; P6 `p6_house` resource | no `home_period` from/to/home_ref record |
| Later edge | P3 B1 mediator records are actor-local; P6 situated reads world/actor | Separate sourcefree read-only P3→P6 first-consumer bridge is repair candidate, not native action |

The exact later-consumer edges are:

```text
P3 sidecar:   PsycheStore.query(project, counterpart, as_of)
              -> P3Owner._effect -> test_rules/projections -> RealizedEvent.readset
P2 material:  S46 interval/world -> S47Session.read_c9_conditioning -> later P2 event
P6 situated:  house.read_house + world.actor_state -> situated.reconsider -> say/decision
```

The missing edge in the author's original source is a **qualified P3→P6 read-only bridge**, not another scheduler. The isolated reviewer branch implements that seam and tests the actual P6 actor speech/no-speech consumer. It does not make material facts into PsycheStore records.

## 3. Minimal CG-B/C/D extension contract

These are interface obligations, not an implementation of CG-B/C/D.

### 3.1 `RootActorSet`

```text
participants(root) -> tuple[str, ...]            # from session.read_root()["actor_ids"]
select_focal_actor(proposal, plan) -> str        # must belong to participants(root)
composite_snapshot() -> StateIdentity            # root, focal actor, branch, clock, state_hash
```

`composite_snapshot.state_hash` must bind at least:

```text
digest({
  "p2_state_hash": <P2Owner.snapshot().state_hash>,
  "actor_store_heads": {actor_id: <PsycheStore.head().hash>, ...},
  "house_hash": <digest(house source/epoch/history)>,
  "home_period_hash": <digest(home_period) or null>
})
```

One `PsycheStore` per actor under the same root/branch; `binding.actor` is that actor. A proposal must not spoof `participants`; the adapter verifies the set against the native root and the focal actor against the plan.

### 3.2 `HomePeriodResource`

```text
establish_home_period(session, *, home_ref, from_clock, to_clock,
                      actors, source_ref) -> dict
read_home_period(session, *, as_of) -> dict | None
```

The record stores `root`, `branch`, `source_hash`, `home_ref`, `from_clock`, `to_clock`, `actors`, `history_refs` and a content hash. It is written into `world.resources` and must be part of the P2 `snapshot` material hash. It must not create a second person/world ledger, a new scheduler, or an automatic trait delta. `from_clock`/`to_clock` are interval inputs; they do not by themselves authorize an encoded change.

### 3.3 `MotherSpeech`

```text
admit_speech(session, *, speaker, recipient, text, source_ref,
             event_time) -> admitted event | HOLD
read_qualified_speech(session, *, recipient, speaker, as_of) -> list[dict]
```

Use the existing P6/P2 event writer and perception store. The child receives only the qualified speech fields (`event_id`, `clock`, `speaker`, bounded `text`) after recipient perception; the child must not receive the mother's private ledger, objective history, or unadmitted model prose. The speaker must be a real actor in `participants(root)`; a counterpart string is insufficient.

### 3.4 `SidecarDecisionReadset`

```text
decision_readset(store, *, project, counterpart, clock) -> {
  "records": [...],
  "hashes": [...],
  "head": <store.head().hash>,
  "as_of": clock
}
```

The existing `situated.reconsider` packet may carry this readset, but it must be read-only. After a grounded decision, any durable actor record must be written through `P3Owner.realize` (plan/source/rule/refusal enforced), never by a direct store mutation from the provider. The provider receives detached records only; it never receives the store or a writer.

## 4. Functional mapping

The author's source search did not locate `PW-01..PW-12` in its selected tree. Their user-blueprint definitions are available in unmerged PR #911; the author result was a limited visibility claim, not global nonexistence. The table below maps functions, not invented IDs.

| Mission function | Selected capital | Disposition |
|---|---|---|
| 1. Exact root/actor/branch/clock identity | P3 contracts; `PsycheStore` binding | REUSE |
| 2. Dated material home/period | P6 `house`; missing `home_period` | ADAPT + BUILD |
| 3. Independent mother actor | P2 root `actor_ids`; no per-actor writer | BUILD (`RootActorSet`) |
| 4. Constrained decision/utterance | P6 `situated.reconsider`; P3 rules | ADAPT |
| 5. Child receives only qualified speech | P6 `recent_speech`; missing mother speaker | BUILD (`MotherSpeech`) |
| 6. Actor state change/HOLD/NOCHANGE | P3 sourcefree records; native `MISSING_RULE` | REUSE mechanical test-only; native issuer HELD |
| 7. P6 situated decision reads actor-qualified prior P3 records | P3 actor-bound store and new optional P6 sourcefree bridge | REPAIR CANDIDATE; sourcefree consumer test required |
| 8. Duration and intermediate time as inputs | P2 interval span/modes; P6 `epoch`/`elapsed` | REUSE/ADAPT |
| 9. Historical positive target write/read | B1 exact `mode_for`; P3 formation/later response | REUSE/ADAPT |
| 10. Transaction/rollback/refusal | `PsycheStore` phases; B3A precedent | REUSE |
| 11. Cold/restart/crash | `BatchEngine` journal; `PsycheStore`; cold-later test | REUSE |
| 12. Source/version/refusal | store binding/source/registry/head; source severance | REUSE |

## 5. Acceptance contract for CG-B/C/D

The following are the minimum S2 tests the next construction must supply; CG-A did not run them because the adapter is absent:

1. one root, one focal actor, one independent mother: a mother speech event is admitted and only the child's qualified perception reaches the next decision;
2. a dated `home_period` is written and read later; removing or altering its source changes the later eligibility/HOLD;
3. a cold reopen between the mother event and the child decision preserves the exact home/period and actor record hashes;
4. a later child decision consumes the exact record hash in its readset; a control without the record chooses the `inspect_alone`/HOLD path;
5. wrong actor, wrong counterpart, wrong root, stale clock, and a non-participant spoof refuse before any effect;
6. a failed or interrupted write leaves no partial record and is not double-applied;
7. `MISSING_RULE` remains distinct from evaluated `NO_CHANGE`; `HELD`/`REFUSED`/`OMITTED` are not converted to `NO_CHANGE`;
8. no provider or model prose writes canonical actor state.

Original author CG-A froze interfaces but did not implement the P6 sidecar first-reader. This isolated repair adds that sourcefree first-reader, not CG-B's material period, CG-C's independent mother, or native developmental rules. Mechanical storage acceptance does not issue psychology, memory or action.

## Independent CG-A semantic repair: owner-domain partition

The author `test_selected_common_readset.py` writes a synthetic `MEDIATOR` with `payload.room=kitchen` to a separate PsycheStore configured with synthetic source/registry hashes, then calls a test-local `later_decision`. This proves isolated storage mechanics but **not** a lawful common writer. Real `P3Owner` freezes the B1 TEST_ONLY registry; `P3Owner._effect` and `projections.activate` are B1 mediator/mode consumers and cannot be silently generalized to world-owned home facts. P2/P6 world resources own dates, homes and material constraints; mother speech must be an actual speaker event with recipient-qualified perception, not a psychological blob. The sourcefree P3→P6 bridge therefore reads ONLY prior actor-bound B1 mediator identities into the existing P6 situated packet, without new owners or native-science claims.
