# Current-35 Usable-Universe & Normalized Authority-Binding Quality Court

Status: `ADJUDICATED__18276_IMPLEMENTATIONS_DISPOSITIONED__CURRENT_AUTHORITY_STACK_BOUND__NEGATIVE_STATES_PRESERVED__NO_NEW_SEMANTIC_AUTHORITY_AUTHORIZED__SCHEMA_MIGRATION_READY`

Recorded: 2026-08-23

## Court question

For each governed current-35 P2 question implementation, what is its present use disposition, what authority binds to it or to its related semantic/structural/source grains, what remains explicitly blocked or conflicted, and what must Trii and Chetiri preserve?

This court begins from the already-adjudicated P2 population law. It does not create a competing question universe or UID.

## Governing evidence stack

The court mechanically joined the exact content-addressed P2/R10 authorities available in Library:

- P2 Phase-0 question implementation skeleton — 18,276 exact implementations; SHA-256 `d38301588fae27c66f6b8627c5007fb0d8ed4ac3d7eb25f32c74228c367b86b6`.
- R10D S00 terminal-use successor ledger — 18,276 / 18,276 implementations, exactly one baseline workstream each.
- R10F central O03/O04 integration — 3,667 topology rows and 2,627 behavior/exposure review rows, terminal within jurisdiction.
- R10G O02/S08 coordinate authority — 3,324 / 3,324 semantic units; cumulative SHA-256 `d524010ffbce1e095da98cfd22e25e83f3293998e10a3a3f2b0ed1717ff4f70f`.
- R10H P0 U1 central reconciliation — O06/O07/O08 over 18,276 / 18,276 implementations; SHA-256 `ffc824f5cf060ac71744913ac4a26a6e0a802fa0644d1d6cb04c92f5129fe8e5`.
- R10I O09 P5 placement authority — all 3,324 semantic units and all 18,276 O08 implementation conditioner dispositions; SHA-256 `c430837467698860338711449076303ba39981642c879705c4abb0d41ebbdd02`.
- H001-H005 recovered QSR, FQRA/QSMv2, V525b, later semantic/driver, source/SWID, QRA/response and provenance authority.

The row-level P2 skeleton remains the identity master. `CURRENT35_IMPLEMENTATION_DISPOSITION_LEDGER.csv` is a lossless **P2-ordinal bytepack**, not a second identity registry. Its 18,276-byte payload is anchored to the immutable P2 SHA-256 `d38301588fae27c66f6b8627c5007fb0d8ed4ac3d7eb25f32c74228c367b86b6`; byte ordinal `N` addresses P2 row `N` (zero-based) for deterministic replay only. P2 row order does **not** establish authority precedence.

The bytepack payload SHA-256 is `64a43ba2d7564d7681770065b843273330dc368b8d01bf328a8af7b19878bd98`. Bits 0–3 encode the primary-use code, bit 4 encodes the cross-cutting fail-closed flag, bit 5 encodes whether an executable routing predicate is required, and bits 6–7 are reserved zero. This gives exhaustive per-implementation accounting without copying the P2 identity column into another mutable master.

### Compact disposition-ledger codes

The packed disposition ledger deliberately uses compact codes so the Control Room can preserve all 18,276 implementation dispositions without duplicating P2 identity or verbose authority text. The codes are lossless projections of the named governing authorities:

- `use`: `SEM` semantic evidence; `TOP` source-topology/non-scalar structure; `POS` respondent-position/demographic coordinate; `END` accepted behavior/exposure endpoint; `CTX` source/respondent context; `SCX` structural context; `ADM` administrative/metadata; `REJ` preserved non-endpoint/rerouted O04 rejection; `CPC` context-position conditioner; `BLK` blocked/unresolved.
- `o03`: `P` preserve source topology; `R` revise topology; blank = outside O03 jurisdiction.
- `o04`: `A` accepted endpoint; `R` rejected endpoint; `B` blocked; blank = outside O04 jurisdiction.
- `o06`: `RU` source routing unresolved; `RA` respondent-answer conditional; `U` unconditional source-proven; `AN` admin/nonrespondent; `CC` country conditional; `MC` multi-condition; `SS` split-sample conditional; `DE` demographic/eligibility conditional; `MB` module/ballot conditional.
- `o07`: `BS` binary state; `SS` signed scalar; `N` nominal; `UO` unsigned ordered; `A` admin; `C` continuous; `CT` count; `MX` mixed/conditional; `D` duration; `R` ranking; `BT` binary tradeoff; `OT` open text; `U` unresolved; `MS` multiselect.
- `o08`: `N` not position; `H` household position; `R` respondent position; `A` admin/paradata; `S` source context; `U` position semantics unresolved.
- `o09`: `N` not P5 conditioner; `A` admitted conditioner; `U` conditioner semantics unresolved.
- `hard_fail=Y` means at least one implementation-level fail-closed condition is present at the current authority stack (primary/source block, O04 block, O06 routing unresolved, O07 unresolved, O08 unresolved, or O09 unresolved). It does not erase otherwise valid semantic/source authority.
- `route_predicate_required=Y` means O06 establishes a conditional routing class whose predicate must be honored by executable consumers.

## 1. Every one of the 18,276 implementations is dispositioned

The bytepack decodes to exactly 18,276 dispositions, one for each of the 18,276 unique P2 implementation IDs.

Primary use classes:

| Primary use disposition | Count |
| --- | ---: |
| `SUBSTANTIVE_SEMANTIC_EVIDENCE` | 4,681 |
| `SOURCE_TOPOLOGY_OR_NONSCALAR_STRUCTURAL_EVIDENCE` | 3,667 |
| `RESPONDENT_POSITION_OR_DEMOGRAPHIC_COORDINATE` | 2,904 |
| `SUBSTANTIVE_BEHAVIOR_OR_EXPOSURE_ENDPOINT` | 2,113 |
| `SOURCE_OR_RESPONDENT_CONTEXT_SUPPORT` | 1,675 |
| `STRUCTURAL_CONTEXT_SUPPORT` | 1,506 |
| `ADMINISTRATIVE_OR_METADATA` | 1,026 |
| `NON_ENDPOINT__REROUTED_OR_EXCLUDED_FROM_O04` | 454 |
| `CONTEXT_POSITION_CONDITIONER` | 183 |
| `BLOCKED_UNRESOLVED` | 67 |

The 67 primary blocked rows are the 60 R10F O04 endpoint blocks plus the seven R10D source-review blockers. This primary use classification does **not** erase cross-cutting routing/measurement/position uncertainty; those remain separate fields.

### Interpretation

The current-35 universe is not a binary “usable / useless” table.

A question implementation may simultaneously be:

- valid semantic evidence;
- subject to a routing predicate;
- non-directional or measurement-unresolved;
- a position conditioner rather than a semantic endpoint;
- source/topology evidence rather than a scalar atom;
- historically covered by V525b;
- absent from FQRA without losing upstream identity;
- blocked for one jurisdiction while preserved for another.

The normalized substrate must preserve these orthogonal facts.

## 2. O03 and O04 are terminal within their jurisdictions

R10F centrally supersedes worker-local O03/O04 decisions where it explicitly says so.

### O03

All 3,667 S2/S2-source-topology implementations are terminal:

- 2,884 `PRESERVE_SOURCE_TOPOLOGY`;
- 783 `REVISE_TOPOLOGY`;
- 0 blocked.

This is source/topology authority. It does not create default directionality, interval assumptions, cross-wave equivalence or P4 portability.

### O04

All 2,627 behavior/exposure candidates are terminal:

- 2,113 `ACCEPT_ENDPOINT`;
- 454 `REJECT_ENDPOINT`;
- 60 `BLOCKED`.

Rejected endpoint status does not erase the question's source/semantic/context meaning. R10F's reroute class is preserved. Blocked rows fail closed until the named source/upstream successor closes them.

## 3. Routing authority exists across the entire implementation universe

The older R10E archaeology state `exact routing bytes not recovered` is historical ancestry, not the current authority state.

R10H U1 centrally reconciles O06 over all 18,276 implementations:

- 10,348 `SOURCE_ROUTING_UNRESOLVED`;
- 2,005 `RESPONDENT_ANSWER_CONDITIONAL`;
- 1,986 `UNCONDITIONAL_SOURCE_PROVEN`;
- 1,495 `ADMIN_OR_NONRESPONDENT`;
- 906 `COUNTRY_CONDITIONAL`;
- 748 `MULTI_CONDITION`;
- 377 `SPLIT_SAMPLE_CONDITIONAL`;
- 236 `DEMOGRAPHIC_OR_ELIGIBILITY_CONDITIONAL`;
- 175 `MODULE_OR_BALLOT_CONDITIONAL`.

`SOURCE_ROUTING_UNRESOLVED` means **existing explicit negative/uncertain routing authority**, not missing carrier coverage and not permission to assume ASK-ALL.

Semantic relation truth and respondent composability remain separate.

## 4. Measurement/use and position authority also cover all 18,276

### O07 measurement/use

All implementations have a current measurement-use class. The surface contains 30 `UNRESOLVED` rows. Those fail closed for use requiring resolved measurement semantics.

R10H O07 must not be mistaken for a global replacement of bounded QRA/manual directionality. The separately accepted bounded directional authority and its response-scale contracts remain their own assertions.

### O08 position

All implementations have a current position lane:

- 12,574 `NOT_POSITION`;
- 2,444 `HOUSEHOLD_POSITION`;
- 1,815 `RESPONDENT_POSITION`;
- 1,130 `ADMIN_OR_PARADATA`;
- 295 `SOURCE_CONTEXT`;
- 18 `POSITION_SEMANTICS_UNRESOLVED`.

The 18 unresolved rows remain unresolved; no semantic vocabulary or demographic heuristic may promote them.

## 5. O09 closes P5 placement/conditioning without creating psyche

R10I O09 is accepted current P5 placement authority.

For the implementation-level conditioner surface:

- 4,544 `P5_CONDITIONER_ADMITTED`;
- 13,704 `NOT_P5_POSITION_CONDITIONER`;
- 28 `P5_CONDITIONER_SEMANTICS_UNRESOLVED`.

At semantic-unit grain O09 terminally handles all 3,324 units, distinguishes permitted strata from resolved direct strata and activation contracts, and preserves bounded Horizon relevance without generating actual personal Horizon states.

Chetiri must preserve those distinctions as separate relations.

## 6. H005 carrier findings remain binding

### FQRA/QSMv2

FQRA binds 18,250 P2 implementations:

- 18,052 exact;
- 198 unique casefold search bindings;
- 26 P2 implementations outside its target;
- nine active FQRA rows explicitly `BLOCKED_IDENTITY_OR_AUTHORITY_JOIN`.

The 26 absences are not question gaps. The nine blocked joins stay blocked until source/manual crosswalk authority resolves them.

### QSR

Register C is a structural/source-topology carrier, not question-population authority:

- 18,792 physical rows;
- seven LiTS III case-sensitive P2 identities become ambiguous if case is discarded;
- five P2 implementations are absent;
- 518 unique QSR-only structural/access keys exist outside P2.

These facts are preserved as crosswalk/cardinality relations rather than normalized away.

### V525b

The accepted V525b semantic and driver masters remain historical epistemic capital. Their current-35 projection binds only part of the 18,276 P2 universe, and their small historical duplicate-key imperfections remain explicit.

Later carrier absence or recency is not supersession.

### Later semantic / d62

The later semantic helper is a generated/inherited projection and may aid recall/crosswalk work.

The d62 driver carrier contains valuable later structural assertions, but H004 proves that its GSS/LiTS flat-row duplication and downstream last-row behavior cannot be treated as semantic supersession. Future migration must split the assertions by grain and provenance.

## 7. No new semantic-authority gap is proved

This court found **zero authority classes** that lawfully reach:

`MISSING_PROVED__NEW_AUTHORITY_CREATION_REQUIRED`

The live unresolved surface consists of:

- explicit routing uncertainty;
- explicit O07/O08/O09 uncertainty;
- explicit O04 source/topology blocks;
- bounded FQRA crosswalk blocks;
- carrier identity/cardinality defects;
- historical supersession uncertainty;
- execution-inheritance divergence such as SWID not inherited by current control;
- source-specific successor obligations.

Those are real debts, but none authorizes fabricated semantic/manual meaning.

New substantive authority remains prohibited until a specific required assertion is positively proved absent after source/provenance exhaustion.

## 8. Current normalized authority stack

The current substrate should treat these as orthogonal authority relations:

1. P2 question-implementation identity;
2. current source-wave UID/SWID identity;
3. exact source-byte/source-native identity;
4. implementation use disposition;
5. semantic-unit meaning/membership;
6. canonical semantic coordinates;
7. source topology / non-scalar structure;
8. behavior/exposure endpoint status;
9. relation/structural assertions including FQRA/QSMv2;
10. historical semantic/driver assertions;
11. routing/applicability predicates;
12. measurement/use class and response contracts;
13. bounded directional authority;
14. respondent/source extraction semantics;
15. position lanes;
16. P5 strata/Horizon placement and activation;
17. source-structure/battery/parent-child relations;
18. provenance/evidence;
19. negative/review/block state;
20. explicit supersession/retirement edges.

No physical row order may establish precedence between these relations.

## 9. Trii consequence

Trii does not need to recreate the 18,276-question semantics.

Trii must certify and preserve the source-native floor beneath already-recovered authority:

- exact source/member SHA identity;
- governed source-wave UID;
- exact variable/instrument identity;
- questionnaire/codebook/methodological evidence;
- response/value-label evidence where source-native;
- routing/applicability evidence where source-native;
- exact evidence ceilings where source material cannot resolve a question.

Source-cert packets must be able to bind into P2/current authority without inventing question identity.

## 10. Chetiri consequence

Chetiri now has enough authority-accounting closure to design the persistent/compiler substrate.

The design must preserve:

- the 18,276 P2 implementation IDs unchanged;
- all separately-grained authority assertions;
- one-to-many assertions without duplicating question occurrence;
- blocked/review/unresolved states;
- explicit source/evidence provenance;
- explicit supersession edges;
- current R10H/R10I authority;
- accepted V525b historical capital;
- FQRA/QSMv2 and QSR within their own jurisdictions;
- bounded QRA/response-scale authority;
- SWID/source identities;
- deterministic replay.

The migration may create new physical row IDs / assertion IDs for normalized storage. It may not create a new semantic question identity system.

## 11. Physical architecture authorized next

The next lawful court is schema/migration/replay design, not more broad authority archaeology.

Target:

- versioned typed Parquet relations;
- DuckDB read-only deterministic compilation;
- explicit schemas/manifests/hashes;
- assertion IDs and provenance edges;
- one derived wide `question_authority_master` compatibility view;
- validators proving conservation, cardinality, negative-state preservation and no implicit precedence.

The d62 failure mode must become mechanically impossible.

## Terminal ruling

`CURRENT35_18276__EVERY_IMPLEMENTATION_DISPOSITIONED`
+
`R10F_O03_O04__BOUND`
+
`R10H_O06_O07_O08__BOUND_CURRENT`
+
`R10I_O09__BOUND_CURRENT`
+
`FQRA_QSR_V525B_QRA_RESPONSE_SWID_SOURCE__PRESERVED_AT_CORRECT_GRAIN`
+
`NEGATIVE_AND_BLOCK_STATES__FIRST_CLASS`
+
`MISSING_PROVED_NEW_SEMANTIC_AUTHORITY__ZERO`
+
`NEXT__UNIFIED_SUBSTRATE_SCHEMA_MIGRATION_AND_REPLAY_CONTRACT`
