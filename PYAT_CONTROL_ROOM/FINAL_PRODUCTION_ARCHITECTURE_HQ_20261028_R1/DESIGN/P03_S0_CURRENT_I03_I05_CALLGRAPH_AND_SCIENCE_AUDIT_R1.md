# P03-S0 — Direct HQ exact-current I03/I05 computation, evidence and authority audit

**Owner:** Browser Architecture HQ; **no rabochiis**, no code edits. **Date:** 2026-10-28.
**Read cut:** `maidiu/rawlsing` integration/pre-main-reconciliation-r1 exact `299f41e97a43c67be9cc76a79fa49b48f4e12e54`.
**Epistemic class:** DIRECT_CURRENT_CONTROL_SOURCE_OBSERVATION (all named files fetched at this exact commit); neither runtime benchmark nor implemented refactor. SRC04 mounted packet is a *different later author branch* for some I03 files. Do not blend their implementations. Historic V550 grouped code is a design precedent, not adopted I03 semantic authority.

## 1. Exact code and SHA inventory

| Current file | Blob SHA | Named symbols and lines | Why relevant |
|---|---|---|---|
| `rawlsing_next/_pre553_query_common.py` | `938a6b03a63dd34ef4f0f63655ed8f11f65c5d92` | QUERY_EXECUTION_CONTRACT_ID 57, scope/measure/risk/topology enums 59–89, _ExecutionProfile 125, _TargetPlan 146, _ReleaseIndex 158, _Evaluation 173; _profile 285, _parse_target_plan 311 | Contract, exact declared target full domain (explicit or Cartesian), output material and encoded exact weight representation |
| `rawlsing_next/_pre553_query_predicate.py` | `8590bacf464b2c61f319f581820a3af76ed1e60c` | _build_release_index 19–74; _leaf_match 119–320; _compile_derived_branch_memberships 321–364; _eval_predicate 366–406 | Exact object indexes, all predicate dialects, authority closure, non-short-circuit boolean traversal |
| `rawlsing_next/_pre553_query_eval.py` | `f808dfcd2008cc71e9203de3cadf1abe14223974` | _UsedObjectAccumulator 11, _UsedAuthorityAccumulator 30; routing 48, risk membership 85; event topology 114–257; target 258; weight 280; _evaluate_index_group 318–493; _make_execution_replay_ref 521–551; _build_fact 552–651; negative 652–727 | Core per-respondent scan and native replay/evidence identity |
| `rawlsing_next/pre553_empirical_query.py` | `03facecf70890bfd13b80418620d274cbcd69d02` | _resolve_release_indices 65–97; _failure_code 148; negatives 169–227; _require_exact_i03_authority_fitness 228–372; execute_empirical_query 373–541; replay_empirical_query 542–575 | Exact permissions, source-scope branching and typed failure classifications |
| `rawlsing_next/pre553_discovery_exact.py` | `905f24d114419dbdd93879ad2bee5b59dd2f23af` | _compile_frontier 617+, _evaluate_candidate 994–1049, execute_exact_bounded_discovery 1050–1237 | I05 iterates each candidate's query roles via independent execute_empirical_query calls; full candidate/frontier coverage including negatives |
| `rawlsing_next/pre553_batch_runner.py` | `2d291600b9a10c56d9c6f6de7f7d619f6c52e829` | BatchExecutionRunner 385+, run 536 | Existing per-unit receipts/resume; not a license to change authority or operation catalog |
| `rawlsing_next/pre553_empirical_objects.py` | `a61365b994e5c3c50de0f598fcf40e90abf757b6` | canonicalize 181, canonical_json 215, semantic_hash 220, EmpiricalFact 696 | Precise result byte identity and exact numeric/no-float constraints |
| `rawlsing_next/pre553_recursive_handoff.py` | `868f43bf9869af5501fd67c3de7a2703ba4cb1b4` | replay_recursive_branch_membership ~574–613 | Separate N+1 consumer of same respondent-scoped data; not safe to replace with marginals |
| `rawlsing_next/pre553_c11_repository.py` | `67c6eb6494522cd11aab1b93d0e73f9cef6036f3` | C11LogicalRelease 19, C11Repository 52 | P01 must provide exact verified logical read view; P03 cannot independently mint C11 evidence |

## 2. Full present call chain / multiple independent queries

```text
I05 execute_exact_bounded_discovery
  verify discovery authority -> compile fixed, complete candidate frontier
  for each candidate:
    _evaluate_candidate:
      for each query role:
        execute_empirical_query(repository, query, predicate, registry, release_refs)
          validate query/predicate exact object identities, states, condition ref
          _profile & _require_exact_i03_authority_fitness (not mere ALLOW)
          _parse_target_plan => per-component exact authority and COMPLETE domain
          _resolve_release_indices => scan release.public_objects per universe and create respondent-grain indexes
          by source_scope_mode:
            SINGLE_UNIVERSE: one _evaluate_index_group
            SOURCE_INDEXED_MULTI_UNIVERSE: one _evaluate_index_group PER universe, negatives per universe
            AUTHORIZED_COMPOSITE: separate exact pooling/nonduplication/estimand authorities, one grouped evaluation
          _evaluate_index_group:
            compile derived-branch membership sets once (ALREADY IMPLEMENTED)
            bind current runtime authority/repository where present
            sorted release-universe loop; per-universe source/risk contract
            sorted respondent loop:
              resolve **all target** routing facts; validate all matches + authority (not just chosen)
              compute member/common-risk + runtime exact successor override
              if risk member: add risk ref; evaluate EVERY predicate leaf whose AST requests it
              if predicate true: add denominator ref; resolve weight only here
              if target domain nonempty: resolve each target component only now
              if resolved: canonical cell lookup, raw/weighted support accumulation
            derive ZERO_OVERLAP/NOT_APPLICABLE/ZERO_SUPPORT/VALID_EMPTY/UNRESOLVED/SUPPORTED
          _make_execution_replay_ref: query + predicate + releases/replay roots + EXACT risk/denom refs + complete cell payload
          _build_fact: exact used provenance object refs and used authority refs, complete zero/positive cell states,
                       raw+weighted numerator/denominator, exact scope/source and replay
      I05 collects ALL role results and all terminal candidate receipts; evaluates support and declared validation
```

I05's frontier enumeration is CURRENTLY FIXED before evaluation (docstring `execute_exact_bounded_discovery`). P03 may speed these calls but **may not claim that alone implements Authority-37 originary result-driven recursive fracture/J>=3 dynamic frontier**. That remains separate P06 science/implementation requirement.

## 3. Important prior optimizations ALREADY PRESENT

- `_UsedObjectAccumulator` and `_UsedAuthorityAccumulator` deduplicate by exact ref at append time; `_evaluate_index_group` also canonical-ref-sorts used objects at exit. Do not propose re-adding those as a novel performance fix. A list of refs still scales with the number actually used for a query.
- `_compile_derived_branch_memberships` already compiles exact branch-member sets once per `_evaluate_index_group` call. Do not call an equivalent per-query cache a new solution; the opportunity is **safe reuse across candidate roles/operations**, subject to binding/authority and witness-trace preservation.
- _ReleaseIndex groups objects by respondent in memory, but is rebuilt for each `execute_empirical_query` against a release and does not implement a compact persistent, common-substrate shared numerical operator.
- Native fact builders already use `Fraction`, complete declared target domains, exact member refs and canonical object refs. A counts-only batch result loses accepted semantics.

## 4. Current scientific-operational contract; not optional

**Risk membership**: _routing_fact_for finds all matching target+risk-set facts and **rejects absence**, conflicts in state/member-set; validates each fact's source authority and requires ROUTING_RISK_SET. _risk_membership rejects ROUTING_UNKNOWN/RULE_UNAVAILABLE rather than counting as nonmember. COMMON_ELIGIBLE needs all targets eligible; other modes have own disagreement law. Current runtime successor can override membership per exact query/target and reject conflict. `component_positive` and `inapplicable_count` affect typed states. Reuse must preserve these precise distinctions.

**Predicates**: _eval_predicate supports AND/OR/NOT/LEAF. Existing AND/OR computes a list of ALL child results without Boolean short-circuit. _leaf_match covers coordinate, response, routing, typed state, runtime governed response dialect, derived-branch cohort; validates relevant exact permissions and may append evidence even when overall predicate false. A bitmap intersection with no witness trail would silently change provenance, and short-circuit would change reachable errors and ref closure.

**Target realization**: _target_component_value accepts topologies with distinct semantics: scalar singular, unordered SET (deduplicates canonical values *at query output*, not source event identity), unordered multiset, ordered/ranked exact semantic key, repeated measurement/event, routed, componentized. It rejects unsupported topology, missing governing authority and ambiguous scalar >1. Full target configuration is computed only AFTER respondent is in exact risk AND predicate-true denominator, and only when domain nonempty. **Never eagerly validate/realize every respondent's target**, because exclusions may hide a topology problem that old I03 would lawfully never reach.

**Weights**: RAW = exact 1 as Fraction. GOVERNED_WEIGHTED fetches exactly one matching weight per **denominator member only**, checks typed state, design and estimand authorities, exact fraction and nonnegative. Global eager weight resolution would convert a valid conditional query into a failure on excluded rows.

**Complete cells and negatives**: _parse_target_plan requires exact arity, component topology/authority, uniqueness of declared domain; uses explicit joint_domain or full Cartesian product. _evaluate_index_group initializes zeros for ALL declared cells, even if supported observations never realize them. Distinguishes `ZERO_OVERLAP`, `NOT_APPLICABLE`, `ZERO_SUPPORT`, `VALID_EMPTY`, `UNRESOLVED`, `SUPPORTED`. Negative results also encode exception text and query/release scope: **error message and where exception arises can affect fact.ref**. No one-size-fits-all typed zero or silent sparse-only output.

**Source scope and use**: exact `SINGLE_UNIVERSE`, `SOURCE_INDEXED_MULTI_UNIVERSE`, and separately authorized `AUTHORIZED_COMPOSITE` cannot be combined; source-indexed emits separate facts, composite requires explicit pooling/nonduplication/estimand permissions. Exact current `_require_exact_i03_authority_fitness` validates operation, object families, universe scope and target-use permission or runtime successor grant. Unqualified release presence never authorizes execution.

**Native evidence**: `_make_execution_replay_ref` includes query/predicate refs, ordered release and ReplayManifest refs, risk member refs, denominator member refs, complete zero-inclusive cell projection and measure/scope parameters. `_build_fact` includes complete used C11 object refs/authorities as provenance and exact weighted/raw support. P03 cannot replace this with aggregate count or unqualified bitmap.

## 5. Proven algorithmic duplication — and bounds of inference

**Direct evidence**: `_evaluate_candidate` calls `execute_empirical_query` for every role; each call uses `_resolve_release_indices` to discover/universe-index, and `_evaluate_index_group` loops every respondent with repeated fact searches, predicate evaluation, authority resolution and possibly weight/target construction. A source-backed compact common view may avoid per-query release-wide object allocation and per-operation index building, and a batch engine can share repeated qualified row evidence. This is a justified optimization target.

**Not measured**: actual current-control per-phase cost; percentage due to Python traversal vs full C11 carrier vs replay JSON; speedup if grouping; memory peak for all35/J3; number of distinct I05 role queries per discovery frontier. Do NOT claim 10x/100x or that all ~15,545 remaining pairs share the same eligible risk set.

**Historical precedent only**: packet `06_INHERITED_IMPLEMENTATION/.../ddm_v550_shared_respondent_substrate.py` functions `canonicalize_shared_respondent_substrate` ~332, `validate_shared_respondent_substrate` ~517, `write_shared_respondent_substrate_atomic` ~565; `ddm_v550j_joint_patterns.py` (5,286 lines) contains respondent-coherent joint evaluation. Reuse physical grouping ideas only after exact current topology/authority audit; neither is a substitute for I03 original fact/replay schema.

## 6. S0 bounded exclusions and next stage

- This audit covers current named control files and current static semantics, not **every** unlisted branch/test, original survey cells, current Mac process, full SRC04 authored code or a full sourcefree end-to-end I03 run.
- There is no independently measured current I03 hot-path profile. Next P03-S1 defines a demand-driven shared evidence/witness interface with exact per-query authority epoch and provenance. Next P03-S2 specifies proof and sourcefree oracle harness, then Codex execution tasks. Maintain separate P01 verified execution view, P04 provenance/read-lifecycle, P06 recursive science and P05 workload/resume.
- **Failure condition**: no shared-cache proposal is acceptable if it changes exceptions, negative classification/detail, full target domain, exact fact/replay IDs, per-query source permissions or evaluated I05 candidate frontier.
