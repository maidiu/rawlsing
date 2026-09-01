# Respondent restoration / admission owner handoff

FFX001-D `d15e32398738a5b52ebede954b79278bd9f32fd2` defines the contract but explicitly refuses to select a carrier or restoration path.

## Owner stack

1. `PROJECT_CURRENT_SELECTION / CURRENT_ADMISSION_AUTHORITY` selects the exact CURRENT respondent carrier/set and governs supersession.
2. `EMPIRICAL/SOURCE OWNER` authenticates respondent/source-scope/value semantics.
3. `SOURCE/MEASUREMENT SEMANTIC AUTHORITY` closes qimpl→empirical-measurement mappings not already exact.
4. deterministic implementation may materialize bindings and execute predicates only after 1–3.

Current PRE-MAIN exposes the relevant owner class through OBL017/018 (`VOZHD/HQ current-admission authority` / competent source-admission authority), but no exact current carrier is admitted by this worker.

## Commissioning act

A grounded bounded current-admission court must be commissioned to answer exactly:

> Which immutable respondent-grain carrier/set is CURRENT for the bounded canary, at which source scope, under which FFX001-D restoration path A/B/C/D/E, with what identity/succession proof and qimpl/measurement binding?

FIELD FORGE may supply candidate evidence and hostile tests. It may not vote on its own carrier.

Required return: immutable `CURRENT_RESPONDENT_EXECUTION_BINDING_PACKAGE` satisfying FFX001-D, including carrier identity, respondent identity, source scope, qimpl→measurement binding, predicate inputs, exposure rule, response binding, ancestry/supersession and canary replay receipt.