# 00 — HQ211 H-D/F8 SOURCE-SCOPE BINDING — independent hostile review — R1

**Role:** independent hostile reviewer. No implementation. No repair. No merge. No self-adoption.
**Branch:** `agent/reviewer-pyat-hq211-hd-f8-binding-r1`
**Review tip:** `b26dcf2e67407b1e42b1d08bd36d0338e9fd91e5` (verified equal to `origin/agent/reviewer-pyat-hq211-hd-f8-binding-r1` before work)
**Commissioned startup base:** `b722f2e7373ad833d5f63833b1d6fe426d3dc55d` (ancestor of the review tip; the tip is the review-setup commission commit)
**Candidate:** `agent/rabochii-pyat-hq210-hd-f8-binding-r1 @ 8d352f7d80983cbf49e7e57511f8cf6d5b80966d`
**Parent H-D contract return:** `6e2649c4d111fd0ec176c9fa29ce1da27ccc448e`
**Service-source owner fan-in:** `3eda3eb598cf9fe6b14df60323af52ae446b21fa`

## DISPOSITION

`HD_F8_BINDING_PARTIAL__BOUNDED_REPAIR_REQUIRED`

The seam is **real and it closes the exact HQ208 gap**. It acquires **no** selection, ranking, pooling, currentness, permission, geometry, distribution or actor power. The three adopted owners are **byte-identical**, the positive F8 core evaluates **unchanged**, and the claimed 148/148 court surface **reproduces exactly** (I ran it). Nothing here is authority overreach and nothing conflicts with adopted law.

But three of the candidate's own claims are not true of its own machinery, and one of them is semantic rather than cosmetic:

1. **`SINGLE_SOURCE_VALIDATION` does not constrain what may be evaluated.** Its `requested_source_universe_ref` is carried in the material and in the replay identity, but `evaluate_bound_positioned_subject_possibility` validates the **query's** source against the whole admitted set, so a single-source binding made for source A evaluates source B and returns a result. The two declared modes differ only in whether set exposure is gated.
2. **"The two positive powers, and only two" is false as an API statement.** The module's declared public surface has **four** returning functions, not two.
3. **The off-release provenance branch is dead code.** The adopted owner stamps *every* decision with the request's release, so the `bound_to_requested_release: False` positive rows the binder can emit can never occur.

All three are bounded repairs. Details and evidence follow.

## 1. What was actually run and verified

Environment: independent venv (`/tmp/hq210venv`), CPython 3.11.3 (same version the candidate declares), pytest 9.1.1, read-only imports of the candidate module from a worktree at the exact candidate SHA. Probe scripts written outside the repository.

### 1.1 Change set — verified

`git diff --stat b722f2e73 8d352f7d8` is the two new files plus handoff/pointer and return-artifact churn:

```
rawlsing_next/pre553_service_f8_source_scope_binding.py                      | 823 ++ (new)
rawlsing_next/tests/test_pre553_service_f8_source_scope_binding_court.py     | 794 ++ (new)
WORKER_COMMISSIONS/PYAT-HQ210-HD-F8-SOURCE-SCOPE-BINDING-R1/00_COMMISSION.md | 143 ++
WORKER_RETURNS/PYAT-HQ210-HD-F8-SOURCE-SCOPE-BINDING-R1/00_RETURN.md ... 05  | 751 ++
HQ_HANDOFF/*                                                                 | pointer moves
```

**No production module other than the new binder was modified.** The two new files are the whole authored change.

### 1.2 Owner-boundary integrity — verified byte-identical

Run at the candidate SHA and again at the review commit; identical both times:

| Adopted owner | blob at candidate | blob at base `b722f2e73` | candidate's claim |
|---|---|---|---|
| `rawlsing_next/pre553_service_source_applicability.py` | `3e40caca29e8c96ee1f412f919cfc7dba63f96c4` | identical | `3e40caca…` ✓ |
| `rawlsing_next/source_backed_positioned_subject_possibility.py` | `62e5eced47b64512f47b004e3e13a6ef3fe21de7` | identical | `62e5eced…` ✓ |
| `rawlsing_next/objective_consumer_bounded_evidence.py` | `f30fca20e7b56e00348e82765d95f974b4b6a195` | identical | `f30fca20…` ✓ |

The court's own write-terrain guard runs on `git hash-object` and I reproduced all three hashes independently; the guard is **not** silently skipping in this environment. I also verified the court's repo-root arithmetic is now correct: `Path(__file__).resolve().parents[1]` resolves to the worktree root, so `repo / rel` finds the real files (the worker's recorded defect #4 was a genuine near-miss with `parents[2]`).

### 1.3 Court surface — independently reproduced

| Suite | Candidate claim | Independently observed |
|---|---|---|
| `test_pre553_service_f8_source_scope_binding_court.py` | 72 | **72 passed, 0 skipped** |
| `test_pre553_service_source_applicability_court.py` | 60 | **60 passed** |
| `test_source_backed_positioned_subject_possibility.py` | 13 | **13 passed** |
| `test_a05_z08_positioned_admission.py` | 3 | **3 passed** |
| **aggregate** | **148** | **148 passed** |

I also ran all four suites in one invocation: `148 passed in 1.95s`. The breakdown matches the candidate's claim exactly, including the `0 skipped` line.

## 2. Attack A — selection / ranking leakage: **NO LEAKAGE FOUND**

I attacked this four ways rather than restating the candidate.

**A1 — permutation invariance, independently.** I bound the same 3-member class with all six permutations of the candidate-class member list *and* with the authority records in reverse order, and collected both the binding replay identity and the exposed admitted order:

```
distinct replay identities: 1
distinct exposed orders:     1
permutation invariance:      HELD
```

Neither the binding identity nor the exposed set order consumes input order. Note the admitted tuple is built through the adopted owner's `_ref_list` (canonical-JSON sorted), so the canonical order is the *owner's*, and the binder adds none.

**A2 — exhaustive classification of every public bound callable.** I called every non-underscore callable on the binding and recorded return vs raise:

```
raising = assert_binding_does_not_authorize, assert_query_source_admitted (arity — see below),
          conditioned_f8_geometry, currentness_authority, first_admitted_source,
          grant_target_use_permission, infer_individual_state, pooled_source_set, ranked_sources
```

Seven selection/permission-shaped methods raise. `assert_query_source_admitted` appears in the "raising" bucket only because my probe called it with no argument; it returns normally when given a query (court tests 1, 490, 498 and my own probes all confirm). **No method returns a chosen, ranked, scored, weighted or preferred source.**

**A3 — lower-level API bypass.** `admitted_source_universe_refs` is a plain `tuple`; there is no accessor, cursor, `.first()`, `.best()` or sorted-key view on the binding. The receipt is reachable only through the caller's own `receipt` object, and the adopted owner exposes `admissible_source_universe_refs()` as a set-like tuple with `ORDERING_SEMANTICS` pinned to replay-only — an owner property, not a new one introduced here.

**A4 — value inspection of emitted material.** Recursively walking `binding.material()` for ranking-shaped leaves, and checking for aggregate/sample-size/actor fields, found none:

```
permission_refs_are_grants: false
currentness_default:       CURRENTNESS_NOT_REQUESTED
has_aggregate_field:       false
has_actor_field:           false
```

**Verdict: no third selection-shaped power is reachable.**

## 3. Attack B — COMPLETE / INCOMPLETE coverage: **HARDENING HELD**

This is where the candidate claims to have gone beyond the literal text, and it does.

| Probe | Result |
|---|---|
| B1 exhaustive bind over an INCOMPLETE receipt | refused `APPLICABILITY_COVERAGE_INCOMPLETE` |
| B1 single-source bind over the same INCOMPLETE receipt | **allowed** |
| B1 power 1 (validate the known-admitted source) under INCOMPLETE | returns `admitted: true` |
| B1 **power 2 (set exposure) under that same single-source binding** | refused `APPLICABILITY_COVERAGE_INCOMPLETE` |

The laundering attempt the candidate names — bind a *single-source* binding over an INCOMPLETE class, then read back the partial set as if it were the admissible set — **is refused**, because `expose_unranked_admitted_source_set` re-checks coverage on every call rather than trusting the bind-time mode. The narrow capability survives exactly as claimed: one known-admitted source can still be validated under INCOMPLETE.

Grain mismatch refusals all fire and are exercised by the court (request/receipt, service, candidate class, release, target use). `NO_ADMITTED_SOURCE_IN_CANDIDATE_CLASS` is first-class and only reachable under COMPLETE coverage, which is enforced twice — in the adopted owner's `__post_init__` and again in the binder's `not admitted and not receipt.no_applicable_source` check.

**Verdict: no partial class can be laundered as exhaustive.**

## 4. Attack C — F8 non-transformation: **NO TRANSFORMATION, ONE MISLEADING GUARD**

**C1 — direct before/after comparison on the same exact evidence.** I built a wide binding (A and B admitted, rule spans A,B) and a narrowed binding (A admitted, B not, rule spans A only), and evaluated the *same* query object and the *same* evidence object through both:

```
geometry byte-equal (wide == narrow == original)  True
conditioner ids                                    ("country","education") unchanged
rule hash at result == caller's rule hash          True
query object identity preserved (out.query_ref == q.ref)  True
result states                                       EXACT_SUPPORTED / EXACT_SUPPORTED
```

Narrowing eligibility changed **which** pre-materialized slice F8 could select; it changed no geometry, no conditioner set and no algorithm identity. `ELIGIBILITY_NARROWING != POSSIBILITY_GEOMETRY_TRANSFORMATION` holds operationally, not only as a declared law.

**C2 — law-drift guard.** Presenting a *different* F8 rule at evaluation is refused `BINDING_RULE_REPLAY_MISMATCH`; the binding never re-points the rule. The guard compares `rule_hash`, so a changed source set, a changed walkback ladder or a changed authority produces a different hash and refuses. I could not construct a same-hash-different-material rule (`same_sources_same_hash: true` for genuinely identical rules). The `_require_f8_rule` algorithm-id and model-rule-id checks add defence in depth.

**C3 — conditioner escape route.** A query whose conditioner names a *different* source than the query cannot even be constructed — the adopted F8 query owner refuses `conditioner source/release mismatch; no implicit bridge`. So the one plausible route by which a non-admitted source could influence F8 is closed upstream of the binder, by the owner, not by the binder. Worth recording because the binder explicitly does not inspect conditioners; it relies on that owner invariant.

**C4 — does the binder read geometry?** I independently parsed the binder's AST: `exact_geometry` is **never referenced**. `geometry` as a bare attribute name is not referenced either.

**Verdict: F8 is not transformed. No source-scope narrowing is interpreted as evidence weighting.**

**Finding C-1 (low).** `test_binding_never_touches_conditioners` claims to prove "the binding module reads no conditioner attribute" by scanning a hard-coded subset: `conditioner_bindings`, `retained_conditioner_ids`, `effective_time_or_interval`, `geometry`, `uncertainty_state`, `raw_support`, `walkback_steps`, `positive_proxy_authority_refs`. It does **not** cover F8 attributes the binder genuinely reads — I measured `algorithm_id`, `model_rule_id`, `release_ref`, `rule_hash`, `source_universe_ref`, `source_universe_refs` — so the assertion is narrower than its docstring. The property it actually needs (no geometry read) does hold and I verified it independently.

## 5. Attack D — owner-boundary integrity and law-drift: **PASS**

Covered in §1.2 (all three owners byte-identical at both commits; the court's guard executes rather than skips) and §4 C2 (the binder refuses a changed F8 algorithm id and a changed rule hash rather than silently continuing).

One structural observation: nothing in `rawlsing_next/pre553_service_source_applicability.py`, `source_backed_positioned_subject_possibility.py` or `objective_consumer_bounded_evidence.py` imports the binder, so the binder is a pure leaf dependency. If F8's law changes, the binder fails closed on `rule_hash`/`algorithm_id` rather than continuing — which is the correct direction, and is the whole point of the guard.

## 6. Attack E — authority leakage: **NO LEAKAGE FOUND**

I probed each named power through the binding's entire public surface:

| Forbidden power | Probe result |
|---|---|
| mint target-use permission | permission refs are carried as inputs, `bound_permission_refs_are_inputs_not_grants: true`; `grant_target_use_permission()` raises `BINDING_REFUSES_PERMISSION_GRANT` |
| decide currentness | default is `CURRENTNESS_NOT_REQUESTED`; `currentness_authority()` raises; a result without a claim refuses `CURRENTNESS_RESULT_WITHOUT_CLAIM`; a claim without a result refuses `CURRENTNESS_MISSING_WHEN_CLAIMED`; conflicting/missing refuses |
| infer source equivalence | no equivalence field, no equivalence method; `SOURCE_SEMANTIC_EQUIVALENCE` is a refused purpose |
| pool or deduplicate respondents | no aggregate/combined/sample-size field; `pooled_source_set()` raises; duplicate authority records are refused by the owner (`_Refusal`) |
| backfill a missing source | `BACKFILL_AUTHORITY` refused; a source outside the admitted set refuses `F8_RULE_SOURCE_OUTSIDE_ADMITTED_SET` and is never added |
| condition F8 on service state | `conditioned_f8_geometry()` raises; the binder reads no conditioner attribute (AST-verified) |
| infer actor/person state | no actor field in the material; `infer_individual_state()` raises; `ACTOR_OR_PERSON_STATE` and `PREV3_TO_V3_ACTOR_WORK` are refused purposes |

**One boundary judgement to record honestly.** `requested_currentness_claim` is a *free-form caller string* that is refused only if it is one of `CONFLICTING/UNKNOWN/MISSING/UNRESOLVED`. Any other string is accepted and becomes `currentness_result` in the material. That is not a currentness *decision* by the binder — the binder decides nothing about currency; it records a caller-supplied, self-consistent claim and refuses the negative cases — but an unconstrained caller vocabulary here is looser than the rest of the module, and no test pins the accepted vocabulary. Low severity; named for the adopting owner.

## 7. Attack F — typed refusal authenticity: **PASS**

I drove nine distinct refusal paths and classified each exception by type:

```
foreign_private_types = []
9 refusal paths, every one ServiceF8ScopeBindingError carrying .reason_code
```

The refusal surface is self-owned: `ServiceF8ScopeBindingError(Pre553IntegrityError)` with a `reason_code`, constructed only through the module's own `_refusal`. The prior worker's recorded defect #3 (leaking the adopted owner's private `_Refusal`) is genuinely fixed — the binder re-implements the coverage check directly (`if receipt.candidate_class_coverage != COVERAGE_COMPLETE: raise _refusal("APPLICABILITY_COVERAGE_INCOMPLETE", …)`) instead of translating the owner's exception. Refusals are stable and replayable: every one is reachable through a deterministic input, and the binding replay identity is permutation-invariant (§2 A1).

## 8. Attack G — court authenticity: **SUBSTANTIALLY AUTHENTIC, THREE CAVEATS**

The commission named five specific attack shapes. Results:

| Commission attack | Verdict |
|---|---|
| wrong-root skips | **FIXED and verified**: the guards now resolve the true repo root and execute; I reproduced all three owner hashes and both guards ran (no skips) |
| silent skips in write-terrain guards | **STILL PRESENT as an escape hatch** (G-3 below) |
| production-self-referential forbidden-purpose tests | **FIXED**: `PINNED_FORBIDDEN_PURPOSES` is 25 literals pinned in the court file, parametrised directly, and the court does **not** iterate the production tuple. Truncating `FORBIDDEN_BINDING_PURPOSES` would make the court fail, not collect fewer cases |
| public-API tests using `dir()` noise rather than `__all__` | **MIXED** (G-2 below) |
| tests that pass after deleting a load-bearing refusal | **NOT FOUND**: the refusal tests assert exact reason codes on exact methods, and the parametrised purpose test asserts `BINDING_POWER_NONCOLLAPSE_VIOLATION` per literal |

**The court is genuinely non-self-referential on the property that matters most.** GAP-3 is closed properly: forbidden purposes are literals in the court; "unranked" is proven by permutation invariance plus value inspection rather than by a self-declared flag; non-authorization is proven by value inspection of emitted material.

**G-1 (low) — the public-surface test is partly name-based.** `test_binding_exposes_no_ordered_or_preferring_surface` filters class attributes with `"source" in n.lower()` and asserts the remainder equals exactly the two source-touching names. That is a name-substring heuristic: a future selection-shaped method whose name does not contain "source" (e.g. `pick_best()`) would not be caught by this test. The separate `assert_binding_does_not_authorize` and reason-code tests do not cover that case either. The module-level `__all__` test is correct and airtight; this class-level one is weaker than it reads.

**G-2 (low) — one test still uses `dir()`.** Line 316 uses `dir(B.ServiceApplicabilityF8SourceScopeBinding)` on the **class**, not the module. It is deterministic (Python sorts `dir()`), and the docstring at line 774 carefully explains why the *module* test uses `__all__` instead — but the class-level enumeration is exactly the shape the commission told me to attack. It is a bounded weakness, not a false proof: the assertion is that the set equals two specific names, which is meaningful.

**G-3 (low) — the write-terrain guards silently skip.** Both `test_F8_owner_module_is_byte_unchanged_from_the_HQ208_recorded_blob` and `test_binding_does_not_modify_the_adopted_owners` call `pytest.skip(...)` when the file is absent, when `git` is unavailable, or when `hash-object` fails. In this checkout they ran and passed, so the evidence is real here — but in a sparse checkout that omits an owner file, or on a host without `git`, the guard **silently degrades to a skip** and still produces an all-green run. The worker recorded this defect family explicitly (defect #4) and fixed the root computation, but did not remove the skip path. A guard that can skip while looking green is the failure mode the candidate itself names.

**G-4 (informational) — the runtime checks vary inputs.** GAP-4 was about tautological "run it twice" checks. The court's runtime checks vary an input or assert a refusal (my C1 used two genuinely different bindings over the same evidence), so the GAP-4 lesson is honoured.

## 9. Attack H — environment classification: **CLAIM IS DISCLOSED CORRECTLY BUT NOT INDEPENDENTLY CHECKABLE HERE**

The candidate states: governed interpreter **absent**, no reconstitution performed, results from an already-existing interpreter `/var/folders/.../opencode/hq204-r9-env/bin/python` (CPython 3.11.3) whose 14-package freeze is **set-identical** to the governed `01_ENVIRONMENT_LOCK.json` at `deea40541cda0627d129dcb7d30e06e0682e0fed`, with `pyreadstat 1.3.6` held, classified **"RECONSTRUCTED-EQUIVALENT EVIDENCE, NOT GOVERNED CERTIFICATION"**.

I **cannot verify** any of the environment-identity claims from this checkout:

- `LOCAL_COURTS/qualification/r7-c4-source-free-venv` — **absent**
- the `PYAT-C4C3-DARWIN-ANCHOR-RUNTIME-R1/01_ENVIRONMENT_LOCK.json` path — **not present in this worktree** (outside sparse scope; I did not widen scope)
- the referenced interpreter path — a different host's temp directory

I re-ran the 148-test surface in my own independent venv (CPython 3.11.3, matching) and reproduced the same counts, so the **mechanical result** is independently confirmed. I explicitly **do not** relabel the candidate's environment claim as governed certification, and I do not claim mine is either.

The candidate's relevance argument is accepted on inspection: the binder is pure source-free logic over synthetic exact refs, reads no survey bytes, no file and no network, so the interpreter affects whether the harness can import and execute, not the semantics under test.

## 10. Findings

### F1 (MEDIUM, blocking) — `SINGLE_SOURCE_VALIDATION`'s requested source does not constrain evaluation

The mode exists to validate **one** exact source. The binder requires `requested_source_universe_ref` to be present and admitted, records it in the binding material and hence in the replay identity, **and then never uses it to constrain anything at evaluation time.**

Evidence. Binding made in `SINGLE_SOURCE_VALIDATION` mode with `requested_source_universe_ref = A`, over a receipt where **A and B are both admitted** and the F8 rule spans A and B:

```
single_mode_requested_source:        a
single_mode_admitted_set:            [b, a]
single_mode_evaluation_on_B:         ALLOWED  state=EXACT_SUPPORTED  result source=b
exhaustive_mode_evaluation_on_B:     ALLOWED  state=EXACT_SUPPORTED
same_result_hash (single vs exhaustive):  True
single_mode_evaluation_on_C (not admitted): REFUSED F8_QUERY_SOURCE_NOT_ADMITTED
```

Root cause: `evaluate_bound_positioned_subject_possibility` calls `binding.assert_query_source_admitted(query)`, and that method tests the **query's** source against `self.admitted_source_universe_refs` — the whole admitted set — not against the requested source. So:

- The two declared modes differ **only** in whether `expose_unranked_admitted_source_set` is gated by coverage.
- A binding labelled `SINGLE_SOURCE_VALIDATION` for A happily returns an F8 result for B.
- A refinement a caller can reasonably believe is enforced is decorative, **and no court test pins it**: the court's single-source tests assert that a *non-admitted* requested source refuses, never that a *different admitted* source is refused at evaluation.

Related, same root: a single-source binding requesting BB is accepted even when the F8 rule's `source_universe_refs` does **not** include BB (`outcome: ALLOWED`), because the rule check compares against the admitted set, not against the requested source. The requested source never has to be in the F8 rule it is bound to.

This is a **semantic gap, not an authority leak** — every source that can be evaluated is positively admitted, so no unauthorized source is used, and the narrowing never widens. But a binding whose declared refinement is inert is exactly the class of "looks like a constraint, is not one" defect this lineage has been repairing.

### F2 (MEDIUM, blocking) — "the two positive powers, and only two" is false as an API statement

`01_BINDING_CONTRACT.json` declares `positive_powers_exactly_two`, and the module docstring says "The two positive powers, exactly". The module's own `__all__` and the court's own public-surface test establish that the declared public callables are **seven**, of which **four return**:

| Public callable | Behaviour |
|---|---|
| `bind_service_applicability_to_f8_scope` | **returns** a binding |
| `assert_query_source_admitted` | returns a per-source validation mapping (power 1) |
| `expose_unranked_admitted_source_set` | returns the admitted tuple (power 2) |
| `evaluate_bound_positioned_subject_possibility` | **returns** a `PositionedSubjectPossibilityResult` — a full F8 evaluation through the binding |
| `verify_service_f8_scope_binding_replay` | **returns** the re-derived binding |
| `assert_complete_coverage_from_binding` | returns `None` (or raises) |
| `ServiceF8ScopeBindingError` | exception type |

To be precise and fair: `evaluate_bound_positioned_subject_possibility` is **not a new authority**. It delegates to the adopted F8 evaluator unchanged, which my C1 verified pixel-for-pixel on geometry and identity. The candidate's substantive statement — "no method that returns a chosen source" — is **true**, and I could not falsify it. What is false is the *counting and enumeration*: the receipt's `positive_powers_exactly_two` is the authoritative power statement a downstream adopter will read, and the declared surface actually has five returning callables, one of which performs a full F8 evaluation. Compare the commission's own framing — *"attack whether any third positive power is reachable through … helper methods, returned material, …"*. The accurate answer is: **no third power over sources is reachable; a third returning function is, and it is exported.** An enumeration that under-counts by two is a documentation defect with real adoption consequences, not an authority defect, and it should be corrected rather than argued.

### F3 (LOW) — dead cross-release provenance branch

`bind_service_applicability_to_f8_scope` handles a positive decision whose release differs from the requested release by emitting a provenance row with `bound_to_requested_release: False` and **still including the source in the admitted set**.

I verified the adopted owner makes this unreachable: `resolve_service_source_applicability` stamps **every** decision with `release_identity_ref=request.release_identity_ref`, so a receipt always presents exactly one release. Probe:

```
receipt_release:               urn:hq211:c11logicalrelease:r1
decision_releases_present:     [urn:hq211:c11logicalrelease:r1]
distinct_decision_releases:    1
```

Consequences: (a) the `False` branch is dead code that no test exercises; (b) the binder's release-grain safety therefore rests entirely on the adopted owner's single-release construction, not on its own check — which the binder's own comment overstates; (c) if the owner ever becomes per-decision-release, the `False` branch would add an off-release source to the admitted set **without** a corresponding release check on the admitted set, and the query release check would not catch it because it compares the query to the *bound* release while the admitted set carries another. Low severity today, but the branch should either be removed or made fail-closed.

### F4 (LOW) — four claim/evidence mismatches

1. **Module docstring, line 51**: "the three that are attempted-against refuse loudly". Seven refusal methods exist; the return and the receipt say seven.
2. **Module docstring, line 49**: "There is no third" — see F2.
3. **`test_binding_never_touches_conditioners`** claims to prove no conditioner/geometry attribute is read, but scans a hard-coded subset that omits six F8 attributes the binder does read. The needed property (no geometry read) holds; the stated proof is narrower than the claim.
4. **`requested_currentness_claim`** accepts any caller string outside four negative tokens, with no court test pinning the accepted vocabulary.

### F5 (LOW) — environment claim not independently checkable

Recorded in §9. Disclosed honestly by the candidate, not verifiable here, and not relabelled by me.

## 11. Bounded repair set

**Repair 1 (F1, blocking).** Make `SINGLE_SOURCE_VALIDATION` mean what it says, or remove the mode.
- *Option A (preferred, tightest):* in single-source mode, `assert_query_source_admitted` (or the evaluate path) must require the query's source to equal `requested_source_universe_ref`; add a reason code such as `F8_QUERY_SOURCE_NOT_THE_REQUESTED_SOURCE`. Also require the requested source to be present in the bound F8 rule's `source_universe_refs`.
- *Option B:* delete `SINGLE_SOURCE_VALIDATION` and `requested_source_universe_ref` and state that the binder has one mode: admission validation against the positively admitted set. Then the binding statement and the material must stop implying a single-source refinement.
Either way, add a court witness for the exact case: **single-source binding for A, evaluation attempted on B, must refuse** (today it succeeds).

**Repair 2 (F2, blocking).** Correct the power enumeration everywhere it appears — `00_RETURN.md`, `01_BINDING_CONTRACT.json` (`positive_powers_exactly_two`, `no_third_power`), `02_REFUSAL_AND_POWER_CEILING.json`, `05_FINAL_DISPOSITION.json`, and the module docstring. State the returning surface as it is: two powers over *sources* (`assert_query_source_admitted`, `expose_unranked_admitted_source_set`) plus a binding constructor, a delegating evaluator, a replay verifier and a coverage guard. If `evaluate_bound_positioned_subject_possibility` is claimed as a non-power, say explicitly that it delegates to the adopted F8 evaluator and grants nothing new — which is true and is the substantive answer.

**Repair 3 (F3, low).** Remove the `bound_to_requested_release: False` branch, or make it fail closed (refuse rather than admit an off-release positive decision). Correct the accompanying comment so the release safety is attributed to the owner invariant it actually depends on, and either add a test that pins the owner's single-release invariant or delete the branch.

**Repair 4 (F4, low).** Fix the two docstring counts; narrow the conditioner-scan claim or widen the scan to the full attribute set; pin the accepted currentness vocabulary with a test.

**Repair 5 (F5/G-3, low).** Consider making the write-terrain guards **fail** rather than **skip** when the owner file is absent, or at minimum emit an explicit non-silent mark so an all-green run cannot hide a guard that never ran.

## 12. What is genuinely achieved (do not discard)

- The binder closes the exact HQ208 gap — "no binding from CandidateClassApplicabilityReceipt/replay identity to `PositionedSubjectPossibilityModelRule.source_universe_refs` or exact query-source validation" — with one thin same-grain adapter and **no adopted-owner edit**.
- All three adopted owners are byte-identical at the candidate tip, verified independently at two commits.
- No selection, ranking, priority, preference, weight, first/best/latest/local power is reachable. Permutation invariance of both the replay identity and the exposed order is proven, not asserted.
- The COMPLETE/INCOMPLETE distinction is enforced **more strictly** than the literal commission text: set exposure requires COMPLETE in every mode, and the exact laundering attempt is refused, while single-source validation survives under INCOMPLETE.
- F8 is not transformed: identical evidence yields byte-identical geometry, unchanged conditioner ids and unchanged algorithm identity across a wide and a narrowed binding; output *selection* is correctly separated from output *transformation*.
- The law-drift guard refuses a changed F8 algorithm id and a changed rule hash rather than continuing silently.
- The refusal surface is self-owned (`ServiceF8ScopeBindingError` + `reason_code`) with no foreign private type leaking, verified across nine refusal paths.
- The court is genuinely non-self-referential on the forbidden-purpose and unranked properties, closing the prior review's GAP-2/GAP-3/GAP-4 lessons.
- 148/148 reproduces exactly, twice, including `0 skipped`.

## 13. Bound on this review

No raw source, no locator discovery, no warrant, no live C4, no C7, no actor/person work. All probes were read-only imports of the candidate module from a worktree at the exact candidate SHA; probe scripts were written outside the repository. I modified no implementation file, repaired nothing, merged nothing, and adopted nothing. The only artifacts are these five return files.

## 14. Answer to the commission, plainly

`accept_for_hq_adoption = false` until Repairs 1 and 2 are made.
`authority_overreach = false`. `selection_or_ranking_leak = false`. `f8_transformation = false`. `owner_modified = false`. `seam_closes_the_HQ208_gap = true`.
`smallest_blocking_repair = Repair 1` (make the single-source refinement binding or remove it) plus `Repair 2` (make the power enumeration true).
`environment = reconstructed-equivalent as disclosed; mechanical result independently reproduced; not relabelled as governed certification.`
