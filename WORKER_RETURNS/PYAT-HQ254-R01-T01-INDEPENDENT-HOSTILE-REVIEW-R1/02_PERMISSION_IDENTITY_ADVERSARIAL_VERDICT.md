# PYAT HQ254 R01 — Permission identity adversarial verdict on FROZEN T01

**Finding:** `R01-PERMISSION-ID-NONREFUSAL-001`.  
**Classification:** `CONFIRMED_CODE_LOCAL_CROSS_INPUT_PERMISSION_IDENTITY_CONSISTENCY_DEFECT__AUTHOR_REPORTED_RUNTIME_NONREFUSAL__NO_T1_PERMISSION_GRANT`.  
**Frozen candidate:** `e609be4f68c51182c5acb3a99c671949f1b71d34`; production binder **unchanged** blob `4ba00b8ecf73f70ad0f6481e255fd0117744418a`, `rawlsing_next/pre553_service_f8_source_scope_binding.py`; source owner unchanged blob `3e40caca29e8c96ee1f412f919cfc7dba63f96c4`.

## Threat model / precise contract

The positive applicability owner `SA.resolve_service_source_applicability(ServiceApplicabilityRequest, CandidateClassBinding, records)` produces a receipt for the **specific** service request key, including **target_use_permission_refs**, and includes those refs in `request_key` and `candidate_set_identity` (`pre553_service_source_applicability.py` blob `3e40caca29e8c96ee1f412f919cfc7dba63f96c4`, lines 308–388, 684–809). `ServiceApplicabilityF8ScopeBindingRequest.bound_target_use_permission_refs` is separately accepted from the caller. Its `__post_init__` checks that supplied refs exist and have the `ExactRef` type, expressly states **“presence still grants nothing”** (binder lines 263–351). The binder is obliged to preserve the *same exact use/permission identity* it claims to bind; it has no independent power to issue a permission.

## Exact hostile witness (candidate test lines 558–588)

| Field | Applicability receipt key | F8 binding request |
|---|---|---|
| service | `REVERSE_POSITIONED_SUBJECT_EMPIRICAL_POSSIBILITY_INFERENCE` | same |
| source/release | one `xor_fixture()` universe / `REL-c1-at09-xor` | same |
| target_use_ref | `hq253-fixture-target-use` | same |
| permission refs | `hq253-fixture-perm-only` | **`hq253-other-perm`** |
| authority grade | fixture-only references | fixture-only references |
| result (author report) | owner-generated `ADMITTED` receipt | binder constructed, F8 `EXACT_SUPPORTED` and same F8 hash |

Exact test variables: `PERMISSION_REF = ref("TARGET_USE_PERMISSION","hq253-fixture-perm-only")`, `OTHER_PERMISSION_REF = ref("TARGET_USE_PERMISSION","hq253-other-perm")` (test 82–100). It positively asserts the old permission is in the receipt and new one is not (558–566), passes only the new permission into the binder request, asserts it was copied into the bound object, then calls the authenticated evaluator with that object (567–587). This is **not** a test that a real-world unauthorized user accessed a production service.

## Root-cause proof from code

`bind_service_applicability_to_f8_scope` (binder blob `4ba00b8ecf73f70ad0f6481e255fd0117744418a`, lines 644–894):
1. Confirms receipt label; compares **`service_request_set_identity`**, service_id, candidate_class, target_use_ref and release against receipt (673–711).
2. Omits comparison of **`request.bound_target_use_permission_refs`** with **`receipt.request_key["target_use_permission_refs"]`** anywhere in the function. Full read of unchanged 1068-line module finds permission refs only in dataclass input/material/output and at assignment line **881**.
3. Computes `binding_ref` including the new binding request material **and** authentic receipt replay (853–869). This cryptographic hash is valid for the pair of **conflicting** inputs, but does not make them agree.
4. `evaluate_bound_positioned_subject_possibility` calls `_authenticate_binding_against_authority`, which re-runs the **same binder with the same conflicting inputs** (894–961, 960–1047), so it detects object forgery but not semantic permission-set mismatch. The unchanged F8 core `result.material()` contains no permission identity (`source_backed_positioned_subject_possibility.py` blob `62e5eced47b64512f47b004e3e13a6ef3fe21de7` lines 334–390), explaining identical output hash.

The receipt's `service_request_set_identity` cannot rescue this on its own: the F8 binding request **carries the receipt identity as an independent input**, not a recomputation over its own distinct permission-ref tuple. This is why “but the receipt hash is authenticated” is a false defense.

## Independent counterhypotheses

- “Permission refs grant access”: **FALSE**, both owner and binder explicitly call them bound inputs, not grants. This defect concerns advertised identity consistency; no new authority exists.
- “A forged receipt is required”: **FALSE**, witness uses a genuine owner-built fixture receipt.
- “Normal HQ217 binding replay would detect it”: **FALSE by frozen code inspection**, rederivation from the same inconsistent inputs reproduces the same binding. No independent test runtime performed.
- “Different permission refs might deliberately select a subset”: **NOT AUTHORIZED** by inspected binder; mode is only single source vs exhaustive unranked, no explicit permission selection/attenuation operation. A deliberate differing permission semantics would require an actual owner contract and an explicit named transformation, which the frozen code does not supply.
- “Reject only permission absence”: **INSUFFICIENT**; two nonempty but different `ExactRef` sets can still mismatch. `ServiceApplicabilityRequest` normalizes exact permission refs via deduplicated sorted canonical materials (source owner 253–258); binder request preserves tuple order (binder 290–299). A normative court must freeze whether comparison is **exact canonical sets** or order-sensitive identity; do not accidentally grant rank or broaden use.

## One precise first-failing owner and independent falsifier

**First failing owner:** H-D / EE14 **service-applicability-to-F8 source-scope binder** owner, not `source_backed_positioned_subject_possibility`, not C1, not GT2, not a new model-rule issuer.

**Minimal acceptance / hostile court after HQ authorizes P01 correction and a fresh independent review:**
- Use the **same original owner-produced** `CandidateClassApplicabilityReceipt` on the exact singleton source and release. Bind the **same** permission refs from receipt key (including multi-permission positive fixture if needed); require positive `SINGLE_SOURCE_VALIDATION`, authenticated F8 `EXACT_SUPPORTED`, equal material and unchanged F8 geometry.
- Independently substitute one **nonempty but different exact permission** ref in `ServiceApplicabilityF8ScopeBindingRequest`, while preserving service/request-id/class/target_use/source/release/rule. Require a **typed fail-closed mismatch** at the binder *before* binding exists, not at later F8 or in a test that happens to refuse on some unrelated source-grain condition. Assert expected refusal reason from a separately adopted frozen owner code vocabulary; reviewer may propose a new reason for HQ approval, but must not silently mint one here.
- For a multi-ref fixture, test omission, addition, alternate hash under same object ID and (subject to adopted canonical set semantics) permutation, without claiming permission ordering rank.
- Reject a negative control that changes the receipt itself; it must remain genuine and **unchanged**. Re-run adopted HQ217 binding authentication positive/hostile courts to ensure source-scope power unchanged.

**HQ action:** P01 is already separately commissioned at `428be7595fce3ecf6ae3cb37852bee884d9ce2e1`. Do not review/adopt its mutable or eventual correction in R01. Receive its frozen return, commission separate hostile code/runtime review, then only HQ may select acceptance or bounded repair.

**Preservation:** T0 proof can remain valid even while this identity defect exists: ordinary matching test has identical permission refs on receipt and binding; defect is the bypass of a different-input consistency condition. No T1 model-use authority can be inferred from successful T0 calls. No runtime execution was available for this independent browser review.

**STOP:** `HQ254_R01_RETURNED_FOR_HQ_REVIEW__NOT_ADOPTED`.
