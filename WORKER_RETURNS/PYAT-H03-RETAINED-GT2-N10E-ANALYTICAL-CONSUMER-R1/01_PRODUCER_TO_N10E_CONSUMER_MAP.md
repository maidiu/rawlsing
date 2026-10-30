# PYAT H03 — actual producer → N10E consumer map

## 1. Exact retained input chain (demonstrated)

```
rawlsing_next.pre553_repo_native_current_payload.load_current_gt2_query_fact_from_committed_transport()
  -> EmpiricalQuerySpec  e4ec3998664975c6a5f9e020b7815cfe6d39a212e264963d8037e6f0db87d0d0
  -> EmpiricalFact       540236d533e9123f6d7b4d1edd4cf0951277154e72c7667deb09fb6550f11f46
       replay            c0c23ca2bb439364756503722b60d047139d42a6128411cc19bfbd87d33c884f
       predicate         bd91b40575035a9ff9ad2e7c507adc2610bfebdcc7fa38ce1cd697b37559cea3
       risk set          FIRST_GENUINE_CANARY_COMMON_COEXPOSURE_RISK_SET@1
       risk member hash  0484fa5c0440c34e9b1f28b385f3ef6c3302eaeb11c3c5b663441553ea11313b
       release           C11LogicalRelease | R5_GT12_Q86A_Q86B_FROZEN | 8315b104…
       universe          urn:rawlsing:pre553:EmpiricalUniverse:sha256:4dc56730…
       19,210 support, 36 native joint cells, 23 zero cells
```

The loader accepts no path, source handle or caller-selected identity. It reads only the fixed manifest and three 32-byte hash shards. The manifest records `sav=false`, `source_rows=false`, `raw_respondent_response_values=false`.

## 2. Exact predicate reconstruction (demonstrated, new H03 helper)

```
rawlsing_next.wave1_gt12_i03_positive_facts.reconstruct_gt2_risk_cohort_predicate(query, fact)
  -> EmpiricalPredicate bd91b405… (exact identity reproduced)
  -> predicate_ast.leaf_type = DERIVED_BRANCH_COHORT
  -> value-bearing conditioner leaves = 0
```

This closes the predicate-body absence for *identity* purposes without executing I03 or reopening source. It does **not** turn the cohort predicate into a value-bearing Q86B condition.

## 3. Exact conditional count producer (demonstrated, reused H02 owner)

```
rawlsing_next.field_forge_conditional_support.produce_exact_conditional_support_profile(
    joint_fact=fact,
    joint_query=query,
    conditioner_ref=query.target_refs[0],   # Q86B
    target_ref=query.target_refs[1],        # Q86A
    producer_permission_ceiling=("STRUCTURAL_MEDIATION_INPUT",),
    relation_permission_ceiling=("STRUCTURAL_MEDIATION_INPUT",),
)
  -> EXACT_CONDITIONAL_SUPPORT_PROFILE_WITHIN_SCOPE@1.0.0
  -> urn:rawlsing:field-forge:conditional-support:sha256:1ffdfe536adc…
  -> 6 conditioner rows, 6 target states each, 36 cells
  -> denominators 6784, 11787, 624, 0, 0, 15 = 19,210
```

This is a structural Field Forge product. Its permission ceiling is not an N10E analytical-model permission and is not widened by H03.

## 4. Prepared analytical frontier (demonstrated, new H03 adapter)

```
rawlsing_next.pre553_retained_gt2_analytical_preparation.load_retained_gt2_analytical_preparation()
  -> RetainedGT2AnalyticalPreparation
       preparation_ref: urn:rawlsing:retained-gt2:n10e-preparation:sha256:0ef9fc9c…
       joint_cells: complete 36-cell native geometry
       conditioned_rows: exact counts + denominators, no ratios
       determinants:
         empirical_query          EXACT_RETAINED
         predicate                EXACT_RECONSTRUCTED_FROM_RETAINED_REFS
         repository               ABSENT_FROM_RETAINED_TRANSPORT
         authority_registry       ABSENT_FROM_RETAINED_TRANSPORT
         release_refs             ABSENT_FROM_RETAINED_TRANSPORT (ref only)
         consumer_query           UNAVAILABLE_OPERATION_SPECIFIC_AUTHORITY
         model_rule               UNAVAILABLE_OPERATION_SPECIFIC_AUTHORITY
         condition_binding_witness UNAVAILABLE_OPERATION_SPECIFIC_AUTHORITY
  -> require_n10e_provider_route()
       raises RetainedGT2N10EContractGapError(N10E_RETAINED_CONTRACT_GAP)
```

The adapter intentionally has no evidence/geometry/probability parameter and cannot fabricate an N10E receipt.

## 5. Accepted N10E direct route (blocked at the exact edges)

```
provide_empirical_possibility_slice(
    repository, empirical_query, predicate, authority_registry, release_refs,
    consumer_query, model_rule, condition_binding_witness)
  -> compose_positioned_subject_possibility(...)
       -> execute_empirical_query(
              repository=C11Repository,
              query=EmpiricalQuerySpec,
              predicate=EmpiricalPredicate,
              authority_registry=AuthorityRegistry,
              release_refs=release_refs)
            -> C11Repository.resolve_release_exact(release_ref)
            -> _build_release_index(release, universe_ref)
            -> _evaluate_index_group(...) over respondent events/routing
       -> _build_evidence(fact, query, predicate, consumer_query, witness)
       -> evaluate_positioned_subject_possibility(query, rule, (evidence,))
  -> EmpiricalPossibilitySliceProviderReceipt / PossibilitySliceEvidence /
     PositionedSubjectPossibilityResult
```

| Edge | Status | Exact reason |
|---|---|---|
| retained query/fact load | DEMONSTRATED | fixed transport, exact hashes |
| predicate identity reconstruction | DEMONSTRATED | `bd91b405…` reproduced exactly |
| Field Forge count profile | DEMONSTRATED | `1ffdfe53…`, 36 cells, 19,210 |
| sealed `C11Repository` for fresh I03 | **UNAVAILABLE** | transport has only executed fact + hash-only refs; no 96,057 public-object or 19,212 internal-record bodies |
| authority registry | **UNAVAILABLE** | fact/query carry `AuthorityRef`s only; snapshot bodies absent |
| value-bearing Q86B predicate | **UNAVAILABLE** | retained predicate is `DERIVED_BRANCH_COHORT`; zero value-bearing leaves |
| condition-value witness | **UNAVAILABLE** | no value-bearing leaf and no operation-specific pairing authority |
| GT2 consumer query | **UNAVAILABLE** | no accepted `PositionedSubjectPossibilityQuery` binding Q86B value → Q86A |
| GT2 model/walkback rule authority | **UNAVAILABLE** | no adopted GT2 N10E authority; HQ230 candidate is AT07-scoped and not adopted |
| provider receipt | **NULL** | no fabricated receipt |
| consumer result | **NULL** | no consumer execution |
| N10E replay | **NULL** | no provider product to replay |

The composition’s `I05_EXACT_BOUNDED_TO_POSITIONED_SUBJECT` and `MX01R2_RECURSIVE_TO_POSITIONED_SUBJECT` routes are not alternative retained-fact entries: they require owner-produced discovery/recursive handoff products with receipts, candidate grammar/coverage or recursive lineage. No such retained handoff exists, and constructing one from the single retained fact would counterfeit an owner product.

## 6. Exact consumer and authority identities inspected

| Object | Identity / state |
|---|---|
| Provider | `N10E_EMPIRICAL_POSSIBILITY_SLICE_PROVIDER@1.0.0`; route `EMPIRICAL_QUERY__C1_ANALYTICAL_COMPOSITION__GENERATED_EVIDENCE`; input mode `EXACT_DETERMINANTS_ONLY__NO_PRECOMPUTED_SLICE_GEOMETRY` |
| Composition | `compose_positioned_subject_possibility`; direct route `DIRECT_I03_TO_POSITIONED_SUBJECT` |
| Consumer | `SOURCE_BACKED_POSITIONED_SUBJECT_POSSIBILITY@1.0.0`; model rule `POSITIONED_SUBJECT_EXACT_CONDITIONAL_WITH_GOVERNED_WALKBACK@1.0.0` |
| Retained query authorities | `GT12-A-R5-Q86-CARRIER-REEXPRESSION`, `GT12-A-R5-Q86-COMMON-RISK-ROUTING`, `GT12-A-R5-Q86-SOURCE-SEMANTICS`, `GT12-A3-GT2-I03-QUERY`, `GT12-A3-GT2-TARGET-USE` |
| N10E model/walkback authority | none adopted for GT2 |
| N10E consumer query | none accepted for GT2 |
| Condition-value pairing authority | none in retained closure |
| HQ230 candidate | `C1-AT07-POSITIONED-SUBJECT-MODEL-RULE` @ `db0060af…`; `CANDIDATE_NOT_ADOPTED`; `fixture_ids=["AT07_BIDIRECTIONAL_100"]`; not GT2 |

## 7. Separation from the already-positive structural lane

The H02 structural positive is real and unchanged: retained GT2 → Field Forge → PRE-V3 admission for `STRUCTURAL_MEDIATION_INPUT` → V554/V557/V558 `CONTEXT` → V3 `DENY_ZERO_EFFECT`. It is **not** the N10E analytical consumer. H03 does not redo, relabel or extend that structural positive into an analytical claim.

## 8. Separation from the A2 fixture route

The A2 route (`execute_and_replay_a2_gt1`) uses a small source-backed C11 release built from synthetic rows. Its pre-existing RED is a fixture/decoder mismatch in `_event_value`, not the retained GT2 product. H03 does not repair or rely on A2; the retained preparation uses the already-executed GT2 fact and Field Forge counts.

DONE: exact call graph, exact demonstrated edges, exact blocked edges, authority/consumer identities. REMAINING: sealed C11 release/preimages or an owner-issued retained-fact bridge; GT2 N10E model/query/witness authority. CRITICAL BLOCKERS: absent repository/preimages and N10E authority. LARGEST PRODUCTIVE MOVE: authorize the thin retained-fact bridge or commission a fresh conditioned I03 execution from a lawful sealed release.
