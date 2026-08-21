# R04 — VECTORIZED / COLUMNAR / MATRIX / BITMAP / LATE-MATERIALIZATION ENDGAME

Status: `RETURNED__NON_DISPOSITIVE__CLASS_C_HOSTILE_DESIGN`

Starting HEAD: `bc2d022d49b1a860a33b29ce171a89c91956c35e`

Candidate name: `CCIV` — Canonical Columnar Incidence + Virtual C11

Primary candidates: `C08`, `C09`, `C10`, `C11`, `C20`, `C21`.

## 1. WHOLE_MACHINE_CONTAINMENT

This return changes no Rawlsing semantics and proposes no production implementation. It sits only at the physical execution/storage layer beneath frozen C11 and above the dumb source decoder. The governing logical chain remains:

`source bytes -> source-native physical incidence -> source authority -> C11 -> I03 -> I05 -> I04 -> closed V553+ machine`.

The proposal is subordinate to source-native truth, M01-M18, ExactRef/content-hash law, I03 positive and negative truth conditions, I05 exact-bounded discovery, I04 admission, and whole-machine carrier ignorance. Physical specialization is permitted only behind one common logical C11 interface. No downstream consumer may ask whether a release is SAV, DTA, dense, sparse, matrix-backed, bitmap-backed, or long-backed in order to decide meaning.

The proposal is deliberately Class C and therefore loses automatically to a simpler streaming-long design if the latter passes the same hostile semantic oracle and operational gates with adequate margin. Compression is not a reason to adopt CCIV.

## 2. PROBLEM_OWNED

R04 owns the strongest plausible physical endgame after R4 exposed real-scale execution/storage pathologies. The target is not a new ontology. The target is to avoid corpus-scale Python event construction and repeated long-row materialization while retaining arbitrary respondent-grain conjunctions, exact joints, unforeseen I05 combinations, routing/risk sets, weights/design, topology, provenance, and deterministic replay.

The checked-in census establishes 486,174,936 physical cells across 35 exact sources, including 112,031,914 system-missing and 47,490,989 SPSS user-missing cells. Twenty-two sources contain SPSS user-missing values; multiple-response metadata is physically declared in Asian Barometer Wave 5, EVS 2008, and EVS 2017. The accepted cross-corpus reconnaissance additionally forbids assuming a universal native respondent ID, permits all-row typed-missing columns, preserves overlapping/alias MR-set identity, preserves ordinary blank strings absent authority, and keeps reader-compatibility metadata distinct from semantic text authority. A simple rectangular matrix is therefore not a lawful universal design.

## 3. PROPOSED_MECHANISM

CCIV is a hybrid release-local columnar compiler with a deterministic virtual long C11 view.

### 3.1 Canonical physical members

Each sealed source release has these logical member classes. Exact filenames and block widths are implementation details, not semantics.

1. **Release manifest and seal**: exact source SHA, decoder/configuration receipt, logical C11 contract version, physical profile identifier, member hashes, deterministic ordering law, authoritative-member list, cache manifest, and replay root. `physical_profile` is execution metadata only.
2. **Respondent axis**: source-row replay ordinal plus the exact C11 respondent-grain material that is already proven lawful at respondent grain. No native ID is promoted to replay identity merely because it is unique in one source.
3. **Question/variable axis**: source variable identity/order, native question binding, source metadata and any exact C11 material already proven lawful at question grain. No event field is moved here without independent grain authority.
4. **Typed incidence blocks**: question-oriented Arrow/Parquet column groups containing raw-value lanes, typed physical-state lanes, governed C11 response-state/canonical-value lanes where authorized, and exact event-coordinate material needed to reconstruct C11. Blocks are bounded collections of question lanes, not one tiny file per question.
5. **Explicit event/topology relation**: all non-rectangular, repeated, ranked, ordered, componentized, multiselect, alias-MR, or otherwise event-specific material that cannot be proved by immutable axis law. This relation carries source-row/respondent coordinate, question coordinate, occurrence/event coordinate, event-group/event-id material, topology/rank/order/multiplicity, and exact exceptions.
6. **Routing/applicability/risk-set relation**: authoritative routing incidence remains separate from response physical state. Missingness never supplies membership by implication.
7. **Coordinate, weight/measure/design, source-relation, authority, dependency, discovery-replay, structural-admission-replay, and replay-manifest relations**: stored in typed columnar relations at their governed logical grain. These are not folded into the response matrix merely to save bytes.
8. **Sparse exact exception relations**: only for fields whose omission/default/derivation has independently proved authority. CCIV itself does not create functional-dependency law owned by R02.
9. **Optional caches/indexes**: state bitmaps, predicate bitmaps, zone maps, bloom filters, respondent selectors, compiled query fragments, and other accelerators. Unless a later authority explicitly elevates one, every such object is `NONAUTHORITATIVE__REGENERABLE_CACHE` and may be deleted without changing any lawful answer.

### 3.2 Two physical geometry profiles, one logical interface

CCIV permits release-local physical specialization based on mechanically proved geometry capabilities, never source-family semantics:

- `AXIS_DENSE`: only where independent authority proves an immutable respondent x question/event coordinate law and exact exception path.
- `EXPLICIT_EVENT`: stores explicit event coordinates where that proof is absent or where topology is non-rectangular.

A release may mix the two by question block. Selection is an ingest-time physical optimization decision validated against the same logical oracle. It is not `if WVS`, `if LiTS`, `if SAV`, or `if DTA` semantics.

### 3.3 Direct decoder-batch -> Arrow compiler

The decoder already yields bounded physical cell batches. CCIV proposes replacing per-cell Python `RespondentEvent` construction on the hot path with batch kernels:

`PhysicalCell batch -> source-authority batch binding -> typed Arrow vectors -> vector invariant checks -> canonical member writers`.

The compiler may vectorize representation and validation; it may not move survey meaning into layout. Source-authority resolution remains exactly the same authority operation as in logical C11. The vector path must reproduce every constructor/integrity invariant and semantic projection observable through the frozen objects. It cannot claim equivalence merely because counts or values match.

Required vector validation classes include: exact reference shape/hashes; allowed typed states; required field presence; response-state == typed-state; authority closure; dependency closure; deterministic canonical set ordering/deduplication; exact canonicalization; reserved-field protection; respondent-universe closure; topology compatibility; replay-manifest closure; duplicate/conflict rejection; and semantic-hash parity against the independent oracle. Any invariant not implemented vectorially forces a slow validated fallback or rejects the vector compiler.

### 3.4 State and predicate bitmaps

The canonical typed physical-state lane may use compact bit-packed codes if and only if it is an information-equivalent encoding of the full physical-state vocabulary. Physical state and semantic response state remain separate lanes.

Predicate-specific bitmaps are never required canonical material. A query may obtain an exact respondent selector by:

1. using a valid cache bitmap whose key includes release identity + exact predicate semantics + authority dependencies; or
2. vector-scanning canonical incidence to construct an ephemeral selector.

Therefore a lawful predicate unseen at ingest remains executable. Cache deletion can only change speed.

### 3.5 Late materialization and respondent set algebra

I03 execution can be implemented behind the common interface as:

1. resolve exact query/predicate/risk-set/measure/source authority;
2. resolve each primitive predicate to an exact respondent selector by bitmap or scan;
3. combine selectors with exact AND/OR/NOT set algebra under the query-defined universe/risk-set, never under storage-local null semantics;
4. resolve exact routing membership and negative/unresolved states;
5. late-fetch only target/question, topology, measure, and provenance columns for surviving respondents;
6. build exact target configurations/joints;
7. construct the same final public `EmpiricalFact` / receipts at the semantic boundary.

NOT is complement relative to the governed respondent/risk-set universe, not file-row absence. Unresolved routing or authority remains an error/state exactly as today.

For k-way targets or pair/k-way cotravel, selected question vectors are aligned by scoped respondent identity/source-row replay coordinate. No pairwise or k-way joint table is required in advance. Tuple construction happens after survivor selection and therefore supports arbitrary combinations.

### 3.6 I05 unforeseen combinations

I05 authority still fixes the exact candidate frontier before data evaluation. CCIV does not encode that frontier at ingest. For any candidate generated later from existing lawful atoms/questions, the execution layer can scan the needed primitive columns, form ephemeral respondent selectors, and evaluate the exact query. Pair cotravel, bounded k-way configurations, reversal grids, recursive subgroup forks, branch-conditioned distributions/cotravel, and cloud-like diagnostics therefore do not require re-ingest or a finite pre-indexed vocabulary.

A cache can accelerate repeated primitives, but absence of a cache cannot prune a candidate, change coverage, or produce `UNEVALUATED` where the frozen I05 contract requires evaluation.

## 4. WHAT_CHANGES_PHYSICALLY

- Hot ingestion becomes column/batch-oriented rather than Python-object/event-row oriented.
- Repeated event columns may be placed on respondent/question axes only when another authority proves the dependency; otherwise they remain explicit incidence.
- Question-oriented blocks replace a monolithic long response fact as the favored hot analytical representation.
- Per-cell physical and semantic states may be compact coded vectors rather than repeated strings/objects.
- Exact non-rectangular event material is stored in explicit typed relations.
- Query execution can produce transient respondent bitsets/selectors and late-materialize target data.
- Release-local physical profiles may differ while exposing the same C11 interface.
- Derived indexes/caches become removable acceleration artifacts.

## 5. WHAT_MUST_NOT_CHANGE_LOGICALLY

Nothing in M01-M18 changes. In particular:

- source snapshot + row ordinal remains irreducible replay identity;
- raw value and authorized canonical value remain distinct;
- physical missingness and semantic response state remain distinct;
- row absence is never substituted for typed source/C11 state;
- routing/applicability/risk-set truth is separately governed;
- topology/multiplicity/order/rank/component/event identity remains reconstructable;
- weight value never substitutes for weight/design/estimand authority;
- authority and ExactRef/content-hash closure remain exact;
- source relation/nonduplication law remains independent of physical co-location;
- I03 failure/negative states remain observable, not normalized to empty/zero;
- I05 complete-frontier semantics remain unchanged;
- I04 receives the same exact empirical facts/receipts and sees no physical profile;
- V553+ never branches on carrier shape.

## 6. INFORMATION_ACCOUNT

The detailed account is in `INFORMATION_PRESERVATION_LEDGER.csv`. The central rule is conservative: CCIV claims no new semantic functional dependency. Information moves off event grain only when immutable release, question-grain, or respondent-grain authority independently proves the determinant; otherwise it is stored directly in typed incidence or an exact sparse exception.

The virtual long view must deterministically reconstruct the complete logical `RespondentEvent` semantic projection, including authority/dependency refs and replay root, then reproduce the same semantic hash/object ID. Column position, Parquet row-group position, filesystem path, or cache bitmap ordinal is never semantic identity.

## 7. ASSUMPTIONS_AND_AUTHORITY

See `ASSUMPTION_LEDGER.csv`. The strongest assumptions are conditional, not asserted facts:

- dense-axis omission is allowed only after R02 or equivalent independent proof;
- vector validation is acceptable only after differential parity with the frozen semantic constructors/integrity laws;
- physical-state code packing is acceptable only if all states/declarations remain invertible;
- late materialization is acceptable only if negative/routing/authority states are resolved before filtering can erase them;
- optional indexes are acceptable only if deletion/rebuild parity is exact.

No raw-source assumption beyond checked-in accepted census/reconnaissance is required for this design return.

## 8. HOSTILE_COUNTEREXAMPLES

The design is intentionally tested against cases that break a simplistic matrix:

- WVS7 Q152-Q157 user-missing incidence and ordered slot distinctions;
- WVS7 D_INTERVIEW non-injectivity and exact Q177-Q181 five-way joints;
- LiTS I ordinary labeled semantic-sentinel values versus Stata system missing, plus three distinct weights with two system-missing rows each;
- overlapping/alias multiple-response sets where shared membership does not authorize deduplication;
- all-row typed-missing columns that must not be elided as useless;
- repeated/ranked/componentized events producing multiple exact events for one respondent/question;
- ordinary blank strings that may not become null;
- compatibility-reader text that remains nonauthoritative for semantics;
- arbitrary NOT over an explicit risk set;
- unseen I05 conjunctions/reversal grids after all predicate caches are deleted;
- high-cardinality/open-text predicates that cannot have a finite bitmap vocabulary;
- cache corruption/staleness and partial-release corruption.

Full cases appear in `HOSTILE_CASES.csv` and `SELF_RED_TEAM.md`.

## 9. I03_I05_I04_EFFECT

**I03:** logical contract unchanged. A backend adapter may use vector scans and respondent-set algebra, but must preserve exact routing resolution, topology reconstruction, target-domain checks, weighting authority, denominator membership, valid-empty/zero/noncomparability/integrity states, and final semantic identity.

**I05:** candidate grammar/frontier remains authority-first and storage-agnostic. CCIV may accelerate repeated leaf evaluation, but no bitmap/index may constrain the frontier. Every candidate remains exactly evaluable from canonical incidence.

**I04:** no physical change is visible. I04 consumes exact empirical facts/query refs and governing authorities. Any CCIV path that changes an `EmpiricalFact` ref/hash/state is a semantic failure before I04.

Historical generalized functionality remains reachable through I03/I05: joints, cotravel, forks, recursive forks, branch-conditioned operations, reversals, co-signatures, cloud-like diagnostics, determinicity-like relations, support/uncertainty, and cross-source/time distinctions.

## 10. INTEGRITY_REPLAY_EFFECT

A sealed CCIV release must hash every authoritative member and declare cache members separately. Reopen verifies the release seal before serving data. Random object reconstruction uses semantic event coordinates / exact refs, not physical row-group location. Full audit streams all canonical members, reconstructs semantic projections, validates authority/replay closure, and compares deterministic aggregate/replay digests.

Vector compiler acceptance requires an independent differential court: logical source fixture -> frozen object constructor/integrity path versus logical source fixture -> CCIV compiler -> virtual reconstruction. Exact semantic projections/hashes, not object count alone, must match.

Deleting all nonauthoritative caches and rebuilding them must leave release identity and all I03/I05/I04 outputs unchanged. Any authoritative member corruption fails closed; cache corruption causes cache discard/fallback, never semantic fallback.

## 11. RESOURCE_EXPECTATION

These are hypotheses for measurement, not acceptance evidence.

Expected wins:

- lower ingest RSS by avoiding millions of Python semantic objects;
- higher compile throughput from Arrow vector kernels and batch validation;
- lower physical bytes where repeated row/question/event keys are lawfully represented by axes;
- lower cold query I/O for few-question I03/I05 workloads via projection pruning;
- faster repeated low-cardinality predicates with exact bitmaps;
- lower materialization cost when restrictive predicates shrink the respondent set early.

Expected losses/risks:

- wide respondent-heavy or many-question joints may read many column groups and lose versus one streaming long scan;
- explicit-event topology can reduce matrix gains;
- too-small question files produce metadata/tiny-file overhead;
- high-cardinality strings defeat bitmap value indexes;
- cache maintenance can consume disk and operational complexity;
- complex backend/profile logic increases test surface.

No storage-ratio claim can win the court by itself.

## 12. COMPLEXITY_COST

CCIV is substantially more complex than streaming long. It adds a physical planner, release-local geometry profiles, vector validation kernels, virtual reconstruction, selector algebra, cache invalidation, and two-way hostile equivalence testing. It creates more ways to be fast and wrong.

The complexity is acceptable only if it removes a demonstrated blocking resource path or produces a clearly material end-to-end gain under the whole hostile workload. If lower-risk streaming-long is sufficiently practical, this complexity is unjustified.

## 13. RAW_SOURCE_PROBES_IF_ANY

`NO_RAW_SOURCE_PROBE_PERFORMED__CHECKED_IN_CENSUS_AND_RECONNAISSANCE_SUFFICIENT`

The accepted SR03 35-source census, WVS/LiTS hostile fixture, SOURCE_BYTE_INVENTORY, accepted SR09-PRE cross-corpus reconnaissance, R4 authorities, and frozen code contracts establish the physical heterogeneity needed for this design. No named unresolved layout/type/cardinality/topology question required reopening raw bytes.

## 14. REASONS_TO_REJECT_OWN_PROPOSAL

Reject CCIV and choose simpler streaming-long if any of the following holds:

1. streaming-long passes all semantic/oracle tests and hard resource gates with comfortable operational margin;
2. CCIV's improvement is primarily compression rather than end-to-end compile/reopen/query/discovery benefit;
3. joint-heavy or I05 hostile workloads materially regress because too many question blocks must be touched;
4. the vector compiler cannot reproduce every semantic constructor/integrity invariant independently;
5. non-rectangular topology forces so much explicit-event storage that the matrix layer becomes decorative complexity;
6. cache/index invalidation cannot be made obviously removable and fail-safe;
7. physical-profile branching leaks into I03/I05 meaning;
8. deterministic virtual reconstruction is harder to audit than streaming-long without a compensating material benefit;
9. maintaining two physical geometry profiles creates disproportionate testing/operations burden;
10. any required omission depends on unproven functional dependency.

## 15. FALSIFICATION_CONDITIONS

CCIV is falsified as an acceptable replacement if one hostile fixture produces a different logical C11 projection/ref/hash/state; if any lawful I03 predicate cannot be evaluated without a prebuilt index; if an unforeseen I05 candidate requires re-ingest; if cache deletion changes a result; if routing state can be mistaken for missingness; if a topology/event can no longer be reconstructed; if weighted/design authority changes; if source-local profile selection changes semantics; if corruption can return a plausible answer rather than fail closed; or if a simpler passing design is operationally adequate and CCIV lacks material measured benefit.

A proposed comparison threshold for HQ synthesis: absent a hard-gate failure in the simpler design, CCIV should demonstrate either (a) at least a 2x improvement on a currently blocking end-to-end metric, or (b) at least ~35% improvement on two primary resource/performance metrics with no required hostile workload regressing more than ~25%. These numbers are a proposed court rule, not frozen law; HQ may replace them before benchmarking.

## 16. SYNTHESIS_REQUIREMENTS

HQ synthesis should combine this return with:

- R01 streaming/memory design as the mandatory lower-risk baseline;
- R02 grain/type/locator proofs before accepting any axis omission or implicit locator;
- R03 independent semantic oracle as the acceptance authority for any replacement;
- R05 integrity/replay/minimality findings, especially cache authority and proof surface;
- R06 benchmark/operational design for final measurement.

No CCIV functional dependency should be accepted merely because this return sketches it. No vector validation should be accepted merely because current R4 reconstructs through `RespondentEvent`. The final court must be representation-independent.

## 17. RECOMMENDATION

`RECOMMEND__RETAIN_AS_CLASS_C_CHALLENGER__DO_NOT_ADOPT_BY_DEFAULT`

CCIV is the strongest plausible endgame architecture I can justify without moving semantics into physical layout: hybrid question-oriented typed incidence, explicit non-rectangular event relations, exact respondent-set algebra, late materialization, and removable bitmaps/indexes behind a uniform virtual C11 interface.

It should proceed to a bounded comparison court only. If R01's simpler streaming-long carrier passes the complete independent oracle and resource gates with sufficient margin, reject CCIV. If the simpler design still hits a blocking real-scale resource wall, CCIV is the next serious candidate because it attacks object materialization and unnecessary long-row I/O while preserving open-world I05 combinations.

Required token: `POST_R4_R04_COLUMNAR_VECTOR_RETURNED`
