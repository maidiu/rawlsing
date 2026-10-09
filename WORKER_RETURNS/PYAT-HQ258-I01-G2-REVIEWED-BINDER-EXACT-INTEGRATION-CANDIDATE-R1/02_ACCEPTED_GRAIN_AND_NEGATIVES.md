# HQ258 I01 — accepted grain and negatives

## 1. The grain this candidate is accepted at, and only at

HQ257 R01 (`f31c6d1394a877d7fa3eec89b678aa0d0f47f6a5`) independently reviewed the frozen P02
candidate on its clean committed code with **16 new / 199 baseline / 215 combined all PASS**.
HQ258 accepts that proof **ONLY** for the narrow grain below.

**Accepted grain — exactly one:**

> A `SERVICE_APPLICABILITY_TO_F8_SOURCE_SCOPE_BINDING` may not be emitted whose declared
> `bound_target_use_permission_refs` disagree, as an exact `ExactRef.key` set, with the
> `target_use_permission_refs` carried in the `CandidateClassApplicabilityReceipt.request_key`
> that the binder consumes. Such a request refuses with `BINDING_PERMISSION_IDENTITY_MISMATCH`.

**Everything else is out of the accepted grain.** Specifically, this candidate does **not**
establish any of the following, and none may be inferred from it:

| not established | status |
|---|---|
| T1 serving adoption | **NOT** claimed |
| EE14 service use or model-use permission | **NOT** granted; live `next_action` keeps `KEEP_EE14_T1_HOLD` |
| F8 producer custody | **NOT** demanded or certified |
| C1 provenance custody | **NOT** certified (the HQ253 T01 provenance/authority gap stays **OPEN**) |
| Currentness / as-of | **NOT** certified (`requested_currentness_claim` remains `None`) |
| Source-scope power widening | **NOT** — refusal-only, one field |
| R01 OBS_01 duplicate insensitivity | **still open**, deliberately not addressed |

## 2. Negatives actually observed on the imported candidate

Re-run at the clean committed candidate HEAD `105510d9ee45bf18ea1086e55221700ecf7ec2b4`:

| negative | observed |
|---|---|
| honest match, binding `[A]` vs receipt `[A]` | **BOUND**, material records `perm-A` |
| mismatch, unrelated `[B]` vs receipt `[A]` | **REFUSED** `BINDING_PERMISSION_IDENTITY_MISMATCH` |
| mismatch, subset `[A]` vs receipt `[A,B]` | **REFUSED** `BINDING_PERMISSION_IDENTITY_MISMATCH` |
| honest reverse order `[B,A]` vs receipt `[A,B]` | **BOUND** — order-insensitive, as reviewed |

Full court negatives (16 total, all passing) additionally cover: superset inventing a permission,
partial substitution within a set, dropping one of three, refusal occurring before any binding
object exists, the new code not shadowing `BINDING_TARGET_USE_GRAIN_MISMATCH`, release-grain
refusal unchanged, and the no-power-widening confinement guard.

## 3. Pre-existing refusal precedence, unchanged by this candidate

Verified on the imported code:

| situation | code |
|---|---|
| wrong target use (and wrong permissions) | `BINDING_TARGET_USE_GRAIN_MISMATCH` — still outranks permission |
| wrong permissions (and wrong release) | `BINDING_PERMISSION_IDENTITY_MISMATCH` |
| wrong release, permissions agree | `BINDING_RELEASE_GRAIN_MISMATCH` — unchanged |

This matches the reviewed candidate exactly. **No existing line was modified by the import**, so
precedence and set semantics are byte-identical to what R01 reviewed.

## 4. Honest positive case preserved byte-for-byte

An honest binding still produces byte-identical `material()` to the pre-candidate binder — the
correction is refusal-only and adds nothing to a permitted binding's canonical material. This is
the same property R01 recorded as `material_sha256` unchanged for the matching case.

## 5. What an adopting reviewer should still check

1. That the guarded control integration preserves review ancestry and the exact +33/-0 diff.
2. That the adopted control records the exact accepted behaviour above, including the
   order-insensitive set semantics and the still-open duplicate insensitivity (R01 OBS_01).
3. That the EE14 T1 HOLD and the open HQ253 custody gap remain visibly open, not closed by
   adoption of this narrow grain.
