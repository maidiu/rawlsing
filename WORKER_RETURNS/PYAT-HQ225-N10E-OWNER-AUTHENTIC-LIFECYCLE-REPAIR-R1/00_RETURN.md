# PYAT HQ225 — N10E OWNER-AUTHENTIC LIFECYCLE REPAIR — R1

**Disposition:** `N10E_OWNER_AUTHENTIC_LIFECYCLE_REPAIR_COMPLETE__READY_FOR_FINAL_REREVIEW`

**Branch:** `agent/rabochii-pyat-hq225-n10e-owner-authentic-lifecycle-repair-r1`  
**Commission tip:** `b23e420f57fc385021cabbee89b7a554468cf832`  
**Implementation head before return packet:** `5be967b5e9eb393032726924496368606ebce82c`  
**Prior hostile review:** `agent/reviewer-pyat-hq224-n10e-exact-determinant-lifecycle-r1 @ 1dc665a67d20fac2960a113a7fb3dcaa415f1dc6`

## Result

The five HQ224 defects are repaired at the commissioned N10E adapter/court boundary.

1. **Ownership/classification coverage now fails closed.**  
   `AnalyticalProductRegistration` may still deserialize an incomplete historical registration, but `AnalyticalDependencyRegistry.build_graph()` cannot claim lifecycle closure until every consumed `determinant_exact_ref` has exactly one classification. Missing classification raises `UNCLASSIFIED_DETERMINANT_REFUSED`.

2. **The actual fresh runner now uses the complete classified path.**  
   It no longer registers query/predicate/consumer/witness refs while silently omitting ownership metadata. The runner recomputes the upstream `EmpiricalFact`, constructs the same owner-authenticated census used by the court, calls `registry.build_graph()`, and exposes the classified registration in its output.

3. **Consumed determinant coverage was completed.**  
   The registration includes the governed query, predicate, consumer query, witness, source universe, upstream `EmpiricalFact`, release, consumer subject/target identities, conditioner-binding exact refs, risk/measure/response-state identities, target-domain replay identity, predicate operator semantics, witness preimage / predicate-leaf / pairing-ground-truth refs, and query/predicate replay-root refs. Direct model-rule authorities now include both model and walkback authority, plus any positive proxy / walkback-step authorities if present.

4. **Ownership is determinant-specific and authenticated.**  
   New `DeterminantOwnerEvidence` requires exact determinant preimage material whose semantic hash equals the determinant ref, exact allowed owner-relation path(s), and an exact equality between the declared owner refs and the refs recorded at those paths. Query ownership is tied to `query_authority_refs`; predicate ownership to `grammar_authority_ref`; consumer/witness ownership to comparability/pairing fields; source universe / fact ownership to their exact authority closure. A foreign authority that merely exists elsewhere in the fixture fails.

5. **The real sealed successor snapshot is consumed.**  
   The query-revision court obtains the successor through the accepted maintenance owner's seal and public `resolve_historical_exact()` path. `assert_authority_snapshot_body_matches_ref()` reconstructs the exact `AuthorityCandidate.authority_material()` projection and requires its hash to equal the snapshot's exposed `AuthorityRef.authority_content_hash`. The HQ223 old-body/new-hash impersonation shape is explicitly hostile-tested and refused.

6. **Recomposition is family-safe.**  
   Both determinant and product recompilation pass through `_assert_replacement_family()`. A predicate callback returning an `EmpiricalQuerySpec` now raises `REPLACEMENT_FAMILY_MISMATCH` before a lawful lifecycle receipt can claim that replacement. The positive query-revision witness now returns the recomputed query, predicate, upstream fact, and product in their correct families.

7. **Selective invalidation remains discriminating.**  
   The court keeps the owner→determinant and determinant→product edge-deletion hostiles, non-consumer unaffected witness, source-universe / upstream-fact reachability, and owner-derived currentness behavior.

## Mandatory court coverage added / repaired

- `test_r14_unclassified_consumed_ref_cannot_claim_lifecycle_closure`
- `test_r15_source_universe_and_empirical_fact_have_real_owner_paths`
- `test_r16_query_revision_uses_real_sealed_snapshot_and_rejects_impersonation`
- `test_r17_predicate_to_query_replacement_fails_before_receipt`
- `test_r18_fresh_runner_registers_complete_classified_census`
- `test_r19_walkback_authority_is_registered_but_not_stageable_from_fixture_material`

Earlier r03-r07/r10-r12 courts were also corrected so the query/predicate/fact replacement chain uses one real governed ceremony, the exact sealed successor snapshot, correct object families, and determinant-specific owner evidence.

## Residual accepted-owner / upstream limits

These are not repaired by inventing authority:

- `C11LogicalRelease` remains an unowned exact lifecycle determinant.
- `C1-AT07-COMPARABILITY` is a real recorded owner ref for consumer-query/witness material, but the installed fixture material is not a full `AuthoritySnapshot` and no current authority kind supplies a lawful comparability revision ceremony.
- `C1-AT07-WALKBACK` is now explicitly registered as a consumed direct model-rule authority. Its installed fixture-only material likewise is not a full stageable `AuthoritySnapshot`; no WALKBACK authority kind is manufactured.
- affected-but-identical recomputation remains an accepted `AuthorityMaintenanceExecutor` contract limitation because the owner requires every affected dependent to move to a new exact ref.

## Execution statement

This browser/GitHub lane had no lawful targeted execution mechanism for the N10E pytest court. Existing push workflows do not target this branch; the pull-request bounded-court spec currently targets unrelated FIABC tests. I did **not** mutate `.github/` or `.rabochii/` to manufacture a run, and I do **not** claim an unobserved pass count.

The final rereviewer should execute the N10E court and related dependency/authority regressions. The implementation and mandatory hostile court construction are complete and ready for that independent run.

## Write terrain

Modified production:
- `rawlsing_next/pre553_analytical_replay_dependency.py`

Modified court/runner:
- `rawlsing_next/tests/n10e_provider_replay_lifecycle_runner.py`
- `rawlsing_next/tests/test_pre553_n10e_provider_replay_lifecycle_court.py`

Production/court blobs at implementation head:
- adapter: `230bd7efed04a8fecc573812d7fbacb6dd93f86f`
- runner: `a146874238d04bd705509066da0520af77f9f521`
- court: `40d61205dc9692c9d867fe1e68c88ce08687d8a5`

No authority-maintenance, learned lifecycle/release, provider, analytical composition, positioned-subject consumer, live C4/C7, raw-source, workflow, or court-spec mutation was performed.
