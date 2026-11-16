# 03 — Design space, strongest alternatives, and savage self-critique

**Status:** comparative architectural analysis, NOT authorization, implementation, final architecture, or verified speedup. The objective is to reason aggressively enough that *one* eventual implementation dominates without building several production contestants. The strongest argument for a rejected design must be retained.

## A. Optimize the right objective

The objective is **minimum total cost of an *actually useful*, scientifically correct, permission-valid whole-machine workload**, not minimum disk bytes, fastest single query, or cheapest initial source decode. Cost includes: engineering effort; original-source interpretation; semantic correctness; cold/steady operations; memory and scratch; replay, revocation and recovery; output and intermediate sizes; downstream discoverability; future missing-function integration; scientific/owner proof; source permission. A design that accelerates present I03 while blocking recursive or temporal science is inferior even if its microbenchmarks win.

The smallest unit of comparison is not one fixed query; it is a **workflow involving multiple distinct queries and transformations**, including F1/F2/F3/F4, ordinary and minority/contrary cases, repeated conditional populations, source/science holds, valid negatives, and a real FF/possibility consumer.

## B. Physically separate concerns, not responsibility

1. **Truth/authority:** exact source rights, survey language and questionnaire, respondent identity, routing, weight design, evidence and replay law.
2. **Canonical representation:** complete irreducible C11 records, durable schema, physical member integrity and atomic publication.
3. **Access:** which respondent/question/occurrence is where; cold read and selective projection.
4. **Analytical computation:** distribution, conditional, overlap, recursive branch, joint, comparative, temporal and signed diagnostics at their authorized grades.
5. **Issued scientific results:** final facts, negatives, provenance closure, replay and later product/possibility/actor seams.

These are conceptually distinct. They need not each perform an entire body serialization or a full fresh universe scan. **The boundary contract is the unit of optimization**, not the number of database brands in use.

## C. Initial staging architectures — choices and objections

| Candidate | Rational upside | Structural deficit / cost | Provisional analytic position |
|---|---|---|---|
| Keep source→13 JSONL journals→readback→direct writer | Very clear replay/finite intermediate; already coded and scoped tested | Extra original-to-body serialization and reconstruction on *integrated* source path; temp disk, source-to-publisher duplication | **Working compatibility fallback**, not selected ideal; do not conflate with direct 100k writer benchmark |
| Direct source-stream private Parquet staging while simultaneously certifying source | One typed object feeds proof and staging; avoids JSONL materialization; one physical estate | Must preserve independent source-to-staged-body binding and crash/partial-publication invariants; cannot remove all proof | **Promising later integrated bridge correction**, subject to exact equivalence |
| Replace JSONL with Arrow IPC then feed writer | Typed stream and potentially lower conversion cost | Still intermediate whole-corpus staging and transfer unless shared zero-copy end-to-end; duplicate validation may remain | **Not justified as first move** |
| Eager in-memory complete object graph | Easy ordinary object access; simple code | Observed old W03 memory ceiling breach; potentially scales with entire universe | **Rejected for default large-survey execution** |
| Typed Parquet with no canonical body_json | Could improve selective scan and reduce duplicate fields | Needs lossless versioned all-13-family reversible codec and changed verifier/replay/reader; schema/ABI churn | **Deferred until data shows current body is critical cost** |
| Full PostgreSQL/DuckDB replatform | Attractive query planner, indexes, relational operations and historical DDM familiarity | New authority, typing, exact identities, replay, cold restore and output boundaries; not a cure for source interpretation or duplicate proof | **No ungrounded wholesale replatform**; a narrowly embedded accelerator may be useful only if it preserves native semantics |
| Retain accepted Parquet/Zstd with derived access and execution substrate | Reuses accepted canon/proof and adds better question-major/respondent-major computation | Requires careful index integrity, power over exact query/replay, incremental comp identity, memory budget | **Strong current candidate, not final adjudication** |

## D. Proof replacement — the tempting but invalid shortcut

**Bad proposed shortcut:** Hash canonical source rows and hash emitted rows, compare equal, replace per-row semantic validation.

**Counterexample:** The same defective producer projects respondent A's Q17 as respondent B's Q17. Writer and verifier compute matching hashes over the wrong projection. Perfect cryptographic consistency; scientifically false assignment.

**Required design:** independent checks across **source record→canonical body→typed selector→exact identity→routing/authority→I02 root**. Whole-file hashes prove persisted bytes did not change; independently pinned semantic commitments/proofs prove *what bytes should mean*. An optimized verifier may avoid constructing expensive full public Python objects, but only if it independently checks the same semantics and detects omission, duplicate, value/typed state mismatch, relocated occurrence, wrong respondent, wrong topology, wrong authority and forged/rehashed transport.

**Never:** replace independent verification with two implementations of the same broken canonicalization routine, or call a cryptographic hash a scientific authority.

## E. Second I02 proof — duplicated or necessary?

- **Separate S2-C direct writer:** builds the semantic I02 proof over one supplied thirteen-family stream. Must continue doing that absent an equivalent external qualified certificate.
- **S1-E integrated source bridge:** upstream certified source stream is journaled/reconstructed, then the direct writer constructs another I02; matching roots establish that reconstructed stream corresponds to upstream semantics. To remove one proof, **ensure same source objects actually reach staging and independently bind staging to upstream certified roots**.
- **Better staging proposal:** source construction emits typed objects once into two logically separate consumers (semantic proof, bounded private physical sink). Physical readback/locators checked independently and bound to finished upstream I02 before atomic publish. A failure at any point prevents release. Crash recovery must not treat unpublished files as accepted proof.
- **Boundary:** no blanket claim that full physical reread is unnecessary. If later using streaming row-group commitments, prove same physical fidelity and independent representation checks first.

## F. Physical I02 SQL optimization — narrow and plausible

Old sourcefree builder appears to maintain text-heavy primary/secondary indexes, uniqueness checks, relational validation and canonical sorting. Plausible improvement: grouped prepared inserts, constraints instead of redundant SELECTs *when negative equivalence proven*, and bulk/index timing changes *where exact proof semantics permit*. Existing SQLite roots and typed integrity errors must not drift. May save substantial time/scratch, but speedup is **unknown** because the measured 3,033s was not decomposed into SQL, row serialization, physical reread and compression.

**Rejected extension:** automatically replace exact ref keys with local ordinals in the proof DB. That adds a string→ordinal dictionary, collision/identity proof, canonical order reconstruction and joins; its net effect is not known. **Ordinals are more clearly justified as local *analytical addresses* in a read-only derived index**, not as canonical ref replacements.

## G. Saved execution index — temporary vs persistent

- Current temp SQLite postings index rebuilt per session: simple lifetime/trust/cleanup and added verification, but expensive on every process cold start.
- New prepared session reuses one index **within** a session, reducing build count. Does not qualify cross-process persistence or reuse scientific computations.
- Durable index could eliminate repeated cold build, but is a new derived trust artifact: exact release root, index-version/codec, physical member IDs, tamper refusal, crash-safe build, permission/currentness, deterministic rebuild and cache eviction must hold. It cannot silently suppress source-member authentication, nor be considered authorized forever.
- Analytical presumption: **use execution-local preparation first; persist demonstrably stable expensive structures under a release-derived commitment once semantics are settled.** Do not introduce an index per query/class/source without evidence that its reuse actually pays.

## H. Question-major vs respondent-major / joined access

**Person-first** (respondent→events) is necessary to preserve same-person response coherence and repeated occurrences. **Question-first** (variable→respondents) is important to efficiently prepare single-variable distributions and many query families. They should be complementary locators into one canonical release, **not duplicate authoritative event stores**.

Only person-first can lead to roughly N×Q selection attempts for many questions; only question-first can make same-person joins awkward or tempt marginal multiplication. A **shared respondent ordinal under one exact source universe**, with question postings and occurrence locators, supports selective column access and exact joins. Ordinals never replace canonical respondent refs, source identity or order semantics.

**Open physical question:** Which projections should be dense typed arrays, compressed bitmaps, sparse postings, Arrow/DuckDB accelerated vectors or lazy body accesses? **Do not choose a fashionable type before enumerating topology/routing, multi-select, weighted and negative cases.**

## I. Early graph/caching enthusiasm — risks

A plan to cache all possible condition intersections is exponential in predicate count. A full cross-product of target domains can also explode, even if few realized cells exist. A plan to retain every `_GroupCore` may copy every respondent ID, answer cell and used-source-ref across thousands of operations.

**Stronger approach:** lazy/incremental dependency DAG with bounded memory and eviction; reuse primitive conditions and truly common intersections; store compact membership addresses plus independently recoverable provenance; exact numeric products emitted only for *authorized* operations. Demand-driven computation avoids combinatorial upfront materialization.

**Potential failure:** computed boolean masks alone erase unknown/not-asked/unauthorized/unresolved distinctions, evidence and per-child provenance. Stage 4 needs typed/evidence-bearing computation contracts, not merely booleans.

## J. Output format is part of economics

Current v1 `EmpiricalFact` and replay have explicit risk/denominator member refs, full cell structure and provenance used-object refs. Shared preparation does not prevent an output lower bound of **O(number of required emitted references)**. The illustrative 100k respondents×1k facts×64 bytes = **6.4GB** before overhead (not a benchmark).

**Candidate:** a versioned authenticated population witness referenced by many results, with complete sorted expansion and authority replay on demand. **Not allowed silently:** substituting witness for required v1 refs or reducing source closure to unsupported counts. Scientific/output owner must approve a new exact replay contract and downstream readers.

## K. The “optimal design” hasn't been selected yet

A partial preference for Parquet+derived computation follows from reuse of accepted capital and costs of broad replatforming. But ANVIL cannot treat current Parquet/13-family layout as sacred *if later full consumer obligations show a fundamental inability to preserve/use source information economically*. Nor should it reopen old proven-wrong W03 for nostalgia.

**This is the real open judgment:** what canonical data, source semantics, computed intermediates, facts, scientific qualifications and concrete downstream consumer requests must coexist; which must be durable; which may be regenerable; what is their access complexity; where to place proof boundaries; and which arrangement has the lowest *whole-machine* cost and scientific loss.
