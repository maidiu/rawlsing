# EE-W4 integration notes for the eventual EE-W1 workload

EE-W4 claims no workload-definition authority. EE-W1 remains the owner of the frozen EE01–EE16 production workload, eligible named universe cells, exact operation order/repetition schedule, semantic requests, authority-limited states and truth/parity oracles.

To execute that workload, EE-W1 (or a purely mechanical HQ adapter) supplies an EE-W4 execution profile with one fully unrolled ordered `steps` list. Each step names `step_id`, `universe_id`, `operation_id`, applicable `EE01..EE16` requirements, phase, action, and an authority-owned eligibility object with nonempty exact basis. Eligible candidate actions additionally carry the opaque semantic `request` and exact oracle. EE-W4 hashes the profile and the candidate-neutral request payload and proves that A/B/C received byte-identical logical requests for each invoked step.

EE-W4 does **not** infer a missing field from question text, labels, numeric values, frequencies, embeddings, neighboring rows, existing candidate outputs or model judgment. If EE-W1 cannot positively bind a required authority/oracle, the step must arrive as a typed non-eligible state (`MISSING_AUTHORITY`, `UNRESOLVED_AUTHORITY`, `NONCOMPARABLE`, etc.), not as a weakened substitute operation.

The profile may include all required lifecycle steps: cold build, `warm_1`, `warm_2`, `warm_5`, hostile fixture execution, delete/rebuild, exact replay, one-source selective invalidation, and one-semantic/routing-authority selective invalidation. EE-W4 preserves exact listed order; it never creates candidate-specific warmups, pruning, search budgets, cache exemptions, alternate sources or operation substitutions.

Candidate adapter configuration is intentionally outside the workload profile. It is a physical mapping for A/B/C to an executable command with `{request}`, `{response}`, `{scratch}`, `{durable}` placeholders. That physical variation cannot modify the semantic request/oracle. Candidate roots are isolated, and logical receipts are canonicalized by candidate ID so candidate execution ordering cannot change logical results.

Metric summaries retain `universe_id`. WVS, LiTS or any later eligible universe may share the same logical interface while remaining distinct empirical universes. `COMMON_QUERY_INTERFACE != POOLED_EMPIRICAL_UNIVERSE`.

The hostile index contains all 20 cases frozen in the common contract. Synthetic fixtures may test only the named conservation property; their exact expected output must still be supplied by frozen workload authority. Synthetic fixtures do not replace real-source performance cells.
