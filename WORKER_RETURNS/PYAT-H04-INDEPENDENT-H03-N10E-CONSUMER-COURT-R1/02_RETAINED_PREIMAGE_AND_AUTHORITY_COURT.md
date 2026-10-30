# H04 retained-preimage and scientific-authority court

## Court B — retained preimages

### Outcome

**`ONLY_EXECUTED_FACT_AND_HASH_ONLY_REFS_RECOVERABLE`**

The fixed committed transport carries the exact executed GT2 query/fact and hash-only respondent/routing/event references. It does not carry a sealed `C11LogicalRelease` with public-object/internal-record bodies. Historical existence of such a release is established; current recoverability of its bodies from the permitted source-free carrier is not.

### Exact observed evidence

`02_CONSTRUCTOR_COMPLETE_MANIFEST.json` at:

`data/ddm_build_copy/recovery_integration/semantic_relation_R1_through_Job3/R1_20260825/PRE_MAIN_RECONCILIATION_R1/WHOLE_SPINE_BUILD_CONSTITUTION_R1/RAWLSING_BUILD_WAR_PLAN_R1/CENTRAL_SYNTHESIS_R1/GT1_GT2_BOUNDED_CLOSURE_FANOUT_R1/R3_PERMISSION_TRANSLATION_AUTHORITY_CONSTITUTION_R1/R4_E2A_RUNTIME_TRANSPORT_SEAL_R1/R4A_CURRENT_GT2_EXECUTION_CONSTRUCTOR_COMPLETE_EXTRACTION_R2/02_CONSTRUCTOR_COMPLETE_MANIFEST.json`

records:

- release ref `C11LogicalRelease` / `R5_GT12_Q86A_Q86B_FROZEN` / `8315b104a94ae985a3ee3d77c8c365d5fcef6b6cb51a606df5bf141434668295`;
- replay manifest ref `C11Internal:ReplayManifest` / `c80d08ca9a5bb4814bdca3c0c21cb4c708da32840d6459b190cca206c3e3b4aa`;
- `public_objects: 96057`;
- `internal_records: 19212`;
- `forbidden_material` all false for E2B execution, raw respondent response values, SAV and source rows;
- exact query `e4ec3998…`, fact `540236d5…`, predicate `bd91b405…`, replay `c0c23ca2…`.

The manifest has no `public_objects_body`, no `internal_records_body`, and no `AuthorityRegistry` snapshot body.

`rawlsing_next/pre553_repo_native_current_payload.py` reconstructs only:

- `RespondentIdentity` refs: 19,210;
- `RoutingEligibilityFact` refs: 38,420;
- `RespondentEvent` refs: 38,420;

from fixed 32-byte hash shards. It has no record-body source, no caller path and no SAV access. This is exactly what H03 describes as the fixed transport.

### Historical carrier evidence

The A1 return (`data/ddm_build_copy/.../A1_REAL_19210_C11_SCALE_CLOSURE_R1/00_RETURN.md`) records a genuine 19,210 release build:

- release `R5_GT12_Q86A_Q86B_FROZEN` @ `8315b104a94ae985a3ee3d77c8c365d5fcef6b6cb51a606df5bf141434668295`;
- 96,057 public objects, 19,212 internal records;
- 19,210 claim members, 51,587 source rows;
- built from governed Library artifacts (FFP014/FFP017), not committed source bytes.

The A1 return states that the raw SAV bytes were not present in the supplied artifact bundle and that no governed carrier/source bytes were committed. The A2 return states: “No governed carrier/source bytes were committed to Git.” The GT12 final rerun states: “No governed respondent/source rows were committed.”

The A2/A1 exact identity and counts therefore establish historical preimage existence. They do not place the bodies in the current permitted source-free repository carrier.

### Local recoverability check

- `/Rawlsing/FIELD_FORGE_R2/` is absent on this Mac.
- `/Users/matthewsmith/Rawlsing/FIELD_FORGE_R2/` is absent.
- The exact release hash `8315b104…` appears in repository returns/docs and projection code, but not as a committed release object body.
- `rawlsing_next/pre553_c11_repository.py` is an in-memory validated-release registry; it has no on-disk object store or persistence path.
- `rawlsing_next/wave1_r5_q86_c11_projection.py` can build a C11 release only from governed source rows (`R5Q86GovernedInputs`), which are not in the fixed transport and are outside this source-free grant.
- `rawlsing_next/wave2_r5_q69b_conditioner_projection.py` references the predecessor release but is a Q69B transport/candidate, not a Q86 release-object carrier.

### Source-use limitation

A fresh conditioned I03 execution would require reconstructing respondent-level event values or reopening the governed source. Both are prohibited here. The correct conclusion is not that the historical release never existed, but that its executable bodies are not recoverable from the current permitted fixed transport.

## Court C — scientific/analytical authority

### Outcome

**AUTHORITY HOLD.** No current adopted owner record supplies the complete GT2 N10E analytical contract.

### What exists

The retained GT2 fact carries two exact authority snapshots:

- `GT12-A3-GT2-I03-QUERY` (`c0ec18e2…`) — `PREDICATE_GRAMMAR`, governing `EmpiricalFact@1.0.0`, `EmpiricalPredicate@1.0.0`, `EmpiricalQuerySpec@1.0.0` for the GT2 joint operation.
- `GT12-A3-GT2-TARGET-USE` (`8be1db86…`) — `TARGET_USE_PERMISSION`, governing `EmpiricalFact@1.0.0` and the ceiling `EMPIRICAL_INPUT_TO_FROZEN_EXACT_CONDITIONAL_SUPPORT_ONLY__NO_CAUSAL_OR_ACTOR_PROMOTION`.

HQ222 independently accepted the structural V554/V557/V558 `CONTEXT` realization at this exact grain: `ACCEPT_C5_GT2_POSITIVE_REALIZATION__V555_CONTRACT_GAP_CONFIRMED`. That is a real structural consumer, not an N10E positioned-subject consumer.

### What is absent

I found no adopted GT2 N10E record for:

- a positive operation-specific analytical-use grant;
- a GT2 positioned-subject consumer query binding Q86B to Q86A;
- a condition-value/subject pairing authority or witness;
- a GT2 model/walkback rule;
- consumer-side semantic authority distinct from Field Forge `STRUCTURAL_MEDIATION_INPUT`.

The only nearby model-authority candidate is HQ230 `C1-AT07-POSITIONED-SUBJECT-MODEL-RULE`:

- `status: CANDIDATE_NOT_ADOPTED`;
- `fixture_ids: ["AT07_BIDIRECTIONAL_100"]`;
- `real_source_effect: false`;
- `permitted_uses: ["SOURCE_FREE_C1_01_COMPATIBILITY", "SOURCE_FREE_N10E_LIFECYCLE"]`;
- no GT2 scope.

It cannot be widened to GT2 by a reviewer.

### Exact contract barriers

1. **Target-order/grain:** `_validate_direct_grain` requires `empirical_query.target_refs[0] == consumer_query.target_ref`. The retained query target order is `[Q86B, Q86A]`; a Q86A-target consumer query therefore fails `TARGET_TOPOLOGY_OR_DOMAIN_MISMATCH`. The retained query is a joint producer query, not the C1-01 consumer query.
2. **Value-bearing witness:** `ConditionValueBindingWitness` and the C1 leaf law expect value-bearing producer leaves. The retained GT2 predicate is `DERIVED_BRANCH_COHORT` with zero value-bearing leaves.
3. **Re-execution:** `compose_positioned_subject_possibility` and `provide_empirical_possibility_slice` accept a `repository` and re-execute I03; neither accepts the retained fact/profile. H03's test independently asserts those signatures and the `execute_empirical_query(` call.
4. **Model rule:** `PositionedSubjectPossibilityModelRule` requires `model_authority_ref`, `walkback_authority_ref`, `source_universe_refs`, walkback steps and positively listed proxy authority. No GT2 instance exists.
5. **Semantic ceiling:** Field Forge's `STRUCTURAL_MEDIATION_INPUT` is a structural relation permission. It does not authorize a positioned-subject possibility model, population-to-individual inference, causal reading or actor psychology.

### The distinction this court preserves

The retained GT2 product is a **population conditional-count profile**: given Q86B state, counts of Q86A states among 19,210 risk-set respondents. It is not a **positioned-subject conditional possibility**. A population conditional distribution can inform a world-level structural object; it cannot, without an explicit model/walkback/pairing authority, become a claim about a particular person's possible state. H03 correctly refuses to make that leap.

### Falsifiers for any future authority

A future GT2 N10E authority must fail closed when:

- the exact universe `4dc56730…` or release `8315b104…` is changed;
- the Q86B conditioner or Q86A target order is swapped;
- a caller injects geometry, probability, counts or a respondent preimage;
- an AT07 rule or fixture authority is substituted;
- the model rule/walkback/pairing authority is absent, malformed or out of scope;
- the consumer attempts an individualized prediction, causal claim or actor-state inference;
- the exact 36-cell/6-row/19,210 geometry is altered or a zero/minority/typed unknown is dropped.

## Owner decision

A competent owner must choose one of two things:

1. **Authorize Route B:** issue the exact GT2 N10E model rule, walkback policy, consumer query, condition-value pairing authority and retained-fact bridge authorization, all scoped to the exact retained fact/profile, universe and release. This is a scientific/authority decision, not a review conclusion.
2. **Defer the analytical lane:** preserve the accepted structural V554/V557/V558 positive and retain H03's preparation as a function card. Do not commission another synthetic N10E demo or a fake retained positive.

Responsible owners: Pyat HQ, EE14 positioned-subject/model owner, C11/I03 source owner, Field Forge owner. A distinct qualified reviewer must review any resulting bridge at its exact SHA.
