# SOROK REMONT — R3 integration and confirmed sourcefree bug repair, 2026-11-19

**Construction base:** ORACLE UM-SOROK R3 PR #1167 `3dba91136870ab5e766ca14faacd847531dea075`.
**Exact inherited source cuts:** SR-P004 PR #1165 `480d3595ef744779cbfce186cd1696d8e8f61e36` and SR-P005 PR #1170 `1b0bbca8e610d81cea820d200f2c90b73ea3efdc`; the older overlapping #1166 remains a separate, unreceived candidate.
**SEAM context:** PR #1161 `b91d857202d8f84a4721cbc185b6d3aeac3349e3`, documentary Constitutive Organism R2, not an implemented owner.

## Reproduced before coding the R3 delta

1. R3 `psychodynamics.validate_tendencies` accepts `{'action':'TELEPORT','polarity':'WITHHOLD'}` without error even though `organism.ACTIONS` does not contain TELEPORT. This can persist as a seed's psychological inhibition of nonexistent conduct. **SR-P024 confirmed first-fault**.
2. R3 `construct_parent` accepts an external `adult_constructor` packet with `forms=[]`, `projects=[]`, `links=[]`, and creates an adult in the persistent world with no operative acquired form or project. **SR-P021 confirmed first-fault**, not legitimate scientific adult constitution.
3. Sourcefree R3 has its own pressure-flow and newly acquired composition, but still omits activity history for blocked/partial attempts and can graft inherited generic plan means onto unrelated projects. **Already independently documented SR-P004 from #1165**.
4. R3 `world.py` is the same original R2 blob `b744eb52913a95998f99cbfa6e2a1f500804c932`, carrying the independently reproduced material-stock authorization and negative-price/wage first-faults. **SR-P005 from #1170**.

## Actual source repair and source conservation

- Preserve R3 pressure-flow (`psychodynamics.py`) and its acquired `qualified_learned_compositions` engine. Replace only its *inherited provisional action-pattern branch* with P004 project-owned means logic.
- Port exact P004 `activity.py` and `runtime.py` from the PR #1165 tested cut; merge `constitution.py` additions (`means` and `latest_lived_attempt`) into R3's existing acquired streams.
- Port exact P005 `world.py` from PR #1170, with legal material controller, world-owned stock grant, and finite nonnegative monetary input guards.
- R3 `parents.py`: refuse empty LLM-proposed forms+projects as `NO_OPERATIVE_FICTIONAL_PARENT_CONSTITUTION`. Do not pretend an empty validated parent is a real simulated adult. Does not mandate an adult taxonomy or invented historical motives.
- R3 `psychodynamics.py`: require `tendency.action in organism.ACTIONS` at source admission; R3 parent and developmental ADD_FORM both call this validator. Correct adult seed rejection precedes any ledger initialization.
- Two inherited P004 unit fixture namespaces lacked R3's new `learned_compositions` slot. Their fixtures now supply `learned_compositions=[]`; this is **test API adaptation, not a production runtime defect**.

## Executed evidence and grade

R3 original archive `b83391bb0b6b20fde7dab1f1bfdf8c0de44e97494371fb8f7f73a4750f9358d5` was materialized and opened; its GitHub R3 world/psychodynamics blobs matched. Original R3 baseline **42 passed, 0 failed**.

After integration, `python -m unittest discover -s tests -v` **58 PASS, 0 FAIL** on locally combined exact source files: original R3 42 + existing P004 5 + existing P005 8 + three new R3 negative/positive tests. A first combined trial had exactly **two test-only errors** because P004's `SimpleNamespace` fixtures lacked R3's `learned_compositions`; fixed by upgrading fixtures, no weakening of R3 runtime. GitHub produced Python/test blobs are byte-verified against `git hash-object` of locally executed files.

**Important limitations:** This is a coherent R3 *sourcefree* research candidate, not a native SOROK person, independent review, LLM external provider execution, empirical POP/DEV/TRANS science, PYAT survey fidelity, owner source rights, full privacy, protected merge, or paired canonical PROGRAMMA/CURRENT_PROGRESS receiving. SR-P004, SR-P005 remain PARTIAL. SR-P022/023 stay OPEN. SR-P021/024 have local author fixes pending receiving. No sourcefree fixture can confer institution issuer competence.
