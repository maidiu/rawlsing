# PYAT HQ268 G01 — D1 owner-identity completeness and D2 canonical G2 replay identity — exact implementation and preserved G1 graph — R1

**STATUS:** HQ268_G01_RETURNED_FOR_HQ__NO_SELF_ADOPTION
**REPOSITORY:** `maidiu/rawlsing`
**BRANCH:** `agent/space-bunny-pyat-hq268-g01-d1-d2-auth-and-replay-identity-repair-r1`
**COMMISSION TIP (unmodified input):** `e64f53a70a5167a7c79712038c9b1e14ae6c747c`
**CODE SHA (final committed, all courts run here):** `46a95a8e62e3e790da3b84dfa7ab1ae4d5bce6bd`
**WORKTREE:** `/Users/matthewsmith/Desktop/Rawlsing/rawlsing-pyat-hq268-g01-r1`
**AGENT:** Existing Space Bunny / OpenCode source-free engineering author lane.
**MODEL / INTELLIGENCE (actual, not a label claim):** **MiMo V2.6-Flash, model id `opencode/mimo-v2.6-flash-free`.** This is NOT GPT-6 Sol High, NOT Sol, and not represented as anything else. Effort: full implementation plus re-verification of every court and a separately written cross-check script.
**TEST ENVIRONMENT (actual):** macOS 13.7.8 x86_64, CPython 3.11.3, pytest 9.1.1 at `/private/tmp/hq210venv/bin/python`. Existing qualified local checkout; no new machine or worktree provisioned by HQ.

---

## 0. Scope actually executed

Only the two authorized paths were edited, and only the four authorized return documents were added.

| Path | Action |
|---|---|
| `rawlsing_next/pre553_ee14_c1_owner_authenticated_ingress.py` | edited (D1, D2, R2) |
| `rawlsing_next/tests/test_pre553_ee14_c1_owner_authenticated_ingress_hq262.py` | edited (+21 tests, docstring) |
| `WORKER_RETURNS/PYAT-HQ268-G01-...-R1/{00,01,02,03}_*` | added (this directory) |

No other path was touched. `git diff --stat e64f53a70..46a95a8e6` reports exactly `2 files changed, 612 insertions(+), 24 deletions(-)`.

**Not done, deliberately:** no Library, no raw survey, no external source, no accepted-owner or fixture edit, no native F7/AT07, no V3, no deployment, no self-review, no self-adoption, no G1 PASS, no trust root, no T1/T2 claim.

---

## 1. D1 — owner-held expected C1 identity completeness

### 1.1 The defect, as fixed

Original `_authenticate` compared with

```python
mismatches = tuple(sorted(k for k, v in observed.items() if k in expected and expected[k] != v))
```

The `if k in expected` condition means **a key absent from `owner_identity[cell]` was never compared at all**. Owner setup could therefore pass `owner_identity={"q1": {}, "q2": {}}`, or a cell carrying only `raw_denominator_support`, and the ingress would still run the whole chain and issue a selected technical receipt. The commission is correct that no external data-only adversary can supply `owner_identity`: this was an **internal owner-setup completeness defect**, not a deployed-client exploit, and it is characterized that way everywhere below.

### 1.2 What was implemented

**A closed required set.** `REQUIRED_IDENTITY_KEYS` (ingress line 151) is a `frozenset` of exactly 19 keys — the complete set the ingress itself observes:

`composed_result_identity_hash`, `producer_predicate_key`, `producer_query_key`, `producer_fact_key`, `condition_binding_witness_key`, `consumer_query_key`, `risk_set_key`, `denominator_member_keys`, `raw_denominator_support`, `evidence_ref_key`, `source_universe_key`, `release_key`, `evidence_state`, `retained_conditioner_ids`, `evidence_authority_keys`, `evidence_provenance_keys`, `target_question_key`, `source_universe_key_owner`, `release_key_owner`.

Nothing in that set is optional. The set is closed: a key outside it is refused, not ignored.

**An exact type per key.** `IDENTITY_KEY_TYPES` (line 176) maps every one of the 19 to one builtin, checked with `type(v) is T` and never `isinstance`, so `bool` cannot satisfy `raw_denominator_support` and no subclass can satisfy a scalar field.

**One shared gate.** `_require_complete_identity(expected, cell)` (line 199) rejects, in order: a non-mapping expectation, a missing key, an extraneous key, and a wrong builtin type — each raising `SelectedIngressAuthenticationError` naming the exact offending keys.

**Enforced twice.**

1. **At owner construction** (`OwnerOnlySelectedIngress.__init__`, line 538): the expectation must be a mapping, must contain every permitted cell, and each cell must pass `_require_complete_identity` — all **before** the object is usable and therefore before any `serve()` can run.
2. **Again immediately before the comparison** (`_authenticate`, line 747): `_require_complete_identity(expected, req.cell)` runs right after the cell lookup and before the observed material is even built.

**The membership hole is gone.** The comparison now iterates the closed set:

```python
mismatches = tuple(sorted(k for k in REQUIRED_IDENTITY_KEYS if observed[k] != expected[k]))
```

There is no membership test on `expected`. A drift guard additionally pins the *observed* builder to the same closed set, so neither side can silently diverge:

```python
observed_missing = tuple(sorted(REQUIRED_IDENTITY_KEYS - set(observed)))
observed_extra   = tuple(sorted(set(observed) - REQUIRED_IDENTITY_KEYS))
if observed_missing or observed_extra: raise ...
```

**Error surface.** `SelectedIngressAuthenticationError` (line 281) gained `missing_keys: Tuple[str, ...] = ()`. `mismatched_fields` carries every required field that failed (absent or differing); `missing_keys` carries only the absent subset, so an incomplete setup is distinguishable from a complete expectation holding a different value. `f8_invoked` remains `False`.

**Placement in the chain.** `_authenticate` runs at step 3 of `serve()`, after the C1 producer and **before** `resolve_service_source_applicability`, `bind_service_applicability_to_f8_scope` and `evaluate_bound_positioned_subject_possibility`. The construction-time gate is earlier still. So incomplete material reaches **no applicability, no G2, no F8**.

### 1.3 Chain-order proof (measured, not asserted)

Independent cross-check `D1h`, with all four accepted owners instrumented, replacing the live expectation after construction:

```
compose=1  applicability=0  binder=0  evaluate=0
```

The C1 producer ran once (material existed to authenticate); every owner downstream of the completeness gate ran zero times. The G01 court's `chain_calls` fixture asserts the same independently (`test_d1_fails_closed_inside_authenticate_before_applicability_and_f8`).

### 1.4 The counterexamples the commission asked for

All in the authorized court, all at **zero F8 and zero applicability/binder/evaluate**:

| Required case | Test | Result |
|---|---|---|
| empty q1 | `test_d1_empty_owner_identity_is_refused_before_any_chain_owner` | refused, 19 keys missing |
| single-key q1 | `test_d1_single_key_owner_identity_is_refused` | refused, 18 missing, the present key not reported |
| missing provenance | `test_d1_missing_evidence_provenance_key_is_refused` | refused, `missing_keys == ("evidence_provenance_keys",)` |
| missing C1 identity | `test_d1_missing_composed_identity_key_is_refused` | refused, `missing_keys == ("composed_result_identity_hash",)` |
| partial q2/q1 | `test_d1_partially_populated_q2_identity_is_refused` | refused, exactly the 3 dropped keys named |
| extraneous key | `test_d1_extraneous_unknown_identity_key_is_refused` | refused, `mismatched_fields == ("attacker_supplied_key",)` |
| wrong builtin type | `test_d1_wrong_builtin_type_is_refused` | 4 sub-cases, each names exactly its field |
| **complete control** | `test_d1_complete_identity_positive_control_runs_the_whole_chain` | **accepted**, compose≥1, applicability=1, binder≥1, **evaluate=1 (F8 > 0)** |

Plus, for the belt-and-braces reading of "fail closed again before compare":

- `test_d1_fails_closed_inside_authenticate_before_applicability_and_f8` — live expectation replaced *after* construction; refused with the full 19-key missing set, `f8_invoked is False`, applicability=binder=evaluate=0, `f8_calls["n"] == 0`.
- `test_d1_authenticate_refuses_a_mismatched_complete_expectation` — a **complete but different** expectation is still caught (`release_key_owner`), at zero F8, with `missing_keys == ()`. Completeness is necessary, not sufficient.
- `test_d1_authenticate_has_no_membership_hole` — source-level: no conditional membership guard remains in `_authenticate`, the completeness call and the closed-set iteration are present, the drift guard is present, and the construction-time gate is wired.

### 1.5 What D1 deliberately does NOT do

It does not create an independent cryptographic trust root. The expected identity is still produced by re-executing the same owner compose over the owner-held fixture — an owner-controlled, source-free **development invariant**. That limitation is preserved explicitly (see return `02`) and is not papered over by the new completeness gate. Closing completeness makes authentication non-vacuous; it does not make it independent.

---

## 2. D2 — canonical complete accepted G2 receipt identity

### 2.1 The defect, as fixed

Original `_build_receipt` (old lines 690–702) built

```python
g2_receipt_hash = semantic_hash({ six chosen fields })
```

covering `service_request_set_identity`, `outcome`, `coverage`, `candidate_class_ref`, `service_id`, `decisions` — and omitting `receipt_id`, `no_applicable_source`, `candidate_class_binding`, `request_key`, `canonical_replay_only_order`, `authorised_authority`. Those six omitted fields did not discriminate the value at all, and `origin_receipt_hash` only transitively carried this truncated value, contradicting the exact G2 receipt/replay-binding claim.

### 2.2 What was implemented

`ingress.py` line 921, replacing the entire hand-built dict:

```python
g2_receipt_hash = receipt.replay_identity()
```

`receipt` is the object returned by the **accepted** `SA.resolve_service_source_applicability`, whose declared return type is `CandidateClassApplicabilityReceipt`, and `replay_identity()` is the accepted owner's own method (`pre553_service_source_applicability.py:631`), defined as `semantic_hash(self._material())`. **The ingress no longer derives anything about the receipt locally.** The `_material()` method returns the receipt's complete canonical material: `receipt_id`, `service_request_set_identity`, `service_id`, `candidate_class_ref`, `candidate_class_coverage`, `outcome`, `no_applicable_source`, `candidate_class_binding`, `request_key`, `decisions`, `authorised_authority`.

The technical field name `g2_receipt_hash` is retained **only because it now equals the accepted primitive exactly** — proven by `test_d2_g2_receipt_hash_equals_the_accepted_owner_replay_identity`, which asserts both `r.g2_receipt_hash == accepted.replay_identity()` and `r.g2_receipt_hash == SA.semantic_hash(accepted._material())`.

`origin_receipt_hash` still transitively includes it: `origin_material["g2_receipt_hash"] = g2_receipt_hash` (line 953).

### 2.3 The `canonical_replay_only_order` residual, and what was done about it

The commission lists `canonical_replay_only_order` among the omitted fields. It is one of the receipt's 12 dataclass fields — **but the accepted owner's own `_material()` does not include it**. So `replay_identity()` cannot carry it, and the D2 minimum ("keep `g2_receipt_hash` only if it now equals the exact `receipt.replay_identity()`") forbids adding it there.

Resolution: bound it **at the origin layer**, which the ingress owns:

```python
"g2_canonical_replay_only_order": list(receipt.canonical_replay_only_order),
```

(`ingress.py` line 957.) This is strictly additive, within the authorized file, and `origin_receipt_hash` is therefore sensitive to all six originally-omitted fields — five via `g2_receipt_hash`, one directly. No adopted owner was changed to achieve this. See return `02` for the residual this leaves against the read-only SA owner.

### 2.4 Discrimination tests (isolated record construction, never operative G0b authority)

| Field | Test | Result |
|---|---|---|
| `receipt_id` | `test_d2_replay_identity_discriminates_receipt_id_and_request_key` | changes `replay_identity()` |
| `request_key` | same | changes `replay_identity()` |
| `service_id` | same | changes `replay_identity()` |
| `no_applicable_source` | `test_d2_replay_identity_discriminates_no_applicable_source_and_binding` | changes `replay_identity()` |
| `candidate_class_binding` | same | changes `replay_identity()` |
| `authorised_authority` | `test_d2_authorised_authority_is_carried_by_the_replay_identity` | present in `_material()`; a differing value changes the hash. (The value itself cannot be varied — the accepted owner validates the exact ratified label in `__post_init__`.) |
| `canonical_replay_only_order` | `test_d2_origin_receipt_hash_binds_the_g2_replay_identity` | bound directly at the origin layer |

All of these use `dataclasses.replace` on a legitimately constructed receipt, or on a copied material dict — **isolated record construction, clearly labeled, never a forged operative authority**.

Negative source checks: `test_d2_no_local_six_field_subset_hash_remains` asserts the hand-rolled dict literal is gone and that `receipt.replay_identity()` appears exactly once in the module; `test_d2_origin_receipt_hash_binds_the_g2_replay_identity` asserts the origin layer carries both `g2_receipt_hash` and `g2_canonical_replay_only_order`.

End-to-end: `test_d2_receipt_identity_varies_with_the_applicability_construction` builds two ingresses differing only in applicability `binding_request_id` and shows the receipt material is shared while `origin_receipt_hash` differs — i.e. the origin layer really does carry the binding.

### 2.5 Preserved exactly

- exact source / release / permission: `test_d1_complete_identity_positive_control_runs_the_whole_chain` and the pre-existing F1/F2 receipt assertions still hold; `r.release_key == "REL-c1-at09-xor"`, `r.g2_permission_keys == (PERMISSION_REF.object_id,)`.
- technical `authorizing=False`: unchanged, still asserted by the pre-existing receipt test.
- no fake CURRENT: `g2_currentness` still taken from `g2_request.requested_currentness_claim` which is `None`; the pre-existing `test_f1_no_currentness_is_claimed` still passes.
- `SelectedRequest` remains data-only: pre-existing structural tests unchanged.

---

## 3. R2 — shallow container freezing, with the residual named

**Done (safe, tested, no original C1/G2 test broken).** In `__init__` (line 529):

```python
self._source = MappingProxyType(dict(source))
self._cells  = MappingProxyType({k: cells[k] for k in ALLOWED_CELLS})
```

`_owner_identity` remains deeply frozen by `_deep_freeze`, as before.

**Tests:**
- `test_r2_live_source_and_cells_containers_are_read_only` — item assignment, item deletion all raise `TypeError`; `_owner_identity` still deeply frozen.
- `test_r2_external_source_dict_mutation_does_not_reach_the_ingress` — mutating the dict handed in at construction no longer reaches the ingress; the served `release_key` is still the honest one.

**Prose corrected.** The blanket claims were narrowed to what is genuinely frozen:
- the module docstring gained an explicit **BOUNDED RESIDUAL (R2)** section stating that `_owner_identity`, `_source` and `_cells` are frozen and that the **nested objects inside `_source` are not**;
- the class docstring gained a matching `WHAT IS FROZEN` block;
- step 3 of the module's chain description now describes the completeness gate rather than implying all owner material is simply "non-mutable".

**Not done, deliberately:** no deep conversion of `source` objects. Their semantic refs are untouched; deep-converting them would change the ref objects the accepted C1/G2 owners consume, which the commission explicitly forbids. The residual — an in-process principal already holding a nested object can still mutate it — is retained as a precisely bounded trusted-harness limitation (return `02`).

---

## 4. The preserved G1 graph, point by point

| Claim | State after this correction | Evidence |
|---|---|---|
| **F1** source-free actual accepted C1 → SA → G2 binder → bound-F8 | unchanged; no scope-hash stand-in reintroduced | pre-existing F1 tests, all still pass |
| **F2** original same-respondent q1/q2 over ONE 4-respondent XOR source | unchanged | pre-existing F2 tests |
| **F2 figures** q1 C\|A=1 n2 (C0=1, C1=1); q2 C\|A=1,B=0 n1 (C0=0, C1=1) | unchanged, source free, same release | pre-existing frozen-figure tests |
| **F3** provenance substitution refused BEFORE F8 despite accepted F8 hash parity | unchanged | `test_f6_hostile_compose_cannot_reach_f8_with_forged_provenance` (F8 count 0) |
| **F3 + D1** authentication is also non-vacuous | **newly enforced** | §1.4 table |
| **F4** actual `ZERO_SUPPORT` native pre-F8 negative; separate `NO_ADMITTED_SOURCE` outcome | unchanged | pre-existing F4 tests |
| **F5** exact builtins | unchanged, now extended to the owner-held expectation's value types | `test_d1_wrong_builtin_type_is_refused` |
| **F6** real binder permission/source/release hostiles, positive non-vacuity | unchanged | pre-existing F6 tests |
| **D2** exact G2 receipt/replay binding | **newly enforced** | §2.4 table |
| **R2** frozen vs not-frozen is stated accurately | **newly enforced** | §3 |

---

## 5. Committed test run — final committed SHA `46a95a8e62e3e790da3b84dfa7ab1ae4d5bce6bd`

Worktree clean at run time (`git status --porcelain --untracked-files=no` empty). Interpreter `/private/tmp/hq210venv/bin/python` (CPython 3.11.3, pytest 9.1.1). Command form: `PYTHONPATH=. <python> -m pytest -q <files> -p no:cacheprovider`.

| # | Oracle | Files | Result | Exit |
|---|---|---|---|---|
| A | G01 court | `test_pre553_ee14_c1_owner_authenticated_ingress_hq262.py` | **96 passed** | 0 |
| B | four accepted G2/SA courts | `test_pre553_service_f8_source_scope_binding_court.py`, `test_pre553_service_f8_binding_authentication_court.py`, `test_pre553_service_f8_source_scope_binding_repair_court.py`, `test_pre553_service_source_applicability_court.py` | **199 passed** | 0 |
| C | C1/query/higher-order regression | `test_pre553_analytical_composition.py`, `test_pre553_empirical_query.py`, `test_pre553_analytical_composition_higher_order.py` | **80 passed** | 0 |
| D | A+B+C combined | all eight | **375 passed** | 0 |
| E | STEP A positive control | `/tmp/hq266/step_a_positive_control.py` | **ALL CHECKS PASSED** | 0 |

- **96 + 199 + 80 = 375** exactly.
- **Skips / xfails / errors in D: 0.**
- **Baseline preservation:** collected test ids at the commission tip vs the code SHA — **75 baseline ids at the tip, 96 at the code SHA, 0 missing, 21 new.**
- Commission's frozen regression obligations **75 / 199 / 80** remain satisfied (75 → 96 by addition only).

Additional author-side evidence (not a substitute for independent QA):
- separately written cross-check `/tmp/hq268/verify.py` at the code SHA: **49 PASS / 0 FAIL**, exit 0 — includes a reconstruction of the *pre-D2 six-key hash* proving it was blind to `receipt_id` while `replay_identity()` now discriminates it.

---

## 6. Blobs, hashes, and what did not move

**Blobs at code SHA `46a95a8e6`:**

| File | Input blob (commission tip) | Output blob |
|---|---|---|
| `rawlsing_next/pre553_ee14_c1_owner_authenticated_ingress.py` | `4ec0038d218a20cc92f114e28fd6c1de4ebd71f5` | `74e6ee826e8b6a2adebe84969fedcea5716d5b63` |
| `rawlsing_next/tests/test_pre553_ee14_c1_owner_authenticated_ingress_hq262.py` | `321e3e03415d1b980156f0ed4355216ca1f2273c` | `64b6c747f76a1909b676566e6b529ed10456d33b` |

**Adopted owners verified unchanged at the code SHA (commission pins in parentheses):**

| File | Blob |
|---|---|
| `rawlsing_next/pre553_analytical_composition.py` | `604c8d59…` (matches) |
| `rawlsing_next/source_backed_positioned_subject_possibility.py` | `62e5eced…` (matches) |
| `rawlsing_next/pre553_service_source_applicability.py` | `3e40caca…` (matches) |
| `rawlsing_next/pre553_service_f8_source_scope_binding.py` | `848d2d0e…` (matches) |
| `rawlsing_next/tests/c1_at08_at13_fixture.py` | `0393cc8c…` (matches) |

**Other refs untouched:** control `origin/integration/pre-main-reconciliation-r1` still `a12f619d8`; HQ266 branch still `bdc65ff89`; HQ267 branch still `2678a10d9`.

**Frozen external figures, re-confirmed unchanged:** universe content hash `318719f670e52a093a9a87ea92f3faf91555c7e1999b03dd47689964483f605c`, release `REL-c1-at09-xor`, q1 tag `hq253-qA` stratum `("c0",)`, q2 tag `hq253-qAB` stratum `("c0","c1")`. The AT09 `xor_fixture()` was not mutated.

---

## 7. Terminal

**STOP: `HQ268_G01_RETURNED_FOR_HQ__NO_SELF_ADOPTION`.**

This return is author evidence only. No G1 PASS, no adoption, no trust root, no T1 claim rests on it. A genuinely separate **GPT-6 Sol High** session, unconnected to this author and not having written or executed the author lane, must perform real independent hostile review before any G1 acceptance. Model label alone does not establish independence.
