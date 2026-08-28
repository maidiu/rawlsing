# I02 CONTROLLER FLOW — AUTHORITY 37 V1

## Boundary

I02 is a deterministic composition/controller layer. It does not make I05 adaptive inside an invocation.

The invariant is:

`RESULT_DRIVEN_GENERATION_ONLY_BETWEEN_I05_INVOCATIONS`

## Generation 0

1. Caller provides:
   - one governed substantive root `EmpiricalQuerySpec`;
   - its exact root condition predicate;
   - exact C11 release refs;
   - exact universe/risk/measure authority already required by I03;
   - positive coordinate authority refs;
   - a versioned `ControllerPolicy`;
   - a `DiscoveryAuthorityBinder` that binds the sealed finite grammar to positive discovery authority.

2. Controller executes the root through unchanged I03.

3. `derive_response_morphology` reads exact complete cell facts.
   - if measure = `GOVERNED_WEIGHTED`, exact weighted cell support selects the modal set;
   - otherwise raw support selects it;
   - maximal ties remain a modal set with `unique_modal_cell = None`;
   - exact pattern cells remain exact cells;
   - optional presence labels are aggregated separately and never replace pattern morphology.

4. Controller enumerates the lawful positional catalog directly from `EmpiricalCoordinateFact` objects in the exact releases and exact universe scope.
   - only `OBSERVED_COORDINATE` facts under explicitly supplied positive coordinate authority are admitted;
   - no caller predictor atom list controls discovery reachability.

5. For every coordinate/value pair the controller creates:
   - exact `P`;
   - exact `CR(P)` = OR of all observed governed values for that coordinate.

6. Controller canonicalizes the full catalog, generates every atomic positional candidate, and seals one exact I05 candidate grammar hash.

7. Only after sealing does the binder return the exact `DiscoveryAuthority`.

8. Unchanged I05 evaluates every candidate. During this invocation, `FractureMapController._open_frontier_ref` prohibits any result-driven generation call.

## Result → branch frontier

9. Between invocations, the controller reads only terminal I05 receipts.

10. Every `DISCOVERED_RESULT_SUPPORTED` positional condition is retained. No top-k or score threshold selects reachability.

11. For each retained predictor with a unique governed modal cell:
    - `M` = exact modal response predicate;
    - `NM` = OR of explicit substantive nonmodal response cells only;
    - `PRESENT = CR(P) AND P`;
    - `ABSENT = CR(P) AND NOT P`.

12. The four Authority-37 branches are:
    - `CONFORMER = B AND PRESENT AND M`;
    - `DEVIANT_EXIT = B AND PRESENT AND NM`;
    - `ALT_CONVERGER = B AND ABSENT AND M`;
    - `ALT_MINORITY = B AND ABSENT AND NM`.

Thus predictor missingness is outside both PRESENT and ABSENT, and focal DK/refusal/missing/not-applicable cannot silently become NM.

13. The branch-role set is canonicalized and sealed as a new finite I05 `RECURSIVE_SUBGROUP_FORK` frontier.

## Exact N → N+1 handoff

14. Branch I05 execution uses the exact accepted MX01R2 wrapper.

15. A supported recursive receipt becomes a `RecursiveBranchHandoff` containing:
    - exact winning predicate;
    - exact immediate parent;
    - exact source/release/scope context;
    - exact candidate grammar/evaluated frontier refs;
    - exact replay binding.

16. Handoffs can be serialized, loaded in a fresh process, and validated by exact hashes.

17. Between invocations, `next_frontier_from_handoff` calls the accepted `recursive_parent_atom` and uses the persisted winning predicate as the exact N+1 parent.

18. The controller enumerates the governed positional catalog again inside that exact discovered parent and seals a new N+1 grammar with the handoff ref in ancestry.

No respondent-ID list is reconstructed by the caller.

## Stop / retention

Authority-37 V1:
- raw n < 25: retain/report only, no split;
- 25 ≤ raw n < 50: retain exploratory/report only, no split;
- raw n ≥ 50: continuation eligible if authority and eligible candidates remain;
- depth ≥ 4: stop;
- no eligible candidates: stop.

A stop never means delete the discovered branch.

## Receipt boundary

I02 does not invent a new public receipt family. If supplied, an external `ControllerReceiptSink` receives a deterministic operational ref envelope containing only:
- policy ID;
- root query ref;
- parent predicate ref;
- candidate grammar ref;
- evaluated frontier ref;
- discovery authority ref;
- I05 receipt refs;
- MX01R2 handoff refs;
- depth.

Public fracture-map receipt construction remains outside this I02 implementation unless separately supplied by the authorized receipt layer.
