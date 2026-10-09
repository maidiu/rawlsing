# HQ255 R01 — independent hostile review of the frozen P01 permission-identity candidate

**VERDICT: `REPAIR_NARROW`** — the production correction is correct, minimal and fail-closed at
its exact grain, but the candidate **as committed cannot be certified green by its own court**:
one test asserts the *committed* binder blob equals the pre-candidate baseline and therefore
fails on the committed candidate.

**Branch:** `agent/deepseek-harness-pyat-hq255-p01-permission-candidate-independent-review-r1`
**Reviewer tip:** `d44678d49ae81da423c5c91c53db3ec7e31a3ccf` (live-origin verified)
**Frozen candidate:** `23438ab52f16abda5960a075dfca3f4d3396eab5` (first parent `428be759…`)
**Reviewed blobs:** binder `848d2d0e…` (baseline `4ba00b8e…`), new court `test_pre553_f8_receipt_permission_identity_hq254.py`
**Runtime:** governed CPython 3.11.3 (sha256 `11d6f541…`), pytest 9.1.1, macOS 13.7.8 x86_64
**Mode:** read-only independent review; no production/source/test edit; no adoption.

## 1. Live control resolution

`integration/pre-main-reconciliation-r1` = `ce8467e833e537719d62e8f3db909bbafda907f1`.
Sealed HQ255 checkpoint `20261008-PYAT-HQ255-FIVE-HQ254-RETURNS-DEEPSEEK-P01-AND-EE14-T1-R1`
(handoff `f5ed4e614545e2365002f080e32b73d153369072`, ancestor of live control) carries the exact
worker row: branch = this branch, `commission_tip = d44678d4…`, `parent_sha = 23438ab5…`,
`sparse = SPARSE_REQUIRED__EXACT_01_MANIFEST`. The P01 lane is recorded
`SOURCE_PLUS_TEST_CANDIDATE_QUARANTINED__POST_CANDIDATE_REVIEW_REQUIRED`. HQ255 **is** sealed;
no branch-local snapshot was used to decide otherwise.

## 2. Candidate lineage — exact

`git diff --name-status 428be759 23438ab5` is exactly the candidate binder (M), the new court (A)
and four author return files (A). Binder blob at the candidate is `848d2d0e…`; at the parent it is
`4ba00b8e…`. Nothing else changed. `BINDING_PERMISSION_IDENTITY_MISMATCH` occurs **0** times in
the baseline binder blob — it is genuinely new candidate vocabulary.

## 3. What I independently ran (governed runtime, sparse worktree)

| Run | Result |
|---|---|
| 4 adopted baseline courts (3 F8 + applicability) | **199 passed, exit 0** — matches the author exactly |
| new P01 court on the **committed** candidate | **15 passed, 1 failed, exit 1** |
| combined | **214 passed, 1 failed, exit 1** |
| negative control: new court vs baseline binder (`4ba00b8e`, `/tmp` copy) | **10 failed, 6 passed** — 9 genuine discriminators + 1 no-git artifact |
| matching-case material vs baseline binder | **byte-identical** (`material_sha256 74fc3ffa…`) |

## 4. The one defect — a commit-state-coupled test (REPAIR_NARROW)

`test_adopted_binder_baseline_was_the_unmodified_owner` runs
`git rev-parse HEAD:rawlsing_next/pre553_service_f8_source_scope_binding.py` and asserts it equals
the baseline constant `4ba00b8e…`. On the committed candidate that value is `848d2d0e…`, so the
assertion fails. It can only pass while the candidate edit is **uncommitted** (HEAD at the
baseline, working tree modified) — which is how the author's reported `16 passed` was produced.
On the committed candidate the court is `15/16`, and there is no commit SHA of this candidate on
which the court is fully green.

Smallest correction (no behaviour change): compare against the parent/base commit
(`git rev-parse f"{COMMISSION_BASE}:{path}"`) or against a documented constant compared to the
*parent* blob, or drop the git-state coupling and assert the recorded baseline constant without
consulting HEAD.

## 5. Substantive assessment of the production guard — sound at its exact grain

- **Positive/backward compatibility**: matching single and multiple permission sets still bind;
  for a matching two-permission binding the candidate's `material()` and replay identities are
  **byte-identical** to the baseline binder. The guard is a pure no-op on honest inputs.
- **Discrimination**: unrelated, superset, subset, partial substitution, and
  **same `object_id` with changed SHA** are all refused with the new named code, because
  `ExactRef.key` includes `content_hash`.
- **Fail-closed placement**: the refusal fires before any binding object/material exists; the
  request object is not mutated.
- **Refusal precedence**: `BINDING_TARGET_USE_GRAIN_MISMATCH` still outranks the new check;
  the new check precedes `BINDING_RELEASE_GRAIN_MISMATCH` for multi-grain dishonest requests
  (explicitly disclosed by the author and observed by me); the release refusal is unchanged when
  permissions agree. Existing single-grain codes are preserved.
- **No widening**: it grants no permission, adds no authority/model use/custody, and the fixed
  `forbidden_binding_purposes` and `grants_no_authority` material are unchanged.

## 6. Independently discovered semantic observations (not blockers)

1. **Set equality is also duplicate-insensitive.** A binding declaring `[A, A]` against a receipt
   holding `[A]` binds, and the duplicate is copied into the canonical material. The receipt's own
   refs are deduped+sorted upstream (`_ref_list`), so the receipt can never carry a duplicate; only
   the binding side can. Benign, but the author's disclosure mentions only ordering.
2. **Order is not preserved between the two sides.** `receipt [A,B]` vs `binding [B,A]` binds and
   the material records the binding's order. No in-repo consumer of
   `bound_target_use_permission_refs` requires order or subset semantics — the only readers are
   the binder itself and its courts — so order-insensitivity is safe today.
3. **Malformed receipt key escapes the binder's typed refusal surface.** If the receipt's
   `request_key["target_use_permission_refs"]` were a malformed mapping, `exact_ref(...)` raises
   plain `Pre553IntegrityError`, not the binder's `ServiceF8ScopeBindingError` subclass. Not
   reachable through the genuine applicability owner (the request builds only exact refs and
   refuses an empty set upstream with `TARGET_USE_PERMISSION_BOUND_REFS_REQUIRED`), so it is a
   defensive-surface note only.
4. Empty permission sets are refused **upstream** by the request's own
   `TARGET_USE_PERMISSION_BOUND_REFS_REQUIRED`, so the new check never sees an empty/empty case.

## 7. Provenance gap preserved (not this lane's to close)

This correction is a binding↔receipt *coherence* check. It does not establish the receipt's own
provenance/authority custody (HQ253 T01 G1/C1) and is not an EE14 use grant, an F8 producer
custody demand, a T1 permission, or F7/native authority. `F7_RR04G` and the T1 trust gap remain
open and untouched.

## 8. Terrain and ceiling

Sparse manifest materialized exactly; a **documented narrow, source-free extension** was required
to run anything at all and is listed in `01_ACTUAL_TEST_LOGS_AND_TERRAIN.json`
(the binder's own import closure plus the pre-existing `c1_at08_at13_fixture` and the three
pinned adopted-owner files the courts' byte-identity guards demand). No raw `.sav`/`.dta`,
Library, issuer or native runtime was touched. All totals below are exact local runs with exit
codes; none are certified by HQ.

**Terminal:** `HQ255_R01_RETURNED_FOR_HQ_INTAKE__NOT_ADOPTED`.
