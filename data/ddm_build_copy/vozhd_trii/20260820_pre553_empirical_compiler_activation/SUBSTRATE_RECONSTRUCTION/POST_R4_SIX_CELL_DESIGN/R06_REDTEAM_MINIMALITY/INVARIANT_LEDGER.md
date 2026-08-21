# R06 Invariant Ledger

## Purpose

This ledger enumerates invariants touched, threatened, relied upon, or intentionally left unchanged by post-R4 physical replacement synthesis. R06 changes no invariant and proposes no new semantic authority. It identifies what every candidate must preserve and where apparently local physical optimizations can violate whole-machine law.

Legend:

- **RELIED** — already governing and assumed by R06.
- **THREATENED** — candidate family can violate it if admitted without proof.
- **TOUCHED** — physical representation may change while invariant must remain observationally identical.
- **UNCHANGED** — synthesis has no authority to revise it.

---

## I01 — Exact source-content identity

**Status:** RELIED / UNCHANGED

Every ingest/replay begins from the exact governed source artifact/content identity. File name, wave label, path, or latest version is not sufficient.

**Threats:** C04 stale cache; C14 orphan chunks; C20 source-specialized compiler using ambient source assumptions; mutable publication aliases.

**Required proof:** source digest is verified before build/replay and bound into the immutable release/root receipt.

---

## I02 — Source row ordinal is replay identity substrate

**Status:** RELIED / TOUCHED / UNCHANGED semantically

`(source_snapshot_id, source_row_ordinal)` remains the replay identity basis unless a stronger source-native identity mapping has been separately proved. Native IDs are attributes, not presumed keys.

**Accepted hostile evidence:** South Asia W1 lacks an evident native ID; Arab Barometer W8 has 2,400 `ID=0` collisions; WVS W4 native candidate V3 includes typed missing/colliding values.

**Threats:** C06, C15, C19, C21.

**Required proof:** logical identity remains invariant under carrier repartitioning, row-group tuning, sorting, compression, and thread-count changes.

---

## I03 — Source variable identity / ordinal survives compaction

**Status:** RELIED / TOUCHED

Native variable name/ordinal is not reducible to canonical question identity or observed vector equality.

**Accepted hostile evidence:** WVS W4/W7 parallel variables with identical raw vectors and distinct dictionary/label views.

**Threats:** C03, C07, C09, C12, C21.

**Required proof:** exact native variable identity is directly stored or deterministically reconstructed from a frozen determinant independent of carrier position.

---

## I04 — Physical value and physical missing class remain independent

**Status:** RELIED / UNCHANGED

System missing, format user-missing values/ranges, Stata extended missing, ordinary values, ordinary absence-looking codes, and valid empty strings cannot collapse into one null category.

**Accepted hostile evidence:** Arab Barometer W2 q2062; LiTS III q112_1; LiTS IV q1032; South Asia W1 code 8; Arab Barometer W8 empty `BLOCK_ID`.

**Threats:** C05, C07, C10, C12, C21.

**Required proof:** round-trip reconstruction distinguishes every frozen physical state and raw value exactly.

---

## I05 — Missing declaration and observed incidence remain independent

**Status:** RELIED / UNCHANGED

A declaration can exist even when no matching cell occurs. Incidence cannot reconstruct declaration authority.

**Accepted hostile evidence:** Afrobarometer R9 Q78F declares `-1` despite zero observed user-missing incidence; GSS-family shared missing-range declarations.

**Threats:** C03, C05, C07, C10, C12, C13, C21.

**Required proof:** declarations survive constant/all-zero/all-missing optimization and are root-bound.

---

## I06 — Label/dictionary/display/storage metadata are not inferred from raw values

**Status:** RELIED / TOUCHED

Equal values do not imply equal labels/dictionaries. Display/storage declarations are distinct from raw magnitude/value semantics.

**Accepted hostile evidence:** WVS W4/W7 raw-vector equality with distinct label views; WVS W1 S007 display/raw-magnitude inconsistency.

**Threats:** C03, C05, C07, C12, C21.

**Required proof:** metadata required for exact reconstruction is stored or reconstructed from an explicit certified determinant, never vector coincidence.

---

## I07 — Source text / reader execution configuration remain distinct

**Status:** RELIED / UNCHANGED

A compatibility decoding option is not source-text authority. Reader configuration is exact execution provenance.

**Accepted hostile evidence:** Asian Barometer W1 BIG-5; EVS/LiTS frozen latin1 compatibility; LiTS reader encoding-report conflicts; Arab Barometer W1 literal C1 controls; LiTS IV reader-option interaction failure.

**Threats:** C05, C08, C12, C20, C21.

**Required proof:** replacement compiler consumes frozen decoder output/configuration and does not independently guess/repair encodings.

---

## I08 — Topology identity is first-class information

**Status:** RELIED / UNCHANGED

Multiple-response set identity, membership, multiplicity, order, rank, repeated-event position, component/subitem identity, and module topology remain independently reconstructable.

**Accepted hostile evidence:** Asian Barometer W5 and EVS 2008 overlapping/alias MR set declarations; frozen WVS repeated/ordered hostile fixtures; LiTS mirrored respondent modules.

**Threats:** C03, C07, C09, C10, C11, C13, C21.

**Required proof:** no false `(respondent, canonical_question)` uniqueness; every logical event and topology relation can be reconstructed exactly.

---

## I09 — Routing/applicability is not physical nullness

**Status:** RELIED / UNCHANGED

Physical absence, semantic response state, and governed routing eligibility are separate dimensions.

**Accepted hostile evidence:** LiTS IV mass explicit skip-variable surface and visit blocks; source constitution/risk-set law.

**Threats:** C09, C10, C11, C13, C21.

**Required proof:** exact routed-applicable and other governed risk sets are reproduced without null-pattern inference.

---

## I10 — All weight/design candidates remain physically available

**Status:** RELIED / UNCHANGED

No physical candidate weight/design/routing variable is dropped or silently defaulted before authority chooses a role.

**Accepted hostile evidence:** WVS W1 high-multiplicity weight-like surface; LiTS IV complementary base/top-up missingness.

**Threats:** C03, C09, C13, C20, C21.

**Required proof:** candidate variables and physical states survive; weighted I03 selects only by explicit governed basis.

---

## I11 — Canonicalization is additive, never destructive

**Status:** RELIED / UNCHANGED

Canonical question/response mappings do not replace source-native identity, raw value, physical state, or topology.

**Threats:** C09, C10, C11, C20, C21.

**Required proof:** source-native reconstruction remains possible after all canonical/query acceleration layers are removed.

---

## I12 — One invariant-checked C11 materialization boundary

**Status:** RELIED / TOUCHED

Current code demonstrates fail-closed object/release boundaries: internal records validate exact refs/typed absence/authorities; sealed releases require private validation; repository resolution is exact/no-fallback. Replacement carriers must not create a second semantic ingress.

**Threats:** C05 direct vector semantics; C08 fast compiler output; C10 bitmap truth; C11 virtual events; C20 specialized compiler; C21 virtual long.

**Required proof:** all downstream logical objects/events pass one audited materializer/facade with the same C11 invariants. No partial/unsafe constructor path.

---

## I13 — ExactRef/content identity remains semantic, not physical-position identity

**Status:** RELIED / UNCHANGED

Content identity follows semantic projection and exact determinants, not row number inside a Parquet file, chunk index, or matrix coordinate that changes with layout.

**Threats:** C06, C15, C19, C21.

**Required proof:** rebuild under changed physical partition/layout yields identical logical refs/semantic hashes where the contract requires semantic determinism.

---

## I14 — Arbitrary respondent-grain conjunctions remain exact

**Status:** RELIED / UNCHANGED

The terminal demand envelope includes arbitrary conjunctions, k-way joints, contradictions, reversals, subgroups, cohorts, and source-indexed scopes.

**Threats:** C09, C10, C11, C13, C21.

**Required proof:** cross-partition/query execution is exact and risk-set preserving; a fast marginal-only benchmark is insufficient.

---

## I15 — Unforeseen I05 predicates remain answerable from canonical stored truth

**Status:** RELIED / UNCHANGED

A finite ingest-time query cube/bitmap vocabulary cannot define future discovery capability.

**Threats:** canonical C10, C11, C21.

**Required proof:** new predicates can be evaluated without source-byte reingest and without inventing missing semantic data.

---

## I16 — I03/I05/I04 remain source-neutral consumers

**Status:** RELIED / UNCHANGED

Source-format/family branching terminates before the neutral C11 interface.

**Threats:** C08, C20, C21.

**Required proof:** source-local optimization outputs converge to identical shared logical contract; no SAV/DTA/corpus branch leaks downstream.

---

## I17 — Replay closure includes more than event values

**Status:** RELIED / UNCHANGED

Replay covers source substrates, semantic projection identity, deterministic tie/order rules, predicate/risk/target/measure bindings, comparator/discovery/structural closure as governed by frozen C11.

**Threats:** replacements optimizing only event facts; C13 hot/cold starvation; C21 virtual-event-only model.

**Required proof:** the entire C11 release/replay manifest is reconstructable and exact, not only respondent answers.

---

## I18 — Publication is immutable and atomic

**Status:** TOUCHED / REQUIRED

A reader must never accept a partial, mutable, cross-release, or stale canonical publication.

**Threats:** incremental files visible before seal; mutable manifests; weak cache aliases; chunk splicing.

**Required proof:** immutable release/root identity enumerates exact members; publication becomes visible only after complete verification; mismatch fails closed.

---

## I19 — One canonical truth; caches are regenerable

**Status:** RELIED / UNCHANGED

C18 is architectural law, not a license to create another representation. Caches/indexes may accelerate but must be disposable and derivable from canonical truth.

**Threats:** C04, persistent C10, hidden DB/index, C13 duplicated stores, C21 plus virtual-long persisted copy.

**Required proof:** deleting all caches cannot destroy empirical/replay information; cache divergence never requires semantic reconciliation.

---

## I20 — Cache identity includes every reconstruction determinant

**Status:** TOUCHED

At minimum the cache receipt must bind the exact source/release identity and every schema/compiler/config/authority-frontier determinant that can change its meaning or reconstruction.

**Threats:** C04 and any persistent accelerator.

**Required proof:** change any determinant and stale cache becomes an explicit miss/failure, never a silent hit.

---

## I21 — Determinism survives physical concurrency/layout choices

**Status:** RELIED / TOUCHED

Logical output, identities, reconstruction, and acceptance receipts at the contracted level do not depend on thread scheduling, partition size, row group, or nondeterministic merge order.

**Threats:** C07 sparse override conflict rules; C08 vector batches; C15 parallel build; C21 partitioned matrix.

**Required proof:** deterministic variant court over batch size, partition count, row group, and thread count.

---

## I22 — Integrity layers have named non-overlapping jobs

**Status:** TOUCHED

Whole-release identity, member hashes, format checksums, and Merkle/chunk trees are not accumulated by default.

**Threats:** C14 plus publication/cache mechanisms.

**Required proof:** each layer detects a distinct required failure or serves a distinct verification/fetch/repair granularity. If two layers have no independent job, delete one.

---

## I23 — Bounded memory is whole-workflow, not ingest-only

**Status:** RELIED / TOUCHED

Build, reopen, reconstruction audit, I03/I05, replay, and integrity verification must not require corpus-scale Python retention merely because ingest is streaming.

**Threats:** C01 without C02; C03 join materialization; C09 cross-partition joins; C11 late materialization cache explosion; C15 parallel RSS multiplication.

**Required proof:** stage-specific peak RSS receipt for the whole runner.

---

## I24 — Resource optimization follows exactness, not vice versa

**Status:** RELIED / UNCHANGED

No hard resource win can compensate for weakening source-native truth, query envelope, replay, or integrity.

**Threats:** all B/C candidates under pressure to hit lower byte/event metrics.

**Required proof:** semantic/equivalence/integrity gates run before resource recommendation is dispositive.

---

## I25 — Minimality / stop rule

**Status:** RELIED / ENFORCED BY R06

Once the simplest candidate closes exactness, hard/preferred resources, practical whole-workflow query/replay, integrity, and maintainability, a new mechanism must close a new named requirement. Improving an already acceptable number is insufficient.

**Threats:** additive synthesis of individually attractive R01–R05 mechanisms.

**Required proof:** every admitted mechanism names the gate it closes and the simpler alternative it displaces.

---

## Invariants intentionally left unchanged by R06

R06 does not reopen or reinterpret:

- source-native constitution;
- format decoder semantics;
- frozen C11 logical/public object law;
- ExactRef/content identity law;
- authority hierarchy;
- I03/I05/I04 semantic/query contracts;
- source-wave / branch replay requirements;
- structural-admission law;
- V553/downstream semantics;
- source relation/composition authority;
- missingness/routing/weight semantics;
- the accepted 35-source corpus boundary.

Any physical proposal requiring one of those to change is not a post-R4 physical replacement; it is an unauthorized semantic redesign.
