# HQ254 P01 — exact changed paths and back-compat evidence

## 1. Changed paths — EXACTLY THREE, all authorized

| path | change | authorization |
|---|---|---|
| `rawlsing_next/pre553_service_f8_source_scope_binding.py` | `+33 / -0` | "Only candidate source edits" |
| `rawlsing_next/tests/test_pre553_f8_receipt_permission_identity_hq254.py` | NEW, 16 tests | "one narrowly named test file" |
| `WORKER_RETURNS/PYAT-HQ254-P01-PERMISSION-IDENTITY-BOUNDED-CANDIDATE-R1/` | NEW, 4 files | "own return folder" |

No other production module, no other test file, no HQ/control path, no authority or issuer path.

## 2. The complete candidate diff

Exactly one refusal block, added after `BINDING_TARGET_USE_GRAIN_MISMATCH`, no deletions and no
modification to any existing line:

```diff
+    # -- bound target-use permission identity coherence ----------------------
+    # HQ254 P01 CANDIDATE. Quarantined correction, NOT adopted security authority.
+    #
+    # Applicability is decided under the exact target_use_permission_refs carried in
+    # the receipt's request key; the receipt itself declares those refs to be "bound
+    # input not a grant". A binding that declares a DIFFERENT permission set is
+    # therefore describing applicability that was never decided. Before this check the
+    # binder copied the divergent set verbatim into the binding's canonical material,
+    # where downstream attestation would read it as the admitted one.
+    #
+    # This is the exact missing sibling of BINDING_TARGET_USE_GRAIN_MISMATCH above:
+    # the same fail-closed grain-coherence intent, one field that had no check at all.
+    # It grants no permission, widens no source-scope power, demands no F8 producer
+    # custody, and adds no model use. It only refuses to emit a binding whose declared
+    # permissions disagree with the receipt it claims to consume.
+    receipt_permission_refs = receipt.request_key.get("target_use_permission_refs", ())
+    declared_permission_refs = tuple(request.bound_target_use_permission_refs or ())
+    declared_permission_keys = {permission.key for permission in declared_permission_refs}
+    receipt_permission_keys = {
+        exact_ref(permission, "target_use_permission_ref").key
+        for permission in receipt_permission_refs
+    }
+    if declared_permission_keys != receipt_permission_keys:
+        raise _refusal(
+            "BINDING_PERMISSION_IDENTITY_MISMATCH",
+            f"binding bound_target_use_permission_refs "
+            f"{sorted(permission.as_dict()['object_id'] for permission in declared_permission_refs)!r} "
+            f"do not equal the receipt's target_use_permission_refs "
+            f"{sorted(permission.get('object_id') for permission in receipt_permission_refs)!r}; a "
+            f"binding may never re-describe applicability that was decided under a different "
+            f"bound target-use permission set",
+        )
```

Refusal site: **line 723**. Blob `4ba00b8ecf73f70ad0f6481e255fd0117744418a` →
`848d2d0eedb04b792747e9d6aaa49bb39d108a2c`.

## 3. Why every existing caller is unaffected

Every pre-existing caller passes a **single identical permission token** on both sides:

| caller | SA `target_use_permission_refs` | binding `bound_target_use_permission_refs` |
|---|---|---|
| `test_pre553_service_f8_source_scope_binding_court.py` | `[tqref("perm-bound")]` | `(ExactRef(tqref("perm-bound")),)` |
| `test_pre553_service_f8_binding_authentication_court.py` | `[tqref("perm-bound")]` | `(ref("TQ","perm-bound"),)` |
| `test_pre553_service_f8_source_scope_binding_repair_court.py` | `[tqref("perm-bound")]` | `(ref("TQ","perm-bound"),)` |

The set comparison is therefore satisfied by every honest existing case, which is why the new
code never fires for them and no existing refusal precedence is disturbed.

## 4. Back-compat evidence

| run | before candidate | after candidate |
|---|---|---|
| 4 adopted baseline courts (199 tests) | **199 passed**, exit 0 | **199 passed**, exit 0 — identical |
| new P01 court (16 tests) | n/a | **16 passed**, exit 0 |
| combined | — | **215 passed**, exit 0 |
| wider sweep | — | **380 passed** + 9 pre-existing collection errors |

The 9 collection errors are missing `pandas`, missing `pyarrow`, and missing
`rawlsing_next.tests.d07_bounded_loss_harness` — all pre-existing on this tree, none imported by
this lane.

## 5. Negative control — the candidate is a genuine discriminator

The production file was reverted to the sealed tip and the new court re-run:

**9 failed / 7 passed.**

The 9 failures are exactly the mismatch-refusal and confinement witnesses. The 7 that pass are
positive, schema, back-compat and no-power-widening guards that assert **unchanged** behaviour, so
passing them against the unmodified binder is the correct outcome rather than a gap.

## 6. Scope discipline

The new court is narrowly named and covers one field. It deliberately does **not** re-litigate
provenance/authority custody, producer identity authentication, or any other binder refusal —
those belong to their own courts and to the separate HQ253 T01 finding, which remains **open**.

## 7. Quarantine

Candidate only. Not merged, not cut over, not adopted. Awaiting separate sealed HQ intake and an
independent post-candidate reviewer.
