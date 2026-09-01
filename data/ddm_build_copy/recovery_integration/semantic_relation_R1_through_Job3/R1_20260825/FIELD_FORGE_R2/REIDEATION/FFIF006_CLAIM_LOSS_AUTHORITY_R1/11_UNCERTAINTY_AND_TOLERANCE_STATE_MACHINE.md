# FFIF006 — UNCERTAINTY AND TOLERANCE STATE MACHINE

## Inputs

The state machine consumes one comparison claim hash, matching normalized output slots, hard-validity results, observed support, an authorized uncertainty procedure, and the frozen CITC row. It does not choose any of them.

## Ordered transitions

| stage | condition | terminal/next state |
|---|---|---|
| U0 | common input, semantic hash, claim identity, view validity, or CITC hash fails | `INVALID_COMPARISON` |
| U1 | support requirement fails | `INSUFFICIENT_SUPPORT` |
| U2 | uncertainty procedure/assumptions not authorized or target not identified | `INSUFFICIENT_SUPPORT_OR_NOT_IDENTIFIED` |
| U3 | deterministic exact objects are byte/assertion equal | `EXACT_AGREEMENT_ON_ASSERTION_SLOT` |
| U4 | deterministic exact objects differ and zero-loss rule applies | `MATERIAL_DIFFERENCE_RESOLVED` |
| U5 | equivalence test explicitly authorized and interval/test lies wholly within frozen margin | `EQUIVALENT_WITHIN_TOLERANCE` |
| U6 | equivalence test authorized but evidence spans both equivalent and material regions | `DIFFERENCE_NOT_RESOLVED_DUE_TO_UNCERTAINTY` |
| U7 | uncertainty region lies wholly beyond materiality boundary | `MATERIAL_DIFFERENCE_RESOLVED` |
| U8 | no equivalence test; observed point/summary difference is within margin | `DIFFERENCE_BELOW_TOLERANCE__NOT_EQUIVALENCE` |
| U9 | no equivalence test; observed difference exceeds margin but uncertainty crosses boundary | `DIFFERENCE_NOT_RESOLVED_DUE_TO_UNCERTAINTY` |
| U10 | required loss component is undefined for a view | `UNDEFINED_FOR_VIEW` then claim-sufficiency court |

## Required distinctions

`NO MATERIAL DIFFERENCE` is not a default machine conclusion. Use one of:

- `EXACT_AGREEMENT_ON_ASSERTION_SLOT` — deterministic exact equality only;
- `DIFFERENCE_BELOW_TOLERANCE__NOT_EQUIVALENCE` — observed difference is small under a descriptive rule, but equivalence was not proved;
- `EQUIVALENT_WITHIN_TOLERANCE` — only under an explicit equivalence margin, assumptions, and test;
- `DIFFERENCE_NOT_RESOLVED_DUE_TO_UNCERTAINTY` — evidence cannot decide the frozen boundary;
- `INSUFFICIENT_SUPPORT` — the claim lacks required support;
- `MATERIAL_DIFFERENCE_RESOLVED` — evidence lies beyond the frozen materiality boundary.

Failure to reject difference is not equivalence. A difference smaller than its standard error is not automatically immaterial. A point estimate below a margin is not an equivalence test.

## Exact/minority claims

When the proposition is exact existence and the source fact is lawfully observed, sampling-style uncertainty is not theatricalized over existence. Provenance/replay governs existence. Generalizing its prevalence or recurrence is a separate claim with a separate uncertainty contract.

## Multi-dimensional output

Each invariant/loss dimension receives its own state. The CVCR may synthesize only by a declared noncompensatory rule, for example:

`ANY_CRITICAL_ROW_MATERIAL -> CLAIM_DIFFERENCE_MATERIAL`

It may not average a material minority loss with a small conditional-distribution error.

