# 07 — Threat model: ways a more elegant C11 engine could become false

**All statements here describe what a correct design must preserve, or hypotheses that need direct falsification.** Do not convert this into an infinite new mandatory test suite. Bind actual tests to accepted existing contracts, real owner demands and demonstrated risk.

## 1. Source/meaning integrity

| Failure | Concrete dangerous optimization | Correct invariant / negative |
|---|---|---|
| Wrong questionnaire/edition | Reuse same variable label across waves | exact native source, form/edition, QSM selected codebook and option/skip rules; otherwise noncomparable/unresolved |
| Selected semantic overlay silently omitted | Carry old role/scale merely because item exists | F03/F08/QRA/QUC applied-vs-member and specificity/duplicate-conflict proofs |
| Different native answer collapsed | Normalize 0/1/9/997/998/−1 as metric numbers | preserve actual semantic and typed code/state; no assumed order or scale |
| Repeated/multiple event coalesced | first encountered respondent×question row wins | preserve each response occurrence, component, order, rank, source row |
| Survey population misidentified | treat household/country frame as individuals with known probability | exact universe, sampling units, eligibility/asked/observed/routing |
| Unapproved weight/design | use available `weight` column by default | exact chosen estimand, basis, validity/strata/cluster where science requires, typed missing/invalid |
| Incorrect cross-source coupling | join WVS and ArabBar people by demographic label | no same-person identity or pooling without actual design and relation authority |

## 2. Statistical and analytical integrity

| Failure | Temptation | Falsifier |
|---|---|---|
| False zero / empty | Translate `NOT_ASKED` or `ROUTING_UNKNOWN` to false bitmap | exact eligible/asked/observed/routing negative parity; unknown must remain unknown/refuse |
| Wrong denominator | Reuse previously cached group regardless of target/risk | F2 forward/reverse produce independently correct bases and support |
| False joint | multiply 2×2 marginals to fabricate 3-way F4 | two datasets with same marginals but different 3+ actual joints must yield different outputs |
| Lost branch meaning | cache child membership without parent/selection/stop evidence | recursive/minority path, chosen indicator, gain/support, truncation and ancestry survive |
| Mislabeled MI | reuse original “mutual_information” function by name | formula/estimand and actual eligible sample; true MI vs pointwise log ratio |
| Missing sample bias | compute weighted without design uncertainty and call it precise | inability to qualify uncertainty stays typed `UNCERTAINTY_UNQUANTIFIED`, not CI fiction |
| Dropped evaluated child | boolean `AND/OR` short-circuit during optimization | v1 fact provenance/used-authorities and negative evaluation equal accepted executor |
| Missing full-cell domain | sparse realized-only response cells served as full domain | requested complete-domain zeros, validity and states preserved without unbounded Cartesian default |
| False empirical→causal promotion | use correlation/majority as objective constraint or pressure | OBSERVED_ASSOCIATION vs EXPERIMENTAL_MODEL vs independently STRUCTURAL_CAUSAL_AUTHORIZED |
| Collapsed source time | same variable name = comparable across years | explicit wave/measurement/time/estimand relation or typed NONCOMPARABLE |

## 3. Security, authority and lifecycle integrity

- **Counterfeit source or external root:** writer hash cannot self-certify an incorrectly projected body. Independent anchoring and cross-representation semantic checks; mutate ref, body, selectors, locators, omission, duplicate and source identity.
- **Stale prepared index:** same filename or directory path does not bind same immutable physical member/semantic release; no stale release after republish/reopen.
- **CURRENT revocation mid-session:** preflight permission alone insufficient; repeated operations must check live rights at existing relevant boundaries, including after execution before issuing a result.
- **Wrong negative state:** deny/error/held is not unsupported query returning empty/zero; preserve typed refusal and exact trace.
- **Forged query/predicate:** attested source doesn't authorize arbitrary leaf/operation; exact query/predicate/catalog + grammar and source-science owner.
- **Wrong as-of world selection:** same empirical history but different active world or permission must not be treated as current; preserve historical replay vs current authorization.
- **Cross-agent self-acceptance:** author-run 80 PASS does not equal independent G5, and open branch does not equal protected CAS.
- **Incomplete crash publication:** on interruption, no half-written C11 or derived index appears as a complete, certified release.
- **False checkpoint reuse:** matching path/checkpoint name, simple hash or metadata isn't proof of same source/consumer/authority body; changed inputs must invalidate.
- **Unauthorized actor use:** learned statistical product is not an actor's belief, motive, action, consent or social relationship; SOROK separately owns these.

## 4. Common-mode validation failure

Construct independent test pairs: producer writes wrong question/response/typed-state field, both producer and verifier share wrong projection, hashes agree. The correct test must be grounded in an independently generated expected semantic body/role and see mismatch. Testing both sides with the same serializer is not independent verification.

Proof/certification has layers:
1. Source/authenticity/rights (independent external owner/custody).
2. Scientific questionnaire/sampling interpretation (issuer).
3. Logical thirteen-family semantic consistency (I02).
4. Physical body/selector/locator fidelity and atomic publication.
5. Query/analysis evidence, typed refusal and replay.
6. Actual first-consumer identity, current/as-of and authority.
No hashing layer substitutes for any other.

## 5. Physical/resource failure modes

- **Memory:** aggregate process tree ≤6GiB is the user-requested court for 100k; whole-core/risk/denominator caches can copy long IDs across hundreds of outputs; full object graph old W03 already exceeded limit.
- **Scratch amplification:** direct writer staging ~5.26GB/retained ~310MB and I02 temp ~4.39GB in one sourcefree run; optimizations need full stage accounting, not just final Parquet size.
- **Cold startup:** full manifest member hashing, per-session temp SQLite posting, query index and output construction differ; warm prepared success doesn't prove restart.
- **Access explosion:** per-person lookup×targets×queries; high questionnaire width makes tiny 3.245 event/respondent pilot unrepresentative.
- **Joint-domain explosion:** F4 3+ targets can have product-domain size far larger than observed cells; the exact full-domain contract still matters even if stored sparsely.
- **Predicate-graph explosion:** precompute all subsets/conditional combinations creates exponential work; demand-driven reuse, bounded cache/eviction.
- **Provenance/output lower bound:** 1000×100k explicit respondent references is 100m refs before source closure; do not claim optimization can eliminate required output materialization without a new scientific version.
- **Materialization bottleneck shift:** speeding index build can expose raw/weighted fact assembly and replay as dominant cost; many queries can share preparation while legitimate unique outputs remain expensive.
- **Cost comparison deception:** compare direct S2-C to itself; don't attribute unrelated bridge JSONL cost to measured writer; separate old pre-W05 vs new W05; no invented baseline on nonmatching source width.
- **Concurrent query / index scope:** one prepared session may not safely serve independent rights contexts or parallel mutators; explicit scope and lifecycle must govern thread/process reuse.

## 6. Scientific/world failure modes

- **Reification of group statistics:** a conditional distribution describes possible patterns in a sampled population, not the actual personality/destiny of an individual.
- **Objective material positions inferred from attitudes:** class/ownership/authority/field position cannot be responsibly manufactured from opinion responses alone.
- **Causal language from descriptive geometry:** positive/negative correlation not evidence of mechanism, power, suppression or structural forcing.
- **No minorities/contradiction:** an aggregate “most likely” tendency cannot eliminate alternative/outlier/contrary configurations the world/person may follow.
- **Temporal flattening:** two cross-sectional surveys at two moments do not necessarily track individual development, still less repeated person events.
- **Unqualified hegemony:** majority preference ≠ institutional capacity to impose; must model ownership/control, coercion and actual structural conditions separately.
- **Premature all35:** user-selected Arab Barometer/WVS plus third-family universal falsifier does not justify source-specific hard-coding or an all35 launch requirement.

## 7. Test principle

Use a finite **selected-design falsification matrix**, not a multi-architecture contest:
- canonical 13-family body/typed refs, duplicate, poisoned locator, raw special state, missing/routing/weight/selector and source/authority;
- F1/F2/F3/F4 exact denominator, full-domain, 3+ same-person, reversed direction, minority branch and typed negative;
- source/country/wave/weight/estimand change; CURRENT revoke mid prepared session; multi-process cold/restart and interrupted write;
- FF01 descriptive fact consumption and refusal of unsupported FF02/N9; temporal/independent-survey only when selected science; actor interface only with separate owner;
- one realistic **wide** survey-shaped 1/10/100 distinct operations, actual output/ref volume, memory/scratch/wall and downstream changed-value/restore.
Any nonapplicable case must be justified by the existing exact owner contract, not silently counted as PASS.
