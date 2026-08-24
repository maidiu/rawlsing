# Trii / Chetiri Authority Requirements

Status: `REQUIREMENTS_FROZEN_FROM_CURRENT35_USABLE_UNIVERSE_BINDING_COURT`

Recorded: 2026-08-23

## Governing premise

The 18,276-question implementation universe and the major current authority layers already exist. Trii and Chetiri are not authorized to simplify the project by silently recreating semantic meaning from raw source files or by choosing a physical model that drops recovered epistemic capital.

Their task is to preserve and serve the authority graph.

---

## A. Requirements common to Trii and Chetiri

### A1. Preserve P2 implementation identity exactly

Canonical current-35 question implementation identity is the existing P2 `question_implementation_id`, bound to exact case-sensitive source-variable identity and source-wave identity.

Required:

- preserve all 18,276 IDs unchanged;
- preserve exact case sensitivity;
- preserve the seven LiTS III case-collision pairs as distinct;
- prohibit casefold, normalized text, similar wording, row position or helper `item_id` from becoming identity authority;
- represent aliases/crosswalks as edges, never as identity mutation.

### A2. Preserve authority grain

At minimum the persistent model must distinguish:

- question implementation;
- question concept / continuity / pair lineage;
- source wave;
- source-native variable/instrument object;
- semantic unit;
- semantic assertion;
- driver assertion;
- facet/domain/block/axis/target assertion;
- source topology;
- behavior/exposure endpoint;
- response/measurement contract;
- directionality assertion;
- routing/applicability predicate;
- respondent/source extraction contract;
- position conditioner;
- P5 placement/activation assertion;
- relation assertion;
- evidence/provenance object;
- review/block/negative decision;
- supersession edge.

A one-to-many assertion set is not a duplicate question.

### A3. Preserve negative authority

The following are data, not nulls to be cleaned away:

- `BLOCKED`;
- `REJECT_ENDPOINT`;
- `SOURCE_ROUTING_UNRESOLVED`;
- O07 `UNRESOLVED`;
- `POSITION_SEMANTICS_UNRESOLVED`;
- `P5_CONDITIONER_SEMANTICS_UNRESOLVED`;
- FQRA `BLOCKED_IDENTITY_OR_AUTHORITY_JOIN`;
- context-only / admin-only / non-endpoint dispositions;
- source-evidence ceilings;
- review-required states;
- unproved supersession.

### A4. Prohibit implicit precedence

No consumer may resolve competing assertions by:

- last row wins;
- newest file wins;
- newest path wins;
- nonblank beats blank;
- generated helper beats accepted historical authority;
- item ID presence beats exact source identity;
- downstream target inclusion beats upstream question membership.

Precedence requires an explicit governed supersession edge with jurisdiction.

### A5. Replay must be deterministic and conservation-tested

A migration/rebuild must prove:

- 18,276 implementation IDs in = 18,276 implementation IDs out;
- source-wave membership conserved;
- case-sensitive identities conserved;
- all accepted authority assertions conserved or explicitly superseded;
- all negative states conserved;
- one-to-many cardinality conserved;
- no extra semantic authority appears;
- no accepted assertion disappears without an explicit retirement/supersession record.

---

## B. Trii requirements

Trii owns source certification / source-native evidence integrity, not semantic reinvention.

### B1. Exact source identity

For each active source wave Trii must preserve:

- source/member SHA-256 identity;
- source archive/member path where relevant;
- source release/version identity;
- current source-wave UID;
- exact source variable/codebook identity;
- source questionnaire/codebook/methodological-document identity.

`SOURCE_BYTE_INVENTORY.csv` is the source identity floor and must remain bindable to current authority.

### B2. Source-native evidence ceilings

Trii packets must distinguish positively:

- source labels present;
- source labels absent;
- routing instruction present;
- routing instruction not recovered;
- source parent/stem/grid structure present;
- target/antecedent unresolved;
- country/module/form scope known or unknown;
- respondent universe known or unresolved.

Absence in the source must not be replaced by model inference.

### B3. Bind source authority to P2, do not rebuild P2

A source certification packet should emit evidence keys that resolve to:

`source_wave_uid + exact source-native variable/instrument identity`

and then bind to existing P2 implementation identity through governed crosswalks.

Trii must not mint a competing question UID because source metadata happens to use another identifier.

### B4. Preserve source-specific blocker obligations

Examples already live in current authority include:

- O04 source/target/topology blocks;
- R10H routing unresolved obligations;
- FQRA identity/crosswalk blocks;
- LiTS exact-case distinctions;
- helper/parent coordinates outside P2;
- source-specific response-label gaps.

Trii may close one only with source-native or otherwise governing authority, with provenance and a successor edge.

### B5. Output contract for Chetiri

Trii certification should provide machine-bindable objects for:

- `source_release`;
- `source_member`;
- `source_wave_uid`;
- `source_variable_or_instrument_object`;
- `source_evidence_locator`;
- `source_response_contract`;
- `source_routing_clause`;
- `source_parent_child_or_grid_structure`;
- `source_evidence_ceiling`.

Every object must be hash-addressed or carry a hash-addressed parent.

---

## C. Chetiri requirements

Chetiri owns persistent physical architecture / compiler serviceability. It must consume the recovered authority graph rather than select a storage design that silently narrows it.

### C1. Canonical physical relations

The candidate physical release must at minimum include typed relations equivalent to:

- `question_implementation`;
- `source_wave`;
- `source_object`;
- `question_source_binding`;
- `implementation_use_disposition`;
- `semantic_unit`;
- `semantic_unit_member`;
- `semantic_assertion`;
- `driver_assertion`;
- `facet_assertion`;
- `structural_coordinate_assertion`;
- `source_topology_assertion`;
- `behavior_endpoint_assertion`;
- `measurement_use_assertion`;
- `response_contract`;
- `directionality_assertion`;
- `routing_predicate`;
- `position_assertion`;
- `p5_placement_assertion`;
- `relation_assertion`;
- `evidence_object`;
- `assertion_evidence`;
- `review_or_block_state`;
- `crosswalk`;
- `supersession_edge`.

Exact names may change. Grains may not be collapsed.

### C2. P2 identity remains the implementation primary key

`question_implementation_id` must be unique across exactly 18,276 current-35 rows.

Other identifiers may be unique within their own tables, but may not substitute for P2 identity.

### C3. Assertion identity is separate from question identity

Chetiri should assign stable physical assertion IDs where needed.

This is specifically required to preserve cases such as d62:

- one question implementation;
- accepted historical semantic assertion;
- later structural assertion;
- possibly a review/block assertion;
- explicit provenance for each.

No assertion is allowed to create a second question occurrence merely because a producer used a different identifier.

### C4. Current authority layers that must be first-class

The physical design must serve without lossy flattening:

- R9D/R10G semantic-unit meaning and coordinates;
- R10F O03 source topology;
- R10F O04 behavior/exposure endpoint status;
- R10H O06 routing;
- R10H O07 measurement/use;
- R10H O08 position;
- R10I O09 P5 placement/conditioning;
- FQRA/QSMv2 relation/structural authority;
- QSR source-structure authority;
- bounded QRA/manual directionality + response-scale contracts;
- V525b accepted historical semantic/driver capital;
- source-wave UID and source-byte authority;
- respondent source/value semantics;
- negative/block/review states.

### C5. Historical carriers become provenance or compatibility views where appropriate

The future canonical store should not keep semantic authority alive merely because an old CSV remains writable.

Historical/helper carriers should be classified as one of:

- canonical normalized authority source;
- immutable historical provenance;
- generated/discovery evidence;
- compatibility view;
- rejected/defective carrier preserved for lineage.

In particular:

- d62 flat row order is forbidden as semantic authority;
- later semantic helper is not canonical by recency;
- V525b remains accepted historical authority until explicit supersession;
- QSR is not question-population authority;
- FQRA target membership is not P2 occurrence membership.

### C6. DuckDB compiler contract

The serving/compiler layer should be deterministic and read-only over a versioned release.

Required properties:

- no mutation of authority during query;
- no row-order precedence;
- explicit joins on declared keys;
- fail closed on ambiguous/missing required joins;
- source/wave UID normalization before execution;
- typed handling of unresolved/blocked state;
- explicit provenance surfaced with compiled result.

### C7. Wide compatibility view

Chetiri may expose one derived wide `question_authority_master` view for inspection and legacy consumers.

That view must be downstream of normalized relations and must:

- never become canonical write authority;
- expose ambiguity rather than arbitrarily choose one assertion;
- include authority status/provenance fields;
- fail or emit structured multiplicity when a consumer assumes false one-to-one cardinality.

### C8. Migration validator gates

Before release acceptance, validators must prove at least:

1. P2 implementation conservation: `18276 == 18276`.
2. implementation IDs unique: `18276`.
3. no casefold collapse of LiTS III pairs.
4. R10D disposition coverage: `18276`.
5. R10F O03 coverage: `3667`.
6. R10F O04 coverage: `2627`, including `2113/454/60`.
7. R10H O06/O07/O08 coverage: `18276` each.
8. O06 unresolved count preserved: `10348`.
9. O07 unresolved count preserved: `30`.
10. O08 unresolved count preserved: `18`.
11. O09 conditioner counts preserved: `4544/13704/28`.
12. FQRA blocked-join count preserved: `9`.
13. FQRA P2-outside-target count preserved: `26`.
14. d62 duplicate history represented without duplicate question occurrence.
15. V525b accepted authority not silently deleted.
16. SWID 35-member scope preserved.
17. no `MISSING_PROVED` semantic assertion created by migration.
18. no implicit supersession edge.
19. deterministic cold replay produces identical manifests/hashes for normalized authority relations.
20. legacy compatibility view is derivable from canonical relations and is never required as input to rebuild them.

---

## D. What is explicitly *not* required before Chetiri schema design

The following do not justify another broad archaeology cycle before physical design:

- a newly invented question UID;
- a second 18,276-row identity census;
- manual re-reading of all questions;
- complete elimination of every routing unresolved state;
- complete global directionality beyond the accepted bounded authority;
- reconstruction of the unrecovered transient pre-d62 full driver master;
- repair of d62 as a flat master.

Those unresolved/historical facts can be represented faithfully in the normalized substrate.

---

## E. Next joint gate

The next joint Trii/Chetiri court should freeze:

`NORMALIZED_SCHEMA`
+
`PARQUET_RELEASE_LAYOUT`
+
`DUCKDB_COMPILER_CONTRACT`
+
`MIGRATION_MAPPING`
+
`VALIDATION_AND_REPLAY_MANIFEST`

against the exact current authority pins identified by this court.

No runtime/source mutation is authorized by this requirements document.
