# R06 Synthesis Notes — What HQ Should Take, Reject, and Refuse to Combine

## 1. R06 synthesis posture

R06 is not a sixth design proposal competing with R01–R05. It is a constraint on how their accepted returns may be synthesized.

The primary danger is symmetrical:

- **underengineering** can lose source-native information, query capability, replay identity, or integrity;
- **overengineering** can preserve every bit while producing a carrier so layered, coupled, and migration-heavy that Rawlsing becomes harder to verify, debug, run, or finish.

HQ should therefore synthesize by **subtraction**.

Start from the complete invariant/query/replay/resource envelope. Admit the smallest mechanism set that closes it. Do not treat the six-cell campaign as a shopping list.

---

## 2. What HQ should take from R06

### TAKE-01 — One common acceptance runner

Every candidate must face the same end-to-end court:

```text
exact source digest
→ governed decoder
→ bounded canonical build
→ immutable seal
→ exact reopen
→ one C11 materializer
→ hostile reconstruction audit
→ I03
→ I05
→ I04
→ selected source-byte replay
→ integrity verification
→ determinism variants
→ whole-workflow resource receipt
```

A candidate that needs a bespoke benchmark/acceptance path is suspect.

### TAKE-02 — Class A presumption is operational, not rhetorical

The first synthesis hypothesis should be:

- C01 bounded streaming write;
- C02 bounded merge/reopen/audit;
- C16 empirical Parquet tuning;
- C17 minimal receipts/telemetry;
- C18 one canonical truth / regenerable cache law;
- C04 only if identity recomputation is actually material.

Run this before adding deeper normalization or Class C machinery.

### TAKE-03 — Functional-dependency certificates

For every C03/C06/C07/C12/C13-style omission/normalization, require a certificate with:

1. exact field(s) omitted;
2. determinant fields;
3. information grain at which dependency holds;
4. source families/releases for which it is claimed;
5. explicit exception law;
6. deterministic reconstruction function;
7. accepted hostile counterexamples tested;
8. byte/RSS/runtime saving;
9. failure mode if certificate is wrong.

No certificate may use “same values in this scan” as its sole proof.

### TAKE-04 — One semantic construction boundary

Physical optimization stays below C11. All fast/vector/virtual paths must converge on one invariant-checked logical materialization law. Preserve the present fail-closed spirit of sealed releases, exact-key resolution, typed absence, ExactRefs, and authority closure.

### TAKE-05 — Layout-independent identity

Make this a synthesis-wide hard test. Change:

- Parquet row-group size;
- batch size;
- partition count;
- file/chunk boundaries;
- worker/thread count;
- deterministic sort implementation where permitted.

Logical event refs/replay identity and semantic receipts must remain invariant.

### TAKE-06 — Accepted cross-corpus hostile shapes as mandatory fixtures

At minimum the integration court must include fixtures covering:

- identical raw vector / distinct dictionary views (WVS W4/W7);
- zero-incidence but declared user missing (Afrobarometer R9);
- same-variable true missing + ordinary absence-like code (Arab Barometer W2; LiTS III/IV);
- same code/label with variable-specific physical class (South Asia W1);
- ordinary empty string (Arab Barometer W8);
- overlapping/alias MR sets (Asian Barometer W5; EVS 2008);
- no/colliding/typed-missing native respondent IDs;
- weight multiplicity/complementarity;
- SPSS continuation slots/header irregularity;
- encoding/reader-option heterogeneity.

This is more valuable than another synthetic regular matrix benchmark.

### TAKE-07 — Non-additive integrity law

Take the R05 integrity mechanisms only to the extent each has a named job. Minimum likely law:

- immutable release/root manifest;
- exact member hashes/identities;
- deterministic semantic/replay receipt;
- fail-closed partial/mismatch handling;
- cache identity bound to all reconstruction determinants.

Add Merkle/chunk trees only when partial independent verification/fetch/repair is a real requirement.

### TAKE-08 — Stop rule with teeth

If the bounded streaming-long candidate passes exactness, preferred/hard resource gates, practical I03/I05/replay, integrity, and maintainability, **stop**. A 30% smaller or 2× faster Class C microbenchmark is not sufficient reason to replace it.

---

## 3. What HQ should reject unless a measured deficiency exists

### REJECT-01 — Canonical matrix as the presumed destination

C21 is not an endgame merely because survey data looks rectangular. The semantic machine is not rectangular at the relevant grain: repeated/ranked/multiple-response/component/routing/authority structures make virtual-event reconstruction the real complexity.

### REJECT-02 — Persistent bitmap truth

Bitmaps are attractive accelerators and dangerous canonical vocabularies. Prefer disposable/regenerable bitmap indexes after canonical truth closes. Do not let precomputed state vocabulary define future I05 discovery.

### REJECT-03 — Question-oriented canonical sharding by default

Question partitions optimize one access pattern while arbitrary respondent-grain conjunctions are first-class machine capabilities. Require hostile k-way join measurements before canonicalizing this layout.

### REJECT-04 — Source-local compilers as architecture

Special cases already exist in readers/decoder compatibility. Do not fossilize every source irregularity into a permanent compiler family unless the neutral compiler measurably fails. If specialization is required, it must terminate at one shared C11 boundary.

### REJECT-05 — Derived locators for aesthetic purity

If a small exact locator can simply be stored, do that unless locator bytes are a measured bottleneck. Identity derivation is proof debt.

### REJECT-06 — Adaptive encoding policy engine before Parquet tuning

Use standard physical encodings/compression first. An adaptive policy matrix should enter only after accepted measurements show material unresolved storage/runtime pressure.

### REJECT-07 — Hot/cold split that changes accessibility

Cold is not “less true.” If exact I05/replay requires cold state, the join is part of the canonical path and must be counted in cost. Reject any design whose fast path silently narrows the machine.

### REJECT-08 — Integrity theater

Do not stack whole-file hashes, member hashes, Parquet checksums, Merkle trees, cache hashes, and mutable index receipts merely because each is available. Assign a failure mode to each layer or delete it.

### REJECT-09 — Telemetry platform

The campaign needs benchmark receipts, not an observability product. Keep counters fixed and boring unless operations later establish a need.

### REJECT-10 — Parallelism before deterministic bounded serial closure

Parallelism is an optimization of wall time, not a substitute for boundedness. It should not be allowed to obscure merge-order/replay bugs or increase RSS beyond the preferred gate.

---

## 4. `DO_NOT_COMBINE` — synthesis veto list

The following bundles should be treated as architectural red flags.

### DNC-01 — Matrix stack

**C21 + C09 + persistent C10 + C11**

Why reject: matrix incidence, question partitions, bitmap truth, and virtual long each become a separate representation/reconstruction layer. This is likely four solutions to one measured problem.

### DNC-02 — Triple normalization

**C03 + C07 + C13 over the same fields**

Why reject: true-grain normalized tables + defaults/exceptions + hot/cold split can require multiple joins merely to recreate one event. Pick the single compaction mechanism with the best measured ratio and clearest determinant.

### DNC-03 — Identity drift bundle

**C06 + C19 + C15**

Why reject: locator derivation, physical row-position semantics, and parallel partitioning are mechanically coupled. If layout changes identity, replay is broken.

### DNC-04 — Compiler cross-product

**C05 + C12 + C08 + C20**

Why reject: typed lanes × adaptive encoding × vector compiler × source-local compilers creates a test/maintenance matrix larger than the storage problem unless full measurements force it.

### DNC-05 — Integrity pile

**C14 + whole-artifact hash + duplicate per-member checksum layers + format checksums** without distinct failure granularity.

Why reject: conflicting integrity authorities complicate recovery and versioning.

### DNC-06 — Shadow truth bundle

**C04 persistent cache + persistent C10 + hidden DB/index**

Why reject: three “accelerators” become a reconciliation system. Keep one canonical truth and at most the measured disposable accelerators.

### DNC-07 — Nondeterministic parallel overrides

**C15 + C07** before stable conflict/default/override ordering is frozen.

Why reject: scheduling can alter output while every individual row remains locally valid.

### DNC-08 — Query starvation split

**C13 + C09** when exact I05/replay needs metadata routed to the cold/other partition.

Why reject: the apparent fast canonical surface becomes incapable of reconstructing its own evidence without hidden joins.

### DNC-09 — Equality-based semantic collapse

**vector-hash FD compaction + dictionary/topology dedupe**

Why reject: directly refuted by accepted WVS/MR-set evidence.

### DNC-10 — Null routing collapse

**physical missing/null encoding + routing bitmap inference**

Why reject: source constitution explicitly separates physical missingness, semantic state, and routing/applicability.

### DNC-11 — Source specialization leakage

**C20 + I03/I05 source-family branches**

Why reject: once specialization crosses C11, the neutral empirical machine is gone.

### DNC-12 — Mutable alias plus caches

**mutable “current” release alias + long-lived cache tiers** without exact immutable root validation.

Why reject: stale-valid cache artifacts can silently attach to the wrong publication.

---

## 5. Minimum viable synthesis sequence

HQ should not start by choosing between “long” and “matrix.” It should execute this sequence.

### Phase 1 — Prove the least complicated plausible carrier

Compose only mechanisms required to make R4 genuinely bounded and publishable:

1. C01 streaming/bounded build.
2. C02 bounded reopen/merge/audit.
3. C16 tuned standard physical files.
4. minimal immutable publication/root/member integrity.
5. C17 fixed resource/integrity receipts.
6. one C11 materialization boundary.
7. C18 one-canonical-copy law.

Then run full WVS/LiTS and the accepted heterogeneous hostile court.

### Phase 2 — Diagnose, do not redesign generically

If the Phase-1 candidate fails, classify the failure exactly:

- storage;
- build RSS;
- reopen RSS;
- I03 latency;
- I05 latency;
- replay latency;
- integrity verification;
- build wall time;
- source-specific physical irregularity.

Choose only the mechanism that targets that failure.

Examples:

- build RSS failure → first revisit C01/batch sizing, not matrix;
- reopen RSS failure → C02, not source specialization;
- carrier storage failure → C03/C05/C07/C12 one at a time with FD proof;
- query latency failure → first pruning/row groups, then disposable C10 cache, before C21;
- build wall-time failure with bounded memory → C15 deterministic parallelism;
- partial-verification/fetch bottleneck → then C14;
- persistent arbitrary-query infeasibility after lower-risk remedies → only then C09/C11/C21 court.

### Phase 3 — Re-run from source truth after each added mechanism

Do not compose two unproven mechanisms and test only the pair. That makes causal diagnosis impossible. Each added mechanism should have its own acceptance/resource delta.

### Phase 4 — Freeze the first sufficient design

When the candidate closes the frozen court, freeze it. Later “better” designs need a new material deficiency, not aesthetic preference.

---

## 6. Class C admission checklist for HQ synthesis

Before accepting any C08/C09/canonical-C10/C11/C14/C19/C20/C21 mechanism, HQ should be able to write `YES` to every item:

- [ ] Lower-risk candidate was actually measured at full relevant scale.
- [ ] A named hard/practical gate remains failed.
- [ ] Obvious streaming/merge/Parquet/narrow-B remedies were exhausted.
- [ ] The Class C pilot materially fixes that specific gate end-to-end.
- [ ] Every event is exactly reconstructable.
- [ ] MR/repeated/ranked/order/component/routing topology survives.
- [ ] Arbitrary respondent conjunctions remain exact.
- [ ] Unforeseen I05 predicates remain possible without source reingest.
- [ ] All weights/design/routing/metadata remain first-class and root-bound.
- [ ] Identity is independent of row-group/partition/thread/layout.
- [ ] There is still one canonical truth.
- [ ] All caches/projections are either explicitly canonical or fully regenerable.
- [ ] Source-local specialization terminates at the shared C11 boundary.
- [ ] Immutable publication/integrity fails closed on stale/partial/cross-release state.
- [ ] Complexity/migration/debug/recovery burden is documented and acceptable.
- [ ] Accepted SR03/SR09 hostile corpus fixtures pass.

If any box is `NO` or `UNKNOWN`, Class C is not ready for synthesis.

---

## 7. Minimal one-runner integration contract HQ should demand

The runner should be representation-neutral and produce one atomic candidate receipt containing:

### Identity

- candidate ID/version;
- exact source SHA/content ref;
- decoder configuration identity;
- carrier schema/config identity;
- compiler/build identity;
- authority/semantic frontier identity;
- immutable release/root identity.

### Exactness

- source-native reconstruction mismatch count;
- C11 semantic-equivalence mismatch count;
- hostile fixture outcomes;
- source relation/topology/weight/routing checks.

### Query/discovery

- I03 exact suite result identity;
- I05 exact suite result identity;
- I04/structural closure result identity;
- arbitrary k-way/risk-set hostile queries.

### Replay/integrity

- selected event replay mismatch count;
- partial/stale/cross-release negative tests;
- cache deletion/rebuild parity if caches exist;
- deterministic rebuild identity under physical-layout variants.

### Resources

- canonical bytes;
- optional accelerator/cache bytes separately;
- temp bytes;
- phase-specific peak RSS;
- build/reopen/I03/I05/I04/replay/integrity timings.

The runner must reject, not warn-and-continue, on exactness/integrity/replay mismatch.

---

## 8. Mechanisms to delete during synthesis if they have no unique job

HQ should conduct a final mechanism deletion pass. Ask of every component: **what accepted failure occurs if this component is removed?**

Delete if the answer is only “performance might be worse” and the remaining design still passes the court.

Likely deletion candidates in a successful bounded-long synthesis:

- matrix canonicalization;
- virtual-long facade;
- persistent bitmaps;
- canonical question sharding;
- source-specific compilers;
- Merkle tree;
- adaptive encoding framework;
- parallel scheduler;
- hot/cold split;
- locator derivation;
- multiple cache tiers;
- telemetry framework;
- extra publication index/database;
- duplicate normalized provenance relations;
- low-value default/override schemes.

Some may be individually good ideas. That is not enough.

---

## 9. Final synthesis recommendation

R06 recommends HQ carry forward the following decision hierarchy:

```text
1. Exactness / frozen empirical machine
2. Fail-closed replay + integrity
3. Bounded whole-workflow memory
4. Governed storage limits
5. Practical I03/I05/I04/replay runtime
6. Maintainability / diagnosability
7. Only then marginal speed/byte improvements
```

The most dangerous synthesis error would be to treat R01–R05 as complementary specialists whose mechanisms should all be preserved. They are alternative attacks on overlapping costs. Their proposals should compete for the right to exist.

If streaming-long, made genuinely bounded on write and read, passes the full hostile court and workstation envelope, it should win because it minimizes semantic distance between stored incidence and the already-frozen C11/query/replay machine.

If it fails materially, escalate one measured deficiency at a time. Class C is justified only by necessity demonstrated in the same full integration court—not by architectural taste, future-proof rhetoric, or local benchmark dominance.

The project is saved from data loss by refusing destructive simplification. It is saved from overengineering by refusing unnecessary mechanisms with equal discipline.
