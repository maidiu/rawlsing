# HQ261 R01 — Independent G3 committed lifecycle review

**TERMINAL: `HQ261_R01_RETURNED__NO_SELF_ADOPTION`**
**VERDICT: `ACCEPT_LOCAL_G3_COURT`**

Reviewer: Space Bunny / OpenCode, independent of the G03 author (DeepSeek harness).
No source, test or production mutation. No self-adoption.

## 1. What was actually reviewed

G03 return under review: `agent/deepseek-harness-pyat-hq260-g3-current-asof-lifecycle-court-r1
@ ccebccb677fd9d3079692e2a058666f790585ad1`.

G03 self-reported `head_at_run=35a8e2c0…`, i.e. **before** its own test file was committed.
Per the commission I therefore did **not** trust that report. I ran everything in a separate
clean worktree checked out at the **final committed SHA** `ccebccb6…`:

- verification worktree HEAD = `ccebccb677fd9d3079692e2a058666f790585ad1`
- G03 test blob = `a1ec3dba504ff866b681d6bbe942d12a9e238257` — matches the commission exactly
- working tree clean at checkout; the only subsequent entries were `__pycache__` (inert)

## 2. Changed-terrain verification

`git diff 788b2bf7… ccebccb6… -- rawlsing_next/` = **one file, 460 insertions**, the test
file. **No production module was changed**, matching G03's claim.

Owner code blobs at G03's final SHA vs the accepted HQ260 base `788b2bf7…` — **all IDENTICAL**:

| owner module | blob |
|---|---|
| `pre553_learned_product_lifecycle.py` | `a11c9eb73aba` |
| `pre553_analytical_replay_dependency.py` | `47e65aad5e0a` |
| `pre553_analytical_composition.py` | `604c8d591d4c` |
| `pre553_authority_maintenance.py` | `547e6bf20354` |
| `pre553_empirical_objects.py` | `a61365b994e5` |

## 3. Independent execution — all four courts, actual results

Governed CPython 3.11.3, sha256 `11d6f541a870a141249ce98d45834a6789e29c07031e85ce17f3e67f24c535f6`.

| court | file | result | exit |
|---|---|---|---|
| 15 new lifecycle | `test_pre553_ee14_selected_current_asof_hq260.py` | **15 passed** | 0 |
| 39 accepted B5 lifecycle owner | `test_pre553_learned_product_lifecycle.py` | **39 passed** | 0 |
| 43 analytical-dependency | `test_pre553_analytical_replay_dependency.py` | **43 passed** | 0 |
| combined 97 | all three | **97 passed** | 0 |

97 = 15 + 39 + 43 exactly. G03's count is confirmed independently on clean committed source.

## 4. Attack coverage

All eight commissioned attack classes map to real tests:

| commissioned attack | covering test |
|---|---|
| forged selection receipt | `g3_self_proclaimed_current_receipt_is_refused` |
| replacement release outside selected purpose | `g3_second_purpose_or_scope_cannot_inherit_currentness`, `g3_currentness_is_not_readable_off_a_release_object_or_cache` |
| tampered checkpoint | `g3_tampered_checkpoint_is_refused` |
| affected / unaffected invalidation | `g3_affected_and_unaffected_dependency_transition`, `g3_invalidated_release_cannot_be_served_as_current` |
| stale product reselected | `g3_staged_but_unselected_release_is_unknown_not_current` |
| historical as-of event vs fresh-process checkpoint | `g3_as_of_event_and_as_of_checkpoint_agree`, `g3_historical_as_of_still_resolves_the_prior_product`, `g3_fresh_process_checkpoint_reconstruction` |
| UNKNOWN_CURRENTNESS under unselected or foreign key | `g3_unknown_selection_key_is_refused_not_guessed`, `g3_owner_unknown_analytical_dependent_is_never_current` |

Plus two honesty guards: `g3_no_new_adapter_module_was_manufactured` and
`g3_court_claims_no_service_or_model_use_permission`.

`g3_fresh_process_checkpoint_reconstruction` genuinely uses `subprocess.run` (test file
line 284), so fresh-process replay is a real separate interpreter, not an in-process
simulation.

## 5. Non-vacuity

- The court imports **real owner modules** (`pre553_learned_product_lifecycle`,
  `pre553_analytical_replay_dependency`, `pre553_authority_maintenance`,
  `pre553_empirical_objects`) — no test-local reimplementation of the behaviour under test.
- 15 tests carry 32 assertions.
- **Honest limitation of my own probe:** I disabled the owner's `declare_no_current` and the
  court went RED — but via a **collection error**, not graded assertion failures. That proves
  dependency, and is **not** a sensitivity proof. I did not achieve a clean behavioural red,
  and I do not claim one.

## 6. Stage-grade vs service-specific

These are **stage-grade local owner capability** tests over source-free material. None of
them exercises a real service join, a real model, T1 or T2 service use, or any adopted
permission. G03's own return states this and its two honesty-guard tests enforce it. No test
here is expected to fail merely because a later service join arrives; equally, none of them
would *detect* a service-join fault, because service-specific behaviour is out of their scope.

## 7. Verdict

`ACCEPT_LOCAL_G3_COURT`. The 97-case combined court reproduces independently on clean committed
source at the exact final SHA, no owner code changed from the accepted HQ260 base, and the new
test file is a genuine non-vacuous additive assertion over real owner code.

HQ may import **only this new court** into canonical control. **Local positive stage
capability only** — this is not a T1 grant, not T2 service use, and not model-use authority.

## 8. What remains at T1

Unchanged by this review: G1 producer-origin trust boundary (from HQ260 G01, which returned
`BLOCKED_REQUIRE_TRUST_ROOT`), G0b, EE14 model-use grant, FF02 positive relation, EE12 pair
authority, and any T2 service join. None is advanced, implied or granted here.
