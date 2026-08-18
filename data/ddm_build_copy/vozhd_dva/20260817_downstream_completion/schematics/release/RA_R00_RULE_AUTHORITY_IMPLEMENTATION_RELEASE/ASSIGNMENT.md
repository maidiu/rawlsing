# RA-R00 — Rule-Authority / Implementation-Release Synthesis

You are RA-R00 release-synthesis Rabochii for Vozhd Dva.

## 0. Mode

Post-architecture release planning and authority verification only.

Do **not** redesign closed architecture.
Do **not** modify production code.
Do **not** launch implementation workers.
Do **not** create new semantic families merely because current code is stale or an implementation packet needs a field.

The whole-machine architecture is CLOSED by:

`integration/WHOLE_MACHINE_ARCHITECTURE_CLOSURE_RULING.md`.

Your task is to turn the closed architecture into a finite, dependency-ordered program of governed authority decisions and implementation packets.

## 1. Governing authority

Read in order:

1. `state/CURRENT_STATE.md`
2. `integration/WHOLE_MACHINE_ARCHITECTURE_CLOSURE_RULING.md`
3. `integration/SEAM_INTEGRITY_CLOSURE_RULING.md`
4. `integration/V3_COMPLETION_IMPLEMENTATION_RULING.md`
5. `integration/V2_COMPLETION_IMPLEMENTATION_RULING.md`
6. `TERMINAL_DEMAND_ENVELOPE.md`
7. `ARCHITECTURE_PASS_LAW.md`
8. `schematics/synthesis/RUNTIME_PRIOR_RESOLUTION_EXPLORATION.md`
9. accepted TD-R00–TD-R07 `RESULT.md` / `RESULT.json`
10. current implementation, schemas, registries, tests and governance artifacts relevant to every named blocker.

Binding law:

**Continuity is desired. V550+-grounded Rawlsing vision-integrity is absolute.**

Architecture closure means implementation inconvenience is not an architecture-reopening argument.

## 2. Required historical downstream evidence

Attach and directly inspect:

`Rawlsing_code_bundle_staging.zip`

Expected SHA256:

`953c9149bd03877206e3cb440d1f4db35dea6473af30b97fd23b7e76c6fc0086`

Use the archive only to determine whether a V3/V2 rule, policy, invariant, mechanism, or validation contract already exists strongly enough to reuse/canonicalize.

Its V5/DDM material is stale and has zero authority over current V550+.

Do not repeat TD-R05/TD-R06 architecture disposition courts.

## 3. Core question

For every blocker named anywhere in accepted TD-R00–TD-R07 results/rulings/seam hardenings, determine:

1. What exact semantic or implementation capability is blocked?
2. Which stage owns the authority?
3. Does authoritative material already exist?
4. If it exists, is it already canonical or does it need binding/versioning/normalization?
5. If it does not exist, what finite governed decision must be made before implementation?
6. Which implementation packet(s) depend on it?
7. Which acceptance harness proves closure?
8. What can run in parallel and what is serially blocked?

## 4. Mandatory blocker classification

Assign every blocker exactly one primary class:

### `AUTHORITY_ALREADY_EXISTS`
The required semantic authority already exists in governed source/registry/spec/rule form and can be consumed directly without new semantic decision.

You must cite exact repo/archive evidence and explain why it is sufficient.

### `AUTHORITY_NEEDS_CANONICALIZATION`
Substantive rule authority exists, but terminal implementation needs a canonical schema, registry entry, version binding, naming normalization, evaluator binding, permission declaration, or machine-readable contract.

No new meaning may be introduced during canonicalization.

### `AUTHORITY_MUST_BE_CREATED`
The terminal need is real and accepted architecture assigns an owner, but no sufficient governed rule exists. State the exact bounded decision needed. Do not solve the substantive rule unless the assignment explicitly authorizes that later.

### `IMPLEMENTATION_ONLY_NO_NEW_AUTHORITY`
Semantic authority is already sufficient; remaining work is code/schema/migration/harness implementation only.

### `EXTERNAL_PRODUCTION_GATE`
The blocker is outside the semantic implementation packet itself, e.g. SWID G8/final merge, required upstream physical publication, environment/runtime database acceptance.

Do not use `AUTHORITY_MUST_BE_CREATED` as a dumping ground for stale code.

## 5. Required authority universe

Construct the union of every named authority/registry/contract/blocker from at least:

### V553
- final source/wave identity basis and narrow identity-delta check;
- V553 completion/build gates and any rule/registry authority required by accepted TD-R00 / SI-R00.

### V554
- `V554_AFFORDANCE_RULE_REGISTRY`;
- exact V553 physical reference bindings;
- any applicability/evaluator authority required by F2 and seam hardening.

### V555
- `V555_MEDIATION_ROUTE_RULE_REGISTRY`;
- `V555_ROUTE_PREDICATE_REGISTRY`;
- exact one-affordance-per-route and inherited-F2 reference law.

### V556
- interaction-rule authority/registry;
- attractor-prerequisite rule authority/registry;
- predicate/evaluator bindings;
- any numeric formula authority if numeric semantics remain desired;
- `V556_ATTRACTOR_PREREQUISITE_SATISFACTION_RULE` as V3-facing shared authority where applicable.

### V557/V558
- runtime publication/use governance authority;
- temporal proxy eligibility authority, separately versioned from runtime-use authority;
- immutable bundle/publication policy;
- resolver predicate/evaluator bindings;
- generated-position binding contract;
- transitive semantic-closure validation;
- refresh policy / next-context-change contract;
- repository/link/index implementation blockers that require no new semantics.

### V3
Every missing/partial authority in `V3_COMPLETION_IMPLEMENTATION_RULING.md`, including at minimum:
- actor initialization;
- developmental phase;
- position generation/transition/mobility;
- encounter/exposure/route realization;
- V556 F1 realization;
- V556 F2 prerequisite satisfaction;
- actor response/metabolization;
- orientation;
- material/organismic/vitality/needs/expectations/striving/framework/buffer/wound/practice update rules;
- relationships/households/genealogy;
- rupture/metabolization/memory;
- attractor update/interpretation;
- external-event admission;
- LLM proposal admission if retained;
- randomness;
- scheduler;
- derived-state schedule.

### V2 / V3→V2 seam
All 19 authorities from `V2_COMPLETION_IMPLEMENTATION_RULING.md`:
- `V3_ACTOR_KNOWLEDGE_ACCESSIBILITY_RULE`;
- `V3_CAUSAL_MEMORY_FORMATION_FORGETTING_RECALL_RULE`;
- `V3_EXTERNAL_INTERACTION_EVENT_ADMISSION_RULE`;
- `V2_PHENOMENOLOGICAL_PROJECTION_RULE`;
- `V2_SALIENCE_ACCESSIBILITY_RULE`;
- `V2_EXPRESSION_REGISTER_RULE`;
- `V2_RESPONSE_MOVE_RULE`;
- `V2_RELATIONSHIP_EXPRESSION_RULE`;
- `V2_UNCERTAINTY_DISCLOSURE_RULE`;
- `V2_BOUNDARY_FACE_RISK_EFFORT_ATTENTION_RULE`;
- `V2_ATTRACTOR_EXPRESSION_RULE`;
- `V2_SESSION_ENERGETIC_FIELD_RULE`;
- `V2_TRANSCRIPT_RETENTION_SUMMARIZATION_POLICY`;
- `V2_RENDER_ADMISSION_PROMPT_CONTRACT`;
- `V2_RENDER_MODEL_RANDOMNESS_VERSION_POLICY`;
- `V2_NATIVE_TRANSLATION_EQUIVALENCE_RULE`;
- `V2_INTERACTION_MODE_POLICY`;
- `V2_TO_V3_EXTERNAL_EVENT_PACKAGING_CONTRACT`;
- `CALLER_CURRENT_SITUATION_AUTHORITY`.

This list is a floor, not permission to invent more blockers. Add an item only if an accepted ruling/result or direct implementation inspection proves it is materially required.

## 6. De-duplication law

Many named blockers may be different references to one shared authority.

For each apparent duplicate, determine whether it is:
- same semantic authority with multiple consumers;
- shared physical registry with logically separate namespaces/versions;
- separate semantic authority that merely uses similar vocabulary;
- implementation adapter only.

Do not merge authorities merely to reduce count.

In particular preserve accepted separation between:
- runtime-use governance and temporal-proxy eligibility;
- V556 F2 topology authority and V3 F2-satisfaction authority;
- V3 causal memory/accessibility and V2 expression/memory presentation;
- V3 external-event admission and V2 external-event packaging;
- causal scheduler and derived/render scheduling;
- structural predicates and generated-runtime facts.

## 7. Direct authority-recovery court

Search actual current repo/source and the attached historical V3/V2 archive before classifying anything `AUTHORITY_MUST_BE_CREATED`.

For each authority:

`required terminal meaning`
→ `candidate existing authority`
→ `exact evidence path/function/registry/spec`
→ `semantic coverage`
→ `gaps`
→ `classification`.

A useful legacy mechanism may be classified `AUTHORITY_NEEDS_CANONICALIZATION` even when its current implementation shape is obsolete, provided the rule meaning itself is compatible and lossless.

## 8. Implementation packet normalization

Collect all accepted implementation packets from TD-R00–TD-R06 and seam rulings.

Normalize them into one finite packet ledger.

For every packet include:
- packet ID;
- stage/write domain;
- exact canonical architecture obligation;
- present implementation delta;
- blocker authority IDs;
- upstream packet dependencies;
- parallel-safe dependencies;
- required fixtures/migrations;
- acceptance tests/harnesses;
- explicit forbidden regressions;
- production gate, if any.

Do not redesign packets into monoliths merely for convenience.

## 9. Release DAG and waves

Produce a dependency DAG and finite worker-wave plan.

At minimum distinguish:

- **external gate lane:** SWID G8/final merge/narrow identity delta;
- **structural implementation lane:** V553→V558;
- **runtime authority lane:** V3 rules/contracts;
- **V2 boundary/expression authority lane:** actor accessibility + V2 rules;
- **cross-cutting harness lane:** replay, fail-closed, seam, synthetic-life acceptance.

Identify what can proceed before SWID closes and what must wait for exact V553 physical publication.

Do not serialize work that is genuinely independent.

Do not parallelize two workers that would define the same semantic authority independently.

## 10. Authority decision packets

For every `AUTHORITY_MUST_BE_CREATED`, create a finite future decision packet specification containing:
- authority ID;
- owner;
- exact question to decide;
- accepted architecture constraints;
- allowed evidence sources;
- forbidden shortcuts;
- consumers;
- acceptance conditions;
- whether the decision can run independently or requires earlier authority decisions.

Do **not** decide the substantive rule in RA-R00 unless an already-governed source makes the answer direct and non-discretionary.

## 11. Release safety checks

Prove the release map cannot reintroduce:
- structural prior→actor belief/personality;
- route possibility→experience;
- proxy→lived history;
- geography→identity;
- V556 F2→type;
- V2 causal mutation;
- rendered/session state→V3 truth without admission;
- analyst omniscience;
- generic missing-data defaults;
- duplicate V556 base edge;
- V557/V558 semantic reownership;
- heuristic substitution for missing rule authority.

## 12. Required output

Write only:

`data/ddm_build_copy/vozhd_dva/20260817_downstream_completion/schematics/release/RA_R00_RULE_AUTHORITY_IMPLEMENTATION_RELEASE/RESULT.md`

`data/ddm_build_copy/vozhd_dva/20260817_downstream_completion/schematics/release/RA_R00_RULE_AUTHORITY_IMPLEMENTATION_RELEASE/RESULT.json`

Do not modify production code or accepted architecture/rulings/state/itinerary.

## 13. Required RESULT sections

Include machine-consistent versions of:

1. executive release-synthesis verdict;
2. complete authority/blocker inventory;
3. source-evidence verification including archive SHA;
4. exact de-duplication map;
5. classification counts by blocker class;
6. authority-already-exists evidence table;
7. authority-needs-canonicalization table;
8. authority-must-be-created decision-packet table;
9. implementation-only blockers;
10. external production gates;
11. normalized implementation packet ledger;
12. blocker→packet dependency matrix;
13. release DAG;
14. parallel worker-wave plan;
15. SWID/V553 gating interaction;
16. V3/V2 shared-authority interaction;
17. acceptance-harness plan;
18. forbidden-regression matrix;
19. finite first execution wave recommendation;
20. unresolved evidence gaps, if any;
21. final release statement;
22. final token.

## 14. Final token

Return exactly one:

`IMPLEMENTATION_RELEASE_SYNTHESIS = PASS | BLOCKED`

`PASS` means the closed architecture has been reduced to a finite, non-overlapping, dependency-ordered authority/implementation program with every blocker classified and no semantic work silently delegated to implementation workers.

`BLOCKED` means specific required evidence is unavailable or the blocker universe cannot yet be classified without reopening forbidden assumptions. Name the exact missing evidence; do not improvise.
