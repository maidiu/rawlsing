# C05 ABI and source derivation

**Grade:** `SOURCEFREE_S2_C05` / `SOURCEFREE_S2_ONLY`
**Frozen candidate:** `9cf13763b0061400e2c936eaf1d0a2f4b76a03f7`
**Start:** `ee82397a979e52eab83f2bd4ea48ed9c28ea7ab9`

This document records the actual C05 ABI, the existing capital it reuses, and
the exact bytes/source relations. It is not a native relation, psychology,
language or authority claim.

## 1. Actual C05 ABI

Module:
`WORKER_RETURNS/SOROK-DEVELOPMENTAL-RECURSION-ENGINE-R1/developmental_recursion/continuing_relations.py`

### Write

```text
record_relation_change(
    session, *,
    actor_id, other_actor_id,
    relation, change, clock, operation_id,
    exposed_actor_ids=None, value=None, private_state=None,
) -> SOROK_P2_CONTINUING_RELATION_READ@1
```

- `actor_id` / `other_actor_id`: distinct live stable IDs. Root actors and C01
  registered supporting actors are accepted through
  `resolve_participants` / `read_supporting_actor`.
- `relation`: non-empty caller-supplied illustrative relation token.
- `change`: `ENTER` | `LEAVE` | `CHANGE`.
- `clock`: integer actual P2 world clock on first write. A future or backdated
  clock refuses (`RELATION_CLOCK_FUTURE` / `RELATION_CLOCK_BACKDATED`).
- `operation_id`: caller request identity. An exact retry returns `UNCHANGED`
  with the same primary/head IDs. Reuse with different content refuses
  `RELATION_OPERATION_REUSE_MISMATCH`.
- `exposed_actor_ids`: explicit exposure list. Both relation parties are
  required; additional live actors are allowed. Omitted means both parties.
- `value`: optional scalar illustrative relation value. `LEAVE` requires null.
- `private_state`: optional scalar mapping stored only in the C12 episode. Any
  private string appearing in the public body refuses
  `RELATION_PRIVATE_STATE_LEAK`.

```text
promote_relation(
    session, *,
    actor_id, other_actor_id, relation, depth, clock, operation_id,
) -> SOROK_P2_CONTINUING_RELATION_READ@1
```

- `depth` is currently exactly `2`. Promotion requires an existing verified
  scope with at least one state change and a lower current depth.
- It appends a `PROMOTE` episode whose `history_hash` commits the prior state
  entries. It adds no relation fact, no past entry and no world effect.
- Exposure for the promotion is the union of all exposures in the verified
  scope plus the two parties. A later exposure cannot see an earlier promotion
  it was not exposed to.

### Read

```text
read_relation_history(
    session, actor_id, *,
    other_actor_id=None, relation=None, as_of_clock=None,
) -> SOROK_P2_CONTINUING_RELATION_READ@1
```

- `as_of_clock` defaults to the current world clock; a future value refuses
  `RELATION_AS_OF_FUTURE`.
- A live viewer sees only entries whose `exposed_actor_ids` name it and whose
  clock is not later than `as_of_clock`.
- Status is one of `QUALIFIED`, `HOLD_NOT_EXPOSED`, `HOLD_UNKNOWN_SCOPE`,
  `HOLD_CUSTODY_SEVERED`. A denied/absent scope is never returned as a negative
  “no relation” fact.
- A partially exposed viewer gets `history_complete: false`,
  `prior_exposure: HOLD_NOT_EXPOSED`, and only the entries it was exposed to;
  no earlier entry is synthesized.

```text
read_actor_relative_context(session, actor_id, event_id)
    -> SOROK_P2_ACTOR_RELATIVE_CONTEXT@1
```

This is the terminal C05 consumer. It verifies the actual BP4 event seal, reads
the event through C01 `read_actor_access`, reads the relation history as of the
event clock, and returns:

- `event_access`: `PERCEIVED` / `NOT_PERCEIVED` / qualified custody HOLD, with
  the public S45 projection and receipt when perceived;
- `relation_scope`: status, custody, representation depth, qualified relation
  representations, withheld count;
- `context_effect`: whether the relation scope is actually used, the relation
  status/value, completion and depth, and (for a relation party) whether both
  parties had actual C12 event access.

Physical co-presence is never consulted for relation knowledge.

## 2. C12 storage and source derivation

### Change episode

Kind: `P2_CONTINUING_RELATION_CHANGE`
Schema: `SOROK_P2_CONTINUING_RELATION_CHANGE@1`

Body fields (actual order does not matter; canonical JSON is used):

```text
schema, grade, root, branch, relation_key, actor_ids, aliases,
relation, change, value, clock, operation_id,
exposed_actor_ids, exposed_aliases, private_state_hash, private_state,
sequence, previous_episode_id, source
```

- `actor_ids` is the sorted two-actor stable-ID pair; `aliases` is the
  corresponding branch aliases.
- `relation_key = sha256(canonical({"actor_ids": [...], "relation": token}))`.
- `sequence` starts at 1 per relation scope.
- `previous_episode_id` is the previous change episode ID in this scope or null.
- `private_state` is the raw caller-supplied private mapping in this C12
  episode only; `private_state_hash = sha256(canonical(private_state))`.
- `source = relation_change_source(body)` where the source callable hashes all
  body fields except `source` and `private_state`. Thus the public source binds
  the private commitment, identity, clock, exposure, sequence and chain
  predecessor without requiring raw private values to be re-derived by a reader.

The function is public:

```text
relation_change_source(body) -> 64-hex sha256
```

### Custody head episode

Kind: `P2_CONTINUING_RELATION_HEAD`
Schema: `SOROK_P2_CONTINUING_RELATION_HEAD@1`

Body fields:

```text
schema, grade, root, branch, relation_key, actor_ids, aliases, relation,
sequence, clock, operation_id, primary_episode_id, primary_episode_hash,
previous_head_episode_id, previous_head_hash,
exposed_actor_ids, exposed_aliases, source
```

`source = relation_head_source(body)` hashes every head field except `source`.
The head is appended in the same C12 transaction as its primary change. It is a
custody anchor, not an actor-facing relation record.

### Verification

`_verify_scope` verifies:

1. primary episode kind, schema, grade, root, branch, relation key and clock;
2. content address and private commitment;
3. live actor IDs and matching aliases;
4. exposure includes both parties, is sorted/unique, and every exposed actor is
   live;
5. sequence is 1..N and `previous_episode_id` links exactly to the prior
   primary;
6. the finite relation state machine over all changes;
7. promotion depth/history hash;
8. head count equals change count, each head points to the matching primary
   ID/hash/clock/operation/identity/exposure/relation, and the head chain links
   exactly;
9. any failure is a qualified `HOLD_CUSTODY_SEVERED`, never partial trust.

Because a head remains when a primary is severed, a reader can distinguish
“absent scope” from “scope whose committed bytes are missing/forged.” A complete
privileged erasure of both primary and head bytes remains a raw-store-authority
residual, not a claim of local read-side custody.

## 3. State machine and representation depth

State changes:

```text
ENTER  requires state ABSENT or LEFT  -> ACTIVE
CHANGE requires state ACTIVE or CHANGED -> CHANGED
LEAVE  requires state ACTIVE or CHANGED -> LEFT
```

`PROMOTE` requires a non-absent relation and depth 2 > current depth; it does not
alter `ACTIVE`/`CHANGED`/`LEFT` or any dated entry.

A reader’s representation depth is 1 until a promotion it was exposed to, then
2. Promotion never rewrites, reorders, deletes or backfills a state entry.

## 4. Exposure and actor-relative context

- Every change names an explicit exposure set including both relation parties.
- A viewer sees an entry only if its stable ID is in that entry’s
  `exposed_actor_ids` and the entry clock is not later than the read clock.
- A viewer never sees the exposure set of an entry; only the relation token,
  parties, counterpart (if a party), visible entries and own history state.
- A viewer that is not a party and not exposed gets no relation token, party IDs,
  entry clock or private value; it gets a qualified HOLD and a withheld count.
- A viewer exposed later sees only its own later entries and
  `history_complete: false`; it never receives an automatic earlier entry.
- For a party, a context effect may report `both_parties_event_access` using the
  existing C01 event reader for both parties. Other viewers do not receive this
  derived fact.

## 5. Existing capital actually reused

| Need | Reused actual API |
|---|---|
| Live root/supporting identity | C01 `resolve_participants` → `read_supporting_actor`, S44 root read |
| C12 durable append | `session.product.store.append_episode`, `episodes` |
| Atomic multi-row write | C01 `supporting_actor._StoreWrite` (`BEGIN IMMEDIATE`/savepoint) |
| Actor-relative event access | C01 `read_actor_access` |
| Real later performed event | existing `P2Owner.realize` / `S47Session.admit_event` |
| Event hash/ID seal | BP4 `EVENT_SCHEMA`, `WORLD_GRADE`, content-addressed event ID |
| Public event projection | `s45_projection.projection.project_event` through C01 reader |
| World/clock | existing S47 world/checkpoint, no new clock |

No new relation owner, world store, psyche store, biography store, scheduler,
actor database, perception channel, speech writer or provider call is added.

No indispensable existing-owner API was missing: the implementation was possible
entirely inside the two leased product files. No proposed additional owner edit
is required for this bounded C05 candidate.

## 6. Nonclaims

- The module is not native ADP-015/C4 issuance, household/genealogy membership,
  family law, maternal psychology, independent volition, autonomy or generated
  language.
- The caller supplies the illustrative relation event; no autonomous actor
  choice or selected activity rule is implemented.
- The later event is the existing sourcefree P2 owner admission; its language
  content (if any) is inherited S45/S39 engineering and is not authored by C05.
- No C04 parent metadata, hidden reason, D03 caller-receipt root/branch binding,
  G2 selector, J1 complete response or protected merge is trusted, promoted or
  repaired.
