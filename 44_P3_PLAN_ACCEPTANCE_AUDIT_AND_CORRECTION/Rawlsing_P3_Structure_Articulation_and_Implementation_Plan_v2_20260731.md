# Rawlsing P3 Structure Articulation and Implementation Plan v2

**Plan version:** v2  
**Authority date:** 2026-07-31  
**Input authority:** cumulative Rawlsing handoff v20  
**Execution owner:** the ChatGPT agent maintaining the cumulative Rawlsing handoff  
**Execution status:** plan authored; P3 implementation has not begun  
**Exact next execution point:** `P3A_CONTRACT_AND_PILOT_V2_IMPLEMENTATION`

This document is the governing architecture and implementation plan for converting the globally closed P2 authority into canonical J-family authority. It consolidates and formalizes the entire P3 discussion in one central specification. The accompanying machine-readable contract pack is co-governing: schemas, vocabularies, composition rules, lifecycle transitions, acceptance gates, contingency responses, algorithms, SQL-compatible DDL, adjudication templates, release controls, and downstream interfaces are delivered alongside this document.

The assistant will build P3. This is not a delegation document for an unknown future implementer. It nevertheless makes every structure and execution step explicit so that work can proceed deterministically, can survive context transfer, and cannot quietly omit a required authority surface.

# 1. Executive decision

P3 exists to solve one bounded problem:

> Convert P2’s pairwise cross-source proposition authority into defensible candidate and canonical J-families without allowing graph connectivity, inherited semantic neighborhoods, battery labels, response similarity, or broad construct kinship to manufacture semantic identity.

P3 is an authority-construction phase. It is not a clustering exercise. It is not a measurement-harmonization phase. It is not a causal model. It is not the nine-strata pressure engine. It does not require a visualization of the user’s conceptual image of nested and interpressuring social formations. That image disciplines the ontology by warning against sealed layers and static identity; it does not dictate a four-dimensional database object, tensor, animation, or new database platform.

The correct immediate architecture is deliberately restrained:

- immutable P2 authority as input;
- Python builders and validators;
- ordinary governed CSV, JSON, YAML, Markdown, DOCX, and optional Parquet artifacts;
- lightweight graph diagnostics in code;
- PostgreSQL-compatible logical schemas for eventual installation;
- no TypeDB, Neo4j, or new service dependency unless a demonstrated production limitation later requires one.

P3 must preserve all distinctions P2 fought to establish. A mathematically clean component built on false semantic closure would be an industrialized error.

# 2. Frozen starting state

P3 begins from the globally closed v20 P2 state:

| Authority surface | Count |
|---|---:|
| Exact survey implementations | 18,276 |
| Source-local continuity lineages | 13,526 |
| Semantic-priority pair candidates closed | 18,831 |
| Semantic-priority proposition relation authority | 641 |
| Exact-only proposition relation authority | 17 |
| Effective connective proposition pair authority | 658 |
| Effective unique direct pair authority after precedence | 19,175 |
| Bounded or coordinate authority | 1,024 |
| Explicit negative authority | 14,857 |
| Redirected other-domain authority | 1,958 |
| Fail-closed unresolved authority | 351 |
| Exact-foundation pair rulings | 751 |
| Exact-foundation accepted / rejected / unresolved | 270 / 78 / 403 |
| Source structures | 2,499 |
| Structure memberships | 15,990 |
| Structure analogies | 19 |
| Structure-member rulings | 119 |
| Semantic-reference anomalies governed | 30 |

P2 is immutable from P3’s perspective. P3 may interpret, normalize, connect, constrain, and adjudicate P2 authority. It may not silently revise a P2 ruling. Any later P2 correction must enter as a new upstream authority release and trigger a dependency-based impact report and new P3 release.

Asian Barometer W6 remains excluded. GSS remains one survey source rather than a universal template. No canonical J-family authority currently exists. No respondent joins, raw-value harmonization, live registry writes, database writes, or production V550/V551/V552 execution are authorized at the start of P3.

# 2A. Effective upstream authority and precedence

P3 consumes two closed P2 pair registries. They are not additive without precedence.

- Semantic-priority closure contains 18,831 pair authorities.
- Exact-foundation closure contains 751 pair authorities.
- The registries overlap on 407 unordered lineage pairs.
- Semantic-priority closure is later and governs every overlap. Exact-foundation overlap rows remain provenance and cannot create P3 connectivity or contradiction by themselves.
- Exact-foundation contributes 344 exact-only pairs absent from semantic-priority closure.

The effective direct pair-authority surface is therefore **19,175 unique pairs**. Its connective proposition surface is **658 pairs**: 641 semantic-priority proposition relations plus 17 exact-only proposition relations. The remaining 18,517 pair authorities are coordinates, hierarchy, negative, redirect, unresolved, metadata, or other non-connective constraints.

The precedence and mapping contracts are delivered in `upstream/P3_UPSTREAM_AUTHORITY_PRECEDENCE.csv`, `upstream/P3_P2_TO_P3_AUTHORITY_MAPPING.csv`, and `upstream/P3_EFFECTIVE_UPSTREAM_PAIR_AUTHORITY_SURFACE.csv`.

# 3. P3 mandate and non-mandate

## P3 must produce

- typed lineage-pair facts;
- proposition signatures with field-level provenance;
- P3 lineage segments where a P2 lineage materially drifts;
- typed and scoped collision authority;
- strict seed components;
- complete internal pair matrices;
- closure obligations;
- candidate families;
- candidate variants;
- explicit exclusions;
- permitted semantic and measurement hyperedges;
- a ranked adjudication queue;
- structured candidate packets;
- append-only adjudication decisions;
- doctrine deltas;
- stable object identities;
- family genealogy;
- dependency and blast-radius ledgers;
- versioned authority releases;
- deterministic builders and adversarial validators;
- PostgreSQL-compatible logical installation schemas;
- shadow-installation, comparison, promotion, and rollback plans.

## P3 must not produce

- value mappings or scale transformations;
- respondent-level joins;
- causal direction;
- pressure-propagation equations;
- nine-strata numerical dynamics;
- probabilistic family membership;
- machine-learned canonical approval;
- automated family authority from graph components;
- a generalized social ontology server;
- a new DBMS merely because the conceptual system is complex;
- production installation into an unidentified or historical repository.

P3 may carry existing strata, driver, facet, and horizon evidence forward as context. It cannot infer those fields from family membership or use them to authorize causal claims.

# 4. Governing definition of a J-family

A J-family is a governed set of source-local question lineages—or P3 lineage segments—that ask the same underlying social proposition while preserving explicitly permitted wording, translation, response-form, source, and historical variants.

The family core is the **question proposition**, not the broad topic.

A proposition is constituted by the combination of:

- subject or actor;
- governing operator;
- material target or object;
- social action, judgment, condition, or outcome;
- modality;
- timeframe where it changes the claim;
- condition;
- population scope;
- geographic scope;
- polarity and direction;
- direct-item or derived-construct status;
- authoritative parent context when the child item is elliptical.

Examples:

- trust in police and trust in courts are separate proposition families;
- trust in police on four-point and ten-point response scales may belong to one family with response variants;
- internet access at home and internet use last week are separate families;
- signing a petition and willingness to sign a petition are separate families;
- general environmental protection versus economic growth and climate mitigation versus economic growth remain separate or explicitly hierarchical;
- a derived institutional-trust index does not become the same family as one constituent trust item.

The default family-granularity question is:

> Would substituting one question proposition for the other preserve the social claim being made?

A change in actor, operator, target, modality, direct/derived status, material timeframe, population, geographic scope, or condition usually changes the proposition and therefore requires a separate family or a governed hierarchy.

# 5. Four kinds of sameness that may never be collapsed

P3 and all downstream phases must preserve four separate authority claims:

1. **Proposition sameness**  
   The items ask the same social question. P3 may authorize this.

2. **Construct kinship**  
   The items occupy the same broader conceptual domain. P3 may record this through coordinates, sibling-family hyperedges, or target hierarchies, but construct kinship does not create family identity.

3. **Measurement compatibility**  
   Response contracts can be compared or transformed under a governed rule. This belongs to P4, not P3.

4. **Runtime substitutability**  
   The pipeline may use measurements interchangeably for a particular computation. This is a later, purpose-specific runtime authority.

No earlier claim implies a later one. A shared family does not authorize scale harmonization. Scale harmonization does not prove causal equivalence. Structural kinship does not imply runtime substitutability.

# 6. Primary object hierarchy

P3 uses a small object hierarchy.

## 6.1 Implementation

A specific source, wave, and variable. This remains the final evidence-bearing atom.

## 6.2 Source-local lineage

The P2-governed longitudinal continuity unit. It is P3’s primary graph node because repeated waves of one source-local question should not count as independent cross-source evidence.

## 6.3 P3 lineage segment

A family-authority segment created only when a source-local lineage contains material proposition drift. Segmentation preserves the original P2 lineage. It specifies which implementations can participate together in a family.

## 6.4 Candidate component

A mechanically generated connected component. It is diagnostic and has no canonical authority.

## 6.5 Candidate family

A provisional proposition grouping produced after signature and collision partitioning. It awaits structured adjudication.

## 6.6 Canonical family

A stable, adjudicated proposition family in a versioned authority release.

## 6.7 Family variant

A governed variation that preserves the proposition while distinguishing response topology, wording/translation, source response form, or another explicitly authorized variant dimension.

## 6.8 Hyperedge

An n-ary semantic or measurement relation with named participant roles. P3 hyperedges are restricted to battery, structure, derived-index, sibling-family, target-hierarchy, and response-contract functions.

# 7. Identity strategies, revisions, splits, and merges

P3 distinguishes three identity strategies. Treating every object alike would either renumber durable authority or preserve unstable diagnostics forever.

1. **Inherited upstream identity.** Implementations, P2 source-local lineages, source structures, and response-contract references retain their upstream IDs and are registered read-only with authority artifact, hash, source, and licensing provenance.
2. **Content-addressed derived identity.** Candidate components, normalized immutable pair facts, packets, and deterministic diagnostic products use hashes of frozen normalized inputs and build-rule version. If their content changes, they are different derived objects.
3. **Registry-allocated durable identity.** Candidate families once admitted to review, canonical families, variants, exclusions, adjudications, hyperedges, doctrine deltas, and genealogy records receive append-only IDs from immutable idempotency keys. Initial allocation uses a stable sorted order; later releases append and never renumber existing IDs.

Content hashes identify revisions and evidence bundles. They do not replace durable family identities.

A canonical family has a stable `JFAM` identity and one or more immutable release-scoped revisions. Ordinary definition changes append revisions under the same family. Splits and merges allocate new family IDs and genealogy:

```text
family A --superseded_by--> family B, family C
family D, family E --superseded_by--> family F
```

Historical outputs identify the exact family revision and authority release that produced them. IDs are never recycled.

# 8. Proposition signature grammar

Each lineage or segment receives a structured proposition signature.

Required dimensions:

| Dimension | Function |
|---|---|
| `subject_role` | Respondent, household, parent, government, institution, group, country, derived system |
| `operator` | Trust, satisfaction, support, action, willingness, expectation, preference, evaluation, and so forth |
| `target` | The concrete social object or institution |
| `object_or_outcome` | What the operator concerns |
| `modality` | Actual behavior, disposition, evaluation, belief, frequency, expectation, state, or principle |
| `timeframe` | Past, present, future, named interval, or explicitly unspecified |
| `condition` | Condition governing the proposition |
| `population_scope` | Self, household, citizens, immigrants, women, foreign workers, and so forth |
| `geographic_scope` | Local, national, named country, or explicitly unspecified |
| `polarity` | Positive, negative, exclusionary, reverse-worded |
| `derived_status` | Direct item, composite, index, calculated measure |
| `parent_context` | Battery parent supplying an elliptical operator, target, or condition |

Response topology is recorded separately because it ordinarily defines measurement variants, not the proposition itself.

Every field carries:

- canonical value;
- evidence state;
- evidence type;
- evidence ID;
- confidence;
- source implementation or parent context.

Authoritative evidence precedence is:

1. direct source-native question;
2. source-native parent prompt;
3. source-native response dictionary;
4. adjudicated source structure;
5. lineage implementation history;
6. direct P2 ruling evidence;
7. semantic correction overlay as diagnostic location only.

Inherited semantic IDs can locate evidence. They cannot populate a family signature authoritatively.

# 9. Missing, unspecified, heterogeneous, and conflicting evidence

Blank fields are prohibited as an undifferentiated state. Every signature field uses one of:

- `KNOWN`;
- `EXPLICITLY_UNSPECIFIED`;
- `NOT_APPLICABLE`;
- `UNRECOVERED`;
- `HETEROGENEOUS`;
- `CONFLICTING`;
- `DIAGNOSTIC_ONLY`.

These distinctions are operational.

- `EXPLICITLY_UNSPECIFIED` may be compatible across sources.
- `UNRECOVERED` blocks the affected authority claim.
- `HETEROGENEOUS` requires segmentation or a collision.
- `CONFLICTING` requires source reconciliation.
- `DIAGNOSTIC_ONLY` cannot satisfy an evidence gate.

A lineage containing several timeframes, targets, operators, or modalities cannot be averaged into one signature. P3 either creates exact implementation segments or blocks clean family membership.

# 10. P3 lineage segmentation

P3 segmentation is required when longitudinal continuity and proposition identity diverge.

Procedure:

1. Recover implementation-level signatures inside the P2 lineage.
2. Compare proposition-defining dimensions.
3. Determine whether differences preserve the social claim.
4. If they do, retain one P3 subject and record wording or response variants.
5. If they do not, allocate P3 segment IDs with exact implementation membership and historical bounds.
6. Preserve the original P2 lineage and its continuity authority.
7. Block use of the unsplit heterogeneous lineage as a clean family member.

Segmentation therefore says:

> These implementations remain historically continuous within the source, but they cannot all carry one cross-source family proposition.

This prevents P3 from rewriting P2 while preventing longitudinal drift from contaminating family identity.

# 11. Typed P2 pair facts

P3 normalizes direct P2 rulings into typed pair facts. There is no generic `RELATED` edge.

The core types are:

- `PROPOSITION_RESPONSE_IDENTITY`;
- `PROPOSITION_IDENTITY_ONLY`;
- `NESTED_TARGET_RELATION`;
- `CONSTRUCT_COORDINATE`;
- `STRUCTURE_MEMBER_ANALOGY`;
- `EXPLICIT_NEGATIVE`;
- `REDIRECT_OTHER_DOMAIN`;
- `UNRESOLVED`.

Each pair fact preserves:

- left and right lineage/segment IDs;
- source P2 ruling IDs;
- target relation;
- operator relation;
- timeframe relation;
- response-topology relation;
- portability ceiling;
- source-structure context;
- direct endpoint evidence;
- whether connectivity is permitted.

Only the first two types may participate in candidate connectivity. Neither automatically authorizes transitive endpoint relations.

# 12. Directionality, symmetry, and composition

Every relation type declares symmetry and direction.

- proposition identity is symmetric;
- broader-than/narrower-than is directional;
- constituent-of is directional;
- construct-coordinate is symmetric but non-connective;
- negative authority may be symmetric at the prohibited operation while its evidence remains endpoint-specific;
- redirect is domain-specific and non-connective.

The complete 8×8 composition matrix is delivered in `P3_RELATION_COMPOSITION_MATRIX_v2.csv`.

The universal rule is:

> A path never creates a new direct pair authority.

Examples:

- A proposition-identical to B and B proposition-identical to C creates an A–C closure obligation, not an inferred ruling.
- A nested under B and B nested under C does not prove the A–C target hierarchy without direct evidence.
- A structure analogy may reinforce a direct pair relation but cannot manufacture one.
- Any unresolved or negative edge on a path blocks clean closure across that path.

# 13. Typed collision authority

P2’s 14,857 negative rulings do not all mean “unrelated.” P3 translates them into operation-specific prohibitions.

Required collision types include:

- block same proposition;
- block same variant;
- block value portability;
- parent-child only;
- block derived/direct merge;
- block behavior/disposition merge;
- block target collapse;
- block operator collapse;
- block timeframe collapse;
- block population-scope collapse;
- block geographic-scope collapse;
- block polarity collapse;
- block source-structure inference;
- block heterogeneous lineage;
- insufficient evidence;
- redirect semantic artifact.

Every collision declares its scope:

- implementation pair;
- lineage pair;
- segment pair;
- variant pair;
- family-wide;
- value-portability only;
- historical interval;
- source-specific.

This prevents a local wording or interval conflict from poisoning an unrelated family, while also preventing a value-only blocker from being misread as a family rejection.

# 14. Connectivity graph and constraint graph

P3 uses two logically separate graph projections.

## Connectivity graph

Contains only direct proposition-plus-response and proposition-only pair facts. It generates candidates and attachment reviews.

## Constraint graph

Contains:

- typed collisions;
- unresolved authority;
- nested/hierarchical relations;
- source-structure constraints;
- response incompatibilities;
- heterogeneous-lineage blockers;
- semantic redirects.

Coordinate relations do not create connectivity. Structure analogies do not create connectivity. The graph model is a multigraph because the same pair may simultaneously carry proposition support, response incompatibility, hierarchy, and value-portability restrictions.

The canonical source of truth remains tabular authority. Graphs are deterministic projections for candidate construction and diagnostics.

# 15. Strict seed components and the non-transitivity safeguard

The initial component builder uses only `PROPOSITION_RESPONSE_IDENTITY` edges.

For each strict component, P3 materializes every possible internal member pair. A component of `n` members must contain exactly `n(n-1)/2` pair-matrix rows.

Each internal pair receives one state:

- direct positive;
- direct collision;
- hierarchical only;
- unruled;
- signature conflict;
- signature compatible without direct pair authority.

The complete pair matrix is the primary defense against transitive flattening.

An unruled pair does not always force rejection, but it creates a closure obligation. Canonical adjudication must explain why the available signatures and direct supporting structure are sufficient despite the absent direct endpoint ruling.

A hard same-proposition collision anywhere inside a candidate prevents clean or canonical status until the candidate is split or the conflict is resolved by new authority.

# 16. Proposition-only attachments

`PROPOSITION_IDENTITY_ONLY` edges enter after strict components exist.

They may:

- support an existing candidate;
- propose attachment of an isolated lineage;
- propose a response variant;
- create a new proposition-only candidate;
- create a merge-or-sibling review between strict components.

They may not silently merge strict components.

Every attachment across existing components creates a closure obligation and must pass:

- proposition-signature compatibility;
- target/operator/modality checks;
- internal negative and unresolved audit;
- response-variant classification;
- exclusion-surface update.

# 17. Variants, splits, and hierarchy

Default variant dimensions are deliberately narrow:

- response topology;
- wording or translation;
- source-specific response form;
- historical interval only where proposition identity is explicitly preserved;
- another dimension only after a doctrine delta.

Default split dimensions are:

- target;
- operator;
- modality;
- actual behavior versus willingness/intention;
- direct item versus derived construct;
- material population or geographic scope;
- timeframe that changes the social claim;
- condition that narrows the proposition.

Nested targets ordinarily form separate families connected by a target-hierarchy hyperedge. “Police” and “police station,” “environmental protection” and “climate mitigation,” or “parties” and “opposition parties” should not be flattened merely because one is lexically contained in the other.

Every variant carries `NOT_AUTHORIZED_BY_P3` for value portability.

# 18. Permitted P3 hyperedges

Pairwise relations are inadequate for several concrete structures. P3 therefore supports a limited hyperedge vocabulary.

1. **Battery hyperedge**  
   Parent prompt, child proposition families, source structure, and response frame.

2. **Cross-source battery analogy**  
   Adjudicated analogous source batteries and exact member correspondences.

3. **Derived-index constitution**  
   A derived index, constituent questions, aggregation rule, and version.

4. **Sibling-family construct**  
   Separate proposition families within a broader construct, such as trust in police, courts, parliament, and parties.

5. **Target hierarchy**  
   Broader and narrower target families.

6. **Response-contract class**  
   Shared response architecture without proposition identity.

P3 hyperedges carry no causal authority. They do not represent pressure mechanisms, historical causation, or nine-strata transmission. Those later structures must be built only after semantic, measurement, and structural authority are separately closed.

# 19. Candidate classification, lifecycle, and decision status

V1 incorrectly placed diagnostic candidate classes inside the same vocabulary as historical lifecycle state. V2 separates three fields.

**Lifecycle stage** records where the object is in the authority process:

```text
DISCOVERED -> GENERATED_CANDIDATE -> EVIDENCE_COMPLETE -> ADJUDICATION_REQUIRED -> DECIDED
DECIDED -> SUPERSEDED or DEPRECATED
SUPERSEDED -> DEPRECATED
```

**Candidate classification** describes the machine-visible decision surface before adjudication: clean, response-variant, split-required, hierarchy-only, collision-bearing, structure-only, insufficient-authority, or semantic artifact. Classification never authorizes a family and may change when evidence or doctrine changes.

**Adjudication decision status** is the terminal human authority result: accepted canonical, accepted with variants, split required, hierarchy only, blocked unresolved, insufficient authority, rejected semantic artifact, or rejected.

Candidate status events and release status events are append-only. A generated candidate cannot jump directly to canonical authority.

# 20. Evidence sufficiency and candidate closure

Candidate generation requires at least one direct P2 proposition relation. Canonical admission requires far more.

A candidate is fully adjudicated only when:

- all members have exact implementation provenance;
- all essential signature fields are known, explicitly unspecified, not applicable, or explicitly fail-closed;
- every direct positive is represented;
- every direct negative is disposed;
- every unresolved pair is disposed;
- every unruled internal pair is acknowledged;
- every heterogeneous lineage is segmented or excluded;
- every response difference is assigned to a variant or split;
- every hierarchy is directional and explicit;
- every named exclusion is recorded;
- rule-based exclusions define the family boundary;
- every closure obligation has a terminal status;
- the evidence-bundle hash matches the delivered packet;
- a structured adjudication record exists.

A persuasive paragraph is not an adjudication. The decision form is authoritative; prose explains it.

# 21. Explicit exclusion surfaces

Every accepted family requires two exclusion layers.

## Named exclusions

Specific lineages, segments, or implementations that were considered and rejected.

## Rule-based exclusions

Classes of propositions that remain outside the family.

For a trust-in-police family, rule-based exclusions may include:

- trust in courts;
- satisfaction with police performance;
- police contact frequency;
- perceived police corruption;
- access to a police station;
- confidence in the criminal-justice system.

The tested exclusion surface and the conceptual rule boundary remain distinct. Absence of a known negative pair does not imply that all possible exclusions have been tested.

# 22. Candidate ranking

Candidate ranking orders work. It never decides truth.

Ranking is lexicographic rather than a compensatory weighted score:

1. candidate status;
2. hard-collision count;
3. unresolved closure-obligation count;
4. signature completeness;
5. represented source count;
6. represented lineage count;
7. direct-positive density;
8. source-structure support;
9. response-variant complexity.

A hard blocker cannot be overcome by broad source coverage, high graph centrality, or a large number of weak positives. Scores and rankings are derived diagnostics and cannot write canonical authority.

# 23. Candidate packets and structured adjudication

Each candidate packet must lead with the actual decision surface:

- proposed canonical proposition;
- members grouped by source and lineage;
- proposition-signature matrix;
- response-contract matrix;
- complete internal pair matrix;
- hard collisions;
- unresolved pairs;
- unruled pairs;
- closure obligations;
- likely split points;
- proposed variants;
- explicit named and rule-based exclusions;
- hyperedge context;
- available strata/horizon context;
- exact evidence links;
- evidence-bundle hash;
- blank structured decision form.

The decision form requires:

- decision status;
- canonical proposition;
- accepted members;
- excluded members;
- variant assignments;
- hierarchical relations;
- collision dispositions;
- response-portability status fixed to not authorized by P3;
- unresolved boundaries;
- rationale;
- evidence-bundle hash;
- superseded decision where applicable;
- authority release.

The assistant will perform these adjudications. The packet structure exists to force precision, enable verification, and make every decision reconstructible.

# 24. Doctrine deltas and permanent pilot fixtures

The pilot will reveal cases the initial doctrine did not fully anticipate. General rule changes must enter through a doctrine delta containing:

- trigger candidate;
- old rule;
- new rule;
- affected objects;
- required rebuild scope;
- tests added;
- authority release.

A candidate-specific judgment does not become general doctrine silently.

The first manually adjudicated pilot candidates become permanent gold regression fixtures. Later builder or doctrine changes must reproduce them unless an explicit doctrine delta changes the expected result. Gold fixtures must include clean identity, response variants, target fractures, behavior/willingness, nested targets, index/constituent cases, non-transitive chains, battery false analogies, heterogeneous lineages, unresolved child items, and source-dominance cases.

# 25. P3A global pilot design

The automated pilot runs across the entire effective surface of 658 connective proposition pair authorities: 641 from semantic-priority closure plus 17 exact-only proposition pairs absent from that registry. It does not restrict candidate generation to an easy sample.

P3A will:

1. freeze and hash all P2 inputs;
2. normalize all proposition relations and relevant constraints;
3. recover signatures for every incident lineage or segment;
4. generate strict components globally;
5. produce internal pair matrices and closure obligations;
6. partition false transitive components;
7. generate candidate variants and permitted hyperedges;
8. produce the complete ranked candidate inventory;
9. select at most forty representative candidates;
10. adjudicate the selected packets manually;
11. record doctrine deltas;
12. rebuild affected and global surfaces as required;
13. run example, property, mutation, determinism, and no-leak tests;
14. issue the next cumulative handoff.

The governed pilot selection targets are:

- 8 clean multi-source;
- 6 response-variant;
- 6 split-required;
- 5 collision or non-transitive;
- 4 hierarchical-target;
- 3 derived-index;
- 3 heterogeneous-lineage;
- 3 structure-supported;
- 2 source-dominated or sparse.

Categories may overlap. Shortfalls must be explained and replaced by the nearest unrepresented risk class.

# 26. P3B global adjudication and work-unit discipline

After the pilot contract passes, global candidate adjudication proceeds in fixed governed tranches measured by candidate families rather than raw pair rows.

Default tranche:

- approximately 50 candidate families;
- lower when collision-heavy candidates dominate;
- exact incoming and outgoing candidate counts;
- complete evidence and decision return;
- doctrine deltas and rebuild scope;
- cumulative handoff packaging;
- clean-extraction verification.

Each candidate receives a terminal disposition. The global process cannot close by leaving difficult candidates in an unlabeled review queue. Fail-closed unresolved is a terminal authority state when evidence is genuinely absent; it is not forgotten work.

# 27. P3C closure

P3 closes only when:

- every one of the 658 effective connective proposition relations is accounted for, and all 19,175 direct pair authorities remain traceable;
- every generated candidate has a terminal disposition;
- every canonical family has a complete governed proposition signature;
- every member has implementation-level provenance;
- internal same-proposition hard collisions are zero;
- every permitted variant is explicit;
- every accepted family has named and rule-based exclusions;
- every unresolved boundary remains fail-closed and queryable;
- every split, merge, supersession, and deprecation chain is valid and acyclic;
- every decision reconstructs from delivered evidence;
- the dependency ledger is complete;
- canonical and derived rebuilds are deterministic;
- an authority release, migration, validation, comparison, and rollback package exists;
- no measurement, causal, strata-direction, respondent, or runtime authority has been inferred.

Shadow installation is prepared at P3 closure but occurs only against a user-designated live repository or database.

# 28. Canonical versus derived artifacts

Canonical authority includes:

- stable canonical family identities and immutable release-scoped family revisions;
- release object snapshots and change ledgers;

- vocabularies and schemas;
- object identities;
- proposition signatures and field evidence;
- lineage segments;
- pair facts;
- collision scopes;
- closure obligations;
- candidate and canonical family definitions;
- variants;
- exclusions;
- hyperedges;
- adjudications;
- doctrine deltas;
- genealogy;
- dependencies;
- authority releases;
- failure ledgers.

Derived diagnostics include:

- connected components;
- candidate rankings;
- graph-density summaries;
- centrality;
- visualization layouts;
- review queues;
- aggregate statistics.

Every derived artifact must be reproducible from canonical inputs. A family decision may never exist only in a graph layout, ranking table, generated summary, or prose report.

# 29. Incremental rebuilding and correction blast radius

Every artifact declares its dependencies.

When an input changes, P3 computes a dirty set across:

- candidate components;
- candidate families;
- canonical families;
- variants and exclusions;
- hyperedges;
- authority releases;
- runtime artifacts;
- downstream measurement, strata, persona, or simulation outputs when they later exist.

Rebuild scopes are:

- candidate local;
- component local;
- affected dependency closure;
- global candidate inventory;
- full P3 authority.

A corrected P2 ruling never overwrites historical P3 output. It creates a new upstream authority, impact report, doctrine or evidence update, and append-only P3 release. Historical outputs remain reproducible against the prior release.

# 30. New-wave and new-source attachment

New data should not require global re-adjudication.

For a new wave:

1. create implementation authority;
2. adjudicate source-local lineage attachment;
3. recover the implementation proposition signature;
4. compare it with the lineage signature;
5. detect material drift;
6. segment or block where necessary;
7. evaluate canonical family exclusions;
8. attach to an existing variant, propose a new variant, create a new family candidate, create a hierarchy, or fail closed;
9. rebuild the affected dependency closure;
10. issue a new authority release.

For a new source, the same process applies without assuming it must fit an existing family. A source may introduce a proposition between two existing families, forcing a new family or hierarchy rather than a coerced attachment.

# 31. Controlled vocabularies and migration

Every categorical field is governed by a versioned controlled vocabulary. Synonymous labels cannot proliferate unpredictably.

The machine contract includes a categorical-field binding registry. JSON Schema enums and the eventual PostgreSQL migration triggers must close to the same vocabulary domain. Signature fields are a fixed twelve-field object, rather than a free-form list, so duplicates, omissions, and invented dimensions fail validation. Open-ended targets and named scopes retain source text while optionally resolving to stable value-registry IDs; they are not forced into a fictitiously exhaustive enum.

Vocabulary domains include:

- field evidence states;
- subject roles;
- operators;
- modalities;
- response topologies;
- relation types;
- collision types and scopes;
- lifecycle statuses;
- portability ceilings;
- evidence types;
- object types;
- hyperedge types.

A vocabulary change requires:

- a new vocabulary version;
- migration mapping;
- doctrine delta where meaning changes;
- affected-object report;
- rebuild scope;
- regression tests.

Unknown vocabulary values fail validation. Builders may not silently create new categories.

# 32. Release, migration, shadow installation, and rollback

Each authority release carries:

- release ID and parent release;
- schema and builder versions;
- input manifest hash;
- accepted, changed, superseded, and blocked objects;
- validation return;
- migration artifacts;
- rollback artifacts;
- status: draft, validated, shadow, promoted, rolled back, or superseded.

Live installation is read-only by default. Write mode must be explicit.

Installation sequence:

1. identify the actual current repository/database;
2. validate migration in isolation;
3. install in a shadow namespace;
4. retain prior runtime authority;
5. rebuild V550J/V551J/V552J under prior and proposed authority;
6. compare family membership, packet certification, component gaps, strata/horizon enrichment, and downstream outputs;
7. reconcile every intended and unintended change;
8. promote transactionally or roll back completely.

Historical snapshots and handoff copies are evidence, not deployment targets.

# 33. Observability, failure ledgers, and security

Builders emit machine-readable failure records for:

- missing evidence;
- orphan IDs;
- duplicate normalized keys;
- unknown vocabulary;
- invalid state transition;
- internal hard collision;
- incomplete pair matrix;
- open closure obligation;
- invalid genealogy;
- broken dependency;
- non-deterministic output;
- stale derived artifact;
- source-dominance warning;
- licensing-provenance failure;
- attempted authority overreach.

No output is not proof of no problem.

When database installation eventually occurs:

- canonical tables are separated from diagnostic tables;
- historical adjudications are immutable;
- write operations require explicit mode;
- promotion is transactional;
- release hashes and provenance are mandatory;
- ordinary application users cannot rewrite authority history.

# 34. Performance and implementation stack

The current scale does not justify specialized infrastructure.

Expected scale:

- 13,526 lineage nodes;
- 658 effective connective proposition relations;
- 19,175 effective direct pair authorities;
- tens to hundreds of candidate families;
- complete pair matrices inside bounded candidate components.

Implementation stack:

- Python;
- pandas or Polars for tabular transformations;
- NetworkX or equivalent lightweight library for deterministic components and diagnostics;
- CSV and JSON canonical artifacts;
- optional Parquet mirrors where size warrants;
- DuckDB or SQLite for local analytical joins where useful;
- PostgreSQL-compatible DDL for later installation.

Performance goals:

- global candidate generation in minutes;
- candidate-local rebuild in seconds;
- complete validation on an ordinary workstation;
- no required external service;
- bounded memory;
- fully inspectable outputs.

Semantic auditability outranks micro-optimization.

# 35. Source licensing and provenance

Every family member retains:

- survey source;
- wave;
- variable;
- implementation ID;
- source-local lineage;
- evidence references;
- authority release;
- source licensing or usage boundary where known.

Cross-source semantic authority does not dissolve source-specific contractual restrictions. Derived exports and runtime artifacts must remain capable of reconstructing which sources contributed to them and what restrictions attach to those sources.

# 36. Downstream interfaces

P3 reserves clean interfaces without performing downstream work.

## P4 — Measurement and encoding compatibility

Attaches beneath family variants:

```text
family
  variant
    response contract
      compatibility class
      transformation authority
      prohibited mappings
```

P4 may authorize direct identity, monotonic mapping, standardization-only, direction-only, rank-only, or no quantitative portability.

## P5 — Strata, driver, facet, and horizon authority

Assignments may attach separately to:

- family;
- variant;
- implementation;
- historical/contextual condition.

This avoids a single flattened “stratum” column. The component-aware V551J bridge is installed only in the user-designated live repository.

## P6 — Shadow runtime installation

Canonical family and structural authority are installed in shadow mode and compared against prior runtime behavior.

## P7 — Persona and pressure integration

Persona and historical-pressure computation uses exact semantic, measurement, strata, and runtime releases. This is where the conceptual image of nested, interacting social formations becomes computationally relevant. P3 merely prevents the semantic foundation from foreclosing that complexity.

# 37. Permanent downstream invariants

No later phase may violate:

- family membership does not authorize value harmonization;
- value harmonization does not establish causal equivalence;
- construct kinship does not establish proposition identity;
- strata assignment does not establish causal direction;
- structural kinship does not establish runtime substitutability;
- a diagnostic semantic ID cannot override source-native evidence;
- a graph path cannot become direct pair authority;
- unresolved authority remains queryable downstream;
- historical outputs remain reproducible after later revisions;
- every simulation or persona output identifies the family, measurement, structural, and runtime releases that produced it.

# 38. Contingency doctrine

The detailed contingency matrix is delivered as `validation/P3_CONTINGENCY_MATRIX.csv`. Governing responses include:

- positive chains with unruled endpoints create closure obligations;
- positive cycles containing a hard negative become collision-bearing;
- must-link/cannot-link contradictions stop normalization;
- lineage drift creates segments or blockers;
- missing parent or response evidence fails closed;
- semantic-overlay conflicts defer to source-native evidence;
- corrected P2 rulings trigger dependency impact and a new release;
- new sources are never forced into existing families;
- source-dominated candidates are flagged and deprioritized;
- response incompatibility creates variants or splits;
- target, operator, modality, scope, and derived/direct fractures are preserved;
- lost ID registries stop the build;
- splits and merges create new IDs and genealogy;
- vocabulary changes require migration;
- nondeterminism blocks release;
- absent live repositories block installation;
- unexplained shadow-runtime differences block promotion;
- licensing failures block affected exports;
- missing dependency records block partial rebuild;
- doctrine gaps require a doctrine delta, tests, and rebuild;
- scale problems trigger optimization only after correctness and do not automatically justify a new DBMS.

# 39. Acceptance and testing

P3 uses layered testing.

## Example tests

Known clean, variant, split, hierarchy, derived-index, and heterogeneous-lineage cases.

## Property tests

Invariants such as:

- row order cannot change IDs or decisions;
- coordinate edges cannot join components;
- removing a positive edge cannot enlarge a component;
- adding a hard negative cannot improve status;
- pair matrices contain exactly `n(n-1)/2` rows;
- unruled pairs always become closure obligations;
- value-portability blocks survive family acceptance;
- superseded families do not appear in current views.

## Mutation tests

Deliberately corrupt targets, operators, ruling IDs, vocabulary values, IDs, genealogy, evidence, collision scope, dependencies, and state transitions. Builders must fail closed.

## Gold tests

The pilot’s manually adjudicated candidates become permanent fixtures.

## Integration tests

Fresh extraction, deterministic artifact hashes, DDL constraint checks, release comparisons, and no generated cache or bytecode debris.

The complete required gates and tests are delivered in `validation/P3_ACCEPTANCE_GATES.csv` and `validation/P3_TEST_AND_MUTATION_PLAN.csv`.

# 40. Exact artifact package

The v2 machine-readable pack contains:

- controlled vocabularies;
- relation composition matrix;
- separate lifecycle state machine, candidate classifications, and adjudication statuses;
- evidence sufficiency matrix;
- artifact catalog;
- schema dictionary;
- twenty-two connected JSON schemas;
- PostgreSQL-compatible logical DDL with canonical family revisions, imported-object references, release snapshots, and dependency edges;
- execution sequence;
- pilot selection rules;
- algorithms and pseudocode;
- acceptance gates;
- test and mutation plan;
- contingency matrix;
- downstream interface registry;
- adjudication packet and decision templates;
- authority release, migration, and rollback protocol;
- central Markdown mirror;
- central DOCX;
- section manifests and validation returns;
- cumulative handoff controls and verifier.

These are co-governing. The central prose defines doctrine; machine artifacts prevent implementation from relying on memory or free interpretation.

# 41. Execution responsibility and boundedness

The assistant will perform P3A, P3B, and P3C. The plan is not written to outsource implementation. It is written so that each build step has:

- explicit inputs;
- deterministic transformation;
- authority boundary;
- expected outputs;
- failure behavior;
- acceptance gate;
- cumulative handoff return.

The architecture remains bounded to J-family construction. It does not turn Rawlsing into a general ontology platform. It carries enough downstream foresight to avoid schema dead ends, authority leakage, forced rewrites, and blind global reruns.

# 42. Exact next work package

The next cumulative build after this planning release is:

`P3A_CONTRACT_AND_PILOT_V2_IMPLEMENTATION`

Execution order:

1. freeze and hash v20 P2 inputs;
2. install P3 contracts and stable ID registry;
3. freeze the 19,175-pair effective upstream surface and normalize all 658 connective proposition relations;
4. recover signatures for all incident lineages;
5. create P3 segments where required;
6. type and scope candidate-relevant collisions;
7. build strict seed components;
8. build complete internal pair matrices;
9. create closure obligations;
10. attach proposition-only relations without automatic merging;
11. partition signature-incompatible components;
12. create variants and permitted hyperedges;
13. rank the complete candidate inventory;
14. select up to forty representative candidates;
15. produce self-contained packets;
16. adjudicate them;
17. record doctrine deltas;
18. rebuild affected surfaces;
19. run all acceptance tests;
20. package the complete cumulative handoff.

The first execution return must answer:

- how many candidate components and candidate families the 658 effective connective proposition relations produce;
- which collision patterns prevent canonical admission;
- whether the P3 contract survives representative manual adjudication;
- what doctrine deltas, if any, are required before global scaling.

# 42A. V21 acceptance-audit corrections

The v21 conceptual doctrine survived review, but implementation acceptance found defects that required correction before execution:

- the upstream surface omitted 17 exact-only proposition pairs and 327 exact-only non-connective authorities;
- overlapping exact-foundation rows lacked an explicit supersession rule;
- relative JSON Schema references were not locally resolvable as a connected schema system;
- the draft decision form was incorrectly validated as a completed decision;
- candidate classification and lifecycle were conflated;
- the logical DDL lacked canonical-family revisions, release snapshots, change ledgers, and fully registered polymorphic references;
- controlled vocabularies did not cover every categorical implementation field;
- the schema dictionary contradicted `creates_endpoint_authority=false` and did not cover the DDL;
- identity doctrine did not distinguish imported, content-addressed, and durable registry objects.

V2 corrects each defect and adds fatal regression gates so none can reappear during P3A. Section 43 remains historical and is superseded by this section.

# 43. Final governing statement

P3’s task is severe but finite:

> Construct a durable authority machine capable of saying that these lineages constitute one proposition family, under these variants and exclusions, because of this exact evidence, in this authority release—and that these other lineages do not.

Everything downstream depends on that statement remaining reconstructible. The plan therefore privileges explicit boundaries, immutable history, fail-closed uncertainty, deterministic rebuilding, and evidence over graph elegance or conceptual compression.


# Appendix D. V22 hostile implementation audit corrections

The v21 prose doctrine remains conceptually governing, but its v1 machine contract is superseded by section 44. The hostile audit found and corrected: the 641-versus-658 connective input undercount; missing precedence for 407 registry overlaps; broken relative JSON Schema references; draft/final adjudication conflation; free-form proposition-signature arrays; generic candidate-packet object arrays; incomplete object-type and categorical vocabularies; candidate lifecycle/classification conflation; absent canonical-family revision persistence; weak polymorphic references; non-historical promotion uniqueness; release snapshot/change-ledger gaps; and missing downstream response, structural-context, and licensing reference interfaces. P3A must use only the v2 contracts in section 44.


## Explicit executable invariants

Paths create closure obligations and never endpoint authority. A transactional singleton promotion pointer identifies the currently active runtime release while preserving historical promotion events.
