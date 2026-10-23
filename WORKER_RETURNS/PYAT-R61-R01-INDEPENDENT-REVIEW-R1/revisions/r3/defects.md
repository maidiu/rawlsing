# R61-R01V R3 independent defects and preserved limitations

Verdict: **ACCEPT_SCOPED_LOCAL**. No blocking R01 defect remains in A1-A3. A4
is an honest, explicit generic-contract gap, not a silent defect and not a
D13 pass. Reviewer code/author files were not edited; probes are disposable
below this return root.

## A1 — conditioned JOINT / CO_TRAVEL: repaired

- Prior R2 defect: conditioned `JOINT`/`CO_TRAVEL` lowered `SUPPORTED` while the
  exact condition value was used by neither the native rule nor any query role.
- R3 behavior verified independently:
  - single condition uses the exact condition predicate as the joint baseline;
  - multiple conditions use one AND-derived predicate whose
    `dependency_refs` contain both exact condition predicate refs;
  - every `JOINT` and `MARGINAL_*` query role in the reviewer-compiled grammar
    uses the derived predicate ref, not the all-response baseline;
  - condition values 0/1 produce distinct derived refs and distinct actual I05
    candidate identities;
  - actual `execute_exact_bounded_discovery` baseline passes the reviewer-owned
    exact candidate/query-role join and the candidate anti-join;
  - same-atom/rule-id mutation of the derived predicate makes both joins fail;
    restoration passes; a cold subprocess reproduces the case.
- Residual: conditional values are exact typed predicate refs. The derived
  predicate object must be supplied to the I05 predicate catalog by R03. That
  is an explicit owner/catalog requirement, not a new engine.
- Evidence: `evidence/conditional_joint_repro.txt`,
  `probes/test_r01v_r3_reviewer.py::test_A1_*`, `replay/own_probes.*`.

## A2 — canonical operation identity: repaired

- `lower_operation` now refuses an `op_id` not equal to
  `urn:r61:op:<canonical_hash>` with typed `OPERATION_ID_NOT_CANONICAL`.
- A semantic condition change retaining the old `op_id` is refused; recomputing
  the canonical ID for the changed operation lowers `SUPPORTED` normally.
- This covers both forged IDs and preserved stale IDs, not only direction/role
  revalidation.
- Evidence: `probes/test_r01v_r3_reviewer.py::test_A2_*`.

## A3 — empty/unsupported/pending: repaired

- Unsupported-only nonempty frontier: exact unsupported operation IDs retained,
  `allow_empty_frontier=False`, coverage report disjoint and no-drop.
- Truly empty complete frontier: `allow_empty_frontier=True`, no records.
- Budget-pending frontier: `allow_empty_frontier=False`.
- Partition/record accounting conserves all operation identities; source
  scientific eligibility is not overwritten by runtime unsupportedness.
- Evidence: `probes/test_r01v_r3_reviewer.py::test_A3_*`.

## A4 — recurrence/baseline: honest preserved limitation, not silently collapsed

R3 does **not** implement independent governed recurrence/baseline
enumeration. It intentionally reports a deferred boundary:

```text
kind = RECURSION_BASELINE_NOT_ENUMERATED
state = EXACT_CONTRACT_GAP
reason = R01_DECLARES_FORK_OVER_CONDITIONERS_ONLY_NO_INDEPENDENT_RECURRENCE_CHAIN
```

Verified independent facts:

- FORK rows carry conditioner `branch_depth` 1/2 while `recursion_depth` is
  independently `0`; D is not used as a disguised conditioner-depth bound.
- `recursion_relation_ref` and `baseline_policy_ref` are carried on operations
  and the deferred record; `baseline_ref` is an exact parent operation ID.
- D=3 is not exercised as an independent recurrence chain; D13 is not claimed
  PASS.
- No existing settled generic recurrence relation/baseline semantics were found:
  `GrammarPolicy` carries only opaque string refs
  (`rawlsing_next/universal_grammar/types.py:437-438`);
  `enumerate_frontier` only records the gap
  (`rawlsing_next/universal_grammar/enumerate.py:489-497`);
  `rawlsing_next/pre553_recursive_handoff.py` consumes a caller-supplied parent
  predicate/replay binding and does not define policy semantics for
  `recursion_relation_ref`/`baseline_policy_ref`.
- The inherited contracts require D bounds and recursion/baseline identity
  (`INPUTS/CONTRACTS.md:24,30`) but do not define a typed recurrence relation or
  baseline issuer policy.
- This is a **generic synthetic/software contract gap**, not an original-source
  scientific issuance requirement. R3 does not need original source authority
  to represent a generic relation; no generic relation schema exists to
  implement. The limitation is therefore honest.

### Smallest competing interpretations (for HQ/issuer, not invented here)

1. **Generic software interpretation (smallest):** define
   `recursion_relation_ref` as a typed dyadic relation over occurrence/unit
   identities and `baseline_policy_ref` as a baseline selection policy; then
   enumerate repeated discovery generations up to D. This needs no original
   source science, only a generic contract/issuer schema.
2. **R3 declared limitation (current):** declare FORK-over-conditioners only;
   reserve D/recurrence for a later competent issuer. No D13 PASS, no silent
   drop, no invented chain.
3. **Original-source issuance interpretation (larger):** require each original
   source to issue specific recurrence/baseline objects. This is not necessary
   merely to represent generic policy and must not be manufactured as a blocker.

R3 chose interpretation 2 and documented it exactly. That is an honest
preserved limitation. It is **not full whole-node recurrence functionality**;
any R03 recursive/minority claim remains outside the qualified scope.

## No remaining blocking defect

No A1-A3 defect was reproduced. No candidate code/test edit was made. Prior R2
defects A1-A3 are closed; A4 is dispositioned as an explicit limitation. R03,
R04 custody, original science, N11/N12 and production/CI remain NOT_REACHED.
