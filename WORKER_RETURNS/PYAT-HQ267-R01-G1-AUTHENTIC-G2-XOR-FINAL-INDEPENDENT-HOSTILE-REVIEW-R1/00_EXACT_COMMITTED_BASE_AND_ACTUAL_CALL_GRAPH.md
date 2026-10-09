# HQ267 R01 — exact committed base and actual C1→SA→G2→bound-F8 call graph

**COMMISSION:** `PYAT-HQ267-R01-G1-AUTHENTIC-G2-XOR-FINAL-INDEPENDENT-HOSTILE-REVIEW-R1`
**REVIEW BRANCH:** `agent/reviewer-pyat-hq267-g01-authentic-g2-xor-final-hostile-r1`
**EXACT REVIEW BASE:** `22d0b474c3b4d6808799f4b55c2d88313abde239` (parent of the commission tip)
**COMMISSION TIP:** `b48b5b4fb7cec83b1977aaeaeaab37ce74aba94f`
**OBJECT UNDER REVIEW:** HQ266 G01, code SHA `3829fc4e63fc9fb0d802e8af237dfab2febc3d23`,
return HEAD `bdc65ff897a8e6a61988fc2bb3a325e7f198222a`

> **READER WARNING — INDEPENDENCE.** This document was produced by the same session
> that executed the HQ266 author lane which created the code under review. It is
> therefore **not** an independent review. See `03_DISPOSITION.json`. The technical
> findings below are objective and independently re-runnable, but they cannot discharge
> the *separate independent hostile review* that G1 adoption requires.

---

## 0. Control authority resolved through origin, not a branch-local pointer

| field | value |
|---|---|
| sealed checkpoint | `20261009-PYAT-HQ267-G01-COMMITTED-G2-XOR-CORRECTION-INDEPENDENT-HOSTILE-REVIEW-R1` |
| decision | `HQD-2026-10-09-267` |
| `next_action` | `LAUNCH_HQ267_R01_INDEPENDENT_G1_FINAL_COMMITTED_G2_XOR_REVIEW_TIP_b48b5b4fb7ce__NO_AUTO_ADOPTION__SOURCE_CUSTODY_RESTORE_SEPARATE` |
| active worker row | branch `agent/reviewer-pyat-hq267-g01-authentic-g2-xor-final-hostile-r1`, `commission_tip = b48b5b4fb7ce…`, `observed_head_at_checkpoint = b48b5b4fb7ce…`, `status = ISSUED_NEEDS_HUMAN_LAUNCH` |
| grain | `FROZEN_FINAL_G01_CODE_BLOBS_STATIC_HOSTILES_F1_F6_PLUS_SEPARATE_CLEAN_COMMITTED_RUNTIME_IF_AVAILABLE` |
| `machine` (HQ) | `QUALIFIED_INDEPENDENT_PYTHON_RUNTIME_NOT_VERIFIED_BY_HQ` |
| `worktree` (HQ) | `NOT_PROVISIONED_BY_HQ` |
| hold `g0b` | `EE14_OPERATIVE_MODEL_USE_AND_SELECTED_SERVICE_GRANT_UNISSUED` — untouched |
| hold `g1` (in) | `HQ266_G01_AUTHORED_COMMITTED_F1_F6_REAL_SA_G2_XOR_OWNER_CANDIDATE__354_AUTHOR_REPORTED_GREEN__INDEPENDENT_R01_PENDING__NO_G1_ACCEPTED_ADOPTION` |

`git ls-remote origin refs/heads/agent/reviewer-pyat-hq267-…-r1` returned
`b48b5b4fb7cec83b1977aaeaeaab37ce74aba94f` — identical to the commission tip. The
active-worker row matched branch and tip exactly. No STOP condition triggered.

## 1. Exact committed base — every pinned identity re-derived

### 1.1 Ancestry

| claim | measured | verdict |
|---|---|---|
| HQ266 branch = 3 ahead / 0 behind `dfab8607177e…` | `rev-list --count` → 3 / 0 | **MATCH** |
| review base `22d0b474c` is the parent of commission tip | `tip^ = 22d0b474c3b4d6808799f4b55c2d88313abde239` | **MATCH** |
| code SHA `3829fc4e6` present | subject `HQ266 G01: restore all 22 baseline test names…` | **PRESENT** |
| return HEAD `bdc65ff89` present | subject `HQ266 G01: record the committed correction and stop for HQ` | **PRESENT** |
| `bdc65ff89` adds documentary returns only, NO code change | ingress/test blob identical at `3829fc4e6` and `bdc65ff89` | **MATCH** |

### 1.2 Blob identities (recomputed, not copied)

| object | expected | measured at `3829fc4e6` | at `bdc65ff89` |
|---|---|---|---|
| `pre553_ee14_c1_owner_authenticated_ingress.py` | `4ec0038d218a20cc92f114e28fd6c1de4ebd71f5` | `4ec0038d…` **MATCH** | `4ec0038d…` **MATCH** |
| `tests/test_pre553_ee14_c1_owner_authenticated_ingress_hq262.py` | `321e3e03415d1b980156f0ed4355216ca1f2273c` | `321e3e03…` **MATCH** | `321e3e03…` **MATCH** |

### 1.3 Accepted owners, fixture and historical witness unchanged

| path | commission-pinned blob | measured at `3829fc4e6` | verdict |
|---|---|---|---|
| `pre553_analytical_composition.py` (C1) | `604c8d591d4cc2b646e9b149cdb233fc9d69cf6b` | same | **MATCH** |
| `source_backed_positioned_subject_possibility.py` (F8) | `62e5eced47b64512f47b004e3e13a6ef3fe21de7` | same | **MATCH** |
| `pre553_service_source_applicability.py` (SA) | `3e40caca29e8c96ee1f412f919cfc7dba63f96c4` | same | **MATCH** |
| `pre553_service_f8_source_scope_binding.py` (adopted G2) | `848d2d0eedb04b792747e9d6aaa49bb39d108a2c` | same | **MATCH** |
| `tests/c1_at08_at13_fixture.py` (AT09 XOR fixture) | `0393cc8c17a313b7944b2a5287d0406d6cbe3849` | same | **MATCH** |
| HQ253 T01 witness test @ `e609be4f68c5…` | `17300a405d78820cd663618918e64bb0323f532e` | same | **MATCH** |

### 1.4 Change scope — exactly six paths, of which exactly two are code

`git diff --name-only dfab8607…bdc65ff89` → **6 paths**:

```
rawlsing_next/pre553_ee14_c1_owner_authenticated_ingress.py          (code)
rawlsing_next/tests/test_pre553_ee14_c1_owner_authenticated_ingress_hq262.py  (code)
WORKER_RETURNS/PYAT-HQ266-G01-…-R1/00_POSITIVE_CONTROL_….md
WORKER_RETURNS/PYAT-HQ266-G01-…-R1/01_CLEAN_COMMITTED_RUN_AND_HOSTILES.json
WORKER_RETURNS/PYAT-HQ266-G01-…-R1/02_CODE_DIFF_AND_AUTHORITY_CEILING.md
WORKER_RETURNS/PYAT-HQ266-G01-…-R1/03_DISPOSITION.json
```

No accepted owner, fixture, authority or other branch was mutated. **Scope claim HOLDS.**

### 1.5 Test-file baseline preservation (independently collected)

```
baseline original function names : 14 of 14 present
baseline collected tests         : 22   (2 cell-parametrized + 8 shape-parametrized + 12 single)
new F1-F6 tests                  : 53
total collected                  : 75
skip / xfail / xpass markers     : 0
duplicate test ids               : none (only the two intended parametrizations)
```

The author's `75 = 22 old + 53 new` claim is **independently confirmed at collection
level in a fresh clone**, not accepted from the author's report.

## 2. The actual call graph as read at the frozen code SHA

Every step below was read from `4ec0038d…` and confirmed live by independent counters
(`chain_calls` / `f8_calls` monkeypatch fixtures in the court, and by the reviewer's own
probe in `01_…json`).

```
OwnerOnlySelectedIngress.serve(request)                     ingress.py:432
  │
  ├─ _validate_request(request)                             ingress.py:257
  │    type(request) is SelectedRequest
  │    type(request.cell) is str ; type(request.stratum_ids) is tuple
  │    type(s) is str for every stratum id            ← F5 exact builtins
  │
  ├─ 1. _call_c1(plan)                                      ingress.py:488
  │      self._c1_compose(source=self._source,              ← OWNER-held source
  │                       qauth=self._qauth,                ← OWNER-held grammar authority
  │                       registry=self._registry,          ← OWNER-held registry
  │                       conditions=plan.conditions,       ← per-cell, owner-held
  │                       target_question=…, tag=…)
  │      → court._compose → fx.direct_condition_composition   (ORIGINAL fixture)
  │      ★ the caller supplies ONLY request.cell + stratum_ids.
  │        There is NO parameter through which source, release,
  │        query authority, registry, conditions or tag can be steered.
  │
  ├─ 2. _require_supported_c1(composed, plan)               ingress.py:511
  │      reads analytical_state AND producer_fact_state
  │      membership check against NATIVE_C1_FACT_STATES      ← F4 native vocabulary
  │      evidence is None  → SelectedIngressC1StateError(native_state=…)
  │                          with f8_invoked=False, applicability_invoked=False
  │      non-SUPPORTED     → SelectedIngressC1StateError     (zero F8)
  │      ★ SelectedIngressPermissionError is NEVER used for a C1 negative.
  │
  ├─ 3. stratum grain vs evidence.retained_conditioner_ids   ingress.py:447
  │      q1 ("c0",) / q2 ("c0","c1") — swap refused          ← F2 no label flip
  │
  ├─ 4. _authenticate(composed, evidence, req)               ingress.py:553
  │      19 structured keys compared field-by-field against
  │      non-mutable self._owner_identity[cell]              ← F3 deep auth
  │      refusal → SelectedIngressAuthenticationError(f8_invoked=False)
  │      ★ PRECEDES every F8/applicability invocation.
  │      ⚠ comparison is guarded by `if k in expected` — see finding D1.
  │
  ├─ 5. _resolve_applicability()                            ingress.py:610
  │      SA.CandidateClassBinding(...)
  │      SA.ServiceApplicabilityRequest.build(...)           ← REAL request
  │      SA.ApplicabilityAuthorityRecord(universe, decision, authority)
  │      receipt = SA.resolve_service_source_applicability(service_request,
  │                                                        candidate_class, records)
  │      admissible set empty → SelectedIngressG2Error(NO_ADMITTED_SOURCE)
  │                             (distinct type from the C1 state error)
  │
  ├─ 6. _bind_g2(receipt, plan)                             ingress.py:654
  │      B.ServiceApplicabilityF8ScopeBindingRequest(
  │          service_request_set_identity = receipt.service_request_set_identity,
  │          release_identity_ref         = self._source["release_ref"],
  │          requested_source_universe_ref = self._source["universe"].ref,
  │          bound_target_use_permission_refs = owner-held permission refs,
  │          requested_currentness_claim  = None,            ← NO fabricated CURRENT
  │          binding_mode = MODE_SINGLE_SOURCE_VALIDATION)
  │      binding = B.bind_service_applicability_to_f8_scope(request, receipt,
  │                                                         rule=plan.model_rule)
  │      ★ plan.model_rule is the SAME per-cell rule used at step 7.
  │
  ├─ 7. B.evaluate_bound_positioned_subject_possibility(     ingress.py:465
  │        binding, request=g2_request, receipt,
  │        query=consumer_query, rule=plan.model_rule,
  │        evidence=(evidence,))          ← the UNCHANGED C1 evidence object
  │      ★ NOT evaluate_positioned_subject_possibility (the raw low-level call).
  │
  ├─ 8. parity gate                                          ingress.py:470
  │      out.result_hash == direct.result_hash
  │      out.material()  == direct.material()
  │      else → SelectedIngressG2Error(BOUND_F8_DIRECT_C1_PARITY_FAILURE)
  │
  └─ 9. _build_receipt(...) → SelectedIngressReceipt         ingress.py:677
         origin_receipt_hash = semantic_hash(origin_material)
         authorizing = False                                 ← always
```

### 2.1 F1 — is the scope-hash stand-in really gone?

| check | result |
|---|---|
| literal `_applicability_scope` anywhere in the module | **ABSENT** (0 occurrences) |
| any locally hashed "scope" dict used as a substitute | **ABSENT** |
| `SA.resolve_service_source_applicability` invoked | **PRESENT**, `ingress.py:641` |
| `B.bind_service_applicability_to_f8_scope` invoked | **PRESENT**, `ingress.py:674` |
| `B.evaluate_bound_positioned_subject_possibility` invoked | **PRESENT**, `ingress.py:465` |
| raw `evaluate_positioned_subject_possibility` bypass | **ABSENT** from the module |
| independent counter: applicability ≥ 1, binder ≥ 1, evaluate ≥ 1 on a serve | **CONFIRMED** (probe P8, court `chain_calls`) |
| monkeypatching the accepted binder to raise → refusal surfaces with F8 count 0 | **CONFIRMED** (court F1 hostile) |

**F1 is genuinely corrected.** The previous candidate's scope-hash stand-in and raw-F8
bypass are structurally absent, and the chain is *proved* to run rather than asserted.

### 2.2 Source / release / permission coherence as actually built (probe P8)

| assertion | measured |
|---|---|
| G2 request release == owner source release | `REL-c1-at09-xor` **MATCH** |
| G2 request source universe == owner source universe | **MATCH** |
| G2 `service_request_set_identity` == resolved receipt identity | **MATCH** |
| G2 bound permission refs == owner-held permission refs | **MATCH** |
| `requested_currentness_claim` | `None` — **no CURRENT/as-of claim** |
| receipt outcome | `ADMISSIBLE_SOURCE_INDEXED_SET` (accepted constant) |
| receipt coverage | `COMPLETE` (accepted constant) |
| issuer inferred from test-only refs | **no** — refs are owner-held fixture material, and `authorising` is `False` |

**Coherence HOLDS.**

## 3. The genuine four-respondent XOR, independently recomputed

Recomputed by the reviewer **directly from `c1_at08_at13_fixture`**, not through the
author's assertions (probe P5):

| | q1 | q2 |
|---|---|---|
| conditions | `(("RESPONSE","A",1),)` | `(("RESPONSE","A",1),("RESPONSE","B",0))` |
| tag | `hq253-qA` | `hq253-qAB` |
| stratum | `("c0",)` | `("c0","c1")` |
| denominator | **2** | **1** |
| cells | C=0 **1**, C=1 **1** → 1/2, 1/2 | C=0 **0**, C=1 **1** → 0/1, 1/1 |
| `analytical_state` / `producer_fact_state` | `SUPPORTED` / `SUPPORTED` | `SUPPORTED` / `SUPPORTED` |
| non-null evidence | yes | yes |
| producer predicate | `urn:rawlsing:pre55:…9bdff5e3…` | `urn:rawlsing:pre55:…a8b05e75…` **DISTINCT** |
| composed identity | `e7a358b587bf6c0d…` | `0556d4abe02e650e…` **DISTINCT** |
| denominator member refs | **DISTINCT from q2** | **DISTINCT from q1** |
| release | `REL-c1-at09-xor` | `REL-c1-at09-xor` **SAME** |
| universe content hash | `318719f670e52a093…` | `318719f670e52a093…` **SAME** |

Additional independent checks:

- **q1 labelled with q2's stratum → refused** (`SelectedIngressError`), so the request
  stratum is enforced against what C1 actually retained, not merely echoed.
- Receipt assertions `r1.c1_raw_denominator_support == 2`, `r1` has 2 denominator
  members, `r2` has 1, and `r1.c1_denominator_member_keys != r2.…`.
- No staged fixture replacement: both cells compose against the single shared
  `fx.xor_fixture()` source object, one release, one universe.
- F8 parity: `out.result_hash == direct.result_hash` and `out.material() == direct.material()`
  for **both** cells (gate at `ingress.py:470`, asserted in court).

**The XOR q1/q2 identities, native denominators 2 and 1, same-respondent lineage and
F8 result parity all HOLD independently.**

## 4. Query authority — grammar, not snapshot

Measured from the object actually passed through `serve()`:

```
authority_kind            : PREDICATE_GRAMMAR
authority_id              : I03-AUTH-c1-at09-xor
authority_version         : 1.0.0
authority_content_hash    : 7fbd015d4d45c533fdb2b9e48082544f284167a7dff5713e897a112b3bc94257
governed_operations       : ('I03-OP-c1-at09-xor',)
governed_object_families  : EmpiricalFact@1.0.0, EmpiricalPredicate@1.0.0,
                             EmpiricalQuerySpec@1.0.0
```

`_verify_query_authority` (`ingress.py:379`) checks all six attributes and rejects
`C1-AT07-QUERY` by explicit deny-list (`ingress.py:383`) *before* the equality checks.
`_query_snapshot` appears **nowhere** in the ingress, and constructing with it raises
before any C1 call (court test confirmed). **The HQ265 hold cause (`AUTHORITY_QUERY_SNAPSHOT_
NOT_HQ253_GRAMMAR_AUTHORITY`) is closed at source level.**
