# FFIF007 — CVCR AND FFX002 R2 IMPLICATIONS

## 1. CVCR dependency change

When a CVCR emits any status quantified over a purported admissible universe, it must consume a matching passed COCR hash in addition to FFIF006's CIM/CITC/common-input/support requirements.

Add fields:

- `object_closure_receipt_ref_hash`
- `closure_status`
- `U_hash`
- `AOS_hashes[]`
- `known_blocked_challenger_status`
- `fresh_challenger_audit_ref_hash`
- `within_U_status`
- `supersession_vulnerability`.

## 2. CVCR statuses not requiring universe closure

Assuming all ordinary claim/materiality/input authorities are valid, a CVCR may emit without COCR:

- `INVALID_COMMON_INPUT`
- `SEMANTIC_INPUT_DIVERGENCE`
- `CLAIM_SPLIT_REQUIRED`
- `CLAIM_IDENTITY_UNRESOLVED`
- `INVALID_VIEW_REMOVED`
- `INSUFFICIENT_EVIDENCE`
- `NONIDENTIFIABILITY`
- `VIEW_ROBUST_AMONG_COMPARED_OBJECTS`
- `KNOWN_LOSS_EXPLAINS_DIFFERENCE`
- `REPRESENTATION_DEPENDENCE_AMONG_COMPARED_OBJECTS`
- `INCREMENTAL_VALUE`
- `SINGLE_TESTED_OBJECT_SUFFICIENT`
- `MULTI_VIEW_RETENTION_REQUIRED_AMONG_TESTED_OBJECTS`.

The qualifier must remain explicit.

## 3. CVCR statuses requiring passed COCR

- `WEAKER_OBJECT_SUFFICIENT_WITHIN_U`
- `SINGLE_OBJECT_SUFFICIENT_WITHIN_U`
- `NO_SINGLE_OBJECT_SUFFICIENT_WITHIN_U`
- `MINIMAL_SUFFICIENT_SET_WITHIN_U`
- `MULTIPLE_NONDOMINATED_MINIMAL_SUFFICIENT_SETS_WITHIN_U`
- `CLAIM_SCOPED_BOUNDED_NONREDUCIBILITY_SUPPORTED_WITHIN_U`.

If COCR is absent/stale/failed/abstained, return `UNRESOLVED__OBJECT_UNIVERSE_NOT_CLOSED` for these slots.

## 4. FFX002 R2 three-level ceiling

### Level 0 — CIM/CITC incomplete

Per FFIF006, preserve raw view outputs, manifests, hostile results, and utility metrics. Do not adjudicate material representation dependence, sufficiency, multi-view necessity, or bounded nonreducibility for the incomplete claim.

### Level 1 — CIM/CITC complete, no passed COCR

FFX002 may emit:

- view validity/internal robustness;
- common-query agreement or material representation dependence;
- known loss;
- incremental value;
- tested-arm weaker/sufficient results;
- `MULTI_VIEW_MINIMAL_SUFFICIENT_SET_REQUIRED_AMONG_TESTED_ARMS`.

It may not emit a global/within-U weaker-object result or bounded nonreducibility.

### Level 2 — matching passed COCR

FFX002/CVCR may run the frozen universe/transform/sufficiency/minimal-set court and emit the within-U statuses, subject to every hostile, nuisance, and holdout gate.

## 5. Mandatory arms do not define U

Core A/B/C remain mandatory for the experimental architectural questions. They are not the closure universe merely because they are mandatory. Graph/topology, motif, latent/model, rank/order, direct fact, or transport specifications receive claim-specific dispositions:

- graph/topology: include only for a constitutive topology claim; otherwise control/not relevant;
- motif: phase-2 challenger only for a predeclared recurrence assertion;
- latent/model: challenger only for an authorized model/predictive/compression claim not answered weaker;
- transport: excluded from local canary; required only for transport CIM with FFIF003/005 dependencies;
- rank/direct fact: obvious weaker challenges where their interfaces cover the exact claim.

## 6. FFX002 output grammar changes

Replace unqualified:

`MULTI_VIEW_RETENTION_REQUIRED`

with one of:

- `MULTI_VIEW_RETENTION_REQUIRED_AMONG_TESTED_ARMS`
- `MINIMAL_MULTI_OBJECT_SET_REQUIRED_WITHIN_U@hash`.

Replace unqualified:

`WEAKER_VIEW_SUFFICIENT`

with:

- `WEAKER_TESTED_OBJECT_SUFFICIENT`
- `STRICTLY_SUFFICIENT_WEAKER_OBJECT_WITHIN_U@hash`.

No result count or algorithm count may strengthen the bounded quantifier.

## 7. Cross-context extension

For FFX002-XC, U can include transport objects only under a transport CIM. Each AOS binds the outcome-blind mapping plan, TTAR/PRA dependencies, local frozen objects, finite map family, and preservation predicate. Local FFX002 closure cannot borrow XC objects or mapping outcomes.

## 8. Exact one-sentence rule

**FFX002 may compare its mandatory arms without a closure receipt, but it may quantify necessity only over the tested arms; any claim over all currently admissible weaker objects requires a matching pre-output COCR.**

