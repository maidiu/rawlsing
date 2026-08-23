# New Survey Semantic / Structural Admission Contract — G1A

Status: `BINDING_PROVISIONAL_CONTRACT__G1A_GATE_REMAINS_BLOCKED`

This contract preserves Authority 38/39 while G1A's historical-current supersession closure is incomplete.

## Layered admission

A new survey family/wave advances only through explicit gates:

1. `PHYSICAL_SOURCE_ADMITTED`
   - exact source identity/hash;
   - frozen decoder/config/dependency replay;
   - source-native metadata and physical incidence.

2. `SOURCE_SEMANTIC_C11_ADMITTED`
   - questionnaire/codebook/methodology authority;
   - respondent/native-ID scope;
   - response-state meaning;
   - routing/applicability/risk-set authority;
   - topology/multiplicity/order/rank;
   - weight/design/estimand authority;
   - source→canonical C11 binding;
   - unresolved meanings remain typed UNKNOWN/BLOCKED.

3. `EMPIRICAL_I03_I05_ADMITTED`
   - exact I03 empirical facts;
   - governed I05 discovery within its frozen frontier;
   - empirical association remains empirical evidence, not semantic authority.

4. `CROSS_SURVEY_SEMANTIC_EQUIVALENCE_ADMITTED` where reuse is requested
   - exact new source item;
   - positive equivalence authority covering wording, scope, response semantics, population/time and relevant routing/topology;
   - only then may existing governed semantics be reused.

5. `RAWLSING_SEMANTIC_STRUCTURAL_AUTHORITY_ADMITTED`
   - semantic role/use eligibility;
   - response-semantic lane;
   - directionality/applicability;
   - block/battery;
   - driver/facet/domain/axis/target;
   - position-conditioning;
   - QRA/QSM/Full Question Relation or successor authority;
   - explicit negative/block/review-required states.

6. `PERSONA_GENERATION_ELIGIBLE`
   - only after all required upstream layers and terminal consumer contracts are satisfied.

## Human/manual review queue

A genuinely new semantic territory enters an explicit review queue when any required meaning lacks positive authority. Queue records must carry:
- exact source family/wave/release/item;
- question/response/documentary evidence references;
- authority field(s) missing;
- proposed candidate, if any, clearly marked proposal-only;
- reviewer/adjudicator;
- decision date/reason;
- resulting canonical authority artifact/version;
- downstream invalidation scope.

No queue item may be auto-promoted because:
- labels/codes resemble an old wave;
- response distributions look similar;
- embeddings or an LLM say they are equivalent;
- I05 association is strong;
- neighboring questions have a mapping.

## Reuse rule

Forbidden:

`SAME LABEL | SAME CODE | SAME FAMILY -> SAME SEMANTICS`

Permitted:

`EXACT NEW SOURCE ITEM + POSITIVE GOVERNED EQUIVALENCE AUTHORITY -> REUSE EXACT EXISTING AUTHORITY`

Reuse must preserve the original authority's epistemic class and provenance.

## Missing authority behavior

When any required authority input is absent, stale, scope-mismatched, tampered, or unresolved:
- emit `MISSING_AUTHORITY`, `UNKNOWN`, `BLOCKED`, or `MANUAL_REVIEW_REQUIRED` as governed;
- do not substitute a heuristic;
- do not silently inherit from a neighboring wave;
- do not admit the affected item to later semantic/structural/persona stages.

## Correction and immutability

A correction creates a new authority identity and invalidates affected rebuildable descendants. It does not retroactively mutate an already accepted V3 life/history. Historical authorities remain audit-addressable even when superseded.

## G1A-specific hold

Until G1A-B01/B02/B03 are closed, this contract is sufficient to prevent new semantic invention but is not proof that the existing 35-source authority corpus is completely compiler-addressable.
