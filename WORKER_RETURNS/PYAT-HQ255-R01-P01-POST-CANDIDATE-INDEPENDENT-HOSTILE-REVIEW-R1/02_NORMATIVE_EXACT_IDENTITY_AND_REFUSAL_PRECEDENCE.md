# HQ255 R01 — normative exact-identity and refusal-precedence findings

Subject: the frozen P01 correction at `rawlsing_next/pre553_service_f8_source_scope_binding.py`
(candidate blob `848d2d0e…` against baseline `4ba00b8e…`), the block that refuses
`BINDING_PERMISSION_IDENTITY_MISMATCH`.

## 1. Exact identity semantics — what is compared

```python
receipt_permission_refs = receipt.request_key.get("target_use_permission_refs", ())
declared_permission_refs = tuple(request.bound_target_use_permission_refs or ())
declared_permission_keys = {permission.key for permission in declared_permission_refs}
receipt_permission_keys = {
    exact_ref(permission, "target_use_permission_ref").key
    for permission in receipt_permission_refs
}
if declared_permission_keys != receipt_permission_keys: raise _refusal(...)
```

`ExactRef.key` is `f"{kind}|{object_id}|{content_hash}"` (`pre553_empirical_objects.py`), so the
comparison is over the **full exact ref identity including the SHA**. Independently confirmed:
the same `object_id` with a changed `content_hash` is **refused** (probe
`same_object_id_changed_sha`). Addition, omission, replacement, superset and subset are all
refused.

## 2. Set normalization — order, duplicates, and what the two sides actually hold

- **Receipt side** is normalized by `_ref_list` in `pre553_service_source_applicability.py`:
  it **dedupes and sorts** by `canonical_json(ref.as_dict())`. Receipt refs are therefore already
  a canonical, duplicate-free set.
- **Binding side** keeps the caller's tuple order and duplicates (`_ref` per element only).
- The check is **set equality**, so it is both order- and duplicate-insensitive.
- Confirmed by independent probes:
  - `receipt [A,B]` vs `binding [B,A]` → **BOUND**; the canonical material records the binding's
    order (`[B, A]`), not the receipt's canonical order.
  - `receipt [A]` vs `binding [A, A]` → **BOUND**; the canonical material records the duplicate
    twice.
- No in-repo consumer of `bound_target_use_permission_refs` requires ordered or subset semantics:
  the only readers are the binder itself (`material()`, the binding record, and the replay
  preimage) and its courts. Order-insensitivity is therefore **safe at this grain**, and it is
  explicitly disclosed by the author for ordering. Duplicate-insensitivity is **not** mentioned
  in the author's disclosure and is recorded here as an observation, not a defect: a duplicated
  declaration of the same exact permission grants nothing new, and the receipt side can never
  carry a duplicate.

## 3. Refusal precedence — observed and assessed

Placement is immediately after `BINDING_TARGET_USE_GRAIN_MISMATCH` and before the release-grain
check. Independently measured:

| request state | code returned |
|---|---|
| wrong target use + wrong permission | `BINDING_TARGET_USE_GRAIN_MISMATCH` (sibling still outranks) |
| wrong permission + wrong release | `BINDING_PERMISSION_IDENTITY_MISMATCH` (new check precedes release) |
| wrong release + agreeing permissions | `BINDING_RELEASE_GRAIN_MISMATCH` (unchanged) |
| wrong permission only | `BINDING_PERMISSION_IDENTITY_MISMATCH` |

Assessment: the only precedence change is for a request that is simultaneously wrong on
permissions **and** release. The new code then wins. That is a **fail-closed** ordering (it
refuses earlier), it does not shadow the target-use sibling, and every pre-existing single-grain
refusal keeps its exact code. It is acceptable as-is; if HQ prefers the older release-first order
for multi-grain requests, the single block would move after the release check, but nothing in the
accepted owner surface requires that.

## 4. Vocabulary and exception surface

- `BINDING_PERMISSION_IDENTITY_MISMATCH` occurs **0** times in the baseline binder blob; it is new
  candidate vocabulary, not adopted authority.
- `ServiceF8ScopeBindingError` subclasses `Pre553IntegrityError`. The new block raises the binder's
  own `_refusal` type on the normal path. One edge: if a receipt's stored permission mapping were
  malformed (not exactly `kind/object_id/content_hash`), `exact_ref(...)` raises plain
  `Pre553IntegrityError` rather than the binder subclass. This is **not reachable** through the
  genuine applicability owner, and the binder's promise of a single typed refusal surface is only
  qualified on that unreachable path — recorded for completeness, not as a blocker.

## 5. Empty and absent permission sets

`ServiceApplicabilityF8ScopeBindingRequest.__post_init__` refuses an empty
`bound_target_use_permission_refs` with `TARGET_USE_PERMISSION_BOUND_REFS_REQUIRED`, and the
applicability owner refuses an absent request-key component with `SERVICE_REQUEST_UNDETERMINED`
(probe `empty_sets`). The new check therefore never sees an empty/empty comparison; its
`.get(..., ())` default only guards a malformed key.

## 6. Backward compatibility and replay identity

For a matching two-permission binding the candidate and the baseline binder produce
**byte-identical** `material()` (`material_sha256 74fc3ffa…`) and identical `binding_ref`,
`binding_request_ref`, receipt id and receipt replay identity. The guard is a pure no-op on
honest inputs and cannot perturb replay identity on matching cases. On a mismatch no binding
object or material is produced at all.

## 7. Normative recommendation to HQ

1. Accept the production block at its exact grain (one field, fail-closed, no widening) — subject
   to item 2.
2. **Repair the court, not the guard**: `test_adopted_binder_baseline_was_the_unmodified_owner` is
   coupled to the uncommitted-edit state and fails on the committed candidate. Compare the
   **parent/base** commit blob (or a documented constant) instead of `HEAD:`. Until that is done,
   the candidate cannot be certified green by its own court on any committed SHA.
3. Record the two semantic disclosures (order-insensitivity — author-disclosed;
   duplicate-insensitivity — first recorded here) in the candidate's normative text so Stage C
   intake inherits them explicitly.
4. Preserve the separate provenance/authority-custody gap (HQ253 T01 G1/C1) and the F7-RR-04G /
   T1 holds as out of scope; this correction is coherence only and grants nothing.
