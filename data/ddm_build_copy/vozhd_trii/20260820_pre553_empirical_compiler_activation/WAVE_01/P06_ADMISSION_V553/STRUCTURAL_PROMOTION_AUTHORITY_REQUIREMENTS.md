# PRE553 P06 — Structural promotion authority requirements

Status: `NORMALIZED_REQUIRED_OUTPUT__NO_SEMANTIC_REDESIGN`

This artifact normalizes the already-accepted P06 structural-admission burden into the immutable Wave-01 output name required by HQ.

## Governing seam

The only generic population-empirical → structural boundary is:

`EmpiricalFact -> exact named STRUCTURAL_EMPIRICAL_ADMISSION_AUTHORITY -> StructuralEmpiricalAdmission`

No EmpiricalFact, empirical coordinate, discovery result, diagnostic score, legacy packet shape, shared label, alias, provenance path, or source harmonization may acquire structural meaning without the exact named admission authority required below.

Only `ADMITTED` is positive.

## Required authority binding for every candidate promotion

A structural-admission rule MUST bind, by exact immutable ID/version/hash and without inference from filenames, labels, recency, similarity, scores, or implementation behavior:

1. **Allowed empirical input family**
   - exact EmpiricalFact / EmpiricalQuerySpec family and topology;
   - exact predicate/target semantics relied upon;
   - exact fact/query references and hashes at evaluation time.

2. **Service/source applicability**
   - exact source-universe applicability authority for this structural use;
   - exact source universe refs;
   - native scope identity refs;
   - no source is admitted because it is local, harmonized, historically related, or label-compatible.

3. **Source relation/composition authority where required**
   - any multi-universe use requires separately owned exact relation/composition authority;
   - source semantic equivalence, respondent linkage, overlap treatment, pooling, estimand composition, and backfill are separate non-inferable permissions;
   - absent positive authority, preserve source plurality and fail closed rather than pool or average.

4. **Structural target identity**
   - exact target structural object/relation/stratum identity refs;
   - exact focal structural proposition ref;
   - exact structural semantic identity refs;
   - target-use permissions and downstream structural producer/use.

5. **Interpretation semantics**
   - exact bounded transformation/interpretive meaning;
   - role/direction semantics, including source→target, target→source, or other governed direction where material;
   - interpretation-critical authority refs and complete negative authority / forbidden conclusions.

6. **Applicability in time/geography**
   - the admission rule's own effective period and geography applicability;
   - exact source/wave/time/interval evidence required by the target use;
   - rule-local mismatch may yield `TEMPORAL_SCOPE_MISMATCH`;
   - this authority does NOT create V553 canonical temporal scope, temporal harmonization, baseline, persistence, drift, reversal, rupture, sequence, coincidence, or cross-time/source comparability.

7. **Measure, estimand, support, and uncertainty**
   - exact estimand refs;
   - exact measure/weight authority refs;
   - explicit support and uncertainty admissibility requirements;
   - `OBSERVED_ZERO != ZERO_SUPPORT`;
   - `ZERO_SUPPORT` never means structural or actor impossibility;
   - `LOW_SUPPORT` can pass only when the named rule explicitly permits it and remains low-support;
   - `UNCERTAINTY_UNQUANTIFIED` remains unquantified.

8. **Source disagreement/noncomparability policy**
   - exact rule for whether separate source-indexed structural admissions may coexist;
   - otherwise typed conflict/noncomparability;
   - no source-majority winner, averaging, nearest-source repair, or implicit composition.

9. **Required external authorities**
   - every externally owned applicability, relation, composition, measure, estimand, uncertainty, temporal, comparability, or compatibility authority required by this exact use;
   - missing, unknown, conflicting, denied, or noncomparable authority fails closed and remains referenced in the receipt.

10. **Replay and authority closure**
    - immutable admission authority ID/version/hash;
    - exact EmpiricalQuerySpec and EmpiricalFact refs/hashes;
    - source-universe and scope refs;
    - all interpretation-critical and negative authority refs;
    - producer replay root sufficient to reproduce the same decision state and admitted payload under the same semantic inputs.

## Compatibility-promotion requirements

Migration of intentionally retained V551/V551J/V552/V552J structural meaning requires ALL of:

- exact compatibility EmpiricalQuerySpec;
- exact compatibility EmpiricalFact;
- exact named compatibility StructuralEmpiricalAdmission rule;
- exact legacy semantic surface being claimed equivalent;
- exact parity-claim scope;
- exact parity receipt;
- exact retained structural meaning/use target.

Historical stage name, filename, packet shape, aggregate similarity, or selected-field parity is insufficient.

## Positive receipt requirements

A positive `StructuralEmpiricalAdmission` must carry enough exact material to populate the accepted downstream admission projection without invention:

- admission ID and content hash;
- admission authority ID/version/hash;
- `admission_decision_state = ADMITTED`;
- exact EmpiricalQuerySpec and EmpiricalFact refs;
- source universe refs;
- native scope identity refs;
- focal structural proposition ref;
- structural semantic identity refs;
- target-use permission refs;
- effective-time/interval evidence required by the target use;
- estimand refs;
- measure/weight authority refs;
- support/uncertainty state and refs;
- applicable negative/denial/noncomparability refs;
- interpretation-critical authority refs;
- bounded structural interpretation payload;
- authority closure refs;
- producer replay root.

## Nonpositive state requirements

The following remain nonpositive and replayable; none may be coerced into positive promotion:

- `MISSING_STRUCTURAL_ADMISSION_AUTHORITY`
- `ADMISSION_DENIED`
- `ADMISSION_DEFERRED`
- `EMPIRICAL_FACT_NONCOMPARABLE`
- `SOURCE_NOT_APPLICABLE_TO_STRUCTURAL_USE`
- `INSUFFICIENT_EVIDENCE_UNDER_RULE`
- `TEMPORAL_SCOPE_MISMATCH`
- `STRUCTURAL_TARGET_UNRESOLVED`
- `NEGATIVE_AUTHORITY_ONLY`
- `UNKNOWN_OR_CONFLICTING_REQUIRED_AUTHORITY`
- `VALID_EMPTY`
- `INTEGRITY_FAILURE`

Fail-closed precedence remains:

`INTEGRITY_FAILURE > MISSING_STRUCTURAL_ADMISSION_AUTHORITY > UNKNOWN_OR_CONFLICTING_REQUIRED_AUTHORITY > ADMISSION_DENIED > NEGATIVE_AUTHORITY_ONLY > SOURCE_NOT_APPLICABLE_TO_STRUCTURAL_USE > EMPIRICAL_FACT_NONCOMPARABLE > TEMPORAL_SCOPE_MISMATCH > STRUCTURAL_TARGET_UNRESOLVED > INSUFFICIENT_EVIDENCE_UNDER_RULE > ADMISSION_DEFERRED > VALID_EMPTY > ADMITTED`.

All simultaneously applicable blocker/negative refs remain preserved even when one primary state wins.

## Explicitly forbidden promotion inferences

This authority may not establish any of the following by generic inference:

- empirical association/prevalence → structural truth;
- empirical coordinate or shared string → generated nine-stratum structural position;
- population fact → actor belief, response, knowledge, memory, identity, persona, psyche, or realized disposition;
- discovery/diagnostic score → structural truth;
- source label/provenance/harmonization → equivalence, respondent linkage, pooling, composition, or backfill;
- timestamp presence → V553 temporal operation;
- an `ADMITTED` receipt → `V553_NOT_REQUIRED_FOR_THIS_USE`;
- an `ADMITTED` receipt → direct V554 eligibility;
- admission authority → V554 signature/equivalence/dedup/F1-F2-B1 identity;
- compatibility packet existence → compatibility parity;
- admission success → source retirement, cutover, or downstream interface redesign.

## Ownership boundary

P06 owns structural-admission decision/receipt semantics and the lossless admission-side projection material.

SCR553 remains owner of use-scoped V553 temporal jurisdiction. SCR554/M1 remains owner of V554 basis/signature/temporal-completeness/equivalence/dedup/precedence and F1/F2/B1 identity. Source applicability/relation/composition, measure/estimand, uncertainty, and other external authority remain with their named owners.

This normalized artifact makes no semantic change to accepted P06 head `d6a56e70822b48be53b74fd2ef9259e959fefc8e`.
