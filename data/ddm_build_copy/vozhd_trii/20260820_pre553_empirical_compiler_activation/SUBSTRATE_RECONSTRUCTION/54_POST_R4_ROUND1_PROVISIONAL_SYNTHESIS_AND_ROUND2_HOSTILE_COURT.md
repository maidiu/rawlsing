# VOZHD TRII — POST-R4 ROUND-1 PROVISIONAL SYNTHESIS & ROUND-2 HOSTILE CROSS-EXAMINATION COURT

Status: `AUTHORIZED__PROVISIONAL_SYNTHESIS__ROUND2_SIX_CELL_HOSTILE_COURT__NO_RUNTIME_MUTATION`

Repository: `maidiu/rawlsing`

Control branch: `agent/vozhd-trii-pre553-substrate-reconstruction-control`

Parent control head:

`bc2d022d49b1a860a33b29ce171a89c91956c35e`

Binding parents:

- `52_POST_R4_PHYSICAL_OPTIMIZATION_CANDIDATE_REGISTER_AND_SAFETY_LAW.md`
- `53_POST_R4_SIX_CELL_ZERO_DESTRUCTION_REPLACEMENT_DESIGN_CAMPAIGN.md`

Frozen PRE553 semantic parent:

`9188dc9fb7a8b92b981f3d3f94754cd6137d17b1`

Accepted R4 reference implementation under current P2 court:

`20cfc676bdcebbf9aa5ef129bb7b94451f3af175`

This authority does NOT authorize implementation or adoption of a replacement carrier.

It banks HQ's provisional synthesis of Round 1 and authorizes one six-cell Round-2 hostile cross-examination before any runtime implementation authority may issue.

---

## 0. PURPOSE

Round 1 answered independent design/proof questions.

Round 2 asks a different question:

> **Can six hostile reviewers, now allowed to see the complete provisional synthesis and the exact Round-1 evidence, find any information loss, semantic narrowing, query/discovery starvation, integrity weakening, replay ambiguity, source-shape assumption, or unnecessary complexity that would make the synthesis unsafe or wasteful?**

The goal is not agreement.

The goal is to defeat the provisional synthesis if it is wrong before code exists.

Round 2 must spend time on the replacement design and its safety, not on broad autopsy of failed R4 full-source execution.

---

## 1. ROUND-1 EXACT RETURN PINS

The six independent Round-1 returns are frozen for this court by exact commit:

- R01 streaming/memory: `f3e1d198ca5b680adfe3330a7460d0b174f395e6`
- R02 grain/types/FD: `6447d57a9818b5a427ad0367858f2030e127f8d8`
- R03 equivalence oracle: `220e017f34b2741fce80b7a6850a1679ea0ce0fe`
- R04 columnar/vector challenger: `bfc6b19c3bbdd43f1a04184d02515dc38dd82712`
- R05 integrity/publication: `b2c74427b568ea9a9447fc2631e002830d700919`
- R06 red-team/minimality: `d573389eaf8df63c124d1439933bbe3cef4dda23`

Workers must read these exact commits, not mutable branch tips.

Example:

`git show <SHA>:<PATH>`

is acceptable.

### 1.1 Round-1 scope/compliance audit

R01-R05:

- began from the mandated common start;
- changed only their authorized design-return directories;
- did not modify `rawlsing_next/**`;
- supplied the common required return package;
- used no raw-source probes because checked-in authority/manifests/recon were sufficient.

R06:

- began from the mandated common start;
- stayed within its authorized design-return directory;
- did not modify `rawlsing_next/**`;
- produced substantial adversarial/minimality artifacts and the required return token;
- did not use raw-source probes;
- BUT did not conform exactly to Section 6 common packaging: it omitted `RESULT.json`, `ASSUMPTION_LEDGER.csv`, `INFORMATION_PRESERVATION_LEDGER.csv`, and `SELF_RED_TEAM.md`, substituting `CANDIDATE_SCORECARD.csv`, `INVARIANT_LEDGER.md`, `PROPOSAL.md`, `RESOURCE_MODEL.md`, and `SYNTHESIS_NOTES.md`.

Disposition:

`R06_SUBSTANCE_ADMISSIBLE_FOR_PROVISIONAL_SYNTHESIS__ROUND1_PACKAGING_NONCONFORMANCE_MUST_BE_REMEDIATED_IN_ROUND2_R06_RETURN`

HQ does not discard the substantive R06 evidence, but it does not waive the procedural defect.

---

## 2. ORIGINAL THIRTEEN-PRIORITY COVERAGE CHECK

The original pre-condensation priorities were:

O01 streaming write;
O02 streaming read;
O03 functional-dependency decomposition;
O04 native typed value carrier;
O05 identity/locator compaction;
O06 topology/routing/weight/design preservation;
O07 direct vectorized compiler;
O08 columnar/question-oriented layout;
O09 bitmap/state/predicate indexes;
O10 I03/I05 execution engine / late materialization;
O11 integrity/replay/publication;
O12 hostile cross-source adversary;
O13 minimality/anti-complexity red team.

Round-1 six-cell coverage was:

- R01 = O01 + O02, plus bounded pipeline/tuning/telemetry and streaming publication mechanics.
- R02 = O03 + O04 + O05 + functional-dependency/default side of O06.
- R03 = additional independent equivalence oracle not isolated strongly enough in O01-O13.
- R04 = O07 + O08 + O09 + O10 + physical-layout side of O06.
- R05 = O11.
- R06 = O12 + O13 and an attack over every C01-C21 candidate family.

Therefore:

`O01_O13_COVERAGE = COMPLETE__PLUS_INDEPENDENT_ORACLE_CELL`

This does NOT mean every proposed mechanism should be combined in production.

Several are alternatives or accelerators whose simultaneous adoption would increase attack surface without preserving additional semantics.

---

## 3. ROUND-1 QUALITY FINDINGS

### 3.1 R01 — substantive quality

R01 proposes a bounded-memory long-form baseline with:

- no semantic omissions;
- bounded buffers/queues/fan-in/cache;
- deterministic external runs/merge where sorting is required;
- fixed-size independently closed shards rather than one corpus-growing writer;
- streamed relation inventories;
- lazy bounded readers/audit;
- no correctness-bearing cache;
- transactional staging/seal/publish law;
- explicit memory accounting that includes Arrow/Parquet internal state rather than assuming caller batching proves boundedness.

Its self-red-team correctly identifies backend dictionaries/footer state, external-sort disk amplification, lazy validation, random-lookup cost, duplicate handling, concurrency reorder buffers, large single rows, compatibility decoder full-frame behavior, and full C11 cross-record validation as possible falsifiers.

HQ disposition:

`HIGH_QUALITY_BASELINE_INPUT__NOT_YET_IMPLEMENTATION_AUTHORITY`

### 3.2 R02 — substantive quality

R02 rejects observed equality/frequency as functional-dependency authority.

It proposes only authority-proven grain movement and explicitly keeps event physical state direct.

Key safe positions include:

- source/release constants at release grain only when sealed;
- respondent replay identity based on release/source row ordinal, not convenient native ID;
- release-variable metadata at question grain only within exact release-variable scope;
- value-label derivation only by exact typed-key identity, with direct event fallback when ambiguous;
- float identity by decoder-observed exact bit pattern rather than text repr/parse;
- integer width from native declared type/cardinality rather than observed sample range;
- strings with no Unicode normalization/trim/NUL collapse;
- dates/times not semantically promoted from display formats;
- conditional logical geometry only under a sealed complete traversal law;
- Parquet/file position never semantic identity;
- hot/cold members remain one sealed canonical root.

HQ disposition:

`HIGH_QUALITY_CLASS_B_INPUT__ALL_OMISSIONS_REMAIN_CONDITIONAL_ON_PROOF`

### 3.3 R03 — substantive quality

R03 establishes a representation-neutral oracle anchored in source-native truth + frozen C11 + I03 + I05 + I04 + whole-machine law, not R4 physical layout.

It requires:

- independent ExactRef/content-hash recomputation;
- independent respondent-set/support evaluation in addition to frozen seams;
- all M01-M18;
- source physical preservation;
- exact topology/routing/weights/provenance;
- I03 positive/negative/integrity distinctions;
- I05 pair, k-way, conditional, reversal, recursive, branch and co-signature/cloud-like coverage;
- a post-candidate-freeze deterministic blind I05 workload;
- I04 admission parity;
- fresh-process determinism;
- corruption/partial-publication failure;
- stale-cache/delete/rebuild invariance;
- hostile real-source evidence spanning all nine source families.

One authoritative mismatch fails claimed scope. Performance cannot waive failure.

HQ disposition:

`STRONG_INDEPENDENT_ACCEPTANCE_ORACLE_INPUT__MANDATORY_FOR_LATER_IMPLEMENTATION_COURT`

### 3.4 R04 — substantive quality

R04's CCIV columnar/vector design is deliberately non-default.

It retains:

- explicit event/topology escape relations for nonrectangular/event-varying material;
- separate physical-state, semantic-state and routing/applicability domains;
- arbitrary respondent conjunction through exact governed selector algebra;
- no finite preindexed query vocabulary;
- canonical scan fallback for uncached lawful predicates;
- no-cache correctness as mandatory;
- source-local physical profiles hidden from semantic consumers;
- cache deletion invariance;
- vector validation parity with frozen constructors/integrity;
- exact event identity independent of physical block/row position.

Its self-red-team says CCIV MUST LOSE if a simpler streaming-long carrier is operationally sufficient.

HQ disposition:

`HIGH_QUALITY_CLASS_C_CHALLENGER__NOT_DEFAULT_SYNTHESIS_CORE`

### 3.5 R05 — substantive quality

R05 distinguishes:

- semantic release identity;
- exact physical-root identity;
- serving authorization.

It requires:

- content-addressed staging/seal/promote/reopen/verify/active-selector lifecycle;
- root/member integrity and retained full-member/full-release audit;
- optional hierarchical chunk verification only when query closure is proven;
- no empirical output merely from CHUNK_VERIFIED state;
- exact negative/absence claims closed over every region capable of refutation unless a root-bound canonical completeness proof exists;
- canonical corruption quarantines the physical release;
- cache cannot repair or substitute for canonical corruption;
- caches are deletable, rebuildable, nonauthoritative;
- active-root authorization cannot be inferred from latest filename/mtime;
- rollback cannot become automatic dual authority;
- physical byte reproducibility is separate from semantic replay unless explicitly frozen.

HQ disposition:

`HIGH_QUALITY_FAIL_CLOSED_INTEGRITY_INPUT__LAZY_VERIFICATION_REMAINS_CONDITIONAL`

### 3.6 R06 — substantive quality

R06 supplies concrete cross-corpus counterexamples and a non-additive synthesis law.

It correctly attacks:

- equality-as-FD;
- null/missing collapse;
- question-only layouts under nonrectangular topology;
- layout-dependent identity;
- source-specialized semantic branching;
- finite bitmap/query vocabulary;
- integrity-layer multiplication;
- constructor/invariant bypass;
- overengineering.

It recommends the minimum sufficient mechanism and rejects many Class-C features by default unless lower-risk designs fail a measured whole-workflow gate.

HQ disposition:

`SUBSTANTIVELY_STRONG_RED_TEAM__PROCEDURAL_PACKAGING_DEFECT_NOTED`

---

## 4. CROSS-CELL AGREEMENTS — PROVISIONALLY BINDING FOR ROUND 2

The following agreements recur independently across the cells and form the provisional synthesis baseline.

### A. The semantic contract does not move

Physical optimization may not alter source truth, C11 M01-M18, I03, I05, I04, V553+, V3/V2, or whole-machine jurisdiction.

### B. No corpus-scale Python semantic retention

No canonical writer/reader/audit may require corpus-sized Python lists/dicts/tables of events, overrides, refs, inventories, or caches.

### C. One uniform logical C11 boundary

Physical representation is hidden behind one source-neutral logical interface.

I03/I05/I04 and V553+ may not branch on carrier/source-family physical implementation for meaning.

### D. Information can move grain only under exact proof

No field is omitted from event grain because it is common, equal, frequent, first-seen, or apparently redundant.

Every omission requires determinant, scope, authority, exception/fallback law, reconstruction law and fail-closed behavior.

### E. Physical missingness, semantic state and routing remain separate

No one-null/no-value-state simplification.

### F. Replay identity is independent of physical layout

No Parquet row position, shard number, block coordinate, thread completion order, directory order or cache position enters semantic identity unless independently source-authorized.

### G. Caches/indexes cannot be necessary for truth

Deletion cannot change correctness or canonical identity.

A structure required to prove exact completeness/absence is canonical root-bound material, not cache.

### H. Open-world query/discovery is mandatory

Every lawful predicate/combination over canonical material must have a correctness-preserving canonical path even when no accelerator was built for it.

I05 cannot be reduced to combinations imagined at ingest/index design time.

### I. Integrity is fail closed

Corrupt/incomplete canonical bytes cannot become valid-empty/no-match/zero-support or any plausible empirical answer.

### J. Publication is transactional

Staging is non-serving; complete candidate roots remain non-serving until admitted; active selection is explicit and atomic; no mixed old/new release; no automatic truth fallback.

### K. Full audit remains available

Any partial/hierarchical verification optimization must coexist with a bounded full integrity/semantic audit path.

### L. Minimality is an acceptance dimension

A more complex carrier does not win merely by being smaller/faster. If a simpler exact design is comfortably operationally sufficient, the more complex design loses.

---

## 5. PROVISIONAL REPLACEMENT ARCHITECTURE P0

Name:

`P0_BOUNDED_TYPED_CANONICAL_INCIDENCE_WITH_UNIFORM_C11_VIEW`

This is a synthesis target for Round-2 attack, NOT implementation authority.

### 5.1 Input boundary

Exact frozen physical decoder output remains source-physical authority.

Compiler consumes bounded decoder batches.

No source-family semantic inference occurs in the compiler.

### 5.2 Vectorization stance

The preferred hot path may compile bounded decoder batches directly to typed Arrow/columnar buffers to avoid per-cell Python semantic-object construction.

However:

- vectorization is execution only;
- every constructor/integrity invariant bypassed by skipping per-event object creation must be enumerated and reproduced;
- a slow validated reference path remains available for the oracle/hostile court;
- exact semantic projection/hash parity is mandatory;
- if invariant reproduction is incomplete, direct vectorization is rejected or narrowed to mechanically safe subpaths.

### 5.3 True-grain canonical members

Provisional canonical release may contain:

1. immutable release/source/decoder/compiler/authority manifest material;
2. release-local respondent dimension keyed by source row replay coordinate;
3. release-local native variable/question physical metadata dimension;
4. bounded typed event-incidence relation(s) containing material that actually varies by event;
5. explicit physical-state incidence separate from semantic response state;
6. explicit nonrectangular/repeated/ranked/multiple-response/event topology relation as needed;
7. routing/applicability/risk-set canonical material under existing authority;
8. coordinate/weight/design/measure candidate material under existing authority;
9. authority/dependency/provenance/replay relations;
10. exact sparse exceptions only where a determinant/default is independently proven;
11. canonical completeness/index material only if it is required to prove exact absence and is itself root-bound;
12. optional nonauthoritative caches/indexes outside canonical identity.

Nothing above may be omitted merely because a proving source is rectangular or a value is common.

### 5.4 Event-incidence physical organization

Round 2 must decide among these possible organizations rather than assuming one:

- `LONG_SHARDED`: one logical event row per occurrence, normalized true-grain dimensions, independently closed bounded shards;
- `QUESTION_BLOCKED_LONG`: same logical event incidence physically clustered by native variable/question blocks, with exact respondent/event coordinates;
- `HYBRID_DENSE_PLUS_EXPLICIT`: dense typed incidence only where R02-style immutable geometry/grain certificates hold, explicit-event escape otherwise.

`CANONICAL_MATRIX_WITHOUT_EXPLICIT_ESCAPE` is not admitted by P0.

Physical organization must be semantically invisible.

### 5.5 Typed raw-value law

Provisional lanes are exact source-physical carriers, not semantic interpretation.

Requirements:

- typed integer/bool values with total range checks;
- exact decoder-observed float bit identity where applicable;
- exact decoded string sequence with empty string/NUL/normalization distinctions;
- native missing/special tokens preserved distinctly;
- date/time-looking values remain raw plus source metadata absent exact type authority;
- unsupported/mixed values use an exact tagged escape or block publication;
- no text-float identity as the normative endgame law;
- no sampled-range narrowing.

### 5.6 Locator / identity law

Universal semantic/replay identity does not use physical carrier position.

A logical arithmetic locator may be derived from immutable release/source coordinates only under a sealed complete traversal law.

If that proof is absent, explicit coordinates/refs remain.

### 5.7 Writer / memory law

All canonical relations are written in bounded batches/shards.

No corpus-scale Python side relation is retained for close.

Canonical sorting/merging, where required, uses fixed-fan-in bounded external mechanics or an equivalently proven bounded algorithm.

Backend dictionaries/footer/inventory/metadata state count toward the memory proof.

### 5.8 Reader / audit law

Reopen may not materialize corpus-scale canonical side relations into Python.

Reader supports bounded sequential/merge scans and exact reconstruction.

Optional exact indexes may accelerate lookup, but missing/corrupt noncanonical indexes cannot become semantic absence.

### 5.9 I03/I05 execution law

The physical layout may support vector scans, selector algebra, late materialization and optional bitmaps.

But:

- authority/routing/risk-set/negative-state requirements precede any pruning that could erase evidence;
- NOT is complement within the governed universe/risk set, not physical row complement;
- arbitrary lawful respondent conjunctions remain possible;
- unforeseen I05 combinations require no re-ingest;
- every uncached lawful predicate has canonical fallback;
- diagnostic cloud-like scores do not prune or become empirical truth unless separately authorized.

### 5.10 Cache/index law

Default disposition for bitmap/predicate/materialized accelerators:

`NONAUTHORITATIVE__REGENERABLE_CACHE`

A cache can improve speed only.

If a structure is required for exact completeness/absence rather than acceleration, it must be explicitly classified canonical, root-bound, integrity-covered and representation-neutral.

### 5.11 Integrity/publication law

Provisional release lifecycle:

`UNIQUE_STAGING -> COMPLETE MEMBERS -> MANIFEST/SEAL -> VERIFY -> CONTENT-ADDRESS PROMOTE -> REOPEN VERIFY -> EXPLICIT ACTIVE-ROOT CAS`

Readers see one explicitly authorized complete root.

No serving from staging/shadow.

No automatic fallback to stale canonical/cache/legacy material on integrity failure.

Canonical corruption fails closed.

Full streaming member/release audit remains available.

Chunk/Merkle hierarchy is NOT mandatory P0 machinery; it must earn inclusion by a named verification/repair/reopen benefit and must never weaken query-closure sufficiency.

### 5.12 One-copy law

There is one serving canonical empirical root.

Caches are not truth.

Shadow candidate is non-serving during migration/testing.

Round 2 must resolve exact retention/rollback semantics so migration safety does not become permanent duplicate canonical truth.

### 5.13 Determinism

Semantic identity/results remain invariant under lawful changes in:

- temporary path;
- file grouping/shard boundaries;
- row-group size/compression profile where semantically incidental;
- filesystem enumeration order;
- Python hash seed;
- worker/thread count where parallelism is enabled;
- cache presence/absence.

Any physical profile claiming byte reproducibility carries a separate exact physical-byte contract.

---

## 6. PROVISIONAL CANDIDATE DISPOSITIONS FOR ROUND-2 ATTACK

These are NOT final adoption decisions.

### PROVISIONAL CORE / KEEP UNLESS ROUND 2 DEFEATS

- C01 streaming canonical side relations;
- C02 bounded merge/read/audit;
- C03 true-grain normalization only with exact FD certificates;
- C04 immutable computation caching only where nonsemantic/correctly keyed;
- C05 exact typed raw lanes;
- C07 authority-proven defaults + exact exceptions only;
- C16 Parquet/physical tuning;
- C17 minimal resource telemetry;
- C18 one canonical copy + regenerable cache law.

### PROVISIONAL CONDITIONAL / MUST EARN IN ROUND 2 OR LATER BENCHMARK

- C06 derivable logical locators;
- C08 direct vectorized physical compiler;
- C09 question-oriented physical clustering;
- C10 bitmap acceleration as cache;
- C11 late materialization;
- C12 adaptive per-variable physical encoding;
- C13 hot/cold member separation under one root;
- C14 chunk/Merkle integrity;
- C15 parallel pipeline;
- C20 source-local physical specialization behind uniform C11;
- C21 hybrid dense+explicit physical incidence / virtual event view.

### PROVISIONAL REJECT / DEFER ABSENT NEW NAMED NECESSITY

- C10 bitmap as sole/canonical truth merely for speed;
- C13 hot/cold as different authority classes;
- C14 Merkle hierarchy merely because it is elegant;
- C19 physical row-position identity;
- C20 semantic source-family branching;
- C21 universal matrix layout with no explicit event/topology escape;
- finite ingest-time joint/query cubes as empirical truth;
- any frequency/observed-equality default;
- text-float identity as endgame exactness law;
- automatic rollback/fallback between empirical roots;
- any persistent accelerator that cannot be deleted without changing truth.

---

## 7. ROUND-2 SIX-CELL CEILING

Exactly six Round-2 worker cells are authorized.

No seventh worker may be spawned from this authority.

Each Round-2 worker may read ALL six exact Round-1 returns and this provisional synthesis.

Unlike Round 1, cross-cell evidence is REQUIRED.

No Round-2 worker may modify `rawlsing_next/**` or any existing semantic/authority/gate artifact.

Round 2 remains design/proof/hostile review only.

Raw-source access remains bound to these same six cells and is default-DENIED unless a named synthesis assumption cannot be settled from checked-in authority/manifests/recon/Round-1 evidence.

If raw probing is necessary:

- use only exact CLOSED_35 source bytes;
- verify source SHA;
- probe only the minimum source/rows/variables needed;
- remain source-physical absent semantic authority;
- record exact need/scope/evidence;
- never commit source bytes.

No separate raw-source worker.

---

## 8. ROUND-2 CELL ASSIGNMENTS

### R2-01 — INFORMATION-LOSS / GRAIN-CLOSURE COURT

Mission:

Try to produce one lawful source/C11 field or occurrence that P0 cannot reconstruct exactly.

Attack:

- every true-grain movement;
- every default/exception law;
- every logical locator derivation;
- source metadata declarations with zero incidence;
- raw-identical/dictionary-distinct variables;
- respondent identity;
- topology/order/rank/multiplicity;
- routing/weights/design;
- source relation/provenance;
- hot/cold classification.

Required output includes a full `P0_INFORMATION_ACCOUNT.csv` mapping every frozen logical/source obligation to stored/derived/exception/rejected disposition.

### R2-02 — TYPE / GEOMETRY / VECTOR-COMPILER COURT

Mission:

Attack exact typed encodings, geometry assumptions and direct decoder-batch->Arrow compilation.

Require explicit hostile treatment of:

- integer domains/overflow/signedness;
- float -0.0/NaN/infinity/payload behavior;
- empty/NUL/normalization-sensitive strings;
- date/time-looking values;
- native missing/special tokens;
- mixed/unsupported types;
- SAV string continuation/logical-width hazards;
- DTA reader-option/encoding compatibility boundaries;
- variable ordering and geometric locators;
- every validation/invariant currently obtained from semantic constructors/integrity code.

Round 2 must decide what can be vectorized directly and what must stay on a validated fallback path.

### R2-03 — ORACLE-OF-THE-ORACLE / NONCIRCULAR ACCEPTANCE COURT

Mission:

Attack R03 itself and P0 acceptance methodology.

Prove the oracle can detect loss not shared with candidate code.

Attack:

- R4 contamination;
- candidate self-reported digests;
- shared frozen-code bugs;
- incomplete incidence masked by aggregate parity;
- blind-I05 benchmark leakage;
- source-family coverage gaps;
- typed negative-state collapse;
- cache/stale-cache/corruption laundering;
- exact reconstruction versus current-query-only behavior.

Specify the smallest independent reference evaluator needed for a dispositive implementation court.

### R2-04 — I03/I05/I04 OPEN-WORLD QUERY/DISCOVERY COURT

Mission:

Try to find a lawful query/discovery/admission workload that P0 makes impossible, approximate, source-specific or dependent on a prebuilt accelerator.

Attack:

- arbitrary respondent-grain AND/OR/NOT;
- pair/k-way joints;
- high-cardinality/string predicates;
- routing/risk-set-sensitive negatives;
- weight/design estimands;
- repeated/ranked/multiple-response events;
- source-indexed multi-universe operations;
- conditional reversal/Simpson;
- recursive subgroup forks;
- branch-conditioned distributions/cotravel;
- co-signature/cloud-like diagnostics;
- post-freeze unseen combinations;
- columnar/question-block scan costs and join pathologies;
- late-materialization negative-state preservation.

No finite query vocabulary is permitted.

### R2-05 — INTEGRITY / PUBLICATION / REPLAY / CACHE HOSTILE COURT

Mission:

Try to make P0 serve plausible wrong truth after corruption, partial publication, stale cache, concurrent publication, TOCTOU, or rollback.

Attack:

- root/member/chunk identity;
- active-root authorization;
- old/new mixed visibility;
- staging/shadow visibility;
- canonical corruption;
- cache disagreement;
- exact negative/absence closure;
- immutable-byte consume-after-verify;
- deterministic rebuild;
- one-copy versus migration/rollback tension;
- whether Merkle/chunk verification is necessary or ornamental.

Round 2 must state the minimum integrity machinery required; redundant cryptographic layers are to be rejected.

### R2-06 — WHOLE-MACHINE / MINIMALITY / INTEGRATION RED TEAM

Mission:

Assume P0 is overengineered AND still capable of hidden semantic damage.

Read all Round-1 returns and all Round-2 sibling assignment requirements, but do not read sibling Round-2 unaccepted returns.

Attack:

- whole-machine capability starvation;
- empirical->structural semantic leakage;
- source-family physical branching becoming semantics;
- duplicate canonical truth;
- unnecessary sidecars/indexes/profiles;
- maintenance/debugging complexity;
- mutually redundant mechanisms;
- benchmark rules that reward a locally fast but globally worse design.

Produce:

- `KEEP_DELETE_DEFER_MATRIX.csv` for every P0 mechanism;
- exact minimum one-runner contract;
- `DO_NOT_COMBINE.md`;
- explicit conditions for choosing LONG_SHARDED vs QUESTION_BLOCKED_LONG vs HYBRID_DENSE_PLUS_EXPLICIT;
- explicit stop rule after a sufficient carrier wins.

Also remediate Round-1 R06 packaging nonconformance by supplying the complete Round-2 common return package defined below. No separate Round-1 rerun is required.

---

## 9. ROUND-2 COMMON REQUIRED RETURN

Each cell writes only under:

`data/ddm_build_copy/vozhd_trii/20260820_pre553_empirical_compiler_activation/SUBSTRATE_RECONSTRUCTION/POST_R4_ROUND2_HOSTILE/<CELL>/`

Required:

- `RESULT.md`
- `RESULT.json`
- `ASSUMPTION_LEDGER.csv`
- `INFORMATION_PRESERVATION_LEDGER.csv`
- `SELF_RED_TEAM.md`
- `SYNTHESIS_RULINGS.csv`
- `P0_ATTACKS.csv`

Where relevant:

- `PROPOSED_CORRECTION.md`
- `HOSTILE_CASES.csv`
- `ORACLE_PLAN.md`
- `BENCHMARK_PLAN.md`
- small bounded proof scripts/receipts inside cell directory only.

Every RESULT must state exactly:

1. `WHOLE_MACHINE_CONTAINMENT`
2. `ROUND1_EVIDENCE_USED`
3. `P0_SCOPE_ATTACKED`
4. `DESTRUCTION_PATHS_FOUND`
5. `P0_MECHANISMS_CONFIRMED`
6. `P0_MECHANISMS_REJECTED`
7. `P0_MECHANISMS_CONDITIONALLY_ADMISSIBLE`
8. `INFORMATION_ACCOUNT`
9. `I03_I05_I04_EFFECT`
10. `INTEGRITY_REPLAY_EFFECT`
11. `SOURCE_HETEROGENEITY_EFFECT`
12. `COMPLEXITY_MINIMALITY_EFFECT`
13. `RAW_SOURCE_PROBES_IF_ANY`
14. `SELF_FALSIFICATION`
15. `REQUIRED_SYNTHESIS_CHANGES`
16. `FINAL_ROUND2_DISPOSITION`

Allowed final dispositions:

- `ROUND2_PASS__P0_SURVIVES_ASSIGNED_ATTACKS`
- `ROUND2_PASS_WITH_REQUIRED_CORRECTIONS__P0_REPAIRABLE`
- `ROUND2_REJECT__P0_DESTRUCTIVE_OR_INCOMPLETE`
- `ROUND2_BLOCKED__NAMED_AUTHORITY_OR_SOURCE_EVIDENCE_REQUIRED`

No score/majority voting. One demonstrated semantic destruction defeats that mechanism.

---

## 10. ROUND-2 NO-WASTE LAW

Round 2 does NOT authorize:

- rerunning failed R4 full-source jobs;
- broad profiling of R4 internals;
- full CLOSED_35 candidate execution;
- production implementation;
- generic raw-source rescans;
- re-auditing already-closed whole-machine architecture;
- reopening C11/I03/I05/I04 semantics;
- debating a mechanism that has already been defeated unless a concrete correction is proposed.

Small bounded mechanical proofs are encouraged where they resolve a real synthesis question cheaply.

---

## 11. ROUND-2 SUCCESS CONDITION

Round 2 closes only when HQ can produce one final implementation contract in which:

- every source/C11 obligation has one exact physical owner/derivation/exception path;
- no semantic capability is narrowed;
- the independent oracle is noncircular;
- the compiler/reader/audit are genuinely bounded-memory;
- no physical position/cache/source family acquires semantic authority;
- arbitrary lawful I03/I05 operations remain possible;
- integrity/publication/replay remain fail closed;
- one-copy law remains intact;
- every optional mechanism has either a named measurable reason to exist or is removed;
- the final implementation can be built as one shadow runner without modifying accepted production semantics.

Only then may HQ issue a runtime implementation authority.

---

## 12. CURRENT DISPOSITION

`ROUND1_PROVISIONAL_SYNTHESIS_COMPLETE__ROUND2_SIX_CELL_HOSTILE_COURT_AUTHORIZED__NO_RUNTIME_IMPLEMENTATION_YET`

Round-2 workers may not self-authorize implementation or production adoption.
