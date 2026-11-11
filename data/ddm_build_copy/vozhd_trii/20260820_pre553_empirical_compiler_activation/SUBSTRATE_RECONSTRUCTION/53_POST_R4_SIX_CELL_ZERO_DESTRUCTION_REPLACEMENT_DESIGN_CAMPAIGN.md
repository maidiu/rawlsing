# VOZHD TRII — POST-R4 SIX-CELL ZERO-DESTRUCTION REPLACEMENT DESIGN CAMPAIGN

Status: `AUTHORIZED__NON_DISPOSITIVE__DESIGN_AND_PROOF_ONLY__SIX_CELL_LIMIT__NO_RUNTIME_MUTATION`

Repository: `maidiu/rawlsing`

Control branch: `agent/vozhd-trii-pre553-substrate-reconstruction-control`

Parent control commit: `27f540986685a8c3c323d64eab7061c6f008d6ec`

Binding parent safety law:

`52_POST_R4_PHYSICAL_OPTIMIZATION_CANDIDATE_REGISTER_AND_SAFETY_LAW.md`

Frozen PRE553 semantic parent:

`9188dc9fb7a8b92b981f3d3f94754cd6137d17b1`

Accepted R4 reference implementation under the current P2 court:

`20cfc676bdcebbf9aa5ef129bb7b94451f3af175`

## 0. PURPOSE

This campaign exists to answer one bounded question:

> **What is the smallest, safest, fully lossless replacement physical design that preserves the complete Rawlsing empirical/query/discovery/admission contract while eliminating the real-scale resource pathologies exposed by R4?**

This is NOT an authorization to implement or adopt a replacement runtime.

This is NOT a reopening of C11 semantics, I03, I05, I04, V553-V558, V3, V2, or whole-machine architecture.

This is NOT a requirement to spend additional hours explaining the internal failure mechanics of a representation that has already failed a real resource gate.

The campaign shall use already-returned/accepted evidence about R4 only to the extent needed to establish a baseline/reference behavior. It shall not rerun a failed full-source court merely to diagnose the corpse when the same time can be spent proving a safer replacement.

The campaign instead spends its effort on:

1. exact preservation obligations;
2. explicit information-accounting;
3. source-law assumptions;
4. hostile counterexamples;
5. replacement architecture;
6. independent equivalence oracle;
7. integration/minimality synthesis preparation.

## 1. ZERO-DESTRUCTION LAW

No cell may change runtime code.

No cell may modify `rawlsing_next/**`.

No cell may modify existing source authority, decoder authority, C11 authority, I03/I05/I04 contracts, gate ledger, campaign DAG, V553+, V3, V2, or whole-machine closure.

No cell may delete, rename, supersede, or weaken any accepted artifact.

All work is design/proof/reconnaissance only.

Each cell writes only under:

`data/ddm_build_copy/vozhd_trii/20260820_pre553_empirical_compiler_activation/SUBSTRATE_RECONSTRUCTION/POST_R4_SIX_CELL_DESIGN/<CELL>/`

Private scratch may be used for experiments. Raw sources, extracted sources, giant carriers, temporary databases, and large logs must never be committed.

A cell may propose code shapes, schemas, algorithms, invariants, pseudocode, benchmark harnesses, property tests, and implementation contracts. It may not install them into runtime.

Every proposal remains `NON_DISPOSITIVE` until HQ synthesis and a later explicit implementation authority.

## 2. NO-UNNECESSARY-R4-AUTOPSY LAW

The fleet is forbidden from consuming time on broad forensic reconstruction of why R4 failed at full scale.

Allowed R4 inspection:

- inspect accepted R4 code to understand the reference logical interface and existing invariants;
- use bounded R4 behavior as a reference oracle where already available;
- identify only those implementation mechanics that a replacement must avoid or preserve;
- cite accepted/returned resource evidence if it becomes available in GitHub.

Forbidden unless HQ separately authorizes a named need:

- rerunning a failed full-source R4 job merely to obtain more detailed phase telemetry;
- exhaustive profiling of dead R4 internals;
- optimizing R4 for its own sake;
- treating R4 physical details as semantic authority.

The reference is ultimately:

`RAW SOURCE / SOURCE-NATIVE TRUTH + FROZEN C11 + I03 + I05 + I04 + CLOSED WHOLE-MACHINE LAW`,

not R4 implementation accidents.

## 3. SIX-AGENT CEILING / RAW-SOURCE ACCESS LAW

Exactly six worker cells are authorized by this campaign.

No seventh worker may be created from this authority.

Default evidence path is repository-first:

1. governing whole-machine corpus;
2. Authority 52 and this campaign;
3. C11 / I03 / I05 / I04 authorities and code;
4. source constitution and decoder contract;
5. `SOURCE_BYTE_INVENTORY.csv`;
6. accepted SR03 source-native physical manifests;
7. accepted SR09-PRE family reconnaissance returns;
8. historical empirical functionality authorities and implementations where needed.

Raw-source access is NOT mandatory when the checked-in authorities/manifests already prove the relevant physical fact.

However, if a cell has a named unresolved physical assumption that cannot be proved from checked-in evidence, that SAME cell may perform a targeted raw-source probe.

Raw-source access is bound to these six cells only.

No separate raw-source reconnaissance worker may be spawned.

Any targeted raw-source probe must:

- use only exact CLOSED_35 source files already in `SOURCE_BYTE_INVENTORY.csv`;
- verify exact SHA before reading;
- obey the frozen decoder/compatibility law;
- extract/read only the minimum source(s)/variables/rows needed to resolve the named assumption;
- remain source-physical unless accepted semantic authority explicitly governs meaning;
- record exactly why raw access was necessary;
- record the source SHA and precise probe scope;
- never add a new source or substitute a newer wave;
- never commit raw bytes.

If an issue would require broad raw-source work beyond the six-cell scope, return:

`BLOCKED__RAW_SOURCE_EVIDENCE_EXCEEDS_SIX_CELL_CAMPAIGN`

and stop. HQ decides.

## 4. COMMON READ-FIRST LAW

Every cell must begin from the complete machine, not the local optimization problem.

Read at minimum:

- `data/ddm_build_copy/vozhd_dva/20260817_downstream_completion/RAWLSING_GOVERNING_SPIRIT.md`
- `data/ddm_build_copy/vozhd_dva/20260817_downstream_completion/CONSTRAINTS_PRIORITIES.md`
- `data/ddm_build_copy/vozhd_dva/20260817_downstream_completion/TERMINAL_DEMAND_ENVELOPE.md`
- `data/ddm_build_copy/vozhd_dva/20260817_downstream_completion/ARCHITECTURE_PASS_LAW.md`
- `data/ddm_build_copy/vozhd_dva/20260817_downstream_completion/CAPABILITY_MATRIX.md`
- whole-machine architecture closure ruling
- `SUBSTRATE_RECONSTRUCTION/00_COMMAND_CHARTER.md`
- `SUBSTRATE_RECONSTRUCTION/02_GATE_LAW.md`
- `SUBSTRATE_RECONSTRUCTION/09_SOURCE_NATIVE_CONSTITUTION.md`
- `SUBSTRATE_RECONSTRUCTION/10_FORMAT_DECODER_CONTRACT.md`
- `SUBSTRATE_RECONSTRUCTION/12_WVS_LITS_HOSTILE_FIXTURE_ORACLE.md`
- `SUBSTRATE_RECONSTRUCTION/49_SR06_R4_FINAL_ACCEPTANCE_AND_REAL_SOURCE_REOPEN.md`
- `SUBSTRATE_RECONSTRUCTION/50_SR07_SR08_P2_R4_REAL_SOURCE_SCALE_CONFIRMATION_AUTHORITY.md`
- `SUBSTRATE_RECONSTRUCTION/52_POST_R4_PHYSICAL_OPTIMIZATION_CANDIDATE_REGISTER_AND_SAFETY_LAW.md`
- this file

Then inspect only the additional code/authority needed for the assigned cell.

## 5. COMMON ABSOLUTE INVARIANTS

Every cell must preserve or explicitly defend all applicable items below:

- exact source identity and source-native physical distinctions;
- complete respondent-grain incidence;
- M01-M18;
- ExactRef / content-hash identity laws;
- raw versus authorized canonical value separation;
- physical missingness versus semantic response/absence separation;
- routing/applicability/risk-set distinctions;
- multiple/repeated/ordered/ranked topology;
- weights/design/measure authority;
- source relation/nonduplication provenance;
- exact provenance/replay/integrity;
- arbitrary lawful respondent-level conjunctions;
- I03 exact-query positive and negative truth conditions;
- I05 exact-bounded discovery frontier, including unforeseen combinations not pre-indexed by the carrier designer;
- I04 structural-admission law;
- historical empirical functionality conserved into the generalized query/discovery layer: joints, cotravel, forks, recursive forks, conditional reversals, co-signatures, cloud-like diagnostics, determinicity-like structures, support/uncertainty, temporal/source differences;
- source evidence != structural prior != generated fact != actor knowledge != memory != expression;
- downstream carrier ignorance: physical layout must not become semantic branching in I03/I05/V553+.

Any proposal that cannot preserve an invariant returns a named contradiction/rejection. It does not weaken the invariant.

## 6. COMMON REQUIRED RETURN SHAPE

Each cell must commit small artifacts only, including at minimum:

- `RESULT.md`
- `RESULT.json`
- `ASSUMPTION_LEDGER.csv`
- `INFORMATION_PRESERVATION_LEDGER.csv`
- `SELF_RED_TEAM.md`

Where useful also include:

- `PROPOSED_CONTRACT.md`
- `HOSTILE_CASES.csv`
- `BENCHMARK_PLAN.md`
- small bounded proof receipts/scripts under the cell directory only.

Every `RESULT.md` must contain these exact sections:

1. `WHOLE_MACHINE_CONTAINMENT`
2. `PROBLEM_OWNED`
3. `PROPOSED_MECHANISM`
4. `WHAT_CHANGES_PHYSICALLY`
5. `WHAT_MUST_NOT_CHANGE_LOGICALLY`
6. `INFORMATION_ACCOUNT`
7. `ASSUMPTIONS_AND_AUTHORITY`
8. `HOSTILE_COUNTEREXAMPLES`
9. `I03_I05_I04_EFFECT`
10. `INTEGRITY_REPLAY_EFFECT`
11. `RESOURCE_EXPECTATION`
12. `COMPLEXITY_COST`
13. `RAW_SOURCE_PROBES_IF_ANY`
14. `REASONS_TO_REJECT_OWN_PROPOSAL`
15. `FALSIFICATION_CONDITIONS`
16. `SYNTHESIS_REQUIREMENTS`
17. `RECOMMENDATION`

Every omitted logical field/material must receive exactly one disposition in `INFORMATION_PRESERVATION_LEDGER.csv`:

- `STORED_DIRECTLY`
- `DERIVED_FROM_IMMUTABLE_RELEASE_LAW`
- `DERIVED_FROM_QUESTION_GRAIN_AUTHORITY`
- `DERIVED_FROM_RESPONDENT_GRAIN_AUTHORITY`
- `DERIVED_FROM_TYPED_EVENT_INCIDENCE`
- `PRESERVED_IN_EXACT_SPARSE_EXCEPTION`
- `NOT_APPLICABLE`
- `REJECTED_NOT_PROVEN_DERIVABLE`

Forbidden dispositions:

- `probably redundant`
- `usually constant`
- `not needed by current queries`
- `recoverable somehow`

## 7. CELL R01 — STREAMING / MEMORY-BOUNDED / TRANSACTIONAL CARRIER MECHANICS

Branch:

`agent/vozhd-trii-postr4-r01-streaming-memory`

Write only:

`.../POST_R4_SIX_CELL_DESIGN/R01_STREAMING_MEMORY/`

Own candidates primarily:

- C01 streaming event/authority/dependency overrides;
- C02 streaming/merge read and audit;
- C04 immutable computation caching;
- C15 bounded pipelined compilation;
- C16 Parquet batch/row-group/compression mechanics;
- C17 telemetry;
- transactional publication mechanics relevant to streaming.

Mission:

Design the simplest genuinely bounded-memory long-form carrier mechanics that preserve the current logical R4/C11 behavior while eliminating corpus-scale Python retention and eager reopen materialization.

Must specify:

- deterministic ordering and duplicate-override law;
- bounded writer state;
- bounded reader/audit state;
- exact random reconstruction strategy;
- crash/partial-publication invalidation;
- atomic/sealed release publication;
- progress/resource telemetry contract;
- deterministic concurrency/pipeline constraints if any;
- what R4 validation behavior must remain observable.

Do NOT optimize semantics or claim functional dependencies owned by R02.

Raw source normally unnecessary. If used, justify a named physical performance/shape question that manifests cannot answer.

Required token:

`POST_R4_R01_STREAMING_MEMORY_RETURNED`

## 8. CELL R02 — GRAIN / FUNCTIONAL DEPENDENCY / TYPED ENCODING / LOCATOR COMPACTION

Branch:

`agent/vozhd-trii-postr4-r02-grain-types`

Write only:

`.../POST_R4_SIX_CELL_DESIGN/R02_GRAIN_TYPES/`

Own candidates primarily:

- C03 normalization by true grain;
- C05 native typed raw-value lanes;
- C06 derivable row/question/event locators;
- C07 question/relation defaults + sparse exceptions;
- C12 adaptive per-variable physical encoding;
- C13 hot/cold canonical information separation;
- C19 implicit physical locator if and only if immutably lawful.

Mission:

Construct an exact functional-dependency and type-preservation account for how repeated event-level material might be stored once at release/question/respondent grain without semantic or source-physical loss.

Must be hostile to apparent redundancy.

For every proposed omission from event grain, prove:

- governing determinant;
- scope of validity;
- exact exception path;
- source-family counterexamples;
- reconstructability;
- failure behavior if the dependency does not hold.

Must explicitly investigate float edge cases, signedness/overflow, strings/Unicode/null bytes, date/time/native format issues, missing declarations, value labels, mixed types, repeated/ranked structures, and decoder order assumptions.

Use checked-in manifests/recon first. Targeted raw probes are authorized where a dependency/type question cannot otherwise be proved.

Required token:

`POST_R4_R02_GRAIN_TYPES_RETURNED`

## 9. CELL R03 — INDEPENDENT SEMANTIC EQUIVALENCE ORACLE / HOSTILE CORPUS

Branch:

`agent/vozhd-trii-postr4-r03-equivalence-oracle`

Write only:

`.../POST_R4_SIX_CELL_DESIGN/R03_EQUIVALENCE_ORACLE/`

Mission:

Design the independent acceptance oracle against which ANY future replacement carrier must be tested.

This cell must not design the preferred storage representation.

Reference authority is the frozen semantic/source/query/admission corpus, not R4 implementation accidents.

Produce a precise oracle covering:

- source identity/shape;
- physical preservation;
- every logically observable C11 field / M01-M18 obligation;
- ExactRef/semantic identity;
- topology/order/rank/multiplicity;
- routing/applicability/risk-set;
- weights/design;
- provenance/replay;
- I03 positive results;
- I03 negative/failure states;
- I05 pair/k-way/conditional/reversal/recursive/branch/cloud-like operations;
- an I05 workload not used to tune physical storage;
- I04 admission parity;
- determinism;
- corruption/fail-closed behavior;
- cache deletion/rebuild behavior.

Design property/metamorphic tests capable of generating hostile logical/source cases, including rare exceptions.

Identify which checked-in source-family evidence is required so the oracle is not WVS/LiTS-shaped.

Targeted raw probes are authorized only to create/verify a named hostile fixture not already established by checked-in source manifests/recon/authority.

Required token:

`POST_R4_R03_EQUIVALENCE_ORACLE_RETURNED`

## 10. CELL R04 — VECTORIZED / COLUMNAR / MATRIX / BITMAP / LATE-MATERIALIZATION ENDGAME

Branch:

`agent/vozhd-trii-postr4-r04-columnar-vector`

Write only:

`.../POST_R4_SIX_CELL_DESIGN/R04_COLUMNAR_VECTOR/`

Own candidates primarily:

- C08 direct vectorized physical compiler;
- C09 question-oriented/columnar organization;
- C10 physical-state/predicate bitmaps;
- C11 late materialization;
- C20 source-local physical specialization behind uniform C11;
- C21 canonical matrix/columnar incidence + virtual long event view.

Mission:

Design the strongest plausible endgame physical architecture while treating it as a hostile proposal that must earn acceptance.

Must specify:

- exact canonical physical members;
- uniform logical C11 interface;
- how arbitrary respondent-grain conjunctions remain possible;
- how respondent-wise joints remain efficient enough;
- how I05 can discover unforeseen combinations without re-ingest or finite precomputed query vocabulary;
- topology/routing/design representation;
- source-specific compiler boundaries without downstream semantic branching;
- optional bitmap/index status as `NONAUTHORITATIVE__REGENERABLE_CACHE` unless separately proven canonical;
- vectorized validation replacing any invariant currently enforced only by Python semantic constructors;
- performance comparison workloads against a streaming-long baseline;
- complexity costs and conditions under which this design should be rejected in favor of a simpler carrier.

This cell does not get to declare matrix/columnar superior merely because it compresses well.

Targeted raw-source probes are authorized for actual layout/type/cardinality/topology questions not proved by manifests/recon.

Required token:

`POST_R4_R04_COLUMNAR_VECTOR_RETURNED`

## 11. CELL R05 — INTEGRITY / REPLAY / CACHE / PUBLICATION / CANONICAL-COPY LAW

Branch:

`agent/vozhd-trii-postr4-r05-integrity-publication`

Write only:

`.../POST_R4_SIX_CELL_DESIGN/R05_INTEGRITY_PUBLICATION/`

Own candidates primarily:

- C14 chunked/Merkle-like integrity;
- C18 one canonical physical copy + regenerable caches;
- integrity side of C13/C20/C21;
- transactional publication and crash recovery independent review.

Mission:

Specify a fail-closed publication/integrity/replay model that permits partial reads and efficient reopen only if it is equal-or-stronger than current authority expectations.

Must specify:

- release identity and root manifest;
- member/chunk hashing model;
- verification states and when positive empirical evidence is permitted;
- atomic publication / incomplete-release behavior;
- cache identity/invalidation/deletion/rebuild law;
- canonical versus nonauthoritative material;
- deterministic rebuild identity;
- corruption tests at manifest/member/chunk/index levels;
- replay requirements;
- no hidden persistent database/second authority;
- migration/rollback safety for a future replacement carrier.

Must explicitly red-team lazy verification: no unverified corrupt material may silently contribute positive evidence.

Raw source normally unnecessary.

Required token:

`POST_R4_R05_INTEGRITY_PUBLICATION_RETURNED`

## 12. CELL R06 — CROSS-CELL ADVERSARIAL RED TEAM / MINIMALITY / SYNTHESIS PREPARATION

Branch:

`agent/vozhd-trii-postr4-r06-redteam-minimality`

Write only:

`.../POST_R4_SIX_CELL_DESIGN/R06_REDTEAM_MINIMALITY/`

Mission:

Assume the other five cells are clever and wrong.

Independently attempt to defeat every candidate family in Authority 52 and every expected design direction in R01-R05.

This cell owns no preferred implementation.

It must produce:

- cross-source hostile assumption matrix;
- likely hidden-coupling map;
- queries/capabilities most likely to be starved by question-oriented/bitmap/vectorized layouts;
- source shapes most likely to defeat functional-dependency compaction;
- integrity/replay failure modes;
- constructor/invariant bypass risks;
- maintenance/complexity traps;
- criteria for removing unnecessary layers from synthesis;
- explicit conditions under which the correct synthesis is merely streaming-long and NOT the more elaborate endgame;
- explicit conditions under which a Class C physical-grain change is actually justified;
- a proposed one-runner integration contract skeleton;
- a `DO_NOT_COMBINE` list identifying individually sound ideas that become unsafe or redundant when composed.

Use accepted source manifests and SR09-PRE returns aggressively. Targeted raw probes are authorized only for named counterexamples not resolvable from checked-in evidence.

Required token:

`POST_R4_R06_REDTEAM_MINIMALITY_RETURNED`

## 13. WORKER NON-INTERFERENCE LAW

Cells do not read each other's unaccepted branch returns while working.

They may read only shared parent authorities and accepted repository evidence.

This prevents convergence by social copying and preserves independent discovery of contradictions.

HQ alone compares and synthesizes returns.

No cell may merge another cell.

No cell may update the control branch.

## 14. HQ SYNTHESIS AFTER ALL SIX RETURNS

After all six returns are available, HQ must independently audit each against TheVision/whole-machine law before local technical merits.

HQ then produces a separate synthesis authority. That future synthesis must:

1. reconcile contradictions among the six;
2. preserve negative findings, not just attractive mechanisms;
3. define a single canonical logical interface;
4. define a field-by-field information ownership/derivation ledger;
5. choose the minimum sufficient physical mechanisms;
6. explicitly reject unnecessary candidate layers;
7. bind an independent equivalence/property oracle;
8. bind a bounded hostile implementation court;
9. bind one shadow replacement runner;
10. forbid promotion until exact parity passes;
11. define real-source WVS/LiTS scale acceptance;
12. define rollback/deletion of failed experimental carriers;
13. preserve the existing accepted machine untouched until promotion authority.

There is no automatic requirement to implement every candidate in Authority 52.

The synthesis objective is:

> **the smallest coherent replacement design that preserves all Rawlsing capability and closes the resource problem with comfortable margin.**

## 15. ACCEPTABLE CELL DISPOSITIONS

Each cell returns exactly one:

- `RETURNED__SAFE_DESIGN_CONTRACT_PROPOSED`
- `RETURNED__PARTIAL_SAFE_COMPONENTS_ONLY`
- `RETURNED__CANDIDATE_FAMILY_REJECTED`
- `BLOCKED__NAMED_AUTHORITY_REQUIRED`
- `BLOCKED__RAW_SOURCE_EVIDENCE_EXCEEDS_SIX_CELL_CAMPAIGN`
- `BLOCKED_POTENTIAL_FROZEN_CONTRACT_CONTRADICTION`

No cell may return `ACCEPTED` or `IMPLEMENT`.

## 16. CURRENT CAMPAIGN DISPOSITION

`SIX_CELL_REPLACEMENT_DESIGN_FLEET_AUTHORIZED__NO_RUNTIME_IMPLEMENTATION_AUTHORIZED`

The fleet may launch immediately once exact worker branches are created from the commit containing this authority.
