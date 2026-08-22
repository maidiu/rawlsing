# C08 — Learned-World Invalidation DAG

Status: `PRE_RECONCILIATION__DEPENDENCY_SEMANTICS_COMPLETE__C04_C05_OPERATIONAL_EVIDENCE_PENDING`

## 1. Rule

A learned-world object is invalidated for a new build only when one of its exact determinants changes or an exact upstream dependency it cites is invalidated. Physical adjacency, cache age, mutable branch state, or the existence of a newer source does not count.

Historical objects remain content-addressed historical objects. "Invalidated" means **not reusable as the output of the new determinant set**; it does not mean erase or rewrite.

## 2. Nodes

| Node | Semantic owner | Minimum identity/determinants | Persistence role |
|---|---|---|---|
| S | source authority | exact source SHA/release identity | P1 |
| D | decoder contract | implementation/version/config/dependency identity | P3/P6 determinant |
| SA | source semantic authority | exact AuthorityRef + jurisdiction | P2/P3 |
| QB | canonical binding | native identity ↔ canonical question/component authority | P2/P3 |
| OT | occurrence/topology | source coordinate + governed occurrence/order/rank/multiplicity law | P2/P3 |
| RR | routing/risk set | exact routing/applicability/risk-set refs | P2/P3 |
| WD | weight/design/estimand | exact measure authority | P2/P3 |
| SR | source relation | exact nonduplication/pooling/composition authority | P2/P3 |
| C11 | sealed logical source release | S+D+SA+QB+OT+RR+WD determinant closure | logical release + P3 replay; physical persistence candidate-dependent |
| I03 | exact empirical fact layer | I03 contract/schema + exact C11/query/predicate/authority refs | P2/P3 outputs where published/cited |
| I05 | discovery frontier/result | I05 contract + DiscoveryAuthority + grammar/frontier + exact I03 inputs | P2/P3 receipts/results |
| VAL | validation/accepted relation | candidate + validation law/version + source/universe/uncertainty refs | P2/P3 where governed |
| I04 | structural admission | I04 contract/rule + exact empirical fact/query + structural target/use authorities | P2/P3 |
| V553–V556 | structural products | exact producer authority + upstream object refs | P2 |
| V557 | publication/governance | exact accepted upstream structural refs + publication law | P3/P2 bundle |
| V558 | immutable structural repository | admitted structural release + publication/governance root | P2/P3 |
| IDX | resolver/rack/serving index | governed release refs + index/rack spec/version | P4 |
| LIFE | V3 generated history | selected sealed structural context + V3 causal execution | downstream V3 authority |

## 3. Forward invalidation edges

```text
S  -> C11 -> I03 -> I05 -> VAL -> I04 -> V553 -> V554 -> V555 -> V556 -> V557 -> V558 -> IDX
D  -> C11
SA -> C11
QB -> C11
OT -> C11 -> I03 joint/cotravel/risk-set-sensitive products
RR -> I03/I05 universe/denominator-sensitive products
WD -> I03/I05/VAL measure-sensitive products
SR -> composite I03/I05/VAL products
I03_CONTRACT -> I03 -> dependent I05/VAL/I04
I05_CONTRACT/GRAMMAR/BOUND -> I05 -> dependent VAL/I04
I04_RULE -> I04 -> structural descendant closure
STRUCTURAL_OBJECT -> exact downstream structural closure -> V557/V558 -> IDX
PUBLICATION_SPEC -> V557/V558 physical publication -> IDX
CACHE_SPEC/KEY -> IDX/P4 only
```

There is deliberately **no invalidation edge from V558 back into C11/I03/I05** and no edge from any upstream rebuild into existing V3 LIFE.

## 4. Candidate overlay

### A — persistent LONG

`S/D/SA/QB/OT/RR/WD` changes may require rewriting affected persistent event-carrier partitions in addition to the semantic closure. That carrier is still a derived execution representation. A global LONG rebuild is operational amplification unless the changed determinant is genuinely global or the physical implementation proves no smaller safe write unit.

### B — source-backed virtual

C11 payload has no mandatory persistent rebuild. The changed determinant updates exact source/authority/replay identity; affected C11 logical state is reconstructed when its downstream closure is rebuilt or queried.

### C — hybrid

B plus:
`changed determinant -> invalidate matching P4 cache-key partitions`.
Unmatched cache partitions survive. Cache loss never produces a semantic invalidation edge.

## 5. I03 version-change rule

Current checked-in I03 consumes exact sealed C11 refs and rejects latest/default/fuzzy resolution. If a new I03 semantic contract is separately authorized:

- old `EmpiricalQuerySpec`/`EmpiricalPredicate`/fact identities stay replayable under the old contract;
- new I03 semantics mint new version-bound objects/results;
- I05/validation/I04 products invalidate only where they cite the changed I03 lineage;
- source/C11 are reusable unless the new I03 authority explicitly requires different upstream semantics.

A global I03 semantic change can require re-executing all I03 outputs **without** implying a global source rebuild.

## 6. I05 grammar/bound rule

Current I05 is `PRE553_I05_EXACT_BOUNDED_DISCOVERY@1.0.0` with candidate grammar `PRE553_I05_EXACT_BOUNDED_CANDIDATE_GRAMMAR@1.0.0`, complete-for-declared-frontier evaluate-all semantics, canonical candidate-hash ordering, and no adaptive pruning/random proposal.

If a grammar/bound/frontier change is separately authorized:

```text
old DiscoveryAuthority/grammar/frontier
  -> retained old complete/partial receipt

new DiscoveryAuthority/grammar/frontier
  -> new candidate compilation
  -> execute every candidate required by the new authority
  -> new coverage receipt
```

Existing exact I03 facts may be reused. A changed frontier cannot be represented by editing the old receipt, and an interrupted/new incomplete frontier cannot be reported as a complete negative.

C05 must still determine the operational working-set/materialization implications.

## 7. I04 admission-authority rule

Current I04 is `PRE553_I04_STRUCTURAL_ADMISSION_V553@1.0.0`. It explicitly owns the admission seam and does not own empirical query execution, source relation inference, generated actor position, or V553 temporal operations.

An authorized I04 rule change therefore invalidates:

```text
affected admission decisions/receipts
 -> admitted structural refs that depend on them
 -> exact V553–V558 descendant closure
 -> derived runtime indexes
```

It does **not** invalidate the empirical facts merely because the admission verdict changed.

## 8. Structural invalidation rule

For one invalid structural prior/object:

1. preserve the old object and ExactRef for replay;
2. mark it unusable for a new structural release under the governing invalidation authority;
3. trace `required_dependency_refs` and `negative_dependency_refs`;
4. rebuild only descendants that actually cite it;
5. republish a complete V557/V558 generation;
6. regenerate P4 resolver/rack indexes;
7. preserve every V3 life already generated under the old selected release.

## 9. Publication and crash isolation

A partial publication has no authority. The previous sealed generation remains serveable. A crash can require rebuilding the whole *staging bundle* as an atomic packaging unit, but that is not evidence that upstream semantic products must be recomputed.

Corrupt P4 indexes/racks are deleted and rebuilt from the sealed V558/product roots. Corruption of a P2/P3 authoritative product is handled from its exact determinants and integrity receipts; no cache is allowed to become the recovery oracle.

## 10. Learned release lifecycle caveat

C02/C07 evidence establishes that governed learned release identity, validation/admission state, provenance and explanation lineage may be durable even when payload is exactly rebuildable.

C08 therefore requires immutable old/new lineages. However, the repository does not yet supply one universal publish/supersede/withdraw lifecycle law for every future learned product. C08 does not invent that missing policy. Where eligibility after correction/revocation is not governed, the system preserves both histories and fails closed on "current" selection.

## 11. Missing authority that invalidation cannot solve

The following remain fail-closed authority gaps rather than rebuild problems:

- general empirical validation law;
- empirical comparability law;
- positioned-subject possibility-model law;
- source-universe composition law where composition is not otherwise exactly authorized;
- adaptive discovery/search replay authority beyond current exact-bounded I05;
- complete universal learned-product publication/supersession/withdrawal policy.

Changing bytes, rebuilding caches, or rerunning a corpus cannot manufacture these semantics.

## 12. Final barrier

This DAG is the independent C08 dependency model. It must be reconciled against actual C04 source-backed I03 materialization witnesses and actual C05 discovery execution-state/working-set/persistence witnesses before final C08 disposition.

`C08_FINAL_RECONCILIATION_PENDING_C04_C05`
