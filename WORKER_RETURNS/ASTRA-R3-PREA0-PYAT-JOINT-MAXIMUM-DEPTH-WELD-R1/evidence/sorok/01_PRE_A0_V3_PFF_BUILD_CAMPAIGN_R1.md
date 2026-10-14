# PRE-A0 V3 / PFF BUILD CAMPAIGN R1

**Project:** Rawlsing / Sorok  
**Status:** WORKING EXECUTION CAMPAIGN — PRE-A0  
**Parent architectural bank:** `00_PRE_A0_ARCHITECTURAL_BANK_R1.md`  
**Branch:** `agent/sorok-prea0-psyche-architecture-r1`

---

## 0. Decision

### Can downstream V3/PFF design and engineering proceed before PRE-V3 and the PRE-V3/V3 seam are complete?

**YES, WITH A HARD BOUNDARY.**

Current Pyat law intentionally defers physical PRE-V3→V3 seam implementation until the sociological/objective PRE-V3 world is mature. At the same time, accepted Dva/Pyat inheritance already fixes enough of the **consumer-side contract and jurisdiction** to permit substantial downstream design and implementation without inventing upstream semantics.

Therefore:

> **BUILD V3/PFF INTERNALS NOW AGAINST A VERSIONED ABSTRACT STRUCTURAL-CONTEXT PORT.**
>
> **DO NOT FREEZE OR IMPLEMENT THE FINAL PRE-V3→V3 WELD YET.**

The downstream system must be architected so the eventual PRE-V3 seam is an adapter/integration problem rather than a rewrite of personhood.

---

## 1. What is already stable enough to build against

The inherited architecture fixes these downstream laws strongly enough for engineering:

1. PRE-V3 is actor-independent sociological / structural / temporal / consequence world production.
2. V3 receives a **stage-blind resolved structural context**, not raw source stages.
3. Structural prior/context is **not actor fact, experience, belief, memory, wound, personality or biography**.
4. V3 alone owns:
   - actor initialization under explicit authority;
   - generated position and movement;
   - encounter/exposure realization;
   - mediation-route realization;
   - actor response/metabolism;
   - organismic/developmental state;
   - relationship/household/genealogy;
   - causal memory/forgetting;
   - rupture/metabolization;
   - personal relational field;
   - attractor development;
   - generated lived history.
5. Context must preserve exact object identity, provenance, temporal applicability, uncertainty/negative/valid-empty states, and referential closure.
6. Generated V3 bindings may trigger context re-resolution but may not be laundered upstream into structural authorship.
7. The structural-world interface must preserve n-ary relations/topologies rather than flattening them into scalar pressure.
8. Missing/unknown/deferred/noncomparable remain lawful and cannot be filled by V3 convenience defaults.
9. V3 must adapt to upstream richness; PRE-V3 must not be compressed merely to satisfy historical V3 schemas.
10. Historical V553–V558 names are function/jurisdiction genealogy, not mandatory current physical nodes.

These are sufficient for a downstream **consumer contract**.

---

## 2. What is NOT stable enough to freeze

Do not yet freeze:

- exact physical PRE-V3 object filenames/modules;
- historical V558 as mandatory current seam implementation;
- exact final terminal PRE-V3 serving schema;
- exact field names/cardinalities of current Pyat products;
- direct mappings from any current structural object to psychic variables;
- numeric pressure/desire/wound mappings from upstream;
- actor initialization distributions not separately governed;
- final structural context query/resolver implementation owned upstream;
- exact provenance envelope implementation details still subject to Pyat completion;
- full seam acceptance / integration tests against the not-yet-finished PRE-V3 estate.

These belong to the future weld.

---

## 3. Anti-fantasy seam rule

The downstream campaign SHALL define only what V3 **needs from a structural-world provider**, not claim that Pyat already produces each field in final form.

Use a versioned abstract port such as:

```text
StructuralWorldPort
    resolve_context(query) -> ResolvedWorldContext

ResolvedWorldContext
    context_id
    effective_time
    subject/location/position binding refs
    structural_object_refs[]
    relation/topology refs[]
    mediation/route refs[]
    temporal applicability refs[]
    consequence/affordance refs[]
    power/recognition-condition refs[]   # only where upstream lawfully owns them
    uncertainty/negative/deferred states[]
    provenance/authority refs[]
    refresh/invalidation metadata
```

This is a **consumer requirement envelope**, not an upstream semantic declaration.

Fixtures may instantiate this port synthetically for engineering.

Every synthetic field must be labeled:
`LABORATORY_STRUCTURAL_FIXTURE__NOT_PREV3_OUTPUT`.

---

## 4. Campaign objective

Build the successor V3/PFF person engine far enough that when Pyat's terminal PRE-V3 service is ready:

1. the actual structural-world service is mapped into `StructuralWorldPort`;
2. seam tests prove zero-loss / no semantic theft;
3. V3 consumes real generated contexts without redesigning its psychic ontology;
4. mismatches are routed to the correct side:
   - missing lawful upstream meaning -> PRE-V3/seam issue;
   - bad adapter/mapping -> seam implementation issue;
   - V3 inability to preserve a lawful upstream distinction -> V3 design defect;
   - desire for an upstream psyche fact -> forbidden downstream theft.

---

# 5. Execution campaign

## C0 — Consumer contract freeze and seam firewall

**Purpose:** Freeze what V3 may ask of upstream without freezing how Pyat physically supplies it.

Deliver:
- `StructuralWorldPort`;
- `ResolvedWorldContext` abstract contract;
- provenance/uncertainty/noncollapse law;
- generated-binding re-resolution contract;
- synthetic-fixture labeling law;
- adapter boundary;
- hostile cases proving no structure->psyche shortcut.

Acceptance:
- V3 core can compile against the port without importing historical V553–V558 modules.
- No field in the port is itself a personality/wound/belief/memory fact.

## C1 — Conative–Relational Substrate

Implement the pre-conscious impulse substrate:

```text
BODY/WORLD/RELATION/HISTORY
-> regulatory discrepancies
-> conative tendencies
-> relational expectations
-> recognition observations/errors
-> power-conditioned affordances/costs
-> desire conflict/blockage pressure
-> historically conditioned routing
-> active flow
```

Objects include:
- regulatory state;
- conative tendency;
- power relation;
- recognition observation / conflict;
- route state;
- event-local conative field;
- actor-accessible projection.

Do not yet require real PRE-V3 input. Use lawful structural fixtures via C0.

## C2 — Psychic Matrix / Personal Relational Field

Implement:
- typed temporal multigraph;
- node genealogy;
- intrapsychic relation modes;
- higher-order motifs;
- compartment/subsystem support;
- path dependence;
- historical relation updates;
- internalized norm -> self-policing -> external policing;
- social-category mediation;
- identification/alienation dynamics.

Acceptance:
- same node inventory + different topology yields different person behavior.
- no global trait/type shortcut.

## C3 — Developmental Recursion and Lived-Artifact System

Implement the developmental-instance triad:

```text
canonical causal transition
+
LLM lived artifact
+
psychic afterlife / memory / accessibility / causal traces / interpretation lineage
```

Implement:
- immutable event ledger;
- checkpoints;
- causal ancestry;
- developmental interpretation lineage;
- memory vs accessibility vs trace;
- recurrence/contrast;
- reactivation and counter-history;
- historical ablation;
- LLM Call A proposal -> admission -> LLM Call B lived instance.

Acceptance uses hostile trajectories H-P1/H-P3/H-P4.

## C4 — Recursive Relationship Field

Implement directed/asymmetric fields for:
- parent A <-> parent B;
- each parent <-> child;
- important siblings/friends/partners/rivals as promoted actors;
- later focal actor <-> user.

Represent separately:
- objective shared history;
- A->B orientation;
- B->A orientation;
- actor models;
- metaperception;
- power;
- recognition authority;
- category construal;
- memories/traces;
- motifs.

Acceptance:
- child development changes when co-parent relation changes even if each parent-child dyad's simple labels are held constant.
- same event from different important people recruits different organization.

## C5 — Attractor / Enneagram Shadow-Gravity

Implement the causal object as a type-agnostic motivational attractor over psychic topology.

```text
personal relational field
-> recurrent motifs
-> attractor state
-> downward organizational bias
-> future topology
```

Optional:
`EnneagramAffinityInterpretation` as versioned uncertain projection only.

Acceptance:
- no type at birth;
- no type label creates psyche;
- attractor can weaken, split, transition, or remain unresolved;
- similar surface style can arise from different attractor lineage.

## C6 — Life-Epochal Scheduler / Recursive Generated Social World

Implement bounded life development:
- generated parents first;
- co-parent relationship recursion;
- child recursion;
- school/friend/mentor/partner promotion rules;
- phase/context changes;
- slow and discrete events;
- bounded material/organismic development;
- structural-context re-resolution through C0 port;
- world breadth bounded without flattening focal relations.

This is the **life-epochal V3**.

## C7 — Live-Time PFF / CAN-008 Successor

Implement live present-event metabolism using the same person substrate:

```text
user/world event
-> semantic event admission
-> whole-person retrieval
-> conative/relational field
-> PFF recruitment
-> actor-accessible projection
-> renderer
-> occurrence admission
-> durable consequences
-> next person state
```

The live engine must not be a separate personality simulator.

It is a finer-grain continuation of the same generated organism.

Acceptance:
- age-seven residue can shape live response without conscious recall;
- live interaction can modify later life state;
- user relation becomes one genuine generated relationship among others.

## C8 — Phenomenal / Surface Projection

Implement the rich learned phenomenal lens:
- observable reality;
- user access/attention;
- prior familiarity;
- recognition competence;
- selective description;
- no hidden-cause leakage;
- no causal mutation.

Keep replaceable so model-assisted phenomenal rendering can be added if local compositor is insufficient.

## C9 — Reference Whole Nadia Vertical Court

Use a complete synthetic upstream fixture and run:
- generated parents;
- parent relationship;
- childhood development;
- multiple recursive epochs;
- adolescent/adult relations;
- attractor development;
- inaccessible trace;
- social-category identification/alienation;
- recognition conflicts;
- adult live user interaction.

This is laboratory proof of the downstream engine, **not proof of PRE-V3 integration**.

## C10 — PRE-V3 Weld Readiness

Do not execute until Pyat declares terminal PRE-V3 serving sufficiently mature.

Prepare:
- field-by-field consumer needs;
- synthetic-fixture provenance;
- exact dependencies;
- zero-loss acceptance cases;
- anticipated adapter transformations;
- forbidden inference matrix.

No assumption that old V558 physical shape is final.

## C11 — Actual PRE-V3 -> V3 Weld

When Pyat is ready:

```text
CURRENT TERMINAL PRE-V3 SERVICE
        ↓
thin versioned adapter
        ↓
StructuralWorldPort
        ↓
V3/PFF successor runtime
```

Court every mapping:
- exact semantic owner;
- upstream evidence/provenance;
- allowed causal use;
- temporal applicability;
- missing/negative state;
- no actor fact laundering;
- no loss of n-ary/relational meaning.

Prefer changing adapter/V3 consumer over flattening upstream.

Reopen upstream only if a genuine terminal consumer starvation is proved.

## C12 — End-to-End Generated-Person Court

Replace all synthetic structural fixtures with real PRE-V3 output.

Success requires:
- pipeline-produced parents/focal actor;
- real upstream structural context;
- epochal recursion;
- generated lived artifacts;
- live PFF interaction;
- relationship/history reentry;
- actor opacity;
- replay/provenance;
- no unsupported structure->psyche leap.

This is the gate into A0/A1.

---

## 6. Parallelism with Pyat

Sorok/Psyche and Pyat should progress in parallel with **sync gates**, not serial waiting.

### Pyat continues:
- source -> empirical -> learned-world;
- Field Forge;
- objective structural/temporal/consequence world;
- terminal PRE-V3 service;
- productive adequacy / all-wave occupancy.

### Sorok/V3-PFF continues:
- person ontology;
- conative/relational substrate;
- developmental recursion;
- relationships;
- attractors;
- memory/access/trace;
- live PFF;
- renderer/phenomenal machinery.

### Sync gates

**SYNC-1 — after C0:** compare abstract consumer demand to current Pyat downstream constraints.

**SYNC-2 — after C3/C4:** expose exact structural-context demands discovered by real psyche engineering; do not demand psyche upstream.

**SYNC-3 — after C6/C7:** provide temporal refresh, position-binding, power/relationship/world demands revealed by epochal + live runtime.

**SYNC-4 — when Pyat terminal service matures:** freeze actual seam and execute C10/C11.

Thus downstream engineering can reveal legitimate terminal consumer requirements early without hijacking Pyat's sociological jurisdiction.

---

## 7. Critical discipline

### Build now
- schemas/data structures internal to V3/PFF;
- state transition engines;
- event ledger/replay;
- conative-relational calculations;
- relationship field;
- psychic multigraph;
- memory/access/trace;
- LLM proposal/admission contracts;
- developmental scheduler;
- live PFF;
- renderer/phenomenal boundaries;
- synthetic fixtures;
- hostile tests.

### Do not build as final yet
- direct Pyat module imports;
- fixed legacy V558 adapter;
- final PRE-V3 structural object mapping;
- ungoverned numeric translation from sociology to psyche;
- production end-to-end seam;
- real-source claims for laboratory fixtures.

---

## 8. Final integration doctrine

The eventual task is **not**:

> "bolt completed PRE-V3 onto old V3."

It is:

> **weld the completed terminal PRE-V3 structural-world service to the successor V3/PFF consumer contract, preserving upstream meaning and downstream personhood.**

The seam should be thin.

If the weld requires rewriting the psychic core, C0 failed.

If the weld requires PRE-V3 to emit wounds, desires, memories or personality, downstream jurisdiction failed.

If the weld cannot represent a lawful structural distinction without flattening it, the V3 consumer contract failed and must adapt.

---

## 9. Current answer in one line

> **We know enough about what Pyat is building toward to engineer the successor person-machine now, provided we build against its stable jurisdictional/semantic envelope rather than its unfinished physical output. The exact PRE-V3→V3 adapter/weld waits for Pyat's terminal service; the psyche does not.**
