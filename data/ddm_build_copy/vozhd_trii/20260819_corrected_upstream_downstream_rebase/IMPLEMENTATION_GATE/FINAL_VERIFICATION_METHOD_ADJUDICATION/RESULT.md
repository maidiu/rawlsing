# FINAL VERIFICATION METHOD ADJUDICATION

**HQ branch prewrite head:** `27e91f2f00e4bc1fef2c45e1e28a455387e0084d`  
**Final integration candidate:** `b66e282f4185ece6682723bc5e53c1a23534d5f0`  
**Blocked inspectorate return:** `9dcaddce1438fd8569b227a4af862c488a144dbb`  
**Blocked token:** `IG_FINAL_VERIFICATION_ENVIRONMENT_BLOCKED`

## Adjudication

The blocked inspectorate return is accepted as an **environmental verification failure only**. It is not an implementation failure, semantic failure, composition failure, or evidence of a defect in the final integration candidate.

The prior requirement for an *actual Git checkout* is an operational transport condition, not a frozen semantic invariant. For this final pure-Python verification gate, exact path-preserving materialization from immutable Git blob objects is accepted as execution-equivalent to a checkout **only under the proof obligations below**.

This adjudication does **not** waive the fresh package-local test rerun. It replaces an unavailable transport mechanism with an immutable-content-equivalent mechanism.

## Authorized equivalent verification method

A verification-only worker may:

1. obtain the exact 17 pinned file contents belonging to candidate `b66e282f4185ece6682723bc5e53c1a23534d5f0` through exact GitHub commit/blob APIs;
2. materialize them under their exact repository-relative paths beneath a fresh temporary root;
3. recompute each Git blob SHA-1 locally as `SHA1("blob " + byte_length + NUL + exact_bytes)` and require equality with all 17 frozen blob pins before test execution;
4. prove that the nine test files and eight runtime files do not depend on `.git`, branch/ref names, Git worktree state, mutable-latest repository discovery, or files outside the 17-file materialized test closure;
5. execute the nine exact package/integration test files from that root with the materialized root as `PYTHONPATH`;
6. record exact command, Python/pytest versions, total passed/failed/error counts, elapsed time, and all 17 local recomputed Git blob hashes.

Any blob mismatch, path mismatch, hidden repository-metadata dependency, import outside the declared closure, or test failure is a verification failure. No reconstruction by semantic rewriting, normalization, copy editing, generated substitutes, or inferred content is allowed.

## Required test set

- `rawlsing_next/tests/test_m1_temporal_v554_admission_dedup.py`
- `rawlsing_next/tests/test_m2_v555_atomic_route.py`
- `rawlsing_next/tests/test_m3_v556_higher_order_structural.py`
- `rawlsing_next/tests/test_m4_v557_v558_publication_repository.py`
- `rawlsing_next/tests/test_m5_runtime_rsc_peer_prior.py`
- `rawlsing_next/tests/test_m6_actor_safe_expression.py`
- `rawlsing_next/tests/test_psepf_zero_positive_guard.py`
- `rawlsing_next/tests/test_render_bounded_expression.py`
- `rawlsing_next/tests/test_whole_machine_integration.py`

## Scope

Runtime/test modification remains forbidden. Semantic redesign remains forbidden. Legacy runtime, deployment, cutover, retirement, positive SPDM, and stage-close authority mutation remain forbidden. Only verification receipts may be committed on the verification mission branch.

## Success token

`IG_FINAL_MATERIALIZED_VERIFICATION_COMPLETE__READY_FOR_FINAL_RECLOSURE_ADJUDICATION`

This token is valid only if all 17 local Git blob hashes match their candidate pins and the complete nine-file pytest invocation passes.