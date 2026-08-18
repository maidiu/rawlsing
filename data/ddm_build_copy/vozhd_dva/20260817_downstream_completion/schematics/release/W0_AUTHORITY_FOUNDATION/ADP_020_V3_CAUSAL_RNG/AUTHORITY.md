# ADP-020 — V3 Causal Randomness / Named-Stream Authority

**Authority ID:** `ADP-020`  
**Authority version:** `1.0.0`  
**RA-R00 authority:** `MUST-020`  
**Repository:** `maidiu/rawlsing`  
**Assigned branch:** `agent/vozhd-dva-w0-adp-020-v3-causal-rng`  
**Exact base SHA:** `655da47b9e03ab310ed4b7fa65ceec9b9d04d3bc`  
**Mode:** authority creation only; whole-machine architecture remains CLOSED  
**Status:** `PASS`  
**Consumer release sufficiency:** `SUFFICIENT`

## 1. Authority verdict

ADP-020 creates the terminal V3 causal-randomness authority required by the accepted V3 and whole-machine architecture.

Its governing law is simple and absolute:

> **Randomness can resolve contingency among already-lawful possibilities. It cannot create lawfulness, repair missing authority, create a candidate, fabricate biography, or make an unadmitted proposal causal.**

Every causal stochastic choice is therefore a function of an immutable causal root seed; a stable actor/joint/genealogy/run scope; a static registered `v3.causal.*` stream; a stable draw coordinate; exact candidate/parameter identity; exact semantic rule identity; and versioned derivation/sampler law. Everything required to recompute the choice is persisted before or with the causal mutation.

This authority does **not** define candidate semantics, event semantics, genealogy semantics, attractor semantics, scheduler precedence, V2 render randomness, or LLM proposal/admission semantics.

`CONSUMER_RELEASE_SUFFICIENCY = SUFFICIENT` means MUST-020 itself is complete. It does not release a consumer packet whose other W0 authorities remain absent or unadjudicated.

## 2. Required archive verification

The attached historical archive was directly hashed before any reliance on its contents.

- logical archive: `Rawlsing_code_bundle_staging.zip`
- expected SHA256: `953c9149bd03877206e3cb440d1f4db35dea6473af30b97fd23b7e76c6fc0086`
- computed SHA256: `953c9149bd03877206e3cb440d1f4db35dea6473af30b97fd23b7e76c6fc0086`
- verdict: `EXACT_MATCH`
- use: continuity / authority-recovery evidence only
- historical archive V5/DDM authority over current V550+: **ZERO**

## 3. Governing evidence inspected

Current binding authority/architecture inspected directly:

- `.../W0_AUTHORITY_FOUNDATION/LAUNCH_REGISTER.md` — common W0 law and **W0-07 only**;
- `.../RA_R00_RULE_AUTHORITY_IMPLEMENTATION_RELEASE/RESULT.md` and `RESULT.json` — ADP-020 / MUST-020, no prerequisite authority, exact consumer packets;
- `.../integration/V3_COMPLETION_IMPLEMENTATION_RULING.md`;
- `.../schematics/recalibration/TD_R05_V3_DEVELOPMENTAL_RUNTIME/RESULT.md`;
- `.../schematics/closure/TD_R07_WHOLE_MACHINE_SYNTHETIC_LIFE/RESULT.md` — replay proof;
- `.../integration/WHOLE_MACHINE_ARCHITECTURE_CLOSURE_RULING.md`;
- `.../state/CURRENT_STATE.md`.

Current source/test terrain inspected:

- recursive current repository tree at the assigned branch/base: no terminal V3 runtime package is present; V3 implementation remains unreleased;
- `data/ddm_build_copy/test_w03_v551j_v3_fail_closed.py`;
- `data/ddm_build_copy/test_w03_v551j_v3_consumer.py`.

These extant tests are upstream V551/V551J consumer-boundary tests, not a terminal V3 RNG implementation. They nevertheless reinforce the current fail-closed contract style: missing manifests, wrong versions/hashes, unresolved authority and identity mismatch are typed failures rather than guessed-through states.

Directly inspected recovered V3/server source in the verified archive:

- `v3/engine/scoring.py`;
- `v3/engine/run_llm_band.py`;
- `v3/engine/event_engine.py`;
- `v3/engine/effects/metabolization_effects.py`;
- `v3/io/seeds.py`;
- `v3/engine/yearly_step.py`;
- `v3/tests/test_distribution_smoke.py`;
- `server/generation/simulation.py`;
- `server/routes/start.py`;
- `server/routes/discovery.py`;
- `server/generation/formatting.py`.

The recovered source establishes useful continuity and exact defects:

1. `select_candidates(..., rng=...)` shows the intended boundary in which code can choose among proposal candidates, but `rng = rng or random.Random()` makes the stream unnamed/unreplayable under terminal law.
2. Surprise selection uses `rng.random()` and `rng.choice()`: stochastic choice exists, but candidate-set identity, stream identity, rule version and draw provenance are insufficient.
3. `run_llm_band_year` repeats the unnamed `Random()` fallback and, when scored selection is empty, forcibly selects the first candidate. Terminal V3 explicitly rejects that concretization fallback.
4. `metabolization_effects.py` contains both optional unnamed `Random()` fallbacks and module-global `random.random()` / `random.choices()` rupture/template decisions. Those are forbidden for causal truth.
5. `server/generation/simulation.py` passes `random.Random()` without a persisted named seed lineage.
6. `v3/io/seeds.py` uses `random.Random(seed)` and is deterministic for a supplied seed: this is useful continuity for explicit seed provenance, but its one sequential stream is not sufficient for cross-domain isolation.
7. `event_engine.py`'s deterministic pseudo-random arithmetic events preserve reproducibility intent but manufacture generic causal content. Terminal law retains provenance/replay and removes RNG-as-event-semantics.
8. `test_distribution_smoke.py` uses explicit per-agent seeds, confirming the historical reproducibility intent that ADP-020 now constitutionalizes.

## 4. Constitutional boundary

ADP-020 binds all of the following:

1. randomness is not semantic authority;
2. RNG may operate only after the owning semantic authority has produced an already-lawful finite possibility/range/probability contract;
3. missing candidate authority is a no-draw failure/defer/typed-empty state;
4. missing semantic rule authority is a no-draw failure/defer state;
5. an empty candidate set remains empty; no arbitrary candidate/event is invented;
6. V3 causal RNG and V2 render RNG are disjoint authorities and namespaces;
7. no wall clock, process ID, filesystem order, mutable `latest`, Python process hash, hidden network entropy, unnamed/global RNG or unrecorded model sampling may influence causal truth;
8. a changed candidate set changes replay identity;
9. a changed semantic rule/version changes replay identity;
10. deterministic operations consume no gratuitous draw;
11. rule/candidate identity and random-draw identity remain diagnostically separable;
12. incomplete RNG metadata blocks live causal mutation or replay rather than causing reseeding/salvage.

## 5. Root-seed provenance

### 5.1 Canonical root

A V3 causal universe/run has exactly one ADP-020 root seed record under this authority version:

- seed width: **32 bytes / 256 bits**;
- serialized form: **64 lowercase hexadecimal characters**;
- the exact seed bytes, or an exact durable capability that reproduces those bytes, must be available for replay;
- a SHA256 digest alone is **not** sufficient to guarantee replay.

### 5.2 Lawful root sources

Only two root-source classes are authorized in v1:

**`EXPLICIT_CALLER_SEED`** — exact 32-byte seed supplied as an immutable causal-run input before any stochastic decision.

**`RECORDED_OS_CSPRNG_ROOT_SEED_V1`** — exactly one 32-byte OS-CSPRNG acquisition when a new causal universe is created. Its source ID/version and resulting seed bytes must be atomically persisted **before the first V3 causal draw**. This one-time seed creation is not permission for ambient runtime entropy.

Forbidden root construction includes time, PID, Python `hash()`, filename/path ordering, mutable `latest`, default library RNG state, a V2 render seed, LLM sampling state or any unrecorded environment entropy.

A root seed cannot be silently replaced inside an existing causal history. A new seed means a new causal-run/universe identity.

### 5.3 Required `RootSeedRecord`

Persist before first draw:

`root_seed_id`, exact seed material/capability, `root_seed_sha256`, root source and source version, `ADP-020@1.0.0`, `seed_scheme_id`, `seed_scheme_version`, and causal-run identity.

## 6. Named-stream namespace

The only namespace governed here is:

`v3.causal.*`

Every semantic rule that may use entropy MUST bind an exact static stream name and one allowed ADP-020 operation in its governed rule-registry entry. Stream names are semantic-purpose labels, not dynamic storage locations.

Pattern:

`^v3\.causal\.[a-z0-9][a-z0-9_.-]{0,127}$`

An actor ID, candidate ID, candidate hash, rule version, wall-clock year, filename/path or incidental loop position must **not** be smuggled into the stream name. Scope identity is carried separately.

The allowed scope kinds are:

| Scope | Meaning under ADP-020 |
|---|---|
| `RUN` | explicitly governed pre-actor/run-level causal decision; consumer must prove no narrower stable scope exists |
| `ACTOR` | exact generated `actor_id` |
| `JOINT` | exact owner-supplied content-addressed joint-scope ID for a multi-actor causal decision |
| `GENEALOGY` | exact owner-supplied content-addressed genealogy-scope ID for reproduction/child-generation decisions |

ADP-020 does not define the participant roles or the semantic identity of a joint/genealogy opportunity. Their owners supply the stable scope ID.

Any `v2.*` render stream, ambient module-global RNG or unnamed `Random()` instance is outside/against this authority.

## 7. Seed-lineage law

Canonical scheme:

`V3_CAUSAL_HMAC_SHA256_COUNTER_V1 @ 1.0.0`

Domain separator:

`RAWLSING\0ADP-020\0V3_CAUSAL_HMAC_SHA256_COUNTER_V1\0`

Canonical coordinate serialization is UTF-8 canonical JSON: controlled field names sorted, no insignificant whitespace, Unicode string values NFC-normalized, and integer numeric coordinate fields only.

Derivation:

```text
scope_seed = HMAC-SHA256(
    root_seed,
    domain_separator || canonical_json({kind:"scope", scope_kind, scope_id})
)

stream_seed = HMAC-SHA256(
    scope_seed,
    domain_separator || canonical_json({kind:"stream", stream_name})
)
```

Persist `root_seed_sha256`, `scope_seed_sha256` and `stream_seed_sha256` with the corresponding identities/versions.

### 7.1 Deliberate orthogonality

**Semantic rule version and candidate-set hash do not salt the stream seed.** They are mandatory components of the *decision replay identity* instead.

This is intentional. If the semantic rule changes while the seed coordinate remains fixed, the raw entropy can remain identical while replay still reports `RULE_VERSION_DIVERGENCE`. If the candidate set changes, raw entropy can remain identical while replay reports `CANDIDATE_SET_DIVERGENCE`. That prevents a semantic change from masquerading as a random-draw change.

### 7.2 Cross-actor / genealogy isolation

Actor A and Actor B derive independent scope seeds from their exact actor IDs. Draws consumed by B can never advance or perturb A.

A child's actor stream derives from:

`root → ACTOR(child_actor_id) → named stream`

It does **not** inherit a parent's mutable RNG state. Adding/reordering siblings therefore cannot shift an existing child's stream.

Multi-actor/genealogy decisions use their exact owner-supplied `JOINT` or `GENEALOGY` scope. They never use “whichever parent's RNG is executing first.”

If a child actor identity is required before an actor-scoped draw and the genealogy authority has not created it, the draw is blocked. RNG does not invent the missing identity.

## 8. Counter-derived entropy and draw coordinates

ADP-020 does not authorize opaque mutable `random.Random` state as replay truth. Entropy is counter-derived from the named stream.

Algorithm:

`ADP020_HMAC_SHA256_UNIFORM_BELOW_V1 @ 1.0.0`

A draw coordinate contains:

- `scope_kind`;
- `scope_id`;
- `stream_name`;
- `anchor_event_index`;
- `anchor_event_id_or_init_checkpoint_hash`;
- `rule_invocation_id`;
- static `decision_slot`;
- `occurrence_index`;
- `draw_index`.

Index base is zero.

For initialization before any committed event:

- `anchor_event_index = -1`;
- `anchor_event_id = INIT:<initial_checkpoint_hash>`.

For ordinary causal decisions, `anchor_event_index` is the zero-based index of the latest committed V3 causal event anchoring the decision; `anchor_event_id` is its exact ID.

`rule_invocation_id` comes from the owning V3 rule/scheduler contract. **ADP-020 does not define scheduler precedence.** `decision_slot` is a static rule-declared slot. If that slot lawfully recurs in one invocation, `occurrence_index` is an owner-defined canonical semantic ordinal, never a loop/filesystem ordinal.

`draw_index` is the zero-based entropy draw within that decision. A deterministic decision has no draw index.

A resulting V3 event index is populated only after the outcome is independently admitted/generated. RNG cannot reserve, create or imply a causal event merely because it selected something.

### 8.1 `UNIFORM_BELOW(n)`

For `1 <= n <= 2^64-1`:

1. derive `HMAC-SHA256(stream_seed, domain_separator || draw_coordinate || block_index)`;
2. interpret the first eight digest bytes as unsigned big-endian `x`;
3. set `limit = 2^64 - (2^64 mod n)`;
4. if `x >= limit`, increment internal `block_index` and derive another block;
5. otherwise return `x mod n`.

Internal rejection blocks remain one semantic draw and do not advance `draw_index`; persist `entropy_block_count`.

The authoritative “stream state” is therefore immutable seed lineage + the content-addressed decision/draw-receipt ledger and coordinate-use index. No hidden mutable PRNG state is required.

Identical coordinate + identical replay identity is idempotent. Identical coordinate + different replay identity is `RNG_DRAW_COORDINATE_REUSE_CONFLICT`.

## 9. Lawful stochastic operations

V1 authorizes only exact finite operations whose semantics/parameters are already supplied by another authority:

| Operation | Lawful use | Draw law |
|---|---|---|
| `UNIFORM_CANDIDATE` | exact nonempty lawful finite set, semantic rule explicitly authorizes equiprobability | one `UNIFORM_BELOW(count)` unless count=1 |
| `WEIGHTED_CANDIDATE_INTEGER` | exact lawful candidates + exact nonnegative integer weight units from semantic rule; >=1 positive | one `UNIFORM_BELOW(total_weight)` unless one positive outcome |
| `BERNOULLI_RATIONAL` | exact `numerator/denominator`, `0 <= n <= d`, `d>0` | one draw only for `0<n<d`; p=0/1 deterministic |
| `UNIFORM_INTEGER_RANGE` | semantic rule has already authorized inclusive finite integer range | one draw unless range cardinality=1 |
| `UNIFORM_FIXED_POINT_RANGE` | semantic rule owns integer-tick range + exact decimal scale/quantization | same as integer range |
| `SAMPLE_WITHOUT_REPLACEMENT` | semantic rule authorizes finite stochastic sample | one draw per nondeterministic selected position |
| `RANDOM_PERMUTATION` | semantic rule explicitly makes order stochastic | versioned Fisher-Yates; 0/1 members consume none |

Arbitrary floating-library distributions, model sampling, random UUIDs, random serialization order and incidental random IDs are not authorized causal operations in v1. A semantic owner that requires a continuous quantity must supply an exact finite/quantized representation or obtain a future versioned sampler authority; ADP-020 will not silently choose an implementation-defined float distribution.

## 10. Candidate-set identity

RNG cannot generate or repair candidates. Before any candidate-selection draw, the semantic owner must hand ADP-020 a fully lawful `ADP020_CANDIDATE_SET_V1` record.

Every candidate entry requires:

- stable `candidate_id`;
- immutable `candidate_replay_hash`;
- `candidate_authority_id`;
- `candidate_authority_version`;
- exact `eligibility_or_admission_receipt_hash`;
- `weight_units` when weighted selection is used.

The candidate replay hash is required so that “same ID, changed payload” cannot masquerade as the same candidate.

### 10.1 Identity modes

**`SET_CANONICAL`** is default. Candidate IDs are NFC-normalized and unique; entries are sorted by UTF-8 bytes of `candidate_id`, then replay hash, strictly for hashing/selection coordinates. This creates no semantic priority.

**`SEMANTIC_ORDERED`** is allowed only when the candidate owner says order itself is semantic. The owner provides contiguous `semantic_position = 0..n-1`, which is persisted and hashed. Incidental runtime order cannot substitute.

### 10.2 Hash

```text
candidate_set_hash = SHA256(
  "ADP020_CANDIDATE_SET_V1\0" ||
  canonical_json({
    identity_mode,
    candidate_owner_authority,
    entries_with_replay_hashes_and_operation_relevant_integer_weights
  })
)
```

Persist the full canonical record or an immutable content-addressed reference that reconstructs it exactly. A hash with no recoverable set is insufficient for replay.

A candidate addition/removal, changed replay hash, changed semantic order or changed stochastic weight changes `candidate_set_hash` and thus the decision replay identity.

Merely receiving the same SET-mode candidates in a different filesystem/container order does not.

### 10.3 Empty set

Zero lawful candidates means **zero RNG draws**. ADP-020 preserves the candidate owner's typed lawful-empty/deferred/blocked state. It cannot select an ungoverned source item, choose “the first thing anyway,” fabricate an event, or inject a default biography.

## 11. Deterministic operations consume no draw

A stochastic-capable rule that has only one lawful result is deterministic for that invocation.

Examples:

- one candidate;
- one positive-weight candidate;
- Bernoulli p=0 or p=1;
- a one-point integer/fixed-point range;
- `k=0` sampling;
- a semantic rule that is deterministic by construction.

Persist a `DecisionReceipt` with `draw_consumed=false`; do not create a fake `DrawReceipt`. No dummy draw is allowed “to keep sequences aligned.” Counter-derived coordinates make such bookkeeping unnecessary.

## 12. Rule/version identity and replay identity

Every stochastic decision requires exact:

- `semantic_rule_id`;
- `semantic_rule_version`;
- `semantic_rule_registry_hash`;
- ADP-020 authority/version;
- seed/entropy algorithm IDs/versions;
- stochastic operation + exact parameters hash;
- candidate-set hash/ref where applicable.

Rule identity is not random entropy. It participates in the `decision_replay_identity_hash`.

```text
decision_replay_identity_hash = SHA256(
  "ADP020_DECISION_REPLAY_V1\0" ||
  canonical_json(
    authority/algorithm versions
    + seed-lineage digests
    + draw coordinate
    + semantic rule identity
    + operation
    + stochastic_parameters_hash
    + candidate_set_hash/ref
  )
)
```

Replay classification is explicit:

- changed rule/version with same entropy coordinate → `RULE_VERSION_DIVERGENCE`;
- changed candidate set with same entropy coordinate → `CANDIDATE_SET_DIVERGENCE`;
- changed root/scope/stream/draw coordinate or recomputed entropy → `RANDOM_DRAW_DIVERGENCE`.

These classes may co-occur; none silently overwrites another.

## 13. Recording obligations

### 13.1 Before first causal draw

Persist `RootSeedRecord`, causal-run identity, ADP-020 authority/version and seed/entropy algorithm versions.

### 13.2 First use of a named stream

Persist scope identity, `scope_seed_sha256`, static stream name, `stream_seed_sha256`, and the rule-registry reference that declares the stream/operation.

### 13.3 Every stochastic-capable decision

Persist `ADP020_DECISION_RECEIPT_V1`, including at minimum:

- authority/algorithm versions;
- root/scope/stream identities and seed digests;
- event anchor + rule invocation + decision slot + occurrence index;
- semantic rule ID/version/registry hash;
- operation and stochastic-parameters hash;
- candidate-set ref/hash when applicable;
- `draw_consumed`;
- draw-receipt IDs;
- selected result/candidate identity and candidate replay hash;
- result V3 event ID/index only after independent admission;
- `decision_replay_identity_hash`;
- causal-run identity.

### 13.4 Every entropy draw

Persist `ADP020_DRAW_RECEIPT_V1`:

`draw_index`, `entropy_block_count`, `uniform_below_n`, accepted raw entropy `u64`, mapped result, draw-coordinate hash and draw-replay hash.

Recording the accepted raw `u64` in addition to its derivation lets replay distinguish seed/KDF divergence from operation-mapping divergence.

### 13.5 Event and checkpoint linkage

If a causal event depended on RNG, the event/admission record links the exact `decision_receipt_id[]`, semantic rule ID/version, selected outcome/candidate identity and result event index.

Every checkpoint required for replay carries or resolves:

- causal event/history hash;
- cumulative RNG DecisionReceipt-ledger hash;
- root seed ID/hash;
- runtime rule-registry hash.

Records required by an admitted causal history are immutable/content-addressed for the lifetime of that replayable history.

## 14. Deterministic causal replay contract

For a completed causal history, replay inputs include the whole-machine inputs already bound by TD-R07 plus the exact ADP-020 tuple:

1. immutable V558 repository bundle identity and resolver policy/selection receipts;
2. initial V3 checkpoint/state;
3. runtime semantic-rule registry IDs/versions/hashes;
4. ADP-020 authority + seed/sampler versions;
5. exact root seed material/provenance;
6. scope/stream lineage;
7. candidate-set records;
8. stochastic-parameter records;
9. draw coordinates and Decision/Draw receipts;
10. admitted external events in exact causal order.

Replay MUST recompute each decision receipt and selected result, then reproduce the same admitted/generated V3 causal-event sequence and event/history/checkpoint hashes under the owning V3 rules.

Same lawful candidates + same root/scope/stream coordinates + same rule versions + same parameters + same ADP-020 versions = same causal stochastic choices.

No hidden wall clock, `latest`, filesystem order, network lookup, process/global RNG state, Python hash randomization, prompt output or model sampling may alter that result.

If a recorded algorithm version is unavailable, replay blocks. It does not reinterpret old receipts under a newer sampler.

If root seed material or required receipt/candidate metadata is incomplete, replay blocks. It does not “best-effort reseed” the same causal history.

## 15. LLM boundary

An LLM's internal sampling is **not ADP-020 RNG**.

A V3 Pass-1-like model may, under its separate authority, emit a non-authoritative proposal. If a later V3 rule considers such proposals, every proposal must first be exact/content-addressed, recorded, independently admitted as a lawful candidate, and included in `CandidateSetRecord`. Only then may ADP-020 select among those candidates if the semantic rule explicitly calls for stochastic selection.

If all model proposals fail admission, the candidate set is empty. There is no forced first candidate, fabricated fallback event or stochastic rescue.

Unrecorded stochastic model output never becomes causal truth.

## 16. Failure behavior

Failure is typed and occurs **before causal mutation** wherever possible.

| State | Meaning / required response |
|---|---|
| `RNG_AUTHORITY_MISSING` | ADP-020 binding unavailable → block stochastic mutation |
| `RNG_ROOT_SEED_MISSING` | exact root material/capability absent → block draw/replay; digest alone insufficient |
| `RNG_ROOT_SEED_INVALID` | wrong width/digest → integrity failure |
| `RNG_SCOPE_IDENTITY_MISSING` | no stable causal scope → block; RNG cannot invent scope |
| `RNG_STREAM_UNREGISTERED` | semantic rule did not declare exact stream/operation → block |
| `RNG_SEED_LINEAGE_INCOMPLETE` | root→scope→stream provenance incomplete → block |
| `RNG_SEMANTIC_RULE_IDENTITY_MISSING` | missing rule/version/registry identity → no draw |
| `RNG_OPERATION_NOT_AUTHORIZED` | operation not ADP-020 v1 or not permitted by semantic rule → no draw |
| `RNG_CANDIDATE_AUTHORITY_MISSING` | candidate lawfulness unproved → no draw; preserve owner state |
| `RNG_CANDIDATE_SET_EMPTY` | zero lawful candidates → zero draw; lawful-empty/blocked owner state; no fallback |
| `RNG_CANDIDATE_REPLAY_IDENTITY_INCOMPLETE` | exact candidate set cannot be replayed → block |
| `RNG_CANDIDATE_SET_HASH_MISMATCH` | canonical set does not match receipt → integrity failure |
| `RNG_STOCHASTIC_PARAMETERS_INVALID` | invalid weights/range/probability/sample → block, no coercive default |
| `RNG_DRAW_COORDINATE_INCOMPLETE` | replay coordinate incomplete → block |
| `RNG_DRAW_COORDINATE_REUSE_CONFLICT` | same coordinate, different replay identity → block |
| `RNG_ALGORITHM_VERSION_UNSUPPORTED` | recorded implementation unavailable → block replay |
| `RNG_DECISION_RECEIPT_MISSING` / `RNG_DRAW_RECEIPT_MISSING` | incomplete replay provenance → block |
| `RNG_REPLAY_MISMATCH` | recomputation differs → stop replay, never silently branch |
| `RNG_AMBIENT_SOURCE_FORBIDDEN` | unnamed/global/time-seeded/default RNG path → authority violation |
| `RNG_UNRECORDED_STOCHASTIC_LLM_FORBIDDEN` | hidden model sampling treated as causal truth → reject mutation |

A failure in RNG metadata is an integrity/authority failure, not a semantic event outcome.

## 17. Exact consumers

RA-R00 binds the direct implementation consumers:

- `V3-P2`
- `V3-P4`
- `V3-P5`
- `V3-P9`
- `V3-P10`
- `V3-P11`

ADP-020's exact obligations to them:

| Consumer | RNG authority supplied here |
|---|---|
| `V3-P2` | root/scope/named-stream law for any separately authorized stochastic actor/entity initialization; no random repair of absent initialization semantics |
| `V3-P4` | stable rule-invocation/decision coordinates for stochastic opportunities; scheduler precedence remains outside ADP-020 |
| `V3-P5` | persist/link Decision/Draw receipts into event admission, DevelopmentalEventLedger and checkpoints; RNG selection is not admission |
| `V3-P9` | actor/joint/genealogy/child stream isolation for separately authorized relationship/reproduction/child-generation stochastic choices |
| `V3-P10` | choose only among already-lawful attractor transition/interpretation candidates when their owner explicitly authorizes stochasticity; no V556-topology→type fallback |
| `V3-P11` | replay/completion court recomputes seed lineage, candidate-set hashes, decisions/draws and causal event/checkpoint hashes |

RA-R00 also records `ADP-007`, `ADP-009`, `ADP-010`, and `ADP-015` as later authorities that depend on MUST-020. This W0 cell does not consume their concurrent returns and does not predetermine their semantics.

## 18. Forbidden inference / fallback behavior

Explicitly forbidden:

- random choice from an ungoverned source list;
- first-candidate fallback after the lawful court returns none;
- arbitrary random event to avoid an empty year/candidate set;
- random default biography, personality, structural position or parent behavior;
- module-global `random.random/random.choice/random.choices` or equivalent for causal truth;
- `random.Random()` / equivalent with implicit seed;
- time/PID/Python-hash/filesystem-derived seed;
- V2 render RNG reused as V3 causal RNG;
- stochastic LLM completion used as generated fact without exact proposal/admission provenance;
- dummy entropy draws on deterministic paths;
- silent replay reseed or metadata repair;
- candidate canonical sorting used as a semantic priority/winner rule.

## 19. Hostile fixture court

The implementation/completion court for MUST-020 must include at least these fixtures:

| ID | Attack | Required result |
|---|---|---|
| H01 | repeat exact inputs | same entropy/result/receipt/event/checkpoint hashes |
| H02 | scramble candidate input/filesystem order | SET hash and result unchanged |
| H03 | add/remove candidate | candidate hash + replay identity change; classified separately from entropy |
| H04 | same candidate ID, changed payload hash/weight | candidate hash changes; old receipt invalid |
| H05 | change rule version only | raw entropy may stay same; replay reports rule-version divergence |
| H06 | one lawful candidate | deterministic result, `draw_consumed=false` |
| H07 | empty candidate set | no draw, no fabricated candidate/event |
| H08 | missing semantic rule/stochastic permission | no draw, typed authority failure |
| H09 | module-global/default RNG | forbidden path detected |
| H10 | actors A/B same root+stream name | isolated scope/stream seeds; B cannot perturb A |
| H11 | add/reorder sibling | existing child's stream unchanged |
| H12 | multi-actor joint scope | owner-supplied joint identity controls scope; runtime list order irrelevant |
| H13 | deterministic p/range/weight branch | no dummy draw |
| H14 | reuse draw coordinate with changed replay identity | conflict; no second causal result |
| H15 | replay with seed digest but no seed material | blocked, never reseeded |
| H16 | hidden stochastic LLM output | noncausal until exact recorded proposal + lawful admission/candidate status |
| H17 | legacy first-candidate/fabricated fallback | forbidden; lawful empty/degraded state |
| H18 | V2 rerender under different render RNG | V3 causal history/receipts unchanged |
| H19 | wall clock/`latest`/filesystem order enters coordinate | authority violation |
| H20 | tamper persisted draw/selection | `RNG_REPLAY_MISMATCH`, replay stops |

These fixtures specifically falsify the recovered defect shapes rather than merely testing a happy-path seed.

## 20. Consumer release sufficiency

`CONSUMER_RELEASE_SUFFICIENCY = SUFFICIENT`

Reason: ADP-020 now fully defines the bounded MUST-020 interface required by V3 consumers: root provenance, static stream namespace, deterministic stream derivation, finite allowed operation classes, candidate-set hashing, draw/event-coordinate semantics, exact rule/version replay identity, required persistence, failure behavior, actor/genealogy isolation and hostile replay proof.

This sufficiency is **local to MUST-020**. It does not mean V3-P2/P4/P5/P9/P10/P11 are independently executable before their other required semantic authorities and Vozhd release decisions exist.

## 21. Final authority statement

V3 may contain contingency without containing hidden arbitrariness.

A random draw is lawful only after another authority has already established what may happen. ADP-020 then gives that bounded contingency a stable causal identity: exact root, exact scope, exact named stream, exact rule, exact candidates or parameters, exact event/draw coordinate, exact sampler version, exact receipt, exact causal linkage. Missing law remains missing; an empty world stays empty until an authorized cause changes it.

The recovered V3's useful reproducibility intent survives. Its ambient RNG, pseudo-random semantic manufacture and fallback concretization do not.

`ADP_020_V3_CAUSAL_RANDOMNESS_AUTHORITY = PASS`
