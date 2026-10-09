# HQ270 R02 — G1 frozen-SHA runtime, interpreter and test reproduction

**Return:** `WORKER_RETURNS/PYAT-HQ270-R02-G1-INDEPENDENT-QUALIFIED-RUNTIME-AND-SA-ORDER-COURT-R1/`
**Commission:** `WORKER_COMMISSIONS/PYAT-HQ270-R02-G1-INDEPENDENT-QUALIFIED-RUNTIME-AND-SA-ORDER-COURT-R1/00_COMMISSION.md`
**Reviewer:** genuinely separate independent runtime hostile reviewer. **Not** the MiMo
HQ266/HQ267/HQ268 author session, and not the HQ269 static-only reviewer.
**Marker:** `TEST_ONLY_UNISSUED__NOT_AN_EE14_GRANT__G1_INTERNAL_OWNER_PATH_CANDIDATE_ONLY`
**Executed:** 2026-10-09 (UTC), commission tip `069905cdb7d228d16b6de47b8ecc8c0090c207cd`.

---

## 1. Frozen candidate pin

| Item | Value | How verified |
|---|---|---|
| Candidate code commit | `46a95a8e62e3e790da3b84dfa7ab1ae4d5bce6bd` | `git cat-file -t` = `commit`; detached worktree `HEAD` = this SHA |
| Author return | `f10523e1584086f38a640505e9a54155f3aef9a0` | present |
| Ingress module blob | `74e6ee826e8b6a2adebe84969fedcea5716d5b63` | `git rev-parse 46a95a8e:rawlsing_next/pre553_ee14_c1_owner_authenticated_ingress.py` |
| G01 test blob | `64b6c747f76a1909b676566e6b529ed10456d33b` | `git rev-parse 46a95a8e:rawlsing_next/tests/test_pre553_ee14_c1_owner_authenticated_ingress_hq262.py` |
| Accepted SA owner blob | `3e40caca29e8c96ee1f412f919cfc7dba63f96c4` | `git rev-parse 46a95a8e:rawlsing_next/pre553_service_source_applicability.py` |
| Accepted G2 binder blob | `848d2d0eedb04b792747e9d6aaa49bb39d108a2c` | present at candidate |
| Analytical composition blob | `604c8d591d4cc2b646e9b149cdb233fc9d69cf6b` | present at candidate |
| Commission base | `e64f53a70a5167a7c79712038c9b1e14ae6c747c` (input blobs `4ec0038d…` / `321e3e03…`) | used only for the baseline-75 collect |

**Worktree hygiene.** The candidate was pinned in a *new detached worktree*. The author's
own worktree was never opened for modification. After every execution
`git status --porcelain` on the pinned worktree returned **0 lines** (`__pycache__`
directories were removed and `PYTHONDONTWRITEBYTECODE=1` used throughout). No
production file, test file, HQ file, checkpoint or accepted-owner file was touched.

**No survey sources.** No raw SAV/DTA, no LITS, no Library, no population computation, no
mass survey fetch. The only empirical object used is the committed four-respondent XOR
test fixture.

---

## 2. Runtime, interpreter and dependencies (declared, not repaired)

| Component | Observed |
|---|---|
| OS | macOS 13.2.1, build 22D68 (`Darwin 22.3.0`), `x86_64` |
| Interpreter | CPython **3.11.3** (`v3.11.3:f3909b8bc8, Apr 4 2023`), Clang 13.0.0, `/usr/local/bin/python3` |
| Test runner | pytest **9.0.2** |
| Numeric stack | numpy 2.3.2, pandas 2.3.1 |

**Declared divergence from the author's environment.** The author's declared venv
`/private/tmp/hq210venv` (pytest 9.1.1, macOS 13.7.8) **no longer exists on this
machine**. Nothing was reinstalled, no package was copied, and no interpreter was
manufactured to make the run look comparable. The divergence is declared rather than
repaired. The author's `/tmp/hq266/step_a_positive_control.py` is likewise gone; the
STEP A positive control used here was re-authored from scratch (§5).

**Command form.** Every pytest invocation below is, from the pinned worktree root:

```
PYTHONPATH=. python3 -m pytest -q <files> -p no:cacheprovider
```

---

## 3. Committed-court reproduction (the author's acceptance surface)

Courts are the four groups the commission names. The group composition was derived
independently from module contents and then cross-checked against the author's own
return.

### Court A — G01 owner-only C1 → G2 → F8 ingress

* `rawlsing_next/tests/test_pre553_ee14_c1_owner_authenticated_ingress_hq262.py`
* collected **96**, passed **96**, skipped/xfail/error **0**, `pytest` exit **0**, 2.14 s

### Court B — accepted SA / G2, four groups

* `test_pre553_service_source_applicability_court.py` — 60
* `test_pre553_service_f8_source_scope_binding_court.py` — 73
* `test_pre553_service_f8_source_scope_binding_repair_court.py` — 41
* `test_pre553_service_f8_binding_authentication_court.py` — 25
* collected **199**, passed **199**, skipped/xfail/error **0**, exit **0**, 1.33 s

### Court C — C1 / analytical composition / query

* `test_pre553_analytical_composition.py` — 13
* `test_pre553_analytical_composition_higher_order.py` — 35
* `test_pre553_empirical_query.py` — 32
* collected **80**, passed **80**, skipped/xfail/error **0**, exit **0**, 9.02 s

### Court D — combined

* A + B + C: collected **375**, passed **375**, skipped/xfail/error **0**, exit **0**, 12.07 s

The numerical match to the author's `96 + 199 + 80 = 375` is recorded as a **cross-check
only**. The court design below is independent of it.

**Author acceptance test names.** All 96 G01 node ids and all 279 SA/G2/C1 node ids were
collected verbatim by pytest from the pinned blobs; none was renamed, skipped or
xfail-marked.

---

## 4. Baseline-75 integrity

| Measure | Value |
|---|---|
| Collect at commission base `e64f53a7` (pre-correction G01) | **75** |
| Collect at candidate `46a95a8e` (G01) | **96** |
| Baseline ids missing from the final collect (`comm -23`) | **0** |
| New ids present (`comm -13`) | **21** |

The 21 new (correction) test names, exactly as pytest collected them:

```
test_d1_authenticate_has_no_membership_hole
test_d1_authenticate_refuses_a_mismatched_complete_expectation
test_d1_complete_identity_positive_control_runs_the_whole_chain
test_d1_empty_owner_identity_is_refused_before_any_chain_owner
test_d1_extraneous_unknown_identity_key_is_refused
test_d1_fails_closed_inside_authenticate_before_applicability_and_f8
test_d1_missing_composed_identity_key_is_refused
test_d1_missing_evidence_provenance_key_is_refused
test_d1_partially_populated_q2_identity_is_refused
test_d1_required_key_set_is_closed_exact_and_typed
test_d1_single_key_owner_identity_is_refused
test_d1_wrong_builtin_type_is_refused
test_d2_authorised_authority_is_carried_by_the_replay_identity
test_d2_g2_receipt_hash_equals_the_accepted_owner_replay_identity
test_d2_no_local_six_field_subset_hash_remains
test_d2_origin_receipt_hash_binds_the_g2_replay_identity
test_d2_receipt_identity_varies_with_the_applicability_construction
test_d2_replay_identity_discriminates_no_applicable_source_and_binding
test_d2_replay_identity_discriminates_receipt_id_and_request_key
test_r2_external_source_dict_mutation_does_not_reach_the_ingress
test_r2_live_source_and_cells_containers_are_read_only
```

**Grade: MEASURED** (executed, not asserted from a declaration).

---

## 5. Independent STEP A positive control

The author's `/tmp/hq266/step_a_positive_control.py` is absent. A replacement was
re-authored for this commission and run against the pinned candidate.

**49 / 49 checks passed, exit 0.** It does not import any author-side test helper for its
assertions. In particular it **re-derives the four-respondent XOR oracle from its own row
table** (`R{a}{b}` for `a,b ∈ {0,1}`, `C = A ⊕ B`) and then confirms that the committed
fixture's denominators equal the independently counted `A=1` (2) and `A=1 ∧ B=0` (1)
respondents, before asserting the q1 `1/2, 1/2` and q2 `0/1, 1/1` figures through the
public `serve` surface.

Also measured in STEP A: the pinned predicate-grammar query authority
(`I03-AUTH-c1-at09-xor` and its content hash), the hard-forbidden snapshot substitute
`C1-AT07-QUERY` refused at owner construction, release `REL-c1-at09-xor`, universe
content hash `318719f6…f605c`, a real G2 receipt (`ADMISSIBLE_SOURCE_INDEXED_SET`) whose
`g2_receipt_hash` equals the accepted owner's `replay_identity()`, full-chain counters
(compose 1 / applicability 1 / binder ≥1 / evaluate 1), bound-F8 ⇔ direct-C1 parity,
deep read-only owner material, and grain substitution refused at zero F8.

---

## 6. Independent hostile harness (new code, deliberately not committed)

Five files were written from the **contract text** of the two candidate modules, not from
the committed G01 test bodies. They live outside the repository; only digests are
recorded here, so the return contains exactly the four documents the commission allows.

| File | sha256 |
|---|---|
| `harness.py` | `3111cc15de330208514341722fb36d9802812bc8d7c6e986f3c634c3272484cc` |
| `step_a_positive_control.py` | `ee0aa9002546f24a1fa1e7cf281b8755f2f286308580fe9f8a0373cb43a7e3a6` |
| `d1_hostile.py` | `17984eecc19e2d76039fea7a06d10d773aa13b76447a5dff67b08e0945506bb0` |
| `d2_hostile.py` | `4111544b527681e12cea8907d515d39aa285ea04a570c42198cc016209f6b06c` |
| `f_hostile.py` | `4b6103b9a9e41431ddd5fbd62c91d67b62133934fbdb125fdc238cb4aff92db3` |

What is shared with the committed courts, and what is not:

* **Shared fixture *data* only:** `fx.xor_fixture()`, `fx.direct_condition_composition()`,
  `fx.make_model_rule()`, `_query_authority("c1-at09-xor")`, `_registry()`, and the frozen
  XOR condition lists. These are the construction the commission fixes as the positive
  control.
* **Re-derived by this reviewer:** every urn, tag, permission/class/universe ref,
  `binding_request_id`, `ApplicabilityMaterial`, owner-expected-identity map (under an
  `HQ270R02` namespace), the XOR oracle row table, and every tamper, bomb, mutation and
  invocation counter.

Results (all four scripts, exit 0, `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. python3 …`):

| Court | Checks | Passed | Failed |
|---|---|---|---|
| STEP A independent positive control | 49 | 49 | 0 |
| D1 independent owner-identity hostile | 81 | 81 | 0 |
| D2 independent replay-identity / order | 41 | 41 | 0 |
| F1–F6 independent reproduction | 49 | 49 | 0 |
| **Total** | **220** | **220** | **0** |

Full per-case results: `01_INDEPENDENT_D1_D2_HOSTILE_EXECUTION.json`.

---

## 7. Grades, precisely separated

**MEASURED** (executed here, on this machine, against the pinned blobs):

* Courts A/B/C/D = 96 / 199 / 80 / 375, all `pytest` exit 0, zero skips, xfails or errors.
* Baseline-75 integrity = 0 missing, 21 new.
* STEP A = 49/49. D1 = 81/81 (28 distinct refusal events). D2 = 41/41. F1–F6 = 49/49.

**SOURCE_STATIC** (read from the pinned blobs, not executed):

* The accepted SA order law (`ORDERING_SEMANTICS`, `_sorted_replay_only`, the single
  `object.__setattr__` assignment at line 804, the 11-key `_material()`).
* The ingress origin binding (lines 952–957 and 1007) and `g2_receipt_hash =
  receipt.replay_identity()` (line 921).
* The static claim that no production module mints a
  `CandidateClassApplicabilityReceipt` outside the SA resolver.

Nothing in this return is graded as anything other than MEASURED or SOURCE_STATIC. No
claim is made that this is deployed security, an EE14 grant, a trust root, or survey-source
validation.
