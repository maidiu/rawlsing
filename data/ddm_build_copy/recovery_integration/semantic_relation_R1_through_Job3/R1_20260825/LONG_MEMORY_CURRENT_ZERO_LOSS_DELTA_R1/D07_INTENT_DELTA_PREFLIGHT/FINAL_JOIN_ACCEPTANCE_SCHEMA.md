# D07 — ADVERSARIAL ZERO-LOSS FINAL JOIN ACCEPTANCE SCHEMA R1

Status: `PREFLIGHT_SCHEMA_FROZEN__NO_CURRENT_ZERO_LOSS_VERDICT`

This schema is for the Authority-39 HQ join after all seven delta lanes and any separately adopted fracture-map work are available. It is deliberately stricter than structural or documentary presence.

## 1. Governing baseline

The row universe begins with the exact 44 inherited obligations from:

- Long Memory terminal commit `669062e6c319f31214f403939dded91300639bde`;
- `RAWLSING_LONG_MEMORY/08_FINAL_WHOLE_HISTORY_DIFFERENCE_SET.csv` blob `0ae29caa6b3c572b2cedf39bebfa737668ebfb5b`;
- Authority 39 blob `9cc69780e8ece14884989ef3482dc051ecd0ec47`.

Post-freeze vocabulary does not create another baseline row unless HQ proves a semantic/function-grain obligation not already contained by those 44.

D07 finds zero such new obligations. The fracture-map grammar is a set of refinements and stronger parity witnesses over inherited obligations, not a second archaeology corpus.

## 2. Atomic join row

HQ SHOULD normalize every inherited obligation and every genuinely new obligation, if any later worker proves one, into one atomic join row with these mandatory fields:

| field | requirement |
|---|---|
| `obligation_id` | Exact `LMX-*` or exact accepted post-freeze new-obligation id. |
| `baseline_requirement` | Verbatim or lossless normalized inherited function/negative law. |
| `baseline_exact_ref` | Exact Long Memory artifact + commit/blob. |
| `post_freeze_delta_ids` | All D07 delta rows that strengthen/restated this obligation, or explicit `NONE`. |
| `current_authority_ref` | Exact current adopted authority governing the function. Old-branch or merely proposed authority is not sufficient. |
| `current_machine_element` | Exact current implementation file/object/public interface or explicit typed absence. |
| `current_test_or_receipt` | Exact executable test/receipt proving same-or-stronger behavior, or explicit typed absence. |
| `semantic_parity_claim` | Exact statement of what is proved equivalent/stronger. |
| `coverage_frontier` | Exact source/universe/routing/question/branch/arity/jurisdiction frontier to which the proof applies. |
| `destructive_replay_ref` | Exact delete/rebuild/reopen/replay evidence where the function depends on persistence/derivability/lineage. |
| `operational_workflow_ref` | Evidence that the actual current workflow consumes/produces the function, not merely that a unit can be invoked. |
| `authority_role_path` | Producer semantic role -> carrier/ref -> consumer semantic role, including fail-closed role mismatch test where applicable. |
| `negative_ceiling` | What the function must not infer, widen, pool, flatten, or promote. |
| `adoption_currentness_ref` | Exact evidence the implementation/test is on the current adopted lineage. |
| `open_gap_kind` | `NONE`, `FUNCTIONAL`, `PROOF`, or exact outside-PRE-V3 owner. |
| `current_disposition` | Exactly one Authority-39 terminal disposition. |

Blank is never equivalent to `NONE`, `NOT_REQUIRED`, `OUTSIDE_JURISDICTION`, or `UNRESOLVED`.

## 3. Required terminal dispositions

Authority 39 permits exactly:

1. `CURRENTLY_PROVED`
2. `CURRENTLY_PROVED_BY_STRONGER_SUPERSESSION`
3. `CURRENTLY_OPEN_FUNCTIONAL_GAP`
4. `CURRENTLY_OPEN_PROOF_GAP`
5. `OUTSIDE_CURRENT_PREV3_JURISDICTION__EXACT_OWNER_IDENTIFIED`
6. `FORMALLY_RETIRED__NO_VALUABLE_FUNCTION_LOST`

D07 adds no seventh positive-looking convenience state.

## 4. Positive-closure gates

A row may be `CURRENTLY_PROVED` only if every applicable gate below passes.

### G0 — baseline identity and jurisdiction

- Exact inherited obligation is identified.
- Exact frontier/jurisdiction is declared.
- No narrower canary or source scope is silently reported as global closure.

Failure -> `CURRENTLY_OPEN_PROOF_GAP` unless the function itself is absent.

### G1 — post-freeze intent delta crosswalk

- Every D07 strengthening touching the row is explicitly consumed.
- New wording is deduplicated against inherited function grain.
- If HQ later claims a genuinely new obligation, it must prove non-equivalence to all 44 before appending it.

Failure -> `CURRENTLY_OPEN_PROOF_GAP`.

### G2 — current adopted authority

- Exact current semantic/function owner exists.
- Authority is on the current adopted lineage or explicitly adopted by current HQ.
- Proposed, historical, worker-local, or still-running authority is not current.

Absence of an owner required in PRE-V3 -> `CURRENTLY_OPEN_FUNCTIONAL_GAP`.

### G3 — current implementation

- Exact executable implementation exists for the claimed function.
- `SCHEMA_CAN_HOLD_IT` and `FIELD_PRESENT` do not pass this gate.
- Representability without autonomous generation fails autonomous-discovery obligations.

Missing implementation -> `CURRENTLY_OPEN_FUNCTIONAL_GAP`.

### G4 — executable same-or-stronger parity

- Exact current test/receipt exists.
- Test attacks the function at its constitutive grain, not an easier proxy.
- No shared-oracle bug, known-answer leakage, favorable runner, or current-query-only shortcut substitutes for independent acceptance.
- Canary scope is explicit and cannot upgrade to product-wide parity.

Implementation with missing/insufficient proof -> `CURRENTLY_OPEN_PROOF_GAP`.

### G5 — information and authority-role conservation

Where applicable, prove:

- source/respondent/question identity;
- same-respondent joins;
- component identity/order/roles;
- exact denominator/risk/routing context;
- weight/design authority separately from raw support;
- typed negative states;
- producer semantic role -> carrier/reference -> consumer semantic role;
- reverse explanation/invalidation lineage.

A byte-identical field with a changed semantic role fails.

### G6 — destructive replay / rebake / relayout

This gate is independent of G3/G4. For LMX-023/026/042/043 and any row whose claimed conservation relies on derivability or operational persistence, HQ must require a destructive path appropriate to the object:

1. seal exact canonical inputs/authority;
2. delete nonauthoritative caches, derived materializations and reopenable learned products under test;
3. start a fresh process without chat memory/private worker state;
4. reconstruct from canonical determinants;
5. compare exact semantic identity or positively defined information-equivalent identity;
6. re-run affected query/discovery/consumer behavior;
7. prove stale outputs are rejected after source/authority invalidation;
8. test interruption/restart at publication or promotion boundary where atomicity is claimed;
9. where layout/migration changes, prove ancestry, multiplicity, authority roles, reverse lineage and consumer behavior survive.

A replay pointer, restart command or successful warm-cache run does not pass G6.

### G7 — operational workflow coverage

- The normal governed current workflow actually reaches the implementation.
- Required producer -> controller -> frontier -> fact/joint -> closure -> consumer choreography is executable without manual splice.
- No step depends on copying IDs/results from a worker report or reconstructing private objects outside public contracts.
- Source/product coverage is stated exactly.

A library, helper, unit test or branch-local module never used by the current workflow fails this gate.

### G8 — negative ceiling and jurisdiction firewall

The positive function must preserve all applicable prohibitions, including:

- empirical coordinate != structural position != actor fact != actor belief/personality;
- semantic equivalence != response portability/joint authority;
- no implicit pooling/noncomparability widening;
- typed negative != false/zero;
- stop recursion != delete branch;
- pairwise association != higher-order joint topology;
- descriptive rank != semantic winner;
- transport/carrier != semantic authority.

Violation is a functional failure, not merely a documentation defect.

### G9 — no-starvation / retirement proof

- Historical/current consumer absence cannot retire a function.
- A physical stage/courier may disappear only if every valuable terminal function has a positively proved successor.
- `FORMALLY_RETIRED__NO_VALUABLE_FUNCTION_LOST` requires explicit retirement authority plus positive supersession evidence.

## 5. Fracture-map-specific strengthening gates

These do not create new baseline obligations; they make inherited discovery/joint/replay rows harder to falsely close.

### F1 — autonomous root-to-frontier generation

Start only from the governed substantive response surface plus ordinary source/coordinate/target authority. Do not seed known winning branch predicates, pair combinations, triples, expected metrics, or oracle rankings.

### F2 — exact multi-label morphology

Prove both source-governed response-presence branches and exact response-pattern morphology. Single-label projection or option marginals alone are insufficient.

### F3 — branch retention independent of continuation

Every supported branch remains addressable with exact distribution, ancestry, replay and typed stop reason even if recursion is not eligible to continue.

### F4 — discovered-child transport

Generation N+1 must consume the actual discovered child ref/public replay surface from generation N. No caller reconstruction of member IDs or private in-memory candidate is accepted.

### F5 — autonomous substantive target enumeration

For each retained supported branch, enumerate the authority-bounded substantive target catalog without relevance leakage. Demographic/positional coordinates remain conditioners and are excluded from attitude/co-signature target ontology.

### F6 — direct same-respondent J=3

For Authority-37 parity workloads, execute direct J=3 same-respondent joints. Prove that a pairwise-margin-equivalent reconstruction is rejected as non-equivalent whenever the direct tensor differs.

### F7 — denominator/weight/state separation

Branch total, per-node eligible denominator, pair denominator and J=3 joint denominator remain separate. Raw support and governed weighted support remain parallel. DK/refusal/missing/not-asked/inapplicable remain typed according to source authority.

### F8 — invocation-boundary adaptation

Result-driven frontier generation may occur only between completed I05 invocations. Within one invocation the frontier is predeclared/hash-sealed and every candidate is evaluated.

### F9 — ref-only closure without truth reownership

A fracture-map aggregate may close over exact refs, but copied payload cannot become a new empirical warehouse or semantic authority. Delete/rebuild must reproduce the closure from canonical owners.

### F10 — PRE-V3 noninference

No branch/co-signature/topology result directly emits actor belief, personality, psyche, biography, causation or ideology.

## 6. Destructive-replay result matrix

HQ should record destructive proof separately from ordinary parity using at least:

| destructive case | required result |
|---|---|
| cache/index deletion | identical semantic frontier/results or exact approved information-equivalence |
| learned aggregate deletion | complete regeneration from canonical refs/determinants |
| fresh-process replay | no dependency on private object memory or chat context |
| source/authority mutation | stale descendant rejection + deterministic recomputation/invalidation |
| interrupted staging/promotion | no mixed current state; restart reaches one lawful atomic state |
| relayout/migration | identity/role/ancestry/reverse-lineage/consumer parity |
| stopped recursive branch | retained branch survives rebuild with same ancestry and typed stop reason |
| J=3 closure rebake | direct joint regenerated; pairwise projection cannot masquerade as source tensor |

## 7. Operational graph choreography proof

For obligations spanning multiple machine elements, presence of all nodes is insufficient. HQ should require one trace/receipt proving the exact choreography:

```text
GOVERNED SOURCE / AUTHORITY
-> CANONICAL EMPIRICAL OBJECTS
-> ROOT RESPONSE SURFACE
-> COMPLETE GENERATION-N RESULTS
-> DETERMINISTIC CONTROLLER COMPOSITION
-> SEALED GENERATION-N+1 FRONTIER
-> COMPLETE EVALUATION
-> DISCOVERED CHILD / RETAINED BRANCH
-> AUTONOMOUS SUBSTANTIVE TARGET ENUMERATION
-> SAME-RESPONDENT PAIR/J<=3 JOINT FACTS
-> REF-ONLY FRACTURE-MAP CLOSURE
-> LAWFUL PRE-V3 CONSUMER / STRUCTURAL SEAM
```

Every arrow must resolve to an exact public/current contract or exact typed gap. Manual report copying is not graph choreography.

## 8. Carried-forward gap classes versus post-freeze sharpenings

### Carried forward from Long Memory

The inherited baseline already left explicit proof/implementation debt around:

- future semantic maintenance/lifecycle execution (`LMX-004`, plus related lifecycle execution debt);
- product-wide joint/vector/denominator consumer proof (`LMX-010`–`LMX-014`, `LMX-022`);
- whole-machine no-starvation and authority-role conservation (`LMX-023`, `LMX-024`);
- cache delete/rebuild (`LMX-026`);
- physical discovery execution/real-source coverage (`LMX-027`, `LMX-028`);
- positioned-subject/possibility service implementation (`LMX-029`, `LMX-036`);
- exact reverse derivability/invalidation lineage (`LMX-042`);
- atomic staging/promotion/restart/replay (`LMX-043`).

D07 does not call these new gaps.

### Post-freeze sharpened proof burdens

Fracture-map recovery gives concrete adversarial forms for several old debts:

- autonomous controller generation instead of hand-authored right query;
- actual discovered-child recursive handoff;
- exact multi-label presence/pattern morphology;
- branch retention distinct from continuation;
- autonomous substantive-target co-signature enumeration;
- direct J=3 same-respondent topology with pairwise-equivalent negative control;
- exact branch/node/joint denominator and raw/weighted separation;
- ref-only map closure that remains rebuildable;
- destructive rebake of controller + joint + closure choreography;
- explicit PRE-V3 actor-state firewall at the fracture-map output.

These are strengthening deltas, not new sovereign functions.

## 9. Pending-work law

Still-running fracture-map I03/I04/I06 work is **pending only** under the D07 command. HQ must not use it as `current_authority_ref`, `current_machine_element`, `current_test_or_receipt`, or `adoption_currentness_ref` until exact adoption is proved on the current lineage.

`PROMISING_PENDING_WORK != CURRENT_SUCCESSOR`

## 10. Whole-machine final verdict law

HQ may issue:

`CURRENT_MACHINE_ZERO_LOSS_PROVED`

only when:

1. every one of the 44 inherited LMX rows has exactly one Authority-39 terminal disposition;
2. every accepted genuinely new post-freeze obligation, if any, has the same treatment;
3. every `CURRENTLY_PROVED*` row passes every applicable G0-G9 gate;
4. no PRE-V3-required row remains `CURRENTLY_OPEN_FUNCTIONAL_GAP` or `CURRENTLY_OPEN_PROOF_GAP`;
5. outside-jurisdiction rows identify exact downstream owners and preserve prerequisites/ceilings;
6. all LMQ queue items receive current dispositions;
7. destructive replay and operational workflow claims are independently evidenced rather than inferred from structural presence;
8. no false-closure pattern in `ADVERSARIAL_FALSE_CLOSURE_PATTERNS.csv` remains untested where applicable.

Otherwise the lawful final state remains fail-closed.

`PRESENCE_IS_NOT_CLOSURE`

`REPRESENTABLE_IS_NOT_GENERATED`

`REPLAY_POINTER_IS_NOT_REPLAY_PROOF`

`GRAPH_NODES_PRESENT_IS_NOT_GRAPH_CHOREOGRAPHY_PROVED`
