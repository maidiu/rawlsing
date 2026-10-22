# R56-R00P — independent TEST_ONLY claim-transition contract

**Contract ID**: `R56-R00P-CLAIM-TRANSITION-GATE@1.0.0`. **Independent issuer**: R00P TEST_ONLY policy owner, not R00E implementer or R00V native reviewer. This is an immutable expected-operation *policy* to be used by a separately authorized gate, **not a gate implementation, a scientific source issue, an R09 trusted runtime, or an N11 release**.

The frozen policy consists of `policy.json`, `synthetic_universes.json`, `decision_cases.json`, this contract and `freeze.json`. Git content blobs are integrity identities only. The director must resolve the policy at the exact R00P return commit **outside candidate request selection**. If the immutable pin is absent/unverified or the candidate names a different pin, fail with `REFUSE_PIN` or `HOLD_TRUSTED_NATIVE` according to whether the mismatch is established or verification is unavailable.

## A. Mechanical implementation boundary

A future R00E may implement:
```python
evaluate_r56_sourcefree_claim(
    submitted_claim: Mapping[str, Any],
    *,
    externally_pinned_policy: PinnedPolicyHandle,
    verified_evidence: TrustedObservationHandle | None,
) -> GateDecision
```

This is a proposed **mechanical interface**, not an existing native API or an R09 attestation implementation. `submitted_claim` is entirely untrusted. `externally_pinned_policy` must be resolved from a separately immutable policy ref by a non-candidate owner. `verified_evidence` is NULL for policy-only validation; if a candidate supplies a string pretending to be such a handle, it is not authenticated.

`GateDecision` is a pure record:
```json
{
  "contract_id": "R56-R00P-CLAIM-TRANSITION-GATE@1.0.0",
  "claim_grade_requested": "LOCAL_OPERATOR",
  "decision": "ALLOW_LOCAL_POLICY_CONSISTENT",
  "grade_ceiling": "LOCAL_ONLY_POLICY_CONSISTENT",
  "reason_rule_ids": ["P00_INDEPENDENT_PIN", "P06_NO_DROP_MULTISETS"],
  "policy_ref": {"commit": "<sealed independent commit>", "path": "<policy root>"},
  "considered_expected_ids": ["<all exact, pre-outcome operation IDs>"],
  "submitted_id_diff": {"missing": [], "extra": [], "duplicate": [], "semantic_mismatch": []},
  "eligibility_partition": {"ELIGIBLE": [], "PROHIBITED": [], "INAPPLICABLE_PROVED": [], "HELD": [], "UNKNOWN": []},
  "execution_partition": {"NOT_STARTED": [], "PENDING": [], "COMPLETED": [], "UNSUPPORTED_RUNTIME": [], "ERROR": []},
  "result_partition": {"SUPPORTED": [], "OBSERVED_ZERO": [], "VALID_NULL": [], "DIFFUSE": [], "VALID_EMPTY": [], "ZERO_SUPPORT": [], "UNSUPPORTED": [], "UNKNOWN": []},
  "unresolved_original_obligations": {"source_count": 35, "per_source_axes": 54, "cells": 1890, "global": ["F6", "F7", "F8"]},
  "trusted_native_provenance": "NOT_PRESENT",
  "published_original_grant": "UNISSUED",
  "actual_consumer_values_read": null,
  "positive_claim_scopes": ["TEST_ONLY_POLICY_SHAPE"],
  "held_requirements": ["G3", "G6", "G7", "G8"]
}
```
`<...>` here are explanatory placeholders in documentation, **not** operative example values or authorized evidence. The exact key equality and partitions come from policy's immutable JSON, not candidate-produced lists. For individual local CASE tests the frozen case may explicitly scope a smaller admitted subset but must retain separately declared held/unvisited members and forbid use of that subset to promote the whole 18-operation or universal claim.

### Canonical typed identities

For each considered operation, bind **both** its independently frozen `operation_id` **and** all semantic fields in `synthetic_universes.json`. Never test only counts or hash strings. Identity `K` uses a versioned canonical encoding with explicit type-tags (`string`, `integer`, `decimal`, `bool`, `null`; omit vs null distinguished), UTF-8 normalized field names, deterministic map-key ordering and preserved declared tuple/order sequence. No float/string coercion or sorting ordered targets/conditions. Sets may be sorted only if *owner-declared unordered*. The `v` of a tagged integer is a canonical base-10 string; booleans are actual JSON booleans, not `"true"`.

Minimum K: contract/claim grade; instrument/source/dataset/family/wave/edition and artifact digest; form/option/repeat/rank occurrence identity and administration; respondent/reporting/sampling unit + any lawful link; ordered target and conditioned occurrence tuples including **typed values, domain/state version**; scope/risk/predicate; direction/operation class/arity/topology/J/K/D; RAW or issued weighted estimand, weight/design/uncertainty refs; policy+grammar+native model versions; release/custody source bytes; rights/host/purpose/use; observation, reference, as-of/current/publication clocks; **exact requesting consumer**. Same labels in different form/repeat/unit/role are not identical.

Full considered universe `C` = disjoint ELIGIBLE + PROHIBITED + INAPPLICABLE_PROVED + HELD + UNKNOWN with *each exact ID once*. Eligible subset `E` = COMPLETED + PENDING + NOT_STARTED + UNSUPPORTED_RUNTIME + ERROR (the runtime partition uses these five states). Do not erase E if unvisited. An execution result is a **third** axis, not the eligibility state. Unknown administration is UNKNOWN rather than not administered. A proven not-administered question may be INAPPLICABLE_PROVED at its particular form/occurrence, but not at the entire source. If `C` is not the exact independently pinned multiset with equal semantic projections, return `REFUSE_FRONTIER`. Count-preserving omissions/additions and duplicate IDs fail.

### Exact grade ceilings

- `LOCAL_OPERATOR`: R00P policy consistency may return `ALLOW_LOCAL_POLICY_CONSISTENT` at the *policy/grain only* when fixed expected operations and statuses are correct, with no native claim. A later **independently authenticated local** native run may receive `ALLOW_LOCAL_OPERATOR_VERIFIED`; R00P does not provide that run. A TEST_ONLY mock may test typed comparison mechanics but stays `HOLD_TRUSTED_NATIVE` when claiming native execution.
- `GENERIC_SOURCEFREE`: independent G0–G7 required **in aggregate**: independent policy, diverse native decoded SAV/DTA edge-class cover, full issued and actually executed frontier, exact identity, status, meaningful same-consumer mutation+restored cold replay, and R09 trusted runner/exact-commit check. If the correct but incomplete local packet lacks trusted G3/G6/G7, return `HOLD_GENERIC_R09` (not false PASS). If its declared generic frontier is contradicted or self-authored, refuse for precise reason first.
- `ORIGINAL35_N11`: G0–G8, 35 real issued current source/edition/rights/method/empirical operations and per-wave **30 source +16 empirical +8 F =1,890** plus *additional* F6/F7/F8 global relation edges, actual consumer, independent assessor. Synthetic 35 names, an unissued original `U_item/U_unit/U_app/E_pre`, or an invented source grant cannot pass. A well-formed but unissued original claim is `HOLD_ORIGINAL_G8` and must show all unsatisfied obligations; a claim positively fabricating their existence is `REFUSE_AUTHORITY`.
- No automatic fallback: supported observed zero `OBSERVED_ZERO`, valid null `VALID_NULL`, diffuse `DIFFUSE`, valid-empty `VALID_EMPTY` and zero-denominator `ZERO_SUPPORT` remain distinct. An honestly **complete and independently declared empty frontier** may return `VALID_EMPTY`, not fake supported. Empty *observed responses* to administered operations do not make eligible operations disappear.

## B. Exact cases and runner instructions

`decision_cases.json` defines nonexecuted, **hand-issued** expected outputs. It contains both a frozen `baseline_input` and deterministic per-case input overlays. A future test runner must apply overlay values to the baseline (map merge is recursive, arrays replaced atomically, explicit JSON null overrides). A case's `expected` is the independent oracle; the R00E candidate is never permitted to author/edit it or derive it by calling its own evaluator. Each case checks `decision`, `reason_rule_ids`, `grade_ceiling` and exact identity/status deltas. The `case_scope` is TEST_ONLY; a test-only mocked trusted transport only exercises parsing/negative mechanics, not generic verification.

Status priority is: (1) externally pinned policy mismatch, (2) invalid complete identity/operations, (3) authenticated original permission/currentness conflict, (4) inconsistent typed state/duplicate scientific counting, (5) explicit fabricated native observation, (6) unmet **independent trusted** runtime/replay/consumer requirements, (7) allowed scoped policy-consistency decision. When multiple blockers exist, return all applicable `reason_rule_ids` without masking the earliest refusal. A legitimate held relation remains HELD even if a candidate says the original title is identical.

For a candidate-reported emitted operation object, matching `operation_id` without matching the exact immutable pre-outcome semantic projection is a `REFUSE_FRONTIER` or `REFUSE_IDENTITY` as appropriate. For actual fact/release/consumer K and provider evidence mismatch, return `REFUSE_IDENTITY`, evidence=null; no positive consumer fallback. For a claimed native=true with fabricated call or a callable-name trace, `REFUSE_FORGED_EVIDENCE`. If merely **unverifiable** (and not affirmatively fabricated), `HOLD_TRUSTED_NATIVE`.

A recomputation attempt can be separately recorded by native owner/algorithm/attempt ref while the **scientific count** for an exact operation and accepted result remains one. Reject duplicated counted result (`REFUSE_DUPLICATE_COUNT`), not mere retry. Cold restore must prove same source/permission/operation/currentness and downstream consumer, not a completed checkpoint with zero outstanding work where partial was claimed.

## C. R56 and downstream implementation holds

**Authorized policy output scope**: only `CROSS_HQ_CONTROL_ROOM/universal_execution_policy/r56_sourcefree_v1/`. This policy owner may write a documentary return under `WORKER_RETURNS/PYAT-R56-R00P-INDEPENDENT-POLICY-R1/`. It may not edit `CROSS_HQ_CONTROL_ROOM/universal_promotion_gate.py`, `tests/universal_execution_oracle/`, decoder/adapters, C11/Route B, workflow, protected config, HQ progress or archived source evidence. R00E implementer cannot edit this frozen policy; R00V native reviewer is distinct.

The policy freeze is a **prerequisite** for separate R02 row/occurrence and R04.byte consumed-byte work, but those future code and reviewer branches require independent correct R56 sealed launch/compatibility and custody. R04.joined awaits R03. R01/R03/R05/R06/R07/R08/R09, J52/W52 and original science remain STOP/HOLD under their own authorities. This policy does not create R09 runner or CI authentication and cannot make N11/N12 proceed. R02/R04 are required to consume stable K/source identity and independent expected-set rules without inventing alternate schemas.

## D. Frozen source precedents (not renewed science)

- U53A `01_INDEPENDENT_UNIVERSAL_DEMAND_ORACLE.md` blob `0aaf795c56026bc11cc52210375e22325ae3d4f3` (unchanged); `UNIVERSAL_RELEASE_GATE_SPEC.json` blob `de1417ad83194b929732e19ec5c87885d33eb0f8`.
- U53A exact original35 `evidence/ORIGINAL35_ACCEPTANCE_OBLIGATIONS.json` blob `f5a3621e83d475e51fff4d3aba3eceb37dbaf9e4`, 35 SRC records, 30 S +16 EE +8 F per source; global F6/F7/F8 separate.
- Director12 at `40511175ca7c2dd6b858e4bc3d4c4bd874d93f16` blob `4208d989c8fe9a147ce5f2d6b638ce0eae58c549`; R56 user stop amendment at `fcbb2ee1d7a6eae040e0964bb8474e8d04d47989`, blob `5cf690c7ff5aed40c64194e0dc138cadc2db431e`.
- UR-M3 `01/02/03` and director13–14 remain inherited as **narrowed** by R56. No unissued M3 broad flight is activated by this policy contract.

**No native execution** occurred in R00P. The directly pushed Git commit, verified startup ancestry, exact allowlist diff and readback of material blobs constitute policy **custody**, not empirical or trusted runner proof.
