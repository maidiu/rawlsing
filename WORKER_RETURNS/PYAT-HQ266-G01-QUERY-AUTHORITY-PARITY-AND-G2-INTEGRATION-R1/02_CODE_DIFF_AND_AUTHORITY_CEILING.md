# HQ266 G01 — code diff and authority ceiling

**FINAL COMMITTED SHA:** `3829fc4e63fc9fb0d802e8af237dfab2febc3d23`
**Commission tip:** `dfab8607177e02872a2da6cfa65a6d97bed8bdda`
**Control parent:** `8d42dbbe9d8c07aa2672abd7a970bf15373fe056`

---

## 1. Edit scope — exactly the two authorized files

```
rawlsing_next/pre553_ee14_c1_owner_authenticated_ingress.py            | 829 +++++++++++---
rawlsing_next/tests/test_pre553_ee14_c1_owner_authenticated_ingress_hq262.py | 1137 ++++++++++---
2 files changed, 1701 insertions(+), 265 deletions(-)
```

`git diff --name-only <commission-tip>..HEAD` returns **exactly these two paths**.

Verified UNCHANGED (read-only) against the commission tip:

| accepted owner / original fixture | status |
|---|---|
| `rawlsing_next/pre553_service_f8_source_scope_binding.py` (G2 binder) | **UNCHANGED** |
| `rawlsing_next/pre553_service_source_applicability.py` (applicability owner) | **UNCHANGED** |
| `rawlsing_next/pre553_analytical_composition.py` (C1) | **UNCHANGED** |
| `rawlsing_next/source_backed_positioned_subject_possibility.py` (F8) | **UNCHANGED** |
| `rawlsing_next/tests/c1_at08_at13_fixture.py` (AT09 XOR fixture) | **UNCHANGED** |
| `rawlsing_next/tests/test_pre553_empirical_query.py` (`_query_authority`, `_registry`) | **UNCHANGED** |

No accepted owner edit was required, so no missing-edge HOLD was issued. No new statistical
model, no parallel binder, no new authority, no new source.

## 2. What changed in the ingress, by finding

### F1 — the scope-hash stand-in and raw-F8 bypass are removed

**Before (HQ262 candidate):**

```python
scope_hash = semantic_hash({"contract": CONTRACT, "cell": req.cell,
                            "scope": self._applicability_scope, ...})   # local stand-in
f8 = evaluate_positioned_subject_possibility(query=..., rule=..., evidence=(evidence,))
```

It never built a `CandidateClassApplicabilityReceipt`, never called
`resolve_service_source_applicability`, never supplied a
`ServiceApplicabilityF8ScopeBindingRequest`, never called
`bind_service_applicability_to_f8_scope`, and never evaluated via
`evaluate_bound_positioned_subject_possibility`.

**After (this lane):**

```python
receipt   = SA.resolve_service_source_applicability(service_request, candidate_class, records)
g2_request, binding = B.bind_service_applicability_to_f8_scope(
    request=g2_request, receipt=receipt, rule=plan.model_rule)
out = B.evaluate_bound_positioned_subject_possibility(
    binding=binding, request=g2_request, receipt=receipt,
    query=consumer_query, rule=plan.model_rule, evidence=(evidence,))   # UNCHANGED evidence
```

- `self._applicability_scope` **no longer exists** (asserted by
  `test_f1_no_locally_hashed_scope_stand_in_remains`, which greps the module source).
- The receipt field `applicability_scope_hash` is **gone**; replaced by real G2 identities:
  `g2_service_request_set_identity`, `g2_receipt_outcome`, `g2_receipt_hash`,
  `g2_binding_request_id`, `g2_binding_hash`, `g2_permission_keys`,
  `g2_query_authority_id`, `g2_query_authority_content_hash`, `g2_replay_protocol_key`.
- Bound F8 is required to equal the direct C1 result; divergence raises
  `BOUND_F8_DIRECT_C1_PARITY_FAILURE`.
- **Wiring is proved, not assumed:** monkeypatching the accepted binder to raise makes that
  exact refusal surface from `serve()` with bound-F8 count 0. A bypass would instead fall
  through silently to raw F8, which the court forbids.

### F2 — two genuinely different C1 producer queries over ONE XOR source

**Before:** `cell_inputs["q1"]` and `cell_inputs["q2"]` shared one `producer_query`,
`predicate`, `consumer_query`, witness and model rule; `cell` only entered the hash. q1 and
q2 were the same query under two labels.

**After:** each cell owns a `CellPlan` with its own `conditions`, `tag`, `stratum_ids` and
`model_rule`, and its own entry in the non-mutable owner-held expected identity:

| | q1 | q2 |
|---|---|---|
| conditions | `(("RESPONSE","A",1),)` | `(("RESPONSE","A",1),("RESPONSE","B",0))` |
| tag | `hq253-qA` | `hq253-qAB` |
| stratum | `("c0",)` | `("c0","c1")` |
| denominator | **2** | **1** |
| cells | C=0 `1`, C=1 `1` (1/2, 1/2) | C=0 `0`, C=1 `1` (0/1, 1/1) |
| producer predicate | `sha256:9bdff5e3…` | `sha256:a8b05e75…` (distinct) |
| composed identity | `e7a358b5…` | `0556d4ab…` (distinct) |

Both sit on the SAME `release_ref = REL-c1-at09-xor` and the same universe content hash
`318719f6…`, which the court asserts explicitly. Flipping a cell label is refused at the
stratum check.

### F3 — deep authentication before any F8 invocation

**Before:** `len(c1_identity) == 64`, "hash whichever evidence projection is supplied at read
time", and "check non-empty authority/provenance refs".

**After:** a field-by-field structured comparison against deeply frozen owner-held material:

```
composed_result_identity_hash, producer_predicate_key, producer_query_key,
producer_fact_key, condition_binding_witness_key, consumer_query_key,
risk_set_key, denominator_member_keys, raw_denominator_support,
evidence_ref_key, source_universe_key, release_key, evidence_state,
retained_conditioner_ids, evidence_authority_keys, evidence_provenance_keys,
target_question_key, source_universe_key_owner, release_key_owner
```

Every mismatch is reported **by field name** in `SelectedIngressAuthenticationError
.mismatched_fields`, and the error carries `f8_invoked = False`. Refusal therefore happens
before the applicability owner, the binder and F8.

This matters because the HQ253 custody false positive is still real: the court proves that
through the accepted chain, substituting only `provenance_refs` leaves
`result_hash` **unchanged**. F8 cannot detect it — which is precisely why the ingress now
does.

### F4 — typed C1 states are read for what they are

**Before:** on `possibility_slice_evidence_or_null is None` the module raised
`SelectedIngressPermissionError` saying an adopted G0b is absent, *without reading
`analytical_state` or `producer_fact_state`*.

**After:** both states are read first, checked against the accepted native empirical
fact-state vocabulary, and:

- a native negative raises `SelectedIngressC1StateError` carrying **the exact state**, with
  `f8_invoked = False` and `applicability_invoked = False`, and a message stating the
  outcome is intrinsic to C1 and **NOT a missing-EE14-G0b condition**;
- `NO_ADMITTED_SOURCE` is a separate `SelectedIngressG2Error` reason, so an applicability
  outcome can never be confused with a C1 negative;
- an out-of-vocabulary value is refused as `UNKNOWN_OR_UNRESOLVED` rather than coerced;
- `UNDERPOWERED` (a route family, not an empirical fact state) is likewise refused rather
  than silently accepted;
- `SelectedIngressPermissionError` remains a distinct type and is never what a C1 negative
  raises.

`ZERO_SUPPORT` is the one native negative genuinely constructible on this XOR source (an
unsatisfiable condition yields `analytical_state = producer_fact_state = ZERO_SUPPORT`,
denominator 0, null evidence); it maps to the `UNDERPOWERED` route family at
`pre553_analytical_state_and_route.py:86`. The remaining named states are verified as
handler-accurate rather than natively constructible on this fixture — recorded honestly in
`01_…json` under `negative_state_accounting`.

### F5 — exact builtin types and deep immutability

- `type(request) is SelectedRequest`, `type(request.cell) is str`,
  `type(request.stratum_ids) is tuple`, `type(s) is str` — subclasses of each are refused.
- `_deep_freeze` converts owner material to `MappingProxyType` / `tuple` / `frozenset`
  recursively at construction and on every `owner_scope_material()` read, so nested mutation
  raises `TypeError` instead of silently rebinding custody.
- The pinned grammar authority is verified at construction (kind, id, version, content hash,
  governed operations, three grammar families) and the forbidden `C1-AT07-QUERY`
  snapshot-style substitute is refused outright.

### F6 — hostiles that actually exercise the ingress

The previous court could not fail meaningfully: it compared an honest hash to `"0"*64`,
checked that a low-level object lacks receipt fields, and checked that a docstring contains
the word `UNPROVED`. Now: forged material is injected at the actual `serve()` boundary via a
hostile compose and refused before F8; real binder refusals surface instead of falling back
to raw F8; a self-consistent forged C1/G2 receipt is attempted and refused; and a non-vacuity
control proves the F8 counter reads 1 on the positive path, so every `== 0` assertion means
something.

## 3. Baseline preservation

All **14 original HQ262 test function names** are restored verbatim, including the original
8-case `@pytest.mark.parametrize("bad", [...])` on the non-request-shape hostile and the
2-case cell parametrization — **22 baseline collected tests, all still passing** — plus
**53 new F1–F6 tests**. Total court: **75 passed, exit 0**.

Baseline assertions changed only where the contract legitimately required it: the locally
hashed `applicability_scope_hash` field no longer exists, and the request validator now
enforces exact builtin types. No baseline test was deleted or weakened.

## 4. AUTHORITY CEILING — what this return does NOT establish

| ceiling | status |
|---|---|
| `PASS_AT_DECLARED_G1_DEVELOPMENT_GRAIN` | **NOT claimed** — author tests still require *separate independent hostile review* |
| EE14 G0b operative model-use / selected-service grant | **NOT issued** — hold `g0b` remains `UNISSUED` |
| Selected T1 service join | **NOT claimed** — hold `t1` unchanged |
| Deployment / production cutover | **NOT claimed** |
| Remote isolation or runtime remote proof | **NOT claimed** |
| Same-process arbitrary-Python adversary | **explicitly UNPROVED**, stated in the module docstring and asserted by the court |
| Exact plain builtin `SelectedRequest` under a real remote serialization boundary | data-only shape enforced in-process; a real remote boundary is **not** established here |
| Native F7 / AT07 use, V3 actor, EE12 pair | **NOT used, NOT claimed** |
| Library access, raw survey | **NOT used** |
| Current / as-of (CURRENT) certification | **NOT claimed** — `requested_currentness_claim` is `None` throughout |
| C1 provenance custody | **NOT certified** — the HQ253 custody gap is reproduced in-court, not closed at F8 |
| Self-adoption / control merge | **NOT performed** |

This candidate is `G1_INTERNAL_OWNER_PATH_CANDIDATE_ONLY`. It grants no permission, mints no
G0b, and issues no authority. Under single HQ lease, HQ may commission a separate independent
hostile review of these author tests before any adoption decision.

**TERMINAL:** `HQ266_G01_RETURNED_FOR_HQ__NO_SELF_ADOPTION`
