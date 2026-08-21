# R06 Proposal — Adversarial Minimality Gate for Post-R4 Synthesis

## 0. Standing

R06 proposes **no preferred implementation**. This document is a hostile decision protocol for HQ synthesis.

The central rule is:

> A mechanism is not admitted because it is exact, elegant, modern, or locally faster. It is admitted only when the simpler candidate is insufficient in the complete machine and the added mechanism closes a named deficiency without opening a larger proof/maintenance surface.

Authority 52 already establishes the presumption hierarchy: Class A before Class B, Class B before Class C, and a stop rule once exactness, resources, practical query/replay behavior, and maintainability are closed. R06 makes that hierarchy operational and adversarial.

---

## 1. Cross-source hostile assumption matrix

| Hostile assumption | Accepted counterexample(s) | Candidate families endangered | Required synthesis law |
|---|---|---|---|
| Equal raw vectors imply one semantic/physical variable | WVS W4 `V220` vs `Q223_LOCAL`; WVS W7 `Q223` / `Q223_ABREV` / `Q223_LOCAL` | C03, C07, C09, C12, C21 | Preserve variable identity, labels/dictionaries, declarations, topology, and authorities separately; equality is not FD proof |
| Equal/overlapping MR membership implies one set | Asian Barometer W5 `Q112`/`SE15`; EVS 2008 alias/overlap sets | C03, C07, C09, C10, C21 | Preserve native set identity, membership, multiplicity, order, label/provenance independently |
| Zero observed user-missing incidence means declaration can be dropped | Afrobarometer R9 `Q78F` declares `-1` while source observes zero user-missing cells | C03, C05, C07, C12, C21 | Declaration metadata and incidence remain independent |
| A source/variable can have one missingness policy | Arab Barometer W2 `q2062`; LiTS III `q112_1`; LiTS IV `q1032`; South Asia W1 code 8 | C05, C07, C10, C12, C21 | Physical missing class is cell/variable-specific; ordinary absence-looking values remain ordinary |
| Blank string is null/absence | Arab Barometer W8 `BLOCK_ID`: 2,408 ordinary empty strings, zero system missing | C05, C10, C12, C21 | Raw string value lane must preserve valid empty independently of null/missing |
| A native respondent ID is reliable and unique | South Asia W1 no evident ID; Arab Barometer W8 `ID=0` repeats 2,400 times; WVS W4 V3 has typed missing/collisions | C06, C19, C20, C21 | Replay identity remains source snapshot + source row ordinal unless stronger mapping is proved |
| Physical row/column position is semantically stable | Any repartition/row-group/parallel merge; source ordinals are frozen but carrier positions are not | C06, C08, C15, C19, C21 | Derived identities must be functions of immutable source/C11 identifiers, never mutable carrier ordering |
| One canonical question column is sufficient | Native MR aliases; repeated/ordered/ranked/componentized topologies; mirrored LiTS respondent modules | C09, C10, C11, C21 | Canonical question is additive; source variable/component/set/order/module dimensions remain reconstructable |
| Routing is reducible to null patterns | LiTS IV 134 `*_skip` variables + visit blocks; routing authority explicitly distinct from physical absence | C09, C10, C11, C13, C21 | Routing carriers and governed applicability remain separate from physical missingness |
| Weight candidates can be coalesced or defaulted by shape | WVS W1 has 13 complete weight-like variables; LiTS IV base/top-up weight missingness is complementary | C03, C09, C13, C20, C21 | Keep every physical candidate and authority; no implicit default or combination |
| Storage/display metadata can be inferred from values | WVS W1 `S007`: F2.0 display metadata while raw magnitudes are much larger | C03, C05, C12, C21 | Raw value and display/storage declaration remain separate |
| SPSS logical variable count equals storage-slot count | Arab Barometer W5/W8 continuation storage slots | C08, C20, C21 | Decoder freezes physical continuation/storage metadata before neutral logical compilation |
| Header dimensions can safely drive physical iteration | Latinobarometro 2024 SAV header/dictionary width inconsistency | C08, C20, C21 | Compiler uses governed decoder contract and hostile fixture, not one convenience header field |
| Text encoding is a source-global UTF-8 fact | Asian Barometer W1 BIG-5; EVS/LiTS frozen latin1 compatibility; LiTS reader-report conflict; Arab Barometer W1 literal C1 controls | C05, C08, C12, C20, C21 | Reader configuration provenance, decoded text, and text authority remain distinct |
| Reader options are interchangeable implementation detail | LiTS IV option interaction can fail under one date/missing configuration | C08, C20 | Source-local execution differences may exist only behind frozen decoder contract; not semantic authority |
| Rectangularity can be presumed because source file is rectangular | Topology/multiplicity/rank/routing/module structure is nonrectangular at semantic event level | C09, C10, C11, C21 | Matrix representation must carry enough topology to reconstruct every logical event exactly |
| All-row typed-missing / constant columns are useless | Accepted SR09-PRE establishes all-row typed-missing columns as replayable physical evidence | C03, C07, C09, C12, C13, C21 | Constant/typed-missing elision requires explicit determinant + declaration retention + exact reconstruction |

### Matrix conclusion

Functional-dependency compaction is admissible only when the dependency is **declared or empirically certified at the correct information grain**. Coincidence of observed values is evidence of compression opportunity, not evidence that information can be erased.

---

## 2. Hidden-coupling map

The physical replacement sits inside a dependency chain. Local savings can create global coupling:

```text
source bytes / exact source digest
    |
    v
format decoder + frozen execution configuration
    |-- source row ordinal
    |-- source variable ordinal/name
    |-- raw typed value
    |-- physical missing class + declaration
    |-- labels/storage/display/text metadata
    |-- MR/repeated/ranked/topology metadata
    v
physical carrier
    |-- relation/default/override tables
    |-- typed lanes/dictionaries
    |-- locator derivation
    |-- partition/chunk/root identity
    v
SINGLE invariant-checked C11 materialization boundary
    |-- ExactRef/content identity
    |-- RespondentIdentity
    |-- RespondentEvent / coordinate / routing / weight objects
    |-- topology / semantic authority links
    |-- ReplayManifest
    v
I03 exact queries ---- I05 discovery ---- I04/structural admission
    |                     |                    |
    +---------- exact risk sets / conjunctions / replay ----------+
    v
publication / cache / branch replay / audit
```

### Couplings synthesis must make explicit

| Coupling | Hidden failure if treated independently | Adversarial requirement |
|---|---|---|
| Locator derivation ↔ partition/order | Same event receives new identity after row-group or parallelism change | Locator function depends only on immutable source/C11 determinants; vary partition/thread count in determinism test |
| Defaults/overrides ↔ declaration grain | A default inferred from majority incidence erases exceptional declaration/label/topology state | Default is an encoding of a proven determinant, not semantic authority; exceptions are exhaustive and audited |
| Dictionary dedupe ↔ labels/missing/topology | Equal values cause metadata views to collapse | Dictionary identity includes every field required for exact reconstruction or dictionaries remain separate |
| Typed lanes ↔ uniform query semantics | Query engine accidentally interprets physical lane/null rather than governed response state | C11 facade reconstructs neutral event first or exposes a single audited vectorized equivalent with parity proof |
| Question partition ↔ respondent conjunction | Arbitrary k-way query becomes multi-partition join whose risk-set semantics drift | Partitioning is physical only; exact respondent/event identity and cross-partition join contract are mandatory |
| Bitmap vocabulary ↔ unforeseen I05 | Unindexed state/query silently becomes unqueryable or requires source reingest | Bitmap is regenerable accelerator; canonical incidence remains sufficient for arbitrary predicates |
| Late materialization ↔ constructor invariants | Virtual object bypasses `__post_init__`, validation seal, authority closure, or ExactRef hash | One construction/materialization API; no downstream direct fabrication from compressed fields |
| Source-local compiler ↔ neutral downstream | Source family branches leak into I03/I05 and become semantic divergence | Source specialization terminates before frozen neutral C11; parity runner rejects divergent logical output |
| Cache key ↔ semantic frontier | Stale cache passes because source digest same while schema/config/code/authority changed | Cache key includes all reconstruction determinants and fails closed on mismatch |
| Parallel build ↔ override merge | Thread/partition scheduling changes winner/order/hash | Stable source ordinals + deterministic merge law; randomized thread/partition determinism court |
| Chunk integrity ↔ publication root | Member passes local checksum but belongs to another release | Every member/chunk is bound to immutable release/root identity; no orphan member accepted |
| Multiple integrity layers ↔ recovery law | Whole hash, Merkle, Parquet checksum disagree with no precedence | Each integrity layer has one named failure granularity and precedence; otherwise delete redundant layer |
| Hot/cold split ↔ exact query/replay | `cold` metadata is skipped by fast path and later becomes unavailable to I05/replay | Cold is storage temperature only, never authority class; one exact read path can rejoin all required state |

---

## 3. Source shapes that defeat naïve functional-dependency compaction

The following shapes are not hypothetical. They are derived from accepted corpus evidence and frozen hostile fixtures.

### FD-1 — Equal raw vector, distinct dictionaries/views

Shape:

```text
(row -> raw_value) identical
variable_identity different
label_dictionary different
possibly display/topology authority different
```

Counterexample: WVS W4/W7 parallel country-local/abbreviation variables.

**Defeats:** dedupe on vector hash; normalize variable metadata by observed values; question-only matrix column dedupe.

**Law:** the determinant must include native variable identity and every semantically required declaration. If that eliminates the expected savings, do not normalize.

### FD-2 — Zero incidence, nonzero declaration

Shape:

```text
all observed cells ordinary
user_missing_declaration = present
```

Counterexample: Afrobarometer R9 Q78F.

**Defeats:** sparse omission based on observed incidence; all-zero bitmap elision; deriving declaration from fact stream.

### FD-3 — Same code/label, different physical class

Shape:

```text
code=8 label="No opinion"
variable A -> ordinary
variable B -> FORMAT_USER_MISSING_VALUE
```

Counterexample: South Asia W1.

**Defeats:** source-global codebook; global missing bitmap keyed by numeric code; dictionary dedupe ignoring variable declaration.

### FD-4 — One variable contains true missing plus ordinary absence-looking value

Counterexamples: Arab Barometer W2 q2062; LiTS III q112_1; LiTS IV q1032.

**Defeats:** nullification of refusal/DK codes; physical-missing inference from semantic-looking labels; source/variable-level missing policy.

### FD-5 — Empty string is an ordinary coordinate

Counterexample: Arab Barometer W8 BLOCK_ID.

**Defeats:** null/blank coalescing in Arrow/Parquet string lanes; sparse omission of empty strings.

### FD-6 — Alias/overlap topology

Shape:

```text
set A members ==/overlap set B members
set A identity != set B identity
```

Counterexamples: Asian Barometer W5; EVS 2008.

**Defeats:** MR-set dedupe by member list; topology reconstruction from columns alone.

### FD-7 — Identity candidate is absent, colliding, or typed missing

Counterexamples: South Asia W1; Arab Barometer W8; WVS W4.

**Defeats:** compaction around guessed respondent key; sorting/repartitioning under an unstable native key.

### FD-8 — Weight surfaces have shared shape but distinct estimands/roles

Counterexamples: WVS W1 weight-like multiplicity; LiTS IV base/top-up complementarity.

**Defeats:** one default weight; null-pattern-based coalescing; source-local compiler selecting a weight implicitly.

### FD-9 — Physical storage declaration differs from apparent logical shape

Counterexamples: SPSS continuation storage slots in Arab Barometer; Latinobarometro 2024 width inconsistency; WVS display/raw magnitude mismatch.

**Defeats:** compiler that derives source physical structure from one header count, display format, or dataframe dtype.

---

## 4. Query/discovery capabilities endangered by question-oriented / vectorized / bitmap layouts

The following capabilities are part of the terminal demand envelope and cannot be made second-class merely to optimize storage.

### Q1 — Arbitrary respondent-grain conjunctions and k-way joints

Question partitioning turns an event scan into cross-partition joins. That may be good physically, but the carrier must preserve exact respondent identity and source/risk-set semantics so that:

- conjunctions across arbitrary questions;
- contradictions/reversals;
- k-way joint distributions;
- branch cohorts;
- source-indexed multi-universe queries

remain exact. A benchmark showing fast single-question marginal scans is irrelevant to this obligation.

### Q2 — Unforeseen I05 discovery predicates

A finite persistent bitmap vocabulary cannot become the canonical empirical substrate. I05 must be able to formulate a predicate not anticipated at ingest without reingesting source bytes or silently degrading to unavailable.

**Admissible:** bitmap cache derived from canonical incidence and discarded/rebuilt freely.

**Not admissible:** bitmap truth whose omissions define what discovery can ask.

### Q3 — Risk-set / routing semantics

Physical null/missingness cannot define eligibility. Exact queries may need whole-question, common-eligible, routed-applicable, anchor-selected, branch-cohort, or governed custom risk sets. Routing carriers and their authority must remain independently retrievable.

### Q4 — Multiplicity, order, rank, componentization

A matrix cell `(respondent, question)` is insufficient when one question can yield multiple ordered/repeated/ranked/componentized events. A Class C coordinate system must include enough dimensions to reconstruct distinct events and their source-native topology.

### Q5 — Weights/design variables as first-class physical evidence

Weight or design columns that look metadata-like cannot be relegated to a side store inaccessible to generic query/replay. Exact weighted queries require the selected governed weight basis while preserving all competing physical candidates.

### Q6 — Exact replay of selected events

A virtual long facade is acceptable only if a selected logical event can be deterministically reconstructed to source snapshot, source row ordinal, source variable identity, physical state/declaration, topology, and authority links without relying on current partition order.

### Q7 — Comparator/structural/discovery replay

The current C11 replay surface contains exact predicate, comparator, discovery-branch, and structural-admission bindings. A replacement that optimizes only RespondentEvent storage but cannot reconstruct these closure refs is not a replacement of the complete logical release.

---

## 5. Integrity / replay failure modes

| Failure mode | Cause | Fail-closed requirement |
|---|---|---|
| Stale cache resurrection | cache keyed only by source/release name | key/cache receipt includes exact source content + schema/compiler/config/frontier determinants; mismatch = miss, never fallback |
| Cross-release chunk splicing | chunk hash valid but root binding absent | member identity includes/binds immutable release root; root manifest enumerates exact members |
| Partial publication becomes visible | files written before release seal | atomic publication marker/root manifest written only after all members verified; readers ignore unsealed prefix |
| Mutable manifest | manifest overwritten in place | content-addressed immutable manifest/root; new release creates new identity |
| Partition-dependent replay | locator derived from row-group/file index | locator derives from immutable source/C11 ordinals/refs; repartition court |
| Nondeterministic override winner | parallel merge/order not frozen | stable deterministic merge and duplicate/conflict rejection |
| Cache becomes second canonical truth | downstream reads cache with no derivation receipt | caches are regenerable, non-authoritative, identity-bound; canonical read remains sufficient |
| Integrity disagreement ambiguity | Merkle/member/file/Parquet checks disagree | define precedence/failure granularity; delete layers with no independent function |
| Silent schema evolution | old reader interprets new lanes/defaults | exact schema/version in root and materializer; unsupported version fails closed |
| Source-local replay divergence | specialized compiler emits different logical C11 | same one-runner equivalence oracle; source family invisible downstream |
| Rebuild non-equivalence | build uses ambient library/thread/compression behavior | freeze semantic determinants; compare semantic/root receipts across rebuild; byte identity required only where contract requires it |
| Integrity checks only bytes, not semantic closure | artifact bytes intact but wrong authority/config/source bound | root receipt binds semantic frontier/config/source identities in addition to member content |

### Minimal integrity law

Prefer the smallest layer set that detects the named failures:

1. immutable release/root manifest;
2. exact member identities/hashes sufficient to bind all canonical members;
3. deterministic semantic/replay identity receipt;
4. fail-closed reader that refuses missing/mismatched/partial members.

Add a Merkle tree only if chunk-level independent verification, partial remote fetch, repair, or scale creates a measured need that cannot be met by the root + member identities already required.

---

## 6. Constructor / invariant bypass hazards

Read-only inspection at the starting HEAD establishes useful current boundaries:

- `C11LogicalRelease` requires a private validation seal.
- `C11Repository._commit_validated` rejects unvalidated releases.
- exact object resolution has no latest/fuzzy fallback.
- C11 internal records validate exact refs, typed absence, authorities, hashes, and approved record families.
- I03 consumes exact C11 objects and exact risk/target/authority references.

R06 found no evidence sufficient to declare a current bypass bug. The replacement hazard is architectural: compressed or virtual representations often add convenience constructors that can accidentally become an alternate semantic ingress.

### Required boundary

Every replacement must provide exactly one audited logical materialization boundary:

```text
physical row/chunk/vector/matrix coordinate
       |
       v
validate physical identity + schema + root membership
       |
       v
reconstruct all required C11 fields
       |
       v
invoke the same invariant-checked semantic/internal record construction law
       |
       v
return exact identity-bearing C11 object/event
```

Forbidden bypasses:

- `dict`/row → downstream semantic use without C11 validation;
- constructing partial `RespondentEvent` equivalents whose omitted fields are recovered opportunistically later;
- `model_construct`/unsafe deserialization-style bypasses if introduced;
- direct use of physical null/bitmap state as governed response/routing state;
- materializers that compute ExactRef from physical row position rather than semantic projection/source identity;
- alternate fast-query code path with semantics not shared by the normal C11 path;
- accepting cache objects lacking canonical derivation/root receipt.

---

## 7. Maintenance / complexity traps

### M1 — Representation multiplication

Canonical long + normalized relations + columnar matrix + persistent bitmap + hot/cold metadata + cache DB is not one optimized carrier. It is a synchronization system. Every extra representation adds migration, invalidation, integrity, replay, and debugging state.

### M2 — Join-graph inflation

C03 + C07 + C13 can turn a self-contained event reconstruction into mandatory joins across source/release/variable/question/default/exception/cold tables. Storage savings must be net of reopen/query CPU, code complexity, and corruption surface.

### M3 — Encoding policy combinatorics

C05 typed lanes + C12 adaptive per-variable encoding + C08 vectorized compiler + C20 source-specialization creates a cross-product of source family × type × missingness × encoding × compiler path. The burden grows faster than the byte savings.

### M4 — Cache invalidation graph

Identity cache + bitmap cache + query cache + materialized partitions each need exact invalidation determinants. One immutable compute cache may be useful; a hierarchy of caches becomes a shadow database.

### M5 — Parallelism before boundedness

Parallel build can reduce wall time while increasing RSS, nondeterministic merge behavior, temporary storage, and debugging burden. First establish bounded deterministic serial mechanics. Parallelism is escalation, not baseline.

### M6 — Integrity ornamentation

Merkle trees are not inherently more correct than a simpler immutable root/member hash scheme. They earn their keep only when partial verification/repair/fetch granularity is a real system requirement.

### M7 — Source-local cleverness

A custom compiler for each corpus may look efficient because each source is locally regular. Across 35 heterogeneous files, it converts physical heterogeneity into permanent code heterogeneity. Source-local handling belongs in the decoder or a narrowly bounded compiler stage and must converge immediately to one neutral contract.

### M8 — Optimization-specific public abstractions

Do not create new public semantic families such as `VirtualQuestionColumn`, `BitmapTruth`, or `MatrixEvent` merely because a physical representation exists. The public ontology should not remember the optimization.

---

## 8. `DO_NOT_COMBINE` list

The following combinations are presumptively rejected. HQ may override only with a named measured failure and a proof that the combination, not one constituent, is necessary.

1. **C21 + C09 + persistent-C10 + C11** — canonical matrix + question partitions + bitmap truth + late materialization creates four interdependent representations of the same incidence.
2. **C03 + C07 + C13 over the same fields** — true-grain normalization + defaults/overrides + hot/cold split can create a reconstruction join labyrinth.
3. **C06 + C19 + C15** — derivable locators + row-position identity + parallel/partitioned build risks identity drift under layout change.
4. **C05 + C12 + C08 + C20** — typed lanes + adaptive encoding + vectorized compiler + source-local compiler creates a combinatorial compiler matrix.
5. **C14 Merkle + whole-artifact root hash + independent per-member hash + format checksum** absent a named distinct failure granularity — redundant integrity layers.
6. **C04 cache + persistent-C10 bitmap + hidden DB/index** — multiple regenerable accelerators can become competing canonical truths.
7. **C15 parallelism + unresolved override/default merge order** — nondeterministic replay.
8. **C13 cold metadata + C09 partitioning when I05/replay needs both** — fast path starves exact path.
9. **FD compaction from vector equality + dictionary dedupe** — WVS accepted counterexamples directly refute this inference.
10. **MR membership dedupe + question-oriented columns** — alias/overlap set identity can disappear twice.
11. **Implicit null-based routing + bitmap absence acceleration** — physical missingness gets promoted into eligibility authority.
12. **Source-local compiler + downstream source branches** — physical specialization escapes its boundary and fractures the machine.
13. **Multiple cache layers + mutable publication alias** — stale-but-valid artifacts become impossible to distinguish from current truth.
14. **Row-position event IDs + repartitionable Parquet tuning** — harmless tuning becomes semantic identity migration.

---

## 9. Exact conditions under which streaming-long is sufficient and should win

Streaming-long **wins and synthesis stops** when all conditions S01–S12 are true in the accepted full-source court:

### S01 — Complete physical exactness

All governed source-native fields/states required by the constitution and decoder contract survive build/reopen/reconstruction, including rare declarations with zero incidence, typed missing states, ordinary absence-looking values, empty strings, topology, routing carriers, weights/design variables, labels/types/storage/display metadata, and source ordinals.

### S02 — One C11 semantic boundary

Every logical event/object used downstream is reconstructed through one invariant-checked C11 materialization law; no optimization-specific semantic ingress exists.

### S03 — Exact I03 parity

Exact respondent-grain distributions, arbitrary conjunctions/k-way joints, risk sets, routing, weighted execution, target topology, reversals/contradictions, and source-scope modes match the independent accepted oracle.

### S04 — Exact I05/I04 capability

Discovery can formulate unforeseen predicates over the canonical incidence without source reingest or finite predeclared bitmap/query vocabulary; structural-admission/replay closure remains exact.

### S05 — Replay identity stability

Source/replay identity remains based on immutable source snapshot/row and exact logical refs, independent of carrier file, row group, sorting, compression, or thread count.

### S06 — Fail-closed integrity/publication

Canonical artifacts are immutable, exact-member/root bound, deterministic at the contracted level, refuse partial/mismatched reads, and have one canonical truth with only regenerable caches.

### S07 — Bounded memory mechanics

No corpus-scale all-event Python retention is needed for ingest, reopen, audit, replay, or core queries. Partition/batch bounds are explicit and stable.

### S08 — Resource gates close

Measured full-source results satisfy the governing hard limits and, absent a documented exception, preferred margins:

- peak RSS preferred `<2 GiB`, hard `4 GiB`;
- WVS carrier preferred `<=2 GiB`, hard `4 GiB`;
- LiTS carrier preferred `<=1.5 GiB`, hard `3 GiB`;
- CLOSED_35 projected/confirmed preferred `<=20 GiB`, hard `32 GiB`.

### S09 — Whole-workflow runtime is practical

Build + reopen + representative I03 + I05 + replay/reconstruction + integrity verification are practical on the target workstation. No single favored kernel is allowed to substitute for this court.

### S10 — Source neutrality downstream

No source-family branches are required in I03/I05/I04/V553-facing logic. All source-specific physical handling terminates before the neutral C11 boundary.

### S11 — Maintainability closes

The representation has a small number of deterministic mechanisms, direct diagnostics, bounded migration/version rules, and no multi-representation synchronization burden.

### S12 — Marginal-optimization stop rule

Every remaining proposed mechanism improves only an already-acceptable number (bytes, RSS, or speed) rather than closing a hard/practical/exactness/integrity gate.

**Disposition:** if S01–S12 hold, Class B/C escalation is overengineering. Streaming-long should win even if a Class C prototype is smaller/faster in isolation.

---

## 10. Exact conditions under which Class C is genuinely justified

Class C is justified only when **all** J01–J13 hold. Failure of any item returns the burden to the proposer.

### J01 — Lower-risk failure is measured

Class A plus any obviously narrow Class B mechanisms were tested first and fail either:

- a hard storage/RSS gate; or
- practical whole-workflow I03/I05/replay/reopen/build feasibility.

“Could be faster/smaller” is not failure.

### J02 — Failure is not an implementation accident

The lower-risk failure cannot be cured by obvious bounded streaming, merge-read, Parquet row-group/compression tuning, removal of eager reopen, or one narrow proven normalization.

### J03 — Class C materially cures the failing dimension

A bounded hostile pilot demonstrates a material whole-workflow improvement on the failed dimension, not merely a microbenchmark win.

### J04 — Event reconstructability is complete

Every logical event can be reconstructed exactly with raw typed value, physical state/declaration, native identities/ordinals, topology/multiplicity/order/rank/component, routing/weight/design links, labels/types as required, authority refs, and ExactRef/content identity.

### J05 — Nonrectangular topology survives

Alias/overlap MR sets, repeated/ranked/ordered/componentized events, mirrored modules, and routing surfaces are representable without forcing false `(respondent, canonical_question)` uniqueness.

### J06 — Arbitrary query/discovery remains possible

Arbitrary conjunctions and unforeseen I05 predicates remain answerable from canonical stored information without source reingest or a finite indexed vocabulary.

### J07 — Metadata is not a hidden second truth

All metadata needed to reconstruct/query/replay the canonical representation is root-bound and first-class. Side metadata stores cannot silently become more authoritative than the incidence carrier.

### J08 — Identity is layout-independent

Repartitioning, row-group tuning, chunking, compression, or thread-count changes do not change logical/replay identity.

### J09 — One canonical truth remains

Matrices/bitmaps/query projections/caches are either canonical by explicit acceptance or regenerable from the accepted canonical representation. There is no persistent shadow database whose divergence needs reconciliation.

### J10 — Source-specialization converges

If source-local compilers exist, every one produces the same audited neutral C11 contract, and no source-family logic leaks downstream.

### J11 — Integrity/replay is fail-closed

Immutable root/release identity binds all members/chunks/config/schema/frontier determinants needed for exact replay. Partial, stale, cross-release, or mismatched inputs fail closed.

### J12 — Complexity cost is bounded and measured

Implementation surface, migration/version rules, cache invalidation, test matrix, debugging/recovery path, and operator burden are materially acceptable compared with the lower-risk design.

### J13 — Heterogeneous-source hostile court passes

The design passes WVS/LiTS and the accepted SR03/SR09 family hazards, including SAV/DTA missingness, string/date/storage heterogeneity, MR aliases, identity failures, encoding compatibility, routing, weights, and topology drift.

**Disposition:** Class C is an exception justified by demonstrated necessity. It is never the default end state.

---

## 11. Proposed minimum one-runner integration-contract skeleton

This is a contract skeleton, not production implementation.

```python
def run_post_r4_candidate(
    *,
    exact_source_manifest,
    candidate_config,
    accepted_authority_frontier,
    exact_query_suite,
    replay_selection,
    resource_limits,
):
    source = verify_exact_source_digest(exact_source_manifest)
    decoder = open_governed_source_native_decoder(
        source,
        accepted_authority_frontier,
    )

    build_receipt = build_canonical_bounded(
        decoder=decoder,
        config=candidate_config,
        forbid_all_events_python_retention=True,
    )

    root = seal_immutable_release(
        build_receipt=build_receipt,
        source=source,
        config=candidate_config,
        authority_frontier=accepted_authority_frontier,
    )

    reader = reopen_exact_release(root)

    # There is exactly one logical materialization boundary.
    c11 = open_validated_c11_facade(reader)

    reconstruction_receipt = audit_hostile_reconstruction(
        c11,
        accepted_source_native_oracle=True,
    )

    i03_receipt = run_exact_I03_suite(c11, exact_query_suite)
    i05_receipt = run_exact_I05_suite(c11, exact_query_suite)
    i04_receipt = run_exact_I04_closure(c11, exact_query_suite)

    replay_receipt = replay_selected_events_to_source(
        c11,
        source,
        replay_selection,
    )

    integrity_receipt = verify_root_membership_and_fail_closed_behavior(root)
    determinism_receipt = rebuild_with_partition_and_thread_variants_and_compare(
        source,
        candidate_config,
    )
    resource_receipt = verify_whole_workflow_resources(resource_limits)

    return one_atomic_acceptance_receipt(
        root=root,
        build=build_receipt,
        reconstruction=reconstruction_receipt,
        i03=i03_receipt,
        i05=i05_receipt,
        i04=i04_receipt,
        replay=replay_receipt,
        integrity=integrity_receipt,
        determinism=determinism_receipt,
        resources=resource_receipt,
    )
```

### Runner law

The runner must enforce:

1. exact starting source hash, no name/latest fallback;
2. governed format-reader configuration;
3. bounded ingest/reopen/audit;
4. one canonical release truth;
5. one invariant-checked C11 facade/materializer;
6. no direct downstream physical-row semantics;
7. exact I03/I05/I04 interfaces;
8. selected event reconstruction to source-native truth;
9. deterministic behavior under partition/thread/layout changes;
10. fail-closed root/member/config/schema/frontier checks;
11. full workflow RSS/storage/runtime receipts;
12. identical test corpus/query/replay court across candidate families.

The runner is deliberately representation-neutral. If a candidate needs a special acceptance runner to look good, that is itself evidence of hidden semantic coupling.

---

## 12. Mechanisms synthesis should delete as redundant or ornamental

Delete these unless a named measured failure independently requires them:

1. **Persistent canonical bitmap layer** if canonical incidence already meets query gates.
2. **Canonical question partition layer** if Parquet pruning/streaming is practical.
3. **Virtual-event matrix facade** if long-form reopen/materialization is already practical.
4. **Source-specialized physical compilers** if one neutral bounded compiler meets gates.
5. **Merkle tree** if immutable root + exact member hashes already provide the required verification/fetch granularity.
6. **Telemetry framework** beyond a small fixed receipt of RSS, bytes, rows/events, build/reopen/query/replay timings, hashes, and failure counters.
7. **More than one persistent cache tier** absent an independently measured workload need.
8. **Duplicate normalized provenance tables** whose byte savings are immaterial relative to join/proof burden.
9. **Adaptive encoding policy engine** if ordinary Parquet encoding/compression tuning closes storage/runtime gates.
10. **Parallel scheduling layer** if deterministic bounded serial build is practical.
11. **Hot/cold semantic split** if exact query/replay routinely requires mandatory rejoin.
12. **Derived locator machinery** if storing the exact immutable locator costs little and removes proof burden.
13. **Defaults/override layer for low-redundancy fields** where exception bookkeeping approaches direct storage cost.
14. **Optimization-specific public object types**. Physical representation must remain below frozen semantic boundaries.
15. **Second publication database/index** when the immutable canonical artifact + regenerable index/cache is sufficient.
16. **Any compression based on observed equality alone**. Without a determinant certificate it is semantic speculation disguised as storage engineering.

---

## 13. Minimum viable synthesis

HQ should begin synthesis from the following **mechanism budget**, not from a union of R01–R05 proposals:

### Mandatory laws, not optional features

- frozen source-native exactness;
- bounded-memory construction/reopen;
- one canonical copy;
- one validated C11 materialization boundary;
- exact replay/source identity independent of physical layout;
- immutable fail-closed release identity;
- deterministic acceptance receipts;
- whole-workflow integration runner.

### Lowest-burden mechanisms worth presuming

- C01 streaming override/build writes where current implementation retains corpus-scale structures;
- C02 bounded merge/read/audit where reopen is eager;
- C16 empirical Parquet row-group/compression tuning;
- C17 minimal resource/receipt telemetry;
- C04 one immutable identity cache only if repeated identity computation is measured material;
- C18 as the **law** of one canonical truth + regenerable caches, not as another storage layer.

### Escalation pool, not baseline

C03/C05/C06/C07/C12/C13/C15 only after measured deficiency and exact determinant proof. C08/C09/C10-canonical/C11/C14/C19/C20/C21 only after all Class-C admission criteria.

### Final anti-overengineering rule

The synthesis target is not the smallest possible carrier or the fastest possible query engine. It is the **least complicated physical system that preserves the complete frozen empirical machine and closes the actual workstation resource court**. Once that exists, further physical cleverness is liability unless a new hard requirement appears.
