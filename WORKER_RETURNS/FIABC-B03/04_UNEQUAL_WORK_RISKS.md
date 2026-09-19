# FIABC-B03 — Unequal-Work Risks

These are factual risks in the current execution/accounting graph. They are not repair proposals.

## 1. Candidate C does not execute the same workload

Current `ee_p2x_darwin_stage_backend.py` hard-stops LiTS-C at S02 because frozen CACC1 omits q310/q311 required by the F02 composite projection. The same backend rejects WVS-C entirely as having no executable backend path.

That means there is no current three-way sequence in which A, B, and C all realize validated C11, execute the same I03/I05 workload, traverse lifecycle stages, and produce comparable terminal vectors.

This alone prevents a proved equal-work A/B/C comparison.

## 2. Current parity is candidate self-replay, not an independent pre-candidate oracle

The frozen court law requires candidate-neutral reference oracles to be materialized and frozen before candidate output exists.

Current implementation order is the reverse:

- S01 calls `_bind` and sets `candidate_output_first`.
- S03 later sets `oracle_frozen` and a hash-derived `oracle_identity`.
- S03 executes `_i03(binding)` twice through the same candidate binding.
- equality of those two candidate executions is copied to five separate parity dimensions: semantic, ExactRef identity, replay, integrity/fail-closed, and frontier/typed-negative.

This proves at most repeatability of one candidate's current I03 output. It does not independently prove cross-candidate semantic or typed-negative parity.

## 3. LiTS A and B preserved preparation evidence is not metrically symmetric

LiTS-A's preserved first-build receipt contains detailed telemetry including wall time, CPU, RSS, scratch, source decode, bytes read/written, and durable bytes.

LiTS-B's preserved cacheless C11 receipt explicitly states:

`NOT_CAPTURED_BY_ACCEPTED_IDENTITY_SESSION_RUNNER__NO_NUMERIC_SUBSTITUTE`

The current backend intentionally emits typed `NOT_CAPTURED_PRESERVED_STAGE` slots rather than fabricating values. That is correct fail-closed behavior, but it also means the two preserved construction stages do not provide equal numerical accounting.

## 4. CPU accounting is per-last-measurement, not candidate-total

`_measure` replaces `cpu_user_ns` and `cpu_system_ns` every time a stage or nested operation is measured. Those slots therefore contain only the most recent call's CPU delta, not the candidate's accumulated CPU burden.

Because the frozen metric manifest exposes one terminal CPU slot per source×candidate vector, current code does not prove that slot equals total candidate CPU cost.

## 5. Peak RSS is process-global across sequential candidates

`_measure` stores `RUSAGE_SELF.ru_maxrss`. On Darwin this is a process-wide peak and is monotonic over the process lifetime.

The court driver executes candidate cells serially in one Python process. Therefore B or C can inherit a peak created by A, and WVS candidates can inherit peaks from LiTS. Filesystem work roots are isolated, but `ru_maxrss` is not reset at candidate boundaries.

This conflicts with interpreting terminal `peak_rss_bytes` as candidate-local resource cost.

## 6. Prior candidate sessions remain referenced in the process

The backend module-global `_SESSIONS` cache is keyed by `(source, candidate)`. Moving to the next candidate does not clear earlier candidate entries. S09 pops only the currently executing candidate when exercising B/C deletion/rebind.

So prior candidate repository/binding/projection objects may remain live in memory while later candidates are measured. This compounds the RSS/accounting ambiguity.

## 7. The cold-I03 metric is overwritten

S04 measures `cold_i03_latency_ns` when first admitting performance. S07 later measures another I03 execution into the same `cold_i03_latency_ns` key.

The terminal vector therefore loses the S04 sample and retains S07. The repository does not state, in the backend, which of these two executions is intended to be the dispositive cold-I03 number.

## 8. A's S09 metric name does not match the work actually timed

For Candidate A, S09 sets `delete_rebuild_wall_ns` by timing only creation of the persistence-information JSON receipt. It does not delete or rebuild R5 in that handler.

For B, the same metric times deletion of named scratch state, session drop, and rebind.

Thus the same metric field represents materially different work.

## 9. Invalidation metrics are assigned, not measured

S10 records source-release invalidation units as:

`1 + int(candidate in {A, C})`

S11 records semantic-authority invalidation units as:

`1 + int(candidate == C)`

No invalidation or recomputation is executed in either handler. These fields encode a model of recomputation breadth, not observed candidate work.

## 10. Stale/corrupt-state behavior is represented by law hashes

S12 and S13 do not make candidate state stale or corrupt and then observe implementation behavior. They hash a law string and record PASS.

B is treated as not applicable by frozen court law. A/C therefore appear to have extra behavior evidence, but the current evidence is documentary/mechanical identity rather than an exercised failure path.

## 11. Interruption recovery does not interrupt the candidate implementation

S14 creates `interruption.partial`, deletes it, hashes that fact, and records PASS. It does not interrupt A's R5 build, B's virtual-C11 materialization, C's accelerator build, or a candidate query/discovery session.

The frozen workload calls for interruption/failure recovery; the current handler does not establish candidate-specific recovery cost or semantics.

## 12. Terminal byte metrics are derived from end-state directory sizes

S16 sets:

- `durable_authoritative_bytes = 0`
- `durable_transformed_regenerable_bytes = durable directory size`
- `bytes_written = durable + scratch directory sizes`
- `bytes_rewritten = 0`

These are not observed byte-write/rewrite counters. A candidate can write and delete large transient state yet end with a small directory, or rewrite bytes without that being reflected.

## 13. Common semantic-materialization work is embedded in candidate S01

LiTS/WVS projection objects and runtime authority packages are common semantic inputs. Current P2X constructs/materializes these inside candidate binding logic.

That is not necessarily wrong, but it means `build_or_open_wall_ns` mixes:

- candidate-neutral semantic/runtime object realization; and
- candidate-owned physical repository realization.

The present code does not mechanically separate those costs, so `WHO_OWNS_THE_TRUTH` is clearer than `WHO_PAYS_TO_REALIZE_IT`.

## 14. C11 is a common interface but not the full treatment boundary

A/B/C owner implementations are designed to converge at validated C11. However, Candidate C's frozen physical meaning also includes CACC2 on the exact I05 path. A court that compares only through C11 would omit part of C's accepted physical treatment.

The later learned empirical product is therefore the stronger end-to-end convergence candidate, but current C cannot reach it.

## 15. Current P2X is still held after infrastructure repair fan-in

Control-branch HQ records that R6U/R6V/R6W/R6X repairs were selectively fanned into P2X but measured execution remains held pending exact local stopped-ledger reconciliation and HQ adjudication.

Therefore no later repaired measured run can currently be treated as evidence closing the gaps above.

## Net result

The repository supports a coherent intended independent variable, but the current court does not yet demonstrate equal executable workload or comparable candidate-local accounting.

Terminal implication:

`FIABC_B03_BLOCKED__A_B_C_EQUAL_WORK_MODEL_UNPROVED`
