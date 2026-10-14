# D06 — Engineering, representation, retrieval and cost

**ASTRA_NEW_RECOMMENDATION, PROVISIONAL.** No schema/runtime implemented or benchmark executed. Inherited requirements: V3_COMPLETION, ADP016, CAN008_R2 and Sorok100/101. Vendor facts below were checked against primary documentation; selection is this review's inference, not a vendor claim.

## E1 — Storage alternatives

| Option | Transactions / serialization | History, ancestry, n-ary and replay | Checkpoints, analytics, operational cost | Decision |
|---|---|---|---|---|
| SQLite event/relational | Local transaction boundary; one writer per DB requires serialized admissions | Event and relation-participant tables, exact parent refs and append-only rules; recursive traversal/indexes | Simple deployment; snapshots/materialized views; cross-run export | Preferred bounded single-host lab baseline |
| PostgreSQL | Concurrent service transactions; explicit actor versions/locks and multi-actor transaction; handle serialization retries | Same logical model, foreign keys and recursive ancestry; immutability still application policy | More operations, stronger shared-service fit | Choose when concurrent writers/service deployment is actually required |
| Graph-first | Can be transactional; not inherently weaker integrity | Natural traversal; relation instances as nodes for n-ary roles; temporal event/version semantics still custom | Strong exploratory traversal, additional operational/query model | Reconsider if measured traversal dominates; not default ontology-driven choice |
| Document/event log | Good append semantics; multi-document invariants depend on chosen store and transaction design | Event payloads convenient, but foreign keys, participant constraints and authoritative ordering need explicit machinery | Easy ingestion; difficult ad hoc integrity/joins; replay needs schema evolution discipline | Useful artifact/log layer; insufficient alone without owner-state transaction design |
| Relational + materialized graph | One authoritative transactional ledger/state; graph derived by exact version | Best separation of truth versus traversal; derived graph rebuildable | Some view maintenance, bounded local updates | Selected logical architecture |
| DuckDB sidecar | Read/analysis lane over immutable exports | Excellent candidate for cross-run analysis; not proposed as competing causal writer | Hash-bind export cut; no feedback into live truth without admission | Optional after real analysis need, not baseline dependency |

SQLite's official guidance supports local storage and describes a single writer per database, recommending client/server systems for many concurrent writers and cautioning against network filesystems. This supports the bounded local choice, not a measured Rawlsing capacity claim. [SQLite guidance](https://www.sqlite.org/whentouse.html).

PostgreSQL Serializable provides serial-equivalent committed execution but can require whole-transaction retries. Default Read Committed alone is not a coherent multi-query world snapshot guarantee. Use explicit immutable snapshot identity and appropriate transaction/locking semantics. [PostgreSQL isolation](https://www.postgresql.org/docs/current/transaction-iso.html).

Neo4j provides ACID transactions; graph-first is rejected as a default because owner/version/temporal semantics still need design, not because graphs lack transactions. [Neo4j transactions](https://neo4j.com/docs/operations-manual/current/database-internals/transaction-management/).

DuckDB's in-process mode has a single read-write process or multiple read-only processes. Its current documentation also describes server/catalog alternatives for multiprocess writes; this review does not claim DuckDB universally cannot support them. Immutable analytical exports keep the proposed causal architecture simpler. [DuckDB concurrency](https://duckdb.org/docs/current/connect/concurrency).

## E2 — Canonical representation

| Record | Minimum contents and authority |
|---|---|
| Event | Event ID, root/branch, occurrence class, participants/roles, effective time/order, parent IDs, world receipt, rule/RNG refs, admitted effects and commit identity |
| Durable object version | Owner/type/semantic ID, actor/scope, valid interval, prior version, parent events and exact state; sparse unknown distinct from neutral |
| Relation | Typed participant roles/context, interval, evidence and owner; perceived and objective versions distinct |
| Hyperrelation | One relation instance plus ordered/typed participant rows and cardinality; pairwise indexes are derived |
| Derived view | Exact source versions and derivation version; rebuildable, no independent truth |
| Motif | Named query/view with evidence; becomes durable only under a distinct admitted lifecycle |
| Checkpoint | Ledger offset/root hash, owner-state snapshot hashes, schema/rule versions; optimization, never an event or authority |
| Lived artifact | Content-addressed immutable payload, typed claim manifest, event/admission/access links and model/prompt/output identity |
| Index | Temporal, participant, causal-parent, scope, access and retrieval keys; caches may be discarded/rebuilt |

Do not duplicate a memory's truth in a summary, an expectation in an attractor vector and a PFF session object, or an objective relation in a perceived-relation record without distinguishing meaning. History corrections append supersession/adjudication, not overwrite occurred facts. Checkpoints accelerate replay; they do not license deleting causal ancestry.

Joint events should atomically commit occurrence plus permitted effects for the affected owner versions, or use a formally specified pending transaction that cannot be observed as committed. Lock actors in deterministic order and version-check shared relations/world resources. A per-actor lock alone cannot protect two actors spending the same resource. Keep model calls outside long-lived database locks; validate expected versions before admission and retry/recompute on change.

For outward speech/actions, record accepted occurrence and an idempotent publication/outbox record before delivery; distinguish committed-for-delivery, actually emitted/delivered and perceived. Rejected/unemitted drafts never self-feedback. Crash recovery must prevent double utterance effects and must not pretend a failed delivery was perceived. Exact scheduling/occurrence semantics require their owners; an outbox is engineering, not permission to mint an event.

## E3 — LLM/deterministic division

| Function | Mode |
|---|---|
| IDs, closure, units, clocks, permissions, selection by accepted predicates, hashes and state transactions | Deterministic computation |
| Event choice/response branch where probabilities are specifically warranted | Governed stochastic rule with exact finite support and RNG receipt |
| Event interpretation, relation candidate nomination, unresolved texture | LLM proposal under schema and bounded evidence; never automatic canonical truth |
| Actor expression and user-visible language | LLM rendering from separate actor-safe/phenomenal projections |
| Meaning of a relation, comparability, quantity scale, response mechanism and new ontology | Competent human/adjudicated semantic/scientific authority |
| Motifs, graph summaries, Enneagram affinity and cross-run analysis | Derived analysis; no causal feedback by default |

Cache exact accepted model outputs and admission receipts for deterministic replay. Rerunning the same prompt/seed against a remote model is not an exact replay guarantee. Model/prompt/version lineage supports audit; it does not alone guarantee causal validity.

## E4 — Retrieval

Start from the current event's participants, relationships, active strivings/expectations, context and declared rule needs. Use exact causal-parent links and owner indexes to retrieve mandatory bases. Then nominate optional related candidates by temporal/topological or lexical/vector search, each with reason and source IDs. Semantic similarity ranks candidates; it never establishes causation or actor access.

Use separate retrieval projections for causal evaluator, actor expression and user phenomenology. A hidden trace may reach the evaluator but not the actor's prompt as autobiographical explanation. Expansion follows unresolved parent/evidence references within a declared budget. If a mandatory base is absent, return unresolved/defer; don't fill it with a summary. Record inspected, admitted and excluded candidate IDs so omission bias is testable.

Maintain hot current state, warm indexed significant histories and immutable cold ledger/artifacts. No full-life prompt each turn. Noncausal summaries point to exact originals; material decisions re-dereference them. Periodic retrieval audits should inject old, low-similarity but causally relevant events and irrelevant high-similarity decoys.

## E5 — Budgets and growth

Let E be admitted events, R admitted relations, a average event ancestry links, k active touched relations, and m bounded motif size. Storage is approximately O(E+R+aE), while naive all-pairs nomination is O(R²) and unconstrained motif enumeration can be worse. Update only touched relation neighborhoods and declared motif queries; retain cold history rather than erase it. A cap must defer optional analysis or expand a declared budget, not silently omit a required causal parent.

Illustrative planning assumptions, **not measurements**: 20,000 typed events × 1 KB plus 5,000 artifacts × 4 KB is about 40 MB before indexes, provenance, copies and backups. Six deeply generated people × 500 significant episodes × two model calls is 6,000 calls. At assumed 8,000 input/1,000 output tokens each, that is 48 million input and 6 million output tokens. The danger is unnecessary semantic calls and recursive social breadth, not this raw storage arithmetic. Monetary cost requires a chosen provider/model and current price; no dollar estimate is asserted.

Use zero calls for mechanically unchanging scheduler intervals and cache derived projections. Reserve semantic work for admitted significant transitions; do not delete developmental depth to hit a call target. Prototype live budget: at most two ordinary model calls, with separately counted rare recovery; report p50/p95 latency, input/output tokens, retry rate and admission rejection. Set the actual latency/cost envelope before court from deployment constraints. No present F5 claim follows from this target. Compare one-call, two-call and deterministic-render controls when they preserve the same authorized semantics.
